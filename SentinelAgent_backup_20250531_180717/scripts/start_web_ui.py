#!/usr/bin/env python3
"""
SentinelAgent Web UI Launch Script
Start the web interface service
"""

import sys
import os
import webbrowser
import time
from pathlib import Path

# Add project root directory to Python path
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_path))

def main():
    """Main function"""
    try:
        # Check dependencies
        try:
            import flask
            import flask_cors
        except ImportError:
            print("❌ Missing dependencies, installing...")
            os.system(f"{sys.executable} -m pip install -r {project_root}/requirements.txt")
            print("✅ Dependencies installation completed")
        
        # Start Flask application
        from src.web.app import app
        
        print("🚀 Starting SentinelAgent Web UI...")
        print("📍 Access URL: http://localhost:5002")
        print("🤖 AI Agent System Analysis & Monitoring Platform")
        print("⏹️  Press Ctrl+C to stop service")
        print("-" * 50)
        
        # Auto open browser
        def open_browser():
            time.sleep(1.5)
            webbrowser.open('http://localhost:5002')
        
        import threading
        threading.Thread(target=open_browser, daemon=True).start()
        
        # Start application
        app.run(debug=False, host='0.0.0.0', port=5002)
        
    except KeyboardInterrupt:
        print("\n👋 Service stopped")
    except Exception as e:
        print(f"❌ Start failed: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
