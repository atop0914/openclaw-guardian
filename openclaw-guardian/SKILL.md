---
name: openclaw-guardian
description: OpenClaw 进程守护技能。自动监控 Gateway 进程状态，进程挂掉时自动尝试恢复。触发条件：需要守护 OpenClaw 进程、监控服务状态、自动重启。
---

# OpenClaw Guardian

自动监控 OpenClaw 进程状态，进程挂掉时自动尝试恢复。

## 功能

1. **进程监控**: 每 3 分钟检查 OpenClaw Gateway 进程是否存活
2. **自动恢复**: 进程挂掉后自动尝试 4 种恢复方法:
   - 方法1: `gateway restart` 重启
   - 方法2: `doctor fix` 自动修复
   - 方法3: 恢复配置文件备份后重启
   - 方法4: `gateway start` 启动
3. **每日备份**: 每天自动备份 `openclaw.json` 配置文件

## 详细说明

见 [docs/README.md](docs/README.md)
