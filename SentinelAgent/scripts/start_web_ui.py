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
    """主函数"""
    try:
        # 检查依赖
        try:
            import flask
            import flask_cors
        except ImportError:
            print("❌ 缺少依赖包，正在安装...")
            os.system(f"{sys.executable} -m pip install -r {project_root}/requirements.txt")
            print("✅ 依赖安装完成")
        
        # 启动Flask应用
        from src.web.app import app
        
        print("🚀 启动 SentinelAgent Web UI...")
        print("📍 访问地址: http://localhost:5002")
        print("🤖 AI Agent系统分析与监控平台")
        print("⏹️  按 Ctrl+C 停止服务")
        print("-" * 50)
        
        # 自动打开浏览器
        def open_browser():
            time.sleep(1.5)
            webbrowser.open('http://localhost:5002')
        
        import threading
        threading.Thread(target=open_browser, daemon=True).start()
        
        # 启动应用
        app.run(debug=False, host='0.0.0.0', port=5002)
        
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
