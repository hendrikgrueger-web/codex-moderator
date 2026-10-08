"""Deterministic unit/CLI/install checks, NOT a live Codex model evaluation."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


snapshot = load("snapshot")
installer = load("install")


def task(tid="10.01", **extra):
    value = {"id": tid, "source_key": "synthetic:" + tid, "project": "Alpha",
             "title": "Testziel", "status": "bereit", "source": "Synthetischer Test"}
    value.update(extra)
    return value


def human(**extra):
    value = {"key": "choice", "action": "A oder B wählen", "why_human": "Explizit zugewiesen",
             "owner_confirmed": True, "ready": True, "resolved": False}
    value.update(extra)
    return value


def data(*tasks):
    return {"scope": "Nur synthetische Tests; keine aktuellen Projektstände", "tasks": list(tasks)}


class SnapshotTests(unittest.TestCase):
    def test_counts_unique_tasks_not_human_duplicates(self):
        result = snapshot.validate(data(task(human=human()), task("10.02", status="fertig", done_confirmed=True)))
        self.assertEqual(result["counts"], {"tasks": 2, "open": 1, "done": 1,
                         "human_actions": 1, "by_status": {"bereit": 1, "fertig": 1}})

    def test_empty_scope_is_not_all_clear(self):
        result = snapshot.validate(data())
        self.assertEqual(result["counts"]["human_actions"], 0)
        self.assertIn("synthetische", result["scope"])

    def test_blocked_does_not_mean_human(self):
        self.assertEqual(snapshot.validate(data(task(status="blockiert")))["actions"], [])

    def test_human_gate(self):
        for change in ({"owner_confirmed": False}, {"ready": False}, {"resolved": True}):
            with self.subTest(change=change):
                self.assertEqual(snapshot.validate(data(task(human=human(**change))))["actions"], [])

    def test_done_and_paused_not_in_human_list(self):
        for state in ("fertig", "pausiert"):
            self.assertEqual(snapshot.validate(data(task(status=state, done_confirmed=True, human=human())))["actions"], [])

    def test_missing_human_evidence_rejected(self):
        value = human()
        del value["why_human"]
        with self.assertRaises(ValueError):
            snapshot.validate(data(task(human=value)))

    def test_string_booleans_rejected(self):
        with self.assertRaises(ValueError):
            snapshot.validate(data(task(human=human(owner_confirmed="false"))))

    def test_group_common_decision(self):
        result = snapshot.validate(data(task(human=human()), task("10.02", human=human())))
        self.assertEqual(len(result["actions"]), 1)
        self.assertEqual(result["actions"][0]["refs"], ["10.01", "10.02"])

    def test_conflicting_shared_action_rejected(self):
        with self.assertRaises(ValueError):
            snapshot.validate(data(task(human=human()), task("10.02", human=human(action="Etwas anderes"))))

    def test_duplicate_task_ids_rejected(self):
        with self.assertRaises(ValueError):
            snapshot.validate(data(task(), task(source_key="different")))

    def test_duplicate_source_rejected(self):
        with self.assertRaises(ValueError):
            snapshot.validate(data(task(), task("10.02", source_key="synthetic:10.01")))

    def test_ambiguous_project_rejected(self):
        with self.assertRaises(ValueError):
            snapshot.validate(data(task(), task("10.02", project="Beta")))

    def test_fake_activity_and_completion_rejected(self):
        for state in ("aktiv", "fertig"):
            with self.subTest(state=state), self.assertRaises(ValueError):
                snapshot.validate(data(task(status=state)))

    def test_unknown_state_rejected(self):
        with self.assertRaises(ValueError):
            snapshot.validate(data(task(status="fast-fertig")))

    def test_missing_source_rejected(self):
        with self.assertRaises(ValueError):
            snapshot.validate(data(task(source="")))

    def test_dictionary_key_order_does_not_change_snapshot(self):
        first = data(task(human=human()))
        second = dict(reversed(list(first.items())))
        self.assertEqual(snapshot.validate(first)["snapshot"], snapshot.validate(second)["snapshot"])

    def test_change_invalidates_old_reply(self):
        first = data(task(human=human()))
        old = snapshot.validate(first)
        first["tasks"][0]["human"]["action"] = "Geänderter Umfang"
        new = snapshot.validate(first)
        with self.assertRaises(ValueError):
            snapshot.resolve(new, 1, old["snapshot"])

    def test_reordering_invalidates_old_reply(self):
        first = data(task(human=human()), task("10.02", human=human(key="other", action="Andere Aktion")))
        old = snapshot.validate(first)
        first["tasks"].reverse()
        with self.assertRaises(ValueError):
            snapshot.resolve(snapshot.validate(first), 1, old["snapshot"])

    def test_resolution_is_not_authorization(self):
        value = snapshot.validate(data(task(human=human())))
        result = snapshot.resolve(value, 1, value["snapshot"])
        self.assertEqual(result["selection"]["refs"], ["10.01"])
        self.assertFalse(result["authorized"])

    def test_missing_snapshot_and_invalid_numbers(self):
        value = snapshot.validate(data(task(human=human())))
        for number, expected in ((1, None), (0, value["snapshot"]), (-1, value["snapshot"]), (2, value["snapshot"])):
            with self.subTest(number=number), self.assertRaises(ValueError):
                snapshot.resolve(value, number, expected)

    def test_cli_unicode_and_no_files_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(ROOT / "scripts/snapshot.py")],
                                    input=json.dumps(data(task(human=human())), ensure_ascii=False),
                                    text=True, capture_output=True, cwd=tmp)
            self.assertEqual(result.returncode, 0)
            self.assertIn("wählen", result.stdout)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_cli_invalid_input_not_echoed(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/snapshot.py")],
                                input='{"scope":"private-test-value","scope":"duplicate"}',
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("private-test-value", result.stderr + result.stdout)


class InstallTests(unittest.TestCase):
    def test_install_check_idempotent_and_remove(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self.assertIn("LINK_CREATED", installer.install(ROOT, home))
            self.assertIn("FILES_VERIFIED", installer.install(ROOT, home))
            self.assertIn("FILES_VERIFIED", installer.install(ROOT, home, "check"))
            self.assertIn("LINK_REMOVED", installer.install(ROOT, home, "remove"))
            self.assertTrue((ROOT / "SKILL.md").is_file())

    def test_unknown_installation_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".agents/skills/moderator"
            target.mkdir(parents=True)
            original = target / "SKILL.md"
            original.write_text("foreign", encoding="utf-8")
            for mode in ("install", "check", "remove"):
                with self.subTest(mode=mode), self.assertRaises(ValueError):
                    installer.install(ROOT, home, mode)
            self.assertEqual(original.read_text(encoding="utf-8"), "foreign")

    def test_check_does_not_create_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            with self.assertRaises(ValueError):
                installer.install(ROOT, home, "check")
            self.assertEqual(list(home.iterdir()), [])

    def test_broken_foreign_link_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            target = home / ".agents/skills/moderator"
            target.parent.mkdir(parents=True)
            target.symlink_to(home / "missing")
            with self.assertRaises(ValueError):
                installer.install(ROOT, home)
            self.assertTrue(target.is_symlink())


class PackageTests(unittest.TestCase):
    def test_required_metadata_and_references(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        ui = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\nname: moderator\n"))
        self.assertIn("Du bist Moderator", skill)
        self.assertIn("$moderator", ui)
        self.assertIn("allow_implicit_invocation: true", ui)
        for name in ("format", "snapshot", "activation", "evaluation"):
            self.assertTrue((ROOT / "references" / (name + ".md")).is_file())
        self.assertNotIn("TODO", skill)


if __name__ == "__main__":
    unittest.main()
