#!/usr/bin/env python3
"""Fail-closed executable validation for S56-M-0612-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0612"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0612-VALIDATION"
THEOREM = "THM-M-0612"
BASE_REVISION = "4c1d50aa6552eb6ec56338a663a5dff79a4ae2e3"
BASE_TREE = "e38ee217e0bb768c5c915905d1d0b04fc89e25f2"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
STATEMENT_SHA256 = "2de623b53340de741e2b691d81a0e1a9f0a6f74bbdeb133f7ebcc5a20d97f919"
DENOMINATOR_SHA256 = "2cad29b7c0b54afdec80a5d7ac1940a49cccfacdab64c1b75c27e140dd7a4bc8"
ROOT_VECTOR = {"H": "H2", "M": "M3", "R": "R4"}
OPEN_ROOT_CUT = ["M0612-T-SQUARED"]
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": STATEMENT_SHA256,
    "LocalEncoding.lean": "278177c5db75abff44ff5576ce8a6912c7f210f96f0b9f27097f895c6d62a117",
    "ObligationTree.lean": "0392a18a80b7cea4fcbba89e23941228ff861cd6406345bf134ef4b857773007",
    "DimensionTwo.lean": "282b485bfe5bed0dcc7cb68b30775252272e29d1ef1ebb7a9bdd1284d01100fd",
    "AnchorAudit.lean": "5b7ae6560bcae68afaedef4576dcd2a0c858ef4223b87461343188390ec12fc1",
    "instance.json": "b8fff47fae4911e633009ea85fbb6bc55168d5a44d99563d4eaa4a265122884d",
    "obligation-registry.json": "635af26d6d87637952beb03486a2e29b9f0cde834da54fc2539e800caf538850",
    "typed-graphs.json": "def7053233342a03342983a55bf7a8ec627a13dca40fc86914e07ffa4f0250b2",
    "validation-specs.json": "206da915511969ccf22b77e14a67d016699e4d345628238c24f6a4c90878858d",
    "anchor-audit-receipt.json": "b849d3a33993dbc3bc999e2832d93476f06e9b657ab07626b3582b9fb9c3acb7",
    "proof-receipt-2026-07-15-slot26.json": "01210378e747d9da81b4d64b6e782c2cff645d274effbf6a164b8ffd164cad5e",
    "check_obligation_tree.py": "bf643f6001168590a4eb7c23e1f837731c34877221aeecb5074fdc7ea58b3708",
    "check_proof.sh": "c340e6d91a5b4a4e31bfef188b9a30a5cbdf7d94e0112659a5b81d6599a36abf",
}
SOURCE_PROVENANCE = {
    "Mathlib/LinearAlgebra/Matrix/ToLin.lean": {
        "blob": "768a55390b60aaab28e90b1dc0d0f5d864747c6b",
        "source_sha256": "a58c81046f02ed406daaf24bd50ab7a68c5e5b43f906b6c8180aea740c49ac2a",
        "olean_sha256": "b654e6e727ecf3085b18c70f68eac0762dc73c8afb7c0c998b3a471c98cead57",
    },
    "Mathlib/MeasureTheory/Function/Jacobian.lean": {
        "blob": "262b0739135ae11eb54b9ab0b953e89d0bacc75f",
        "source_sha256": "8ef05ea1f035e9281c768c453536cfeb9e6bdc205657563628ebc81ee6de6c33",
        "olean_sha256": "21222dc7ba4286c223cbf9d755c93a9fd53d0ec9a02252c2e54c0ab334ff4030",
    },
    "Mathlib/MeasureTheory/Measure/Lebesgue/VolumeOfBalls.lean": {
        "blob": "09c30c53a7e7805e28222549f6d30558ac2cac67",
        "source_sha256": "a4fe84dfb7419d46de17ced885299a9f1d60626ab8b4aa912ecfd3af31cec895",
        "olean_sha256": "e1be0d7c2e9e0842df6981781871b88f485d38bf86177ed79ae990be4af9d68b",
    },
}
PROOF_DECLARATIONS = (
    "Stage1.THM_M_0612.symplectic_det_dimTwo",
    "Stage1.THM_M_0612.image_volume_eq_dimTwo",
    "Stage1.THM_M_0612.volume_ball_dimTwo",
    "Stage1.THM_M_0612.dimTwo_radiusSquaredObstruction",
)
COMPOSITION_DECLARATIONS = (
    "Stage1.THM_M_0612.radius_le_of_sq_le",
    "Stage1.THM_M_0612.root_of_radiusSquaredObstruction",
    "Stage1.THM_M_0612.Validation.rootFromRadiusSquaredObstruction",
)
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
    "PASS network-isolated trust-zero replay: exact statement, local encoding, dimension-two bodies, conditional composition, anchors, and validation audit elaborated",
    "PASS trust observation: seven audited declarations are sorry-free and use only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen inputs, clean mathlib pin/tree/remote, three source/object boundaries, tools, and license agree",
    "OPEN exact nonsqueezing root: the universal higher-dimensional RadiusSquaredObstruction has no proof body",
    "FAIL CLOSED proof dependency: S56-M-0612-PROOF is worker-provisional and its receipt is unaccepted with root_kernel_closed=false",
    "FAIL CLOSED release gates: the shared warm cache is not cold hermetic evidence and this worker is not a distinct signed verifier",
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


def code_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    depth = 0
    index = 0
    in_string = False
    while index < len(source):
        if not in_string and source.startswith("/-", index):
            depth += 1
            output.extend("  ")
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            output.extend("  ")
            index += 2
        elif depth:
            output.append("\n" if source[index] == "\n" else " ")
            index += 1
        elif not in_string and source.startswith("--", index):
            end = source.find("\n", index)
            end = len(source) if end < 0 else end
            output.extend(" " * (end - index))
            index = end
        elif source[index] == '"':
            in_string = not in_string
            output.append(" ")
            index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if source[index] == "\n" else " ")
                index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL
    )
    matches = pattern.findall(output)
    assert matches, f"missing axiom report for {declaration}"
    return {part.strip() for part in matches[-1].split(",") if part.strip()}


def compiled_roots() -> list[Path]:
    roots = sorted(
        (path / ".lake/build/lib/lean").resolve()
        for path in (LEAN_ROOT / ".lake/packages").iterdir()
        if path.is_dir() and (path / ".lake/build/lib/lean").is_dir()
    )
    local = (LEAN_ROOT / ".lake/build/lib/lean").resolve()
    if local.is_dir():
        roots.append(local)
    assert roots, "no pre-existing pinned compiled artifacts"
    return roots


def sandboxed_replay(lean: Path, bwrap: Path) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="m0612-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        names = (
            "Statement.lean", "LocalEncoding.lean", "DimensionTwo.lean",
            "ObligationTree.lean", "AnchorAudit.lean", "Validation.lean",
        )
        for name in names:
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()
        dependency_path = ":".join(str(path) for path in compiled_roots())
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp / "home"), "--setenv", "TMPDIR",
            str(tmp), "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1", "--chdir",
            str(tmp),
        ]

        def lean_run(name: str, local_imports: bool, emit_olean: bool) -> str:
            lean_path = f"{tmp}:{dependency_path}" if local_imports else dependency_path
            argv = base + ["--setenv", "LEAN_PATH", lean_path, str(lean), "--trust=0", "-t0"]
            if emit_olean:
                argv += ["-o", Path(name).with_suffix(".olean").name]
            argv.append(name)
            return run(argv)

        return {
            "statement": lean_run("Statement.lean", False, True),
            "local_encoding": lean_run("LocalEncoding.lean", True, True),
            "dimension_two": lean_run("DimensionTwo.lean", True, True),
            "obligation_tree": lean_run("ObligationTree.lean", True, True),
            "anchor_audit": lean_run("AnchorAudit.lean", False, False),
            "validation": lean_run("Validation.lean", True, False),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    instance = load(HERE / "instance.json")
    local_tasks = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    node_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt-2026-07-15-slot26.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 256 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 256,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0612-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0612-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    assert local_tasks["accepted_states"] == []
    assert all(task["state"] == "open" for task in local_tasks["tasks"])

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == []
    assert instance["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_against_statement_sha256"] == STATEMENT_SHA256
    assert len(registry["obligations"]) == 26
    required_machine = registry["frozen_denominators"]["required_machine"]
    assert len(required_machine) == 24
    root = next(row for row in registry["obligations"] if row["obligation_id"] == "M0612-ROOT")
    assert root["statement_fingerprint"] == f"lean-source:v1:sha256:{STATEMENT_SHA256}"
    assert root["terminal_proof_body_id"] is None
    higher = next(row for row in registry["obligations"] if row["obligation_id"] == "M0612-B-HIGHER")
    assert higher["terminal_proof_body_id"] is None
    assert node_specs["item_id"] == "S56-M-0612-OBLIGATION_TREE"
    assert len(node_specs["recipes"]) == 26
    assert all(recipe["covered_declarations"] == [] for recipe in node_specs["recipes"])
    assert {tuple(recipe["argv"]) for recipe in node_specs["recipes"]} == {
        ("python3", "Stage1_Instances/THM-M-0612/check_obligation_tree.py")
    }
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["root_machine_debt"] == "M3" and closure["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert proof_receipt["item_id"] == "S56-M-0612-PROOF"
    assert proof_receipt["accepted"] is False and proof_receipt["verdict"] == "no_state_change"
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["partial_declarations_kernel_closed"] is True
    assert proof_receipt["result"]["proof_phase_complete"] is False
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    for name in (
        "Statement.lean", "LocalEncoding.lean", "DimensionTwo.lean",
        "ObligationTree.lean", "AnchorAudit.lean", "Validation.lean",
    ):
        source = code_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, name
    validation_source = code_without_comments_and_strings((HERE / "Validation.lean").read_text())
    assert "theorem rootFromRadiusSquaredObstruction" in validation_source
    assert "(geometry : RadiusSquaredObstruction" in validation_source
    assert "theorem statementShape_proof" not in validation_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    mathlib = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in SOURCE_PROVENANCE.items():
        source = mathlib / relative
        olean = mathlib / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=mathlib) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]

    tool_root = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin"
    lean = tool_root / "lean"
    lake = tool_root / "lake"
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    assert sha256(Path("/usr/bin/git")) == GIT_SHA256
    fixed_env = {
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    assert LEAN_COMMIT in run([str(lean), "--version"], env=fixed_env)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], env=fixed_env)

    outputs = sandboxed_replay(lean, bwrap)
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    assert all("error:" not in output for output in outputs.values())
    for declaration in PROOF_DECLARATIONS:
        assert printed_axioms(outputs["dimension_two"], declaration) == EXPECTED_AXIOMS
        assert printed_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    for declaration in COMPOSITION_DECLARATIONS:
        assert printed_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 1
    closure_match = re.search(
        r"VALIDATION_CLOSURE roots=(\d+) declarations=(\d+) modules=(\d+)",
        outputs["validation"],
    )
    assert closure_match is not None and int(closure_match.group(1)) == 7
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unexpected_axioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    observation = {
        "lean_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest() for name, output in outputs.items()
        },
        "trust_closure_observation": {
            "roots": 7,
            "declarations": int(closure_match.group(2)),
            "modules": int(closure_match.group(3)),
            "axioms": sorted(EXPECTED_AXIOMS),
            "unexpected_axioms": [],
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
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0612-PROOF"]
    assert len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert recipe["cwd"] == "."
    assert recipe["argv"] == [
        "/usr/bin/python3", "-I", "-B",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert set(recipe["covered_obligation_ids"]) == set(required_machine)
    assert receipt["recipe"] == recipe
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False and receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["canonical_target"]["statement_source_sha256"] == STATEMENT_SHA256
    assert receipt["canonical_target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    for name in ("Validation.lean", "check_validation.py", "validation-spec.json"):
        assert receipt["inputs"][name] == sha256(HERE / name), name
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert receipt["result"]["lean_output_sha256"] == observation["lean_output_sha256"]
    assert receipt["result"]["trust_closure_observation"] == observation["trust_closure_observation"]
    assert receipt["result"]["proof_dependency_master_acceptance"] == "fail_closed"
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["open_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["result"]["complete_trust_provenance_gate"] == "fail_closed"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt["first_failed_gate"] == "dependency.S56-M-0612-PROOF.master_acceptance"
    assert blocker["first_failed_gate"] == receipt["first_failed_gate"]
    assert blocker["root_kernel_closed"] is blocker["validation_phase_complete"] is False
    assert blocker["audit_complete"] is blocker["theorem_complete"] is False
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
        assert packet["known_failures"] == receipt["known_failures"]
        status = git("status", "--short", "--untracked-files=all")
        actual = [
            line[3:] for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        ]
        assert sorted(actual) == sorted(CHANGED_PATHS), (actual, CHANGED_PATHS)

    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
