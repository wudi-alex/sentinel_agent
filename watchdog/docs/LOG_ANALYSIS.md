# Log Analysis Guide

## Overview

The Watchdog project now includes powerful execution log analysis capabilities for Agent systems. This feature allows you to analyze execution logs from systems like Magentic-One, AutoGen, and other multi-agent frameworks to detect errors, validate compliance, and optimize performance.

## Quick Start

### Basic Usage

```bash
# Analyze a log file with auto-detection
python -m src.cli --analyze-logs path/to/logfile.txt

# Specify format explicitly
python -m src.cli --analyze-logs path/to/logfile.csv --log-format csv

# Get detailed analysis with verbose output
python -m src.cli --analyze-logs path/to/logfile.txt --verbose

# Save analysis to custom file
python -m src.cli --analyze-logs path/to/logfile.txt --log-output my_analysis.json
```

### Using the Python API

```python
from src.log_analyzer import ExecutionLogAnalyzer

# Create analyzer
analyzer = ExecutionLogAnalyzer()

# Analyze log file
result = analyzer.analyze_log_file('path/to/logfile.txt')

# Access results
print(f"Found {len(result.execution_paths)} execution paths")
print(f"Detected {len(result.errors)} errors")
print(f"Generated {len(result.warnings)} warnings")

# Generate detailed report
report = analyzer.generate_report(result, 'analysis_report.md')
```

## Supported Log Formats

### 1. Text Format (TXT)
Structured text logs with message separators:

```
---------- TextMessage (user) ----------
Help me process this file.
---------- TextMessage (MagenticOneOrchestrator) ----------
I'll coordinate the team to help you...
---------- MultiModalMessage (web_surfer) ----------
I'm accessing the webpage...
```

### 2. CSV Format
Structured CSV with columns for input/output messages, tools, etc.:

```csv
input_messages,output_messages,input_tools,usage
"[{'role': 'user', 'content': 'Hello'}]","[{'role': 'assistant', 'content': 'Hi'}]","[]","{}"
```

## Analysis Capabilities

### 🛣️ Execution Path Analysis
- **Path Extraction**: Identifies distinct execution flows
- **Node Mapping**: Maps agent interactions and calls
- **Edge Detection**: Tracks communication between agents
- **Timeline Analysis**: Tracks execution timing and duration

### ❌ Error Detection
- **Execution Errors**: Runtime errors and exceptions
- **Role Violations**: Agents behaving outside their defined roles
- **Pattern Errors**: Infinite loops, deadlocks, etc.
- **Permission Errors**: Access control and authorization issues

### ⚠️ Warning System
- **Compliance Warnings**: Deviations from expected behavior
- **Performance Warnings**: Potential bottlenecks
- **Pattern Warnings**: Suspicious execution patterns

### 📊 Statistical Analysis
- **Agent Activity**: Usage statistics per agent
- **Performance Metrics**: Execution times and efficiency
- **Error Rates**: Failure analysis and trends
- **Resource Utilization**: Tool and API usage patterns

## Agent System Support

### Magentic-One
Full support for Magentic-One execution logs including:
- **MagenticOneOrchestrator**: Coordination and planning
- **FileSurfer**: File handling operations
- **Coder**: Code generation tasks
- **Executor**: Code execution
- **web_surfer**: Web browsing and interaction

### AutoGen
Compatible with AutoGen conversation logs and execution traces.

### Generic Systems
Extensible pattern system for custom agent frameworks.

## Configuration

### Agent Patterns
Customize agent behavior patterns in `log_analyzer.py`:

```python
self.agent_patterns = {
    "MyCustomAgent": {
        "role": "custom_processor",
        "expected_inputs": ["data", "parameters"],
        "expected_outputs": ["result", "status"],
        "keywords": ["process", "analyze", "compute"]
    }
}
```

### Error Detection Rules
Extend error detection patterns:

```python
def _detect_custom_errors(self, path: ExecutionPath) -> List[ErrorInfo]:
    errors = []
    # Custom error detection logic
    return errors
```

## CrewAI Integration

Use the LogAnalysisTool in CrewAI workflows:

```python
from src.tools import LogAnalysisTool

# Create tool instance
log_tool = LogAnalysisTool()

# Use in CrewAI crew
crew = Crew(
    agents=[...],
    tasks=[...],
    tools=[log_tool]
)
```

## Output Formats

### JSON Analysis Result
```json
{
  "execution_paths": [...],
  "errors": [...],
  "warnings": [...],
  "statistics": {...},
  "recommendations": [...],
  "summary": "..."
}
```

### Markdown Report
Generated reports include:
- Executive summary
- Error analysis
- Execution path details
- Recommendations
- Statistical insights

## Best Practices

### 1. Regular Analysis
- Run log analysis after major system changes
- Monitor error trends over time
- Set up automated analysis in CI/CD

### 2. Error Response
- Address HIGH and CRITICAL errors immediately
- Investigate patterns of similar errors
- Implement fixes based on recommendations

### 3. Performance Monitoring
- Track execution path efficiency
- Monitor agent utilization
- Optimize based on statistical insights

### 4. Compliance Checking
- Validate agents follow expected patterns
- Ensure proper role separation
- Monitor for security violations

## Troubleshooting

### Common Issues

**No execution paths detected:**
- Check log format matches expected structure
- Verify agent names are correctly parsed
- Use verbose mode to debug parsing

**Missing agent patterns:**
- Add custom agent definitions to agent_patterns
- Update keywords for better detection
- Verify agent naming consistency

**Performance issues:**
- Process large logs in batches
- Use specific log formats instead of auto-detection
- Filter logs to relevant time periods

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

analyzer = ExecutionLogAnalyzer()
result = analyzer.analyze_log_file('logfile.txt')
```

## Examples

See `examples/log_analysis_demo.py` for comprehensive usage examples.

## API Reference

### ExecutionLogAnalyzer

#### Methods
- `analyze_log_file(file_path, file_type="auto")`: Analyze a log file
- `generate_report(result, output_path=None)`: Generate analysis report
- `_parse_csv_log(file_path)`: Parse CSV format logs
- `_parse_txt_log(file_path)`: Parse text format logs

#### Data Structures
- `LogEntry`: Individual log entry
- `ExecutionPath`: Execution flow representation
- `ErrorInfo`: Error details and metadata
- `AnalysisResult`: Complete analysis output

### LogAnalysisTool (CrewAI)

CrewAI tool for log analysis integration.

#### Parameters
- `log_file_path`: Path to log file
- `log_format`: Format type (csv/txt/auto)
- `output_file`: Optional output file path

## Contributing

To extend log analysis capabilities:

1. Add new agent patterns to `agent_patterns`
2. Implement custom error detection methods
3. Extend supported log formats
4. Add new analysis metrics

See the main project documentation for contribution guidelines.
