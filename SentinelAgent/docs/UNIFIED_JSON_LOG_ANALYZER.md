# 统一JSON日志分析器使用指南

## 🎯 概述

SentinelAgent现在支持统一的JSON日志分析，可以处理CrewAI和MagneticOne/AutoGen两种格式的JSON日志，无需分别处理不同的CSV格式。

## 🔄 架构改进

### 统一分析流程
```
原始CSV → JSON转换器 → 统一JSON分析器 → 分析结果
```

### 核心优势
- **格式统一**: 所有日志都转换为标准JSON格式
- **自动检测**: 自动识别CrewAI和MagneticOne格式差异
- **扩展性强**: 易于添加新的Agent框架支持
- **错误处理**: 健壮的解析和错误恢复机制

## 📊 支持的格式

### CrewAI格式特征
- `agent.role`, `agent.goal`, `agent.backstory`
- `task.description`, `task.expected_output`
- `input`, `output` 结构
- 工具调用模式

### MagneticOne/AutoGen格式特征  
- `agent.name` (Orchestrator, Coder, Executor等)
- `input.messages`, `output.messages`
- 工具函数定义
- LLM调用信息

## 🚀 使用方法

### 1. 直接分析JSON文件

```python
from sentinelagent.core.log_analyzer import ExecutionLogAnalyzer

analyzer = ExecutionLogAnalyzer()
result = analyzer.analyze_log_file("converted_log.json", file_type="json")

print(f"Total entries: {len(result.log_entries)}")
print(f"Execution paths: {len(result.execution_paths)}")
print(f"Format type: {result.statistics['format_type']}")
```

### 2. 命令行使用

```bash
# 自动检测JSON格式
sentinelagent --analyze-logs converted_log.json

# 明确指定JSON格式
sentinelagent --analyze-logs converted_log.json --log-format json
```

### 3. Web UI使用

1. 访问SentinelAgent Web界面
2. 选择"Load JSON Logs"
3. 上传转换后的JSON文件
4. 查看可视化分析结果

## 📈 分析能力

### 统一分析指标
- **日志条目数量**: 总条目数和类型分布
- **执行路径**: 路径数量、长度统计
- **Agent使用**: 各Agent的调用次数
- **错误检测**: 错误类型和严重级别
- **性能分析**: 执行效率和瓶颈识别

### 格式特定分析

#### CrewAI专项分析
- 任务类型分布
- Agent-Task配对检查
- 工具使用统计
- 决策流程分析

#### MagneticOne专项分析
- Agent类型分布（Orchestrator, Coder等）
- 协调器存在检查
- 消息传递模式
- 工具调用链分析

## 🔍 错误检测

### 通用错误模式
- **无限循环**: 同一Agent连续执行
- **路径不完整**: 缺少关键步骤
- **Agent错误**: 执行失败或异常
- **角色冲突**: Agent角色不一致

### 格式特定检查
- **CrewAI**: Agent-Task配对、工具链完整性
- **MagneticOne**: Orchestrator协调、消息流检查

## 💡 最佳实践

### 1. 数据准备
```bash
# 先转换CSV为JSON
python scripts/analysis/csv_to_json_converter_v2.py input.csv

# 再进行统一分析
sentinelagent --analyze-logs converted_input.json
```

### 2. 批量处理
```python
import os
from pathlib import Path

analyzer = ExecutionLogAnalyzer()
json_files = Path("converted_logs/").glob("*.json")

for json_file in json_files:
    result = analyzer.analyze_log_file(str(json_file), file_type="json")
    print(f"{json_file.name}: {result.summary}")
```

### 3. 结果对比
```python
# 比较不同格式的分析结果
crewai_result = analyzer.analyze_log_file("crewai_log.json", "json")
magneticone_result = analyzer.analyze_log_file("magneticone_log.json", "json")

print("CrewAI agents:", len(crewai_result.statistics['agent_usage']))
print("MagneticOne agents:", len(magneticone_result.statistics['agent_usage']))
```

## 🔧 技术实现

### 核心组件

#### JSONLogAnalyzer类
- **格式检测**: `_detect_format_type()`
- **条目解析**: `_parse_json_log_entries()`
- **路径提取**: `_extract_execution_paths()`
- **错误分析**: `_analyze_execution_path()`

#### 格式特定解析器
- **CrewAI解析**: `_parse_crewai_entry()`
- **MagneticOne解析**: `_parse_magneticone_entry()`
- **通用解析**: `_parse_generic_entry()`

### 集成方式
1. **主分析器**: ExecutionLogAnalyzer自动调用JSON分析器
2. **Web应用**: handle_json_log_analysis()使用统一分析器
3. **CLI工具**: 支持json格式参数

## 🧪 测试验证

运行测试脚本验证功能：
```bash
python test_unified_json_analyzer.py
```

测试内容：
- 格式自动检测
- CrewAI和MagneticOne日志分析
- 错误检测和建议生成
- 统计信息准确性

## 📚 相关文档

- [CSV到JSON转换器指南](CSV_TO_JSON_CONVERTER_GUIDE.md)
- [JSON日志可视化指南](JSON_LOG_VISUALIZATION.md)
- [SentinelAgent用户手册](README.md)

## 🔮 未来扩展

### 计划功能
- 支持更多Agent框架（LangChain, LlamaIndex等）
- 实时日志流分析
- 自定义分析规则配置
- 跨会话执行路径追踪

### 贡献指南
如需添加新的Agent框架支持：
1. 在`_detect_format_type()`中添加检测逻辑
2. 实现新的`_parse_[framework]_entry()`方法
3. 添加格式特定的统计和分析功能
4. 更新测试用例和文档
