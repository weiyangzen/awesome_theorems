#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1285-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1285"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1285-VALIDATION"
THEOREM = "THM-M-1285"
BASE_REVISION = "be35cd8f5123e9d06247b12859f3843bdd90c66f"
BASE_TREE = "a275a21a449fbcbd6c2333f5cfe737e906b20db6"
EXPRESSION_SHA256 = "ffce741885f8c5eeb87a6dd893e7c5bf6ccc7a7f88fcc37e9fdd8750ab2d41ac"
DENOMINATOR_SHA256 = "6e441bf6a37b0bb83ae0a752e94b30ebf47c8eb567a9284969e869f68b032e9c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
MACHINE_IDS = [
    "M1285-ROOT", "M1285-S-INTERFACE", "M1285-S-FOUNDATION",
    "M1285-D-DISTRIBUTION", "M1285-L-DISTRIBUTION", "M1285-C-INVERSE",
    "M1285-C-RADIUS", "M1285-C-WITNESS", "M1285-L-MEASURABLE",
    "M1285-L-RADIAL", "M1285-L-ANTITONE", "M1285-L-EQUIMEASURABLE",
    "M1285-T-PACKAGE", "M1285-T-ASSEMBLE",
]
PROOF_DECLARATIONS = [
    "Stage1Instances.THM_M_1285.isRadial_profile",
    "Stage1Instances.THM_M_1285.isRadiallyNonincreasing_profile",
    "Stage1Instances.THM_M_1285.measurable_profile",
    "Stage1Instances.THM_M_1285.distribution_antitone",
    "Stage1Instances.THM_M_1285.iUnion_strictSuperlevel_gt",
    "Stage1Instances.THM_M_1285.distribution_iSup_rat_gt",
    "Stage1Instances.THM_M_1285.volume_ball_radiusForVolume",
    "Stage1Instances.THM_M_1285.radiusForVolume_nonneg",
    "Stage1Instances.THM_M_1285.radiusForVolume_mono",
    "Stage1Instances.THM_M_1285.starProfile_measurable",
    "Stage1Instances.THM_M_1285.starProfile_antitone",
    "Stage1Instances.THM_M_1285.strictSuperlevel_starProfile",
    "Stage1Instances.THM_M_1285.measure_strictSuperlevel_starProfile",
    "Stage1Instances.THM_M_1285.schwarzRearrangementTarget_proof",
]
EXPECTED_INPUTS = {
    "Statement.lean": "5b3e9ec5606263ee7aac7cd59ba0c7c91c1f8017ba41ada01f8c0327528ac5e6",
    "ObligationTree.lean": "02c170e403d2a42c334f0c0817b5ba0366e82e97a7e35cfb88d136479d5d35a0",
    "Proof.lean": "bb9581ad1b9840d95c7a37b66221dd5234b5730268f6173efc9e8892bc07a8fb",
    "statement.json": "978a9e3b662dcb60932aad407b65d1b9f0b6680b04586e0f3844e8019c430c65",
    "anchor-audit.json": "25b578433367fffa235a26d7b2331f9d0c536117ee0371f8d9aec9e32a99127f",
    "obligation-registry.json": "b3efcc1e3e14dcf4798268f8017f67a924c0c25a996bea06255d9ed3cc4ef68a",
    "typed-graphs.json": "e97017ba4c2f659866a5ce8fff8f3cd6a2e7b32191f04b8c9d98353fe320d219",
    "proof-receipt.json": "158f2338a037bb96e45583c16e0d3a7b62266097658d637b797dfb549fa6b6ad",
    "source_statement_crosswalk.md": "2a262a08d72f60101bbdee90a628cbbd9877333b87031b886e1955e7a7c09e99",
    "check_obligation_tree.py": "2bc4554d558f3351b351ac7886ce15bc79236b08d45c8d965f03efd55e5b4966",
    "Validation.lean": "b90b4862c49309ba764e526af45c3ec8bffab648e272a2d21ee4f240ebd855eb",
    "check_validation.sh": "3dfb2568142f8282c011380f617454b9baaafb3e4f4660b8c801f5e19611e003",
    "validation-spec.json": "b36c5b4ebf83828f016aab9e03946149cd49bb569c9598add4ebbf09e9041969",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
SELECTED_MATHLIB_SOURCES = {
    "Mathlib/MeasureTheory/Measure/Haar/InnerProductSpace.lean": (
        "fc7fbcde914fd92e72570f5251c1673375dd540d",
        "a152589d44e44992a6b9ba7763ab37f8230ba10c6e90052b5fb54004bc27af31",
    ),
    "Mathlib/MeasureTheory/Measure/Lebesgue/VolumeOfBalls.lean": (
        "09c30c53a7e7805e28222549f6d30558ac2cac67",
        "a4fe84dfb7419d46de17ced885299a9f1d60626ab8b4aa912ecfd3af31cec895",
    ),
}
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
]
SUMMARY_LINES = [
    "PASS THM-M-1285 narrow validation",
    "PASS network-isolated trust-zero kernel replay: exact statement, conditional composition, complete local proof, and trust probe elaborated",
    "PASS hygiene: Lean transitive sorry collectors and a nested-comment-aware prohibited-construct scan passed",
    "PASS selected provenance: frozen hashes, proof-body identity, mathlib source/blob/license, clean pin, and tool identities agree",
    "FAIL CLOSED authority: proof is provisional; registry and graphs accept no proof evidence; accepted root remains H2/M3/R3",
    "FAIL CLOSED node coverage: planned fingerprints and missing body, composition, evidence, and provenance links require master reconciliation",
    "FAIL CLOSED foundation/trust: observed axioms are unaccepted and complete transitive declaration, compiled-artifact, and TCB closure are absent",
    "FAIL CLOSED hermetic release: shared warm .lake is not an empty-cache clean-checkout offline replay or deterministic bundle",
    "FAIL CLOSED independent release: the trust probe shares this worker, checkout, kernel, and cache; no distinct signed runner or minimal verifier exists",
    "audit_complete=false; theorem_complete=false",
]
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 900.0


if sys.flags.optimize:
    raise SystemExit("validation failed: Python optimization disables assertions")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 900) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 900-second wall-clock bound")
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=min(timeout, remaining), check=False,
    )
    if result.returncode:
        raise RuntimeError(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    output: list[str] = []
    depth = 0
    index = 0
    while index < len(source):
        if source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            index += 1
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def assert_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 456 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 456
    assert item["phase"] == "validation" and item["layer"] == 5
    assert item["state"] == "[ ]" and item["depends_on"] == ["S56-M-1285-PROOF"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1285-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] >= 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1285.SchwarzRearrangementTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "minimal_open_root_cut": ["M1285-T-PACKAGE"],
        "root_closed": False,
        "root_machine_debt": "M3",
        "theorem_complete": False,
    }

    assert proof_receipt["item_id"] == "S56-M-1285-PROOF"
    assert proof_receipt["accepted"] is False and proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["proof_body"]["terminal_declaration"] == PROOF_DECLARATIONS[-1]
    assert set(proof_receipt["result"]["axioms"]) == EXPECTED_AXIOMS
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["theorem_complete"] is False
    assert set(proof_receipt["provisionally_closed_obligation_ids"]) < set(MACHINE_IDS)

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-1285-VALIDATION-narrow-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["timeout_seconds"] == 900 and spec["network_policy"] == "denied"
    assert spec["covered_obligation_ids"] == MACHINE_IDS
    assert set(PROOF_DECLARATIONS) <= set(spec["covered_declarations"])

    combined = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    )
    stripped = code_without_comments(combined)
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b"
        r"|^[ \t]*(?:(?:private|protected|noncomputable|scoped|local)\s+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(stripped) is None
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    assert re.search(r"^[ \t]*(?:theorem|lemma|def|opaque|axiom)\b", validation_source, re.MULTILINE) is None
    assert "import Proof" in validation_source and "import ObligationTree" in validation_source
    for declaration in PROOF_DECLARATIONS:
        assert f"assert_no_sorry {declaration}" in validation_source
        assert f"#print sorries {declaration}" in validation_source
        assert f"#print axioms {declaration}" in validation_source

    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    assert anchor["immutable_environment"]["mathlib_revision"] == MATHLIB_REVISION
    for name, (blob, digest) in SELECTED_MATHLIB_SOURCES.items():
        assert git("rev-parse", f"HEAD:{name}", cwd=MATHLIB) == blob
        assert sha256(MATHLIB / name) == digest

    tool_hashes = receipt["environment"]["tool_hashes"]
    for name, path in {
        "python3": Path(sys.executable),
        "git": Path(run(["bash", "-lc", "command -v git"]).strip()),
        "bash": Path("/usr/bin/bash"),
        "bubblewrap": Path("/usr/bin/bwrap"),
        "elan": Path(run(["bash", "-lc", "command -v elan"]).strip()),
    }.items():
        assert sha256(path) == tool_hashes[name]
    assert (LEAN_ROOT / "lean-toolchain").read_text(encoding="utf-8").strip() == LEAN_TOOLCHAIN
    lean_path = Path(run(["elan", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake_path = Path(run(["elan", "which", "lake"], cwd=LEAN_ROOT).strip())
    assert sha256(lean_path) == tool_hashes["lean"]
    assert sha256(lake_path) == tool_hashes["lake"]
    assert LEAN_COMMIT in run([str(lean_path), "--version"])

    replay = run(["bash", str(HERE / "check_validation.sh")])
    replay_sha256 = hashlib.sha256(replay.encode()).hexdigest()
    assert replay_sha256 == receipt["result"]["kernel_output_sha256"]
    assert len(replay.encode()) == receipt["result"]["kernel_output_bytes"]
    for declaration in PROOF_DECLARATIONS:
        assert f"'{declaration}' depends on axioms:" in replay
    assert replay.count("Declarations are sorry-free!") == 16
    assert "sorryAx" not in replay and "error:" not in replay

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["output_summary"] == SUMMARY_LINES
    assert receipt["changed_paths"] == CHANGED_PATHS
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["trust"]["accepted_foundation_policy"] is False
    assert receipt["independent_validation"]["distinct_runner"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1285-PROOF.master_acceptance"

    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert packet["changed_paths"] == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == SUMMARY_LINES
    assert packet["commands"] == receipt["commands"]

    for name in CHANGED_PATHS:
        assert_hygiene(ROOT / name)
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
