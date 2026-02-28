---
name: feishu-image
description: 发送图片到飞书。触发条件：用户要求发送图片到飞书、发送图片到钉钉。
---

# Feishu Image

发送图片到飞书。

## 使用方式

```bash
python3 <skill-path>/send_image.py <图片路径> <接收人open_id> [消息]
```

## 参数

| 参数 | 说明 |
|------|------|
| 图片路径 | 本地图片文件路径 |
| 接收人open_id | 飞书用户 open_id |
| 消息（可选） | 附加消息 |

## 示例

```bash
python3 send_image.py /path/to/image.png ou_93ae9772bb20755c375035e320815bfd "请查看图片"
```
