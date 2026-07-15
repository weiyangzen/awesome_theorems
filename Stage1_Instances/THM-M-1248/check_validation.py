#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-1248-VALIDATION."""

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


if not __debug__:
    raise RuntimeError("validation requires Python assertions; optimized mode is forbidden")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1248"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1248-VALIDATION"
THEOREM = "THM-M-1248"
BASE_REVISION = "fc1568a2997ca815b767b8cc172f3d4d339bf3b9"
BASE_TREE = "635319193989301e577a430446e682952c51c538"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
LAKE_LAUNCHER_SHA256 = "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385"
EXPRESSION_SHA256 = "f6a65804d336bcc7f72d03e35c0e43715fc92c648507b805117a09ec13648d5b"
DENOMINATOR_SHA256 = "a0c3a82c3c3655d323873c8e3dc1164bbe6021d60d32521261f7d82cdcceaa11"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "e3e257722b165a262b421b602e0a6e898251549b06c8bc65539dc6ebd2403c00",
    "ObligationTree.lean": "97334a1ed6471cf8b07774a877651930a63292706f8cbb9051f90d46c5eee8dd",
    "Proof.lean": "ff1d55daac75a934bfb807596d424310f080836c02cc13b05c054e81aeac7f13",
    "statement.json": "a787b9e129b16974309d7c0b4a3d7a576eaa7c40a7b11ce1af7c6836318948ba",
    "anchor-audit.json": "2548e53752cf1cffeceb3a288550997500317e8361b6a34ffd9f7b149b3efac5",
    "obligation-registry.json": "2e1d91b7ee8ff66bcad84eeeb3c21b5ca9c0b670274cac11fc929b5b5474841e",
    "typed-graphs.json": "4b4a42007bfbc4789584aac36e47dadf03da31b57b945a328cc6b2c5bd8b3fad",
    "proof-receipt.json": "6edc8ec3c70fee43d04040e47219d4063ddb025fa1a6228991d60843d79a64b8",
}
SOURCE_BOUNDARIES = {
    "Mathlib/Analysis/Analytic/Uniqueness.lean": {
        "blob": "31d6205aa1f2b4cfc60a3af581b4ed2c1df88c69",
        "source_sha256": "c396287ccdf62666424020214fc8c123ec5024a25eee01f02962f80e22b8656c",
        "olean_sha256": "a30459265f5394063a1aba859d38f0f95fa8af85b357d2b7fad52898a0a9fbc1",
        "olean_bytes": 122032,
        "declaration": "AnalyticOnNhd.eqOn_zero_of_preconnected_of_eventuallyEq_zero",
    },
    "Mathlib/Analysis/Calculus/ContDiff/Defs.lean": {
        "blob": "48fa38706dd12f7fcf7fc44d3c51a6e763ed5132",
        "source_sha256": "562b303f3e948decac52c1ac88dc8e100311a42c0c64a77b4b0972fc85fa7f88",
        "olean_sha256": "583529ccee3458e367b88fe1edd6c0da3c166888da0da17894aa728ee8cfe1a7",
        "olean_bytes": 649272,
        "declaration": "ContDiff.analyticOnNhd",
    },
}
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_1248.compactlySupported_analytic_eq_zero",
    "Stage1Instances.THM_M_1248.caffarelliKohnNirenbergTarget",
)
VALIDATION_DECLARATIONS = (
    "Stage1Instances.THM_M_1248.Validation.independentlyCompactlySupportedTopEqZero",
    "Stage1Instances.THM_M_1248.Validation.independentlyReconstructedFrozenTarget",
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
    "PASS narrow kernel replay: the exact frozen root and a no-Proof differential reconstruction elaborated at trust zero",
    "PASS trust observation: both routes report only propext, Classical.choice, and Quot.sound and are transitively sorry-free",
    "PASS selected provenance: local inputs, pinned mathlib revision/tree, two direct source/olean boundaries, license, and tools agree",
    "FAIL CLOSED source identity: ContDiff Real top is analytic omega rather than smooth infinity, and the radial weight mixes Pi/sup with Euclidean/L2 norms",
    "FAIL CLOSED complete trust/provenance: the proof predecessor is unaccepted, the frozen graph is unreconciled, and no complete TCB/source closure exists",
    "FAIL CLOSED hermetic/independent: the replay uses a shared warm cache in this worker, not a cold clean restoration or distinct signed verifier",
]


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


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
        timeout: int = 600) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


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
    pattern = re.compile(re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL)
    matches = pattern.findall(output)
    assert len(matches) == 1, f"missing or duplicate axiom report for {declaration}"
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


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
    with tempfile.TemporaryDirectory(prefix="stage1-m1248-validation-", dir="/tmp") as name:
        tmp = Path(name).resolve()
        for source in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / source, tmp / source)
        (tmp / "home").mkdir()
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp / "home"), "--setenv", "TMPDIR", str(tmp),
            "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(source: str, path: str, emit_olean: bool) -> str:
            argv = base + ["--setenv", "LEAN_PATH", path, str(lean), "--trust=0", "-t0", "--root", str(tmp)]
            if emit_olean:
                argv += ["-o", source.replace(".lean", ".olean")]
            argv.append(source)
            return run(argv, timeout=300)

        return {
            "statement": lean_run("Statement.lean", lean_path, True),
            "obligation": lean_run("ObligationTree.lean", f"{tmp}:{lean_path}", True),
            "proof": lean_run("Proof.lean", f"{tmp}:{lean_path}", False),
            "validation": lean_run("Validation.lean", f"{tmp}:{lean_path}", False),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 428 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 428,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-1248-PROOF"], "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1248-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for source, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / source) == expected, f"stale validation input: {source}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["remaining_root_cut_set"] == ["M1248-T-ALL-PARAMS"]
    root_node = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1248-ROOT")
    assert root_node["machine_debt"] == "M3"
    assert proof_receipt["item_id"] == "S56-M-1248-PROOF"
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["accepted"] is False and proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["exact_frozen_root_kernel_closed"] is True
    assert proof_receipt["result"]["source_claim_proved"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["first_failed_completion_gate"] == "S56-5.1-EXACT-TARGET-IDENTITY-OR-TRANSPORT"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b", re.MULTILINE,
    )
    sources = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    combined_source = "\n".join(source_without_comments((HERE / name).read_text()) for name in sources)
    assert prohibited.search(combined_source) is None
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    imports = validation_source.split("/-!", 1)[0]
    assert "import Proof" not in imports and "import ObligationTree" not in imports
    for marker in (
        "theorem frozenOrder_eq_omega", "theorem frozenOrder_ne_infinity",
        "theorem independentlyCompactlySupportedTopEqZero",
        "theorem independentlyReconstructedFrozenTarget",
        "assert_no_sorry independentlyReconstructedFrozenTarget", "#print_validation_closure",
    ):
        assert marker in validation_source, marker

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
        assert sha256(olean) == expected["olean_sha256"] and olean.stat().st_size == expected["olean_bytes"]

    launcher = Path(HOME) / ".elan/bin/lake"
    assert sha256(launcher) == LAKE_LAUNCHER_SHA256
    lean = Path(run([str(launcher), "env", "which", "lean"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    lake = Path(run([str(launcher), "env", "which", "lake"], cwd=LEAN_ROOT, env=BASE_ENV).strip())
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git")
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    assert sha256(git_executable) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=BASE_ENV)

    outputs = isolated_replay(lean, bwrap, pinned_lean_path(lean))
    combined_output = "\n".join(outputs.values())
    assert "sorryAx" not in combined_output and "declaration uses 'sorry'" not in combined_output
    assert all("error:" not in output for output in outputs.values())
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    for declaration in VALIDATION_DECLARATIONS:
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 4
    closure = re.search(r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", outputs["validation"])
    assert closure is not None
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    observation = {
        "lean_output_sha256": {name: hashlib.sha256(output.encode()).hexdigest() for name, output in outputs.items()},
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "validation_closure": {
            "declarations": int(closure.group(1)), "modules": int(closure.group(2)),
            "bodyless_nonaxioms": [], "unsafe_declarations": [],
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
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-1248-PROOF"]
    assert len(spec["recipes"]) == 1 and spec["recipes"][0] == receipt["recipe"]
    recipe = spec["recipes"][0]
    assert recipe["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["cwd"] == "." and recipe["timeout_seconds"] == 600
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked" and receipt["accepted"] is False
    assert receipt["proposed_state"] == "[_]" and receipt["release_grade"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["target"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    for source, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][source] == expected
    assert receipt["inputs"]["Validation.lean"] == sha256(HERE / "Validation.lean")
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    repository_state = receipt["repository_state"]
    assert repository_state["release_clean"] is False
    input_paths = [
        f"Stage1_Instances/{THEOREM}/Validation.lean",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
        f"Stage1_Instances/{THEOREM}/validation-phase.md",
        f"Stage1_Instances/{THEOREM}/validation-spec.json",
    ]
    payload = [{"path": path, "sha256": sha256(ROOT / path)} for path in input_paths]
    assert repository_state["untracked_input_scope"] == input_paths
    assert repository_state["untracked_input_sha256"] == hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert repository_state["preexisting_untracked_lake_symlink_target_sha256"] == hashlib.sha256(
        os.readlink(LEAN_ROOT / ".lake").encode()
    ).hexdigest()
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
    assert receipt["environment"]["lean_executable_sha256"] == sha256(lean)
    assert receipt["environment"]["lake_executable_sha256"] == sha256(lake)
    assert receipt["environment"]["bubblewrap_executable_sha256"] == sha256(bwrap)
    assert receipt["environment"]["python_executable_sha256"] == sha256(python)
    assert receipt["environment"]["git_executable_sha256"] == sha256(git_executable)
    result = receipt["result"]
    assert result["lean_output_sha256"] == observation["lean_output_sha256"]
    assert result["observed_axioms"] == observation["observed_axioms"]
    assert result["validation_closure"] == observation["validation_closure"]
    assert result["exact_frozen_root_kernel_replay"] == "provisional_pass"
    assert result["source_claim_proved"] is False
    assert result["proof_dependency_master_acceptance"] == "fail_closed"
    assert result["accepted_closed_obligation_ids"] == []
    assert result["source_identity_gate"] == "fail_closed"
    assert result["complete_trust_provenance_gate"] == "fail_closed"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_distinct_runner_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["hermeticity"]["fresh_clean_checkout"] is False
    assert receipt["hermeticity"]["empty_user_package_and_build_caches"] is False
    assert receipt["hermeticity"]["cold_dependency_rebuild"] is False
    assert receipt["independent_validation"]["distinct_verifier_identity"] is False
    assert receipt["independent_validation"]["second_signed_attestation"] is False
    assert receipt["independent_validation"]["decision"] == "fail_closed"
    assert receipt["first_failed_gate"] == "dependency.S56-M-1248-PROOF.master_acceptance"
    assert receipt["first_failed_theorem_gate"] == "S56-5.1-EXACT-TARGET-IDENTITY-OR-TRANSPORT"
    assert receipt["remaining_root_cut_set"] == [
        "dependency.S56-M-1248-PROOF.master_acceptance",
        "S56-5.1-EXACT-TARGET-IDENTITY-OR-TRANSPORT",
    ]
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(expected_stdout).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)
    assert receipt["changed_paths"] == CHANGED_PATHS
    assert receipt["known_failures"] and receipt["invalidation_inputs"]

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
        actual = {line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"}
        assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))

    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
