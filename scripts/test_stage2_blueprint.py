#!/usr/bin/env python3
"""Mutation tests for the Stage2 authority and Gantt contract."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "Docs" / "tools" / "check_stage2_blueprint.py"
SPEC = importlib.util.spec_from_file_location("check_stage2_blueprint", CHECKER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import Stage2 checker")
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
SPEC.loader.exec_module(checker)


class Stage2BlueprintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.blueprint = (ROOT / "Docs" / "Stage2_Blueprint.md").read_text()
        cls.gantt = (ROOT / "Docs" / "Stage2_Gantt.md").read_text()

    def assert_invalid(self, blueprint: str | None = None, gantt: str | None = None) -> None:
        with self.assertRaises(checker.ValidationError):
            checker.validate_texts(blueprint or self.blueprint, gantt or self.gantt)

    def test_current_files_pass(self) -> None:
        summary = checker.validate_texts(self.blueprint, self.gantt)
        tasks = checker.parse_tasks(self.blueprint)
        self.assertEqual(summary["items"], len(tasks))
        self.assertEqual(
            summary["open"] + summary["self_tested"] + summary["master_accepted"],
            summary["items"],
        )

    def test_duplicate_item_is_rejected(self) -> None:
        duplicate = next(
            line for line in self.blueprint.splitlines() if "`S2-ENV-001`" in line and line.startswith("- [")
        )
        mutated = self.blueprint.replace(checker.END, duplicate + "\n" + checker.END)
        self.assert_invalid(blueprint=mutated)

    def test_missing_dependency_is_rejected(self) -> None:
        mutated = self.blueprint.replace(
            "depends_on=S2-ENV-001 | owned_paths=Docs/evidence/lean_dependencies.json",
            "depends_on=S2-ENV-999 | owned_paths=Docs/evidence/lean_dependencies.json",
            1,
        )
        self.assert_invalid(blueprint=mutated)

    def test_cycle_is_rejected(self) -> None:
        mutated = self.blueprint.replace(
            "`S2-AUTH-001` Freeze repository evidence, execution-skill version and Stage2 authority boundary | depends_on=-",
            "`S2-AUTH-001` Freeze repository evidence, execution-skill version and Stage2 authority boundary | depends_on=S2-REL-005",
            1,
        )
        self.assert_invalid(blueprint=mutated)

    def test_uppercase_checkbox_is_rejected(self) -> None:
        item = next(
            line
            for line in self.blueprint.splitlines()
            if line.startswith("- [") and "`S2-" in line
        )
        uppercase = item[:3] + "X" + item[4:]
        mutated = self.blueprint.replace(item, uppercase, 1)
        self.assert_invalid(blueprint=mutated)

    def test_self_tested_item_requires_accepted_dependencies(self) -> None:
        mutated = self.blueprint.replace("- [ ] `S2-AUTH-004`", "- [_] `S2-AUTH-004`", 1)
        self.assert_invalid(blueprint=mutated)

    def test_absolute_owned_path_is_rejected(self) -> None:
        mutated = self.blueprint.replace(
            "owned_paths=Docs/evidence/lean_environment.json",
            "owned_paths=/tmp/lean_environment.json",
            1,
        )
        self.assert_invalid(blueprint=mutated)

    def test_gantt_must_cover_every_item(self) -> None:
        mutated = self.gantt.replace("| `S2-ENV-005` | `S2-ENV-004` |\n", "", 1)
        self.assert_invalid(gantt=mutated)

    def test_gantt_dependency_drift_is_rejected(self) -> None:
        mutated = self.gantt.replace(
            "| `S2-ENV-002` | `S2-ENV-001` |",
            "| `S2-ENV-002` | `S2-AUTH-001` |",
            1,
        )
        self.assert_invalid(gantt=mutated)

    def test_gantt_mermaid_title_drift_is_rejected(self) -> None:
        mutated = self.gantt.replace(
            "title Stage2 Catalog Integrity and Isolated Execution",
            "title Stage1 Stale Schedule",
            1,
        )
        self.assert_invalid(gantt=mutated)

    def test_gantt_cannot_be_a_second_cursor(self) -> None:
        mutated = self.gantt + "\n- [ ] S2-SHADOW-001\n"
        self.assert_invalid(gantt=mutated)

    def test_machine_absolute_path_is_rejected(self) -> None:
        mutated = self.blueprint + f"\nObserved at {ROOT}\n"
        self.assert_invalid(blueprint=mutated)


if __name__ == "__main__":
    unittest.main()
