#!/usr/bin/env python3
"""
Documentation cleanup verification script
Checks that documentation is clean and all links work
"""

import os
from pathlib import Path
import re

def check_documentation_links():
    """Check for broken internal links in documentation"""
    print("🔍 Checking documentation links...")
    
    docs_dir = Path("docs")
    broken_links = []
    
    # Get all markdown files
    md_files = list(docs_dir.glob("*.md")) + [Path("README.md")]
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find markdown links [text](file.md)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content)
        
        for link_text, link_path in links:
            # Check if it's a relative link to a local file
            if not link_path.startswith('http'):
                # Resolve relative to the file's directory
                if md_file.name == "README.md":
                    target_path = Path(link_path)
                else:
                    target_path = docs_dir / link_path
                
                if not target_path.exists():
                    broken_links.append(f"{md_file}: [{link_text}]({link_path})")
    
    if broken_links:
        print("  ❌ Broken links found:")
        for link in broken_links:
            print(f"    {link}")
        return False
    else:
        print("  ✅ All documentation links are valid")
        return True

def check_outdated_references():
    """Check for outdated path references"""
    print("\n🔍 Checking for outdated references...")
    
    outdated_patterns = [
        "data/output/",
        "scripts/start_web_ui.py",
        "launch.py",
        "USER_GUIDE.md",
        "API_REFERENCE.md",
        "CONFIGURATION.md",
        "DEVELOPMENT.md"
    ]
    
    docs_dir = Path("docs")
    md_files = list(docs_dir.glob("*.md")) + [Path("README.md")]
    
    issues_found = []
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for pattern in outdated_patterns:
            if pattern in content:
                issues_found.append(f"{md_file}: contains '{pattern}'")
    
    if issues_found:
        print("  ❌ Outdated references found:")
        for issue in issues_found:
            print(f"    {issue}")
        return False
    else:
        print("  ✅ No outdated references found")
        return True

def check_documentation_completeness():
    """Check that essential documentation exists"""
    print("\n🔍 Checking documentation completeness...")
    
    essential_docs = [
        "README.md",
        "docs/QUICK_START.md",
        "docs/INSTALLATION.md", 
        "docs/CLI_USAGE.md",
        "docs/DOCKER_DEPLOYMENT.md",
        "docs/DIRECTORY_STRUCTURE.md"
    ]
    
    missing_docs = []
    for doc in essential_docs:
        if not Path(doc).exists():
            missing_docs.append(doc)
    
    if missing_docs:
        print("  ❌ Missing essential documentation:")
        for doc in missing_docs:
            print(f"    {doc}")
        return False
    else:
        print("  ✅ All essential documentation present")
        return True

def check_no_redundant_files():
    """Check that redundant files have been removed"""
    print("\n🔍 Checking for redundant files...")
    
    unwanted_docs = [
        "PROJECT_CLEANUP_COMPLETE.md",
        "docs/PROJECT_CLEANUP_SUMMARY.md",
        "docs/EXAMPLE_CASE.md",
        "docs/DEMO_GUIDE.md"
    ]
    
    redundant_found = []
    for doc in unwanted_docs:
        if Path(doc).exists():
            redundant_found.append(doc)
    
    if redundant_found:
        print("  ❌ Redundant files still present:")
        for doc in redundant_found:
            print(f"    {doc}")
        return False
    else:
        print("  ✅ No redundant documentation files found")
        return True

def main():
    """Run all documentation cleanup verification checks"""
    print("📚 Documentation Cleanup Verification")
    print("=" * 50)
    
    checks = [
        check_documentation_completeness,
        check_no_redundant_files,
        check_documentation_links,
        check_outdated_references
    ]
    
    results = []
    for check in checks:
        results.append(check())
    
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 ALL DOCUMENTATION CHECKS PASSED!")
        print("\n✨ Documentation is clean and well-organized:")
        print("  • Essential docs present")
        print("  • Redundant files removed")
        print("  • All links working")
        print("  • No outdated references")
        print("\n📚 Current documentation structure:")
        
        # Show current structure
        for doc in sorted(Path(".").glob("*.md")):
            print(f"  📄 {doc}")
        for doc in sorted(Path("docs").glob("*.md")):
            print(f"  📄 {doc}")
            
        return True
    else:
        print("❌ SOME DOCUMENTATION CHECKS FAILED!")
        print("Please review and fix the issues above.")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
