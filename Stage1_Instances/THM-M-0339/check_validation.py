#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0339-VALIDATION."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0339"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0339-VALIDATION"
THEOREM = "THM-M-0339"
BASE_REVISION = "e4c6d32d1eb44bab8a06b606e6f2274e442d7f45"
BASE_TREE = "c987baeda5c9641649fa79fa00eb4ec435472142"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
STATEMENT_EXPRESSION_SHA256 = (
    "65f33abcebfa3d3c007b923852d0f89d71c3250f72b95b8645546178813503dc"
)
DENOMINATOR_SHA256 = "29ab54f13bdf31d2d84b7eb0ac2a07fe21a19ac12587dae5e5e58d97374c4b62"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
PARTIAL_IDS = [
    "M0339-S-BOUNDARY",
    "M0339-B-RONE",
    "M0339-B-RMANY",
    "M0339-T-COR15",
    "M0339-T-ASSEMBLE",
]
FROZEN_MINIMAL_CUT = ["M0339-L-THEOREM14"]
EXPANDED_OPEN_DEBT = [
    "M0339-C-RANDOM",
    "M0339-C-MCP",
    "M0339-L-REALROOTED",
    "M0339-L-INTERLACING",
    "M0339-L-BARRIER",
    "M0339-L-THEOREM14",
]
EXPECTED_INPUTS = {
    "Statement.lean": "b906c95d7778f7d908a4f2e1373f2256786fcb62094be72b79920a558f3679fd",
    "Proof.lean": "6656a0d0b433069e149a583d053d98cfcdd42bcddfb374ad68428f513d379ccd",
    "ObligationTree.lean": "9722eb3711877516e30d040d30fcb6c998d28244d72cbb4342034e25c9881323",
    "instance.json": "073704317907a3e923ea925577d250cf6971bd55d388438678184a4d70f04675",
    "anchor-audit.json": "ee53efba48e877cbe76508602952ddd03b6ba18fd7c5dd003513f2870d37e8a9",
    "obligation-registry.json": "e61f9b1e4146bde5fbe0c3beec92663cac3645d26a12c616af7b7f79a2b383c0",
    "typed-graphs.json": "6700d71b249d3405dbe251589a6f662c6ba3454dbba7dbec34d7b43a4d728046",
    "validation-specs.json": "4bdf40da25a428a8b1551d8a88833f34ef0e9f03e6d2827112886fc608332ce2",
    "proof-receipt.json": "551a1f9dc6f454d142ef3a15e3a6cd7c33b3f39b7b68b89ce271a35d1f97711a",
    "proof-blocker.json": "a68f7411396d8cfe7f5b8e06522ed5230725170c5be3bd808a67fdea84f6b1a7",
    "source-statement-crosswalk.md": "6b16fd0285d90a04362272be8221381fbfcc36b8ee82daacbab704f76087c6c3",
    "check_obligation_tree.py": "0f1ad2f39c600012cbd76000dea01606be48368123d4132f277de950180f2049",
    "check_proof.sh": "457c00509d574cb51ff0d7994ec25388b36c8d48dd63585ab216be969beb661c",
    "Validation.lean": "0724a0464dd045471f539a33887292448a28cf2fc454ffc04606179406dbffe3",
}
SOURCE_BOUNDARIES = {
    "Mathlib/Analysis/InnerProductSpace/LinearMap.lean": {
        "declaration": "InnerProductSpace.norm_rankOne",
        "blob": "82d6d42b5f0fced401f3a4e3c3c0f951d7454d17",
        "source_sha256": "e1e7305fbf6ac17146475fffd056631c78f128d85314af4fdde87345a1d5747b",
        "olean_sha256": "f6c856a22a4bf2d2250b1cf67c04faa20fbccc1ab2a565924ccf6efb8299ff97",
        "olean_bytes": 911152,
    },
    "Mathlib/Analysis/Normed/Operator/Basic.lean": {
        "declaration": "ContinuousLinearMap.norm_id_le",
        "blob": "45fe5b39d6fd4d4f26de9439e20c9fdb35a4d99d",
        "source_sha256": "58e0278f8a8af3304d31244b01a7157a149e8f8e803a9b352875035b93e75de4",
        "olean_sha256": "676484febbe64ba43d8f5ce02e7694ca23823b21a19bd711feb1a0ab3cb3602f",
        "olean_bytes": 659120,
    },
    "Mathlib/Data/Fin/SuccPred.lean": {
        "declaration": "Fin.castLE_injective",
        "blob": "c7560b79ad514ab7587c0b980a59b561e807ba52",
        "source_sha256": "8c49fd2444d2c6c49a9c7f710c69468452954f0efed81718de622b28085814a5",
        "olean_sha256": "617660810dbb63cccbce030eee9a0cc369afe76174868bc4931c4060ccfd4e52",
        "olean_bytes": 243632,
    },
}
PROOF_DECLARATIONS = (
    "Stage1.THM_M_0339.Proof.one_part",
    "Stage1.THM_M_0339.Proof.zero_dimension",
    "Stage1.THM_M_0339.Proof.empty_family",
    "Stage1.THM_M_0339.Proof.enough_colors",
    "Stage1.THM_M_0339.Proof.constant_color_large_bound",
    "Stage1.THM_M_0339.Proof.delta_ge_one",
    "Stage1.THM_M_0339.Proof.zero_delta",
    "Stage1.THM_M_0339.Proof.mssPartitionStatement_of_hardRegimeEngine",
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
    "PASS narrow kernel replay: exact statement, seven elementary bodies, and conditional root composition elaborated at trust zero",
    "PASS trust observation: all eight declarations report only propext, Classical.choice, and Quot.sound; closure has no unexpected bodyless or unsafe declaration",
    "PASS selected provenance: frozen hashes, three direct mathlib source/olean boundaries, toolchain pins, license, and clean pinned revision agree",
    "OPEN exact root: HardRegimeEngine and six substantive MSS packages remain unproved at M4; zero frozen obligations are closed",
    "FAIL CLOSED complete trust/provenance: accepted foundation policy, transitive artifact provenance, and full TCB/SBOM inventory are absent",
    "FAIL CLOSED release gates: Lake recipe is blocked, shared warm cache is not cold hermetic evidence, and this worker is not an independent verifier",
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
    timeout: int = 600, expected_exit: int = 0,
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
    if result.returncode != expected_exit:
        raise RuntimeError(
            f"command exit {result.returncode}, expected {expected_exit}: {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV).strip()


def git_bytes(*args: str, cwd: Path = ROOT) -> bytes:
    result = subprocess.run(
        ["/usr/bin/git", *args], cwd=cwd, env=BASE_ENV,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git command failed ({result.returncode}): {args!r}\n"
            f"{result.stderr.decode(errors='replace')}"
        )
    return result.stdout


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
    matches = re.findall(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        flags=re.DOTALL,
    )
    assert len(matches) == 1, f"missing or duplicate axiom report for {declaration}"
    return {part.strip() for part in matches[0].split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


HOME = os.environ["HOME"]
BASE_ENV = {
    "HOME": HOME,
    "PATH": f"{HOME}/.elan/bin:/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


def pinned_lean_path(lean: Path) -> str:
    roots = sorted(
        path.resolve()
        for path in (LEAN_ROOT / ".lake/packages").glob("*/.lake/build/lib/lean")
        if path.resolve().is_dir()
    )
    assert roots
    return ":".join([*(str(path) for path in roots), str(lean.parent.parent / "lib/lean")])


def isolated_replay(lean: Path, bwrap: Path, lean_path: str) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0339-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        (tmp / "home").mkdir()
        base = [
            str(bwrap), "--ro-bind", "/", "/", "--bind", str(tmp), str(tmp),
            "--dev", "/dev", "--proc", "/proc", "--unshare-net",
            "--die-with-parent", "--clearenv", "--setenv", "HOME", str(tmp / "home"),
            "--setenv", "TMPDIR", str(tmp), "--setenv", "LANG", "C.UTF-8",
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "TZ", "UTC",
            "--setenv", "LEAN_NUM_THREADS", "1", "--chdir", str(tmp),
        ]

        def lean_run(name: str, module_path: str, emit_olean: bool) -> str:
            argv = base + ["--setenv", "LEAN_PATH", module_path, str(lean), "--trust=0", "-t0"]
            if emit_olean:
                argv += ["-o", name.replace(".lean", ".olean")]
            argv.append(name)
            return run(argv)

        statement = lean_run("Statement.lean", lean_path, True)
        proof = lean_run("Proof.lean", f"{tmp}:{lean_path}", True)
        validation = lean_run("Validation.lean", f"{tmp}:{lean_path}", False)
        return {"statement": statement, "proof": proof, "validation": validation}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 832 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 832,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0339-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0339-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    formal = instance["canonical_formal_target"]
    assert formal["elaborated_expression_hash"] == f"sha256:{STATEMENT_EXPRESSION_SHA256}"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure == {
        "closed_obligations": [],
        "root_closed": False,
        "root_machine_debt": "M4",
        "remaining_root_cut_set": FROZEN_MINIMAL_CUT,
        "composition_certificates_checked": [
            "Stage1.THM_M_0339.ObligationTree.root_compose"
        ],
        "audit_complete": False,
        "theorem_complete": False,
    }
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0339-ROOT")
    assert {"H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]} == ROOT_VECTOR

    assert proof_receipt["item_id"] == "S56-M-0339-PROOF"
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof_receipt["supported_obligation_ids"] == []
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["accepted"] is False
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == EXPANDED_OPEN_DEBT
    assert proof_blocker["remaining_root_cut_set"] == EXPANDED_OPEN_DEBT
    assert proof_blocker["root_closed"] is proof_blocker["audit_complete"] is False
    assert proof_blocker["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "Proof.lean", "Validation.lean")
    )
    assert prohibited.search(all_source) is None
    proof_source = (HERE / "Proof.lean").read_text(encoding="utf-8")
    assert "def HardRegimeEngine : Prop" in proof_source
    assert "(engine : HardRegimeEngine) : Stage1.THM_M_0339.MSSPartitionStatement" in proof_source
    assert "theorem mssPartitionStatement :" not in proof_source
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    assert validation_source.count("assert_no_sorry Proof.") == len(PROOF_DECLARATIONS)
    assert "#print_validation_closure" in validation_source

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

    lean = Path(HOME) / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
    bwrap = Path("/usr/bin/bwrap")
    python = Path("/usr/bin/python3").resolve()
    git_executable = Path("/usr/bin/git")
    assert sha256(lean) == LEAN_SHA256
    assert sha256(bwrap) == BWRAP_SHA256 and sha256(python) == PYTHON_SHA256
    assert Path(sys.executable).resolve() == python
    assert sha256(git_executable) == GIT_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], env=BASE_ENV)

    flt_regular = LEAN_ROOT / ".lake/packages/flt-regular"
    assert flt_regular.is_dir()
    head_ref = (flt_regular / ".git/HEAD").read_text(encoding="utf-8").strip()
    flt_blocker = f"{head_ref}:lake-recipe-not-run"

    outputs = isolated_replay(lean, bwrap, pinned_lean_path(lean))
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and all("error:" not in output for output in outputs.values())
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == 8
    closure_match = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", outputs["validation"]
    )
    assert closure_match is not None
    assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unexpected_bodyless=[]" in outputs["validation"]
    assert "VALIDATION_CLOSURE unsafe=[]" in outputs["validation"]
    observation = {
        "lean_output_sha256": {
            name: hashlib.sha256(output.encode()).hexdigest()
            for name, output in outputs.items()
        },
        "lake_blocker_sha256": hashlib.sha256(flt_blocker.encode()).hexdigest(),
        "observed_axioms": sorted(EXPECTED_AXIOMS),
        "validation_closure": {
            "declarations": int(closure_match.group(1)),
            "modules": int(closure_match.group(2)),
            "unexpected_bodyless": [],
            "unsafe_declarations": [],
        },
    }
    if args.probe:
        print(json.dumps(observation, sort_keys=True))
        return

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["spec_id"] == "S56-M-0339-VALIDATION-local-v1"
    assert spec["intent"] == "validate" and spec["status_boundary"]
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0339-PROOF"]
    assert len(spec["recipes"]) == 1
    recipe = spec["recipes"][0]
    assert recipe == receipt["recipe"]
    assert recipe["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py",
        "--worker-packet", ".stage1-worker-selftest.json",
    ]
    assert recipe["cwd"] == "." and recipe["timeout_seconds"] == 600
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert recipe["covered_obligation_ids"] == []

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["lifecycle_before"] == receipt["lifecycle_after"] == "planned"
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == ROOT_VECTOR
    assert receipt["accepted_receipt_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())
    repository_state = receipt["repository_state"]
    assert repository_state["release_clean"] is False
    tracked_patch = git_bytes("diff", "--binary", BASE_REVISION, "--", f"Stage1_Instances/{THEOREM}")
    assert repository_state["base_commit_clean_for_owned_path"] is (tracked_patch == b"")
    assert repository_state["tracked_patch_sha256"] == hashlib.sha256(tracked_patch).hexdigest()
    assert repository_state["tracked_patch_bytes"] == len(tracked_patch)
    input_scope = [
        f"Stage1_Instances/{THEOREM}/Validation.lean",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
        f"Stage1_Instances/{THEOREM}/validation-phase.md",
        f"Stage1_Instances/{THEOREM}/validation-spec.json",
    ]
    payload = [{"path": path, "sha256": sha256(ROOT / path)} for path in input_scope]
    assert repository_state["untracked_input_sha256"] == hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert repository_state["untracked_input_scope"] == input_scope
    assert repository_state["preexisting_untracked_lake_symlink_target_sha256"] == hashlib.sha256(
        os.readlink(LEAN_ROOT / ".lake").encode()
    ).hexdigest()
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    result = receipt["result"]
    assert result["lean_output_sha256"] == observation["lean_output_sha256"]
    assert result["lake_blocker_sha256"] == observation["lake_blocker_sha256"]
    assert result["observed_axioms"] == observation["observed_axioms"]
    assert result["validation_closure"] == observation["validation_closure"]
    assert result["validated_partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert result["supported_obligation_ids"] == []
    assert result["provisionally_closed_obligation_ids"] == []
    assert result["accepted_closed_obligation_ids"] == []
    assert result["proof_dependency_master_acceptance"] == "fail_closed"
    assert result["root_closed"] is result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M4"
    assert result["frozen_graph_minimal_open_root_cut"] == FROZEN_MINIMAL_CUT
    assert result["expanded_open_root_debt"] == EXPANDED_OPEN_DEBT
    assert result["complete_trust_provenance_gate"] == "fail_closed"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_distinct_runner_gate"] == "fail_closed"
    assert result["source_h0_gate"] == "fail_closed"
    assert result["readability_r0_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["direct_provenance"]["proof_dependency_master_accepted"] is False
    assert receipt["trust"]["accepted_foundation_profile"] is False
    assert receipt["trust"]["complete_transitive_trust_closure"] is False
    assert receipt["hermeticity"]["fresh_clean_checkout"] is False
    assert receipt["hermeticity"]["empty_user_package_and_build_caches"] is False
    assert receipt["hermeticity"]["decision"].startswith("fail_closed")
    assert receipt["independent_validation"]["distinct_verifier_identity"] is False
    assert receipt["independent_validation"]["independently_provisioned_clean_runner"] is False
    assert receipt["independent_validation"]["independently_implemented_minimal_release_verifier"] is False
    assert receipt["independent_validation"]["second_signed_attestation"] is False
    assert receipt["independent_validation"]["decision"] == "fail_closed"
    assert receipt["remaining_root_cut_set"] == EXPANDED_OPEN_DEBT
    assert receipt["first_failed_gate"] == (
        "dependency.S56-M-0339-PROOF.master_acceptance_and_M0339-L-THEOREM14.root_closure"
    )
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout
    ).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)
    assert receipt["changed_paths"] == CHANGED_PATHS

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
