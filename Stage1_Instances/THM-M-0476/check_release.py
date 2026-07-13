#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0476-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0476"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0476-RELEASE"
THEOREM = "THM-M-0476"
BASE_REVISION = "309f58b7a54d36653b3483a543c6378eea53882c"
BASE_TREE = "1051ab77fe56d6e32ba26761bbcfd3ad8a258743"
EXPRESSION_SHA256 = "ee76edb160426d3e8d95b11bfedca7febcfe915f50007e042875c922ebc8a4ac"
DENOMINATOR_SHA256 = "9375f9b987132465572c04a019d70b32638823c1279dd91a7935007f108fe62b"
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
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
VALIDATION_OUTPUT_SHA256 = "06d60bc8482b2b2026ce5900c765fe635fd8ed3b836af7003675e2159ef73699"
WILSON_SOURCE_SHA256 = "7bd6ec0e909f037f8632e1b495f9647a61fe950f3bfe3af98a5a22914622aeb7"
WILSON_OLEAN_SHA256 = "c932050e2dca74d0ba033d36338122b2927bad7800f2ac592a20daf42c91d9eb"
FINITE_SOURCE_SHA256 = "808bb4eddb8a4b48785e4430f944fe0827c96842dffa0c08cd21b5659bd85d44"
FINITE_OLEAN_SHA256 = "4cede73b3c7f85692307990d9cdaf819b5ac61dc50272e31586b7899d9f32119"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M0476-ROOT",
    "M0476-S-INTERFACE",
    "M0476-S-BOUNDARY",
    "M0476-S-FACT-TRANSPORT",
    "M0476-S-FOUNDATION",
    "M0476-T-COMPOSE",
    "M0476-L-WILSON",
    "M0476-N-FACTORIAL-PRODUCT",
    "M0476-L-FACTORIAL-INTERVAL",
    "M0476-T-NAT-CAST-PRODUCT",
    "M0476-N-PRIME-ENDPOINT",
    "M0476-C-RESIDUE-UNITS-BIJECTION",
    "M0476-B-UNIT-VAL-RANGE",
    "M0476-L-UNIT-VAL-INJECTIVE",
    "M0476-C-RESIDUE-TO-UNIT",
    "M0476-T-REPRESENTATIVE-COE",
    "M0476-L-UNITS-PRODUCT",
    "M0476-C-INVERSE-PAIRING",
    "M0476-L-INVERSE-FIXED-POINTS",
    "M0476-T-INSERT-NEGONE",
    "M0476-T-UNITS-COE-NEGONE",
    "M0476-X-SOURCE",
    "M0476-X-PROVENANCE",
    "M0476-X-TRUST",
    "M0476-X-READABLE",
    "M0476-X-WORKFLOW",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}
SUMMARY_LINES = [
    "release-authority: PASS (rank 1357; validation [_] and unaccepted; release [ ])",
    "release-evidence: PASS (exact target, frozen graph, receipts, pins, and hashes reconciled)",
    "release-lean: PASS (25 sorry-free reports; exact roots use allowed axioms only)",
    "AUDIT-Z: BLOCKED (accepted H0/R0, classification reconciliation, and release bundle absent)",
    "THEOREM-Z: BLOCKED (accepted M0-W/E1, trust, cold replay, and independence absent)",
    "release-verdict: blocked at S56-10.2-DEPENDENCY-ACCEPTANCE",
    "release-boundary: planned H1/M3/R4 unchanged; accepted receipts 0; theorem_complete=false",
]


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
    if f"'{declaration}' does not depend on any axioms" in output:
        return set()
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        flags=re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def check_authority(receipt: dict) -> None:
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1357
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release = next(row for row in execution["items"] if row["id"] == ITEM)
    validation = next(
        row for row in execution["items"] if row["id"] == "S56-M-0476-VALIDATION"
    )
    assert release == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1357,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0476-VALIDATION"],
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
    assert dag["accepted_states"] == []
    local_release = next(row for row in dag["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in dag["tasks"] if row["id"] == "S56-M-0476-VALIDATION"
    )
    assert local_release["state"] == local_validation["state"] == "open"
    assert receipt["authority_inputs"] == {
        "Docs/Stage1_Targets_rev-5.6.json": sha256(
            ROOT / "Docs/Stage1_Targets_rev-5.6.json"
        ),
        "Docs/Stage1_Execution_DAG_rev-5.6.json": sha256(
            ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json"
        ),
        f"Stage1_Instances/{THEOREM}/instance.json": sha256(HERE / "instance.json"),
        f"Stage1_Instances/{THEOREM}/task-dag.json": sha256(HERE / "task-dag.json"),
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
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    assert decision["phase"] == receipt["phase"] == "release"
    assert decision["intent"] == receipt["intent"] == "release"
    assert decision["execution_rank"] == receipt["execution_rank"] == 1357
    assert decision["decision_support"] == receipt["support_state"] == (
        "provisional_worker_selftest"
    )
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["normative_profile"] == receipt["normative_profile"] == (
        "machine-theorem-assurance/1.0"
    )
    assert decision["content_addressed"] is receipt["content_addressed"] is False
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert decision["decided_at"] == receipt["validated_at"] == "2026-07-14T01:37:18+08:00"
    assert decision["attestor"] == receipt["attestor"] == "stage1-rev56-worker-slot11"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["accepted"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["master_acceptance"] == "pending_and_not_claimed"
    assert receipt["accepted_receipt_ids"] == decision["accepted_receipt_ids"] == []
    for relative, expected in decision["reconciled_inputs"].items():
        assert sha256(ROOT / relative) == expected, f"reconciled input drifted: {relative}"

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0476-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["proposed_state"] == validation["proposed_state"] == "[_]"
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["content_addressed_release_evidence"] is (
        validation["content_addressed_release_evidence"]
    ) is False
    assert dependency["master_accepted"] is False
    predecessor = receipt["predecessor_inputs"]
    assert predecessor["proof_receipt_id"] == proof["receipt_id"]
    assert predecessor["proof_receipt_sha256"] == sha256(HERE / "proof-receipt.json")
    assert predecessor["validation_receipt_id"] == validation["receipt_id"]
    assert predecessor["validation_receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert predecessor["historical_validation_checker_sha256"] == sha256(
        HERE / "check_validation.py"
    )
    assert predecessor["historical_validation_checker_fresh_for_release"] is False
    assert proof["accepted"] is False and proof["proposed_state"] == "[_]"
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert validation["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert validation["result"]["accepted_root_machine_debt"] == "M3"
    assert validation["result"]["accepted_root_closed"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0476-ROOT"
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False and boundary["root_machine_debt"] == "M3"
    assert boundary["accepted_closed_obligations"] == []
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert decision["canonical_target_expression_sha256"] == (
        receipt["canonical_target_expression_sha256"]
    ) == EXPRESSION_SHA256
    assert decision["registry_denominator_sha256"] == (
        receipt["registry_denominator_sha256"]
    ) == DENOMINATOR_SHA256
    assert spec["decision_covered_obligation_ids"] == INVENTORY_IDS
    assert receipt["decision_covered_obligation_ids"] == INVENTORY_IDS

    result = decision["decision"]
    assert result["verdict"] == receipt["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == [
        "H1", "M3", "R4"
    ]
    assert result["best_provisional_vector"] == ["H1", "M0-W", "R4"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    receipt_result = receipt["result"]
    assert receipt_result["verdict"] == "blocked"
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == [
        "H1", "M3", "R4"
    ]
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["accepted_receipt_ids"] == []
    assert receipt_result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt_result["next_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": hashlib.sha256(
            ("\n".join(SUMMARY_LINES) + "\n").encode("utf-8")
        ).hexdigest(),
        "expected_line_count": len(SUMMARY_LINES),
        "exit_code": 0,
    }
    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "accepted_exact_root_kernel_closure",
        "authoritative_graph_reconciled",
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
        "audit_z_accepted",
        "theorem_z_accepted",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["accepted_closed_obligations"] == []
    assert decision["known_failures"] == receipt["known_failures"]
    assert result["remaining_root_cut_set"] == receipt["remaining_root_cut_set"]
    assert decision["retry_condition"] == receipt["retry_condition"]
    for boundary in (decision["status_boundary"], receipt["status_boundary"]):
        for fragment in (
            "Self-tested negative release reconciliation only",
            "accepts no receipt",
            "AUDIT-Z",
            "THEOREM-Z",
            "theorem completion",
            "master acceptance",
        ):
            assert fragment in boundary, fragment

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["recipe_id"] == receipt["recipe"]["recipe_id"] == (
        "S56-M-0476-RELEASE-local-v1"
    )
    for key in (
        "cwd", "argv", "env_allowlist", "timeout_seconds", "network_policy",
        "network_enforcement", "expected_exit", "expected_outputs",
    ):
        assert receipt["recipe"][key] == spec[key], key
    assert spec["covered_declarations"] == receipt["kernel_replayed_declarations"]


def check_environment(receipt: dict) -> None:
    environment = receipt["environment"]
    assert environment["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256
    assert sha256(MATHLIB / "Mathlib/NumberTheory/Wilson.lean") == WILSON_SOURCE_SHA256
    assert sha256(
        MATHLIB / ".lake/build/lib/lean/Mathlib/NumberTheory/Wilson.olean"
    ) == WILSON_OLEAN_SHA256
    assert sha256(MATHLIB / "Mathlib/FieldTheory/Finite/Basic.lean") == FINITE_SOURCE_SHA256
    assert sha256(
        MATHLIB / ".lake/build/lib/lean/Mathlib/FieldTheory/Finite/Basic.olean"
    ) == FINITE_OLEAN_SHA256

    lean = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
    lake = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lake"
    python = Path(os.path.realpath(os.sys.executable))
    git_path = shutil.which("git")
    bwrap = shutil.which("bwrap")
    assert git_path is not None and bwrap is not None
    assert sha256(lean) == environment["lean_executable_sha256"] == LEAN_SHA256
    assert sha256(lake) == environment["lake_executable_sha256"] == LAKE_SHA256
    assert sha256(python) == environment["python_executable_sha256"] == PYTHON_SHA256
    assert sha256(Path(os.path.realpath(git_path))) == environment["git_executable_sha256"] == (
        GIT_SHA256
    )
    assert sha256(Path(os.path.realpath(bwrap))) == (
        environment["bubblewrap_executable_sha256"]
    ) == BWRAP_SHA256
    assert environment["lean_toolchain_sha256"] == TOOLCHAIN_SHA256
    assert environment["lake_manifest_sha256"] == MANIFEST_SHA256
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_remote"] == MATHLIB_REMOTE
    assert environment["mathlib_license_sha256"] == LICENSE_SHA256
    version = run([str(lean), "--version"])
    assert "4.29.0" in version and LEAN_COMMIT in version


def check_lean(receipt: dict) -> None:
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        flags=re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    for source in (
        MATHLIB / "Mathlib/NumberTheory/Wilson.lean",
        MATHLIB / "Mathlib/FieldTheory/Finite/Basic.lean",
    ):
        assert prohibited.search(code_without_comments(source.read_text(encoding="utf-8"))) is None

    recipe_env = os.environ.copy()
    recipe_env.update(receipt["recipe"]["env_allowlist"])
    output = run(["bash", str(HERE / "check_validation.sh")], env=recipe_env)
    assert hashlib.sha256(output.encode("utf-8")).hexdigest() == VALIDATION_OUTPUT_SHA256
    assert len(output.encode("utf-8")) == 10563
    assert output.count("Declarations are sorry-free!") == 25
    assert "sorryAx" not in output and "declaration uses 'sorry'" not in output
    proof_declarations = (
        "Stage1Instances.THM_M_0476.Proof.wilsonTheorem",
        "Stage1Instances.THM_M_0476.Proof.wilsonTheorem_via_frozen_composition",
    )
    differential = (
        "Stage1Instances.THM_M_0476.Validation.wilsonTheorem_via_primeCharacterization"
    )
    for declaration in proof_declarations + (differential,):
        assert observed_axioms(output, declaration) == EXPECTED_AXIOMS, declaration
    assert receipt["result"]["observed_axioms"] == sorted(EXPECTED_AXIOMS)
    assert receipt["result"]["sorry_free_reports"] == 25


def check_packet(packet_path: Path, receipt: dict, decision: dict) -> None:
    packet = load(packet_path)
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path, required=True)
    args = parser.parse_args()
    receipt = load(HERE / "release-receipt.json")
    decision = load(HERE / "release-decision.json")
    spec = load(HERE / "release-spec.json")
    check_authority(receipt)
    check_reconciliation(receipt, decision, spec)
    check_environment(receipt)
    check_lean(receipt)
    check_packet(ROOT / args.worker_packet, receipt, decision)
    handoff = (HERE / "release-phase.md").read_text(encoding="utf-8")
    for fragment in (
        "**blocked**", "`[H1, M3, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "This worker accepts\nno receipt", "not theorem completion",
    ):
        assert fragment in handoff, fragment
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
