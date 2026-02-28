#!/bin/bash
#==============================================================================
# OpenClaw 进程守护脚本
# 作用: 监控 OpenClaw 进程是否存活，挂了则自动尝试恢复
# 定时: 每1分钟执行一次 (由系统 crontab 控制)
#==============================================================================

# 自动寻找 openclaw 命令
find_openclaw() {
    # 1. 尝试 PATH 中的 openclaw
    if command -v openclaw &> /dev/null; then
        command -v openclaw
        return 0
    fi
    
    # 2. 尝试常见安装路径
    local paths=(
        "$HOME/.npm-global/bin/openclaw"
        "$HOME/.local/bin/openclaw"
        "/usr/local/bin/openclaw"
        "/usr/bin/openclaw"
        "$HOME/.nvm/current/bin/openclaw"
        "$HOME/.nvm/versions/node/*/bin/openclaw"
        "$HOME/.config/yarn/global/node_modules/.bin/openclaw"
        "$HOME/.yarn/bin/openclaw"
    )
    
    for pattern in "${paths[@]}"; do
        for path in $pattern; do
            if [ -x "$path" ]; then
                echo "$path"
                return 0
            fi
        done
    done
    
    # 3. 尝试使用 npx
    if command -v npx &> /dev/null; then
        echo "npx openclaw"
        return 0
    fi
    
    return 1
}

# 初始化时设置 OPENCLAW 变量
OPENCLAW=$(find_openclaw)
if [ -z "$OPENCLAW" ]; then
    # 兜底：尝试从环境加载 PATH
    [ -f "$HOME/.bashrc" ] && source "$HOME/.bashrc" 2>/dev/null
    [ -f "$HOME/.zshrc" ] && source "$HOME/.zshrc" 2>/dev/null
    [ -f "$HOME/.profile" ] && source "$HOME/.profile" 2>/dev/null
    
    OPENCLAW=$(find_openclaw)
fi

# 定义日志文件路径
LOG_FILE="$HOME/.openclaw/logs/oc_monitor.log"
# 定义配置文件路径
CONFIG_FILE="$HOME/.openclaw/openclaw.json"

# 日志函数: 输出时间戳 + 消息，并同时写入日志文件
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" | tee -a "$LOG_FILE"
}

# 检查是否找到 openclaw
if [ -z "$OPENCLAW" ]; then
    log "ERROR: 找不到 openclaw 命令，请检查安装或手动设置 OPENCLAW 环境变量"
    exit 1
fi

log "使用 openclaw: $OPENCLAW"

# 清理超过24小时的日志
clean_old_logs() {
    if [ -f "$LOG_FILE" ]; then
        # 删除24小时前的日志文件
        find "$LOG_FILE" -mtime +1 -delete 2>/dev/null
        # 同时清理空的日志文件
        find "$HOME/.openclaw/logs/" -name "*.log" -size 0 -delete 2>/dev/null
    fi
}

# 进程检查函数: 检查 openclaw-gateway 进程是否存在
# 返回: 进程存在返回0，不存在返回1
check_process() {
    # pgrep 搜索包含 "openclaw-gateway" 的进程
    pgrep -f "openclaw-gateway" > /dev/null 2>&1
}

#==============================================================================
# 主逻辑
#==============================================================================

# 先清理旧日志
clean_old_logs

log "========== 开始检查 =========="

# 第一步: 检查进程是否已经存活
if check_process; then
    log "OK: OpenClaw进程正常"
    exit 0  # 正常，退出
fi

# 进程已挂，记录警告
log "WARNING: OpenClaw进程已挂掉"

#------------------------------------------------------------------------------
# 方法1: 尝试用 gateway restart 重启
#------------------------------------------------------------------------------
log "尝试方法1: gateway restart..."

$OPENCLAW gateway restart >> "$LOG_FILE" 2>&1
sleep 5

if check_process; then
    log "SUCCESS: 方法1成功，OpenClaw已重启"
    exit 0
fi

log "方法1失败"

#------------------------------------------------------------------------------
# 方法2: 尝试用 doctor fix 自动修复
#------------------------------------------------------------------------------
log "尝试方法2: doctor fix..."

$OPENCLAW doctor fix >> "$LOG_FILE" 2>&1
sleep 5

if check_process; then
    log "SUCCESS: 方法2成功，doctor fix修复成功"
    exit 0
fi

log "方法2失败"

#------------------------------------------------------------------------------
# 方法3: 恢复备份配置文件后重启
#------------------------------------------------------------------------------
log "尝试方法3: 恢复备份配置..."

BACKUP=$(ls -t ~/.openclaw/openclaw.json.bak.* 2>/dev/null | grep -E '[0-9]{8}' | head -1)

if [ -n "$BACKUP" ] && [ -f "$BACKUP" ] && [ -s "$BACKUP" ]; then
    log "找到备份: $BACKUP"
    cp "$BACKUP" "$CONFIG_FILE"
    log "已恢复配置: cp $BACKUP -> $CONFIG_FILE"
    
    $OPENCLAW gateway restart >> "$LOG_FILE" 2>&1
    sleep 5
    
    if check_process; then
        log "SUCCESS: 方法3成功，恢复备份后启动"
        exit 0
    fi
else
    log "FAIL: 没有找到有效的备份文件"
fi

log "方法3失败"

#------------------------------------------------------------------------------
# 方法4: 尝试用 gateway start 启动
#------------------------------------------------------------------------------
log "尝试方法4: gateway start..."

$OPENCLAW gateway start >> "$LOG_FILE" 2>&1
sleep 5

if check_process; then
    log "SUCCESS: 方法4成功"
    exit 0
fi

log "方法4失败"

#------------------------------------------------------------------------------
# 全部方法都失败
#------------------------------------------------------------------------------
log "FAIL: 所有方法都失败，需要人工介入"
exit 1
