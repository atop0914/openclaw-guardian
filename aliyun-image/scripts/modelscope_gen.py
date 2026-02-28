#!/usr/bin/env python3
"""
ModelScope 图片生成脚本
用法: python3 modelscope_gen.py <prompt> [--output result.jpg]
"""
import requests
import time
import json
import sys
import os
from PIL import Image
from io import BytesIO

BASE_URL = 'https://api-inference.modelscope.cn/'
API_KEY = os.environ.get("MODELSCOPE_TOKEN", "")  # 从环境变量读取

def generate_image(prompt, output_path="result.jpg"):
    if not API_KEY:
        print("错误: 请设置 MODELSCOPE_TOKEN 环境变量")
        print("export MODELSCOPE_TOKEN='your_token'")
        sys.exit(1)
    
    common_headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    # 提交任务
    response = requests.post(
        f"{BASE_URL}v1/images/generations",
        headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
        data=json.dumps({
            "model": "Qwen/Qwen-Image",
            "prompt": prompt
        }, ensure_ascii=False).encode('utf-8')
    )
    response.raise_for_status()
    task_id = response.json()["task_id"]
    print(f"任务提交成功, task_id: {task_id}")
    
    # 轮询结果
    while True:
        result = requests.get(
            f"{BASE_URL}v1/tasks/{task_id}",
            headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
        )
        result.raise_for_status()
        data = result.json()
        
        if data["task_status"] == "SUCCEED":
            image = Image.open(BytesIO(requests.get(data["output_images"][0]).content))
            image.save(output_path)
            print(f"图片已保存: {output_path}")
            break
        elif data["task_status"] == "FAILED":
            print("图片生成失败")
            sys.exit(1)
        
        time.sleep(5)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    prompt = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "result.jpg"
    
    generate_image(prompt, output)
