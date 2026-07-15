#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0594-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0594"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0594-VALIDATION"
THEOREM = "THM-M-0594"
BASE_REVISION = "b366bdd9f72217b5465ccd19133760b911ed0b58"
BASE_TREE = "987b635fe76400c0818b485a6e5fc7a7067311e4"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
ELAN_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPRESSION_SHA256 = "32943593a17c04d3b6fab019d7cf0db88d5e59b59f3d73703e82514987e97ef6"
DENOMINATOR_SHA256 = "0ad656eddf1e42c8f47912729ceddcab9e45d56fd8a68e24b7bc82d59d367443"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R3"}
AUTHORITATIVE_OPEN_CUT = ["M0594-C-GLOBAL", "M0594-L-TOPOLOGICAL"]
PROVISIONAL_OPEN_CUT = ["M0594-C-GLOBAL"]
PROVISIONALLY_VALIDATED = ["M0594-L-TOPOLOGICAL"]

LEAN_NAMES = (
    "Statement.lean",
    "AnchorAudit.lean",
    "ObligationTree.lean",
    "ProofSupport.lean",
    "ProofBoundary.lean",
    "Proof.lean",
    "Validation.lean",
)
MODULE_DECLARATIONS = {
    "AnchorAudit.lean": ("compactSpecialization_of_mathlib",),
    "ObligationTree.lean": ("root_of_smooth_embedding_witness",),
    "ProofSupport.lean": (
        "exists_compact_exhaustion",
        "exists_global_smooth_bump_covering",
        "isEmbedding_of_isProperMap_of_injective",
    ),
    "ProofBoundary.lean": ("whitneyEmbeddingTarget_of_isEmpty",),
    "Proof.lean": (
        "properInjectiveEuclideanMap_isEmbedding",
        "whitneyEmbeddingTarget_of_properInjectiveImmersion",
    ),
    "Validation.lean": ("properInjectiveProbe", "conditionalExactTargetProbe"),
}
EXPECTED_INPUTS = {
    "Statement.lean": "a70005e624a0745c077c074e1eacf399c0050b45853721473d318b7eb3651445",
    "AnchorAudit.lean": "5f5c674b00c1a911bc89d6806c078635db62bc2f9a9cce8b9617a4877a7ae89a",
    "ObligationTree.lean": "207a15390247960dd2578f9530b4e1470a03801b4890615f3d507629aad127cc",
    "ProofSupport.lean": "67d205b49a8bd24bbd86e4cb75178e984b9825f996b5bd9854bcdb0814a29083",
    "ProofBoundary.lean": "e8605dee8fde1f3ac83333c7f7decc7114a8feb948dded2cbd9836d88bbdac78",
    "Proof.lean": "4a46bdb092125e0a00d2450fd264f5f1f0be92c7cffa4fa5de1712316689e312",
    "Validation.lean": "9aafe47697b7ae8f64b8e2f3df35382787c7f3555bc377bb349c59b4ba86fa85",
    "statement.json": "fd651a374b6c7569f8fe0a28950ec9e4b109bd2c9489096d348dc615ed896fe2",
    "anchor_candidates.json": "7d5f94203900ef02305208e21da8d1aab3c7d40f8af5a02247ad1fdfce42d0ac",
    "obligation-registry.json": "ba31185450c503b47557f6e988f3176cfdc39d02acee60fc03425746837c6db5",
    "typed-graphs.json": "cecbfa3dfa5fea5917c11a076222609fc29c836a52ac343d63534c09f7138ec5",
    "validation-specs.json": "fe55468f51e1c5408c536255aff2eaed25585734292aaf01266c070b05924de7",
    "proof-receipt.json": "36aa282a9e40fa96582f75d33723ad6647f516fd003785b30f68845af9108434",
}
SOURCE_PROVENANCE = {
    "Mathlib/Geometry/Manifold/WhitneyEmbedding.lean": {
        "blob": "c60acf0777322d1d813b9467d6084798360c1fcd",
        "source_sha256": "6d77ea459398c5c015f0c331040956cf28c8bc971ef59f40fffe18f1ac772845",
        "olean_sha256": "3dfa5d9055d7c1408837b7d1cf4129e91c2117b72de135f50dce6383cae32b8a",
        "olean_bytes": 130192,
    },
    "Mathlib/Topology/Maps/Proper/Basic.lean": {
        "blob": "7247e72398e6f75ed57e6d11e429f403b0e34797",
        "source_sha256": "ef338993895d428c71077654b5ce52fd3f7e35bd937edada74db59966e495ef8",
        "olean_sha256": "deee8a624f4cee03f9c3d723d53b705eac87b800ba8a657ed8a205232e3bf2d2",
        "olean_bytes": 84416,
    },
    "Mathlib/Util/AssertNoSorry.lean": {
        "blob": "060d8a764d2a6d1d2963d9c500b6084a05bed534",
        "source_sha256": "aa9f7bebacafc688c894ef2171930e51ed19e0dfe722581848a2414d28900d4d",
        "olean_sha256": "c8bf37753d9bad47b9fe67e32436da8b9af516a4abbbe14e74726f01ba2fb30b",
        "olean_bytes": 51336,
    },
    "Mathlib/Util/PrintSorries.lean": {
        "blob": "24d72cc680fa8b07f0d1062f670a5a824934a227",
        "source_sha256": "03670b0b0007740e5390dadd49c3d10a02b7d0919092d2b3214ef8a6a8cf798f",
        "olean_sha256": "9bcc4076e0aee5febb2eea5cf9dc959f38526e9f974afdfdd8658bfd318d5bb7",
        "olean_bytes": 314480,
    },
}
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-blocker.json",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
]
SUMMARY_LINES = [
    "PASS narrow kernel replay: exact statement, compact specialization, conditional compositions, partial proof bodies, empty boundary, and independent probes elaborated at trust zero",
    "PASS trust observation: eight local and two independently written declarations are sorry-free and use only propext, Classical.choice, and Quot.sound; probe closure has no bodyless nonaxiom or unsafe declaration",
    "PASS selected provenance: frozen inputs, clean mathlib pin/tree/remote, four direct source/olean boundaries, executable identities, and license agree",
    "FAIL CLOSED proof dependency and exact root: proof is worker-provisional, accepted closure is empty, and M0594-C-GLOBAL remains without a premise-free body",
    "FAIL CLOSED complete trust/provenance and hermetic release: accepted foundation, full TCB/SBOM closure, cold empty-cache offline replay, and deterministic release evidence are absent",
    "FAIL CLOSED independent verification: same-worker differential probes are not a second signed clean runner or independently implemented release verifier",
]

if not __debug__:
    raise RuntimeError("validation requires Python assertions; optimized mode is forbidden")


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


def code_without_comments(source: str) -> str:
    """Remove nested Lean comments and strings for a conservative source scan."""
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        if depth:
            if source.startswith("/-", index):
                depth += 1
                index += 2
            elif source.startswith("-/", index):
                depth -= 1
                index += 2
            else:
                index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                index += 2
            elif source[index] == '"':
                in_string = False
                output.append('"')
                index += 1
            else:
                index += 1
        elif source.startswith("/-", index):
            depth = 1
            index += 2
        elif source.startswith("--", index):
            end = source.find("\n", index)
            index = len(source) if end < 0 else end
        elif source[index] == '"':
            in_string = True
            output.append('"')
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'[^']*{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output,
        flags=re.DOTALL,
    )
    assert match is not None, (declaration, output)
    return {
        part.strip()
        for part in match.group(1).replace("\n", "").split(",")
        if part.strip()
    }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def compiled_roots() -> list[Path]:
    roots = sorted(
        (path / ".lake" / "build" / "lib" / "lean").resolve()
        for path in (LEAN_ROOT / ".lake" / "packages").iterdir()
        if path.is_dir() and (path / ".lake" / "build" / "lib" / "lean").is_dir()
    )
    assert roots, "no pre-existing pinned compiled artifacts"
    return roots


def sandboxed_replay(lean: Path, bwrap: Path) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="m0594-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in LEAN_NAMES:
            shutil.copy2(HERE / name, tmp / name)
        dependency_path = ":".join(str(path) for path in compiled_roots())
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(name: str, local_imports: bool, emit_olean: bool) -> str:
            lean_path = f"{tmp}:{dependency_path}" if local_imports else dependency_path
            argv = base + ["--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0", "-t0"]
            if emit_olean:
                argv += ["-o", Path(name).with_suffix(".olean").name]
            argv.append(name)
            return run(argv, timeout=600)

        return {
            "Statement.lean": lean_run("Statement.lean", False, True),
            "AnchorAudit.lean": lean_run("AnchorAudit.lean", True, False),
            "ObligationTree.lean": lean_run("ObligationTree.lean", True, False),
            "ProofSupport.lean": lean_run("ProofSupport.lean", False, True),
            "ProofBoundary.lean": lean_run("ProofBoundary.lean", True, False),
            "Proof.lean": lean_run("Proof.lean", True, False),
            "Validation.lean": lean_run("Validation.lean", True, False),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    old_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    spec = load(HERE / "validation-spec.json")
    blocker = load(HERE / "validation-blocker.json")
    receipt = load(HERE / "validation-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 255 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 255,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0594-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0594-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    dependency_accepted = (
        predecessor["state"] == "[x]"
        and proof_receipt.get("support_state") == "master_accepted"
    )
    assert dependency_accepted is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert statement["declaration"] == "Stage1Instances.THM_M_0594.WhitneyEmbeddingTarget"
    assert statement["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert statement["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor_candidates.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    inventory = registry["frozen_denominators"]["inventory"]
    assert len(inventory) == 16 and len(set(inventory)) == 16
    assert [row["obligation_id"] for row in registry["obligations"]] == inventory
    assert len(old_specs["recipes"]) == len(inventory)
    assert {
        recipe["covered_obligation_ids"][0] for recipe in old_specs["recipes"]
    } == set(inventory)

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["depends_on"] == ["S56-M-0594-PROOF"] and len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert recipe["argv"] == [
        "/usr/bin/python3", "-I", "-B",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["cwd"] == "." and recipe["env_allowlist"] == {}
    assert recipe["timeout_seconds"] == 600 and recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0
    assert recipe["covered_obligation_ids"] == inventory
    assert recipe["covered_declarations"] == [
        "Stage1Instances.THM_M_0594.compactSpecialization_of_mathlib",
        "Stage1Instances.THM_M_0594.root_of_smooth_embedding_witness",
        "Stage1Instances.THM_M_0594.exists_compact_exhaustion",
        "Stage1Instances.THM_M_0594.exists_global_smooth_bump_covering",
        "Stage1Instances.THM_M_0594.isEmbedding_of_isProperMap_of_injective",
        "Stage1Instances.THM_M_0594.whitneyEmbeddingTarget_of_isEmpty",
        "Stage1Instances.THM_M_0594.properInjectiveEuclideanMap_isEmbedding",
        "Stage1Instances.THM_M_0594.whitneyEmbeddingTarget_of_properInjectiveImmersion",
        "Stage1Instances.THM_M_0594.Validation.properInjectiveProbe",
        "Stage1Instances.THM_M_0594.Validation.conditionalExactTargetProbe",
    ]

    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0594-ROOT")
    assert {
        "H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]
    } == ROOT_VECTOR
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == AUTHORITATIVE_OPEN_CUT
    assert proof_receipt["item_id"] == "S56-M-0594-PROOF"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["result"]["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert "M0594-L-TOPOLOGICAL" in proof_receipt["status_boundary"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        flags=re.MULTILINE,
    )
    for name in LEAN_NAMES:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = source.replace("#print sorries", "")
        assert prohibited.search(source) is None, name
    validation_source = code_without_comments((HERE / "Validation.lean").read_text())
    assert "import Proof" not in validation_source
    assert "import ObligationTree" not in validation_source
    assert "properInjectiveProbe" in validation_source
    assert "conditionalExactTargetProbe" in validation_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=no", cwd=mathlib) == ""
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in SOURCE_PROVENANCE.items():
        source = mathlib / relative
        olean = mathlib / ".lake" / "build" / "lib" / "lean" / Path(relative).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert olean.stat().st_size == expected["olean_bytes"]

    fixed_env = {
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    elan = Path.home() / ".elan" / "bin" / "elan"
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git")
    tool_root = Path.home() / ".elan" / "toolchains" / "leanprover--lean4---v4.29.0" / "bin"
    lean = tool_root / "lean"
    lake = tool_root / "lake"
    assert sha256(lean) == LEAN_SHA256
    assert sha256(lake) == LAKE_SHA256
    assert sha256(elan) == ELAN_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    assert sha256(python) == PYTHON_SHA256
    assert sha256(git_executable) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], env=fixed_env)

    outputs = sandboxed_replay(lean, bwrap)
    for module, declarations in MODULE_DECLARATIONS.items():
        for declaration in declarations:
            assert printed_axioms(outputs[module], declaration) == EXPECTED_AXIOMS, declaration
    validation_output = outputs["Validation.lean"]
    assert validation_output.count("Declarations are sorry-free!") == 2
    assert "VALIDATION_CLOSURE roots=2 declarations=28110 modules=1052" in validation_output
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in validation_output
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in validation_output
    assert "VALIDATION_CLOSURE unsafe=[]" in validation_output
    assert "error:" not in "\n".join(outputs.values()).lower()

    assert blocker["item_id"] == receipt["item_id"] == ITEM
    assert blocker["verdict"] == receipt["verdict"] == "blocked"
    assert blocker["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert blocker["accepted"] is receipt["accepted"] is False
    assert blocker["validation_phase_complete"] is receipt["result"]["validation_complete"] is False
    assert blocker["root_kernel_closed"] is receipt["result"]["root_kernel_closed"] is False
    assert blocker["audit_complete"] is blocker["theorem_complete"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert blocker["root_vector_before"] == blocker["root_vector_after"] == ROOT_VECTOR
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == ROOT_VECTOR
    assert blocker["authoritative_remaining_root_cut_set"] == AUTHORITATIVE_OPEN_CUT
    assert receipt["authoritative_remaining_root_cut_set"] == AUTHORITATIVE_OPEN_CUT
    assert blocker["provisional_remaining_root_cut_set"] == PROVISIONAL_OPEN_CUT
    assert receipt["provisional_remaining_root_cut_set"] == PROVISIONAL_OPEN_CUT
    assert blocker["provisionally_validated_obligation_ids"] == PROVISIONALLY_VALIDATED
    assert receipt["provisionally_validated_obligation_ids"] == PROVISIONALLY_VALIDATED
    assert blocker["accepted_closed_obligation_ids"] == receipt["accepted_closed_obligation_ids"] == []
    assert blocker["first_failed_gate"] == receipt["first_failed_gate"] == (
        "dependency.S56-M-0594-PROOF.master_acceptance"
    )
    assert blocker["changed_paths"] == receipt["changed_paths"] == CHANGED_PATHS
    assert receipt["base_revision"] == blocker["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == blocker["base_tree"] == BASE_TREE
    for key, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][key] == expected
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit", "expected_outputs", "covered_obligation_ids",
        "covered_declarations", "coverage_boundary",
    ):
        assert receipt["recipe"][key] == recipe[key], key
    assert receipt["result"]["lean_output_sha256"] == {
        name: hashlib.sha256(output.encode()).hexdigest()
        for name, output in outputs.items()
    }
    assert receipt["result"]["validation_closure"] == {
        "roots": 2,
        "declarations": 28110,
        "modules": 1052,
        "axioms": ["propext", "Classical.choice", "Quot.sound"],
        "bodyless_nonaxioms": [],
        "unsafe_declarations": [],
    }

    if args.worker_packet is not None:
        packet_path = args.worker_packet
        if not packet_path.is_absolute():
            packet_path = ROOT / packet_path
        packet = load(packet_path)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["output_summary"] == "\n".join(SUMMARY_LINES)
        assert packet["commands"][-1] == {
            "argv": recipe["argv"],
            "cwd": ".",
            "exit_code": 0,
            "output_summary": "exact six-line PASS/FAIL CLOSED summary",
        }
        status = git("status", "--short", "--untracked-files=all")
        actual_changed = sorted(
            line[3:] for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        )
        assert actual_changed == sorted(CHANGED_PATHS), (actual_changed, CHANGED_PATHS)
        for relative in CHANGED_PATHS:
            assert_text_hygiene(ROOT / relative)

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
