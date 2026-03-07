#!/usr/bin/env python3
"""
新闻抓取脚本
使用 Playwright 无头浏览器抓取新闻
"""

import argparse
import sys
from playwright.sync_api import sync_playwright


def scrape_sina_news(count=10):
    """抓取新浪新闻"""
    news_list = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto('https://news.sina.com.cn/', timeout=15000)
            page.wait_for_timeout(3000)
            
            all_links = page.query_selector_all('a')
            seen = set()
            
            for link in all_links:
                try:
                    title = link.inner_text().strip()
                    href = link.get_attribute('href') or ''
                    
                    if (title and len(title) > 10 and 
                        'news.sina.com.cn' in href and 
                        title not in seen and
                        'javascript' not in href.lower()):
                        seen.add(title)
                        news_list.append({
                            'title': title[:80],
                            'url': href
                        })
                except:
                    pass
                    
        except Exception as e:
            print(f"抓取失败: {e}")
        finally:
            browser.close()
    
    return news_list[:count]


def scrape_tencent_news(count=10):
    """抓取腾讯新闻"""
    news_list = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto('https://news.qq.com/', timeout=15000)
            page.wait_for_timeout(3000)
            
            all_links = page.query_selector_all('a')
            seen = set()
            
            for link in all_links:
                try:
                    title = link.inner_text().strip()
                    href = link.get_attribute('href') or ''
                    
                    if (title and len(title) > 8 and 
                        'news.qq.com' in href and 
                        title not in seen and
                        'javascript' not in href.lower()):
                        seen.add(title)
                        news_list.append({
                            'title': title[:80],
                            'url': href
                        })
                except:
                    pass
                    
        except Exception as e:
            print(f"抓取失败: {e}")
        finally:
            browser.close()
    
    return news_list[:count]


def main():
    parser = argparse.ArgumentParser(description='新闻抓取工具')
    parser.add_argument('--count', type=int, default=10, help='新闻数量')
    parser.add_argument('--source', type=str, default='sina', 
                        choices=['sina', 'tencent'], help='新闻源')
    args = parser.parse_args()
    
    print(f"正在抓取 {args.source} 新闻...")
    
    if args.source == 'sina':
        news = scrape_sina_news(args.count)
    elif args.source == 'tencent':
        news = scrape_tencent_news(args.count)
    else:
        print(f"不支持的新闻源: {args.source}")
        sys.exit(1)
    
    if not news:
        print("未能获取新闻")
        sys.exit(1)
    
    # 打印新闻
    from datetime import datetime
    source_name = "新浪" if args.source == "sina" else "腾讯"
    print(f"\n📰 {source_name}新闻 ({datetime.now().strftime('%Y-%m-%d')}):")
    print("-" * 50)
    for i, n in enumerate(news, 1):
        print(f"{i}. {n['title']}")
    
    print(f"\n共获取 {len(news)} 条新闻")


if __name__ == '__main__':
    main()
