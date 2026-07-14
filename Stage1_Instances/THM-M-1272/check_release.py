#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1272-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1272"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1272-RELEASE"
THEOREM = "THM-M-1272"
BASE_REVISION = "818d5a5c4333773091da1eab98b76f3ac87cfa12"
BASE_TREE = "f833363d3cf0a9a67bd0b1ab128ec5e4796b16b1"
VALIDATION_BASE = "e6c4d56e017f77b02752e6c1325f0298dfb7f4d4"
EXPRESSION_SHA256 = "529bd5aeec0b1e9e58034f05dc03531a3fd9063547aeb54b68d5c0821d46cd31"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_RUNTIME_HASHES = {
    "lean_executable_sha256": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "python_executable_sha256": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "git_executable_sha256": "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a",
    "bash_executable_sha256": "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd",
    "bubblewrap_executable_sha256": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
    "cp_executable_sha256": "ddffb913956d7f8cbdd7722b8c331cea51e9a13c59e92de8c194ae30e5eb0b1e",
    "mktemp_executable_sha256": "48893b0fb21436b54619db80486e83ef39dfccaf1aefe83dfa00c02d6146e8c0",
    "mkdir_executable_sha256": "48893b0fb21436b54619db80486e83ef39dfccaf1aefe83dfa00c02d6146e8c0",
    "sha256sum_executable_sha256": "48893b0fb21436b54619db80486e83ef39dfccaf1aefe83dfa00c02d6146e8c0",
}
INVENTORY_IDS = [
    "M1272-ROOT",
    "M1272-S-DEFINITIONS",
    "M1272-S-BOUNDARY",
    "M1272-S-FOUNDATION",
    "M1272-N-SYMMETRIC",
    "M1272-C-MINIMAX",
    "M1272-L-LINKING",
    "M1272-T-LOWER-BOUND",
    "M1272-C-DEFORMATION",
    "M1272-L-LEVEL-BOUNDED",
    "M1272-L-PS-SUBSEQUENCE",
    "M1272-L-LIMIT-PASSAGE",
    "M1272-T-CRITICAL-LEVELS",
    "M1272-T-ASSEMBLE",
    "M1272-X-SOURCE",
    "M1272-X-PROVENANCE",
]
PARTIAL_IDS = [
    "M1272-L-LEVEL-BOUNDED",
    "M1272-L-PS-SUBSEQUENCE",
    "M1272-L-LIMIT-PASSAGE",
    "M1272-T-CRITICAL-LEVELS",
]
AUTHORITATIVE_CUT = ["M1272-T-LOWER-BOUND", "M1272-T-CRITICAL-LEVELS"]
PROVISIONAL_CUT = [
    "M1272-N-SYMMETRIC",
    "M1272-C-MINIMAX",
    "M1272-L-LINKING",
    "M1272-C-DEFORMATION",
    "M1272-T-LOWER-BOUND",
]
EXPECTED_INPUTS = {
    "Statement.lean": "da530b9b71de757b21579996e2c90558c2affcb6a1fc0e90517986deb7ee1eec",
    "ObligationTree.lean": "e155ad286cce68905562dad3249f44678a6e412ada2872b1484299bddae8a3e2",
    "Proof.lean": "0b9b1d51ce105c1d96fec5927018771569b61187b985888b1c33d3b4bf7f0b73",
    "Validation.lean": "da9794a52e67be68326b15db966f0658956784624ba3d41631804400ffd7327e",
    "instance.json": "be03c0851b67571edee686dab17724a731a836da3b76ed5fb58089525cb68577",
    "task-dag.json": "05c5bc724d78b2a1e30d0149ab6ecb162476caedc909edb7ea6d3a0abae63de6",
    "statement.json": "9feb63c9e24540b8ca00942cb2a23c852e17716fd17572f0e074810718503010",
    "anchor-audit.json": "dfe7218e8bb9a79c28e708897fb076457a0cd636201f17dd15da21b795e6360c",
    "obligation-registry.json": "601e7af4df4b5b1ef0a74ceafd93b5fa04187b2d694d5501ccd46ea7eb6d82e8",
    "typed-graphs.json": "71edd6a8ee145997c997a0b68f73ff3444c27a6553f73604f0b67c505c3c9c23",
    "proof-receipt.json": "791c810401a4b6d4ed1783a556703151f910a4e1d7b2dd40c253db227a116365",
    "validation-spec.json": "25e4ac71b4aeeb83d647d3c09d9e70ebb3eca49401e51a1b672e15dc3856190b",
    "validation-receipt.json": "a0669119a3b0e5623e27afad30fb902dabdf25c99414b9c51c08f5db23573cb8",
    "check_validation.py": "17d1445c259c6c3df7f522005a1d55724390b917c39daa9f9771e719abf846b7",
    "check_validation.sh": "4e68223d3a68e14c265fddb16b4c8578e6c2c9ddafec4b33fba96e18b5a43d58",
    "source-statement-crosswalk.md": "1285f26caed291fe88fce5ac6b59804b73dc829ffe9f66abe259017c21c5a92e",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/check_release.sh",
    f"Stage1_Instances/{THEOREM}/check_release_lean.sh",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = (
    "PASS release inputs: target, DAG, receipts, graph, source hashes, and decision agree",
    "PASS current narrow Lean evidence: compactness package elaborated at trust zero",
    "PASS stale validation detected: historical recipe is bound to a different base commit",
    "BLOCKED dependency/root/audit/release: validation unaccepted, minimax and assurance gates open",
    "verdict=blocked lifecycle=planned audit_complete=false theorem_complete=false",
)


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON key {key!r} in {path}")
            value[key] = item
        return value

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    expected_exit: int = 0,
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=600,
        check=False,
    )
    if result.returncode != expected_exit:
        raise RuntimeError(
            f"command exit {result.returncode}, expected {expected_exit}: {argv!r}\n"
            f"{result.stdout}"
        )
    return result.stdout


def command_records() -> list[dict]:
    return [
        {
            "argv": ["python3", "Docs/tools/check_stage1_standard.py"],
            "exit_code": 0,
            "classification": "pass",
        },
        {
            "argv": ["python3", "scripts/stage1_target.py", "check"],
            "exit_code": 0,
            "classification": "pass",
        },
        {
            "argv": ["python3", "scripts/stage1_target.py", "show", THEOREM],
            "exit_code": 0,
            "classification": "pass",
        },
        {
            "argv": ["bash", f"Stage1_Instances/{THEOREM}/check_proof.sh"],
            "exit_code": 0,
            "classification": "nonrelease_partial_pass",
        },
        {
            "argv": ["/usr/bin/bash", f"Stage1_Instances/{THEOREM}/check_validation.sh"],
            "exit_code": 1,
            "classification": "expected_blocker",
        },
        {
            "argv": ["/usr/bin/bash", f"Stage1_Instances/{THEOREM}/check_release.sh"],
            "exit_code": 0,
            "classification": "pass",
        },
        {
            "argv": [
                "python3",
                "-O",
                "-I",
                "-B",
                f"Stage1_Instances/{THEOREM}/check_release.py",
            ],
            "exit_code": 1,
            "classification": "expected_fail_closed_guard",
        },
        {
            "argv": [
                "python3",
                "-m",
                "json.tool",
                "<each release JSON and .stage1-worker-selftest.json>",
            ],
            "exit_code": 0,
            "classification": "pass",
        },
        {
            "argv": [
                "git",
                "diff",
                "--check",
                "--",
                f"Stage1_Instances/{THEOREM}",
                ".stage1-worker-selftest.json",
            ],
            "exit_code": 0,
            "classification": "pass",
        },
    ]


def git(*args: str) -> str:
    return run(["/usr/bin/git", *args]).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions (no -O/PYTHONOPTIMIZE)")
    if os.environ.get("STAGE1_NETWORK_DENIED") != "1":
        raise RuntimeError("release checker requires the network-denied wrapper")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    local_dag = load(HERE / "task-dag.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["decision_sha256"] == sha256(HERE / "release-decision.json")
    assert receipt["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["checker_sha256"] == sha256(HERE / "check_release.py")
    assert receipt["checker_wrapper_sha256"] == sha256(HERE / "check_release.sh")
    assert receipt["lean_replay_wrapper_sha256"] == sha256(
        HERE / "check_release_lean.sh"
    )
    assert receipt["public_projection_sha256"] == sha256(HERE / "release-validation.md")
    authority_inputs = receipt["authority_inputs"]
    for relative, expected in authority_inputs.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    patch_hashes = receipt["owned_untracked_patch_hashes"]
    for relative, expected in patch_hashes.items():
        if relative == "boundary":
            continue
        patch = run(
            ["/usr/bin/git", "diff", "--binary", "--no-index", "/dev/null", relative],
            expected_exit=1,
        )
        assert hashlib.sha256(patch.encode()).hexdigest() == expected, (
            f"untracked patch drifted: {relative}"
        )
    environment = receipt["environment"]
    assert os.environ["LANG"] == os.environ["LC_ALL"] == environment["locale"]
    assert os.environ["TZ"] == environment["timezone"]
    assert os.environ["LEAN_NUM_THREADS"] == environment["lean_num_threads"]
    runtime_paths = {
        "lean_executable_sha256": Path(os.environ["STAGE1_LEAN_BIN"]),
        "python_executable_sha256": Path(sys.executable),
        "git_executable_sha256": Path("/usr/bin/git"),
        "bash_executable_sha256": Path("/usr/bin/bash"),
        "bubblewrap_executable_sha256": Path("/usr/bin/bwrap"),
        "cp_executable_sha256": Path("/usr/bin/cp"),
        "mktemp_executable_sha256": Path("/usr/bin/mktemp"),
        "mkdir_executable_sha256": Path("/usr/bin/mkdir"),
        "sha256sum_executable_sha256": Path("/usr/bin/sha256sum"),
    }
    for key, expected in EXPECTED_RUNTIME_HASHES.items():
        assert environment[key] == expected
        assert sha256(runtime_paths[key]) == expected, f"runtime identity drifted: {key}"
    selected_dependency = receipt["selected_dependency_identity"]
    mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
    assert run(["/usr/bin/git", "rev-parse", "HEAD"], cwd=mathlib).strip() == (
        selected_dependency["mathlib_revision"]
    )
    assert run(["/usr/bin/git", "rev-parse", "HEAD^{tree}"], cwd=mathlib).strip() == (
        selected_dependency["mathlib_tree"]
    )
    assert run(["/usr/bin/git", "status", "--porcelain=v1"], cwd=mathlib) == ""
    selected_oleans = {
        "Mathlib.Analysis.Calculus.ContDiff.Basic_olean_sha256":
            mathlib / ".lake/build/lib/lean/Mathlib/Analysis/Calculus/ContDiff/Basic.olean",
        "Mathlib.Analysis.InnerProductSpace.l2Space_olean_sha256":
            mathlib / ".lake/build/lib/lean/Mathlib/Analysis/InnerProductSpace/l2Space.olean",
    }
    for key, path in selected_oleans.items():
        assert sha256(path) == selected_dependency[key], f"compiled import drifted: {key}"

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 165
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1272-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 165,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1272-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]"
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-1272-VALIDATION"]
    assert local_dag["accepted_states"] == []

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    assert decision["reconciled_inputs"] == {**EXPECTED_INPUTS, **EXPECTED_TOOL_INPUTS}

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
        EXPRESSION_SHA256
    )
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1272-ROOT"
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False
    assert boundary["root_machine_debt"] == "M3"
    assert boundary["theorem_complete"] is False
    assert boundary["first_open_cut_set"] == AUTHORITATIVE_CUT

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert anchor["audit_complete"] is True
    assert anchor["accepted_receipts"] == []
    assert anchor["gate_state"] == "self_tested_pending_master_acceptance"

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["provisionally_closed_obligation_ids"] == PARTIAL_IDS
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["open_root_cut_set"] == PROVISIONAL_CUT
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["accepted_closed_obligation_ids"] == []
    assert validation["locally_revalidated_provisional_obligation_ids"] == PARTIAL_IDS
    assert validation["result"]["root_closed"] is False
    assert validation["result"]["root_machine_debt"] == "M3"
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["remaining_root_cut_set"] == PROVISIONAL_CUT

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["execution_rank"] == 165 and decision["intent"] == "release"
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]"
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["recorded_base_revision"] == VALIDATION_BASE
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    assert decision["accepted_receipt_ids"] == []
    assert decision["provisional_receipt_ids_inspected"] == [
        proof["receipt_id"],
        validation["receipt_id"],
    ]

    accepted = decision["authoritative_boundary"]
    vector = {"H": "H2", "M": "M3", "R": "R4"}
    assert accepted["root_vector_before"] == accepted["root_vector_after"] == vector
    assert accepted["accepted_closed_obligation_ids"] == []
    assert accepted["typed_graph_root_closed"] is False
    assert accepted["typed_graph_first_open_cut_set"] == AUTHORITATIVE_CUT
    provisional = decision["best_provisional_evidence"]
    assert provisional["root_vector"] == vector
    assert provisional["kernel_replayed_obligation_ids"] == PARTIAL_IDS
    assert provisional["open_root_cut_set"] == PROVISIONAL_CUT
    assert provisional["observed_axioms"] == EXPECTED_AXIOMS

    outcome = decision["decision"]
    assert outcome["verdict"] == "blocked"
    assert outcome["lifecycle_before"] == outcome["lifecycle_after"] == "planned"
    assert outcome["root_vector_before"] == outcome["root_vector_after"] == vector
    assert outcome["audit_complete"] is outcome["theorem_complete"] is False
    assert outcome["audit_z"] == outcome["theorem_z"] == "blocked"
    assert outcome["release_accepted"] is False
    assert outcome["first_failed_gate"]["gate_id"] == (
        "S56-10.2-DEPENDENCY-ACCEPTANCE"
    )
    assert outcome["first_failed_gate"]["dependency_gate"] == (
        "dependency.S56-M-1272-VALIDATION.master_acceptance"
    )
    assert outcome["first_failed_theorem_gate"]["gate_id"] == (
        "M1272-T-LOWER-BOUND.kernel_closure"
    )
    assert outcome["first_failed_release_protocol_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert outcome["remaining_root_cut_set"] == PROVISIONAL_CUT
    release_cut = "\n".join(outcome["remaining_release_cut_set"])
    for fragment in (
        "S56-M-1272-VALIDATION",
        "FountainMinimaxPackage",
        "H0 primary-source",
        "R0 node-anchored",
        "AUDIT-Z",
        "empty-cache network-denied cold build",
        "two signed attestations",
        "minimal release verifier",
        "deterministic build-twice evidence bundle",
    ):
        assert fragment in release_cut, fragment

    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "/usr/bin/bash",
        f"Stage1_Instances/{THEOREM}/check_release.sh",
    ]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
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
    ):
        assert receipt["recipe"][key] == spec[key], key

    assert receipt["depends_on"] == ["S56-M-1272-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["verdict"] == "blocked"
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["kernel_replayed_obligation_ids"] == PARTIAL_IDS
    assert receipt["accepted_receipt_ids"] == []
    receipt_id_basis = {
        "item_id": ITEM,
        "base_revision": BASE_REVISION,
        "verdict": "blocked",
        "release_spec_sha256": receipt["release_spec_sha256"],
        "checker_sha256": receipt["checker_sha256"],
        "checker_wrapper_sha256": receipt["checker_wrapper_sha256"],
        "lean_replay_wrapper_sha256": receipt["lean_replay_wrapper_sha256"],
        "public_projection_sha256": receipt["public_projection_sha256"],
        "dependency_receipt_sha256": dependency["receipt_sha256"],
        "canonical_statement_fingerprint": receipt["canonical_statement_fingerprint"],
    }
    receipt_id_digest = hashlib.sha256(
        json.dumps(receipt_id_basis, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert receipt["receipt_id"] == f"{ITEM}-BLOCKED-{receipt_id_digest[:16]}"
    result = receipt["result"]
    assert result["verdict"] == "blocked"
    assert result["root_vector_before"] == result["root_vector_after"] == vector
    assert result["observed_axioms"] == EXPECTED_AXIOMS
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["release_accepted"] is False
    assert result["authoritative_typed_graph_cut_set"] == AUTHORITATIVE_CUT
    assert result["provisional_post_proof_root_cut_set"] == PROVISIONAL_CUT
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["changed_paths"] == decision["changed_paths"]
    receipt_commands = receipt["commands_and_results"]
    expected_commands = command_records()
    assert len(receipt_commands) == len(expected_commands)
    for actual, expected in zip(receipt_commands, expected_commands, strict=True):
        for key, value in expected.items():
            assert actual[key] == value, (key, actual, expected)

    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "accepted_exact_root_kernel_closure",
        "authoritative_graph_reconciled",
        "authoritative_h_debt_reconciled",
        "local_task_dag_reconciled",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "accepted_foundation_and_complete_transitive_provenance_tcb",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_mutation_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["current_validation_recipe_status"] == (
        "fail_closed_stale_base_revision"
    )
    debt_conflict = decision["debt_classification_conflict"]
    assert debt_conflict["accepted_projection_preserved"] == "H2"
    assert debt_conflict["evidence_supported_upper_bound"] == "H1"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        assert prohibited.search(without_comments((HERE / name).read_text(encoding="utf-8"))) is None

    proof_output = run(["/usr/bin/bash", str(HERE / "check_release_lean.sh")])
    for fragment in (
        "PASS THM-M-1272 release Lean replay: compactness package closed",
        "symmetric minimax package remains explicit and open",
        "'Stage1Instances.THM_M_1272.fountainLimitPackage_proof' depends on axioms: "
        "[propext, Classical.choice, Quot.sound]",
        "'Stage1Instances.THM_M_1272.fountainTheoremTarget_of_minimax' depends on axioms: "
        "[propext, Classical.choice, Quot.sound]",
    ):
        assert fragment in proof_output, fragment

    assert validation["repository_state"]["commit"] == VALIDATION_BASE
    assert validation["repository_state"]["commit"] != BASE_REVISION
    assert validation["base_tree"] != BASE_TREE
    validation_checker = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert 'receipt["repository_state"]["commit"] == git("rev-parse", "HEAD")' in (
        validation_checker
    )

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
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    packet_commands = packet["commands"]
    assert len(packet_commands) == len(expected_commands)
    for actual, expected in zip(packet_commands, expected_commands, strict=True):
        assert actual["argv"] == expected["argv"], (actual, expected)
        assert actual["exit_code"] == expected["exit_code"], (actual, expected)
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`",
        "`[H2, M3, R4]`",
        "`AUDIT-Z`",
        "`THEOREM-Z`",
        "This worker accepts\nno receipt",
        "accepted=false",
        "release_grade=false",
    ):
        assert fragment in handoff, fragment
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
