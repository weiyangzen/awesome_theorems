#!/usr/bin/env python3
"""Fail-closed consistency check for S56-M-0526-RELEASE."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0526"
EXPECTED_HEAD = "bb2a1ec294938a22b88699da0d30ced721d8ee7b"
EXPECTED_TREE = "d8d58ab94c83274db18efd3af989171acb898759"
EXPECTED_TARGETS_SHA256 = "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
EXPECTED_DAG_SHA256 = "53c09b6b05a2caa909ee27a0d9aace9846e73c702e2182fe8ebfd6b2f6e35728"
ROOT_VECTOR = ["H2", "M4", "R4"]
OPEN_PROOF_CUT = [
    "SVK-CHANGE-BASEPATH",
    "SVK-WORD-DEFINITION",
    "SVK-REFINEMENT-INVARIANCE",
    "SVK-HOMOTOPY-INVARIANCE",
    "SVK-LIFT-HOM",
    "SVK-GENERATION",
    "SVK-AGREEMENT-ON-WORDS",
]
FROZEN_ROOT_CUT = [
    "SVK-MAP-FUNCTORIALITY",
    "SVK-LEBESGUE-NUMBER",
    *OPEN_PROOF_CUT,
]
PROVISIONAL_OBLIGATIONS = [
    "SVK-MAP-FUNCTORIALITY",
    "SVK-SQUARE",
    "SVK-LEBESGUE-NUMBER",
]
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0526/check_release.py",
    "Stage1_Instances/THM-M-0526/release-decision.json",
    "Stage1_Instances/THM-M-0526/release-phase.md",
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

    result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(result, dict), path
    return result


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


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                output.append("\n")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


decision = load(HERE / "release-decision.json")
instance = load(HERE / "instance.json")
task_dag = load(HERE / "task-dag.json")
statement = load(HERE / "statement.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
proof = load(HERE / "proof-receipt.json")
blocker = load(HERE / "proof-blocker.json")
validation = load(HERE / "validation-receipt.json")
targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

assert digest(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json") == EXPECTED_TARGETS_SHA256
assert digest(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json") == EXPECTED_DAG_SHA256
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == EXPECTED_HEAD
assert subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True).strip() == EXPECTED_TREE

target = next(row for row in targets["targets"] if row["theorem_id"] == "THM-M-0526")
assert target == {
    "execution_rank": 583,
    "legacy_priority_slot": None,
    "theorem_id": "THM-M-0526",
    "name": "范坎彭定理",
    "category": "拓扑学 / 代数拓扑",
    "source_status_untrusted": "已验证",
    "baseline": "L0",
    "rework_required": True,
    "legacy_artifacts_accepted": False,
    "target_lane": "hard_statement_first_partial_verification",
    "intake_score": 132,
    "lifecycle_mode": "planned",
    "theorem_complete": False,
}
release_item = next(row for row in execution["items"] if row["id"] == decision["item_id"])
validation_item = next(row for row in execution["items"] if row["id"] == validation["item_id"])
assert release_item == {
    "id": "S56-M-0526-RELEASE",
    "theorem_id": "THM-M-0526",
    "execution_rank": 583,
    "phase": "release",
    "layer": 6,
    "state": "[ ]",
    "depends_on": ["S56-M-0526-VALIDATION"],
    "owned_paths": ["Stage1_Instances/THM-M-0526"],
    "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
assert validation_item["depends_on"] == ["S56-M-0526-PROOF"]

assert instance["lifecycle"] == "planned"
assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
assert instance["accepted_proof_state"] == []
assert instance["audit_complete"] is instance["theorem_complete"] is False
assert task_dag["lifecycle"] == "planned" and task_dag["accepted_states"] == []
assert next(row for row in task_dag["tasks"] if row["id"] == decision["item_id"])["state"] == "open"
assert statement["canonical_formal_target"]["declaration_or_expression"] == decision["canonical_target"]
assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == decision["canonical_target_expression_sha256"]
assert statement["theorem_complete"] is False
assert registry["frozen_denominator_sha256"] == decision["registry_denominator_sha256"]
assert registry["closure_summary"] == {
    "required": 17,
    "closed": 0,
    "open": 17,
    "root_closed": False,
}
assert graphs["deduplication"]["distinct_terminal_proof_bodies"] == 0
assert "no proof-body credit" in graphs["status_boundary"]

assert decision["schema_version"] == "stage1-release-decision/1.0"
assert decision["item_id"] == "S56-M-0526-RELEASE"
assert decision["theorem_id"] == "THM-M-0526" and decision["execution_rank"] == 583
assert decision["phase"] == decision["intent"] == "release"
assert decision["depends_on"] == ["S56-M-0526-VALIDATION"]
assert decision["base_revision"] == EXPECTED_HEAD and decision["base_tree"] == EXPECTED_TREE
assert decision["verdict"] == "blocked" and decision["release_grade"] is False
assert decision["content_addressed_release_evidence"] is False
assert decision["support_state"] == "provisional_worker_selftest"
assert decision["proposed_state"] == "[_]" and decision["accepted"] is False
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["root_vector"]["recorded_before"] == ROOT_VECTOR
assert decision["root_vector"]["recorded_after"] == ROOT_VECTOR
assert decision["root_vector"]["best_provisional_evidence"] == ROOT_VECTOR
assert decision["changed_paths"] == CHANGED_PATHS

for name, expected in decision["reconciled_inputs"].items():
    assert digest(HERE / name) == expected, f"reconciled input drifted: {name}"

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0526-VALIDATION"
assert dependency["authoritative_projection"] == validation_item["state"] == "[_]"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest(HERE / "validation-receipt.json")
assert dependency["receipt_base_revision"] == validation["base_revision"]
assert dependency["receipt_base_tree"] == validation["base_tree"]
assert dependency["support_state"] == validation["support_state"] == "provisional_worker_selftest"
assert dependency["proposed_state"] == validation["proposed_state"] == "[_]"
assert dependency["accepted"] is validation["accepted"] is False
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False

assert proof["support_state"] == "provisional_worker_selftest"
assert proof["accepted"] is False and proof["accepted_closed_obligation_ids"] == []
assert proof["provisionally_closed_obligation_ids"] == PROVISIONAL_OBLIGATIONS
assert proof["result"]["root_kernel_closed"] is False
assert proof["remaining_root_cut_set"] == OPEN_PROOF_CUT
assert blocker["remaining_root_cut_set"] == OPEN_PROOF_CUT
assert blocker["root_closed"] is blocker["theorem_complete"] is False
assert validation["result"]["provisionally_revalidated_obligation_ids"] == PROVISIONAL_OBLIGATIONS
assert validation["result"]["accepted_closed_obligation_ids"] == []
assert validation["result"]["root_closed"] is validation["result"]["root_kernel_closed"] is False
assert validation["result"]["root_vector_before"] == {"H": "H2", "M": "M4", "R": "R4"}
assert validation["result"]["root_vector_after"] == validation["result"]["root_vector_before"]
assert validation["result"]["remaining_root_cut_set"] == OPEN_PROOF_CUT
assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
assert validation["first_failed_gate"].startswith("SVK-CHANGE-BASEPATH:")
assert validation["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
assert registry["root_cut_set"] == FROZEN_ROOT_CUT
assert decision["remaining_proof_frontier"] == OPEN_PROOF_CUT
assert decision["remaining_root_cut_set"] == FROZEN_ROOT_CUT

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
assert decision["next_failed_theorem_gate"]["gate_id"] == "SVK-CHANGE-BASEPATH"
assert decision["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"

reconciliation = decision["evidence_reconciliation"]
assert reconciliation["accepted_closed_obligation_ids"] == []
assert reconciliation["exact_root_kernel_closure"] is False
assert reconciliation["root_machine_debt"] == "M4"
assert reconciliation["provisional_implementation_frontier"] == OPEN_PROOF_CUT
assert reconciliation["audit_z_accepted"] is reconciliation["theorem_z_accepted"] is False
assert reconciliation["master_acceptance"] is False
for key in (
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

cut_set = "\n".join(decision["remaining_assurance_gates"])
for fragment in (
    "master acceptance",
    "accepted exact root composition",
    "AUDIT-Z inventory",
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
assert "Open proof debt may remain classified" in decision["audit_retry_condition"]
assert "After accepted AUDIT-Z" in decision["theorem_retry_condition"]

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe|extern)\b",
    flags=re.MULTILINE,
)
all_lean = "\n".join(
    source_without_comments(path.read_text(encoding="utf-8"))
    for path in sorted(HERE.glob("*.lean"))
)
assert prohibited.search(all_lean) is None
assert not re.search(r"^theorem[ \t]+SeifertVanKampenTarget\b", all_lean, re.MULTILINE)

tree_check = run(["python3", "-B", str(HERE / "check_obligation_tree.py")])
assert tree_check.returncode == 0, tree_check.stdout
assert "validated 17 obligations, 9 leaves, 16 proof edges" in tree_check.stdout

lean_replay = run(["bash", str(HERE / "check_proof.sh")], timeout=360)
assert lean_replay.returncode == 0, lean_replay.stdout
assert "PASS: three THM-M-0526 local proof bodies elaborated with allowed axioms" in lean_replay.stdout

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
    assert packet["known_failures"] == decision["known_failures"]
    summary = packet["output_summary"]
    assert summary["verdict"] == decision["verdict"]
    assert summary["lifecycle_before"] == summary["lifecycle_after"] == "planned"
    assert summary["root_vector_before"] == summary["root_vector_after"] == ROOT_VECTOR
    assert summary["audit_complete"] is summary["theorem_complete"] is False
    assert summary["accepted_receipt_ids"] == []
    assert summary["remaining_root_cut_set"] == FROZEN_ROOT_CUT
    assert summary["remaining_proof_frontier"] == OPEN_PROOF_CUT
    expected_commands = [
        ["python3", "Docs/tools/check_stage1_standard.py"],
        ["python3", "scripts/stage1_target.py", "check"],
        ["python3", "scripts/stage1_target.py", "show", "THM-M-0526"],
        ["git", "status", "--short", "--untracked-files=all"],
        ["python3", "-B", "Stage1_Instances/THM-M-0526/check_obligation_tree.py"],
        ["bash", "Stage1_Instances/THM-M-0526/check_proof.sh"],
        ["python3", "-B", "Stage1_Instances/THM-M-0526/check_release.py", "--worker-packet", ".stage1-worker-selftest.json"],
        ["python3", "-m", "json.tool", "Stage1_Instances/THM-M-0526/release-decision.json"],
        ["python3", "-m", "json.tool", ".stage1-worker-selftest.json"],
        ["git", "diff", "--check", "--", "Stage1_Instances/THM-M-0526", ".stage1-worker-selftest.json"],
    ]
    assert [command.get("argv") for command in packet["commands"]] == expected_commands
    assert all(command.get("exit_code") == 0 and command.get("result") for command in packet["commands"])
    status = run(["git", "status", "--short", "--untracked-files=all"])
    assert status.returncode == 0, status.stdout
    actual = {line[3:] for line in status.stdout.splitlines()}
    actual.discard("Formalizations/Lean/.lake")
    assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))

for relative in CHANGED_PATHS:
    path = ROOT / relative
    if not path.exists() and relative == ".stage1-worker-selftest.json" and args.worker_packet is None:
        continue
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

print("release-decision: ok (blocked; validation dependency provisional and unaccepted)")
print("root reconciliation: H2/M4/R4; accepted obligations=[]; frozen nine-node cut unchanged; seven-node proof frontier open")
print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")
print("release gates: cold/offline, supply-chain, independent verifier, deterministic bundle all fail closed")
