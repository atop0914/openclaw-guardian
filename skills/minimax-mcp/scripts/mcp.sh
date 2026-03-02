#!/bin/bash
# MiniMax MCP 工具封装

SERVER="minimax"
CONFIG_FILE="$HOME/.openclaw/workspace/config/mcporter.json"

# 检查配置
if [ ! -f "$CONFIG_FILE" ]; then
    echo "错误: 配置文件不存在 $CONFIG_FILE"
    exit 1
fi

# 解析命令
COMMAND=$1
shift

case "$COMMAND" in
    search|web_search)
        if [ -z "$1" ]; then
            echo "用法: $0 search <搜索内容>"
            exit 1
        fi
        mcporter call $SERVER.web_search query="$1"
        ;;
    image|understand_image)
        if [ -z "$1" ] || [ -z "$2" ]; then
            echo "用法: $0 image <问题> <图片路径或URL>"
            exit 1
        fi
        mcporter call $SERVER.understand_image prompt="$1" image_source="$2"
        ;;
    list)
        mcporter list
        ;;
    *)
        echo "MiniMax MCP 工具"
        echo ""
        echo "用法:"
        echo "  $0 search <内容>    - 网络搜索"
        echo "  $0 image <问题> <图片> - 图片理解"
        echo "  $0 list            - 列出可用工具"
        ;;
esac
