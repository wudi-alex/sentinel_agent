#!/usr/bin/env python3
"""
Agent System Graph Builder
Build relationship graphs for agents and tools from scan results
"""

import json
import re
from typing import Dict, List, Any, Set, Tuple
from datetime import datetime
from pathlib import Path


class AgentSystemGraphBuilder:
    """Agent system graph builder - builds relationship graphs for agents and tools"""
    
    def __init__(self):
        self.nodes = {}  # All nodes (agents + tools)
        self.edges = []  # Directed edges
        self.graph_metadata = {}
        
    def build_graph_from_scan(self, scan_result: Dict[str, Any]) -> Dict[str, Any]:
        """Build graph from scan results"""
        # Reset graph data
        self._reset_graph()
        
        # Extract nodes
        self._extract_nodes_from_scan(scan_result)
        
        # Analyze relationships and build edges
        self._build_edges_from_scan(scan_result)
        
        # Generate graph report
        return self._generate_graph_report(scan_result)
    
    def _reset_graph(self):
        """Reset graph data"""
        self.nodes = {}
        self.edges = []
        self.graph_metadata = {}
    
    def _extract_nodes_from_scan(self, scan_result: Dict[str, Any]):
        """Extract nodes from scan results - includes only agents and tools"""
        # Add agent nodes, including related crew and task information
        for i, agent in enumerate(scan_result.get('agents', [])):
            node_id = f"agent_{i}"
            
            # Find crews and tasks related to this agent
            agent_crews = self._find_related_crews(agent, scan_result.get('crews', []))
            agent_tasks = self._find_related_tasks(agent, scan_result.get('tasks', []))
            agent_tools = agent.get('arguments', {}).get('tools', [])
            
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
                    'tools': agent_tools,  # Add configured tools
                    'crews': agent_crews,  # Crews this agent belongs to
                    'tasks': agent_tasks   # Tasks this agent executes
                }
            }
        
        # Add tool nodes
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
                    'function_name': tool.get('function_name', ''),
                    'tool_type': tool.get('type', ''),
                    'used_by_agent': tool.get('used_by_agent', '')  # Which agent uses this tool
                }
            }
    
    def _build_edges_from_scan(self, scan_result: Dict[str, Any]):
        """Build edges based on scan result analysis"""
        # Skip file proximity and naming similarity analysis - they don't represent actual execution relationships
        # Only analyze content relationships for more accurate graph representing real execution flows
        
        # Analyze relationships based on code content (if detailed code analysis available)
        self._analyze_content_relationships(scan_result)
    
    def _analyze_file_relationships(self, scan_result: Dict[str, Any]):
        """Analyze relationships based on file locations"""
        # If two components are in the same file, they may have relationships
        file_components = {}
        
        # Group all components by file
        for node_id, node in self.nodes.items():
            file_path = node['file']
            if file_path not in file_components:
                file_components[file_path] = []
            file_components[file_path].append(node_id)
        
        # Add edges between components in the same file (representing possible access relationships)
        for file_path, components in file_components.items():
            if len(components) > 1:
                for i in range(len(components)):
                    for j in range(len(components)):
                        if i != j:
                            source = components[i]
                            target = components[j]
                            
                            # Add directed edge, indicating source can access target
                            self._add_edge(source, target, 'file_proximity', 0.3)
    
    def _analyze_naming_relationships(self):
        """Analyze relationships based on naming conventions"""
        # Agents typically use Tools
        agent_nodes = [nid for nid, node in self.nodes.items() if node['type'] == 'agent']
        tool_nodes = [nid for nid, node in self.nodes.items() if node['type'] == 'tool']
        
        # Agent -> Tool relationships
        for agent_id in agent_nodes:
            for tool_id in tool_nodes:
                agent_name = self.nodes[agent_id]['name'].lower()
                tool_name = self.nodes[tool_id]['name'].lower()
                
                # If agent and tool names are similar, add connection
                if self._names_similar(agent_name, tool_name):
                    self._add_edge(agent_id, tool_id, 'name_similarity', 0.6)
        
        # Add relationships between agents based on crew information (but respect task dependencies)
        for agent_id in agent_nodes:
            agent = self.nodes[agent_id]
            agent_crews = agent['metadata'].get('crews', [])
            
            # If two agents belong to the same crew, they have collaborative relationships
            for other_agent_id in agent_nodes:
                if agent_id != other_agent_id:
                    other_agent = self.nodes[other_agent_id]
                    other_crews = other_agent['metadata'].get('crews', [])
                    
                    # Check if there are common crews
                    common_crews = self._find_common_crews(agent_crews, other_crews)
                    if common_crews:
                        # Check if there's already a task dependency edge between these agents
                        has_dependency = any(
                            edge['source'] in [agent_id, other_agent_id] and 
                            edge['target'] in [agent_id, other_agent_id] and 
                            edge['relationship'] == 'task_dependency'
                            for edge in self.edges
                        )
                        
                        if not has_dependency:
                            # Only add collaborative edge if no dependency exists
                            # Lower weight for crew collaboration as task_dependency is more authoritative
                            self._add_edge(agent_id, other_agent_id, 'same_crew_collaboration', 0.4)
    
    def _analyze_content_relationships(self, scan_result: Dict[str, Any]):
        """Analyze relationships based on code content"""
        # Analyze explicit tool usage relationships
        for i, agent in enumerate(scan_result.get('agents', [])):
            agent_id = f"agent_{i}"
            agent_tools = agent.get('arguments', {}).get('tools', [])
            
            # Create explicit relationships between agents and their configured tools
            if agent_tools:
                for tool_name in agent_tools:
                    # Find the corresponding tool node
                    for j, tool in enumerate(scan_result.get('tools', [])):
                        if tool.get('name') == tool_name:
                            tool_id = f"tool_{j}"
                            # Add explicit usage relationship
                            self._add_edge(agent_id, tool_id, 'explicit_usage', 0.9)
                            print(f"🔗 Added explicit usage: {agent_id} uses {tool_id} ({tool_name})")
                            break
        
        # Analyze task assignment relationships
        for i, task in enumerate(scan_result.get('tasks', [])):
            assigned_agent = task.get('assigned_agent')
            if assigned_agent:
                # Find the agent node that matches the assigned agent
                for j, agent in enumerate(scan_result.get('agents', [])):
                    if agent.get('name') == assigned_agent:
                        agent_id = f"agent_{j}"
                        # Create a conceptual task-agent assignment relationship
                        print(f"🔗 Task assignment: {task.get('name')} -> {assigned_agent} ({agent_id})")
                        break
        
        # Analyze task dependency relationships
        self._analyze_task_dependencies(scan_result)
        
        # Analyze same crew collaboration relationships
        self._analyze_crew_collaboration(scan_result)
    
    def _analyze_task_dependencies(self, scan_result: Dict[str, Any]):
        """Analyze task dependencies and create temporal ordering edges"""
        tasks = scan_result.get('tasks', [])
        task_name_to_agent = {}
        
        # Create mapping from task name to assigned agent
        for task in tasks:
            task_name = task.get('name')
            assigned_agent = task.get('assigned_agent')
            if task_name and assigned_agent:
                task_name_to_agent[task_name] = assigned_agent
        
        # Analyze dependencies and create temporal edges between agents
        for task in tasks:
            current_task_name = task.get('name')
            current_agent = task.get('assigned_agent')
            resolved_deps = task.get('resolved_dependencies', [])
            
            if resolved_deps and current_agent:
                # Find current agent node
                current_agent_id = None
                for i, agent in enumerate(scan_result.get('agents', [])):
                    if agent.get('name') == current_agent:
                        current_agent_id = f"agent_{i}"
                        break
                
                if current_agent_id:
                    for dep in resolved_deps:
                        dep_task_name = dep.get('task_name')
                        dep_agent = task_name_to_agent.get(dep_task_name)
                        
                        if dep_agent and dep_agent != current_agent:
                            # Find dependency agent node
                            dep_agent_id = None
                            for i, agent in enumerate(scan_result.get('agents', [])):
                                if agent.get('name') == dep_agent:
                                    dep_agent_id = f"agent_{i}"
                                    break
                            
                            if dep_agent_id:
                                # Create temporal dependency edge (predecessor -> successor)
                                self._add_edge(dep_agent_id, current_agent_id, 'task_dependency', 0.95)
                                print(f"🔗 Task dependency: {dep_agent_id} ({dep_agent}) must execute before {current_agent_id} ({current_agent})")
                        
                        elif dep_agent == current_agent:
                            # Same agent has sequential tasks - this is important for path analysis
                            print(f"📋 Sequential task: {current_agent} executes {dep_task_name} before {current_task_name}")
    
    def _find_related_crews(self, agent: Dict[str, Any], crews: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find crews related to the agent"""
        related_crews = []
        agent_file = agent.get('file', '')
        
        for crew in crews:
            # If crew and agent are in the same file, consider them related
            if crew.get('file', '') == agent_file:
                related_crews.append({
                    'name': crew.get('name', ''),
                    'file': crew.get('file', ''),
                    'line': crew.get('line', 0)
                })
        
        return related_crews
    
    def _find_related_tasks(self, agent: Dict[str, Any], tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find tasks specifically assigned to this agent"""
        related_tasks = []
        agent_name = agent.get('name', '')
        
        for task in tasks:
            # Check if task is specifically assigned to this agent
            assigned_agent = task.get('assigned_agent')
            if assigned_agent == agent_name:
                task_info = {
                    'name': task.get('name', ''),
                    'file': task.get('file', ''),
                    'line': task.get('line', 0),
                    'assigned_agent': assigned_agent,
                    'variable_name': task.get('variable_name', ''),
                    'description': task.get('arguments', {}).get('description', '')[:100] + '...' if task.get('arguments', {}).get('description') else ''
                }
                
                # Add dependency information
                resolved_deps = task.get('resolved_dependencies', [])
                if resolved_deps:
                    task_info['dependencies'] = [dep.get('task_name') for dep in resolved_deps]
                    task_info['dependency_variables'] = [dep.get('variable_name') for dep in resolved_deps]
                
                related_tasks.append(task_info)
        
        return related_tasks

    def _names_similar(self, name1: str, name2: str) -> bool:
        """Check if two names are similar"""
        # Simple name similarity check
        name1_parts = set(re.findall(r'\w+', name1.lower()))
        name2_parts = set(re.findall(r'\w+', name2.lower()))
        
        # If there are common words, consider them similar
        return len(name1_parts.intersection(name2_parts)) > 0
    
    def _add_edge(self, source: str, target: str, relationship_type: str, weight: float):
        """Add directed edge"""
        edge = {
            'source': source,
            'target': target,
            'relationship': relationship_type,
            'weight': weight
        }
        
        # Avoid duplicate edges
        for existing_edge in self.edges:
            if (existing_edge['source'] == source and 
                existing_edge['target'] == target and
                existing_edge['relationship'] == relationship_type):
                return
        
        self.edges.append(edge)
    
    def _generate_graph_report(self, scan_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate graph report"""
        # Calculate graph statistics information
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
        """Save graph to JSON file"""
        output_path = Path(output_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        print(f"Graph data saved to: {output_path}")


# Convenience functions
def build_graph_from_scan(scan_result: Dict[str, Any]) -> Dict[str, Any]:
    """Convenient graph building function"""
    return AgentSystemGraphBuilder().build_graph_from_scan(scan_result)


def build_and_save_graph(scan_result: Dict[str, Any], output_path: str) -> Dict[str, Any]:
    """Build graph and save to file"""
    builder = AgentSystemGraphBuilder()
    graph_data = builder.build_graph_from_scan(scan_result)
    builder.save_graph_to_file(graph_data, output_path)
    return graph_data


def scan_and_build_graph(directory_path: str, output_path: str = None) -> Dict[str, Any]:
    """Scan directory and build graph"""
    from .scanner import scan_directory
    
    # Execute scan
    scan_result = scan_directory(directory_path)
    
    # Build graph
    graph_data = build_graph_from_scan(scan_result)
    
    # Save graph (if output path is specified)
    if output_path:
        builder = AgentSystemGraphBuilder()
        builder.save_graph_to_file(graph_data, output_path)
    
    return graph_data
