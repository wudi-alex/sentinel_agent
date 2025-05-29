from crewai import Agent, Task, Crew
from .tools import DirectoryScanTool, FileScanTool
from pathlib import Path
from .graph_builder import build_graph_from_scan, build_and_save_graph
from .path_analyzer import analyze_graph_paths, analyze_and_save_paths


class InspectorAgent:
    """Inspector Agent - Agent系统扫描、图构建和路径分析"""
    
    def __init__(self):
        # 创建工具
        self.directory_scan_tool = DirectoryScanTool()
        self.file_scan_tool = FileScanTool()
        
        # 创建Agent
        self.scanner_agent = Agent(
            role='Agent System Scanner and Analyzer',
            goal='扫描、分析agent系统结构，构建关系图并分析执行路径',
            backstory='专业的代码分析专家，能够识别各种agent组件、构建关系图并检测异常模式',
            tools=[self.directory_scan_tool, self.file_scan_tool],
            verbose=True
        )
    
    def comprehensive_analysis(self, target_path: str, 
                             scan_output: str = None, 
                             graph_output: str = None, 
                             path_output: str = None) -> dict:
        """完整的系统分析：扫描 + 图构建 + 路径分析"""
        target_name = Path(target_path).name
        
        # 设置默认输出文件名
        if scan_output is None:
            scan_output = f"scan_{target_name}.json"
        if graph_output is None:
            graph_output = f"graph_{target_name}.json"
        if path_output is None:
            path_output = f"paths_{target_name}.json"
        
        print(f"开始完整分析: {target_path}")
        
        # 1. 扫描
        print("1. 执行系统扫描...")
        scan_result = self._perform_scan(target_path, scan_output)
        
        # 2. 构建图
        print("2. 构建关系图...")
        graph_data = build_and_save_graph(scan_result, graph_output)
        
        # 3. 路径分析
        print("3. 分析执行路径...")
        path_analysis = analyze_and_save_paths(graph_data, path_output)
        
        print(f"完整分析完成！")
        print(f"- 扫描结果: {scan_output}")
        print(f"- 关系图: {graph_output}")
        print(f"- 路径分析: {path_output}")
        
        return {
            'scan_result': scan_result,
            'graph_data': graph_data,
            'path_analysis': path_analysis,
            'output_files': {
                'scan': scan_output,
                'graph': graph_output,
                'paths': path_output
            }
        }
    
    def analyze_existing_graph(self, graph_file: str, path_output: str = None) -> dict:
        """分析已有的图文件"""
        if path_output is None:
            graph_path = Path(graph_file)
            path_output = f"paths_{graph_path.stem}.json"
        
        print(f"分析图文件: {graph_file}")
        
        # 读取图数据
        import json
        with open(graph_file, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
        
        # 执行路径分析
        path_analysis = analyze_and_save_paths(graph_data, path_output)
        
        print(f"路径分析完成: {path_output}")
        
        return {
            'graph_data': graph_data,
            'path_analysis': path_analysis,
            'output_file': path_output
        }
    
    def _perform_scan(self, target_path: str, output_file: str) -> dict:
        """执行扫描操作"""
        if Path(target_path).is_dir():
            return self._scan_directory_internal(target_path, output_file)
        else:
            return self._scan_file_internal(target_path, output_file)
    
    def _scan_directory_internal(self, target_path: str, output_file: str) -> dict:
        """内部目录扫描方法"""
        from .scanner import scan_directory
        return scan_directory(target_path, output_file)
    
    def _scan_file_internal(self, target_path: str, output_file: str) -> dict:
        """内部文件扫描方法"""
        from .scanner import scan_file
        return scan_file(target_path, output_file)
    
    def scan_directory(self, target_path: str, output_file: str = None) -> str:
        """扫描目录"""
        if output_file is None:
            output_file = f"scan_{Path(target_path).name}.json"
        
        task = Task(
            description=f"扫描目录 '{target_path}' 并保存结果到 '{output_file}'",
            expected_output="扫描摘要",
            agent=self.scanner_agent
        )
        
        crew = Crew(agents=[self.scanner_agent], tasks=[task], verbose=True)
        return crew.kickoff()
    
    def scan_file(self, target_file: str, output_file: str = None) -> str:
        """扫描文件"""
        if output_file is None:
            output_file = f"scan_{Path(target_file).stem}.json"
        
        task = Task(
            description=f"扫描文件 '{target_file}' 并保存结果到 '{output_file}'",
            expected_output="扫描摘要",
            agent=self.scanner_agent
        )
        
        crew = Crew(agents=[self.scanner_agent], tasks=[task], verbose=True)
        return crew.kickoff()


def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Inspector Agent')
    parser.add_argument('target', help='要扫描的目录或文件')
    parser.add_argument('--output', '-o', help='输出文件名')
    
    args = parser.parse_args()
    inspector = InspectorAgent()
    
    target_path = Path(args.target)
    
    print(f"🔍 Inspector Agent 开始工作...")
    print(f"📂 目标: {args.target}")
    
    try:
        if target_path.is_dir():
            result = inspector.scan_directory(args.target, args.output)
        else:
            result = inspector.scan_file(args.target, args.output)
        
        print("✅ 扫描完成!")
        print(result)
        
    except Exception as e:
        print(f"❌ 扫描失败: {e}")


if __name__ == "__main__":
    main()
