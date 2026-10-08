#!/usr/bin/env python3
"""Link only this skill into the current user's Codex discovery directory."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys


def install(source: Path, home: Path, mode: str = "install") -> str:
    source = source.resolve(strict=True)
    if not (source / "SKILL.md").is_file():
        raise ValueError("Kein vollständiger Skill im Quellordner.")
    if mode not in {"install", "check", "remove"}:
        raise ValueError("Unbekannter Installationsmodus.")
    target = home.expanduser().resolve() / ".agents" / "skills" / "moderator"
    exists = target.exists() or target.is_symlink()
    same = exists and target.resolve() == source
    if mode == "remove":
        if not target.is_symlink() or not same:
            raise ValueError("Nur den exakt zugehörigen Link entfernen; nichts geändert.")
        target.unlink()
        return "LINK_REMOVED; Quelldateien unverändert."
    if same:
        return "FILES_VERIFIED; Codex-Discovery und Aufruf noch separat prüfen."
    if exists:
        raise ValueError("Andere Installation vorhanden; nichts überschrieben.")
    if mode == "check":
        raise ValueError("Discovery-Link fehlt; nichts geändert.")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(source, target_is_directory=True)
    if target.resolve(strict=True) != source:
        raise ValueError("Linkprüfung fehlgeschlagen.")
    return "LINK_CREATED; Codex-Discovery und Aufruf noch separat prüfen."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home(), help="Ziel-Home; z. B. isolierter Testordner")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--remove", action="store_true")
    args = parser.parse_args()
    mode = "check" if args.check else "remove" if args.remove else "install"
    try:
        print(install(Path(__file__).resolve().parents[1], args.home, mode))
        return 0
    except (OSError, ValueError) as error:
        print(f"Aktivierung offen: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
