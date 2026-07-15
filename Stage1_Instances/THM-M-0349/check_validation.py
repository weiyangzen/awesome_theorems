#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0349-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0349"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0349-VALIDATION"
THEOREM = "THM-M-0349"
BASE_REVISION = "d5ab961cb3cd92c7febcf21fb9ab746fde231c24"
BASE_TREE = "5f3d5abbfee8a0f11198a295ecf024aca301867f"
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
    "5f80bebbbf59938add2cb517d6b6219f7a7a22ad8f09586d01e508db2e2ac908"
)
DENOMINATOR_SHA256 = "559befd6c5ac888249539d74acc96e0a274afa52e3b2e0683c05dc010cd3185d"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
ROOT_VECTOR = {"H": "H3", "M": "M4", "R": "R4"}
FROZEN_ROOT_CUT = ["M0349-P-EXISTENCE", "M0349-P-BOUND"]
PARTIAL_IDS = ["M0349-C-POLYNOMIAL", "M0349-L-L2"]
EXPANDED_OPEN_DEBT = [
    "M0349-L-WEAK11",
    "M0349-L-INTERPOLATE",
    "M0349-C-EXTEND",
    "M0349-L-FOURIER-ID",
    "M0349-P-EXISTENCE",
    "M0349-P-BOUND",
]
EXPECTED_INPUTS = {
    "Statement.lean": "c548991ce6ec39da14646f359edea6ad3b53e31dc71e27c4b90345b034afcf62",
    "ObligationTree.lean": "2c08dcdbe1871a1c3c3613aacb31b9fea6a05e59b6c0eb03da9781875be28ff7",
    "Proof.lean": "a7bbea29d7ebeaadcee60e352d1294617f3a8f46e4b4adc3142041ef15517942",
    "instance.json": "2593850ad0812654e4afbf28beb9252814d54c9fd355ce066e9a34ef09ed73ff",
    "task-dag.json": "fd94e3999832a9c9c3029af559c11326203c1da043501949987f12b907d9c42f",
    "anchor-audit.json": "f08d1cf12c010c556b2dd03c5d689493b403edfb7b81ccfc413bdac4fa27d820",
    "obligation-registry.json": "ae975d9ff9ea0432de87cf6b5794463ba81ac4057eaba42dbcf456506328bfe7",
    "typed-graphs.json": "1cd55ee81552085c965ffa43cea205b1e7f0e21c38c296eca043bf6b906cbad8",
    "proof-receipt.json": "6bd1042271f4a19fa3e2f0717b88f1c61ca5305d490ed8095d5e0ccd95c66cb1",
    "proof-blocker.json": "1a2d8ff322dc7eb1f709edae9699ea03bf61803ea4af2acca7f5147662e5391d",
    "source-statement-crosswalk.md": "2e4c2d79dd7c0ddfa9337df26368545a1fb267a3a51b64223086de78e8754d52",
    "check_obligation_tree.py": "1c5a4037eb21f656e0a0762f99f950ca93aa64bb4890951780813fe7005c077d",
    "check_proof.sh": "74aaf2853ee083bdd8d5feae1604104f6110dd6221ab288cda8528df3ded1df9",
    "Validation.lean": "802f05d6665c8d6d044520da844382169aa610368e568b991f55040226c18808",
}
SOURCE_BOUNDARY = {
    "file": "Mathlib/Analysis/Fourier/AddCircle.lean",
    "git_blob": "adeceb59e11905f424d720ba78cc87cdfdca7607",
    "source_sha256": "32363b7144bee4cdc3f96e41237eb6944c8dd6ac92449340a0c27462959e7c81",
    "olean": ".lake/build/lib/lean/Mathlib/Analysis/Fourier/AddCircle.olean",
    "olean_sha256": "8ce42ea0aeca73155104faa89418b61a06201d8af544391db7c0b76816f761f2",
    "olean_bytes": 307424,
}
AXIOM_DECLARATIONS = (
    "Stage1Instances.THM_M_0349.conjugate_l2_bound",
    "Stage1Instances.THM_M_0349.root_of_conjugate_packages",
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
    "PASS narrow kernel replay: exact statement, partial L2 bodies, and conditional root composition elaborated at trust zero with network denied",
    "PASS trust observation: both terminal declarations report only propext, Classical.choice, and Quot.sound; no sorry, unexpected bodyless declaration, or unsafe dependency was observed",
    "PASS selected provenance: frozen inputs, proof receipt, clean pinned mathlib source/tree/license, AddCircle source blob, and compiled import agree",
    "OPEN exact root: the L2 node lacks an exact frozen interface and weak-(1,1), interpolation, extension, Fourier identity, and both all-p packages remain open",
    "FAIL CLOSED complete trust/provenance: no accepted foundation profile, full transitive artifact provenance, or complete TCB/SBOM inventory exists",
    "FAIL CLOSED release gates: shared warm cache is not cold hermetic evidence and this worker is not an independent verifier",
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


HOME = os.environ["HOME"]
BASE_ENV = {
    "HOME": HOME,
    "PATH": f"{HOME}/.elan/bin:/usr/bin:/bin",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "TZ": "UTC",
    "LEAN_NUM_THREADS": "1",
}


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


def source_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    block_depth = 0
    in_string = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if block_depth:
            if pair == "/-":
                block_depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                block_depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif in_string:
            output.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
        elif pair == "/-":
            block_depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            newline = source.find("\n", index)
            if newline < 0:
                output.extend(" " * (len(source) - index))
                index = len(source)
            else:
                output.extend(" " * (newline - index))
                index = newline
        elif char == '"':
            in_string = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    assert block_depth == 0 and not in_string
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


def pinned_lean_path(lean: Path) -> str:
    roots = sorted(
        path.resolve()
        for path in (LEAN_ROOT / ".lake/packages").glob("*/.lake/build/lib/lean")
        if path.resolve().is_dir()
    )
    assert roots
    return ":".join([*(str(path) for path in roots), str(lean.parent.parent / "lib/lean")])


def isolated_replay(lean: Path, bwrap: Path, lean_path: str) -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="stage1-m0349-validation-", dir="/tmp") as tmp_name:
        tmp = Path(tmp_name).resolve()
        for name in ("Statement.lean", "Proof.lean", "ObligationTree.lean", "Validation.lean"):
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
            return run(argv, env=BASE_ENV)

        statement = lean_run("Statement.lean", lean_path, True)
        proof = lean_run("Proof.lean", f"{tmp}:{lean_path}", True)
        obligation = lean_run("ObligationTree.lean", f"{tmp}:{lean_path}", True)
        validation = lean_run("Validation.lean", f"{tmp}:{lean_path}", False)
        return {
            "statement": statement,
            "proof": proof,
            "obligation_tree": obligation,
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
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    local_tasks = load(HERE / "task-dag.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 842 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 842,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0349-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0349-PROOF")
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
        "root_closed": False,
        "theorem_complete": False,
        "minimal_open_root_cut": FROZEN_ROOT_CUT,
    }
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0349-ROOT")
    graph_root_vector = {
        "H": root["human_debt"],
        "M": root["machine_debt"],
        "R": root["readability_debt"],
    }
    assert graph_root_vector == {"H": "H3", "M": "M3", "R": "R4"}
    assert instance["root_vector"] == ROOT_VECTOR

    assert proof_receipt["item_id"] == "S56-M-0349-PROOF"
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["supported_obligation_ids"] == []
    assert proof_receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["accepted"] is False
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["remaining_root_cut_set"] == FROZEN_ROOT_CUT
    assert proof_blocker["remaining_root_cut_set"] == FROZEN_ROOT_CUT
    assert proof_blocker["root_closed"] is proof_blocker["audit_complete"] is False
    assert proof_blocker["theorem_complete"] is False
    local_proof_task = next(row for row in local_tasks["tasks"] if row["id"] == "S56-M-0349-PROOF")
    local_validation_task = next(row for row in local_tasks["tasks"] if row["id"] == ITEM)
    assert local_proof_task["state"] == local_validation_task["state"] == "open"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    all_source = "\n".join(
        source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        for name in ("Statement.lean", "Proof.lean", "ObligationTree.lean", "Validation.lean")
    )
    assert prohibited.search(all_source) is None
    proof_source = (HERE / "Proof.lean").read_text(encoding="utf-8")
    assert "theorem conjugate_l2_bound" in proof_source
    assert "theorem ConjugateFunctionTheoremTarget" not in proof_source
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    assert validation_source.count("assert_no_sorry Stage1Instances.THM_M_0349.") == 13
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
    source = mathlib / SOURCE_BOUNDARY["file"]
    olean = mathlib / SOURCE_BOUNDARY["olean"]
    assert git("rev-parse", f"HEAD:{SOURCE_BOUNDARY['file']}", cwd=mathlib) == SOURCE_BOUNDARY["git_blob"]
    assert sha256(source) == SOURCE_BOUNDARY["source_sha256"]
    assert sha256(olean) == SOURCE_BOUNDARY["olean_sha256"]
    assert olean.stat().st_size == SOURCE_BOUNDARY["olean_bytes"]

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
    expression_match = re.search(
        r" : Prop :=\n(?P<expression>.*)\Z", outputs["statement"], flags=re.DOTALL
    )
    assert expression_match is not None
    observed_expression_sha256 = hashlib.sha256(
        expression_match.group("expression").strip().encode()
    ).hexdigest()
    assert observed_expression_sha256 == STATEMENT_EXPRESSION_SHA256
    for declaration in AXIOM_DECLARATIONS:
        assert reported_axioms(outputs["validation"], declaration) == EXPECTED_AXIOMS
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
        "statement_expression_sha256": observed_expression_sha256,
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
    assert spec["spec_id"] == "S56-M-0349-VALIDATION-local-v1"
    assert spec["intent"] == "validate" and spec["status_boundary"]
    assert spec["item_id"] == receipt["item_id"] == blocker["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert spec["depends_on"] == receipt["depends_on"] == ["S56-M-0349-PROOF"]
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
    assert receipt["inputs"]["lean-toolchain"] == TOOLCHAIN_SHA256
    assert receipt["inputs"]["lake-manifest.json"] == MANIFEST_SHA256
    repository_state = receipt["repository_state"]
    assert repository_state["release_clean"] is False
    tracked_patch = git_bytes("diff", "--binary", BASE_REVISION, "--", f"Stage1_Instances/{THEOREM}")
    assert repository_state["base_commit_clean_for_owned_path"] is (tracked_patch == b"")
    assert repository_state["tracked_patch_sha256"] == hashlib.sha256(tracked_patch).hexdigest()
    assert repository_state["tracked_patch_bytes"] == len(tracked_patch)
    input_scope = [
        f"Stage1_Instances/{THEOREM}/Validation.lean",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
        f"Stage1_Instances/{THEOREM}/validation-blocker.json",
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
    assert result["observed_axioms"] == observation["observed_axioms"]
    assert result["statement_expression_sha256"] == observation["statement_expression_sha256"]
    assert result["validation_closure"] == observation["validation_closure"]
    assert result["validated_partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert result["supported_obligation_ids"] == []
    assert result["provisionally_closed_obligation_ids"] == []
    assert result["accepted_closed_obligation_ids"] == []
    assert result["proof_dependency_master_acceptance"] == "fail_closed"
    assert result["root_closed"] is result["root_kernel_closed"] is False
    assert result["root_machine_debt"] == "M4"
    assert result["frozen_graph_minimal_open_root_cut"] == FROZEN_ROOT_CUT
    assert result["expanded_open_root_debt"] == EXPANDED_OPEN_DEBT
    assert result["complete_trust_provenance_gate"] == "fail_closed"
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["independent_distinct_runner_gate"] == "fail_closed"
    assert result["source_h0_gate"] == "fail_closed"
    assert result["readability_r0_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["direct_provenance"]["proof_dependency_master_accepted"] is False
    assert receipt["direct_provenance"]["local_task_dag_state"] == {
        "proof": "open", "validation": "open", "classification": "stale_pre_proof_projection"
    }
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
        "dependency.S56-M-0349-PROOF.master_acceptance_and_M0349-L-L2.exact_node_mapping"
    )
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout
    ).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)
    assert receipt["changed_paths"] == CHANGED_PATHS

    assert blocker["outcome"] == "validation_self_tested_root_and_release_blocked"
    assert blocker["supported_obligation_ids"] == []
    assert blocker["accepted_closed_obligation_ids"] == []
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False
    assert blocker["first_failed_gate"] == receipt["first_failed_gate"]
    assert blocker["remaining_root_cut_set"] == EXPANDED_OPEN_DEBT

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
