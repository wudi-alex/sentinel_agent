# 🤖 SentinelAgent
*Advanced Agent System Analysis & Monitoring Platform*

![SentinelAgent](https://img.shields.io/badge/SentinelAgent-v2.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Overview

SentinelAgent is a comprehensive platform for analyzing, monitoring, and optimizing AI agent systems. It provides deep insights into agent configurations, execution graphs, potential issues, and runtime behaviors through an intuitive web interface.

## ✨ Key Features

### 🔍 **System Analysis**
- **Agent Discovery**: Automatically scan and identify agents, tools, tasks, and crews
- **Configuration Analysis**: Deep dive into agent configurations and relationships
- **Structure Validation**: Verify system architecture and dependencies

### 🕸️ **Execution Graph Building**
- **Visual Graph Generation**: Create interactive execution flow diagrams
- **Relationship Mapping**: Understand data flow and control relationships
- **Graph Optimization**: Identify bottlenecks and optimization opportunities

### 🛤️ **Path Analysis**
- **Execution Path Discovery**: Find all possible execution routes
- **Correctness Verification**: Identify potential incorrect execution paths
- **Performance Analysis**: Detect inefficient execution patterns

### 📋 **Runtime Log Analysis**
- **Error Detection**: Automatically identify runtime errors and issues
- **Performance Monitoring**: Track execution times and resource usage
- **Behavioral Analysis**: Understand real-world agent behavior patterns

### 🌐 **Modern Web Interface**
- **Interactive Dashboard**: Beautiful, responsive web UI
- **Real-time Visualization**: Live graphs and charts
- **Demo Mode**: Test features with built-in demo data

## 🚀 Quick Start

### 🐳 Docker Deployment (Recommended)

The simplest deployment method is using Docker:

```bash
# Clone the project
git clone https://github.com/your-repo/SentinelAgent.git
cd SentinelAgent

# Build and start services
./scripts/docker_build.sh
./scripts/docker_deploy.sh start

# Access the application
open http://localhost:5002
```

#### Docker Management Commands
```bash
# Check service status
./scripts/docker_deploy.sh status

# View logs
./scripts/docker_deploy.sh logs

# Stop services
./scripts/docker_deploy.sh stop

# Restart services
./scripts/docker_deploy.sh restart
```

### 📦 Local Installation

#### Installation
```bash
git clone https://github.com/your-repo/SentinelAgent.git
cd SentinelAgent
pip install -r requirements.txt
```

#### Launch Web Interface
```bash
python scripts/start_web_ui.py
```

Visit: **http://localhost:5002**

### Command Line Usage
```bash
# Scan an agent system
python src/core/scanner.py --path /path/to/agent/project

# Build execution graph
python src/core/graph_builder.py --input scan_results.json

# Analyze execution paths
python src/core/path_analyzer.py --graph graph_results.json

# Analyze runtime logs
python src/core/log_analyzer.py --logs /path/to/logs
```

## 📁 Project Structure

```
SentinelAgent/
├── 📁 src/                    # Core source code
│   ├── 📁 core/              # Core analysis engines
│   ├── 📁 web/               # Web application
│   └── 📁 utils/             # Utility functions
├── 📁 web/                   # Web interface assets
│   ├── 📁 static/            # CSS, JS, images
│   └── 📁 templates/         # HTML templates
├── 📁 docs/                  # Documentation
├── 📁 examples/              # Example usage
├── 📁 tests/                 # Test suite
├── 📁 data/                  # Data storage
│   ├── 📁 output/            # Analysis results
│   ├── 📁 uploads/           # Uploaded files
│   └── 📁 demo/              # Demo data
├── 📁 config/                # Configuration files
└── 📁 scripts/               # Utility scripts
```

## 🛠️ Technology Stack

- **Backend**: Python Flask + CORS
- **Frontend**: Vue.js 3 + Element Plus
- **Visualization**: D3.js
- **Analysis**: NetworkX, Pandas
- **File Processing**: JSON, CSV, Text parsing

## 📊 Supported Agent Frameworks

- ✅ **CrewAI**: Full support for crews, agents, tasks, tools
- ✅ **AutoGen**: Support for agent conversations and workflows  
- ✅ **LangChain**: Agent chains and tool integrations
- ✅ **Custom Frameworks**: Extensible architecture

## 🎮 Demo Mode

SentinelAgent includes rich demo data to explore features:
- Sample agent configurations
- Pre-built execution graphs
- Simulated runtime logs
- Interactive examples

## 📖 Documentation

- [📚 User Guide](docs/USER_GUIDE.md)
- [🔧 API Reference](docs/API_REFERENCE.md)
- [🎯 Quick Start](docs/QUICK_START.md)
- [🐳 Docker Deployment](docs/DOCKER_DEPLOYMENT.md)
- [⚙️ Configuration](docs/CONFIGURATION.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md).

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

Built with ❤️ for the AI agent development community.

---

**SentinelAgent** - *Your AI Agent System Guardian*
