# News Scraper Skill

使用 Playwright 无头浏览器抓取新闻。

## 功能
- 抓取新浪新闻标题
- 抓取腾讯新闻标题
- 支持指定新闻数量
- 返回格式化新闻列表

## 使用方法

```bash
python3 scripts/news_scraper.py [--count 10] [--source sina|tencent]
```

## 参数
- `--count`: 新闻数量（默认10条）
- `--source`: 新闻源（sina/tencent，默认 sina）

## 示例

```bash
# 抓取新浪新闻
python3 scripts/news_scraper.py --count 10

# 抓取腾讯新闻
python3 scripts/news_scraper.py --source tencent --count 10
```

## 示例输出
```
正在抓取 sina 新闻...

📰 新浪新闻 (2026-03-05):
--------------------------------------------------
1. 标题1
2. 标题2
...

共获取 10 条新闻
```
