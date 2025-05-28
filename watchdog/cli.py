#!/usr/bin/env python3
"""
Inspector Agent - 命令行接口
简单易用的agent系统扫描工具
"""

import sys
import json
from pathlib import Path
from scanner import AgentSystemScanner


def print_usage():
    """打印使用说明"""
    print("🔍 Inspector Agent - Agent系统结构扫描器")
    print("\n使用方法:")
    print("  python cli.py <目标路径> [选项]")
    print("\n参数:")
    print("  目标路径          要扫描的目录或文件路径")
    print("\n选项:")
    print("  -o, --output     指定输出文件名 (默认: scan_result.json)")
    print("  -v, --verbose    显示详细信息")
    print("  -h, --help       显示此帮助信息")
    print("\n示例:")
    print("  python cli.py ../crewai_gmail")
    print("  python cli.py ../crewai_gmail --output gmail_scan.json")
    print("  python cli.py tools.py --verbose")


def format_summary(summary):
    """格式化摘要信息"""
    return f"""📊 扫描摘要:
  🤖 Agents: {summary['total_agents']}
  🔧 Tools: {summary['total_tools']}
  👥 Crews: {summary['total_crews']}
  📋 Tasks: {summary['total_tasks']}
  📄 Files: {summary['total_files']}"""


def format_details(result, verbose=False):
    """格式化详细信息"""
    details = []
    
    if result['agents'] and verbose:
        details.append("\n🤖 发现的Agents:")
        for agent in result['agents'][:10]:  # 最多显示10个
            details.append(f"  - {agent['name']} ({agent['type']})")
            if 'role' in agent.get('arguments', {}):
                details.append(f"    角色: {agent['arguments']['role']}")
    
    if result['tools'] and verbose:
        details.append("\n🔧 发现的Tools:")
        for tool in result['tools'][:10]:  # 最多显示10个
            details.append(f"  - {tool['name']} ({tool['type']})")
    
    return "\n".join(details)


def main():
    """主函数"""
    args = sys.argv[1:]
    
    # 解析参数
    if not args or '--help' in args or '-h' in args:
        print_usage()
        return
    
    target_path = args[0]
    output_file = "scan_result.json"
    verbose = False
    
    # 解析选项
    i = 1
    while i < len(args):
        if args[i] in ['-o', '--output'] and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif args[i] in ['-v', '--verbose']:
            verbose = True
            i += 1
        else:
            i += 1
    
    # 检查目标路径
    path = Path(target_path)
    if not path.exists():
        print(f"❌ 错误: 路径不存在 '{target_path}'")
        return
    
    # 执行扫描
    print(f"🔍 正在扫描: {target_path}")
    print("-" * 50)
    
    try:
        scanner = AgentSystemScanner()
        
        if path.is_dir():
            result = scanner.scan_directory(target_path)
            scan_type = "目录"
        else:
            result = scanner.scan_file(target_path)
            scan_type = "文件"
        
        # 显示结果
        print(f"✅ {scan_type}扫描完成!")
        print(format_summary(result['scan_summary']))
        
        if verbose:
            print(format_details(result, verbose=True))
        
        # 保存结果
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 详细结果已保存到: {output_file}")
        
        if not verbose and (result['agents'] or result['tools']):
            print("💡 使用 --verbose 选项查看详细信息")
    
    except Exception as e:
        print(f"❌ 扫描失败: {e}")
        return 1


if __name__ == "__main__":
    exit(main() or 0)
