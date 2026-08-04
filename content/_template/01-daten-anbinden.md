# Modul 1 · Daten anbinden

*Etwa 15 Minuten*

## Ziel dieses Moduls

Die Datei `{{datei_name}}` liegt in Power BI und du hast einmal draufgeschaut.

## So geht's

1. Klicke im Menüband auf **Start → Daten abrufen**. Es klappt eine Liste auf.
2. Wähle darin **Web**. (Steht es nicht in der Liste: **Mehr…** ganz unten,
   dann links **Andere**, dann **Web**.)
3. Ein Fenster **Aus dem Web** geht auf. Kopiere diese Adresse in das Feld **URL**:

   ```
   {{csv_url}}
   ```

   Klick dann auf **OK**.
4. Jetzt fragt Power BI, wie es sich anmelden soll. Wähle links **Anonym** und
   klick auf **Verbinden**. Anonym heißt: Die Datei ist öffentlich, es braucht
   kein Passwort.
5. Du siehst eine Vorschau der Daten. Sie sieht unordentlich aus — die Spalten
   heißen `Column1`, `Column2` und so weiter, und in der ersten Zeile steht
   Kauderwelsch. **Das ist so gewollt.** Genau das räumen wir im nächsten Modul auf.
6. Klick unten rechts auf **Laden**. Nicht auf „Daten transformieren" — das
   kommt gleich.
7. Rechts erscheint der Bereich **Daten**, darin die Tabelle **{{tabellen_name}}**.
   Klick darauf, dann klappen die Spalten auf.
8. Schau dir die Tabelle einmal ganz an: Klick links am Bildschirmrand auf das
   mittlere der drei Symbole — die **Tabellenansicht** (ein Gittersymbol).
   Jetzt siehst du die Daten wie in einer Tabelle.

## 📖 Neues Wort

**Zeile und Spalte.** Eine **Zeile** ist ein einzelner Vorgang — hier: ein
Auftrag. Eine **Spalte** ist eine Eigenschaft, die jeder Vorgang hat — hier zum
Beispiel das Datum oder die Region. Alles, was du gleich baust, beruht auf
dieser einen Idee.

## ✅ Kontrollpunkt

> Ganz unten am Bildschirmrand steht: **{{tabellen_name}} ({{zeilen_roh}} Zeilen)**.
>
> Steht da was anderes? → Häufigste Ursache: Bei der Anmeldung war nicht
> **Anonym** ausgewählt, oder die Adresse wurde beim Kopieren abgeschnitten.
> Lösch die Abfrage rechts (Rechtsklick auf **{{tabellen_name}}** → **Aus Bericht
> löschen**) und fang bei Schritt 1 neu an.
>
> Geht es gar nicht? Lade die Datei stattdessen herunter
> ([{{datei_name}}]({{download_url}})) und binde sie über
> **Start → Daten abrufen → Text/CSV** ein. Der Rest der Anleitung bleibt gleich.

## Weiter

→ [Modul 2 · Aufräumen](02-aufraeumen.md)
