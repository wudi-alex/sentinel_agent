# Inspector Agent - Agent系统结构扫描器

一个轻量级的agent系统分析工具，专门用于扫描和分析CrewAI、AutoGen等agent框架的项目结构，并构建组件关系图。

## ✨ 功能特性

- 🔍 **智能扫描**: 自动识别agents、tools、crews、tasks等组件
- 🧠 **AST解析**: 使用Python AST进行精确代码分析
- 🔄 **正则后备**: AST失败时自动切换到正则表达式解析
- 📊 **详细报告**: 生成包含位置、参数、类型等详细信息的JSON报告
- 🔗 **关系图构建**: 构建agent系统组件的有向关系图
- 🎯 **多种扫描模式**: 支持目录扫描和单文件扫描
- 📱 **命令行工具**: 简单易用的CLI界面
- 🎮 **交互式演示**: 内置演示脚本展示所有功能

## 🚀 快速开始

### 命令行使用

```bash
# 基础扫描
python cli.py ../your_agent_project

# 指定输出文件
python cli.py ../your_agent_project --output my_scan.json

# 同时构建关系图
python cli.py ../your_agent_project --graph my_graph.json

# 显示详细信息
python cli.py ../your_agent_project --verbose

# 查看帮助
python cli.py --help
```

### Python API使用

#### 基础扫描

```python
from scanner import scan_directory, scan_file

# 扫描目录
result = scan_directory('/path/to/agent/project')
print(f"发现 {result['scan_summary']['total_agents']} 个agents")

# 扫描单个文件
result = scan_file('agent_file.py')
```

#### 图构建

```python
from graph_builder import build_graph_from_scan, scan_and_build_graph

# 从扫描结果构建图
graph_data = build_graph_from_scan(scan_result)

# 一体化扫描和图构建
graph_data = scan_and_build_graph('/path/to/project', 'output_graph.json')

print(f"构建了包含 {graph_data['graph_summary']['total_nodes']} 个节点的图")
```

## 📊 输出格式

### 扫描结果

```json
{
  "scan_info": {
    "target": "/path/to/project",
    "scan_type": "directory",
    "timestamp": "2025-05-29T00:00:00.000000",
    "scanner_version": "2.0-simplified"
  },
  "scan_summary": {
    "total_agents": 3,
    "total_tools": 2,
    "total_crews": 1,
    "total_tasks": 2,
    "total_files": 15,
    "python_files": 8
  },
  "agents": [...],
  "tools": [...],
  "crews": [...],
  "tasks": [...]
}
```

### 关系图结构

```json
{
  "graph_info": {
    "source_scan": {...},
    "build_timestamp": "2025-05-29T00:00:00.000000",
    "builder_version": "1.0"
  },
  "graph_summary": {
    "total_nodes": 5,
    "total_edges": 12,
    "node_types": {
      "agent": 3,
      "tool": 2
    },
    "relationship_types": {
      "file_proximity": 6,
      "same_crew_collaboration": 4,
      "name_similarity": 2
    },
    "average_degree": 2.4
  },
  "nodes": [
    {
      "id": "agent_0",
      "type": "agent",
      "name": "Agent_1",
      "metadata": {
        "role": "Email Classifier",
        "crews": [...],
        "tasks": [...]
      }
    }
  ],
  "edges": [...]
}
```

## 🔗 关系图功能

Inspector Agent 能够构建agent系统的有向关系图，采用优化的节点结构：

### 节点类型
- **Agent**: CrewAI或其他框架的智能体，包含相关的crew和task信息作为元数据
- **Tool**: 工具和函数

### 关系类型
- **file_proximity**: 同文件内的组件关系 (权重: 0.3)
- **same_crew_collaboration**: 相同crew内的agent协作关系 (权重: 0.7)
- **name_similarity**: 基于命名的相似关系 (权重: 0.6)
- **explicit_usage**: 明确的使用关系 (权重: 0.9)

### 图结构优势
- **简化节点**: 只有agents和tools作为主要节点，使图更清晰
- **丰富元数据**: crew和task信息完整保存在agent节点的元数据中
- **准确关系**: 关系更好地反映实际的系统架构和协作模式

## 🎮 演示脚本

运行交互式演示查看所有功能：

```bash
python demo_enhanced.py
```

或运行图构建专门演示：

```bash
python graph_demo.py
```

## 🛠️ 支持的框架

- ✅ **CrewAI**: 完全支持agents、tools、crews、tasks检测
- ✅ **AutoGen**: 支持agent检测
- ✅ **自定义框架**: 通过正则表达式模式检测

## 📁 项目结构

```
watchdog/
├── scanner.py           # 核心扫描器 (273行，优化版)
├── graph_builder.py     # 关系图构建器
├── cli.py              # 命令行接口
├── demo_enhanced.py    # 增强演示脚本
├── graph_demo.py       # 图构建演示
├── example.py          # 简单示例
├── test.py             # 基础测试
└── README.md           # 项目文档
```

## 🔧 技术实现

- **AST分析**: 使用Python内置ast模块进行精确解析
- **正则后备**: 语法错误时自动降级到正则表达式
- **图算法**: 基于文件位置、命名约定、内容分析构建关系
- **JSON输出**: 标准化的结构化数据格式
- **错误处理**: 优雅的错误处理和信息提示

## 💡 使用场景

1. **项目分析**: 了解agent项目的整体结构
2. **代码审查**: 快速识别所有agent组件
3. **架构可视化**: 通过关系图理解组件依赖
4. **重构支持**: 识别需要修改的相关组件
5. **文档生成**: 自动生成项目组件清单

## 🎯 优化亮点

- **代码简化**: 从373行优化到273行 (-27%)
- **性能提升**: 移除不必要的复杂度
- **功能增强**: 新增关系图构建功能
- **易用性**: 更简洁的API和命令行接口
- **可扩展性**: 模块化设计，易于扩展新功能

## 📄 许可证

MIT License - 详见LICENSE文件

---

*Inspector Agent - 让agent系统结构一目了然* 🔍✨
