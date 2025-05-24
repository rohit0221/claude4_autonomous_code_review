# Clean Iterative Code Review System

## 🎯 What This Does

A **clean, single-file** iterative code review system that:
- Runs **5 focused iterations** by default (parameterizable)
- Generates **both JSON and Markdown** reports in `reports/` folder
- Provides **human review** and **optional fix application**
- **No duplicated code** - one clean implementation

## 🚀 Quick Start

### **Run Review (Generates JSON + Markdown)**
```bash
python src/claude4_autonomous_code_review/clean_review.py review C:\GitHub\claude4_autonomous_code_review\code_under_review --iterations 3
```

### **Human Review & Apply Fixes**
```bash
python src/claude4_autonomous_code_review/clean_review.py apply
```

### **Complete Workflow (Review → Human → Fixes)**
```bash
python src/claude4_autonomous_code_review/clean_review.py complete C:\GitHub\claude4_autonomous_code_review\code_under_review --iterations 5
```

## 📁 Clean File Structure

```
src/claude4_autonomous_code_review/
├── clean_review.py           # 🎯 MAIN FILE - Everything in one place
├── claude4_client.py         # 🤖 Claude API client
├── config.py                 # ⚙️  Configuration
├── iteration_prompts.py      # 📝 Focused prompts for each iteration
├── enhanced_file_editor.py   # 🔧 File modification system
├── debug_fixes.py            # 🔍 Debug fix parsing
├── view_results.py           # 📊 Results viewer
└── setup.py                  # 🛠️ Setup utility
```

**Removed duplicates:**
- ❌ `old_*.py.bak` - All duplicate implementations moved to backup

## 📊 What You Get

### **Reports Generated (Both in `reports/` folder):**
1. **JSON Report**: `reports/review_TIMESTAMP.json` (for processing)
2. **Markdown Report**: `reports/review_TIMESTAMP.md` (for humans)

### **Iteration Focus Areas:**
1. **🔒 Security & Critical Bugs** - SQL injection, auth bypasses
2. **⚡ Performance & Resources** - O(n²) algorithms, memory leaks  
3. **🔍 Input Validation & Data Flow** - Unvalidated inputs, sanitization
4. **🐛 Error Handling & Edge Cases** - Exceptions, race conditions
5. **🏗️ Architecture & Design** - SOLID violations, design patterns

## 💰 Cost & Performance

- **Cost**: ~$0.02-0.08 per review (cheap Haiku model)
- **Time**: 1-2 minutes for 5 iterations
- **Files**: Up to 10 Python files analyzed
- **Output**: JSON + Markdown in same folder

## 🎯 Usage Examples

### **Quick 3-iteration Review**
```bash
python src/claude4_autonomous_code_review/clean_review.py review ./my_project --iterations 3
```

### **Security-Focused Review**
```bash
python src/claude4_autonomous_code_review/clean_review.py review ./webapp --goals "Find security vulnerabilities only" --iterations 4
```

### **Complete Workflow with Custom Goals**
```bash
python src/claude4_autonomous_code_review/clean_review.py complete ./backend --goals "Performance optimization and memory usage analysis" --iterations 6
```

### **View Latest Results**
```bash
python src/claude4_autonomous_code_review/view_results.py
```

## 🔧 Commands Reference

### **Review Command**
```bash
python clean_review.py review <path> [--goals "custom goals"] [--iterations N] [--production]
```
- Generates JSON + Markdown reports
- Parameterizable iterations (default: 5)
- Uses cheap model by default

### **Apply Command** 
```bash
python clean_review.py apply [--json-file specific_file.json]
```
- Human review of findings
- Optional fix generation
- Optional file modification

### **Complete Command**
```bash
python clean_review.py complete <path> [options]
```
- Runs review then apply in sequence
- Full workflow with human oversight

## 🛡️ Safety Features

1. **✅ Human Approval Required** - No automatic file changes
2. **✅ Automatic Backups** - Original files backed up before modification
3. **✅ Cost Control** - Defaults to cheap model, explicit confirmation for expensive
4. **✅ Reports Saved** - Both JSON and Markdown preserved
5. **✅ Clean Output** - All reports in `reports/` folder, not scattered

## 📄 Sample Markdown Report

The generated markdown includes:
- **📊 Executive Summary** with costs and metrics
- **🎯 Review Goals** clearly stated
- **📁 Files Analyzed** with numbered list
- **🔄 Iteration Summary** with collapsible detailed findings
- **📊 Technical Details** with token usage

## 🎉 Key Improvements

✅ **Single Implementation** - No more duplicate files  
✅ **Consistent Output Location** - Everything in `reports/` folder  
✅ **Both JSON + Markdown** - Machine readable + human readable  
✅ **Parameterizable Iterations** - 1 to 50+ iterations supported  
✅ **Clean CLI** - Simple commands, no confusion  
✅ **Human Control** - Review findings before applying fixes  

## 🚀 Try It Now

```bash
# Quick test with 3 iterations
python src/claude4_autonomous_code_review/clean_review.py review C:\GitHub\claude4_autonomous_code_review\code_under_review --iterations 3

# View the results
python src/claude4_autonomous_code_review/view_results.py

# Apply fixes if you approve them
python src/claude4_autonomous_code_review/clean_review.py apply
```

**Clean, simple, effective! No more confusion with multiple files doing the same thing.** 🎯
