# Feishu Image Sender

通过飞书发送图片到用户私信。

## 文件

- `send_image.py` - 主脚本

## 参数

1. 图片路径 (必填)
2. 接收人open_id (必填)
3. 消息文本 (可选，默认"图片")

## 使用方式

```bash
python3 ~/.openclaw/workspace/skills/feishu-image/send_image.py \
  /path/to/image.png \
  ou_93ae9772bb20755c375035e320815bfd \
  "这是图片"
```

## 示例

```bash
# 发送给用户
python3 ~/.openclaw/workspace/skills/feishu-image/send_image.py \
  /home/zhuyitao/openclaw/images/photo.png \
  ou_93ae9772bb20755c375035e320815bfd
```
