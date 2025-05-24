#!/usr/bin/env python3
"""
Complete 3-phase autonomous code review workflow
Execute all phases with human oversight and cost control
"""
import sys
import logging
from pathlib import Path
from datetime import datetime

from .three_phase_reviewer import ThreePhaseReviewer
from .config import LOGS_DIR

def setup_logging():
    """Setup logging for the 3-phase workflow"""
    LOGS_DIR.mkdir(exist_ok=True)
    log_file = LOGS_DIR / f"3phase_workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def run_complete_3_phase_workflow(codebase_path: str, review_goals: str = None):
    """
    Run all 3 phases of autonomous code review with human oversight
    
    Args:
        codebase_path: Path to codebase to analyze
        review_goals: Optional custom review goals
    """
    logger = setup_logging()
    
    if not review_goals:
        review_goals = "Comprehensive code review: find security vulnerabilities, performance issues, bugs, and code quality problems"
    
    logger.info("🚀 Starting 3-Phase Autonomous Code Review Workflow")
    logger.info("=" * 60)
    logger.info(f"📁 Codebase: {codebase_path}")
    logger.info(f"🎯 Goals: {review_goals}")
    
    # Initialize with CHEAP model (cost-controlled)
    logger.info("💰 Using DEVELOPMENT model (Claude 3 Haiku) for cost efficiency")
    reviewer = ThreePhaseReviewer(use_production_model=False)
    
    total_cost = 0.0
    
    try:
        # ============================================================
        # PHASE 1: AUTONOMOUS REVIEW (READ-ONLY)
        # ============================================================
        logger.info("\n🔍 PHASE 1: Autonomous Code Analysis (READ-ONLY)")
        logger.info("-" * 40)
        logger.info("Claude will analyze your code and identify issues...")
        logger.info("⚠️  NO CODE CHANGES will be made in this phase")
        
        phase1_results = reviewer.phase1_review(
            codebase_path=Path(codebase_path),
            review_goals=review_goals
        )
        
        phase1_cost = phase1_results.get('cost_estimate', 0.0)
        total_cost += phase1_cost
        
        logger.info("✅ PHASE 1 COMPLETED")
        logger.info(f"💰 Cost: ${phase1_cost:.4f}")
        logger.info(f"📄 Analysis saved to: reports/phase1_review_*.json")
        
        # ============================================================ 
        # PHASE 2: HUMAN REVIEW & APPROVAL
        # ============================================================
        logger.info("\n👤 PHASE 2: Human Review & Decision Making")
        logger.info("-" * 40)
        logger.info("Now YOU will review Claude's findings and make decisions...")
        
        phase2_results = reviewer.phase2_human_review()
        
        human_decisions = phase2_results['human_decisions']
        logger.info("✅ PHASE 2 COMPLETED")
        logger.info(f"📄 Human decisions saved to: reports/phase2_human_decisions_*.json")
        logger.info(f"👤 Reviewer: {human_decisions['human_reviewer']}")
        logger.info(f"📊 Assessment: {human_decisions['overall_assessment']}")
        logger.info(f"✋ Approved for fixes: {human_decisions['approved_for_fixes']}")
        
        # ============================================================
        # PHASE 3: APPLY FIXES (CONDITIONAL)
        # ============================================================
        if human_decisions['approved_for_fixes']:
            logger.info("\n🔧 PHASE 3: Applying Approved Fixes")
            logger.info("-" * 40)
            logger.info("Human approved fixes. Claude will now generate solutions...")
            
            phase3_results = reviewer.phase3_apply_fixes()
            
            phase3_cost = phase3_results['applied_fixes'].get('cost_estimate', 0.0)
            total_cost += phase3_cost
            
            logger.info("✅ PHASE 3 COMPLETED")
            logger.info(f"💰 Cost: ${phase3_cost:.4f}")
            logger.info(f"📄 Fixes saved to: reports/phase3_fixes_*.json")
            logger.info(f"🎯 Priority focus: {human_decisions['priority_focus']}")
            
        else:
            logger.info("\n⏹️  PHASE 3 SKIPPED")
            logger.info("-" * 40)
            logger.info("Human reviewer did not approve fixes.")
            logger.info("Review completed at Phase 2.")
        
        # ============================================================
        # FINAL SUMMARY
        # ============================================================
        logger.info("\n🎉 3-PHASE WORKFLOW COMPLETED")
        logger.info("=" * 60)
        logger.info(f"💰 Total Cost: ${total_cost:.4f}")
        logger.info(f"📁 All results saved in: reports/")
        logger.info(f"📊 View results: python src/claude4_autonomous_code_review/view_results.py")
        
        if human_decisions['approved_for_fixes']:
            logger.info("✅ Complete workflow: Analysis → Human Review → Fixes Applied")
        else:
            logger.info("✅ Safe workflow: Analysis → Human Review → No Changes Made")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\n❌ Workflow interrupted by user")
        return 1
        
    except Exception as e:
        logger.error(f"\n❌ Workflow failed: {e}")
        logger.error("Check the logs for details")
        return 1

def main():
    """CLI interface for 3-phase workflow"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="3-Phase Autonomous Code Review: Analysis → Human Review → Fixes"
    )
    
    parser.add_argument(
        "codebase_path",
        help="Path to codebase to analyze"
    )
    
    parser.add_argument(
        "--goals",
        default=None,
        help="Custom review goals (optional)"
    )
    
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run on project itself as a test"
    )
    
    args = parser.parse_args()
    
    if args.test:
        # Test on this project itself
        codebase_path = str(Path(__file__).parent)
        goals = "Review this autonomous code review system for improvements"
        print("🧪 TEST MODE: Analyzing this project itself")
    else:
        codebase_path = args.codebase_path
        goals = args.goals
    
    # Validate path
    if not Path(codebase_path).exists():
        print(f"❌ Error: Path does not exist: {codebase_path}")
        return 1
    
    # Run the complete workflow
    return run_complete_3_phase_workflow(codebase_path, goals)

if __name__ == "__main__":
    exit(main())
