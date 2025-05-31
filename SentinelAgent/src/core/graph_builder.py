#!/usr/bin/env python3
"""
Agent System Graph Builder
从扫描结果构建agent和tool的关系图
"""

import json
import re
from typing import Dict, List, Any, Set, Tuple
from datetime import datetime
from pathlib import Path


class AgentSystemGraphBuilder:
    """Agent系统图构建器 - 构建agents和tools的关系图"""
    
    def __init__(self):
        self.nodes = {}  # 所有节点 (agents + tools)
        self.edges = []  # 有向边
        self.graph_metadata = {}
        
    def build_graph_from_scan(self, scan_result: Dict[str, Any]) -> Dict[str, Any]:
        """从扫描结果构建图"""
        # 重置图数据
        self._reset_graph()
        
        # 提取节点
        self._extract_nodes_from_scan(scan_result)
        
        # 分析关系并构建边
        self._build_edges_from_scan(scan_result)
        
        # 生成图报告
        return self._generate_graph_report(scan_result)
    
    def _reset_graph(self):
        """重置图数据"""
        self.nodes = {}
        self.edges = []
        self.graph_metadata = {}
    
    def _extract_nodes_from_scan(self, scan_result: Dict[str, Any]):
        """从扫描结果中提取节点 - 只包含agents和tools"""
        # 添加agent节点，包含相关的crew和task信息
        for i, agent in enumerate(scan_result.get('agents', [])):
            node_id = f"agent_{i}"
            
            # 查找与此agent相关的crew和task
            agent_crews = self._find_related_crews(agent, scan_result.get('crews', []))
            agent_tasks = self._find_related_tasks(agent, scan_result.get('tasks', []))
            
            self.nodes[node_id] = {
                'id': node_id,
                'type': 'agent',
                'name': agent.get('name', f'Agent_{i}'),
                'file': agent.get('file', ''),
                'line': agent.get('line', 0),
                'metadata': {
                    'role': agent.get('arguments', {}).get('role', ''),
                    'goal': agent.get('arguments', {}).get('goal', ''),
                    'backstory': agent.get('arguments', {}).get('backstory', ''),
                    'crews': agent_crews,  # 此agent所属的crew
                    'tasks': agent_tasks   # 此agent执行的task
                }
            }
        
        # 添加tool节点
        for i, tool in enumerate(scan_result.get('tools', [])):
            node_id = f"tool_{i}"
            self.nodes[node_id] = {
                'id': node_id,
                'type': 'tool',
                'name': tool.get('name', f'Tool_{i}'),
                'file': tool.get('file', ''),
                'line': tool.get('line', 0),
                'metadata': {
                    'description': tool.get('description', ''),
                    'function_name': tool.get('function_name', '')
                }
            }
    
    def _build_edges_from_scan(self, scan_result: Dict[str, Any]):
        """基于扫描结果分析并构建边"""
        # 基于文件位置分析关系
        self._analyze_file_relationships(scan_result)
        
        # 基于命名约定分析关系
        self._analyze_naming_relationships()
        
        # 基于代码内容分析关系 (如果有详细的代码分析)
        self._analyze_content_relationships(scan_result)
    
    def _analyze_file_relationships(self, scan_result: Dict[str, Any]):
        """基于文件位置分析关系"""
        # 如果两个组件在同一个文件中，它们可能有关系
        file_components = {}
        
        # 按文件分组所有组件
        for node_id, node in self.nodes.items():
            file_path = node['file']
            if file_path not in file_components:
                file_components[file_path] = []
            file_components[file_path].append(node_id)
        
        # 在同一文件中的组件之间添加边（表示可能的访问关系）
        for file_path, components in file_components.items():
            if len(components) > 1:
                for i in range(len(components)):
                    for j in range(len(components)):
                        if i != j:
                            source = components[i]
                            target = components[j]
                            
                            # 添加有向边，表示source可以访问target
                            self._add_edge(source, target, 'file_proximity', 0.3)
    
    def _analyze_naming_relationships(self):
        """基于命名约定分析关系"""
        # Agent通常会使用Tool
        agent_nodes = [nid for nid, node in self.nodes.items() if node['type'] == 'agent']
        tool_nodes = [nid for nid, node in self.nodes.items() if node['type'] == 'tool']
        
        # Agent -> Tool关系
        for agent_id in agent_nodes:
            for tool_id in tool_nodes:
                agent_name = self.nodes[agent_id]['name'].lower()
                tool_name = self.nodes[tool_id]['name'].lower()
                
                # 如果agent和tool名称相似，添加连接
                if self._names_similar(agent_name, tool_name):
                    self._add_edge(agent_id, tool_id, 'name_similarity', 0.6)
        
        # 基于agent的crew和task信息添加agent之间的关系
        for agent_id in agent_nodes:
            agent = self.nodes[agent_id]
            agent_crews = agent['metadata'].get('crews', [])
            
            # 如果两个agent属于相同的crew，它们之间有协作关系
            for other_agent_id in agent_nodes:
                if agent_id != other_agent_id:
                    other_agent = self.nodes[other_agent_id]
                    other_crews = other_agent['metadata'].get('crews', [])
                    
                    # 检查是否有共同的crew
                    common_crews = self._find_common_crews(agent_crews, other_crews)
                    if common_crews:
                        self._add_edge(agent_id, other_agent_id, 'same_crew_collaboration', 0.7)
    
    def _find_common_crews(self, crews1: List[Dict], crews2: List[Dict]) -> List[Dict]:
        """查找两个agent共同的crew"""
        common = []
        for c1 in crews1:
            for c2 in crews2:
                if (c1.get('file') == c2.get('file') and 
                    c1.get('line') == c2.get('line')):
                    common.append(c1)
        return common
    
    def _analyze_content_relationships(self, scan_result: Dict[str, Any]):
        """基于代码内容分析关系"""
        # 这里可以添加更复杂的代码分析逻辑
        # 例如：分析function calls, imports等
        
        # 如果有扫描到的具体工具引用，添加更强的连接
        for agent in scan_result.get('agents', []):
            agent_file = agent.get('file', '')
            agent_id = None
            
            # 找到对应的agent节点
            for nid, node in self.nodes.items():
                if node['type'] == 'agent' and node['file'] == agent_file:
                    agent_id = nid
                    break
            
            if agent_id:
                # 检查是否有tool的引用
                for tool in scan_result.get('tools', []):
                    tool_name = tool.get('name', '')
                    if tool_name and agent.get('arguments', {}).get('tools'):
                        # 如果agent明确使用了某个tool
                        tool_id = None
                        for nid, node in self.nodes.items():
                            if node['type'] == 'tool' and node['name'] == tool_name:
                                tool_id = nid
                                break
                        
                        if tool_id:
                            self._add_edge(agent_id, tool_id, 'explicit_usage', 0.9)
    
    def _find_related_crews(self, agent: Dict[str, Any], crews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """查找与agent相关的crew"""
        related_crews = []
        agent_file = agent.get('file', '')
        
        for crew in crews:
            # 如果crew和agent在同一个文件中，认为它们相关
            if crew.get('file', '') == agent_file:
                related_crews.append({
                    'name': crew.get('name', ''),
                    'file': crew.get('file', ''),
                    'line': crew.get('line', 0)
                })
        
        return related_crews
    
    def _find_related_tasks(self, agent: Dict[str, Any], tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """查找与agent相关的task"""
        related_tasks = []
        agent_file = agent.get('file', '')
        
        for task in tasks:
            # 如果task和agent在同一个文件中，认为它们相关
            if task.get('file', '') == agent_file:
                related_tasks.append({
                    'name': task.get('name', ''),
                    'file': task.get('file', ''),
                    'line': task.get('line', 0)
                })
        
        return related_tasks

    def _names_similar(self, name1: str, name2: str) -> bool:
        """检查两个名称是否相似"""
        # 简单的名称相似性检查
        name1_parts = set(re.findall(r'\w+', name1.lower()))
        name2_parts = set(re.findall(r'\w+', name2.lower()))
        
        # 如果有共同的词汇，认为相似
        return len(name1_parts.intersection(name2_parts)) > 0
    
    def _add_edge(self, source: str, target: str, relationship_type: str, weight: float):
        """添加有向边"""
        edge = {
            'source': source,
            'target': target,
            'relationship': relationship_type,
            'weight': weight
        }
        
        # 避免重复边
        for existing_edge in self.edges:
            if (existing_edge['source'] == source and 
                existing_edge['target'] == target and
                existing_edge['relationship'] == relationship_type):
                return
        
        self.edges.append(edge)
    
    def _generate_graph_report(self, scan_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成图报告"""
        # 计算图统计信息
        node_types = {}
        for node in self.nodes.values():
            node_type = node['type']
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        relationship_types = {}
        for edge in self.edges:
            rel_type = edge['relationship']
            relationship_types[rel_type] = relationship_types.get(rel_type, 0) + 1
        
        return {
            'graph_info': {
                'source_scan': scan_result.get('scan_info', {}),
                'build_timestamp': datetime.now().isoformat(),
                'builder_version': '1.0'
            },
            'graph_summary': {
                'total_nodes': len(self.nodes),
                'total_edges': len(self.edges),
                'node_types': node_types,
                'relationship_types': relationship_types,
                'average_degree': len(self.edges) / max(len(self.nodes), 1) if self.nodes else 0
            },
            'nodes': list(self.nodes.values()),
            'edges': self.edges,
            'graph_metadata': {
                'directed': True,
                'weighted': True,
                'description': 'Agent system component relationship graph'
            }
        }
    
    def save_graph_to_file(self, graph_data: Dict[str, Any], output_path: str):
        """保存图到JSON文件"""
        output_path = Path(output_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        print(f"图数据已保存到: {output_path}")


# 便捷函数
def build_graph_from_scan(scan_result: Dict[str, Any]) -> Dict[str, Any]:
    """便捷的图构建函数"""
    return AgentSystemGraphBuilder().build_graph_from_scan(scan_result)


def build_and_save_graph(scan_result: Dict[str, Any], output_path: str) -> Dict[str, Any]:
    """构建图并保存到文件"""
    builder = AgentSystemGraphBuilder()
    graph_data = builder.build_graph_from_scan(scan_result)
    builder.save_graph_to_file(graph_data, output_path)
    return graph_data


def scan_and_build_graph(directory_path: str, output_path: str = None) -> Dict[str, Any]:
    """扫描目录并构建图"""
    from .scanner import scan_directory
    
    # 执行扫描
    scan_result = scan_directory(directory_path)
    
    # 构建图
    graph_data = build_graph_from_scan(scan_result)
    
    # 保存图（如果指定了输出路径）
    if output_path:
        builder = AgentSystemGraphBuilder()
        builder.save_graph_to_file(graph_data, output_path)
    
    return graph_data
