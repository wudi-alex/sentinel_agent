# SentinelAgent Docker Deployment Guide

## Overview
SentinelAgent has been successfully dockerized with a multi-stage build approach for optimal image size and security.

## Quick Start

### Option 1: Docker Compose (Recommended)
```bash
# Start the application
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Option 2: Direct Docker Run
```bash
# Build the image
docker build -t sentinel-agent:latest .

# Run the container
docker run -d -p 5002:5002 --name sentinel-agent sentinel-agent:latest

# Check logs
docker logs -f sentinel-agent

# Stop the container
docker stop sentinel-agent && docker rm sentinel-agent
```

## Features

### Docker Configuration
- **Multi-stage build**: Optimized for size and security
- **Non-root user**: Runs as `appuser` for security
- **Health checks**: Built-in health monitoring
- **Persistent storage**: Data and logs are preserved across restarts
- **Production ready**: Uses production Flask settings

### Persistent Volumes
- `sentinel_data`: Application data storage
- `sentinel_logs`: Application logs storage
- `examples`: Read-only examples directory

### Health Monitoring
The application includes a health endpoint at `/health` that returns:
```json
{
  "service": "SentinelAgent Web UI",
  "status": "healthy",
  "timestamp": "2025-05-31T19:28:07.419211",
  "uptime": "running",
  "version": "1.0.0"
}
```

## Image Details
- **Base Image**: python:3.11-slim
- **Final Size**: ~1.2GB
- **Security**: Non-root user execution
- **Port**: 5002 (configurable)

## Environment Variables
- `PYTHONUNBUFFERED=1`: Enable real-time log output
- `FLASK_ENV=production`: Production mode
- `FLASK_DEBUG=false`: Disable debug mode
- `SENTINEL_DATA_DIR=/app/data`: Data directory
- `SENTINEL_LOG_LEVEL=INFO`: Logging level

## Access
Once running, access the application at:
- **Web UI**: http://localhost:5002
- **Health Check**: http://localhost:5002/health

## Build Script
Use the provided build script for automated builds:
```bash
./scripts/docker_build.sh
```

## Network Configuration
- **Network**: `sentinel-network` (bridge)
- **Port Mapping**: 5002:5002
- **Container Name**: `sentinel-agent`

## Future Enhancements
The docker-compose.yml includes commented configurations for:
- Redis caching
- PostgreSQL database
- Additional services integration

## Troubleshooting

### Common Issues
1. **Port already in use**: Change the host port in docker-compose.yml
2. **Permission issues**: Ensure Docker daemon is running
3. **Build failures**: Check system resources and network connectivity

### Logs
```bash
# Docker Compose logs
docker-compose logs sentinel-agent

# Direct Docker logs
docker logs sentinel-agent
```

### Debugging
```bash
# Enter the container
docker exec -it sentinel-agent /bin/bash

# Check processes
docker exec sentinel-agent ps aux
```

## Production Deployment

For production deployment, consider:
1. Using a reverse proxy (nginx/traefik)
2. Enabling SSL/TLS
3. Setting up log aggregation
4. Implementing monitoring and alerting
5. Database persistence (PostgreSQL/Redis)

## Security Notes
- Application runs as non-root user
- Minimal base image with only necessary packages
- No sensitive data in image layers
- Health checks prevent unhealthy container deployment
