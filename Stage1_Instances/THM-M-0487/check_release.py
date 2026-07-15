#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0487-RELEASE."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0487"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0487-RELEASE"
THEOREM = "THM-M-0487"
BASE_REVISION = "5134bae303d5f5104698e8c96d7af4c26306eb47"
BASE_TREE = "54e4bd2793df37c5451b86659fbd95a83504c25a"
VALIDATION_RECEIPT_ID = (
    "sha256:5d0bfada1868d33b29171b1d32d33fe6902cb370fe40b9cea92e4f41371917a5"
)
VALIDATION_BASE_REVISION = "9d50d838c8132b2aaf005a4863baeb5385e52a97"
EXPRESSION_SHA256 = "29ac94dd615869191754270061d8fe7123991d403a07bbdf27a09f706665e703"
DENOMINATOR_SHA256 = "1d456b6ecd31a58a47bac58a2746bc0f8d16ce4b4e2821348331c511e21c1a41"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
MACHINE_CUT = ["M0487-T-ANALYTIC", "M0487-T-FINITE-UPPER"]
RELEASE_CUT = [
    "M0487-X-SOURCE-MAIN",
    "M0487-X-SOURCE-MAJOR",
    "M0487-X-SOURCE-MINOR",
    "M0487-X-SOURCE-PRIME-BOUNDS",
    "M0487-X-SOURCE-FINITE",
    "M0487-S-FOUNDATION",
    "M0487-X-COMPUTATION",
    "M0487-X-EVIDENCE",
    "M0487-X-PROVENANCE",
    "M0487-X-TRUST",
    "M0487-X-READABLE",
    "M0487-X-WORKFLOW",
]
INTERFACE_OBLIGATIONS = [
    "M0487-S-INTERFACE",
    "M0487-S-DOMAIN",
    "M0487-S-BOUNDARY",
    "M0487-S-TRANSPORT",
    "M0487-N-REPRESENTATION",
    "M0487-N-CUTOFF",
    "M0487-B-RANGE-SPLIT",
    "M0487-N-FINITE-COVERAGE",
    "M0487-T-FINITE",
    "M0487-T-ASSEMBLE",
]
COMPOSITION_DECLARATIONS = [
    "Stage1Instances.THM_M_0487.ObligationTree.threePrimeRepresentation_iff",
    "Stage1Instances.THM_M_0487.ObligationTree.cutoff_cases",
    "Stage1Instances.THM_M_0487.ObligationTree.analyticCutoff_le_publishedFiniteUpper",
    "Stage1Instances.THM_M_0487.ObligationTree.finiteCoverage_of_publishedUpper",
    "Stage1Instances.THM_M_0487.ObligationTree.finiteRange_of_publishedFiniteUpper",
    "Stage1Instances.THM_M_0487.ObligationTree.root_of_analytic_and_finite",
    "Stage1Instances.THM_M_0487.ObligationTree.root_iff_analytic_and_finite",
]
PROOF_DECLARATIONS = [
    "Stage1Instances.THM_M_0487.Proof.representationCount_pos_iff",
    "Stage1Instances.THM_M_0487.Proof.weakGoldbachTarget_iff_positiveRepresentationCountTarget",
]
SOURCE_HASHES = {
    "Statement.lean": "9d0200046173c0b0d9d0b52cbf696087f4beea6946c92bfa41f03402a4090b0d",
    "ObligationTree.lean": "296af72935ce926686387ce60385a6565831c49029be2a70e1d93025cbd338f8",
    "Proof.lean": "b6257c8fb81fed20ce32c9c15392066a9dfd56e8e96469ca38e12d14689149be",
    "Validation.lean": "24367c2e40260d4329f9281cdd17fc34ddd94712686e58c235da89c563b4f223",
    "statement.json": "9c1088a26cf9eb7bb80753fb900aa189a14bfa0c8a39080325526758b8966247",
    "obligation-registry.json": "6fc1d3df9c49ffcd837ebe26d1a0f9c751480058585985150ff3cdb30086052f",
    "typed-graphs.json": "c3195f3fefd420fadd3875900db9fbb1a86d2bea3d876082e1325d2e369ba236",
    "proof-receipt.json": "d5a5fce77e4dcfbf7e67e2df42d686c5f9c7e61f9bb4c536245907024e601a5e",
    "proof-blocker-current.json": "a84d3920035e7a6aa993df21d650d8bbc77dada4debd6472e89ea536dba2471c",
    "validation-spec.json": "2589c11c75152f01a3c953f07b88e95f1051ae1e5e33781af302b4e703bd2399",
    "check_validation.py": "6a6630a6de147780fc0cbfd0de3c406e1b9dae6a768e06e897b6ec9a664b2508",
    "validation-receipt.json": "7a355987b9f37c44c60b03b277aa9063fec842de2cc9f57ef76265ef3ad5caf7",
    "validation-blocker.json": "1357bf06c30582c79126f3256870d57cb524c95550c55aef5d7036804fb3e9aa",
    "anchor-audit.json": "569ce7bc7b56c01ae6a8a57f03071e2d95d0bc01aeae28cdd2181217f8a99f36",
    "source-statement-crosswalk.md": "11bc2b4d59fca275412236f32a4b93153e3fc7f6cd1600ca6e6962c57c98eb92",
}
# Keep the human-readable output deterministic so its receipt hash is meaningful.
SEMANTIC_OUTPUT = "\n".join(
    (
        "PASS S56-M-0487-RELEASE: current authority, frozen denominator, receipts, and unchanged cuts reconcile",
        "PASS partial replay: exact statement, obligation-tree interfaces/compositions, and two finite-count interfaces pass trust-zero checks",
        "BLOCKED first gate: S56-10.2-DEPENDENCY-ACCEPTANCE / dependency.S56-M-0487-VALIDATION.master_acceptance",
        "OPEN exact root: M0487-T-ANALYTIC and M0487-T-FINITE-UPPER have no terminal proof bodies",
        "BLOCKED assurance: H0/R0/provenance/TCB/cold-offline/independent/bundle gates remain",
        "VERDICT blocked: planned H1/M3/R3; audit_complete=false; theorem_complete=false",
    )
)
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
]


if not __debug__:
    raise RuntimeError("release reconciliation requires Python assertions")


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


def run(
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 650,
    expected_exit: int = 0,
) -> str:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != expected_exit:
        raise RuntimeError(
            f"command exited {completed.returncode}, expected {expected_exit}: "
            f"{argv!r}\n{completed.stdout}"
        )
    return completed.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).rstrip()


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


def reported_axioms(output: str, declaration: str) -> set[str]:
    no_axioms = f"'{declaration}' does not depend on any axioms"
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL
    )
    matches = pattern.findall(output)
    assert output.count(no_axioms) + len(matches) == 1, declaration
    if not matches:
        return set()
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def check_authority(receipt: dict, decision: dict) -> None:
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1366
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release = next(row for row in execution["items"] if row["id"] == ITEM)
    validation = next(
        row for row in execution["items"] if row["id"] == "S56-M-0487-VALIDATION"
    )
    assert release == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1366,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0487-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation["state"] == "[_]" and validation["attempts"] == 1
    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert dag["lifecycle"] == "planned" and dag["accepted_states"] == []
    assert dag["audit_complete"] is dag["theorem_complete"] is False
    local_release = next(row for row in dag["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in dag["tasks"] if row["id"] == "S56-M-0487-VALIDATION"
    )
    assert local_release["state"] == local_validation["state"] == "open"

    assert receipt["authority_inputs"] == {
        "Docs/Stage1_Targets_rev-5.6.json": sha256(
            ROOT / "Docs/Stage1_Targets_rev-5.6.json"
        ),
        "Docs/Stage1_Execution_DAG_rev-5.6.json": sha256(
            ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json"
        ),
        "instance.json": sha256(HERE / "instance.json"),
        "task-dag.json": sha256(HERE / "task-dag.json"),
    }
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    vector = {"H": "H1", "M": "M3", "R": "R3"}
    assert decision["root_vector_before"] == decision["root_vector_after"] == vector


def check_reconciliation(receipt: dict, decision: dict, spec: dict) -> None:
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker-current.json")
    validation = load(HERE / "validation-receipt.json")
    validation_blocker = load(HERE / "validation-blocker.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["execution_rank"] == decision["execution_rank"] == 1366
    assert receipt["phase"] == receipt["intent"] == decision["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0487-VALIDATION"]
    assert receipt["verdict"] == decision["verdict"] == "blocked"
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["receipt_class"] == receipt["support_state"] == (
        "provisional_worker_selftest"
    )
    assert receipt["content_addressed"] is False and receipt["release_grade"] is False
    assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
    assert receipt["master_acceptance"] == "pending_and_not_claimed"
    assert receipt["accepted_receipt_ids"] == decision["accepted_receipt_ids"] == []
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["result"]["semantic_output_sha256"] == hashlib.sha256(
        SEMANTIC_OUTPUT.encode("utf-8")
    ).hexdigest()

    for name, digest in SOURCE_HASHES.items():
        assert sha256(HERE / name) == digest, f"bound predecessor input changed: {name}"
    assert decision["reconciled_inputs"] == SOURCE_HASHES
    for name, digest in receipt["release_artifact_inputs"].items():
        assert sha256(HERE / name) == digest, f"release artifact input changed: {name}"

    assert decision["dependency"]["receipt_id"] == validation["receipt_id"] == (
        VALIDATION_RECEIPT_ID
    )
    assert decision["dependency"]["receipt_sha256"] == sha256(
        HERE / "validation-receipt.json"
    )
    assert validation["base_revision"] == VALIDATION_BASE_REVISION != BASE_REVISION
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]" and validation["verdict"] == "blocked"
    assert validation["accepted"] is False and validation["content_addressed"] is False
    assert validation["release_grade"] is False and validation["accepted_receipt_ids"] == []
    assert validation["first_failed_gate"] == "dependency.S56-M-0487-PROOF.not_complete"
    assert validation["first_failed_root_gate"] == MACHINE_CUT[0]
    assert validation["first_failed_release_gate"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert validation["remaining_root_cut_set"] == MACHINE_CUT
    result = validation["result"]
    assert result["accepted_closed_obligation_ids"] == []
    assert result["root_kernel_closed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert validation_blocker["remaining_root_cut_set"] == MACHINE_CUT
    assert validation_blocker["theorem_complete"] is False

    assert proof["accepted"] is False and proof["proposed_state"] == "[_]"
    assert proof["supported_obligation_ids"] == []
    assert proof["provisionally_closed_obligation_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["remaining_root_cut_set"] == proof_blocker["remaining_root_cut_set"] == (
        MACHINE_CUT
    )
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False

    canonical = statement["canonical_formal_target"]
    assert canonical["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert canonical["statement_file_sha256"] == SOURCE_HASHES["Statement.lean"]
    assert registry["root_obligation_id"] == graphs["root_obligation_id"] == "M0487-ROOT"
    assert registry["denominator_sha256"] == graphs[
        "registry_denominator_sha256"
    ] == DENOMINATOR_SHA256
    assert len(registry["obligations"]) == 54
    obligation_ids = {row["obligation_id"] for row in registry["obligations"]}
    assert set(INTERFACE_OBLIGATIONS + MACHINE_CUT + RELEASE_CUT + ["M0487-ROOT"]) <= (
        obligation_ids
    )
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["minimal_open_proof_cut_sets"] == [MACHINE_CUT]
    assert closure["open_release_gates"] == RELEASE_CUT
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert decision["authoritative_graph_remaining_machine_root_cut_set"] == MACHINE_CUT
    assert decision["authoritative_graph_remaining_release_cut_set"] == RELEASE_CUT

    assert decision["audit_complete"] is decision["theorem_complete"] is False
    assert decision["release_accepted"] is False
    assert decision["first_failed_gate"]["gate_id"] == receipt["first_failed_gate"] == (
        "S56-10.2-DEPENDENCY-ACCEPTANCE"
    )
    assert decision["first_failed_gate"]["node_gate"] == (
        "dependency.S56-M-0487-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_root_gate"]["gate_id"] == (
        receipt["first_failed_root_gate"]
    ) == MACHINE_CUT[0]
    assert decision["first_failed_release_assurance_gate"]["gate_id"] == (
        receipt["first_failed_release_gate"]
    ) == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    assert decision["known_failures"] == receipt["known_failures"]
    assert decision["remaining_root_cut_set"] == receipt["remaining_root_cut_set"]
    assert decision["retry_condition"] == receipt["retry_condition"]
    assert decision["freshness"] == receipt["freshness"]
    assert decision["invalidation_inputs"] == receipt["invalidation_inputs"]

    gate_state = decision["evidence_reconciliation"]
    required_false = (
        "validation_dependency_master_accepted",
        "validation_recipe_fresh_at_current_authority",
        "exact_root_kernel_closed",
        "accepted_root_m0_e1",
        "authoritative_graph_reconciled",
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
    )
    for gate in required_false:
        assert gate_state[gate] is False, f"release gate silently cleared: {gate}"

    cut = "\n".join(decision["remaining_root_cut_set"])
    for phrase in (
        "master acceptance",
        "M0487-T-ANALYTIC",
        "M0487-T-FINITE-UPPER",
        "M0/E1",
        "H0 primary-source",
        "R0 node-complete",
        "TCB closure",
        "empty-cache network-denied cold build",
        "SBOM",
        "two signed attestations",
        "minimal release verifier",
        "protected CI",
        "deterministic content-addressed release bundle",
    ):
        assert phrase in cut, f"release cut omits {phrase!r}"

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["recipe_id"] == receipt["recipe"]["recipe_id"]
    assert spec["cwd"] == "." and spec["network_policy"] == "denied"
    assert spec["timeout_seconds"] == 720 and spec["expected_exit"] == 0
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id",
            "cwd",
            "argv",
            "env_allowlist",
            "timeout_seconds",
            "network_policy",
            "network_enforcement",
            "expected_exit",
            "expected_outputs",
            "covered_obligation_ids",
            "covered_declarations",
        )
    }
    assert spec["covered_obligation_ids"] == INTERFACE_OBLIGATIONS
    assert spec["covered_declarations"] == [
        "Stage1Instances.THM_M_0487.WeakGoldbachTarget",
        *COMPOSITION_DECLARATIONS,
        *PROOF_DECLARATIONS,
    ]
    assert spec["negative_status_only_obligation_ids"] == [
        "M0487-ROOT",
        *MACHINE_CUT,
        *RELEASE_CUT,
    ]
    assert "receive no closure credit" in spec["scope_boundary"]

    prose = (HERE / "release-phase.md").read_text(encoding="utf-8")
    for fragment in (
        "The release verdict is **blocked**.",
        "`audit_complete=false`",
        "`theorem_complete=false`",
        "`S56-10.2-DEPENDENCY-ACCEPTANCE`",
        "not theorem completion",
    ):
        assert fragment in prose, f"release prose lost boundary: {fragment}"


def replay_partial_scope(spec: dict, receipt: dict) -> None:
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert (LEAN_ROOT / ".lake").is_symlink()
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert sha256(Path("/usr/bin/python3")) == PYTHON_SHA256
    assert sha256(Path("/usr/bin/bwrap")) == BWRAP_SHA256

    toolchain_bin = (
        Path(pwd.getpwuid(os.getuid()).pw_dir)
        / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin"
    )
    lean = toolchain_bin / "lean"
    lake = toolchain_bin / "lake"
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    fixed_env = {
        "HOME": os.environ["HOME"],
        "PATH": f"{toolchain_bin}:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    assert {key: os.environ[key] for key in spec["env_allowlist"]} == (
        spec["env_allowlist"]
    )
    assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT, env=fixed_env)
    assert "5.0.0" in run([str(lake), "--version"], cwd=LEAN_ROOT, env=fixed_env)

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    lean_names = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in lean_names
    )
    assert prohibited.search(all_source) is None
    validation_source = source_without_comments(
        (HERE / "Validation.lean").read_text(encoding="utf-8")
    )
    assert re.search(r"^(?:theorem|def|abbrev|instance)\b", validation_source, re.MULTILINE) is None
    assert validation_source.count("assert_no_sorry ") == len(PROOF_DECLARATIONS)
    for forbidden in (
        "AnalyticRangePackage :=",
        "FiniteUpperBoundPackage :=",
        "WeakGoldbachTarget :=",
    ):
        assert forbidden not in validation_source

    compiled_dirs = sorted(
        path.resolve()
        for path in (LEAN_ROOT / ".lake" / "packages").glob("*/.lake/build/lib/lean")
        if path.is_dir()
    )
    root_build = (LEAN_ROOT / ".lake" / "build" / "lib" / "lean").resolve()
    if root_build.is_dir():
        compiled_dirs.insert(0, root_build)
    assert compiled_dirs and any("/mathlib/" in str(path) for path in compiled_dirs)
    lean_path = ":".join(str(path) for path in compiled_dirs)

    temp_root = Path(tempfile.mkdtemp(prefix="stage1-m0487-release-", dir="/tmp"))
    try:
        target_dir = temp_root / "Stage1_Instances" / THEOREM
        target_dir.mkdir(parents=True)
        for name in lean_names:
            shutil.copy2(HERE / name, target_dir / name)
        (temp_root / "home").mkdir()

        def isolated_lean(name: str, *, module_path: bool) -> str:
            path = f"{target_dir}:{lean_path}" if module_path else lean_path
            return run(
                [
                    str(lake),
                    "env",
                    "lean",
                    "--trust=0",
                    "-t0",
                    "--root",
                    str(target_dir),
                    "-o",
                    str(target_dir / f"{Path(name).stem}.olean"),
                    str(target_dir / name),
                ],
                cwd=MATHLIB,
                env={**fixed_env, "HOME": str(temp_root / "home"), "LEAN_PATH": path},
            )

        statement_output = isolated_lean("Statement.lean", module_path=False)
        obligation_output = isolated_lean("ObligationTree.lean", module_path=True)
        proof_output = isolated_lean("Proof.lean", module_path=True)
        validation_output = isolated_lean("Validation.lean", module_path=True)
        olean_hashes = {
            name: sha256(target_dir / name)
            for name in (
                "Statement.olean",
                "ObligationTree.olean",
                "Proof.olean",
                "Validation.olean",
            )
        }
    finally:
        shutil.rmtree(temp_root)

    for declaration in COMPOSITION_DECLARATIONS:
        assert reported_axioms(obligation_output, declaration) <= EXPECTED_AXIOMS
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(proof_output, declaration) == EXPECTED_AXIOMS
        assert reported_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    combined = "\n".join(
        (statement_output, obligation_output, proof_output, validation_output)
    )
    assert "Stage1Instances.THM_M_0487.WeakGoldbachTarget" in statement_output
    assert proof_output.count("Declarations are sorry-free!") == 2
    assert validation_output.count("Declarations are sorry-free!") == 1
    assert "sorryAx" not in proof_output + validation_output
    assert "declaration uses 'sorry'" not in proof_output + validation_output
    assert "error:" not in combined
    assert receipt["result"]["fresh_olean_sha256"] == olean_hashes
    assert receipt["result"]["observed_axioms"] == sorted(EXPECTED_AXIOMS)
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""


def check_worker_packet(receipt: dict, packet_path: Path) -> None:
    packet = load(packet_path.resolve())
    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"] == CHANGED_PATHS
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    actual = {
        line[3:]
        for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    spec = load(HERE / "release-spec.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    check_authority(receipt, decision)
    check_reconciliation(receipt, decision, spec)
    replay_partial_scope(spec, receipt)
    if args.worker_packet is not None:
        check_worker_packet(receipt, args.worker_packet)

    for relative in CHANGED_PATHS[1:]:
        assert_text_hygiene(ROOT / relative)
    print(SEMANTIC_OUTPUT)


if __name__ == "__main__":
    main()
