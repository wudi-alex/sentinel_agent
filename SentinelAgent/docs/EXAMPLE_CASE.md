# SentinelAgent Examples

This directory contains focused examples demonstrating SentinelAgent's capabilities on real AI agent projects.

## Overview

The examples focus on analyzing two specific AI agent projects:
- **CrewAI Gmail Project**: Demonstrates email classification using CrewAI agents
- **AutoGen MagneticOne Project**: Shows multi-agent systems with web surfing and file handling capabilities

## Files

### `example.py`
Main demonstration script that performs comprehensive analysis of both target projects.

**Features:**
- Full directory scanning with detailed results
- Individual file analysis
- Security issue detection
- Results saved to JSON files
- CLI usage examples
- Formatted output with visual indicators

**Usage:**
```bash
# Run all examples
python examples/example.py

# Run from project root
python -m examples.example
```

### `scan_results/`
Directory containing detailed JSON outputs from scans:
- `crewai_gmail_scan_results.json` - Complete analysis of CrewAI Gmail project
- `autogen_magneticone_scan_results.json` - Complete analysis of AutoGen MagneticOne project

## Target Projects

### CrewAI Gmail Project
**Location:** `/Users/xuhe/Documents/agent_experiments/crewai_gmail`

**Key Files:**
- `crewai_mail_test.py` - Main email classification logic with agents
- `tools.py` - Email sending and processing tools
- `google_service_utils.py` - Gmail API integration
- `Attack_Paths.py` - Various agent attack scenarios

**What SentinelAgent Detects:**
- Email classifier agents
- Gmail API integration tools
- Task definitions and crew configurations
- Potential security considerations in email handling

### AutoGen MagneticOne Project
**Location:** `/Users/xuhe/Documents/agent_experiments/autogen_magneticone`

**Key Files:**
- `autogen_remote_server_upload_file.py` - Main MagneticOne setup with web surfer
- `payload.py` - File upload and SSH operations
- `forbiden_web_server.py` - Web server implementation

**What SentinelAgent Detects:**
- Multi-agent chat systems
- Web surfing capabilities
- File system operations
- Network operations and potential security issues

## Expected Output

When you run `example.py`, you'll see:

1. **CrewAI Gmail Analysis**
   - Directory scan results with agent/tool counts
   - Individual file breakdowns
   - Detailed agent information (roles, types, files)

2. **AutoGen MagneticOne Analysis**
   - Multi-agent system detection
   - Tool and capability identification
   - Security issue flagging

3. **Saved Results**
   - JSON files in `scan_results/` directory
   - Detailed metadata and findings

4. **CLI Examples**
   - Ready-to-use command line examples
   - Various scanning options and output formats

## CLI Usage Examples

Basic scanning:
```bash
# Scan CrewAI project
python -m sentinelagent.cli.main /Users/xuhe/Documents/agent_experiments/crewai_gmail

# Scan AutoGen project
python -m sentinelagent.cli.main /Users/xuhe/Documents/agent_experiments/autogen_magneticone
```

Advanced analysis:
```bash
# Full analysis with security checks
python -m sentinelagent.cli.main /Users/xuhe/Documents/agent_experiments/crewai_gmail --all

# Save to custom file
python -m sentinelagent.cli.main /Users/xuhe/Documents/agent_experiments/autogen_magneticone --output analysis.json
```

Individual file scanning:
```bash
# Scan specific files
python -m sentinelagent.cli.main /Users/xuhe/Documents/agent_experiments/crewai_gmail/tools.py
python -m sentinelagent.cli.main /Users/xuhe/Documents/agent_experiments/autogen_magneticone/payload.py
```

Web interface:
```bash
# Start interactive web UI
python -m sentinelagent.cli.start_web_ui
# Navigate to: http://localhost:8000
```

## Prerequisites

1. **SentinelAgent installed:**
   ```bash
   pip install -e .
   ```

2. **Target projects exist:**
   - Ensure both crewai_gmail and autogen_magneticone projects are available
   - Paths in example.py may need adjustment for your setup

3. **Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Customization

To adapt these examples for your own projects:

1. **Update target paths** in `example.py`:
   ```python
   target_dir = "/path/to/your/agent/project"
   ```

2. **Modify key_files lists** to match your project structure

3. **Adjust display_scan_results()** function for custom output formatting

## Related Documentation

- `../docs/DEMO_GUIDE.md` - Comprehensive usage guide
- `../README.md` - Project overview and installation
- `../docs/` - Full documentation directory

## Troubleshooting

**Common Issues:**
- **"Directory does not exist"**: Update paths in example.py to match your setup
- **Import errors**: Ensure SentinelAgent is properly installed (`pip install -e .`)
- **Permission errors**: Check file/directory permissions for target projects

**Getting Help:**
- Check the main project documentation
- Review the comprehensive demo guide
- Examine the JSON output files for detailed analysis
