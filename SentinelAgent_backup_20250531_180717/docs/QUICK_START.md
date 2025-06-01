# SentinelAgent 快速开始指南

## 🚀 快速安装

### 1. 克隆项目
```bash
git clone <repository-url>
cd SentinelAgent
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 启动Web界面
```bash
python scripts/start_web_ui.py
```

或使用主程序：
```bash
python sentinel_agent.py --web
```

访问: **http://localhost:5002**

## 🔧 命令行使用

### 系统扫描
```bash
# 扫描目录
python sentinel_agent.py scan --path /path/to/agent/project

# 扫描单个文件
python sentinel_agent.py scan --path /path/to/agent/file.py --type file
```

### 构建执行图
```bash
# 从扫描结果构建图
python sentinel_agent.py build-graph --input scan_results.json

# 直接从项目构建图
python sentinel_agent.py build-graph --path /path/to/project
```

### 路径分析
```bash
# 分析执行路径
python sentinel_agent.py analyze-paths --graph graph_results.json
```

### 日志分析
```bash
# 分析运行时日志
python sentinel_agent.py analyze-logs --logs /path/to/logfile.txt
python sentinel_agent.py analyze-logs --logs /path/to/logfile.txt --graph graph_results.json
```

## 🌐 Web界面功能

### 1. 系统扫描器
- 📁 选择项目目录或文件
- 🔍 自动识别Agent、Tool、Task、Crew
- 📊 生成扫描报告

### 2. 图构建器
- 🕸️ 基于扫描结果构建执行图
- 🎨 交互式可视化界面
- 📈 图结构统计分析

### 3. 路径分析器
- 🛤️ 发现所有可能的执行路径
- ⚠️ 识别潜在问题路径
- 🔧 提供优化建议

### 4. 日志分析器
- 📋 分析运行时日志
- 🚨 检测错误和异常
- 📈 性能监控分析

## 💡 使用技巧

### 演示模式
Web界面提供内置演示数据，无需真实项目即可体验所有功能：
- 点击"加载演示数据"按钮
- 体验完整的分析流程

### 批量处理
```bash
# 批量扫描多个项目
for project in /path/to/projects/*; do
    python sentinel_agent.py scan --path "$project" --output "scan_$(basename $project).json"
done
```

### 结果导出
所有分析结果自动保存在 `data/output/` 目录下，支持：
- JSON格式结果
- 图像格式导出
- CSV数据导出

## 🔧 配置

编辑 `config/sentinel_agent.conf` 自定义：
- 服务器端口和主机
- 文件路径配置
- 分析参数调整
- 日志级别设置

## 📚 更多文档

- [用户指南](USER_GUIDE.md)
- [API参考](API_REFERENCE.md)
- [配置指南](CONFIGURATION.md)
- [开发指南](DEVELOPMENT.md)
