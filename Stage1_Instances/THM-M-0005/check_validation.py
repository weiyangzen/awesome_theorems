#!/usr/bin/env python3
"""Fail-closed validator for S56-M-0005-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import signal
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0005"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0005-VALIDATION"
THEOREM = "THM-M-0005"
BASE_REVISION = "63a9ed9c4aae594da31423142b0658129d5452a7"
BASE_TREE = "7bee4fac4489bad36fd615a023df13bb294d1781"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "f6396a70702a8bb45dbbb267ebd3ba10aae4f4db28cf25355f8fcd7bb607ddd4"
DENOMINATOR_SHA256 = "563eac891739af1e2468c4fd23e7465013f9e5791e069a03e22ccdf67119a762"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R3"}
PARTIAL_IDS = ["M0005-CHAIN-FREE", "M0005-DIRECT-SUM", "M0005-COMPONENTS"]
OPEN_ROOT_CUT = [
    "M0005-CHAIN-FREE",
    "M0005-EZ-MAP",
    "M0005-EZ-EQUIV",
    "M0005-EZ-NAT",
    "M0005-ALG-MAPS",
    "M0005-ALG-ZERO",
    "M0005-ALG-EXACT",
    "M0005-ALG-NAT",
    "M0005-DIRECT-SUM",
    "M0005-COMPONENTS",
    "M0005-TOP-NAT",
]
EXPECTED_INPUTS = {
    "intake.json": "17a5131f3cce379494f775aed9f60c690a48076d30fd8a2f6c1342e196888fd5",
    "KunnethStatement.lean": "f91fb92e25655c923340755a9b64b5b32e4667a51f48474db1f4f14ac0edea53",
    "AnchorAuditProbe.lean": "186bb6ed4e28eca108bb5ca5a7cd5d9abf746deb95b798f3867df152d39393d1",
    "anchor_candidates.json": "59cf20f29ed09cc978fbd4b37f4ee1c163b5a05f380ae56901b601311344c63b",
    "source_statement_crosswalk.md": "7c63daeb3343890394938a1acc52f2ea5d2b9a9800c62d97da81c557530dd357",
    "obligation-registry.json": "49ff9c2df1103dffa12c4f48f7cf812378bbbc43280e3017a17d8657dc40df36",
    "typed-graphs.json": "e10788b66d74a1c88a08f9a7e0b935f695fe6e0a2a384c0a4eb9fbfd5e2fa839",
    "ObligationTree.lean": "6702c54e8e53a33011427a85f5c03a599001c47a29417f5f1ee39b5b3fd4881a",
    "Proof.lean": "9257e31e3cbd321cb8aee61c663f6bb5b91f7af92e26bdbf6c7afb4c008950db",
    "ProofProgress20260715Slot21.lean": "b2fda08796e0feeb5ecc1fc5004c4162e76b6a9cb9d1ed2aaf31596b1a14cd21",
    "ProofDirectSum20260715Head5bb51543Slot21.lean": "8577f084bc162051ebd98e996e8870f9ea9dba74192e35973d5edb7b2d5e04e7",
    "proof-direct-sum-receipt-20260715-head-5bb51543-slot21.json": "a717cdb0177d3072bce358908b7df5a414be7e9c30a9bd230c1b31783c0f366d",
    "validation-specs.json": "7ce5b5bf2c2595ed42b4a23bd0e7831a8c72fc81ed4ae57d3ff00a5fac1787ce",
}
SOURCE_BOUNDARIES = {
    "Mathlib/AlgebraicTopology/SingularHomology/Basic.lean": {
        "blob": "fc17ce502e264d73bfb91e78a0595e66f240558a",
        "source_sha256": "655867a11ed5ec706a554ac32f8f273c5227cafd4b47f0de42d84e24b0d33c7c",
        "olean_sha256": "03202b1396ef4a2ab9ba226ee4aaa93b492667ff0c882c60dc584ca9c4b7f4a7",
        "olean_bytes": 54000,
    },
    "Mathlib/CategoryTheory/Monoidal/Tor.lean": {
        "blob": "be278f05b835432cad600a74de58f78c9031162f",
        "source_sha256": "63aeefddef4fdbf5f74cade1c13f0d63b742247c2ff2c69a9546454c57d34860",
        "olean_sha256": "8421c99f20c5e610965a6444cb33e4adc1248596279ead96390f50841c88df62",
        "olean_bytes": 76064,
    },
    "Mathlib/Algebra/Homology/ShortComplex/ShortExact.lean": {
        "blob": "af39e0f79aa422c073b97a45cbc9b3974578f921",
        "source_sha256": "38b1e879c02dd9160e3e299c2f02bf9313c02b1d1d61d4450b288cae310ee869",
        "olean_sha256": "d026f908b52071b5129e46e6a58e587d12f9faaa85559ef584eeebe825c6e272",
        "olean_bytes": 77768,
    },
}
MODULE_DECLARATIONS = {
    "ObligationTree.lean": (
        "AwesomeTheorems.Stage1.THM_M_0005.ObligationTree.assemble_sequence",
        "AwesomeTheorems.Stage1.THM_M_0005.ObligationTree.root_compose",
    ),
    "Proof.lean": (
        "AwesomeTheorems.Stage1.THM_M_0005.Proof.tensorMap",
        "AwesomeTheorems.Stage1.THM_M_0005.Proof.tensorMap_component",
        "AwesomeTheorems.Stage1.THM_M_0005.Proof.torMap",
        "AwesomeTheorems.Stage1.THM_M_0005.Proof.torMap_component",
        "AwesomeTheorems.Stage1.THM_M_0005.Proof.singularChains_projective",
    ),
    "ProofProgress20260715Slot21.lean": (
        "AwesomeTheorems.Stage1.THM_M_0005.ProofProgress20260715Slot21.singularChains_free",
        "AwesomeTheorems.Stage1.THM_M_0005.ProofProgress20260715Slot21.singularChains_free_and_projective",
        "AwesomeTheorems.Stage1.THM_M_0005.ProofProgress20260715Slot21.tensorMap_id",
        "AwesomeTheorems.Stage1.THM_M_0005.ProofProgress20260715Slot21.tensorMap_comp",
        "AwesomeTheorems.Stage1.THM_M_0005.ProofProgress20260715Slot21.torMap_id",
        "AwesomeTheorems.Stage1.THM_M_0005.ProofProgress20260715Slot21.torMap_comp",
        "AwesomeTheorems.Stage1.THM_M_0005.ProofProgress20260715Slot21.kunnethFormula_of_fields",
    ),
    "ProofDirectSum20260715Head5bb51543Slot21.lean": (
        "AwesomeTheorems.Stage1.THM_M_0005.ProofDirectSum20260715Head5bb51543Slot21.torDegreesSuccEquivTensorDegrees",
        "AwesomeTheorems.Stage1.THM_M_0005.ProofDirectSum20260715Head5bb51543Slot21.torDegreesSuccEquivTensorDegrees_apply",
        "AwesomeTheorems.Stage1.THM_M_0005.ProofDirectSum20260715Head5bb51543Slot21.torDegreesSuccEquivTensorDegrees_symm_apply",
        "AwesomeTheorems.Stage1.THM_M_0005.ProofDirectSum20260715Head5bb51543Slot21.torDegrees_zero_empty",
        "AwesomeTheorems.Stage1.THM_M_0005.ProofDirectSum20260715Head5bb51543Slot21.torTerm_zero_isZero",
        "AwesomeTheorems.Stage1.THM_M_0005.ProofDirectSum20260715Head5bb51543Slot21.torTermSuccIso",
        "AwesomeTheorems.Stage1.THM_M_0005.ProofDirectSum20260715Head5bb51543Slot21.torTermSuccIso_hom_ι",
        "AwesomeTheorems.Stage1.THM_M_0005.ProofDirectSum20260715Head5bb51543Slot21.torTermSuccIso_inv_ι",
    ),
}
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
]
SUMMARY_LINES = [
    "PASS narrow kernel replay: exact statement, two conditional compositions, and 20 partial proof declarations elaborated at trust zero",
    "PASS trust observation: all 22 checked declarations report only propext, Classical.choice, and Quot.sound; validation closure has no bodyless nonaxiom or unsafe declaration",
    "PASS selected provenance: frozen inputs, tracked-clean mathlib pin, three direct source/olean boundaries, tool identities, and license agree",
    "FAIL CLOSED exact root and dependency: proof remains provisional, zero frozen obligations close, and no premise-free Kunneth sequence exists",
    "FAIL CLOSED complete trust/provenance and hermetic release: accepted foundation, complete TCB/SBOM closure, cold empty-cache rebuild, and offline restoration are absent",
    "FAIL CLOSED independent verification: this same-workspace replay is not a second signed clean runner or independently implemented release verifier",
]

if not __debug__:
    raise RuntimeError("validation requires Python assertions; optimized mode is forbidden")


def timeout_handler(_signum: int, _frame: object) -> None:
    raise TimeoutError("validation exceeded the structured 600-second recipe bound")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).strip()


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
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL,
    )
    matches = pattern.findall(output)
    assert len(matches) == 1, f"missing or duplicate axiom report for {declaration}"
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def explicit_lean_path(tmp: Path, lean: Path) -> str:
    package_names = (
        "Cli", "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "checkdecls", "mathlib",
    )
    roots = [tmp]
    for name in package_names:
        path = (LEAN_ROOT / ".lake/packages" / name / ".lake/build/lib/lean").resolve()
        if path.is_dir():
            roots.append(path)
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    if local.is_dir():
        roots.append(local)
    roots.append(lean.parent.parent / "lib/lean")
    return ":".join(str(path) for path in roots)


def isolated_replay(lean: Path, bwrap: Path) -> dict[str, str]:
    names = [
        "KunnethStatement.lean", "AnchorAuditProbe.lean", "ObligationTree.lean",
        "Proof.lean", "ProofProgress20260715Slot21.lean",
        "ProofDirectSum20260715Head5bb51543Slot21.lean", "Validation.lean",
    ]
    with tempfile.TemporaryDirectory(prefix="stage1-m0005-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in names:
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()
        lean_path = explicit_lean_path(tmp, lean)
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--setenv", "LEAN_PATH", lean_path,
            "--chdir", str(tmp), str(lean), "--trust=0", "-t0", "-R", str(tmp),
        ]
        outputs: dict[str, str] = {}
        for name in names:
            outputs[name] = run(base + ["-o", name.replace(".lean", ".olean"), name])
        return outputs


def main() -> None:
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(600)
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    intake = load(HERE / "intake.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-direct-sum-receipt-20260715-head-5bb51543-slot21.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 100 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 100
    assert item["phase"] == "validation" and item["layer"] == 5 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0005-PROOF"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0005-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert intake["canonical_formal_target"]["elaborated_expression_hash"] == f"sha256:{EXPRESSION_SHA256}"
    assert registry["root_obligation_id"] == "M0005-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == OPEN_ROOT_CUT
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0005-ROOT")
    assert {"H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]} == ROOT_VECTOR
    assert proof_receipt["accepted"] is False
    assert proof_receipt["supported_obligation_ids"] == []
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    lean_names = [
        "KunnethStatement.lean", "AnchorAuditProbe.lean", "ObligationTree.lean",
        "Proof.lean", "ProofProgress20260715Slot21.lean",
        "ProofDirectSum20260715Head5bb51543Slot21.lean", "Validation.lean",
    ]
    for name in lean_names:
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = source.replace("#print sorries", "")
        assert prohibited.search(source) is None, f"prohibited construct in {name}"
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    assert "#print_validation_closure" in validation_source
    expected_short_names = {
        declaration.removeprefix("AwesomeTheorems.Stage1.THM_M_0005.")
        for declarations in MODULE_DECLARATIONS.values()
        for declaration in declarations
    }
    for prefix in ("assert_no_sorry ", "#print sorries ", "#print axioms "):
        actual_short_names = {
            line.removeprefix(prefix).strip()
            for line in validation_source.splitlines()
            if line.startswith(prefix)
        }
        assert actual_short_names == expected_short_names

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=no", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in SOURCE_BOUNDARIES.items():
        source = mathlib / relative
        olean = mathlib / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert olean.stat().st_size == expected["olean_bytes"]

    lean_override = os.environ.get("STAGE1_LEAN_BIN")
    if lean_override:
        lean = Path(lean_override)
    else:
        elan = shutil.which("elan")
        assert elan is not None, "elan or STAGE1_LEAN_BIN is required for relocatable tool discovery"
        elan_root = Path(elan).resolve().parent.parent
        lean = elan_root / "toolchains/leanprover--lean4---v4.29.0/bin/lean"
    lake = lean.with_name("lake")
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git")
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    assert sha256(git_executable) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"])

    outputs = isolated_replay(lean, bwrap)
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert all("error:" not in output for output in outputs.values())
    observed_axioms: set[str] = set()
    for module, declarations in MODULE_DECLARATIONS.items():
        for declaration in declarations:
            actual_axioms = reported_axioms(outputs[module], declaration)
            assert actual_axioms <= EXPECTED_AXIOMS
            observed_axioms.update(actual_axioms)
    assert observed_axioms == EXPECTED_AXIOMS
    assert outputs["Validation.lean"].count("Declarations are sorry-free!") == 22
    closure_match = re.search(
        r"VALIDATION_CLOSURE roots=22 declarations=(\d+) modules=(\d+)",
        outputs["Validation.lean"],
    )
    assert closure_match is not None
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["Validation.lean"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["Validation.lean"]
    closure_axiom_match = re.search(
        r"VALIDATION_CLOSURE axioms=\[(.*?)]", outputs["Validation.lean"]
    )
    assert closure_axiom_match is not None
    closure_axioms = {
        part.strip()
        for part in closure_axiom_match.group(1).split(",")
        if part.strip()
    }
    assert closure_axioms == EXPECTED_AXIOMS
    observation = {
        "lean_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest()
            for name, output in outputs.items()
        },
        "observed_axioms": sorted(observed_axioms),
        "validation_closure": {
            "declarations": int(closure_match.group(1)),
            "modules": int(closure_match.group(2)),
            "bodyless_nonaxioms": [],
            "unsafe_declarations": [],
        },
    }
    if args.probe:
        print(json.dumps(observation, sort_keys=True))
        return

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0005-PROOF"]
    assert len(spec["recipes"]) == 1 and spec["recipes"][0] == receipt["recipe"]
    recipe = spec["recipes"][0]
    assert recipe["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["env_allowlist"] == {
        "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
        "HOME": (
            "inherited only by the Python recipe; every Lean subprocess receives a fresh "
            "disposable HOME"
        ),
        "PATH": "must contain the elan launcher used for relocatable Lean discovery",
        "STAGE1_LEAN_BIN": (
            "optional explicit pinned Lean executable override; its SHA-256 must match the receipt"
        ),
    }
    assert recipe["covered_obligation_ids"] == []
    all_declarations = {
        declaration
        for declarations in MODULE_DECLARATIONS.values()
        for declaration in declarations
    }
    assert len(all_declarations) == 22
    assert set(recipe["covered_declarations"]) == all_declarations

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_class"] == "provisional_blocked_validation_selftest"
    assert receipt["content_addressed"] is False
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["owner"] == "S56-M-0005 validation execution lane"
    assert receipt["reviewer"] == "independent Stage1 integration reviewer required"
    assert receipt["review_due"]
    assert receipt["validation_started_at"] < receipt["validation_ended_at"]
    assert receipt["validation_ended_at"] == receipt["validated_at"]
    assert receipt["target"] == {
        "canonical_declaration": "AwesomeTheorems.Stage1.THM_M_0005.KunnethFormula",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["Validation.lean"] == sha256(HERE / "Validation.lean")
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    authority_files = {
        "Docs/Stage1_Blueprint_rev-5.6.md",
        "Docs/Stage1_Targets_rev-5.6.json",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "skills/execute-stage1-rev56/SKILL.md",
    }
    assert set(receipt["authority_hashes"]) == authority_files
    for relative, expected in receipt["authority_hashes"].items():
        assert sha256(ROOT / relative) == expected
    assert receipt["result"]["lean_output_sha256"] == observation["lean_output_sha256"]
    assert receipt["result"]["validation_closure"] == observation["validation_closure"]
    assert receipt["result"]["validated_partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert receipt["result"]["supported_obligation_ids"] == []
    assert receipt["result"]["provisionally_closed_obligation_ids"] == []
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["root_kernel_closed"] is receipt["result"]["root_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["complete_trust_provenance_gate"] == "fail_closed"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    environment = receipt["environment"]
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(git_executable)
    assert environment["lean_toolchain_sha256"] == TOOLCHAIN_SHA256
    assert environment["lake_manifest_sha256"] == MANIFEST_SHA256
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_remote"] == MATHLIB_REMOTE
    assert environment["mathlib_license_sha256"] == MATHLIB_LICENSE_SHA256
    direct_provenance = receipt["selected_direct_provenance"]
    for relative, expected in SOURCE_BOUNDARIES.items():
        record = direct_provenance[relative]
        assert record["git_blob"] == expected["blob"]
        assert record["source_sha256"] == expected["source_sha256"]
        assert record["olean_sha256"] == expected["olean_sha256"]
    assert direct_provenance[
        "complete_terminal_body_import_artifact_source_boundary_and_tcb_closure"
    ] is False
    proof_dependency = receipt["proof_dependency"]
    assert proof_dependency == {
        "dag_state": "[_]",
        "master_accepted": False,
        "strongest_receipt_accepted": False,
        "supported_obligation_ids": [],
        "root_kernel_closed": False,
        "decision": "fail_closed",
    }
    trust = receipt["trust"]
    assert trust["observed_axioms"] == observation["observed_axioms"]
    assert trust["all_22_recipe_listed_declarations_sorry_free"] is True
    assert trust["observed_closure_bodyless_nonaxioms"] == []
    assert trust["observed_closure_unsafe_declarations"] == []
    assert trust["accepted_foundation_profile"] is False
    assert trust["complete_transitive_trust_closure"] is False
    hermeticity = receipt["hermeticity"]
    assert hermeticity["network_denied_during_replay"] is True
    assert hermeticity["fresh_output_directory"] is True
    assert hermeticity["host_and_shared_cache_read_only_inside_replay"] is True
    assert hermeticity["fresh_clean_checkout"] is False
    assert hermeticity["empty_user_package_and_build_caches"] is False
    assert hermeticity["cold_dependency_rebuild"] is False
    assert hermeticity["offline_restorable_source_dependency_sbom_license_archive"] is False
    independent = receipt["independent_validation"]
    assert independent["same_worker_no_new_proof_content"] is True
    assert independent["distinct_verifier_identity"] is False
    assert independent["independently_provisioned_clean_runner"] is False
    assert independent["second_signed_attestation"] is False
    assert independent["independently_implemented_minimal_release_verifier"] is False
    assert independent["decision"] == "fail_closed"
    assert receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["first_failed_gate"] == "dependency.S56-M-0005-PROOF.master_acceptance"
    assert receipt["retry_condition"].startswith("Master-accept placeholder-free proof evidence")
    assert receipt["changed_paths"] == CHANGED_PATHS
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        ("\n".join(SUMMARY_LINES) + "\n").encode()
    ).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)
    assert receipt["output_evidence"]["exit_code"] == 0
    assert receipt["known_failures"] and receipt["invalidation_inputs"]
    assert receipt["freshness"] == {
        "support_state": "provisional_nonrelease_worker_evidence",
        "revocation_state": "unaccepted",
        "supersession_state": "current worker proposal",
        "incident_path": (
            "rerun this recipe and integration review after any invalidation input changes"
        ),
    }

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == receipt["changed_paths"] == CHANGED_PATHS
        assert packet["commands"] == receipt["commands"]
        assert packet["output_summary"] == receipt["output_summary"]
        assert packet["known_failures"] == receipt["known_failures"]
        status = git("status", "--short", "--untracked-files=all")
        actual = {
            line[3:] for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))

    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
