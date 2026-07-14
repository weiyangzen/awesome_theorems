#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1078-RELEASE."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1078"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1078-RELEASE"
THEOREM = "THM-M-1078"
BASE_REVISION = "e04243daf889845e1649146b8777095223d800ba"
BASE_TREE = "64f87b307e68abee8e4a7a19f511dbf28dbf1e39"
EXPRESSION_SHA256 = "675f66dd17fc5f438fc69d579af60f3784063f985924f2c2b059945a7f038aa8"
DENOMINATOR_SHA256 = "f7a3b25e4d46cf0e67ad09199b7b4035216a1bc5acc4b2c6f7c21fd07e63c73e"
VALIDATION_RECEIPT_SHA256 = "55b12d50d7a05de237d48c8331dab7dede80eac4e057d167dd599cefd7da7704"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ROOT_CUT = [
    "M1078-C-EXTERNAL-PIN",
    "M1078-T-ALLTIME",
    "M1078-B-PREDICTABLE",
    "M1078-B-NORM",
]
ALL_OBLIGATIONS = [
    "M1078-ROOT",
    "M1078-S-TARGET",
    "M1078-S-BOUNDARY",
    "M1078-S-FOUNDATION",
    "M1078-C-EXTERNAL-PIN",
    "M1078-B-INDEX",
    "M1078-B-PREDICTABLE",
    "M1078-B-BOUND",
    "M1078-B-FINITE",
    "M1078-B-NORM",
    "M1078-T-ALLTIME",
    "M1078-T-LOCAL-BODY",
    "M1078-T-ASSEMBLE",
    "M1078-X-SOURCE",
    "M1078-X-PROVENANCE",
]
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-1078/check_release.py",
    "Stage1_Instances/THM-M-1078/release-decision.json",
    "Stage1_Instances/THM-M-1078/release-phase.md",
    "Stage1_Instances/THM-M-1078/release-receipt.json",
    "Stage1_Instances/THM-M-1078/release-spec.json",
]
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json":
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json":
        "b921e6adb61d4d34f1cbb3b4fc90226b0d4a0c3247ff3ef2df2ae0f901111084",
    "Docs/Stage1_Blueprint_rev-5.6.md":
        "0c3a91e3bc3a95dafa4fbe4b8fdf8ac6c38254dc3f896b84ae291a0925bbe119",
    "skills/execute-stage1-rev56/SKILL.md":
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain":
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json":
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}

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


def run(
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 360,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )


def git(*argv: str, cwd: Path = ROOT) -> str:
    result = run(["git", *argv], cwd=cwd)
    assert result.returncode == 0, result.stdout
    return result.stdout.strip()


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
spec = load(HERE / "release-spec.json")
receipt = load(HERE / "release-receipt.json")
instance = load(HERE / "instance.json")
task_dag = load(HERE / "task-dag.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
proof = load(HERE / "proof-receipt.json")
validation = load(HERE / "validation-receipt.json")
targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

assert git("rev-parse", "HEAD") == BASE_REVISION
assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
for relative, expected in AUTHORITY_INPUTS.items():
    assert digest(ROOT / relative) == expected, f"authority input drifted: {relative}"

target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
assert target == {
    "execution_rank": 520,
    "legacy_priority_slot": None,
    "theorem_id": THEOREM,
    "name": "\u9785\u53d8\u6362",
    "category": "\u6982\u7387\u8bba\u4e0e\u968f\u673a\u8fc7\u7a0b / \u968f\u673a\u8fc7\u7a0b",
    "source_status_untrusted": "\u5df2\u9a8c\u8bc1",
    "baseline": "L0",
    "rework_required": True,
    "legacy_artifacts_accepted": False,
    "target_lane": "hard_mathlib_anchor_and_wrapper",
    "intake_score": 138,
    "lifecycle_mode": "planned",
    "theorem_complete": False,
}
release_item = next(row for row in execution["items"] if row["id"] == ITEM)
validation_item = next(
    row for row in execution["items"] if row["id"] == "S56-M-1078-VALIDATION"
)
assert release_item == {
    "id": ITEM,
    "theorem_id": THEOREM,
    "execution_rank": 520,
    "phase": "release",
    "layer": 6,
    "state": "[ ]",
    "depends_on": ["S56-M-1078-VALIDATION"],
    "owned_paths": ["Stage1_Instances/THM-M-1078"],
    "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
assert validation_item["depends_on"] == ["S56-M-1078-PROOF"]

assert instance["lifecycle"] == "planned"
assert instance["canonical_claim_status"] == "human_scope_frozen_formal_statement_open"
assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
assert instance["accepted_proof_state"] == []
assert instance["audit_complete"] is instance["theorem_complete"] is False
assert task_dag["lifecycle"] == "planned" and task_dag["accepted_states"] == []
assert next(row for row in task_dag["tasks"] if row["id"] == ITEM)["state"] == "open"

assert [row["obligation_id"] for row in registry["obligations"]] == ALL_OBLIGATIONS
assert registry["closure_observed_after_freeze"] is False
assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
assert [row["obligation_id"] for row in graphs["nodes"]] == ALL_OBLIGATIONS
root = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1078-ROOT")
assert (root["human_debt"], root["machine_debt"], root["readability_debt"]) == (
    "H2", "M2", "R4",
)
assert root["formal_target"] == "Stage1Instances.THM_M_1078.MartingaleTransformTarget"
closure = graphs["closure_boundary"]
assert closure == {
    "closed_obligations": [],
    "root_closed": False,
    "audit_complete": False,
    "theorem_complete": False,
    "remaining_root_cut_set": ROOT_CUT,
    "root_machine_debt": "M2",
}
assert graphs["composition_certificates"] == [{
    "certificate_id": "COMP-M1078-ROOT-CONDITIONAL",
    "declaration":
        "Stage1Instances.THM_M_1078.ObligationTree.root_of_allTimeMemLpTransformBound",
    "exact_target_transport":
        "Stage1Instances.THM_M_1078.ObligationTree.local_target_iff_frozen_target",
    "covered_edges": ["PROOF-01", "PROOF-05", "PROOF-06"],
    "status": "checked_conditional_composition_only",
}]

assert proof["support_state"] == "provisional_worker_selftest"
assert proof["closed_obligation_ids"] == ["M1078-T-ALLTIME"]
assert proof["result"]["root_closed"] is proof["result"]["theorem_complete"] is False
assert "forall k, k <= n" in source_without_comments((HERE / "Proof.lean").read_text())
tree_source = source_without_comments((HERE / "ObligationTree.lean").read_text())
assert "forall k, MemLp (f k) p mu" in tree_source
assert "forall k, k <= n" not in tree_source

assert digest(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
assert validation["item_id"] == "S56-M-1078-VALIDATION"
assert validation["support_state"] == "provisional_worker_selftest"
assert validation["proposed_state"] == "[_]"
assert validation["accepted"] is False and validation["release_grade"] is False
assert validation["verdict"] == "blocked"
assert validation["result"]["root_closed"] is False
assert validation["result"]["root_kernel_closed"] is False
assert validation["result"]["accepted_closed_obligation_ids"] == []
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert validation["remaining_root_cut_set"] == ROOT_CUT

assert decision["schema_version"] == "stage1-release-decision/1.0"
assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
assert decision["phase"] == decision["intent"] == "release"
assert decision["depends_on"] == ["S56-M-1078-VALIDATION"]
assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
assert decision["support_state"] == "provisional_worker_selftest"
assert decision["proposed_state"] == "[_]" and decision["accepted"] is False
assert decision["verdict"] == "blocked" and decision["release_grade"] is False
assert decision["content_addressed_release_evidence"] is False
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["canonical_target"] == {
    "declaration": "Stage1Instances.THM_M_1078.MartingaleTransformTarget",
    "elaborated_expression_sha256": EXPRESSION_SHA256,
    "registry_denominator_sha256": DENOMINATOR_SHA256,
    "exact_statement_delta": "none",
}
for name, expected in decision["reconciled_inputs"].items():
    assert digest(HERE / name) == expected, f"reconciled input drifted: {name}"
assert decision["authority_inputs"] == AUTHORITY_INPUTS
assert decision["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
assert decision["dependency"]["receipt_id"] == validation["receipt_id"]
assert decision["dependency"]["master_accepted"] is False
assert decision["dependency"]["freshness_at_release_head"].startswith(
    "stale_phase_bound_recipe:"
)
assert decision["root_vector"] == {
    "authoritative_intake_before": {"H": "H1", "M": "M4", "R": "R4"},
    "authoritative_intake_after": {"H": "H1", "M": "M4", "R": "R4"},
    "latest_provisional_graph_before": {"H": "H2", "M": "M2", "R": "R4"},
    "latest_provisional_graph_after": {"H": "H2", "M": "M2", "R": "R4"},
    "reconciliation": (
        "fail_closed_without_promotion: the intake projection and later provisional graph "
        "disagree and no master-accepted evidence reconciles them"
    ),
}
assert decision["terminal_decisions"] == {
    "audit_complete": False,
    "theorem_complete": False,
    "audit_z": "blocked",
    "theorem_z": "blocked",
    "release_accepted": False,
    "master_acceptance": False,
}
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_theorem_gate"]["gate_id"] == (
    "proof.exact_root_kernel_closure.M1078-ROOT"
)
assert decision["first_failed_release_gate"]["gate_id"] == (
    "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
)
assert decision["remaining_root_cut_set"] == ROOT_CUT
assert decision["changed_paths"] == CHANGED_PATHS

reconciliation = decision["evidence_reconciliation"]
assert reconciliation["accepted_closed_obligation_ids"] == []
assert reconciliation["conditional_composition_only"] is True
for key in (
    "validation_dependency_master_accepted",
    "exact_root_kernel_closed",
    "structured_projection_reconciled",
    "pinpoint_h0_and_independent_source_review",
    "independent_r0_review",
    "audit_z_accepted",
    "accepted_foundation_profile",
    "complete_transitive_provenance_and_tcb",
    "immutable_clean_release_input",
    "hermetic_empty_cache_cold_offline_replay",
    "complete_sbom_license_archive_closure",
    "two_independent_signed_runner_attestations",
    "independently_implemented_minimal_verifier",
    "protected_ci_and_adversarial_gates",
    "deterministic_content_addressed_release_bundle",
    "master_acceptance",
):
    assert reconciliation[key] is False, key

assert spec["schema_version"] == "stage1-validation-spec/1.0"
assert spec["item_id"] == receipt["item_id"] == ITEM
assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
assert spec["argv"] == [
    "python3", "-B", "Stage1_Instances/THM-M-1078/check_release.py",
    "--worker-packet", ".stage1-worker-selftest.json",
]
assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
assert spec["timeout_seconds"] == 900
assert spec["covered_obligation_ids"] == ALL_OBLIGATIONS
assert len(spec["covered_declarations"]) == len(set(spec["covered_declarations"])) == 6

assert receipt["schema_version"] == "stage1-node-receipt/1.0"
assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
assert receipt["phase"] == receipt["intent"] == "release"
assert receipt["depends_on"] == ["S56-M-1078-VALIDATION"]
assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
assert receipt["release_grade"] is False and receipt["master_accepted"] is False
assert receipt["verdict"] == "blocked"
assert receipt["decision_id"] == decision["decision_id"]
assert receipt["decision_sha256"] == digest(HERE / "release-decision.json")
assert receipt["release_spec_sha256"] == digest(HERE / "release-spec.json")
assert receipt["checker_sha256"] == digest(HERE / "check_release.py")
assert receipt["public_projection_sha256"] == digest(HERE / "release-phase.md")
assert receipt["dependency"] == decision["dependency"]
assert receipt["known_failures"] == decision["known_failures"]
assert receipt["changed_paths"] == CHANGED_PATHS
assert receipt["result"] == {
    "verdict": "blocked",
    "lifecycle_before": "planned",
    "lifecycle_after": "planned",
    "authoritative_intake_root_vector": ["H1", "M4", "R4"],
    "latest_provisional_graph_root_vector": ["H2", "M2", "R4"],
    "accepted_closed_obligation_ids": [],
    "remaining_root_cut_set": ROOT_CUT,
    "audit_complete": False,
    "theorem_complete": False,
}
for key in (
    "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
    "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
    "covered_obligation_ids", "covered_declarations", "scope_boundary",
):
    assert receipt["recipe"][key] == spec[key], f"receipt/spec mismatch: {key}"

environment = receipt["environment"]
assert environment["python_executable_sha256"] == digest(Path("/usr/bin/python3"))
assert environment["git_executable_sha256"] == digest(Path("/usr/bin/git"))
assert environment["bubblewrap_executable_sha256"] == digest(Path("/usr/bin/bwrap"))
lean_which = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT)
assert lean_which.returncode == 0, lean_which.stdout
lean_path = Path(lean_which.stdout.strip())
lake_path = lean_path.with_name("lake")
assert environment["lean_executable_sha256"] == digest(lean_path)
assert environment["lake_executable_sha256"] == digest(lake_path)

if args.worker_packet is not None:
    packet = load(args.worker_packet.resolve())
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary", "base_revision",
        "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    summary = packet["output_summary"]
    assert summary["verdict"] == "blocked"
    assert summary["lifecycle_before"] == summary["lifecycle_after"] == "planned"
    assert summary["authoritative_intake_root_vector_before"] == ["H1", "M4", "R4"]
    assert summary["authoritative_intake_root_vector_after"] == ["H1", "M4", "R4"]
    assert summary["latest_provisional_graph_root_vector_before"] == ["H2", "M2", "R4"]
    assert summary["latest_provisional_graph_root_vector_after"] == ["H2", "M2", "R4"]
    assert summary["audit_complete"] is summary["theorem_complete"] is False
    assert summary["accepted_receipt_ids"] == []
    assert summary["remaining_root_cut_set"] == ROOT_CUT
    expected_commands = [
        ["python3", "Docs/tools/check_stage1_standard.py"],
        ["python3", "scripts/stage1_target.py", "check"],
        ["python3", "scripts/stage1_target.py", "show", THEOREM],
        ["git", "status", "--short", "--untracked-files=all"],
        ["execute", "Stage1_Instances/THM-M-1078/validation-spec.json", "argv"],
        ["python3", "-B", "Stage1_Instances/THM-M-1078/check_obligation_tree.py"],
        ["python3", "-B", "Stage1_Instances/THM-M-1078/check_proof.py"],
        ["cd", "Formalizations/Lean", "&&", "lake", "env", "lean", "--trust=0",
         "-j1", "-t0", "../../Stage1_Instances/THM-M-1078/Proof.lean"],
        ["bash", "Stage1_Instances/THM-M-1078/check_exact_composition.sh"],
        ["python3", "-B", "Stage1_Instances/THM-M-1078/check_release.py",
         "--worker-packet", ".stage1-worker-selftest.json"],
        ["python3", "-m", "json.tool", "Stage1_Instances/THM-M-1078/release-spec.json"],
        ["python3", "-m", "json.tool", "Stage1_Instances/THM-M-1078/release-decision.json"],
        ["python3", "-m", "json.tool", "Stage1_Instances/THM-M-1078/release-receipt.json"],
        ["python3", "-m", "json.tool", ".stage1-worker-selftest.json"],
        ["python3", "-m", "py_compile", "Stage1_Instances/THM-M-1078/check_release.py"],
        ["git", "diff", "--check", "--", "Stage1_Instances/THM-M-1078",
         ".stage1-worker-selftest.json"],
    ]
    assert [row["argv"] for row in packet["commands"]] == expected_commands
    assert [row["exit_code"] for row in packet["commands"]] == [
        0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
    assert packet["commands"][4]["classification"] == "expected_freshness_failure"
    status = run([
        "git", "status", "--short", "--untracked-files=all", "--",
        "Stage1_Instances/THM-M-1078", ".stage1-worker-selftest.json",
        "Formalizations/Lean/.lake",
    ])
    assert status.returncode == 0, status.stdout
    actual = {line[3:] for line in status.stdout.splitlines()}
    actual.discard("Formalizations/Lean/.lake")
    assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|oracle)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe|extern)\b",
    re.MULTILINE,
)
for path in sorted(HERE.glob("*.lean")):
    assert prohibited.search(source_without_comments(path.read_text(encoding="utf-8"))) is None, path

assert MATHLIB.resolve().is_dir()
assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""

tree_check = run(["python3", "-B", str(HERE / "check_obligation_tree.py")])
assert tree_check.returncode == 0, tree_check.stdout
assert "root closure: open (M2); conditional composition only" in tree_check.stdout
proof_check = run(["python3", "-B", str(HERE / "check_proof.py")])
assert proof_check.returncode == 0, proof_check.stdout
assert "frozen conditional interface mismatch remains" in proof_check.stdout
lean_replay = run([
    "lake", "env", "lean", "--trust=0", "-j1", "-t0",
    "../../Stage1_Instances/THM-M-1078/Proof.lean",
], cwd=LEAN_ROOT)
assert lean_replay.returncode == 0, lean_replay.stdout
for declaration in (
    "Stage1Instances.THM_M_1078.Proof.memLp_condExp_of_one_lt",
    "Stage1Instances.THM_M_1078.Proof.earlierMemLpUpTo",
):
    report = (
        f"'{declaration}' depends on axioms: "
        "[propext, Classical.choice, Quot.sound]"
    )
    assert report in lean_replay.stdout
composition = run(["bash", str(HERE / "check_exact_composition.sh")])
assert composition.returncode == 0, composition.stdout
assert "local_target_iff_frozen_target" in composition.stdout

public = (HERE / "release-phase.md").read_text(encoding="utf-8")
for fragment in (
    "**blocked**", "[H1, M4, R4]", "[H2, M2, R4]", "`AUDIT-Z`",
    "`THEOREM-Z`", "accepted=false", "M1078-C-EXTERNAL-PIN",
):
    assert fragment in public, fragment
assert "/home/" not in public and ".cron/" not in public

for relative in CHANGED_PATHS:
    path = ROOT / relative
    if not path.exists() and relative == ".stage1-worker-selftest.json" and args.worker_packet is None:
        continue
    data = path.read_bytes()
    assert data.endswith(b"\n"), f"missing final newline: {relative}"
    assert b"\r" not in data and b"\x00" not in data, f"invalid byte: {relative}"
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), relative

print("PASS release inputs: target, DAG, receipts, registry, graph, and hashes agree")
print("PASS current Lean replay: two horizon-local declarations; conditional composition only")
print("PASS fail-closed state: planned; authority H1/M4/R4; provisional graph H2/M2/R4")
print("BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and stale")
print("BLOCKED proof.exact_root_kernel_closure.M1078-ROOT: four-node cut remains")
print("BLOCKED cold/offline, provenance, source/readability, independent verifier, and bundle gates")
print("verdict=blocked audit_complete=false theorem_complete=false")
