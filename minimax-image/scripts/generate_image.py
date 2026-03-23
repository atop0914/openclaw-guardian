#!/usr/bin/env python3
"""
MiniMax 图片生成脚本
支持自定义尺寸、书名/作者合成
API Key 从环境变量 MINIMAX_API_KEY 读取
"""

import argparse
import base64
import os
import json
import requests
from PIL import Image, ImageDraw, ImageFont


def get_api_key():
    """获取 API Key"""
    # 优先从环境变量读取
    api_key = os.environ.get("MINIMAX_API_KEY")
    if api_key:
        return api_key
    
    # 从 OpenClaw 配置读取
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                config = json.load(f)
            # 从 minimax provider 获取 apiKey
            api_key = config.get("models", {}).get("providers", {}).get("minimax", {}).get("apiKey")
            if api_key:
                return api_key
        except Exception as e:
            print(f"读取配置文件失败: {e}")
    
    raise ValueError("未找到 API Key，请设置 MINIMAX_API_KEY 环境变量")


def generate_image(prompt, width=1024, height=1024, api_key=None, output="output.png"):
    """生成图片"""
    if api_key is None:
        api_key = get_api_key()
    
    url = "https://api.minimaxi.com/v1/image_generation"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "width": width,
        "height": height,
        "response_format": "base64"
    }
    
    print(f"正在生成图片，尺寸 {width}×{height}...")
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    
    if response.status_code == 200:
        result = response.json()
        images = result["data"]["image_base64"]
        
        # 保存原始图片
        with open(output, "wb") as f:
            f.write(base64.b64decode(images[0]))
        
        print(f"图片已保存到: {output}")
        return output
    else:
        raise Exception(f"API 错误: {response.status_code}\n{response.text}")


def add_text_overlay(image_path, title=None, author=None, output=None):
    """添加书名和作者文字"""
    if output is None:
        output = image_path
    
    img = Image.open(image_path)
    w, h = img.size
    
    # 如果没有文字要添加，直接返回
    if not title and not author:
        return image_path
    
    draw = ImageDraw.Draw(img)
    
    # 加载中文字体
    font_paths = [
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    
    font_title = None
    font_author = None
    for path in font_paths:
        try:
            font_title = ImageFont.truetype(path, int(h * 0.05))
            font_author = ImageFont.truetype(path, int(h * 0.03))
            break
        except:
            continue
    
    if font_title is None:
        font_title = ImageFont.load_default()
        font_author = ImageFont.load_default()
    
    # 添加底部黑色半透明区域
    if title or author:
        overlay_h = int(h * 0.15)
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle([(0, h - overlay_h), (w, h)], fill=(0, 0, 0, 180))
        
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)
    
    # 绘制书名
    if title:
        bbox = draw.textbbox((0, 0), title, font=font_title)
        title_w = bbox[2] - bbox[0]
        title_x = (w - title_w) // 2
        draw.text((title_x, h - overlay_h + 10), title, font=font_title, fill=(255, 255, 255))
    
    # 绘制作者
    if author:
        bbox = draw.textbbox((0, 0), author, font=font_author)
        author_w = bbox[2] - bbox[0]
        author_x = (w - author_w) // 2
        draw.text((author_x, h - overlay_h + int(h * 0.08)), author, font=font_author, fill=(200, 200, 200))
    
    img.save(output)
    print(f"已添加文字: {title} | {author}")
    return output


def main():
    parser = argparse.ArgumentParser(description="MiniMax 图片生成")
    parser.add_argument("--prompt", "-p", required=True, help="图片描述")
    parser.add_argument("--width", "-w", type=int, default=1024, help="宽度 (512-2048)")
    parser.add_argument("--height", "-H", type=int, default=1024, help="高度 (512-2048)")
    parser.add_argument("--aspect-ratio", "-a", help="宽高比 (16:9, 1:1, 9:16)")
    parser.add_argument("--output", "-o", default="output.png", help="输出路径")
    parser.add_argument("--title", "-t", help="书名 (会合成到图片)")
    parser.add_argument("--author", help="作者名 (会合成到图片)")
    parser.add_argument("--api-key", help="API Key (不填则使用环境变量)")
    
    args = parser.parse_args()
    
    try:
        # 生成图片
        image_path = generate_image(
            prompt=args.prompt,
            width=args.width,
            height=args.height,
            api_key=args.api_key,
            output=args.output
        )
        
        # 添加文字
        if args.title or args.author:
            add_text_overlay(image_path, args.title, args.author, args.output)
        
        print("完成!")
        
    except Exception as e:
        print(f"错误: {e}")
        exit(1)


if __name__ == "__main__":
    main()
