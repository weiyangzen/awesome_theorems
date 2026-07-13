#!/usr/bin/env python3
"""Fail-closed consistency check for S56-M-0498-RELEASE."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0498"
EXPECTED_HEAD = "bad90e2e2479d376609447202eb4f437789d0d11"
EXPECTED_TREE = "df3ade7b4d06057f8aac33369c3d69bd391aa05a"
EXPECTED_TARGETS_SHA256 = "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
EXPECTED_DAG_SHA256 = "62a7ebe18c138d5b4413cb1bd9409e6f9597502966045c142e34fab3fbcc2614"
ROOT_VECTOR = ["H3", "M4", "R4"]
OPEN_ROOT_CUT = ["M0498-T-ANALYTIC"]
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0498/check_release.py",
    "Stage1_Instances/THM-M-0498/release-decision.json",
    "Stage1_Instances/THM-M-0498/release-validation.md",
]

if not __debug__:
    raise RuntimeError("release reconciliation requires assertions; optimized mode is forbidden")

parser = argparse.ArgumentParser()
parser.add_argument("--worker-packet", type=Path)
args = parser.parse_args()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )


def git_value(expression: str) -> str:
    result = run(["git", "rev-parse", expression], timeout=10)
    assert result.returncode == 0, result.stdout
    return result.stdout.strip()


decision = load(HERE / "release-decision.json")
intake = load(HERE / "intake.json")
statement = load(HERE / "statement.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
proof = load(HERE / "proof-receipt.json")
proof_blocker = load(HERE / "proof-blocker.json")
validation = load(HERE / "validation-receipt.json")
targets_path = ROOT / "Docs" / "Stage1_Targets_rev-5.6.json"
dag_path = ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json"
targets = load(targets_path)
dag = load(dag_path)

assert digest(targets_path) == EXPECTED_TARGETS_SHA256
assert digest(dag_path) == EXPECTED_DAG_SHA256
assert decision["base_revision"] == EXPECTED_HEAD
assert decision["base_tree"] == EXPECTED_TREE
assert git_value(f"{EXPECTED_HEAD}^{{tree}}") == EXPECTED_TREE
ancestor = run(["git", "merge-base", "--is-ancestor", EXPECTED_HEAD, "HEAD"], timeout=10)
assert ancestor.returncode == 0, ancestor.stdout

target = next(row for row in targets["targets"] if row["theorem_id"] == "THM-M-0498")
validation_item = next(row for row in dag["items"] if row["id"] == "S56-M-0498-VALIDATION")
release_item = next(row for row in dag["items"] if row["id"] == "S56-M-0498-RELEASE")
assert target["execution_rank"] == decision["execution_rank"] == 258
assert target["baseline"] == "L0" and target["rework_required"] is True
assert target["legacy_artifacts_accepted"] is False
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert validation_item["state"] == "[_]"
assert release_item == {
    "id": "S56-M-0498-RELEASE",
    "theorem_id": "THM-M-0498",
    "execution_rank": 258,
    "phase": "release",
    "layer": 6,
    "state": "[ ]",
    "depends_on": ["S56-M-0498-VALIDATION"],
    "owned_paths": ["Stage1_Instances/THM-M-0498"],
    "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}

assert decision["schema_version"] == "stage1-release-decision/1.0"
assert decision["normative_profile"] == "machine-theorem-assurance/1.0"
assert decision["item_id"] == release_item["id"]
assert decision["theorem_id"] == target["theorem_id"]
assert decision["phase"] == decision["intent"] == "release"
assert decision["verdict"] == "blocked"
assert decision["decision_support"] == "provisional_worker_selftest"
assert decision["proposed_state"] == "[_]"
assert decision["accepted"] is False and decision["release_grade"] is False
assert decision["content_addressed_release_evidence"] is False
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []

for name, expected in decision["reconciled_inputs"].items():
    assert digest(HERE / name) == expected, f"reconciled input drifted: {name}"
assert decision["canonical_target_expression_sha256"] == statement["canonical_formal_target"]["elaborated_expression_sha256"]
assert decision["registry_denominator_sha256"] == registry["denominator_sha256"] == graphs["registry_denominator_sha256"]

dependency = decision["dependency"]
assert dependency["item_id"] == validation_item["id"] == validation["item_id"]
assert dependency["authoritative_projection"] == validation_item["state"] == "[_]"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest(HERE / "validation-receipt.json")
assert dependency["receipt_base_revision"] == validation["base_revision"]
assert dependency["receipt_base_tree"] == validation["base_tree"]
assert dependency["support_state"] == validation["support_state"] == "provisional_worker_selftest"
assert dependency["proposed_state"] == validation["proposed_state"] == "[_]"
assert dependency["accepted"] is validation["accepted"] is False
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["content_addressed_release_evidence"] is validation["content_addressed_release_evidence"] is False
assert dependency["master_accepted"] is False

root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0498-ROOT")
current_vector = [root["human_debt"], root["machine_debt"], root["readability_debt"]]
assert current_vector == ROOT_VECTOR
assert decision["root_vector"]["accepted_before"] == ROOT_VECTOR
assert decision["root_vector"]["accepted_after"] == ROOT_VECTOR
assert decision["root_vector"]["best_provisional_evidence"] == ROOT_VECTOR
assert decision["root_vector"]["stale_intake_projection"] == [
    intake["root_vector"]["human"],
    intake["root_vector"]["machine"],
    intake["root_vector"]["readability"],
] == ["H2", "M3", "R3"]

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["audit_complete"] is closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == OPEN_ROOT_CUT
assert validation["root_vector_after"] == {"H": "H3", "M": "M4", "R": "R4"}
result = validation["result"]
assert result["accepted_closed_obligation_ids"] == []
assert result["root_kernel_closed"] is False and result["root_machine_debt"] == "M4"
assert result["open_root_cut_set"] == OPEN_ROOT_CUT
assert result["audit_complete"] is result["theorem_complete"] is False
assert result["enumeration_nonvacuity_or_realizability"].startswith("fail_closed:")
assert proof["closed_obligation_ids"] == []
assert proof["result"]["root_closed"] is proof["result"]["theorem_complete"] is False
assert proof["remaining_root_cut_set"] == OPEN_ROOT_CUT
assert proof_blocker["outcome"] == "blocked" and proof_blocker["machine_classification"] == "M4"
assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False

terminal = decision["terminal_decisions"]
assert terminal == {
    "audit_complete": False,
    "theorem_complete": False,
    "audit_z": "blocked",
    "theorem_z": "blocked",
    "release_accepted": False,
    "master_acceptance": False,
}
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["next_failed_theorem_gate"]["gate_id"] == "S56-M-0498-ROOT-KERNEL-CLOSURE"
assert decision["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"

reconciliation = decision["evidence_reconciliation"]
assert reconciliation["accepted_closed_obligation_ids"] == []
assert reconciliation["exact_root_kernel_closure"] is False
assert reconciliation["root_machine_debt"] == "M4"
assert reconciliation["minimal_open_root_cut"] == OPEN_ROOT_CUT
assert reconciliation["audit_z_accepted"] is reconciliation["theorem_z_accepted"] is False
assert reconciliation["master_acceptance"] is False
for key in (
    "zero_enumeration_realizability",
    "validation_dependency_acceptance",
    "audit_inventory_reconciliation",
    "human_source_acceptance",
    "readability_acceptance",
    "complete_provenance_foundation_tcb_closure",
    "immutable_clean_release_input",
    "hermetic_cold_offline_replay",
    "sbom_license_archive_closure",
    "independent_clean_runner_attestations",
    "independently_implemented_minimal_verifier",
    "protected_ci_and_mutation_gates",
    "deterministic_release_bundle",
):
    assert reconciliation[key] == "missing", key

cut_set = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "master acceptance",
    "M0498-T-ANALYTIC",
    "NontrivialZeroEnumeration",
    "AUDIT-Z",
    "H0 primary-source",
    "R0 node-by-node",
    "transitive declaration/import/artifact",
    "immutable clean",
    "empty-cache network-denied cold build",
    "SBOM, license",
    "two signed attestations",
    "minimal release verifier",
    "mutation, adversarial, differential, and metamorphic",
    "deterministic content-addressed release bundle",
    "THEOREM-Z",
):
    assert fragment in cut_set, f"remaining cut set omits {fragment!r}"

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)
for path in HERE.glob("*.lean"):
    source = re.sub(r"/-.*?-/", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    source = re.sub(r"--.*$", "", source, flags=re.MULTILINE)
    assert prohibited.search(source) is None, f"prohibited construct in {path.name}"

tree_check = run(["python3", "-B", str(HERE / "check_obligation_tree.py")], timeout=60)
assert tree_check.returncode == 0, tree_check.stdout
assert "root closure: open (M4)" in tree_check.stdout
assert "analytic explicit-formula package remains M4" in tree_check.stdout

if args.worker_packet is not None:
    packet = load(args.worker_packet.resolve())
    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == decision["item_id"]
    assert packet["base_revision"] == decision["base_revision"]
    assert packet["state"] == decision["proposed_state"] == "[_]"
    assert packet["changed_paths"] == decision["changed_paths"] == CHANGED_PATHS
    assert packet["known_failures"] and all(packet["known_failures"])
    assert packet["output_summary"]["verdict"] == decision["verdict"]
    assert packet["output_summary"]["lifecycle_before"] == decision["lifecycle_before"]
    assert packet["output_summary"]["lifecycle_after"] == decision["lifecycle_after"]
    assert packet["output_summary"]["root_vector_before"] == ROOT_VECTOR
    assert packet["output_summary"]["root_vector_after"] == ROOT_VECTOR
    assert packet["output_summary"]["audit_complete"] is False
    assert packet["output_summary"]["theorem_complete"] is False
    assert packet["output_summary"]["accepted_receipt_ids"] == []
    assert packet["output_summary"]["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert all(
        isinstance(command.get("argv"), list)
        and isinstance(command.get("exit_code"), int)
        and command.get("result")
        for command in packet["commands"]
    )
    status = run(["git", "status", "--short", "--untracked-files=all"], timeout=10)
    assert status.returncode == 0, status.stdout
    actual = {
        line[3:]
        for line in status.stdout.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))

print("release-decision: ok (blocked; validation dependency provisional and unaccepted)")
print("root reconciliation: H3/M4/R4; accepted obligations=[]; open cut=[M0498-T-ANALYTIC]")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
print("release gates: cold/offline, supply-chain, independent verifier, deterministic bundle all fail closed")
