#!/usr/bin/env python3
"""Baut aus den gerenderten Modulseiten eine HTML-Seite im Kitchen-Look.

    python generator/build_site.py business

Liest content/<case>/*.md, wandelt sie nach HTML und setzt sie zu EINER Seite
zusammen: site/powerbi_praxis_pfad.html. Alles auf einer Seite, weil der Pfad
in einem Zug durchgearbeitet wird - Sprungmarken statt Seitenwechsel.

Die Bildverweise stehen als HTML-Kommentar im Markdown:
    <!-- BILD: dateiname | Bildunterschrift -->
So bleibt die Markdown-Fassung ohne kaputte Bildpfade lesbar.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

import markdown
import yaml

WURZEL = Path(__file__).resolve().parent.parent
BILDPFAD = "assets/praxis-pfad"

# Dateiname -> (Anker, Kurztitel fuer die Navigation)
MODULE = [
    ("00-installieren.md",      "modul-0", "Installieren"),
    ("01-daten-anbinden.md",    "modul-1", "Daten anbinden"),
    ("02-aufraeumen.md",        "modul-2", "Aufräumen"),
    ("03-erste-antworten.md",   "modul-3", "Erste Antworten"),
    ("04-filtern.md",           "modul-4", "Filtern"),
    ("05-aggregation.md",       "modul-5", "Aggregation"),
    ("06-fertig-machen.md",     "modul-6", "Fertig machen"),
    ("exkurs-kreuztabelle.md",  "exkurs",  "Exkurs"),
]

BILD = re.compile(r"<!--\s*BILD:\s*([\w-]+)\s*\|\s*(.+?)\s*-->", re.DOTALL)


def bilder_ersetzen(text: str) -> str:
    def figur(treffer: re.Match) -> str:
        name, beschriftung = treffer.group(1), treffer.group(2).strip()
        return (
            f'<figure class="pp-shot">'
            f'<img src="{BILDPFAD}/{name}.png" alt="{html.escape(beschriftung)}" loading="lazy">'
            f'<figcaption>{html.escape(beschriftung)}</figcaption>'
            f"</figure>"
        )
    return BILD.sub(figur, text)


def kontrollpunkte(inhalt: str) -> str:
    """Der Kontrollpunkt besteht aus Überschrift + Zitatblock. Das Wort
    'Kontrollpunkt' steht in der ÜBERSCHRIFT, nicht im Block - deshalb muss
    das Paar zusammen gefunden werden."""
    return re.sub(
        r"<h2>(\s*✅[^<]*)</h2>\s*<blockquote>",
        r'<h2 class="pp-check-titel">\1</h2>\n<blockquote class="pp-check">',
        inhalt,
    )


def begriffe(inhalt: str) -> str:
    """Fasst '📖 Neues Wort' und die Erklärung darunter zu einer Box zusammen -
    die sieben Begriffe sind ein Kernstück des Pfads und sollen auffallen."""
    return re.sub(
        r"<h2>\s*📖([^<]*)</h2>\s*<p>(.*?)</p>",
        r'<div class="pp-wort"><div class="pp-wort-label">📖\1</div><p>\2</p></div>',
        inhalt,
        flags=re.DOTALL,
    )


def bloecke_auszeichnen(inhalt: str) -> str:
    """Gibt den übrigen Zitatblöcken je nach Inhalt eine eigene Klasse.
    Bereits klassifizierte Blöcke (<blockquote class=...>) bleiben unberührt,
    weil das Muster nur auf '<blockquote>' ohne Attribute passt."""
    def klassifizieren(treffer: re.Match) -> str:
        block = treffer.group(0)
        if "Kontrollpunkt" in block:
            klasse = "pp-check"
        elif "⚠️" in block:
            klasse = "pp-warn"
        elif "Für Genaue" in block or "Warum der Umweg" in block:
            klasse = "pp-note"
        else:
            klasse = "pp-tip"
        return block.replace("<blockquote>", f'<blockquote class="{klasse}">', 1)
    return re.sub(r"<blockquote>.*?</blockquote>", klassifizieren, inhalt, flags=re.DOTALL)


def links_umbiegen(inhalt: str) -> str:
    """Aus Dateilinks zwischen den Modulen werden Sprungmarken."""
    for datei, anker, _ in MODULE:
        inhalt = inhalt.replace(f'href="{datei}"', f'href="#{anker}"')
    return inhalt


def modul_html(pfad: Path, anker: str) -> str:
    roh = bilder_ersetzen(pfad.read_text(encoding="utf-8"))
    inhalt = markdown.markdown(roh, extensions=["tables", "fenced_code", "sane_lists"])
    inhalt = links_umbiegen(inhalt)
    inhalt = begriffe(kontrollpunkte(inhalt))
    inhalt = bloecke_auszeichnen(inhalt)
    # Die H1 der Moduldatei wird zur Section-Ueberschrift.
    inhalt = inhalt.replace("<h1>", '<h2 class="pp-modul-titel">', 1)
    inhalt = inhalt.replace("</h1>", "</h2>", 1)
    return f'<section class="pp-modul" id="{anker}">\n{inhalt}\n</section>'


def seite_bauen(case: str, werte: dict) -> str:
    ordner = WURZEL / "content" / case
    teile = []
    for datei, anker, _ in MODULE:
        pfad = ordner / datei
        if not pfad.exists():
            print(f"  fehlt: {datei}", file=sys.stderr)
            continue
        teile.append(modul_html(pfad, anker))

    nav = "\n".join(
        f'      <a class="pp-nav-item" href="#{anker}">'
        f'<span class="pp-nav-num">{i if i < 7 else "Ex"}</span>'
        f'<span class="pp-nav-name">{titel}</span></a>'
        for i, (_, anker, titel) in enumerate(MODULE)
    )

    return SEITE.format(
        titel=werte["titel"],
        nav=nav,
        module="\n\n".join(teile),
        csv_url=werte["csv_url"],
        fertig=werte["checkpoint_fertig"],
    )


SEITE = """<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Power BI Praxis-Pfad · {titel} · Knowledge Kitchen</title>
<meta name="description" content="Von null zum ersten fertigen Power-BI-Dashboard in gut zwei Stunden. Kostenlos, ohne Konto, ohne Vorkenntnisse.">
<style>
:root {{
  --bg:        #FAFAF5;
  --bg-card:   #FFFFFF;
  --bg-soft:   #F4F1E8;
  --ink:       #1A1A1A;
  --ink-soft:  #4A4A4A;
  --ink-mute:  #6B6B6B;
  --line:      #E5E2D8;
  --line-strong: #1A1A1A;
  --akzent:    #C0392B;
  --akzent-soft: #FDF0EE;
  --gruen:     #2A857A;
  --gruen-soft:#EDF6F4;
  --blau:      #1E3A5F;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; background: var(--bg); color: var(--ink);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 17px; line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}}
.pp-wrap {{ max-width: 780px; margin: 0 auto; padding: 0 20px 100px; }}

/* Kopf */
.pp-hero {{ padding: 72px 0 40px; border-bottom: 2px solid var(--line-strong); }}
.pp-eyebrow {{
  font-size: 12px; letter-spacing: .14em; text-transform: uppercase;
  color: var(--ink-mute); font-weight: 600; margin-bottom: 18px;
}}
.pp-hero h1 {{ font-size: clamp(34px, 6vw, 52px); line-height: 1.1; margin: 0 0 20px; font-weight: 700; }}
.pp-hero h1 em {{ font-style: italic; color: var(--akzent); }}
.pp-lead {{ font-size: 20px; color: var(--ink-soft); margin: 0 0 28px; }}
.pp-meta {{ display: flex; flex-wrap: wrap; gap: 10px; }}
.pp-badge {{
  background: var(--bg-soft); border: 1px solid var(--line); border-radius: 100px;
  padding: 6px 14px; font-size: 13px; font-weight: 600; color: var(--ink-soft);
}}

/* Warnkasten */
.pp-hinweis {{
  background: var(--akzent-soft); border: 1px solid #F3C9C3;
  border-left: 4px solid var(--akzent);
  border-radius: 8px; padding: 18px 22px; margin: 32px 0;
}}
.pp-hinweis strong {{ color: var(--akzent); }}

/* Navigation */
.pp-nav {{ margin: 40px 0 0; }}
.pp-nav-titel {{ font-size: 13px; letter-spacing: .1em; text-transform: uppercase; color: var(--ink-mute); font-weight: 600; margin-bottom: 14px; }}
.pp-nav-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 8px; }}
.pp-nav-item {{
  display: flex; align-items: center; gap: 12px; text-decoration: none;
  background: var(--bg-card); border: 1px solid var(--line); border-radius: 8px;
  padding: 12px 14px; color: var(--ink); transition: border-color .15s, transform .15s;
}}
.pp-nav-item:hover {{ border-color: var(--line-strong); transform: translateY(-1px); }}
.pp-nav-num {{
  flex: 0 0 28px; height: 28px; border-radius: 50%; background: var(--bg-soft);
  display: grid; place-items: center; font-size: 13px; font-weight: 700; color: var(--ink-soft);
}}
.pp-nav-name {{ font-size: 15px; font-weight: 600; }}

/* Module */
.pp-modul {{ padding: 56px 0 8px; border-bottom: 1px solid var(--line); scroll-margin-top: 20px; }}
.pp-modul-titel {{ font-size: clamp(26px, 4vw, 34px); line-height: 1.2; margin: 0 0 6px; font-weight: 700; }}
.pp-modul h2 {{ font-size: 22px; margin: 36px 0 10px; font-weight: 700; }}
.pp-modul h3 {{ font-size: 18px; margin: 28px 0 8px; font-weight: 700; color: var(--ink-soft); }}
.pp-modul p {{ margin: 0 0 16px; }}
.pp-modul em {{ color: var(--ink-mute); }}
.pp-modul ol, .pp-modul ul {{ margin: 0 0 18px; padding-left: 24px; }}
.pp-modul li {{ margin-bottom: 10px; }}
.pp-modul strong {{ font-weight: 700; }}
.pp-modul a {{ color: var(--blau); text-decoration: underline; text-underline-offset: 2px; }}
.pp-modul code {{
  background: var(--bg-soft); border: 1px solid var(--line); border-radius: 4px;
  padding: 1px 6px; font-size: .88em; font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}}
.pp-modul pre {{
  background: #1A1A1A; color: #F4F1E8; border-radius: 8px; padding: 16px 18px;
  overflow-x: auto; font-size: 13px; line-height: 1.5;
}}
.pp-modul pre code {{ background: none; border: none; padding: 0; color: inherit; }}
.pp-modul table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 15px; }}
.pp-modul th, .pp-modul td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--line); vertical-align: top; }}
.pp-modul th {{ background: var(--bg-soft); font-weight: 700; }}

/* Zitatblöcke nach Zweck */
blockquote {{ margin: 22px 0; padding: 16px 20px; border-radius: 8px; border-left: 4px solid var(--line-strong); background: var(--bg-card); border: 1px solid var(--line); }}
blockquote p {{ margin: 0 0 10px; }}
blockquote p:last-child {{ margin-bottom: 0; }}
blockquote.pp-check {{ background: var(--gruen-soft); border-color: #BEE0DA; border-left: 4px solid var(--gruen); }}
blockquote.pp-warn {{ background: var(--akzent-soft); border-color: #F3C9C3; border-left: 4px solid var(--akzent); }}
blockquote.pp-note {{ background: var(--bg-soft); border-left: 4px solid var(--ink-mute); }}
blockquote.pp-tip {{ background: #F5F8FB; border-color: #D6E2EE; border-left: 4px solid var(--blau); }}

/* Kontrollpunkt: Überschrift und Kasten gehören zusammen */
.pp-check-titel {{
  font-size: 17px !important; color: var(--gruen); margin: 32px 0 0 !important;
  letter-spacing: .01em;
}}
.pp-check-titel + blockquote {{ margin-top: 8px; }}

/* Neues Wort */
.pp-wort {{
  background: var(--bg-soft); border: 1px solid var(--line);
  border-radius: 10px; padding: 18px 22px; margin: 28px 0;
}}
.pp-wort-label {{
  font-size: 12px; letter-spacing: .12em; text-transform: uppercase;
  color: var(--ink-mute); font-weight: 700; margin-bottom: 8px;
}}
.pp-wort p {{ margin: 0 !important; }}

/* Screenshots */
.pp-shot {{ margin: 26px 0; }}
.pp-shot img {{
  width: 100%; height: auto; display: block;
  border: 1px solid var(--line); border-radius: 8px; background: #fff;
}}
.pp-shot figcaption {{ font-size: 14px; color: var(--ink-mute); margin-top: 8px; }}

/* Fuss */
.pp-foot {{ margin-top: 56px; padding-top: 28px; border-top: 2px solid var(--line-strong); font-size: 15px; color: var(--ink-mute); }}
.pp-foot a {{ color: var(--blau); }}

@media (max-width: 640px) {{
  body {{ font-size: 16px; }}
  .pp-hero {{ padding: 44px 0 28px; }}
  .pp-modul {{ padding: 40px 0 8px; }}
}}
</style>
</head>
<body>
<div class="pp-wrap">

  <header class="pp-hero">
    <div class="pp-eyebrow">Praxis-Pfad · Power BI · Für absolute Anfänger</div>
    <h1>Dein erstes <em>Dashboard</em></h1>
    <p class="pp-lead">Von der Installation bis zur fertigen Auswertung — in gut zwei
    Stunden. Kostenlos, ohne Konto, ohne Vorkenntnisse. Du kannst jederzeit pausieren.</p>
    <div class="pp-meta">
      <span class="pp-badge">7 Module</span>
      <span class="pp-badge">≈ 2 Stunden</span>
      <span class="pp-badge">Kein Konto nötig</span>
      <span class="pp-badge">Rettungsdatei je Kapitel</span>
    </div>

    <div class="pp-hinweis">
      <strong>⚠️ Du brauchst einen Windows-Rechner.</strong> Power BI Desktop gibt es
      nicht für Mac, nicht fürs iPad und nicht fürs Handy. Das ist eine Entscheidung
      von Microsoft. Wenn du am Mac sitzt: Lies gern mit — mitmachen kannst du leider nicht.
    </div>

    <nav class="pp-nav">
      <div class="pp-nav-titel">Die sieben Module</div>
      <div class="pp-nav-grid">
{nav}
      </div>
    </nav>
  </header>

{module}

  <footer class="pp-foot">
    <p>Alle Kontrollzahlen in diesem Pfad sind aus den echten Daten berechnet und in
    Power BI Desktop nachgeprüft. Die Datenquelle ist simuliert:
    <a href="{csv_url}">verkaeufe_2025.csv</a>.</p>
    <p>Steckst du fest? An jedem Kontrollpunkt liegt eine fertige Datei zum
    Weitermachen. <a href="{fertig}">Den Endstand ansehen</a>.</p>
  </footer>

</div>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="HTML-Seite aus den Modulen bauen")
    parser.add_argument("case", nargs="?", default="business")
    args = parser.parse_args()

    werte_pfad = WURZEL / "content" / "werte" / f"{args.case}.yaml"
    if not werte_pfad.exists():
        print(f"Kontrollzahlen fehlen: {werte_pfad}", file=sys.stderr)
        return 1
    werte = yaml.safe_load(werte_pfad.read_text(encoding="utf-8"))

    ziel = WURZEL / "site" / "powerbi_praxis_pfad.html"
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(seite_bauen(args.case, werte), encoding="utf-8")

    kb = ziel.stat().st_size // 1024
    print(f"geschrieben: {ziel.relative_to(WURZEL)}  ({kb} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
