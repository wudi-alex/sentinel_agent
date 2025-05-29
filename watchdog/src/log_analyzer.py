"""
执行日志分析器 - 分析Agent系统的执行日志并检测异常

此模块提供对Magentic-One等Agent系统执行日志的深度分析功能：
- 解析CSV和TXT格式的执行日志
- 匹配执行路径到系统架构图
- 验证节点输入输出符合性
- 识别执行错误和异常模式
- 生成详细的分析报告

主要类：
- ExecutionLogAnalyzer: 主分析器类
- LogEntry: 日志条目数据结构
- ExecutionPath: 执行路径表示
- AnalysisResult: 分析结果容器
"""

import re
import json
import csv
import ast
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import pandas as pd

class LogEntryType(Enum):
    """日志条目类型枚举"""
    USER_INPUT = "user_input"
    AGENT_RESPONSE = "agent_response"
    TOOL_CALL = "tool_call"
    ERROR = "error"
    SYSTEM_MESSAGE = "system_message"
    ORCHESTRATOR = "orchestrator"

class ErrorSeverity(Enum):
    """错误严重程度枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class LogEntry:
    """日志条目数据结构"""
    timestamp: Optional[datetime] = None
    agent_name: str = ""
    message_type: LogEntryType = LogEntryType.SYSTEM_MESSAGE
    content: str = ""
    role: str = ""
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    tools_used: List[str] = field(default_factory=list)
    raw_data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ExecutionPath:
    """执行路径表示"""
    path_id: str
    nodes: List[str] = field(default_factory=list)
    edges: List[Tuple[str, str]] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: str = "unknown"
    log_entries: List[LogEntry] = field(default_factory=list)

@dataclass
class ErrorInfo:
    """错误信息"""
    error_type: str
    severity: ErrorSeverity
    description: str
    node_or_edge: str
    suggested_fix: str = ""
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AnalysisResult:
    """分析结果容器"""
    execution_paths: List[ExecutionPath] = field(default_factory=list)
    errors: List[ErrorInfo] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    statistics: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    summary: str = ""

class ExecutionLogAnalyzer:
    """执行日志分析器主类"""
    
    def __init__(self, system_graph: Optional[Dict] = None):
        """
        初始化执行日志分析器
        
        Args:
            system_graph: 系统架构图，用于路径匹配
        """
        self.system_graph = system_graph or {}
        self.logger = logging.getLogger(__name__)
        self.agent_patterns = self._load_agent_patterns()
        
    def _load_agent_patterns(self) -> Dict[str, Dict]:
        """加载Agent模式定义"""
        return {
            "MagenticOneOrchestrator": {
                "role": "协调器",
                "expected_inputs": ["user_request", "team_status"],
                "expected_outputs": ["task_assignment", "progress_check"],
                "keywords": ["plan", "team", "request", "progress"]
            },
            "FileSurfer": {
                "role": "文件处理器",
                "expected_inputs": ["file_path", "operation_type"],
                "expected_outputs": ["file_content", "operation_result"],
                "keywords": ["file", "open", "read", "path"]
            },
            "Coder": {
                "role": "代码生成器",
                "expected_inputs": ["code_requirement", "language"],
                "expected_outputs": ["generated_code", "explanation"],
                "keywords": ["code", "script", "python", "generate"]
            },
            "Executor": {
                "role": "代码执行器",
                "expected_inputs": ["code_to_execute"],
                "expected_outputs": ["execution_result", "output"],
                "keywords": ["execute", "run", "result", "output"]
            },
            "web_surfer": {
                "role": "网页浏览器",
                "expected_inputs": ["url", "action"],
                "expected_outputs": ["page_content", "action_result"],
                "keywords": ["website", "url", "browser", "page"]
            }
        }
    
    def analyze_log_file(self, log_file_path: str, file_type: str = "auto") -> AnalysisResult:
        """
        分析日志文件
        
        Args:
            log_file_path: 日志文件路径
            file_type: 文件类型 ("csv", "txt", "auto")
            
        Returns:
            AnalysisResult: 分析结果
        """
        try:
            # 自动检测文件类型
            if file_type == "auto":
                file_type = self._detect_file_type(log_file_path)
            
            # 解析日志文件
            log_entries = self._parse_log_file(log_file_path, file_type)
            
            # 提取执行路径
            execution_paths = self._extract_execution_paths(log_entries)
            
            # 分析每个路径
            errors = []
            warnings = []
            
            for path in execution_paths:
                path_errors, path_warnings = self._analyze_execution_path(path)
                errors.extend(path_errors)
                warnings.extend(path_warnings)
            
            # 生成统计信息
            statistics = self._generate_statistics(log_entries, execution_paths, errors)
            
            # 生成建议
            recommendations = self._generate_recommendations(errors, warnings)
            
            # 生成摘要
            summary = self._generate_summary(execution_paths, errors, statistics)
            
            return AnalysisResult(
                execution_paths=execution_paths,
                errors=errors,
                warnings=warnings,
                statistics=statistics,
                recommendations=recommendations,
                summary=summary
            )
            
        except Exception as e:
            self.logger.error(f"分析日志文件时发生错误: {e}")
            raise
    
    def _detect_file_type(self, file_path: str) -> str:
        """检测文件类型"""
        if file_path.endswith('.csv'):
            return "csv"
        elif file_path.endswith('.txt') or file_path.endswith('.log'):
            return "txt"
        else:
            # 通过文件内容检测
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if ',' in first_line and ('input_messages' in first_line or 'role' in first_line):
                        return "csv"
                    else:
                        return "txt"
            except:
                return "txt"
    
    def _parse_log_file(self, file_path: str, file_type: str) -> List[LogEntry]:
        """解析日志文件"""
        if file_type == "csv":
            return self._parse_csv_log(file_path)
        else:
            return self._parse_txt_log(file_path)
    
    def _parse_csv_log(self, file_path: str) -> List[LogEntry]:
        """解析CSV格式日志"""
        log_entries = []
        
        try:
            df = pd.read_csv(file_path)
            
            for _, row in df.iterrows():
                entry = LogEntry()
                entry.raw_data = row.to_dict()
                
                # 解析输入消息
                if 'input_messages' in row and pd.notna(row['input_messages']):
                    try:
                        input_msgs = ast.literal_eval(row['input_messages'])
                        if input_msgs:
                            first_msg = input_msgs[0] if isinstance(input_msgs, list) else input_msgs
                            entry.content = first_msg.get('content', '')
                            entry.role = first_msg.get('role', '')
                            entry.agent_name = first_msg.get('name', 'unknown')
                    except:
                        entry.content = str(row['input_messages'])
                
                # 解析输出消息
                if 'output_messages' in row and pd.notna(row['output_messages']):
                    try:
                        output_msgs = ast.literal_eval(row['output_messages'])
                        if output_msgs:
                            entry.output_data = output_msgs[0] if isinstance(output_msgs, list) else output_msgs
                    except:
                        entry.output_data = {'content': str(row['output_messages'])}
                
                # 解析工具
                if 'input_tools' in row and pd.notna(row['input_tools']):
                    try:
                        tools = ast.literal_eval(row['input_tools'])
                        if isinstance(tools, list):
                            entry.tools_used = [tool.get('function', {}).get('name', '') for tool in tools]
                    except:
                        pass
                
                # 设置消息类型
                entry.message_type = self._determine_message_type(entry)
                
                log_entries.append(entry)
                
        except Exception as e:
            self.logger.error(f"解析CSV日志文件失败: {e}")
            raise
        
        return log_entries
    
    def _parse_txt_log(self, file_path: str) -> List[LogEntry]:
        """解析TXT格式日志"""
        log_entries = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 按分隔符拆分消息，使用正确的正则表达式
            parts = re.split(r'---------- [^-]+ ----------', content)
            
            # 提取所有分隔符（包含agent信息）
            separators = re.findall(r'---------- ([^-]+) ----------', content)
            
            # 配对内容和agent信息
            for i, part in enumerate(parts):
                if not part.strip():
                    continue
                
                entry = LogEntry()
                entry.content = part.strip()
                
                # 从分隔符中提取agent信息
                if i > 0 and i - 1 < len(separators):
                    separator_text = separators[i - 1].strip()
                    
                    # 解析 "TextMessage (agent_name)" 格式
                    agent_match = re.search(r'\(([^)]+)\)', separator_text)
                    if agent_match:
                        entry.agent_name = agent_match.group(1)
                    
                    # 判断消息类型
                    if 'TextMessage' in separator_text:
                        entry.message_type = LogEntryType.AGENT_RESPONSE
                    elif 'MultiModalMessage' in separator_text:
                        entry.message_type = LogEntryType.TOOL_CALL
                    else:
                        entry.message_type = LogEntryType.SYSTEM_MESSAGE
                
                # 检测消息类型
                if not entry.message_type or entry.message_type == LogEntryType.SYSTEM_MESSAGE:
                    entry.message_type = self._determine_message_type(entry)
                
                # 提取时间戳（从文件名中提取）
                time_match = re.search(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', file_path)
                if time_match:
                    try:
                        base_time = datetime.strptime(time_match.group(1), '%Y-%m-%d_%H-%M-%S')
                        # 为每个条目添加偏移时间
                        entry.timestamp = base_time.replace(second=base_time.second + i)
                    except:
                        pass
                
                log_entries.append(entry)
                
        except Exception as e:
            self.logger.error(f"解析TXT日志文件失败: {e}")
            raise
        
        return log_entries
    
    def _determine_message_type(self, entry: LogEntry) -> LogEntryType:
        """确定消息类型"""
        content = entry.content.lower()
        agent_name = entry.agent_name.lower()
        
        if 'user' in agent_name or entry.role == 'user':
            return LogEntryType.USER_INPUT
        elif 'orchestrator' in agent_name or 'coordinator' in agent_name:
            return LogEntryType.ORCHESTRATOR
        elif 'error' in content or 'exception' in content or 'failed' in content or 'traceback' in content:
            return LogEntryType.ERROR
        elif entry.tools_used or entry.message_type == LogEntryType.TOOL_CALL:
            return LogEntryType.TOOL_CALL
        else:
            return LogEntryType.AGENT_RESPONSE
    
    def _extract_execution_paths(self, log_entries: List[LogEntry]) -> List[ExecutionPath]:
        """提取执行路径"""
        paths = []
        current_path = None
        path_counter = 0
        
        for entry in log_entries:
            # 检测新路径的开始（用户输入或第一个来自user的消息通常是新任务的开始）
            if (entry.message_type == LogEntryType.USER_INPUT or 
                (entry.agent_name.lower() == 'user' and current_path is None)):
                
                if current_path:
                    paths.append(current_path)
                
                path_counter += 1
                current_path = ExecutionPath(
                    path_id=f"path_{path_counter}",
                    start_time=entry.timestamp
                )
                # 修正第一个用户消息的类型
                if entry.agent_name.lower() == 'user':
                    entry.message_type = LogEntryType.USER_INPUT
            
            if current_path:
                current_path.log_entries.append(entry)
                
                # 添加节点
                if entry.agent_name and entry.agent_name not in current_path.nodes:
                    current_path.nodes.append(entry.agent_name)
                
                # 添加边（agent间的调用关系）
                if len(current_path.log_entries) > 1:
                    prev_entry = current_path.log_entries[-2]
                    if prev_entry.agent_name != entry.agent_name:
                        edge = (prev_entry.agent_name, entry.agent_name)
                        if edge not in current_path.edges:
                            current_path.edges.append(edge)
                
                # 更新结束时间
                if entry.timestamp:
                    current_path.end_time = entry.timestamp
        
        # 添加最后一个路径
        if current_path:
            paths.append(current_path)
        
        # 如果没有找到明确的用户输入，将所有条目作为一个路径
        if not paths and log_entries:
            current_path = ExecutionPath(
                path_id="path_1",
                start_time=log_entries[0].timestamp if log_entries[0].timestamp else None
            )
            current_path.log_entries = log_entries
            
            # 提取所有唯一的agent名称作为节点
            for entry in log_entries:
                if entry.agent_name and entry.agent_name not in current_path.nodes:
                    current_path.nodes.append(entry.agent_name)
            
            # 构建边
            for i in range(1, len(log_entries)):
                prev_agent = log_entries[i-1].agent_name
                curr_agent = log_entries[i].agent_name
                if prev_agent != curr_agent:
                    edge = (prev_agent, curr_agent)
                    if edge not in current_path.edges:
                        current_path.edges.append(edge)
            
            if log_entries[-1].timestamp:
                current_path.end_time = log_entries[-1].timestamp
            
            paths.append(current_path)
        
        return paths
    
    def _analyze_execution_path(self, path: ExecutionPath) -> Tuple[List[ErrorInfo], List[str]]:
        """分析单个执行路径"""
        errors = []
        warnings = []
        
        # 分析节点合规性
        for entry in path.log_entries:
            node_errors, node_warnings = self._analyze_node_compliance(entry)
            errors.extend(node_errors)
            warnings.extend(node_warnings)
        
        # 分析路径完整性
        path_errors, path_warnings = self._analyze_path_completeness(path)
        errors.extend(path_errors)
        warnings.extend(path_warnings)
        
        # 分析错误模式
        pattern_errors = self._detect_error_patterns(path)
        errors.extend(pattern_errors)
        
        return errors, warnings
    
    def _analyze_node_compliance(self, entry: LogEntry) -> Tuple[List[ErrorInfo], List[str]]:
        """分析节点合规性"""
        errors = []
        warnings = []
        
        agent_name = entry.agent_name
        if agent_name in self.agent_patterns:
            pattern = self.agent_patterns[agent_name]
            
            # 检查关键词
            content_lower = entry.content.lower()
            expected_keywords = pattern.get('keywords', [])
            
            found_keywords = [kw for kw in expected_keywords if kw in content_lower]
            
            if not found_keywords:
                warnings.append(
                    f"{agent_name} 的输出中未找到预期关键词: {expected_keywords}"
                )
            
            # 检查角色一致性
            role = pattern.get('role', '')
            if 'error' in content_lower and agent_name != 'error_handler':
                errors.append(ErrorInfo(
                    error_type="role_violation",
                    severity=ErrorSeverity.MEDIUM,
                    description=f"{agent_name} ({role}) 产生了错误消息",
                    node_or_edge=agent_name,
                    suggested_fix="检查agent实现和错误处理机制"
                ))
        
        return errors, warnings
    
    def _analyze_path_completeness(self, path: ExecutionPath) -> Tuple[List[ErrorInfo], List[str]]:
        """分析路径完整性"""
        errors = []
        warnings = []
        
        # 检查是否有错误条目
        error_entries = [e for e in path.log_entries if e.message_type == LogEntryType.ERROR]
        
        if error_entries:
            for error_entry in error_entries:
                errors.append(ErrorInfo(
                    error_type="execution_error",
                    severity=ErrorSeverity.HIGH,
                    description=f"执行过程中发生错误: {error_entry.content[:200]}...",
                    node_or_edge=error_entry.agent_name,
                    suggested_fix="检查错误原因并修复相关代码"
                ))
        
        # 检查路径是否完整（有开始有结束）
        if not path.log_entries:
            errors.append(ErrorInfo(
                error_type="empty_path",
                severity=ErrorSeverity.MEDIUM,
                description="执行路径为空",
                node_or_edge="path",
                suggested_fix="检查日志记录机制"
            ))
        
        # 检查是否有未完成的任务
        last_entry = path.log_entries[-1] if path.log_entries else None
        if last_entry and 'incomplete' in last_entry.content.lower():
            warnings.append("执行路径可能未完成")
        
        return errors, warnings
    
    def _detect_error_patterns(self, path: ExecutionPath) -> List[ErrorInfo]:
        """检测错误模式"""
        errors = []
        
        # 检测循环调用
        agent_sequence = [entry.agent_name for entry in path.log_entries if entry.agent_name]
        
        for i in range(len(agent_sequence) - 2):
            if i + 3 <= len(agent_sequence):
                window = agent_sequence[i:i+3]
                if len(set(window)) == 1:  # 同一个agent连续调用3次
                    errors.append(ErrorInfo(
                        error_type="infinite_loop",
                        severity=ErrorSeverity.HIGH,
                        description=f"检测到可能的无限循环: {window[0]} 连续执行",
                        node_or_edge=window[0],
                        suggested_fix="检查agent逻辑，防止无限循环"
                    ))
        
        # 检测权限错误
        for entry in path.log_entries:
            if 'access denied' in entry.content.lower() or 'permission' in entry.content.lower():
                errors.append(ErrorInfo(
                    error_type="permission_error",
                    severity=ErrorSeverity.HIGH,
                    description="检测到权限相关错误",
                    node_or_edge=entry.agent_name,
                    suggested_fix="检查文件权限和访问控制设置"
                ))
        
        return errors
    
    def _generate_statistics(self, log_entries: List[LogEntry], 
                           execution_paths: List[ExecutionPath], 
                           errors: List[ErrorInfo]) -> Dict[str, Any]:
        """生成统计信息"""
        agent_usage = {}
        message_types = {}
        
        for entry in log_entries:
            # 统计agent使用情况
            if entry.agent_name:
                agent_usage[entry.agent_name] = agent_usage.get(entry.agent_name, 0) + 1
            
            # 统计消息类型
            msg_type = entry.message_type.value
            message_types[msg_type] = message_types.get(msg_type, 0) + 1
        
        error_by_severity = {}
        for error in errors:
            severity = error.severity.value
            error_by_severity[severity] = error_by_severity.get(severity, 0) + 1
        
        return {
            "total_log_entries": len(log_entries),
            "total_execution_paths": len(execution_paths),
            "total_errors": len(errors),
            "agent_usage": agent_usage,
            "message_types": message_types,
            "error_by_severity": error_by_severity,
            "most_active_agent": max(agent_usage, key=agent_usage.get) if agent_usage else None
        }
    
    def _generate_recommendations(self, errors: List[ErrorInfo], warnings: List[str]) -> List[str]:
        """生成建议"""
        recommendations = []
        
        # 基于错误类型生成建议
        error_types = [error.error_type for error in errors]
        
        if "infinite_loop" in error_types:
            recommendations.append("建议: 在agent逻辑中添加循环检测和中断机制")
        
        if "permission_error" in error_types:
            recommendations.append("建议: 检查文件系统权限和访问控制配置")
        
        if "execution_error" in error_types:
            recommendations.append("建议: 加强错误处理和异常捕获机制")
        
        if len(warnings) > 5:
            recommendations.append("建议: 关注警告信息，优化agent行为模式")
        
        # 基于错误严重程度生成建议
        critical_errors = [e for e in errors if e.severity == ErrorSeverity.CRITICAL]
        if critical_errors:
            recommendations.append("紧急: 发现严重错误，建议立即修复")
        
        return recommendations
    
    def _generate_summary(self, execution_paths: List[ExecutionPath], 
                         errors: List[ErrorInfo], 
                         statistics: Dict[str, Any]) -> str:
        """生成分析摘要"""
        total_paths = len(execution_paths)
        total_errors = len(errors)
        error_rate = (total_errors / total_paths * 100) if total_paths > 0 else 0
        
        critical_errors = len([e for e in errors if e.severity == ErrorSeverity.CRITICAL])
        high_errors = len([e for e in errors if e.severity == ErrorSeverity.HIGH])
        
        summary = f"""
        执行日志分析摘要:
        
        总体情况:
        - 分析了 {total_paths} 个执行路径
        - 发现 {total_errors} 个错误 (错误率: {error_rate:.1f}%)
        - 其中严重错误 {critical_errors} 个，高级错误 {high_errors} 个
        
        主要活跃Agent: {statistics.get('most_active_agent', 'N/A')}
        
        建议: {'立即关注严重错误' if critical_errors > 0 else '系统运行基本正常，关注优化建议'}
        """
        
        return summary.strip()
    
    def generate_report(self, analysis_result: AnalysisResult, output_path: str = None) -> str:
        """生成详细报告"""
        report_lines = []
        
        # 标题
        report_lines.append("# 执行日志分析报告")
        report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # 摘要
        report_lines.append("## 分析摘要")
        report_lines.append(analysis_result.summary)
        report_lines.append("")
        
        # 统计信息
        report_lines.append("## 统计信息")
        for key, value in analysis_result.statistics.items():
            report_lines.append(f"- {key}: {value}")
        report_lines.append("")
        
        # 错误详情
        if analysis_result.errors:
            report_lines.append("## 错误详情")
            for i, error in enumerate(analysis_result.errors, 1):
                report_lines.append(f"### 错误 {i}")
                report_lines.append(f"- 类型: {error.error_type}")
                report_lines.append(f"- 严重程度: {error.severity.value}")
                report_lines.append(f"- 位置: {error.node_or_edge}")
                report_lines.append(f"- 描述: {error.description}")
                report_lines.append(f"- 建议修复: {error.suggested_fix}")
                report_lines.append("")
        
        # 执行路径
        report_lines.append("## 执行路径")
        for i, path in enumerate(analysis_result.execution_paths, 1):
            report_lines.append(f"### 路径 {i} ({path.path_id})")
            report_lines.append(f"- 节点: {' -> '.join(path.nodes)}")
            report_lines.append(f"- 日志条目数: {len(path.log_entries)}")
            if path.start_time:
                report_lines.append(f"- 开始时间: {path.start_time}")
            if path.end_time:
                report_lines.append(f"- 结束时间: {path.end_time}")
            report_lines.append("")
        
        # 建议
        if analysis_result.recommendations:
            report_lines.append("## 优化建议")
            for rec in analysis_result.recommendations:
                report_lines.append(f"- {rec}")
            report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        # 保存到文件
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
        
        return report_content


def main():
    """主函数 - 用于测试"""
    analyzer = ExecutionLogAnalyzer()
    
    # 示例使用
    log_file = "/path/to/log/file.csv"  # 替换为实际路径
    result = analyzer.analyze_log_file(log_file)
    
    # 生成报告
    report = analyzer.generate_report(result, "execution_analysis_report.md")
    print("分析完成，报告已生成")


if __name__ == "__main__":
    main()
