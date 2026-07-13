#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1520-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1520"
ITEM = "S56-M-1520-RELEASE"
THEOREM = "THM-M-1520"
BASE_REVISION = "504e508e93fd30c552d715ef48be068d5e131df2"
BASE_TREE = "745f1603c60b7bb726e7789f08a6170c82621b6a"
EXPRESSION_SHA256 = "547fe7d61d57e7ea242aaff7a97763a769275f0c6f1c64d03ca5db45e82a012b"
DENOMINATOR_SHA256 = "3e5ecbc29279547f4e05323bfea6cdbda08b8e69545cffba35df81df8b460e4c"
VALIDATION_RECEIPT_ID = "S56-M-1520-VALIDATION-local-20260714T050000+0800"
VALIDATION_RECEIPT_SHA256 = "239168d2c6c0e18a8d7be79c40889535355f2f074237180c01870b345c3e48e8"
INVENTORY_IDS = [
    "M1520-ROOT", "M1520-S-DEFS", "M1520-S-DOMAIN", "M1520-S-BOUNDARY",
    "M1520-S-FOUNDATION", "M1520-N-FLOW", "M1520-B-DIVERGENCE",
    "M1520-C-VARIATION", "M1520-L-JACOBIAN", "M1520-L-MEASURABLE",
    "M1520-L-CHANGE", "M1520-T-ALL-TIMES", "M1520-T-ASSEMBLE",
    "M1520-X-SOURCE", "M1520-X-PROVENANCE", "M1520-X-TRUST",
]
RECONCILED_INPUTS = {
    "intake.json": "fe1f419b89de7b5f7da97a0c0e6855ddf058a3d843ef8d54cc95d84dd257304e",
    "Statement.lean": "0b3bb7e3410047f58ca7790fd4640c547604bbf8b2e715b0bf46c32634ce2ef0",
    "Proof.lean": "24fe83d637e32fba4339836b621d973364b3aa216d309026919209184d4958ac",
    "ObligationTree.lean": "e73e0e967957fe57d94dba19206bd7f23e5499f54149e19ca693787500e4d4d0",
    "obligation-registry.json": "705f92d2c5a61eb289f27aef71ff454d4afc397f7039e57044498af825cad851",
    "typed-graphs.json": "e4116a46fa9a193b332bc30be1c3c025d258fa2318d328e53b3e7fb1fe866a90",
    "proof-receipt.json": "26dab222a908b9b94a79a060a820931ddaad11b694fa8cb5c301c9cdcfe5b301",
    "validation-spec.json": "a642405bbf507e18e5323e1889e9b83b3451c6ba41d3dce8b29c2c550a3cf58e",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "b7c9294faa74883dc680e8e2b475c77217c8dfa0e76e7b2b643642a72f2f7917",
    "source_statement_crosswalk.md": "a0acd0ac603b566b732f6ac2f767ad15357004413e5aee4479ee08d68c361f97",
    "anchor_audit.md": "da7dc36cb1b07bc2bade0d3a0adff0a1840a4fb101e763b763179020d3bf73b8",
    "check_obligation_tree.py": "e035b6c693027fdbabeae149404845622cb0cbef0f762a7d53b790e5d8b6be10",
}
SUMMARY_LINES = [
    "release-decision: ok (blocked at validation dependency acceptance)",
    "structured authority: ok (root M3/open; M1520-T-ALL-TIMES remains the cut)",
    "validation replay boundary: fail closed (historical base and phase packet unavailable)",
    "AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]",
    "authoritative vector: H2/M3/R3 unchanged",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 60) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    assert result.returncode == 0, (argv, result.returncode, result.stdout)
    return result.stdout.strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    intake = load(HERE / "intake.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")

    assert run(["git", "rev-parse", "HEAD"]) == BASE_REVISION
    assert run(["git", "rev-parse", "HEAD^{tree}"]) == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 189 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 189,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1520-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1520-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    assert decision["reconciled_inputs"] == RECONCILED_INPUTS
    for name, expected in RECONCILED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"

    assert intake["canonical_formal_target"]["elaborated_expression_hash"] == (
        f"sha256:{EXPRESSION_SHA256}"
    )
    assert intake["root_vector"] == {
        "human": "H2", "machine": "M3", "readability": "R3"
    }
    assert registry["root_obligation_id"] == "M1520-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == ["M1520-T-ASSEMBLE"]
    assert closure["root_closed"] is closure["audit_complete"] is False
    assert closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == ["M1520-T-ALL-TIMES"]

    assert proof["accepted"] is False and proof["result"]["root_kernel_closed"] is False
    assert validation["receipt_id"] == VALIDATION_RECEIPT_ID
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["accepted_receipt_ids"] == []
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == "dependency.S56-M-1520-PROOF.master_acceptance"

    assert decision["item_id"] == ITEM and decision["verdict"] == "blocked"
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == []
    vector = {"H": "H2", "M": "M3", "R": "R3"}
    assert decision["root_vector"]["accepted_before"] == vector
    assert decision["root_vector"]["accepted_after"] == vector
    assert decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked",
    }
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_theorem_gate"]["gate_id"] == (
        "M1520-C-VARIATION.kernel_closure"
    )
    assert decision["first_failed_release_assurance_gate"]["gate_id"] == (
        "S56-7.3-TRANSITIVE-PROVENANCE-CLOSURE"
    )
    for key in (
        "authoritative_root_closure", "current_validation_recipe_replay",
        "human_source_acceptance", "readability_acceptance",
        "foundation_and_trust_closure", "hermetic_release_reproduction",
        "supply_chain_closure", "independent_release_verification",
        "deterministic_release_bundle",
    ):
        assert decision["evidence_reconciliation"][key].startswith("missing"), key

    assert spec["recipe_id"] == "S56-M-1520-RELEASE-negative-reconciliation-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert receipt["recipe"] == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids", "covered_declarations",
        )
    }

    assert receipt["receipt_id"] == "S56-M-1520-RELEASE-local-20260714"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == vector
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["first_failed_dependency_gate"] == (
        "dependency.S56-M-1520-VALIDATION.master_acceptance"
    )
    assert receipt["first_failed_theorem_gate"] == "M1520-C-VARIATION.kernel_closure"
    assert receipt["first_failed_release_gate"] == (
        "S56-7.3-TRANSITIVE-PROVENANCE-CLOSURE"
    )
    assert receipt["remaining_root_cut_set"] == decision["remaining_root_cut_set"]
    assert receipt["inputs"]["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["inputs"]["release_decision_sha256"] == sha256(HERE / "release-decision.json")
    assert receipt["inputs"]["release_validation_sha256"] == sha256(HERE / "release-validation.md")
    assert receipt["inputs"]["check_release_sha256"] == sha256(HERE / "check_release.py")

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["output_summary"] == SUMMARY_LINES

    status = run(["git", "status", "--short", "--untracked-files=all"])
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    obligation_output = run([
        "python3", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"
    ])
    assert "root closure: open (M3); analytic package remains M4" in obligation_output
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
