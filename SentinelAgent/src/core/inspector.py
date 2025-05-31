from crewai import Agent, Task, Crew
fr        print(f"Starting complete analysis: {target_path}")
        
        # 1. Scan
        print("1. Executing system scan...")
        scan_data = self.scan_system(target_path, scan_output)
        
        # 2. Build graph
        print("2. Building relationship graph...")s import DirectoryScanTool, FileScanTool
from pathlib import Path
from .graph_builder import build_graph_from_scan, build_and_save_graph
from .path_analyzer import analyze_graph_paths, analyze_and_save_paths


class InspectorAgent:
    """Inspector Agent - Agent system scanning, graph building and path analysis"""
    
    def __init__(self):
        # Create tools
        self.directory_scan_tool = DirectoryScanTool()
        self.file_scan_tool = FileScanTool()
        
        # Create Agent
        self.scanner_agent = Agent(
            role='Agent System Scanner and Analyzer',
            goal='Scan and analyze agent system structure, build relationship graphs and analyze execution paths',
            backstory='Professional code analysis expert capable of identifying various agent components, building relationship graphs and detecting abnormal patterns',
            tools=[self.directory_scan_tool, self.file_scan_tool],
            verbose=True
        )
    
    def comprehensive_analysis(self, target_path: str, 
                             scan_output: str = None, 
                             graph_output: str = None, 
                             path_output: str = None) -> dict:
        """Complete system analysis: scan + graph building + path analysis"""
        target_name = Path(target_path).name
        
        # Set default output file names
        if scan_output is None:
            scan_output = f"scan_{target_name}.json"
        if graph_output is None:
            graph_output = f"graph_{target_name}.json"
        if path_output is None:
            path_output = f"paths_{target_name}.json"
        
        print(f"Starting complete analysis: {target_path}")
        
        # 1. Scan
        print("1. Executing system scan...")
        scan_result = self._perform_scan(target_path, scan_output)
        
        # 2. Build graph
        print("2. Building relationship graph...")
        graph_data = build_and_save_graph(scan_result, graph_output)
        
        # 3. Path analysis
        print("3. Analyzing execution paths...")
        path_analysis = analyze_and_save_paths(graph_data, path_output)
        
        print(f"Complete analysis finished!")
        print(f"- Scan results: {scan_output}")
        print(f"- Relationship graph: {graph_output}")
        print(f"- Path analysis: {path_output}")
        
        return {
            'scan_result': scan_result,
            'graph_data': graph_data,
            'path_analysis': path_analysis,
            'output_files': {
                'scan': scan_output,
                'graph': graph_output,
                'paths': path_output
            }
        }
    
    def analyze_existing_graph(self, graph_file: str, path_output: str = None) -> dict:
        """Analyze existing graph file"""
        if path_output is None:
            graph_path = Path(graph_file)
            path_output = f"paths_{graph_path.stem}.json"
        
        print(f"Analyzing graph file: {graph_file}")
        
        # Read graph data
        import json
        with open(graph_file, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
        
        # Execute path analysis
        path_analysis = analyze_and_save_paths(graph_data, path_output)
        
        print(f"Path analysis completed: {path_output}")
        
        return {
            'graph_data': graph_data,
            'path_analysis': path_analysis,
            'output_file': path_output
        }
    
    def _perform_scan(self, target_path: str, output_file: str) -> dict:
        """Execute scan operation"""
        if Path(target_path).is_dir():
            return self._scan_directory_internal(target_path, output_file)
        else:
            return self._scan_file_internal(target_path, output_file)
    
    def _scan_directory_internal(self, target_path: str, output_file: str) -> dict:
        """Internal directory scanning method"""
        from .scanner import scan_directory
        return scan_directory(target_path, output_file)
    
    def _scan_file_internal(self, target_path: str, output_file: str) -> dict:
        """Internal file scanning method"""
        from .scanner import scan_file
        return scan_file(target_path, output_file)
    
    def scan_directory(self, target_path: str, output_file: str = None) -> str:
        """Scan directory"""
        if output_file is None:
            output_file = f"scan_{Path(target_path).name}.json"
        
        task = Task(
            description=f"Scan directory '{target_path}' and save results to '{output_file}'",
            expected_output="Scan summary",
            agent=self.scanner_agent
        )
        
        crew = Crew(agents=[self.scanner_agent], tasks=[task], verbose=True)
        return crew.kickoff()
    
    def scan_file(self, target_file: str, output_file: str = None) -> str:
        """Scan file"""
        if output_file is None:
            output_file = f"scan_{Path(target_file).stem}.json"
        
        task = Task(
            description=f"Scan file '{target_file}' and save results to '{output_file}'",
            expected_output="Scan summary",
            agent=self.scanner_agent
        )
        
        crew = Crew(agents=[self.scanner_agent], tasks=[task], verbose=True)
        return crew.kickoff()


def main():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Inspector Agent')
    parser.add_argument('target', help='Directory or file to scan')
    parser.add_argument('--output', '-o', help='Output file name')
    
    args = parser.parse_args()
    inspector = InspectorAgent()
    
    target_path = Path(args.target)
    
    print(f"🔍 Inspector Agent starting work...")
    print(f"📂 Target: {args.target}")
    
    try:
        if target_path.is_dir():
            result = inspector.scan_directory(args.target, args.output)
        else:
            result = inspector.scan_file(args.target, args.output)
        
        print("✅ Scan completed!")
        print(result)
        
    except Exception as e:
        print(f"❌ Scan failed: {e}")


if __name__ == "__main__":
    main()
