#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0338-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0338"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0338-VALIDATION"
THEOREM = "THM-M-0338"
BASE_REVISION = "38502dd8cfdb1c7b89d62d802952ab596838ec7e"
BASE_TREE = "334fd05726c0b982153d6aec154745629a2c9bc1"
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
    "c0c479c898a7b418bd4d82ad05d7514edfcc885cfd9a5487fb1a4ac5ffc37868"
)
DENOMINATOR_SHA256 = "e53a0b15267ae38e68bb1b727edd51b52d0b60c8f244fd912fc2153c2a0cca6e"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
AUTHORITATIVE_OPEN_CUT = [
    "M0338-E-EXTENSION",
    "M0338-KS-PAVING",
    "M0338-W-MSS",
    "M0338-X-SOURCE",
    "M0338-X-FOUNDATION",
]
PROVISIONAL_REMAINING_CUT = [
    "M0338-KS-PAVING",
    "M0338-W-MSS",
    "M0338-X-SOURCE",
    "M0338-X-FOUNDATION",
]
FIRST_FAILED_GATE = (
    "dependency.S56-M-0338-PROOF.master_acceptance_and_M0338-U-UNIQUE.root_closure"
)
EXPECTED_INPUTS = {
    "Statement.lean": "6619fde250e55f083e861d4de954745713a3448e12a10d0e140f1d7a4064ad12",
    "ObligationTree.lean": "fdce8a20bf3dd3c352231fd96191dfb586be762dc16d70ef65275c1d161feecc",
    "Proof.lean": "e01e94a10cd5ce14e8ed6a9db278613dc36db450bd6321b6b7b024d5b745ce63",
    "instance.json": "2bd5e0507fae9dc0e7d4ae0414e48760ded5c56022707055acf53e1c5374b07b",
    "task-dag.json": "2f900821c1603775bf5e97d747c1410ef0b7b8a1f81b4642e66b3885183eb522",
    "statement.json": "4958303246f52b32343c85eb0e84632baf3431f8a33c49e1aa683b247105dc7a",
    "anchor-audit.json": "f5f569f97f8191ec2bb496d0ad6d16c1fd7d926d11529c913685a15a01e95e69",
    "obligation-registry.json": "cf68ffc3d5de606e9160b88caea41d416987fb4819b29d0675297e0c3f770c0e",
    "typed-graphs.json": "5377a8337b27397d9429db358c731574236f17cfaa8fba733e2cdc25193df237",
    "validation-specs.json": "51e7d818bf31c945b476b5368544df5640b80951eeb94822b5d161eb9ee9e44d",
    "proof-receipt.json": "9d77bf742ddeb4d71b802bead98c64607d7d08e3e897774a2b28c4c3980781c7",
    "proof-blocker.json": "2b029cf5a081d4beb6c0766619b8e1fec90fe9b565bae04af46dedf266f56ca1",
    "source-statement-crosswalk.md": "a81f9c569f0ec8e63053b180bfb6cbeb404581402757d784344924ad5974a13a",
    "check_statement.py": "041fed1af21748bdb379497a537afc33c4ab841ecd773096666b7b4bdc2abe45",
    "check_anchor_audit.py": "6df59026e07139ae6b48c558214db4dcbb751ab7b8462d545ed9541128fb7e5d",
    "check_obligation_tree.py": "91947e8d9be1d6cbab113abd1e7b1c3e0d09fe277c7b54480dcd8a13d3ced37c",
    "check_proof.sh": "2e505d195731d34d4fc5bf70cf70cf42e403771d2f415dc655f92ae154c46013",
    "Validation.lean": "8055c5c3b52893f32d66b1103eb9f6070a1c310111fa91b85c0891c037e423ee",
}
SOURCE_BOUNDARIES = {
    "Mathlib/Analysis/Convex/Cone/Extension.lean": {
        "declaration": "riesz_extension",
        "blob": "be1bd948de9e7c9926e1f3745242e900dc55ac10",
        "source_sha256": "235ea43966395b2a9a8535482cb072f5c12f596b39b8db81b138326c9c70c1d5",
        "olean_sha256": "51d08245dc8d1fb33b2a4cc16cc1fd056d4bee1af9d858f5e2eb696f6d6a2909",
        "olean_bytes": 45720,
    },
    "Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Order.lean": {
        "declaration": "IsSelfAdjoint.neg_algebraMap_norm_le_self",
        "blob": "9a06d133e2161e71f4ba628f1e9df13c15039e73",
        "source_sha256": "5b59fbaac682534e489514e4a4fbdcae06e398f42340dedc95ae8ff1d8dd0a48",
        "olean_sha256": "26b91cdcf4640b310eed953839aa29782707330dccad68269919333cc66888a1",
        "olean_bytes": 269784,
    },
    "Mathlib/Algebra/Order/Module/PositiveLinearMap.lean": {
        "declaration": "PositiveLinearMap.mk₀",
        "blob": "c3a5a4faaeac5693925644d8bc8d93de2dbe27bd",
        "source_sha256": "506061174ca70fb944989ee4395b3eb3fcb67a1204a7b25b57bfb10841fd5105",
        "olean_sha256": "6c737a9e291fa59eea2ad90159b8aba9ff344b959e83d37e09d0e9bf55d158f8",
        "olean_bytes": 327800,
    },
}
CHECKED_DECLARATIONS = (
    "Stage1.THM_M_0338.root_of_components",
    "Stage1.THM_M_0338.extension_exists_for_state",
    "Stage1.THM_M_0338.extension_exists_for_kadison_singer_input",
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
    "PASS narrow kernel replay: exact statement, conditional composition, and two extension-existence declarations elaborated at trust zero",
    "PASS trust observation: all three declarations report only propext, Classical.choice, and Quot.sound; closure has no unexpected bodyless or unsafe declaration",
    "PASS selected provenance: frozen hashes, three direct mathlib source/olean boundaries, toolchain pins, license, and clean pinned revision agree",
    "OPEN exact root: extension uniqueness, paving, Weaver/MSS, source, and foundation obligations remain open at M3",
    "FAIL CLOSED complete trust/provenance: accepted foundation policy, transitive artifact provenance, and full TCB/SBOM inventory are absent",
    "FAIL CLOSED release gates: shared warm cache is not cold hermetic evidence and this worker is not an independent verifier",
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
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != expected_exit:
        raise RuntimeError(
            f"command exit {result.returncode}, expected {expected_exit}: {argv!r}\n{result.stdout}"
        )
    return result.stdout


HOME = os.environ["HOME"]
BASE_ENV = {
    "HOME": HOME,
    "PATH": f"{HOME}/.elan/bin:/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


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
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def pinned_lean_path(lean: Path) -> str:
    roots = sorted(
        path.resolve()
        for path in (LEAN_ROOT / ".lake/packages").glob("*/.lake/build/lib/lean")
        if path.resolve().is_dir()
    )
    assert roots
    return ":".join([*(str(path) for path in roots), str(lean.parent.parent / "lib/lean")])


def isolated_replay(lean: Path, bwrap: Path, lean_path: str) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0338-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
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
        obligation = lean_run("ObligationTree.lean", f"{tmp}:{lean_path}", True)
        proof = lean_run("Proof.lean", f"{tmp}:{lean_path}", True)
        validation = lean_run("Validation.lean", f"{tmp}:{lean_path}", False)
        return {
            "statement": statement,
            "obligation_tree": obligation,
            "proof": proof,
            "validation": validation,
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", action="store_true")
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 831 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 831,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0338-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0338-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    formal = instance["canonical_formal_target"]
    assert formal["elaborated_expression_hash"] == f"sha256:{STATEMENT_EXPRESSION_SHA256}"
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "root_machine_classification": "M3",
        "theorem_complete": False,
        "open_cut_set": AUTHORITATIVE_OPEN_CUT,
    }
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0338-ROOT")
    assert {"H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]} == ROOT_VECTOR

    assert instance["accepted_proof_state"] == [] and instance["theorem_complete"] is False
    assert proof_receipt["item_id"] == "S56-M-0338-PROOF"
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["provisionally_closed_obligation_ids"] == ["M0338-E-EXTENSION"]
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["accepted"] is False
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["provisional_remaining_machine_cut"] == PROVISIONAL_REMAINING_CUT
    assert proof_blocker["remaining_machine_root_cut_set"] == PROVISIONAL_REMAINING_CUT
    assert proof_blocker["root_closed"] is proof_blocker["audit_complete"] is False
    assert proof_blocker["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    all_source = "\n".join(
        source_without_comments((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
    )
    assert prohibited.search(all_source) is None
    proof_source = (HERE / "Proof.lean").read_text(encoding="utf-8")
    assert "theorem extension_exists_for_state" in proof_source
    assert "theorem extension_exists_for_kadison_singer_input" in proof_source
    assert "theorem KadisonSingerStatement" not in proof_source
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    assert validation_source.count("assert_no_sorry Stage1.THM_M_0338.") == len(CHECKED_DECLARATIONS)
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

    outputs = isolated_replay(lean, bwrap, pinned_lean_path(lean))
    combined = "\n".join(outputs.values())
    assert "sorryAx" not in combined and all("error:" not in output for output in outputs.values())
    assert reported_axioms(outputs["obligation_tree"], CHECKED_DECLARATIONS[0]) == EXPECTED_AXIOMS
    for declaration in CHECKED_DECLARATIONS[1:]:
        assert reported_axioms(outputs["proof"], declaration) == EXPECTED_AXIOMS
    for declaration in CHECKED_DECLARATIONS:
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
    assert outputs["validation"].count("Declarations are sorry-free!") == len(CHECKED_DECLARATIONS)
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
    blocker = load(HERE / "validation-blocker.json")
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["spec_id"] == "S56-M-0338-VALIDATION-local-v1"
    assert spec["intent"] == "validate" and spec["status_boundary"]
    assert spec["item_id"] == receipt["item_id"] == blocker["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0338-PROOF"]
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
    assert set(recipe["covered_declarations"]) == {
        "Stage1.THM_M_0338.KadisonSingerStatement", *CHECKED_DECLARATIONS
    }

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == blocker["verdict"] == "blocked"
    assert receipt["base_revision"] == blocker["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == blocker["base_tree"] == BASE_TREE
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
    result = receipt["result"]
    assert result["lean_output_sha256"] == observation["lean_output_sha256"]
    assert result["observed_axioms"] == observation["observed_axioms"]
    assert result["validation_closure"] == observation["validation_closure"]
    assert result["validated_partial_progress_toward_obligation_ids"] == ["M0338-E-EXTENSION"]
    assert result["supported_obligation_ids"] == []
    assert result["accepted_closed_obligation_ids"] == []
    assert result["proof_dependency_master_acceptance"] == "fail_closed"
    assert result["root_closed"] is result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M3"
    assert result["authoritative_open_root_cut"] == AUTHORITATIVE_OPEN_CUT
    assert result["provisional_remaining_root_cut"] == PROVISIONAL_REMAINING_CUT
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
    assert receipt["remaining_root_cut_set"] == PROVISIONAL_REMAINING_CUT
    assert receipt["first_failed_gate"] == blocker["first_failed_gate"] == FIRST_FAILED_GATE
    assert blocker["theorem_complete"] is blocker["audit_complete"] is False
    assert blocker["root_closed"] is False and blocker["state"] == "[_]"
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
