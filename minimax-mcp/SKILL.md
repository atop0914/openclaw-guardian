---
name: minimax-mcp
description: MiniMax MCP 服务，包含 web_search（网络搜索）和 understand_image（图片理解）。使用 mcporter 调用。
allowed-tools: Bash(mcporter:*), Bash(eval:*)
---

# MiniMax MCP

使用 MiniMax Coding Plan MCP 服务进行网络搜索和图片理解。

## 前置要求

### 1. 安装 mcporter
```bash
npm install -g mcporter
```

### 2. 配置 MCP 服务器

创建配置文件 `~/.openclaw/workspace/config/mcporter.json`:

```json
{
  "mcpServers": {
    "minimax": {
      "type": "stdio",
      "command": "uvx",
      "args": ["minimax-coding-plan-mcp", "-y"],
      "env": {
        "MINIMAX_API_KEY": "你的 Minimax API Key",
        "MINIMAX_BASE_URL": "https://api.minimax.chat/v1"
      }
    }
  }
}
```

**获取 API Key**:
1. 访问 https://platform.minimaxi.cn
2. 登录后进入「API 密钥」页面
3. 创建新的 API Key

### 3. 启动 MCP 服务
```bash
mcporter daemon start
```

## 工具

### 1. web_search - 网络搜索
- 参数: `query` (搜索关键词)
- 返回: 搜索结果列表

### 2. understand_image - 图片理解
- 参数: 
  - `prompt` (问题)
  - `image_source` (图片路径或URL，支持 HTTP URL 或本地文件路径)

## 使用方式

### 使用 mcporter 直接调用

```bash
# 网络搜索
mcporter call minimax.web_search query="最新新闻"

# 图片理解
mcporter call minimax.understand_image prompt="描述这张图片" image_source="https://example.com/image.jpg"

# 图片理解（本地文件）
mcporter call minimax.understand_image prompt="这张图片有什么" image_source="/path/to/image.jpg"
```

### 使用 skill 封装脚本

```bash
# 搜索
./scripts/mcp.sh search "搜索内容"

# 图片理解
./scripts/mcp.sh image "问题" "/path/to/image.jpg"
```

## 列出可用工具

```bash
mcporter list minimax
```

或

```bash
mcporter list minimax --schema
```

## 常见问题

### Q: 提示 "Unknown MCP server"
A: 确保 MCP 服务已启动: `mcporter daemon start`

### Q: 提示 "API Key 无效"
A: 检查 `~/.openclaw/workspace/config/mcporter.json` 中的 API Key 是否正确

### Q: 如何更新 MCP 配置?
A: 修改配置文件后重启: `mcporter daemon restart`

## 文件结构

```
minimax-mcp/
├── SKILL.md          # 本文件
└── scripts/
    └── mcp.sh        # 封装脚本
```
