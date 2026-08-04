# Modul 2 · Aufräumen

*Etwa 25 Minuten · Das ist das längste Modul. Danach wird es leichter.*

## Ziel dieses Moduls

Aus der unordentlichen Datei wird eine saubere Tabelle mit richtigen
Spaltennamen und richtigen Datentypen.

## Vorher: warum überhaupt?

Rohdaten aus einem System sind nie sauber. In dieser Datei stecken fünf typische
Probleme: eine Müllzeile ganz oben, fehlende Spaltenüberschriften, leere Zeilen
mittendrin, Leerzeichen hinter manchen Werten und Zahlen, die Power BI für Text
hält. Alle fünf reparieren wir jetzt — mit **8 Handgriffen**.

## So geht's

Klick zuerst im Menüband auf **Start → Daten transformieren**. Es öffnet sich
ein neues Fenster: der **Power Query-Editor**. Hier arbeitest du das ganze Modul.

Rechts siehst du eine Liste **Angewendete Schritte**. Dort erscheint jeder
Handgriff als Eintrag. Merk dir die Liste — dazu unten mehr.

**Handgriff 1 — Müllzeile weg**
Klick auf **Start → Zeilen entfernen → Obere Zeilen entfernen**. Tippe **1** ein
und klick **OK**. Die Zeile mit dem Kauderwelsch ist weg.

**Handgriff 2 — Überschriften setzen**
Klick auf **Start → Erste Zeile als Überschrift verwenden**. Aus `Column1` wird
`Auftragsdatum`, aus `Column2` wird `Region` und so weiter.

**Handgriff 3 — leere Zeilen weg**
Klick auf **Start → Zeilen entfernen → Leere Zeilen entfernen**.

**Handgriff 4 — Leerzeichen abschneiden**
Klick oben auf die Spaltenüberschrift **Region**, sodass die Spalte markiert ist.
Dann: **Transformieren → Format → Kürzen**. Damit verschwinden die unsichtbaren
Leerzeichen hinter manchen Werten. Ohne diesen Schritt wären `Nord` und `Nord `
später zwei verschiedene Regionen.

**Handgriff 5 — Schreibweise vereinheitlichen**
Klick auf die Spaltenüberschrift **Produktgruppe**. Dann:
**Transformieren → Format → Jedes Wort großschreiben**. Aus `bürobedarf` wird
`Bürobedarf`. Auch hier gilt: Für Power BI sind Groß- und Kleinschreibung
zwei verschiedene Dinge.

**Handgriff 6 — Datum ist ein Datum**
Klick auf die Spaltenüberschrift **Auftragsdatum**. Links neben dem Namen steht
ein kleines Symbol: **ABC** — das heißt „Power BI hält das für Text". Klick auf
das Symbol und wähle **Datum**. Das Symbol wird zu einem Kalender.

**Handgriff 7 — Umsatz ist eine Zahl**
Klick auf die Spaltenüberschrift **Umsatz**. Klick jetzt **nicht** auf das
ABC-Symbol, sondern mach einen **Rechtsklick** auf die Überschrift und wähle
**Typ ändern → Gebietsschema verwenden…**.
Im Fenster stellst du ein:
- Datentyp: **Dezimalzahl**
- Gebietsschema: **Englisch (USA)**

Klick **OK**.

> Warum der Umweg? In der Datei stehen die Zahlen mit einem **Punkt** als
> Komma: `1796.80`. Dein Windows ist auf Deutsch eingestellt und liest den
> Punkt als Tausendertrennzeichen — aus 1796.80 € würden 179.680 €.
> Mit „Gebietsschema: Englisch (USA)" sagst du Power BI: *Diese Datei kommt
> aus einem englischsprachigen System, lies den Punkt als Komma.*

**Handgriff 8 — Marge ist eine Zahl**
Dasselbe noch einmal für die Spalte **Marge**: Rechtsklick auf die Überschrift →
**Typ ändern → Gebietsschema verwenden…** → Datentyp **Dezimalzahl**,
Gebietsschema **Englisch (USA)** → **OK**.

**Fertig — jetzt zurück**
Klick oben links auf **Start → Schließen & übernehmen**. Das Fenster schließt
sich und Power BI lädt die saubere Tabelle.

## Die Schrittliste ist dein Rezept

Rechts im Power Query-Editor stand die Liste **Angewendete Schritte**. Das ist
kein Protokoll, sondern ein Rezept: Power BI arbeitet diese Liste jedes Mal neu
ab, wenn die Daten aktualisiert werden. Du kannst jeden Schritt anklicken und
sehen, wie die Tabelle an dieser Stelle aussah, und du kannst jeden Schritt mit
dem **X** davor wieder löschen. Nichts, was du hier tust, ist endgültig — und
die Ursprungsdatei wird nie verändert.

## 📖 Neues Wort

**Transformation.** Eine Transformation ist ein Handgriff, der die Form der
Daten ändert, ohne die Ursprungsdatei anzufassen — zum Beispiel eine Spalte
umbenennen, Leerzeichen abschneiden oder aus Text ein Datum machen.

## ✅ Kontrollpunkt

> Klick links am Bildschirmrand auf die **Tabellenansicht** (Gittersymbol).
> Ganz unten steht: **verkaeufe_2025 (2.400 Zeilen)**.
> Die Tabelle hat **6 Spalten** mit richtigen Namen, und in der Spalte
> **Auftragsdatum** stehen Datumsangaben, keine Textzeilen.
>
> Steht da eine andere Zahl? → Häufigste Ursache: Handgriff 1 und 2 wurden
> vertauscht — die Überschriften müssen gesetzt werden, *nachdem* die Müllzeile
> weg ist. Öffne **Start → Daten transformieren**, lösch rechts in
> **Angewendete Schritte** alles außer **Quelle** und **Geänderter Typ** und
> mach ab Handgriff 1 weiter.
>
> Oder: [Checkpoint-Datei laden](https://github.com/Losveratos/powerbi-einstieg/releases/latest/download/business_checkpoint_geputzt.pbix) und mit Modul 3
> weitermachen. Öffne die Datei einfach per Doppelklick — sie ist genau auf
> diesem Stand.

## Weiter

→ [Modul 3 · Erste Antworten](03-erste-antworten.md)
