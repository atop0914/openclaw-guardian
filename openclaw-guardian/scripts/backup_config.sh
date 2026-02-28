#!/bin/bash
#==============================================================================
# OpenClaw 配置文件每日备份脚本
# 作用: 每天自动备份 openclaw.json 配置文件
# 定时: 建议每天凌晨 02:00 执行 (由系统 crontab 控制)
#==============================================================================

CONFIG_FILE="$HOME/.openclaw/openclaw.json"
BACKUP_DIR="$HOME/.openclaw"
LOG_FILE="$HOME/.openclaw/logs/backup.log"

# 备份文件名格式: openclaw.json.bak.YYYYMMDD
BACKUP_FILE="$BACKUP_DIR/openclaw.json.bak.$(date +%Y%m%d)"

# 日志函数
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" | tee -a "$LOG_FILE"
}

log "========== 开始备份 =========="

# 检查配置文件是否存在
if [ ! -f "$CONFIG_FILE" ]; then
    log "ERROR: 配置文件不存在 - $CONFIG_FILE"
    exit 1
fi

# 执行备份
cp "$CONFIG_FILE" "$BACKUP_FILE"
if [ $? -eq 0 ]; then
    log "备份成功: $BACKUP_FILE"
else
    log "ERROR: 备份失败"
    exit 1
fi

# 清理7天前的备份
DELETED=$(find "$BACKUP_DIR" -name "openclaw.json.bak.*" -mtime +7)
if [ -n "$DELETED" ]; then
    find "$BACKUP_DIR" -name "openclaw.json.bak.*" -mtime +7 -delete
    log "已清理7天前的旧备份"
else
    log "没有超过7天的备份需要清理"
fi

# 显示当前备份数量
COUNT=$(ls -1 "$BACKUP_DIR"/openclaw.json.bak.* 2>/dev/null | wc -l)
log "当前共有 $COUNT 个备份文件"

log "========== 备份完成 =========="
