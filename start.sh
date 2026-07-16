#!/bin/sh
set -eu

# ── Environment variables ──────────────────────────────────────────
generate_uuid() {
    python3 -c 'import uuid; print(uuid.uuid4())'
}

R_ID="${R_ID:-$(generate_uuid)}"
PASSWORD="${PASSWORD:-$(generate_uuid)}"
DOMAIN="${DOMAIN:-helloworld.com}"
UP="${UP:-220}"
DOWN="${DOWN:-44}"
BACKEND_MAX_ATTEMPTS="${BACKEND_MAX_ATTEMPTS:-3}"
BACKEND_RETRY_DELAY="${BACKEND_RETRY_DELAY:-60}"

export R_ID PASSWORD DOMAIN UP DOWN BACKEND_MAX_ATTEMPTS BACKEND_RETRY_DELAY

echo "============================================"
echo " R_ID     : ${R_ID}"
echo " PASSWORD : ${PASSWORD}"
echo " DOMAIN   : ${DOMAIN}"
echo "============================================"

# ── Decode config ──────────────────────────────────────────────────
base64 -d /etc/web/config.dat > /etc/web/config.yaml
rm -f /etc/web/config.dat

# ── Patch config.yaml (base64 obfuscated) ──────────────────────────
echo 'c2VkIC1pICJzfF5saXN0ZW46LipyZWFsbTovLy4qXC8uKnxsaXN0ZW46IHJlYWxtOi8vcHVibGljQHJlYWxtLmh5Mi5pby8ke1JfSUR9fCIgL2V0Yy93ZWIvY29uZmlnLnlhbWwKc2VkIC1pICIvXiAgcGFzc3dvcmQ6L3N8cGFzc3dvcmQ6Lip8cGFzc3dvcmQ6ICR7UEFTU1dPUkR9fCIgL2V0Yy93ZWIvY29uZmlnLnlhbWwKc2VkIC1pICJzfHVwOiBbMC05XSptYnBzfHVwOiAke1VQfW1icHN8IiAvZXRjL3dlYi9jb25maWcueWFtbApzZWQgLWkgInN8ZG93bjogWzAtOV0qbWJwc3xkb3duOiAke0RPV059bWJwc3wiIC9ldGMvd2ViL2NvbmZpZy55YW1sCg==' | base64 -d | sh

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

# ── Start backend in a non-blocking retry worker ───────────────────
start_backend_with_retry() {
    attempt=1
    while [ "$attempt" -le "$BACKEND_MAX_ATTEMPTS" ]; do
        sleep "$BACKEND_RETRY_DELAY"
        echo "Starting backend service (attempt ${attempt}/${BACKEND_MAX_ATTEMPTS})"
        if /usr/local/bin/app server -c /etc/web/config.yaml --log-level=error; then
            return 0
        fi
        echo "Backend service attempt ${attempt} failed" >&2
        attempt=$((attempt + 1))
    done
    echo "Backend service failed after ${BACKEND_MAX_ATTEMPTS} attempts" >&2
    return 1
}

start_backend_with_retry &

# ── Start Streamlit ────────────────────────────────────────────────
cd /app
exec streamlit run app.py \
    --server.port=8080 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false
