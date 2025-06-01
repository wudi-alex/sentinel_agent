"""
SentinelAgent Core Modules

This package contains the core functionality for agent system analysis:
- scanner: System scanning and file analysis
- inspector: Code inspection and pattern detection  
- graph_builder: System graph construction
- path_analyzer: Execution path analysis
- log_analyzer: Log analysis and anomaly detection

Main modules:
- scanner: Scans agent systems and extracts components
- graph_builder: Builds relationship graphs from scan results  
- path_analyzer: Analyzes execution paths for anomaly detection
- inspector: High-level interface for comprehensive analysis
- cli: Command-line interface

Example usage:
    from watchdog import InspectorAgent
    
    inspector = InspectorAgent()
    result = inspector.comprehensive_analysis("./agent_project")
"""

__version__ = "1.0.0"
__author__ = "Watchdog Team"

# Import main classes for easy access
from .inspector import InspectorAgent
from .scanner import AgentSystemScanner
from .graph_builder import AgentSystemGraphBuilder
from .path_analyzer import PathAnalyzer

__all__ = [
    "InspectorAgent",
    "AgentSystemScanner", 
    "AgentSystemGraphBuilder",
    "PathAnalyzer"
]
