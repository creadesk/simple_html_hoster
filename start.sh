#!/usr/bin/env bash
set -e

# Caddy in den Hintergrund starten
caddy run --config /etc/caddy/Caddyfile --adapter caddyfile &

# Flask‑App starten (der `exec` ersetzt das Shell‑Prozess‑Image)
exec python /app/app.py