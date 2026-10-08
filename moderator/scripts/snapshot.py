#!/usr/bin/env python3
"""Validate a normalized cockpit; count and bind reply numbers. No I/O writes."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from typing import Any

STATES = {"aktiv", "bereit", "wartet", "blockiert", "pausiert", "unklar", "fertig"}
MAX_BYTES = 1_000_000


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "Doppelter JSON-Schlüssel.")
        result[key] = value
    return result


def validate(data: dict[str, Any]) -> dict[str, Any]:
    require(isinstance(data, dict), "Snapshot muss ein Objekt sein.")
    require(text(data.get("scope")), "Sichtgrenze scope fehlt.")
    require(isinstance(data.get("tasks"), list), "tasks muss eine Liste sein.")
    ids: set[str] = set()
    sources: set[str] = set()
    projects: dict[str, str] = {}
    actions: dict[str, dict[str, Any]] = {}
    counts: Counter[str] = Counter()
    for task in data["tasks"]:
        require(isinstance(task, dict), "Task muss ein Objekt sein.")
        for field in ("id", "source_key", "project", "title", "status", "source"):
            require(text(task.get(field)), f"Task-Pflichtfeld fehlt: {field}.")
        tid = task["id"]
        require(bool(re.fullmatch(r"[0-9]{2,}\.[0-9]{2,}", tid)), "Ungültige Cockpit-ID.")
        require(tid not in ids, "Doppelte Task-ID.")
        require(task["source_key"] not in sources, "Doppelte Quellaufgabe; zuerst deduplizieren.")
        ids.add(tid)
        sources.add(task["source_key"])
        prefix = tid.split(".")[0]
        require(projects.get(prefix, task["project"]) == task["project"], "Projekt-ID ist mehrdeutig.")
        projects[prefix] = task["project"]
        state = task["status"]
        require(state in STATES, "Unbekannter Task-Status.")
        if state == "aktiv":
            require(task.get("active_confirmed") is True, "Aktive Bearbeitung nicht bestätigt.")
        if state == "fertig":
            require(task.get("done_confirmed") is True, "Abschluss nicht bestätigt.")
        counts[state] += 1
        human = task.get("human")
        if human is None:
            continue
        require(isinstance(human, dict), "human muss Objekt oder null sein.")
        for field in ("key", "action", "why_human"):
            require(text(human.get(field)), f"Mensch-Aktionsfeld fehlt: {field}.")
        for field in ("owner_confirmed", "ready", "resolved"):
            require(type(human.get(field)) is bool, f"Explizites Boolean erforderlich: {field}.")
        if (not human["owner_confirmed"] or not human["ready"] or human["resolved"]
                or state in {"fertig", "pausiert"}):
            continue
        key = human["key"]
        if key in actions:
            require(actions[key]["action"] == human["action"], "Gemeinsame Aktion ist widersprüchlich.")
            actions[key]["refs"].append(tid)
        else:
            actions[key] = {"number": len(actions) + 1, "key": key,
                            "action": human["action"], "refs": [tid]}
    signature = hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False,
                                         separators=(",", ":")).encode("utf-8")).hexdigest()[:12]
    return {"snapshot": "M-" + signature, "scope": data["scope"],
            "counts": {"tasks": len(ids), "open": len(ids) - counts["fertig"],
                       "done": counts["fertig"], "human_actions": len(actions),
                       "by_status": dict(sorted(counts.items()))},
            "actions": list(actions.values()), "tasks": data["tasks"]}


def resolve(result: dict[str, Any], number: int, expected: str | None) -> dict[str, Any]:
    require(bool(expected) and expected == result["snapshot"],
            "Snapshot fehlt oder hat sich geändert; Nummer nicht neu zuordnen.")
    require(type(number) is int and 1 <= number <= len(result["actions"]),
            "Antwortnummer ist in diesem Stand nicht vorhanden.")
    return {"snapshot": expected, "selection": result["actions"][number - 1],
            "authorized": False,
            "notice": "Nur Nummernauflösung. Nutzerabsicht und Autorisierung separat prüfen."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resolve", type=int, metavar="NUMBER")
    parser.add_argument("--expected", metavar="SNAPSHOT")
    args = parser.parse_args()
    try:
        raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        require(len(raw) <= MAX_BYTES, "Snapshot zu groß.")
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=no_duplicate_keys)
        result = validate(data)
        if args.resolve is not None:
            result = resolve(result, args.resolve, args.expected)
        else:
            require(args.expected is None, "--expected nur mit --resolve verwenden.")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, TypeError, UnicodeError):
        # Never echo raw source text, input values or possible credentials on failure.
        print("Snapshot ungültig oder Antwort nicht eindeutig. Eingabe/letzten Stand prüfen.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
