#!/usr/bin/env python3
"""
阿里云百炼图片生成脚本
使用 qwen-image-max 模型（推荐）
"""

import os
import sys
import argparse
import time
import requests

# 配置
CREDENTIALS_FILE = os.path.expanduser("~/.openclaw/credentials/aliyun.env")
OUTPUT_DIR = os.path.expanduser("~/openclaw/images")
API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"

def load_api_key():
    """从配置文件加载API Key"""
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            return f.read().strip()
    return None

def generate_image(prompt, style='default', output_path=None):
    """调用阿里云百炼API生成图片"""
    
    api_key = load_api_key()
    if not api_key:
        print("错误：未找到API Key，请配置 ~/.openclaw/credentials/aliyun.env")
        sys.exit(1)
    
    # 风格参数（qwen-image-max 使用 negative_prompt）
    negative_prompt = "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "qwen-image-max",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"text": prompt}
                    ]
                }
            ]
        },
        "parameters": {
            "negative_prompt": negative_prompt,
            "prompt_extend": True,
            "watermark": False,
            "size": "600*800"
        }
    }
    
    print(f"正在调用 qwen-image-max 模型...")
    
    response = requests.post(API_URL, headers=headers, json=data, timeout=30)
    
    if response.status_code != 200:
        print(f"错误：API返回 {response.status_code}")
        print(f"信息: {response.text}")
        sys.exit(1)
    
    result = response.json()
    
    if "output" not in result or "choices" not in result.get("output", {}):
        print(f"错误：{result}")
        sys.exit(1)
    
    # 轮询等待结果
    for i in range(60):
        time.sleep(2)
        
        # 检查是否直接完成
        if result.get("output", {}).get("choices"):
            img_url = result["output"]["choices"][0]["message"]["content"][0]["image"]
            break
        
        print(f"进度: {i*2}s...")
    else:
        print("❌ 超时")
        sys.exit(1)
    
    # 下载图片
    print(f"✅ 图片生成成功!")
    
    if output_path is None:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(OUTPUT_DIR, f"image_{timestamp}.png")
    
    img_data = requests.get(img_url, timeout=30)
    with open(output_path, "wb") as f:
        f.write(img_data.content)
    
    print(f"📁 保存路径: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='阿里云百炼图片生成 (qwen-image-max)')
    parser.add_argument('prompt', help='图片描述文本')
    parser.add_argument('--style', '-s', default='default', help='图片风格（暂不支持）')
    parser.add_argument('--output', '-o', default=None, help='输出文件路径')
    
    args = parser.parse_args()
    
    generate_image(args.prompt, args.style, args.output)

if __name__ == '__main__':
    main()
