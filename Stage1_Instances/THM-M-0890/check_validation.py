#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0890-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


if not __debug__:
    raise SystemExit("check_validation.py requires Python assertions")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0890"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0890-VALIDATION"
THEOREM = "THM-M-0890"
BASE_REVISION = "fd50bb07f6632a2ad0bdc17737c200432ee242c8"
BASE_TREE = "ed66432029954bfa5b17e0afda5f3817eeb32d48"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
ELAN_LAKE_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPRESSION_SHA256 = "512ebe658ca83b7fb4bb3d3565122d065e3bc6e589898b4f3cf74ab2e12ea54d"
DENOMINATOR_SHA256 = "259c6e160437f0fc2646c6f1e302441c3e129c6d3e70346d04438ea3f7a45169"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_INPUTS = {
    "Statement.lean": "beb6cbe0437f78f26188cc3ed1ebe82bed84d2a07f1f8ea1abd78468740a787f",
    "ObligationTree.lean": "6959e302e3676c172f1db7003014b56e153057f367ecaebb3b8c81a86bf27ff2",
    "Proof.lean": "b41705e275a454f9412a05b8f09b5be8701ff989840c7be216629824a5b08e68",
    "statement.json": "dd9b94824f9f5e3a4f8627da05c132a69fcd18cdf476a11046d253ec4d78be21",
    "anchor-audit.json": "b922f69cb16eed05e8f29f281460a928e787619a7c7f4c923ea312a1bf098549",
    "obligation-registry.json": "079b565a392e4e81e291e3bed8b45d4b6b77e51668a733bce7435b8c89857110",
    "typed-graphs.json": "8c9906787a3fe386d98ddef9442904ce43f63eeead34c15a4f17ca664eaf0903",
    "validation-specs.json": "45f9587856a82ef19ffac2e21f180c67dc3a16d00ee9518638b74f9fb21675ed",
    "proof-receipt.json": "c78f5dac72be0e6e7eedeb1cd66b2d6ccb5a4df62634d859b9fc845328e76efa",
    "instance.json": "030d142bc502f89b768709136ebac408d8fe02d2d779de272291944c0ada8101",
    "task-dag.json": "8540d20add89f3528bbf1d69969025828862dd3043d30eeae2f4db8890dd74c7",
    "source-statement-crosswalk.md": "9d1bdd83df32c11c18262a16d5f20ce3e3ab29b2cd73b1e2e1efd14dee2bfebf",
    "Validation.lean": "d61056333f26855318bce6ff50de8f71f133814c212bf56545a62880ab9bbdce",
    "validation-spec.json": "d3070f767b6ece9ab23cd85eb419a783d20a768f64121311f1196d5b6fdb6949",
}
POLICY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "e999167643cde6dbccbde134545710ae92cc16a42b615c8be6160211723ce2a4",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "faef3cb448c94bc4a3b9ec9bf2ccc14bb637e69af3e33ee2b2e30c6f3ade45e5",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
SOURCE_BOUNDARIES = {
    "Mathlib/Combinatorics/SimpleGraph/Clique.lean": {
        "blob": "d738a06a31bbb198287b8cdbccdfc032257cb50c",
        "source_sha256": "18cce0904728a2c5db839682aebe39f1f0ebb9213971ef9b09c93ba1a17e9cf2",
        "olean_sha256": "e7bfc9f5091fdfff969840ffa3208f9c71a20bf4c5f2497ff99d39a5cc90c3c2",
        "olean_bytes": 350792,
    },
    "Mathlib/Combinatorics/SimpleGraph/LapMatrix.lean": {
        "blob": "5cdaded28624ebd6e8ca69bb4f9696c71a550d54",
        "source_sha256": "8a8ca58ac3a8c808973531ce8bff0610b4552a07dbfca0f74d2e5e92efa88612",
        "olean_sha256": "0fca99c608edb807b3c425d8d08bd6a1c3a137952b92d028b552c8cdd4ce6b53",
        "olean_bytes": 194392,
    },
    "Mathlib/Analysis/Matrix/PosDef.lean": {
        "blob": "465685f996335eb3aaaded9db231205c9dafa1be",
        "source_sha256": "e61c86114386b24cbf757026f61201c768b305ece890853404175fdb9d4269d5",
        "olean_sha256": "325eeedcce5e1ffcc2a16f479cd364d13e5ea89c93df11ed7faa22eea9d890bf",
        "olean_bytes": 177616,
    },
}
PROOF_IDS = [
    "M0890-ROOT", "M0890-S-TARGET", "M0890-S-LEAST",
    "M0890-S-INDEPENDENCE", "M0890-S-BOUNDARY", "M0890-S-TRANSPORT",
    "M0890-S-FOUNDATION", "M0890-N-MAX-WITNESS", "M0890-N-LEAST-MIN",
    "M0890-L-LEAST-NEGATIVE", "M0890-N-DENOMINATOR",
    "M0890-L-REGULAR-ONES", "M0890-L-ONES-ORTHOGONAL",
    "M0890-C-HOFFMAN-MATRIX", "M0890-L-COMMON-EIGENBASIS",
    "M0890-L-HOFFMAN-PSD", "M0890-C-PRINCIPAL", "M0890-L-PSD-PRINCIPAL",
    "M0890-L-INDEPENDENT-ZERO", "M0890-T-RESTRICTED-FORM",
    "M0890-C-ONES-VECTOR", "M0890-L-QUADRATIC-EVAL",
    "M0890-B-ALPHA-POSITIVE", "M0890-L-SCALAR-ESTIMATE",
    "M0890-T-DIVISION-FREE", "M0890-T-ASSEMBLE",
]
COVERED_IDS = PROOF_IDS + ["M0890-X-PROVENANCE", "M0890-X-TRUST"]
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_0890_Proof.leastAdjacencyEigenvalue_le_eigenvalue",
    "Stage1Instances.THM_M_0890_Proof.leastAdjacencyEigenvalue_neg",
    "Stage1Instances.THM_M_0890_Proof.denominatorPositive_proof",
    "Stage1Instances.THM_M_0890_Proof.shiftedAdjacency_posSemidef",
    "Stage1Instances.THM_M_0890_Proof.independentSet_adjacency_quadratic_zero",
    "Stage1Instances.THM_M_0890_Proof.independentSet_characteristic_norm",
    "Stage1Instances.THM_M_0890_Proof.regular_adjacency_mulVec_one",
    "Stage1Instances.THM_M_0890_Proof.independentSet_adjacency_one",
    "Stage1Instances.THM_M_0890_Proof.one_dotProduct_one_real",
    "Stage1Instances.THM_M_0890_Proof.centered_shifted_quadratic",
    "Stage1Instances.THM_M_0890_Proof.independentSet_scalar_nonnegative",
    "Stage1Instances.THM_M_0890_Proof.indepNum_pos",
    "Stage1Instances.THM_M_0890_Proof.maximumIndependentSetEstimate_proof",
    "Stage1Instances.THM_M_0890_Proof.divisionFreeInequality_proof",
    "Stage1Instances.THM_M_0890_Proof.ratioAssembly_proof",
    "Stage1Instances.THM_M_0890_Proof.hoffmanRatioBound_proof",
)
VALIDATION_DECLARATIONS = (
    "Stage1Instances.THM_M_0890_Validation.exactDivisionFreeReplay",
    "Stage1Instances.THM_M_0890_Validation.exactRootReplay",
)
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
]
PACKET_COMMANDS = [
    "python3 Docs/tools/check_stage1_standard.py",
    "python3 scripts/stage1_target.py check",
    "python3 scripts/stage1_target.py show THM-M-0890",
    "python3 -I -B Stage1_Instances/THM-M-0890/check_validation.py --probe",
    "python3 -I -B Stage1_Instances/THM-M-0890/check_validation.py --worker-packet .stage1-worker-selftest.json",
    "python3 -m json.tool Stage1_Instances/THM-M-0890/validation-spec.json",
    "python3 -m json.tool Stage1_Instances/THM-M-0890/validation-receipt.json",
    "python3 -m json.tool .stage1-worker-selftest.json",
    "PYTHONPYCACHEPREFIX=/tmp/stage1-m0890-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0890/check_validation.py",
    "git diff --check -- Stage1_Instances/THM-M-0890 .stage1-worker-selftest.json",
]
PACKET_OUTPUT_SUMMARY = (
    "Network-isolated trust-zero fresh-output replay passed for the exact Hoffman-bound "
    "statement, frozen terminal composition, repo-local proof root, and two exact-type aliases. "
    "Eighteen declarations were sorry-free and used only propext, Classical.choice, and "
    "Quot.sound; the transitive environment walk found no unexpected axiom or unsafe "
    "declaration, and selected direct pinned provenance matched. Proof master acceptance, ten "
    "internal composition bindings, complete trust/provenance, cold hermetic replay, "
    "distinct-runner independence, AUDIT-Z, THEOREM-Z, and theorem completion remain fail-closed."
)
SUMMARY_LINES = [
    "PASS THM-M-0890 narrow validation",
    "PASS network-isolated kernel replay: exact statement, frozen terminal composition, proof root, and exact-type validation aliases elaborated at trust zero",
    "PASS trust observation: eighteen declarations are sorry-free and report exactly propext, Classical.choice, and Quot.sound; closure has no unexpected axiom or unsafe declaration",
    "PASS selected provenance: frozen inputs, local proof-body location, three direct mathlib source/olean boundaries, clean pin, license, and tool identities agree",
    "FAIL CLOSED authority: proof is worker-self-tested but not master-accepted; authoritative instance and graph remain planned pre-proof H1/M3/R4 with ten internal composition plans unreconciled",
    "FAIL CLOSED foundation/trust: the observed axiom ceiling is not an accepted profile and complete transitive provenance and TCB closure remain open",
    "FAIL CLOSED hermetic release: shared warm .lake is not a clean-checkout empty-cache cold build, offline restoration, or deterministic TCB/SBOM bundle",
    "FAIL CLOSED independent release: exact-type aliases share this worker, checkout, proof body, kernel, and cache; no distinct signed verifier exists",
    "audit_complete=false; theorem_complete=false",
]


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
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


def source_without_comments_and_strings(source: str) -> str:
    """Erase nested Lean comments, line comments, and strings for lexical defense."""
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif in_string:
            if char == "\\" and index + 1 < len(source):
                output.extend("  ")
                index += 2
            elif char == '"':
                in_string = False
                output.append(" ")
                index += 1
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif pair == "/-":
            depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            while index < len(source) and source[index] != "\n":
                output.append(" ")
                index += 1
        elif char == '"':
            in_string = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    assert depth == 0 and not in_string, "unterminated Lean comment or string"
    return "".join(output)


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output, re.DOTALL,
    )
    assert match is not None, f"missing axiom report: {declaration}"
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


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


def isolated_replay(lean: Path, bwrap: Path, lean_path: str) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0890-validation-", dir="/tmp") as temp_name:
        temp = Path(temp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (temp / name).write_bytes((HERE / name).read_bytes())
        (temp / "home").mkdir()
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(temp), str(temp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(temp / "home"),
            "--setenv", "TMPDIR", str(temp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(temp),
        ]

        def lean_run(name: str, module_path: str) -> str:
            return run(base + [
                "--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0",
                "-o", name.replace(".lean", ".olean"), name,
            ])

        outputs: dict[str, object] = {}
        outputs["statement"] = lean_run("Statement.lean", lean_path)
        local_path = f"{temp}:{lean_path}"
        outputs["obligation_tree"] = lean_run("ObligationTree.lean", local_path)
        outputs["proof"] = lean_run("Proof.lean", local_path)
        outputs["validation"] = lean_run("Validation.lean", local_path)
        outputs["olean_sha256"] = {
            name: sha256(temp / name)
            for name in ("Statement.olean", "ObligationTree.olean", "Proof.olean", "Validation.olean")
        }
        return outputs


def observe() -> dict[str, object]:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in POLICY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"changed policy input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert mathlib_entry["url"] == MATHLIB_REMOTE
    assert (LEAN_ROOT / ".lake").is_symlink()
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    for relative, expected in SOURCE_BOUNDARIES.items():
        source = MATHLIB / relative
        olean = MATHLIB / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]
        assert olean.stat().st_size == expected["olean_bytes"]

    lake_launcher = Path(HOME) / ".elan/bin/lake"
    assert sha256(lake_launcher) == ELAN_LAKE_SHA256
    lean = Path(run([str(lake_launcher), "env", "which", "lean"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    lake = Path(run([str(lake_launcher), "env", "which", "lake"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git")
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(python) == PYTHON_SHA256 and sha256(git_executable) == GIT_SHA256
    assert sha256(bwrap) == BWRAP_SHA256
    lean_version = run([str(lean), "--version"], env=BASE_ENV)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    lean_path = run(
        [str(lake_launcher), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=BASE_ENV
    ).strip()

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited Lean device in {name}"

    outputs = isolated_replay(lean, bwrap, lean_path)
    proof_output = str(outputs["proof"])
    validation_output = str(outputs["validation"])
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(proof_output + validation_output, declaration) == EXPECTED_AXIOMS
    for declaration in VALIDATION_DECLARATIONS:
        assert reported_axioms(validation_output, declaration) == EXPECTED_AXIOMS
    assert validation_output.count("Declarations are sorry-free!") == 18
    combined = "".join(str(outputs[key]) for key in (
        "statement", "obligation_tree", "proof", "validation"
    ))
    assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
    closure_match = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", validation_output
    )
    assert closure_match is not None
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in validation_output
    assert "VALIDATION_CLOSURE unexpected_axioms=[]" in validation_output
    assert "VALIDATION_CLOSURE unsafe=[]" in validation_output
    return {
        "lean_output_sha256": {
            key: hashlib.sha256(str(outputs[key]).encode()).hexdigest()
            for key in ("statement", "obligation_tree", "proof", "validation")
        },
        "fresh_olean_sha256": outputs["olean_sha256"],
        "closure": {
            "declarations": int(closure_match.group(1)),
            "modules": int(closure_match.group(2)),
            "axioms": EXPECTED_AXIOM_LIST,
            "unexpected_axioms": [],
            "unsafe_declarations": [],
        },
        "tools": {
            "lean": str(lean), "lake": str(lake), "python": str(python),
            "git": str(git_executable), "bubblewrap": str(bwrap),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    observation = observe()
    if args.probe:
        print(json.dumps(observation, sort_keys=True))
        return

    assert args.worker_packet is not None, "final self-test requires --worker-packet"
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(args.worker_packet)
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1440 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 1440,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0890-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0890-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and local_task["depends_on"] == ["S56-M-0890-PROOF"]
    assert local_dag["accepted_states"] == []

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0890.HoffmanRatioBoundTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == "M0890-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == PROOF_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["closed_obligations"] == []
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["remaining_machine_root_cut_set"] == [
        "M0890-N-DENOMINATOR", "M0890-L-SCALAR-ESTIMATE",
    ]
    assert len(graphs["unverified_decomposition_plans"]) == 10
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["mapped_proof_graph_ids"] == PROOF_IDS
    assert proof_receipt["closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["unverified_internal_composition_count"] == 10
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["depends_on"] == ["S56-M-0890-PROOF"] and spec["intent"] == "validate"
    assert len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert recipe["recipe_id"] == "S56-M-0890-VALIDATION-narrow-v1"
    assert recipe["cwd"] == "." and recipe["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["timeout_seconds"] == 600 and recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0 and "--unshare-net" in recipe["network_enforcement"]
    assert recipe["covered_obligation_ids"] == COVERED_IDS
    assert recipe["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": (
            "exact nine-line UTF-8 PASS/FAIL-CLOSED summary bound by validation-receipt.json"
        ),
    }]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-0890-PROOF"]
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE and receipt["verdict"] == "blocked"
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is receipt["content_addressed"] is False
    assert receipt["covered_obligation_ids"] == COVERED_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    for name, expected in POLICY_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["result"]["lean_output_sha256"] == observation["lean_output_sha256"]
    assert receipt["result"]["fresh_olean_sha256"] == observation["fresh_olean_sha256"]
    assert receipt["result"]["transitive_environment_observation"] == observation["closure"]
    assert receipt["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert receipt["result"]["exact_type_alias_replay"] == "provisional_pass_same_worker"
    assert receipt["result"]["proof_master_acceptance"] == "fail_closed"
    assert receipt["result"]["accepted_root_machine_debt"] == "M3"
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["unreconciled_internal_composition_plans"] == 10
    assert receipt["result"]["complete_provenance_tcb_gate"] == "fail_closed"
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0890-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    assert receipt["recipe"] == recipe
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": hashlib.sha256("\n".join(SUMMARY_LINES).encode()).hexdigest(),
        "expected_line_count": 9,
        "exit_code": 0,
        "raw_logs_retained": False,
        "raw_log_sha256": None,
        "boundary": (
            "Subprocess semantic hashes and the exact final summary are retained; no raw release "
            "log bundle is claimed."
        ),
    }

    expected_keys = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet) == expected_keys
    assert set(receipt["changed_paths"]) == set(CHANGED_PATHS)
    assert set(packet["changed_paths"]) == set(CHANGED_PATHS)
    assert packet["commands"] == PACKET_COMMANDS
    assert packet["output_summary"] == PACKET_OUTPUT_SUMMARY
    assert packet["known_failures"] == receipt["known_failures"]
    actual_changed = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == set(CHANGED_PATHS), (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
