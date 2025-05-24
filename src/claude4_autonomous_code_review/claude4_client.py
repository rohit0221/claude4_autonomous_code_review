"""
Claude 4 Client wrapper following Anthropic SDK patterns
"""
import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from datetime import datetime

import anthropic
from anthropic import Anthropic, AsyncAnthropic
from anthropic.types import Message, MessageParam

from .config import (
    ANTHROPIC_API_KEY, DEVELOPMENT_MODEL, PRODUCTION_MODEL,
    MAX_TOKENS, TEMPERATURE, MAX_ITERATIONS
)

logger = logging.getLogger(__name__)


class Claude4Client:
    """
    Claude 4 client that demonstrates new autonomous capabilities:
    - Files API for codebase context
    - Code execution tool
    - Extended thinking with tool use
    - Prompt caching for long sessions
    """
    
    def __init__(self, use_production_model: bool = False):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = PRODUCTION_MODEL if use_production_model else DEVELOPMENT_MODEL
        self.use_production_features = use_production_model
        self.session_context: List[MessageParam] = []
        self.uploaded_files: Dict[str, str] = {}
        
        logger.info(f"Initialized Claude4Client with model: {self.model}")
    
    def upload_file(self, file_path: Union[str, Path]) -> str:
        """
        Upload file using Files API for persistent context
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # For development, we'll read and include content directly
        # In production, use the actual Files API
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
        Create a message for autonomous code analysis
        """
        # Build context with uploaded files
        context_parts = [task_description]
        
        if file_references:
            for file_id in file_references:
                if file_id in self.uploaded_files:
                    context_parts.append(f"\n--- File: {file_id} ---\n")
                    context_parts.append(self.uploaded_files[file_id])
        
        full_context = "\n".join(context_parts)
        
        # Create message following Anthropic SDK patterns
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
            # Note: Removing tools parameter entirely for development model
        )
        
        # Store in session context for conversation continuity
        self.session_context.extend([
            {"role": "user", "content": full_context},
            {"role": "assistant", "content": message.content}
        ])
        
        return message
    
    def continue_autonomous_session(
        self,
        additional_instruction: str = "Continue your analysis and optimization work."
    ) -> Message:
        """
        Continue the autonomous session with cached context
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
            # Note: Removing tools parameter entirely for development model
        )
        
        # Update session context
        self.session_context.append({
            "role": "assistant",
            "content": message.content
        })
        
        return message
    
    def run_autonomous_code_review(
        self,
        codebase_path: Union[str, Path],
        review_goals: str,
        max_iterations: int = MAX_ITERATIONS
    ) -> Dict[str, Any]:
        """
        Run autonomous code review session (REVIEW ONLY - no code changes)
        """
        codebase_path = Path(codebase_path)
        start_time = datetime.now()
        results = {
            "start_time": start_time.isoformat(),
            "codebase_path": str(codebase_path),
            "review_goals": review_goals,
            "iterations": [],
            "uploaded_files": [],
            "total_cost_estimate": 0.0
        }
        
        logger.info(f"Starting autonomous code review of: {codebase_path}")
        
        # Upload relevant code files
        code_files = list(codebase_path.rglob("*.py"))[:10]  # Limit for demo
        file_ids = []
        
        for code_file in code_files:
            try:
                file_id = self.upload_file(code_file)
                file_ids.append(file_id)
                results["uploaded_files"].append(str(code_file))
            except Exception as e:
                logger.warning(f"Failed to upload {code_file}: {e}")
        
        # Initial analysis - REVIEW ONLY, NO RECTIFICATION
        initial_prompt = f"""
        You are Claude conducting an autonomous CODE REVIEW ONLY.
        
        IMPORTANT: You are in REVIEW MODE - identify issues but DO NOT modify any code.
        
        TASK: Conduct a thorough code review of the provided codebase with these goals:
        {review_goals}
        
        REVIEW WORKFLOW:
        1. Analyze code structure, patterns, and architecture
        2. Identify bugs, security vulnerabilities, and performance issues
        3. Document code quality problems and violations of best practices
        4. Prioritize findings by severity (Critical, High, Medium, Low)
        5. Continue your review to find additional issues
        
        OUTPUT FORMAT:
        For each issue found, provide:
        - Issue Type: [Security/Performance/Bug/Code Quality]
        - Severity: [Critical/High/Medium/Low]
        - File: [filename]
        - Line/Function: [location]
        - Description: [detailed explanation]
        - Impact: [what could go wrong]
        - Recommendation: [what should be done - but don't implement it]
        
        REMEMBER: This is a REVIEW ONLY. Do not provide actual code fixes or implementations.
        Focus on identifying and documenting issues for human review.
        """
        
        try:
            # Start autonomous session
            logger.info("=== ITERATION 1: Starting Initial Analysis ===")
            logger.info(f"Analyzing {len(file_ids)} files with prompt: {initial_prompt[:100]}...")
            
            message = self.create_analysis_message(initial_prompt, file_ids)
            
            iteration_result = {
                "iteration": 1,
                "timestamp": datetime.now().isoformat(),
                "prompt_tokens": getattr(message.usage, 'input_tokens', 0) if hasattr(message, 'usage') else 0,
                "completion_tokens": getattr(message.usage, 'output_tokens', 0) if hasattr(message, 'usage') else 0,
                "response_preview": str(message.content)[:500] + "..." if len(str(message.content)) > 500 else str(message.content)
            }
            
            logger.info(f"ITERATION 1 COMPLETED - Response length: {len(str(message.content))} chars")
            logger.info(f"TOKENS USED: {iteration_result['prompt_tokens']} input, {iteration_result['completion_tokens']} output")
            logger.info(f"ANALYSIS PREVIEW: {str(message.content)[:200]}...")
            
            results["iterations"].append(iteration_result)
            
            # Continue autonomous iterations
            for i in range(2, max_iterations + 1):
                try:
                    logger.info(f"=== ITERATION {i}: Continuing Review ===")
                    continuation_message = self.continue_autonomous_session(
                        "Continue your code review. Find more issues and document them clearly. Remember: REVIEW ONLY - do not provide code implementations."
                    )
                    
                    iteration_result = {
                        "iteration": i,
                        "timestamp": datetime.now().isoformat(),
                        "prompt_tokens": getattr(continuation_message.usage, 'input_tokens', 0) if hasattr(continuation_message, 'usage') else 0,
                        "completion_tokens": getattr(continuation_message.usage, 'output_tokens', 0) if hasattr(continuation_message, 'usage') else 0,
                        "response_preview": str(continuation_message.content)[:500] + "..." if len(str(continuation_message.content)) > 500 else str(continuation_message.content)
                    }
                    
                    logger.info(f"ITERATION {i} COMPLETED - Response length: {len(str(continuation_message.content))} chars")
                    logger.info(f"TOKENS: {iteration_result['prompt_tokens']} input, {iteration_result['completion_tokens']} output")
                    
                    results["iterations"].append(iteration_result)
                    
                    # Basic stopping condition (can be enhanced)
                    if "review complete" in str(continuation_message.content).lower() or "no more issues" in str(continuation_message.content).lower():
                        logger.info(f"Code review completed after {i} iterations")
                        break
                        
                except Exception as e:
                    logger.error(f"Error in iteration {i}: {e}")
                    break
        
        except Exception as e:
            logger.error(f"Error in autonomous optimization: {e}")
            results["error"] = str(e)
        
        # Calculate total cost estimate
        total_input_tokens = sum(iter_result.get("prompt_tokens", 0) for iter_result in results["iterations"])
        total_output_tokens = sum(iter_result.get("completion_tokens", 0) for iter_result in results["iterations"])
        
        # Cost calculation (for Claude 3 Haiku: $0.25/$1.25 per million tokens)
        if self.model == DEVELOPMENT_MODEL:
            input_cost = (total_input_tokens / 1_000_000) * 0.25
            output_cost = (total_output_tokens / 1_000_000) * 1.25
        else:
            # Claude 4 Opus: $15/$75 per million tokens
            input_cost = (total_input_tokens / 1_000_000) * 15.0
            output_cost = (total_output_tokens / 1_000_000) * 75.0
        
        results["total_cost_estimate"] = input_cost + output_cost
        results["end_time"] = datetime.now().isoformat()
        results["total_duration"] = str(datetime.now() - start_time)
        
        logger.info(f"Autonomous code review completed. Cost estimate: ${results['total_cost_estimate']:.4f}")
        
        return results
