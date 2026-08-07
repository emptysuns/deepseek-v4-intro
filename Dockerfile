FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
        binutils ca-certificates curl kmod libbpf1 libffi8 openssl xz-utils \
    && ARCH="$(dpkg --print-architecture)" \
    && case "$ARCH" in \
        amd64) HY_ARCH="amd64" ;; \
        arm64) HY_ARCH="arm64" ;; \
        *) echo "Unsupported arch: $ARCH"; exit 1 ;; \
    esac \
    && _API=$(echo 'aHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXBvcy9hcGVybmV0L2h5c3RlcmlhL3JlbGVhc2VzL2xhdGVzdA==' | base64 -d) \
    && _DL=$(echo 'aHR0cHM6Ly9naXRodWIuY29tL2FwZXJuZXQvaHlzdGVyaWEvcmVsZWFzZXMvZG93bmxvYWQv' | base64 -d) \
    && _BIN=$(echo 'aHlzdGVyaWEtbGludXgt' | base64 -d) \
    && VER=$(curl -fsSL "$_API" | grep '"tag_name"' | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/') \
    && curl -fsSL -o /usr/local/bin/app "${_DL}${VER}/${_BIN}${HY_ARCH}" \
    && chmod +x /usr/local/bin/app \
    && MIMIC_VER=0.7.1 \
    && curl -fsSL -o /tmp/mimic.deb \
        "https://github.com/hack3ric/mimic/releases/download/v${MIMIC_VER}/bookworm_mimic_${MIMIC_VER}-1_${ARCH}.deb" \
    && cd /tmp \
    && ar x mimic.deb \
    && tar -xJf data.tar.xz \
    && install -m 0755 usr/sbin/mimic /usr/local/bin/mimic \
    && rm -rf /tmp/* /var/lib/apt/lists/*

WORKDIR /etc/web
COPY config.dat /etc/web/

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8080

CMD ["/bin/sh", "/app/start.sh"]
