#!/usr/bin/env python3
"""
邮件发送脚本
读取 ~/.openclaw/credentials/email.env 配置，发送邮件
"""

import smtplib
import sys
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

CONFIG_PATH = os.path.expanduser("~/.openclaw/credentials/email.env")

def load_config():
    """从 .env 文件加载邮件配置"""
    config = {}
    try:
        with open(CONFIG_PATH, 'r') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if not line or line.startswith('#'):
                    continue
                # 解析 KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
        return config
    except FileNotFoundError:
        print(f"错误: 配置文件不存在: {CONFIG_PATH}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 读取配置文件失败: {e}")
        sys.exit(1)

def send_email(to_email, subject, body, attachments=None):
    """
    发送邮件
    
    参数:
        to_email: 收件人邮箱（多个用逗号分隔）
        subject: 邮件主题
        body: 邮件正文（支持 HTML）
        attachments: 附件路径列表（可选）
    """
    config = load_config()
    
    # 获取配置
    smtp_server = config.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(config.get('SMTP_PORT', 587))
    sender_email = config.get('SENDER_EMAIL', '')
    sender_password = config.get('SENDER_PASSWORD', '')
    
    if not sender_email or not sender_password:
        print("错误: 邮件配置不完整，请检查 SENDER_EMAIL 和 SENDER_PASSWORD")
        sys.exit(1)
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # 添加正文
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    
    # 添加附件
    if attachments:
        for filepath in attachments:
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                filename = os.path.basename(filepath)
                part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                msg.attach(part)
    
    # 发送邮件
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启用 TLS
        server.login(sender_email, sender_password)
        
        text = msg.as_string()
        server.sendmail(sender_email, to_email.split(','), text)
        server.quit()
        
        print(f"✅ 邮件发送成功!")
        print(f"   收件人: {to_email}")
        print(f"   主题: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def main():
    if len(sys.argv) < 4:
        print("用法: python3 send_email.py <收件人> <主题> <正文文件路径> [附件1,附件2,...]")
        print("")
        print("示例:")
        print("  python3 send_email.py 'user@example.com' '测试邮件' /tmp/body.txt")
        print("  python3 send_email.py 'a@ex.com,b@ex.com' '报告' /tmp/body.html /tmp/report.pdf")
        sys.exit(1)
    
    to_email = sys.argv[1]
    subject = sys.argv[2]
    body_file = sys.argv[3]
    attachments = sys.argv[4:] if len(sys.argv) > 4 else None
    
    # 读取正文
    try:
        with open(body_file, 'r', encoding='utf-8') as f:
            body = f.read()
    except FileNotFoundError:
        # 如果没有文件，直接把第三个参数当正文
        body = body_file
    
    success = send_email(to_email, subject, body, attachments)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
