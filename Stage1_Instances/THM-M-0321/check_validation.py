#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0321-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0321"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0321-VALIDATION"
THEOREM = "THM-M-0321"
BASE_REVISION = "1729533156a59958dac4908793303a66434eb925"
BASE_TREE = "604b6669e6ab2f485c9dcb71de3a150c6deaf755"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
ELAN_LAUNCHER_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "7a9628fca04eb72d787efad1f852517f4385377b3ad16f3eba662ccea4bb86a5"
DENOMINATOR_SHA256 = "9963eb2002e7418a51e79b3ed2dd651e2c29a701cdfa1e18f47123041207f9ac"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H2", "M": "M3", "R": "R4"}
FROZEN_OPEN_CUT = ["M0321-T-UPGRADE"]
EXPECTED_INPUTS = {
    "Statement.lean": "2eed8783dc85ee0ab4f07c68d096c7bab70a3936dfb86d6a30285279b96388dd",
    "ObligationTree.lean": "c3b3e313e7db5dcd3b22d2de153ebed8d50697412540b748c0d67bf6b93f7273",
    "Proof.lean": "e34100a1471ea5e20bb2af9cec123ce21e1fde9a0131baa1381a3a881638b644",
    "statement.json": "1c590c636af5d7562083131d5d8b23dceff5902b97da0e79e481eeb14406b2d2",
    "anchor-audit.json": "1af5e332cdd5dedd6b3230d0c644a8e14a4313ff3f083256311f9812736e1a75",
    "obligation-registry.json": "f40fa32165ad49bfed9a7b2db898a9df01380f59d186bb4659fcf3fcb8eb59b0",
    "typed-graphs.json": "a2b9ff8667a791051ec919f63682666e7e739d3b3d1282132c6f3b07ae037d64",
    "proof-receipt.json": "a46ecd9989e8c4ce623e2ffc02ec99933f2986f4f7f47791cf7919203e4c778c",
    "proof-blocker.json": "cdbb8fea127c80227dd3715a03a5e9182619c21b867a9649899089b7cca9740c",
    "source-statement-crosswalk.md": "89f075ed551e193b99abf015da7fb1e45e1ac27fe4bb89168093fe5fcdb391ca",
    "Validation.lean": "e032f53e7c677e76558631401c9aba40236cb595ff86438585cf392c7b5aadcb",
}
SOURCE_BOUNDARIES = {
    "Mathlib/Analysis/Convex/Combination.lean": {
        "blob": "48e48fcb09f569566fea60179c82547c5bdd3c63",
        "source_sha256": "caa5b31cbbf33bb64b05e0e86665bb3e6f893f4c061b9621e0d3fae74c0748ca",
        "olean_sha256": "a18af2fd5d7deab21832f31b418bd7a3b23fbdbeff23601df5c6efb573a74758",
        "olean_bytes": 305464,
    },
    "Mathlib/Analysis/LocallyConvex/Bounded.lean": {
        "blob": "a09a73c1f99b3bd60207f1ba7e9a617b89b3d009",
        "source_sha256": "8824f3d335db9d69ce50fe25e9f4b40e57f044e102c2473bc8c4a420bdbce0f2",
        "olean_sha256": "7fe0b169471cc3997464702512c943a87aa315951d4df943630c91a625883eae",
        "olean_bytes": 282136,
    },
    "Mathlib/Analysis/SpecificLimits/Basic.lean": {
        "blob": "bc8ec6bb99d6f20d35ebe38f6b6d736e0ffe4868",
        "source_sha256": "610f7383f9487ad6a68c0e27eeedc98236f5cb5cffed8bfbbf78cf2c43b521ca",
        "olean_sha256": "aa4bf5024b7b011d370e7e6d895e381de2404ec501a14273abc0bf1eb6dcf68b",
        "olean_bytes": 217584,
    },
    "Mathlib/Topology/Ultrafilter.lean": {
        "blob": "4bd744b0937d7dd0b610d11f2f39722b7c997721",
        "source_sha256": "d4f13835575c5d19e0669c1711e5cdd9ebe1612a72ec57a0896bb8957095a385",
        "olean_sha256": "d8970475cb7674518055118cce417f07b24f6d22205feebff27bc78ab253dff6",
        "olean_bytes": 22552,
    },
    "Mathlib/Topology/Algebra/Module/LocallyConvex.lean": {
        "blob": "c888514e51ead30a9f3606a3860f6fc24e88bfc0",
        "source_sha256": "78543352ca66c1f01173c45faccce3d5bb827936842ab5a8d3936143d3ddc8c9",
        "olean_sha256": "c65819edab0ac3bf047b53a41cb996a5dafa0aece39488ae404ef997a27faddd",
        "olean_bytes": 118352,
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
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_0321.isClosed_fixedSetWithin",
    "Stage1Instances.THM_M_0321.isCompact_fixedSetWithin",
    "Stage1Instances.THM_M_0321.convex_fixedSetWithin",
    "Stage1Instances.THM_M_0321.mapsTo_fixedSetWithin_of_commute",
    "Stage1Instances.THM_M_0321.continuousOn_fixedSetWithin",
    "Stage1Instances.THM_M_0321.isAffineOn_fixedSetWithin",
    "Stage1Instances.THM_M_0321.cesaroAverage_mem",
    "Stage1Instances.THM_M_0321.affine_centerMass",
    "Stage1Instances.THM_M_0321.map_cesaroAverage",
    "Stage1Instances.THM_M_0321.cesaro_defect_eq",
    "Stage1Instances.THM_M_0321.tendsto_cesaro_defect_zero",
    "Stage1Instances.THM_M_0321.singleMap_fixedPoint",
    "Stage1Instances.THM_M_0321.isClosed_commonFixedSet",
    "Stage1Instances.THM_M_0321.isCompact_commonFixedSet",
    "Stage1Instances.THM_M_0321.convex_commonFixedSet",
    "Stage1Instances.THM_M_0321.mapsTo_commonFixedSet_of_commute",
    "Stage1Instances.THM_M_0321.finiteFamilyStep",
    "Stage1Instances.THM_M_0321.continuousCompactnessUpgrade",
    "Stage1Instances.THM_M_0321.markovKakutani_of_finiteFamily",
    "Stage1Instances.THM_M_0321.markovKakutani_proof",
)
VALIDATION_DECLARATION = (
    "Stage1Instances.THM_M_0321.Validation.recomposedMarkovKakutani"
)
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
]
SUMMARY_LINES = [
    "PASS narrow kernel replay: exact statement, frozen interfaces, proof bodies, exact root, and differential recomposition elaborated at trust zero",
    "PASS trust observation: checked roots use only propext, Classical.choice, and Quot.sound; closure has no unexpected bodyless or unsafe declarations",
    "PASS selected provenance: frozen hashes, seven direct source/blob/olean boundaries, tool identities, license, and clean pinned mathlib agree",
    "FAIL CLOSED authority: proof master acceptance and authoritative state reconciliation are pending; accepted root remains H2/M3/R4",
    "FAIL CLOSED frozen composition: CompactnessUpgrade omits continuity or closedness, so M0321-T-UPGRADE receives no closure credit",
    "FAIL CLOSED complete trust/provenance: accepted foundation policy and complete transitive TCB/SBOM closure are absent",
    "FAIL CLOSED hermetic/independent: warm shared cache and same-worker helper recomposition are not cold replay or distinct signed verification",
    "audit_complete=false; theorem_complete=false",
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


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=600, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = depth = 0
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
    report = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output, re.DOTALL,
    )
    if report:
        return {part.strip() for part in report.group(1).split(",") if part.strip()}
    assert f"'{declaration}' does not depend on any axioms" in output, declaration
    return set()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


HOME = os.environ["HOME"]
BASE_ENV = {
    "HOME": HOME,
    "PATH": f"{HOME}/.elan/bin:/usr/bin:/bin",
    "ELAN_TOOLCHAIN": TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


def pinned_lean_path(lean: Path) -> str:
    package_names = (
        "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "mathlib",
    )
    roots = [
        (LEAN_ROOT / ".lake" / "packages" / name / ".lake/build/lib/lean").resolve()
        for name in package_names
    ]
    assert all(path.is_dir() for path in roots)
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    assert local.is_dir()
    return ":".join([*(str(path) for path in roots), str(local), str(lean.parent.parent / "lib/lean")])


def isolated_replay(lean: Path, bwrap: Path, lean_path: str) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0321-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        target = tmp / "Stage1_Instances" / "THM-M-0321"
        target.mkdir(parents=True)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (target / name).write_bytes((HERE / name).read_bytes())
        (tmp / "home").mkdir()
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(name: str, module_path: str, emit_olean: bool) -> str:
            argv = base + ["--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0", "-R", str(tmp)]
            if emit_olean:
                argv += ["-o", str(target / name.replace(".lean", ".olean"))]
            argv.append(str(target / name))
            return run(argv, env=BASE_ENV)

        statement = lean_run("Statement.lean", lean_path, True)
        tree = lean_run("ObligationTree.lean", f"{tmp}:{lean_path}", True)
        proof = lean_run("Proof.lean", f"{tmp}:{lean_path}", True)
        validation = lean_run("Validation.lean", f"{tmp}:{lean_path}", False)
        return {"statement": statement, "tree": tree, "proof": proof, "validation": validation}


def assert_network_isolation(bwrap: Path) -> None:
    probe = subprocess.run(
        [
            str(bwrap), "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
            "--unshare-net", "--die-with-parent", "/usr/bin/python3", "-I", "-c",
            "import socket; s=socket.socket(); s.settimeout(0.2); s.connect(('1.1.1.1', 53))",
        ],
        env=BASE_ENV,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=10,
        check=False,
    )
    assert probe.returncode != 0, "bubblewrap network-denial mutation unexpectedly connected"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args()

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    instance = load(HERE / "instance.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target_row = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target_row["execution_rank"] == 687 and target_row["baseline"] == "L0"
    assert target_row["rework_required"] is True and target_row["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 687,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0321-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0321-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert statement["canonical_formal_target"]["expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M0321-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_machine_debt"] == "M3"
    assert closure["theorem_complete"] is False
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["result"]["root_closed"] is True
    assert proof_receipt["accepted"] is proof_receipt["result"]["theorem_complete"] is False
    assert proof_blocker["root_closed"] is True and proof_blocker["theorem_complete"] is False
    assert proof_blocker["remaining_root_cut_set"] == FROZEN_OPEN_CUT
    assert proof_blocker["frozen_interface_defect"]["declaration"].endswith("CompactnessUpgrade")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    )
    assert prohibited.search(all_source) is None
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    for fragment in (
        "theorem recomposedMarkovKakutani", "continuousCompactnessUpgrade",
        "finiteFamilyStep E I K f", "assert_no_sorry markovKakutani_proof",
        "#print_validation_closure",
    ):
        assert fragment in validation_source, fragment
    assert "markovKakutani_proof" not in validation_source.split("theorem recomposedMarkovKakutani", 1)[1].split("assert_no_sorry", 1)[0]

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in SOURCE_BOUNDARIES.items():
        source = mathlib / relative
        olean = mathlib / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert olean.stat().st_size == expected["olean_bytes"]

    launcher = Path(HOME) / ".elan/bin/lake"
    assert sha256(launcher) == ELAN_LAUNCHER_SHA256
    lean = Path(run([str(launcher), "env", "which", "lean"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    lake = Path(run([str(launcher), "env", "which", "lake"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git")
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    assert sha256(git_executable) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=BASE_ENV)
    assert_network_isolation(bwrap)

    outputs = isolated_replay(lean, bwrap, pinned_lean_path(lean))
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "error:" not in combined
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) <= EXPECTED_AXIOMS
    assert reported_axioms(outputs["validation"], "Stage1Instances.THM_M_0321.markovKakutani_proof") == EXPECTED_AXIOMS
    assert reported_axioms(outputs["validation"], VALIDATION_DECLARATION) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 2
    closure_match = re.search(r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", outputs["validation"])
    assert closure_match is not None
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    observation = {
        "lean_output_sha256": {name: hashlib.sha256(output.encode()).hexdigest() for name, output in outputs.items()},
        "observed_axioms": sorted(EXPECTED_AXIOMS),
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
    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0321-PROOF"]
    assert len(spec["recipes"]) == 1 and spec["recipes"][0] == receipt["recipe"]
    assert receipt["target"] == {
        "declaration": "Stage1Instances.THM_M_0321.MarkovKakutaniTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "statement_source_sha256": EXPECTED_INPUTS["Statement.lean"],
        "registry_denominator_sha256": DENOMINATOR_SHA256,
        "exact_statement_delta": "none",
    }
    recipe = spec["recipes"][0]
    assert recipe["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert "bubblewrap" in recipe["network_enforcement"]
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["accepted_receipt_ids"] == []
    repository_state = receipt["repository_state"]
    assert repository_state["release_clean"] is False
    assert repository_state["tracked_patch_sha256"] == hashlib.sha256(b"").hexdigest()
    assert repository_state["tracked_patch_bytes"] == 0
    input_payload = [
        {"path": relative, "sha256": sha256(ROOT / relative)}
        for relative in (
            f"Stage1_Instances/{THEOREM}/Validation.lean",
            f"Stage1_Instances/{THEOREM}/check_validation.py",
            f"Stage1_Instances/{THEOREM}/validation-phase.md",
            f"Stage1_Instances/{THEOREM}/validation-spec.json",
        )
    ]
    assert repository_state["untracked_input_scope"] == [row["path"] for row in input_payload]
    assert repository_state["untracked_input_sha256"] == {
        row["path"]: row["sha256"] for row in input_payload
    }
    assert repository_state["untracked_input_bundle_sha256"] == hashlib.sha256(
        json.dumps(input_payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert repository_state["preexisting_lake_symlink_target_sha256"] == hashlib.sha256(
        os.readlink(LEAN_ROOT / ".lake").encode()
    ).hexdigest()
    change_impact = receipt["change_impact"]
    assert change_impact["exact_statement_changes"] == []
    assert change_impact["typed_graph_changes"] == []
    assert change_impact["authoritative_state_changes"] == []
    assert change_impact["exact_declarations_added"] == [VALIDATION_DECLARATION]
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["lean-toolchain"] == TOOLCHAIN_SHA256
    assert receipt["inputs"]["lake-manifest.json"] == MANIFEST_SHA256
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    environment = receipt["environment"]
    assert environment["lean_executable_sha256"] == sha256(lean)
    assert environment["lake_executable_sha256"] == sha256(lake)
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(git_executable)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_worktree_clean"] is True
    assert receipt["trust"]["accepted_foundation_policy"] is False
    assert receipt["trust"]["complete_transitive_tcb_inventory"] is False
    assert receipt["provenance"]["complete_provenance_gate"] == "fail_closed"
    assert receipt["hermeticity"]["decision"].startswith("fail_closed")
    assert receipt["independent_validation"]["decision"] == "fail_closed"
    assert receipt["result"]["lean_output_sha256"] == observation["lean_output_sha256"]
    assert receipt["result"]["observed_axioms"] == observation["observed_axioms"]
    assert receipt["result"]["validation_closure"] == observation["validation_closure"]
    assert receipt["result"]["exact_root_kernel_replay"] == "pass_provisional_nonrelease"
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["frozen_composition_gate"] == "fail_closed"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0321-PROOF.master_acceptance"
    assert receipt["remaining_root_cut_set"] == FROZEN_OPEN_CUT
    assert receipt["output_summary"] == ["PASS THM-M-0321 narrow validation", *SUMMARY_LINES]
    assert set(receipt["changed_paths"]) == set(CHANGED_PATHS)
    assert set(packet["changed_paths"]) == set(CHANGED_PATHS)
    assert packet["base_revision"] == BASE_REVISION and packet["known_failures"]
    status = git("status", "--short", "--untracked-files=all").splitlines()
    actual = {line[3:] for line in status if line[3:] != "Formalizations/Lean/.lake"}
    assert actual == set(CHANGED_PATHS), (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("PASS THM-M-0321 narrow validation")
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
