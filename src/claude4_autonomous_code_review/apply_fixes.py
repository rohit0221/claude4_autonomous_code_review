"""
Standalone File Editor CLI
Apply fixes from existing reports to source files
"""
import argparse
import sys
from pathlib import Path

# Add current directory for imports
sys.path.insert(0, str(Path(__file__).parent))

from file_editor import apply_fixes_to_files, CodeFileEditor


def main():
    """CLI for applying fixes to source files"""
    parser = argparse.ArgumentParser(
        description="Apply code fixes from reports to actual source files"
    )
    
    parser.add_argument(
        'report_file',
        help='Path to Step 2 fix report JSON file'
    )
    
    parser.add_argument(
        'codebase_path',
        help='Path to codebase directory'
    )
    
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Skip creating backup files'
    )
    
    parser.add_argument(
        '--revert',
        help='Revert changes using backup directory'
    )
    
    args = parser.parse_args()
    
    try:
        if args.revert:
            # Revert mode
            editor = CodeFileEditor()
            editor.revert_changes(Path(args.revert), Path(args.codebase_path))
            return 0
        
        # Validate inputs
        if not Path(args.report_file).exists():
            print(f"❌ Report file not found: {args.report_file}")
            return 1
        
        if not Path(args.codebase_path).exists():
            print(f"❌ Codebase path not found: {args.codebase_path}")
            return 1
        
        # Confirm before modifying files
        print(f"🔧 APPLYING FIXES TO SOURCE FILES")
        print("=" * 50)
        print(f"📄 Report: {args.report_file}")
        print(f"📁 Codebase: {args.codebase_path}")
        print(f"📦 Backup: {'No' if args.no_backup else 'Yes'}")
        print()
        
        confirm = input("Proceed with file modifications? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Cancelled.")
            return 0
        
        # Apply fixes
        editor = CodeFileEditor(backup_original_files=not args.no_backup)
        results = editor.apply_fixes_from_report(
            Path(args.report_file),
            Path(args.codebase_path)
        )
        
        if "error" in results:
            print(f"❌ Failed: {results['error']}")
            return 1
        
        # Show revert command if backups were created
        if results.get('backup_directory'):
            print(f"\n💡 To revert changes:")
            print(f"   python apply_fixes.py dummy {args.codebase_path} --revert {results['backup_directory']}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n❌ Interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
