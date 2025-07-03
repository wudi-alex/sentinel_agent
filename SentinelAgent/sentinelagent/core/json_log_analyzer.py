#!/usr/bin/env python3
"""
JSON Log Analyzer for SentinelAgent
统一的JSON日志分析器，支持CrewAI和MagneticOne/AutoGen格式
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

from .log_analyzer import (
    LogEntry, LogEntryType, ExecutionPath, ErrorInfo, ErrorSeverity,
    AnalysisResult, PathStatus
)


class JSONLogAnalyzer:
    """统一的JSON日志分析器"""
    
    def __init__(self, system_graph: Optional[Dict] = None):
        """
        初始化JSON日志分析器
        
        Args:
            system_graph: 系统架构图，用于路径匹配
        """
        self.system_graph = system_graph or {}
        self.logger = logging.getLogger(__name__)
        
    def analyze_json_log(self, json_file_path: str) -> AnalysisResult:
        """
        分析JSON格式的日志文件
        
        Args:
            json_file_path: JSON日志文件路径
            
        Returns:
            AnalysisResult: 分析结果
        """
        try:
            # 读取JSON文件
            with open(json_file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # 验证JSON格式
            if not self._validate_json_format(json_data):
                raise ValueError("Invalid JSON log format")
            
            # 检测格式类型
            format_type = self._detect_format_type(json_data)
            self.logger.info(f"Detected format type: {format_type}")
            
            # 解析日志条目
            log_entries = self._parse_json_log_entries(json_data, format_type)
            
            # 提取执行路径
            execution_paths = self._extract_execution_paths(log_entries)
            
            # 分析执行路径
            all_errors = []
            all_warnings = []
            
            for path in execution_paths:
                errors, warnings = self._analyze_execution_path(path, format_type)
                all_errors.extend(errors)
                all_warnings.extend(warnings)
            
            # 生成统计信息
            statistics = self._generate_statistics(log_entries, execution_paths, all_errors, format_type)
            
            # 生成建议
            recommendations = self._generate_recommendations(all_errors, all_warnings, statistics, format_type)
            
            # 生成摘要
            summary = self._generate_summary(log_entries, execution_paths, all_errors, format_type)
            
            return AnalysisResult(
                log_entries=log_entries,
                execution_paths=execution_paths,
                errors=all_errors,
                warnings=all_warnings,
                statistics=statistics,
                recommendations=recommendations,
                summary=summary
            )
            
        except Exception as e:
            self.logger.error(f"Failed to analyze JSON log: {e}")
            raise
    
    def _validate_json_format(self, json_data: Dict) -> bool:
        """验证JSON格式"""
        return (
            isinstance(json_data, dict) and
            'execution_log' in json_data and
            'metadata' in json_data and
            isinstance(json_data['execution_log'], list)
        )
    
    def _detect_format_type(self, json_data: Dict) -> str:
        """检测格式类型"""
        metadata = json_data.get('metadata', {})
        
        # 检查转换器版本信息
        if 'converter_version' in metadata:
            return 'converted'
        
        # 检查第一个执行条目的结构
        execution_log = json_data.get('execution_log', [])
        if not execution_log:
            return 'unknown'
        
        first_entry = execution_log[0]
        
        # CrewAI格式特征
        if 'agent' in first_entry and 'task' in first_entry:
            agent_info = first_entry['agent']
            if isinstance(agent_info, dict) and ('role' in agent_info or 'goal' in agent_info):
                return 'crewai'
        
        # MagneticOne格式特征
        if 'agent' in first_entry and 'input' in first_entry:
            agent_info = first_entry['agent']
            if isinstance(agent_info, dict) and 'name' in agent_info:
                agent_name = agent_info['name']
                if any(keyword in agent_name.lower() for keyword in ['orchestrator', 'coder', 'executor', 'filesurfer']):
                    return 'magneticone'
        
        return 'unknown'
    
    def _parse_json_log_entries(self, json_data: Dict, format_type: str) -> List[LogEntry]:
        """解析JSON日志条目"""
        log_entries = []
        execution_log = json_data.get('execution_log', [])
        
        for entry_data in execution_log:
            entry = LogEntry()
            
            # 通用字段
            entry.timestamp = self._parse_timestamp(entry_data.get('timestamp'))
            entry.raw_data = entry_data
            
            # 根据格式类型解析特定字段
            if format_type == 'crewai':
                self._parse_crewai_entry(entry, entry_data)
            elif format_type == 'magneticone':
                self._parse_magneticone_entry(entry, entry_data)
            else:
                # 通用解析
                self._parse_generic_entry(entry, entry_data)
            
            # 设置消息类型
            entry.message_type = self._determine_message_type(entry, format_type)
            
            log_entries.append(entry)
        
        return log_entries
    
    def _parse_crewai_entry(self, entry: LogEntry, entry_data: Dict):
        """解析CrewAI格式条目"""
        # Agent信息
        agent_info = entry_data.get('agent', {})
        if isinstance(agent_info, dict):
            entry.agent_name = agent_info.get('role', 'unknown')
            entry.role = agent_info.get('role', '')
        
        # Task信息
        task_info = entry_data.get('task', {})
        if isinstance(task_info, dict):
            entry.content = task_info.get('description', '')
        
        # 输入输出信息
        input_info = entry_data.get('input', {})
        output_info = entry_data.get('output', {})
        
        if isinstance(input_info, dict):
            entry.input_data = input_info
        
        if isinstance(output_info, dict):
            entry.output_data = output_info
            if 'raw' in output_info:
                if entry.content:
                    entry.content += f"\n\nOutput: {output_info['raw']}"
                else:
                    entry.content = str(output_info['raw'])
        
        # 工具信息
        tools = entry_data.get('tools', [])
        if isinstance(tools, list):
            entry.tools_used = [str(tool) for tool in tools]
    
    def _parse_magneticone_entry(self, entry: LogEntry, entry_data: Dict):
        """解析MagneticOne格式条目"""
        # Agent信息
        agent_info = entry_data.get('agent', {})
        if isinstance(agent_info, dict):
            entry.agent_name = agent_info.get('name', 'unknown')
            entry.role = agent_info.get('role', agent_info.get('name', ''))
        
        # 输入信息
        input_info = entry_data.get('input', {})
        if isinstance(input_info, dict):
            entry.input_data = input_info
            
            # 从messages中提取内容
            messages = input_info.get('messages', [])
            if isinstance(messages, list) and messages:
                first_message = messages[0]
                if isinstance(first_message, dict):
                    entry.content = first_message.get('content', '')
                    entry.role = first_message.get('role', entry.role)
        
        # 输出信息
        output_info = entry_data.get('output', {})
        if isinstance(output_info, dict):
            entry.output_data = output_info
            
            # 从messages中提取输出内容
            messages = output_info.get('messages', [])
            if isinstance(messages, list) and messages:
                first_message = messages[0]
                if isinstance(first_message, dict):
                    output_content = first_message.get('content', '')
                    if output_content:
                        if entry.content:
                            entry.content += f"\n\nOutput: {output_content}"
                        else:
                            entry.content = output_content
        
        # 工具信息
        tools = entry_data.get('tools', {})
        if isinstance(tools, dict):
            entry.tools_used = list(tools.keys())
    
    def _parse_generic_entry(self, entry: LogEntry, entry_data: Dict):
        """通用格式解析"""
        entry.agent_name = str(entry_data.get('agent', {}).get('name', 'unknown'))
        entry.content = str(entry_data.get('content', ''))
        entry.role = str(entry_data.get('role', ''))
        entry.input_data = entry_data.get('input', {})
        entry.output_data = entry_data.get('output', {})
    
    def _parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """解析时间戳"""
        if not timestamp_str:
            return None
        
        try:
            # 支持多种时间格式
            formats = [
                '%Y-%m-%dT%H:%M:%S.%f',  # ISO format with microseconds
                '%Y-%m-%dT%H:%M:%S',     # ISO format
                '%Y-%m-%d %H:%M:%S',     # Standard format
                '%Y-%m-%d_%H-%M-%S'      # File name format
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(timestamp_str, fmt)
                except ValueError:
                    continue
            
            # 如果都不匹配，返回当前时间
            return datetime.now()
            
        except Exception:
            return None
    
    def _determine_message_type(self, entry: LogEntry, format_type: str) -> LogEntryType:
        """确定消息类型"""
        content = entry.content.lower()
        agent_name = entry.agent_name.lower()
        
        # 通用规则
        if 'user' in agent_name or entry.role == 'user':
            return LogEntryType.USER_INPUT
        elif 'orchestrator' in agent_name or 'coordinator' in agent_name:
            return LogEntryType.ORCHESTRATOR
        elif 'error' in content or 'exception' in content or 'failed' in content:
            return LogEntryType.ERROR
        elif entry.tools_used:
            return LogEntryType.TOOL_CALL
        
        # 格式特定规则
        if format_type == 'crewai':
            if 'tool' in entry.raw_data.get('input', {}):
                return LogEntryType.TOOL_CALL
        elif format_type == 'magneticone':
            if 'tool_calls' in str(entry.raw_data):
                return LogEntryType.TOOL_CALL
        
        return LogEntryType.AGENT_RESPONSE
    
    def _extract_execution_paths(self, log_entries: List[LogEntry]) -> List[ExecutionPath]:
        """提取执行路径"""
        paths = []
        current_path = None
        path_counter = 0
        
        for entry in log_entries:
            # 检测新路径的开始
            if (entry.message_type == LogEntryType.USER_INPUT or 
                (entry.agent_name.lower() == 'user' and current_path is None) or
                ('orchestrator' in entry.agent_name.lower() and current_path is None)):
                
                if current_path:
                    paths.append(current_path)
                
                path_counter += 1
                current_path = ExecutionPath(
                    path_id=f"path_{path_counter}",
                    start_time=entry.timestamp,
                    status=PathStatus.RUNNING
                )
            
            if current_path:
                current_path.log_entries.append(entry)
                
                # 添加节点
                if entry.agent_name and entry.agent_name not in current_path.nodes:
                    current_path.nodes.append(entry.agent_name)
                
                # 添加边（Agent调用关系）
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
            current_path.status = PathStatus.COMPLETED
            paths.append(current_path)
        
        # 如果没有明确的路径分界，将所有条目作为一个路径
        if not paths and log_entries:
            single_path = ExecutionPath(
                path_id="path_1",
                start_time=log_entries[0].timestamp,
                end_time=log_entries[-1].timestamp,
                status=PathStatus.COMPLETED
            )
            single_path.log_entries = log_entries
            single_path.nodes = list(set(entry.agent_name for entry in log_entries if entry.agent_name))
            paths.append(single_path)
        
        return paths
    
    def _analyze_execution_path(self, path: ExecutionPath, format_type: str) -> Tuple[List[ErrorInfo], List[str]]:
        """分析执行路径"""
        errors = []
        warnings = []
        
        # 检查路径完整性
        if not path.log_entries:
            errors.append(ErrorInfo(
                error_type="empty_path",
                severity=ErrorSeverity.HIGH,
                description="Execution path has no log entries",
                node_or_edge=path.path_id
            ))
        
        # 检查Agent响应
        for entry in path.log_entries:
            if entry.message_type == LogEntryType.ERROR:
                errors.append(ErrorInfo(
                    error_type="agent_error",
                    severity=ErrorSeverity.HIGH,
                    description=f"Error in {entry.agent_name}: {entry.content[:100]}...",
                    node_or_edge=entry.agent_name
                ))
        
        # 检查循环调用
        agent_sequence = [entry.agent_name for entry in path.log_entries if entry.agent_name]
        for i in range(len(agent_sequence) - 2):
            if i + 3 <= len(agent_sequence):
                window = agent_sequence[i:i+3]
                if len(set(window)) == 1:
                    errors.append(ErrorInfo(
                        error_type="infinite_loop",
                        severity=ErrorSeverity.HIGH,
                        description=f"Possible infinite loop detected: {window[0]} executed consecutively",
                        node_or_edge=window[0]
                    ))
        
        # 格式特定检查
        if format_type == 'crewai':
            warnings.extend(self._check_crewai_specific_issues(path))
        elif format_type == 'magneticone':
            warnings.extend(self._check_magneticone_specific_issues(path))
        
        return errors, warnings
    
    def _check_crewai_specific_issues(self, path: ExecutionPath) -> List[str]:
        """检查CrewAI特定问题"""
        warnings = []
        
        # 检查Agent和Task的配对
        agent_count = 0
        task_count = 0
        
        for entry in path.log_entries:
            if entry.raw_data.get('agent', {}).get('role'):
                agent_count += 1
            if entry.raw_data.get('task', {}).get('description'):
                task_count += 1
        
        if agent_count != task_count:
            warnings.append(f"Agent-Task mismatch: {agent_count} agents, {task_count} tasks")
        
        return warnings
    
    def _check_magneticone_specific_issues(self, path: ExecutionPath) -> List[str]:
        """检查MagneticOne特定问题"""
        warnings = []
        
        # 检查Orchestrator的存在
        has_orchestrator = any(
            'orchestrator' in entry.agent_name.lower() 
            for entry in path.log_entries
        )
        
        if not has_orchestrator:
            warnings.append("No Orchestrator found in MagneticOne execution path")
        
        return warnings
    
    def _generate_statistics(self, log_entries: List[LogEntry], 
                           execution_paths: List[ExecutionPath], 
                           errors: List[ErrorInfo], 
                           format_type: str) -> Dict[str, Any]:
        """生成统计信息"""
        # 基础统计
        agent_usage = {}
        message_types = {}
        
        for entry in log_entries:
            if entry.agent_name:
                agent_usage[entry.agent_name] = agent_usage.get(entry.agent_name, 0) + 1
            
            msg_type = entry.message_type.value
            message_types[msg_type] = message_types.get(msg_type, 0) + 1
        
        # 错误统计
        error_by_severity = {}
        for error in errors:
            severity = error.severity.value
            error_by_severity[severity] = error_by_severity.get(severity, 0) + 1
        
        # 路径统计
        path_stats = {
            'total_paths': len(execution_paths),
            'avg_path_length': sum(len(p.nodes) for p in execution_paths) / len(execution_paths) if execution_paths else 0,
            'avg_log_entries_per_path': sum(len(p.log_entries) for p in execution_paths) / len(execution_paths) if execution_paths else 0
        }
        
        # 格式特定统计
        format_specific_stats = {}
        if format_type == 'crewai':
            format_specific_stats = self._generate_crewai_stats(log_entries)
        elif format_type == 'magneticone':
            format_specific_stats = self._generate_magneticone_stats(log_entries)
        
        return {
            "format_type": format_type,
            "total_log_entries": len(log_entries),
            "total_execution_paths": len(execution_paths),
            "total_errors": len(errors),
            "unique_agents": len(agent_usage),
            "agent_usage": agent_usage,
            "message_type_distribution": message_types,
            "error_severity_distribution": error_by_severity,
            "path_statistics": path_stats,
            "format_specific": format_specific_stats
        }
    
    def _generate_crewai_stats(self, log_entries: List[LogEntry]) -> Dict[str, Any]:
        """生成CrewAI特定统计"""
        task_types = {}
        tool_usage = {}
        
        for entry in log_entries:
            # 统计任务类型
            task_info = entry.raw_data.get('task', {})
            if isinstance(task_info, dict) and 'description' in task_info:
                task_type = 'classification' if 'classif' in task_info['description'].lower() else 'other'
                task_types[task_type] = task_types.get(task_type, 0) + 1
            
            # 统计工具使用
            for tool in entry.tools_used:
                tool_usage[tool] = tool_usage.get(tool, 0) + 1
        
        return {
            "task_types": task_types,
            "tool_usage": tool_usage,
            "total_tool_calls": sum(tool_usage.values())
        }
    
    def _generate_magneticone_stats(self, log_entries: List[LogEntry]) -> Dict[str, Any]:
        """生成MagneticOne特定统计"""
        agent_types = {}
        
        for entry in log_entries:
            agent_name = entry.agent_name.lower()
            if 'orchestrator' in agent_name:
                agent_types['orchestrator'] = agent_types.get('orchestrator', 0) + 1
            elif 'coder' in agent_name:
                agent_types['coder'] = agent_types.get('coder', 0) + 1
            elif 'executor' in agent_name:
                agent_types['executor'] = agent_types.get('executor', 0) + 1
            elif 'filesurfer' in agent_name:
                agent_types['filesurfer'] = agent_types.get('filesurfer', 0) + 1
            else:
                agent_types['other'] = agent_types.get('other', 0) + 1
        
        return {
            "agent_types": agent_types,
            "has_orchestrator": agent_types.get('orchestrator', 0) > 0
        }
    
    def _generate_recommendations(self, errors: List[ErrorInfo], 
                                warnings: List[str], 
                                statistics: Dict[str, Any], 
                                format_type: str) -> List[str]:
        """生成建议"""
        recommendations = []
        
        # 基于错误的建议
        if errors:
            high_severity_errors = [e for e in errors if e.severity == ErrorSeverity.HIGH]
            if high_severity_errors:
                recommendations.append(f"Address {len(high_severity_errors)} high-severity errors immediately")
        
        # 基于统计的建议
        agent_usage = statistics.get('agent_usage', {})
        if agent_usage:
            max_usage = max(agent_usage.values())
            min_usage = min(agent_usage.values())
            
            if max_usage > min_usage * 3:
                recommendations.append("Consider load balancing - some agents are significantly more active")
        
        # 格式特定建议
        if format_type == 'crewai':
            recommendations.extend(self._generate_crewai_recommendations(statistics))
        elif format_type == 'magneticone':
            recommendations.extend(self._generate_magneticone_recommendations(statistics))
        
        return recommendations
    
    def _generate_crewai_recommendations(self, statistics: Dict[str, Any]) -> List[str]:
        """生成CrewAI特定建议"""
        recommendations = []
        
        format_stats = statistics.get('format_specific', {})
        tool_usage = format_stats.get('tool_usage', {})
        
        if not tool_usage:
            recommendations.append("Consider adding tools to improve agent capabilities")
        
        return recommendations
    
    def _generate_magneticone_recommendations(self, statistics: Dict[str, Any]) -> List[str]:
        """生成MagneticOne特定建议"""
        recommendations = []
        
        format_stats = statistics.get('format_specific', {})
        if not format_stats.get('has_orchestrator', False):
            recommendations.append("MagneticOne system should have an Orchestrator for proper coordination")
        
        return recommendations
    
    def _generate_summary(self, log_entries: List[LogEntry], 
                         execution_paths: List[ExecutionPath], 
                         errors: List[ErrorInfo], 
                         format_type: str) -> str:
        """生成分析摘要"""
        total_entries = len(log_entries)
        total_paths = len(execution_paths)
        total_errors = len(errors)
        
        summary_parts = [
            f"Analyzed {total_entries} log entries from {format_type.upper()} format",
            f"Found {total_paths} execution paths",
            f"Detected {total_errors} errors" if total_errors > 0 else "No errors detected"
        ]
        
        if execution_paths:
            avg_path_length = sum(len(p.nodes) for p in execution_paths) / len(execution_paths)
            summary_parts.append(f"Average path length: {avg_path_length:.1f} nodes")
        
        return ". ".join(summary_parts) + "."
