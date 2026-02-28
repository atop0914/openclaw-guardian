---
name: aliyun-image
description: 使用阿里云百炼（通义万相）生成图片。当用户需要AI生成图片、小说封面、插图时使用此Skill。
---

# 阿里云百炼图片生成

使用阿里云百炼的文生图API生成图片。

## 配置

API Key 存储在 `~/.openclaw/credentials/aliyun.env`：
```bash
DASHSCOPE_API_KEY=your_api_key_here
```

## 使用方法

### 方式1: 直接调用脚本

```bash
# 基本用法 - 中文提示词
python3 ~/.openclaw/workspace/skills/aliyun-image/scripts/generate_image.py \
  "一个穿汉服的古代美女，站在桃花树下"

# 英文提示词
python3 ~/.openclaw/workspace/skills/aliyun-image/scripts/generate_image.py \
  "A beautiful Chinese woman in hanfu standing under cherry blossoms" \
  --english

# 指定风格
python3 ~/.openclaw/workspace/skills/aliyun-image/scripts/generate_image.py \
  "小说封面：一个古代书生在书院读书" \
  --style anime

# 保存到指定路径
python3 ~/.openclaw/workspace/skills/aliyun-image/scripts/generate_image.py \
  "风景画：山水意境" \
  --output /home/zhuyitao/images/landscape.png
```

### 方式2: 在对话中使用

当用户要求生成图片时，使用上述命令调用。

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| prompt | 图片描述（必填） | - |
| --english | 使用英文提示词 | 自动翻译 |
| --style | 风格 (anime/realistic/default) | default |
| --output | 保存路径 | ./output.png |

## 支持的风格

- `default` - 默认风格
- `anime` - 动漫风格
- `realistic` - 写实风格
- `watercolor` - 水彩风格
- `oil_painting` - 油画风格
- `sketch` - 素描风格

## 输出

- 返回图片保存路径
- 图片自动保存到 `~/openclaw/images/` 目录

## 常见场景

1. **小说封面生成**
   - 根据小说内容生成符合主题的封面

2. **插图生成**
   - 为文章、故事配图

3. **海报设计**
   - 活动海报、宣传图

## 注意事项

- 提示词越详细，生成效果越好
- 中文提示词会自动翻译为英文
- 生成图片需要几秒钟时间
- API有调用频率限制
