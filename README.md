# Power BI Einstieg

Ein kostenloser, deutschsprachiger Einsteiger-Pfad für Power BI Desktop:
von der Installation bis zum ersten fertigen Dashboard, in gut zwei Stunden.

**Zielgruppe:** Absolute Anfänger ohne Vorerfahrung.
**Live-Seite:** *(Link eintragen, sobald veröffentlicht)*

## Aufbau

Ein Template, vier Cases. Die Anleitung existiert genau einmal — in
`content/_template/` mit Platzhaltern. Jeder Case liefert nur Werte, keine
eigene Struktur, keine eigenen Klickpfade.

```
data/           simulierte CSV je Case (erzeugt, aber eingecheckt —
                die Anleitung lädt sie über raw.githubusercontent)
generator/      generate.py · verify.py · render.py + Parametersätze
content/        _template/ (Quelle) · <case>/ (gerendert) · werte/ (Kontrollzahlen)
checkpoints/    nur Doku — die .pbix-Dateien hängen an einem GitHub-Release
powerbi/        PBIP-Projekt für den Checkpoint nach Modul 2 (Text, kein .pbix)
```

## Bauen

```bash
python generator/generate.py  business   # CSV erzeugen (Seed 42)
python generator/verify.py    business   # Kontrollzahlen aus der CSV errechnen
python generator/render.py    business   # Templates rendern -> content/business/
python generator/build_pbip.py business  # Checkpoint-Projekt -> powerbi/geputzt/
```

Braucht Python 3.10+ und `pyyaml`.

Die drei Skripte müssen **in dieser Reihenfolge** laufen. `render.py` bricht ab,
wenn ein Platzhalter im Template keinen Wert hat — damit kann keine Kontrollzahl
versehentlich von Hand im Text landen.

## Grundregeln

- **Seed 42 und die Zeilenzahl nie ändern.** Alle Kontrollzahlen in den Texten
  hängen daran. Ändert sich die CSV, müssen `verify.py` und `render.py` neu
  laufen — und die .pbix-Checkpoints neu erzeugt werden.
- **Kontrollzahlen nie von Hand schreiben.** Nur Platzhalter aus
  `content/werte/<case>.yaml`.
- **Keine .pbix-Dateien committen.** Binärdateien blähen die Historie auf; sie
  gehören als Release-Assets ans Repo (siehe `checkpoints/README.md`).
- **Screenshots minimal.** Klickpfade stehen als Text im Format
  „Menüband → Start → Daten transformieren". Screenshots veralten monatlich.
- **Alles simuliert.** Keine echten Datenquellen — keine Lizenz-, keine
  Pflegefragen.

## Status

| Case | Stand |
|---|---|
| 💼 Business | v1 fertig |
| 🎮 Spiele | Parametersatz skizziert |
| 🏠 Haushalt | Parametersatz skizziert |
| 🎒 Reise | Parametersatz skizziert |

Cases 2–4 brauchen zusätzlich eine Erweiterung von `generate.py` — der
Generator kennt derzeit nur die Spaltenstruktur von Case 1.

## Lizenz

Inhalte (`content/`, `data/`): [CC BY 4.0](LICENSE).
Code (`generator/`): MIT, siehe [LICENSE](LICENSE).
