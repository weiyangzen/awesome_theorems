#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1237-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import time


if not __debug__:
    raise SystemExit("check_validation.py must run without Python optimization")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1237"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1237-VALIDATION"
THEOREM = "THM-M-1237"
BASE_REVISION = "c45f3c7090cb4adf616d45e5414985f956e807b2"
BASE_TREE = "da6f991c07f11e8608ddc090af9356558d64d360"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
DENOMINATOR_SHA256 = "1a309fe73f42f45071752d8097db176fe8f343549f0a35bf1bb834dcc4827ab2"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "490f7dc2b30c9d2cb4a1d2f24ee5635fbf02b50f443cd1c7a3430ed7162ec439",
    "ObligationTree.lean": "9c67e735e4fe98d3092007c455c76ce287a3812a489d33b46ab5e4198c69b099",
    "Proof.lean": "6be4f06a2b28551c2c78133ffa450fd82142546b7cd153da75282206af1337b7",
    "ProofAudit.lean": "6fd30eaff6d23fc0d21a399fa51e983270facf9fadc59e8dae85cb36d8216aa1",
    "Validation.lean": "fb48776ca92ddcb096db29f7afdd91cb00d4190e0f5c2f32ae1ec05844cfb66f",
    "statement.json": "faaba0b3086bd912fdcfff84cabd9e2cc7771d7c1d101e2d9e99e1dcdf03ecf4",
    "obligation-registry.json": "7bdb1e61eee9f1c790f281371af80a09e113bbad73548f330f9aedee278c8143",
    "typed-graphs.json": "d14f3c4c59ee2f255e28c69e16ffce9185702c51cf4c4038da7145c71f464cae",
    "anchor-audit.json": "ffc4c20d39c685975826a64bc2fadf80bb9b033c6af5ad90da967337456aa15e",
    "proof-phase.json": "5a10caba8ddc2f0eb66fc2e763a9899b7f8a3792424cc899ddbc34f5ba80a7f9",
    "proof-receipt.json": "04f8fa7318fc6d0cd823d461ccac63a9c506ab498502c425aa948cf27332da6d",
    "check_validation.sh": "20c8955efbf557b9498b1cd1cba907bee9b612ca2fbdfe3a37783164edf841ce",
    "validation-spec.json": "60ff2c85e4ef343b6e72952938947526f145af4583f9d82a2f6cf4074f18ae49",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
NO_ATOMS_SOURCE = "Mathlib/MeasureTheory/Measure/Typeclasses/NoAtoms.lean"
LP_SOURCE = "Mathlib/MeasureTheory/Function/LpSeminorm/Basic.lean"
NO_ATOMS_BLOB = "eaab333200bab4b3bcdaa56276fb04581fe0f92c"
LP_BLOB = "e0a122dd1bc6d05024bec05b80a03fcd6f390fb6"
NO_ATOMS_SHA256 = "00c911ddff66ff8cee84a136785326a441ad91e6f4f8373f000f5a931c05a5d9"
LP_SHA256 = "e849c1fa8b9b499c93dada90025449c07d1b07126edd80f05f5c456b27ffc652"
NO_ATOMS_OLEAN_SHA256 = "c912f9041d449614701d92d155cc1f2c34f69661a5fb2569e3ae575e595c5987"
LP_OLEAN_SHA256 = "2b8a8fe0dd4f840d44338320dc2030f79bf6f4c0954b9c0626708c2718f8b9e8"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/ProofAudit.lean",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1237 narrow validation",
    "PASS network-isolated trust-zero replay: exact statement, conditional composition, proof units, and differential countermodel elaborated",
    "PASS hygiene: kernel sorry checks and comment-stripped prohibited-construct scan passed",
    "PASS trust observation: checked proof and differential declarations use only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, clean mathlib pin/tree/remote, selected source and olean hashes, license, and tools agree",
    "FAIL CLOSED root: M1237-L-VALUE is independently kernel-refuted; M1237-L-HOLDER remains open; exact root stays M3",
    "FAIL CLOSED hermetic/trust: shared warm .lake is not an empty-cache offline replay or complete transitive TCB/SBOM bundle",
    "FAIL CLOSED independence/authority: same-worker differential replay is not a distinct signed runner, and the proof prerequisite is not master-accepted",
    "audit_complete=false; theorem_complete=false",
)
VALIDATION_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 600.0


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - VALIDATION_STARTED)
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
    if result.returncode != 0:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_phase = load(HERE / "proof-phase.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 175 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 175,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1237-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1237-PROOF"
    )
    assert predecessor["state"] == "[_]"

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    assert statement["canonical_formal_target"]["statement_file_sha256"] == (
        EXPECTED_INPUTS["Statement.lean"]
    )
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["statement.json"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_phase["inputs"]["proof_source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    fingerprints = {
        row["obligation_id"]: row["statement_fingerprint"]
        for row in registry["obligations"]
    }
    implemented = proof_receipt["obligation_statement_fingerprints"]
    assert implemented == {
        "M1237-C": fingerprints["M1237-C"],
        "M1237-L-VALUE": fingerprints["M1237-L-VALUE"],
    }
    assert proof_receipt["closed_obligation_ids"] == ["M1237-C"]
    assert proof_receipt["disproved_interface_obligation_ids"] == ["M1237-L-VALUE"]
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["first_failed_gate"] == "M1237-L-VALUE"
    assert proof_receipt["remaining_root_cut_set"] == [
        "M1237-L-HOLDER", "M1237-L-VALUE"
    ]
    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert anchor["exact_closure_found"] is False
    boundary = graphs["closure_boundary"]
    assert boundary["closed_obligations"] == [] and boundary["root_closed"] is False
    assert boundary["root_machine_debt"] == "M3"
    assert boundary["remaining_root_cut_set"] == [
        "M1237-C", "M1237-L-HOLDER", "M1237-L-VALUE"
    ]
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "ObligationTree.lean", "Proof.lean", "ProofAudit.lean",
        "Validation.lean",
    ):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    differential = code_without_comments((HERE / "Validation.lean").read_text())
    for forbidden in ("import «Proof»", "Proof.", "not_valueEstimateFamily", "singletonSpike"):
        assert forbidden not in differential, forbidden
    assert "oneOnNullDomain" in differential
    assert "independentlyRefutedValueEstimateFamily" in differential
    assert "assert_no_sorry independentlyRefutedValueEstimateFamily" in differential

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert git("rev-parse", f"HEAD:{NO_ATOMS_SOURCE}", cwd=MATHLIB) == NO_ATOMS_BLOB
    assert git("rev-parse", f"HEAD:{LP_SOURCE}", cwd=MATHLIB) == LP_BLOB
    assert sha256(MATHLIB / NO_ATOMS_SOURCE) == NO_ATOMS_SHA256
    assert sha256(MATHLIB / LP_SOURCE) == LP_SHA256
    assert sha256(
        MATHLIB / ".lake/build/lib/lean/Mathlib/MeasureTheory/Measure/Typeclasses/NoAtoms.olean"
    ) == NO_ATOMS_OLEAN_SHA256
    assert sha256(
        MATHLIB / ".lake/build/lib/lean/Mathlib/MeasureTheory/Function/LpSeminorm/Basic.olean"
    ) == LP_OLEAN_SHA256
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    lake_version = run(["lake", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in lake_version
    python = Path(os.path.realpath(os.sys.executable))
    git_path = shutil.which("git")
    bwrap = shutil.which("bwrap")
    assert git_path is not None and bwrap is not None
    assert sha256(Path(lean)) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(Path(lake)) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert sha256(python) == "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
    assert sha256(Path(os.path.realpath(git_path))) == (
        "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
    )
    assert sha256(Path(os.path.realpath(bwrap))) == (
        "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
    )

    runner_output = run(["bash", str(HERE / "check_validation.sh")])
    runner_bytes = runner_output.encode("utf-8")
    assert hashlib.sha256(runner_bytes).hexdigest() == receipt["result"]["kernel_output_sha256"]
    assert len(runner_bytes) == receipt["result"]["kernel_output_bytes"]
    assert runner_output.count("Declarations are sorry-free!") == 5
    assert "sorryAx" not in runner_output and "declaration uses 'sorry'" not in runner_output
    assert receipt["result"]["observed_axioms"] == sorted(EXPECTED_AXIOMS)
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")

    # The dependency cache is shared, so reject a revision, source, or compiled-object race.
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / NO_ATOMS_SOURCE) == NO_ATOMS_SHA256
    assert sha256(MATHLIB / LP_SOURCE) == LP_SHA256
    assert sha256(
        MATHLIB / ".lake/build/lib/lean/Mathlib/MeasureTheory/Measure/Typeclasses/NoAtoms.olean"
    ) == NO_ATOMS_OLEAN_SHA256
    assert sha256(
        MATHLIB / ".lake/build/lib/lean/Mathlib/MeasureTheory/Function/LpSeminorm/Basic.olean"
    ) == LP_OLEAN_SHA256

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "Bubblewrap" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == [
        "M1237-S", "M1237-C", "M1237-L-VALUE", "M1237-X-TRUST", "M1237-T"
    ]
    for field in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
        "scope_boundary",
    ):
        assert receipt["recipe"][field] == spec[field], field

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["release_grade"] is False
    assert receipt["root_decision"] == {
        "machine_debt": "M3",
        "kernel_closed": False,
        "theorem_complete": False,
    }
    assert receipt["first_failed_gate"] == "proof.M1237-L-VALUE.invalid_frozen_interface"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["root_vector_before"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert receipt["root_vector_after_worker_selftest"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }

    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == [
        "python3 Docs/tools/check_stage1_standard.py",
        "python3 scripts/stage1_target.py check",
        "python3 scripts/stage1_target.py show THM-M-1237",
        "bash Stage1_Instances/THM-M-1237/check_validation.sh",
        "python3 -B Stage1_Instances/THM-M-1237/check_validation.py",
        "python3 -m json.tool Stage1_Instances/THM-M-1237/validation-spec.json",
        "python3 -m json.tool Stage1_Instances/THM-M-1237/validation-receipt.json",
        "python3 -m json.tool .stage1-worker-selftest.json",
        "git diff --check -- Stage1_Instances/THM-M-1237 .stage1-worker-selftest.json",
    ]
    assert packet["output_summary"] == list(SUMMARY_LINES)
    assert packet["known_failures"] == receipt["known_failures"]

    public_text = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("validation-phase.md", "validation-receipt.json")
    )
    assert "/home/" not in public_text and ".cron/" not in public_text
    assert '"theorem_complete": true' not in public_text
    changed = set(
        git(
            "status", "--porcelain=v1", "-uall", "--",
            f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
            "Formalizations/Lean/.lake",
        ).splitlines()
    )
    allowed_status = {f"?? {path}" for path in CHANGED_PATHS}
    allowed_status.add("?? Formalizations/Lean/.lake")
    assert changed == allowed_status, (changed, allowed_status)

    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
