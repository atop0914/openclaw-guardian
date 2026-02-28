#!/usr/bin/env python3
"""
ModelScope 多模型图片生成脚本
当前模型失败时，自动尝试其他模型
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
API_KEY = os.environ.get("MODELSCOPE_TOKEN", "")

# 可用模型列表（按优先级排序）
MODELS = [
    "Tongyi-MAI/Z-Image",
    "Tongyi-MAI/Z-Image-Turbo", 
    "MusePublic/489_ckpt_FLUX_1",
    "Qwen/Qwen-Image",  # 备用
]

def generate_image(prompt, output_path="result.jpg", model=None):
    if not API_KEY:
        print("错误: 请设置 MODELSCOPE_TOKEN 环境变量")
        print("export MODELSCOPE_TOKEN='your_token'")
        sys.exit(1)
    
    # 确定要尝试的模型列表
    models_to_try = [model] if model else MODELS.copy()
    
    common_headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    
    last_error = None
    
    for attempt_model in models_to_try:
        print(f"尝试模型: {attempt_model}")
        
        try:
            # 提交任务
            response = requests.post(
                f"{BASE_URL}v1/images/generations",
                headers={**common_headers, "X-ModelScope-Async-Mode": "true"},
                data=json.dumps({
                    "model": attempt_model,
                    "prompt": prompt
                }, ensure_ascii=False).encode('utf-8'),
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"  模型 {attempt_model} 提交失败: {response.status_code}")
                last_error = f"HTTP {response.status_code}"
                continue
                
            result = response.json()
            
            # 检查是否立即返回结果（同步模式）
            if "output_images" in result and result["output_images"]:
                image = Image.open(BytesIO(requests.get(result["output_images"][0]).content))
                image.save(output_path)
                print(f"✓ 图片生成成功: {output_path} (模型: {attempt_model})")
                return
            
            # 异步模式，轮询任务状态
            task_id = result.get("task_id")
            if not task_id:
                print(f"  模型 {attempt_model} 无 task_id，继续下一个")
                continue
                
            print(f"  任务ID: {task_id}, 等待结果...")
            
            # 轮询等待
            max_wait = 180
            elapsed = 0
            while elapsed < max_wait:
                task_result = requests.get(
                    f"{BASE_URL}v1/tasks/{task_id}",
                    headers={**common_headers, "X-ModelScope-Task-Type": "image_generation"},
                    timeout=30
                )
                
                if task_result.status_code != 200:
                    time.sleep(5)
                    elapsed += 5
                    continue
                    
                data = task_result.json()
                status = data.get("task_status", "UNKNOWN")
                
                if status == "SUCCEED":
                    if "output_images" in data and data["output_images"]:
                        image = Image.open(BytesIO(requests.get(data["output_images"][0]).content))
                        image.save(output_path)
                        print(f"✓ 图片生成成功: {output_path} (模型: {attempt_model})")
                        return
                    else:
                        print(f"  模型 {attempt_model} 返回成功但无图片")
                        break
                elif status == "FAILED":
                    print(f"  模型 {attempt_model} 生成失败")
                    break
                
                time.sleep(5)
                elapsed += 5
                
            print(f"  模型 {attempt_model} 超时，继续下一个模型")
            
        except Exception as e:
            print(f"  模型 {attempt_model} 异常: {e}")
            last_error = str(e)
            continue
    
    print(f"❌ 所有模型都尝试失败，最后错误: {last_error}")
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        print("可用模型:", ", ".join(MODELS))
        sys.exit(1)
    
    prompt = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "result.jpg"
    
    generate_image(prompt, output)
