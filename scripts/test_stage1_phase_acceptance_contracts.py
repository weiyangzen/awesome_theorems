#!/usr/bin/env python3
"""Focused fail-closed tests for Stage1 phase acceptance authority."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "Docs" / "tools" / "check_stage1_phase_acceptance_contracts.py"
CONTRACT = ROOT / "Docs" / "Stage1_Phase_Acceptance_Contracts.json"
STANDARD_GATE = ROOT / "Docs" / "tools" / "check_stage1_standard.py"

SPEC = importlib.util.spec_from_file_location("stage1_phase_contract_validator", VALIDATOR)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)

STANDARD_SPEC = importlib.util.spec_from_file_location("stage1_standard_validator", STANDARD_GATE)
assert STANDARD_SPEC is not None and STANDARD_SPEC.loader is not None
standard = importlib.util.module_from_spec(STANDARD_SPEC)
STANDARD_SPEC.loader.exec_module(standard)


class PhaseAcceptanceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    def validate(self, mutation=None):
        value = copy.deepcopy(self.contract)
        if mutation is not None:
            mutation(value)
        return validator.validate_contract(value, root=ROOT)

    def assert_rejected(self, mutation, message: str) -> None:
        with self.assertRaisesRegex(validator.ContractError, message):
            self.validate(mutation)

    def test_authoritative_contract_passes(self) -> None:
        self.assertEqual(len(self.validate()["phases"]), 7)
        self.assertTrue(all(
            row["validator_authorities"] == [{
                "path_pattern": "scripts/stage1_phase_validators/current.py",
                "language": "python",
                "argv_template": [
                    "/usr/bin/python3", "-I", "-B", "{validator_path}"
                ],
                "authority_generation": "stage1-v2",
                "requirements_authority": "Docs/Stage1_Blueprint_v2.md",
                "positive_acceptance_capable": True,
            }]
            for row in self.contract["phases"]
        ))

    def test_all_normative_source_references_are_v2_blueprint_only(self) -> None:
        references = self.contract["source_references"]
        self.assertEqual(
            {row["reference_id"] for row in references},
            validator.REQUIRED_SOURCE_REFERENCE_IDS,
        )
        self.assertEqual(
            {row["path"] for row in references},
            {"Docs/Stage1_Blueprint_v2.md"},
        )
        serialized = json.dumps(self.contract, sort_keys=True)
        self.assertNotIn("rev56-", serialized)
        self.assertNotIn("G07-REV56-RECOMPUTE", serialized)
        self.assertNotIn("Stage1_Assurance_Standard_rev-5.6.md", serialized)
        self.assertIn("G07-V2-ASSURANCE-RECOMPUTE", serialized)

    def test_every_source_reference_range_contains_its_required_phrases(self) -> None:
        lines = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(
            encoding="utf-8"
        ).splitlines()
        for reference in self.contract["source_references"]:
            with self.subTest(reference_id=reference["reference_id"]):
                excerpt = "\n".join(
                    lines[reference["line_start"] - 1 : reference["line_end"]]
                )
                for phrase in reference["required_phrases"]:
                    self.assertIn(phrase, excerpt)

    def test_non_v2_source_reference_path_fails_closed(self) -> None:
        self.assert_rejected(
            lambda value: value["source_references"][0].update(
                path="Docs/Stage1_Assurance_Standard_rev-5.6.md"
            ),
            "source path is not the v2 blueprint SSOT",
        )

    def test_required_v2_assurance_reference_cannot_be_removed(self) -> None:
        self.assert_rejected(
            lambda value: value["source_references"].pop(),
            "v2 source-reference coverage is incomplete",
        )

    def test_v2_blueprint_contains_complete_normative_acceptance_section(self) -> None:
        blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(
            encoding="utf-8"
        )
        policy = blueprint.split(
            "<!-- STAGE1-EXECUTION-CHECKLIST:BEGIN -->", 1
        )[0]
        required = (
            "## 17. Seven-Phase Assurance and Acceptance Contract",
            "### 17.1 Lifecycle, Verdicts, and Terminal Decisions",
            "`AUDIT-Z` and `THEOREM-Z` are separate terminal decisions",
            "### 17.3 Intake and Exact Statement",
            "removed-hypothesis",
            "### 17.4 Obligation Registry, Typed DAGs, and Composition",
            "checked composition certificate",
            "### 17.5 Discovery, Provenance, Human Source, and Readability",
            "Human-source acceptance",
            "Every required readable node",
            "Every `[_]` worker packet",
            "literal argv array",
            "Release-grade replay",
            "two signed attestations",
            "independently implemented minimal verifier",
            "`G07-V2-ASSURANCE-RECOMPUTE`",
            "The seven positive phase predicates",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, policy)

    def test_each_phase_requires_exactly_one_current_validator(self) -> None:
        self.assert_rejected(
            lambda value: value["phases"][0].update(validator_authorities=[]),
            "exactly one current validator authority",
        )
        self.assert_rejected(
            lambda value: value["phases"][0]["validator_authorities"].append(
                copy.deepcopy(value["phases"][0]["validator_authorities"][0])
            ),
            "exactly one current validator authority",
        )

    def test_review_runtime_uses_requested_default_service_tier(self) -> None:
        runtime = self.contract["review_runtime"]
        self.assertEqual(runtime["model"], "gpt-5.6-sol")
        self.assertEqual(runtime["reasoning_effort"], "ultra")
        self.assertEqual(runtime["service_tier"], "default")
        self.assertEqual(runtime["catalog_label"], "Default")
        self.assertEqual(runtime["shared_total_concurrency_limit"], 0)

    def test_raw_blocked_can_never_close_or_be_review_eligible(self) -> None:
        self.assert_rejected(
            lambda value: value["phases"][4].update(raw_blocked_can_close_phase=True),
            "raw blocked closes proof",
        )
        self.assert_rejected(
            lambda value: value["phases"][4]["worker_verdicts_eligible_for_review"].append("blocked"),
            "reviews a raw failure as closable",
        )

    def test_proof_intent_is_derived_from_focus_disposition(self) -> None:
        self.assertEqual(
            self.contract["phases"][4]["intent"],
            {
                "organize_or_integrate": "integrate",
                "frontier_exception": "frontier_prove",
            },
        )
        self.assert_rejected(
            lambda value: value["phases"][4].update(intent="prove"),
            "proof intent is wrong",
        )
        self.assert_rejected(
            lambda value: value["phases"][4]["intent"].update(
                organize_or_integrate="frontier_prove"
            ),
            "proof intent is wrong",
        )

    def test_accepted_audit_only_is_release_only_and_not_theorem_complete(self) -> None:
        self.assert_rejected(
            lambda value: value["phases"][2]["worker_verdicts_eligible_for_review"].append(
                "accepted_audit_only"
            ),
            "accepted_audit_only cannot close anchor_audit",
        )
        self.assert_rejected(
            lambda value: value["verdict_protocol"]["accepted_audit_only_policy"].update(
                theorem_complete=True
            ),
            "manufactured theorem completion",
        )
        self.assertFalse(
            self.contract["verdict_protocol"]["accepted_audit_only_policy"][
                "phase_can_close"
            ]
        )
        self.assertNotIn(
            "accepted_audit_only",
            self.contract["phases"][6]["worker_verdicts_eligible_for_review"],
        )
        self.assert_rejected(
            lambda value: value["verdict_protocol"]["accepted_audit_only_policy"].update(
                phase_can_close=True
            ),
            "must not close release",
        )

    def test_release_phase_acceptance_requires_theorem_z(self) -> None:
        self.assert_rejected(
            lambda value: value["phases"][6]["theorem_boundary"].update(
                phase_acceptance_implies_theorem_complete=False
            ),
            r"release \[x\] must establish THEOREM-Z",
        )
        self.assert_rejected(
            lambda value: value["phases"][6]["theorem_boundary"].update(
                allowed_theorem_complete_values=[False, True]
            ),
            "release may close only with theorem_complete=true",
        )
        self.assert_rejected(
            lambda value: value["phases"][6]["audit_boundary"].update(
                allowed_audit_complete_values=[False, True]
            ),
            "release may not close with an incomplete audit",
        )

    def test_exit_zero_and_worker_selected_argv_are_insufficient(self) -> None:
        self.assert_rejected(
            lambda value: value["validator_selection"].update(exit_zero_is_sufficient=True),
            "exit zero cannot erase a negative verdict",
        )
        self.assert_rejected(
            lambda value: value["validator_selection"].update(
                worker_or_reviewer_may_select_argv=True
            ),
            "worker-selected argv is forbidden",
        )

    def test_all_legacy_validator_patterns_are_explicitly_superseded(self) -> None:
        rows = [
            row
            for phase in self.contract["phases"]
            for row in phase["superseded_validator_sources"]
        ]
        self.assertEqual(len(rows), 14)
        self.assertTrue(all(
            len(phase["validator_authorities"]) == 1
            and phase["validator_authorities"][0]["path_pattern"]
            == "scripts/stage1_phase_validators/current.py"
            for phase in self.contract["phases"]
        ))
        self.assertTrue(all(row["authority_generation"] == "pre-v2" for row in rows))
        self.assertTrue(all(row["status"] == "superseded" for row in rows))
        self.assertTrue(all(row["positive_acceptance_capable"] is False for row in rows))
        self.assertTrue(
            all(row["superseded_by"] == "Docs/Stage1_Blueprint_v2.md" for row in rows)
        )

    def test_all_723_retired_path_python_files_are_non_authoritative(self) -> None:
        output = subprocess.run(
            [
                "git",
                "grep",
                "-l",
                "-E",
                (
                    r"Docs/Stage1_Blueprint_rev-5\.6\.md|"
                    r"Docs/Stage1_Blueprint_Applicable_Theorems\.md"
                ),
                "HEAD",
                "--",
                "Stage1_Instances/*/*.py",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.splitlines()
        retired = {line.removeprefix("HEAD:") for line in output}
        current_patterns = {
            row["path_pattern"]
            for phase in self.contract["phases"]
            for row in phase["validator_authorities"]
        }
        superseded_patterns = {
            row["path_pattern"]
            for phase in self.contract["phases"]
            for row in phase["superseded_validator_sources"]
        }
        matched_superseded = {
            path
            for path in retired
            if any(
                path == pattern.replace(
                    "{theorem_id}", Path(path).parent.name
                )
                for pattern in superseded_patterns
            )
        }
        self.assertEqual(len(retired), 723)
        self.assertEqual(
            current_patterns, {"scripts/stage1_phase_validators/current.py"}
        )
        self.assertTrue(all(not path.startswith("Stage1_Instances/") for path in current_patterns))
        self.assertEqual(len(matched_superseded), 719)
        self.assertEqual(
            {Path(path).name for path in retired - matched_superseded},
            {"build_obligation_artifacts.py"},
        )

    def test_superseded_validator_cannot_be_promoted_by_field_mutation(self) -> None:
        self.assert_rejected(
            lambda value: value["phases"][0]["superseded_validator_sources"][0].update(
                positive_acceptance_capable=True
            ),
            "superseded validator could accept a phase",
        )
        self.assert_rejected(
            lambda value: value["validator_selection"].update(
                required_authority_generation="pre-v2"
            ),
            "validator authority generation is not stage1-v2",
        )

    def test_current_authority_must_be_central_and_v2_bound(self) -> None:
        def add_legacy_current(value):
            value["phases"][0]["validator_authorities"] = [{
                "path_pattern": "Stage1_Instances/{theorem_id}/check_intake.py",
                "language": "python",
                "argv_template": [
                    "/usr/bin/python3", "-I", "-B", "{validator_path}"
                ],
                "authority_generation": "stage1-v2",
                "requirements_authority": "Docs/Stage1_Blueprint_v2.md",
                "positive_acceptance_capable": True,
            }]

        self.assert_rejected(
            add_legacy_current,
            "current validator is outside the scheduler namespace",
        )

    def test_aliases_do_not_imply_artifact_compliance(self) -> None:
        self.assert_rejected(
            lambda value: value["artifact_resolution"].update(
                matching_path_never_implies_compliance=False
            ),
            "artifact rule disabled",
        )
        self.assert_rejected(
            lambda value: value["phases"][0]["required_artifact_roles"][0].update(
                aliases_are_candidates_only=False
            ),
            "aliases imply compliance",
        )

    def test_per_item_role_map_is_scheduler_owned_and_precedes_review(self) -> None:
        self.assert_rejected(
            lambda value: value["artifact_resolution"].update(
                per_item_role_map_owner="worker"
            ),
            "role map is not authority-owned",
        )
        self.assert_rejected(
            lambda value: value["artifact_resolution"].update(
                per_item_role_map_publication="after_review"
            ),
            "must be frozen before independent review",
        )

    def test_worker_and_review_verdict_vocabularies_remain_separate(self) -> None:
        self.assert_rejected(
            lambda value: value["verdict_protocol"].update(
                worker_verdict_is_not_master_verdict=False
            ),
            "worker and master verdicts are conflated",
        )

    def test_authoritative_contract_digest_rejects_otherwise_valid_tampering(self) -> None:
        value = copy.deepcopy(self.contract)
        value["phases"][0]["semantic_gates"][0]["parameters"]["extra_noop"] = True
        canonical = json.dumps(value, ensure_ascii=True, indent=2) + "\n"
        with self.assertRaisesRegex(validator.ContractError, "contract digest changed"):
            validator.validate_contract_digest(CONTRACT, canonical)

    def test_aggregate_standard_gate_executes_phase_contract_validator(self) -> None:
        source = STANDARD_GATE.read_text(encoding="utf-8")
        self.assertIn("str(PHASE_ACCEPTANCE_VALIDATOR)", source)
        self.assertIn("phase acceptance contract validator failed", source)
        self.assertNotIn("FEATURE_GROUPS", source)
        self.assertNotIn("STANDARD =", source)
        commands = []

        def fail_phase_validator(argv, **_kwargs):
            commands.append(argv)
            if argv == [sys.executable, str(standard.PHASE_ACCEPTANCE_VALIDATOR)]:
                return subprocess.CompletedProcess(argv, 73, "", "synthetic contract failure")
            return subprocess.CompletedProcess(argv, 0, "", "")

        with (
            mock.patch.object(standard.subprocess, "run", side_effect=fail_phase_validator),
            mock.patch.object(
                standard.subprocess,
                "check_output",
                return_value="Docs/Stage1_Blueprint_v2.md\n",
            ),
        ):
            with self.assertRaisesRegex(
                SystemExit,
                "phase acceptance contract validator failed: synthetic contract failure",
            ):
                standard.main()
        self.assertIn(
            [sys.executable, str(standard.PHASE_ACCEPTANCE_VALIDATOR)],
            commands,
        )


if __name__ == "__main__":
    unittest.main()
