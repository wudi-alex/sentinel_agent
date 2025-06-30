# SentinelAgent Quick Start Guide

## 🚀 Quick Installation

### 1. Clone the Project
```bash
git clone <repository-url>
cd SentinelAgent
```

### 2. Install as Package (Recommended)
```bash
pip install -e .
```

**For detailed installation options, see [Installation Guide](INSTALLATION.md)**

### 3. Start the Web Interface

#### Option A: Using Python Module (Recommended)
```bash
python -m sentinelagent.cli.start_web_ui
```

#### Option B: Install as Package and Use Entry Points
```bash
pip install -e .
sentinelagent-web
```

Visit: **http://localhost:5002**

## 🔧 Command Line Usage

### System Scan
```bash
# Using Python module
python -m sentinelagent.cli.main /path/to/agent/project

# Or after installing as package
sentinelagent /path/to/agent/project

# Scan with specific output file
python -m sentinelagent.cli.main /path/to/agent/project --output my_scan.json
```

### Build Execution Graph
```bash
# Build graph from scan results
python -m sentinelagent.cli.main /path/to/project --graph graph_results.json

# Build both scan and graph
python -m sentinelagent.cli.main /path/to/project --output scan.json --graph graph.json
```

### Path Analysis
```bash
# Analyze execution paths
python -m sentinelagent.cli.main /path/to/project --paths path_analysis.json

# Full analysis (scan + graph + paths)
python -m sentinelagent.cli.main /path/to/project --all
```

### Specialized Analysis
```bash
# Analyze existing graph file
python -m sentinelagent.cli.main --analyze-graph graph_results.json

# Analyze runtime logs
python -m sentinelagent.cli.main --analyze-logs /path/to/logfile.txt
python -m sentinelagent.cli.main --analyze-logs /path/to/logfile.csv --log-format csv
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
    python -m sentinelagent.cli.main "$project" --output "scan_$(basename $project).json"
done
```

### Export Results
All analysis results are automatically saved in the `data/generated_outputs/` directory, supporting:
- JSON format results
- Graph visualization exports
- Path analysis reports
- Log analysis summaries
- CSV data export

## 🔧 Configuration

Edit `config/sentinel_agent.conf` to customize:
- Server port and host
- File path configuration
- Analysis parameter adjustment
- Log level settings

## 📚 More Documentation

- [Installation Guide](INSTALLATION.md) - Detailed installation instructions
- [CLI Usage Guide](CLI_USAGE.md) - Complete command-line reference
- [Docker Deployment](DOCKER_DEPLOYMENT.md) - Container deployment guide
- [Directory Structure](DIRECTORY_STRUCTURE.md) - Project organization overview
