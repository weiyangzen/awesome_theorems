#!/usr/bin/env python3
"""Focused tests for the read-only Stage1 legacy migration inventory."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


MODULE_PATH = Path(__file__).with_name("stage1_legacy_migration_inventory.py")
SPEC = importlib.util.spec_from_file_location("stage1_legacy_inventory_under_test", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
inventory = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = inventory
SPEC.loader.exec_module(inventory)


def run(root: Path, *argv: str) -> str:
    result = subprocess.run(argv, cwd=root, text=True, capture_output=True, check=False)
    if result.returncode:
        raise AssertionError(f"{argv!r} failed:\n{result.stdout}\n{result.stderr}")
    return result.stdout.strip()


def contract() -> dict[str, object]:
    common_fields = [
        "/schema_version",
        "/receipt_id",
        "/item_id",
        "/theorem_id",
        "/phase",
        "/intent",
        "/base_revision",
        "/base_tree",
        "/inputs",
        "/support_state",
        "/proposed_state",
        "/accepted",
        "/verdict",
        "/selftest_status",
        "/selftest_result/exit_code",
        "/selftest_result/commands",
        "/known_failures",
        "/first_failed_gate",
        "/retry_condition",
        "/status_boundary",
        "/audit_complete",
        "/theorem_complete",
        "/invalidation_inputs",
    ]
    return {
        "schema_version": "stage1-phase-acceptance-contracts/1.0",
        "phases": [
            {
                "phase": "intake",
                "item_suffix": "INTAKE",
                "required_artifact_roles": [
                    {
                        "role": "instance_manifest",
                        "requirement": "required",
                        "cardinality": "exactly_one",
                        "resolution": "path_candidates",
                        "path_candidates": ["Stage1_Instances/{theorem_id}/instance.json"],
                    },
                    {
                        "role": "phase_receipt",
                        "requirement": "required",
                        "cardinality": "exactly_one",
                        "resolution": "path_candidates",
                        "path_candidates": [
                            "Stage1_Instances/{theorem_id}/intake-receipt.json"
                        ],
                    },
                ],
                "phase_receipt_required_fields": common_fields,
                "validator_authorities": [
                    {
                        "path_pattern": "scripts/stage1_phase_validators/check_intake.py",
                        "language": "python",
                    }
                ],
                "superseded_validator_sources": [
                    {
                        "path_pattern": "Stage1_Instances/{theorem_id}/check_intake.py",
                        "language": "python",
                    }
                ],
            }
        ],
    }


def receipt(base: str, tree: str, *, phase: str = "intake") -> dict[str, object]:
    return {
        "schema_version": inventory.RECEIPT_SCHEMA,
        "receipt_id": "fixture-intake",
        "item_id": "S56-M-0001-INTAKE",
        "theorem_id": "THM-M-0001",
        "phase": phase,
        "intent": "intake",
        "base_revision": base,
        "base_tree": tree,
        "inputs": {},
        "support_state": "provisional_worker_selftest",
        "proposed_state": "[_]",
        "accepted": False,
        "verdict": "no_state_change",
        "selftest_status": "passed",
        "selftest_result": {"exit_code": 0, "commands": ["python3 check_intake.py"]},
        "known_failures": [],
        "first_failed_gate": None,
        "retry_condition": None,
        "status_boundary": "phase only",
        "audit_complete": False,
        "theorem_complete": False,
        "invalidation_inputs": [],
    }


SEMANTIC_VALIDATOR = """#!/usr/bin/env python3
import json
print(json.dumps({
    "schema_version": "stage1-validator-semantic-result/1.0",
    "item_id": "S56-M-0001-INTAKE",
    "theorem_id": "THM-M-0001",
    "phase": "intake",
    "status": "passed",
    "verdict": "phase_accepted",
    "phase_accepted": True,
    "audit_complete": False,
    "theorem_complete": False,
    "phase_predicate_proven": True,
    "first_failed_gate": None,
    "open_obligations": 0,
    "stale_inputs": [],
    "blocked": False
}))
"""


class Fixture:
    def __init__(self, *, tracked_contract: bool = True) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        run(self.root, "git", "init", "-q", "-b", "main")
        run(self.root, "git", "config", "user.name", "Inventory Tests")
        run(self.root, "git", "config", "user.email", "inventory@example.invalid")
        docs = self.root / "Docs"
        self.instance = self.root / "Stage1_Instances" / "THM-M-0001"
        self.validator = self.root / "scripts" / "stage1_phase_validators"
        docs.mkdir()
        self.instance.mkdir(parents=True)
        self.validator.mkdir(parents=True)
        (docs / "Stage1_Blueprint_v2.md").write_text(
            "- [_] `S56-M-0001-INTAKE` / `THM-M-0001` / `intake`: fixture {attempts=1}\n",
            encoding="utf-8",
        )
        self.contract_path = docs / "Stage1_Phase_Acceptance_Contracts.json"
        self.contract_path.write_text(json.dumps(contract()) + "\n", encoding="utf-8")
        (self.instance / "instance.json").write_text(
            '{"theorem_id":"THM-M-0001"}\n', encoding="utf-8"
        )
        (self.instance / "check_intake.py").write_text(
            SEMANTIC_VALIDATOR, encoding="utf-8"
        )
        (self.validator / "check_intake.py").write_text(
            SEMANTIC_VALIDATOR, encoding="utf-8"
        )
        run(self.root, "git", "add", ".")
        if not tracked_contract:
            run(self.root, "git", "reset", "-q", "Docs/Stage1_Phase_Acceptance_Contracts.json")
        run(self.root, "git", "commit", "-qm", "base")
        self.base = run(self.root, "git", "rev-parse", "HEAD")
        self.tree = run(self.root, "git", "rev-parse", "HEAD^{tree}")

    def add_receipt(self, **updates: object) -> None:
        value = receipt(self.base, self.tree)
        value.update(updates)
        (self.instance / "intake-receipt.json").write_text(
            json.dumps(value) + "\n", encoding="utf-8"
        )
        run(self.root, "git", "add", ".")
        run(self.root, "git", "commit", "-qm", "receipt")

    def close(self) -> None:
        self.temp.cleanup()


class InventoryTests(unittest.TestCase):
    def test_head_contract_is_required_by_default(self) -> None:
        fixture = Fixture(tracked_contract=False)
        self.addCleanup(fixture.close)
        with self.assertRaisesRegex(inventory.InventoryError, "not tracked"):
            inventory.build_inventory(fixture.root)

    def test_candidate_contract_is_explicitly_non_authoritative(self) -> None:
        fixture = Fixture(tracked_contract=False)
        self.addCleanup(fixture.close)
        result = inventory.build_inventory(
            fixture.root, candidate_contract=fixture.contract_path
        )
        self.assertEqual(result["authority_mode"], "candidate_preflight")
        self.assertFalse(result["authoritative_for_acceptance"])
        self.assertFalse(result["items"][0]["acceptance_claimed"])

    def test_missing_receipt_and_runtime_checks_do_not_fake_clear(self) -> None:
        fixture = Fixture()
        self.addCleanup(fixture.close)
        result = inventory.build_inventory(fixture.root)
        item = result["items"][0]
        classes = {row["category"]: row for row in item["classifications"]}
        self.assertEqual(classes["missing_receipt"]["status"], "blocked")
        self.assertEqual(classes["legacy_receipt"]["status"], "unknown")
        self.assertEqual(classes["phase_mismatch"]["status"], "unknown")
        self.assertEqual(classes["validator_authority_superseded"]["status"], "blocked")
        self.assertEqual(classes["validator_base_mismatch"]["status"], "blocked")
        self.assertEqual(classes["validator_stdout_mismatch"]["status"], "unknown")
        self.assertEqual(classes["sandbox_incompatible"]["status"], "unknown")
        self.assertFalse(item["migration_ready"])

    def test_phase_mismatch_is_content_and_head_blob_bound(self) -> None:
        fixture = Fixture()
        self.addCleanup(fixture.close)
        fixture.add_receipt(phase="proof")
        result = inventory.build_inventory(fixture.root)
        item = result["items"][0]
        row = next(
            value for value in item["classifications"] if value["category"] == "phase_mismatch"
        )
        self.assertEqual(row["status"], "blocked")
        self.assertEqual(len(row["bindings"]), 1)
        binding = row["bindings"][0]
        self.assertRegex(binding["git_blob"], r"^[0-9a-f]{40,64}$")
        receipt_path = fixture.instance / "intake-receipt.json"
        self.assertEqual(binding["sha256"], hashlib.sha256(receipt_path.read_bytes()).hexdigest())

    def test_static_markers_remain_unknown_without_validator_execution(self) -> None:
        fixture = Fixture()
        self.addCleanup(fixture.close)
        fixture.add_receipt()
        result = inventory.build_inventory(fixture.root)
        item = result["items"][0]
        classes = {row["category"]: row for row in item["classifications"]}
        self.assertEqual(classes["missing_receipt"]["status"], "clear")
        self.assertEqual(classes["legacy_receipt"]["status"], "clear")
        self.assertEqual(classes["phase_mismatch"]["status"], "clear")
        self.assertEqual(classes["validator_authority_superseded"]["status"], "blocked")
        self.assertEqual(classes["validator_base_mismatch"]["status"], "blocked")
        self.assertEqual(classes["validator_stdout_mismatch"]["status"], "unknown")
        self.assertEqual(classes["sandbox_incompatible"]["status"], "unknown")
        self.assertFalse(item["migration_ready"])
        self.assertEqual(result["migration_ready_count"], 0)

    def test_inventory_and_each_item_have_recomputable_digests(self) -> None:
        fixture = Fixture()
        self.addCleanup(fixture.close)
        fixture.add_receipt()
        result = inventory.build_inventory(fixture.root)
        item = dict(result["items"][0])
        item_digest = item.pop("item_sha256")
        self.assertEqual(item_digest, inventory.sha256_bytes(inventory.canonical_json(item)))
        value = dict(result)
        digest = value.pop("inventory_sha256")
        self.assertEqual(digest, inventory.sha256_bytes(inventory.canonical_json(value)))

    def test_candidate_preflight_is_deterministic_and_never_ready(self) -> None:
        fixture = Fixture(tracked_contract=False)
        self.addCleanup(fixture.close)
        first = inventory.build_inventory(
            fixture.root, candidate_contract=fixture.contract_path
        )
        second = inventory.build_inventory(
            fixture.root, candidate_contract=fixture.contract_path
        )
        self.assertEqual(first, second)
        self.assertEqual(first["migration_ready_count"], 0)
        self.assertFalse(first["authoritative_for_acceptance"])


if __name__ == "__main__":
    unittest.main()
