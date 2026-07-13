#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1522-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1522"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1522-VALIDATION"
THEOREM = "THM-M-1522"
BASE_REVISION = "0afbf514f9bd5f339943542106f6b811869fe572"
BASE_TREE = "adbd9c80e360931a3e7c51cae73dda809b5bed65"
EXPRESSION_SHA256 = "1ae3d8a352060fb26372a07d0128af2f465933e4c3c08b6c752b0b5fe72c83b5"
DENOMINATOR_SHA256 = "8a9a7f243137efb0ac3ebafe2b5de3a292f41bcb0cc6bdc4a1a6adc364fb3242"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
UPSTREAM_REVISION = "ed3fa6b8a30594eeb791160563942ba115581aa0"
UPSTREAM_MAXIMAL_SHA256 = "6b9c40bd0e8d7238919283ad8666d0563d780a3b31eeb67d0ca66aae821817cc"
UPSTREAM_BIRKHOFF_SHA256 = "bed8d81c6eb7f0ba74548255779dad7c3dc4e75ecf7ad935e1c68ef6fcb6ea6a"
UPSTREAM_ARCHIVE_SHA256 = "3c0ef177500430ab55950061cfd73991347f5336b5b3d5032ffe46ac56009a52"
TARGET_LICENSE_SHA256 = "cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
MACHINE_IDS = [
    "M1522-ROOT",
    "M1522-S-DEFINITIONS",
    "M1522-S-DOMAIN",
    "M1522-S-BOUNDARY",
    "M1522-S-TRANSPORT",
    "M1522-S-FOUNDATION",
    "M1522-N-GENERAL",
    "M1522-C-LIMIT-DATA",
    "M1522-L-POINTWISE",
    "M1522-B-ERGODIC",
    "M1522-L-INTEGRAL-ID",
    "M1522-T-IDENTIFY",
    "M1522-T-ASSEMBLE",
    "M1522-X-UPSTREAM",
]
EXPECTED_INPUTS = {
    "Statement.lean": "2ef66fbbe0b1f6130270ff944ae95df04bc688f15e8009a6ceef5a4d28f9d87c",
    "MaximalErgodic.lean": "af39bb1048599b97b58f4a982cc7de8a379b2f54597d0c3aba08ca476b01924d",
    "Birkhoff.lean": "d78b7eaa868ed59d8ed852649d309fd4388630b99e1c3498b09e34ade5e74f06",
    "ObligationTree.lean": "4b540d4dc61e36e20afe53d228d4aee7b0f022f046c540767654c93f8b1cdc4f",
    "Proof.lean": "f75d7d98d250bb557188c8a44139d7d5ce05275bd91962f37e51e619aaba797f",
    "statement.json": "2812ad428abf680cd4ee518b780b80697cb1fd008c8bbf9c7736ea77f6bd3e75",
    "anchor-audit.json": "131a286180faec74ffbf95803269dbb0d4119ab2a2cdb95105d322e1dc697e7f",
    "obligation-registry.json": "46e2fee724bfbd90b554b02daabe0d73d9c9b8eaded63851aad9f80fcf6c52dd",
    "typed-graphs.json": "9506ce707579e0055afd1ad1edd04ae97bc4dcbc993c04c9db5294647cd935cc",
    "proof-receipt.json": "262d47cd3aee6b7ea0fa92339208a88ae3b13722008ac3f668c023442783346e",
    "PORT_PROVENANCE.md": "7f795116873bd03d9be801d54791750eede38ad03bc1a46d12fe0e12f939655d",
    "LICENSE": TARGET_LICENSE_SHA256,
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MATHLIB_SOURCES = {
    "Mathlib/Dynamics/BirkhoffSum/Average.lean": {
        "blob": "c6b32577397be7f5df109128ba63c2c6b82d1772",
        "sha256": "806ac5104deed43f15adc7854be78c5eaa22483148a0733f03e4d772ac227c34",
    },
    "Mathlib/Dynamics/Ergodic/Ergodic.lean": {
        "blob": "d07e6257a84d3756217b5b692b5c86edccbe9bc7",
        "sha256": "853dac930e9abd11a440ad1a6b1390d34a33ed09a5c96915b623196e943ac0f4",
    },
    "Mathlib/Dynamics/Ergodic/Function.lean": {
        "blob": "86b366bccf56d55b262b59157fef5d227cf68063",
        "sha256": "9767f751f891a797ae46fc6715a830de83dc0b6a5c0661d62cd0205ba98e93c0",
    },
    "Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean": {
        "blob": "684a5cc254c1e01d9dc48c99e6dc605b95275b82",
        "sha256": "572455e8b2d197efe5001ad3b1673a0894337aaa79cb19fd2260f1c1aff7f8ea",
    },
    "Mathlib/MeasureTheory/MeasurableSpace/Invariants.lean": {
        "blob": "2fc1fef927a4dd087178861e43dd2eacc70deae8",
        "sha256": "33c9aed9097b72edd9ddd349bba9f31fad56e8e369f40cf1dff61324efb24879",
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
    "PASS THM-M-1522 narrow validation",
    "PASS network-isolated kernel replay: exact statement, vendored terminals, frozen composition, two proof roots, and differential root elaborated",
    "PASS trust observation: proof and validation declarations are sorry-free and report exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, reconstructed upstream sources, clean mathlib pin, selected source blobs, licenses, and tools agree",
    "FAIL CLOSED authority: proof is only worker-self-tested and the authoritative graph remains M3 with the pre-proof open cut set",
    "FAIL CLOSED foundation/trust: M1522-S-FOUNDATION and complete transitive declaration, compiled-artifact, and TCB closure remain open",
    "FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout empty-cache bootstrap, offline restoration, or a deterministic TCB/SBOM bundle",
    "FAIL CLOSED independent release: the differential proof used this worker and shared cache, not a distinct signed verifier",
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


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
    assert target["execution_rank"] == 190 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 190,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1522-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1522-PROOF"
    )
    assert predecessor["state"] == "[_]"

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1522.BirkhoffPointwiseErgodicTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert anchor["canonical_target"] == (
        "Stage1Instances.THM_M_1522.BirkhoffPointwiseErgodicTarget"
    )
    assert anchor["machine_classification"] == "M3"
    assert registry["frozen_against_statement_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_machine_debt"] == "M3"
    assert closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == [
        "M1522-L-POINTWISE", "M1522-T-IDENTIFY"
    ]
    composition = graphs["composition_certificate"]
    assert composition["parent"] == "M1522-ROOT"
    assert composition["children"] == ["M1522-L-POINTWISE", "M1522-T-IDENTIFY"]
    assert proof_receipt["item_id"] == "S56-M-1522-PROOF"
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["proof_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["proof_body"]["maximal_port_sha256"] == EXPECTED_INPUTS["MaximalErgodic.lean"]
    assert proof_receipt["proof_body"]["birkhoff_port_sha256"] == EXPECTED_INPUTS["Birkhoff.lean"]
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
        "Statement.lean", "MaximalErgodic.lean", "Birkhoff.lean",
        "ObligationTree.lean", "Proof.lean", "Validation.lean",
    )
    for name in lean_sources:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    differential = code_without_comments(
        (HERE / "Validation.lean").read_text(encoding="utf-8")
    )
    for forbidden in (
        "import Proof", "import ObligationTree", "generalPointwiseLimitPackage",
        "ergodicInvariantLimitIdentification", "birkhoffPointwiseErgodicDirect",
        "birkhoffPointwiseErgodicViaFrozenComposition",
    ):
        assert forbidden not in differential, forbidden
    assert "ErgodicTheory.tendsto_birkhoffAverage_ae_integral hT hf" in differential
    assert "assert_no_sorry independentlyReconstructedBirkhoffPointwiseErgodic" in differential

    maximal = (HERE / "MaximalErgodic.lean").read_bytes()
    birkhoff = (HERE / "Birkhoff.lean").read_bytes()
    notice_maximal = (
        b"/-\nPort note: this file is modified from\n"
        + f"`marcmorningstar/lean4-ergodic-theory@{UPSTREAM_REVISION}`.\n".encode()
        + b"The sole compatibility change is the pinned-mathlib spelling\n"
        + b"`integrable_finset_sum`; see `PORT_PROVENANCE.md`.\n-/\n"
    )
    notice_birkhoff = (
        b"/-\nPort note: this file is modified from\n"
        + f"`marcmorningstar/lean4-ergodic-theory@{UPSTREAM_REVISION}`.\n".encode()
        + b"Only the sibling module import below is target-local; see `PORT_PROVENANCE.md`.\n-/\n"
    )
    assert maximal.count(notice_maximal) == birkhoff.count(notice_birkhoff) == 1
    upstream_maximal = maximal.replace(notice_maximal, b"", 1).replace(
        b"integrable_finset_sum", b"integrable_finsetSum", 1
    )
    upstream_birkhoff = birkhoff.replace(notice_birkhoff, b"", 1).replace(
        b"import MaximalErgodic", b"import ErgodicTheory.Ergodic.MaximalErgodic", 1
    )
    assert sha256_bytes(upstream_maximal) == UPSTREAM_MAXIMAL_SHA256
    assert sha256_bytes(upstream_birkhoff) == UPSTREAM_BIRKHOFF_SHA256
    origin = proof_receipt["proof_body"]["origin"]
    assert origin["revision"] == UPSTREAM_REVISION
    assert origin["archive_sha256"] == UPSTREAM_ARCHIVE_SHA256
    assert origin["maximal_source_sha256"] == UPSTREAM_MAXIMAL_SHA256
    assert origin["birkhoff_source_sha256"] == UPSTREAM_BIRKHOFF_SHA256
    assert origin["license_sha256"] == TARGET_LICENSE_SHA256

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
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

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
    proof_declarations = (
        "ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg",
        "ErgodicTheory.tendsto_birkhoffAverage_ae",
        "ErgodicTheory.tendsto_birkhoffAverage_ae_integral",
        "Stage1Instances.THM_M_1522.generalPointwiseLimitPackage",
        "Stage1Instances.THM_M_1522.ergodicInvariantLimitIdentification",
        "Stage1Instances.THM_M_1522.birkhoffPointwiseErgodicViaFrozenComposition",
        "Stage1Instances.THM_M_1522.birkhoffPointwiseErgodicDirect",
        "Stage1Instances.THM_M_1522.Validation."
        "independentlyReconstructedBirkhoffPointwiseErgodic",
    )
    for declaration in proof_declarations:
        assert printed_axioms(runner_output, declaration) == EXPECTED_AXIOMS
    assert runner_output.count("Declarations are sorry-free!") == 11
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
    assert receipt["depends_on"] == ["S56-M-1522-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["Validation.lean"] == sha256(HERE / "Validation.lean")
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["check_validation.sh"] == sha256(HERE / "check_validation.sh")
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
    assert result["differential_exact_root_replay"] == "provisional_pass_same_worker"
    assert result["observed_axioms"] == EXPECTED_AXIOM_LIST
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["selected_provenance"] == "pass"
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_root_closed"] is False
    assert result["foundation_and_complete_trust_closure"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1522-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    phase_notes = (HERE / "validation-phase.md").read_text(encoding="utf-8")
    assert "same-worker differential" in phase_notes
    assert "empty-cache cold bootstrap" in phase_notes
    assert "theorem completion remain false" in phase_notes
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
