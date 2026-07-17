#!/usr/bin/env python3
"""Focused regression tests for the sole Stage1 blueprint boundary."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "Docs" / "tools"
sys.path.insert(0, str(TOOLS))

import generate_stage1_blueprint as generator  # noqa: E402


class Stage1BlueprintSsotTests(unittest.TestCase):
    EXPECTED_CHECKLIST_SHA256 = (
        "8ffdc57f4002d3e70a7c53984b441ab22bec9a1ecf7141fe740e94608db9fe62"
    )

    def test_only_v2_blueprint_is_tracked(self) -> None:
        tracked = subprocess.run(
            ["git", "ls-files", "Docs/Stage1_Blueprint*.md"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.splitlines()
        self.assertEqual(tracked, ["Docs/Stage1_Blueprint_v2.md"])

    def test_only_v2_blueprint_exists_physically(self) -> None:
        physical = sorted(
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "Docs").glob("Stage1_Blueprint*.md")
            if path.is_file()
        )
        self.assertEqual(physical, ["Docs/Stage1_Blueprint_v2.md"])

    def test_retired_markdown_sources_are_absent(self) -> None:
        self.assertFalse((ROOT / "Docs/Stage1_Blueprint.md").exists())
        self.assertFalse((ROOT / "Docs/Stage1_Blueprint_Applicable_Theorems.md").exists())

    def test_generator_writes_only_the_target_manifest(self) -> None:
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            temp_root = Path(directory)
            output = temp_root / "Docs" / "Stage1_Targets_rev-5.6.json"
            output.parent.mkdir()
            with (
                mock.patch.object(generator, "TARGET_MANIFEST_FILE", output),
                mock.patch.object(generator.subprocess, "run") as validation_gate,
            ):
                generator.main()

            validation_gate.assert_called_once()
            self.assertEqual(
                [path.relative_to(temp_root).as_posix() for path in temp_root.rglob("*") if path.is_file()],
                ["Docs/Stage1_Targets_rev-5.6.json"],
            )
            manifest = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(manifest["task_state_authority"], "Docs/Stage1_Blueprint_v2.md")
            self.assertNotIn("generated_projection", manifest)

    def test_checked_in_manifest_is_reproducible(self) -> None:
        items, removed_count = generator.load_stage0_items()
        selected = generator.select_items(items)
        expected = generator.build_target_manifest(selected, items, removed_count)
        actual = json.loads(
            (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
        )
        self.assertEqual(actual, expected)

    def test_assurance_history_has_no_checkbox_cursor(self) -> None:
        standard = (ROOT / "Docs/Stage1_Assurance_Standard_rev-5.6.md").read_text(
            encoding="utf-8"
        )
        records = re.findall(
            r"^- Historically (?:checked|open): `(S56-M0387-[A-Z0-9]+)`",
            standard,
            re.MULTILINE | re.IGNORECASE,
        )
        self.assertEqual(len(records), 41)
        self.assertEqual(len(set(records)), 41)
        self.assertIsNone(re.search(r"^- \[[ _xX]\] `S56-M0387-", standard, re.MULTILINE))

    def test_historical_lean_artifacts_are_explicitly_non_authoritative(self) -> None:
        boundary = (
            ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("pre-v2 proof and audit artifacts", boundary)
        self.assertIn("Docs/Stage1_Blueprint_v2.md", boundary)
        self.assertIn("sole current Stage1", boundary)

    def test_authoritative_checklist_is_frozen_at_the_migrated_cursor(self) -> None:
        blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
        begin = "<!-- STAGE1-EXECUTION-CHECKLIST:BEGIN -->"
        end = "<!-- STAGE1-EXECUTION-CHECKLIST:END -->"
        self.assertEqual(blueprint.count(begin), 1)
        self.assertEqual(blueprint.count(end), 1)
        body = blueprint.split(begin, 1)[1].split(end, 1)[0]
        self.assertEqual(
            hashlib.sha256(body.encode("utf-8")).hexdigest(),
            self.EXPECTED_CHECKLIST_SHA256,
        )
        states = re.findall(
            r"^- (\[[_x ]\]) `S56-M-\d{4}-(?:INTAKE|STATEMENT|ANCHOR_AUDIT|OBLIGATION_TREE|PROOF|VALIDATION|RELEASE)`",
            body,
            re.MULTILINE,
        )
        self.assertEqual(
            {state: states.count(state) for state in ("[ ]", "[_]", "[x]")},
            {"[ ]": 7521, "[_]": 3300, "[x]": 1},
        )


if __name__ == "__main__":
    unittest.main()
