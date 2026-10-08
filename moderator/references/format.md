# Darstellung

## Chat / Desktop: dauerhafter Standard

Zuerst notwendige Aktionen für Hendrik in nativem Markdown; danach kompakte Ampel-Karten, nach Projekten gruppiert, mit aufklappbaren Details. Dieser Standard gilt auch nach einem Neustart und bei `$moderator`, bis Hendrik ausdrücklich eine andere Darstellung wählt. Kein zusätzliches Management-Summary vor der menschlichen Liste.

### Menschliche Aktionen

- Kurzer Kopf mit Prüfzeit, Sichtgrenze und validierter Snapshot-Kennung.
- Nur nach dem Mensch-Filter belegte Aktionen nummerieren. Projekt/Task-ID, konkretes Verb und nötige Antwort nennen; Quellen oder vorbereitete Ergebnisse direkt verlinken.
- Möglichst zwei kurze Zeilen pro Aktion, keine breite Tabelle. Keine Pflichtaktionen erfinden, um die Liste zu füllen.
- Ohne menschliche Aktion: `Bei dir: Im geprüften Umfang keine Aktion nötig.` Offene Agentenarbeit bleibt darunter sichtbar.
- Viele notwendige Aktionen nach `Jetzt` und `Danach` gliedern, keine stillen Kürzungen.

### Ampel-Karten

Den verfügbaren visualize-Skill vollständig lesen und dessen Inline-Ausgabeweg benutzen. Eine Darstellung im Chat ist kein Website-/Exportauftrag. Die aktuelle task-eigene Darstellung aktualisieren und ihre visualize-Referenz in derselben finalen Antwort zeigen. Keine zusätzliche Statusdatei oder Aufgabenverwaltung erzeugen.

- Ein kompakter Projektbereich mit verständlichem Namen, darunter die zugehörigen Unteraufgaben. Desktop: zwei Bereiche nebeneinander, soweit lesbar; auf schmalen Ansichten untereinander. Keine fixen Außenbreiten, internen Scrollflächen oder verschachtelten Karten.
- Jede Unteraufgabe hat einen kleinen Ampelpunkt, das ausgeschriebene Statuswort, ihre stabile Referenz und einen kurzen Ergebnistitel.
- Jede Unteraufgabe erhält eine eigene, optisch deutlich getrennte Box: native `.card`-Fläche, Abstand zwischen Aufgaben und Projektgruppen, keine Karten ineinander. Ampel und aufklappbare Details bleiben erhalten; auf schmalen Ansichten stapeln.
- Direkt unter dem Titel einen sichtbaren Link `Aufgabe öffnen ↗` zum bestehenden Arbeitschat anbieten. Ziel ausschließlich aus der belegten Chat-ID ableiten (`codex://threads/<threadId>`), niemals aus einem Cockpit-Alias. Mehrere Unteraufgaben desselben Chats dürfen auf denselben Chat zeigen. Ist kein direkter Link verfügbar, die Grenze kurz nennen; keinen Share-Link erzeugen oder neuen Chat anlegen. Der Klick öffnet nur den Chat und sendet keine Fortsetzung.
- Direkt sichtbar: kurzer Sachkontext (`Worum geht es?`) und nächster konkreter Schritt in der aufklappbaren Zusammenfassung. Projektnamen oder Fachbegriffe allein reichen nicht.
- Native, zunächst geschlossene `<details>` mit verständlichem `<summary>` verwenden, z. B. `Nächster Schritt · Archivzugang`. Darin bei Bedarf Handlung, Akteur, konkrete Voraussetzung, Quellen und Prüfgrenzen erklären.
- Essenzielle Blockade, menschliche Aktion und Ergebnisgrenze dürfen nicht ausschließlich im aufgeklappten Bereich stehen. Quellen klickbar beim zugehörigen Task halten; keine geheimen Daten oder unnötigen Personendetails.
- Farben an das aktuelle helle/dunkle Thema anpassen; unaufdringliche Flächen, gut lesbarer Text und sparsame Abstände. Keine dekorativen Fortschrittsbalken, erfundenen Prozentwerte oder Scores.

| Farbe | Statuswort | Bedeutung |
| --- | --- | --- |
| Grün | FERTIG | Genau beauftragtes Ergebnis passend verifiziert |
| Gelb | AKTIV | Aktuelle Bearbeitung belegt |
| Gelb | BEREIT | Ausführbar, kein laufender Bearbeiter belegt |
| Gelb | WARTET | Konkrete Rückmeldung oder Nachweis ausstehend |
| Rot | BLOCKIERT | Benannte notwendige Voraussetzung fehlt |
| Grau | PAUSIERT | Bewusst zurückgestellt |
| Grau | UNKLAR | Status nicht ausreichend belegt |

Farbe niemals ohne Statuswort. `PAUSIERT` und `UNKLAR` sowie die drei gelben Zustände ausdrücklich unterscheiden. Keine grünen Gesamtprojekte wegen einzelner fertiger Teilaufgaben.

**Synthetisches Inhaltsmuster – keine tatsächlichen Projektstände:**

- Projekt Alpha · `WARTET · 10.01` · Pilotumfang festlegen
- Kontext: Der Pilot braucht einen fachlich festgelegten Umfang.
- Eingeklappte Zusammenfassung: `Nächster Schritt · deine Auswahl`
- Aufgeklappt: Hendrik wählt A oder B; dadurch kann der bestehende Pilot weiter vorbereitet werden. Konkrete Quelle und Prüfzeit zuordnen.

Ein früheres HTML oder dieses Muster liefert ausschließlich die Gestaltung. Aufgaben, Akteure, Zahlen und Statuswerte immer aus dem autorisierten aktuellen Bestand und seinen Quellen ableiten. Alte Vorschauinhalte niemals übernehmen.

### Abschlüsse und Abnahmen

Abgeschlossene Hauptprojekte verlassen die offene Übersicht. Neu bestätigte Abschlüsse kurz in einem getrennten Bereich melden, danach entfernen; ältere nur auf Nachfrage. Eine offene Unterschrift, Entscheidung oder Abnahme bleibt nur dann als solche sichtbar, wenn sie nachweislich erforderlich ist. Erstellung, technische Prüfung und fachliche Abnahme sind unterschiedliche Ergebnisse. Den genau beauftragten Endzustand nach dem ursprünglichen Auftrag bewerten.

### Bewusste Alternativen

- `nur ich`: nur menschliche Aktionen in Markdown, keine Karten; Sichtgrenze erhalten.
- `status`: nur Projektkarten; `delta`/Projektfilter behalten die Karten für den gewählten Ausschnitt.
- `Baum`, `Text`, Terminal oder konkret fehlende Inline-Unterstützung: natives Markdown mit schmalem Unicode-Baum. Falls technisch nötig, den Ersatz knapp benennen; nach Rückkehr zur Desktop-Unterstützung wieder Karten verwenden. Ein technischer Ersatz ändert die dauerhafte Nutzerwahl nicht.
- Quellen außerhalb von Codeblöcken direkt zuordnen. Kurze Titel, echte Zeilenumbrüche, keine gepaddeten rechten Ränder oder Emoji-Spaltenausrichtung.

Keine reine Codeblock-/Baumübersicht als stiller Ersatz für die gewählten Ampel-Karten. Keine Gesamtpunktzahl, animierten Balken oder geschätzten Restzeiten. `NEU` bezeichnet eine belegte Änderung zur letzten vergleichbaren Ausgabe.
