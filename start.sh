#!/bin/sh
set -eu

# ── Environment variables ──────────────────────────────────────────
# Required
: "${R_ID:?ERROR: R_ID is required}"
: "${PASSWORD:?ERROR: PASSWORD is required}"
# Optional (with defaults)
DOMAIN="${DOMAIN:-helloworld.com}"
UP="${UP:-220}"
DOWN="${DOWN:-44}"

echo "=== Initializing services ==="
echo "  DOMAIN  : ${DOMAIN}"
echo "  R_ID    : ${R_ID}"
echo "  UP      : ${UP}mbps"
echo "  DOWN    : ${DOWN}mbps"

# ── Decode config ──────────────────────────────────────────────────
base64 -d /etc/web/config.dat > /etc/web/config.yaml
rm -f /etc/web/config.dat

# ── Patch config.yaml with env values ──────────────────────────────
# Listen address: replace UUID in the listen line only
sed -i "/^listen:/s|\(realm://[^/]*/\)[^ ]*|\1${R_ID}|" /etc/web/config.yaml

# Auth password (only the line indented under auth:, not secret:)
sed -i "/^  password:/s|password:.*|password: ${PASSWORD}|" /etc/web/config.yaml

# Bandwidth
sed -i "s|up: [0-9]*mbps|up: ${UP}mbps|" /etc/web/config.yaml
sed -i "s|down: [0-9]*mbps|down: ${DOWN}mbps|" /etc/web/config.yaml

# ── Generate self-signed certificate ───────────────────────────────
echo "=== Generating self-signed certificate for ${DOMAIN} ==="
if ! openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 \
    -days 3650 -nodes \
    -keyout /etc/web/a.key \
    -out /etc/web/a.crt \
    -subj "/CN=${DOMAIN}" \
    2>/dev/null; then
    echo "ERROR: Failed to generate certificate"
    exit 1
fi

# Verify cert was created
if [ ! -f /etc/web/a.crt ] || [ ! -f /etc/web/a.key ]; then
    echo "ERROR: Certificate files not found after generation"
    exit 1
fi
echo "=== Certificate generated ==="

# Debug: show patched config
echo "=== Patched config.yaml ==="
cat /etc/web/config.yaml
echo "==========================="

# ── Start backend service ──────────────────────────────────────────
/usr/local/bin/app server -c /etc/web/config.yaml --log-level=error &

echo "=== Starting NextChat ==="
cd /app
export PORT=8080
export HOSTNAME="0.0.0.0"
exec node server.js
