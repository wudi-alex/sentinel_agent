# Inspector Agent 使用指南

## 🎉 成功构建完成！

Inspector Agent 已经在 `watchdog` 文件夹下成功构建并测试完成。这是一个基于CrewAI架构的智能代理系统，专门用于扫描和分析其他agent系统的结构。

## 📁 项目结构

```
watchdog/
├── scanner.py              # 核心扫描引擎
├── tools.py               # CrewAI工具定义
├── inspector.py           # 主要的Inspector Agent类
├── demo.py               # 简单演示脚本
├── test.py               # 功能测试脚本
├── example.py            # 详细使用示例
├── requirements.txt      # 依赖包列表
├── README.md            # 项目文档
└── *.json               # 扫描结果文件
```

## 🚀 快速开始

### 1. 基础使用

```bash
# 进入项目目录
cd /Users/xuhe/Documents/agent_experiments/watchdog

# 使用核心扫描器扫描目录
python -c "
from scanner import AgentSystemScanner
scanner = AgentSystemScanner()
result = scanner.scan_directory('../crewai_gmail')
print(f'发现 {result[\"scan_summary\"][\"total_agents\"]} 个agents')
"

# 使用命令行工具
python inspector.py ../crewai_gmail --output crewai_analysis.json
```

### 2. 编程接口

```python
from inspector import InspectorAgent

# 创建inspector实例
inspector = InspectorAgent()

# 扫描目录
result = inspector.scan_directory("../crewai_gmail")

# 扫描单个文件
result = inspector.scan_file("../crewai_gmail/tools.py")
```

### 3. 直接使用工具

```python
from tools import DirectoryScanTool, ReportAnalysisTool

# 使用目录扫描工具
scanner = DirectoryScanTool()
result = scanner._run("project_path", "output.json")

# 使用报告分析工具
analyzer = ReportAnalysisTool()
analysis = analyzer._run("output.json")
```

## 🔍 已验证的扫描能力

Inspector Agent 已经成功测试并验证了以下扫描能力：

### ✅ CrewAI 项目扫描
- ✅ 识别 6 个 Agents
- ✅ 识别 1 个 Tool (EmailSenderTool)
- ✅ 识别 2 个 Crews  
- ✅ 识别 5 个 Tasks
- ✅ 分析项目结构和配置

### ✅ AutoGen 项目扫描
- ✅ 识别 AutoGen agents
- ✅ 分析 agent 配置
- ✅ 扫描项目文件结构

### ✅ 自我扫描能力
- ✅ 识别自身的 10 个 Agents
- ✅ 识别自身的 8 个 Tools
- ✅ 完整的递归分析能力

## 📊 扫描结果示例

扫描 CrewAI Gmail 项目的实际结果：

```json
{
  "scan_summary": {
    "total_agents": 6,
    "total_tools": 1,
    "total_crews": 2,
    "total_tasks": 5,
    "total_files": 6
  },
  "agents": [
    {
      "name": "email_classifier",
      "type": "instance",
      "arguments": {
        "role": "Email Classifier",
        "goal": "Classify emails into priority levels"
      }
    }
  ]
}
```

## 🛠️ 核心功能

1. **智能识别**: 自动识别 agents、tools、crews、tasks
2. **多框架支持**: 支持 CrewAI、AutoGen 等框架
3. **AST 分析**: 使用 Python AST 进行精确代码分析
4. **正则回退**: 当 AST 失败时使用正则表达式
5. **详细报告**: 生成完整的 JSON 格式分析报告
6. **架构分析**: 提供专业的系统架构洞察

## 📈 性能特点

- **快速扫描**: 支持大型项目的快速扫描
- **准确识别**: 高精度的组件识别
- **容错能力**: 即使遇到语法错误也能继续分析
- **灵活配置**: 支持自定义扫描模式

## 💡 使用建议

1. **日常使用**: 用于理解和分析现有的 agent 项目
2. **项目迁移**: 帮助理解项目结构，便于迁移和重构
3. **学习研究**: 分析不同框架的 agent 系统设计
4. **质量评估**: 评估 agent 系统的架构质量

## 🔄 扩展开发

Inspector Agent 设计为可扩展的架构：

1. **添加新框架支持**: 在 `scanner.py` 中添加新的分析模式
2. **自定义工具**: 继承 `BaseTool` 创建新的分析工具
3. **增强分析**: 扩展 AST 分析功能
4. **报告格式**: 支持新的输出格式

## 📞 使用支持

如果在使用过程中遇到问题：

1. 查看生成的 JSON 文件获取详细信息
2. 检查目标路径是否正确
3. 确保有足够的文件读取权限
4. 查看 README.md 获取更多信息

## 🎯 总结

Inspector Agent 已经成功构建并验证了核心功能：

- ✅ **扫描引擎**: 正常工作，能够识别多种 agent 组件
- ✅ **CrewAI 集成**: 完美集成 CrewAI 架构
- ✅ **多项目支持**: 成功扫描 CrewAI 和 AutoGen 项目
- ✅ **详细分析**: 生成完整的结构分析报告
- ✅ **自我认知**: 具备完整的自我扫描能力

Inspector Agent 现在可以正式投入使用，帮助你理解和分析各种 agent 系统的结构！
