#!/usr/bin/env python3
"""
ModelScope 多模型图片生成
自动轮换模型，每个模型失败后尝试下一个
用法: python3 modelscope_gen.py <prompt> [--output result.jpg]
"""
import requests
import time
import json
import sys
import os
from PIL import Image
from io import BytesIO

API_KEY = os.environ.get("MODELSCOPE_TOKEN", "")
MODELS = [
    "Qwen/Qwen-Image-2512",
    "Tongyi-MAI/Z-Image",
    "Tongyi-MAI/Z-Image-Turbo", 
    "MusePublic/489_ckpt_FLUX_1",
]

def download_image(url):
    if url.startswith("http"):
        return requests.get(url, timeout=60).content
    return requests.get(f"https://api-inference.modelscope.cn/{url.lstrip('/')}", timeout=60).content

def generate(prompt, output="result.jpg"):
    if not API_KEY:
        print("请设置 MODELSCOPE_TOKEN 环境变量")
        sys.exit(1)
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    for model in MODELS:
        print(f"尝试: {model}")
        try:
            # 提交
            r = requests.post(
                "https://api-inference.modelscope.cn/v1/images/generations",
                headers={**headers, "X-ModelScope-Async-Mode": "true"},
                data=json.dumps({"model": model, "prompt": prompt, "width": 1024, "height": 1024}, ensure_ascii=False).encode(),
                timeout=30
            )
            result = r.json()
            
            # 同步返回
            if result.get("output_images"):
                img = Image.open(BytesIO(download_image(result["output_images"][0])))
                img.save(output)
                print(f"✓ 成功: {output}")
                return
            
            # 异步轮询
            task_id = result.get("task_id")
            if not task_id:
                continue
            
            print(f"  任务: {task_id}")
            poll_interval, elapsed = 2, 0
            
            while elapsed < 300:
                task = requests.get(
                    f"https://api-inference.modelscope.cn/v1/tasks/{task_id}",
                    headers={**headers, "X-ModelScope-Task-Type": "image_generation"},
                    timeout=30
                ).json()
                
                if task.get("task_status") == "SUCCEED" and task.get("output_images"):
                    img = Image.open(BytesIO(download_image(task["output_images"][0])))
                    img.save(output)
                    print(f"✓ 成功: {output}")
                    return
                elif task.get("task_status") == "FAILED":
                    break
                
                time.sleep(poll_interval)
                elapsed += poll_interval
                poll_interval = min(poll_interval * 1.5, 30)
                print(f"  等待中... {elapsed}s")
                
        except Exception as e:
            print(f"  异常: {e}")
            continue
    
    print("❌ 所有模型失败")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    generate(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "result.jpg")
