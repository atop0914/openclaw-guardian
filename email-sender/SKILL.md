---
name: email-sender
description: 发送邮件到指定邮箱地址。支持纯文本/HTML格式、多收件人、附件。当用户需要发送邮件通知、报告、提醒时使用此 Skill。
---

# Email Sender - 邮件发送工具

通过 SMTP 发送邮件，支持 Gmail 等主流邮箱服务。

## 配置

邮件配置存储在 `~/.openclaw/credentials/email.env`：
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your@gmail.com
SENDER_PASSWORD=your_app_password
```

**注意**: Gmail 需要使用应用专用密码，不是账号密码。

## 使用方法

### 方式1: 直接调用脚本

```bash
# 基本用法
python3 ~/.openclaw/workspace/skills/email-sender/scripts/send_email.py \
  'recipient@example.com' \
  '邮件主题' \
  '邮件正文内容'

# 带附件
python3 ~/.openclaw/workspace/skills/email-sender/scripts/send_email.py \
  'user1@ex.com,user2@ex.com' \
  '月度报告' \
  '/path/to/body.html' \
  '/path/to/attachment1.pdf' \
  '/path/to/attachment2.xlsx'
```

### 方式2: 从文件读取正文

```bash
# 先创建邮件正文文件
cat > /tmp/email_body.html <> 'EOF'
<h1>您好</h1>
<p>这是邮件内容。</p>
EOF

# 发送
python3 scripts/send_email.py 'to@ex.com' '主题' /tmp/email_body.html
```

## 功能特性

| 功能 | 说明 |
|------|------|
| 多收件人 | 用逗号分隔多个邮箱 |
| HTML 邮件 | 正文支持 HTML 格式 |
| 附件 | 支持多个附件 |
| 自动编码 | UTF-8 编码支持中文 |

## 常见场景

1. **发送定时报告**
   - 生成报告文件
   - 调用脚本发送给相关人员

2. **系统告警通知**
   - 监控异常时发送邮件

3. **任务完成提醒**
   - 长时间任务完成后通知

## 注意事项

- 确保 `email_config.json` 存在且配置正确
- Gmail 需要开启两步验证并生成应用专用密码
- 附件路径必须是绝对路径或相对于当前目录的路径
