#!/usr/bin/env python3
"""
Inspector实际使用指南和示例
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sentinelagent.core.inspector import InspectorAgent

class InspectorUsageGuide:
    """Inspector使用指南"""
    
    def __init__(self):
        self.inspector = InspectorAgent()
    
    def basic_file_analysis(self, file_path: str):
        """基础文件分析 - 最简单的Inspector使用方式"""
        print(f"🔍 基础文件分析: {file_path}")
        print("-" * 50)
        
        # 直接使用Inspector分析单个文件
        result = self.inspector.scan_file(file_path, "basic_analysis.json")
        
        print("✅ 分析完成")
        print(f"📄 结果: {result}")
        return result
    
    def comprehensive_project_analysis(self, project_path: str):
        """全面项目分析 - Inspector的核心功能"""
        print(f"🏗️ 全面项目分析: {project_path}")
        print("-" * 50)
        
        # 使用Inspector进行完整的项目分析
        result = self.inspector.comprehensive_analysis(
            target_path=project_path,
            scan_output="comprehensive_scan.json",
            graph_output="comprehensive_graph.json",
            path_output="comprehensive_paths.json"
        )
        
        print("✅ 全面分析完成")
        print(f"📊 分析结果包含:")
        print(f"  - 扫描结果: {result['output_files']['scan']}")
        print(f"  - 关系图: {result['output_files']['graph']}")
        print(f"  - 路径分析: {result['output_files']['paths']}")
        
        return result
    
    def intelligent_error_recovery(self, problematic_path: str):
        """智能错误恢复 - Inspector处理复杂情况的能力"""
        print(f"🛠️ 智能错误恢复分析: {problematic_path}")
        print("-" * 50)
        
        try:
            # Inspector可以智能处理各种复杂情况
            if Path(problematic_path).is_dir():
                result = self.inspector.scan_directory(problematic_path, "error_recovery_scan.json")
            else:
                result = self.inspector.scan_file(problematic_path, "error_recovery_scan.json")
            
            print("✅ 智能错误恢复成功")
            return result
            
        except Exception as e:
            print(f"❌ 即使Inspector也无法处理: {e}")
            print("💡 这种情况下建议:")
            print("  1. 检查文件权限")
            print("  2. 确认文件编码")
            print("  3. 检查文件结构")
            return None
    
    def analyze_existing_graph(self, graph_file: str):
        """分析现有图数据 - Inspector的高级分析功能"""
        print(f"📊 分析现有图数据: {graph_file}")
        print("-" * 50)
        
        # 使用Inspector分析已有的图数据
        result = self.inspector.analyze_existing_graph(graph_file, "graph_analysis.json")
        
        print("✅ 图数据分析完成")
        return result


def demonstrate_inspector_advantages():
    """演示Inspector相比直接CLI的优势"""
    
    print("🎯 Inspector vs CLI 对比演示")
    print("=" * 60)
    
    guide = InspectorUsageGuide()
    
    # 测试文件
    test_file = "/Users/xuhe/Documents/agent_experiments/crewai_gmail/email_assistant_agent_system.py"
    
    print("\n1️⃣ 基础文件分析演示")
    basic_result = guide.basic_file_analysis(test_file)
    
    print("\n📊 Inspector的优势体现:")
    print("  ✅ 提供了结构化的JSON响应")
    print("  ✅ Agent可以理解复杂的分析需求")
    print("  ✅ 可以自动处理异常情况")
    print("  ✅ 生成了解释性的分析报告")
    
    return basic_result


def when_to_choose_inspector():
    """选择Inspector的决策指南"""
    
    print("\n🤔 何时选择Inspector？")
    print("=" * 40)
    
    scenarios = {
        "✅ 推荐使用Inspector": [
            "🔍 需要深度代码理解和推理",
            "🛠️ 处理复杂或损坏的文件结构", 
            "💬 需要解释性的分析结果",
            "🏗️ 大型项目的架构分析",
            "📊 生成详细的分析报告",
            "🔄 多轮交互式的分析过程",
            "⚡ 需要智能错误恢复",
            "🎯 自适应的分析策略"
        ],
        "❌ 推荐使用CLI直接调用": [
            "⚡ 快速简单的一次性扫描",
            "🔧 批量自动化处理",
            "💨 性能敏感的场景",
            "🤖 纯编程式的API调用",
            "📈 CI/CD管道中的自动化检查",
            "🎮 简单的开发调试",
            "💾 资源受限的环境",
            "⏱️ 时间敏感的任务"
        ]
    }
    
    for category, items in scenarios.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  {item}")
    
    print(f"\n💡 实用建议:")
    print(f"  - 开发阶段 → CLI直接调用（快速验证）")
    print(f"  - 安全审查 → Inspector（深度分析）") 
    print(f"  - 项目文档 → Inspector（生成报告）")
    print(f"  - 生产监控 → CLI直接调用（性能优先）")


def practical_usage_examples():
    """实用使用示例"""
    
    print("\n📝 实用使用示例")
    print("=" * 30)
    
    examples = {
        "安全审查场景": {
            "代码": """
guide = InspectorUsageGuide()
result = guide.comprehensive_project_analysis("/path/to/project")

# Inspector会自动:
# 1. 识别所有agents和工具
# 2. 构建组件关系图
# 3. 分析潜在的安全风险
# 4. 生成详细的审查报告
            """,
            "适用性": "需要深度理解项目架构和潜在风险"
        },
        
        "日常开发调试": {
            "代码": """
# 直接使用CLI - 更快更简单
import subprocess
result = subprocess.run([
    "python", "-m", "sentinelagent.cli.main", 
    "/path/to/file.py", "--output", "debug_scan.json"
], capture_output=True)
            """,
            "适用性": "快速验证代码结构，性能优先"
        },
        
        "复杂项目分析": {
            "代码": """
guide = InspectorUsageGuide()
result = guide.comprehensive_project_analysis("/complex/project")

# Inspector的Agent可以:
# 1. 理解复杂的项目结构
# 2. 自动调整分析策略
# 3. 处理多种文件类型
# 4. 生成架构级别的见解
            """,
            "适用性": "大型项目架构审查，需要智能分析"
        }
    }
    
    for scenario, details in examples.items():
        print(f"\n🎯 {scenario}:")
        print(f"📋 适用性: {details['适用性']}")
        print(f"💻 代码示例:")
        print(details['代码'])


if __name__ == "__main__":
    print("📚 Inspector实际使用指南")
    print("=" * 50)
    
    try:
        # 运行演示
        demonstrate_inspector_advantages()
        when_to_choose_inspector()
        practical_usage_examples()
        
        print("\n🎉 Inspector使用指南演示完成！")
        print("💡 根据你的具体需求选择合适的工具")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        print("🔧 请检查环境配置和文件路径")
