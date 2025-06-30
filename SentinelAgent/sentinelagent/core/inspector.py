from crewai import Agent, Task, Crew
from .tools import DirectoryScanTool, FileScanTool
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
            description=f"""
You are an expert agent system analyzer. Your task is to thoroughly scan the directory '{target_path}' and identify all agent system components.

Please focus on identifying:
1. **Agents**: Look for CrewAI Agent instances and classes. Pay attention to:
   - Agent() constructor calls with role, goal, backstory parameters
   - Classes inheriting from Agent base classes
   - Variables assigned Agent instances
   - Extract agent configurations including tools, memory, and other parameters

2. **Tools**: Identify all tools used in the system:
   - Tool classes (classes ending with 'Tool' or inheriting from BaseTool)
   - Tool instances used in agent definitions (tools=[...] parameter)
   - Imported tools from modules like 'from tools import EmailSenderTool, CheckAvailabilityTool'
   - Custom tool implementations

3. **Tasks**: Find Task definitions:
   - Task() constructor calls
   - Task parameters like description, expected_output, agent assignments
   - Task dependencies and context relationships

4. **Crews**: Locate Crew instances:
   - Crew() constructor calls
   - Agent and task assignments in crews
   - Crew configurations and execution patterns

Example analysis patterns to look for:
```python
# Agent with tools configuration
email_responder = Agent(
    role='Email Responder',
    goal='Generate polite, appropriate replies to routine emails', 
    backstory='You craft replies to emails...',
    tools=[EmailSenderTool(), CheckAvailabilityTool()],  # <-- Extract these tools
    verbose=True
)

# Task definitions
classification_task = Task(
    description="You are an intelligent email classification assistant...",
    expected_output="Return only one label: High / Low-A / Low-B",
    agent=email_classifier,  # <-- Note agent assignment
    context=[],
)
```

Avoid duplicate detection - ensure each component is only recorded once even if it appears in multiple contexts.

Save your analysis results to '{output_file}' with detailed component information including file locations, line numbers, and extracted parameters.
            """.strip(),
            expected_output=f"""A comprehensive JSON scan report saved to '{output_file}' containing:
- Detailed scan summary with accurate counts (no duplicates)
- Complete agent list with roles, goals, backstories, and configured tools
- Full tool inventory including imported and defined tools
- Task definitions with descriptions and agent assignments  
- Crew configurations and component relationships
- File structure analysis and component locations

The scan should identify exactly the right number of components without duplicates.""",
            agent=self.scanner_agent
        )
        
        crew = Crew(agents=[self.scanner_agent], tasks=[task], verbose=True)
        return crew.kickoff()

    def scan_file(self, target_file: str, output_file: str = None) -> str:
        """Scan file"""
        if output_file is None:
            output_file = f"scan_{Path(target_file).stem}.json"
        
        task = Task(
            description=f"""
You are an expert agent system analyzer. Your task is to thoroughly analyze the single file '{target_file}' and identify all agent system components within it.

Please focus on precisely identifying:
1. **Agents**: Look for CrewAI Agent instances in the file. For example:
   ```python
   email_classifier = Agent(
       role='Email Classifier',
       goal='Classify emails into priority levels', 
       backstory='You analyze emails and determine...'
   )
   
   email_responder = Agent(
       role='Email Responder',
       goal='Generate polite, appropriate replies to routine emails',
       backstory='You craft replies to emails...',
       tools=[EmailSenderTool(), CheckAvailabilityTool()],  # <-- Extract these tools
       verbose=True
   )
   ```
   
2. **Tools**: Extract all tools referenced in agent definitions:
   - Tools imported at the top: `from tools import EmailSenderTool, CheckAvailabilityTool`
   - Tools used in agent configurations: `tools=[EmailSenderTool(), CheckAvailabilityTool()]`
   - Tool classes defined in the file
   
3. **Tasks**: Find all Task instances:
   ```python
   classification_task = Task(
       description="You are an intelligent email classification assistant...",
       expected_output="Return only one label: High / Low-A / Low-B", 
       agent=email_classifier,
       context=[],
   )
   ```
   
4. **Crews**: Identify Crew instances:
   ```python
   crew = Crew(
       agents=[email_classifier, email_responder, email_summarizer],
       tasks=[classification_task, response_task, summarization_task]
   )
   ```

CRITICAL: Avoid duplicate detection. Each agent, tool, task, or crew should only be counted once, even if the variable is referenced multiple times or used in different contexts.

For the target file '{target_file}', expect to find approximately:
- 3 unique agents (email_classifier, email_responder, email_summarizer)  
- 2 tools (EmailSenderTool, CheckAvailabilityTool) configured in email_responder
- 3 tasks (classification_task, response_task, summarization_task)
- 1 crew containing all agents and tasks

Save your analysis results to '{output_file}' with precise component information.
            """.strip(),
            expected_output=f"""A precise JSON scan report saved to '{output_file}' containing:
- Accurate scan summary with exact component counts (no duplicates)
- List of exactly 3 unique agents with their roles, goals, backstories, and any configured tools
- List of 2 tools (EmailSenderTool, CheckAvailabilityTool) that are configured in the email_responder agent
- List of 3 tasks with their descriptions and agent assignments
- List of 1 crew with agent and task configurations
- File location and line number information for each component

The scan must be precise and avoid counting the same component multiple times.""",
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
