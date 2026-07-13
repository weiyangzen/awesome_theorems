#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0061-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0061"
ITEM = "S56-M-0061-RELEASE"
THEOREM = "THM-M-0061"
BASE_REVISION = "b4e1220a37cc10a96534cfd411e3b29523d7fd81"
BASE_TREE = "a67dd08a83c396119f4762e0ff109cd0df43ee60"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
EXPECTED_LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AUTHORITY = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "4c9b425b87ebb98c488fa5bb237018a16d9dc04757c89d2012f5e93d6e546c2c",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "0f1a74af1e415166719dd8c440a31fa96428b549f761156eaefe185c54c171e6",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
EXPECTED_INPUTS = {
    "instance.json": "1b8c4b6b08faa5ab619880a3fc7826d0fb324d2c7b80de6e686796daa4954e5b",
    "task-dag.json": "1ae0f73de9c404db7dd535bad7c098ada1a47296754c5979c094878688fa2cfb",
    "statement.json": "b27ab2139df6f5a8dd45ad146c70438c93372e0039796466b34be5957c10f25b",
    "obligation-registry.json": "9eb5592fa68b33d6dbb9003607a34c13236f9f78dbb8ea9a0d3df7ff47195451",
    "typed-graphs.json": "ed8113cfc8540530a5f6743ca8a340fe116597f42a362101f7e4ecbf81d162a3",
    "Proof.lean": "d9843be41f6ddb7c6cf335a1e242fb0444d37e478f7f7d5b9cb488e86f50fe94",
    "proof-receipt.json": "0719b7584fef820bf61e2eedbf31635c60dde58182f39f16727ebaed02bd48c0",
    "Validation.lean": "f0715d0a281586aaa3436c22cc66ba104afa5a0554d80c6f5241056550e0699a",
    "validation-receipt.json": "64f823e0055d05afe1ea7fb69fc7fb5be3d3d62c0c1e1f2bd7388b82d8fb9297",
    "validation-spec.json": "113f939e6c399c973cd00135d1e0a514eb3da9efa3bb50827e3fe6bcd61c5065",
    "check_proof.sh": "26bb20b777ea052137c27231e93df212655ce84a2935f64e346ccfd928970c54",
}
PROOF_OBLIGATION_IDS = [
    "M0061-ROOT",
    "M0061-S-INTERFACE",
    "M0061-S-BOUNDARY",
    "M0061-S-FINTYPE-TRANSPORT",
    "M0061-T-FINITE-SCOPE",
    "M0061-A-LAGRANGE",
    "M0061-L-CARD-PRODUCT",
    "M0061-L-NATCARD-PROD",
    "M0061-L-NATCARD-CONGR",
    "M0061-C-COSET-PRODUCT-EQUIV",
    "M0061-C-FIBER-DECOMPOSITION",
    "M0061-T-FIBER-TO-COSET",
    "M0061-C-LEFT-COSET-EQUIV",
    "M0061-T-SIGMA-PRODUCT",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}
SUMMARY_LINES = (
    "PASS S56-M-0061-RELEASE negative reconciliation",
    "PASS narrow kernel replay: fourteen proof declarations are sorry-free and use only the observed allowed axioms",
    "FAIL CLOSED dependency: validation is provisional [_], unaccepted, and non-release-grade",
    "FAIL CLOSED release: cold offline, trust/TCB/SBOM, H0/R0, independent-verifier, deterministic-bundle, and master gates remain open",
    "verdict=blocked; lifecycle=planned; root=H1/M3/R4; audit_complete=false; theorem_complete=false",
)


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=30, check=False,
    )
    assert result.returncode == 0, result.stdout
    return result.stdout.strip()


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    manifest = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    lean_root = ROOT / "Formalizations" / "Lean"
    lake_link = lean_root / ".lake"
    mathlib = lake_link / "packages" / "mathlib"

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1093 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is target["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["state"] == "[ ]" and item["depends_on"] == ["S56-M-0061-VALIDATION"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0061-VALIDATION"
    )
    assert predecessor["state"] == "[_]"
    tasks = {row["id"]: row for row in local_dag["tasks"]}
    assert tasks[ITEM]["state"] == tasks["S56-M-0061-VALIDATION"]["state"] == "open"
    assert local_dag["accepted_states"] == []

    for name, expected in EXPECTED_AUTHORITY.items():
        assert sha256(ROOT / name) == expected, f"changed authority input: {name}"
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale release input: {name}"
    assert lake_link.is_symlink() and lake_link.resolve().is_dir()
    assert git("-C", str(mathlib), "rev-parse", "HEAD") == EXPECTED_MATHLIB_REVISION
    assert git("-C", str(mathlib), "rev-parse", "HEAD^{tree}") == EXPECTED_MATHLIB_TREE
    assert git("-C", str(mathlib), "status", "--short", "--untracked-files=all") == ""
    lean = subprocess.run(
        ["lake", "env", "which", "lean"], cwd=lean_root, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30, check=False,
    )
    lake = subprocess.run(
        ["lake", "env", "which", "lake"], cwd=lean_root, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30, check=False,
    )
    assert lean.returncode == lake.returncode == 0
    assert sha256(Path(lean.stdout.strip())) == EXPECTED_LEAN_SHA256
    assert sha256(Path(lake.stdout.strip())) == EXPECTED_LAKE_SHA256

    accepted_vector = {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == accepted_vector
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert registry["root_obligation_id"] == "M0061-ROOT"
    assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert set(proof["result"]["axioms"]) == EXPECTED_AXIOMS
    assert proof["accepted"] is False
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["result"]["provisional_exact_root_kernel_closed"] is True
    assert validation["result"]["accepted_root_kernel_closed"] is False
    assert validation["result"]["hermetic_release_gate"] == "fail_closed"
    assert validation["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False

    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["phase"] == receipt["phase"] == "release"
    assert decision["intent"] == receipt["intent"] == "release"
    assert decision["support_state"] == receipt["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert receipt["depends_on"] == ["S56-M-0061-VALIDATION"]
    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector_before"] == decision["root_vector_after"] == accepted_vector
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert decision["terminal_decisions"]["audit_complete"] is False
    assert decision["terminal_decisions"]["theorem_complete"] is False
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_release_specific_gate"]["gate_id"] == "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    assert decision["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["master_accepted"] is dependency["receipt_accepted"] is False
    assert dependency["receipt_release_grade"] is False

    required_cut_fragments = (
        "master acceptance", "authoritative H1/M3/R4", "foundation policy",
        "H0 primary-source", "R0 node-anchored", "empty-cache network-denied cold build",
        "SBOM, license", "two signed attestations", "minimal release verifier",
        "deterministic content-addressed release bundle",
    )
    cut_set = "\n".join(decision["remaining_root_cut_set"])
    for fragment in required_cut_fragments:
        assert fragment in cut_set, fragment
    for key in (
        "authoritative_dependency_acceptance", "authoritative_graph_reconciliation",
        "accepted_foundation_and_trust_closure", "human_source_acceptance",
        "readability_acceptance", "hermetic_release_reproduction",
        "supply_chain_archive", "independent_release_verification",
        "deterministic_release_bundle", "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] == "missing", key

    assert spec["cwd"] == receipt["recipe"]["cwd"] == "."
    assert spec["argv"] == receipt["recipe"]["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["env_allowlist"] == receipt["recipe"]["env_allowlist"] == {
        "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
    }
    assert spec["timeout_seconds"] == receipt["recipe"]["timeout_seconds"] == 180
    assert spec["expected_exit"] == receipt["recipe"]["expected_exit"] == 0
    assert spec["network_policy"] == receipt["recipe"]["network_policy"] == "denied"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    canonical_ids = [row["obligation_id"] for row in registry["obligations"]]
    assert len(canonical_ids) == 20
    assert receipt["kernel_replayed_obligation_ids"] == proof["closed_obligation_ids"] == PROOF_OBLIGATION_IDS
    assert spec["kernel_replayed_obligation_ids"] == PROOF_OBLIGATION_IDS
    assert receipt["canonical_obligation_ids"] == spec["covered_obligation_ids"] == canonical_ids
    assert spec["covered_declarations"] == [
        "Stage1Instances.THM_M_0061.LagrangeDivisibilityTarget",
        "Stage1Instances.THM_M_0061.Proof.lagrangeDivisibility",
        "Stage1Instances.THM_M_0061.Proof.lagrangeDivisibility_mathlib",
    ]
    assert receipt["statement_fingerprint"] == "sha256:" + proof["canonical_target_expression_sha256"]
    assert receipt["typed_graph_changes"].startswith("none;")
    assert receipt["declaration_ownership"] == []
    assert receipt["readable_ownership"] == [f"Stage1_Instances/{THEOREM}/release-phase.md"]
    assert receipt["change_impact_set"] == [ITEM]
    assert receipt["input_bindings"]["release-spec.json"] == sha256(HERE / "release-spec.json")
    assert receipt["input_bindings"]["release-decision.json"] == sha256(HERE / "release-decision.json")
    assert receipt["input_bindings"]["check_release.py"] == sha256(HERE / "check_release.py")
    assert receipt["input_bindings"]["release-phase.md"] == sha256(HERE / "release-phase.md")
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode("utf-8")
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact five-line PASS/FAIL-CLOSED release status summary",
    }]
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": hashlib.sha256(expected_stdout).hexdigest(),
        "expected_line_count": len(SUMMARY_LINES),
        "exit_code": 0,
    }
    assert receipt["first_failed_gate"] == decision["first_failed_gate"]["gate_id"]
    assert receipt["first_failed_release_gate"] == decision["first_failed_release_specific_gate"]["gate_id"]
    assert receipt["next_failed_release_gate"] == decision["next_failed_release_gate"]["gate_id"]
    environment = receipt["environment"]
    assert environment["lean_executable_sha256"] == EXPECTED_LEAN_SHA256
    assert environment["lake_executable_sha256"] == EXPECTED_LAKE_SHA256
    assert environment["mathlib_revision"] == EXPECTED_MATHLIB_REVISION
    assert environment["mathlib_tree"] == EXPECTED_MATHLIB_TREE
    assert environment["lake_symlink_target_policy"].startswith(
        "automation-provided canonical checkout cache"
    )
    assert len(receipt["invalidation_inputs"]) >= 6
    assert receipt["worker_reference"]["git_state"] == "detached HEAD"
    assert receipt["worker_reference"]["worktree_class"] == "stage1-rev56 automation worker slot2"
    assert set(receipt["composition_certificates"]) == set(closure["composition_certificates"]) | {
        "Stage1Instances.THM_M_0061.Proof.cosetProductEquivalence",
        "Stage1Instances.THM_M_0061.Proof.cardProductIdentity",
        "Stage1Instances.THM_M_0061.Proof.lagrangeDivisibility",
    }

    fixed_env = dict(os.environ)
    fixed_env.update({
        "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
    })
    replay = subprocess.run(
        ["bash", str(HERE / "check_proof.sh")], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120, check=False,
        env=fixed_env,
    )
    assert replay.returncode == 0, replay.stdout
    assert replay.stdout.count("Declarations are sorry-free!") == 14
    for axiom in EXPECTED_AXIOMS:
        assert axiom in replay.stdout
    assert "error:" not in replay.stdout and "sorryAx" not in replay.stdout

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    actual_changed = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
