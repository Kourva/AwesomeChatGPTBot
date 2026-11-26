#!/usr/bin/env bash
# Installs the bot as a service (systemd, OpenRC or runit) and schedules daily updates.
# Usage: sudo ./scripts/install.sh   (REPO_URL=... BRANCH=... to override)
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE="${SERVICE_NAME:-kowshan-bot}"
RUN_USER="${SUDO_USER:-$(id -un)}"
PYTHON="${PYTHON:-python3}"
CONF="/etc/default/$SERVICE"
REPO_URL="${REPO_URL:-https://github.com/Kourva/AwesomeChatGPTBot.git}"
BRANCH="${BRANCH:-main}"

if [[ $EUID -ne 0 ]]; then
    echo "Run with sudo: sudo $0" >&2
    exit 1
fi

run_as_user() {
    if [[ "$RUN_USER" == "root" ]]; then
        "$@"
    else
        sudo -u "$RUN_USER" "$@"
    fi
}

echo "==> dependencies"
[[ -d "$APP_DIR/.venv" ]] || run_as_user "$PYTHON" -m venv "$APP_DIR/.venv"
run_as_user "$APP_DIR/.venv/bin/pip" install -q --upgrade pip
run_as_user "$APP_DIR/.venv/bin/pip" install -q -r "$APP_DIR/requirements.txt"
chmod +x "$APP_DIR/scripts/update.sh" "$APP_DIR/scripts/install.sh"

cat > "$CONF" <<EOF
APP_DIR="$APP_DIR"
REPO_URL="$REPO_URL"
BRANCH="$BRANCH"
SERVICE_NAME="$SERVICE"
EOF

schedule_cron() {
    if [[ -d /etc/cron.d ]]; then
        cat > "/etc/cron.d/$SERVICE-update" <<EOF
# daily auto update for $SERVICE
0 4 * * * root "$APP_DIR/scripts/update.sh" >> "/var/log/$SERVICE-update.log" 2>&1
EOF
        echo "==> daily update scheduled in /etc/cron.d/$SERVICE-update"
    else
        echo "!! no /etc/cron.d, add this to cron:"
        echo "0 4 * * * root $APP_DIR/scripts/update.sh >> /var/log/$SERVICE-update.log 2>&1"
    fi
}

if command -v systemctl >/dev/null 2>&1; then
    echo "==> systemd"
    cat > "/etc/systemd/system/$SERVICE.service" <<EOF
[Unit]
Description=Kowshan Telegram bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$RUN_USER
WorkingDirectory=$APP_DIR
EnvironmentFile=-$CONF
ExecStart=$APP_DIR/.venv/bin/python src/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

    cat > "/etc/systemd/system/$SERVICE-update.service" <<EOF
[Unit]
Description=Update Kowshan Telegram bot
After=network-online.target

[Service]
Type=oneshot
EnvironmentFile=-$CONF
ExecStart=$APP_DIR/scripts/update.sh
EOF

    cat > "/etc/systemd/system/$SERVICE-update.timer" <<EOF
[Unit]
Description=Daily update for Kowshan Telegram bot

[Timer]
OnCalendar=*-*-* 04:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

    systemctl daemon-reload
    systemctl enable --now "$SERVICE"
    systemctl enable --now "$SERVICE-update.timer"
    echo "==> started $SERVICE and $SERVICE-update.timer"

elif command -v rc-update >/dev/null 2>&1; then
    echo "==> OpenRC"
    cat > "/etc/init.d/$SERVICE" <<EOF
#!/sbin/openrc-run
name="$SERVICE"
description="Kowshan Telegram bot"
command="$APP_DIR/.venv/bin/python"
command_args="src/main.py"
command_background=true
directory="$APP_DIR"
pidfile="/run/$SERVICE.pid"
output_log="/var/log/$SERVICE.log"
error_log="/var/log/$SERVICE.log"

depend() {
    need net
    after firewall
}
EOF
    chmod +x "/etc/init.d/$SERVICE"
    rc-update add "$SERVICE" default
    rc-service "$SERVICE" restart || rc-service "$SERVICE" start
    schedule_cron
    echo "==> started $SERVICE"

elif command -v sv >/dev/null 2>&1 && [[ -d /etc/sv ]]; then
    echo "==> runit"
    LIVE_DIR="/var/service"
    [[ -d "$LIVE_DIR" ]] || LIVE_DIR="/service"

    mkdir -p "/etc/sv/$SERVICE"
    cat > "/etc/sv/$SERVICE/run" <<EOF
#!/bin/sh
exec 2>&1
cd "$APP_DIR" || exit 1
exec chpst -u "$RUN_USER" "$APP_DIR/.venv/bin/python" src/main.py
EOF
    chmod +x "/etc/sv/$SERVICE/run"
    ln -sfn "/etc/sv/$SERVICE" "$LIVE_DIR/$SERVICE"
    sv up "$SERVICE" || true
    schedule_cron
    echo "==> started $SERVICE in $LIVE_DIR"

else
    echo "!! unknown init system (no systemd, OpenRC or runit)"
    echo "   run manually: cd $APP_DIR && .venv/bin/python src/main.py"
    schedule_cron
fi

echo "==> done. service: $SERVICE, app: $APP_DIR"
