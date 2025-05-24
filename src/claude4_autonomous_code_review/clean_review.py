"""
CLEAN Iterative Code Review System - Single Point of Truth
Generates both JSON (for processing) and Markdown (for humans) in reports/ folder
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add current directory for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from claude4_client import Claude4Client
from config import REPORTS_DIR
from iteration_prompts import get_iteration_prompt


class CleanIterativeReviewer:
    """
    Single, clean implementation of iterative review
    """
    
    def __init__(self, use_production_model: bool = False):
        self.client = Claude4Client(use_production_model)
        
    def run_iterative_review(
        self, 
        codebase_path: Path, 
        review_goals: str,
        max_iterations: int = 5
    ) -> Dict[str, Any]:
        """
        Run iterative review and generate both JSON and Markdown reports
        """
        print(f"🔍 ITERATIVE CODE REVIEW ({max_iterations} iterations)")
        print("=" * 50)
        print(f"📁 Path: {codebase_path}")
        print(f"🎯 Goals: {review_goals}")
        print(f"🤖 Model: {self.client.model}")
        print()
        
        codebase_path = Path(codebase_path)
        start_time = datetime.now()
        
        # Upload files for analysis
        code_files = list(codebase_path.rglob("*.py"))[:10]
        file_ids = []
        
        print(f"📤 Uploading {len(code_files)} files...")
        for code_file in code_files:
            try:
                file_id = self.client.upload_file(code_file)
                file_ids.append(file_id)
                print(f"   ✓ {code_file.name}")
            except Exception as e:
                print(f"   ✗ Failed: {code_file.name} - {e}")
        
        iterations_data = []
        
        # Run iterations
        for i in range(1, max_iterations + 1):
            focus_areas = {
                1: "Security & Critical Bugs",
                2: "Performance & Resources",
                3: "Input Validation & Data Flow", 
                4: "Error Handling & Edge Cases",
                5: "Architecture & Design",
                6: "Concurrency & Thread Safety",
                7: "Configuration & Environment",
                8: "Integration & API Security",
                9: "Business Logic & Domain Rules",
                10: "Comprehensive Risk Assessment"
            }
            
            focus = focus_areas.get(i, f"Deep Analysis {i}")
            print(f"\n=== ITERATION {i}: {focus} ===")
            
            if i == 1:
                # Initial iteration
                prompt = f"""
                {get_iteration_prompt(i, max_iterations)}
                
                REVIEW GOALS: {review_goals}
                
                You are conducting ITERATION {i} of {max_iterations} for comprehensive code review.
                
                OUTPUT FORMAT - For each issue provide:
                ## Issue: [Brief Title]
                - **Type**: [Security/Performance/Bug/Code Quality]
                - **Severity**: [Critical/High/Medium/Low]  
                - **File**: [filename]
                - **Location**: [line/function]
                - **Description**: [detailed explanation]
                - **Impact**: [what could go wrong]
                - **Recommendation**: [what should be done]
                
                Focus on {focus.lower()}.
                """
                
                message = self.client.create_analysis_message(prompt, file_ids)
            else:
                # Continuation iterations
                prompt = f"""
                {get_iteration_prompt(i, max_iterations)}
                
                This is ITERATION {i} of {max_iterations}. 
                Focus on: {focus}
                
                Continue finding NEW issues and generating review comments.
                Use the same structured format as before.
                """
                
                message = self.client.continue_autonomous_session(prompt)
            
            iteration_result = {
                "iteration": i,
                "focus": focus,
                "timestamp": datetime.now().isoformat(),
                "prompt_tokens": getattr(message.usage, 'input_tokens', 0) if hasattr(message, 'usage') else 0,
                "completion_tokens": getattr(message.usage, 'output_tokens', 0) if hasattr(message, 'usage') else 0,
                "response": str(message.content)
            }
            
            print(f"✓ Completed - {len(str(message.content))} chars")
            print(f"  Tokens: {iteration_result['prompt_tokens']} → {iteration_result['completion_tokens']}")
            
            iterations_data.append(iteration_result)
        
        # Calculate costs
        total_input_tokens = sum(iter_data.get("prompt_tokens", 0) for iter_data in iterations_data)
        total_output_tokens = sum(iter_data.get("completion_tokens", 0) for iter_data in iterations_data)
        
        if self.client.model == "claude-3-haiku-20240307":
            input_cost = (total_input_tokens / 1_000_000) * 0.25
            output_cost = (total_output_tokens / 1_000_000) * 1.25
        else:
            input_cost = (total_input_tokens / 1_000_000) * 15.0
            output_cost = (total_output_tokens / 1_000_000) * 75.0
        
        total_cost = input_cost + output_cost
        
        # Combine all analysis
        all_analysis = "\n\n".join([
            f"=== ITERATION {iter_data['iteration']}: {iter_data['focus']} ===\n{iter_data['response']}"
            for iter_data in iterations_data
        ])
        
        review_results = {
            "review_type": "iterative_focused",
            "timestamp": datetime.now().isoformat(),
            "codebase_path": str(codebase_path),
            "review_goals": review_goals,
            "max_iterations": max_iterations,
            "actual_iterations": len(iterations_data),
            "files_analyzed": [str(f) for f in code_files],
            "model_used": self.client.model,
            "iterations_detail": iterations_data,
            "comprehensive_analysis": all_analysis,
            "tokens_used": {
                "total_input": total_input_tokens,
                "total_output": total_output_tokens
            },
            "cost_estimate": total_cost,
            "duration": str(datetime.now() - start_time)
        }
        
        # Save reports - BOTH JSON AND MARKDOWN IN REPORTS FOLDER
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON Report (for processing)
        json_file = REPORTS_DIR / f"review_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(review_results, f, indent=2, ensure_ascii=False)
        
        # Markdown Report (for humans) - SAME FOLDER
        markdown_file = REPORTS_DIR / f"review_{timestamp}.md"
        markdown_content = self._generate_markdown(review_results)
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"\n✅ ITERATIVE REVIEW COMPLETED!")
        print(f"📊 Summary:")
        print(f"   - Iterations: {len(iterations_data)}/{max_iterations}")
        print(f"   - Files: {len(code_files)}")
        print(f"   - Cost: ${total_cost:.4f}")
        print(f"   - Duration: {review_results['duration']}")
        print(f"   - JSON: {json_file}")
        print(f"   - Markdown: {markdown_file}")
        
        return review_results
    
    def _generate_markdown(self, results: Dict[str, Any]) -> str:
        """Generate markdown content"""
        lines = []
        
        # Header
        lines.extend([
            "# 🔍 Iterative Code Review Report",
            "",
            f"**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            f"**Codebase:** `{Path(results['codebase_path']).name}`",
            f"**Model:** {results['model_used']}",
            f"**Iterations:** {results['actual_iterations']}/{results['max_iterations']}",
            f"**Cost:** ${results['cost_estimate']:.4f}",
            f"**Duration:** {results['duration']}",
            "",
            "---",
            "",
            "## 🎯 Review Goals",
            "",
            f"> {results['review_goals']}",
            "",
            "## 📁 Files Analyzed",
            ""
        ])
        
        # Files
        for i, file_path in enumerate(results['files_analyzed'], 1):
            lines.append(f"{i}. `{Path(file_path).name}`")
        
        lines.extend([
            "",
            "## 🔄 Iteration Summary",
            ""
        ])
        
        # Iterations
        for iteration in results['iterations_detail']:
            iter_num = iteration['iteration']
            focus = iteration['focus']
            tokens_in = iteration.get('prompt_tokens', 0)
            tokens_out = iteration.get('completion_tokens', 0)
            
            emoji = self._get_emoji(focus)
            
            lines.extend([
                f"### {emoji} Iteration {iter_num}: {focus}",
                "",
                f"**Tokens:** {tokens_in:,} input → {tokens_out:,} output",
                "",
                "<details>",
                f"<summary>View detailed findings from Iteration {iter_num}</summary>",
                "",
                "```",
                iteration['response'],
                "```",
                "",
                "</details>",
                ""
            ])
        
        # Footer
        lines.extend([
            "---",
            "",
            "## 📊 Summary",
            "",
            f"- **Total Tokens:** {results['tokens_used']['total_input']:,} input → {results['tokens_used']['total_output']:,} output",
            f"- **Total Cost:** ${results['cost_estimate']:.4f}",
            f"- **Analysis Duration:** {results['duration']}",
            "",
            f"*Report generated by Clean Iterative Code Review System*"
        ])
        
        return '\n'.join(lines)
    
    def _get_emoji(self, focus: str) -> str:
        """Get emoji for focus area"""
        focus_lower = focus.lower()
        if "security" in focus_lower: return "🔒"
        elif "performance" in focus_lower: return "⚡"
        elif "input" in focus_lower or "validation" in focus_lower: return "🔍"
        elif "error" in focus_lower: return "🐛"
        elif "architecture" in focus_lower: return "🏗️"
        elif "concurrency" in focus_lower: return "⚖️"
        elif "configuration" in focus_lower: return "⚙️"
        elif "integration" in focus_lower or "api" in focus_lower: return "🌐"
        elif "business" in focus_lower: return "💼"
        elif "comprehensive" in focus_lower: return "🎯"
        else: return "📝"


def human_review_and_apply_fixes(json_file: Path = None) -> Dict[str, Any]:
    """
    Human review of results and optional fix application
    """
    print(f"\n👤 HUMAN REVIEW & APPLY FIXES")
    print("=" * 50)
    
    # Find latest JSON if not specified
    if not json_file:
        json_files = list(REPORTS_DIR.glob("review_*.json"))
        if not json_files:
            print("❌ No review results found. Run iterative review first.")
            return {"error": "No review results"}
        json_file = max(json_files, key=lambda x: x.stat().st_mtime)
        print(f"📄 Using latest: {json_file.name}")
    
    # Load results
    with open(json_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # Show summary
    print(f"📁 Analyzed: {results['codebase_path']}")
    print(f"🎯 Goals: {results['review_goals']}")
    print(f"🔄 Iterations: {results['actual_iterations']}")
    print(f"💰 Cost: ${results['cost_estimate']:.4f}")
    print()
    
    # Show analysis preview
    analysis = results['comprehensive_analysis']
    print("📝 REVIEW FINDINGS PREVIEW:")
    print("-" * 30)
    if len(analysis) > 1000:
        print(analysis[:1000])
        print(f"... ({len(analysis) - 1000} more characters)")
    else:
        print(analysis)
    
    print()
    
    # Human decisions
    print("👤 YOUR DECISIONS:")
    print("-" * 20)
    
    decisions = {
        "timestamp": datetime.now().isoformat(),
        "reviewer_name": input("Your name: ").strip(),
        "approve_fixes": input("Generate fixes for these issues? (y/n): ").strip().lower() == 'y',
        "priority_focus": input("Priority focus (critical/high/medium/all): ").strip(),
        "notes": input("Additional notes: ").strip()
    }
    
    if not decisions['approve_fixes']:
        print("\n⏹️  FIX GENERATION NOT APPROVED")
        print("Review complete - no fixes will be generated.")
        return {"approved": False, "decisions": decisions}
    
    # Generate fixes
    print(f"\n🔧 GENERATING FIXES...")
    
    fix_prompt = f"""
    Based on the review findings below, generate specific code fixes.
    
    HUMAN APPROVAL:
    - Reviewer: {decisions['reviewer_name']}
    - Priority: {decisions['priority_focus']}
    - Notes: {decisions['notes']}
    
    FINDINGS TO ADDRESS:
    {analysis}
    
    Generate fixes in this EXACT format for each file:
    
    **File: filename.py**
    ```python
    # Complete fixed version of the code
    # Include all necessary imports
    # Fix all identified issues
    ```
    
    **File: another_file.py**
    ```python
    # Complete fixed version
    ```
    
    Focus on {decisions['priority_focus']} priority issues.
    Provide complete file contents, not just snippets.
    """
    
    # Generate fixes with new client session
    fix_client = Claude4Client()
    fix_message = fix_client.create_analysis_message(fix_prompt)
    
    # Save fix results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    fix_file = REPORTS_DIR / f"fixes_{timestamp}.json"
    
    # Extract content properly
    fix_content = str(fix_message.content)
    if hasattr(fix_message.content, 'text'):
        fix_content = fix_message.content.text
    elif isinstance(fix_message.content, list) and len(fix_message.content) > 0:
        if hasattr(fix_message.content[0], 'text'):
            fix_content = fix_message.content[0].text
    
    fix_results = {
        "original_review": json_file.name,
        "human_decisions": decisions,
        "timestamp": datetime.now().isoformat(),
        # FIXED: Correct structure that editor expects
        "applied_fixes": {
            "generated_fixes": fix_content
        }
    }
    
    with open(fix_file, 'w', encoding='utf-8') as f:
        json.dump(fix_results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ FIXES GENERATED!")
    print(f"📄 Fixes saved: {fix_file}")
    
    # Ask about applying to files
    apply_to_files = input("\nApply fixes to actual source files? (y/n): ").strip().lower() == 'y'
    
    if apply_to_files:
        from simple_file_editor import apply_fixes_to_files
        
        codebase_path = Path(results['codebase_path'])
        file_results = apply_fixes_to_files(str(fix_file), str(codebase_path))
        
        print(f"\n✅ FILES MODIFIED!")
        if 'error' in file_results:
            print(f"❌ Error: {file_results['error']}")
            if 'debug_text' in file_results:
                print("🔍 Debug output:")
                print(file_results['debug_text'])
        else:
            print(f"📁 Files changed: {len(file_results.get('files_modified', []))}")
            if file_results.get('backup_directory'):
                print(f"📦 Backups: {file_results['backup_directory']}")
    
    return {"approved": True, "decisions": decisions, "fix_file": fix_file}


def main():
    """Clean CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Clean Iterative Code Review")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Review command
    review_parser = subparsers.add_parser('review', help='Run iterative review')
    review_parser.add_argument('codebase_path', help='Path to codebase')
    review_parser.add_argument('--goals', default="Find security vulnerabilities, performance issues, bugs, and code quality problems", help='Review goals')
    review_parser.add_argument('--iterations', type=int, default=5, help='Number of iterations')
    review_parser.add_argument('--production', action='store_true', help='Use expensive model')
    
    # Apply command
    apply_parser = subparsers.add_parser('apply', help='Human review and apply fixes')
    apply_parser.add_argument('--json-file', help='Specific JSON file to use')
    
    # Complete command
    complete_parser = subparsers.add_parser('complete', help='Review then apply')
    complete_parser.add_argument('codebase_path', help='Path to codebase')
    complete_parser.add_argument('--goals', default="Find security vulnerabilities, performance issues, bugs, and code quality problems", help='Review goals')
    complete_parser.add_argument('--iterations', type=int, default=5, help='Number of iterations')
    complete_parser.add_argument('--production', action='store_true', help='Use expensive model')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'review':
            if not Path(args.codebase_path).exists():
                print(f"❌ Path not found: {args.codebase_path}")
                return 1
            
            reviewer = CleanIterativeReviewer(args.production)
            results = reviewer.run_iterative_review(
                Path(args.codebase_path),
                args.goals,
                args.iterations
            )
            
            if "error" not in results:
                print("\n➡️  Next: Run 'python clean_review.py apply' to review and apply fixes")
            
        elif args.command == 'apply':
            json_file = Path(args.json_file) if args.json_file else None
            human_review_and_apply_fixes(json_file)
        
        elif args.command == 'complete':
            if not Path(args.codebase_path).exists():
                print(f"❌ Path not found: {args.codebase_path}")
                return 1
            
            # Step 1: Review
            reviewer = CleanIterativeReviewer(args.production)
            results = reviewer.run_iterative_review(
                Path(args.codebase_path),
                args.goals,
                args.iterations
            )
            
            if "error" in results:
                return 1
            
            # Step 2: Human review and apply
            human_review_and_apply_fixes()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n❌ Interrupted")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
