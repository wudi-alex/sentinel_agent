# Inspector Agent

一个基于CrewAI架构的智能代理系统，专门用于扫描和分析其他agent系统的结构。Inspector Agent能够自动识别项目中的agents、tools、crews和tasks，并生成详细的架构分析报告。

## 功能特性

- 🔍 **智能扫描**: 自动识别和分析agent系统结构
- 🤖 **多框架支持**: 支持CrewAI、AutoGen等主流agent框架
- 📊 **详细报告**: 生成包含agents、tools、crews、tasks的完整JSON报告
- 🏗️ **架构分析**: 提供专业的系统架构洞察和建议
- 🛠️ **灵活工具**: 可单独使用扫描工具或完整的agent系统

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 命令行使用

```bash
# 扫描目录
python inspector.py /path/to/agent/project

# 扫描单个文件
python inspector.py /path/to/agent_file.py

# 指定输出文件
python inspector.py /path/to/project --output my_analysis.json

# 强制指定类型
python inspector.py /path/to/target --type dir
```

### 2. 编程使用

```python
from inspector import InspectorAgent

# 创建inspector实例
inspector = InspectorAgent()

# 扫描目录
result = inspector.scan_directory("../crewai_gmail")

# 扫描文件
result = inspector.scan_file("../autogen_project/main.py")
```

### 3. 直接使用工具

```python
from tools import DirectoryScanTool, FileScanTool, ReportAnalysisTool

# 目录扫描
scanner = DirectoryScanTool()
result = scanner._run("project_path", "output.json")

# 报告分析
analyzer = ReportAnalysisTool()
analysis = analyzer._run("output.json")
```

## 示例演示

运行示例脚本查看各种使用方式：

```bash
python example.py
```

## 项目结构

```
watchdog/
├── inspector.py      # 主要的Inspector Agent类
├── scanner.py        # 核心扫描引擎
├── tools.py          # CrewAI工具定义
├── example.py        # 使用示例
├── requirements.txt  # 依赖包
└── README.md        # 本文档
```

## 扫描能力

Inspector Agent能够识别以下组件：

### Agents
- CrewAI Agent实例
- 自定义Agent类
- AutoGen Agent组件
- Agent配置参数

### Tools
- CrewAI BaseTool子类
- 工具函数定义
- 工具配置参数

### Crews
- CrewAI Crew实例
- 团队配置
- Agent组合关系

### Tasks
- Task定义和配置
- 任务依赖关系
- 任务流程

### 文件结构
- Python文件组织
- 项目目录结构
- 文件大小和类型

## 输出格式

扫描结果以JSON格式保存，包含：

```json
{
  "scan_summary": {
    "total_agents": 3,
    "total_tools": 2,
    "total_crews": 1,
    "total_tasks": 4,
    "total_files": 8
  },
  "agents": [...],
  "tools": [...],
  "crews": [...],
  "tasks": [...],
  "file_structure": {...},
  "analysis_metadata": {...}
}
```

## 高级功能

### 1. AST解析
使用Python AST模块进行精确的代码结构分析

### 2. 正则表达式回退
当AST解析失败时，使用正则表达式进行模式匹配

### 3. 智能分析
基于CrewAI的智能代理提供架构分析和改进建议

### 4. 多格式支持
支持扫描目录、单文件、以及混合项目结构

## 注意事项

1. **API Key**: 如果需要使用完整的AI分析功能，请设置OPENAI_API_KEY环境变量
2. **权限**: 确保有足够权限读取目标目录和文件
3. **大项目**: 对于大型项目，扫描可能需要一些时间

## 扩展开发

### 添加新的扫描模式

在`scanner.py`中的`AgentSystemScanner`类中添加新的分析方法：

```python
def _analyze_custom_pattern(self, content: str, file_path: Path):
    # 自定义分析逻辑
    pass
```

### 创建新工具

继承`BaseTool`创建新的分析工具：

```python
class CustomAnalysisTool(BaseTool):
    name: str = "custom_analyzer"
    description: str = "自定义分析工具"
    # 实现_run方法
```

## 贡献

欢迎提交Issues和Pull Requests来改进Inspector Agent！

## 许可证

MIT License
