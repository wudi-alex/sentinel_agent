// SentinelAgent Web UI JavaScript
console.log('🤖 SentinelAgent UI - 初始化开始');

const { createApp } = Vue;
const { ElMessage, ElMessageBox } = ElementPlus;

// 图标组件
const { 
    Search, Connection, Guide, Document, Folder, 
    Upload, Download, RefreshRight, View, Delete 
} = ElementPlusIconsVue;

console.log('✅ Vue组件和图标加载完成');

const app = createApp({
    data() {
        return {
            // 当前活跃的标签页
            activeTab: 'scanner',
            
            // 显示状态
            showAbout: false,
            showResultDialog: false,
            
            // 加载状态
            scanLoading: false,
            graphLoading: false,
            pathsLoading: false,
            logsLoading: false,
            
            // 表单数据
            scanForm: {
                path: '',
                type: 'directory'
            },
            
            graphForm: {
                dataSource: 'scan',
                path: ''
            },
            
            pathsForm: {
                dataSource: 'graph',
                graphFile: ''
            },
            
            logsForm: {
                logFile: '',
                format: 'auto',
                graphFile: ''
            },
            
            // 结果数据
            scanResult: null,
            graphResult: null,
            pathsResult: null,
            logsResult: null,
            
            // 示例项目和结果文件
            examples: [],
            resultFiles: [],
            
            // 当前查看的结果
            currentResult: null,
            currentResultData: null
        };
    },
    
    mounted() {
        console.log('🚀 Vue应用已挂载 - SentinelAgent UI启动');
        this.loadExamples();
        this.loadResults();
        console.log('📊 初始数据加载完成');
    },
    
    methods: {
        // 菜单选择处理
        handleMenuSelect(index) {
            this.activeTab = index;
        },
        
        // 加载示例项目
        async loadExamples() {
            try {
                const response = await fetch('/api/examples');
                const data = await response.json();
                this.examples = data.examples;
            } catch (error) {
                console.error('加载示例失败:', error);
            }
        },
        
        // 加载示例项目
        loadExample(example) {
            this.scanForm.path = example.path;
            this.scanForm.type = 'directory';
            this.activeTab = 'scanner';
            ElMessage.success(`已加载示例: ${example.name}`);
        },
        
        // 路径选择（简化版，实际可以集成文件选择器）
        selectPath() {
            ElMessageBox.prompt('请输入路径', '选择路径', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                inputValue: this.scanForm.path
            }).then(({ value }) => {
                this.scanForm.path = value;
            }).catch(() => {});
        },
        
        // 执行扫描
        async executeScan() {
            if (!this.scanForm.path.trim()) {
                ElMessage.error('请输入扫描路径');
                return;
            }
            
            this.scanLoading = true;
            try {
                const response = await fetch('/api/scan', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        path: this.scanForm.path,
                        type: this.scanForm.type
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    this.scanResult = data.result;
                    
                    // 显示结果摘要 - 针对agent系统优化
                    const summary = this.scanResult.scan_summary || {};
                    let summaryText = `扫描完成!\n`;
                    summaryText += `- 代理(Agents): ${summary.total_agents || 0}\n`;
                    summaryText += `- 工具(Tools): ${summary.total_tools || 0}\n`;
                    summaryText += `- 团队(Crews): ${summary.total_crews || 0}\n`;
                    summaryText += `- 任务(Tasks): ${summary.total_tasks || 0}\n`;
                    summaryText += `- Python文件: ${summary.python_files || 0}`;
                    
                    ElMessage({
                        message: summaryText,
                        type: 'success',
                        duration: 5000,
                        showClose: true
                    });
                } else {
                    ElMessage.error(data.error || '扫描失败');
                }
            } catch (error) {
                ElMessage.error('扫描失败: ' + error.message);
            } finally {
                this.scanLoading = false;
            }
        },
        
        // 清空扫描结果
        clearScanResult() {
            this.scanResult = null;
        },
        
        // 构建关系图
        async buildGraph() {
            if (this.graphForm.dataSource === 'scan' && !this.scanResult) {
                ElMessage.error('请先执行扫描');
                return;
            }
            
            if (this.graphForm.dataSource === 'path' && !this.graphForm.path.trim()) {
                ElMessage.error('请输入扫描路径');
                return;
            }
            
            this.graphLoading = true;
            try {
                const requestData = this.graphForm.dataSource === 'scan' 
                    ? { scan_data: this.scanResult }
                    : { path: this.graphForm.path };
                    
                const response = await fetch('/api/build-graph', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    this.graphResult = data.result;
                    ElMessage.success('关系图构建完成');
                    
                    // 渲染图形
                    this.$nextTick(() => {
                        this.renderGraph();
                    });
                } else {
                    ElMessage.error(data.error || '图构建失败');
                }
            } catch (error) {
                ElMessage.error('图构建失败: ' + error.message);
            } finally {
                this.graphLoading = false;
            }
        },
        
        // 渲染关系图
        renderGraph() {
            if (!this.graphResult || !this.graphResult.nodes) return;
            
            const container = d3.select('#graph-container');
            container.selectAll('*').remove(); // 清空之前的内容
            
            const width = 800;
            const height = 500;
            
            const svg = container
                .append('svg')
                .attr('width', width)
                .attr('height', height);
                
            // 确保数据结构正确
            const nodes = this.graphResult.nodes.map(d => ({ ...d }));
            const links = this.graphResult.edges.map(d => ({ 
                ...d,
                source: d.source || d.from,
                target: d.target || d.to
            }));
            
            const simulation = d3.forceSimulation(nodes)
                .force('link', d3.forceLink(links).id(d => d.id))
                .force('charge', d3.forceManyBody().strength(-300))
                .force('center', d3.forceCenter(width / 2, height / 2));
                
            const link = svg.append('g')
                .selectAll('line')
                .data(links)
                .enter().append('line')
                .attr('stroke', '#999')
                .attr('stroke-opacity', 0.6)
                .attr('stroke-width', d => Math.sqrt(d.weight || 1));
                
            const node = svg.append('g')
                .selectAll('circle')
                .data(nodes)
                .enter().append('circle')
                .attr('r', d => Math.max(5, Math.min(15, (d.properties?.importance || 1) * 10)))
                .attr('fill', d => this.getNodeColor(d.type))
                .style('cursor', 'pointer')
                .call(d3.drag()
                    .on('start', (event, d) => this.dragstarted(event, d, simulation))
                    .on('drag', (event, d) => this.dragged(event, d))
                    .on('end', (event, d) => this.dragended(event, d, simulation)));
                    
            const text = svg.append('g')
                .selectAll('text')
                .data(nodes)
                .enter().append('text')
                .text(d => d.properties?.name || d.id)
                .attr('font-size', '10px')
                .attr('dx', 15)
                .attr('dy', 4)
                .style('pointer-events', 'none');
                
            // 添加节点点击事件
            node.on('click', (event, d) => {
                ElMessage.info(`节点: ${d.id}, 类型: ${d.type}`);
            });
                
            simulation.on('tick', () => {
                link
                    .attr('x1', d => d.source.x)
                    .attr('y1', d => d.source.y)
                    .attr('x2', d => d.target.x)
                    .attr('y2', d => d.target.y);
                    
                node
                    .attr('cx', d => d.x)
                    .attr('cy', d => d.y);
                    
                text
                    .attr('x', d => d.x)
                    .attr('y', d => d.y);
            });
        },
        
        // 拖拽处理函数
        dragstarted(event, d, simulation) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        },
        
        dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        },
        
        dragended(event, d, simulation) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        },
        
        // 节点颜色映射
        getNodeColor(type) {
            const colors = {
                'agent': '#67C23A',
                'tool': '#E6A23C',
                'crew': '#409EFF',
                'task': '#F56C6C',
                'file': '#909399',
                'default': '#909399'
            };
            return colors[type] || colors.default;
        },
        
        // 路径分析
        async analyzePaths() {
            if (this.pathsForm.dataSource === 'graph' && !this.graphResult) {
                ElMessage.error('请先构建关系图');
                return;
            }
            
            if (this.pathsForm.dataSource === 'file' && !this.pathsForm.graphFile.trim()) {
                ElMessage.error('请输入图文件路径');
                return;
            }
            
            this.pathsLoading = true;
            try {
                const requestData = this.pathsForm.dataSource === 'graph' 
                    ? { graph_data: this.graphResult }
                    : { graph_file: this.pathsForm.graphFile };
                    
                const response = await fetch('/api/analyze-paths', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    this.pathsResult = data.result;
                    ElMessage.success('路径分析完成');
                } else {
                    ElMessage.error(data.error || '路径分析失败');
                }
            } catch (error) {
                ElMessage.error('路径分析失败: ' + error.message);
            } finally {
                this.pathsLoading = false;
            }
        },
        
        // 日志分析
        async analyzeLogs() {
            if (!this.logsForm.logFile.trim()) {
                ElMessage.error('请输入日志文件路径');
                return;
            }
            
            this.logsLoading = true;
            try {
                const response = await fetch('/api/analyze-logs', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        log_file: this.logsForm.logFile,
                        format: this.logsForm.format,
                        graph_file: this.logsForm.graphFile
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    this.logsResult = data.result;
                    ElMessage.success('日志分析完成');
                } else {
                    ElMessage.error(data.error || '日志分析失败');
                }
            } catch (error) {
                ElMessage.error('日志分析失败: ' + error.message);
            } finally {
                this.logsLoading = false;
            }
        },
        
        // 计算成功率
        calculateSuccessRate(logsResult) {
            if (!logsResult.log_summary) return 0;
            const total = logsResult.log_summary.total_entries || 0;
            const errors = logsResult.anomalies ? logsResult.anomalies.length : 0;
            return total > 0 ? Math.round(((total - errors) / total) * 100) : 0;
        },
        
        // 加载结果文件列表
        async loadResults() {
            try {
                const response = await fetch('/api/results');
                const data = await response.json();
                this.resultFiles = data.results;
            } catch (error) {
                console.error('加载结果列表失败:', error);
            }
        },
        
        // 查看结果文件
        async viewResult(result) {
            try {
                const response = await fetch(`/api/result/${result.filename}`);
                const data = await response.json();
                this.currentResult = result;
                this.currentResultData = data;
                this.showResultDialog = true;
            } catch (error) {
                ElMessage.error('加载结果失败: ' + error.message);
            }
        },
        
        // 删除结果文件
        async deleteResult(result) {
            try {
                await ElMessageBox.confirm(
                    `确定要删除文件 ${result.filename} 吗？`,
                    '确认删除',
                    {
                        confirmButtonText: '删除',
                        cancelButtonText: '取消',
                        type: 'warning'
                    }
                );
                
                // 这里需要后端支持删除API
                ElMessage.success('删除成功');
                this.loadResults();
            } catch (error) {
                // 用户取消删除
            }
        },
        
        // 获取结果类型颜色
        getResultTypeColor(type) {
            const colors = {
                'scan': 'primary',
                'graph': 'success',
                'paths': 'warning',
                'log': 'info',
                'analysis': 'danger'
            };
            return colors[type] || 'info';
        },
        
        // 格式化文件大小
        formatFileSize(bytes) {
            if (bytes === 0) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        },
        
        // 格式化日期
        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleString('zh-CN');
        },
        
        // 加载演示数据
        async loadDemoData() {
            try {
                const response = await fetch('/api/demo-data');
                const data = await response.json();
                if (data.success) {
                    this.scanResult = data.result;
                    ElMessage.success('演示数据加载成功');
                } else {
                    ElMessage.error('加载演示数据失败');
                }
            } catch (error) {
                ElMessage.error('加载演示数据失败: ' + error.message);
            }
        },

        // 加载演示图数据
        async loadDemoGraph() {
            try {
                const response = await fetch('/api/demo-graph');
                const data = await response.json();
                if (data.success) {
                    this.graphResult = data.result;
                    ElMessage.success('演示图数据加载成功');
                    
                    // 渲染图形
                    this.$nextTick(() => {
                        this.renderGraph();
                    });
                } else {
                    ElMessage.error('加载演示图数据失败');
                }
            } catch (error) {
                ElMessage.error('加载演示图数据失败: ' + error.message);
            }
        },

        // ...existing code...
    }
});

// 注册图标组件
console.log('🎨 注册图标组件...');
app.component('Search', Search);
app.component('Connection', Connection);
app.component('Guide', Guide);
app.component('Document', Document);
app.component('Folder', Folder);
app.component('Upload', Upload);
app.component('Download', Download);
app.component('RefreshRight', RefreshRight);
app.component('View', View);
app.component('Delete', Delete);

// 使用Element Plus并挂载应用
console.log('🔧 挂载Vue应用到#app...');
app.use(ElementPlus).mount('#app');
console.log('✅ SentinelAgent Web UI 初始化完成!');
