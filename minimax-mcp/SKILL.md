---
name: minimax-mcp
description: MiniMax MCP 服务，包含 web_search（网络搜索）和 understand_image（图片理解）。使用 mcporter 调用。
allowed-tools: Bash(mcporter:*), Bash(eval:*)
---

# MiniMax MCP

使用 MiniMax Coding Plan MCP 服务进行网络搜索和图片理解。

## 快速安装

一键自动安装（推荐）：

```bash
# 1. 安装 mcporter（如不存在）
which mcporter || npm install -g mcporter

# 2. 添加 PATH（确保 npm 全局模块可用）
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$PATH"

# 3. 启动 MCP 服务
mcporter daemon start 2>/dev/null || true

# 4. 验证
mcporter list
```

## 手动安装步骤

### 1. 安装 mcporter
```bash
npm install -g mcporter

# 确保 PATH 包含 npm 全局模块
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$PATH"
```

### 2. 配置 MCP 服务器

**方式一：使用已有配置**

如果 OpenClaw 已配置 MCP，复制配置：
```bash
mkdir -p ~/.mcporter
cp ~/.mcporter/config.json ~/.mcporter/config.json 2>/dev/null || \
cp ~/.openclaw/workspace/config/mcporter.json ~/.mcporter/config.json 2>/dev/null || true
```

**方式二：新建配置**

创建 `~/.mcporter/config.json`:

```json
{
  "mcpServers": {
    "minimax": {
      "command": "uvx",
      "args": ["minimax-coding-plan-mcp", "-y"],
      "env": {
        "MINIMAX_API_KEY": "你的API Key",
        "MINIMAX_API_HOST": "https://api.minimaxi.com"
      }
    }
  }
}
```

**获取 API Key**:
1. 访问 https://platform.minimaxi.cn
2. 登录后进入「API 密钥」页面
3. 创建新的 API Key（选择 Coding Plan 订阅）

### 3. 启动 MCP 服务
```bash
mcporter daemon start
```

## 工具

### 1. web_search - 网络搜索
- 参数: `query` (搜索关键词)
- 返回: 搜索结果列表（标题、链接、摘要、日期）

### 2. understand_image - 图片理解
- 参数: 
  - `prompt` (问题)
  - `image_source` (图片路径或URL，支持 HTTP URL 或本地文件路径)

## 使用方式

### 直接调用

```bash
# 网络搜索
mcporter call minimax.web_search query="最新新闻"

# 图片理解（URL）
mcporter call minimax.understand_image prompt="描述这张图片" image_source="https://example.com/image.jpg"

# 图片理解（本地文件）
mcporter call minimax.understand_image prompt="这张图片有什么" image_source="/path/to/image.jpg"
```

### 列出可用工具

```bash
mcporter list minimax
```

### 查看工具 schema

```bash
mcporter list minimax --schema
```

## 常见问题

### Q: 提示 "command not found: mcporter"
A: 
```bash
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$PATH"
# 或重新安装
npm install -g mcporter
```

### Q: 提示 "Unknown MCP server"
A: 确保 MCP 服务已启动: `mcporter daemon start`

### Q: 提示 "API Key 无效"
A: 检查 `~/.mcporter/config.json` 中的 API Key 是否正确

### Q: 配置后仍无法使用
A: 重启 MCP 服务: 
```bash
mcporter daemon restart
```

## 文件结构

```
minimax-mcp/
├── SKILL.md          # 本文件
└── scripts/
    └── mcp.sh        # 封装脚本（可选）
```
