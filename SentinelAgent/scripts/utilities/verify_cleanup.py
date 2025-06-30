#!/usr/bin/env python3
"""
Post-cleanup verification script for SentinelAgent
Verifies that the project structure is correct and core functionality works
"""

import os
import sys
from pathlib import Path

def check_directory_structure():
    """Check that all expected directories exist"""
    print("🔍 Checking directory structure...")
    
    expected_dirs = [
        "sentinelagent",
        "sentinelagent/core", 
        "sentinelagent/cli",
        "sentinelagent/web",
        "sentinelagent/utils",
        "scripts/analysis",
        "scripts/demo", 
        "scripts/utilities",
        "data/demo",
        "data/uploads",
        "data/generated_outputs",
        "data/analysis_results",
        "docs",
        "examples",
        "tests",
        "config"
    ]
    
    missing_dirs = []
    for dir_path in expected_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
        else:
            print(f"  ✅ {dir_path}")
    
    if missing_dirs:
        print(f"  ❌ Missing directories: {missing_dirs}")
        return False
    
    print("  ✅ All expected directories present")
    return True

def check_core_files():
    """Check that core files exist"""
    print("\n🔍 Checking core files...")
    
    expected_files = [
        "sentinelagent/__init__.py",
        "sentinelagent/core/scanner.py",
        "sentinelagent/core/graph_builder.py", 
        "sentinelagent/core/path_analyzer.py",
        "sentinelagent/core/inspector.py",
        "sentinelagent/cli/main.py",
        "setup.py",
        "requirements.txt",
        "README.md",
        ".gitignore"
    ]
    
    missing_files = []
    for file_path in expected_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    if missing_files:
        print(f"  ❌ Missing files: {missing_files}")
        return False
        
    print("  ✅ All core files present")
    return True

def check_no_clutter():
    """Check that root directory is clean"""
    print("\n🔍 Checking for clutter in root directory...")
    
    # Check for files that should have been moved
    unwanted_patterns = ["*.json", "*.png", "*.pyc"]
    unwanted_dirs = ["__pycache__", "venv", "*.egg-info"]
    
    clutter_found = []
    
    # Check for unwanted files in root
    for pattern in unwanted_patterns:
        import glob
        matches = glob.glob(pattern)
        if matches:
            clutter_found.extend(matches)
    
    # Check for unwanted directories
    for item in Path(".").iterdir():
        if item.is_dir():
            if (item.name == "__pycache__" or 
                item.name == "venv" or 
                item.name.endswith(".egg-info")):
                clutter_found.append(str(item))
    
    if clutter_found:
        print(f"  ❌ Clutter found: {clutter_found}")
        return False
        
    print("  ✅ Root directory is clean")
    return True

def check_package_import():
    """Check that the package can be imported"""
    print("\n🔍 Checking package import...")
    
    try:
        # Add current directory to path so we can import without installation
        sys.path.insert(0, ".")
        
        import sentinelagent
        print(f"  ✅ sentinelagent package imported successfully")
        
        from sentinelagent.core import scanner
        print(f"  ✅ core.scanner imported successfully")
        
        from sentinelagent.core import graph_builder
        print(f"  ✅ core.graph_builder imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def check_gitignore():
    """Check that gitignore has been updated"""
    print("\n🔍 Checking .gitignore configuration...")
    
    with open(".gitignore", "r") as f:
        gitignore_content = f.read()
    
    expected_patterns = [
        "data/generated_outputs/*",
        "data/analysis_results/*",
        "*.json",
        "*.png"
    ]
    
    missing_patterns = []
    for pattern in expected_patterns:
        if pattern not in gitignore_content:
            missing_patterns.append(pattern)
        else:
            print(f"  ✅ {pattern}")
    
    if missing_patterns:
        print(f"  ❌ Missing gitignore patterns: {missing_patterns}")
        return False
        
    print("  ✅ .gitignore is properly configured")
    return True

def main():
    """Run all verification checks"""
    print("🧹 SentinelAgent Post-Cleanup Verification")
    print("=" * 50)
    
    checks = [
        check_directory_structure,
        check_core_files,
        check_no_clutter,
        check_package_import,
        check_gitignore
    ]
    
    results = []
    for check in checks:
        results.append(check())
    
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 ALL CHECKS PASSED! Project cleanup was successful.")
        print("\n✨ Your SentinelAgent project is now clean and properly organized!")
        print("\nNext steps:")
        print("1. Create virtual environment: python -m venv venv")
        print("2. Activate it: source venv/bin/activate (or venv\\Scripts\\activate on Windows)")
        print("3. Install dependencies: pip install -r requirements.txt")
        print("4. Install package in development mode: pip install -e .")
        return True
    else:
        print("❌ SOME CHECKS FAILED. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
