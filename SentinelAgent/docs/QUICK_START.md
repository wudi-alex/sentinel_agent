# SentinelAgent Quick Start Guide

## 🚀 Quick Installation

### 1. Clone the Project
```bash
git clone <repository-url>
cd SentinelAgent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Web Interface
```bash
python scripts/start_web_ui.py
```

Or use the main program:
```bash
python sentinel_agent.py --web
```

Visit: **http://localhost:5002**

## 🔧 Command Line Usage

### System Scan
```bash
# Scan a directory
python sentinel_agent.py scan --path /path/to/agent/project

# Scan a single file
python sentinel_agent.py scan --path /path/to/agent/file.py --type file
```

### Build Execution Graph
```bash
# Build graph from scan results
python sentinel_agent.py build-graph --input scan_results.json

# Build graph directly from project
python sentinel_agent.py build-graph --path /path/to/project
```

### Path Analysis
```bash
# Analyze execution paths
python sentinel_agent.py analyze-paths --graph graph_results.json
```

### Log Analysis
```bash
# Analyze runtime logs
python sentinel_agent.py analyze-logs --logs /path/to/logfile.txt
python sentinel_agent.py analyze-logs --logs /path/to/logfile.txt --graph graph_results.json
```

## 🌐 Web Interface Features

### 1. System Scanner
- 📁 Select project directory or file
- 🔍 Automatically identify Agent, Tool, Task, Crew
- 📊 Generate scan report

### 2. Graph Builder
- 🕸️ Build execution graph based on scan results
- 🎨 Interactive visualization interface
- 📈 Graph structure statistical analysis

### 3. Path Analyzer
- 🛤️ Discover all possible execution paths
- ⚠️ Identify potential problematic paths
- 🔧 Provide optimization suggestions

### 4. Log Analyzer
- 📋 Analyze runtime logs
- 🚨 Detect errors and exceptions
- 📈 Performance monitoring and analysis

## 💡 Tips

### Demo Mode
The web interface provides built-in demo data, allowing you to experience all features without a real project:
- Click the "Load Demo Data" button
- Experience the full analysis workflow

### Batch Processing
```bash
# Batch scan multiple projects
for project in /path/to/projects/*; do
    python sentinel_agent.py scan --path "$project" --output "scan_$(basename $project).json"
done
```

### Export Results
All analysis results are automatically saved in the `data/output/` directory, supporting:
- JSON format results
- Image export
- CSV data export

## 🔧 Configuration

Edit `config/sentinel_agent.conf` to customize:
- Server port and host
- File path configuration
- Analysis parameter adjustment
- Log level settings

## 📚 More Documentation

- [User Guide](USER_GUIDE.md)
- [API Reference](API_REFERENCE.md)
- [Configuration Guide](CONFIGURATION.md)
- [Development Guide](DEVELOPMENT.md)
