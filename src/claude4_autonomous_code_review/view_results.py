"""
Simple viewer for autonomous code review results
"""
import json
import sys
from pathlib import Path

def view_latest_results():
    """View the latest autonomous code review results"""
    
    # Find the reports directory
    project_root = Path(__file__).parent.parent.parent
    reports_dir = project_root / "reports"
    
    if not reports_dir.exists():
        print("No reports directory found")
        return
    
    # Find the latest report
    json_files = list(reports_dir.glob("claude4_optimization_report_*.json"))
    if not json_files:
        print("No report files found")
        return
    
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    print(f"📊 Reading latest report: {latest_file.name}")
    print("=" * 60)
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        # Summary
        print(f"🎯 Optimization Goals: {results['optimization_goals']}")
        print(f"📁 Analyzed Path: {results['codebase_path']}")
        print(f"⏱️  Duration: {results['total_duration']}")
        print(f"💰 Cost Estimate: ${results['total_cost_estimate']:.4f}")
        print(f"🔄 Iterations: {len(results['iterations'])}")
        print()
        
        # Files analyzed
        print("📋 Files Analyzed:")
        for i, file_path in enumerate(results['uploaded_files']):
            print(f"  {i+1}. {Path(file_path).name}")
        print()
        
        # Iteration details
        print("🔍 Analysis Details:")
        print("-" * 40)
        
        for iteration in results['iterations']:
            print(f"\n📍 ITERATION {iteration['iteration']}")
            print(f"   ⏰ Time: {iteration['timestamp']}")
            print(f"   📊 Tokens: {iteration['prompt_tokens']} → {iteration['completion_tokens']}")
            
            # Show response preview
            response = iteration['response_preview']
            if len(response) > 300:
                response = response[:300] + "..."
            
            print(f"   💬 Claude's Analysis:")
            
            # Try to extract key findings
            lines = response.split('\\n')
            for line in lines[:10]:  # Show first 10 lines
                if line.strip():
                    print(f"      {line.strip()}")
            
            if len(lines) > 10:
                print(f"      ... ({len(lines)-10} more lines)")
            
            print()
        
        # Check for errors
        if 'error' in results:
            print(f"❌ Error: {results['error']}")
        else:
            print("✅ Analysis completed successfully!")
            
    except Exception as e:
        print(f"Error reading report: {e}")

if __name__ == "__main__":
    view_latest_results()
