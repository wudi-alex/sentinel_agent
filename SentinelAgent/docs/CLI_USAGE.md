# SentinelAgent CLI Usage Guide

## Overview

SentinelAgent provides a powerful command-line interface for analyzing AI agent systems. This guide covers all available commands and usage patterns.

## Installation & Setup

### Install as Package (Recommended)
```bash
pip install -e .
```

After installation, you can use the entry points:
```bash
sentinelagent --help
sentinelagent-web
```

### Direct Module Usage
```bash
python -m sentinelagent.cli.main --help
python -m sentinelagent.cli.start_web_ui
```

## Core Commands

### System Scanning

#### Basic Directory Scan
```bash
# Scan a project directory
sentinelagent /path/to/agent/project

# With custom output file
sentinelagent /path/to/agent/project --output my_scan.json
```

#### Verbose Output
```bash
# Show detailed scanning information
sentinelagent /path/to/agent/project --verbose
```

### Graph Building

#### Build Relationship Graph
```bash
# Build graph alongside scanning
sentinelagent /path/to/project --graph graph_output.json

# Combined scan and graph
sentinelagent /path/to/project --output scan.json --graph graph.json
```

### Path Analysis

#### Analyze Execution Paths
```bash
# Analyze paths alongside scanning
sentinelagent /path/to/project --paths path_analysis.json

# Full analysis (scan + graph + paths)
sentinelagent /path/to/project --all
```

### Specialized Analysis

#### Analyze Existing Graph Files
```bash
# Analyze a previously generated graph
sentinelagent --analyze-graph existing_graph.json
```

#### Log Analysis
```bash
# Analyze text log files
sentinelagent --analyze-logs /path/to/logfile.txt

# Analyze CSV log files
sentinelagent --analyze-logs /path/to/logfile.csv --log-format csv

# Specify output file for analysis
sentinelagent --analyze-logs /path/to/logfile.txt --log-output analysis_result.json
```

## Command Reference

### Basic Syntax
```bash
sentinelagent [TARGET_PATH] [OPTIONS]
sentinelagent [SPECIAL_COMMAND] [OPTIONS]
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--output` | `-o` | Specify scan output file name |
| `--graph` | `-g` | Build and save relationship graph |
| `--paths` | `-p` | Perform path analysis and save |
| `--all` | `-a` | Perform full analysis (scan + graph + paths) |
| `--verbose` | `-v` | Show detailed information |
| `--help` | `-h` | Show help message |

### Special Commands

| Command | Description |
|---------|-------------|
| `--analyze-graph` | Analyze an existing graph file |
| `--analyze-logs` | Analyze execution log files |

### Log Analysis Options

| Option | Description |
|--------|-------------|
| `--log-format` | Specify log format (csv/txt/auto) |
| `--log-output` | Specify log analysis output file |

## Usage Examples

### Complete Workflow
```bash
# 1. Scan and build everything
sentinelagent /path/to/agent/project --all

# 2. View results with verbose output
sentinelagent /path/to/agent/project --verbose

# 3. Analyze specific components
sentinelagent --analyze-graph scan_result_graph.json
sentinelagent --analyze-logs /path/to/logs/execution.log
```

### Development Workflow
```bash
# Quick scan during development
sentinelagent . --output dev_scan.json

# Build graph for visualization
sentinelagent . --graph dev_graph.json

# Analyze paths for optimization
sentinelagent . --paths dev_paths.json
```

### Batch Processing
```bash
# Scan multiple projects
for project in /path/to/projects/*; do
    sentinelagent "$project" --output "scan_$(basename $project).json"
done
```

### CI/CD Integration
```bash
# Automated analysis in CI pipeline
sentinelagent . --all --verbose > analysis_report.txt
```

## Output Files

### Scan Results (`*.json`)
Contains discovered agents, tools, crews, and tasks with their configurations.

### Graph Files (`*_graph.json`)
Contains relationship mappings and execution flow data.

### Path Analysis (`*_paths.json`)
Contains execution path analysis with risk assessments.

### Log Analysis (`*_analysis.json`)
Contains runtime behavior analysis and anomaly detection results.

## Tips & Best Practices

### Performance Optimization
- Use `--verbose` only when needed for debugging
- Specify output files to avoid default naming conflicts
- Use `--all` for comprehensive analysis in production

### Error Handling
- Check file permissions if scanning fails
- Ensure target paths exist before scanning
- Use absolute paths to avoid resolution issues

### Integration
- Combine with web interface for visualization
- Export results to other analysis tools
- Integrate with monitoring systems

## Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
# Ensure proper installation
pip install -e .

# Or use direct module path
python -m sentinelagent.cli.main --help
```

#### Permission denied
```bash
# Check file permissions
ls -la /path/to/target

# Run with appropriate permissions
sudo sentinelagent /protected/path --output result.json
```

#### Memory issues with large projects
```bash
# Process smaller chunks
sentinelagent /path/to/project/module1 --output module1.json
sentinelagent /path/to/project/module2 --output module2.json
```

## Advanced Usage

### Custom Output Directories
```bash
# Organize outputs by date
mkdir -p results/$(date +%Y%m%d)
sentinelagent /path/to/project --output results/$(date +%Y%m%d)/scan.json
```

### Filtering Large Results
```bash
# Use jq to filter results
sentinelagent /path/to/project --output - | jq '.agents[] | select(.type=="CrewAI")'
```

### Integration with Other Tools
```bash
# Pipe to analysis scripts
sentinelagent /path/to/project --verbose | grep "ERROR" > errors.log

# Combine with monitoring
sentinelagent /path/to/project --all && notify-send "Analysis complete"
```
