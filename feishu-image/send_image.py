#!/usr/bin/env python3
"""
飞书发送图片脚本
用法: python3 feishu_send_image.py <图片路径> <接收人open_id> [消息]
"""
import os
import sys
import json
import requests
import time

# 飞书应用配置（替换为你的实际值）
APP_ID = "YOUR_APP_ID"
APP_SECRET = "YOUR_APP_SECRET"
API_BASE = "https://open.feishu.cn/open-apis"

def get_tenant_access_token():
    """获取tenant_access_token"""
    url = f"{API_BASE}/auth/v3/tenant_access_token/internal"
    data = {"app_id": APP_ID, "app_secret": APP_SECRET}
    resp = requests.post(url, json=data)
    result = resp.json()
    if result.get("code") == 0:
        return result.get("tenant_access_token") or result.get("data", {}).get("tenant_access_token")
    raise Exception(f"获取token失败: {result}")

def upload_image(token, image_path):
    """上传图片获取image_key"""
    url = f"{API_BASE}/im/v1/images"
    headers = {"Authorization": f"Bearer {token}"}
    files = {"image": open(image_path, "rb")}
    data = {"image_type": "message"}
    resp = requests.post(url, headers=headers, files=files, data=data)
    result = resp.json()
    if result.get("code") == 0:
        return result["data"]["image_key"]
    raise Exception(f"上传图片失败: {result}")

def send_image(token, image_key, receive_id, receive_id_type="open_id"):
    """发送图片消息"""
    url = f"{API_BASE}/im/v1/messages?receive_id_type={receive_id_type}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    content = json.dumps({"image_key": image_key})
    data = {
        "receive_id": receive_id,
        "msg_type": "image",
        "content": content
    }
    resp = requests.post(url, headers=headers, json=data)
    result = resp.json()
    if result.get("code") == 0:
        return result["data"]["message_id"]
    raise Exception(f"发送图片失败: {result}")

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    image_path = sys.argv[1]
    receive_id = sys.argv[2]
    message = sys.argv[3] if len(sys.argv) > 3 else "图片"
    
    if not os.path.exists(image_path):
        print(f"错误: 图片文件不存在: {image_path}")
        sys.exit(1)
    
    print(f"正在发送图片: {image_path}")
    print(f"接收人: {receive_id}")
    
    # 获取token
    token = get_tenant_access_token()
    print("✓ 获取token成功")
    
    # 上传图片
    image_key = upload_image(token, image_path)
    print(f"✓ 上传图片成功, image_key: {image_key}")
    
    # 发送图片
    msg_id = send_image(token, image_key, receive_id)
    print(f"✓ 发送成功, message_id: {msg_id}")
    print(f"\n✅ 图片发送完成!")

if __name__ == "__main__":
    main()
