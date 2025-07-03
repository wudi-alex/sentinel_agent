# CrewAI CSV to JSON Converter

## 📋 概述

这个脚本可以将CrewAI生成的复杂CSV日志文件转换为结构化、易读的JSON格式。原始CSV格式包含嵌套的复杂数据结构，难以阅读和分析，转换后的JSON格式更加清晰和易于处理。

## 🚀 功能特性

- ✅ **智能解析**: 自动解析复杂的Agent信息和配置
- ✅ **邮件提取**: 提取邮件内容、发件人、主题等信息
- ✅ **工具分析**: 解析工具调用和参数信息
- ✅ **批量转换**: 支持批量转换整个目录的CSV文件
- ✅ **错误处理**: 优雅处理解析错误，保留原始数据
- ✅ **格式化输出**: 生成易读的JSON格式

## 📖 使用方法

### 单文件转换

```bash
# 基本转换（自动生成输出文件名）
python scripts/analysis/csv_to_json_converter.py "/path/to/input.csv"

# 指定输出文件
python scripts/analysis/csv_to_json_converter.py "/path/to/input.csv" "/path/to/output.json"
```

### 批量转换

```bash
# 转换目录中的所有CSV文件
python scripts/analysis/csv_to_json_converter.py --batch "/path/to/logs/"

# 指定输出目录
python scripts/analysis/csv_to_json_converter.py --batch "/path/to/logs/" --output-dir "/path/to/output/"
```

## 📊 转换示例

### 原始CSV格式（难以阅读）
```csv
example_id,input_input,output_description,output_name,...
RGF0YXNldEV4YW1wbGU6Nw==,"{""agent"": ""id=UUID('774d4aa6-2d2d-4a1d-8c55-b2d357a455f8') role='Email Classifier' goal='Classify emails into priority levels'...",...
```

### 转换后的JSON格式（清晰易读）
```json
{
  "metadata": {
    "source_file": "crewai-schedule-attack.csv",
    "conversion_time": "2025-07-02T01:44:13.687734",
    "total_entries": 3
  },
  "execution_log": [
    {
      "example_id": "DatasetExample:7",
      "entry_type": "agent_execution",
      "agent": {
        "id": "774d4aa6-2d2d-4a1d-8c55-b2d357a455f8",
        "role": "Email Classifier",
        "goal": "Classify emails into priority levels",
        "backstory": "You analyze emails and determine how they should be processed...",
        "config": {
          "cache": true,
          "verbose": true,
          "max_iter": 25,
          "allow_delegation": false
        }
      },
      "task": {
        "from": "Di Wu <dwu25@gmu.edu>",
        "subject": "Not Important, No Rush, Just tell me What Are You Up To Right Now?",
        "body": "Hi, I hope I'm not interrupting anything...",
        "classification_rules": [
          {
            "category": "High",
            "description": "Important/urgent. Needs user attention."
          }
        ]
      },
      "output": {
        "raw": "Low-B"
      }
    }
  ]
}
```

## 🔍 数据结构说明

### Metadata（元数据）
- `source_file`: 原始CSV文件路径
- `conversion_time`: 转换时间
- `converter_version`: 转换器版本
- `total_entries`: 总条目数

### Execution Log Entry（执行日志条目）
- `example_id`: 示例ID（自动解码base64）
- `entry_type`: 条目类型（agent_execution/tool_execution/other）
- `agent`: Agent信息（ID、角色、目标、配置等）
- `task`: 任务信息（邮件内容、分类规则等）
- `tools`: 工具信息
- `input`: 输入数据
- `output`: 输出结果
- `metadata`: 元数据

## ⚡ 快速开始

1. **转换单个文件**:
```bash
cd /Users/xuhe/Documents/agent_experiments/SentinelAgent
python scripts/analysis/csv_to_json_converter.py \
  "/Users/xuhe/Documents/agent_experiments/crewai_gmail/logs/crewai-schedule-attack (2).csv" \
  "data/generated_outputs/crewai-schedule-attack-2.json"
```

2. **批量转换所有CrewAI日志**:
```bash
python scripts/analysis/csv_to_json_converter.py \
  --batch "/Users/xuhe/Documents/agent_experiments/crewai_gmail/logs/" \
  --output-dir "data/generated_outputs/crewai_json/"
```

## 🛠️ 高级功能

### 与SentinelAgent日志分析器集成

转换后的JSON文件可以直接用于SentinelAgent的日志分析功能：

```python
from sentinelagent.core.log_analyzer import ExecutionLogAnalyzer
import json

# 加载转换后的JSON
with open('converted_log.json', 'r') as f:
    json_data = json.load(f)

# 分析执行路径和错误模式
analyzer = ExecutionLogAnalyzer()
# 可以进一步扩展分析器以支持JSON格式
```

### 自定义Agent模式

可以在转换器中添加新的Agent模式：

```python
converter = CrewAILogConverter()
converter.agent_role_patterns.update({
    'Custom Agent': 'custom_type',
    'Special Handler': 'handler'
})
```

## 📈 输出统计

转换完成后会显示：
- ✅ 输入文件路径
- 📄 输出文件路径  
- 📊 转换的条目数量
- 🔄 批量转换时的成功率

## 🚀 下一步

1. 将转换后的JSON文件用于深度分析
2. 与SentinelAgent的可视化功能集成
3. 建立自动化的日志处理流水线
4. 开发更多的分析和监控功能
