#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0063-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0063"
ITEM = "S56-M-0063-RELEASE"
THEOREM = "THM-M-0063"
BASE_REVISION = "03bed3c211cb739ccd2629908210fda0f9adf6ca"
BASE_TREE = "a48670276bfe2105ddbfb4057314b21056dae0cb"
EXPRESSION_SHA256 = "40929846f1d1d1ff4479e5be6a989358a65ecebec5a2646f6e2dab508c641a1a"
DENOMINATOR_SHA256 = "384a00c490054109773a2b786763af466971bd50c093a6facd39b614133b74a1"
VALIDATION_RECEIPT_SHA256 = "31230ba405e346b866a7300569b5a8d7bc4137d511ab3609a8c3454e2f0983ee"
PROOF_RECEIPT_SHA256 = "200db9b33a8e75ebf48731ae0f0b06d39815f4be294270fe434bfd1257eceb9f"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
GRAPH_PROOF_CUT = [
    "M0063-C-PERM-HOM",
    "M0063-L-POINTWISE",
    "M0063-L-REGULAR-FAITHFUL",
    "M0063-C-LEFT-INVERSE",
    "M0063-C-MRANGE-EQUIV",
    "M0063-N-MRANGE-RANGE",
]
GRAPH_NONPROOF_CUT = [
    "M0063-S-FOUNDATION",
    "M0063-X-SOURCE",
    "M0063-X-PROVENANCE",
    "M0063-X-TRUST",
    "M0063-X-DOCUMENTATION",
    "M0063-X-WORKFLOW",
]


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )


def git(*args: str, cwd: Path = ROOT) -> str:
    completed = run(["git", *args], cwd=cwd)
    assert completed.returncode == 0, completed.stdout
    return completed.stdout.strip()


decision = load(HERE / "release-decision.json")
instance = load(HERE / "instance.json")
tasks = load(HERE / "task-dag.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
proof = load(HERE / "proof-receipt.json")
validation = load(HERE / "validation-receipt.json")
validation_spec = load(HERE / "validation-spec.json")
receipt = load(HERE / "release-receipt.json")
targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
release_node = next(row for row in execution["items"] if row["id"] == ITEM)
validation_node = next(row for row in execution["items"] if row["id"] == "S56-M-0063-VALIDATION")
local_release = next(row for row in tasks["tasks"] if row["id"] == ITEM)

assert target["execution_rank"] == 1094
assert target["baseline"] == "L0" and target["rework_required"] is True
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert release_node["state"] == "[ ]" and release_node["depends_on"] == ["S56-M-0063-VALIDATION"]
assert validation_node["state"] == "[_]"
assert local_release["state"] == "open"
assert git("rev-parse", "HEAD") == BASE_REVISION
assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

assert instance["lifecycle"] == "planned"
assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
assert instance["audit_complete"] is instance["theorem_complete"] is False
assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
assert tasks["lifecycle"] == "planned" and tasks["accepted_states"] == []
assert tasks["audit_complete"] is tasks["theorem_complete"] is False

assert registry["root_obligation_id"] == "M0063-ROOT"
assert registry["denominator_sha256"] == DENOMINATOR_SHA256
assert load(HERE / "statement.json")["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["root_machine_classification"] == "M3"
assert graphs["closure_boundary"]["accepted_closed_obligations"] == []
assert graphs["closure_boundary"]["remaining_root_cut_set"] == GRAPH_PROOF_CUT
assert graphs["closure_boundary"]["remaining_root_critical_nonproof_gates"] == GRAPH_NONPROOF_CUT
assert graphs["closure_boundary"]["audit_complete"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False

assert digest(HERE / "proof-receipt.json") == PROOF_RECEIPT_SHA256
assert digest(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
assert proof["support_state"] == validation["support_state"] == "provisional_worker_selftest"
assert proof["accepted"] is False and validation["accepted"] is False
assert proof["result"]["root_kernel_closed"] is True
assert proof["result"]["accepted_root_closed"] is False
assert validation["release_grade"] is validation["content_addressed_release_evidence"] is False
assert validation["result"]["kernel_replay"] == "provisional_pass"
assert validation["result"]["accepted_root_closed"] is False
assert validation["result"]["foundation_and_complete_trust_closure"] == "fail_closed"
assert validation["result"]["hermetic_cold_offline_replay"] == "fail_closed"
assert validation["result"]["independent_distinct_runner"] == "fail_closed"
assert validation["result"]["placeholder_and_unsafe_scan"] == "pass"
assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False

assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
assert decision["verdict"] == "blocked" and decision["release_grade"] is False
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["root_vector_before"] == decision["root_vector_after"] == instance["root_vector"]
assert decision["audit_complete"] is decision["theorem_complete"] is False
assert decision["accepted_receipt_ids"] == []
assert decision["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
assert decision["dependency"]["master_accepted"] is False
assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
assert decision["authoritative_graph_remaining_root_cut_set"] == GRAPH_PROOF_CUT + GRAPH_NONPROOF_CUT
assert decision["evidence_reconciliation"]["canonical_expression_sha256"] == EXPRESSION_SHA256
assert decision["evidence_reconciliation"]["registry_denominator_sha256"] == DENOMINATOR_SHA256

assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
assert receipt["phase"] == receipt["intent"] == "release"
assert receipt["depends_on"] == ["S56-M-0063-VALIDATION"]
assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
assert receipt["started_at"] <= receipt["validated_at"] <= receipt["ended_at"]
for name in ("release-decision.json", "release-spec.json", "check_release.py", "release-phase.md"):
    assert receipt["inputs"][name] == digest(HERE / name), name
assert receipt["inputs"]["validation-receipt.json"] == VALIDATION_RECEIPT_SHA256
assert receipt["inputs"]["proof-receipt.json"] == PROOF_RECEIPT_SHA256
assert receipt["result"]["verdict"] == "blocked"
assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
assert receipt["result"]["accepted_receipt_ids"] == []
assert receipt["result"]["semantic_output_sha256"] == "aa7a44ca807f6fa17e99d9b777542d3c7c1026ba0c2427bdc798f26f24eb6d52"
assert receipt["result"]["stdout_bytes"] == 437 and receipt["result"]["stdout_line_count"] == 5
for name in (
    "instance.json",
    "task-dag.json",
    "statement.json",
    "obligation-registry.json",
    "typed-graphs.json",
    "Statement.lean",
    "ObligationTree.lean",
    "Proof.lean",
    "Validation.lean",
):
    assert receipt["inputs"][name] == digest(HERE / name), name
for name in (
    "Docs/Stage1_Targets_rev-5.6.json",
    "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "skills/execute-stage1-rev56/SKILL.md",
):
    assert receipt["authority_inputs"][name] == digest(ROOT / name), name
for name, expected in decision["reconciled_inputs"].items():
    path = ROOT / name if "/" in name else HERE / name
    assert expected == digest(path), name

mathlib = ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib"
assert git("rev-parse", "HEAD", cwd=mathlib) == receipt["environment"]["mathlib_revision"]
assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == receipt["environment"]["mathlib_tree"]
assert git("status", "--porcelain=v1", cwd=mathlib) == ""

for key in (
    "authoritative_graph_reconciled",
    "accepted_root_m0_e1",
    "audit_z_accepted",
    "pinpoint_h0_review",
    "independent_r0_review",
    "accepted_provenance_foundation_tcb_closure",
    "immutable_clean_release_input",
    "hermetic_cold_offline_replay",
    "sbom_license_offline_archive_closure",
    "two_independent_signed_runner_attestations",
    "independently_implemented_minimal_release_verifier",
    "protected_ci_and_adversarial_gates",
    "deterministic_content_addressed_release_bundle",
    "master_acceptance",
):
    assert decision["evidence_reconciliation"][key] is False, key

cut_text = "\n".join(decision["remaining_theorem_completion_gates"])
for fragment in (
    "master acceptance",
    "graph reconciliation",
    "AUDIT-Z",
    "H0 primary-source",
    "R0 node-specific",
    "transitive provenance",
    "empty-cache network-denied cold build",
    "two signed attestations",
    "minimal release verifier",
    "deterministic content-addressed release bundle",
):
    assert fragment in cut_text, fragment

# The prior validation recipe is historical evidence, not replayable current release evidence.
validation_checker = (HERE / "check_validation.py").read_text(encoding="utf-8")
assert 'BASE_REVISION = "1944ddb6f503b699293e82f18d19efe0f32b4380"' in validation_checker
assert 'load(ROOT / ".stage1-worker-selftest.json")' in validation_checker
packet = load(ROOT / ".stage1-worker-selftest.json")
assert packet["item_id"] == ITEM and packet["state"] == "[_]"
assert packet["base_revision"] == BASE_REVISION
for relative in packet["changed_paths"]:
    whitespace = run(["git", "diff", "--no-index", "--check", "/dev/null", relative])
    assert whitespace.returncode in (0, 1), whitespace.stdout
    assert whitespace.stdout == "", f"whitespace diagnostics for {relative}: {whitespace.stdout}"
assert validation_spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
stale_replay = run(validation_spec["argv"])
assert stale_replay.returncode != 0

# The smallest live Lean evidence still replays independently of the stale validation packet.
proof_replay = run(["bash", f"Stage1_Instances/{THEOREM}/check_proof.sh"])
assert proof_replay.returncode == 0, proof_replay.stdout
assert proof_replay.stdout.count("Declarations are sorry-free!") == 12
axiom_blocks = re.findall(r"depends on axioms: \[(.*?)]", proof_replay.stdout, flags=re.DOTALL)
assert len(axiom_blocks) == 11
assert "'Stage1Instances.THM_M_0063.Proof.pointwiseFaithfulness' does not depend on any axioms" in proof_replay.stdout
for block in axiom_blocks:
    reported = {name.strip() for name in block.split(",") if name.strip()}
    assert reported <= EXPECTED_AXIOMS
assert EXPECTED_AXIOMS in (
    {name.strip() for name in block.split(",") if name.strip()}
    for block in axiom_blocks
)
assert "sorryAx" not in proof_replay.stdout

print("release-decision: ok (blocked; validation dependency provisional and unaccepted)")
print("authority: ok (planned H1/M3/R4; accepted receipts=[]; AUDIT-Z=false; THEOREM-Z=false)")
print("validation recipe: stale and non-replayable at the integrated base, preserved fail-closed")
print("Lean proof replay: provisional pass (12 declarations sorry-free; axioms within policy)")
print("release gates: fail closed (H0/R0, trust, cold/offline, SBOM, independent verifier, bundle)")
