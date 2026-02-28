---
name: aliyun-image
description: AI 图片生成 Skill。支持多种图片生成服务：阿里云百炼（通义万相）、ModelScope（Qwen-Image）。当用户需要AI生成图片、小说封面、插图时使用此Skill。
---

# 图片生成 Skill

支持多种图片生成方式。

## 支持的服务

1. **阿里云百炼** - 通义万相 (默认)
2. **ModelScope** - Qwen-Image

---

## 方式1: 阿里云百炼（通义万相）

### 配置

API Key 存储在 `~/.openclaw/credentials/aliyun.env`：
```bash
DASHSCOPE_API_KEY=your_api_key_here
```

### 使用方法

```bash
# 基本用法
python3 aliyun-image/scripts/generate_image.py "一个穿汉服的古代美女"

# 指定风格
python3 aliyun-image/scripts/generate_image.py "小说封面" --style anime

# 保存到指定路径
python3 aliyun-image/scripts/generate_image.py "风景画" --output /path/to/output.png
```

### 参数说明

| 参数 | 说明 |
|------|------|
| prompt | 图片描述 |
| --style | 风格 (anime/realistic/default/watercolor/oil_painting/sketch) |
| --output | 保存路径 |

---

## 方式2: ModelScope (Qwen-Image)

### 配置

设置环境变量：
```bash
export MODELSCOPE_TOKEN='your_token'
```

### 使用方法

```bash
python3 aliyun-image/scripts/modelscope_gen.py "A golden cat" --output result.jpg
```

### 参数说明

| 参数 | 说明 |
|------|------|
| prompt | 图片描述（必填） |
| --output | 保存路径（默认 result.jpg） |
