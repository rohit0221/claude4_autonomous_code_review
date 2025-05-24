"""
Debug Script for Autonomous Code Review System
Helps diagnose issues with fix application
"""
import json
import sys
from pathlib import Path


def debug_fix_report(report_file: str):
    """
    Debug a fix report to understand its structure
    """
    print("🔍 FIX REPORT DEBUG")
    print("=" * 50)
    
    report_path = Path(report_file)
    if not report_path.exists():
        print(f"❌ Report file not found: {report_file}")
        return
    
    # Load and analyze the report
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    print(f"📄 Report file: {report_path}")
    print(f"📊 File size: {report_path.stat().st_size} bytes")
    print()
    
    # Show top-level structure
    print("📋 TOP-LEVEL KEYS:")
    for key in report.keys():
        value = report[key]
        if isinstance(value, str):
            print(f"  {key}: string[{len(value)}]")
        elif isinstance(value, dict):
            print(f"  {key}: dict[{len(value)} keys]")
        elif isinstance(value, list):
            print(f"  {key}: list[{len(value)} items]")
        else:
            print(f"  {key}: {type(value).__name__}")
    print()
    
    # Look for fixes content
    fixes_locations = []
    
    # Check direct keys
    if 'generated_fixes' in report:
        fixes_locations.append(('generated_fixes', report['generated_fixes']))
    
    # Check nested keys
    if 'applied_fixes' in report and isinstance(report['applied_fixes'], dict):
        print("📋 APPLIED_FIXES KEYS:")
        for key in report['applied_fixes'].keys():
            value = report['applied_fixes'][key]
            if isinstance(value, str):
                print(f"  {key}: string[{len(value)}]")
            else:
                print(f"  {key}: {type(value).__name__}")
        
        if 'generated_fixes' in report['applied_fixes']:
            fixes_locations.append(('applied_fixes.generated_fixes', report['applied_fixes']['generated_fixes']))
    print()
    
    # Analyze fixes content
    if fixes_locations:
        print("🔧 FIXES CONTENT ANALYSIS:")
        for location, content in fixes_locations:
            print(f"\n📍 Location: {location}")
            print(f"📊 Type: {type(content).__name__}")
            
            if isinstance(content, str):
                print(f"📊 Length: {len(content)} characters")
                print("📝 Preview (first 500 chars):")
                print("-" * 30)
                print(content[:500])
                if len(content) > 500:
                    print("... (truncated)")
                print("-" * 30)
                
                # Look for file patterns
                import re
                file_patterns = re.findall(r'\*\*\s*File:\s*([^*\n]+?)\s*\*\*', content, re.IGNORECASE)
                code_blocks = re.findall(r'```', content)
                
                print(f"🔍 Analysis:")
                print(f"  - File headers found: {len(file_patterns)}")
                if file_patterns:
                    print(f"  - Filenames: {file_patterns}")
                print(f"  - Code block markers: {len(code_blocks)}")
                print(f"  - .py mentions: {len(re.findall(r'\.py', content))}")
            
            elif isinstance(content, list):
                print(f"📊 List length: {len(content)}")
                if len(content) > 0:
                    print(f"📊 First item type: {type(content[0]).__name__}")
                    if hasattr(content[0], 'text'):
                        print("📊 First item has .text attribute")
                    elif isinstance(content[0], dict) and 'text' in content[0]:
                        print("📊 First item has 'text' key")
    else:
        print("❌ No fixes content found in report!")
        print("🔍 This explains why no fixes are being applied.")
    
    print("\n" + "=" * 50)


def debug_codebase(codebase_path: str):
    """
    Debug the codebase to see what files are available
    """
    print("🔍 CODEBASE DEBUG")
    print("=" * 50)
    
    codebase = Path(codebase_path)
    if not codebase.exists():
        print(f"❌ Codebase path not found: {codebase_path}")
        return
    
    py_files = list(codebase.glob("*.py"))
    print(f"📁 Codebase: {codebase}")
    print(f"📊 Python files found: {len(py_files)}")
    
    for i, py_file in enumerate(py_files, 1):
        print(f"  {i}. {py_file.name} ({py_file.stat().st_size} bytes)")
    
    print("\n" + "=" * 50)


def main():
    """
    Main debug function
    """
    if len(sys.argv) < 2:
        print("Debug Script for Autonomous Code Review")
        print("Usage:")
        print("  python debug_fixes.py <fix_report.json>")
        print("  python debug_fixes.py <fix_report.json> <codebase_path>")
        return
    
    report_file = sys.argv[1]
    debug_fix_report(report_file)
    
    if len(sys.argv) > 2:
        codebase_path = sys.argv[2]
        debug_codebase(codebase_path)
    
    print("\n💡 RECOMMENDATIONS:")
    print("1. Check that fix generation is working properly")
    print("2. Verify the report structure matches what the editor expects")
    print("3. Make sure filenames in fixes match actual files")
    print("4. Use the simple_file_editor.py for better debugging")


if __name__ == "__main__":
    main()
