# CSV to JSON Log Converter v2.0 使用指南

## 概述

CSV to JSON Log Converter v2.0 是一个强大的日志转换工具，专门用于将不同AI Agent框架的CSV日志文件转换为结构化的JSON格式，以便在SentinelAgent Web UI中进行可视化分析。

## 支持的框架

### 1. CrewAI 
- **列名**: `input_input`, `output_raw`, `output_summary`, `output_agent`, 等
- **特点**: 包含Agent角色、目标、背景故事和任务信息
- **使用场景**: CrewAI框架生成的执行日志

### 2. MagneticOne/AutoGen
- **列名**: `input_messages`, `output_messages`, `metadata_span_kind`, `input_tools`, 等  
- **特点**: 基于消息对话的格式，包含角色对话和工具调用
- **使用场景**: AutoGen、MagneticOne框架生成的执行日志

## 安装要求

```bash
pip install argparse json logging ast base64 pathlib
```

## 使用方法

### 单文件转换

#### 转换CrewAI日志
```bash
python csv_to_json_converter_v2.py \
  --input "/path/to/crewai_log.csv" \
  --output "/path/to/output.json" \
  --format crewai
```

#### 转换MagneticOne日志  
```bash
python csv_to_json_converter_v2.py \
  --input "/path/to/magneticone_log.csv" \
  --output "/path/to/output.json" \
  --format magneticone
```

#### 自动检测格式
```bash
python csv_to_json_converter_v2.py \
  --input "/path/to/log.csv" \
  --output "/path/to/output.json" \
  --auto-detect
```

### 批量转换

#### 转换整个目录
```bash
python csv_to_json_converter_v2.py \
  --batch-input "/path/to/csv_logs/" \
  --batch-output "/path/to/json_logs/" \
  --format magneticone
```

#### 批量转换并自动检测
```bash
python csv_to_json_converter_v2.py \
  --batch-input "/path/to/mixed_logs/" \
  --batch-output "/path/to/json_logs/" \
  --auto-detect
```

## 参数说明

| 参数 | 说明 | 必需 |
|------|------|------|
| `--input` | 输入CSV文件路径 | 单文件转换时必需 |
| `--output` | 输出JSON文件路径 | 单文件转换时必需 |
| `--batch-input` | 输入CSV文件目录 | 批量转换时必需 |
| `--batch-output` | 输出JSON文件目录 | 批量转换时必需 |
| `--format` | 日志格式 (`crewai` 或 `magneticone`) | 可选，默认`crewai` |
| `--auto-detect` | 自动检测日志格式 | 可选 |

## 输出格式

转换后的JSON文件包含以下结构：

```json
{
  "metadata": {
    "source_file": "/path/to/source.csv",
    "conversion_time": "2025-07-02T21:51:28.109061",
    "converter_version": "2.0",
    "total_entries": 11
  },
  "execution_log": [
    {
      "example_id": "DatasetExample:103",
      "timestamp": "2025-07-02T21:51:28.109258",
      "entry_type": "agent_response",
      "agent": {
        "name": "MagenticOneOrchestrator",
        "role": "MagenticOneOrchestrator"
      },
      "task": {
        "content": "任务描述...",
        "type": "file_processing"
      },
      "tools": [],
      "input": { /* 输入数据 */ },
      "output": { /* 输出数据 */ },
      "metadata": { /* 元数据 */ }
    }
  ]
}
```

## 实际使用示例

### 示例1: 转换MagneticOne日志

```bash
cd /Users/xuhe/Documents/agent_experiments/SentinelAgent

python scripts/analysis/csv_to_json_converter_v2.py \
  --input "/Users/xuhe/Documents/agent_experiments/autogen_magneticone/logs/magentic-one-file-code-execution.csv" \
  --output "data/analysis_results/magneticone/magentic-one-file-code-execution-v2.json" \
  --format magneticone
```

### 示例2: 批量转换并自动检测

```bash
python scripts/analysis/csv_to_json_converter_v2.py \
  --batch-input "/Users/xuhe/Documents/agent_experiments/autogen_magneticone/logs/" \
  --batch-output "data/analysis_results/magneticone/" \
  --auto-detect
```

## 在SentinelAgent Web UI中查看

1. 启动测试服务器:
   ```bash
   python test_server.py
   ```

2. 在浏览器中打开: http://localhost:5001

3. 使用"Load JSON Logs"按钮上传转换后的JSON文件

4. 选择"JSON Format (CrewAI)"格式

5. 查看可视化结果:
   - **概览**: 总体统计信息
   - **执行流程**: 按时间顺序的执行步骤
   - **时间线**: 交互式时间线视图
   - **原始数据**: JSON格式的完整数据

## 错误处理

转换器包含以下错误处理机制：

1. **格式检测**: 自动检测并处理不同的CSV格式
2. **数据解析**: 安全解析JSON字符串和Python字面量
3. **Base64解码**: 安全解码编码的ID
4. **容错处理**: 跳过无法解析的行并记录警告
5. **日志记录**: 详细的转换过程日志

## 故障排除

### 常见问题

1. **转换后的数据为空**
   - 检查CSV文件格式是否正确
   - 尝试使用`--auto-detect`参数

2. **解析错误**
   - 检查CSV文件编码（应为UTF-8）
   - 确认列名与预期格式匹配

3. **Web UI无法加载**
   - 检查JSON文件格式是否正确
   - 确认文件路径和权限

### 日志输出示例

```
2025-07-02 21:51:28,109 - INFO - Converting /path/to/input.csv to /path/to/output.json using magneticone format
2025-07-02 21:51:28,111 - INFO - Successfully converted 11 entries
```

## 版本更新

### v2.0 新特性
- ✅ 支持MagneticOne/AutoGen日志格式
- ✅ 自动格式检测功能
- ✅ 增强的错误处理
- ✅ 改进的数据解析
- ✅ 更好的日志记录

### 与v1.0的差异
- 新增MagneticOne格式支持
- 改进的类结构设计
- 更强的容错能力
- 自动检测功能

## 技术支持

如果您遇到问题，请检查：
1. CSV文件格式和编码
2. 命令行参数是否正确
3. 文件路径和权限
4. 日志输出中的错误信息

建议先使用`--auto-detect`功能进行测试转换。
