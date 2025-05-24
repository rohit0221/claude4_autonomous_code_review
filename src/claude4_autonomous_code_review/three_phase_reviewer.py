"""
Three-phase autonomous code review system:
1. REVIEW: Autonomous analysis and issue identification
2. HUMAN: Human reviews and approves/rejects findings  
3. APPLY: Apply approved fixes

This separates analysis from implementation with human oversight.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

from .claude4_client import Claude4Client
from .config import REPORTS_DIR

logger = logging.getLogger(__name__)


class ThreePhaseReviewer:
    """
    Three-phase code review system with human oversight
    """
    
    def __init__(self, use_production_model: bool = False):
        self.client = Claude4Client(use_production_model)
        self.review_results = None
        self.human_decisions = None
        
    def phase1_review(self, codebase_path: Path, review_goals: str) -> Dict[str, Any]:
        """
        Phase 1: Autonomous code review and issue identification
        NO CODE CHANGES - ONLY ANALYSIS
        """
        logger.info("🔍 PHASE 1: Starting autonomous code review (READ-ONLY)")
        
        codebase_path = Path(codebase_path)
        start_time = datetime.now()
        
        # Upload files for analysis
        code_files = list(codebase_path.rglob("*.py"))[:10]
        file_ids = []
        
        logger.info(f"📁 Uploading {len(code_files)} files for review...")
        for code_file in code_files:
            try:
                file_id = self.client.upload_file(code_file)
                file_ids.append(file_id)
                logger.info(f"   ✅ {code_file.name}")
            except Exception as e:
                logger.warning(f"   ❌ Failed to upload {code_file}: {e}")
        
        # Analysis-only prompt - explicitly NO code changes
        analysis_prompt = f"""
        You are a senior code reviewer conducting a thorough code review.
        
        IMPORTANT: This is ANALYSIS ONLY - Do NOT provide code fixes or implementations.
        
        REVIEW GOALS: {review_goals}
        
        YOUR TASK:
        1. Identify all code quality issues, bugs, security vulnerabilities, and performance problems
        2. Categorize issues by severity (CRITICAL, HIGH, MEDIUM, LOW)
        3. Explain WHY each issue is problematic
        4. Suggest WHAT should be changed (not HOW to implement it)
        5. Prioritize issues by impact and difficulty
        
        CATEGORIES TO REVIEW:
        - 🔒 Security vulnerabilities (SQL injection, hardcoded secrets, etc.)
        - ⚡ Performance issues (O(n²) algorithms, memory leaks, etc.)  
        - 🐛 Bugs and error handling (exceptions, edge cases, etc.)
        - 📝 Code quality (naming, structure, maintainability, etc.)
        - 🏗️ Architecture and design patterns
        
        FORMAT YOUR RESPONSE AS:
        ## CRITICAL ISSUES
        - Issue description and location
        - Why it's problematic
        - Suggested approach to fix
        
        ## HIGH PRIORITY ISSUES  
        [same format]
        
        ## MEDIUM PRIORITY ISSUES
        [same format]
        
        ## LOW PRIORITY ISSUES
        [same format]
        
        Remember: ANALYSIS ONLY - No code implementations!
        """
        
        try:
            logger.info("🤖 Claude analyzing code...")
            message = self.client.create_analysis_message(analysis_prompt, file_ids)
            
            review_results = {
                "phase": "review",
                "timestamp": datetime.now().isoformat(),
                "codebase_path": str(codebase_path),
                "review_goals": review_goals,
                "files_analyzed": [str(f) for f in code_files],
                "model_used": self.client.model,
                "analysis": str(message.content),
                "tokens_used": {
                    "input": getattr(message.usage, 'input_tokens', 0) if hasattr(message, 'usage') else 0,
                    "output": getattr(message.usage, 'output_tokens', 0) if hasattr(message, 'usage') else 0
                },
                "cost_estimate": self._calculate_cost(message),
                "duration": str(datetime.now() - start_time)
            }
            
            # Save Phase 1 results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            phase1_file = REPORTS_DIR / f"phase1_review_{timestamp}.json"
            
            with open(phase1_file, 'w', encoding='utf-8') as f:
                json.dump(review_results, f, indent=2, ensure_ascii=False)
            
            self.review_results = review_results
            
            logger.info("✅ PHASE 1 COMPLETED")
            logger.info(f"💰 Cost: ${review_results['cost_estimate']:.4f}")
            logger.info(f"📄 Results saved: {phase1_file}")
            
            return review_results
            
        except Exception as e:
            logger.error(f"❌ Phase 1 failed: {e}")
            raise
    
    def phase2_human_review(self, review_file: Optional[Path] = None) -> Dict[str, Any]:
        """
        Phase 2: Human reviews Claude's findings and makes decisions
        """
        logger.info("👤 PHASE 2: Human review of findings")
        
        # Load review results if not already loaded
        if review_file:
            with open(review_file, 'r', encoding='utf-8') as f:
                self.review_results = json.load(f)
        
        if not self.review_results:
            raise ValueError("No review results available. Run phase1_review first.")
        
        print("=" * 60)
        print("🔍 CLAUDE'S CODE REVIEW FINDINGS")
        print("=" * 60)
        print(f"📁 Analyzed: {self.review_results['codebase_path']}")
        print(f"🎯 Goals: {self.review_results['review_goals']}")
        print(f"📊 Cost: ${self.review_results['cost_estimate']:.4f}")
        print()
        
        # Display Claude's analysis
        analysis = self.review_results['analysis']
        print("🤖 CLAUDE'S ANALYSIS:")
        print("-" * 40)
        print(analysis)
        print()
        
        # Human decision interface
        print("👤 HUMAN DECISIONS:")
        print("-" * 20)
        print("Please review Claude's findings above.")
        print()
        
        # Simple approval process
        decisions = {
            "timestamp": datetime.now().isoformat(),
            "human_reviewer": input("Your name/ID: ").strip(),
            "overall_assessment": input("Overall assessment (excellent/good/needs-work/poor): ").strip(),
            "approved_for_fixes": input("Approve findings for Phase 3 fixes? (y/n): ").strip().lower() == 'y',
            "priority_focus": input("Priority focus (critical/high/medium/all): ").strip(),
            "additional_notes": input("Additional notes: ").strip()
        }
        
        # Save human decisions
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        phase2_file = REPORTS_DIR / f"phase2_human_decisions_{timestamp}.json"
        
        combined_results = {
            "phase": "human_review", 
            "original_review": self.review_results,
            "human_decisions": decisions
        }
        
        with open(phase2_file, 'w', encoding='utf-8') as f:
            json.dump(combined_results, f, indent=2, ensure_ascii=False)
        
        self.human_decisions = decisions
        
        logger.info("✅ PHASE 2 COMPLETED")
        logger.info(f"📄 Decisions saved: {phase2_file}")
        
        return combined_results
    
    def phase3_apply_fixes(self, decisions_file: Optional[Path] = None) -> Dict[str, Any]:
        """
        Phase 3: Apply approved fixes based on human decisions
        """
        logger.info("🔧 PHASE 3: Applying approved fixes")
        
        # Load decisions if not already loaded
        if decisions_file:
            with open(decisions_file, 'r', encoding='utf-8') as f:
                combined_data = json.load(f)
                self.review_results = combined_data['original_review']
                self.human_decisions = combined_data['human_decisions']
        
        if not self.human_decisions:
            raise ValueError("No human decisions available. Run phase2_human_review first.")
        
        if not self.human_decisions['approved_for_fixes']:
            logger.info("❌ Human did not approve fixes. Stopping.")
            return {"status": "not_approved", "message": "Human reviewer did not approve fixes"}
        
        logger.info("✅ Human approved fixes. Proceeding...")
        
        # Implementation prompt based on human decisions
        implementation_prompt = f"""
        Based on the code review findings and human approval, implement the approved fixes.
        
        HUMAN DECISIONS:
        - Approved for fixes: {self.human_decisions['approved_for_fixes']}
        - Priority focus: {self.human_decisions['priority_focus']}
        - Additional notes: {self.human_decisions['additional_notes']}
        
        ORIGINAL ANALYSIS:
        {self.review_results['analysis']}
        
        YOUR TASK:
        1. Focus on {self.human_decisions['priority_focus']} priority issues
        2. Provide specific code fixes and implementations
        3. Show before/after code examples
        4. Explain what each fix accomplishes
        
        Generate concrete code improvements based on the approved review findings.
        """
        
        try:
            logger.info("🤖 Claude implementing approved fixes...")
            implementation_message = self.client.continue_autonomous_session(implementation_prompt)
            
            fix_results = {
                "phase": "apply_fixes",
                "timestamp": datetime.now().isoformat(),
                "human_approved": True,
                "priority_focus": self.human_decisions['priority_focus'],
                "implemented_fixes": str(implementation_message.content),
                "tokens_used": {
                    "input": getattr(implementation_message.usage, 'input_tokens', 0) if hasattr(implementation_message, 'usage') else 0,
                    "output": getattr(implementation_message.usage, 'output_tokens', 0) if hasattr(implementation_message, 'usage') else 0
                },
                "cost_estimate": self._calculate_cost(implementation_message)
            }
            
            # Save Phase 3 results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            phase3_file = REPORTS_DIR / f"phase3_fixes_{timestamp}.json"
            
            final_results = {
                "phase": "complete",
                "review_results": self.review_results,
                "human_decisions": self.human_decisions,
                "applied_fixes": fix_results
            }
            
            with open(phase3_file, 'w', encoding='utf-8') as f:
                json.dump(final_results, f, indent=2, ensure_ascii=False)
            
            logger.info("✅ PHASE 3 COMPLETED")
            logger.info(f"💰 Cost: ${fix_results['cost_estimate']:.4f}")
            logger.info(f"📄 Results saved: {phase3_file}")
            
            return final_results
            
        except Exception as e:
            logger.error(f"❌ Phase 3 failed: {e}")
            raise
    
    def _calculate_cost(self, message) -> float:
        """Calculate cost estimate for a message"""
        if not hasattr(message, 'usage'):
            return 0.0
        
        input_tokens = getattr(message.usage, 'input_tokens', 0)
        output_tokens = getattr(message.usage, 'output_tokens', 0)
        
        # Claude 3 Haiku pricing: $0.25/$1.25 per million tokens
        if self.client.model == "claude-3-haiku-20240307":
            input_cost = (input_tokens / 1_000_000) * 0.25
            output_cost = (output_tokens / 1_000_000) * 1.25
        else:
            # Claude 4 Opus pricing: $15/$75 per million tokens  
            input_cost = (input_tokens / 1_000_000) * 15.0
            output_cost = (output_tokens / 1_000_000) * 75.0
        
        return input_cost + output_cost
