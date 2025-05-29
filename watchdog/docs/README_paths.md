# 路径分析系统 (Path Analysis System)

## 概述

路径分析系统是Watchdog项目的高级功能，用于分析agent系统中的执行路径，识别正常和可疑的行为模式，进行异常检测。该系统扩展了现有的扫描和图构建功能，添加了路径分析能力。

## 核心功能

### 1. 路径发现 (Path Discovery)
- 使用深度优先搜索(DFS)算法发现图中的所有执行路径
- 支持可配置的最大路径长度
- 自动避免无限循环

### 2. 状态分类 (State Classification)
- **节点状态**: normal, suspicious, critical, isolated, overloaded
- **边状态**: normal, suspicious, critical, weak, strong

### 3. 路径类型分析 (Path Type Analysis)
- **agent_collaboration**: Agent之间的协作路径
- **agent_tool_usage**: Agent使用工具的路径
- **mixed_interaction**: 混合交互路径

### 4. 异常检测 (Anomaly Detection)
系统包含7个默认分析规则：
- `isolated_agents`: 检测孤立的Agent
- `excessive_tool_usage`: 检测过度的工具使用
- `circular_dependencies`: 检测循环依赖
- `unused_tools`: 检测未使用的工具
- `complex_collaboration`: 检测复杂协作模式
- `high_weight_relationships`: 检测高权重关系
- `cross_file_anomalies`: 检测跨文件异常

### 5. 风险评分 (Risk Scoring)
- 路径级别风险评分
- 节点级别风险评分
- 整体系统风险评分
- 风险等级分类：low, medium, high

## 使用方法

### 1. 命令行接口 (CLI)

#### 基本使用
```bash
# 只执行扫描
python cli.py <目标路径>

# 扫描 + 图构建
python cli.py <目标路径> --graph graph_output.json

# 扫描 + 路径分析
python cli.py <目标路径> --paths paths_output.json

# 完整分析 (扫描 + 图 + 路径)
python cli.py <目标路径> --all

# 分析已有图文件
python cli.py --analyze-graph graph_file.json

# 详细输出
python cli.py <目标路径> --paths paths.json --verbose
```

#### CLI选项说明
- `-o, --output`: 指定扫描输出文件名
- `-g, --graph`: 同时构建关系图并保存
- `-p, --paths`: 同时进行路径分析并保存
- `-a, --all`: 执行完整分析
- `--analyze-graph`: 分析已有的图文件
- `-v, --verbose`: 显示详细信息

### 2. 编程接口

#### 使用Inspector进行完整分析
```python
from inspector import InspectorAgent

inspector = InspectorAgent()

# 完整分析
result = inspector.comprehensive_analysis(
    target_path="./my_agent_project",
    scan_output="scan.json",
    graph_output="graph.json", 
    path_output="paths.json"
)

# 分析已有图
path_analysis = inspector.analyze_existing_graph(
    graph_file="graph.json",
    output_file="paths.json"
)
```

#### 直接使用路径分析器
```python
from path_analyzer import PathAnalyzer, analyze_graph_paths

# 从图数据分析
analyzer = PathAnalyzer()
result = analyzer.analyze_paths(graph_data)

# 便捷函数
result = analyze_graph_paths(graph_data)

# 从文件分析并保存
from path_analyzer import analyze_paths_from_file
result = analyze_paths_from_file("graph.json", "paths.json")
```

### 3. 演示系统

运行交互式演示：
```bash
python path_demo.py
```

演示包含：
- 完整分析流程演示
- 路径类型分析演示
- 异常检测演示
- 安全洞察演示
- 自定义目录分析

## 输出格式

### JSON输出结构
```json
{
  "analysis_info": {
    "timestamp": "2025-05-29T01:07:58.874632",
    "analyzer_version": "1.0",
    "rules_applied": 7
  },
  "overall_assessment": {
    "total_risk_score": 0.0,
    "risk_level": "low",
    "total_paths_analyzed": 4,
    "suspicious_patterns_found": 1
  },
  "node_analysis": {
    "total_nodes": 2,
    "node_state_distribution": {"normal": 2},
    "nodes_with_states": {"agent_0": "normal", "agent_1": "normal"}
  },
  "edge_analysis": {
    "total_edges": 4,
    "edge_state_distribution": {"normal": 4},
    "edges_with_states": {"0": "normal", "1": "normal", "2": "normal", "3": "normal"}
  },
  "path_analysis": {
    "path_type_distribution": {"agent_collaboration": 4},
    "risk_score_distribution": {"low": 4, "medium": 0, "high": 0},
    "detailed_paths": [...]
  },
  "suspicious_patterns": [
    {
      "pattern_type": "circular_dependencies",
      "affected_nodes": ["agent_1", "agent_0"],
      "risk_level": "high",
      "details": "Detected circular dependencies in the graph",
      "rule": "circular_dependencies",
      "severity": "high",
      "description": "检测循环依赖"
    }
  ],
  "recommendations": [
    "CRITICAL: Resolve circular dependencies to prevent infinite loops"
  ]
}
```

## 配置选项

### PathAnalyzer参数
```python
analyzer = PathAnalyzer(
    max_path_length=10,    # 最大路径长度
    enable_cycles=False,   # 是否启用环路检测
    risk_threshold=0.7     # 风险阈值
)
```

### 自定义分析规则
```python
def custom_rule(graph_data):
    """自定义分析规则"""
    return {
        'pattern_type': 'custom_pattern',
        'affected_nodes': [],
        'risk_level': 'medium',
        'details': 'Custom pattern detected'
    }

analyzer.add_custom_rule('custom_pattern', custom_rule)
```

## 实际应用场景

### 1. 安全监控
- 检测异常的Agent行为模式
- 识别潜在的安全威胁
- 监控系统完整性

### 2. 性能优化
- 识别低效的协作模式
- 检测资源使用异常
- 优化Agent交互路径

### 3. 系统诊断
- 分析系统架构问题
- 检测设计缺陷
- 提供改进建议

### 4. 合规检查
- 验证系统符合安全标准
- 确保正确的权限控制
- 检查数据流合规性

## 文件结构

```
watchdog/
├── path_analyzer.py      # 核心路径分析器
├── path_demo.py         # 演示系统
├── inspector.py         # Inspector Agent (已增强)
├── cli.py              # 命令行接口 (已增强)
├── scanner.py          # 扫描器 (已修复)
├── graph_builder.py    # 图构建器
└── README_paths.md     # 本文档
```

## 依赖项

确保安装以下依赖：
```bash
pip install crewai
pip install networkx  # 如果使用图算法增强
```

## 扩展开发

### 添加新的分析规则
1. 在PathAnalyzer中定义新规则函数
2. 将规则添加到default_rules
3. 定义规则的严重程度和描述

### 自定义路径类型
1. 扩展path_type_classifier方法
2. 添加新的路径类型定义
3. 更新路径分析逻辑

### 增强风险评分算法
1. 修改calculate_path_risk方法
2. 调整风险因子权重
3. 添加新的风险指标

## 故障排除

### 常见问题
1. **函数签名错误**: 确保scanner模块的convenience函数支持output_file参数
2. **循环依赖检测**: 系统会自动检测并报告循环依赖
3. **内存使用**: 对于大型图，考虑调整max_path_length参数

### 调试模式
```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 使用调试模式
analyzer = PathAnalyzer(debug=True)
```

## 版本历史

- **v1.0**: 初始版本，包含基本路径分析功能
- 支持7种默认分析规则
- 完整的CLI和编程接口
- 交互式演示系统

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 添加测试用例
4. 提交Pull Request

## 许可证

本项目遵循MIT许可证。
