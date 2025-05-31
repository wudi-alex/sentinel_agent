#!/usr/bin/env python3
"""
SentinelAgent Web UI - Flask Application
Web interface for AI Agent system analysis and monitoring platform
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

# Import SentinelAgent core modules
from core.scanner import scan_directory, scan_file
from core.graph_builder import build_graph_from_scan, scan_and_build_graph
from core.path_analyzer import analyze_graph_paths, analyze_and_save_paths
from core.log_analyzer import ExecutionLogAnalyzer
from utils.path_resolver import get_examples_config, resolve_path

# Get project root directory
project_root = Path(__file__).parent.parent.parent
web_dir = project_root / "web"

app = Flask(__name__, 
           template_folder=str(web_dir / "templates"),
           static_folder=str(web_dir / "static"))
CORS(app)

# Configuration
app.config['OUTPUT_DIR'] = str(project_root / 'data' / 'output')
app.config['UPLOAD_FOLDER'] = str(project_root / 'data' / 'uploads')

# Ensure output directories exist
os.makedirs(app.config['OUTPUT_DIR'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/health')
def health_check():
    """Health check endpoint - for Docker health checks"""
    try:
        # Check basic functionality
        status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'service': 'SentinelAgent Web UI',
            'version': '1.0.0',
            'uptime': 'running'
        }
        
        # Check if output directory is accessible
        if not os.path.exists(app.config['OUTPUT_DIR']):
            status['status'] = 'degraded'
            status['message'] = 'Output directory not accessible'
            return jsonify(status), 503
            
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }), 503


@app.route('/api/scan', methods=['POST'])
def api_scan():
    """Scan API endpoint"""
    try:
        data = request.get_json()
        target_path = data.get('path')
        scan_type = data.get('type', 'directory')  # directory, file
        
        if not target_path:
            return jsonify({'error': 'Please provide scan path'}), 400
        
        # Resolve path - support relative paths in container
        resolved_path = resolve_path(target_path)
        
        # Check if path exists
        if not os.path.exists(resolved_path):
            return jsonify({'error': f'Path does not exist: {target_path} (resolved to: {resolved_path})'}), 400
            
        # Execute scan
        if scan_type == 'directory':
            result = scan_directory(resolved_path)
        else:
            result = scan_file(resolved_path)
            
        # Save scan results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(app.config['OUTPUT_DIR'], f'scan_{timestamp}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
            
        return jsonify({
            'success': True,
            'result': result,
            'output_file': output_file
        })
        
    except Exception as e:
        logger.error(f"Scan error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/build-graph', methods=['POST'])
def api_build_graph():
    """Build relationship graph API endpoint"""
    try:
        data = request.get_json()
        scan_data = data.get('scan_data')
        target_path = data.get('path')
        
        if not scan_data and not target_path:
            return jsonify({'error': 'Please provide scan data or path'}), 400
            
        # Build graph
        if scan_data:
            graph_data = build_graph_from_scan(scan_data)
        else:
            graph_data = scan_and_build_graph(target_path)
            
        # Save graph data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(app.config['OUTPUT_DIR'], f'graph_{timestamp}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
            
        return jsonify({
            'success': True,
            'result': {
                **graph_data,
                'metadata': graph_data.get('graph_summary', {}),
                'graph_summary': graph_data.get('graph_summary', {})
            },
            'output_file': output_file
        })
        
    except Exception as e:
        logger.error(f"Graph building error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze-paths', methods=['POST'])
def api_analyze_paths():
    """Path analysis API endpoint"""
    try:
        data = request.get_json()
        graph_data = data.get('graph_data')
        graph_file = data.get('graph_file')
        
        if not graph_data and not graph_file:
            return jsonify({'error': 'Please provide graph data or graph file path'}), 400
            
        # Path analysis
        if graph_data:
            paths_data = analyze_graph_paths(graph_data)
        else:
            with open(graph_file, 'r', encoding='utf-8') as f:
                graph_data = json.load(f)
            paths_data = analyze_graph_paths(graph_data)
            
        # Save path analysis results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(app.config['OUTPUT_DIR'], f'paths_{timestamp}.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(paths_data, f, indent=2, ensure_ascii=False)
            
        return jsonify({
            'success': True,
            'result': paths_data,
            'output_file': output_file
        })
        
    except Exception as e:
        logger.error(f"Path analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze-logs', methods=['POST'])
def api_analyze_logs():
    """Log analysis API endpoint"""
    try:
        data = request.get_json()
        log_file = data.get('log_file')
        log_format = data.get('format', 'auto')
        graph_file = data.get('graph_file')
        
        if not log_file:
            return jsonify({'error': 'Please provide log file path'}), 400
            
        if not os.path.exists(log_file):
            return jsonify({'error': f'Log file does not exist: {log_file}'}), 400
            
        # Create log analyzer
        analyzer = ExecutionLogAnalyzer()
        
        # Load graph data (if provided)
        if graph_file and os.path.exists(graph_file):
            with open(graph_file, 'r', encoding='utf-8') as f:
                graph_data = json.load(f)
            analyzer.load_graph(graph_data)
            
        # Execute analysis
        analysis_result = analyzer.analyze_log_file(log_file, format_hint=log_format)
        
        # Save analysis results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(app.config['OUTPUT_DIR'], f'log_analysis_{timestamp}.json')
        
        # Convert results to serializable format
        result_dict = {
            'analysis_info': analysis_result.analysis_info,
            'log_summary': analysis_result.log_summary,
            'execution_paths': [path.__dict__ for path in analysis_result.execution_paths],
            'anomalies': analysis_result.anomalies,
            'recommendations': analysis_result.recommendations
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)
            
        return jsonify({
            'success': True,
            'result': result_dict,
            'output_file': output_file
        })
        
    except Exception as e:
        logger.error(f"Log analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/results')
def api_list_results():
    """List all analysis result files"""
    try:
        output_dir = Path(app.config['OUTPUT_DIR'])
        results = []
        
        for file_path in output_dir.glob('*.json'):
            stat = file_path.stat()
            results.append({
                'filename': file_path.name,
                'path': str(file_path),
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'type': file_path.stem.split('_')[0] if '_' in file_path.stem else 'unknown'
            })
            
        # Sort by modification time in descending order
        results.sort(key=lambda x: x['modified'], reverse=True)
        
        return jsonify({'results': results})
        
    except Exception as e:
        logger.error(f"Get results list error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/result/<filename>')
def api_get_result(filename):
    """Get specific analysis result"""
    try:
        file_path = os.path.join(app.config['OUTPUT_DIR'], filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File does not exist'}), 404
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        return jsonify(data)
        
    except Exception as e:
        logger.error(f"Get result error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/examples')
def api_list_examples():
    """List example projects"""
    examples = get_examples_config()
    
    # Check if paths exist and add status information
    for example in examples:
        example['exists'] = Path(example['resolved_path']).exists()
        example['resolved_path_display'] = example['resolved_path']
    
    return jsonify({'examples': examples})


@app.route('/api/demo-data')
def api_demo_data():
    """Generate demo data"""
    demo_scan_data = {
        "scan_info": {
            "target": "demo_project",
            "scan_type": "directory",
            "timestamp": datetime.now().isoformat(),
            "scanner_version": "2.0"
        },
        "scan_summary": {
            "total_agents": 3,
            "total_tools": 2,
            "total_crews": 1,
            "total_tasks": 4,
            "total_files": 8,
            "python_files": 5
        },
        "agents": [
            {
                "name": "email_classifier",
                "type": "instance",
                "file": "agents.py",
                "line": 15,
                "arguments": {
                    "role": "Email Classifier",
                    "goal": "Classify emails into priority levels"
                }
            },
            {
                "name": "email_responder", 
                "type": "instance",
                "file": "agents.py",
                "line": 28,
                "arguments": {
                    "role": "Email Responder",
                    "goal": "Generate appropriate email responses"
                }
            },
            {
                "name": "task_manager",
                "type": "instance", 
                "file": "agents.py",
                "line": 41,
                "arguments": {
                    "role": "Task Manager",
                    "goal": "Coordinate email processing workflow"
                }
            }
        ],
        "tools": [
            {
                "name": "EmailTool",
                "type": "class",
                "file": "tools.py", 
                "line": 10,
                "methods": ["send_email", "read_email"]
            },
            {
                "name": "ClassificationTool",
                "type": "class",
                "file": "tools.py",
                "line": 45,
                "methods": ["classify_text", "extract_entities"]
            }
        ],
        "crews": [
            {
                "name": "email_crew",
                "type": "instance",
                "file": "main.py",
                "line": 20,
                "agents": ["email_classifier", "email_responder", "task_manager"]
            }
        ],
        "tasks": [
            {
                "name": "classify_task",
                "type": "instance", 
                "file": "tasks.py",
                "line": 8,
                "description": "Classify incoming emails"
            },
            {
                "name": "respond_task",
                "type": "instance",
                "file": "tasks.py", 
                "line": 18,
                "description": "Generate email responses"
            },
            {
                "name": "monitor_task",
                "type": "instance",
                "file": "tasks.py",
                "line": 28,
                "description": "Monitor email processing"
            },
            {
                "name": "report_task",
                "type": "instance",
                "file": "tasks.py",
                "line": 38,
                "description": "Generate processing reports"
            }
        ]
    }
    
    return jsonify({
        'success': True,
        'result': demo_scan_data
    })


@app.route('/api/demo-graph')
def api_demo_graph():
    """Generate demo graph data"""
    demo_graph_data = {
        "graph_summary": {
            "total_nodes": 10,
            "total_edges": 12,
            "components": 1,
            "density": 0.267
        },
        "nodes": [
            {"id": "email_classifier", "type": "agent", "properties": {"name": "Email Classifier", "importance": 0.8}},
            {"id": "email_responder", "type": "agent", "properties": {"name": "Email Responder", "importance": 0.7}},
            {"id": "task_manager", "type": "agent", "properties": {"name": "Task Manager", "importance": 0.9}},
            {"id": "EmailTool", "type": "tool", "properties": {"name": "Email Tool", "importance": 0.6}},
            {"id": "ClassificationTool", "type": "tool", "properties": {"name": "Classification Tool", "importance": 0.5}},
            {"id": "email_crew", "type": "crew", "properties": {"name": "Email Crew", "importance": 1.0}},
            {"id": "classify_task", "type": "task", "properties": {"name": "Classify Task", "importance": 0.6}},
            {"id": "respond_task", "type": "task", "properties": {"name": "Respond Task", "importance": 0.6}},
            {"id": "monitor_task", "type": "task", "properties": {"name": "Monitor Task", "importance": 0.4}},
            {"id": "report_task", "type": "task", "properties": {"name": "Report Task", "importance": 0.3}}
        ],
        "edges": [
            {"source": "email_crew", "target": "email_classifier", "relationship": "contains", "weight": 1.0},
            {"source": "email_crew", "target": "email_responder", "relationship": "contains", "weight": 1.0},
            {"source": "email_crew", "target": "task_manager", "relationship": "contains", "weight": 1.0},
            {"source": "email_classifier", "target": "ClassificationTool", "relationship": "uses", "weight": 0.8},
            {"source": "email_responder", "target": "EmailTool", "relationship": "uses", "weight": 0.9},
            {"source": "task_manager", "target": "EmailTool", "relationship": "uses", "weight": 0.7},
            {"source": "classify_task", "target": "email_classifier", "relationship": "assigned_to", "weight": 0.9},
            {"source": "respond_task", "target": "email_responder", "relationship": "assigned_to", "weight": 0.9},
            {"source": "monitor_task", "target": "task_manager", "relationship": "assigned_to", "weight": 0.8},
            {"source": "report_task", "target": "task_manager", "relationship": "assigned_to", "weight": 0.7},
            {"source": "email_classifier", "target": "email_responder", "relationship": "data_flow", "weight": 0.6},
            {"source": "task_manager", "target": "email_classifier", "relationship": "coordinates", "weight": 0.5}
        ],
        "metadata": {
            "total_nodes": 10,
            "total_edges": 12,
            "components": 1,
            "density": 0.267
        }
    }
    
    return jsonify({
        'success': True,
        'result': demo_graph_data
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
