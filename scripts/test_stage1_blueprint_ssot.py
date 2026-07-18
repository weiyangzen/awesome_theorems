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
        "5087d407f7b3d5813b60a9e757dab890abadf82cf2666038bb2c1b872e4b42c3"
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
            output = temp_root / "Docs" / "Stage1_Target_Membership_v2.json"
            output.parent.mkdir()
            with (
                mock.patch.object(generator, "TARGET_MANIFEST_FILE", output),
                mock.patch.object(generator.subprocess, "run") as validation_gate,
            ):
                generator.main()

            validation_gate.assert_called_once()
            self.assertEqual(
                [path.relative_to(temp_root).as_posix() for path in temp_root.rglob("*") if path.is_file()],
                ["Docs/Stage1_Target_Membership_v2.json"],
            )
            manifest = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(manifest["task_state_authority"], "Docs/Stage1_Blueprint_v2.md")
            self.assertEqual(manifest["schema_version"], "stage1-target-membership/2.0")
            self.assertNotIn("generated_projection", manifest)

    def test_checked_in_manifest_is_reproducible(self) -> None:
        items, removed_count = generator.load_stage0_items()
        selected = generator.select_items(items)
        expected = generator.build_target_manifest(selected, items, removed_count)
        actual = json.loads(
            (ROOT / "Docs/Stage1_Target_Membership_v2.json").read_text(encoding="utf-8")
        )
        self.assertEqual(actual, expected)

    def test_manifest_generator_is_membership_only_and_preserves_legacy_lanes(self) -> None:
        self.assertEqual(
            generator.MEMBERSHIP_PREDICATE_SEMANTICS,
            "frozen_membership_discovery_only",
        )
        self.assertEqual(
            generator.TARGET_LANE_SEMANTICS,
            "legacy_discovery_metadata_only",
        )
        self.assertIn(
            "Deprecated compatibility alias",
            generator.is_stage1_eligible.__doc__ or "",
        )
        self.assertIn(
            "Deprecated compatibility alias", generator.stage1_lane.__doc__ or ""
        )
        items, removed_count = generator.load_stage0_items()
        selected = generator.select_items(items)
        manifest = generator.build_target_manifest(selected, items, removed_count)
        by_id = {item.uid: item for item in items}
        self.assertEqual(len(manifest["targets"]), 1546)
        for target in manifest["targets"]:
            item = by_id[target["theorem_id"]]
            self.assertEqual(
                target["target_lane"], generator.legacy_discovery_lane(item)
            )
            self.assertEqual(
                generator.stage1_lane(item), generator.legacy_discovery_lane(item)
            )

    def test_guidelines_do_not_authorize_legacy_frontier_lanes(self) -> None:
        guidelines = (ROOT / "Docs/Blueprint_Guidelines.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("membership/discovery-only", guidelines)
        self.assertIn("`target_lane`", guidelines)
        self.assertIn("`research_required` / `defer_frontier`", guidelines)
        self.assertIn("`>= 0.70`", guidelines)
        self.assertIn("`frontier_exception`", guidelines)
        self.assertNotIn(
            "`mathematical_debt` 与 `formalization_debt` 可以存在，"
            "因为它们分别用于组织未来的新数学证明与新机器形式化工作",
            guidelines,
        )
        self.assertNotIn(
            "可以进入 Stage1，但必须标为 `deep_formalization_debt`",
            guidelines,
        )

    def test_current_tools_do_not_require_the_historical_standard(self) -> None:
        generator_source = (TOOLS / "generate_stage1_blueprint.py").read_text(
            encoding="utf-8"
        )
        checker_source = (TOOLS / "check_stage1_standard.py").read_text(
            encoding="utf-8"
        )
        skill = (ROOT / "skills/execute-stage1-v2/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("STANDARD_FILE", generator_source)
        self.assertNotIn("STANDARD =", checker_source)
        self.assertNotIn("FEATURE_GROUPS", checker_source)
        self.assertIn("Superseded assurance material exists only in Git history", skill)
        self.assertIn("Do not restore or read it during current\nexecution", skill)

    def test_historical_lean_artifacts_are_explicitly_non_authoritative(self) -> None:
        boundary = (
            ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("pre-v2 proof and audit artifacts", boundary)
        self.assertIn("Docs/Stage1_Blueprint_v2.md", boundary)
        self.assertIn("sole current Stage1", boundary)

    def test_v2_focuses_existing_machine_proofs_and_fails_closed(self) -> None:
        blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
        policy = blueprint.split("<!-- STAGE1-EXECUTION-CHECKLIST:BEGIN -->", 1)[0]
        required = (
            "Stage1 v2 Machine-Proof Integration Blueprint",
            "stage1-integration/2.1",
            "stage1-focus-policy/1.0",
            "Stage1_Instances/<THEOREM-ID>/focus-eligibility.json",
            "stage1-focus-eligibility/1.0",
            "exact_pinned_closure",
            "exact_external_unintegrated",
            "no_exact_candidate_as_of",
            "unknown",
            "organize_or_integrate",
            "frontier_exception",
            "defer_frontier",
            "research_required",
            "exclude_scope",
            "at least `0.70` probability",
            "scheduler-owned admission",
            "phase_permissions",
            "focus_eligibility_summary",
            "skills/execute-stage1-v2/SKILL.md",
        )
        for value in required:
            with self.subTest(value=value):
                self.assertIn(value, policy)
        self.assertRegex(
            policy,
            r"Only a prompt bound to an\s+active `frontier_exception`",
        )
        self.assertIn("Candidate filtering alone is insufficient", policy)
        self.assertIn("editing them cannot admit work", policy)
        self.assertIn(
            "Both `exact_pinned_closure` and `exact_external_unintegrated` MUST carry",
            policy,
        )
        self.assertIn(
            "Pinning a proof after the cutoff cannot retroactively establish",
            policy,
        )
        self.assertIn(
            "current execution\nauthority for a pinned proof remains exclusively",
            policy,
        )

    def test_v2_policy_has_exact_two_axis_vocabularies(self) -> None:
        blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
        policy = blueprint.split("<!-- STAGE1-EXECUTION-CHECKLIST:BEGIN -->", 1)[0]
        machine_values = set(re.findall(
            r"^\| `(exact_pinned_closure|exact_external_unintegrated|no_exact_candidate_as_of|unknown)` \|",
            policy,
            re.MULTILINE,
        ))
        disposition_values = set(re.findall(
            r"^\| `(organize_or_integrate|frontier_exception|defer_frontier|research_required|exclude_scope)` \|",
            policy,
            re.MULTILINE,
        ))
        self.assertEqual(
            machine_values,
            {
                "exact_pinned_closure",
                "exact_external_unintegrated",
                "no_exact_candidate_as_of",
                "unknown",
            },
        )
        self.assertEqual(
            disposition_values,
            {
                "organize_or_integrate",
                "frontier_exception",
                "defer_frontier",
                "research_required",
                "exclude_scope",
            },
        )

    def test_authoritative_checklist_is_frozen_at_the_migrated_cursor(self) -> None:
        blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
        begin = "<!-- STAGE1-EXECUTION-CHECKLIST:BEGIN -->"
        end = "<!-- STAGE1-EXECUTION-CHECKLIST:END -->"
        self.assertEqual(blueprint.count(begin), 1)
        self.assertEqual(blueprint.count(end), 1)
        body = blueprint.split(begin, 1)[1].split(end, 1)[0]
        self.assertEqual(blueprint.split(end, 1)[1], "\n")
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

    def test_v2_skill_separates_integration_from_frontier_proof_intent(self) -> None:
        skill = (ROOT / "skills/execute-stage1-v2/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("`integrate`", skill)
        self.assertIn("`frontier_prove`", skill)
        self.assertNotIn("For `prove`", skill)
        self.assertNotIn("`intake`, `audit`, `prove`", skill)
        self.assertRegex(
            skill,
            r"`frontier_prove`[^\n]*\n?(?:.*\n){0,4}.*only when the current\s+receipt has disposition `frontier_exception`",
        )


if __name__ == "__main__":
    unittest.main()
