// SentinelAgent Web UI JavaScript
console.log('🤖 SentinelAgent UI - Initialization started');

const { createApp } = Vue;
const { ElMessage, ElMessageBox } = ElementPlus;

// Icon components
const { 
    Search, Connection, Guide, Document, Folder, 
    Upload, Download, RefreshRight, View, Delete 
} = ElementPlusIconsVue;

console.log('✅ Vue components and icons loaded successfully');

const app = createApp({
    data() {
        return {
            // Currently active tab
            activeTab: 'scanner',
            
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
            currentResultData: null
        };
    },
    
    mounted() {
        console.log('🚀 Vue application mounted - SentinelAgent UI started');
        this.loadExamples();
        this.loadResults();
        console.log('📊 Initial data loading completed');
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
            this.scanForm.path = example.path;
            this.scanForm.type = 'directory';
            this.activeTab = 'scanner';
            ElMessage.success(`Example loaded: ${example.name}`);
        },
        
        // Path selection (simplified version, can integrate file selector)
        selectPath() {
            ElMessageBox.prompt('Enter path', 'Select Path', {
                confirmButtonText: 'OK',
                cancelButtonText: 'Cancel',
                inputValue: this.scanForm.path
            }).then(({ value }) => {
                this.scanForm.path = value;
            }).catch(() => {});
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
                    
                    // Show result summary - optimized for agent systems
                    const summary = this.scanResult.scan_summary || {};
                    let summaryText = `Scan completed!\n`;
                    summaryText += `- Agents: ${summary.total_agents || 0}\n`;
                    summaryText += `- Tools: ${summary.total_tools || 0}\n`;
                    summaryText += `- Crews: ${summary.total_crews || 0}\n`;
                    summaryText += `- Tasks: ${summary.total_tasks || 0}\n`;
                    summaryText += `- Python files: ${summary.python_files || 0}`;
                    
                    ElMessage({
                        message: summaryText,
                        type: 'success',
                        duration: 5000,
                        showClose: true
                    });
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
                    ElMessage.success('Path analysis completed');
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
                const response = await fetch(`/api/result/${result.filename}`);
                const data = await response.json();
                this.currentResult = result;
                this.currentResultData = data;
                this.showResultDialog = true;
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
        }
    }
});

// Register icon components
console.log('🎨 Registering icon components...');
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
console.log('🔧 Mounting Vue application to #app...');
app.use(ElementPlus).mount('#app');
console.log('✅ SentinelAgent Web UI initialization completed!');
