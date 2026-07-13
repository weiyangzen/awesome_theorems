#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1029-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1029"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1029-VALIDATION"
THEOREM = "THM-M-1029"
BASE_REVISION = "2d334dfd1443fdb9dbdf08b9d53d6c67399ec7af"
BASE_TREE = "1e9faa0af7424ddabe787898ee4534051a4cc145"
TARGET_EXPRESSION = "f3e443377f8cac2eba62a6ebcf6f05ce5bd453f3075d9de573641856e21331b2"
REGISTRY_DENOMINATOR = "f5ba78d2ff64231db87b356cdf2827f4d9173387c0a387c3acfbddad19cf0fb4"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_INPUTS = {
    "Statement.lean": "ae6a30cd8ba78423f8d4577bb1c6e9e047cc7c8f10e5a2ba8b6d500337f06782",
    "ObligationTree.lean": "9298952a961d60af29ff4fe28ce1600174837a08e1addbfd51f06da678678453",
    "Proof.lean": "d1b7395e0a5206f4c655e1c9b226036d786eb24d7c09b5f43340cf3c17bdebc6",
    "Validation.lean": "1abd510ed8795c6b21615830f0a6183860d1cda083a287c5fa245ac67643427e",
    "statement.json": "32d7ae2323df43130a91e511a65b2d31cb5aed42518bdcc8deea12dd8c5d7400",
    "anchor-audit.json": "0d281883b5c2d62c07d485fd5e9c606ccff04d233d97293dcedd04c1c956573b",
    "obligation-registry.json": "22a9b3af299a84aecefdc49c60ca96a261a8c37157e6d1f15ae0cddcba577053",
    "typed-graphs.json": "96fe778b583d0c3d5e4e4b8936428b2a0f928736aa0c4032722e199b9e22e774",
    "proof-receipt.json": "c6de98f9443838002fbd4606561cd67dff76d6fe16ab3b473dc2a185e8574aed",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_PROOF_DECLARATIONS = {
    "Stage1Instances.THM_M_1029.Proof.bracketCompensated_deterministicTime_eq",
    "Stage1Instances.THM_M_1029.Proof.deterministicTimeProcess_continuousPaths",
    "Stage1Instances.THM_M_1029.Proof.deterministicTimeProcess_monotonePaths",
    "Stage1Instances.THM_M_1029.Proof.deterministicTimeProcess_startsAtZero",
    "Stage1Instances.THM_M_1029.Proof.bracketCompensated_martingale_of_quadratic",
    "Stage1Instances.THM_M_1029.Proof.quadraticCompensated_stronglyAdapted",
    "Stage1Instances.THM_M_1029.Proof.square_stronglyAdapted",
    "Stage1Instances.THM_M_1029.Proof.deterministicTime_stronglyAdapted_of_martingales",
    "Stage1Instances.THM_M_1029.Proof.quadratic_coordinate_integrable",
    "Stage1Instances.THM_M_1029.Proof.coordinate_memLp_two",
    "Stage1Instances.THM_M_1029.Proof.increment_memLp_two",
    "Stage1Instances.THM_M_1029.Proof.increment_square_integrable",
    "Stage1Instances.THM_M_1029.Proof.increment_condExp_eq_zero",
    "Stage1Instances.THM_M_1029.Proof.increment_condExp_sq",
    "Stage1Instances.THM_M_1029.Proof.integral_process_eq_zero",
    "Stage1Instances.THM_M_1029.Proof.integral_process_sq_eq_time",
    "Stage1Instances.THM_M_1029.Proof.variance_process_eq_time",
    "Stage1Instances.THM_M_1029.Proof.zeroElapsedIncrement",
    "Stage1Instances.THM_M_1029.Proof.hasLaw_gaussianReal_of_charFun",
    "Stage1Instances.THM_M_1029.Proof.hasLaw_gaussianReal_zero",
    "Stage1Instances.THM_M_1029.Proof.incrementLawPackage_of_components",
    "Stage1Instances.THM_M_1029.Proof.incrementLawPackage_of_strict",
    "Stage1Instances.THM_M_1029.Proof.root_of_assumedIncrementComponents",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 900) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        timeout=timeout, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=30).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def axiom_reports(output: str) -> dict[str, list[str]]:
    matches = re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL)
    return {
        name: [part.strip() for part in raw.split(",") if part.strip()]
        for name, raw in matches
    }


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 222 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["phase"] == "validation" and item["layer"] == 5 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-1029-PROOF"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1029-PROOF")
    assert predecessor["state"] == "[_]"
    assert instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == []

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1029.LevyMartingaleCharacterizationTarget"
    )
    assert formal["elaborated_expression_sha256"] == TARGET_EXPRESSION
    assert registry["root_obligation_id"] == "M1029-ROOT"
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR
    assert graphs["registry_denominator_sha256"] == REGISTRY_DENOMINATOR
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == ["M1029-T-INCREMENTS"]
    assert graphs["graphs"]["evidence"]["edges"] == []
    assert proof_receipt["accepted"] is False
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["closed_obligation_ids"] == []

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
        assert receipt["inputs"][name] == expected, name
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == anchor["immutable_environment"]["mathlib_license_sha256"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    for forbidden in (
        "import Proof", "import ObligationTree", "root_of_incrementLawPackage",
        "incrementLawPackage_of_strict", "root_of_assumedIncrementComponents",
    ):
        assert forbidden not in code_without_comments(validation_source), forbidden
    assert "(hstrict : DirectStrictIncrementLaw" in validation_source
    assert not list(HERE.glob("*.olean")) and not list(HERE.glob("tmp*.lean"))

    bwrap = shutil.which("bwrap")
    assert bwrap is not None, "bubblewrap is required for network-denied Lean replay"
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, timeout=60).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT, timeout=60).strip())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, timeout=60).strip()
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT, timeout=60)
    assert "4.29.0" in lean_version and "98dc76e3c0a9b856c9b98726b713fb04fab16740" in lean_version

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="m1029-validation-") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        base = [
            bwrap, "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--setenv", "HOME", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]
        outputs["Statement.lean"] = run(base + [
            "--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0", "-t0",
            "-o", "Statement.olean", "Statement.lean",
        ])
        module_path = f"{tmp}:{lean_path}"
        outputs["ObligationTree.lean"] = run(base + [
            "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
            "-o", "ObligationTree.olean", "ObligationTree.lean",
        ])
        outputs["Proof.lean"] = run(base + [
            "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0", "Proof.lean",
        ])
        outputs["Validation.lean"] = run(base + [
            "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
            "Validation.lean",
        ])

    tree_reports = axiom_reports(outputs["ObligationTree.lean"])
    assert tree_reports == {
        "Stage1Instances.THM_M_1029.root_of_incrementLawPackage": EXPECTED_AXIOMS
    }
    proof_reports = axiom_reports(outputs["Proof.lean"])
    assert set(proof_reports) == EXPECTED_PROOF_DECLARATIONS
    assert all(axioms == EXPECTED_AXIOMS for axioms in proof_reports.values())
    validation_reports = axiom_reports(outputs["Validation.lean"])
    assert validation_reports == {
        "Stage1Instances.THM_M_1029.Validation.exactRootOfDirectStrictIncrementLaw": EXPECTED_AXIOMS
    }
    assert "sorryAx" not in "".join(outputs.values())

    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == spec["item_id"] == ITEM
    assert receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["started_at"] == "2026-07-14T04:12:03+08:00"
    assert receipt["finished_at"] == receipt["validated_at"] == "2026-07-14T04:14:38+08:00"
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["first_failed_gate"] == "dependency.S56-M-1029-PROOF.master_acceptance"
    assert receipt["first_failed_theorem_gate"] == "proof.root_kernel_closure.M1029-T-INCREMENTS"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    environment = receipt["environment"]
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["bubblewrap_executable_sha256"] == sha256(Path(bwrap).resolve())
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["platform"] == f"{platform.system()} {platform.machine()}"
    result = receipt["result"]
    assert result["network_isolated_trust_zero_replay"] == "pass"
    assert result["axiom_report_count"] == 25
    assert result["observed_axioms"] == EXPECTED_AXIOMS
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M3"
    assert result["remaining_root_cut_set"] == ["M1029-T-INCREMENTS"]
    assert result["complete_foundation_tcb_gate"] == "fail_closed"
    assert result["complete_provenance_gate"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False

    required_packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary", "base_revision",
        "known_failures", "state",
    }
    assert set(packet) == required_packet_fields
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]
    status = git(
        "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1029 narrow validation")
    print("PASS network-isolated trust-zero kernel replay: statement, conditional composition, 23 partial proof declarations, and differential conditional adapter elaborated")
    print("PASS trust observation: 25 reports list exactly propext, Classical.choice, and Quot.sound")
    print("PASS selected provenance: frozen hashes, clean mathlib revision/tree/remote, toolchain, manifest, and license agree")
    print("OPEN root: M1029-T-INCREMENTS has no proof body; audit_complete=false; theorem_complete=false")
    print("BLOCKED release: warm shared dependency cache, incomplete foundation/TCB/provenance, and no distinct signed independent verifier")


if __name__ == "__main__":
    main()
