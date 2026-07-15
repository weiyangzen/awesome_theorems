#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1060-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1060"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1060-VALIDATION"
THEOREM = "THM-M-1060"
BASE_REVISION = "5cca979173a36d739670a3b5ecad23d89dc96292"
BASE_TREE = "97ccf7381b147bf0f25425a5a7678e51265c6eb3"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
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
EXPRESSION_SHA256 = "a5d3c4e6d9c19f45a79240a26c72c098a43adf164171b3167ee8bee67c1ab7f8"
DENOMINATOR_SHA256 = "32d2df11f1dd7faa40b53ee0ae86fc93d52317f80c4d3e9c1f8bcbe00b2a3f74"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H2", "M": "M4", "R": "R4"}
PARTIAL_ID = "M1060-N-WIENER"
OPEN_ROOT_CUT = [
    "M1060-L-GAUSSIAN",
    "M1060-L-MODULUS",
    "M1060-L-EXP-EQUIV",
    "M1060-L-RATE-ID",
    "M1060-L-RATE-LSC",
    "M1060-L-SUBLEVEL-BOUND",
]
EXPECTED_INPUTS = {
    "Statement.lean": "d2bfdc20fcb2cd7c3de27588917dad689056d73e05880814590ab1e3c604581a",
    "ObligationTree.lean": "36b33f8fc27041bda1f08bfdbea6a776848b974d1cf8f6825bb07bc7da3bf985",
    "AnchorAudit.lean": "073381c52bca1c31a618aaaf50e23b57f26003333bea987ace5c098a43b7f7fd",
    "Proof.lean": "9d5626f018862f239c79cdc49b2917abc23565d81fb8c8b8dc7aee6cbedf2069",
    "Validation.lean": "f80cc0d2c02d03d09f987990aa2253ac04e053105149c916736deef05f473036",
    "instance.json": "10525f4db03d4f453d9a0fc2b885f588f8b7707572b5135f987964f6efba8600",
    "obligation-registry.json": "cb01f4a60e1dc76401a13d41c7fc14a38e391e6d15325827dff178788f2add05",
    "typed-graphs.json": "f707b692bd77c98f1aa435c51165a83f539fdb1bb96a2d765f47746c95814cb9",
    "proof-receipt.json": "28bd48441b97aa7f472f41d53ec0c2f3ab345f1d879c800e8882fa21f491ca38",
    "proof-blocker-2026-07-15-head-48fb6596.json": (
        "a2b6c24a9433e521a8138bcc62e9a82515bc07d4c80202964f4d98763feffbc1"
    ),
    "check_obligation_tree.py": "10fe4302b23c37de54207396428ce18115c639b961b6c96ab744bb082596c5f8",
    "check_proof.sh": "356f7b432ae01d6b35b130543ce83d826772fce007ca705d0df8b105ae804531",
}
SOURCE_BOUNDARIES = {
    "Mathlib/Probability/Distributions/Gaussian/Real.lean": {
        "blob": "f5795fbfb92475879b67b0ee8577687575a82258",
        "source_sha256": "f5321db08f0156c5a12e15986d2ced9108183c907e3082d2566da8ef8da931a8",
        "olean_sha256": "b5894530bc315c897142ff650c774ed5ee3180b1df45690021fdd830e6e82ea4",
        "olean_bytes": 156560,
    },
    "Mathlib/Probability/Distributions/Gaussian/IsGaussianProcess/Basic.lean": {
        "blob": "5f40ebb2479839da872d565bfe932dfae2074a9d",
        "source_sha256": "b324daeb7f5868696e257f603b1eed66e72228890bdc32c251f838f7c08421b3",
        "olean_sha256": "1b6d9f0530fc05deed850214607c75e822dc19bc0f1929eb75961dd9511180ed",
        "olean_bytes": 78984,
    },
    "Mathlib/Probability/Distributions/Gaussian/Basic.lean": {
        "blob": "ccbe20ff5afb4d6695d3359f617aa04020de3461",
        "source_sha256": "5d2d373c3a4471077f8a4ea2e32ec3c2cfce0efd5f97899c20a61dadb10ea38a",
        "olean_sha256": "1dfbe5e0c10a53c6e14d5a536a172360fde9cfe29e5f9fec7978fcd5a0b6b249",
        "olean_bytes": 171504,
    },
}
PROOF_DECLARATIONS = (
    "Stage1Instances.THM_M_1060.isProbabilityMeasure_of_isWienerMeasure",
    "Stage1Instances.THM_M_1060.measurableEvaluationLinear",
    "Stage1Instances.THM_M_1060.continuousScale",
    "Stage1Instances.THM_M_1060.zeroTimeVarianceAndLaw",
    "Stage1Instances.THM_M_1060.zeroTimeLaw",
    "Stage1Instances.THM_M_1060.oneTimeVarianceAndLaw",
    "Stage1Instances.THM_M_1060.oneTimeLaw",
    "Stage1Instances.THM_M_1060.isGaussianProcess_of_isWienerMeasure",
)
COMPOSITION_DECLARATIONS = (
    "Stage1Instances.THM_M_1060.ObligationTree.smallNoiseLDP_of_bounds_and_good",
    "Stage1Instances.THM_M_1060.ObligationTree.schilderTarget_of_components",
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
    "PASS network-isolated trust-zero replay: statement, obligation interfaces, anchors, eight partial bodies, and audit module elaborated",
    "PASS trust observation: ten audited declarations are sorry-free and use only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, tool identities, clean mathlib pin, license, and three source/olean boundaries agree",
    "OPEN exact Schilder root: zero frozen obligations are closed and all 19 required terminal proof-body IDs are null",
    "FAIL CLOSED complete trust/provenance: the accepted foundation policy, serialized transitive provenance, and full TCB/SBOM are absent",
    "FAIL CLOSED release gates: shared warm cache is not cold hermetic evidence and this worker is not a distinct independent verifier",
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
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


BASE_ENV = {
    "HOME": os.environ["HOME"],
    "PATH": f"{os.environ['HOME']}/.elan/bin:/usr/bin:/bin",
    "ELAN_TOOLCHAIN": TOOLCHAIN,
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


def source_without_comments_and_strings(source: str) -> str:
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


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", re.DOTALL
    )
    matches = pattern.findall(output)
    assert len(matches) == 1, f"missing or duplicate axiom report for {declaration}"
    return {part.strip() for part in matches[0].split(",") if part.strip()}


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
    with tempfile.TemporaryDirectory(prefix="stage1-m1060-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in (
            "Statement.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean",
            "Validation.lean",
        ):
            shutil.copy2(HERE / name, tmp / name)
        (tmp / "home").mkdir()
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net", "--die-with-parent",
            "--clearenv", "--setenv", "HOME", str(tmp / "home"), "--setenv", "TMPDIR",
            str(tmp), "--setenv", "LANG", "C.UTF-8", "--setenv", "LC_ALL", "C.UTF-8",
            "--setenv", "TZ", "UTC", "--setenv", "LEAN_NUM_THREADS", "1", "--chdir",
            str(tmp),
        ]

        def lean_run(name: str, module_path: str, emit_olean: bool) -> str:
            argv = base + ["--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0"]
            if emit_olean:
                argv += ["-o", name.replace(".lean", ".olean")]
            argv.append(name)
            return run(argv)

        statement = lean_run("Statement.lean", lean_path, True)
        proof = lean_run("Proof.lean", f"{tmp}:{lean_path}", True)
        tree = lean_run("ObligationTree.lean", lean_path, True)
        return {
            "statement": statement,
            "proof": proof,
            "obligation_tree": tree,
            "anchor_audit": lean_run("AnchorAudit.lean", lean_path, False),
            "validation": lean_run("Validation.lean", f"{tmp}:{lean_path}", False),
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker-2026-07-15-head-48fb6596.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 503 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 503,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1060-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1060-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    assert instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1060-ROOT"
    denominator = hashlib.sha256(
        json.dumps(registry["frozen_denominators"], sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert denominator == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    required_machine = registry["frozen_denominators"]["required_machine"]
    assert len(registry["obligations"]) == 21 and len(required_machine) == 19
    assert all(
        row["terminal_proof_body_id"] is None
        for row in registry["obligations"]
        if row["obligation_id"] in required_machine
    )
    root = next(row for row in registry["obligations"] if row["obligation_id"] == "M1060-ROOT")
    assert root["statement_fingerprint"] == f"lean-expression-sha256:{EXPRESSION_SHA256}"
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M4" and closure["audit_complete"] is False
    assert closure["theorem_complete"] is False and closure["remaining_root_cut_set"] == OPEN_ROOT_CUT
    graph_root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1060-ROOT")
    assert {
        "H": graph_root["human_debt"],
        "M": graph_root["machine_debt"],
        "R": graph_root["readability_debt"],
    } == ROOT_VECTOR

    assert proof_receipt["item_id"] == "S56-M-1060-PROOF" and proof_receipt["accepted"] is False
    assert proof_receipt["partial_progress_toward_obligation_ids"] == [PARTIAL_ID]
    assert proof_receipt["supported_obligation_ids"] == []
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["proof_phase_complete"] is False
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_blocker["proof_phase_complete"] is proof_blocker["root_closed"] is False
    assert proof_blocker["audit_complete"] is proof_blocker["theorem_complete"] is False
    assert proof_blocker["frozen_implementation_cut_set"] == OPEN_ROOT_CUT

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac|oracle)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    for name in (
        "Statement.lean", "ObligationTree.lean", "AnchorAudit.lean", "Proof.lean",
        "Validation.lean",
    ):
        source = source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, name
    proof_source = source_without_comments_and_strings((HERE / "Proof.lean").read_text())
    assert "SchilderTarget" not in proof_source

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

    toolchain_dir = TOOLCHAIN.replace("/", "--").replace(":", "---")
    lean = Path(os.environ["HOME"]) / ".elan" / "toolchains" / toolchain_dir / "bin" / "lean"
    lake = lean.with_name("lake")
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    assert sha256(Path("/usr/bin/git")) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=BASE_ENV)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], env=BASE_ENV)

    outputs = isolated_replay(lean, bwrap, pinned_lean_path(lean))
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and all("error:" not in output for output in outputs.values())
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    for declaration in (*PROOF_DECLARATIONS, *COMPOSITION_DECLARATIONS):
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 10
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
            name: hashlib.sha256(output.encode()).hexdigest() for name, output in outputs.items()
        },
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "validation_closure": {
            "roots": 10,
            "declarations": int(closure_match.group(2)),
            "modules": int(closure_match.group(3)),
            "bodyless_nonaxioms": [],
            "unsafe": [],
        },
    }
    if args.probe:
        print(json.dumps(observation, sort_keys=True))
        return

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    blocker = load(HERE / "validation-blocker.json")
    packet_path = args.worker_packet or (ROOT / ".stage1-worker-selftest.json")
    packet = load(packet_path.resolve())
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == blocker["item_id"] == packet["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-1060-PROOF"]
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
    assert receipt["base_revision"] == blocker["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == blocker["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked" and receipt["release_grade"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["covered_obligation_ids"] == required_machine
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["validation_complete"] is False
    assert receipt["result"]["hermetic_cold_offline_replay"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert blocker["outcome"] == "validation_packet_self_tested_gates_blocked"
    assert blocker["validation_phase_complete"] is False
    assert blocker["root_closed"] is blocker["audit_complete"] is blocker["theorem_complete"] is False
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary", "base_revision",
        "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert packet["changed_paths"] == receipt["changed_paths"] == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual = [
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
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
