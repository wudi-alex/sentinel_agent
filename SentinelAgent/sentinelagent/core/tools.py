from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import json
from pathlib import Path
from .scanner import AgentSystemScanner
from .log_analyzer import ExecutionLogAnalyzer


class DirectoryScanInput(BaseModel):
    directory_path: str = Field(..., description="Directory path to scan")
    output_file: str = Field(default="scan_result.json", description="Output file name")


class FileScanInput(BaseModel):
    file_path: str = Field(..., description="File path to scan")
    output_file: str = Field(default="scan_result.json", description="Output file name")


class DirectoryScanTool(BaseTool):
    """Directory scan tool"""
    name: str = "directory_scanner"
    description: str = "Scan agent system components in directory"
    args_schema: Type[BaseModel] = DirectoryScanInput

    def _run(self, directory_path: str, output_file: str = "scan_result.json") -> str:
        try:
            scanner = AgentSystemScanner()
            result = scanner.scan_directory(directory_path)
            
            # Save result
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            summary = result['scan_summary']
            return f"Scan completed: {summary['total_agents']} agents, {summary['total_tools']} tools"
        
        except Exception as e:
            return f"Scan failed: {e}"


class FileScanTool(BaseTool):
    """File scan tool"""
    name: str = "file_scanner"
    description: str = "Scan agent components in a single file"
    args_schema: Type[BaseModel] = FileScanInput

    def _run(self, file_path: str, output_file: str = "scan_result.json") -> str:
        try:
            scanner = AgentSystemScanner()
            result = scanner.scan_file(file_path)
            
            # saveresult
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            summary = result['scan_summary']
            return f"文件扫描完成: {summary['total_agents']} agents, {summary['total_tools']} tools"
        
        except Exception as e:
            return f"扫描失败: {e}"
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
    """scan单个file中agentsystem的tool"""
    name: str = "file_scanner"
    description: str = "扫描指定文件，分析其中的agent系统结构，识别agents、tools等组件"
    args_schema: Type[BaseModel] = FileScanInput

    def _run(self, file_path: str, output_file: str = "scan_result.json") -> str:
        try:
            scanner = AgentSystemScanner()
            result = scanner.scan_file(file_path)
            
            # saveresult到JSONfile
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
    """analyzescanreport的tool"""
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
            
            # analyzeagents
            if data['agents']:
                analysis.append("🤖 发现的Agents:")
                for agent in data['agents']:
                    analysis.append(f"  - {agent['name']} ({agent['type']}) - {agent['file']}")
                    if 'arguments' in agent and agent['arguments']:
                        for key, value in agent['arguments'].items():
                            analysis.append(f"    {key}: {value}")
                analysis.append("")
            
            # analyzetools
            if data['tools']:
                analysis.append("🔧 发现的Tools:")
                for tool in data['tools']:
                    analysis.append(f"  - {tool['name']} ({tool['type']}) - {tool['file']}")
                    if 'arguments' in tool and tool['arguments']:
                        for key, value in tool['arguments'].items():
                            analysis.append(f"    {key}: {value}")
                analysis.append("")
            
            # analyzecrews
            if data['crews']:
                analysis.append("👥 发现的Crews:")
                for crew in data['crews']:
                    analysis.append(f"  - {crew['name']} ({crew['type']}) - {crew['file']}")
                analysis.append("")
            
            # analyzetasks
            if data['tasks']:
                analysis.append("📋 发现的Tasks:")
                for task in data['tasks']:
                    analysis.append(f"  - {task['name']} ({task['type']}) - {task['file']}")
                analysis.append("")
            
            # file结构analyze
            analysis.append("📁 文件结构:")
            for file_path, file_info in data['file_structure'].items():
                if file_info['type'] == 'file' and file_path.endswith('.py'):
                    analysis.append(f"  - {file_path} ({file_info['size']} bytes)")
            
            return "\n".join(analysis)
            
        except Exception as e:
            return f"分析报告失败: {str(e)}"


class LogAnalysisInput(BaseModel):
    log_file_path: str = Field(..., description="要分析的日志文件路径")
    log_format: str = Field(default="auto", description="日志格式 (csv/txt/auto)")
    output_file: str = Field(default="", description="分析结果输出文件 (可选)")


class LogAnalysisTool(BaseTool):
    """execution日志analyzetool"""
    name: str = "log_analyzer"
    description: str = "分析Agent系统的执行日志，检测错误和异常模式"
    args_schema: Type[BaseModel] = LogAnalysisInput

    def _run(self, log_file_path: str, log_format: str = "auto", output_file: str = "") -> str:
        try:
            if not Path(log_file_path).exists():
                return f"❌ 错误: 日志文件不存在 '{log_file_path}'"
            
            # createanalyze器
            analyzer = ExecutionLogAnalyzer()
            
            # analyze日志
            analysis_result = analyzer.analyze_log_file(log_file_path, log_format)
            
            # buildresultreport
            report_lines = []
            report_lines.append("=== 执行日志分析报告 ===\n")
            
            # 基本统计
            stats = analysis_result.statistics
            report_lines.append("📊 基本统计:")
            report_lines.append(f"  - 执行路径: {len(analysis_result.execution_paths)}")
            report_lines.append(f"  - 错误数量: {len(analysis_result.errors)}")
            report_lines.append(f"  - 警告数量: {len(analysis_result.warnings)}")
            report_lines.append(f"  - 日志条目: {stats.get('total_entries', 0)}")
            report_lines.append(f"  - 活跃Agents: {stats.get('active_agents', 0)}")
            report_lines.append("")
            
            # 错误information
            if analysis_result.errors:
                report_lines.append("❌ 发现的错误:")
                for i, error in enumerate(analysis_result.errors[:10], 1):  # 最多显示10个
                    report_lines.append(f"  {i}. {error.error_type} ({error.severity.value.upper()})")
                    report_lines.append(f"     节点: {error.node_or_edge}")
                    report_lines.append(f"     描述: {error.description}")
                    if error.suggested_fix:
                        report_lines.append(f"     建议: {error.suggested_fix}")
                    report_lines.append("")
                
                if len(analysis_result.errors) > 10:
                    report_lines.append(f"  ... 还有 {len(analysis_result.errors) - 10} 个错误")
                report_lines.append("")
            
            # 警告information
            if analysis_result.warnings:
                report_lines.append("⚠️  警告信息:")
                for i, warning in enumerate(analysis_result.warnings[:5], 1):
                    report_lines.append(f"  {i}. {warning}")
                if len(analysis_result.warnings) > 5:
                    report_lines.append(f"  ... 还有 {len(analysis_result.warnings) - 5} 个警告")
                report_lines.append("")
            
            # 改进建议
            if analysis_result.recommendations:
                report_lines.append("💡 改进建议:")
                for i, rec in enumerate(analysis_result.recommendations[:5], 1):
                    report_lines.append(f"  {i}. {rec}")
                if len(analysis_result.recommendations) > 5:
                    report_lines.append(f"  ... 还有 {len(analysis_result.recommendations) - 5} 个建议")
                report_lines.append("")
            
            # executionpath概览
            if analysis_result.execution_paths:
                report_lines.append("🛣️  执行路径概览:")
                for i, path in enumerate(analysis_result.execution_paths[:3], 1):
                    report_lines.append(f"  路径 {i}: {path.path_id}")
                    report_lines.append(f"    节点数: {len(path.nodes)}")
                    report_lines.append(f"    状态: {path.status}")
                    if path.start_time and path.end_time:
                        duration = path.end_time - path.start_time
                        report_lines.append(f"    耗时: {duration}")
                    report_lines.append("")
            
            # 总结
            if analysis_result.summary:
                report_lines.append("📋 分析总结:")
                report_lines.append(f"  {analysis_result.summary}")
                report_lines.append("")
            
            # savedetailedresult
            if output_file:
                analysis_dict = {
                    'execution_paths': [
                        {
                            'path_id': path.path_id,
                            'nodes': path.nodes,
                            'edges': path.edges,
                            'start_time': path.start_time.isoformat() if path.start_time else None,
                            'end_time': path.end_time.isoformat() if path.end_time else None,
                            'status': path.status,
                            'log_entries_count': len(path.log_entries)
                        }
                        for path in analysis_result.execution_paths
                    ],
                    'errors': [
                        {
                            'error_type': error.error_type,
                            'severity': error.severity.value,
                            'description': error.description,
                            'node_or_edge': error.node_or_edge,
                            'suggested_fix': error.suggested_fix,
                            'context': error.context
                        }
                        for error in analysis_result.errors
                    ],
                    'warnings': analysis_result.warnings,
                    'statistics': analysis_result.statistics,
                    'recommendations': analysis_result.recommendations,
                    'summary': analysis_result.summary
                }
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(analysis_dict, f, indent=2, ensure_ascii=False)
                
                report_lines.append(f"💾 详细分析结果已保存到: {output_file}")
            
            return "\n".join(report_lines)
            
        except Exception as e:
            return f"日志分析失败: {str(e)}"
