# SentinelAgent Docker部署指南

本指南介绍如何使用Docker部署SentinelAgent系统。

## 🛠️ 环境要求

- Docker >= 20.10
- Docker Compose >= 1.29
- 内存: 至少512MB
- 磁盘空间: 至少2GB

## 🚀 快速开始

### 1. 克隆或准备项目
```bash
# 确保在SentinelAgent项目根目录
cd /path/to/SentinelAgent
```

### 2. 配置环境变量
```bash
# 复制环境配置示例
cp .env.example .env

# 编辑配置文件 (可选)
nano .env
```

### 3. 构建和启动服务
```bash
# 构建Docker镜像
./scripts/docker_build.sh

# 启动服务
./scripts/docker_deploy.sh start
```

### 4. 访问应用
打开浏览器访问: http://localhost:5002

## 📋 管理命令

### 服务管理
```bash
# 启动服务
./scripts/docker_deploy.sh start

# 停止服务
./scripts/docker_deploy.sh stop

# 重启服务
./scripts/docker_deploy.sh restart

# 查看状态
./scripts/docker_deploy.sh status
```

### 日志查看
```bash
# 查看最近100行日志
./scripts/docker_deploy.sh logs

# 实时跟踪日志
./scripts/docker_deploy.sh logs -f
```

### 清理资源
```bash
# 清理所有相关Docker资源
./scripts/docker_deploy.sh clean
```

## 🔧 手动Docker命令

### 使用docker-compose
```bash
# 后台启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f sentinel-agent

# 停止服务
docker-compose down

# 重新构建并启动
docker-compose up -d --build
```

### 使用docker直接运行
```bash
# 构建镜像
docker build -t sentinel-agent .

# 运行容器
docker run -d \
  --name sentinel-agent \
  -p 5002:5002 \
  -v sentinel_data:/app/data \
  -v sentinel_logs:/app/logs \
  sentinel-agent

# 查看容器状态
docker ps

# 查看容器日志
docker logs -f sentinel-agent

# 停止容器
docker stop sentinel-agent

# 删除容器
docker rm sentinel-agent
```

## 🔍 健康检查

系统提供了健康检查端点:
```bash
# 检查服务健康状态
curl http://localhost:5002/health

# 预期响应
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "service": "SentinelAgent Web UI",
  "version": "1.0.0",
  "uptime": "running"
}
```

## 💾 数据持久化

### 卷挂载
- `sentinel_data`: 应用数据存储 (`/app/data`)
- `sentinel_logs`: 日志文件存储 (`/app/logs`)

### 备份数据
```bash
# 备份数据卷
docker run --rm -v sentinel_data:/data -v $(pwd):/backup alpine tar czf /backup/sentinel_data_backup.tar.gz -C /data .

# 恢复数据卷
docker run --rm -v sentinel_data:/data -v $(pwd):/backup alpine tar xzf /backup/sentinel_data_backup.tar.gz -C /data
```

## 🔧 自定义配置

### 环境变量配置
在`.env`文件中设置:
```env
FLASK_ENV=production
FLASK_HOST=0.0.0.0
FLASK_PORT=5002
SENTINEL_LOG_LEVEL=INFO
SECRET_KEY=your-secret-key
```

### 端口配置
修改`docker-compose.yml`中的端口映射:
```yaml
services:
  sentinel-agent:
    ports:
      - "8080:5002"  # 将服务映射到主机的8080端口
```

### 资源限制
在`docker-compose.yml`中添加资源限制:
```yaml
services:
  sentinel-agent:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

## 🛡️ 安全建议

### 生产环境部署
1. **更改默认密钥**: 在`.env`文件中设置强密码
2. **使用HTTPS**: 在反向代理中配置SSL证书
3. **网络隔离**: 使用Docker网络隔离服务
4. **定期更新**: 定期更新Docker镜像和依赖

### 防火墙配置
```bash
# 仅允许来自特定IP的访问
sudo ufw allow from 192.168.1.0/24 to any port 5002

# 或者使用反向代理 (推荐)
sudo ufw allow 80
sudo ufw allow 443
```

## 🐛 故障排除

### 常见问题

#### 1. 端口被占用
```bash
# 检查端口占用
sudo netstat -tlnp | grep 5002

# 停止占用端口的进程
sudo kill -9 <PID>
```

#### 2. 权限问题
```bash
# 确保用户有Docker权限
sudo usermod -aG docker $USER
newgrp docker
```

#### 3. 内存不足
```bash
# 检查系统资源
docker system df
docker stats

# 清理未使用的资源
docker system prune -f
```

#### 4. 容器无法启动
```bash
# 查看详细错误信息
docker-compose logs sentinel-agent

# 检查配置文件
docker-compose config
```

### 日志位置
- 容器内日志: `/app/logs/`
- Docker日志: `docker logs sentinel-agent`
- 系统日志: `/var/log/docker/`

## 📚 更多资源

- [Docker官方文档](https://docs.docker.com/)
- [Docker Compose文档](https://docs.docker.com/compose/)
- [SentinelAgent项目文档](../README.md)
- [快速开始指南](QUICK_START.md)
