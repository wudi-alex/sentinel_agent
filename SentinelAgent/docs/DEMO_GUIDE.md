# SentinelAgent Demo Guide

## 🎉 Status: COMPLETE & OPTIMIZED

This comprehensive guide provides step-by-step instructions for running all SentinelAgent demonstrations. The demo system has been fully optimized with clean, focused scripts and comprehensive web UI integration.

**Last Updated**: June 8, 2025 | **Demo Optimization**: ✅ COMPLETE

## Overview of Available Demos

The SentinelAgent project includes comprehensive demo scripts designed to showcase different aspects of the system:

| Demo Script | Purpose | Level | Estimated Time |
|-------------|---------|-------|----------------|
| `unified_demo.py` | **Main comprehensive demo** - Complete feature showcase | Beginner | 10-15 minutes |
| `example.py` | **Basic usage examples** - Simple scanning demonstrations | Beginner | 5 minutes |
| `graph_demo.py` | Advanced graph structure analysis and metrics | Intermediate | 5-10 minutes |
| `path_demo.py` | Security-focused path analysis and vulnerability detection | Intermediate | 5-10 minutes |
| `log_analysis_demo.py` | Specialized log analysis and anomaly detection | Advanced | 5-10 minutes |

## Prerequisites

### System Requirements
- Python 3.8 or higher
- Operating System: Linux, macOS, or Windows  
- Terminal/Command prompt access
- At least 100MB free disk space

### Required Project Structure
The demos expect the following project structure in `/Users/xuhe/Documents/agent_experiments/`:
```
agent_experiments/
├── SentinelAgent/           # Main SentinelAgent project
├── crewai_gmail/           # CrewAI demo project with agents and tools
└── autogen_magneticone/    # AutoGen/MagneticOne demo project with logs
```

### Installation
1. **Install SentinelAgent** (if not already installed):
   ```bash
   cd /Users/xuhe/Documents/agent_experiments/SentinelAgent
   pip install -e .
   ```

2. **Verify installation**:
   ```bash
   python -c "import sentinelagent; print('SentinelAgent installed successfully')"
   ```

3. **Navigate to demo directory**:
   ```bash
   cd /Users/xuhe/Documents/agent_experiments/SentinelAgent/examples
   ```

## Demo 1: Basic Examples

### Purpose
Simple demonstrations of core SentinelAgent functionality:
- Scanning CrewAI projects for agents and tools
- Scanning AutoGen projects for agent components  
- Self-scanning the SentinelAgent project
- CLI command examples with absolute paths

### How to Run
```bash
cd /Users/xuhe/Documents/agent_experiments/SentinelAgent/examples
python example.py
```

### What to Expect
- Scans the CrewAI Gmail project at `/Users/xuhe/Documents/agent_experiments/crewai_gmail`
- Scans an AutoGen file at `/Users/xuhe/Documents/agent_experiments/autogen_magneticone`
- Shows CLI command examples with absolute paths
- Displays scan summaries and found components

### Sample Output
```
🤖 SentinelAgent Examples
==================================================
🔍 Example 1: Scan CrewAI Gmail project
--------------------------------------------------
✅ Scan completed for: /Users/xuhe/Documents/agent_experiments/crewai_gmail
📊 Found: 8 agents, 0 tools

🔍 Example 2: Scan single AutoGen file
--------------------------------------------------
✅ File scan completed for: /Users/xuhe/Documents/agent_experiments/autogen_magneticone/autogen_remote_server_upload_file.py
📊 Found: 0 tools

💻 CLI Equivalent Commands
--------------------------------------------------
# Scan CrewAI directory:
python -m sentinelagent.cli.main /Users/xuhe/Documents/agent_experiments/crewai_gmail

# Scan AutoGen directory:
python -m sentinelagent.cli.main /Users/xuhe/Documents/agent_experiments/autogen_magneticone

# Scan specific file:
python -m sentinelagent.cli.main /Users/xuhe/Documents/agent_experiments/crewai_gmail/tools.py
```

## Demo 2: Unified Demo (Main Interactive Demo)

### Purpose
The unified demo is your comprehensive starting point. It provides:
- Complete system feature showcase
- Interactive scanning demonstrations with real projects
- Graph building and analysis
- Web UI explanations and tutorials
- API documentation and examples
- Target-specific scanning for CrewAI and AutoGen projects

### How to Run

```bash
cd /Users/xuhe/Documents/agent_experiments/SentinelAgent/examples/demos
python unified_demo.py
```

### What to Expect

1. **Interactive Menu**: The demo presents a menu-driven interface
2. **Multiple Demo Sections**: Choose from scanning, graph building, web UI overview, etc.
3. **Real Project Scanning**: Options to scan actual CrewAI and AutoGen projects
4. **Generated Files**: Creates various output files (graphs, scans, analyses)
5. **Detailed Explanations**: Each feature includes explanatory text
6. **Duration**: 10-15 minutes for full exploration

### Target Scanning Options

The unified demo now includes target-specific scanning:

- **Option 1**: CrewAI Gmail project (`/Users/xuhe/Documents/agent_experiments/crewai_gmail`)
- **Option 2**: AutoGen MagneticOne project (`/Users/xuhe/Documents/agent_experiments/autogen_magneticone`) 
- **Option 3**: SentinelAgent project (current directory)
- **Option 4**: Custom path input

### Sample Output

```text
============================================================
🔍 SentinelAgent - Unified Demo Platform
   AI Agent System Analysis & Monitoring
============================================================

📋 Main Demo Menu
----------------------------------------
1. 🎮 Interactive Core Demos (scanning, graph building)
2. 🌐 Web UI Features Overview
3. 🔗 API Endpoints Documentation
4. 🔒 Security Analysis Features
5. 📖 Usage Instructions
6. 🔧 Technical Implementation Details
7. 🎯 Run All Demonstrations
0. Exit

Please enter your choice (0-7):
```

### Generated Files

- `unified_scan_result.json` - Directory scan results
- `unified_graph_result.json` - Generated graph data
- `unified_paths_result.json` - Path analysis results
- Various timestamped output files in `data/output/`

## Demo 3: Graph Analysis Demo

### Purpose
Advanced graph structure analysis including:
- Node importance ranking (in-degree/out-degree analysis)
- Graph topology insights and detailed metrics
- Hub identification and connectivity analysis
- Automated report generation

### Prerequisites
- Run `unified_demo.py` first to generate graph data, OR
- Have existing graph JSON files in the directory

### How to Run
```bash
python graph_demo.py
```

### What to Expect
1. **Automatic Graph Loading**: Loads existing graph files or creates new ones
2. **Detailed Analysis**: Comprehensive graph metrics and statistics
3. **Visual Insights**: Node rankings and relationship analysis
4. **Report Generation**: Creates a detailed markdown report

### Sample Output
```
🔍 SentinelAgent - Advanced Graph Analysis Demo
============================================================
📊 Loading existing graph: unified_demo_graph.json

🔍 Advanced Graph Structure Analysis
============================================================

📊 Basic Graph Statistics:
   • Total nodes: 156
   • Total edges: 203
   • Average degree: 2.60
   • Maximum in-degree: 15
   • Maximum out-degree: 12
   • Graph density: 0.017

🌟 Most Influential Nodes (by out-degree):
   1. main_controller.py (function) - out-degree: 12
   2. security_scanner.py (class) - out-degree: 8
   3. data_processor.py (module) - out-degree: 7
```

### Generated Files
- `graph_analysis_report.md` - Detailed analysis report
- `graph_analysis_demo.json` - New graph (if created)

## Demo 3: Path Analysis Demo

### Purpose
Security-focused path analysis featuring:
- Advanced path security analysis and risk assessment
- Path traversal vulnerability detection
- Security-focused insights and recommendations
- Threat modeling for file system access patterns

### Prerequisites
- Existing graph or path analysis files, OR
- Run `unified_demo.py` first to generate base data

### How to Run
```bash
python path_demo.py
```

### What to Expect
1. **Security Analysis**: Focus on path-based security vulnerabilities
2. **Risk Assessment**: Identification of high-risk paths and patterns
3. **Vulnerability Detection**: Detection of potential path traversal issues
4. **Detailed Reporting**: Security-focused analysis and recommendations

### Sample Output
```
🛡️ SentinelAgent - Advanced Path Security Analysis Demo
========================================================

🔍 Loading existing analysis: unified_demo_paths.json

🛡️ Advanced Path Security Analysis
========================================================

📊 Path Security Overview:
   • Total paths analyzed: 89
   • High-risk paths: 7
   • Medium-risk paths: 23
   • Low-risk paths: 59

⚠️ High-Risk Path Detection:
   1. /admin/config/*.conf - Configuration exposure risk
   2. /uploads/../* - Path traversal vulnerability
   3. /logs/sensitive.log - Sensitive data exposure
```

### Generated Files
- `path_security_report.md` - Security analysis report
- `security_paths_demo.json` - Security-focused path data

## Demo 4: Log Analysis Demo

### Purpose
Specialized log analysis capabilities including:
- Advanced anomaly detection in execution logs
- Performance pattern analysis and optimization insights
- Security incident detection and alerting
- Log correlation and trend analysis

### Prerequisites
- Existing log files in the project, OR
- Generated logs from previous demo runs

### How to Run
```bash
python log_analysis_demo.py
```

### What to Expect
1. **Log Discovery**: Automatic detection of available log files
2. **Anomaly Detection**: Identification of unusual patterns
3. **Performance Analysis**: Bottleneck and optimization insights
4. **Security Monitoring**: Detection of potential security incidents

### Sample Output
```
📊 SentinelAgent - Advanced Log Analysis Demo
==============================================

🔍 Discovering log files...
Found 5 log files for analysis

📈 Advanced Log Analysis Results
==============================================

⚠️ Anomalies Detected:
   • High error rate detected at 2025-06-08 14:30:15
   • Unusual access pattern in security logs
   • Performance degradation: 3x slower response times

🔒 Security Incidents:
   • Failed authentication attempts: 15
   • Suspicious file access patterns detected
   • Potential intrusion attempt logged
```

### Generated Files
- `log_analysis_report.md` - Comprehensive log analysis
- `anomaly_detection_results.json` - Detected anomalies
- `security_incidents.json` - Security-related findings

## Demo 5: Web UI Interactive Demo

### Purpose
The Web UI provides a complete visual interface for all SentinelAgent features:
- **No Setup Required**: Instant demo data without configuration
- **Realistic Scenarios**: Based on real-world agent system patterns
- **Complete Coverage**: All major features demonstrated with one-click loading
- **Interactive Experience**: Full UI functionality with sample data

### Web UI Features Overview

#### 1. System Scanner
- 📁 Select project directory or file  
- 🔍 Automatically identify Agent, Tool, Task, Crew
- 📊 Generate comprehensive scan reports
- **Demo Button**: Load sample agent system scan results

#### 2. Relationship Graph Builder
- 🕸️ Build execution graph based on scan results
- 🎨 Interactive D3.js visualization with zoom and pan
- 📈 Graph structure statistical analysis
- **Demo Button**: Load interactive graph with sample relationships

#### 3. Path Analyzer  
- 🛤️ Discover all possible execution paths
- ⚠️ Identify potential security vulnerabilities and problematic paths
- 🔧 Risk assessment and optimization suggestions
- **Demo Button**: Load security-focused path analysis

#### 4. Log Analyzer
- 📋 Analyze runtime logs and execution patterns
- 🚨 Detect errors, exceptions, and anomalies
- 📈 Performance monitoring and trend analysis
- **Demo Button**: Load comprehensive log analysis with anomaly detection

#### 5. Results Management
- 📁 Browse all analysis results by type (scan, graph, paths, logs, security)
- 📊 View detailed file metadata and descriptions
- 🔍 Interactive result viewing and exploration
- **Demo Button**: Load complete demo result set

### How to Run Web UI Demo

```bash
# 1. Start the web service
cd /Users/xuhe/Documents/agent_experiments/SentinelAgent
python scripts/start_web_ui.py

# 2. Open browser and navigate to:
# http://localhost:5002
```

### Demo Workflow Sequence

1. **Scanner Tab** → Click "Load Demo Data" → View agent system scan results
2. **Graph Tab** → Click "Load Demo Graph" → Explore interactive relationship visualization  
3. **Paths Tab** → Click "Load Demo Paths" → Analyze security insights and risk assessment
4. **Logs Tab** → Click "Load Demo Logs" → Review execution analysis and anomaly detection
5. **Results Tab** → Click "Load Demo Results" → Browse all result types and view details

### Demo Data Statistics

The web UI demo includes realistic data representing:

#### System Overview
- **Agents**: 3 (email_classifier, email_responder, task_manager)
- **Tools**: 2 (EmailTool, ClassificationTool)  
- **Crews**: 1 (email_crew)
- **Tasks**: 4 (classify, respond, monitor, report)
- **Total Nodes**: 10
- **Total Edges**: 12

#### Security Analysis  
- **Overall Risk Score**: 0.42 (Medium risk)
- **Critical Vulnerabilities**: 1 (Privilege escalation)
- **High Risk Vulnerabilities**: 1 (Unencrypted communication)
- **Medium Risk Issues**: 1 (Input validation)
- **Security Recommendations**: 5 actionable items

#### Execution Analysis
- **Total Log Entries**: 156
- **Execution Paths**: 4 tracked paths
- **Success Rate**: 87.5%
- **Anomalies Detected**: 4 (errors, performance, security)
- **Average Execution Time**: 2.8 seconds

### Key Benefits

#### For Demonstrations
- **No Setup Required**: Instant demo data without external configuration
- **Realistic Scenarios**: Based on real-world agent system patterns
- **Complete Coverage**: All major features demonstrated
- **Interactive Experience**: Full UI functionality with sample data

#### For Development  
- **Testing Framework**: Comprehensive data for feature testing
- **API Examples**: Reference implementation for all endpoints
- **UI Components**: Complete demo integration patterns
- **Data Structures**: Proper formatting examples

#### For Users
- **Learning Tool**: Understand features before using real data
- **Feature Exploration**: Try all capabilities risk-free  
- **Best Practices**: See recommended analysis workflows
- **Quick Validation**: Verify installation and functionality

### Demo Scenarios Covered

#### 1. Complete System Scan
- Multi-agent system with realistic configuration
- Tools and crew relationships
- Task assignments and dependencies

#### 2. Security Analysis
- Privilege escalation vulnerabilities
- Cross-agent communication risks
- Input validation weaknesses
- Compliance assessment

#### 3. Execution Monitoring
- Real-time log analysis
- Performance bottleneck detection
- Error pattern recognition
- Success rate tracking

#### 4. Comprehensive Reporting
- Combined analysis results
- Executive summary views
- Detailed technical findings
- Actionable recommendations

## Demo Cleanup & Optimization Summary

### ✅ Completed Optimizations (June 8, 2025)

The SentinelAgent demo system has undergone comprehensive cleanup and optimization:

#### File Removals
**Removed redundant demo files** (functionality merged into `unified_demo.py`):
- ❌ `complete_demo.py` (313 lines) - Basic comprehensive demo
- ❌ `demo_enhanced.py` (142 lines) - Enhanced scanning features  
- ❌ `demo.py` (104 lines) - Basic scanning demo

#### Optimized Demo Structure

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `unified_demo.py` | **Main comprehensive demo** - Start here | 651 | ✅ Complete |
| `graph_demo.py` | Advanced graph structure analysis and metrics | 311 | ✅ Rewritten |
| `path_demo.py` | Security-focused path analysis and vulnerability detection | 337 | ✅ Cleaned |
| `log_analysis_demo.py` | Specialized log analysis and anomaly detection | 387 | ✅ Cleaned |

#### Benefits Achieved

- **Maintainability**: Eliminated code duplication, clear separation of concerns
- **User Experience**: Clear progression from basic to advanced features  
- **Code Quality**: Removed redundant code (559 lines total), enhanced existing demos
- **Organization**: Logical demo sequence and dependencies, clean file structure

## Running All Demos (Recommended Sequence)

For the best experience, run the demos in this order:

```bash
# 1. Start with the main demo (creates base data)
python unified_demo.py

# 2. Analyze the generated graph structure
python graph_demo.py

# 3. Perform security-focused path analysis
python path_demo.py

# 4. Analyze logs and detect anomalies
python log_analysis_demo.py
```

## Troubleshooting

### Common Issues

#### 1. Import Errors
**Problem**: `ModuleNotFoundError: No module named 'sentinelagent'`

**Solution**:
```bash
# Make sure you're in the SentinelAgent directory
cd /Users/xuhe/Documents/agent_experiments/SentinelAgent

# Install in development mode
pip install -e .

# Verify installation
python -c "import sentinelagent"
```

#### 2. No Graph Files Found
**Problem**: Graph demo can't find existing graph files

**Solution**:
```bash
# Run the unified demo first to generate base data
python unified_demo.py
# Then run the graph demo
python graph_demo.py
```

#### 3. Permission Errors
**Problem**: Cannot write output files

**Solution**:
```bash
# Check directory permissions
ls -la examples/demos/

# Ensure write access to the demos directory
chmod 755 examples/demos/
```

#### 4. Missing Target Directories
**Problem**: "Directory not found" errors when running demos

**Solution**:
```bash
# Verify the target directories exist
ls -la /Users/xuhe/Documents/agent_experiments/crewai_gmail
ls -la /Users/xuhe/Documents/agent_experiments/autogen_magneticone

# If missing, the demos will still work but with limited examples
# You can create sample directories or modify the demo paths as needed
```

#### 5. Missing Dependencies
**Problem**: Some analysis features unavailable

**Solution**:
```bash
# Install additional dependencies if needed
pip install -r requirements.txt

# For development dependencies
pip install -e .[dev]
```

### Getting Help

1. **Check the output**: All demos provide detailed status messages
2. **Review generated files**: Check output files for additional insights
3. **Consult documentation**: See `docs/` directory for more information
4. **Check logs**: Look in `data/output/` for detailed logs

## Understanding the Output

### File Organization
```
SentinelAgent/
├── examples/demos/          # Demo scripts
├── data/output/            # Generated outputs (timestamped)
├── data/demo/              # Demo-specific data
└── docs/                   # Documentation including this guide
```

### Output Files Explained

| File Pattern | Content | Purpose |
|--------------|---------|---------|
| `*_demo.json` | Core data files | Base data for analysis |
| `*_report.md` | Analysis reports | Human-readable insights |
| `scan_*.json` | Directory scans | File system analysis |
| `graph_*.json` | Graph structures | Relationship mapping |
| `paths_*.json` | Path analysis | Security path data |

### Interpreting Results

- **High numbers** in metrics generally indicate complexity
- **Isolated nodes** may represent unused or orphaned code
- **High-degree nodes** are often critical system components
- **Security findings** should be investigated and addressed

## Next Steps

After running the demos:

1. **Review generated reports** for insights about your system
2. **Explore the Web UI** (see `docs/QUICK_START.md`)
3. **Try the CLI tools** (see `docs/CLI_USAGE.md`)
4. **Integrate into your workflow** using the API
5. **Customize analysis** for your specific needs

## Integration Examples

### CI/CD Integration
```bash
# Add to your CI pipeline
python unified_demo.py --automated
python graph_demo.py --report-only
```

### Scheduled Analysis
```bash
# Create a cron job for regular analysis
0 2 * * * cd /Users/xuhe/Documents/agent_experiments/SentinelAgent && python examples/demos/unified_demo.py
```

### Custom Workflows
```python
# Import SentinelAgent modules in your own scripts
from sentinelagent.core.scanner import scan_directory
from sentinelagent.core.graph_builder import build_graph_from_scan

# Your custom analysis code here
```

---

## Additional Resources

- **Quick Start Guide**: `docs/QUICK_START.md`
- **Installation Guide**: `docs/INSTALLATION.md` 
- **CLI Usage**: `docs/CLI_USAGE.md`
- **API Documentation**: `docs/` directory
- **Docker Deployment**: `docs/deployment/DOCKER_DEPLOYMENT.md`

---

**Happy analyzing! 🚀**

For questions or issues, please check the existing documentation or create an issue in the project repository.

---

## Documentation Organization

This `DEMO_GUIDE.md` is the consolidated demo documentation that combines and replaces:
- ❌ `DEMO_CLEANUP_SUMMARY.md` (merged - cleanup details included above)
- ❌ `DEMO.md` (merged - web UI demo features included above)  

All demo-related information is now centralized in this single comprehensive guide.
