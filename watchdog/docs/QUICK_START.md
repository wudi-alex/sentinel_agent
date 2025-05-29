# Inspector Agent - 快速开始指南

## 🚀 5分钟快速上手

### 1. 基础扫描
```bash
# 扫描agent项目
python cli.py /path/to/your/agent/project

# 扫描当前项目自身
python cli.py .
```

### 2. 保存结果
```bash
# 指定输出文件
python cli.py ../crewai_gmail --output my_scan.json
```

### 3. 构建关系图
```bash
# 同时生成扫描结果和关系图
python cli.py ../crewai_gmail --graph my_graph.json
```

### 4. 详细模式
```bash
# 显示详细信息
python cli.py ../crewai_gmail --verbose
```

### 5. 完整命令
```bash
# 完整功能演示
python cli.py ../crewai_gmail --output scan.json --graph graph.json --verbose
```

## 🎮 交互式演示

```bash
# 运行增强演示
python demo_enhanced.py

# 运行图构建专门演示
python graph_demo.py
```

## 💻 编程接口

### 基础扫描
```python
from scanner import scan_directory
result = scan_directory('/path/to/project')
print(f"发现 {result['scan_summary']['total_agents']} 个agents")
```

### 图构建
```python
from graph_builder import scan_and_build_graph
graph_data = scan_and_build_graph('.', 'my_graph.json')
print(f"构建了 {graph_data['graph_summary']['total_nodes']} 个节点的图")
```

## 📊 理解输出

### 扫描统计
- **Agents**: 发现的智能体数量
- **Tools**: 发现的工具数量  
- **Crews**: 发现的团队数量
- **Tasks**: 发现的任务数量

### 图统计
- **节点**: 所有组件总数
- **边**: 组件间关系总数
- **平均度数**: 每个节点的平均连接数

## 🎯 常用场景

### 项目分析
```bash
python cli.py /path/to/unknown/project --verbose
```

### 架构理解
```bash
python cli.py /path/to/project --graph architecture.json
```

### 代码审查
```bash
python cli.py /path/to/project --output review.json --verbose
```

## 💡 提示和技巧

1. **使用相对路径**: `../project_name` 比绝对路径更方便
2. **详细模式**: 添加 `--verbose` 查看组件详情
3. **批量分析**: 可以编写脚本批量扫描多个项目
4. **图可视化**: JSON图文件可以用于后续可视化
5. **错误排查**: 如果扫描失败，检查目标路径是否正确

## 🔍 支持的项目类型

- ✅ **CrewAI项目**: 完整支持
- ✅ **AutoGen项目**: 基础支持  
- ✅ **混合项目**: 智能识别
- ✅ **自定义Agent**: 通过正则匹配

## 📱 获取帮助

```bash
# 查看帮助
python cli.py --help

# 查看版本信息
python -c "from scanner import AgentSystemScanner; print('Scanner v2.0')"
```

---

**开始探索你的Agent系统吧！** 🔍✨
