from crewai import Agent, Task, Crew
from tools import DirectoryScanTool, FileScanTool, ReportAnalysisTool
import os
from pathlib import Path


class InspectorAgent:
    """Inspector Agent - 用于扫描和分析agent系统的智能代理"""
    
    def __init__(self):
        # 设置环境变量（如果需要）
        self._setup_environment()
        
        # 创建工具
        self.directory_scan_tool = DirectoryScanTool()
        self.file_scan_tool = FileScanTool()
        self.report_analysis_tool = ReportAnalysisTool()
        
        # 创建代理
        self.scanner_agent = Agent(
            role='Agent System Scanner',
            goal='扫描和分析目标项目的agent系统结构，识别所有的agents、tools、crews和tasks',
            backstory="""你是一个专业的代码分析专家，专门负责分析agent系统的架构。
            你能够深入理解CrewAI、AutoGen等agent框架的代码结构，
            准确识别其中的各种组件，并生成详细的分析报告。""",
            tools=[self.directory_scan_tool, self.file_scan_tool],
            verbose=True,
            allow_delegation=False
        )
        
        self.analyst_agent = Agent(
            role='System Architecture Analyst',
            goal='分析扫描结果，提供深入的架构洞察和建议',
            backstory="""你是一个经验丰富的系统架构师，专门分析agent系统的设计模式。
            你能够从扫描结果中提取有价值的信息，理解系统的组织结构，
            并提供专业的架构分析和改进建议。""",
            tools=[self.report_analysis_tool],
            verbose=True,
            allow_delegation=False
        )
    
    def _setup_environment(self):
        """设置环境变量"""
        # 如果需要API key，可以在这里设置
        # os.environ['OPENAI_API_KEY'] = 'your-api-key'
        pass
    
    def scan_directory(self, target_path: str, output_file: str = None) -> str:
        """扫描目录的主要方法"""
        if output_file is None:
            output_file = f"scan_result_{Path(target_path).name}.json"
        
        # 创建扫描任务
        scan_task = Task(
            description=f"""
            请扫描目录 '{target_path}' 中的agent系统结构。
            
            任务要求:
            1. 使用directory_scanner工具扫描整个目录
            2. 识别所有的agents、tools、crews和tasks
            3. 分析文件结构和组织方式
            4. 将结果保存到 '{output_file}' 文件中
            5. 提供扫描摘要
            
            目标目录: {target_path}
            输出文件: {output_file}
            """,
            expected_output="扫描摘要和结果文件路径",
            agent=self.scanner_agent
        )
        
        # 创建分析任务
        analysis_task = Task(
            description=f"""
            请分析扫描结果文件 '{output_file}'，提供详细的架构分析。
            
            任务要求:
            1. 使用report_analyzer工具分析扫描结果
            2. 提供agents的详细信息和功能描述
            3. 分析tools的能力和用途
            4. 理解crews和tasks的组织结构
            5. 总结系统的整体架构特点
            6. 提供改进建议（如有必要）
            """,
            expected_output="详细的系统架构分析报告",
            agent=self.analyst_agent,
            context=[scan_task]
        )
        
        # 创建并运行crew
        crew = Crew(
            agents=[self.scanner_agent, self.analyst_agent],
            tasks=[scan_task, analysis_task],
            verbose=True
        )
        
        result = crew.kickoff()
        return result
    
    def scan_file(self, target_file: str, output_file: str = None) -> str:
        """扫描单个文件的方法"""
        if output_file is None:
            output_file = f"scan_result_{Path(target_file).stem}.json"
        
        # 创建扫描任务
        scan_task = Task(
            description=f"""
            请扫描文件 '{target_file}' 中的agent系统组件。
            
            任务要求:
            1. 使用file_scanner工具扫描指定文件
            2. 识别文件中的agents、tools、crews和tasks
            3. 分析代码结构和设计模式
            4. 将结果保存到 '{output_file}' 文件中
            5. 提供扫描摘要
            
            目标文件: {target_file}
            输出文件: {output_file}
            """,
            expected_output="扫描摘要和结果文件路径",
            agent=self.scanner_agent
        )
        
        # 创建分析任务
        analysis_task = Task(
            description=f"""
            请分析扫描结果文件 '{output_file}'，提供详细的代码分析。
            
            任务要求:
            1. 使用report_analyzer工具分析扫描结果
            2. 详细描述发现的每个组件
            3. 分析代码的设计模式和架构
            4. 评估代码质量和结构
            5. 提供优化建议
            """,
            expected_output="详细的代码分析报告",
            agent=self.analyst_agent,
            context=[scan_task]
        )
        
        # 创建并运行crew
        crew = Crew(
            agents=[self.scanner_agent, self.analyst_agent],
            tasks=[scan_task, analysis_task],
            verbose=True
        )
        
        result = crew.kickoff()
        return result


def main():
    """主函数 - 命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Inspector Agent - Agent系统结构扫描器')
    parser.add_argument('target', help='要扫描的目录或文件路径')
    parser.add_argument('--output', '-o', help='输出文件名', default=None)
    parser.add_argument('--type', '-t', choices=['dir', 'file'], 
                       help='指定目标类型（自动检测）', default=None)
    
    args = parser.parse_args()
    
    # 创建Inspector Agent
    inspector = InspectorAgent()
    
    # 确定目标类型
    target_path = Path(args.target)
    if args.type:
        is_directory = args.type == 'dir'
    else:
        is_directory = target_path.is_dir()
    
    print(f"🔍 Inspector Agent 开始工作...")
    print(f"📂 目标: {args.target}")
    print(f"📋 类型: {'目录' if is_directory else '文件'}")
    print("-" * 50)
    
    try:
        if is_directory:
            result = inspector.scan_directory(args.target, args.output)
        else:
            result = inspector.scan_file(args.target, args.output)
        
        print("\n" + "=" * 50)
        print("✅ 扫描完成!")
        print("=" * 50)
        print(result)
        
    except Exception as e:
        print(f"❌ 扫描失败: {e}")


if __name__ == "__main__":
    main()
