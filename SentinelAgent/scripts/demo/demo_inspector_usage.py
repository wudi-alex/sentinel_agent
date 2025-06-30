#!/usr/bin/env python3
"""
Inspector Demo - 展示InspectorAgent的高级使用场景
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sentinelagent.core.inspector import InspectorAgent

def scenario_1_adaptive_analysis():
    """场景1: 自适应分析 - 根据项目类型调整分析策略"""
    print("🔍 场景1: 自适应分析")
    print("=" * 50)
    
    inspector = InspectorAgent()
    
    # 对复杂项目进行全面分析
    target_path = "/Users/xuhe/Documents/agent_experiments/crewai_gmail"
    
    print(f"开始对 {target_path} 进行智能分析...")
    
    # Inspector会根据项目特征自动调整分析深度
    result = inspector.comprehensive_analysis(
        target_path=target_path,
        scan_output="adaptive_scan.json",
        graph_output="adaptive_graph.json", 
        path_output="adaptive_paths.json"
    )
    
    print("✅ 自适应分析完成!")
    return result

def scenario_2_intelligent_error_handling():
    """场景2: 智能错误处理 - 当文件结构复杂时的智能重试"""
    print("\n🛠️ 场景2: 智能错误处理")
    print("=" * 50)
    
    inspector = InspectorAgent()
    
    # 分析可能有问题的文件
    problem_file = "/Users/xuhe/Documents/agent_experiments/crewai_gmail/email_assistant_agent_system.py"
    
    print(f"使用Inspector智能分析问题文件: {problem_file}")
    
    # Inspector的Agent可以处理复杂情况并提供更好的错误信息
    result = inspector.scan_file(problem_file, "intelligent_scan.json")
    
    print("✅ 智能错误处理完成!")
    return result

def scenario_3_interactive_analysis():
    """场景3: 交互式分析 - 可以进行对话式的深度分析"""
    print("\n💬 场景3: 交互式分析能力展示")
    print("=" * 50)
    
    inspector = InspectorAgent()
    
    # 模拟复杂的分析需求
    print("Inspector Agent具备以下交互能力:")
    print("1. 可以理解自然语言任务描述")
    print("2. 可以根据上下文调整分析策略") 
    print("3. 可以提供详细的分析解释")
    print("4. 可以处理多轮对话式的分析请求")
    
    return "交互式分析演示完成"

def scenario_4_complex_project_analysis():
    """场景4: 复杂项目分析 - 多模块、多文件的大型项目"""
    print("\n🏗️ 场景4: 复杂项目分析")
    print("=" * 50)
    
    inspector = InspectorAgent()
    
    # 分析整个SentinelAgent项目本身
    target_path = "/Users/xuhe/Documents/agent_experiments/SentinelAgent"
    
    print(f"使用Inspector分析复杂项目: {target_path}")
    print("Inspector的优势:")
    print("- 可以理解项目结构的复杂性")
    print("- 可以识别不同模块间的关系")
    print("- 可以提供架构级别的分析建议")
    
    # 这里实际调用会比较耗时，仅做演示
    print("📝 建议使用Inspector的情况:")
    print("  - 项目包含100+个Python文件")
    print("  - 需要深度理解代码架构")
    print("  - 需要生成分析报告")
    print("  - 需要智能的异常检测")
    
    return "复杂项目分析演示完成"

def when_to_use_inspector():
    """总结：什么时候使用Inspector"""
    print("\n📋 Inspector使用指南")
    print("=" * 60)
    
    print("✅ 建议使用Inspector的场景:")
    print("1. 🔍 需要智能分析策略调整")
    print("2. 🛠️ 处理复杂或有问题的代码结构")
    print("3. 💬 需要解释性的分析结果")
    print("4. 🏗️ 大型多模块项目分析")
    print("5. 🔄 需要多轮对话式的分析")
    print("6. 📊 生成详细的分析报告")
    print("7. ⚡ 需要自适应的错误恢复")
    
    print("\n❌ 不建议使用Inspector的场景:")
    print("1. ⚡ 简单快速的一次性扫描")
    print("2. 🔧 批量自动化处理")
    print("3. 💨 性能敏感的场景")
    print("4. 🤖 纯编程式的API调用")
    
    print("\n🎯 选择建议:")
    print("- 日常开发调试 → 使用CLI直接调用")
    print("- 深度安全分析 → 使用Inspector")
    print("- 复杂项目审查 → 使用Inspector") 
    print("- 自动化CI/CD → 使用CLI直接调用")

if __name__ == "__main__":
    print("🚀 Inspector使用场景演示")
    print("=" * 60)
    
    # 运行各种场景演示
    try:
        scenario_1_adaptive_analysis()
        scenario_2_intelligent_error_handling() 
        scenario_3_interactive_analysis()
        scenario_4_complex_project_analysis()
        when_to_use_inspector()
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        print("💡 这正是Inspector可以智能处理的情况!")
