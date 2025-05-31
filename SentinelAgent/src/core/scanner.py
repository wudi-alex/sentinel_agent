#!/usr/bin/env python3
"""
Agent System Scanner - Simplified Version
Core scanner for analyzing agent system structure
"""

import os
import json
import ast
import re
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime


class AgentSystemSc    """Convenient directory scanning function"""
    result = AgentSystemScanner().scan_directory(path)
    
    # If output file is specified, save the result
    if output_file::
    """Agent System Scanner - Analyze Agent project component structure"""
    
    def __init__(self):
        self.agents = []
        self.tools = []
        self.crews = []
        self.tasks = []
        self.file_structure = {}
    
    def scan_directory(self, directory_path: str) -> Dict[str, Any]:
        """Scan directory and analyze agent system structure"""
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory does not exist: {directory_path}")
        
        # Reset scan results
        self._reset_scan_results()
        
        # Scan file structure
        self._scan_file_structure(directory_path)
        
        # Analyze Python files
        for py_file in directory_path.rglob("*.py"):
            if py_file.is_file():
                self._analyze_python_file(py_file)
        
        # Generate scan report
        return self._generate_report(directory_path)
    
    def scan_file(self, file_path: str) -> Dict[str, Any]:
        """Scan single file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")
        
        # Reset scan results
        self._reset_scan_results()
        
        # Only analyze Python files
        if file_path.suffix == '.py':
            self._analyze_python_file(file_path)
        
        # Generate scan report
        return self._generate_file_report(file_path)
    
    def _reset_scan_results(self):
        """Reset scan results"""
        self.agents = []
        self.tools = []
        self.crews = []
        self.tasks = []
        self.file_structure = {}
    
    def _scan_file_structure(self, directory: Path):
        """Scan file structure"""
        self.file_structure = {
            "total_files": 0,
            "python_files": 0,
            "directories": 0,
            "file_types": {}
        }
        
        for item in directory.rglob("*"):
            if item.is_file():
                self.file_structure["total_files"] += 1
                suffix = item.suffix.lower()
                if suffix == '.py':
                    self.file_structure["python_files"] += 1
                self.file_structure["file_types"][suffix] = self.file_structure["file_types"].get(suffix, 0) + 1
            elif item.is_dir():
                self.file_structure["directories"] += 1
    
    def _analyze_python_file(self, file_path: Path):
        """Analyze Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try AST analysis
            try:
                tree = ast.parse(content)
                self._analyze_ast(tree, file_path)
            except SyntaxError:
                # Use regex when AST fails
                self._analyze_with_regex(content, file_path)
                
        except Exception as e:
            print(f"Failed to analyze file {file_path}: {e}")
    
    def _analyze_ast(self, tree: ast.AST, file_path: Path):
        """Analyze code using AST"""
        for node in ast.walk(tree):
            # Find Agent class definitions
            if isinstance(node, ast.ClassDef):
                self._check_agent_class(node, file_path)
            
            # Find function calls
            elif isinstance(node, ast.Call):
                self._check_function_call(node, file_path)
            
            # Find variable assignments
            elif isinstance(node, ast.Assign):
                self._check_assignment(node, file_path)
    
    def _analyze_with_regex(self, content: str, file_path: Path):
        """Analyze code using regular expressions"""
        # CrewAI Agent mode
        agent_patterns = [
            r'Agent\s*\(',
            r'class\s+\w+Agent\s*\(',
            r'from\s+crewai\s+import\s+Agent',
        ]
        
        # CrewAI Tool mode
        tool_patterns = [
            r'class\s+\w+Tool\s*\(\s*BaseTool',
            r'from\s+crewai_tools\s+import',
            r'@tool\s*def',
        ]
        
        # Check Agent
        for pattern in agent_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                self.agents.append({
                    'name': f'Agent_{len(self.agents)+1}',
                    'type': 'regex_detected',
                    'file': str(file_path),
                    'line': content[:match.start()].count('\n') + 1
                })
        
        # Check Tool
        for pattern in tool_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                self.tools.append({
                    'name': f'Tool_{len(self.tools)+1}',
                    'type': 'regex_detected',
                    'file': str(file_path),
                    'line': content[:match.start()].count('\n') + 1
                })
    
    def _check_agent_class(self, node: ast.ClassDef, file_path: Path):
        """Check if it's an Agent class"""
        # Check base classes
        for base in node.bases:
            if hasattr(base, 'id') and 'Agent' in base.id:
                self.agents.append({
                    'name': node.name,
                    'type': 'class_definition',
                    'file': str(file_path),
                    'line': node.lineno
                })
                break
    
    def _check_function_call(self, node: ast.Call, file_path: Path):
        """Check function calls"""
        # Agent instantiation
        if hasattr(node.func, 'id') and node.func.id == 'Agent':
            # Extract arguments
            args = {}
            for keyword in node.keywords:
                if keyword.arg in ['role', 'goal', 'backstory']:
                    if isinstance(keyword.value, ast.Constant):
                        args[keyword.arg] = keyword.value.value
            
            self.agents.append({
                'name': f'Agent_{len(self.agents)+1}',
                'type': 'instance',
                'file': str(file_path),
                'line': node.lineno,
                'arguments': args
            })
        
        # Crew instantiation
        elif hasattr(node.func, 'id') and node.func.id == 'Crew':
            self.crews.append({
                'name': f'Crew_{len(self.crews)+1}',
                'type': 'instance',
                'file': str(file_path),
                'line': node.lineno
            })
        
        # Task instantiation
        elif hasattr(node.func, 'id') and node.func.id == 'Task':
            self.tasks.append({
                'name': f'Task_{len(self.tasks)+1}',
                'type': 'instance',
                'file': str(file_path),
                'line': node.lineno
            })
    
    def _check_assignment(self, node: ast.Assign, file_path: Path):
        """Check variable assignments"""
        # Check Agent/Tool/Crew/Task assignments
        if isinstance(node.value, ast.Call):
            self._check_function_call(node.value, file_path)
    
    def _generate_report(self, directory_path: Path) -> Dict[str, Any]:
        """Generate scan report"""
        return {
            'scan_info': {
                'target': str(directory_path),
                'scan_type': 'directory',
                'timestamp': datetime.now().isoformat(),
                'scanner_version': '2.0-simplified'
            },
            'scan_summary': {
                'total_agents': len(self.agents),
                'total_tools': len(self.tools),
                'total_crews': len(self.crews),
                'total_tasks': len(self.tasks),
                'total_files': self.file_structure.get('total_files', 0),
                'python_files': self.file_structure.get('python_files', 0)
            },
            'agents': self.agents,
            'tools': self.tools,
            'crews': self.crews,
            'tasks': self.tasks,
            'file_structure': self.file_structure
        }
    
    def _generate_file_report(self, file_path: Path) -> Dict[str, Any]:
        """Generate file scan report"""
        return {
            'scan_info': {
                'target': str(file_path),
                'scan_type': 'file',
                'timestamp': datetime.now().isoformat(),
                'scanner_version': '2.0-simplified'
            },
            'scan_summary': {
                'total_agents': len(self.agents),
                'total_tools': len(self.tools),
                'total_crews': len(self.crews),
                'total_tasks': len(self.tasks),
                'total_files': 1,
                'python_files': 1 if file_path.suffix == '.py' else 0
            },
            'agents': self.agents,
            'tools': self.tools,
            'crews': self.crews,
            'tasks': self.tasks
        }


# Convenience functions
def scan_directory(path: str, output_file: str = None) -> Dict[str, Any]:
    """Convenient directory scanning function"""
    result = AgentSystemScanner().scan_directory(path)
    
    # If output file is specified, save the result
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result


def scan_file(path: str, output_file: str = None) -> Dict[str, Any]:
    """Convenient file scanning function"""
    result = AgentSystemScanner().scan_file(path)
    
    # 如果指定了输出文件，保存结果
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result
