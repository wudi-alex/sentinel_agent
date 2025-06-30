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


class AgentSystemScanner:
    """Agent System Scanner - Analyze Agent project component structure"""
    
    def __init__(self):
        self.agents = []
        self.tools = []
        self.crews = []
        self.tasks = []
        self.file_structure = {}
        self.variable_assignments = {}  # Track variable assignments to agents
        self.task_variables = {}  # Track task variable assignments
    
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
        self.variable_assignments = {}
        self.task_variables = {}
    
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
                # Resolve task dependencies after AST analysis
                self._resolve_task_dependencies()
            except SyntaxError:
                # Use regex when AST fails
                self._analyze_with_regex(content, file_path)
                
        except Exception as e:
            print(f"Failed to analyze file {file_path}: {e}")
    
    def _analyze_ast(self, tree: ast.AST, file_path: Path):
        """Analyze code using AST"""
        # First pass: collect variable assignments that create agents and tasks
        agent_variables = {}  # variable_name -> agent_info
        task_variables = {}   # variable_name -> task_info
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                # Check if this is an agent assignment
                if isinstance(node.value, ast.Call) and hasattr(node.value.func, 'id') and node.value.func.id == 'Agent':
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            var_name = target.id
                            # Extract agent info
                            args = {}
                            agent_tools = []
                            
                            for keyword in node.value.keywords:
                                if keyword.arg in ['role', 'goal', 'backstory']:
                                    if isinstance(keyword.value, ast.Constant):
                                        args[keyword.arg] = keyword.value.value
                                elif keyword.arg == 'tools':
                                    # Extract tools list
                                    if isinstance(keyword.value, ast.List):
                                        for elt in keyword.value.elts:
                                            if isinstance(elt, ast.Call) and hasattr(elt.func, 'id'):
                                                tool_name = elt.func.id
                                                agent_tools.append(tool_name)
                                                # Add to global tools list if not already present
                                                tool_exists = any(t['name'] == tool_name for t in self.tools)
                                                if not tool_exists:
                                                    self.tools.append({
                                                        'name': tool_name,
                                                        'type': 'tool_instance',
                                                        'file': str(file_path),
                                                        'line': elt.lineno if hasattr(elt, 'lineno') else node.lineno,
                                                        'used_by_agent': var_name
                                                    })
                            
                            if agent_tools:
                                args['tools'] = agent_tools
                            
                            agent_name = f'Agent_{len(self.agents)+1}'
                            agent_variables[var_name] = agent_name
                            
                            self.agents.append({
                                'name': agent_name,
                                'type': 'instance',
                                'file': str(file_path),
                                'line': node.lineno,
                                'arguments': args,
                                'variable_name': var_name
                            })
                
                # Check if this is a task assignment
                elif isinstance(node.value, ast.Call) and hasattr(node.value.func, 'id') and node.value.func.id == 'Task':
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            var_name = target.id
                            task_name = f'Task_{len(self.tasks)+1}'
                            task_variables[var_name] = task_name
                            
                            # Extract task arguments including agent assignment and dependencies
                            task_args = {}
                            assigned_agent = None
                            assigned_agent_name = None
                            dependencies = []
                            
                            for keyword in node.value.keywords:
                                if keyword.arg in ['description', 'expected_output']:
                                    if isinstance(keyword.value, ast.Constant):
                                        task_args[keyword.arg] = keyword.value.value
                                    elif isinstance(keyword.value, ast.JoinedStr):
                                        # Handle f-strings by extracting the string parts
                                        task_args[keyword.arg] = self._extract_fstring_content(keyword.value)
                                elif keyword.arg == 'agent':
                                    # Extract agent assignment - could be a variable name
                                    if isinstance(keyword.value, ast.Name):
                                        assigned_agent_name = keyword.value.id
                                        # Look up the agent from our variable assignments
                                        assigned_agent = agent_variables.get(assigned_agent_name)
                                elif keyword.arg == 'context':
                                    # Extract context dependencies
                                    if isinstance(keyword.value, ast.List):
                                        for elt in keyword.value.elts:
                                            if isinstance(elt, ast.Name):
                                                dependencies.append(elt.id)
                                        task_args['context'] = dependencies
                            
                            self.tasks.append({
                                'name': task_name,
                                'type': 'instance',
                                'file': str(file_path),
                                'line': node.lineno,
                                'arguments': task_args,
                                'assigned_agent': assigned_agent,
                                'assigned_agent_variable': assigned_agent_name,
                                'variable_name': var_name,
                                'dependencies': dependencies  # Add explicit dependencies field
                            })
                            
                            # Store task variable mapping for dependency resolution
                            self.task_variables[var_name] = task_name
        
        # Second pass: collect other function calls (Crew instantiation, standalone tools)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Handle Crew instantiation
                if hasattr(node.func, 'id') and node.func.id == 'Crew':
                    self.crews.append({
                        'name': f'Crew_{len(self.crews)+1}',
                        'type': 'instance',
                        'file': str(file_path),
                        'line': node.lineno
                    })
                
                # Handle standalone tool instantiation
                elif hasattr(node.func, 'id') and node.func.id.endswith('Tool'):
                    tool_exists = any(t['name'] == node.func.id for t in self.tools)
                    if not tool_exists:
                        self.tools.append({
                            'name': node.func.id,
                            'type': 'standalone_instance',
                            'file': str(file_path),
                            'line': node.lineno
                        })
        
        # Third pass: find imports that might be tools
        imported_tools = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module == 'tools' or (node.module and 'tools' in node.module):
                    for alias in node.names:
                        if alias.name.endswith('Tool'):
                            imported_tools.append(alias.name)
            
            # Find tool class definitions
            elif isinstance(node, ast.ClassDef):
                self._check_tool_class(node, file_path)
    
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
    
    def _check_tool_class(self, node: ast.ClassDef, file_path: Path):
        """Check if it's a Tool class"""
        # Check base classes for BaseTool
        for base in node.bases:
            if hasattr(base, 'id') and 'Tool' in base.id:
                self.tools.append({
                    'name': node.name,
                    'type': 'class_definition',
                    'file': str(file_path),
                    'line': node.lineno
                })
                break
        # Check if class name ends with Tool (alternative check)
        if node.name.endswith('Tool'):
            # Only add if not already added by base class check
            if not any(t['name'] == node.name and t['file'] == str(file_path) for t in self.tools):
                self.tools.append({
                    'name': node.name,
                    'type': 'class_definition',
                    'file': str(file_path),
                    'line': node.lineno
                })
    
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
    
    def _extract_fstring_content(self, node: ast.JoinedStr) -> str:
        """Extract content from f-string for basic description capture"""
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant):
                parts.append(str(value.value))
            elif isinstance(value, ast.FormattedValue):
                # For formatted values, just add a placeholder
                parts.append("[formatted_value]")
        return "".join(parts)
    
    def _resolve_task_dependencies(self):
        """Resolve task dependencies after scanning"""
        for task in self.tasks:
            dependencies = task.get('dependencies', [])
            resolved_dependencies = []
            
            for dep_var in dependencies:
                # Look up the task name from variable name
                dep_task_name = self.task_variables.get(dep_var)
                if dep_task_name:
                    resolved_dependencies.append({
                        'variable_name': dep_var,
                        'task_name': dep_task_name
                    })
            
            task['resolved_dependencies'] = resolved_dependencies


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
    
    # If output file is specified, save the result
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result
