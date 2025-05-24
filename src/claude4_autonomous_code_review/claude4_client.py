"""
Clean Claude 4 Client for Iterative Code Reviews Only
"""
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

import anthropic
from anthropic import Anthropic
from anthropic.types import Message, MessageParam

from config import (
    ANTHROPIC_API_KEY, DEVELOPMENT_MODEL, PRODUCTION_MODEL,
    MAX_TOKENS, TEMPERATURE
)

logger = logging.getLogger(__name__)


class Claude4Client:
    """
    Streamlined Claude 4 client for iterative code reviews
    """
    
    def __init__(self, use_production_model: bool = False):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = PRODUCTION_MODEL if use_production_model else DEVELOPMENT_MODEL
        self.session_context: List[MessageParam] = []
        self.uploaded_files: Dict[str, str] = {}
        
        logger.info(f"Initialized Claude4Client with model: {self.model}")
    
    def upload_file(self, file_path: Union[str, Path]) -> str:
        """
        Upload file for analysis context
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        file_id = f"file_{len(self.uploaded_files)}_{file_path.name}"
        self.uploaded_files[file_id] = content
        
        logger.info(f"Uploaded file: {file_path.name} -> {file_id}")
        return file_id
    
    def create_analysis_message(
        self,
        task_description: str,
        file_references: Optional[List[str]] = None
    ) -> Message:
        """
        Create initial analysis message with file context
        """
        # Build context with uploaded files
        context_parts = [task_description]
        
        if file_references:
            for file_id in file_references:
                if file_id in self.uploaded_files:
                    context_parts.append(f"\n--- File: {file_id} ---\n")
                    context_parts.append(self.uploaded_files[file_id])
        
        full_context = "\n".join(context_parts)
        
        # Create message
        message = self.client.messages.create(
            model=self.model,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[
                {
                    "role": "user",
                    "content": full_context
                }
            ]
        )
        
        # Store in session context for conversation continuity
        self.session_context.extend([
            {"role": "user", "content": full_context},
            {"role": "assistant", "content": message.content}
        ])
        
        return message
    
    def continue_autonomous_session(self, additional_instruction: str) -> Message:
        """
        Continue the iterative session with new instruction
        """
        if not self.session_context:
            raise ValueError("No session context available. Start with create_analysis_message first.")
        
        # Add the continuation instruction
        self.session_context.append({
            "role": "user", 
            "content": additional_instruction
        })
        
        message = self.client.messages.create(
            model=self.model,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=self.session_context
        )
        
        # Update session context
        self.session_context.append({
            "role": "assistant",
            "content": message.content
        })
        
        return message
