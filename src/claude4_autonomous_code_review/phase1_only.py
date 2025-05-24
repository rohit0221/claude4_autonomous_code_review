#!/usr/bin/env python3
"""
Phase 1 ONLY: Autonomous Code Review (Read-only analysis)
"""

from claude4_autonomous_code_review.three_phase_reviewer import ThreePhaseReviewer
from pathlib import Path

def run_phase1():
    """Run Phase 1: Autonomous code analysis only"""
    
    print("🔍 PHASE 1: Autonomous Code Review")
    print("=" * 40)
    print("💰 Using CHEAP Claude 3 Haiku model")
    print("⚠️  READ-ONLY: No code changes will be made")
    print()
    
    # Initialize with cheap model
    reviewer = ThreePhaseReviewer(use_production_model=False)
    
    # Your code path
    code_path = Path("C:\\GitHub\\claude4_autonomous_code_review\\code_under_review")
    
    # Check if path exists
    if not code_path.exists():
        print(f"❌ Error: Code path does not exist: {code_path}")
        print("Please make sure the path is correct")
        return 1
    
    print(f"📁 Analyzing code at: {code_path}")
    print("🎯 Review goals: Find security vulnerabilities, bugs, performance issues, and code quality problems")
    print()
    
    try:
        # Run Phase 1
        results = reviewer.phase1_review(
            codebase_path=code_path,
            review_goals="Find security vulnerabilities, bugs, performance issues, and code quality problems"
        )
        
        print("✅ PHASE 1 COMPLETED!")
        print("=" * 40)
        print(f"💰 Cost: ${results['cost_estimate']:.4f}")
        print(f"⏱️  Duration: {results['duration']}")
        print(f"📄 Results saved to: reports/phase1_review_*.json")
        print()
        
        print("🔍 ANALYSIS PREVIEW:")
        print("-" * 30)
        analysis = results['analysis']
        if len(analysis) > 1000:
            print(analysis[:1000] + "\n... (truncated, see full report in JSON file)")
        else:
            print(analysis)
        
        print()
        print("➡️  Next: Run phase2_only.py for human review")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error in Phase 1: {e}")
        return 1

if __name__ == "__main__":
    exit(run_phase1())
