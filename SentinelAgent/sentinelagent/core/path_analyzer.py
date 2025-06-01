#!/usr/bin/env python3
"""
Agent System Path Analyzer
Analyzes execution paths in agent systems, identifying normal and suspicious behavior patterns
"""

import json
import math
from typing import Dict, List, Any, Set, Tuple, Optional
from datetime import datetime
from pathlib import Path
from enum import Enum
from dataclasses import dataclass


class NodeState(Enum):
    """Node state enumeration"""
    NORMAL = "normal"
    SUSPICIOUS = "suspicious"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class EdgeState(Enum):
    """Edge state enumeration"""
    NORMAL = "normal"
    SUSPICIOUS = "suspicious"
    ANOMALOUS = "anomalous"
    FORBIDDEN = "forbidden"


@dataclass
class PathAnalysisRule:
    """Path analysis rule"""
    name: str
    description: str
    check_function: str  # Check function name
    severity: str  # 'low', 'medium', 'high', 'critical'
    enabled: bool = True


class PathAnalyzer:
    """Path Analyzer - Analyzes execution paths in agent systems"""
    
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
        """Analyze paths in the graph"""
        self.graph_data = graph_data
        self.nodes = {node['id']: node for node in graph_data.get('nodes', [])}
        self.edges = graph_data.get('edges', [])
        
        # Initialize node and edge states
        self._initialize_states()
        
        # Analyze node states
        self._analyze_node_states()
        
        # Analyze edge states
        self._analyze_edge_states()
        
        # Discover all paths
        self._discover_paths()
        
        # Analyze path patterns
        self._analyze_path_patterns()
        
        # Generate analysis report
        return self._generate_analysis_report()
    
    def _load_default_rules(self) -> List[PathAnalysisRule]:
        """Load default analysis rules"""
        return [
            PathAnalysisRule(
                name="isolated_agents",
                description="Detect isolated agents (without any connections)",
                check_function="_check_isolated_agents",
                severity="medium"
            ),
            PathAnalysisRule(
                name="excessive_tool_usage",
                description="Detect agents with excessive tool usage",
                check_function="_check_excessive_tool_usage",
                severity="low"
            ),
            PathAnalysisRule(
                name="circular_dependencies",
                description="Detect circular dependencies",
                check_function="_check_circular_dependencies",
                severity="high"
            ),
            PathAnalysisRule(
                name="tool_without_agent",
                description="Detect tools not used by agents",
                check_function="_check_unused_tools",
                severity="low"
            ),
            PathAnalysisRule(
                name="complex_collaboration_chains",
                description="Detect complex agent collaboration chains",
                check_function="_check_complex_collaborations",
                severity="medium"
            ),
            PathAnalysisRule(
                name="high_weight_relationships",
                description="Detect abnormally high weight relationships",
                check_function="_check_high_weight_relationships",
                severity="high"
            ),
            PathAnalysisRule(
                name="cross_file_anomalies",
                description="Detect cross-file access anomalies",
                check_function="_check_cross_file_anomalies",
                severity="medium"
            )
        ]
    
    def _initialize_states(self):
        """Initialize node and edge states"""
        # Default all nodes to normal state
        for node_id in self.nodes:
            self.node_states[node_id] = NodeState.NORMAL
        
        # Default all edges to normal state
        for i, edge in enumerate(self.edges):
            self.edge_states[i] = EdgeState.NORMAL
    
    def _analyze_node_states(self):
        """analyzenodestate"""
        for node_id, node in self.nodes.items():
            node_type = node.get('type')
            
            # Judge state based on node type and attributes
            if node_type == 'agent':
                self._analyze_agent_node(node_id, node)
            elif node_type == 'tool':
                self._analyze_tool_node(node_id, node)
    
    def _analyze_agent_node(self, node_id: str, node: Dict[str, Any]):
        """analyzeagentnodestate"""
        metadata = node.get('metadata', {})
        
        # Check if agent has sufficient information
        if not metadata.get('role') or not metadata.get('goal'):
            self.node_states[node_id] = NodeState.SUSPICIOUS
            return
        
        # Check if agent is isolated (no connections)
        connected_edges = [e for e in self.edges if e['source'] == node_id or e['target'] == node_id]
        if not connected_edges:
            self.node_states[node_id] = NodeState.SUSPICIOUS
            return
        
        # Check if agent has too many tool connections
        tool_connections = [e for e in connected_edges 
                          if e['source'] == node_id and 
                          self.nodes.get(e['target'], {}).get('type') == 'tool']
        if len(tool_connections) > 5:  # Adjustable threshold
            self.node_states[node_id] = NodeState.SUSPICIOUS
    
    def _analyze_tool_node(self, node_id: str, node: Dict[str, Any]):
        """analyzetoolnodestate"""
        # Check if tool is used by any agent
        incoming_edges = [e for e in self.edges if e['target'] == node_id]
        agent_connections = [e for e in incoming_edges 
                           if self.nodes.get(e['source'], {}).get('type') == 'agent']
        
        if not agent_connections:
            self.node_states[node_id] = NodeState.SUSPICIOUS
    
    def _analyze_edge_states(self):
        """analyzeedgestate"""
        for i, edge in enumerate(self.edges):
            relationship = edge.get('relationship')
            weight = edge.get('weight', 0)
            
            # Judge state based on relationship type and weight
            if relationship == 'explicit_usage' and weight > 0.8:
                # High-weight explicit usage relationship, normal
                self.edge_states[i] = EdgeState.NORMAL
            elif relationship == 'file_proximity' and weight < 0.4:
                # Low-weight file proximity relationship, normal
                self.edge_states[i] = EdgeState.NORMAL
            elif weight > 0.9:
                # Abnormally high weight may indicate anomaly
                self.edge_states[i] = EdgeState.SUSPICIOUS
            elif relationship == 'same_crew_collaboration':
                # Same crew collaboration, normal
                self.edge_states[i] = EdgeState.NORMAL
            else:
                # Other cases, judge by weight
                if weight > 0.7:
                    self.edge_states[i] = EdgeState.SUSPICIOUS
                else:
                    self.edge_states[i] = EdgeState.NORMAL
    
    def _discover_paths(self):
        """Discover all paths in the graph"""
        self.paths = []
        
        # Find all possible starting nodes (agent nodes)
        agent_nodes = [nid for nid, node in self.nodes.items() if node['type'] == 'agent']
        
        for start_node in agent_nodes:
            # Start discovery from each agent
            visited = set()
            current_path = [start_node]
            self._dfs_paths(start_node, visited, current_path, max_depth=5)
    
    def _dfs_paths(self, current_node: str, visited: Set[str], current_path: List[str], max_depth: int):
        """Depth-first search to discover paths"""
        if len(current_path) > max_depth:
            return
        
        visited.add(current_node)
        
        # If path length is greater than 1, record this path
        if len(current_path) > 1:
            path_info = {
                'path': current_path.copy(),
                'length': len(current_path),
                'path_type': self._classify_path(current_path),
                'risk_score': self._calculate_path_risk(current_path)
            }
            self.paths.append(path_info)
        
        # Continue exploring neighbor nodes
        outgoing_edges = [e for e in self.edges if e['source'] == current_node]
        for edge in outgoing_edges:
            target = edge['target']
            if target not in visited:
                current_path.append(target)
                self._dfs_paths(target, visited, current_path, max_depth)
                current_path.pop()
        
        visited.remove(current_node)
    
    def _classify_path(self, path: List[str]) -> str:
        """Classify path types"""
        if len(path) < 2:
            return "trivial"
        
        # Check node types in path
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
        """Calculate path risk score"""
        if len(path) < 2:
            return 0.0
        
        risk_score = 0.0
        
        # Based on path length
        if len(path) > 4:
            risk_score += 0.3
        
        # Based on node states
        for node_id in path:
            if self.node_states[node_id] == NodeState.SUSPICIOUS:
                risk_score += 0.4
            elif self.node_states[node_id] == NodeState.CRITICAL:
                risk_score += 0.8
        
        # Based on edge states
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
        
        return min(risk_score, 1.0)  # Limit to 0-1 range
    
    def _find_edge_index(self, source: str, target: str) -> Optional[int]:
        """Find edge index connecting two nodes"""
        for i, edge in enumerate(self.edges):
            if edge['source'] == source and edge['target'] == target:
                return i
        return None
    
    def _analyze_path_patterns(self):
        """Analyze path patterns and identify suspicious patterns"""
        self.suspicious_patterns = []
        
        # Apply analysis rules
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
        """Check for isolated agents"""
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
        """Check for agents with excessive tool usage"""
        excessive_agents = []
        for node_id, node in self.nodes.items():
            if node['type'] == 'agent':
                tool_connections = [e for e in self.edges 
                                 if e['source'] == node_id and 
                                 self.nodes.get(e['target'], {}).get('type') == 'tool']
                if len(tool_connections) > 3:  # Threshold configurable
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
        """Check for circular dependencies"""
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
        """Check for unused tools"""
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
        """Check for complex agent collaboration chains"""
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
        """Check for abnormally high-weight relationships"""
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
        """Check for cross-file access anomalies"""
        cross_file_edges = []
        for edge in self.edges:
            source_node = self.nodes[edge['source']]
            target_node = self.nodes[edge['target']]
            
            source_file = source_node.get('file', '')
            target_file = target_node.get('file', '')
            
            if source_file and target_file and source_file != target_file:
                # Cross-file connection, check if abnormal
                if edge.get('weight', 0) > 0.7:  # High-weight cross-file connections may be abnormal
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
        """generatepathanalyzereport"""
        # Count path types
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
        
        # Count node states
        node_state_counts = {}
        for state in self.node_states.values():
            node_state_counts[state.value] = node_state_counts.get(state.value, 0) + 1
        
        # Count edge states
        edge_state_counts = {}
        for state in self.edge_states.values():
            edge_state_counts[state.value] = edge_state_counts.get(state.value, 0) + 1
        
        # Calculate overall risk score
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
        """Determine risk level based on risk score"""
        if risk_score < 0.3:
            return 'low'
        elif risk_score < 0.7:
            return 'medium'
        else:
            return 'high'
    
    def _generate_recommendations(self) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        # Generate recommendations based on suspicious patterns
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
        
        # Based on nodestate generation suggestions
        suspicious_nodes = sum(1 for state in self.node_states.values() if state == NodeState.SUSPICIOUS)
        if suspicious_nodes > 0:
            recommendations.append(f"Review {suspicious_nodes} suspicious node(s) for potential issues")
        
        return recommendations
    
    def save_analysis_to_file(self, analysis_data: Dict[str, Any], output_path: str):
        """Save analysis results to JSON file"""
        output_path = Path(output_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
        
        print(f"Path analysis results saved to: {output_path}")


# Convenience functions
def analyze_graph_paths(graph_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenient path analysis function"""
    return PathAnalyzer().analyze_graph_paths(graph_data)


def analyze_and_save_paths(graph_data: Dict[str, Any], output_path: str) -> Dict[str, Any]:
    """Analyze path and save to file"""
    analyzer = PathAnalyzer()
    analysis_data = analyzer.analyze_graph_paths(graph_data)
    analyzer.save_analysis_to_file(analysis_data, output_path)
    return analysis_data


def analyze_paths_from_file(graph_file: str, output_path: str = None) -> Dict[str, Any]:
    """Analyze path from graph file"""
    # readgraphdata
    with open(graph_file, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
    
    # analyzepath
    analysis_data = analyze_graph_paths(graph_data)
    
    # Save analysis results (if output path is specified)
    if output_path:
        analyzer = PathAnalyzer()
        analyzer.save_analysis_to_file(analysis_data, output_path)
    
    return analysis_data
