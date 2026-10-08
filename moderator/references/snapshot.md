# Snapshot-Vertrag

Der Agent recherchiert und normalisiert. Der Python-Helfer validiert Struktur, Mensch-Filter, eindeutige Referenzen und Zahlen. Er greift nicht auf Konten zu, führt keine Tasks aus und speichert keinen Zustand. Seine Hash-Kennung ist eine Konsistenzhilfe, kein Sicherheits- oder Freigabetoken.

## Eingabe

```json
{
  "scope": "Dieser Chat; Vorlage, nicht live geprüft",
  "tasks": [
    {
      "id": "10.01",
      "source_key": "projekt-alpha:pilotumfang",
      "project": "Projekt Alpha",
      "title": "Pilotumfang festlegen",
      "status": "wartet",
      "source": "Ausdrückliche Frage im aktuellen Chat",
      "next": "A oder B auswählen",
      "human": {
        "key": "pilotumfang",
        "action": "Variante A oder B wählen",
        "why_human": "Hendrik entscheidet laut aktuellem Auftrag über den Umfang.",
        "owner_confirmed": true,
        "ready": true,
        "resolved": false
      }
    }
  ]
}
```

`human` weglassen/null, wenn nichts ausschließlich bei Hendrik liegt. Alle menschlichen Pflichtfelder sind zwingend; fehlende Belege nicht mit `true` auffüllen. Bei `aktiv` ist `active_confirmed: true` erforderlich; bei `fertig` `done_confirmed: true`. Diese Werte nur aus passenden Quellen ableiten. Andernfalls den Status vor dem Aufruf auf `bereit`, `wartet` oder `unklar` korrigieren und fehlende Prüfung nennen.

Gemeinsame Entscheidung: gleiche `human.key` und exakt gleiche `action` für mehrere Tasks; daraus entsteht eine Antwortnummer mit allen Referenzen. Unterschiedliche Handlungen erhalten verschiedene Schlüssel. Reihenfolge der Eingabe entspricht der begründeten Priorisierung; der Helfer erfindet keine Prioritäten.

## Nutzung

```bash
python3 scripts/snapshot.py < /sicherer/temporärer/snapshot.json
python3 scripts/snapshot.py --resolve 1 --expected M-HASH < /sicherer/temporärer/snapshot.json
python3 -m unittest discover -s tests -v
```

Relative Pfade beziehen sich auf den Skillordner. Pfad/Interpreter hostgerecht auflösen; keine wörtlichen Platzhalter ausführen. JSON auch direkt per stdin ohne Datei übergeben. Unter Windows den vorhandenen Python-3-Interpreter nutzen.

Die erste Ausgabe liefert `snapshot`, `counts`, `actions` und geprüfte Tasks. Pro Aktion enthält sie `number`, `key`, `action` und `refs`. Die Kennung zusammen mit genau dieser Reihenfolge anzeigen. Vor Auflösung nummerierter Antworten muss `--expected` die zuletzt gezeigte Kennung sein. Jede inhaltliche Änderung der Eingabe ändert die Kennung; dann nicht still neu zuordnen. Eine Filteransicht erzeugt ihren eigenen sichtbaren Stand. Task-IDs dabei nicht umnummerieren.

Der Helfer prüft keine Freigabe, keine Aktualität, keine Quellenwahrheit und kein laufendes Modell. Nach erfolgreicher Nummernauflösung separat die Nutzerabsicht und geltende Autorisierung prüfen. Keine neuen Aktionen als erledigt markieren, nur weil eine Antwort parsebar ist.
