# Watchdog - Agent System Analysis Tool

🔍 **一个专业的Agent系统分析工具，用于扫描、分析和监控基于Agent的系统架构。**

## ✨ 主要功能

- 🔍 **系统扫描**: 自动扫描Agent项目，识别组件结构
- 🔗 **关系图构建**: 构建Agent和Tool之间的关系图
- 🛣️ **路径分析**: 分析执行路径，检测异常模式
- 📊 **风险评估**: 评估系统安全风险和性能问题
- 📈 **可视化支持**: 生成JSON格式的分析结果

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 基本使用
```bash
# 完整分析（推荐）
python watchdog.py <目标路径> --all

# 只进行扫描
python watchdog.py <目标路径>

# 扫描 + 图构建
python watchdog.py <目标路径> --graph output_graph.json

# 扫描 + 路径分析
python watchdog.py <目标路径> --paths output_paths.json

# 分析已有图文件
python watchdog.py --analyze-graph existing_graph.json
```

### 编程接口
```python
from src.inspector import InspectorAgent

# 创建分析器
inspector = InspectorAgent()

# 完整分析
result = inspector.comprehensive_analysis(
    target_path="./my_agent_project",
    scan_output="scan.json",
    graph_output="graph.json", 
    path_output="paths.json"
)

# 查看分析结果
print(f"发现 {result['graph_data']['graph_summary']['total_nodes']} 个组件")
print(f"检测到 {len(result['path_analysis']['suspicious_patterns'])} 个可疑模式")
```

## 📁 项目结构

```
watchdog/
├── README.md                 # 项目说明
├── requirements.txt          # 依赖列表
├── watchdog.py              # 主入口文件
├── src/                     # 核心源代码
│   ├── __init__.py          # 包初始化
│   ├── scanner.py           # 系统扫描器
│   ├── graph_builder.py     # 关系图构建器
│   ├── path_analyzer.py     # 路径分析器
│   ├── inspector.py         # 主要分析接口
│   ├── cli.py               # 命令行接口
│   └── tools.py             # CrewAI工具
├── examples/                # 示例和演示
│   ├── demo.py              # 基础演示
│   ├── graph_demo.py        # 图构建演示
│   └── path_demo.py         # 路径分析演示
├── tests/                   # 测试文件
│   └── test.py              # 功能测试
├── docs/                    # 文档
│   ├── USAGE.md             # 使用指南
│   ├── README_ENHANCED.md   # 增强功能说明
│   └── README_paths.md      # 路径分析文档
├── output/                  # 分析结果输出
└── archives/                # 历史文档
```

## 🔧 核心模块

### 📊 Scanner (扫描器)
- 自动检测Agent、Tool、Crew、Task组件
- 支持多种文件格式和代码结构
- 提取组件元数据和关系信息

### 🔗 Graph Builder (图构建器)
- 基于扫描结果构建关系图
- 支持多种关系类型：文件位置、名称相似、显式使用等
- 优化的图结构，突出核心组件关系

### 🛣️ Path Analyzer (路径分析器)
- 分析执行路径和组件交互模式
- 内置7种异常检测规则
- 风险评分和安全建议

### 🕵️ Inspector (检查器)
- 统一的高级分析接口
- 支持完整的分析流程
- 集成CrewAI Agent能力

## 📈 分析输出

### 扫描结果 (JSON)
```json
{
  "scan_info": {...},
  "agents": [...],
  "tools": [...],
  "crews": [...],
  "tasks": [...]
}
```

### 关系图 (JSON)
```json
{
  "graph_summary": {...},
  "nodes": [...],
  "edges": [...],
  "graph_metadata": {...}
}
```

### 路径分析 (JSON)
```json
{
  "overall_assessment": {...},
  "path_analysis": {...},
  "suspicious_patterns": [...],
  "recommendations": [...]
}
```

## 🎯 使用场景

- **🔒 安全审计**: 检测Agent系统中的安全风险
- **⚡ 性能优化**: 识别系统瓶颈和低效模式
- **🏗️ 架构分析**: 理解和优化系统设计
- **📋 合规检查**: 验证系统符合最佳实践

## 📚 文档

- [使用指南](docs/USAGE.md) - 详细的使用说明
- [路径分析文档](docs/README_paths.md) - 路径分析功能详解
- [功能增强说明](docs/README_ENHANCED.md) - 高级功能介绍

## 🎮 示例演示

```bash
# 运行基础演示
python examples/demo.py

# 图构建演示
python examples/graph_demo.py

# 路径分析演示（交互式）
python examples/path_demo.py
```

## 🧪 测试

```bash
# 运行功能测试
python tests/test.py
```

## 🔧 开发

### 添加自定义分析规则
```python
from src.path_analyzer import PathAnalyzer

def custom_rule(graph_data):
    # 自定义检测逻辑
    return {...}

analyzer = PathAnalyzer()
analyzer.add_custom_rule('custom_pattern', custom_rule)
```

### 扩展扫描器
```python
from src.scanner import AgentSystemScanner

class CustomScanner(AgentSystemScanner):
    def _analyze_custom_components(self, file_path):
        # 自定义组件检测逻辑
        pass
```

## 📝 版本历史

- **v1.0.0**: 完整的路径分析系统
  - 7种内置异常检测规则
  - 完整的CLI和编程接口
  - 交互式演示系统

## 🤝 贡献

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

MIT License - 详见LICENSE文件

---

**Watchdog - 让Agent系统分析更简单、更专业！** 🚀

## 功能特性

- 🔍 **智能扫描**: 自动识别和分析agent系统结构
- 🤖 **多框架支持**: 支持CrewAI、AutoGen等主流agent框架  
- 📊 **详细报告**: 生成包含agents、tools、crews、tasks的完整JSON报告
- 🛠️ **简化架构**: 轻量级设计，易于使用和扩展
- ⚡ **快速响应**: 精简的代码结构，快速扫描和分析

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 命令行使用

```bash
# 扫描目录
python cli.py /path/to/agent/project

# 扫描单个文件  
python cli.py /path/to/agent_file.py

# 指定输出文件和详细模式
python cli.py /path/to/project --output my_analysis.json --verbose
```

### 2. 演示脚本

```bash
# 交互式演示
python demo.py

# 运行示例
python example.py

# 功能测试
python test.py
```

### 3. 编程接口

```python
from scanner import scan_directory, scan_file

# 扫描目录
result = scan_directory('/path/to/agent/project')
print(f"发现 {result['scan_summary']['total_agents']} 个agents")

# 扫描文件
result = scan_file('/path/to/agent_file.py')
print(f"发现 {len(result['agents'])} 个agents")
```

## 项目结构

```
watchdog/
├── scanner.py        # 核心扫描引擎
├── cli.py           # 命令行接口
├── demo.py          # 交互式演示
├── example.py       # 使用示例
├── test.py          # 功能测试
├── tools.py         # CrewAI工具定义
├── inspector.py     # 简化的Inspector Agent
└── requirements.txt # 依赖包
```

## 扫描能力

Inspector Agent能够识别以下组件：

### Agents
- CrewAI Agent实例和类定义
- 自定义Agent类
- AutoGen Agent组件
- Agent配置参数（role, goal, backstory）

### Tools
- CrewAI BaseTool子类
- 工具函数定义
- 工具装饰器(@tool)

### Crews & Tasks
- CrewAI Crew和Task实例
- 团队和任务配置

### 文件结构
- Python文件统计
- 项目目录结构
- 文件类型分布

## 输出格式

扫描结果以JSON格式保存，包含：

```json
{
  "scan_info": {
    "target": "/path/to/project",
    "scan_type": "directory",
    "timestamp": "2025-05-28T20:39:00",
    "scanner_version": "2.0-simplified"
  },
  "scan_summary": {
    "total_agents": 3,
    "total_tools": 2,
    "total_crews": 1,
    "total_tasks": 4,
    "total_files": 8,
    "python_files": 5
  },
  "agents": [...],
  "tools": [...],
  "crews": [...],
  "tasks": [...],
  "file_structure": {...}
}
```

## 技术特性

### 1. AST解析
使用Python AST模块进行精确的代码结构分析

### 2. 正则表达式回退
当AST解析失败时，使用正则表达式进行模式匹配

### 3. 轻量级设计
移除了复杂的AI分析功能，专注于核心扫描能力

### 4. 多格式支持
支持扫描目录、单文件、以及混合项目结构

## 示例用法

```bash
# 扫描CrewAI项目
python cli.py ../crewai_gmail --verbose

# 扫描AutoGen项目
python cli.py ../autogen_magneticone

# 快速测试当前项目
python cli.py . --output self_scan.json
```

## 优化亮点

1. **代码精简**: 从373行减少到273行，提高了可维护性
2. **架构简化**: 移除了双agent架构，使用单一扫描器
3. **依赖减少**: 减少了对外部AI服务的依赖
4. **性能提升**: 更快的扫描速度和响应时间
5. **易于扩展**: 清晰的代码结构便于功能扩展

## 贡献

欢迎提交Issues和Pull Requests来改进Inspector Agent！

## 许可证

MIT License
