#!/bin/bash
# filepath: /Users/xuhe/Documents/agent_experiments/SentinelAgent/scripts/docker_deploy.sh
# SentinelAgent Docker部署脚本

set -e

echo "🚀 SentinelAgent Docker部署脚本"
echo "========================================"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

# 检查Docker和docker-compose是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: Docker未安装"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ 错误: docker-compose未安装"
    exit 1
fi

# 函数定义
show_usage() {
    echo "用法: $0 [命令] [选项]"
    echo ""
    echo "命令:"
    echo "  start    启动服务 (默认)"
    echo "  stop     停止服务"
    echo "  restart  重启服务"
    echo "  logs     查看日志"
    echo "  status   查看状态"
    echo "  clean    清理资源"
    echo ""
    echo "选项:"
    echo "  -d, --detach    后台运行 (默认)"
    echo "  -f, --follow    跟踪日志输出"
    echo "  --build         强制重新构建镜像"
}

# 解析命令行参数
COMMAND="${1:-start}"
DETACH=true
FOLLOW=false
BUILD_FLAG=""

shift || true
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--detach)
            DETACH=true
            shift
            ;;
        -f|--follow)
            FOLLOW=true
            shift
            ;;
        --build)
            BUILD_FLAG="--build"
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            echo "❌ 未知选项: $1"
            show_usage
            exit 1
            ;;
    esac
done

# 执行命令
case $COMMAND in
    start)
        echo "🚀 启动SentinelAgent服务..."
        if [ "$DETACH" = true ]; then
            docker-compose up -d $BUILD_FLAG
            echo "✅ 服务已在后台启动"
            echo "🌐 Web界面地址: http://localhost:5002"
            echo "📊 查看日志: $0 logs"
            echo "📋 查看状态: $0 status"
        else
            docker-compose up $BUILD_FLAG
        fi
        ;;
    stop)
        echo "🛑 停止SentinelAgent服务..."
        docker-compose down
        echo "✅ 服务已停止"
        ;;
    restart)
        echo "🔄 重启SentinelAgent服务..."
        docker-compose down
        docker-compose up -d $BUILD_FLAG
        echo "✅ 服务已重启"
        echo "🌐 Web界面地址: http://localhost:5002"
        ;;
    logs)
        echo "📊 显示服务日志..."
        if [ "$FOLLOW" = true ]; then
            docker-compose logs -f
        else
            docker-compose logs --tail=100
        fi
        ;;
    status)
        echo "📋 服务状态:"
        echo "----------------------------------------"
        docker-compose ps
        echo ""
        echo "📊 容器资源使用:"
        echo "----------------------------------------"
        docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}" $(docker-compose ps -q) 2>/dev/null || echo "无运行中的容器"
        ;;
    clean)
        echo "🧹 清理Docker资源..."
        read -p "确定要清理所有SentinelAgent相关的Docker资源吗? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose down -v --rmi all
            docker system prune -f
            echo "✅ 清理完成"
        else
            echo "❌ 已取消清理操作"
        fi
        ;;
    *)
        echo "❌ 未知命令: $COMMAND"
        show_usage
        exit 1
        ;;
esac
