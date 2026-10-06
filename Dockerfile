# ---- Build‑Stufe ----
FROM python:3.11-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg && rm -rf /var/lib/apt/lists/*

ENV CADDY_VERSION=2.11.7
RUN curl -sL "https://github.com/caddyserver/caddy/releases/download/v${CADDY_VERSION}/caddy_${CADDY_VERSION}_linux_amd64.tar.gz" | \
    tar -xzC /usr/bin caddy

# ---- Lauf‑Stufe ----
FROM python:3.11-slim

COPY --from=builder /usr/bin/caddy /usr/bin/caddy

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app.py /app/app.py
COPY Caddyfile /etc/caddy/Caddyfile
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

RUN mkdir -p /srv/www/static

EXPOSE 80 5001

WORKDIR /app
CMD ["./start.sh"]
