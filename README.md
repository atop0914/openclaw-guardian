# OpenClaw Skills Collection

OpenClaw 自动化技能集合，包含多种工具和服务的封装。

## Skills

| Skill | 功能 |
|-------|------|
| [minimax-mcp](./minimax-mcp) | MiniMax MCP 服务（网络搜索、图片理解） |
| [serper-search](./serper-search) | Serper Google 搜索 API |
| [aliyun-image](./aliyun-image) | 阿里云百炼图片生成 |
| [feishu-image](./feishu-image) | 飞书图片发送 |
| [email-sender](./email-sender) | 邮件发送（Gmail SMTP） |
| [voice-to-text](./voice-to-text) | 语音转文字（faster-whisper） |
| [news-scraper](./news-scraper) | 新闻抓取（Playwright） |
| [chinese-novelist](./chinese-novelist) | 中文小说写作辅助 |

## 安全

- 🔒 所有敏感配置通过环境变量或配置文件管理
- ✅ GitHub Actions TruffleHog 扫描，防止 API Key 泄露

## 使用方法

每个 skill 目录包含独立的 `SKILL.md` 说明文档，按照文档步骤安装即可。
