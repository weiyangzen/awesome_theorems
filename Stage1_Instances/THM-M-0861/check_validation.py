#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0861-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0861"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0861-VALIDATION"
THEOREM = "THM-M-0861"
BASE_REVISION = "61f7b69093a1a921bba3b39c1c58955f9b3a4808"
BASE_TREE = "5849148c92f4a72549a18481b3eda847afb1e3da"
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
EXPRESSION_SHA256 = "4e7919ed3b44379a42d69ef88cfb5e512248eccfe755392723cb6769c4f8e197"
DENOMINATOR_SHA256 = "1272c7806d6c29040abda962a5fd83037c2f57a04631ddd5507b6e84c46af230"
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
OPEN_ROOT_CUT = ["M0861-T-UPPER"]
PROVISIONAL_CLOSED = [
    "M0861-L-DEGREE-LE-MAX",
    "M0861-L-INCIDENCE-FIN",
    "M0861-L-COLOR-INJECTIVE",
    "M0861-L-SUP-LOWER",
    "M0861-T-LOWER",
    "M0861-B-SMALL-EDGE-COUNT",
    "M0861-L-SMALL-PALETTE-EMBED",
]
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
SOURCE_PROVENANCE = {
    "Mathlib/Combinatorics/Graph/Basic.lean": {
        "blob": "72ae0789f49228ac2fb458a9bf7da842d0638190",
        "source_sha256": "dc3f9c7793f8de09261868afeb7e1d8804914b90b1fc4615feb139f2452dd2b9",
        "olean_sha256": "4affbfa144a2039c6510cf4faf1d366836f297caa730683b9065bfc198e33f5e",
    },
    "Mathlib/Data/Set/Card.lean": {
        "blob": "1ca79eb8302a1a2ba01d994973a135386712af62",
        "source_sha256": "09942e2b66a4dfafd949dc32da33c41d3ada901769fda4ceb1f7e06dc8b0b5f5",
        "olean_sha256": "f9c99acb0b77cbe736df02464b0f2349f57ff5efe638fcd53a7b454e4472b62d",
    },
    "Mathlib/Data/Finset/Card.lean": {
        "blob": "d1c2c1e36ea9028aa27c4724c2c9d76afd9af35b",
        "source_sha256": "5566f2afb81cb80e2aa7349d8b04214f3667d84e4b81d965f85714ec5a8f0e27",
        "olean_sha256": "b8504bc80578476685d30420a182799a2e385bde6c35299494034e828767023d",
    },
    "Mathlib/Logic/Function/Basic.lean": {
        "blob": "44534ad0ffc9444b1758a0fdc099b216b0da6ac0",
        "source_sha256": "5dffbb69147f9bf2cfc8de6083b7eab88d0b297762052e5e81d19a77f346dc97",
        "olean_sha256": "0eaa970b546776cc0908bb720718e6b9d499e3e6b5c90836739f174d92352293",
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
    "README.md": "6e6e55e838121c6ff3650d9e6b2f87db961698814920eb3f4a838833b49402d0",
    "Statement.lean": "a6ce9ee3edd720d38fa9306324e38b48d5f0430a8b9513b9207e7808ea1b380d",
    "ObligationTree.lean": "066fe4c9e401d6a5c45fe7699cfca3278661f77b32404d4eb7151dfe5b8aa5be",
    "AnchorAudit.lean": "d109f2336caa28e017313e05572986ec1e1e2311d267b486789fb240552628e6",
    "Proof.lean": "fc9fab5aadcf161926b3f1efee51e6e0f47fb638cf940f91a4d0945edd3244db",
    "statement.json": "af40ef59543ec155fe465f78fc3d3393aa651952f108f70ea36a27366401fb3d",
    "anchor-audit.json": "3adb7aaf96cc2fa6959da59a6a4556a9447505ee6f4be4078e73db7e17bd1c34",
    "obligation-registry.json": "44f0fcb20dce6ed0c1d60302a41e0f58aa86d2c5c91bc6821e5ccb14e87629d3",
    "typed-graphs.json": "dc170c799a1fc6f9711befe8daf5b5629d7b600a851db130e8525a8372e83ea5",
    "validation-specs.json": "f315c8f6fe4e3514ab6c13266333e67e4b0440690a9b6b96684dea287b08b11a",
    "proof-receipt.json": "8cc938ba3d65f43f691b2a4b28794cd371f90f544662de51a6494593e59891aa",
    "proof-blocker.json": "08e546a93f3f1ac4da1f9c597b4d4146d08b6596da63d6e32a198b9c383f31f4",
    "instance.json": "6a4f30bd9aef94ec6416130d7cf3ff7ec35e9e13657a64099cef17f442d06418",
    "task-dag.json": "6c802c333cd0e8529e0b7f97b78a9eb2d2ec3b939ab3d0e995c794541a42cdc3",
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
    "PASS narrow kernel replay: statement, audited anchors, proof bodies, conditional handoff, and differential composition elaborated at trust zero",
    "PASS trust observation: ten checked roots are sorry-free and use only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen inputs, clean mathlib pin/tree/remote, six selected sources and oleans, toolchain, and license agree",
    "OPEN exact root: BoundedSatzCTarget has no inhabitant; accepted root remains M4 with cut M0861-T-UPPER",
    "FAIL CLOSED proof dependency: S56-M-0861-PROOF is worker-provisional rather than master-accepted",
    "FAIL CLOSED release gates: shared warm cache is not cold hermetic evidence and this worker is not a distinct signed verifier",
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
    return run(["/usr/bin/git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    """Remove nested Lean comments and strings for defense-in-depth scans."""
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
    roots = sorted(
        (path / ".lake" / "build" / "lib" / "lean").resolve()
        for path in (LEAN_ROOT / ".lake" / "packages").iterdir()
        if path.is_dir() and (path / ".lake" / "build" / "lib" / "lean").is_dir()
    )
    assert roots, "no pre-existing pinned compiled artifacts"
    return roots


def sandboxed_replay(lean: Path, bwrap: Path) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="m0861-validation-", dir="/tmp") as tmp_name:
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
            argv = base + ["--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0", "-t0"]
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
    node_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    local_tasks = load(HERE / "task-dag.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1415 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1415,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0861-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0861-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    dependency_accepted = (
        predecessor["state"] == "[x]"
        and proof_receipt.get("support_state") == "master_accepted"
    )
    assert dependency_accepted is False
    assert local_tasks["accepted_states"] == []
    assert all(task["state"] == "open" for task in local_tasks["tasks"])

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    canonical = statement["canonical_formal_target"]
    assert canonical["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0861.KonigEdgeColoringTarget"
    )
    assert canonical["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert canonical["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert node_specs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert {
        recipe["covered_obligation_ids"][0] for recipe in node_specs["recipes"]
    } == set(registry["frozen_denominators"]["inventory"])
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0861-ROOT")
    assert {
        "H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]
    } == ROOT_VECTOR
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["audit_complete"] is False
    assert graphs["closure_boundary"]["theorem_complete"] is False
    assert proof_receipt["item_id"] == "S56-M-0861-PROOF"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["provisionally_closed_obligation_ids"] == PROVISIONAL_CLOSED
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
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
    assert "theorem rootFromBoundedSatzC" in validation_source
    assert "(satzC : BoundedSatzCTarget" in validation_source
    assert "theorem konigEdgeColoringTarget_proof" not in validation_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert (LEAN_ROOT / ".lake").is_symlink()
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

    fixed_env = {
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    elan = Path("/home/sansha-2/.elan/bin/elan")
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
    proof_declarations = (
        "Stage1Instances.THM_M_0861_Proof.degree_le_maxDegree",
        "Stage1Instances.THM_M_0861_Proof.incidenceSet_finite",
        "Stage1Instances.THM_M_0861_Proof.incidentColor_injective",
        "Stage1Instances.THM_M_0861_Proof.maxDegree_le_of_degree_le",
        "Stage1Instances.THM_M_0861_Proof.lowerBound",
        "Stage1Instances.THM_M_0861_Proof.edgePaletteEmbedding",
        "Stage1Instances.THM_M_0861_Proof.edgeColorable_of_edge_ncard_le",
        "Stage1Instances.THM_M_0861_Proof.upperBound_of_boundedSatzC",
        "Stage1Instances.THM_M_0861_Proof.konigEdgeColoring_of_boundedSatzC",
    )
    for declaration in proof_declarations:
        assert printed_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
        assert printed_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    differential = "Stage1Instances.THM_M_0861_Validation.rootFromBoundedSatzC"
    assert printed_axioms(outputs["validation"], differential) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 1
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert all("error:" not in output for output in outputs.values())
    closure_match = re.search(
        r"VALIDATION_CLOSURE roots=(\d+) declarations=(\d+) modules=(\d+)",
        outputs["validation"],
    )
    assert closure_match is not None and int(closure_match.group(1)) == 10
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    observation = {
        "lean_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest()
            for name, output in outputs.items()
        },
        "closure": {
            "roots": 10,
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
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0861-PROOF"]
    assert len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert recipe["cwd"] == "."
    assert recipe["argv"] == [
        "/usr/bin/python3", "-I", "-B",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert set(recipe["covered_obligation_ids"]) == set(
        registry["frozen_denominators"]["required_machine"]
    )
    assert receipt["recipe"] == recipe
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False and receipt["accepted_receipt_ids"] == []
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
    assert receipt["first_failed_gate"] == "dependency.S56-M-0861-PROOF.master_acceptance"
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
