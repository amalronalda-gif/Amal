#!/usr/bin/env bash
# MarketFlow bot: one-command installer for an Ubuntu/Debian VPS.
#
#   curl -fsSL https://raw.githubusercontent.com/amalronalda-gif/Amal/claude/xauusdt-liquidity-sweeps-xehad0/trading-bot/deploy/install.sh | bash
#
# or clone the repo first and run: bash trading-bot/deploy/install.sh
# Installs to /opt/marketflow, stores the token in /etc/marketflow.env,
# registers a systemd service with auto-restart and starts it.

set -euo pipefail

REPO="https://github.com/amalronalda-gif/Amal.git"
BRANCH="claude/xauusdt-liquidity-sweeps-xehad0"
DIR="/opt/marketflow"

if [ -z "${TELEGRAM_BOT_TOKEN:-}" ]; then
    read -rp "Telegram bot token (from @BotFather): " TELEGRAM_BOT_TOKEN
fi
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "error: empty token" >&2
    exit 1
fi

SUDO=""
[ "$(id -u)" -ne 0 ] && SUDO="sudo"

echo "==> installing system packages"
$SUDO apt-get update -y
$SUDO apt-get install -y python3 python3-pip git

echo "==> installing matplotlib (chart images; optional but recommended)"
$SUDO python3 -m pip install --quiet matplotlib --break-system-packages \
    || $SUDO python3 -m pip install --quiet matplotlib \
    || echo "matplotlib install failed — bot will run text-only"

echo "==> fetching the bot into $DIR"
if [ -d "$DIR/.git" ]; then
    $SUDO git -C "$DIR" fetch origin "$BRANCH"
    $SUDO git -C "$DIR" checkout "$BRANCH"
    $SUDO git -C "$DIR" pull origin "$BRANCH"
else
    $SUDO git clone --branch "$BRANCH" "$REPO" "$DIR"
fi

echo "==> writing /etc/marketflow.env (token kept out of the unit file)"
printf 'TELEGRAM_BOT_TOKEN=%s\n' "$TELEGRAM_BOT_TOKEN" | $SUDO tee /etc/marketflow.env >/dev/null
$SUDO chmod 600 /etc/marketflow.env

echo "==> registering systemd service"
$SUDO cp "$DIR/trading-bot/deploy/marketflow-bot.service" /etc/systemd/system/
$SUDO systemctl daemon-reload
$SUDO systemctl enable --now marketflow-bot

sleep 3
$SUDO systemctl --no-pager --full status marketflow-bot || true
echo
echo "Done. Useful commands:"
echo "  journalctl -u marketflow-bot -f      # live logs"
echo "  systemctl restart marketflow-bot     # restart"
echo "  systemctl stop marketflow-bot        # stop"
