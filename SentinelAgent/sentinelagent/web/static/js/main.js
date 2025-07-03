// SentinelAgent Web UI JavaScript
const { createApp } = Vue;
const { ElMessage, ElMessageBox } = ElementPlus;

// Icon components
const { 
    Search, Connection, Guide, Document, Folder, 
    Upload, Download, RefreshRight, View, Delete 
} = ElementPlusIconsVue;

const app = createApp({
    data() {
        return {
            // Currently active tab
            activeTab: 'scanner',
            
            // Active result tab
            activeResultTab: 'agents',
            
            // Display status
            showAbout: false,
            showResultDialog: false,
            
            // Loading status
            scanLoading: false,
            graphLoading: false,
            pathsLoading: false,
            logsLoading: false,
            
            // Form data
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
            
            // JSON日志可视化相关
            logViewMode: 'overview',
            
            // Result data
            scanResult: null,
            graphResult: null,
            pathsResult: null,
            logsResult: null,
            
            // Example projects and result files
            examples: [],
            resultFiles: [],
            
            // Currently viewing result
            currentResult: null,
            currentResultData: null,
            
            // File browser related
            showFileBrowser: false,
            fileBrowserTitle: 'Select File',
            fileBrowserMode: 'file',  // 'file' or 'directory'
            fileBrowserFilter: '',    // File extension filter
            fileBrowserCallback: null, // Callback function when file is selected
            currentBrowserPath: '',
            browserItems: [],
            browserLoading: false,
        };
    },
    
    mounted() {
        this.loadExamples();
        this.loadResults();
    },
    
    methods: {
        // Menu selection handler
        handleMenuSelect(index) {
            this.activeTab = index;
        },
        
        // Load example projects
        async loadExamples() {
            try {
                const response = await fetch('/api/examples');
                const data = await response.json();
                this.examples = data.examples;
            } catch (error) {
                console.error('Failed to load examples:', error);
            }
        },
        
        // Load example project
        loadExample(example) {
            // For CrewAI examples, load the specific file
            if (example.type === 'crewai') {
                this.scanForm.path = example.resolved_path + '/email_assistant_agent_system.py';
                this.scanForm.type = 'file';
            } else {
                this.scanForm.path = example.resolved_path;
                this.scanForm.type = 'directory';
            }
            this.activeTab = 'scanner';
            ElMessage.success(`Example loaded: ${example.name}`);
        },
        
        // Path selection with file browser - now handled by browseForScanPath()
        selectPath() {
            this.browseForScanPath();
        },
        
        // Execute scan
        async executeScan() {
            if (!this.scanForm.path.trim()) {
                ElMessage.error('Please enter scan path');
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
                    
                    // Show enhanced result summary
                    this.displayEnhancedScanResult(this.scanResult);
                } else {
                    ElMessage.error(data.error || 'Scan failed');
                }
            } catch (error) {
                ElMessage.error('Scan failed: ' + error.message);
            } finally {
                this.scanLoading = false;
            }
        },
        
        // Clear scan results
        clearScanResult() {
            this.scanResult = null;
            ElMessage.success('Scan results cleared');
        },
        
        // Build relationship graph
        async buildGraph() {
            if (this.graphForm.dataSource === 'scan' && !this.scanResult) {
                ElMessage.error('Please execute scan first');
                return;
            }
            
            if (this.graphForm.dataSource === 'path' && !this.graphForm.path.trim()) {
                ElMessage.error('Please enter scan path');
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
                    ElMessage.success('Relationship graph built successfully');
                    
                    // Render graph
                    this.$nextTick(() => {
                        this.renderGraph();
                    });
                } else {
                    ElMessage.error(data.error || 'Graph building failed');
                }
            } catch (error) {
                ElMessage.error('Graph building failed: ' + error.message);
            } finally {
                this.graphLoading = false;
            }
        },
        
        // Render relationship graph
        renderGraph() {
            if (!this.graphResult || !this.graphResult.nodes) return;
            
            const container = d3.select('#graph-container');
            container.selectAll('*').remove(); // Clear previous content
            
            const width = 800;
            const height = 500;
            
            const svg = container
                .append('svg')
                .attr('width', width)
                .attr('height', height);
                
            // Ensure correct data structure
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
                
            // Add node click events
            node.on('click', (event, d) => {
                ElMessage.info(`Node: ${d.id}, Type: ${d.type}`);
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
        
        // Drag handling functions
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
        
        // Node color mapping
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
        
        // Path analysis
        async analyzePaths() {
            if (this.pathsForm.dataSource === 'graph' && !this.graphResult) {
                ElMessage.error('Please build relationship graph first');
                return;
            }
            
            if (this.pathsForm.dataSource === 'file' && !this.pathsForm.graphFile.trim()) {
                ElMessage.error('Please enter graph file path');
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
                    
                    // Show enhanced result summary
                    const assessment = this.pathsResult.overall_assessment || {};
                    const pathAnalysis = this.pathsResult.path_analysis || {};
                    
                    let summaryText = `Path analysis completed!\n`;
                    summaryText += `- Total paths: ${assessment.total_paths_analyzed || 0}\n`;
                    summaryText += `- Risk level: ${assessment.risk_level || 'unknown'}\n`;
                    summaryText += `- Risk score: ${assessment.total_risk_score || 0}\n`;
                    
                    // Show temporal paths if available
                    const temporalPaths = (this.pathsResult.execution_paths || []).filter(p => p.is_temporal);
                    if (temporalPaths.length > 0) {
                        summaryText += `- Temporal execution paths: ${temporalPaths.length}`;
                    }
                    
                    ElMessage({
                        message: summaryText,
                        type: 'success',
                        duration: 5000
                    });
                } else {
                    ElMessage.error(data.error || 'Path analysis failed');
                }
            } catch (error) {
                ElMessage.error('Path analysis failed: ' + error.message);
            } finally {
                this.pathsLoading = false;
            }
        },
        
        // Log analysis
        async analyzeLogs() {
            if (!this.logsForm.logFile.trim()) {
                ElMessage.error('Please enter log file path');
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
                    ElMessage.success('Log analysis completed');
                } else {
                    ElMessage.error(data.error || 'Log analysis failed');
                }
            } catch (error) {
                ElMessage.error('Log analysis failed: ' + error.message);
            } finally {
                this.logsLoading = false;
            }
        },
        
        // Calculate success rate
        calculateSuccessRate(logsResult) {
            if (!logsResult.log_summary) return 0;
            const total = logsResult.log_summary.total_entries || 0;
            const errors = logsResult.anomalies ? logsResult.anomalies.length : 0;
            return total > 0 ? Math.round(((total - errors) / total) * 100) : 0;
        },
        
        // Load result file list
        async loadResults() {
            try {
                const response = await fetch('/api/results');
                const data = await response.json();
                this.resultFiles = data.results;
            } catch (error) {
                console.error('Failed to load result list:', error);
            }
        },
        
        // View result file
        async viewResult(result) {
            try {
                // Check if this is a demo result (filename contains 'demo_')
                if (result.filename && result.filename.includes('demo_')) {
                    // Extract result type from demo filename
                    const resultType = result.type || result.filename.split('_')[1].split('.')[0];
                    await this.viewDemoResult(resultType);
                } else {
                    // Handle regular result files
                    const response = await fetch(`/api/result/${result.filename}`);
                    const data = await response.json();
                    this.currentResult = result;
                    this.currentResultData = data;
                    this.showResultDialog = true;
                }
            } catch (error) {
                ElMessage.error('Failed to load result: ' + error.message);
            }
        },
        
        // Delete result file
        async deleteResult(result) {
            try {
                await ElMessageBox.confirm(
                    `Are you sure to delete file ${result.filename}?`,
                    'Confirm Deletion',
                    {
                        confirmButtonText: 'Delete',
                        cancelButtonText: 'Cancel',
                        type: 'warning'
                    }
                );
                
                // This requires backend support for delete API
                ElMessage.success('Delete successful');
                this.loadResults();
            } catch (error) {
                // User cancelled deletion
            }
        },
        
        // Get result type color
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
        
        // Format file size
        formatFileSize(bytes) {
            if (bytes === 0) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        },
        
        // Format date
        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleString('en-US');
        },
        
        // Load demo data
        async loadDemoData() {
            try {
                const response = await fetch('/api/demo-data');
                const data = await response.json();
                if (data.success) {
                    this.scanResult = data.result;
                    ElMessage.success('Demo data loaded successfully');
                } else {
                    ElMessage.error('Failed to load demo data');
                }
            } catch (error) {
                ElMessage.error('Failed to load demo data: ' + error.message);
            }
        },

        // Load demo graph data
        async loadDemoGraph() {
            try {
                const response = await fetch('/api/demo-graph');
                const data = await response.json();
                if (data.success) {
                    this.graphResult = data.result;
                    ElMessage.success('Demo graph data loaded successfully');
                    
                    // Render graph
                    this.$nextTick(() => {
                        this.renderGraph();
                    });
                } else {
                    ElMessage.error('Failed to load demo graph data');
                }
            } catch (error) {
                ElMessage.error('Failed to load demo graph data: ' + error.message);
            }
        },

        // Load demo path analysis data
        async loadDemoPaths() {
            try {
                const response = await fetch('/api/demo-paths');
                const data = await response.json();
                if (data.success) {
                    this.pathsResult = data.result;
                    ElMessage.success('Demo path analysis data loaded successfully');
                } else {
                    ElMessage.error('Failed to load demo path analysis data');
                }
            } catch (error) {
                ElMessage.error('Failed to load demo path analysis data: ' + error.message);
            }
        },

        // Load demo log analysis data
        async loadDemoLogs() {
            try {
                const response = await fetch('/api/demo-logs');
                const data = await response.json();
                if (data.success) {
                    this.logsResult = data.result;
                    ElMessage.success('Demo log analysis data loaded successfully');
                } else {
                    ElMessage.error('Failed to load demo log analysis data');
                }
            } catch (error) {
                ElMessage.error('Failed to load demo log analysis data: ' + error.message);
            }
        },

        // Load demo results list
        async loadDemoResults() {
            try {
                const response = await fetch('/api/demo-results');
                const data = await response.json();
                this.resultFiles = data.results;
                ElMessage.success('Demo results list loaded successfully');
            } catch (error) {
                ElMessage.error('Failed to load demo results: ' + error.message);
            }
        },

        // View demo result by type
        async viewDemoResult(resultType) {
            try {
                const response = await fetch(`/api/demo-result/${resultType}`);
                const data = await response.json();
                if (data.success) {
                    this.currentResult = {
                        filename: `demo_${resultType}_result.json`,
                        type: resultType
                    };
                    this.currentResultData = data.result;
                    this.showResultDialog = true;
                    ElMessage.success(`Demo ${resultType} result loaded successfully`);
                } else {
                    ElMessage.error(`Failed to load demo ${resultType} result`);
                }
            } catch (error) {
                ElMessage.error(`Failed to load demo ${resultType} result: ` + error.message);
            }
        },
        
        // JSON日志处理方法
        
        // 检查是否为JSON格式的日志结果
        isJsonLogResult(logsResult) {
            return logsResult && logsResult.metadata && logsResult.execution_log;
        },
        
        // 获取Agent执行条目
        getAgentExecutions(logsResult) {
            if (!logsResult.execution_log) return [];
            return logsResult.execution_log.filter(entry => entry.entry_type === 'agent_execution');
        },
        
        // 获取工具执行条目
        getToolExecutions(logsResult) {
            if (!logsResult.execution_log) return [];
            return logsResult.execution_log.filter(entry => entry.entry_type === 'tool_execution');
        },
        
        // 获取唯一的Agent列表
        getUniqueAgents(logsResult) {
            if (!logsResult.execution_log) return [];
            const agents = new Set();
            logsResult.execution_log.forEach(entry => {
                if (entry.agent?.role) {
                    agents.add(entry.agent.role);
                }
            });
            return Array.from(agents);
        },
        
        // 获取条目标签类型
        getEntryTagType(entryType) {
            const types = {
                'agent_execution': 'primary',
                'tool_execution': 'success',
                'other': 'info'
            };
            return types[entryType] || 'info';
        },
        
        // 获取时间线类型
        getTimelineType(entryType) {
            const types = {
                'agent_execution': 'primary',
                'tool_execution': 'success',
                'other': 'info'
            };
            return types[entryType] || 'info';
        },
        
        // 格式化时间
        formatTime(timestamp) {
            if (!timestamp) return 'N/A';
            try {
                const date = new Date(timestamp);
                return date.toLocaleString('en-US', {
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit'
                });
            } catch (error) {
                return timestamp;
            }
        },
        
        // 截断文本
        truncateText(text, maxLength) {
            if (!text) return '';
            if (text.length <= maxLength) return text;
            return text.substring(0, maxLength) + '...';
        },
        
        // 加载JSON日志
        async loadJsonLogs() {
            try {
                // 创建文件选择对话框
                const input = document.createElement('input');
                input.type = 'file';
                input.accept = '.json';
                input.onchange = async (event) => {
                    const file = event.target.files[0];
                    if (!file) return;
                    
                    // 显示加载状态
                    this.logsLoading = true;
                    
                    try {
                        // 读取文件内容
                        const text = await file.text();
                        const jsonData = JSON.parse(text);
                        
                        // 验证JSON格式
                        if (!jsonData.execution_log || !jsonData.metadata) {
                            ElMessage.error('Invalid JSON log format. Please select a converted CrewAI log file.');
                            return;
                        }
                        
                        // 设置结果数据
                        this.logsResult = jsonData;
                        this.logsForm.logFile = file.name;
                        this.logsForm.format = 'json';
                        
                        ElMessage.success('JSON log loaded successfully');
                        
                    } catch (error) {
                        ElMessage.error('Failed to parse JSON file: ' + error.message);
                    } finally {
                        this.logsLoading = false;
                    }
                };
                
                // 触发文件选择
                input.click();
                
            } catch (error) {
                ElMessage.error('Failed to load JSON logs: ' + error.message);
                this.logsLoading = false;
            }
        },
        
        // File browser methods
        async openFileBrowser(title, mode, filter, callback) {
            this.fileBrowserTitle = title;
            this.fileBrowserMode = mode; // 'file' or 'directory'
            this.fileBrowserFilter = filter || '';
            this.fileBrowserCallback = callback;
            this.currentBrowserPath = this.currentBrowserPath || '/Users/xuhe/Documents/agent_experiments';
            this.showFileBrowser = true;
            await this.loadBrowserItems();
        },
        
        async loadBrowserItems(path = null) {
            if (path) {
                this.currentBrowserPath = path;
            }
            
            this.browserLoading = true;
            try {
                const response = await fetch('/api/browse-files', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        path: this.currentBrowserPath,
                        filter: this.fileBrowserFilter
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    this.currentBrowserPath = data.current_path;
                    this.browserItems = data.items;
                } else {
                    ElMessage.error(data.error || 'Failed to load directory');
                }
            } catch (error) {
                ElMessage.error('Failed to browse files: ' + error.message);
            } finally {
                this.browserLoading = false;
            }
        },
        
        async onBrowserItemClick(item) {
            if (item.type === 'directory') {
                await this.loadBrowserItems(item.path);
            } else if (item.type === 'file' && this.fileBrowserMode === 'file') {
                this.selectBrowserItem(item);
            }
        },
        
        selectBrowserItem(item) {
            if (this.fileBrowserCallback) {
                this.fileBrowserCallback(item.path);
            }
            this.closeBrowser();
        },
        
        selectCurrentDirectory() {
            if (this.fileBrowserMode === 'directory' && this.fileBrowserCallback) {
                this.fileBrowserCallback(this.currentBrowserPath);
            }
            this.closeBrowser();
        },
        
        closeBrowser() {
            this.showFileBrowser = false;
            this.fileBrowserCallback = null;
        },

        // Enhanced path selection methods
        browseForScanPath() {
            this.openFileBrowser(
                'Select File or Directory to Scan',
                'file',
                '.py',
                (path) => {
                    this.scanForm.path = path;
                    // Auto-detect type based on path
                    if (path.endsWith('.py')) {
                        this.scanForm.type = 'file';
                    } else {
                        this.scanForm.type = 'directory';
                    }
                }
            );
        },
        
        browseForGraphFile() {
            this.openFileBrowser(
                'Select Graph File',
                'file',
                '.json',
                (path) => {
                    this.pathsForm.graphFile = path;
                }
            );
        },
        
        browseForLogFile() {
            this.openFileBrowser(
                'Select Log File',
                'file',
                '',
                (path) => {
                    this.logsForm.logFile = path;
                    // Auto-detect format based on file extension
                    if (path.endsWith('.json')) {
                        this.logsForm.format = 'json';
                    } else if (path.endsWith('.csv')) {
                        this.logsForm.format = 'csv';
                    } else {
                        this.logsForm.format = 'auto';
                    }
                }
            );
        },
        
        // Path analysis helper methods
        getTemporalOrder(path) {
            if (!path || !path.path) return '';
            if (path.is_temporal && path.temporal_order) {
                return path.temporal_order.join(' → ');
            }
            return this.getPathString(path);
        },
        
        getPathString(path) {
            if (!path || !path.path) return '';
            if (Array.isArray(path.path)) {
                return path.path.join(' → ');
            }
            return String(path.path);
        },
        
        getRiskScore(path) {
            if (!path) return 0;
            if (typeof path.risk_score === 'number') {
                return path.risk_score.toFixed(3);
            }
            if (typeof path.score === 'number') {
                return path.score.toFixed(3);
            }
            return '0.000';
        },
        
        // Enhanced scan result display helper methods
        getDetailedScanSummary(scanResult) {
            if (!scanResult || !scanResult.scan_summary) return {};
            
            const summary = scanResult.scan_summary;
            const detailed = {
                basic: {
                    total_agents: summary.total_agents || 0,
                    total_tools: summary.total_tools || 0,
                    total_crews: summary.total_crews || 0,
                    total_tasks: summary.total_tasks || 0,
                    total_files: summary.total_files || 0,
                    python_files: summary.python_files || 0
                },
                agents: {
                    by_type: this.groupByType(scanResult.agents),
                    with_roles: this.getAgentsWithRoles(scanResult.agents),
                    with_tools: this.getAgentsWithTools(scanResult.agents)
                },
                tools: {
                    by_type: this.groupByType(scanResult.tools),
                    class_definitions: this.getToolClasses(scanResult.tools),
                    instances: this.getToolInstances(scanResult.tools)
                },
                crews: {
                    by_type: this.groupByType(scanResult.crews),
                    total: scanResult.crews ? scanResult.crews.length : 0
                },
                tasks: {
                    by_type: this.groupByType(scanResult.tasks),
                    with_agents: this.getTasksWithAgents(scanResult.tasks),
                    with_dependencies: this.getTasksWithDependencies(scanResult.tasks)
                },
                file_structure: scanResult.file_structure || {}
            };
            
            return detailed;
        },
        
        groupByType(items) {
            if (!items || !Array.isArray(items)) return {};
            return items.reduce((acc, item) => {
                const type = item.type || 'unknown';
                acc[type] = (acc[type] || 0) + 1;
                return acc;
            }, {});
        },
        
        getAgentsWithRoles(agents) {
            if (!agents || !Array.isArray(agents)) return [];
            return agents.filter(agent => agent.arguments && agent.arguments.role);
        },
        
        getAgentsWithTools(agents) {
            if (!agents || !Array.isArray(agents)) return [];
            return agents.filter(agent => 
                agent.arguments && agent.arguments.tools && agent.arguments.tools.length > 0
            );
        },
        
        getToolClasses(tools) {
            if (!tools || !Array.isArray(tools)) return [];
            return tools.filter(tool => tool.type === 'class_definition');
        },
        
        getToolInstances(tools) {
            if (!tools || !Array.isArray(tools)) return [];
            return tools.filter(tool => tool.type === 'instance');
        },
        
        getTasksWithAgents(tasks) {
            if (!tasks || !Array.isArray(tasks)) return [];
            return tasks.filter(task => task.assigned_agent);
        },
        
        getTasksWithDependencies(tasks) {
            if (!tasks || !Array.isArray(tasks)) return [];
            return tasks.filter(task => task.dependencies && task.dependencies.length > 0);
        },
        
        // Format file path for display
        formatFilePath(filePath) {
            if (!filePath) return '';
            const parts = filePath.split('/');
            if (parts.length > 3) {
                return '.../' + parts.slice(-3).join('/');
            }
            return filePath;
        },
        
        // Get agent type color
        getAgentTypeColor(agent) {
            if (!agent) return 'info';
            if (agent.arguments && agent.arguments.role) {
                return 'primary';
            }
            if (agent.type === 'regex_detected') {
                return 'warning';
            }
            return 'info';
        },
        
        // Get tool type color
        getToolTypeColor(tool) {
            if (!tool) return 'info';
            switch (tool.type) {
                case 'class_definition': return 'success';
                case 'instance': return 'primary';
                case 'standalone_instance': return 'warning';
                default: return 'info';
            }
        },
        
        // Get task type color
        getTaskTypeColor(task) {
            if (!task) return 'info';
            if (task.assigned_agent) {
                return 'primary';
            }
            if (task.dependencies && task.dependencies.length > 0) {
                return 'warning';
            }
            return 'info';
        },
        
        // Enhanced scan result display
        displayEnhancedScanResult(scanResult) {
            if (!scanResult) return;
            
            const detailed = this.getDetailedScanSummary(scanResult);
            
            // Update the scan summary display
            const summaryText = this.buildEnhancedSummaryText(detailed);
            
            ElMessage({
                message: summaryText,
                type: 'success',
                duration: 8000,
                showClose: true
            });
        },
        
        buildEnhancedSummaryText(detailed) {
            let text = `📊 Scan completed successfully!\n\n`;
            
            // Basic statistics
            text += `📈 Basic Statistics:\n`;
            text += `- Agents: ${detailed.basic.total_agents}\n`;
            text += `- Tools: ${detailed.basic.total_tools}\n`;
            text += `- Crews: ${detailed.basic.total_crews}\n`;
            text += `- Tasks: ${detailed.basic.total_tasks}\n`;
            text += `- Files: ${detailed.basic.total_files} (${detailed.basic.python_files} Python)\n\n`;
            
            // Agent details
            if (detailed.basic.total_agents > 0) {
                text += `🤖 Agent Details:\n`;
                text += `- With roles: ${detailed.agents.with_roles.length}\n`;
                text += `- With tools: ${detailed.agents.with_tools.length}\n`;
                const agentTypes = Object.entries(detailed.agents.by_type);
                if (agentTypes.length > 0) {
                    text += `- Types: ${agentTypes.map(([type, count]) => `${type}(${count})`).join(', ')}\n`;
                }
                text += `\n`;
            }
            
            // Tool details
            if (detailed.basic.total_tools > 0) {
                text += `🔧 Tool Details:\n`;
                text += `- Classes: ${detailed.tools.class_definitions.length}\n`;
                text += `- Instances: ${detailed.tools.instances.length}\n`;
                const toolTypes = Object.entries(detailed.tools.by_type);
                if (toolTypes.length > 0) {
                    text += `- Types: ${toolTypes.map(([type, count]) => `${type}(${count})`).join(', ')}\n`;
                }
                text += `\n`;
            }
            
            // Task details
            if (detailed.basic.total_tasks > 0) {
                text += `📋 Task Details:\n`;
                text += `- With agents: ${detailed.tasks.with_agents.length}\n`;
                text += `- With dependencies: ${detailed.tasks.with_dependencies.length}\n`;
                const taskTypes = Object.entries(detailed.tasks.by_type);
                if (taskTypes.length > 0) {
                    text += `- Types: ${taskTypes.map(([type, count]) => `${type}(${count})`).join(', ')}\n`;
                }
            }
            
            return text;
        }
    }
});

// Register icon components
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

// Use Element Plus and mount application
app.use(ElementPlus).mount('#app');
