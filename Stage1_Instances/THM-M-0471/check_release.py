#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0471-RELEASE."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0471"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0471-RELEASE"
THEOREM = "THM-M-0471"
BASE_REVISION = "dc600635160cace0916df5234bf8808c39dc656d"
BASE_TREE = "8ee34b31ec38be1ef067aaab38c9a4cb4935b75a"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
FACTORS_SOURCE_SHA256 = "3e64e2c8ba907c05209966a7bba8754cf2ab33f328a3010667ffe58c95e0bca3"
FACTORS_OLEAN_SHA256 = "ca04f32795ce6aba7a89b812e7b57cf1a11ebebb4a2428469252dad6fa132b70"
LIST_PRIME_SOURCE_SHA256 = "148cf3e70ddc39591270dd3c4d9da733a91ff574e8f5c1bd6fd8fd2f42e33591"
LIST_PRIME_OLEAN_SHA256 = "0070fd6c21af18e3bc139e406be76fc7f7d6d2b62165eee6910aee740126c328"
EXPRESSION_SHA256 = "07ae92b7b398b89a1bbe8413563f1c30da5b8bbd0522f6d070fd62dcea0ac4e4"
DENOMINATOR_SHA256 = "d3f11762e2a0f4c384d094d53e44100f20a21f81eb6ce527cd5f9897a9bc445c"
VALIDATION_OUTPUT_SHA256 = "97ce534ac3d2011dcd3210c0e39711c53181e7cb5462e3ca9e751799a0f4999c"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
GRAPH_CUT = [
    "M0471-T-ASSEMBLE",
    "M0471-S-FOUNDATION",
    "M0471-X-SOURCE",
    "M0471-X-PROVENANCE",
    "M0471-X-READABLE",
    "M0471-X-WORKFLOW",
]
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
]

if not __debug__:
    raise RuntimeError("release validation requires Python assertions")


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
    timeout: int = 330,
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
    if completed.returncode != 0:
        raise RuntimeError(f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}")
    return completed.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).rstrip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def observed_axioms(output: str, declaration: str) -> set[str]:
    no_axioms = f"'{declaration}' does not depend on any axioms"
    if no_axioms in output:
        return set()
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        flags=re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


def check_authority(receipt: dict) -> None:
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1353
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release = next(row for row in execution["items"] if row["id"] == ITEM)
    validation = next(
        row for row in execution["items"] if row["id"] == "S56-M-0471-VALIDATION"
    )
    assert release == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1353,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0471-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation["state"] == "[_]" and validation["attempts"] == 1
    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert dag["lifecycle"] == dag["lifecycle_mode"] == "planned"
    assert dag["accepted_states"] == []
    assert dag["audit_complete"] is dag["theorem_complete"] is False
    local_release = next(row for row in dag["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in dag["tasks"] if row["id"] == "S56-M-0471-VALIDATION"
    )
    assert local_release["state"] == local_validation["state"] == "open"
    assert receipt["authority_inputs"] == {
        "Docs/Stage1_Targets_rev-5.6.json": sha256(
            ROOT / "Docs/Stage1_Targets_rev-5.6.json"
        ),
        "Docs/Stage1_Execution_DAG_rev-5.6.json": sha256(
            ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json"
        ),
        "Stage1_Instances/THM-M-0471/instance.json": sha256(HERE / "instance.json"),
        "Stage1_Instances/THM-M-0471/task-dag.json": sha256(HERE / "task-dag.json"),
    }


def check_reconciliation(receipt: dict, decision: dict, spec: dict) -> None:
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert receipt["decision_id"] == decision["decision_id"]
    assert decision["phase"] == receipt["phase"] == "release"
    assert decision["intent"] == receipt["intent"] == "release"
    assert decision["execution_rank"] == receipt["execution_rank"] == 1353
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    assert receipt["depends_on"] == ["S56-M-0471-VALIDATION"]
    assert decision["normative_profile"] == receipt["normative_profile"] == (
        "machine-theorem-assurance/1.0"
    )
    assert decision["content_addressed"] is receipt["content_addressed"] is False
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert decision["decided_at"] == receipt["validated_at"] == (
        "2026-07-13T23:42:00+08:00"
    )
    assert decision["attestor"] == receipt["attestor"] == "stage1-rev56-worker-slot2"
    assert receipt["acceptance_authority"] == "Stage1 integration lane"
    assert receipt["receipt_class"] == receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["release_grade"] is False
    assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
    assert receipt["master_acceptance"] == "pending_and_not_claimed"
    assert receipt["accepted_receipt_ids"] == decision["accepted_receipt_ids"] == []
    for name, expected in receipt["release_artifact_inputs"].items():
        assert sha256(HERE / name) == expected, f"release artifact drifted: {name}"
    for relative, expected in decision["reconciled_inputs"].items():
        assert sha256(ROOT / relative) == expected, f"reconciled input drifted: {relative}"

    dependency = decision["dependency"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0471-VALIDATION"
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["proposed_state"] == validation["proposed_state"] == "[_]"
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["content_addressed_release_evidence"] is (
        validation["content_addressed_release_evidence"]
    ) is False
    assert dependency["master_accepted"] is False
    assert decision["provisional_receipt_ids_inspected"] == [
        proof["receipt_id"], validation["receipt_id"]
    ]
    assert receipt["predecessor_inputs"]["proof_receipt_sha256"] == sha256(
        HERE / "proof-receipt.json"
    )
    assert receipt["predecessor_inputs"]["proof_receipt_id"] == proof["receipt_id"]
    assert receipt["predecessor_inputs"]["validation_receipt_sha256"] == sha256(
        HERE / "validation-receipt.json"
    )
    assert receipt["predecessor_inputs"]["validation_receipt_id"] == validation["receipt_id"]
    assert receipt["predecessor_inputs"]["validation_support_state"] == (
        validation["support_state"]
    )
    assert receipt["predecessor_inputs"]["validation_accepted"] is validation["accepted"] is False
    assert receipt["predecessor_inputs"]["validation_release_grade"] is (
        validation["release_grade"]
    ) is False
    assert proof["accepted"] is False and proof["proposed_state"] == "[_]"
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert validation["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert validation["result"]["accepted_root_machine_debt"] == "M3"
    assert validation["result"]["accepted_root_closed"] is False
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0471-ROOT"
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert decision["canonical_target_expression_sha256"] == (
        receipt["canonical_target_expression_sha256"]
    ) == EXPRESSION_SHA256
    assert decision["registry_denominator_sha256"] == (
        receipt["registry_denominator_sha256"]
    ) == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["accepted_closed_obligations"] == []
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == GRAPH_CUT

    result = decision["decision"]
    receipt_result = receipt["result"]
    assert result["verdict"] == receipt["verdict"] == receipt_result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H1", "M3", "R4"]
    assert receipt_result["lifecycle_before"] == receipt_result["lifecycle_after"] == "planned"
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == [
        "H1", "M3", "R4"
    ]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == receipt["first_failed_gate"]
    assert receipt["first_failed_gate"] == receipt_result["first_failed_gate"] == (
        "S56-10.2-DEPENDENCY-ACCEPTANCE"
    )
    assert receipt_result["dependency_master_acceptance"] == "fail_closed"
    assert receipt_result["authoritative_root_state"] == "H1/M3/R4_open"
    assert receipt_result["audit_z"] == receipt_result["theorem_z"] == "fail_closed"
    assert receipt_result["hermetic_release_gate"] == "fail_closed"
    assert receipt_result["supply_chain_gate"] == "fail_closed"
    assert receipt_result["independent_verification_gate"] == "fail_closed"
    assert receipt_result["deterministic_bundle_gate"] == "fail_closed"
    assert receipt_result["master_acceptance_gate"] == "pending"
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        receipt_result["next_failed_release_gate"]
    ) == "S56-10.6-HERMETIC-COLD-BUILD"
    assert result["remaining_root_cut_set"] == receipt["remaining_root_cut_set"]
    assert decision["known_failures"] == receipt["known_failures"]
    assert decision["retry_condition"] == receipt["retry_condition"]
    assert decision["freshness"] == receipt["freshness"]
    assert decision["invalidation_inputs"] == receipt["invalidation_inputs"]

    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["provisional_exact_root_kernel_replay"] is True
    assert reconciliation["provisional_same_worker_differential_replay"] is True
    for gate in (
        "accepted_exact_root_kernel_closure",
        "authoritative_graph_reconciled",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_mutation_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[gate] is False, f"release gate silently cleared: {gate}"
    assert reconciliation["accepted_closed_obligations"] == []

    cut = "\n".join(result["remaining_root_cut_set"])
    for phrase in (
        "master acceptance",
        "M0-W/E1",
        "M0471-S-FOUNDATION",
        "H0 primary-source",
        "R0 node-anchored",
        "TCB inventory",
        "empty-cache network-denied cold build",
        "SBOM",
        "two signed attestations",
        "minimal release verifier",
        "protected CI",
        "deterministic content-addressed release bundle",
    ):
        assert phrase in cut, f"release cut set omits {phrase!r}"

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["recipe_id"] == decision["release_recipe_id"]
    assert spec["argv"] == [
        "python3", "-I", "-B",
        f"Stage1_Instances/{THEOREM}/check_release.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert spec["cwd"] == "." and spec["network_policy"] == "denied"
    assert spec["timeout_seconds"] == 360 and spec["expected_exit"] == 0
    assert set(spec["decision_covered_obligation_ids"]) == {
        row["obligation_id"] for row in registry["obligations"]
    }
    assert receipt["decision_covered_obligation_ids"] == (
        spec["decision_covered_obligation_ids"]
    )
    assert spec["covered_declarations"] == [
        "Stage1Instances.THM_M_0471.FundamentalTheoremOfArithmeticTarget",
        "Stage1Instances.THM_M_0471.Proof.fundamentalTheoremOfArithmetic",
        "Stage1Instances.THM_M_0471.Proof."
        "fundamentalTheoremOfArithmetic_via_frozen_composition",
        "Stage1Instances.THM_M_0471.Validation."
        "independentlyReconstructedFundamentalTheoremOfArithmetic",
    ]
    assert receipt["kernel_replayed_declarations"] == spec["covered_declarations"]
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact seven-line release reconciliation summary",
    }]
    assert spec["scope_boundary"] == (
        "All 22 obligation IDs are covered only as fail-closed release-decision "
        "state reconciliation. The narrow kernel replay checks the four named "
        "declarations over the existing pinned warm cache. The outer Python process "
        "is observational and made no network request; bubblewrap enforces network "
        "denial only for the nested Lean subprocesses. This is not whole-recipe "
        "network isolation, dependency acceptance, a cold empty-cache offline build, "
        "complete provenance/foundation/TCB or SBOM closure, accepted H0/R0 review, "
        "independent signed verification, a deterministic release bundle, or master "
        "acceptance."
    )
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
    ):
        assert receipt["recipe"][key] == spec[key], key


def replay_validation(spec: dict) -> None:
    env = os.environ.copy()
    env.update(spec["env_allowlist"])
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    lean = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
    lake = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lake"
    python = Path(os.path.realpath(os.sys.executable))
    git_path = shutil.which("git")
    bwrap = shutil.which("bwrap")
    assert git_path is not None and bwrap is not None
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(python) == PYTHON_SHA256
    assert sha256(Path(os.path.realpath(git_path))) == GIT_SHA256
    assert sha256(Path(os.path.realpath(bwrap))) == BWRAP_SHA256
    version = run([str(lean), "--version"], env=env)
    assert "4.29.0" in version and LEAN_COMMIT in version
    lake_version = run([str(lake), "--version"], env=env).strip()
    assert lake_version == "Lake version 5.0.0-src+98dc76e (Lean version 4.29.0)"
    assert MATHLIB.resolve().is_dir() and (LEAN_ROOT / ".lake").is_symlink()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    factors = MATHLIB / "Mathlib/Data/Nat/Factors.lean"
    factors_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/Data/Nat/Factors.olean"
    list_prime = MATHLIB / "Mathlib/Data/List/Prime.lean"
    list_prime_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/Data/List/Prime.olean"
    assert sha256(factors) == FACTORS_SOURCE_SHA256
    assert sha256(factors_olean) == FACTORS_OLEAN_SHA256
    assert sha256(list_prime) == LIST_PRIME_SOURCE_SHA256
    assert sha256(list_prime_olean) == LIST_PRIME_OLEAN_SHA256
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    environment = load(HERE / "release-receipt.json")["environment"]
    assert environment == {
        "platform": f"{platform.system()} {platform.release()} {platform.machine()}",
        "toolchain": f"Lean 4.29.0, commit {LEAN_COMMIT}",
        "lean_executable_sha256": LEAN_SHA256,
        "lake_version": "5.0.0-src+98dc76e",
        "lake_executable_sha256": LAKE_SHA256,
        "python_executable_sha256": PYTHON_SHA256,
        "git_executable_sha256": GIT_SHA256,
        "bubblewrap_executable_sha256": BWRAP_SHA256,
        "mathlib_revision": MATHLIB_REVISION,
        "mathlib_tree": MATHLIB_TREE,
        "network": (
            "denied for the nested Lean replay by bubblewrap --unshare-net; "
            "host-side release reconciliation made no network request"
        ),
        "filesystem": (
            "read-only host root for the nested Lean processes; only a fresh "
            "temporary output directory was writable"
        ),
        "dependency_cache": (
            "pre-existing scheduler-provided canonical pinned .lake symlink, "
            "warm and reused read-only"
        ),
        "worktree_classification": (
            "nonrelease worker handoff containing only owned release artifacts, "
            "the root worker packet, and the pre-existing untracked .lake symlink"
        ),
        "fixed_recipe_environment": spec["env_allowlist"],
    }

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for path in (
        HERE / "Statement.lean",
        HERE / "ObligationTree.lean",
        HERE / "Proof.lean",
        HERE / "Validation.lean",
        factors,
        list_prime,
    ):
        assert prohibited.search(code_without_comments(path.read_text(encoding="utf-8"))) is None

    output = run(["bash", str(HERE / "check_validation.sh")], env=env)
    assert hashlib.sha256(output.encode("utf-8")).hexdigest() == VALIDATION_OUTPUT_SHA256
    assert output.count("Declarations are sorry-free!") == 25
    assert "sorryAx" not in output and "declaration uses 'sorry'" not in output
    roots = (
        "Stage1Instances.THM_M_0471.Proof.fundamentalTheoremOfArithmetic",
        "Stage1Instances.THM_M_0471.Proof.fundamentalTheoremOfArithmetic_via_frozen_composition",
        "Stage1Instances.THM_M_0471.Validation."
        "independentlyReconstructedFundamentalTheoremOfArithmetic",
    )
    for declaration in roots:
        assert observed_axioms(output, declaration) == EXPECTED_AXIOMS, declaration
    receipt_result = load(HERE / "release-receipt.json")["result"]
    assert receipt_result["observed_axioms"] == sorted(EXPECTED_AXIOMS)
    assert receipt_result["sorry_free_reports"] == output.count(
        "Declarations are sorry-free!"
    ) == 25
    assert receipt_result["placeholder_and_unsafe_scan"] == (
        "pass for the four local Lean modules and two pinned terminal source modules"
    )
    assert receipt_result["local_kernel_replay"] == (
        "pass_for_exact_statement_two_frozen_compositions_two_exact_roots_"
        "and_same_worker_differential_root"
    )
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""


def check_worker_packet(receipt: dict, packet_path: Path) -> None:
    packet = load(packet_path.resolve())
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"] == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    decision = load(HERE / "release-decision.json")
    assert decision["changed_paths"] == receipt["changed_paths"]
    assert "accepts no receipt" in decision["status_boundary"]
    assert "accepts no receipt" in receipt["status_boundary"]
    status = git("status", "--short", "--untracked-files=all")
    actual = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))


def assert_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()
    spec = load(HERE / "release-spec.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    check_authority(receipt)
    check_reconciliation(receipt, decision, spec)
    replay_validation(spec)
    if args.worker_packet is not None:
        check_worker_packet(receipt, args.worker_packet)
    for relative in CHANGED_PATHS[1:]:
        assert_hygiene(ROOT / relative)

    summary = (
        "PASS S56-M-0471-RELEASE: exact root and differential kernel replay agree",
        "PASS reconciliation: authority, pins, receipts, graph cut, and unchanged vector agree",
        "PASS hygiene: local and selected terminal sources contain no prohibited construct",
        "BLOCKED first gate: S56-10.2-DEPENDENCY-ACCEPTANCE",
        "BLOCKED release input/cold replay: immutable clean and S56-10.6 gates remain",
        "BLOCKED assurance: H0/R0/provenance/TCB/independent/bundle gates remain",
        "VERDICT blocked: planned H1/M3/R4; audit_complete=false; theorem_complete=false",
    )
    output = "\n".join(summary) + "\n"
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": hashlib.sha256(output.encode("utf-8")).hexdigest(),
        "expected_line_count": len(summary),
        "exit_code": 0,
    }
    print(output, end="")


if __name__ == "__main__":
    main()
