#!/bin/sh
set -eu

# ── Environment variables ──────────────────────────────────────────
: "${R_ID:?ERROR: R_ID is required}"
: "${PASSWORD:?ERROR: PASSWORD is required}"
DOMAIN="${DOMAIN:-helloworld.com}"
UP="${UP:-220}"
DOWN="${DOWN:-44}"

# ── Decode config ──────────────────────────────────────────────────
base64 -d /etc/web/config.dat > /etc/web/config.yaml
rm -f /etc/web/config.dat

# ── Patch config.yaml ──────────────────────────────────────────────
sed -i "s|^listen:.*realm://.*\/.*|listen: realm://public@realm.hy2.io/${R_ID}|" /etc/web/config.yaml
sed -i "/^  password:/s|password:.*|password: ${PASSWORD}|" /etc/web/config.yaml
sed -i "s|up: [0-9]*mbps|up: ${UP}mbps|" /etc/web/config.yaml
sed -i "s|down: [0-9]*mbps|down: ${DOWN}mbps|" /etc/web/config.yaml

# ── Generate self-signed certificate ───────────────────────────────
cat > /tmp/ssl.cnf <<EOF
[req]
distinguished_name = req_dn
x509_extensions = v3_ext
prompt = no

[req_dn]
CN = ${DOMAIN}

[v3_ext]
subjectAltName = DNS:${DOMAIN},DNS:*.${DOMAIN}
basicConstraints = CA:TRUE
keyUsage = digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
EOF

openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 \
    -days 3650 -nodes \
    -keyout /etc/web/a.key \
    -out /etc/web/a.crt \
    -config /tmp/ssl.cnf \
    2>/dev/null
rm -f /tmp/ssl.cnf

# ── Wait before starting server ────────────────────────────────────
sleep 60

# ── Start backend service ──────────────────────────────────────────
/usr/local/bin/app server -c /etc/web/config.yaml --log-level=error &

cd /app
export PORT=8080
export HOSTNAME="0.0.0.0"
exec node server.js
