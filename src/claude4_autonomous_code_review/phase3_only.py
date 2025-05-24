#!/usr/bin/env python3
"""
Phase 3 ONLY: Apply Approved Fixes
"""
from three_phase_reviewer import ThreePhaseReviewer
from pathlib import Path

def run_phase3():
    """Run Phase 3: Apply fixes approved by human in Phase 2"""
    
    print("🔧 PHASE 3: Apply Approved Fixes")
    print("=" * 40)
    print("💰 Using CHEAP Claude 3 Haiku model")
    print("⚠️  Only runs if human approved in Phase 2")
    print()
    
    # Initialize reviewer
    reviewer = ThreePhaseReviewer(use_production_model=False)
    
    # Check if Phase 2 results exist
    reports_dir = Path("reports")
    if not reports_dir.exists():
        print("❌ No reports directory found")
        print("Please run phase1_only.py and phase2_only.py first")
        return 1
    
    phase2_files = list(reports_dir.glob("phase2_human_decisions_*.json"))
    if not phase2_files:
        print("❌ No Phase 2 results found")
        print("Please run phase2_only.py first")
        return 1
    
    # Use the latest Phase 2 results
    latest_phase2 = max(phase2_files, key=lambda x: x.stat().st_mtime)
    print(f"📄 Using Phase 2 decisions from: {latest_phase2.name}")
    print()
    
    try:
        # Run Phase 3
        print("🔍 Checking human approval...")
        
        fixes = reviewer.phase3_apply_fixes(decisions_file=latest_phase2)
        
        if fixes.get('status') == 'not_approved':
            print("⏹️  PHASE 3 SKIPPED")
            print("=" * 40)
            print("❌ Human did not approve fixes in Phase 2")
            print("   No code changes will be applied")
            print("   Re-run phase2_only.py if you want to change your decision")
            return 0
        
        print("✅ PHASE 3 COMPLETED!")
        print("=" * 40)
        print(f"💰 Cost: ${fixes['applied_fixes']['cost_estimate']:.4f}")
        print(f"🎯 Priority focus: {fixes['human_decisions']['priority_focus']}")
        print(f"📄 Fixes saved to: reports/phase3_fixes_*.json")
        print()
        
        print("🔧 FIXES PREVIEW:")
        print("-" * 30)
        implemented_fixes = fixes['applied_fixes']['implemented_fixes']
        if len(implemented_fixes) > 1000:
            print(implemented_fixes[:1000] + "\n... (truncated, see full report in JSON file)")
        else:
            print(implemented_fixes)
        
        print()
        print("🎉 ALL 3 PHASES COMPLETED!")
        print("Check the reports/ folder for complete results")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error in Phase 3: {e}")
        return 1

if __name__ == "__main__":
    exit(run_phase3())
