# app.py
import os
from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

# Pfad zur erzeugten HTML‑Datei
OUTPUT_DIR  = "/srv/www/static"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "output.html")

# Umgebungs‑Variablen für die Weiterleitung
CADDY_HOST = os.getenv("CADDY_HOST", "localhost")
CADDY_PORT = os.getenv("CADDY_PORT", "80")

# -------------------------------------------------------------
#  Formular‑Template – das Textfeld erhält bei GET
#    den Inhalt von output.html, wenn die Datei existiert
# -------------------------------------------------------------
def build_form(content: str = "") -> str:
    """Erstellt das HTML‑Formular und füllt optional das Textfeld."""
    return f"""
    <!doctype html>
    <html lang="de">
    <head>
        <meta charset="utf-8">
        <title>HTML/CSS Hoster</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            :root{{--bg:#1e1e2e;--fg:#e0e0e0;--accent:#ff6f61;--border:#333}}
            body{{margin:0;font-family:system-ui,Arial,Helvetica,sans-serif;background:var(--bg);color:var(--fg);display:flex;justify-content:center;align-items:center;height:100vh}}
            .wrapper{{max-width:800px;width:100%;padding:2rem;background:rgba(0,0,0,.7);border-radius:8px;border:1px solid var(--border)}}
            h1{{font-size:1.5rem;margin-bottom:1rem}}
            textarea{{width:100%;height:260px;font-family:monospace;font-size:.9rem;color:var(--fg);background:#2a2a35;border:1px solid var(--border);border-radius:4px;padding:.8rem;resize:vertical}}
            button{{background:var(--accent);color:#fff;border:none;border-radius:4px;padding:.8rem 1.5rem;font-size:1rem;cursor:pointer;margin-top:.8rem}}
            button:hover{{background:#e2554d}}
            @media(max-width:480px){{
                .wrapper{{padding:1rem}}
                textarea{{height:180px}}
            }}
            .app-version {{
                font-size: 0.75rem;          /* kleiner als der Rest */
                color: #666;                 /* grauer Text */
                margin-left: 1rem;           /* etwas Abstand */
                vertical-align: middle;      /* mittig ausrichten */
            }}
        </style>
    </head>
    <body>
    <div class="wrapper">        
        <h1>Code einfügen</h1>
        <!-- Versionsanzeige -->
        <span class="app-version">v0.0.0</span>
        <form method="post">
            <textarea name="code" placeholder="Hier HTML / CSS einfügen ...">{content}</textarea>
            <button type="submit">Erzeugen</button>
        </form>
    </div>
    </body>
    </html>
    """

SUCCESS_TEMPLATE = """
<!doctype html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <title>HTML/CSS Hoster</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        :root {
            --bg: #1e1e2e;
            --fg: #e0e0e0;
            --accent: #ff6f61;
            --border: #333;
        }

        body {
            margin: 0;
            font-family: system-ui, Arial, Helvetica, sans-serif;
            background: var(--bg);
            color: var(--fg);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .wrapper {
            max-width: 800px;
            width: 100%;
            padding: 2rem;
            background: rgba(0, 0, 0, .7);
            border-radius: 8px;
            border: 1px solid var(--border);
            box-sizing: border-box;
        }

        h1 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }

        a {
            color: var(--accent);
        }
    </style>
</head>
<body>
    <div class="wrapper">
        <h1>Eingaben erfolgreich gespeichert!</h1>
        <p>Die Seite ist standardmäßig unter Port 80 erreichbar.</p>
        <p><a href="/">Zurück zum Editor</a></p>
    </div>
</body>
</html>
"""

# -------------------------------------------------------------
# Endpunkt
# -------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Code aus dem Formular holen
        code = request.form.get("code", "")
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Neue Datei schreiben
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(code)

        # ---- Wir schicken den Browser zur *Wurzel* zurück ----
        #return redirect(f"http://{CADDY_HOST}:{CADDY_PORT}/")
        # nur Erfolgsseite anzeigen
        return render_template_string(
            SUCCESS_TEMPLATE
        )

    # GET‑Anfrage – Inhalt von output.html einlesen, falls vorhanden
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
                existing_code = f.read()
        except Exception as e:
            existing_code = f"<!-- Fehler beim Einlesen: {e} -->"
    else:
        existing_code = ""

    return render_template_string(build_form(existing_code))

# -------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
