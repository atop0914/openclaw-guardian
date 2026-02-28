# OpenClaw Guardian

OpenClaw 进程守护工具，自动监控并恢复 Gateway 进程。

## 功能

1. **进程监控**: 每 1 分钟检查 OpenClaw Gateway 进程是否存活
2. **自动恢复**: 进程挂掉后自动尝试 4 种恢复方法
3. **智能路径探测**: 自动寻找 openclaw 命令，支持多种安装方式（npm 全局、nvm、yarn、npx）
4. **配置备份**: 每天自动备份 openclaw.json 配置文件
5. **自动清理**: 保留最近 7 天备份和 24 小时日志

## 安装

### 1. 复制脚本

```bash
cp -r scripts ~/.openclaw/
```

### 2. 添加 crontab 任务

```bash
crontab -e
```

添加以下内容:

```cron
# OpenClaw Guardian - 进程监控（每1分钟检查）
*/1 * * * * $HOME/.openclaw/scripts/oc_monitor.sh >> $HOME/.openclaw/logs/oc_monitor.log 2>&1

# OpenClaw Guardian - 配置备份（每天凌晨2点）
0 2 * * * $HOME/.openclaw/scripts/backup_config.sh
```

### 3. 首次执行

```bash
# 创建日志目录
mkdir -p ~/.openclaw/logs

# 执行一次备份
~/.openclaw/scripts/backup_config.sh
```

## 恢复策略

当检测到 Gateway 进程不存在时，按以下顺序尝试恢复：

1. `openclaw gateway restart` - 正常重启
2. `openclaw doctor fix` - 自动修复
3. 恢复最近备份配置后重启
4. `openclaw gateway start` - 强制启动

## 备份格式

文件名: `openclaw.json.bak.YYYYMMDD`

示例:
- `openclaw.json.bak.20260222` (2026年2月22日)
- `openclaw.json.bak.20260223` (2026年2月23日)

保留最近 7 天备份，旧备份自动清理。

## 日志

| 日志文件 | 说明 |
|---------|------|
| `~/.openclaw/logs/oc_monitor.log` | 守护进程监控日志 |
| `~/.openclaw/logs/backup.log` | 配置备份日志 |

日志自动保留最近 24 小时，超期自动清理。

## 环境兼容性

脚本支持多种 openclaw 安装方式：
- npm 全局安装 (`~/.npm-global/bin/`)
- nvm 安装
- yarn 全局安装
- npx 运行
- 系统包管理器安装 (`/usr/local/bin/`, `/usr/bin/`)

无需手动配置 PATH，脚本会自动探测 openclaw 路径。

## 手动测试

```bash
# 测试监控脚本
~/.openclaw/scripts/oc_monitor.sh

# 测试备份脚本
~/.openclaw/scripts/backup_config.sh
```
