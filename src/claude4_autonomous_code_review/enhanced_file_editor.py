"""
Fixed Enhanced File Editor with Correct Regex Patterns
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple
import shutil
from datetime import datetime


class EnhancedCodeFileEditor:
    """
    Enhanced editor that can parse Claude's fix suggestions in various formats
    """
    
    def __init__(self, backup_original_files: bool = True):
        self.backup_original_files = backup_original_files
        self.backup_dir = None
        
    def apply_fixes_from_report(self, report_file: Path, codebase_path: Path) -> Dict[str, Any]:
        """
        Apply fixes from a Step 2 report to actual source files
        """
        print(f"🔧 ENHANCED FILE EDITING")
        print("=" * 50)
        
        # Load the fix report
        with open(report_file, 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        # FIXED: Check for the correct structure
        fixes_text = None
        if 'applied_fixes' in report and 'generated_fixes' in report['applied_fixes']:
            fixes_text = report['applied_fixes']['generated_fixes']
        elif 'generated_fixes' in report:
            # Fallback for old structure
            fixes_text = report['generated_fixes']
        
        if not fixes_text:
            print("❌ No fixes found in report")
            print("🔍 Available keys:", list(report.keys()))
            return {"error": "No fixes in report", "available_keys": list(report.keys())}
        
        # Extract text from TextBlock if needed
        if isinstance(fixes_text, list) and len(fixes_text) > 0:
            if hasattr(fixes_text[0], 'text'):
                fixes_text = fixes_text[0].text
            elif isinstance(fixes_text[0], dict) and 'text' in fixes_text[0]:
                fixes_text = fixes_text[0]['text']
        elif str(fixes_text).startswith('[TextBlock('):
            # Parse TextBlock string format
            import ast
            try:
                # Extract text content from TextBlock representation
                text_start = fixes_text.find("text='") + 6
                text_end = fixes_text.rfind("')]")
                if text_start > 5 and text_end > text_start:
                    fixes_text = fixes_text[text_start:text_end]
                    # Unescape the text
                    fixes_text = fixes_text.replace('\\n', '\n').replace('\\t', '\t').replace("\\'", "'")
            except:
                pass
        
        codebase_path = Path(codebase_path)
        
        print(f"📄 Analyzing fix suggestions...")
        print(f"📊 Fix text length: {len(fixes_text)} characters")
        
        # Create backup directory if needed
        if self.backup_original_files:
            self.backup_dir = codebase_path / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.backup_dir.mkdir(exist_ok=True)
            print(f"📁 Backup directory: {self.backup_dir}")
        
        # Enhanced parsing with multiple strategies
        file_fixes = self._enhanced_parse_fixes(fixes_text, codebase_path)
        
        if not file_fixes:
            print("❌ No parseable fixes found")
            print("🔍 Debug: First 1000 chars of fix content:")
            print("-" * 50)
            print(fixes_text[:1000])
            print("-" * 50)
            return {"error": "No parseable fixes found", "debug_text": fixes_text[:1000]}
        
        print(f"✅ Found fixes for {len(file_fixes)} files")
        
        # Apply fixes file by file
        results = {
            "files_modified": [],
            "fixes_applied": [],
            "backup_directory": str(self.backup_dir) if self.backup_dir else None,
            "errors": [],
            "debug_info": {
                "total_files_detected": len(file_fixes),
                "parsing_method": "enhanced"
            }
        }
        
        for file_path, fixes in file_fixes.items():
            try:
                print(f"\n🔧 Processing: {file_path.name}")
                self._apply_fixes_to_file(file_path, fixes, results)
            except Exception as e:
                error_msg = f"Error applying fixes to {file_path}: {e}"
                print(f"❌ {error_msg}")
                results["errors"].append(error_msg)
        
        print(f"\n✅ ENHANCED FILE EDITING COMPLETED")
        print(f"📊 Summary:")
        print(f"   - Files detected: {results['debug_info']['total_files_detected']}")
        print(f"   - Files modified: {len(results['files_modified'])}")
        print(f"   - Fixes applied: {len(results['fixes_applied'])}")
        print(f"   - Errors: {len(results['errors'])}")
        if self.backup_dir:
            print(f"   - Backups saved: {self.backup_dir}")
        
        return results
    
    def _enhanced_parse_fixes(self, fixes_text: str, codebase_path: Path) -> Dict[Path, List[Dict]]:
        """
        Enhanced parsing with multiple strategies to extract fixes
        """
        file_fixes = {}
        
        # Strategy 1: Look for explicit file headers like "**File: filename.py**"
        file_fixes.update(self._parse_explicit_file_headers(fixes_text, codebase_path))
        
        # Strategy 2: Look for filename mentions with code blocks
        file_fixes.update(self._parse_filename_with_codeblocks(fixes_text, codebase_path))
        
        # Strategy 3: Look for function/class fixes and match to files
        file_fixes.update(self._parse_function_fixes(fixes_text, codebase_path))
        
        # Strategy 4: Look for "In file X" or "File X contains" patterns
        file_fixes.update(self._parse_file_mentions(fixes_text, codebase_path))
        
        return file_fixes
    
    def _parse_explicit_file_headers(self, text: str, codebase_path: Path) -> Dict[Path, List[Dict]]:
        """
        Parse explicit file headers like **File: filename.py**
        """
        file_fixes = {}
        
        # Pattern: **File: filename.py** followed by code block
        pattern = r'\*\*\s*File:\s*([^*]+?)\s*\*\*\s*```(?:python)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
        
        for filename, code in matches:
            filename = filename.strip()
            # Remove any file_X_ prefix that Claude might add
            clean_filename = re.sub(r'^file_\d+_', '', filename)
            
            file_path = codebase_path / clean_filename
            if file_path.exists():
                if file_path not in file_fixes:
                    file_fixes[file_path] = []
                
                file_fixes[file_path].append({
                    "type": "code_replacement",
                    "new_code": code.strip(),
                    "description": f"Fix from explicit header for {clean_filename}",
                    "method": "explicit_header"
                })
        
        return file_fixes
    
    def _parse_filename_with_codeblocks(self, text: str, codebase_path: Path) -> Dict[Path, List[Dict]]:
        """
        Find filenames mentioned near code blocks
        """
        file_fixes = {}
        
        # Find all Python files in the codebase
        py_files = list(codebase_path.glob("*.py"))
        
        for py_file in py_files:
            filename = py_file.name
            
            # Look for mentions of this file near code blocks
            file_pattern = re.escape(filename)
            
            # Find all positions where the file is mentioned
            file_mentions = []
            for match in re.finditer(file_pattern, text, re.IGNORECASE):
                file_mentions.append(match.start())
            
            if not file_mentions:
                continue
            
            # Find all code blocks
            code_blocks = []
            for match in re.finditer(r'```(?:python)?\n(.*?)```', text, re.DOTALL):
                code_blocks.append((match.start(), match.end(), match.group(1).strip()))
            
            # Match file mentions to nearby code blocks
            for file_pos in file_mentions:
                for code_start, code_end, code in code_blocks:
                    # If file mention is within 500 chars of code block
                    if abs(file_pos - code_start) < 500:
                        if py_file not in file_fixes:
                            file_fixes[py_file] = []
                        
                        file_fixes[py_file].append({
                            "type": "code_replacement",
                            "new_code": code,
                            "description": f"Fix near filename mention for {filename}",
                            "method": "filename_proximity"
                        })
                        break
        
        return file_fixes
    
    def _parse_function_fixes(self, text: str, codebase_path: Path) -> Dict[Path, List[Dict]]:
        """
        Parse function-specific fixes and match to files containing those functions
        """
        file_fixes = {}
        
        # Find function definitions in code blocks
        code_blocks = re.findall(r'```(?:python)?\n(.*?)```', text, re.DOTALL)
        
        for code in code_blocks:
            # Find function names in the code
            func_matches = re.findall(r'def\s+(\w+)\s*\(', code)
            class_matches = re.findall(r'class\s+(\w+)\s*[\(:]', code)
            
            all_names = func_matches + class_matches
            
            for name in all_names:
                # Find which files contain this function/class
                matching_files = self._find_files_with_name(name, codebase_path)
                
                for file_path in matching_files:
                    if file_path not in file_fixes:
                        file_fixes[file_path] = []
                    
                    file_fixes[file_path].append({
                        "type": "function_replacement",
                        "new_code": code.strip(),
                        "target_name": name,
                        "description": f"Fix for {name} in {file_path.name}",
                        "method": "function_matching"
                    })
        
        return file_fixes
    
    def _parse_file_mentions(self, text: str, codebase_path: Path) -> Dict[Path, List[Dict]]:
        """
        Parse patterns like "In file X" or "File X contains"
        """
        file_fixes = {}
        
        # Patterns for file mentions
        patterns = [
            r'(?:In|File)\s+([\w_]+\.py)[^\n]*?```(?:python)?\n(.*?)```',
            r'([\w_]+\.py)[^\n]*?(?:should be|needs to be|fix)[^\n]*?```(?:python)?\n(.*?)```',
            r'(?:Fix for|Update)\s+([\w_]+\.py)[^\n]*?```(?:python)?\n(.*?)```'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            
            for filename, code in matches:
                file_path = codebase_path / filename
                if file_path.exists():
                    if file_path not in file_fixes:
                        file_fixes[file_path] = []
                    
                    file_fixes[file_path].append({
                        "type": "code_replacement",
                        "new_code": code.strip(),
                        "description": f"Fix from file mention for {filename}",
                        "method": "file_mention"
                    })
        
        return file_fixes
    
    def _find_files_with_name(self, name: str, codebase_path: Path) -> List[Path]:
        """
        Find files that contain a specific function or class name
        """
        matching_files = []
        
        for py_file in codebase_path.glob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                # Look for function or class definitions
                if re.search(rf'(?:def|class)\s+{re.escape(name)}\s*[\(:]', content):
                    matching_files.append(py_file)
            except Exception:
                continue
        
        return matching_files
    
    def _apply_fixes_to_file(self, file_path: Path, fixes: List[Dict], results: Dict):
        """
        Apply fixes to a specific file with enhanced logic
        """
        print(f"  📝 Found {len(fixes)} potential fixes")
        
        # Backup original file
        if self.backup_original_files and self.backup_dir:
            backup_path = self.backup_dir / file_path.name
            shutil.copy2(file_path, backup_path)
            print(f"  📁 Backed up to: {backup_path}")
        
        # Read original file
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        modified_content = original_content
        fixes_applied_to_file = []
        
        for i, fix in enumerate(fixes, 1):
            print(f"  🔧 Applying fix {i}/{len(fixes)}: {fix['method']}")
            
            try:
                new_content = self._apply_single_fix(modified_content, fix, file_path)
                if new_content != modified_content:
                    modified_content = new_content
                    fixes_applied_to_file.append(fix["description"])
                    print(f"     ✓ Applied: {fix['description']}")
                else:
                    print(f"     ℹ️  No changes made for this fix")
            except Exception as e:
                print(f"     ❌ Failed to apply fix: {e}")
        
        # Write modified file if changes were made
        if modified_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            results["files_modified"].append(str(file_path))
            results["fixes_applied"].extend(fixes_applied_to_file)
            print(f"  ✅ File updated with {len(fixes_applied_to_file)} fixes")
        else:
            print(f"  ℹ️  No changes made to file")
    
    def _apply_single_fix(self, content: str, fix: Dict, file_path: Path) -> str:
        """
        Apply a single fix to content with multiple strategies
        """
        new_code = fix["new_code"]
        
        if fix["type"] == "function_replacement" and "target_name" in fix:
            # Replace specific function/class
            target_name = fix["target_name"]
            
            # Try to replace the function
            pattern = rf'((?:def|class)\s+{re.escape(target_name)}\s*[\(:].*?)(?=\n(?:def|class|\Z))'
            
            if re.search(pattern, content, re.DOTALL):
                return re.sub(pattern, new_code, content, flags=re.DOTALL)
        
        elif fix["type"] == "code_replacement":
            # Multiple strategies for code replacement
            
            # Strategy 1: If new code contains function/class, replace existing one
            func_matches = re.findall(r'def\s+(\w+)\s*\(', new_code)
            class_matches = re.findall(r'class\s+(\w+)\s*[\(:]', new_code)
            
            for name in func_matches + class_matches:
                pattern = rf'((?:def|class)\s+{re.escape(name)}\s*[\(:].*?)(?=\n(?:def|class|\Z))'
                if re.search(pattern, content, re.DOTALL):
                    return re.sub(pattern, new_code, content, flags=re.DOTALL)
            
            # Strategy 2: Look for similar code patterns
            # If new code has imports, try to replace imports section
            if new_code.strip().startswith('import ') or new_code.strip().startswith('from '):
                lines = content.split('\n')
                new_lines = []
                in_imports = False
                imports_added = False
                
                for line in lines:
                    if line.strip().startswith(('import ', 'from ')) and not imports_added:
                        if not in_imports:
                            new_lines.append(new_code)
                            imports_added = True
                            in_imports = True
                        # Skip original import lines
                    elif in_imports and not line.strip().startswith(('import ', 'from ')):
                        in_imports = False
                        new_lines.append(line)
                    elif not in_imports:
                        new_lines.append(line)
                
                if imports_added:
                    return '\n'.join(new_lines)
        
        # Fallback: Append at end with clear marker
        return content + f"\n\n# === CLAUDE GENERATED FIX ({fix['method']}) ===\n" + new_code + "\n# === END CLAUDE FIX ===\n"


def apply_fixes_to_files(report_file: str, codebase_path: str):
    """
    Main function with enhanced parsing
    """
    editor = EnhancedCodeFileEditor(backup_original_files=True)
    
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
        print("Usage: python enhanced_file_editor.py <report_file> <codebase_path>")
