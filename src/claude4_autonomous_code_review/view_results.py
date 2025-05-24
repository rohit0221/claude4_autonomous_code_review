"""
Clean Results Viewer for the simplified system
"""
import json
import sys
from pathlib import Path

def view_latest_results():
    """View the latest review results"""
    
    # Find the reports directory
    project_root = Path(__file__).parent.parent.parent
    reports_dir = project_root / "reports"
    
    if not reports_dir.exists():
        print("❌ No reports directory found")
        return
    
    # Find the latest review
    json_files = list(reports_dir.glob("review_*.json"))
    if not json_files:
        print("❌ No review reports found")
        return
    
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    print(f"📊 Latest review: {latest_file.name}")
    print("=" * 60)
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        # Review summary
        print(f"🎯 Review Goals: {results['review_goals']}")
        print(f"📁 Analyzed Path: {results['codebase_path']}")
        print(f"⏱️  Duration: {results['duration']}")
        print(f"💰 Cost: ${results['cost_estimate']:.4f}")
        print(f"🔄 Iterations: {results['actual_iterations']}/{results['max_iterations']}")
        print(f"🤖 Model: {results['model_used']}")
        print()
        
        # Files analyzed
        print("📋 Files Analyzed:")
        for i, file_path in enumerate(results['files_analyzed']):
            print(f"  {i+1}. {Path(file_path).name}")
        print()
        
        # Check for markdown report
        markdown_file = latest_file.with_suffix('.md')
        if markdown_file.exists():
            print(f"📄 Markdown Report: {markdown_file}")
        
        # Iteration summary
        print("🔍 Iteration Summary:")
        print("-" * 40)
        
        iterations = results.get('iterations_detail', [])
        for iteration in iterations:
            iter_num = iteration['iteration']
            focus = iteration['focus']
            tokens_in = iteration.get('prompt_tokens', 0)
            tokens_out = iteration.get('completion_tokens', 0)
            
            print(f"\n📍 ITERATION {iter_num}: {focus}")
            print(f"   📊 Tokens: {tokens_in:,} → {tokens_out:,}")
            
            # Show brief preview
            response = iteration.get('response', '')
            if response:
                preview = response[:200].replace('\n', ' ')
                print(f"   💬 Preview: {preview}...")
        
        print("\n✅ Review completed successfully!")
        print(f"📄 JSON Report: {latest_file}")
        if markdown_file.exists():
            print(f"📄 Markdown Report: {markdown_file}")
        
    except Exception as e:
        print(f"❌ Error reading report: {e}")

def list_all_reports():
    """List all available reports"""
    project_root = Path(__file__).parent.parent.parent
    reports_dir = project_root / "reports"
    
    if not reports_dir.exists():
        print("❌ No reports directory found")
        return
    
    json_files = list(reports_dir.glob("review_*.json"))
    if not json_files:
        print("❌ No reports found")
        return
    
    print("📁 Available Reports:")
    print("-" * 40)
    
    # Sort by modification time (newest first)
    sorted_files = sorted(json_files, key=lambda x: x.stat().st_mtime, reverse=True)
    
    for i, file_path in enumerate(sorted_files):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"{i+1}. {file_path.name}")
            print(f"   📅 {data.get('timestamp', 'Unknown time')}")
            print(f"   🔄 {data.get('actual_iterations', '?')} iterations")
            print(f"   💰 ${data.get('cost_estimate', 0):.4f}")
            print(f"   📁 {Path(data.get('codebase_path', '')).name}")
            
            # Check for markdown
            markdown_file = file_path.with_suffix('.md')
            if markdown_file.exists():
                print(f"   📄 Markdown available")
            
            print()
        except:
            print(f"{i+1}. {file_path.name} (corrupted)")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        list_all_reports()
    else:
        view_latest_results()
