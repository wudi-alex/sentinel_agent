#!/bin/bash
# filepath: /Users/xuhe/Documents/agent_experiments/SentinelAgent/scripts/docker_build.sh
# SentinelAgent Docker构建脚本

set -e

echo "🤖 SentinelAgent Docker构建脚本"
echo "========================================"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# 检查Dockerfile是否存在
if [ ! -f "Dockerfile" ]; then
    echo "❌ 错误: 未找到Dockerfile"
    exit 1
fi

# 检查docker-compose.yml是否存在
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ 错误: 未找到docker-compose.yml"
    exit 1
fi

# 设置镜像标签
IMAGE_NAME="sentinel-agent"
VERSION="${1:-latest}"
FULL_TAG="${IMAGE_NAME}:${VERSION}"

echo "📦 构建Docker镜像: $FULL_TAG"
echo "----------------------------------------"

# 构建镜像
if docker build -t "$FULL_TAG" .; then
    echo "✅ 镜像构建成功: $FULL_TAG"
else
    echo "❌ 镜像构建失败"
    exit 1
fi

# 显示镜像信息
echo ""
echo "📋 镜像信息:"
echo "----------------------------------------"
docker images | grep "$IMAGE_NAME" | head -5

echo ""
echo "🚀 构建完成! 使用以下命令启动服务:"
echo "   docker-compose up -d"
echo "   或者直接运行:"
echo "   docker run -p 5002:5002 $FULL_TAG"
