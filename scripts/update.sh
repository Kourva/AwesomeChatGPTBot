#!/usr/bin/env bash
# Updates the bot, keeping .env, the database and the virtualenv.
# Settings come from the environment or /etc/default/<service>.
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -r /etc/default/acgptb-bot ]]; then
    . /etc/default/acgptb-bot
fi

APP_DIR="${APP_DIR:-$(pwd)}"
SERVICE_NAME="${SERVICE_NAME:-acgptb-bot}"
BRANCH="${BRANCH:-main}"
REPO_URL="${REPO_URL:-https://github.com/Kourva/AwesomeChatGPTBot.git}"
VENV="$APP_DIR/.venv"

log() { printf '%s %s\n' "$(date '+%F %T')" "$*"; }

restart() {
    if command -v systemctl >/dev/null 2>&1 && systemctl cat "$SERVICE_NAME.service" >/dev/null 2>&1; then
        systemctl restart "$SERVICE_NAME"
    elif command -v rc-service >/dev/null 2>&1 && [[ -x "/etc/init.d/$SERVICE_NAME" ]]; then
        rc-service "$SERVICE_NAME" restart
    elif command -v sv >/dev/null 2>&1 && [[ -d "/etc/sv/$SERVICE_NAME" ]]; then
        sv restart "$SERVICE_NAME"
    else
        log "no service manager for $SERVICE_NAME, restart the bot yourself"
    fi
}

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

if [[ -d "$APP_DIR/.git" ]]; then
    log "updating git checkout in $APP_DIR"
    git -C "$APP_DIR" fetch --depth 1 origin "$BRANCH"
    git -C "$APP_DIR" merge --ff-only FETCH_HEAD
else
    log "cloning $REPO_URL ($BRANCH)"
    git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$tmp/repo"

    if command -v rsync >/dev/null 2>&1; then
        rsync -a \
            --exclude '.env' --exclude '.venv' --exclude '.git' \
            --exclude '__pycache__' --exclude '*.db' --exclude '*.db-*' \
            "$tmp/repo/" "$APP_DIR/"
    else
        (cd "$tmp/repo" && tar --exclude=.env --exclude=.venv --exclude=.git \
            --exclude=__pycache__ --exclude='*.db*' -cf - .) | (cd "$APP_DIR" && tar -xf -)
    fi
fi

install_requirements() {
    local owner
    owner="$(stat -c '%U' "$VENV/bin/pip" 2>/dev/null || echo root)"
    if [[ $EUID -eq 0 && "$owner" != "root" ]] && command -v runuser >/dev/null 2>&1; then
        runuser -u "$owner" -- "$VENV/bin/pip" install -q -r "$APP_DIR/requirements.txt"
    else
        "$VENV/bin/pip" install -q -r "$APP_DIR/requirements.txt"
    fi
}

if [[ -x "$VENV/bin/pip" ]]; then
    log "installing requirements"
    install_requirements
fi

chmod +x "$APP_DIR/scripts/update.sh" "$APP_DIR/scripts/install.sh" 2>/dev/null || true
restart
log "update finished"
