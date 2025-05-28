from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any
import json
from pathlib import Path
from scanner import AgentSystemScanner


class DirectoryScanInput(BaseModel):
    directory_path: str = Field(..., description="要扫描的目录路径")
    output_file: str = Field(default="scan_result.json", description="输出JSON文件名")


class FileScanInput(BaseModel):
    file_path: str = Field(..., description="要扫描的文件路径")
    output_file: str = Field(default="scan_result.json", description="输出JSON文件名")


class DirectoryScanTool(BaseTool):
    """扫描目录中agent系统的工具"""
    name: str = "directory_scanner"
    description: str = "扫描指定目录，分析其中的agent系统结构，识别agents、tools等组件"
    args_schema: Type[BaseModel] = DirectoryScanInput

    def _run(self, directory_path: str, output_file: str = "scan_result.json") -> str:
        try:
            scanner = AgentSystemScanner()
            result = scanner.scan_directory(directory_path)
            
            # 保存结果到JSON文件
            output_path = Path(output_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            summary = result['scan_summary']
            return f"""
扫描完成! 结果已保存到 {output_file}

扫描摘要:
- 发现 {summary['total_agents']} 个 agents
- 发现 {summary['total_tools']} 个 tools  
- 发现 {summary['total_crews']} 个 crews
- 发现 {summary['total_tasks']} 个 tasks
- 总共扫描 {summary['total_files']} 个文件

详细结果请查看 {output_file} 文件。
            """
        except Exception as e:
            return f"扫描失败: {str(e)}"


class FileScanTool(BaseTool):
    """扫描单个文件中agent系统的工具"""
    name: str = "file_scanner"
    description: str = "扫描指定文件，分析其中的agent系统结构，识别agents、tools等组件"
    args_schema: Type[BaseModel] = FileScanInput

    def _run(self, file_path: str, output_file: str = "scan_result.json") -> str:
        try:
            scanner = AgentSystemScanner()
            result = scanner.scan_file(file_path)
            
            # 保存结果到JSON文件
            output_path = Path(output_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            summary = result['scan_summary']
            return f"""
扫描完成! 结果已保存到 {output_file}

扫描摘要:
- 发现 {summary['total_agents']} 个 agents
- 发现 {summary['total_tools']} 个 tools  
- 发现 {summary['total_crews']} 个 crews
- 发现 {summary['total_tasks']} 个 tasks

详细结果请查看 {output_file} 文件。
            """
        except Exception as e:
            return f"扫描失败: {str(e)}"


class ReportAnalysisTool(BaseTool):
    """分析扫描报告的工具"""
    name: str = "report_analyzer"
    description: str = "分析扫描结果JSON文件，提供详细的agent系统架构分析"
    
    class ReportAnalysisInput(BaseModel):
        report_file: str = Field(..., description="扫描结果JSON文件路径")
    
    args_schema: Type[BaseModel] = ReportAnalysisInput

    def _run(self, report_file: str) -> str:
        try:
            with open(report_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            analysis = []
            analysis.append("=== Agent系统架构分析 ===\n")
            
            # 分析agents
            if data['agents']:
                analysis.append("🤖 发现的Agents:")
                for agent in data['agents']:
                    analysis.append(f"  - {agent['name']} ({agent['type']}) - {agent['file']}")
                    if 'arguments' in agent and agent['arguments']:
                        for key, value in agent['arguments'].items():
                            analysis.append(f"    {key}: {value}")
                analysis.append("")
            
            # 分析tools
            if data['tools']:
                analysis.append("🔧 发现的Tools:")
                for tool in data['tools']:
                    analysis.append(f"  - {tool['name']} ({tool['type']}) - {tool['file']}")
                    if 'arguments' in tool and tool['arguments']:
                        for key, value in tool['arguments'].items():
                            analysis.append(f"    {key}: {value}")
                analysis.append("")
            
            # 分析crews
            if data['crews']:
                analysis.append("👥 发现的Crews:")
                for crew in data['crews']:
                    analysis.append(f"  - {crew['name']} ({crew['type']}) - {crew['file']}")
                analysis.append("")
            
            # 分析tasks
            if data['tasks']:
                analysis.append("📋 发现的Tasks:")
                for task in data['tasks']:
                    analysis.append(f"  - {task['name']} ({task['type']}) - {task['file']}")
                analysis.append("")
            
            # 文件结构分析
            analysis.append("📁 文件结构:")
            for file_path, file_info in data['file_structure'].items():
                if file_info['type'] == 'file' and file_path.endswith('.py'):
                    analysis.append(f"  - {file_path} ({file_info['size']} bytes)")
            
            return "\n".join(analysis)
            
        except Exception as e:
            return f"分析报告失败: {str(e)}"
