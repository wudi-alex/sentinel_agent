#!/usr/bin/env python3
"""
Agent System Path Analyzer
分析agent系统中的执行路径，识别正常和可疑的行为模式
"""

import json
import math
from typing import Dict, List, Any, Set, Tuple, Optional
from datetime import datetime
from pathlib import Path
from enum import Enum
from dataclasses import dataclass


class NodeState(Enum):
    """节点状态枚举"""
    NORMAL = "normal"
    SUSPICIOUS = "suspicious"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class EdgeState(Enum):
    """边状态枚举"""
    NORMAL = "normal"
    SUSPICIOUS = "suspicious"
    ANOMALOUS = "anomalous"
    FORBIDDEN = "forbidden"


@dataclass
class PathAnalysisRule:
    """路径分析规则"""
    name: str
    description: str
    check_function: str  # 检查函数名
    severity: str  # 'low', 'medium', 'high', 'critical'
    enabled: bool = True


class PathAnalyzer:
    """路径分析器 - 分析agent系统执行路径"""
    
    def __init__(self):
        self.graph_data = None
        self.nodes = {}
        self.edges = []
        self.node_states = {}
        self.edge_states = {}
        self.analysis_rules = self._load_default_rules()
        self.paths = []
        self.suspicious_patterns = []
    
    def analyze_graph_paths(self, graph_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析图中的路径"""
        self.graph_data = graph_data
        self.nodes = {node['id']: node for node in graph_data.get('nodes', [])}
        self.edges = graph_data.get('edges', [])
        
        # 初始化节点和边的状态
        self._initialize_states()
        
        # 分析节点状态
        self._analyze_node_states()
        
        # 分析边状态
        self._analyze_edge_states()
        
        # 发现所有路径
        self._discover_paths()
        
        # 分析路径模式
        self._analyze_path_patterns()
        
        # 生成分析报告
        return self._generate_analysis_report()
    
    def _load_default_rules(self) -> List[PathAnalysisRule]:
        """加载默认分析规则"""
        return [
            PathAnalysisRule(
                name="isolated_agents",
                description="检测孤立的agents（没有任何连接）",
                check_function="_check_isolated_agents",
                severity="medium"
            ),
            PathAnalysisRule(
                name="excessive_tool_usage",
                description="检测过度使用tools的agents",
                check_function="_check_excessive_tool_usage",
                severity="low"
            ),
            PathAnalysisRule(
                name="circular_dependencies",
                description="检测循环依赖",
                check_function="_check_circular_dependencies",
                severity="high"
            ),
            PathAnalysisRule(
                name="tool_without_agent",
                description="检测没有被agent使用的tools",
                check_function="_check_unused_tools",
                severity="low"
            ),
            PathAnalysisRule(
                name="complex_collaboration_chains",
                description="检测复杂的agent协作链",
                check_function="_check_complex_collaborations",
                severity="medium"
            ),
            PathAnalysisRule(
                name="high_weight_relationships",
                description="检测异常高权重的关系",
                check_function="_check_high_weight_relationships",
                severity="high"
            ),
            PathAnalysisRule(
                name="cross_file_anomalies",
                description="检测跨文件访问异常",
                check_function="_check_cross_file_anomalies",
                severity="medium"
            )
        ]
    
    def _initialize_states(self):
        """初始化节点和边的状态"""
        # 默认所有节点为正常状态
        for node_id in self.nodes:
            self.node_states[node_id] = NodeState.NORMAL
        
        # 默认所有边为正常状态
        for i, edge in enumerate(self.edges):
            self.edge_states[i] = EdgeState.NORMAL
    
    def _analyze_node_states(self):
        """分析节点状态"""
        for node_id, node in self.nodes.items():
            node_type = node.get('type')
            
            # 基于节点类型和属性判断状态
            if node_type == 'agent':
                self._analyze_agent_node(node_id, node)
            elif node_type == 'tool':
                self._analyze_tool_node(node_id, node)
    
    def _analyze_agent_node(self, node_id: str, node: Dict[str, Any]):
        """分析agent节点状态"""
        metadata = node.get('metadata', {})
        
        # 检查agent是否有足够的信息
        if not metadata.get('role') or not metadata.get('goal'):
            self.node_states[node_id] = NodeState.SUSPICIOUS
            return
        
        # 检查agent是否孤立（没有任何连接）
        connected_edges = [e for e in self.edges if e['source'] == node_id or e['target'] == node_id]
        if not connected_edges:
            self.node_states[node_id] = NodeState.SUSPICIOUS
            return
        
        # 检查agent是否有过多的工具连接
        tool_connections = [e for e in connected_edges 
                          if e['source'] == node_id and 
                          self.nodes.get(e['target'], {}).get('type') == 'tool']
        if len(tool_connections) > 5:  # 阈值可调
            self.node_states[node_id] = NodeState.SUSPICIOUS
    
    def _analyze_tool_node(self, node_id: str, node: Dict[str, Any]):
        """分析tool节点状态"""
        # 检查tool是否被任何agent使用
        incoming_edges = [e for e in self.edges if e['target'] == node_id]
        agent_connections = [e for e in incoming_edges 
                           if self.nodes.get(e['source'], {}).get('type') == 'agent']
        
        if not agent_connections:
            self.node_states[node_id] = NodeState.SUSPICIOUS
    
    def _analyze_edge_states(self):
        """分析边状态"""
        for i, edge in enumerate(self.edges):
            relationship = edge.get('relationship')
            weight = edge.get('weight', 0)
            
            # 基于关系类型和权重判断状态
            if relationship == 'explicit_usage' and weight > 0.8:
                # 高权重的显式使用关系，正常
                self.edge_states[i] = EdgeState.NORMAL
            elif relationship == 'file_proximity' and weight < 0.4:
                # 低权重的文件邻近关系，正常
                self.edge_states[i] = EdgeState.NORMAL
            elif weight > 0.9:
                # 异常高的权重可能表示异常
                self.edge_states[i] = EdgeState.SUSPICIOUS
            elif relationship == 'same_crew_collaboration':
                # 同crew协作，正常
                self.edge_states[i] = EdgeState.NORMAL
            else:
                # 其他情况，根据权重判断
                if weight > 0.7:
                    self.edge_states[i] = EdgeState.SUSPICIOUS
                else:
                    self.edge_states[i] = EdgeState.NORMAL
    
    def _discover_paths(self):
        """发现图中的所有路径"""
        self.paths = []
        
        # 找到所有可能的起始节点（agent节点）
        agent_nodes = [nid for nid, node in self.nodes.items() if node['type'] == 'agent']
        
        for start_node in agent_nodes:
            # 从每个agent开始，发现路径
            visited = set()
            current_path = [start_node]
            self._dfs_paths(start_node, visited, current_path, max_depth=5)
    
    def _dfs_paths(self, current_node: str, visited: Set[str], current_path: List[str], max_depth: int):
        """深度优先搜索发现路径"""
        if len(current_path) > max_depth:
            return
        
        visited.add(current_node)
        
        # 如果路径长度大于1，记录这个路径
        if len(current_path) > 1:
            path_info = {
                'path': current_path.copy(),
                'length': len(current_path),
                'path_type': self._classify_path(current_path),
                'risk_score': self._calculate_path_risk(current_path)
            }
            self.paths.append(path_info)
        
        # 继续探索邻居节点
        outgoing_edges = [e for e in self.edges if e['source'] == current_node]
        for edge in outgoing_edges:
            target = edge['target']
            if target not in visited:
                current_path.append(target)
                self._dfs_paths(target, visited, current_path, max_depth)
                current_path.pop()
        
        visited.remove(current_node)
    
    def _classify_path(self, path: List[str]) -> str:
        """分类路径类型"""
        if len(path) < 2:
            return "trivial"
        
        # 检查路径中的节点类型
        node_types = [self.nodes[nid]['type'] for nid in path]
        
        if all(t == 'agent' for t in node_types):
            return "agent_collaboration"
        elif node_types[0] == 'agent' and all(t == 'tool' for t in node_types[1:]):
            return "agent_tool_usage"
        elif 'agent' in node_types and 'tool' in node_types:
            return "mixed_interaction"
        else:
            return "unknown"
    
    def _calculate_path_risk(self, path: List[str]) -> float:
        """计算路径风险评分"""
        if len(path) < 2:
            return 0.0
        
        risk_score = 0.0
        
        # 基于路径长度
        if len(path) > 4:
            risk_score += 0.3
        
        # 基于节点状态
        for node_id in path:
            if self.node_states[node_id] == NodeState.SUSPICIOUS:
                risk_score += 0.4
            elif self.node_states[node_id] == NodeState.CRITICAL:
                risk_score += 0.8
        
        # 基于边状态
        for i in range(len(path) - 1):
            source = path[i]
            target = path[i + 1]
            edge_idx = self._find_edge_index(source, target)
            if edge_idx is not None:
                edge_state = self.edge_states[edge_idx]
                if edge_state == EdgeState.SUSPICIOUS:
                    risk_score += 0.3
                elif edge_state == EdgeState.ANOMALOUS:
                    risk_score += 0.6
                elif edge_state == EdgeState.FORBIDDEN:
                    risk_score += 1.0
        
        return min(risk_score, 1.0)  # 限制在0-1范围内
    
    def _find_edge_index(self, source: str, target: str) -> Optional[int]:
        """找到连接两个节点的边索引"""
        for i, edge in enumerate(self.edges):
            if edge['source'] == source and edge['target'] == target:
                return i
        return None
    
    def _analyze_path_patterns(self):
        """分析路径模式，识别可疑模式"""
        self.suspicious_patterns = []
        
        # 应用分析规则
        for rule in self.analysis_rules:
            if rule.enabled:
                check_method = getattr(self, rule.check_function, None)
                if check_method:
                    pattern = check_method()
                    if pattern:
                        pattern['rule'] = rule.name
                        pattern['severity'] = rule.severity
                        pattern['description'] = rule.description
                        self.suspicious_patterns.append(pattern)
    
    def _check_isolated_agents(self) -> Optional[Dict[str, Any]]:
        """检查孤立的agents"""
        isolated_agents = []
        for node_id, node in self.nodes.items():
            if node['type'] == 'agent':
                connected_edges = [e for e in self.edges if e['source'] == node_id or e['target'] == node_id]
                if not connected_edges:
                    isolated_agents.append(node_id)
        
        if isolated_agents:
            return {
                'pattern_type': 'isolated_agents',
                'affected_nodes': isolated_agents,
                'risk_level': 'medium',
                'details': f"Found {len(isolated_agents)} isolated agent(s)"
            }
        return None
    
    def _check_excessive_tool_usage(self) -> Optional[Dict[str, Any]]:
        """检查过度使用tools的agents"""
        excessive_agents = []
        for node_id, node in self.nodes.items():
            if node['type'] == 'agent':
                tool_connections = [e for e in self.edges 
                                 if e['source'] == node_id and 
                                 self.nodes.get(e['target'], {}).get('type') == 'tool']
                if len(tool_connections) > 3:  # 阈值可调
                    excessive_agents.append({
                        'agent': node_id,
                        'tool_count': len(tool_connections)
                    })
        
        if excessive_agents:
            return {
                'pattern_type': 'excessive_tool_usage',
                'affected_nodes': [a['agent'] for a in excessive_agents],
                'risk_level': 'low',
                'details': f"Found {len(excessive_agents)} agent(s) with excessive tool usage",
                'data': excessive_agents
            }
        return None
    
    def _check_circular_dependencies(self) -> Optional[Dict[str, Any]]:
        """检查循环依赖"""
        def has_cycle(start_node, visited, rec_stack):
            visited.add(start_node)
            rec_stack.add(start_node)
            
            outgoing = [e['target'] for e in self.edges if e['source'] == start_node]
            for neighbor in outgoing:
                if neighbor not in visited:
                    if has_cycle(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(start_node)
            return False
        
        visited = set()
        for node_id in self.nodes:
            if node_id not in visited:
                if has_cycle(node_id, visited, set()):
                    return {
                        'pattern_type': 'circular_dependencies',
                        'affected_nodes': list(visited),
                        'risk_level': 'high',
                        'details': "Detected circular dependencies in the graph"
                    }
        return None
    
    def _check_unused_tools(self) -> Optional[Dict[str, Any]]:
        """检查未使用的tools"""
        unused_tools = []
        for node_id, node in self.nodes.items():
            if node['type'] == 'tool':
                incoming_edges = [e for e in self.edges if e['target'] == node_id]
                if not incoming_edges:
                    unused_tools.append(node_id)
        
        if unused_tools:
            return {
                'pattern_type': 'unused_tools',
                'affected_nodes': unused_tools,
                'risk_level': 'low',
                'details': f"Found {len(unused_tools)} unused tool(s)"
            }
        return None
    
    def _check_complex_collaborations(self) -> Optional[Dict[str, Any]]:
        """检查复杂的agent协作链"""
        long_chains = [path for path in self.paths 
                      if path['path_type'] == 'agent_collaboration' and path['length'] > 3]
        
        if long_chains:
            return {
                'pattern_type': 'complex_collaborations',
                'affected_paths': [path['path'] for path in long_chains],
                'risk_level': 'medium',
                'details': f"Found {len(long_chains)} complex collaboration chain(s)"
            }
        return None
    
    def _check_high_weight_relationships(self) -> Optional[Dict[str, Any]]:
        """检查异常高权重的关系"""
        high_weight_edges = []
        for i, edge in enumerate(self.edges):
            if edge.get('weight', 0) > 0.9:
                high_weight_edges.append({
                    'source': edge['source'],
                    'target': edge['target'],
                    'weight': edge['weight'],
                    'relationship': edge['relationship']
                })
        
        if high_weight_edges:
            return {
                'pattern_type': 'high_weight_relationships',
                'affected_edges': high_weight_edges,
                'risk_level': 'high',
                'details': f"Found {len(high_weight_edges)} relationship(s) with unusually high weights"
            }
        return None
    
    def _check_cross_file_anomalies(self) -> Optional[Dict[str, Any]]:
        """检查跨文件访问异常"""
        cross_file_edges = []
        for edge in self.edges:
            source_node = self.nodes[edge['source']]
            target_node = self.nodes[edge['target']]
            
            source_file = source_node.get('file', '')
            target_file = target_node.get('file', '')
            
            if source_file and target_file and source_file != target_file:
                # 跨文件连接，检查是否异常
                if edge.get('weight', 0) > 0.7:  # 高权重跨文件连接可能异常
                    cross_file_edges.append({
                        'source': edge['source'],
                        'target': edge['target'],
                        'source_file': source_file,
                        'target_file': target_file,
                        'weight': edge['weight']
                    })
        
        if cross_file_edges:
            return {
                'pattern_type': 'cross_file_anomalies',
                'affected_edges': cross_file_edges,
                'risk_level': 'medium',
                'details': f"Found {len(cross_file_edges)} potentially anomalous cross-file relationship(s)"
            }
        return None
    
    def _generate_analysis_report(self) -> Dict[str, Any]:
        """生成路径分析报告"""
        # 统计路径类型
        path_types = {}
        risk_distribution = {'low': 0, 'medium': 0, 'high': 0}
        
        for path in self.paths:
            path_type = path['path_type']
            path_types[path_type] = path_types.get(path_type, 0) + 1
            
            risk_score = path['risk_score']
            if risk_score < 0.3:
                risk_distribution['low'] += 1
            elif risk_score < 0.7:
                risk_distribution['medium'] += 1
            else:
                risk_distribution['high'] += 1
        
        # 统计节点状态
        node_state_counts = {}
        for state in self.node_states.values():
            node_state_counts[state.value] = node_state_counts.get(state.value, 0) + 1
        
        # 统计边状态
        edge_state_counts = {}
        for state in self.edge_states.values():
            edge_state_counts[state.value] = edge_state_counts.get(state.value, 0) + 1
        
        # 计算总体风险评分
        total_risk_score = sum(path['risk_score'] for path in self.paths) / max(len(self.paths), 1)
        
        return {
            'analysis_info': {
                'timestamp': datetime.now().isoformat(),
                'analyzer_version': '1.0',
                'rules_applied': len([r for r in self.analysis_rules if r.enabled])
            },
            'overall_assessment': {
                'total_risk_score': round(total_risk_score, 3),
                'risk_level': self._get_risk_level(total_risk_score),
                'total_paths_analyzed': len(self.paths),
                'suspicious_patterns_found': len(self.suspicious_patterns)
            },
            'node_analysis': {
                'total_nodes': len(self.nodes),
                'node_state_distribution': node_state_counts,
                'nodes_with_states': {
                    node_id: state.value for node_id, state in self.node_states.items()
                }
            },
            'edge_analysis': {
                'total_edges': len(self.edges),
                'edge_state_distribution': edge_state_counts,
                'edges_with_states': {
                    i: state.value for i, state in self.edge_states.items()
                }
            },
            'path_analysis': {
                'path_type_distribution': path_types,
                'risk_score_distribution': risk_distribution,
                'detailed_paths': self.paths
            },
            'suspicious_patterns': self.suspicious_patterns,
            'recommendations': self._generate_recommendations()
        }
    
    def _get_risk_level(self, risk_score: float) -> str:
        """根据风险评分确定风险等级"""
        if risk_score < 0.3:
            return 'low'
        elif risk_score < 0.7:
            return 'medium'
        else:
            return 'high'
    
    def _generate_recommendations(self) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于可疑模式生成建议
        for pattern in self.suspicious_patterns:
            pattern_type = pattern['pattern_type']
            
            if pattern_type == 'isolated_agents':
                recommendations.append("Consider connecting isolated agents to tools or other agents")
            elif pattern_type == 'excessive_tool_usage':
                recommendations.append("Review agents with excessive tool usage for potential optimization")
            elif pattern_type == 'circular_dependencies':
                recommendations.append("CRITICAL: Resolve circular dependencies to prevent infinite loops")
            elif pattern_type == 'unused_tools':
                recommendations.append("Consider removing unused tools or connecting them to agents")
            elif pattern_type == 'complex_collaborations':
                recommendations.append("Simplify complex agent collaboration chains if possible")
            elif pattern_type == 'high_weight_relationships':
                recommendations.append("Review relationships with unusually high weights")
            elif pattern_type == 'cross_file_anomalies':
                recommendations.append("Verify cross-file relationships are intentional and secure")
        
        # 基于节点状态生成建议
        suspicious_nodes = sum(1 for state in self.node_states.values() if state == NodeState.SUSPICIOUS)
        if suspicious_nodes > 0:
            recommendations.append(f"Review {suspicious_nodes} suspicious node(s) for potential issues")
        
        return recommendations
    
    def save_analysis_to_file(self, analysis_data: Dict[str, Any], output_path: str):
        """保存分析结果到JSON文件"""
        output_path = Path(output_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        print(f"路径分析结果已保存到: {output_path}")


# 便捷函数
def analyze_graph_paths(graph_data: Dict[str, Any]) -> Dict[str, Any]:
    """便捷的路径分析函数"""
    return PathAnalyzer().analyze_graph_paths(graph_data)


def analyze_and_save_paths(graph_data: Dict[str, Any], output_path: str) -> Dict[str, Any]:
    """分析路径并保存到文件"""
    analyzer = PathAnalyzer()
    analysis_data = analyzer.analyze_graph_paths(graph_data)
    analyzer.save_analysis_to_file(analysis_data, output_path)
    return analysis_data


def analyze_paths_from_file(graph_file: str, output_path: str = None) -> Dict[str, Any]:
    """从图文件分析路径"""
    # 读取图数据
    with open(graph_file, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
    
    # 分析路径
    analysis_data = analyze_graph_paths(graph_data)
    
    # 保存分析结果（如果指定了输出路径）
    if output_path:
        analyzer = PathAnalyzer()
        analyzer.save_analysis_to_file(analysis_data, output_path)
    
    return analysis_data
