#!/usr/bin/env python3
"""
CrewAI CSV Log to JSON Converter
===============================

This script converts CrewAI CSV log files to structured JSON format for better readability and analysis.
The CSV format contains complex nested data that is hard to read, this tool extracts and structures it.

Features:
- Parse complex agent information from CSV
- Extract email content and classifications
- Structure tool calls and execution flows
- Generate readable JSON with proper formatting
- Support batch conversion of multiple files

Usage:
    python csv_to_json_converter.py input.csv output.json
    python csv_to_json_converter.py --batch /path/to/logs/
"""

import csv
import json
import re
import base64
import argparse
import html
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class CrewAILogConverter:
    """Converter for CrewAI CSV logs to structured JSON"""
    
    def __init__(self):
        self.agent_role_patterns = {
            'Email Classifier': 'classifier',
            'Email Responder': 'responder',
            'Email Sender': 'sender'
        }
        
    def decode_example_id(self, example_id: str) -> str:
        """Decode base64 example ID if possible"""
        try:
            decoded = base64.b64decode(example_id).decode('utf-8')
            return decoded
        except:
            return example_id
    
    def extract_agent_info(self, agent_string: str) -> Dict[str, Any]:
        """Extract agent information from the complex agent string"""
        agent_info = {
            'id': None,
            'role': None,
            'goal': None,
            'backstory': None,
            'tools': [],
            'config': {}
        }
        
        # Extract UUID
        uuid_match = re.search(r"id=UUID\('([^']+)'\)", agent_string)
        if uuid_match:
            agent_info['id'] = uuid_match.group(1)
        
        # Extract role
        role_match = re.search(r"role='([^']+)'", agent_string)
        if role_match:
            agent_info['role'] = role_match.group(1)
        
        # Extract goal
        goal_match = re.search(r"goal='([^']+)'", agent_string)
        if goal_match:
            agent_info['goal'] = goal_match.group(1)
        
        # Extract backstory
        backstory_match = re.search(r"backstory='([^']+)'", agent_string)
        if backstory_match:
            agent_info['backstory'] = backstory_match.group(1)
        
        # Extract configuration values
        config_patterns = {
            'cache': r'cache=(\w+)',
            'verbose': r'verbose=(\w+)',
            'max_iter': r'max_iter=(\d+)',
            'allow_delegation': r'allow_delegation=(\w+)',
            'max_retry_limit': r'max_retry_limit=(\d+)',
            'code_execution_mode': r"code_execution_mode='([^']+)'",
            'respect_context_window': r'respect_context_window=(\w+)'
        }
        
        for key, pattern in config_patterns.items():
            match = re.search(pattern, agent_string)
            if match:
                value = match.group(1)
                if value in ['True', 'False']:
                    agent_info['config'][key] = value == 'True'
                elif value.isdigit():
                    agent_info['config'][key] = int(value)
                else:
                    agent_info['config'][key] = value
        
        return agent_info
    
    def extract_email_content(self, description: str) -> Dict[str, Any]:
        """Extract email information from description text"""
        email_info = {
            'from': None,
            'subject': None,
            'body': None,
            'task_description': None,
            'classification_rules': []
        }
        
        # Extract sender
        from_match = re.search(r'From:\s*([^\n]+)', description)
        if from_match:
            email_info['from'] = from_match.group(1).strip()
        
        # Extract subject
        subject_match = re.search(r'Subject:\s*([^\n]+)', description)
        if subject_match:
            email_info['subject'] = subject_match.group(1).strip()
        
        # Extract email body (content after "Subject:" line)
        subject_index = description.find('Subject:')
        if subject_index != -1:
            # Find the end of subject line
            subject_end = description.find('\n', subject_index)
            if subject_end != -1:
                body_start = subject_end + 1
                # Find next empty line or end of content
                body_section = description[body_start:].strip()
                
                # Remove HTML entities
                body_section = html.unescape(body_section)
                
                if body_section:
                    email_info['body'] = body_section
        
        # Extract classification rules
        rules_section = description.split('categories:')
        if len(rules_section) > 1:
            rules_text = rules_section[1].split('Email content:')[0]
            rules = re.findall(r'-\s*([^:]+):\s*([^\n]+)', rules_text)
            email_info['classification_rules'] = [
                {'category': rule[0].strip(), 'description': rule[1].strip()}
                for rule in rules
            ]
        
        # Extract task description (before categories)
        task_desc_match = re.search(r'You are ([^.]+\.)', description)
        if task_desc_match:
            email_info['task_description'] = task_desc_match.group(1)
        
        return email_info
    
    def extract_tool_info(self, tools_string: str) -> List[Dict[str, Any]]:
        """Extract tool information from tools string"""
        tools = []
        
        if not tools_string or tools_string == '[]':
            return tools
        
        # Parse tool strings
        tool_matches = re.findall(r"name='([^']+)'[^}]+description=[\"']([^\"']+)[\"']", tools_string)
        
        for tool_match in tool_matches:
            tool_name = tool_match[0]
            tool_desc = tool_match[1]
            
            # Extract arguments if available
            args_pattern = rf"name='{tool_name}'[^{{}}]*Tool Arguments:\s*(\{{[^}}]+\}})"
            args_match = re.search(args_pattern, tools_string)
            
            tool_info = {
                'name': tool_name,
                'description': tool_desc,
                'arguments': {}
            }
            
            if args_match:
                try:
                    # Parse arguments (simplified)
                    args_text = args_match.group(1)
                    # Extract argument names and types
                    arg_matches = re.findall(r"'([^']+)':\s*\{[^}]*'type':\s*'([^']+)'", args_text)
                    for arg_name, arg_type in arg_matches:
                        tool_info['arguments'][arg_name] = {'type': arg_type}
                except:
                    pass
            
            tools.append(tool_info)
        
        return tools
    
    def parse_csv_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """Parse a single CSV row into structured JSON"""
        parsed_entry = {
            'example_id': self.decode_example_id(row.get('example_id', '')),
            'timestamp': datetime.now().isoformat(),
            'entry_type': 'unknown',
            'agent': {},
            'task': {},
            'tools': [],
            'input': {},
            'output': {},
            'metadata': {}
        }
        
        # Determine entry type based on metadata
        span_kind = row.get('metadata_span_kind', '')
        if span_kind == 'AGENT':
            parsed_entry['entry_type'] = 'agent_execution'
        elif span_kind == 'TOOL':
            parsed_entry['entry_type'] = 'tool_execution'
        else:
            parsed_entry['entry_type'] = 'other'
        
        # Parse input information
        input_data = row.get('input_input', '')
        if input_data:
            try:
                # Try to parse as JSON
                import ast
                input_dict = ast.literal_eval(input_data)
                
                # Extract agent information
                if 'agent' in input_dict:
                    agent_string = input_dict['agent']
                    parsed_entry['agent'] = self.extract_agent_info(agent_string)
                
                # Extract context
                if 'context' in input_dict:
                    parsed_entry['input']['context'] = input_dict['context']
                
                # Extract tools
                if 'tools' in input_dict:
                    tools_string = str(input_dict['tools'])
                    parsed_entry['tools'] = self.extract_tool_info(tools_string)
                
            except Exception as e:
                # If parsing fails, store as raw text
                parsed_entry['input']['raw'] = input_data
        
        # Parse task description
        task_description = row.get('output_description', '')
        if task_description:
            if parsed_entry['entry_type'] == 'agent_execution':
                parsed_entry['task'] = self.extract_email_content(task_description)
            else:
                parsed_entry['task']['description'] = task_description
        
        # Parse output information
        output_fields = {
            'name': 'output_name',
            'expected_output': 'output_expected_output',
            'summary': 'output_summary',
            'raw': 'output_raw',
            'final_output': 'output_output'
        }
        
        for key, csv_key in output_fields.items():
            value = row.get(csv_key, '')
            if value:
                parsed_entry['output'][key] = value
        
        # Parse agent name
        agent_name = row.get('output_agent', '')
        if agent_name and not parsed_entry['agent'].get('role'):
            parsed_entry['agent']['role'] = agent_name
            parsed_entry['agent']['type'] = self.agent_role_patterns.get(agent_name, 'unknown')
        
        # Parse metadata
        parsed_entry['metadata'] = {
            'span_kind': row.get('metadata_span_kind', ''),
            'output_format': row.get('output_output_format', ''),
            'annotations': row.get('metadata_annotations', '')
        }
        
        return parsed_entry
    
    def convert_csv_to_json(self, csv_file_path: str, output_file_path: str = None) -> Dict[str, Any]:
        """Convert CSV file to structured JSON"""
        csv_path = Path(csv_file_path)
        
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
        
        # Generate output path if not provided
        if output_file_path is None:
            output_file_path = csv_path.with_suffix('.json')
        
        converted_data = {
            'metadata': {
                'source_file': str(csv_path),
                'conversion_time': datetime.now().isoformat(),
                'converter_version': '1.0',
                'total_entries': 0
            },
            'execution_log': []
        }
        
        # Read and convert CSV
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                try:
                    parsed_entry = self.parse_csv_row(row)
                    converted_data['execution_log'].append(parsed_entry)
                except Exception as e:
                    print(f"Warning: Failed to parse row {len(converted_data['execution_log']) + 1}: {e}")
                    # Add raw row for debugging
                    converted_data['execution_log'].append({
                        'error': str(e),
                        'raw_row': dict(row)
                    })
        
        converted_data['metadata']['total_entries'] = len(converted_data['execution_log'])
        
        # Save to JSON file
        with open(output_file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(converted_data, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"✅ Conversion complete!")
        print(f"   📁 Input: {csv_file_path}")
        print(f"   📄 Output: {output_file_path}")
        print(f"   📊 Entries: {converted_data['metadata']['total_entries']}")
        
        return converted_data
    
    def batch_convert(self, directory_path: str, output_dir: str = None):
        """Convert all CSV files in a directory"""
        dir_path = Path(directory_path)
        
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        # Set output directory
        if output_dir is None:
            output_dir = dir_path / 'json_converted'
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(exist_ok=True)
        
        # Find all CSV files
        csv_files = list(dir_path.glob('*.csv'))
        
        if not csv_files:
            print(f"❌ No CSV files found in {directory_path}")
            return
        
        print(f"🔄 Found {len(csv_files)} CSV files to convert...")
        
        converted_files = []
        for csv_file in csv_files:
            try:
                output_file = output_dir / f"{csv_file.stem}.json"
                self.convert_csv_to_json(str(csv_file), str(output_file))
                converted_files.append(output_file)
            except Exception as e:
                print(f"❌ Failed to convert {csv_file}: {e}")
        
        print(f"\n🎉 Batch conversion complete!")
        print(f"   📁 Converted: {len(converted_files)}/{len(csv_files)} files")
        print(f"   📂 Output directory: {output_dir}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Convert CrewAI CSV logs to structured JSON format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python csv_to_json_converter.py input.csv
  python csv_to_json_converter.py input.csv output.json
  python csv_to_json_converter.py --batch /path/to/logs/
  python csv_to_json_converter.py --batch /path/to/logs/ --output /path/to/output/
        """
    )
    
    parser.add_argument('input', help='Input CSV file or directory (for batch mode)')
    parser.add_argument('output', nargs='?', help='Output JSON file (optional)')
    parser.add_argument('--batch', action='store_true', help='Convert all CSV files in directory')
    parser.add_argument('--output-dir', help='Output directory for batch mode')
    
    args = parser.parse_args()
    
    converter = CrewAILogConverter()
    
    try:
        if args.batch:
            converter.batch_convert(args.input, args.output_dir)
        else:
            converter.convert_csv_to_json(args.input, args.output)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
