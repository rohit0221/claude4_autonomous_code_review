#!/usr/bin/env python3
"""
Phase 2 ONLY: Human Review of Claude's Findings
"""
from three_phase_reviewer import ThreePhaseReviewer
import json
from pathlib import Path

def run_phase2():
    """Run Phase 2: Human review of Claude's findings"""
    
    print("👤 PHASE 2: Human Review")
    print("=" * 40)
    print("💰 Cost: $0 (human review only)")
    print("🔍 You will review Claude's findings from Phase 1")
    print()
    
    # Initialize reviewer
    reviewer = ThreePhaseReviewer(use_production_model=False)
    
    # Check if Phase 1 results exist
    reports_dir = Path("reports")
    if not reports_dir.exists():
        print("❌ No reports directory found")
        print("Please run phase1_only.py first")
        return 1
    
    phase1_files = list(reports_dir.glob("phase1_review_*.json"))
    if not phase1_files:
        print("❌ No Phase 1 results found")
        print("Please run phase1_only.py first")
        return 1
    
    # Use the latest Phase 1 results
    latest_phase1 = max(phase1_files, key=lambda x: x.stat().st_mtime)
    print(f"📄 Using Phase 1 results from: {latest_phase1.name}")
    print()
    
    try:
        # Run Phase 2 - this will be interactive
        print("🔍 Loading Claude's analysis for your review...")
        print()
        
        decisions = reviewer.phase2_human_review(review_file=latest_phase1)
        
        print()
        print("✅ PHASE 2 COMPLETED!")
        print("=" * 40)
        print(f"👤 Reviewer: {decisions['human_decisions']['human_reviewer']}")
        print(f"📊 Assessment: {decisions['human_decisions']['overall_assessment']}")
        print(f"✋ Approved for fixes: {decisions['human_decisions']['approved_for_fixes']}")
        print(f"🎯 Priority focus: {decisions['human_decisions']['priority_focus']}")
        print(f"📄 Decisions saved to: reports/phase2_human_decisions_*.json")
        print()
        
        if decisions['human_decisions']['approved_for_fixes']:
            print("➡️  Next: Run phase3_only.py to apply approved fixes")
        else:
            print("⏹️  Workflow complete - no fixes will be applied")
            print("   (You can re-run Phase 2 if you change your mind)")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error in Phase 2: {e}")
        return 1

if __name__ == "__main__":
    exit(run_phase2())
