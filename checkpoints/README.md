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

Gearbeitet wird an einem **deutschsprachigen Windows** mit Power BI Desktop —
die Klickpfade und die Zahlenformate der Anleitung beziehen sich genau darauf.

### Checkpoint 1 ist vorgebaut

`business_checkpoint_geputzt.pbix` musst du **nicht** durchklicken. Das Projekt
liegt fertig als PBIP unter `powerbi/geputzt/` — mit Datenquelle, allen acht
Power-Query-Handgriffen aus Modul 2 und den fertigen Spaltentypen.

```bash
python generator/build_pbip.py business   # erzeugt/aktualisiert powerbi/geputzt/
```

1. `powerbi/geputzt/geputzt.pbip` per Doppelklick in Power BI Desktop öffnen.
2. **Start → Aktualisieren**. Die Daten werden von GitHub geladen — das geht
   erst, wenn das Repo öffentlich online ist.
3. Prüfen: **2.400 Zeilen**, 6 Spalten, Auftragsdatum als Datum, Umsatz und
   Marge als Dezimalzahl. Rechts in **Angewendete Schritte** stehen dieselben
   acht Handgriffe wie in Modul 2.
4. **Datei → Speichern unter** → `business_checkpoint_geputzt.pbix`.

### Checkpoint 2 und 3 von Hand

Die beiden anderen Stände entstehen durch Weiterklicken ab Checkpoint 1:

1. Ab **Modul 3** der Anleitung folgen, exakt so, wie sie in
   `content/business/` steht.
2. Nach **Modul 4** speichern als `business_checkpoint_visuals.pbix`.
3. Nach **Modul 6** speichern als `business_fertig.pbix`.
4. Dabei prüfen, ob die Zahlen in Power BI mit `content/werte/business.yaml`
   übereinstimmen — besonders die Karte in Modul 3 (`gesamtwert`) und der
   Mittelwert in Modul 5 (`richtige_zahl`).

Aufwand: rund zwei bis drei Stunden statt eines Tages, weil der aufwändigste
Teil — Datenanbindung und Power Query — schon steht.

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
