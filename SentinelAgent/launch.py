#!/usr/bin/env python3
"""
SentinelAgent Launch Script
Convenient launcher for all SentinelAgent functionalities
"""

import sys
import argparse
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description="SentinelAgent - Advanced Agent System Analysis & Monitoring Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s web                 # Start web UI
  %(prog)s scan /path/to/dir   # Scan a directory
  %(prog)s demo               # Run demo
  %(prog)s --help             # Show this help
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Web UI command
    web_parser = subparsers.add_parser('web', help='Start web UI')
    web_parser.add_argument('--port', type=int, default=5002, help='Port to run on (default: 5002)')
    web_parser.add_argument('--host', default='localhost', help='Host to bind to (default: localhost)')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan directory or file')
    scan_parser.add_argument('path', help='Path to scan')
    scan_parser.add_argument('--output', '-o', help='Output file for results')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demonstration')
    demo_parser.add_argument('--type', choices=['complete', 'scan', 'graph', 'paths', 'logs'], 
                           default='complete', help='Type of demo to run')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'web':
            from sentinelagent.cli.start_web_ui import main as web_main
            return web_main()
            
        elif args.command == 'scan':
            from sentinelagent.core.scanner import scan_directory, scan_file
            import json
            
            path = Path(args.path)
            if not path.exists():
                print(f"❌ Path does not exist: {path}")
                return 1
                
            print(f"🔍 Scanning: {path}")
            
            if path.is_file():
                result = scan_file(str(path))
            else:
                result = scan_directory(str(path))
                
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"💾 Results saved to: {args.output}")
            else:
                print("📊 Scan Results:")
                print(json.dumps(result, indent=2))
                
        elif args.command == 'demo':
            demo_file = f"examples/demos/{args.type}_demo.py"
            if args.type == 'complete':
                demo_file = "examples/demos/complete_demo.py"
            
            demo_path = project_root / demo_file
            if not demo_path.exists():
                print(f"❌ Demo file not found: {demo_file}")
                return 1
                
            print(f"🚀 Running {args.type} demo...")
            import subprocess
            result = subprocess.run([sys.executable, str(demo_path)], cwd=str(project_root))
            return result.returncode
            
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
