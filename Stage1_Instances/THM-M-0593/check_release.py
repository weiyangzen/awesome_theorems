#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0593-RELEASE."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0593"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0593-RELEASE"
THEOREM = "THM-M-0593"
BASE_REVISION = "e46e0735d0940bb558acaf027d8386de2579f55d"
BASE_TREE = "9f03ecc77e82eda1f0ea3f0f4b08d1d7419ce0cf"
STATEMENT_SHA256 = "dd2a4da4f6cb0b0723a656e627378047834867641d63c6e5a8a0255108aed3bb"
DENOMINATOR_SHA256 = "ff56394a72695c35f72ed72fc1c961a3297943517a2e8b8056047678fb1157e2"
VALIDATION_RECEIPT_SHA256 = "1ad740e23e22e077c8ac49dd40d70eeedb823815f1ecb732db68512014da1095"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
AUTHORITATIVE_CUT = [
    "M0593-L-DIMENSION-IMAGE",
    "M0593-L-RANK-REDUCTION",
    "M0593-L-TAYLOR",
]
PROVISIONAL_CUT = ["M0593-L-RANK-REDUCTION", "M0593-L-TAYLOR"]
PROVISIONALLY_VALIDATED = [
    "M0593-B-ZERO",
    "M0593-L-DIMENSION-IMAGE",
    "M0593-B-LOWDIM",
    "M0593-B-MERGE",
]
ALL_OBLIGATIONS = [
    "M0593-ROOT",
    "M0593-S-DEFINITIONS",
    "M0593-S-DOMAINS",
    "M0593-S-BOUNDARY",
    "M0593-S-FOUNDATION",
    "M0593-N-LOCAL",
    "M0593-B-ZERO",
    "M0593-B-LOWDIM",
    "M0593-B-HARD",
    "M0593-B-MERGE",
    "M0593-L-DIMENSION-IMAGE",
    "M0593-C-RANK-STRATA",
    "M0593-L-RANK-REDUCTION",
    "M0593-L-HIGHER-STRATA",
    "M0593-L-TAYLOR",
    "M0593-L-CUBE-COVER",
    "M0593-L-NULL-LIMIT",
    "M0593-T-HARD-LOCAL",
    "M0593-T-LOCAL-GLOBAL",
    "M0593-X-EQUAL-DIM",
    "M0593-X-SOURCE",
    "M0593-X-PROVENANCE",
]
PROOF_DECLARATIONS = {
    "Stage1Instances.THMM0593.zeroCodomainBranch_proof",
    "Stage1Instances.THMM0593.lowDimensionBranch_proof",
    "Stage1Instances.THMM0593.sardTarget_of_hardDimensionBranch",
}
VALIDATION_DECLARATIONS = {
    "Stage1Instances.THMM0593.Validation.exactRoot_iff_frozen",
    "Stage1Instances.THMM0593.Validation.zeroCodomainBranch_validation",
    "Stage1Instances.THMM0593.Validation.conditionalExactRoot",
}
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
]
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json":
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json":
        "8dab05d8ff970c4470ea7697750232eb4da84c740783e4c95ed4a1c9f1848594",
    "Docs/Stage1_Blueprint_rev-5.6.md":
        "fa230704792c24bf86d3e87ca9f58cf74e20f91fd4d13066d953701658078f77",
    "skills/execute-stage1-rev56/SKILL.md":
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": TOOLCHAIN_SHA256,
    "Formalizations/Lean/lake-manifest.json": MANIFEST_SHA256,
}

if not __debug__:
    raise RuntimeError("release reconciliation requires Python assertions")

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
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )


def git(*argv: str, cwd: Path = ROOT) -> str:
    result = run(["git", *argv], cwd=cwd, timeout=60)
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


def axiom_report(output: str, declaration: str) -> set[str]:
    no_axioms = f"'{declaration}' does not depend on any axioms"
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    assert output.count(no_axioms) + len(matches) == 1, declaration
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


decision = load(HERE / "release-decision.json")
spec = load(HERE / "release-spec.json")
receipt = load(HERE / "release-receipt.json")
instance = load(HERE / "instance.json")
task_dag = load(HERE / "task-dag.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
proof = load(HERE / "proof-receipt.json")
blocker = load(HERE / "proof-blocker.json")
validation = load(HERE / "validation-receipt.json")
targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

assert git("rev-parse", "HEAD") == BASE_REVISION
assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
for relative, expected in AUTHORITY_INPUTS.items():
    assert digest(ROOT / relative) == expected, f"authority input drifted: {relative}"
assert decision["authority_inputs"] == AUTHORITY_INPUTS

target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
assert target == {
    "execution_rank": 633,
    "legacy_priority_slot": None,
    "theorem_id": THEOREM,
    "name": "\u8428\u5fb7\u5b9a\u7406",
    "category": "\u62d3\u6251\u5b66 / \u5fae\u5206\u62d3\u6251",
    "source_status_untrusted": "\u5df2\u9a8c\u8bc1",
    "baseline": "L0",
    "rework_required": True,
    "legacy_artifacts_accepted": False,
    "target_lane": "hard_statement_first_partial_verification",
    "intake_score": 132,
    "lifecycle_mode": "planned",
    "theorem_complete": False,
}
items = {row["id"]: row for row in execution["items"]}
assert items[ITEM] == {
    "id": ITEM,
    "theorem_id": THEOREM,
    "execution_rank": 633,
    "phase": "release",
    "layer": 6,
    "state": "[ ]",
    "depends_on": ["S56-M-0593-VALIDATION"],
    "owned_paths": [f"Stage1_Instances/{THEOREM}"],
    "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
    "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
    "attempts": 0,
    "children": [],
}
assert items["S56-M-0593-VALIDATION"]["state"] == "[_]"
assert items["S56-M-0593-VALIDATION"]["attempts"] == 1

assert instance["lifecycle"] == "planned"
assert instance["intent"] == "intake"
assert instance["canonical_claim_status"].endswith("formal_statement_open")
assert "manifold" in instance["canonical_claim"]
assert instance["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"}
assert instance["accepted_proof_state"] == []
assert instance["audit_complete"] is instance["theorem_complete"] is False
assert task_dag["lifecycle"] == "planned" and task_dag["accepted_states"] == []
assert all(row["state"] == "open" for row in task_dag["tasks"])

assert registry["root_obligation_id"] == "M0593-ROOT"
assert registry["denominator_sha256"] == DENOMINATOR_SHA256
assert [row["obligation_id"] for row in registry["obligations"]] == ALL_OBLIGATIONS
assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
assert [row["obligation_id"] for row in graphs["nodes"]] == ALL_OBLIGATIONS
root = next(row for row in graphs["nodes"] if row["obligation_id"] == "M0593-ROOT")
assert (root["human_debt"], root["machine_debt"], root["readability_debt"]) == (
    "H1", "M4", "R4",
)
closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["root_machine_debt"] == "M4"
assert closure["audit_complete"] is closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == AUTHORITATIVE_CUT
assert graphs["graphs"]["evidence"]["edges"] == [{
    "edge_id": "EVID-ANCHOR",
    "from": "M0593-X-PROVENANCE",
    "type": "evidence_for",
    "to": "M0593-X-EQUAL-DIM",
}]

assert proof["support_state"] == "provisional_worker_selftest"
assert proof["closed_obligation_ids"] == PROVISIONALLY_VALIDATED
assert proof["result"]["root_closed"] is proof["result"]["theorem_complete"] is False
assert proof["result"]["root_vector_after_proposed"] == {
    "H": "H1", "M": "M2", "R": "R4",
}
assert proof["remaining_root_cut_set_after"] == PROVISIONAL_CUT
assert blocker["root_closed"] is blocker["theorem_complete"] is False
assert blocker["remaining_root_cut_set"] == PROVISIONAL_CUT

assert digest(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
assert validation["item_id"] == "S56-M-0593-VALIDATION"
assert validation["support_state"] == "provisional_worker_selftest"
assert validation["proposed_state"] == "[_]"
assert validation["accepted"] is False and validation["release_grade"] is False
assert validation["verdict"] == "blocked"
assert validation["result"]["accepted_root_closed"] is False
assert validation["result"]["provisional_root_closed"] is False
assert validation["result"]["accepted_closed_obligation_ids"] == []
assert validation["result"]["provisionally_validated_obligation_ids"] == (
    PROVISIONALLY_VALIDATED
)
assert validation["result"]["frozen_remaining_root_cut_set"] == AUTHORITATIVE_CUT
assert validation["result"]["provisional_remaining_root_cut_set"] == PROVISIONAL_CUT
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert validation["result"]["hermetic_release_gate"] == "fail_closed"
assert validation["result"]["independent_distinct_runner_gate"] == "fail_closed"
assert validation["composition"]["unproved_input"] == "HardDimensionBranch"

assert decision["schema_version"] == "stage1-release-decision/1.0"
assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
assert decision["phase"] == decision["intent"] == "release"
assert decision["depends_on"] == ["S56-M-0593-VALIDATION"]
assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
assert decision["decision_support"] == "provisional_worker_selftest"
assert decision["proposed_state"] == "[_]" and decision["accepted"] is False
assert decision["release_grade"] is decision["content_addressed_release_evidence"] is False
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []
assert decision["canonical_target"] == {
    "declaration": "Stage1Instances.THMM0593.SardTarget",
    "source_sha256": STATEMENT_SHA256,
    "registry_denominator_sha256": DENOMINATOR_SHA256,
    "exact_statement_delta": "none",
}
for name, expected in decision["reconciled_inputs"].items():
    assert digest(HERE / name) == expected, f"reconciled input drifted: {name}"
dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"]
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
assert dependency["receipt_support_state"] == validation["support_state"]
assert dependency["receipt_accepted"] is validation["accepted"] is False
assert dependency["receipt_release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False
assert dependency["freshness_at_release_head"].startswith("stale_phase_bound_recipe:")
assert decision["root_vector"] == {
    "authoritative_before": {"H": "H1", "M": "M4", "R": "R4"},
    "authoritative_after": {"H": "H1", "M": "M4", "R": "R4"},
    "best_provisional_before": {"H": "H1", "M": "M2", "R": "R4"},
    "best_provisional_after": {"H": "H1", "M": "M2", "R": "R4"},
    "reconciliation": (
        "No promotion: instance and frozen graph remain authoritative at H1/M4/R4; "
        "later branch proofs are provisional H1/M2/R4 and leave the exact root open."
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
    "proof.exact_root_kernel_closure.M0593-B-HARD"
)
assert decision["first_failed_release_gate"]["gate_id"] == (
    "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
)
assert decision["authoritative_remaining_root_cut_set"] == AUTHORITATIVE_CUT
assert decision["provisional_remaining_root_cut_set"] == PROVISIONAL_CUT
assert decision["changed_paths"] == CHANGED_PATHS
reconciliation = decision["evidence_reconciliation"]
assert reconciliation["conditional_composition_only"] is True
assert reconciliation["accepted_closed_obligation_ids"] == []
assert reconciliation["provisionally_validated_obligation_ids"] == PROVISIONALLY_VALIDATED
for key in (
    "validation_dependency_master_accepted",
    "exact_root_kernel_closed",
    "structured_scope_reconciled",
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
    "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py",
    "--worker-packet", ".stage1-worker-selftest.json",
]
assert spec["expected_exit"] == 0 and spec["timeout_seconds"] == 900
assert spec["decision_covered_obligation_ids"] == ALL_OBLIGATIONS
assert len(spec["covered_declarations"]) == len(set(spec["covered_declarations"])) == 8

assert receipt["schema_version"] == "stage1-node-receipt/1.0"
assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
assert receipt["phase"] == receipt["intent"] == "release"
assert receipt["depends_on"] == ["S56-M-0593-VALIDATION"]
assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
assert receipt["master_accepted"] is False and receipt["verdict"] == "blocked"
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
    "authoritative_root_vector": ["H1", "M4", "R4"],
    "best_provisional_root_vector": ["H1", "M2", "R4"],
    "accepted_closed_obligation_ids": [],
    "authoritative_remaining_root_cut_set": AUTHORITATIVE_CUT,
    "provisional_remaining_root_cut_set": PROVISIONAL_CUT,
    "audit_complete": False,
    "theorem_complete": False,
}
for key in (
    "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
    "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
    "decision_covered_obligation_ids", "covered_declarations", "scope_boundary",
):
    assert receipt["recipe"][key] == spec[key], f"receipt/spec mismatch: {key}"

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
    assert summary == {
        "verdict": "blocked",
        "lifecycle_before": "planned",
        "lifecycle_after": "planned",
        "authoritative_root_vector_before": ["H1", "M4", "R4"],
        "authoritative_root_vector_after": ["H1", "M4", "R4"],
        "best_provisional_root_vector": ["H1", "M2", "R4"],
        "audit_complete": False,
        "theorem_complete": False,
        "accepted_receipt_ids": [],
        "authoritative_remaining_root_cut_set": AUTHORITATIVE_CUT,
        "provisional_remaining_root_cut_set": PROVISIONAL_CUT,
    }
    assert packet["commands"] == receipt["commands_and_results"]
    status = run([
        "git", "status", "--short", "--untracked-files=all", "--",
        f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
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
    source = source_without_comments(path.read_text(encoding="utf-8"))
    assert prohibited.search(source) is None, path
proof_source = source_without_comments((HERE / "Proof.lean").read_text(encoding="utf-8"))
assert re.search(
    r"theorem sardTarget_of_hardDimensionBranch\s+\(hard : HardDimensionBranch\)\s*:\s*SardTarget",
    proof_source,
)
assert "theorem sardTarget_proof" not in proof_source

assert digest(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
assert digest(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir()
assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""

tree_check = run(["python3", "-I", "-B", str(HERE / "check_obligation_tree.py")])
assert tree_check.returncode == 0, tree_check.stdout
assert "PASS THM-M-0593 obligation tree: 22 obligations, 43 typed edges" in tree_check.stdout

lean_which = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT)
assert lean_which.returncode == 0, lean_which.stdout
lean = Path(lean_which.stdout.strip())
lean_path_result = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT)
assert lean_path_result.returncode == 0, lean_path_result.stdout
base_lean_path = lean_path_result.stdout.strip()
assert base_lean_path
tmp = Path(tempfile.mkdtemp(prefix="stage1-m0593-release-", dir="/tmp"))
try:
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        shutil.copy2(HERE / name, tmp / name)
    fixed_env = {
        "HOME": str(tmp),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
        "LEAN_PATH": base_lean_path,
    }
    statement_output = run(
        [str(lean), "--trust=0", "-t0", "-o", "Statement.olean", "Statement.lean"],
        cwd=tmp, env=fixed_env,
    )
    assert statement_output.returncode == 0, statement_output.stdout
    fixed_env["LEAN_PATH"] = f"{tmp}:{base_lean_path}"
    obligation_output = run(
        [str(lean), "--trust=0", "-t0", "-o", "ObligationTree.olean", "ObligationTree.lean"],
        cwd=tmp, env=fixed_env,
    )
    proof_output = run(
        [str(lean), "--trust=0", "-t0", "Proof.lean"], cwd=tmp, env=fixed_env,
    )
    validation_output = run(
        [str(lean), "--trust=0", "-t0", "Validation.lean"], cwd=tmp, env=fixed_env,
    )
    for result in (obligation_output, proof_output, validation_output):
        assert result.returncode == 0, result.stdout
finally:
    shutil.rmtree(tmp)

assert axiom_report(
    obligation_output.stdout, "Stage1Instances.THMM0593.root_of_sard_branches"
) == EXPECTED_AXIOMS
for declaration in PROOF_DECLARATIONS:
    assert axiom_report(proof_output.stdout, declaration) == EXPECTED_AXIOMS
for declaration in VALIDATION_DECLARATIONS:
    assert axiom_report(validation_output.stdout, declaration) <= EXPECTED_AXIOMS
assert proof_output.stdout.count("Declarations are sorry-free!") == 3
# Validation.lean's third `#print sorries` is intentionally a bare expression
# continued from the command above, so Lean prints two explicit hygiene lines.
assert validation_output.stdout.count("Declarations are sorry-free!") == 2
all_output = (
    statement_output.stdout + obligation_output.stdout + proof_output.stdout
    + validation_output.stdout
)
assert "sorryAx" not in all_output and "error:" not in all_output

public = (HERE / "release-phase.md").read_text(encoding="utf-8")
for fragment in (
    "**blocked**", "[H1, M4, R4]", "[H1, M2, R4]", "`AUDIT-Z`",
    "`THEOREM-Z`", "accepted=false", "HardDimensionBranch",
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
print("PASS current Lean replay: exact statement, two proved branches, conditional composition")
print("PASS fail-closed state: planned H1/M4/R4; provisional H1/M2/R4 only")
print("BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and stale")
print("BLOCKED proof.exact_root_kernel_closure.M0593-B-HARD: hard branch remains")
print("BLOCKED cold/offline, provenance, source/readability, independent verifier, and bundle gates")
print("verdict=blocked audit_complete=false theorem_complete=false")
