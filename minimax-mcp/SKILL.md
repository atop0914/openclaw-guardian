---
name: minimax-mcp
description: MiniMax MCP 服务，包含 web_search（网络搜索）和 understand_image（图片理解）。使用 mcporter 调用。
---

# MiniMax MCP

使用 MiniMax Coding Plan MCP 服务进行网络搜索和图片理解。

## 工具

1. **web_search** - 网络搜索
   - 参数: query (搜索关键词)
   
2. **understand_image** - 图片理解
   - 参数: prompt (问题), image_source (图片路径或URL)

## 配置

已配置的 MCP 服务器在 `~/.openclaw/workspace/config/mcporter.json`

## 使用方式

```bash
# 搜索
mcporter call minimax.web_search query="搜索内容"

# 图片理解
mcporter call minimax.understand_image prompt="图片内容" image_source="/path/to/image.jpg"
```

## 环境要求

- mcporter
- uvx
