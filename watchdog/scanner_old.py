import os
import json
import ast
import re
from typing import Dict, List, Any, Optional
from pathlib import Path


class AgentSystemScanner:
    """扫描agent系统的核心类"""
    
    def __init__(self):
        self.agents = []
        self.tools = []
        self.crews = []
        self.tasks = []
        self.file_structure = {}
        
    def scan_directory(self, directory_path: str) -> Dict[str, Any]:
        """扫描指定目录并分析agent系统结构"""
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            raise FileNotFoundError(f"目录不存在: {directory_path}")
        
        # 重置扫描结果
        self.agents = []
        self.tools = []
        self.crews = []
        self.tasks = []
        self.file_structure = {}
        
        # 扫描文件结构
        self._scan_file_structure(directory_path)
        
        # 分析Python文件
        python_files = list(directory_path.rglob("*.py"))
        for py_file in python_files:
            self._analyze_python_file(py_file)
        
        return self._generate_report()
    
    def scan_file(self, file_path: str) -> Dict[str, Any]:
        """扫描单个文件并分析agent系统结构"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 重置扫描结果
        self.agents = []
        self.tools = []
        self.crews = []
        self.tasks = []
        self.file_structure = {}
        
        if file_path.suffix == '.py':
            self._analyze_python_file(file_path)
        
        return self._generate_report()
    
    def _scan_file_structure(self, directory_path: Path):
        """扫描文件结构"""
        try:
            for item in directory_path.iterdir():
                if item.is_file():
                    self.file_structure[str(item.relative_to(directory_path))] = {
                        'type': 'file',
                        'size': item.stat().st_size,
                        'extension': item.suffix
                    }
                elif item.is_dir() and not item.name.startswith('.') and item.name != '__pycache__':
                    self.file_structure[str(item.relative_to(directory_path))] = {
                        'type': 'directory',
                        'contents': self._get_directory_contents(item)
                    }
        except PermissionError:
            pass
    
    def _get_directory_contents(self, directory: Path) -> List[str]:
        """获取目录内容"""
        try:
            return [item.name for item in directory.iterdir() 
                   if not item.name.startswith('.') and item.name != '__pycache__']
        except PermissionError:
            return []
    
    def _analyze_python_file(self, file_path: Path):
        """分析Python文件中的agent系统组件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析AST
            try:
                tree = ast.parse(content)
                self._analyze_ast(tree, file_path)
            except SyntaxError:
                # 如果AST解析失败，使用正则表达式
                self._analyze_with_regex(content, file_path)
                
        except Exception as e:
            print(f"分析文件 {file_path} 时出错: {e}")
    
    def _analyze_ast(self, tree: ast.AST, file_path: Path):
        """使用AST分析Python代码"""
        for node in ast.walk(tree):
            # 检测Agent类定义
            if isinstance(node, ast.ClassDef):
                self._analyze_class_definition(node, file_path)
            
            # 检测函数和变量赋值
            elif isinstance(node, ast.Assign):
                self._analyze_assignment(node, file_path)
            
            # 检测函数调用
            elif isinstance(node, ast.Call):
                self._analyze_function_call(node, file_path)
    
    def _analyze_class_definition(self, node: ast.ClassDef, file_path: Path):
        """分析类定义"""
        class_name = node.name
        base_classes = [self._get_name_from_node(base) for base in node.bases]
        
        # 检测Agent类
        if any('Agent' in base or 'BaseTool' in base for base in base_classes):
            agent_info = {
                'name': class_name,
                'file': str(file_path),
                'type': 'custom_class',
                'base_classes': base_classes,
                'methods': [method.name for method in node.body if isinstance(method, ast.FunctionDef)],
                'attributes': self._extract_class_attributes(node)
            }
            
            if any('Tool' in base for base in base_classes):
                self.tools.append(agent_info)
            else:
                self.agents.append(agent_info)
    
    def _analyze_assignment(self, node: ast.Assign, file_path: Path):
        """分析变量赋值"""
        if isinstance(node.value, ast.Call):
            func_name = self._get_name_from_node(node.value.func)
            
            # 检测Agent实例化
            if 'Agent' in func_name and len(node.targets) > 0:
                var_name = self._get_name_from_node(node.targets[0])
                if var_name:
                    agent_info = {
                        'name': var_name,
                        'file': str(file_path),
                        'type': 'instance',
                        'class': func_name,
                        'arguments': self._extract_call_arguments(node.value)
                    }
                    self.agents.append(agent_info)
            
            # 检测Tool实例化
            elif 'Tool' in func_name and len(node.targets) > 0:
                var_name = self._get_name_from_node(node.targets[0])
                if var_name:
                    tool_info = {
                        'name': var_name,
                        'file': str(file_path),
                        'type': 'instance',
                        'class': func_name,
                        'arguments': self._extract_call_arguments(node.value)
                    }
                    self.tools.append(tool_info)
            
            # 检测Crew实例化
            elif 'Crew' in func_name and len(node.targets) > 0:
                var_name = self._get_name_from_node(node.targets[0])
                if var_name:
                    crew_info = {
                        'name': var_name,
                        'file': str(file_path),
                        'type': 'instance',
                        'class': func_name,
                        'arguments': self._extract_call_arguments(node.value)
                    }
                    self.crews.append(crew_info)
            
            # 检测Task实例化
            elif 'Task' in func_name and len(node.targets) > 0:
                var_name = self._get_name_from_node(node.targets[0])
                if var_name:
                    task_info = {
                        'name': var_name,
                        'file': str(file_path),
                        'type': 'instance',
                        'class': func_name,
                        'arguments': self._extract_call_arguments(node.value)
                    }
                    self.tasks.append(task_info)
    
    def _analyze_function_call(self, node: ast.Call, file_path: Path):
        """分析函数调用"""
        func_name = self._get_name_from_node(node.func)
        
        # 检测列表中的Agent/Tool/Task定义
        if isinstance(node.func, ast.Name) and node.func.id in ['Agent', 'Task']:
            args = self._extract_call_arguments(node)
            if node.func.id == 'Agent':
                agent_info = {
                    'name': args.get('role', 'Unknown Agent'),
                    'file': str(file_path),
                    'type': 'direct_call',
                    'class': 'Agent',
                    'arguments': args
                }
                self.agents.append(agent_info)
            elif node.func.id == 'Task':
                task_info = {
                    'name': args.get('description', 'Unknown Task')[:50] + '...',
                    'file': str(file_path),
                    'type': 'direct_call',
                    'class': 'Task',
                    'arguments': args
                }
                self.tasks.append(task_info)
    
    def _analyze_with_regex(self, content: str, file_path: Path):
        """使用正则表达式分析代码（当AST解析失败时）"""
        # 检测Agent定义
        agent_patterns = [
            r'(\w+)\s*=\s*Agent\s*\(',
            r'class\s+(\w+)\s*\([^)]*Agent[^)]*\)',
            r'(\w+)\s*=\s*(\w*Agent)\s*\('
        ]
        
        for pattern in agent_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                agent_name = match.group(1)
                agent_info = {
                    'name': agent_name,
                    'file': str(file_path),
                    'type': 'regex_detected',
                    'pattern': pattern
                }
                self.agents.append(agent_info)
        
        # 检测Tool定义
        tool_patterns = [
            r'(\w+)\s*=\s*(\w*Tool)\s*\(',
            r'class\s+(\w+)\s*\([^)]*Tool[^)]*\)'
        ]
        
        for pattern in tool_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                tool_name = match.group(1)
                tool_info = {
                    'name': tool_name,
                    'file': str(file_path),
                    'type': 'regex_detected',
                    'pattern': pattern
                }
                self.tools.append(tool_info)
    
    def _get_name_from_node(self, node) -> str:
        """从AST节点获取名称"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name_from_node(node.value)}.{node.attr}"
        elif isinstance(node, ast.Constant):
            return str(node.value)
        return ""
    
    def _extract_call_arguments(self, call_node: ast.Call) -> Dict[str, Any]:
        """提取函数调用的参数"""
        args = {}
        
        # 处理关键字参数
        for keyword in call_node.keywords:
            if keyword.arg:
                if isinstance(keyword.value, ast.Constant):
                    args[keyword.arg] = keyword.value.value
                elif isinstance(keyword.value, ast.Name):
                    args[keyword.arg] = f"var:{keyword.value.id}"
                elif isinstance(keyword.value, ast.List):
                    args[keyword.arg] = f"list[{len(keyword.value.elts)} items]"
                else:
                    args[keyword.arg] = "complex_value"
        
        return args
    
    def _extract_class_attributes(self, class_node: ast.ClassDef) -> List[str]:
        """提取类的属性"""
        attributes = []
        for node in class_node.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        attributes.append(target.id)
        return attributes
    
    def _generate_report(self) -> Dict[str, Any]:
        """生成扫描报告"""
        return {
            'scan_summary': {
                'total_agents': len(self.agents),
                'total_tools': len(self.tools),
                'total_crews': len(self.crews),
                'total_tasks': len(self.tasks),
                'total_files': len([f for f, info in self.file_structure.items() if info['type'] == 'file'])
            },
            'agents': self.agents,
            'tools': self.tools,
            'crews': self.crews,
            'tasks': self.tasks,
            'file_structure': self.file_structure,
            'analysis_metadata': {
                'scanner_version': '1.0',
                'scan_timestamp': str(Path.cwd())
            }
        }
