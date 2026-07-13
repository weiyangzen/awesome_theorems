#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1553-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1553"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1553-VALIDATION"
THEOREM = "THM-M-1553"
BASE_REVISION = "f78ecdb166de720e4af8d8859826b4a22a4c1733"
BASE_TREE = "6d72b645f5722769d4ed5d9eea3559c9e4c69856"
EXPRESSION_SHA256 = "ef5d4bb909f3eba6d2a347e8bad055e3a4a08402beb725499259bb9bf1a9c3bc"
DENOMINATOR_SHA256 = "553f66664b7a640a7e299ac12a65bfcf668173fbfb556f179614ae1dd4fbfed1"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
MACHINE_IDS = [
    "M1553-ROOT",
    "M1553-S-CONTEXT",
    "M1553-N-HIROTA",
    "M1553-N-TRANSFORM",
    "M1553-L-REGULARITY",
    "M1553-L-LOG",
    "M1553-L-MIXED",
    "M1553-B-POLYNOMIAL",
    "M1553-T-ZERO",
    "M1553-T-ASSEMBLE",
    "M1553-S-BOUNDARY",
]
COVERED_IDS = MACHINE_IDS + ["M1553-X-PROVENANCE", "M1553-X-TRUST"]
EXPECTED_INPUTS = {
    "Statement.lean": "d5e88315d8d721409648fd87cbdfa08d6774567e73218a24040f4bda13670c32",
    "ObligationTree.lean": "20678d4d4da4c2b395762568edcd44699f6cb888348f1300da168eb6d11cd031",
    "ProofLemmas.lean": "f7eaf88193e7d1af86e9871ff975344e4bb49d614714bb77dee5d4c48e3e6cb2",
    "Proof.lean": "a1f1de80b12de4d124157474193d1199f33a5a54e57e90fc123e5bc365dfd8ec",
    "statement.json": "1317dfdae0ce90254dbd71249e7c684db25fdb10a0c9323dd1689fa4d1075bcb",
    "anchor-audit.json": "dcaa52f18c97f048251edfca4bf39b65b4a938c0b84231dc02a683afdec6c123",
    "obligation-registry.json": "216b591a11f219bbf32aafcae6d580d21cc777cf7edd55ca4af4c1f3d47556fc",
    "typed-graphs.json": "4c522e9ca5de8746f483e4ec522ee619eb71fa6633fe7a98d0e278dd0e24489e",
    "proof-receipt.json": "e7f31fe00fc47c7c5128c65e7d7a1ba70eb0a96d512a4ee21887adf49c1bdf6a",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
VALIDATION_INPUTS = {
    "Validation.lean": "549e596fa71279a1ebd9fbbd1d71ea4d1a71775dcf3df234d926ce3a17365c01",
    "check_validation.sh": "8cabc62bbf986f506f80a9c91a64ed69c40b19f2562d998e36d2870ec8cdd3f6",
    "validation-spec.json": "3312845aa86b644ec246d713d352ae6d31b89da16f078490a3853be0ed943d72",
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
    "PASS THM-M-1553 narrow validation",
    "PASS network-isolated kernel replay: exact statement, frozen composition, proof root, and differential root elaborated",
    "PASS trust observation: proof and validation declarations are sorry-free and report exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen input hashes, local proof-body location, clean mathlib pin, and tool identities agree",
    "FAIL CLOSED authority: proof is worker-self-tested but not master-accepted; authoritative graph remains pre-proof M3",
    "FAIL CLOSED foundation/trust: accepted axiom policy and complete transitive declaration, compiled-artifact, and TCB closure remain open",
    "FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout empty-cache bootstrap, offline restoration, or a deterministic TCB/SBOM bundle",
    "FAIL CLOSED independent release: the differential proof used this worker, shared lemmas, checkout, kernel, and cache, not a distinct signed verifier",
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
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 212 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 212,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1553-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1553-PROOF"
    )
    assert predecessor["state"] == "[_]"

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    for name, expected in VALIDATION_INPUTS.items():
        assert sha256(HERE / name) == expected, f"changed validation input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1553.HirotaKdVTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == "M1553-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == ["M1553-B-POLYNOMIAL", "M1553-T-ZERO"]
    assert proof_receipt["item_id"] == "S56-M-1553-PROOF"
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["proof_body"]["lemmas_sha256"] == EXPECTED_INPUTS["ProofLemmas.lean"]
    assert proof_receipt["result"]["root_machine_proof_body_present"] is True
    assert proof_receipt["result"]["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    lean_sources = (
        "Statement.lean", "ObligationTree.lean", "ProofLemmas.lean",
        "Proof.lean", "Validation.lean",
    )
    for name in lean_sources:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = re.sub(r"^#print sorries .*?$", "", source, flags=re.MULTILINE)
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    differential = code_without_comments((HERE / "Validation.lean").read_text())
    for forbidden in (
        "import Proof\n", "import «ObligationTree»", "logarithmic_bilinear_identity",
        "logDerivativeBridge", "hirotaKdVTarget_proof",
        "hirotaKdVTarget_of_logDerivativeBridge",
    ):
        assert forbidden not in differential, forbidden
    assert "theorem independentlyReconstructedHirotaKdVTarget : HirotaKdVTarget" in differential
    assert "assert_no_sorry independentlyReconstructedHirotaKdVTarget" in differential

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    lake_version = run(["lake", "env", "lake", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in lake_version
    python = Path(os.path.realpath(sys.executable))
    git_path = Path(os.path.realpath(shutil.which("git") or ""))
    bwrap = Path(os.path.realpath(shutil.which("bwrap") or ""))
    assert sha256(lean) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(lake) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert sha256(python) == "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
    assert sha256(git_path) == "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
    assert sha256(bwrap) == "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"

    runner_output = run(["bash", str(HERE / "check_validation.sh")])
    declarations = (
        "Stage1Instances.THM_M_1553.hirotaKdVTarget_of_logDerivativeBridge",
        "Stage1Instances.THM_M_1553.logarithmic_bilinear_identity",
        "Stage1Instances.THM_M_1553.logDerivativeBridge",
        "Stage1Instances.THM_M_1553.hirotaKdVTarget_proof",
        "Stage1Instances.THM_M_1553.Validation."
        "independentlyReconstructedLogarithmicIdentity",
        "Stage1Instances.THM_M_1553.Validation."
        "independentlyReconstructedHirotaKdVTarget",
    )
    for declaration in declarations:
        assert printed_axioms(runner_output, declaration) == EXPECTED_AXIOMS
    assert runner_output.count("Declarations are sorry-free!") == 5
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
    assert spec["covered_obligation_ids"] == COVERED_IDS
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact nine-line PASS/FAIL-CLOSED status summary",
    }]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1553-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["covered_obligation_ids"] == COVERED_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    for name, expected in VALIDATION_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
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
    assert result["differential_exact_root_replay"] == "provisional_pass_same_worker_shared_lemmas"
    assert result["observed_axioms"] == EXPECTED_AXIOM_LIST
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["selected_provenance"] == "pass"
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_root_closed"] is False
    assert result["foundation_and_complete_trust_closure"] == "fail_closed"
    assert result["complete_provenance_closure"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1553-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    notes = (HERE / "validation-phase.md").read_text(encoding="utf-8")
    assert "same-worker differential" in notes
    assert "empty-cache cold bootstrap" in notes
    assert "theorem completion remain false" in notes
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
