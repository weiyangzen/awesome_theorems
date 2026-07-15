#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1271-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1271"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1271-RELEASE"
THEOREM = "THM-M-1271"
BASE_REVISION = "7348dc646fd6babfe2b82c35b4c03a9ed5921f8e"
BASE_TREE = "ddd6941316b5d4a9d6574d9532212c24de6fe516"
VALIDATION_BASE = "557b928b377b386864527c9fb4831d45857837aa"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "686a7f777a77c3f91504e4c48cd3d0fab19ef802ce3df1751dc4288e62592d7b"
DENOMINATOR_SHA256 = "2f6d1a3dc9064aff967ba0cf8443ff438e9cb99e0b2d34994252e6410d2d75bc"
VALIDATION_RECEIPT_SHA256 = "51981c0d81f18ec44797151e8f9f8c776f50d29b8df21ea8bb7d9444a6d8a41c"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M1271-ROOT",
    "M1271-S-DEFINITIONS",
    "M1271-S-FOUNDATION",
    "M1271-C-PATH-MAX",
    "M1271-L-SPHERE-CROSSING",
    "M1271-T-BARRIER",
    "M1271-C-PS-SEQUENCE",
    "M1271-L-PS-COMPACT",
    "M1271-L-LIMIT-PASSAGE",
    "M1271-T-CRITICAL",
    "M1271-T-ASSEMBLE",
    "M1271-X-SOURCE",
    "M1271-X-PROVENANCE",
]
PROVISIONAL_IDS = [
    "M1271-C-PATH-MAX",
    "M1271-L-SPHERE-CROSSING",
    "M1271-T-BARRIER",
    "M1271-L-PS-COMPACT",
    "M1271-L-LIMIT-PASSAGE",
    "M1271-T-ASSEMBLE",
]
ROOT_CUT = ["M1271-C-PS-SEQUENCE", "M1271-T-CRITICAL", "M1271-ROOT"]
LEAN_MODULES = (
    "Statement.lean",
    "ObligationTree.lean",
    "Proof.lean",
    "AnchorAudit.lean",
    "Validation.lean",
)
AXIOM_DECLARATIONS = {
    "ObligationTree.lean": ("root_of_barrier_and_critical_packages",),
    "Proof.lean": (
        "admissiblePath_meets_sphere",
        "alpha_le_pathHeight",
        "pathHeight_attained",
        "mountainPassBarrierPackage",
        "exists_valueSequence_at_mountainPassLevel",
        "exists_criticalPoint_of_psSequence",
        "mountainPassCriticalPackage_of_psSequence",
    ),
    "Validation.lean": (
        "directAdmissiblePath_meets_sphere",
        "directAlpha_le_pathHeight",
        "directAlpha_le_mountainPassLevel",
        "directConditionalRoot",
    ),
}
EXPECTED_LEAN_OUTPUTS = {
    "Statement.lean": "bba8a90b894307a541074c63ab2c929201d66faefc0154b80760b20f8f7becaa",
    "ObligationTree.lean": "85f371a6e40720abe1c326aea759ebbd91a059329598369bb6b7c70a632b5055",
    "Proof.lean": "9453e695e8434317b6ee10c11667a5613b8e7b09159f3f963a3bfc3d314c69a5",
    "AnchorAudit.lean": "0336d02d65bd0de0b3e031547f8142d8f50dd0e12d3ab2c9c6085717d97e7493",
    "Validation.lean": "e9b31207a910377471d804eb722c39ad146d85b07287c653a052a96fca607341",
}
EXPECTED_INPUTS = {
    "Statement.lean": "984ec64013fa92caf23696c39017a28b7c8a908224ae8e1018a156734469f70c",
    "ObligationTree.lean": "8877433688d159ad88c07307d59cb8e6bad9d0c54b97cbae739609bf5a69602e",
    "Proof.lean": "707249895e0dfca3638f1fb8f94ae907d0e55a4ffeb1c07cb7e4697000e4b9ae",
    "AnchorAudit.lean": "3f2ed9d48513168e33323b09a21e977fcfa10301255c744cbc6d65b6ad89574b",
    "Validation.lean": "e072ad47b44d45245b7397c841706bee577d93345ecb28ed689e3444d73d8480",
    "instance.json": "730008cde87ff5a63b33a7f08c9082bfedc1546ab4d5a1debedcce1f2dbc2fff",
    "statement.json": "1af288978c86bf3bf24bdc627fef502a15df88b919e7926a0c79d63afa263362",
    "anchor-audit.json": "a653c9c9a230ad26d3160905542831fa716ed6135ea5eb2f1f676f62dd3c6dbf",
    "obligation-registry.json": "1310ad818e169b8d56d1a5dfcd75294756051d5b834979bc996daadce1a58bef",
    "typed-graphs.json": "93b9f4757d1739dd78bfd914ffe98f4ab45c4e86ac0308e2b942dd53e1e98f77",
    "validation-specs.json": "0dd4e5771731cebf9811dc3671d04bc940465affadec79f58b1808ec0e15404a",
    "proof-blocker.json": "5f53ba41386360b0b673bc2e493989c485f12ab81a8951930077ce53a219dea2",
    "proof-receipt.json": "ff8dc94634474ec113721a57cc48ed46ee6c6a4fdaea4cbfdf82b96db131f368",
    "validation-spec.json": "f883e4650e1c1041c7fe7f52f89b9cdb54a243a6dd80cd158547c3a94c282b52",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "bfe473cc1c4fd4ab7b09caff0c110c2d7261340bca23362c4440a653862f2032",
    "source-statement-crosswalk.md": "598260f0cdd29500e3a43e0384a5970292930985fe72363e88c1755f7747cfac",
    "README.md": "8342035b7010d7c566f3c2880158eaf412ebb1d9ec7b89a3a0db26748961144a",
    "obligation-tree.md": "0d87006c00b1f3a3067568ff0ad883bfd7d468b451bb26404761dcf9e7511ea0",
    "task-dag.json": "3fa6d4269141c147908af4f5b24447dfab726bdfce0190a4a83621a3ea4282b9",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "d8e9381497e9ea2b8d85beaacff31dd3b8e004f48a3149580581dda0312a6322",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3f9d0b4dd2d9e8c2cf1ce4f4d070f6ebe645b42a4a8dd92a17354afdf5907908",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_OUTPUTS = {
    "release-spec.json": "28655e1b183d5b497cb5cbbc4feb194e27514eb1c82ada80af07195e54e8e15c",
    "release-decision.json": "4b97039f5b1031d68a3ad5f05f9d7ab0a49fbaa632fc9225e260ca43330ed378",
    "release-phase.md": "e3c293b3d09823b8b763bc0d3e615e51a702ea0b924a64b487082bbda0483ab4",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1271 current network-isolated trust-zero partial replay",
    "PASS release inputs, frozen denominator, provisional dependency, and negative authority boundary reconciled",
    "BLOCKED dependency: S56-M-1271-VALIDATION is provisional, unaccepted, and nonrelease",
    "BLOCKED exact root: M1271-C-PS-SEQUENCE, M1271-T-CRITICAL, and M1271-ROOT remain open",
    "BLOCKED AUDIT-Z: source review and public/structured state are unreconciled",
    "verdict=blocked lifecycle=planned root=H3/M3/R4 audit_complete=false theorem_complete=false accepted_receipts=0",
)


if sys.flags.optimize:
    raise SystemExit("release check failed: Python optimization disables assertions")


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
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).strip()


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
    match = re.search(
        rf"'[^']*{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output,
        flags=re.DOTALL,
    )
    if match is None:
        assert re.search(
            rf"'[^']*{re.escape(declaration)}' does not depend on any axioms", output
        ), declaration
        return set()
    return {
        part.strip()
        for part in match.group(1).replace("\n", "").split(",")
        if part.strip()
    }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def narrow_lean_replay() -> dict[str, str]:
    fixed_env = os.environ.copy()
    fixed_env.pop("LEAN_PATH", None)
    fixed_env.update({
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    })
    lake_name = shutil.which("lake")
    bwrap_name = shutil.which("bwrap")
    assert lake_name is not None and bwrap_name is not None
    lake = Path(lake_name).resolve()
    bwrap = Path(bwrap_name).resolve()
    assert sha256(lake) == LAKE_SHA256 and sha256(bwrap) == BWRAP_SHA256
    lean = Path(run([str(lake), "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env).strip())
    lean_path = run(
        ["env", "-u", "LEAN_PATH", str(lake), "env", "printenv", "LEAN_PATH"],
        cwd=LEAN_ROOT,
        env=fixed_env,
    ).strip()
    assert lean.is_file() and sha256(lean) == LEAN_SHA256
    version = run([str(lean), "--version"], env=fixed_env, timeout=60)
    assert "Lean (version 4.29.0" in version and LEAN_COMMIT in version

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="stage1-m1271-release-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        home = tmp / "home"
        home.mkdir()
        for source in LEAN_MODULES:
            shutil.copy2(HERE / source, tmp / source)
        base = [
            str(bwrap),
            "--ro-bind", "/", "/",
            "--bind", str(tmp), str(tmp),
            "--dev", "/dev",
            "--proc", "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--clearenv",
            "--setenv", "HOME", str(home),
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1",
            "--setenv", "LEAN_PATH", lean_path,
            "--chdir", str(tmp),
            str(lean), "--trust=0", "--root", str(tmp),
        ]
        local = base.copy()
        local[local.index(lean_path)] = f"{tmp}:{lean_path}"
        outputs["Statement.lean"] = run(
            base + ["-o", "Statement.olean", "Statement.lean"], env=fixed_env, timeout=300
        )
        outputs["ObligationTree.lean"] = run(
            local + ["-o", "ObligationTree.olean", "ObligationTree.lean"],
            env=fixed_env,
            timeout=300,
        )
        outputs["Proof.lean"] = run(
            local + ["-o", "Proof.olean", "Proof.lean"], env=fixed_env, timeout=300
        )
        outputs["Validation.lean"] = run(
            local + ["-o", "Validation.olean", "Validation.lean"],
            env=fixed_env,
            timeout=300,
        )
        outputs["AnchorAudit.lean"] = run(
            base + ["AnchorAudit.lean"], env=fixed_env, timeout=300
        )

    report_count = 0
    for module, declarations in AXIOM_DECLARATIONS.items():
        for declaration in declarations:
            assert reported_axioms(outputs[module], declaration) == ALLOWED_AXIOMS
            report_count += 1
    assert report_count == 12
    combined = "\n".join(outputs[name] for name in LEAN_MODULES)
    assert "sorryAx" not in combined and "error:" not in combined
    return {name: hashlib.sha256(output.encode()).hexdigest() for name, output in outputs.items()}


def main() -> None:
    os.umask(0o022)
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 164
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned"
    assert target["legacy_artifacts_accepted"] is target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 164,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1271-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1271-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert decision["authority_inputs"] == AUTHORITY_INPUTS
    expected_bindings = {
        **{f"Stage1_Instances/{THEOREM}/{name}": value for name, value in EXPECTED_INPUTS.items()},
        **AUTHORITY_INPUTS,
    }
    assert receipt["input_bindings"] == expected_bindings

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1271.MountainPassTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1271-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == (
        DENOMINATOR_SHA256
    )
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert all(row["terminal_proof_body_id"] is None for row in registry["obligations"])
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["theorem_complete"] is False
    assert closure["root_machine_debt"] == "M3"
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1271-ROOT")
    assert [root["human_debt"], root["machine_debt"], root["readability_debt"]] == [
        "H3", "M3", "R4"
    ]
    assert graphs["graphs"]["evidence"]["edges"] == []
    assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    local_dag = load(HERE / "task-dag.json")
    assert local_dag["lifecycle"] == "planned" and local_dag["accepted_states"] == []
    assert {row["state"] for row in local_dag["tasks"]} == {"open"}
    crosswalk = (HERE / "source-statement-crosswalk.md").read_text(encoding="utf-8")
    assert "exact page, wording, hypotheses" in crosswalk
    assert "Independent review is required before `H0`" in crosswalk

    assert anchor["root_decision"]["kernel_closed"] is False
    assert proof["accepted"] is False and proof["proposed_state"] == "[_]"
    assert proof["closed_obligation_ids"] == ["M1271-C-PATH-MAX"]
    assert proof["partial_progress"]["obligation_id"] == "M1271-C-PS-SEQUENCE"
    assert proof["partial_progress"]["obligation_closed"] is False
    assert proof["result"]["root_closed"] is proof["result"]["theorem_complete"] is False
    assert proof["remaining_root_cut_set"] == ROOT_CUT
    assert blocker["first_failed_gate"].startswith("M1271-C-PS-SEQUENCE")
    assert blocker["remaining_root_cut_set"] == ROOT_CUT

    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["item_id"] == "S56-M-1271-VALIDATION"
    assert validation["receipt_id"] == "S56-M-1271-VALIDATION-local-20260715"
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["verdict"] == "blocked"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["accepted_receipt_ids"] == []
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["root_machine_debt"] == "M3"
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["remaining_root_cut_set"] == ROOT_CUT
    old_checker = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert f'BASE_REVISION = "{VALIDATION_BASE}"' in old_checker
    assert 'load(ROOT / ".stage1-worker-selftest.json")' in old_checker
    assert '"phase": "validation"' in old_checker and '"state": "[ ]"' in old_checker
    assert VALIDATION_BASE != BASE_REVISION

    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink() and MATHLIB.is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["receipt_support_state"] == validation["support_state"]
    assert dependency["receipt_verdict"] == validation["verdict"] == "blocked"
    assert dependency["receipt_accepted"] is dependency["receipt_release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["historical_recipe_currently_replayable"] is False

    decision_result = decision["decision"]
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["accepted_receipt_ids"] == []
    assert decision_result["verdict"] == "blocked"
    assert decision_result["lifecycle_before"] == decision_result["lifecycle_after"] == "planned"
    expected_vector = {"H": "H3", "M": "M3", "R": "R4"}
    assert decision_result["root_vector_before"] == decision_result["root_vector_after"] == (
        expected_vector
    )
    assert decision_result["audit_complete"] is decision_result["theorem_complete"] is False
    assert decision_result["release_accepted"] is False
    assert decision_result["audit_z"] == decision_result["theorem_z"] == "blocked"
    assert decision_result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision_result["first_failed_gate_detail"] == (
        "dependency.S56-M-1271-VALIDATION.master_acceptance"
    )
    assert decision_result["first_failed_theorem_gate"] == (
        "proof.M1271-C-PS-SEQUENCE.kernel_closure"
    )
    for obligation in ROOT_CUT:
        assert obligation in decision_result["remaining_root_cut_set"]
    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["accepted_closed_obligation_ids"] == []
    assert reconciliation["provisionally_observed_obligation_ids"] == PROVISIONAL_IDS
    assert reconciliation["partially_observed_obligation_ids"] == [
        "M1271-C-PS-SEQUENCE"
    ]
    for key in (
        "exact_root_kernel_closure",
        "validation_dependency_master_accepted",
        "accepted_foundation_profile",
        "complete_transitive_tcb_and_provenance",
        "source_fidelity_h0_accepted",
        "readability_r0_accepted",
        "audit_z_accepted",
        "immutable_clean_release_input",
        "cold_empty_cache_build",
        "offline_archive_replay",
        "complete_sbom_and_license_closure",
        "deterministic_release_bundle",
        "distinct_runner_independent_verification",
        "independently_implemented_minimal_verifier",
        "second_signed_attestation",
        "protected_release_ci",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    conflicts = decision["authority_conflicts"]
    assert set(conflicts) == {
        "local_task_dag", "human_debt_taxonomy", "machine_candidate_taxonomy"
    }
    assert "H3" in conflicts["human_debt_taxonomy"]
    assert "M0-P" in conflicts["machine_candidate_taxonomy"]
    assert decision["exact_statement_delta"] == "none"
    assert decision["typed_graph_delta"].startswith("none")
    assert decision["canonical_obligation_ids"] == INVENTORY_IDS
    assert decision["statement_fingerprint"] == f"lean-expression-sha256:{EXPRESSION_SHA256}"
    assert decision["actual_source_ownership"] == [
        f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert decision["declaration_ownership"] == []
    assert decision["readable_ownership"] == [
        f"Stage1_Instances/{THEOREM}/release-phase.md"
    ]
    assert decision["change_impact_set"] == [ITEM]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == (
        "outer_not_namespace_enforced; nested_lean_denied"
    )
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-1271-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is receipt["master_accepted"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["root_vector_before"] == receipt["result"]["root_vector_after"] == (
        expected_vector
    )
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["provisionally_observed_obligation_ids"] == PROVISIONAL_IDS
    assert receipt["result"]["partially_observed_obligation_ids"] == [
        "M1271-C-PS-SEQUENCE"
    ]
    assert receipt["result"]["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["result"]["first_failed_theorem_gate"] == (
        "proof.M1271-C-PS-SEQUENCE.kernel_closure"
    )
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations", "covered_decisions",
    ):
        assert receipt["recipe"][key] == spec[key], key
    expected_release_bindings = {
        f"Stage1_Instances/{THEOREM}/{name}": digest
        for name, digest in RELEASE_OUTPUTS.items()
    }
    assert receipt["release_output_bindings"] == expected_release_bindings
    for relative, expected in expected_release_bindings.items():
        assert sha256(ROOT / relative) == expected, f"release output drifted: {relative}"
    assert receipt["repository_state"]["initial_status"] == [
        "?? Formalizations/Lean/.lake"
    ]
    assert receipt["checker_binding"] == {
        "path": f"Stage1_Instances/{THEOREM}/check_release.py",
        "sha256": sha256(Path(__file__).resolve()),
    }
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["execution"]["exit_code"] == 0
    assert receipt["execution"]["stdout_sha256"] == hashlib.sha256(
        expected_stdout
    ).hexdigest()
    assert receipt["execution"]["stdout_bytes"] == len(expected_stdout)
    assert receipt["execution"]["stdout_line_count"] == len(SUMMARY_LINES)
    assert receipt["current_replay"]["expected_axiom_report_count"] == 12
    assert set(receipt["current_replay"]["observed_axioms"]) == ALLOWED_AXIOMS

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b|\bextern[ \t]+",
        flags=re.MULTILINE,
    )
    for name in LEAN_MODULES:
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited proof construct in {name}"
    validation_source = source_without_comments((HERE / "Validation.lean").read_text())
    assert "import Proof" not in validation_source and "import ObligationTree" not in validation_source
    assert "(critical :" in validation_source
    proof_source = source_without_comments((HERE / "Proof.lean").read_text())
    assert "(produce :" in proof_source
    assert not re.search(r"^theorem\s+\w+\s*:\s*MountainPassTarget", proof_source, re.MULTILINE)
    assert not list(HERE.glob("*.olean")) and not list(HERE.glob("tmp*.lean"))
    lean_hashes = narrow_lean_replay()
    assert lean_hashes == EXPECTED_LEAN_OUTPUTS

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for relative in CHANGED_PATHS - {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/check_release.py",
    }:
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    assert platform.system() == "Linux"
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
