# JSON日志可视化功能使用指南

## 🎯 功能概述

SentinelAgent现在支持加载和可视化JSON格式的CrewAI日志，提供了比原始CSV格式更加直观、易读的展示方式。

## 🚀 快速开始

### 1. 转换CSV日志为JSON格式

首先使用我们的转换脚本将CSV格式的CrewAI日志转换为JSON：

```bash
# 转换单个文件
python scripts/analysis/csv_to_json_converter.py "/path/to/crewai-log.csv"

# 批量转换
python scripts/analysis/csv_to_json_converter.py --batch "/path/to/logs/"
```

### 2. 启动Web界面

```bash
cd /Users/xuhe/Documents/agent_experiments/SentinelAgent
python test_server.py
```

然后在浏览器中访问: http://localhost:5001

### 3. 加载JSON日志

在Web界面中有三种方式加载JSON日志：

#### 方法1：手动输入路径
1. 点击左侧菜单的 "Log Analysis"
2. 在 "Log File" 字段输入JSON文件路径
3. 将 "Log Format" 设置为 "JSON Format (CrewAI)"
4. 点击 "Analyze Logs"

#### 方法2：使用Load JSON Logs按钮
1. 点击 "Load JSON Logs" 按钮
2. 在文件选择对话框中选择转换后的JSON文件
3. 系统自动加载并显示

#### 方法3：使用示例文件
1. 点击 "Load Demo Logs" 按钮加载预设的示例文件

## 📊 可视化界面功能

### Overview（概览）
- **总条目数**: 显示日志中的总执行条目数量
- **Agent执行数**: 显示Agent执行的任务数量
- **工具调用数**: 显示使用工具的次数
- **唯一Agent数**: 显示参与执行的不同Agent数量

### Execution Flow（执行流程）
详细展示每个执行条目的信息：

- **🤖 Agent信息**: 显示Agent的角色、目标和背景描述
- **📧 邮件任务**: 展示邮件内容、发件人、主题等
- **📤 输出结果**: 显示Agent的执行结果
- **🔧 使用的工具**: 列出Agent调用的工具

### Agent Timeline（时间线）
按时间顺序展示Agent的执行过程：
- 时间戳信息
- Agent角色
- 执行的主要任务
- 输出预览

### Raw Data（原始数据）
以格式化的JSON形式显示完整的原始数据，便于调试和详细分析。

## 🎨 可视化特性

### 颜色编码
- **蓝色边框**: Agent执行任务
- **绿色边框**: 工具执行
- **灰色边框**: 其他类型

### 信息组织
- **邮件信息**: 独立区域显示邮件内容
- **分类规则**: 清晰展示邮件分类标准
- **输出结果**: 代码风格显示执行结果
- **工具标签**: 标签形式显示使用的工具

## 📈 分析能力

### CrewAI特定分析
- **邮件分类流程**: 追踪邮件从分类到回复的完整流程
- **Agent协作模式**: 理解多个Agent之间的协作关系
- **工具使用模式**: 分析工具调用的模式和效果
- **决策路径**: 可视化AI的决策过程

### 性能洞察
- **执行时间**: 通过时间戳分析执行效率
- **路径复杂度**: 理解任务执行的复杂程度
- **Agent负载**: 分析不同Agent的工作量

## 🔍 使用案例

### 邮件自动化系统分析
通过可视化界面可以清楚看到：
1. **Email Classifier**: 如何分析邮件内容并分类
2. **Email Responder**: 基于分类结果生成响应
3. **工具调用**: check_availability工具的使用情况
4. **决策逻辑**: 从Low-B分类到检查日历到生成回复的完整流程

### 调试和优化
- **错误定位**: 快速找到执行失败的环节
- **性能瓶颈**: 识别耗时较长的操作
- **逻辑验证**: 验证Agent的决策是否合理

## 🛠️ 高级功能

### 数据导出
分析结果自动保存为JSON文件，支持：
- 结果存档
- 离线分析
- 与其他工具集成

### 扩展性
系统支持：
- 自定义Agent模式识别
- 新的可视化组件
- 更多分析指标

## 💡 最佳实践

1. **定期转换**: 定期将新的CSV日志转换为JSON格式
2. **批量处理**: 使用批量转换功能处理多个日志文件
3. **结果对比**: 比较不同时间段的执行模式
4. **性能监控**: 定期检查Agent系统的执行效率

## 🔧 故障排除

### 常见问题

**Q: JSON文件加载失败**
A: 确保文件格式正确，包含 `execution_log` 和 `metadata` 字段

**Q: 可视化显示不完整**
A: 检查JSON文件是否由我们的转换脚本生成

**Q: 时间戳显示异常**
A: 确保时间戳字段格式为ISO 8601标准

## 📚 相关文档

- [CSV转换器使用指南](README_csv_converter.md)
- [SentinelAgent主文档](../README.md)
- [日志分析Demo](../examples/demos/log_analysis_demo.py)

---

*SentinelAgent - 让AI Agent系统的行为可视化、可理解、可优化*
