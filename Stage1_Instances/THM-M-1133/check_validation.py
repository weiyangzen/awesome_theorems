#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1133-VALIDATION."""

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
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1133"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1133-VALIDATION"
THEOREM = "THM-M-1133"
BASE_REVISION = "bad90e2e2479d376609447202eb4f437789d0d11"
BASE_TREE = "df3ade7b4d06057f8aac33369c3d69bd391aa05a"
EXPRESSION_SHA256 = "cb70ff9396c3c5fad0ea98bf234dc38f20738f5ff2accc32b4712675e90e5c3b"
DENOMINATOR_SHA256 = "8ae5b9f05fb5913dcb53d061df667c4fcbc5343c208bd22cba9c7f78ef506fd6"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_EXECUTABLE_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_EXECUTABLE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_EXECUTABLE_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_EXECUTABLE_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
BWRAP_EXECUTABLE_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 600

FROZEN_INPUT_HASHES = {
    "Statement.lean": "63e7f31ae3f3b1a8d0a06836f6afe31960fa1cb0c461922eaf69c08cedcd7bee",
    "ObligationTree.lean": "1ec64c882d599a5ee2c40c441e1cc7dd5c6635c21f6debd25cdcc49e4a54b6d2",
    "Proof.lean": "5f6ca5374c7f3666475f9d0b27a298b3138ed0daa3d5b5fb0c8ad9e38ebea4fe",
    "statement.json": "caf73f64adbe2900f0f030bda0361b37056b8c1b6b678107ae005ff71e29e379",
    "anchor-audit.json": "4898f449ad4acfafdf94fc14fb9affb56f20f64acdad0818cae9ad39b97b2c09",
    "obligation-registry.json": "a80612db8440ab7249994fd5e732beda9a54177cba06673e896268b4c58b3801",
    "typed-graphs.json": "867ec2cd3456c748416716d2a70dc028d8127b94cb0034b17a042f267262ac10",
    "proof-receipt.json": "ec8b25511ffafc8be6cfb92119cf7c05839a26e3248dff3405ffcf6c25e4e92f",
    "source_statement_crosswalk.md": "2dbdb59a9d5806911e3f7604c71565fcc996aa4a244622470361fb63162d9940",
    "validation-specs.json": "777d6eb29552f2b18d046dd471596185ae5e1b3c53ff3b24b82eb5658b744945",
}

DIRECT_MATHLIB_SURFACES = {
    "Mathlib/Analysis/Calculus/ContDiff/Basic.lean": (
        "c3da4bad51dbed2870e5a92284953176992b5a04bc959a4c3284f63411ad52d4",
        "b2d73b6e964ed930bc8db763568dea3578ba0b60808a6f59b8b8055e6ec66b1e",
    ),
    "Mathlib/Analysis/InnerProductSpace/PiL2.lean": (
        "4df49dd497992b022f3d18ee79ea0ae5536be7a452779b4c2400b1d136b7a2bb",
        "b421e082ec7b4bfab92f0fd05c51968deb0933812e975beec781bdab0a826ea4",
    ),
    "Mathlib/Analysis/Calculus/DerivativeTest.lean": (
        "4d89b7883a04a373e0dc4d73b0163a7542a690249d9316509701e96074fb7dbb",
        "e16cab82cfcf4ca5b58c533ee745886cfd088b745aca3efb4231cb58ad731a8a",
    ),
    "Mathlib/Analysis/Calculus/ContDiff/Operations.lean": (
        "8c379c8bc1c1203e2573f1d5d423b4f3cf1ecee458b59731b01ccd6d3ddd03fe",
        "4d7f2fd73c05cf83b979b10dd59e41b9e062c2b23356c202f5004c5a83b5076e",
    ),
    "Mathlib/Analysis/Calculus/IteratedDeriv/Defs.lean": (
        "b3640de8496ae13884cf729bc255521580f95890fdca123354c97570d7ed24ff",
        "52b88f5c20362ab24e3a747012f6351050a6a3b2a865ffdba0a768f3ff6c1619",
    ),
    "Mathlib/Analysis/Calculus/FDeriv/CompCLM.lean": (
        "b2247b2964fc7508b785d65ee0f33f23478e586c16faa99757f8c126bb182ff9",
        "b1361c118f521252da828561622ebc56810cc3ce0765fcb3c78698b2d5c96f24",
    ),
    "Mathlib/Analysis/Calculus/Deriv/Mul.lean": (
        "8f43e7deca19d616824a91d97b5a6bbdeff47861b5b8c9303d8c296f287cd7f0",
        "e009eeb0ae0cd091a8053ad006d46a674297acad5bd2159dfcb46bd150470c09",
    ),
}

PROOF_AXIOM_DECLARATIONS = (
    "Stage1Instances.THM_M_1133.second_deriv_nonpos_of_localMax",
    "Stage1Instances.THM_M_1133.iteratedFDeriv_diag_nonpos_of_localMax",
    "Stage1Instances.THM_M_1133.spatialLaplacian_nonpos_of_localMax",
    "Stage1Instances.THM_M_1133.deriv_nonneg_of_isLocalMaxOn_Iic",
    "Stage1Instances.THM_M_1133.strictSubsolutionMaximumPrinciple",
    "Stage1Instances.THM_M_1133.perturb_isStrictSubcaloric",
    "Stage1Instances.THM_M_1133.weakSubsolutionMaximumPrinciple",
    "Stage1Instances.THM_M_1133.heatEquationWeakMaximumPrinciple",
)
COMPOSITION_AXIOM_DECLARATIONS = (
    "Stage1Instances.THM_M_1133.caloric_isSubcaloric",
    "Stage1Instances.THM_M_1133.root_of_subsolutionMaximumPrinciple",
)
ALL_OBLIGATION_IDS = {
    "M1133-ROOT", "M1133-S-INTERFACE", "M1133-S-BOUNDARY",
    "M1133-S-FOUNDATION", "M1133-N-SUBSOLUTION", "M1133-N-PERTURB",
    "M1133-L-EXTREMUM", "M1133-B-LOCATION", "M1133-L-SPATIAL",
    "M1133-B-TIME", "M1133-L-TIME", "M1133-T-STRICT",
    "M1133-T-LIMIT", "M1133-T-ASSEMBLE", "M1133-X-SOURCE",
    "M1133-X-PROVENANCE",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}


def fail(message: str) -> None:
    print(f"validation: FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def require(value: bool, message: str) -> None:
    if not value:
        fail(message)


def load(path: Path) -> dict:
    require(path.is_file(), f"required artifact is missing: {path.name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path.name} must contain a JSON object")
    return value


def digest(path: Path) -> str:
    require(path.is_file(), f"required artifact is missing: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def run(
    argv: list[str], *, cwd: Path, env: dict[str, str] | None = None
) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    require(remaining > 0, "whole validation recipe timed out")
    try:
        result = subprocess.run(
            argv,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=remaining,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        fail(f"command timed out: {argv!r}\n{error.stdout or ''}")
    if result.returncode:
        fail(f"command exited {result.returncode}: {argv!r}\n{result.stdout}")
    return result.stdout


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    """Remove nested Lean block comments and line comments for a defense scan."""
    output: list[str] = []
    index = 0
    depth = 0
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
            end = source.find("\n", index)
            if end < 0:
                break
            output.append("\n")
            index = end + 1
        else:
            output.append(source[index])
            index += 1
    require(depth == 0, "unterminated Lean block comment")
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output,
        re.DOTALL,
    )
    require(match is not None, f"missing axiom report for {declaration}")
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def check_text_file(path: Path) -> None:
    data = path.read_bytes()
    require(data.endswith(b"\n"), f"missing final newline: {path}")
    require(b"\r" not in data and b"\x00" not in data, f"invalid byte: {path}")
    require(
        all(not line.endswith((b" ", b"\t")) for line in data.splitlines()),
        f"trailing whitespace: {path}",
    )


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    require(git_output("rev-parse", "HEAD") == BASE_REVISION, "base revision drifted")
    require(git_output("rev-parse", "HEAD^{tree}") == BASE_TREE, "base tree drifted")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    require(item["theorem_id"] == THEOREM, "execution item theorem drifted")
    require(item["execution_rank"] == 338 and item["phase"] == "validation", "wrong execution node")
    require(item["state"] == "[ ]" and item["depends_on"] == ["S56-M-1133-PROOF"], "execution dependency state drifted")
    require(item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"], "owned path drifted")

    require(spec["schema_version"] == "stage1-validation-spec/1.0", "wrong validation spec schema")
    require(spec["item_id"] == receipt["item_id"] == ITEM, "wrong validation item")
    require(spec["theorem_id"] == receipt["theorem_id"] == THEOREM, "wrong theorem")
    require(spec["argv"] == ["/usr/bin/python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"], "recipe argv drifted")
    require(spec["cwd"] == "." and spec["expected_exit"] == 0, "recipe cwd/exit drifted")
    require(spec["env_allowlist"] == {}, "recipe environment allowlist drifted")
    require(spec["timeout_seconds"] == RECIPE_TIMEOUT_SECONDS, "recipe timeout drifted")
    require(spec["network_policy"] == "denied", "recipe must deny network")
    require("isolated network namespace" in spec["network_enforcement"], "network enforcement drifted")
    require(set(spec["covered_obligation_ids"]) == ALL_OBLIGATION_IDS, "recipe obligation coverage drifted")
    require(set(spec["obligation_evidence_map"]) == ALL_OBLIGATION_IDS, "obligation evidence map is incomplete")
    require("Stage1Instances.THM_M_1133.heatEquationWeakMaximumPrinciple" in spec["covered_declarations"], "root declaration is not covered")
    require("Stage1Instances.THM_M_1133.Validation.exactRootProbe" in spec["covered_declarations"], "exact-type probe is not covered")

    for name, expected in FROZEN_INPUT_HASHES.items():
        require(digest(HERE / name) == expected, f"frozen input hash mismatch: {name}")
    require(statement["canonical_formal_target"]["statement_file_sha256"] == digest(HERE / "Statement.lean"), "statement record does not bind Statement.lean")
    require(statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256, "canonical expression fingerprint drifted")
    require(registry["denominator_sha256"] == DENOMINATOR_SHA256, "registry denominator drifted")
    require(graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256, "graph denominator drifted")
    require(registry["root_obligation_id"] == graphs["root_node_id"] == "M1133-ROOT", "root ID drifted")
    require({row["obligation_id"] for row in registry["obligations"]} == ALL_OBLIGATION_IDS, "registry obligation set drifted")
    require(proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean"), "proof receipt does not bind Proof.lean")
    require(proof_receipt["result"]["root_kernel_closed"] is True, "proof receipt does not claim local root closure")
    require(proof_receipt["result"]["accepted_root_closed"] is False, "proof receipt overstates acceptance")
    require(proof_receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"], "proof axiom record drifted")
    require(proof_receipt["accepted"] is False and proof_receipt["proposed_state"] == "[_]", "proof prerequisite is not provisional")
    require(anchor["canonical_target"] == "Stage1Instances.THM_M_1133.HeatEquationWeakMaximumPrinciple", "anchor target drifted")
    require("Dimension n = 0 remains quantified but cannot satisfy" in statement["degenerate_cases"], "inherited n=0 record boundary changed")
    crosswalk = (HERE / "source_statement_crosswalk.md").read_text(encoding="utf-8")
    for pending in (
        "exact theorem/page, scanned edition hash, assumptions, and errata remain unaccepted",
        "No `H0` or machine-closure claim is made",
        "obtain independent review",
    ):
        require(pending in crosswalk, "source-fidelity boundary drifted")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(?:axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        require(prohibited.search(source) is None, f"prohibited mechanism in {name}")
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    require("import «Stage1_Instances».«THM-M-1133».Proof" in validation_source, "validation probe must bind the proof module")
    require("theorem exactRootProbe : HeatEquationWeakMaximumPrinciple" in validation_source, "missing exact-root probe")

    require(digest(LEAN_ROOT / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256, "Lean toolchain file drifted")
    require(digest(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256, "Lake manifest drifted")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    require(mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION, "manifest mathlib pin drifted")
    require(MATHLIB.resolve().is_dir(), "canonical pinned mathlib artifacts are missing")
    require(git_output("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION, "mathlib checkout revision drifted")
    require(git_output("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE, "mathlib tree drifted")
    require(git_output("status", "--porcelain=v1", cwd=MATHLIB) == "", "mathlib source checkout is dirty")
    require(git_output("remote", "get-url", "origin", cwd=MATHLIB) == "https://github.com/leanprover-community/mathlib4.git", "mathlib origin drifted")
    require(digest(MATHLIB / "LICENSE") == "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1", "mathlib license drifted")
    for relative, (source_hash, olean_hash) in DIRECT_MATHLIB_SURFACES.items():
        source = MATHLIB / relative
        olean = MATHLIB / ".lake" / "build" / "lib" / "lean" / Path(relative).with_suffix(".olean")
        require(digest(source) == source_hash, f"direct mathlib source drifted: {relative}")
        require(digest(olean) == olean_hash, f"direct mathlib olean drifted: {relative}")

    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()).resolve()
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()).resolve()
    bwrap_name = shutil.which("bwrap")
    git_name = shutil.which("git")
    require(bwrap_name is not None and git_name is not None, "required validation executable is missing")
    bwrap = Path(bwrap_name).resolve()
    require(digest(lean) == LEAN_EXECUTABLE_SHA256, "Lean executable drifted")
    require(digest(lake) == LAKE_EXECUTABLE_SHA256, "Lake executable drifted")
    require(digest(Path(sys.executable).resolve()) == PYTHON_EXECUTABLE_SHA256, "Python executable drifted")
    require(digest(Path(git_name).resolve()) == GIT_EXECUTABLE_SHA256, "Git executable drifted")
    require(digest(bwrap) == BWRAP_EXECUTABLE_SHA256, "bubblewrap executable drifted")
    require("4.29.0" in run([str(lean), "--version"], cwd=LEAN_ROOT), "unexpected Lean version")

    outputs: dict[str, str] = {}
    with tempfile.TemporaryDirectory(prefix="stage1-m1133-validation-") as temporary_name:
        temporary = Path(temporary_name)
        module_dir = temporary / "Stage1_Instances" / "THM-M-1133"
        module_dir.mkdir(parents=True)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (module_dir / name).write_bytes((HERE / name).read_bytes())
        sandbox = [
            str(bwrap),
            "--ro-bind", "/", "/",
            "--bind", str(temporary), str(temporary),
            "--dev", "/dev",
            "--proc", "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--clearenv",
            "--setenv", "HOME", str(temporary),
            "--setenv", "LEAN_NUM_THREADS", "1",
            "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "NO_COLOR", "1",
            "--setenv", "TZ", "UTC",
            "--chdir", str(module_dir),
        ]
        base_args = [str(lean), "--trust=0", "-t0", "--root", str(temporary)]
        outputs["Statement.lean"] = run(
            sandbox + ["--setenv", "LEAN_PATH", lean_path] + base_args
            + ["-o", "Statement.olean", "Statement.lean"],
            cwd=ROOT,
        )
        local_path = f"{temporary}:{lean_path}"
        outputs["ObligationTree.lean"] = run(
            sandbox + ["--setenv", "LEAN_PATH", local_path] + base_args
            + ["-o", "ObligationTree.olean", "ObligationTree.lean"],
            cwd=ROOT,
        )
        outputs["Proof.lean"] = run(
            sandbox + ["--setenv", "LEAN_PATH", local_path] + base_args
            + ["-o", "Proof.olean", "Proof.lean"],
            cwd=ROOT,
        )
        outputs["Validation.lean"] = run(
            sandbox + ["--setenv", "LEAN_PATH", local_path] + base_args
            + ["Validation.lean"],
            cwd=ROOT,
        )

    for declaration in COMPOSITION_AXIOM_DECLARATIONS:
        require(printed_axioms(outputs["ObligationTree.lean"], declaration) == EXPECTED_AXIOMS, f"unexpected axiom closure for {declaration}")
    for declaration in PROOF_AXIOM_DECLARATIONS:
        require(printed_axioms(outputs["Proof.lean"], declaration) == EXPECTED_AXIOMS, f"unexpected axiom closure for {declaration}")
    require(printed_axioms(outputs["Validation.lean"], "Stage1Instances.THM_M_1133.Validation.exactRootProbe") == EXPECTED_AXIOMS, "unexpected axiom closure for exactRootProbe")
    require(outputs["Validation.lean"].count("Declarations are sorry-free!") == 11, "expected eleven elaborator-aware no-sorry reports")
    require("sorryAx" not in "".join(outputs.values()), "Lean output reports a placeholder axiom")

    closure = graphs["closure_boundary"]
    require(closure["root_closed"] is False and closure["theorem_complete"] is False, "frozen graph must remain pre-proof")
    require(closure["remaining_root_cut_set"] == ["M1133-T-LIMIT"], "frozen graph root cut drifted")

    expected_inputs = {
        **FROZEN_INPUT_HASHES,
        "Validation.lean": digest(HERE / "Validation.lean"),
        "validation-spec.json": digest(HERE / "validation-spec.json"),
        "check_validation.py": digest(HERE / "check_validation.py"),
    }
    require(receipt["inputs"] == expected_inputs, "receipt input hashes drifted")
    require(receipt["schema_version"] == "stage1-node-receipt/1.0", "wrong receipt schema")
    require(receipt["receipt_id"] == "S56-M-1133-VALIDATION-local-20260714T041250+0800", "receipt ID drifted")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE, "receipt base drifted")
    require(receipt["intent"] == "validate" and receipt["depends_on"] == ["S56-M-1133-PROOF"], "receipt intent/dependency drifted")
    require(receipt["support_state"] == "provisional_worker_selftest", "receipt support state drifted")
    require(receipt["proposed_state"] == "[_]" and receipt["accepted"] is False, "receipt overstates acceptance")
    require(receipt["verdict"] == "blocked" and receipt["release_grade"] is False, "receipt overstates validation grade")
    require(set(receipt["changed_paths"]) == CHANGED_PATHS, "receipt changed paths drifted")
    require(receipt["canonical_target"] == "Stage1Instances.THM_M_1133.HeatEquationWeakMaximumPrinciple", "receipt target drifted")
    require(receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256, "receipt expression fingerprint drifted")
    require(receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256, "receipt denominator drifted")
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit",
    ):
        require(receipt["recipe"][key] == spec[key], f"receipt recipe field drifted: {key}")
    receipt_environment = receipt["environment"]
    require(receipt_environment["lean_executable_sha256"] == LEAN_EXECUTABLE_SHA256, "receipt Lean identity drifted")
    require(receipt_environment["lake_executable_sha256"] == LAKE_EXECUTABLE_SHA256, "receipt Lake identity drifted")
    require(receipt_environment["python_executable_sha256"] == PYTHON_EXECUTABLE_SHA256, "receipt Python identity drifted")
    require(receipt_environment["git_executable_sha256"] == GIT_EXECUTABLE_SHA256, "receipt Git identity drifted")
    require(receipt_environment["bubblewrap_executable_sha256"] == BWRAP_EXECUTABLE_SHA256, "receipt bubblewrap identity drifted")
    require(receipt_environment["mathlib_revision"] == MATHLIB_REVISION, "receipt mathlib revision drifted")
    require(receipt_environment["mathlib_tree"] == MATHLIB_TREE, "receipt mathlib tree drifted")
    expected_direct_surfaces = {
        relative: [source_hash, olean_hash]
        for relative, (source_hash, olean_hash) in DIRECT_MATHLIB_SURFACES.items()
    }
    require(
        receipt["provenance"]["direct_mathlib_source_and_olean_hashes"]
        == expected_direct_surfaces,
        "receipt direct provenance hashes drifted",
    )
    require(receipt["provenance"]["transitive_trust_closure_sha256"] is None, "receipt overstates transitive trust closure")
    require(receipt["result"]["provisional_root_kernel_closed"] is True, "receipt omits local root closure")
    require(
        receipt["result"]["semantic_output_summary_sha256"]
        == canonical_digest(receipt["output_summary"]),
        "receipt semantic output summary hash drifted",
    )
    require("not archived as content-addressed raw logs" in receipt["result"]["raw_log_boundary"], "receipt raw-log boundary drifted")
    require(receipt["result"]["observed_axioms"] == ["propext", "Classical.choice", "Quot.sound"], "receipt axiom observation drifted")
    require(receipt["result"]["accepted_root_closed"] is False, "receipt overstates accepted root")
    require(receipt["result"]["hermetic_release_gate"] == "fail_closed", "receipt overstates hermetic evidence")
    require(receipt["result"]["independent_distinct_runner_gate"] == "fail_closed", "receipt overstates independent evidence")
    require(receipt["result"]["audit_complete"] is False and receipt["result"]["theorem_complete"] is False, "receipt overstates terminal status")
    require(receipt["first_failed_gate"] == "dependency.S56-M-1133-PROOF.master_acceptance", "first failed gate drifted")
    require(receipt["first_failed_release_gate"] == "hermetic.cold_empty_cache_offline_replay", "first release gate drifted")
    require(receipt["environment"]["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}", "receipt platform drifted")

    require(packet == {
        "item_id": ITEM,
        "changed_paths": receipt["changed_paths"],
        "commands": receipt["commands_and_results"],
        "output_summary": receipt["output_summary"],
        "base_revision": BASE_REVISION,
        "known_failures": receipt["known_failures"],
        "state": "[_]",
    }, "worker self-test packet drifted")
    status = git_output("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    require(actual_changes == CHANGED_PATHS, f"unexpected changed paths: {sorted(actual_changes)}")
    for relative in CHANGED_PATHS:
        check_text_file(ROOT / relative)

    print("PASS THM-M-1133 validation: exact root, frozen composition, and exact-type probe kernel-replayed with --trust=0")
    print("PASS isolation: fresh local oleans, read-only host root, cleared environment, and denied network namespace")
    print("PASS trust observation: eleven declarations are sorry-free and all proof reports use exactly propext, Classical.choice, and Quot.sound")
    print("PASS direct provenance: local hashes, clean pinned mathlib revision/tree, seven direct source/olean pairs, tools, and license agree")
    print("STALE authoritative state: proof prerequisite is provisional and the frozen graph remains pre-proof M3 pending master reconciliation")
    print("BLOCKED validation trust/source: accepted foundation and complete transitive TCB/provenance plus H0 source review remain open")
    print("BLOCKED release gates: warm shared .lake is not cold offline replay and this import-dependent probe is not distinct-runner verification")
    print("audit_complete=false; theorem_complete=false")
    print(f"validation spec sha256: {digest(HERE / 'validation-spec.json')}")
    print(f"validation probe sha256: {digest(HERE / 'Validation.lean')}")
    print(f"validator sha256: {digest(HERE / 'check_validation.py')}")


if __name__ == "__main__":
    main()
