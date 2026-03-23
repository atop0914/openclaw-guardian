# MiniMax 图片生成

使用 MiniMax image-01 模型生成高质量图片。

## 文件结构

```
minimax-image/
├── SKILL.md                    # Skill 说明文档
├── README.md                   # 本文件
└── scripts/
    └── generate_image.py       # 图片生成脚本
```

## 快速开始

### 1. 设置环境变量

```bash
# 在 ~/.bashrc 或 ~/.zshrc 中添加
export MINIMAX_API_KEY="你的API Key"

# 然后执行
source ~/.bashrc
```

### 2. 安装依赖

```bash
pip3 install requests Pillow
```

### 3. 生成图片

```bash
# 基础用法
python3 scripts/generate_image.py --prompt "一只可爱的猫" --output cat.png

# 指定尺寸
python3 scripts/generate_image.py --prompt "风景图" --width 1024 --height 768 --output landscape.png

# 添加书名和作者
python3 scripts/generate_image.py \
  --prompt "科幻风格封面" \
  --width 600 --height 800 \
  --title "倒计时：最后一次后悔" \
  --author "锦珩不晚" \
  --output cover.png
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--prompt, -p` | 图片描述 (必填) |
| `--width, -w` | 宽度 (512-2048, 默认1024) |
| `--height, -H` | 高度 (512-2048, 默认1024) |
| `--aspect-ratio, -a` | 宽高比 (16:9, 1:1, 9:16) |
| `--output, -o` | 输出路径 (默认 output.png) |
| `--title, -t` | 书名 (会合成到图片底部) |
| `--author` | 作者名 |
| `--api-key` | API Key (不填使用环境变量) |

## 注意事项

1. **API Key 安全**: 不建议在命令行直接传 Key，使用环境变量更安全
2. **中文支持**: 模型对中文文字生成支持较差，建议使用 `--title` 和 `--author` 参数进行后期合成
3. **尺寸限制**: 宽度和高度必须在 512-2048 之间，且是 8 的倍数
