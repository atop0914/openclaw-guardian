---
name: minimax-image
description: MiniMax 图片生成。使用 MiniMax image-01 模型生成图片，支持自定义尺寸、图生图、角色参考等。
allowed-tools: Bash(python3:*)
---

# MiniMax 图片生成

使用 MiniMax image-01 模型生成高质量图片。

## 前置要求

### 1. 设置 API Key

在 `~/.bashrc` 或 `~/.zshrc` 中添加：

```bash
export MINIMAX_API_KEY="你的API Key"
```

然后执行：

```bash
source ~/.bashrc
```

### 2. 安装依赖

```bash
pip3 install requests Pillow
```

## 快速使用

### 基础生图

```bash
python3 ~/.openclaw/workspace/openclaw-guardian/minimax-image/scripts/generate_image.py \
  --prompt "一只可爱的猫" \
  --width 1024 \
  --height 1024 \
  --output ~/Desktop/cat.png
```

### 带书名和作者

```bash
python3 ~/.openclaw/workspace/openclaw-guardian/minimax-image/scripts/generate_image.py \
  --prompt "科幻风格封面，画面中央有发光的数字1..." \
  --width 600 \
  --height 800 \
  --title "倒计时：最后一次后悔" \
  --author "锦珩不晚" \
  --output ~/Desktop/cover.png
```

## 参数说明

| 参数 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `--prompt` | 是 | 图片描述 | "一只可爱的猫" |
| `--width` | 否 | 宽度 (512-2048, 8的倍数) | 1024 |
| `--height` | 否 | 高度 (512-2048, 8的倍数) | 1024 |
| `--aspect-ratio` | 否 | 宽高比 (与width/height二选一) | 16:9, 1:1, 9:16 |
| `--output` | 否 | 输出路径 (默认 output.png) | ~/Desktop/cat.png |
| `--title` | 否 | 书名 (会在图片下方合成) | "书名" |
| `--author` | 否 | 作者名 | "作者名" |
| `--api-key` | 否 | API Key (不填则使用环境变量) | sk-xxx |

## 尺寸参数规则

- 范围：512×512 到 2048×2048
- 必须是 8 的倍数
- 如果同时指定 `width/height` 和 `aspect_ratio`，**aspect_ratio 优先**

## 图生图 (待实现)

支持上传参考图，保持角色一致性：

```bash
python3 generate_image.py \
  --prompt "把这个角色变成赛博朋克风格" \
  --input-image path/to/reference.png \
  --output out.png
```

## 注意事项

1. **API Key 安全**：不要在命令行中直接暴露 Key，使用环境变量
2. **中文支持**：模型对中文文字生成支持较差，建议用 PIL 后期合成文字
3. **费用**：image-01 按调用次数计费，注意控制成本
