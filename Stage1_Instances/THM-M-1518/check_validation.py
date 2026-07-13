#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1518-VALIDATION."""

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
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1518"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1518-VALIDATION"
THEOREM = "THM-M-1518"
BASE_REVISION = "35d23d0193cd7c8fccb1d09f22534c6eba066b02"
BASE_TREE = "4325d20b5ec8db888f28fcedc79cc1b7745c0c68"
EXPRESSION_SHA256 = "4cc15786f13f4e4ad7594012ab3e96613f5bffbf572523e8282b41139fe6979f"
DENOMINATOR_SHA256 = "dc5ea1db035dfa578766c6af2fac7c562127454ec7c9a7f7f073766e095002b1"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
MACHINE_IDS = [
    "M1518-ROOT",
    "M1518-S-DEFINITIONS",
    "M1518-S-BOUNDARY",
    "M1518-S-FOUNDATION",
    "M1518-N-DIFFERENTIATE",
    "M1518-N-WEAK",
    "M1518-L-IBP",
    "M1518-L-FUNDAMENTAL",
    "M1518-L-WEAK-POINTWISE",
    "M1518-T-ASSEMBLE",
]
EXPECTED_INPUTS = {
    "Statement.lean": "c5f7022ac18e06a2dd9e5ee8d35590e15ee46777468c2c197884535230c1c167",
    "ObligationTree.lean": "026f35442b9a3580db9dd8aed098d273c95c9d559f86b8cdba1331703999fdc6",
    "Proof.lean": "1b93c59d624e8989ac79910253c071b044588b8daae22dae39ebb5e68c5ab8f4",
    "WeakToPointwise.lean": "db0514399f5f07c7f49537dcfc26c9a2616cd24160a76689ca0efcd1edf2648d",
    "ExactProof.lean": "e234f8dfa16e2f6867895ae393c4dd9d023a177fe61adcce7c4893ee65269d46",
    "statement.json": "ce936dd890c8d808fae5a2869f0831fc7b8854a343ce90ed78d1647e48a6ef9f",
    "anchor-audit.json": "b7f872bd76e8157715ecddfa61cfe8e9ce8b7fa18c6e0cdd7bb394836c5d264e",
    "obligation-registry.json": "32502789f8cd24c0c816e58a36f505d7fb71dfbb65904cb13292e38b5ab0f35c",
    "typed-graphs.json": "5e98dbe3ee8bd5c884f4a1785472a092823cec2026e17c69370d38f64e8761cb",
    "proof-receipt.json": "d03954c0f4db858feb332df30e847b6717f03e60089d9b59cb2fc6f39d376d31",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_SOURCES = {
    "Mathlib/Analysis/Calculus/ParametricIntervalIntegral.lean": {
        "blob": "6a44e04a88fffa136f8dbb0c8478f83837c7092e",
        "sha256": "67f55a565f3bcda00a0e5840b2d90b51290b3bea01e7861254cf58da95e0bc35",
        "olean_sha256": "0675c65847379e75bba92477f204d4fc1e54e389c931947e0609979388ac37d1",
    },
    "Mathlib/MeasureTheory/Integral/IntervalIntegral/IntegrationByParts.lean": {
        "blob": "eb3e198721429296381f334036905dbb6cc4a067",
        "sha256": "792edb9e7e44264e4e802f8ef929ea9c7a404dba6ea5f02d5740b4eb2f721bb9",
        "olean_sha256": "9a84d5e28860a5ebd3305c6f3a44519e9d81076ada76e5c2bf9d09921b8c960a",
    },
    "Mathlib/Analysis/Distribution/AEEqOfIntegralContDiff.lean": {
        "blob": "d4552cafa158305afcb31ebdea62639bb8e9d3c8",
        "sha256": "e31b3d69ca4eba63b3afc414645ca78ba071fae1ed8054870a5c940a75552919",
        "olean_sha256": "b689da24e7809a3bb3aef3cecd611bce29d6b8027610e9687913a572f16ee9a4",
    },
    "Mathlib/MeasureTheory/Measure/OpenPos.lean": {
        "blob": "601971614b849cf52e4d3b6ea28056990419882f",
        "sha256": "e3534e47559897179921b525da64019a356238b1dff1fd0521588bf2102020e9",
        "olean_sha256": "001a5cae1dd998ef5c343b224d4fdc323375ee08ac15bd2d7e11e986c54ed217",
    },
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1518 narrow validation",
    "PASS network-isolated kernel replay: exact statement, frozen composition, analytic packages, exact root, and differential root elaborated",
    "PASS trust observation: checked declarations are sorry-free and report exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, clean mathlib pin, selected source blobs/oleans, license, and tools agree",
    "FAIL CLOSED authority: proof is only worker-self-tested and the authoritative graph remains M4 with its pre-proof cut set",
    "FAIL CLOSED foundation/trust: M1518-S-FOUNDATION and complete transitive declaration, compiled-artifact, and TCB closure remain open",
    "FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout empty-cache bootstrap, offline restoration, or a deterministic TCB/SBOM bundle",
    "FAIL CLOSED independent release: differential composition used this worker and shared cache, not a distinct signed verifier",
    "audit_complete=false; theorem_complete=false",
)
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 600.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables fail-closed assertions")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 600-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, declaration
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    selftest = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 187 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 187,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1518-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1518-PROOF"
    )
    assert predecessor["state"] == "[_]"

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1518.StationaryActionEulerLagrangeTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert anchor["canonical_target"] == (
        "Stage1Instances.THM_M_1518.StationaryActionEulerLagrangeTarget"
    )
    assert anchor["canonical_target_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == [
        "M1518-N-DIFFERENTIATE", "M1518-L-IBP", "M1518-L-FUNDAMENTAL"
    ]
    assert proof_receipt["item_id"] == "S56-M-1518-PROOF"
    assert proof_receipt["canonical_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["inputs"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    for name in ("Proof.lean", "WeakToPointwise.lean", "ExactProof.lean"):
        assert proof_receipt["proof_bodies"][name]["source_sha256"] == EXPECTED_INPUTS[name]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOM_LIST
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["accepted"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    lean_sources = (
        "Statement.lean", "ObligationTree.lean", "Proof.lean",
        "WeakToPointwise.lean", "ExactProof.lean", "Validation.lean",
    )
    for name in lean_sources:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    differential = code_without_comments(
        (HERE / "Validation.lean").read_text(encoding="utf-8")
    )
    assert "import «Stage1_Instances».«THM-M-1518».ExactProof" not in differential
    assert "stationaryActionEulerLagrange" not in differential
    assert "independentlyRecomposedStationaryActionEulerLagrange" in differential
    assert "assert_no_sorry ObligationTree.weakToPointwise" in differential

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    for relative, expected in MATHLIB_SOURCES.items():
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == expected["blob"]
        assert sha256(MATHLIB / relative) == expected["sha256"]
        olean = MATHLIB / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert sha256(olean) == expected["olean_sha256"]
    assert sha256(MATHLIB / "LICENSE") == (
        "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
    )

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    lake_version = run(["lake", "env", "lake", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in lake_version
    python = Path(os.path.realpath(sys.executable))
    git_path = Path(os.path.realpath(shutil.which("git") or ""))
    bash = Path(os.path.realpath(shutil.which("bash") or ""))
    bwrap = Path(os.path.realpath(shutil.which("bwrap") or ""))
    assert sha256(lean) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(lake) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert sha256(python) == "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
    assert sha256(git_path) == "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
    assert sha256(bash) == "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd"
    assert sha256(bwrap) == "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"

    runner_output = run(["bash", str(HERE / "check_validation.sh")])
    proof_declarations = (
        "Stage1Instances.THM_M_1518.ObligationTree.exactTarget_of_packages",
        "Stage1Instances.THM_M_1518.firstVariationFormula",
        "Stage1Instances.THM_M_1518.ObligationTree.weakToPointwise",
        "Stage1Instances.THM_M_1518.stationaryActionEulerLagrange",
        "Stage1Instances.THM_M_1518.Validation."
        "independentlyRecomposedStationaryActionEulerLagrange",
    )
    for declaration in proof_declarations:
        assert printed_axioms(runner_output, declaration) == EXPECTED_AXIOMS
    assert runner_output.count("Declarations are sorry-free!") == 3
    assert "sorryAx" not in runner_output and "declaration uses 'sorry'" not in runner_output

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "--unshare-net" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == MACHINE_IDS
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact nine-line PASS/FAIL-CLOSED status summary",
    }]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1518-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    for name in (
        "Validation.lean", "validation-spec.json", "check_validation.py",
        "check_validation.sh", "validation-phase.md",
    ):
        assert receipt["inputs"][name] == sha256(HERE / name), name
    canonical = receipt["canonical_target"]
    assert canonical["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert canonical["registry_denominator_sha256"] == DENOMINATOR_SHA256
    environment = receipt["environment"]
    assert environment["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(git_path)
    assert environment["bash_executable_sha256"] == sha256(bash)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    result = receipt["result"]
    assert result["exact_root_kernel_replay"] == "provisional_pass"
    assert result["differential_exact_root_replay"] == "provisional_pass_same_worker_composition"
    assert result["observed_axioms"] == EXPECTED_AXIOM_LIST
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["selected_provenance"] == "pass"
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["accepted_root_machine_debt"] == "M4"
    assert result["accepted_root_closed"] is False
    assert result["foundation_and_complete_trust_closure"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1518-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert set(selftest) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
    assert selftest["base_revision"] == BASE_REVISION
    assert set(selftest["changed_paths"]) == CHANGED_PATHS
    assert all(command["exit_code"] == 0 for command in selftest["commands"])
    assert selftest["known_failures"]
    assert "theorem_complete=false" in selftest["output_summary"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    phase_notes = (HERE / "validation-phase.md").read_text(encoding="utf-8")
    assert "same-worker differential composition" in phase_notes
    assert "empty-cache cold bootstrap" in phase_notes
    assert "theorem completion remain false" in phase_notes
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
