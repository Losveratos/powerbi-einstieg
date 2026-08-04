# Checkpoint-Dateien

Hier liegen **keine** Dateien. `.pbix` sind Binärdateien — jede Version würde
komplett neu in der Git-Historie landen und das Repo unbrauchbar aufblähen.

Die Checkpoint-Dateien hängen stattdessen als **Release-Assets** am Repo. Die
Links in den Anleitungsseiten zeigen auf `releases/latest/download/…` und
bleiben damit auch nach einem neuen Release stabil.

## Welche Dateien gebraucht werden

Pro Case genau drei:

| Datei | Stand | Verlinkt in |
|---|---|---|
| `business_checkpoint_geputzt.pbix` | nach Modul 2 (häufigster Frustpunkt) | Modul 2, Modul 3 |
| `business_checkpoint_visuals.pbix` | nach Modul 4 | Modul 4, Modul 5 |
| `business_fertig.pbix` | Endstand nach Modul 6 | Modul 6 („Ziel ansehen") |

Zusätzlich sollte die CSV selbst am Release hängen — Modul 1 verlinkt sie als
Notausgang, falls der Web-Abruf beim Lernenden nicht funktioniert:

| Datei | Quelle |
|---|---|
| `verkaeufe_2025.csv` | `data/business/verkaeufe_2025.csv` (unverändert) |

## So werden sie erzeugt

Das geht nur von Hand, an einem **deutschsprachigen Windows** mit Power BI
Desktop — die Klickpfade und die Zahlenformate der Anleitung beziehen sich
genau darauf.

1. Den Pfad einmal selbst durchklicken, exakt so, wie er in
   `content/business/` steht.
2. Nach **Modul 2** speichern als `business_checkpoint_geputzt.pbix`.
3. Nach **Modul 4** speichern als `business_checkpoint_visuals.pbix`.
4. Nach **Modul 6** speichern als `business_fertig.pbix`.
5. Dabei prüfen, ob die Zahlen in Power BI mit `content/werte/business.yaml`
   übereinstimmen — besonders bei den Gebietsschema-Umwandlungen in Modul 2.

Aufwand: rund ein halber bis ein Tag, inklusive Screenshots.

## Release anlegen

```bash
gh release create v1.0 \
  business_checkpoint_geputzt.pbix \
  business_checkpoint_visuals.pbix \
  business_fertig.pbix \
  data/business/verkaeufe_2025.csv \
  --title "Business-Case v1" \
  --notes "Checkpoint-Dateien zum Einsteiger-Pfad, Case Business."
```

Danach die Links in den gerenderten Seiten einmal durchklicken.

## Wichtig bei Änderungen

Ändert sich die CSV — also Seed, Zeilenzahl oder ein Parameter in
`generator/cases/business.yaml` — ändern sich alle Kontrollzahlen. Dann müssen
**alle drei .pbix-Dateien neu erzeugt** werden. Deshalb: Seed und Zeilenzahl
liegen fest.
