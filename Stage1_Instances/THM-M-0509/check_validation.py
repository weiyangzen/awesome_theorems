#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0509-VALIDATION."""

from __future__ import annotations

import argparse
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
HERE = ROOT / "Stage1_Instances" / "THM-M-0509"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0509-VALIDATION"
THEOREM = "THM-M-0509"
BASE_REVISION = "229ca98e7478d389ccf8de8173c94e0e7c8fe670"
BASE_TREE = "d3cc9562940b923aebbe7e01ce66232079760b3b"
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
GIT_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPRESSION_SHA256 = "e2c8d3782d80648aa229dab05f90a84506ed5b6f213fa3083e312674aa6c64f7"
DENOMINATOR_SHA256 = "74b4c30d82e3aa7c44f356d24eb5cd21c2d48ce06e53898a12333504350703bd"
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
OPEN_ROOT_CUT = ["M0509-T-P2-EXTRACTION"]
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
SOURCE_PROVENANCE = {
    "Mathlib/Data/Nat/Prime/Basic.lean": {
        "blob": "e059d0ae408fdf5dcf90e34afbcc397a2f880a9b",
        "source_sha256": "b97e83d65681b68b3ad1f4bdfd36defd0a30aa173cf726b3d2807acf8bde5027",
        "olean_sha256": "40563ffd4a337bd07e5832a763aed1c5243602aba08aa0509844081b61b79d12",
    },
    "Mathlib/Data/Nat/Factors.lean": {
        "blob": "292355d305be37499c8415d15b430aa241132c9b",
        "source_sha256": "3e64e2c8ba907c05209966a7bba8754cf2ab33f328a3010667ffe58c95e0bca3",
        "olean_sha256": "ca04f32795ce6aba7a89b812e7b57cf1a11ebebb4a2428469252dad6fa132b70",
    },
    "Mathlib/NumberTheory/ArithmeticFunction/Misc.lean": {
        "blob": "02a38ea4c86e219d120c615a3369e926ac1f962a",
        "source_sha256": "bae8dc45e6fbb14f57475fbc389b3bdca270976912da171860aff6ee878d22c8",
        "olean_sha256": "fa28150ac517fc4fc9738e2bd0e0ccfe00fd4f055418ebdce90871b07d24e622",
    },
    "Mathlib/Data/Finset/Prod.lean": {
        "blob": "9161ff8ee434b8cb3305ad4a86ceb8dfc7d4dd7d",
        "source_sha256": "2cdc3c68d117332b7e947e3628a3903cd3a94cbed37764fe05f402966a979744",
        "olean_sha256": "17246154756657153ca03c888df021501b2befe866bc410c644e3084a20a69eb",
    },
    "Mathlib/Util/AssertNoSorry.lean": {
        "blob": "060d8a764d2a6d1d2963d9c500b6084a05bed534",
        "source_sha256": "aa9f7bebacafc688c894ef2171930e51ed19e0dfe722581848a2414d28900d4d",
        "olean_sha256": "c8bf37753d9bad47b9fe67e32436da8b9af516a4abbbe14e74726f01ba2fb30b",
    },
    "Mathlib/Util/PrintSorries.lean": {
        "blob": "24d72cc680fa8b07f0d1062f670a5a824934a227",
        "source_sha256": "03670b0b0007740e5390dadd49c3d10a02b7d0919092d2b3214ef8a6a8cf798f",
        "olean_sha256": "9bcc4076e0aee5febb2eea5cf9dc959f38526e9f974afdfdd8658bfd318d5bb7",
    },
}
EXPECTED_INPUTS = {
    "README.md": "8627c7381963a8418c3ee5cd566d18c55edf0fbd34cd2b14b89457a5d582f220",
    "Statement.lean": "fe4685daeb9747b01adb0d896c293c167c2e763a0c1f5b9130e80eb1afa776a9",
    "ObligationTree.lean": "6af99da9bbe9840cb3e3d51c6544c4452deab4b7f4bf13ad3dd0fe9079215dd4",
    "AnchorAudit.lean": "97508a37bc81c8ebf97d09a407f88f1be7e219ac96efd66717e4b5f8bc9a93e4",
    "Proof.lean": "20f0ca7f8822a590fdbb3c3b9ad2b4e375aebe3e8357244e00f7dc655f896428",
    "statement.json": "4873c32b63234d892a49fe4724a1eaee96cdb18097ca933af544c2dd9a74636b",
    "anchor-audit.json": "36afc1d91251bfae073fff8f29eee977844b4e957c93065dab6ff7d86a4c5dd7",
    "obligation-registry.json": "e8430fa07323ff530331012a6cc75b96df84302ce3c215e3832aca6aabb6eb13",
    "typed-graphs.json": "549160e15c5ef40e3644142a7745e9e011f3bb3fe0f3a4f2598dd3b5836d1bff",
    "validation-specs.json": "0ba293244a4789c03b690eb08b08383d578b921db5a6fa07bcd574101cda85e9",
    "proof-receipt.json": "8264c431575417e4e69b543b06b373a3fa75960fff139c283dd93ade9881ba0e",
    "proof-blocker.json": "db05852bd2ea8c2240d55c44866906d7613329b0603221c9c3f0b4a5c8658266",
    "instance.json": "31297cb5449dfd1773fcadce2cded5ca22cec345bcee6dc1cbc074510c1115e4",
    "task-dag.json": "6f720a26fff6b245da7a7f645be23cd55c9006fadd6ee05bac7a5434b3cf9905",
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
    "PASS narrow kernel replay: statement, conditional handoff, proof interfaces, and differential composition elaborated at trust zero",
    "PASS trust observation: five checked declarations are sorry-free and use only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen inputs, clean mathlib pin/tree/remote, six selected sources and oleans, toolchain, and license agree",
    "OPEN exact root: no inhabitant of EventualPositiveRepresentationCount exists; root remains M4 with cut M0509-T-P2-EXTRACTION",
    "FAIL CLOSED proof dependency: S56-M-0509-PROOF is worker-provisional rather than master-accepted",
    "FAIL CLOSED release gates: shared warm cache is not cold hermetic evidence and this worker is not a distinct signed verifier",
]

if not __debug__:
    raise RuntimeError("validation requires Python assertions; optimized mode is forbidden")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600,
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    """Remove nested Lean comments while preserving strings enough for hygiene scans."""
    out: list[str] = []
    i = 0
    depth = 0
    in_string = False
    while i < len(source):
        if depth:
            if source.startswith("/-", i):
                depth += 1
                i += 2
            elif source.startswith("-/", i):
                depth -= 1
                i += 2
            else:
                i += 1
        elif in_string:
            if source[i] == "\\" and i + 1 < len(source):
                i += 2
            elif source[i] == '"':
                in_string = False
                out.append('"')
                i += 1
            else:
                i += 1
        elif source.startswith("/-", i):
            depth = 1
            i += 2
        elif source.startswith("--", i):
            end = source.find("\n", i)
            i = len(source) if end < 0 else end
        elif source[i] == '"':
            in_string = True
            out.append('"')
            i += 1
        else:
            out.append(source[i])
            i += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(out)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'[^']*{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output,
        flags=re.DOTALL,
    )
    if match is None:
        assert f"'{declaration}' does not depend on any axioms" in output
        return set()
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
    packages = LEAN_ROOT / ".lake" / "packages"
    roots = sorted(
        (path / ".lake" / "build" / "lib" / "lean").resolve()
        for path in packages.iterdir()
        if path.is_dir() and (path / ".lake" / "build" / "lib" / "lean").is_dir()
    )
    assert roots, "no pre-existing pinned compiled artifacts"
    return roots


def sandboxed_replay(lean: Path, bwrap: Path) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="m0509-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        names = (
            "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean",
            "Proof.lean", "Validation.lean",
        )
        for name in names:
            (tmp / name).write_bytes((HERE / name).read_bytes())
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
            argv = base + ["--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0"]
            if emit_olean:
                argv += ["-o", Path(name).with_suffix(".olean").name]
            argv.append(name)
            return run(argv, timeout=600)

        return {
            "statement": lean_run("Statement.lean", False, True),
            "anchor_audit": lean_run("AnchorAudit.lean", True, False),
            "obligation_tree": lean_run("ObligationTree.lean", True, True),
            "proof": lean_run("Proof.lean", True, True),
            "validation": lean_run("Validation.lean", True, False),
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
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 883 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 883,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0509-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0509-PROOF")
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
    canonical = statement["canonical_formal_target"]
    assert canonical["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert canonical["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == OPEN_ROOT_CUT
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0509-ROOT")
    assert {
        "H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]
    } == ROOT_VECTOR
    assert proof_receipt["item_id"] == "S56-M-0509-PROOF"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert proof_blocker["root_closed"] is False
    assert proof_blocker["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        flags=re.MULTILINE,
    )
    for name in (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean",
        "Proof.lean", "Validation.lean",
    ):
        assert prohibited.search(code_without_comments((HERE / name).read_text())) is None, name
    validation_source = code_without_comments((HERE / "Validation.lean").read_text())
    assert "theorem rootFromEventualPositiveCount" in validation_source
    assert "(positive : EventualPositiveRepresentationCount)" in validation_source
    assert "theorem chenTheoremTarget_proof" not in validation_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert (LEAN_ROOT / ".lake").is_symlink(), "automation-provided canonical .lake symlink missing"
    mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in SOURCE_PROVENANCE.items():
        source = mathlib / relative
        olean = mathlib / ".lake" / "build" / "lib" / "lean" / Path(relative).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        if not relative.startswith("Mathlib/Util/"):
            assert prohibited.search(code_without_comments(source.read_text())) is None

    fixed_env = {
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    elan_name = shutil.which("elan")
    bwrap_name = shutil.which("bwrap")
    python_name = shutil.which("python3")
    git_name = shutil.which("git")
    assert all((elan_name, bwrap_name, python_name, git_name))
    elan = Path(elan_name).resolve()
    bwrap = Path(bwrap_name).resolve()
    python = Path(python_name).resolve()
    git_executable = Path(git_name).resolve()
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
    proof_declarations = (
        "Stage1Instances.THM_M_0509.Proof.isP2_iff_cardFactors_pos_le_two",
        "Stage1Instances.THM_M_0509.Proof.representationCount_pos_iff",
        "Stage1Instances.THM_M_0509.Proof.chenTheoremTarget_iff_eventualPositiveRepresentationCount",
    )
    for declaration in proof_declarations:
        assert printed_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
        assert printed_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert printed_axioms(
        outputs["obligation_tree"],
        "Stage1Instances.THM_M_0509.root_of_sieve_package",
    ) == {"propext"}
    assert printed_axioms(
        outputs["validation"],
        "Stage1Instances.THM_M_0509.Validation.rootFromEventualPositiveCount",
    ) == EXPECTED_AXIOMS
    assert outputs["proof"].count("Declarations are sorry-free!") == 3
    assert outputs["validation"].count("Declarations are sorry-free!") == 1
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert all("error:" not in output for output in outputs.values())
    closure_match = re.search(
        r"VALIDATION_CLOSURE roots=(\d+) declarations=(\d+) modules=(\d+)",
        outputs["validation"],
    )
    assert closure_match is not None and int(closure_match.group(1)) == 5
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    observation = {
        "lean_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest()
            for name, output in outputs.items()
        },
        "closure": {
            "roots": 5,
            "declarations": int(closure_match.group(2)),
            "modules": int(closure_match.group(3)),
            "axioms": sorted(EXPECTED_AXIOMS),
            "bodyless_nonaxioms": [],
            "unsafe_declarations": [],
        },
    }
    if args.probe:
        print(json.dumps(observation, sort_keys=True))
        return

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    blocker = load(HERE / "validation-blocker.json")
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == blocker["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0509-PROOF"]
    assert len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert recipe["cwd"] == "."
    assert recipe["argv"] == [
        "/usr/bin/python3", "-I", "-B",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert receipt["recipe"] == recipe
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    for name in ("Validation.lean", "check_validation.py", "validation-spec.json"):
        assert receipt["inputs"][name] == sha256(HERE / name), name
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert receipt["environment"]["lean_executable_sha256"] == sha256(lean)
    assert receipt["environment"]["lake_executable_sha256"] == sha256(lake)
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["result"]["lean_output_sha256"] == observation["lean_output_sha256"]
    assert receipt["result"]["trust_closure_observation"] == observation["closure"]
    assert receipt["result"]["proof_dependency_master_acceptance"] == "fail_closed"
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["open_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["result"]["complete_trust_provenance_gate"] == "fail_closed"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["first_failed_gate"] == "dependency.S56-M-0509-PROOF.master_acceptance"
    assert blocker["first_failed_gate"] == receipt["first_failed_gate"]
    assert blocker["root_kernel_closed"] is blocker["theorem_complete"] is False
    assert receipt["changed_paths"] == blocker["changed_paths"] == CHANGED_PATHS

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert packet["changed_paths"] == CHANGED_PATHS
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
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
