#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0843-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0843"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0843-RELEASE"
THEOREM = "THM-M-0843"
BASE_REVISION = "936bf2b9e968abd3b79b5b36d32f2f2bff648c7e"
BASE_TREE = "8c9d3261b0ba9a81deb5bfc19a335a02cb80f962"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "6afd11f23d5245eaa4c487ad4484249b517f6fcf4f99373a2f437d5307aee9ec",
    "ObligationTree.lean": "59b179eeb8b7cdc9f96f131fd52c50e51a4400f7c50625acd9af7e0277ebf417",
    "Proof.lean": "03d47b0be61e4e75cbcd4320ad413a98e5014abbd592c5998172cc28e73c8229",
    "Validation.lean": "47aa8748007d0b5853f805b8d3a584cb0593270ab164331a9ac0bda99c896eba",
    "statement.json": "81d3759ec2f92c9e2f78fe5ff7d961a00aaf22bc8b75248fe8cfdfc42d849720",
    "anchor-audit.json": "8c581b2d671b928481cd73876bf71c3ea0a3b4f1a06c2021946401741f814d20",
    "obligation-registry.json": "43ff3a49c316a51636a9972ef62ee9d37101b5d8e88ca4e68e42cb12b16bb2ce",
    "typed-graphs.json": "ca4d7c16e81e5e0dc4fd84f7a99ae03fae7426523b0c45ee4dabb07d4cb384de",
    "proof-receipt.json": "4b1a91cca81d2b7abaa266247a3ae431d5b86b0082af34d9b846b6fe4de2db22",
    "validation-spec.json": "bdee88fbd87aeca4c123ec63aadc03a60bd64f5a8da50226951b3b205cd6c8bc",
    "validation-receipt.json": "cf22b85ce9dceb9d340cea34faf6547e36648be9e1cde40ad447afbbf5d2c0f3",
    "instance.json": "2422f3b62f8137f4dd365fdaf359ac31c72dd15660e1378385998913dbad942f",
    "task-dag.json": "455f1803842b82c195209554e4c1e690ddc9ab7ffbaa2b27beee015854bbb238",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/README.md",
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
        {"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC", "LEAN_PATH": lean_path}
    )
    with tempfile.TemporaryDirectory(prefix="m0843-release-") as tmp_name:
        tmp = Path(tmp_name)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        run(
            [lean, "-o", "Statement.olean", "Statement.lean"],
            cwd=tmp,
            env=base_env,
        )
        module_env = base_env.copy()
        module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        obligation_output = run(
            [lean, "-o", "ObligationTree.olean", "ObligationTree.lean"],
            cwd=tmp,
            env=module_env,
        )
        proof_output = run(
            [lean, "Proof.lean"], cwd=tmp, env=module_env
        )
        validation_output = run(
            [lean, "Validation.lean"], cwd=tmp, env=module_env
        )

    assert_axioms(obligation_output, "szemeredi_regularity")
    assert_axioms(
        obligation_output,
        "Stage1Instances.THM_M_0843_Obligations.terminal_adapter",
    )
    assert_axioms(
        obligation_output,
        "Stage1Instances.THM_M_0843_Obligations.compose_root",
    )
    for declaration in (
        "szemeredi_regularity",
        "Stage1Instances.THM_M_0843.Proof.pinnedTerminal",
        "Stage1Instances.THM_M_0843.Proof.szemerediRegularity_via_frozen_composition",
        "Stage1Instances.THM_M_0843.Proof.szemerediRegularity",
    ):
        assert_axioms(proof_output, declaration)
    assert_axioms(validation_output, "szemeredi_regularity")
    assert_axioms(
        validation_output,
        "Stage1Instances.THM_M_0843.Validation.differentialSzemerediRegularity",
    )
    assert proof_output.count("Declarations are sorry-free!") >= 4
    assert validation_output.count("Declarations are sorry-free!") >= 2


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    graphs = load(HERE / "typed-graphs.json")
    local_dag = load(HERE / "task-dag.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1032
    assert target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    assert target["baseline"] == "L0" and target["rework_required"] is True

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0843-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1032,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0843-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]"
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["intent"] == "release"
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0843-VALIDATION"
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
    assert receipt["receipt_id"] == "S56-M-0843-RELEASE-local-20260712T222201Z"
    assert receipt["depends_on"] == ["S56-M-0843-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["release_grade"] is receipt["master_accepted"] is False
    for name, expected in receipt["inputs"].items():
        path = ROOT / name if name.startswith(".") or name.startswith("Stage1_") else LEAN_ROOT / name
        assert sha256(path) == expected, f"release receipt input drifted: {name}"
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
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["unverified_internal_composition_count"] == 18
    assert reconciliation["accepted_closed_obligations"] == []
    assert reconciliation["historical_validation_recipe_replay"] == (
        "not_currently_replayable_outside_its_original_worker_packet_and_base_revision"
    )

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False
    assert boundary["accepted_root_machine_debt"] == "M3"
    assert boundary["closed_obligations"] == []
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["result"]["accepted_state_changed"] is False
    validation_result = validation["result"]
    assert validation_result["exact_root_kernel_closed"] is True
    assert validation_result["accepted_root_machine_debt"] == "M3"
    assert validation_result["accepted_closed_obligations"] == []
    assert validation_result["unverified_internal_composition_count"] == 18
    assert validation_result["hermetic_release_gate"] == "fail_closed"
    assert validation_result["independent_distinct_runner_gate"] == "fail_closed"
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False

    cut_set = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "18 unverified internal",
        "H0 primary-source",
        "R0 structured reconstruction",
        "empty-cache network-denied cold build",
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
    status = run(["git", "status", "--short", "--untracked-files=all"])
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    readme = (HERE / "README.md").read_text(encoding="utf-8")
    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for public in (readme, handoff):
        for fragment in (
            "`blocked`",
            "`[H1, M3, R4]`",
            "`AUDIT-Z`",
            "`THEOREM-Z`",
        ):
            assert fragment in public, fragment
    assert "advances no lifecycle, debt, receipt, or theorem-completion state" in readme
    assert "This worker accepts no receipt" in handoff
    assert "release_grade=false" in handoff

    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS release inputs: target, DAG dependency, receipts, graph, and hashes agree")
    print("PASS current Lean replay: exact root wrappers are sorry-free with the recorded axiom set")
    print("PASS fail-closed state: lifecycle planned; accepted root H1/M3/R4; accepted receipts 0")
    print("BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted")
    print("BLOCKED S56-10.6-HERMETIC-COLD-BUILD and independent release gates")
    print("verdict=blocked audit_complete=false theorem_complete=false")


if __name__ == "__main__":
    main()
