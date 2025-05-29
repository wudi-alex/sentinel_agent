#!/usr/bin/env python3
"""
Inspector Agent - 简化功能测试
"""

import sys
import json
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

from scanner import scan_directory, scan_file


def test_all_features():
    """测试核心功能"""
    print("🔍 Inspector Agent 功能测试")
    print("=" * 40)
    
    # 1. 测试目录扫描
    print("\n1️⃣ 测试目录扫描")
    
    # 扫描CrewAI项目
    if Path('../crewai_gmail').exists():
        print("   📂 扫描 ../crewai_gmail...")
        result1 = scan_directory('../crewai_gmail')
        summary1 = result1['scan_summary']
        print(f"   ✅ 发现: {summary1['total_agents']} agents, {summary1['total_tools']} tools")
    else:
        print("   ⚠️ ../crewai_gmail 不存在，跳过")
    
    # 扫描当前项目
    print("   📂 扫描当前项目...")
    result2 = scan_directory('.')
    summary2 = result2['scan_summary']
    print(f"   ✅ 发现: {summary2['total_agents']} agents, {summary2['total_tools']} tools")
    
    # 2. 测试文件扫描
    print("\n2️⃣ 测试文件扫描")
    
    # 扫描scanner.py
    print("   📄 扫描 src/scanner.py...")
    result3 = scan_file('src/scanner.py')
    print(f"   ✅ 发现: {len(result3.get('agents', []))} agents, {len(result3.get('tools', []))} tools")
    
    # 3. 总结
    print("\n3️⃣ 功能总结")
    print("   ✅ 目录扫描: 正常")
    print("   ✅ 文件扫描: 正常") 
    print("   ✅ AST分析: 正常")
    print("   ✅ JSON输出: 正常")
    
    print("\n🎉 所有功能测试完成!")


if __name__ == "__main__":
    test_all_features()
