"""
Simple and Robust File Editor for Claude Fixes
Focuses on the most common patterns and provides clear debugging
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Any
import shutil
from datetime import datetime


class SimpleFileEditor:
    """
    Simple, robust file editor with clear debugging
    """
    
    def __init__(self, backup_original_files: bool = True):
        self.backup_original_files = backup_original_files
        self.backup_dir = None
        
    def apply_fixes_from_report(self, report_file: Path, codebase_path: Path) -> Dict[str, Any]:
        """
        Apply fixes from a report to actual source files
        """
        print(f"🔧 SIMPLE FILE EDITING")
        print("=" * 50)
        
        # Load the fix report
        with open(report_file, 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        # Find the fixes text in the report
        fixes_text = self._extract_fixes_text(report)
        
        if not fixes_text:
            print("❌ No fixes found in report")
            print("🔍 Available keys:", list(report.keys()))
            if 'applied_fixes' in report:
                print("🔍 Applied fixes keys:", list(report['applied_fixes'].keys()))
            return {"error": "No fixes in report", "report_structure": self._debug_report_structure(report)}
        
        codebase_path = Path(codebase_path)
        
        print(f"📄 Analyzing fix suggestions...")
        print(f"📊 Fix text length: {len(fixes_text)} characters")
        print(f"📊 Fix text preview: {fixes_text[:200]}...")
        
        # Create backup directory if needed
        if self.backup_original_files:
            self.backup_dir = codebase_path / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.backup_dir.mkdir(exist_ok=True)
            print(f"📁 Backup directory: {self.backup_dir}")
        
        # Parse fixes with debugging
        file_fixes = self._parse_file_fixes_with_debug(fixes_text, codebase_path)
        
        if not file_fixes:
            print("❌ No parseable fixes found")
            return {
                "error": "No parseable fixes found", 
                "debug_info": {
                    "text_length": len(fixes_text),
                    "text_preview": fixes_text[:500],
                    "file_pattern_attempts": self._debug_patterns(fixes_text)
                }
            }
        
        print(f"✅ Found fixes for {len(file_fixes)} files:")
        for file_path in file_fixes.keys():
            print(f"  - {file_path.name}")
        
        # Apply fixes file by file
        results = {
            "files_modified": [],
            "fixes_applied": [],
            "backup_directory": str(self.backup_dir) if self.backup_dir else None,
            "errors": []
        }
        
        for file_path, new_content in file_fixes.items():
            try:
                print(f"\n🔧 Processing: {file_path.name}")
                self._apply_fix_to_file(file_path, new_content, results)
            except Exception as e:
                error_msg = f"Error applying fixes to {file_path}: {e}"
                print(f"❌ {error_msg}")
                results["errors"].append(error_msg)
        
        print(f"\n✅ SIMPLE FILE EDITING COMPLETED")
        print(f"📊 Summary:")
        print(f"   - Files modified: {len(results['files_modified'])}")
        print(f"   - Errors: {len(results['errors'])}")
        if self.backup_dir:
            print(f"   - Backups saved: {self.backup_dir}")
        
        return results
    
    def _extract_fixes_text(self, report: Dict) -> str:
        """
        Extract fixes text from various possible locations
        """
        # Try multiple possible locations
        possible_paths = [
            ['applied_fixes', 'generated_fixes'],
            ['generated_fixes'],
            ['fixes'],
            ['fix_content'],
            ['content']
        ]
        
        for path in possible_paths:
            current = report
            try:
                for key in path:
                    current = current[key]
                
                # Handle different content types
                if isinstance(current, str):
                    return current
                elif isinstance(current, list) and len(current) > 0:
                    if hasattr(current[0], 'text'):
                        return current[0].text
                    elif isinstance(current[0], dict) and 'text' in current[0]:
                        return current[0]['text']
                    else:
                        return str(current[0])
                
            except (KeyError, TypeError, IndexError):
                continue
        
        return None
    
    def _debug_report_structure(self, report: Dict, max_depth: int = 2) -> Dict:
        """
        Create a debug view of the report structure
        """
        def explore_dict(d, depth=0):
            if depth > max_depth:
                return "..."
            
            result = {}
            for key, value in d.items():
                if isinstance(value, dict):
                    result[key] = explore_dict(value, depth + 1)
                elif isinstance(value, list):
                    result[key] = f"list[{len(value)}]"
                elif isinstance(value, str):
                    result[key] = f"string[{len(value)}]"
                else:
                    result[key] = str(type(value).__name__)
            return result
        
        return explore_dict(report)
    
    def _parse_file_fixes_with_debug(self, text: str, codebase_path: Path) -> Dict[Path, str]:
        """
        Parse file fixes with detailed debugging information
        """
        print("🔍 PARSING DEBUG:")
        
        # Get list of Python files in codebase
        py_files = list(codebase_path.glob("*.py"))
        print(f"  - Found {len(py_files)} Python files in codebase:")
        for f in py_files:
            print(f"    * {f.name}")
        
        file_fixes = {}
        
        # Pattern 1: **File: filename.py** followed by ```python code ```
        pattern1 = r'\*\*\s*File:\s*([^*\n]+?)\s*\*\*.*?```(?:python)?\s*\n(.*?)```'
        matches1 = re.findall(pattern1, text, re.DOTALL | re.IGNORECASE)
        print(f"  - Pattern 1 (**File: filename**): {len(matches1)} matches")
        
        for filename, code in matches1:
            filename = filename.strip()
            print(f"    * Found file reference: '{filename}'")
            
            # Try to match to actual files
            matched_file = self._find_matching_file(filename, py_files)
            if matched_file:
                file_fixes[matched_file] = code.strip()
                print(f"      ✓ Matched to: {matched_file.name}")
            else:
                print(f"      ❌ No matching file found")
        
        # Pattern 2: filename.py mentioned near code blocks
        if not file_fixes:
            print("  - Trying pattern 2: filename near code blocks")
            code_blocks = re.findall(r'```(?:python)?\s*\n(.*?)```', text, re.DOTALL)
            print(f"    * Found {len(code_blocks)} code blocks")
            
            for py_file in py_files:
                # Look for mentions of this filename
                if py_file.name in text:
                    print(f"    * File {py_file.name} mentioned in text")
                    # Find closest code block
                    file_pos = text.find(py_file.name)
                    
                    closest_code = None
                    min_distance = float('inf')
                    
                    for match in re.finditer(r'```(?:python)?\s*\n(.*?)```', text, re.DOTALL):
                        distance = abs(file_pos - match.start())
                        if distance < min_distance:
                            min_distance = distance
                            closest_code = match.group(1).strip()
                    
                    if closest_code and min_distance < 1000:  # Within 1000 chars
                        file_fixes[py_file] = closest_code
                        print(f"      ✓ Matched to nearby code block (distance: {min_distance})")
        
        # Pattern 3: If we have same number of files and code blocks, match by position
        if not file_fixes:
            print("  - Trying pattern 3: positional matching")
            code_blocks = re.findall(r'```(?:python)?\s*\n(.*?)```', text, re.DOTALL)
            
            if len(code_blocks) == len(py_files):
                print(f"    * Equal numbers: {len(code_blocks)} blocks, {len(py_files)} files")
                for i, py_file in enumerate(sorted(py_files, key=lambda x: x.name)):
                    file_fixes[py_file] = code_blocks[i].strip()
                    print(f"      ✓ Position {i}: {py_file.name}")
        
        return file_fixes
    
    def _find_matching_file(self, filename: str, py_files: List[Path]) -> Path:
        """
        Find the best matching file for a given filename
        """
        filename = filename.strip()
        
        # Clean up filename - remove common prefixes
        clean_filename = re.sub(r'^(?:file_\d+_)?', '', filename)
        
        # Direct matches
        for py_file in py_files:
            if py_file.name == clean_filename:
                return py_file
            if py_file.name == filename:
                return py_file
        
        # Partial matches
        for py_file in py_files:
            if clean_filename in py_file.name or py_file.name in clean_filename:
                return py_file
        
        # Add .py if missing
        if not clean_filename.endswith('.py'):
            clean_filename += '.py'
            for py_file in py_files:
                if py_file.name == clean_filename:
                    return py_file
        
        return None
    
    def _debug_patterns(self, text: str) -> Dict[str, int]:
        """
        Debug information about pattern matching attempts
        """
        return {
            "file_headers": len(re.findall(r'\*\*\s*File:', text, re.IGNORECASE)),
            "code_blocks": len(re.findall(r'```', text)),
            "python_mentions": len(re.findall(r'\.py', text)),
            "text_length": len(text)
        }
    
    def _apply_fix_to_file(self, file_path: Path, new_content: str, results: Dict):
        """
        Apply fix to a specific file
        """
        # Backup original file
        if self.backup_original_files and self.backup_dir:
            backup_path = self.backup_dir / file_path.name
            shutil.copy2(file_path, backup_path)
            print(f"  📁 Backed up to: {backup_path}")
        
        # Read original content for comparison
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Clean up the new content
        new_content = new_content.strip()
        
        # Show content preview
        print(f"  📊 Original: {len(original_content)} chars")
        print(f"  📊 New: {len(new_content)} chars")
        print(f"  📊 Preview: {new_content[:100]}...")
        
        # Write the new content
        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            results["files_modified"].append(str(file_path))
            results["fixes_applied"].append(f"Applied fix to {file_path.name}")
            print(f"  ✅ File updated")
        else:
            print(f"  ℹ️  No changes needed")


def apply_fixes_to_files(report_file: str, codebase_path: str):
    """
    Main function using the simple editor
    """
    editor = SimpleFileEditor(backup_original_files=True)
    
    results = editor.apply_fixes_from_report(
        Path(report_file),
        Path(codebase_path)
    )
    
    return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2:
        report_file = sys.argv[1]
        codebase_path = sys.argv[2]
        
        apply_fixes_to_files(report_file, codebase_path)
    else:
        print("Usage: python simple_file_editor.py <report_file> <codebase_path>")
