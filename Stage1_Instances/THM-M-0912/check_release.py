#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0912-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0912"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0912-RELEASE"
THEOREM = "THM-M-0912"
BASE_REVISION = "be4282f0548d68633fface1489942950fd0b9c4d"
BASE_TREE = "60074bc0f2f6f496e4668123ef22b34c6a01917f"
EXPRESSION_SHA256 = "b322549a05e57fbf466b60eb8ff89f4a08c6ee3b68ea5bf3ff3bf86d99521776"
DENOMINATOR_SHA256 = "c66f1840e6d1bcc7b0a64f7ecdc24ee2f13adc10098ca8467cd238c649f7432b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext"}
EXPECTED_INPUTS = {
    "Statement.lean": "63fda2462d33fba5f18ba0c46df33d7c34c2442609992e7435a2ab4ac33e434e",
    "statement.json": "6156f7f6c281342bbd85a18d5de37235c9da47e9ce0ad537c7d3d614f75da2e2",
    "anchor-audit.json": "953d035b5abfc58c6236667e8f04aa03e7d27a30e492897bfb2d8df33e2c3fd1",
    "obligation-registry.json": "00f2f0d24e2d940d07b6626bd29d077ec52fb044eea58519290c32fdc27d2566",
    "typed-graphs.json": "32f0d888d2bb01bd2113c8d954b969f654803897f544eb5f099a2fffdf649f12",
    "ObligationTree.lean": "c880f3d4738a4ca182e939f52356ff8ad4b2f6d23468ebc4193e74ed0602ff2e",
    "Proof.lean": "43b7e98283100cd708a6743ceea7e4f617f94cc04740f344fc75afdce07be138",
    "proof-receipt.json": "df78d7f49702a181c4df36ee73ef4746954258633c409b59dfbd6adc77173f9d",
    "Validation.lean": "9b7331721030afb1a1fe2c02bbb0c98b4d3bd340c2c6c74f192592784d10d3a2",
    "validation-phase-spec.json": "43f23cc67ac54e2934053233b6860e763e196be7e8eb34fcd899e113e9394c5d",
    "validation-receipt.json": "c225f1cb0b0f8e0337d2c41884a8e5ac2cfd151bb935d91be00065f864404695",
    "instance.json": "7304e32d6ff33a017da19bd747ff6ad749693148b1275db86e86e9a7e2630307",
    "task-dag.json": "4d9cb30b152363c0478d967b263ce4236020d1eda6e12f13ad8b5677d0ba1e38",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_axioms(output: str, declaration: str) -> None:
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, (declaration, output)
    observed = {part.strip() for part in match.group(1).split(",")}
    assert observed == EXPECTED_AXIOMS, (declaration, observed)


def replay_lean() -> None:
    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in version and LEAN_COMMIT in version
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT
    ).strip()
    base_env = os.environ.copy()
    base_env.update(
        {
            "LANG": "C",
            "LC_ALL": "C",
            "TZ": "UTC",
            "NO_COLOR": "1",
            "LEAN_PATH": lean_path,
        }
    )
    with tempfile.TemporaryDirectory(prefix="m0912-release-") as tmp_name:
        tmp = Path(tmp_name)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        run([lean, "-o", "Statement.olean", "Statement.lean"], cwd=tmp, env=base_env)
        module_env = base_env.copy()
        module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        run(
            [lean, "-o", "ObligationTree.olean", "ObligationTree.lean"],
            cwd=tmp,
            env=module_env,
        )
        proof_output = run([lean, "Proof.lean"], cwd=tmp, env=module_env)
        validation_output = run([lean, "Validation.lean"], cwd=tmp, env=module_env)

    proof_declarations = (
        "Nat.choose_succ_right",
        "Nat.choose_eq_choose_pred_add",
        "Stage1Instances.THM_M_0912.Proof.positiveColumnReindex_proof",
        "Stage1Instances.THM_M_0912.Proof.chooseSuccRight_proof",
        "Stage1Instances.THM_M_0912.Proof.predecessorRecurrence_from_frozen_children",
        "Stage1Instances.THM_M_0912.Proof.predecessorRecurrence_pinned",
        "Stage1Instances.THM_M_0912.Proof.root_via_pinned_composition",
        "Stage1Instances.THM_M_0912.Proof.root_via_frozen_children",
        "Stage1Instances.THM_M_0912.Proof.pascalIdentityTarget_proof",
        "Stage1Instances.THM_M_0912.Proof.pascalIdentityTarget_via_frozen_children",
    )
    validation_declarations = (
        "Nat.choose_eq_choose_pred_add",
        "Stage1Instances.THM_M_0912.Validation.pascalIdentityTarget_independent_local",
    )
    for declaration in proof_declarations:
        assert_axioms(proof_output, declaration)
    for declaration in validation_declarations:
        assert_axioms(validation_output, declaration)
    assert proof_output.count("Declarations are sorry-free!") == 10
    assert validation_output.count("Declarations are sorry-free!") == 2
    assert "sorryAx" not in proof_output + validation_output


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    instance = load(HERE / "instance.json")
    graphs = load(HERE / "typed-graphs.json")
    local_dag = load(HERE / "task-dag.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1454
    assert target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    assert target["baseline"] == "L0" and target["rework_required"] is True

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0912-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1454,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0912-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]"
    assert validation_item["attempts"] == 1
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in local_dag["tasks"] if row["id"] == "S56-M-0912-VALIDATION"
    )
    assert local_release["state"] == local_validation["state"] == "open"
    assert local_dag["accepted_states"] == []

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0912-ROOT"

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["intent"] == "release"
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["release_grade"] is False
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0912-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    assert decision["provisional_receipt_ids_inspected"] == [
        proof["receipt_id"],
        validation["receipt_id"],
    ]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-B", str(HERE.relative_to(ROOT) / "check_release.py")]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 180 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_id"] == "S56-M-0912-RELEASE-local-20260714T003501+0800"
    assert receipt["depends_on"] == ["S56-M-0912-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["release_grade"] is receipt["master_accepted"] is False
    assert receipt["dependency_receipt"] == dependency
    for key in (
        "recipe_id",
        "cwd",
        "argv",
        "env_allowlist",
        "timeout_seconds",
        "network_policy",
        "expected_exit",
        "covered_obligation_ids",
        "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key]

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H1", "M3", "R4"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    receipt_result = receipt["result"]
    assert receipt_result["exit_code"] == 0
    assert receipt_result["verdict"] == "blocked"
    assert receipt_result["lifecycle_before"] == receipt_result["lifecycle_after"] == "planned"
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == ["H1", "M3", "R4"]
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["accepted_receipt_ids"] == []
    assert receipt_result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt_result["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["changed_paths"] == decision["changed_paths"]
    assert "not release-grade evidence" in receipt["status_boundary"]
    assert "does not claim E1" in decision["status_boundary"]

    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "accepted_exact_root_kernel_closure",
        "authoritative_graph_reconciled",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["accepted_closed_obligations"] == []
    assert reconciliation["observed_axioms"] == ["propext"]

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False
    assert boundary["root_machine_debt"] == "M3"
    assert boundary["accepted_closed_obligations"] == []
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["remaining_root_cut_set"] == [
        "M0912-T-PREDECESSOR-COMPOSE",
        "M0912-X-SOURCE",
        "M0912-S-FOUNDATION",
        "M0912-X-PROVENANCE",
        "M0912-X-TRUST",
        "M0912-X-READABLE",
        "M0912-X-WORKFLOW",
    ]

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    validation_result = validation["result"]
    assert validation["accepted"] is False and validation["content_addressed"] is False
    assert validation_result["root_kernel_closed"] is True
    assert validation_result["accepted_root_closed"] is False
    assert validation_result["structured_state_freshness"].startswith("fail_closed:")
    assert validation_result["transitive_provenance_and_trust"] == "fail_closed"
    assert validation_result["hermetic_release_gate"] == "fail_closed"
    assert validation_result["independent_distinct_runner_gate"] == "fail_closed"
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False

    cut_set = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "master acceptance",
        "graph and debt reconciliation",
        "AUDIT-Z",
        "H0 primary-source",
        "R0 structured reconstruction",
        "transitive declaration",
        "empty-cache network-denied cold build",
        "SBOM",
        "two signed attestations",
        "minimal release verifier",
        "deterministic content-addressed release bundle",
    ):
        assert fragment in cut_set, fragment

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain", cwd=MATHLIB) == ""
    replay_lean()

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
    assert set(packet["changed_paths"]) == set(decision["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"]
    status = run(["git", "status", "--short", "--untracked-files=all"])
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    normalized_handoff = " ".join(handoff.split())
    for fragment in (
        "`blocked`",
        "`[H1, M3, R4]`",
        "`AUDIT-Z`",
        "`THEOREM-Z`",
        "release_grade=false",
        "This worker accepts no receipt",
    ):
        assert fragment in normalized_handoff, fragment
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS release inputs: target, DAG dependency, receipts, graph, and hashes agree")
    print("PASS current Lean replay: exact root and differential wrapper are sorry-free; axioms [propext]")
    print("PASS fail-closed state: lifecycle planned; accepted root H1/M3/R4; accepted receipts 0")
    print("BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted")
    print("BLOCKED S56-10.6-HERMETIC-COLD-BUILD and independent release gates")
    print("verdict=blocked audit_complete=false theorem_complete=false")


if __name__ == "__main__":
    main()
