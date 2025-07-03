"""
Execution Log Analyzer - Analyze Agent System Execution Logs and Detect Anomalies

This module provides deep analysis for execution logs of Agent systems such as Magentic-One:
- Parse execution logs in CSV and TXT formats
- Match execution paths to system architecture diagrams
- Validate node input/output compliance
- Identify execution errors and anomaly patterns
- Generate detailed analysis reports

Main classes:
- ExecutionLogAnalyzer: Main analyzer class
- LogEntry: Log entry data structure
- ExecutionPath: Execution path representation
- AnalysisResult: Analysis result container
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
    """Log entry type enumeration"""
    USER_INPUT = "user_input"
    AGENT_RESPONSE = "agent_response"
    TOOL_CALL = "tool_call"
    ERROR = "error"
    SYSTEM_MESSAGE = "system_message"
    ORCHESTRATOR = "orchestrator"

class ErrorSeverity(Enum):
    """Error severity enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class PathStatus(Enum):
    """Execution path status"""
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    INTERRUPTED = "interrupted"

@dataclass
class LogEntry:
    """Log entry data structure"""
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
    """Execution path representation"""
    path_id: str
    nodes: List[str] = field(default_factory=list)
    edges: List[Tuple[str, str]] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: str = "unknown"
    log_entries: List[LogEntry] = field(default_factory=list)

@dataclass
class ErrorInfo:
    """Error information"""
    error_type: str
    severity: ErrorSeverity
    description: str
    node_or_edge: str
    suggested_fix: str = ""
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
@dataclass
class AnalysisResult:
    """Analysis result container"""
    # 添加可选的log_entries字段以支持新的JSON分析器
    log_entries: List[LogEntry] = field(default_factory=list)
    execution_paths: List[ExecutionPath] = field(default_factory=list)
    errors: List[ErrorInfo] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    statistics: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    summary: str = ""

class ExecutionLogAnalyzer:
    """Main class for execution log analysis"""
    
    def __init__(self, system_graph: Optional[Dict] = None):
        """
        Initialize the execution log analyzer
        
        Args:
            system_graph: System architecture graph for path matching
        """
        self.system_graph = system_graph or {}
        self.logger = logging.getLogger(__name__)
        self.agent_patterns = self._load_agent_patterns()
        
    def _load_agent_patterns(self) -> Dict[str, Dict]:
        """Load agent pattern definitions"""
        return {
            "MagenticOneOrchestrator": {
                "role": "Coordinator",
                "expected_inputs": ["user_request", "team_status"],
                "expected_outputs": ["task_assignment", "progress_check"],
                "keywords": ["plan", "team", "request", "progress"]
            },
            "FileSurfer": {
                "role": "File Processor",
                "expected_inputs": ["file_path", "operation_type"],
                "expected_outputs": ["file_content", "operation_result"],
                "keywords": ["file", "open", "read", "path"]
            },
            "Coder": {
                "role": "Code Generator",
                "expected_inputs": ["code_requirement", "language"],
                "expected_outputs": ["generated_code", "explanation"],
                "keywords": ["code", "script", "python", "generate"]
            },
            "Executor": {
                "role": "Code Executor",
                "expected_inputs": ["code_to_execute"],
                "expected_outputs": ["execution_result", "output"],
                "keywords": ["execute", "run", "result", "output"]
            },
            "web_surfer": {
                "role": "Web Browser",
                "expected_inputs": ["url", "action"],
                "expected_outputs": ["page_content", "action_result"],
                "keywords": ["website", "url", "browser", "page"]
            }
        }
    
    def analyze_log_file(self, log_file_path: str, file_type: str = "auto") -> AnalysisResult:
        """
        Analyze log file
        
        Args:
            log_file_path: Path to the log file
            file_type: File type ("csv", "txt", "json", "auto")
            
        Returns:
            AnalysisResult: Analysis result
        """
        try:
            # Auto-detect file type
            if file_type == "auto":
                file_type = self._detect_file_type(log_file_path)
            
            # 如果是JSON格式，使用JSON专用分析器
            if file_type == "json":
                from .json_log_analyzer import JSONLogAnalyzer
                json_analyzer = JSONLogAnalyzer(self.system_graph)
                return json_analyzer.analyze_json_log(log_file_path)
            
            # Parse log file (for CSV and TXT)
            log_entries = self._parse_log_file(log_file_path, file_type)
            
            # Extract execution paths
            execution_paths = self._extract_execution_paths(log_entries)
            
            # Analyze each path
            errors = []
            warnings = []
            
            for path in execution_paths:
                path_errors, path_warnings = self._analyze_execution_path(path)
                errors.extend(path_errors)
                warnings.extend(path_warnings)
            
            # Generate statistics
            statistics = self._generate_statistics(log_entries, execution_paths, errors)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(errors, warnings)
            
            # Generate summary
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
            self.logger.error(f"Error analyzing log file: {e}")
            raise
    
    def _detect_file_type(self, file_path: str) -> str:
        """Detect file type"""
        if file_path.endswith('.csv'):
            return "csv"
        elif file_path.endswith('.txt') or file_path.endswith('.log'):
            return "txt"
        elif file_path.endswith('.json'):
            return "json"
        else:
            # Detect by file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('{') or first_line.startswith('['):
                        return "json"
                    elif ',' in first_line and ('input_messages' in first_line or 'role' in first_line):
                        return "csv"
                    else:
                        return "txt"
            except:
                return "txt"
    
    def _parse_log_file(self, file_path: str, file_type: str) -> List[LogEntry]:
        """Parse log file"""
        if file_type == "csv":
            return self._parse_csv_log(file_path)
        else:
            return self._parse_txt_log(file_path)
    
    def _parse_csv_log(self, file_path: str) -> List[LogEntry]:
        """Parse CSV format log"""
        log_entries = []
        
        try:
            df = pd.read_csv(file_path)
            
            for _, row in df.iterrows():
                entry = LogEntry()
                entry.raw_data = row.to_dict()
                
                # Parse input messages
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
                
                # Parse output messages
                if 'output_messages' in row and pd.notna(row['output_messages']):
                    try:
                        output_msgs = ast.literal_eval(row['output_messages'])
                        if output_msgs:
                            entry.output_data = output_msgs[0] if isinstance(output_msgs, list) else output_msgs
                    except:
                        entry.output_data = {'content': str(row['output_messages'])}
                
                # Parse tools
                if 'input_tools' in row and pd.notna(row['input_tools']):
                    try:
                        tools = ast.literal_eval(row['input_tools'])
                        if isinstance(tools, list):
                            entry.tools_used = [tool.get('function', {}).get('name', '') for tool in tools]
                    except:
                        pass
                
                # Set message type
                entry.message_type = self._determine_message_type(entry)
                
                log_entries.append(entry)
                
        except Exception as e:
            self.logger.error(f"Failed to parse CSV log file: {e}")
            raise
        
        return log_entries
    
    def _parse_txt_log(self, file_path: str) -> List[LogEntry]:
        """Parse TXT format log"""
        log_entries = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split messages by separator, using correct regex
            parts = re.split(r'---------- [^-]+ ----------', content)
            
            # Extract all separators (including agent information)
            separators = re.findall(r'---------- ([^-]+) ----------', content)
            
            # Pair content and agent information
            for i, part in enumerate(parts):
                if not part.strip():
                    continue
                
                entry = LogEntry()
                entry.content = part.strip()
                
                # Extract agent information from separator
                if i > 0 and i - 1 < len(separators):
                    separator_text = separators[i - 1].strip()
                    
                    # Parse "TextMessage (agent_name)" format
                    agent_match = re.search(r'\(([^)]+)\)', separator_text)
                    if agent_match:
                        entry.agent_name = agent_match.group(1)
                    
                    # Determine message type
                    if 'TextMessage' in separator_text:
                        entry.message_type = LogEntryType.AGENT_RESPONSE
                    elif 'MultiModalMessage' in separator_text:
                        entry.message_type = LogEntryType.TOOL_CALL
                    else:
                        entry.message_type = LogEntryType.SYSTEM_MESSAGE
                
                # Detect message type
                if not entry.message_type or entry.message_type == LogEntryType.SYSTEM_MESSAGE:
                    entry.message_type = self._determine_message_type(entry)
                
                # Extract timestamp (from file name)
                time_match = re.search(r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', file_path)
                if time_match:
                    try:
                        base_time = datetime.strptime(time_match.group(1), '%Y-%m-%d_%H-%M-%S')
                        # Add offset time for each entry
                        entry.timestamp = base_time.replace(second=base_time.second + i)
                    except:
                        pass
                
                log_entries.append(entry)
                
        except Exception as e:
            self.logger.error(f"Failed to parse TXT log file: {e}")
            raise
        
        return log_entries
    
    def _determine_message_type(self, entry: LogEntry) -> LogEntryType:
        """Determine message type"""
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
        """Extract execution paths"""
        paths = []
        current_path = None
        path_counter = 0
        
        for entry in log_entries:
            # Detect start of new path (user input or first message from user usually marks new task)
            if (entry.message_type == LogEntryType.USER_INPUT or 
                (entry.agent_name.lower() == 'user' and current_path is None)):
                
                if current_path:
                    paths.append(current_path)
                
                path_counter += 1
                current_path = ExecutionPath(
                    path_id=f"path_{path_counter}",
                    start_time=entry.timestamp
                )
                # Fix type for first user message
                if entry.agent_name.lower() == 'user':
                    entry.message_type = LogEntryType.USER_INPUT
            
            if current_path:
                current_path.log_entries.append(entry)
                
                # Add node
                if entry.agent_name and entry.agent_name not in current_path.nodes:
                    current_path.nodes.append(entry.agent_name)
                
                # Add edge (call relationship between agents)
                if len(current_path.log_entries) > 1:
                    prev_entry = current_path.log_entries[-2]
                    if prev_entry.agent_name != entry.agent_name:
                        edge = (prev_entry.agent_name, entry.agent_name)
                        if edge not in current_path.edges:
                            current_path.edges.append(edge)
                
                # Update end time
                if entry.timestamp:
                    current_path.end_time = entry.timestamp
        
        # Add last path
        if current_path:
            paths.append(current_path)
        
        # If no clear user input found, treat all entries as one path
        if not paths and log_entries:
            current_path = ExecutionPath(
                path_id="path_1",
                start_time=log_entries[0].timestamp if log_entries[0].timestamp else None
            )
            current_path.log_entries = log_entries
            
            # Extract all unique agent names as nodes
            for entry in log_entries:
                if entry.agent_name and entry.agent_name not in current_path.nodes:
                    current_path.nodes.append(entry.agent_name)
            
            # Build edges
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
        """Analyze a single execution path"""
        errors = []
        warnings = []
        
        # Analyze node compliance
        for entry in path.log_entries:
            node_errors, node_warnings = self._analyze_node_compliance(entry)
            errors.extend(node_errors)
            warnings.extend(node_warnings)
        
        # Analyze path completeness
        path_errors, path_warnings = self._analyze_path_completeness(path)
        errors.extend(path_errors)
        warnings.extend(path_warnings)
        
        # Analyze error patterns
        pattern_errors = self._detect_error_patterns(path)
        errors.extend(pattern_errors)
        
        return errors, warnings
    
    def _analyze_node_compliance(self, entry: LogEntry) -> Tuple[List[ErrorInfo], List[str]]:
        """Analyze node compliance"""
        errors = []
        warnings = []
        
        agent_name = entry.agent_name
        if agent_name in self.agent_patterns:
            pattern = self.agent_patterns[agent_name]
            
            # Check keywords
            content_lower = entry.content.lower()
            expected_keywords = pattern.get('keywords', [])
            
            found_keywords = [kw for kw in expected_keywords if kw in content_lower]
            
            if not found_keywords:
                warnings.append(
                    f"Expected keywords not found in output of {agent_name}: {expected_keywords}"
                )
            
            # Check role consistency
            role = pattern.get('role', '')
            if 'error' in content_lower and agent_name != 'error_handler':
                errors.append(ErrorInfo(
                    error_type="role_violation",
                    severity=ErrorSeverity.MEDIUM,
                    description=f"{agent_name} ({role}) produced an error message",
                    node_or_edge=agent_name,
                    suggested_fix="Check agent implementation and error handling"
                ))
        
        return errors, warnings
    
    def _analyze_path_completeness(self, path: ExecutionPath) -> Tuple[List[ErrorInfo], List[str]]:
        """Analyze path completeness"""
        errors = []
        warnings = []
        
        # Check for error entries
        error_entries = [e for e in path.log_entries if e.message_type == LogEntryType.ERROR]
        
        if error_entries:
            for error_entry in error_entries:
                errors.append(ErrorInfo(
                    error_type="execution_error",
                    severity=ErrorSeverity.HIGH,
                    description=f"Error occurred during execution: {error_entry.content[:200]}...",
                    node_or_edge=error_entry.agent_name,
                    suggested_fix="Check error cause and fix related code"
                ))
        
        # Check if path is complete (has start and end)
        if not path.log_entries:
            errors.append(ErrorInfo(
                error_type="empty_path",
                severity=ErrorSeverity.MEDIUM,
                description="Execution path is empty",
                node_or_edge="path",
                suggested_fix="Check log recording mechanism"
            ))
        
        # Check for unfinished tasks
        last_entry = path.log_entries[-1] if path.log_entries else None
        if last_entry and 'incomplete' in last_entry.content.lower():
            warnings.append("Execution path may be incomplete")
        
        return errors, warnings
    
    def _detect_error_patterns(self, path: ExecutionPath) -> List[ErrorInfo]:
        """Detect error patterns"""
        errors = []
        
        # Detect loop calls
        agent_sequence = [entry.agent_name for entry in path.log_entries if entry.agent_name]
        
        for i in range(len(agent_sequence) - 2):
            if i + 3 <= len(agent_sequence):
                window = agent_sequence[i:i+3]
                if len(set(window)) == 1:  # Same agent called 3 times in a row
                    errors.append(ErrorInfo(
                        error_type="infinite_loop",
                        severity=ErrorSeverity.HIGH,
                        description=f"Possible infinite loop detected: {window[0]} executed consecutively",
                        node_or_edge=window[0],
                        suggested_fix="Check agent logic to prevent infinite loops"
                    ))
        
        # Detect permission errors
        for entry in path.log_entries:
            if 'access denied' in entry.content.lower() or 'permission' in entry.content.lower():
                errors.append(ErrorInfo(
                    error_type="permission_error",
                    severity=ErrorSeverity.HIGH,
                    description="Permission-related error detected",
                    node_or_edge=entry.agent_name,
                    suggested_fix="Check file permissions and access control settings"
                ))
        
        return errors
    
    def _generate_statistics(self, log_entries: List[LogEntry], 
                           execution_paths: List[ExecutionPath], 
                           errors: List[ErrorInfo]) -> Dict[str, Any]:
        """Generate statistics"""
        agent_usage = {}
        message_types = {}
        
        for entry in log_entries:
            # Count agent usage
            if entry.agent_name:
                agent_usage[entry.agent_name] = agent_usage.get(entry.agent_name, 0) + 1
            
            # Count message types
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
        """Generate recommendations"""
        recommendations = []
        
        # Generate recommendations based on error types
        error_types = [error.error_type for error in errors]
        
        if "infinite_loop" in error_types:
            recommendations.append("Recommendation: Add loop detection and interruption mechanisms in agent logic")
        
        if "permission_error" in error_types:
            recommendations.append("Recommendation: Check file system permissions and access control configuration")
        
        if "execution_error" in error_types:
            recommendations.append("Recommendation: Enhance error handling and exception catching mechanisms")
        
        if len(warnings) > 5:
            recommendations.append("Recommendation: Pay attention to warnings and optimize agent behavior patterns")
        
        # Generate recommendations based on error severity
        critical_errors = [e for e in errors if e.severity == ErrorSeverity.CRITICAL]
        if critical_errors:
            recommendations.append("Urgent: Critical errors found, immediate fix recommended")
        
        return recommendations
    
    def _generate_summary(self, execution_paths: List[ExecutionPath], 
                         errors: List[ErrorInfo], 
                         statistics: Dict[str, Any]) -> str:
        """Generate analysis summary"""
        total_paths = len(execution_paths)
        total_errors = len(errors)
        error_rate = (total_errors / total_paths * 100) if total_paths > 0 else 0
        
        critical_errors = len([e for e in errors if e.severity == ErrorSeverity.CRITICAL])
        high_errors = len([e for e in errors if e.severity == ErrorSeverity.HIGH])
        
        summary = f"""
        Execution Log Analysis Summary:
        
        Overview:
        - Analyzed {total_paths} execution paths
        - Found {total_errors} errors (Error rate: {error_rate:.1f}%)
        - Including {critical_errors} critical errors, {high_errors} high severity errors
        
        Most active agent: {statistics.get('most_active_agent', 'N/A')}
        
        Recommendation: {'Immediate attention to critical errors' if critical_errors > 0 else 'System is basically normal, focus on optimization suggestions'}
        """
        
        return summary.strip()
    
    def generate_report(self, analysis_result: AnalysisResult, output_path: str = None) -> str:
        """Generate detailed report"""
        report_lines = []
        
        # Title
        report_lines.append("# Execution Log Analysis Report")
        report_lines.append(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Summary
        report_lines.append("## Analysis Summary")
        report_lines.append(analysis_result.summary)
        report_lines.append("")
        
        # Statistics
        report_lines.append("## Statistics")
        for key, value in analysis_result.statistics.items():
            report_lines.append(f"- {key}: {value}")
        report_lines.append("")
        
        # Error details
        if analysis_result.errors:
            report_lines.append("## Error Details")
            for i, error in enumerate(analysis_result.errors, 1):
                report_lines.append(f"### Error {i}")
                report_lines.append(f"- Type: {error.error_type}")
                report_lines.append(f"- Severity: {error.severity.value}")
                report_lines.append(f"- Location: {error.node_or_edge}")
                report_lines.append(f"- Description: {error.description}")
                report_lines.append(f"- Suggested Fix: {error.suggested_fix}")
                report_lines.append("")
        
        # Execution paths
        report_lines.append("## Execution Paths")
        for i, path in enumerate(analysis_result.execution_paths, 1):
            report_lines.append(f"### Path {i} ({path.path_id})")
            report_lines.append(f"- Nodes: {' -> '.join(path.nodes)}")
            report_lines.append(f"- Log entries: {len(path.log_entries)}")
            if path.start_time:
                report_lines.append(f"- Start time: {path.start_time}")
            if path.end_time:
                report_lines.append(f"- End time: {path.end_time}")
            report_lines.append("")
        
        # Recommendations
        if analysis_result.recommendations:
            report_lines.append("## Recommendations")
            for rec in analysis_result.recommendations:
                report_lines.append(f"- {rec}")
            report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        # Save to file
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
        
        return report_content


def main():
    """Main function - for testing"""
    analyzer = ExecutionLogAnalyzer()
    
    # Example usage
    log_file = "/path/to/log/file.csv"  # Replace with actual path
    result = analyzer.analyze_log_file(log_file)
    
    # Generate report
    report = analyzer.generate_report(result, "execution_analysis_report.md")
    print("Analysis complete, report generated")


if __name__ == "__main__":
    main()
