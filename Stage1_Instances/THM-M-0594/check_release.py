#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0594-RELEASE."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0594"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0594-RELEASE"
THEOREM = "THM-M-0594"
BASE_REVISION = "f976b9b21418bfda4bc815ba2a7238e932666231"
BASE_TREE = "6fbe6e3a73d5005115818a8f902da2b70f4aab24"
VALIDATION_REVISION = "b366bdd9f72217b5465ccd19133760b911ed0b58"
VALIDATION_RECEIPT_SHA256 = (
    "945184a81e98d5169d59fbfd7592309b1a0db732613ddf5edcbc6e80b604b818"
)
EXPRESSION_SHA256 = (
    "32943593a17c04d3b6fab019d7cf0db88d5e59b59f3d73703e82514987e97ef6"
)
DENOMINATOR_SHA256 = (
    "0ad656eddf1e42c8f47912729ceddcab9e45d56fd8a68e24b7bc82d59d367443"
)
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R3"}
AUTHORITATIVE_OPEN_CUT = ["M0594-C-GLOBAL", "M0594-L-TOPOLOGICAL"]
PROVISIONAL_OPEN_CUT = ["M0594-C-GLOBAL"]
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": (
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
    ),
    "Docs/Stage1_Execution_DAG_rev-5.6.json": (
        "38187e4939d19734672a37b19cb087035a31468cb041b8a6020516bbb7de5abc"
    ),
    "Docs/Stage1_Blueprint_rev-5.6.md": (
        "8145664aa8d0b02d99e6197a3e3d4fc695e0afaadcfaf3b2bf3128a5d9c0fe63"
    ),
    "skills/execute-stage1-rev56/SKILL.md": (
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8"
    ),
    "Stage1_Instances/THM-M-0594/intake.json": (
        "3f7d86ed95c748e0bd33e28d8eae9fa1957df86004d4eec06cce75e9010e70b0"
    ),
    "Stage1_Instances/THM-M-0594/statement.json": (
        "fd651a374b6c7569f8fe0a28950ec9e4b109bd2c9489096d348dc615ed896fe2"
    ),
    "Stage1_Instances/THM-M-0594/obligation-registry.json": (
        "ba31185450c503b47557f6e988f3176cfdc39d02acee60fc03425746837c6db5"
    ),
    "Stage1_Instances/THM-M-0594/typed-graphs.json": (
        "cecbfa3dfa5fea5917c11a076222609fc29c836a52ac343d63534c09f7138ec5"
    ),
    "Stage1_Instances/THM-M-0594/Statement.lean": (
        "a70005e624a0745c077c074e1eacf399c0050b45853721473d318b7eb3651445"
    ),
    "Stage1_Instances/THM-M-0594/ProofSupport.lean": (
        "67d205b49a8bd24bbd86e4cb75178e984b9825f996b5bd9854bcdb0814a29083"
    ),
    "Stage1_Instances/THM-M-0594/AnchorAudit.lean": (
        "5f5c674b00c1a911bc89d6806c078635db62bc2f9a9cce8b9617a4877a7ae89a"
    ),
    "Stage1_Instances/THM-M-0594/Proof.lean": (
        "4a46bdb092125e0a00d2450fd264f5f1f0be92c7cffa4fa5de1712316689e312"
    ),
    "Stage1_Instances/THM-M-0594/proof-receipt.json": (
        "36aa282a9e40fa96582f75d33723ad6647f516fd003785b30f68845af9108434"
    ),
    "Stage1_Instances/THM-M-0594/validation-receipt.json": (
        "945184a81e98d5169d59fbfd7592309b1a0db732613ddf5edcbc6e80b604b818"
    ),
    "Stage1_Instances/THM-M-0594/validation-blocker.json": (
        "59579e252c6b28b164f3781753a34ee251064273cfa20106961d42e31085266c"
    ),
    "Stage1_Instances/THM-M-0594/source_statement_crosswalk.md": (
        "9e1e24c6b1f5d39967f9a5ef1a3686f416f632c847ce8e5d2418dd544b0cb7aa"
    ),
    "Stage1_Instances/THM-M-0594/obligation-tree.md": (
        "25b99df5b349960901c12944c5c6a07ccebee4633fb7abf5c2bc4c777ce1ba0b"
    ),
    "Stage1_Instances/THM-M-0594/README.md": (
        "c85a1c508e83b092e898dc4588884c4e6a3ad24dd7f65762cdf499277d7a50ca"
    ),
    "Formalizations/Lean/lean-toolchain": (
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    ),
    "Formalizations/Lean/lakefile.lean": (
        "43259bbc1b42b1574b78c8584753029dc5e118c0a0e752ac0a5bad9004b4dcda"
    ),
    "Formalizations/Lean/lake-manifest.json": (
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
    ),
}
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "5516c9f362c29376ab9a499a33082f9f611941d8c75930c880e30ad109e39c9a"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
]
SUMMARY_LINES = [
    "PASS current-base trust-zero replay: exact statement and partial or conditional bodies elaborate with only the expected axioms",
    "PASS release reconciliation: target, DAG, receipts, registry, graph, hashes, and worktree classification agree",
    "BLOCKED dependency.S56-M-0594-VALIDATION.master_acceptance: validation is provisional, unaccepted, and nonrelease-grade",
    "BLOCKED exact root: M0594-C-GLOBAL has no premise-free body; H1/M3/R3 remains unchanged",
    "BLOCKED AUDIT-Z and THEOREM-Z: source, readability, trust, hermetic, supply-chain, and independent gates remain open",
    "verdict=blocked lifecycle=planned audit_complete=false theorem_complete=false accepted_receipts=0",
]
SUMMARY_SHA256 = "51f617d0388300c9f49c493e07c9444336127620e8371136beb95e23c1900767"
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL THM-M-0594 release: {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate JSON key {key!r} in {path.relative_to(ROOT)}")
            result[key] = value
        return result

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
        )
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {path.relative_to(ROOT)}: {error}")
    if not isinstance(value, dict):
        fail(f"expected JSON object in {path.relative_to(ROOT)}")
    return value


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600, expected_exit: int = 0,
) -> subprocess.CompletedProcess[str]:
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
        fail(
            f"command exited {result.returncode}, expected {expected_exit}: "
            f"{argv!r}\n{result.stdout}"
        )
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd, timeout=60).stdout.strip()


def code_without_comments(source: str) -> str:
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
                output.append("\n" if source[index] == "\n" else " ")
                index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                output.extend("  ")
                index += 2
            elif source[index] == '"':
                in_string = False
                output.append(" ")
                index += 1
            else:
                output.append("\n" if source[index] == "\n" else " ")
                index += 1
        elif source.startswith("/-", index):
            depth = 1
            output.extend("  ")
            index += 2
        elif source.startswith("--", index):
            while index < len(source) and source[index] != "\n":
                output.append(" ")
                index += 1
        elif source[index] == '"':
            in_string = True
            output.append(" ")
            index += 1
        else:
            output.append(source[index])
            index += 1
    if depth or in_string:
        fail("unterminated Lean comment or string")
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'[^']*{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        output,
        flags=re.DOTALL,
    )
    if match is None:
        fail(f"missing axiom report for {declaration}")
    return {
        part.strip()
        for part in match.group(1).replace("\n", "").split(",")
        if part.strip()
    }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
        fail(f"text hygiene failure: {path.relative_to(ROOT)}")
    if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
        fail(f"trailing whitespace: {path.relative_to(ROOT)}")


def compiled_roots() -> list[Path]:
    lake = LEAN_ROOT / ".lake"
    if not lake.is_symlink():
        fail("automation-provided pinned .lake symlink is missing")
    roots = sorted(
        (path / ".lake" / "build" / "lib" / "lean").resolve()
        for path in (lake / "packages").iterdir()
        if path.is_dir() and (path / ".lake" / "build" / "lib" / "lean").is_dir()
    )
    if not roots:
        fail("pre-existing pinned compiled artifacts are missing")
    return roots


def narrow_replay() -> dict[str, str]:
    fixed_env = {
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
    tool_root = (
        Path.home()
        / ".elan"
        / "toolchains"
        / "leanprover--lean4---v4.29.0"
        / "bin"
    )
    lean = tool_root / "lean"
    lake = tool_root / "lake"
    if sha256(lean) != LEAN_SHA256 or sha256(lake) != LAKE_SHA256:
        fail("Lean or Lake executable identity drifted")
    if sha256(Path("/usr/bin/python3").resolve()) != PYTHON_SHA256:
        fail("Python executable identity drifted")
    if sha256(Path("/usr/bin/git")) != GIT_SHA256:
        fail("Git executable identity drifted")
    if sha256(Path("/usr/bin/bwrap")) != BWRAP_SHA256:
        fail("Bubblewrap executable identity drifted")
    if LEAN_COMMIT not in run([str(lean), "--version"], env=fixed_env).stdout:
        fail("Lean version drifted")

    with tempfile.TemporaryDirectory(prefix="m0594-release-", dir="/tmp") as raw:
        tmp = Path(raw).resolve()
        (tmp / "home").mkdir()
        for name in ("Statement.lean", "ProofSupport.lean", "Proof.lean"):
            shutil.copy2(HERE / name, tmp / name)
        dependencies = ":".join(str(path) for path in compiled_roots())
        if not dependencies:
            fail("empty pinned Lean dependency path")
        base = [
            "/usr/bin/bwrap",
            "--ro-bind",
            "/",
            "/",
            "--bind",
            str(tmp),
            str(tmp),
            "--dev",
            "/dev",
            "--proc",
            "/proc",
            "--unshare-net",
            "--die-with-parent",
            "--clearenv",
            "--setenv",
            "HOME",
            str(tmp / "home"),
            "--setenv",
            "TMPDIR",
            str(tmp),
            "--setenv",
            "LANG",
            "C.UTF-8",
            "--setenv",
            "LC_ALL",
            "C.UTF-8",
            "--setenv",
            "TZ",
            "UTC",
            "--setenv",
            "LEAN_NUM_THREADS",
            "1",
            "--chdir",
            str(tmp),
        ]

        def lean_run(name: str, local_imports: bool, emit_olean: bool) -> str:
            module_path = dependencies
            if local_imports:
                module_path = f"{tmp}{os.pathsep}{dependencies}"
            argv = base + [
                "--setenv",
                "LEAN_PATH",
                module_path,
                str(lean),
                "--trust=0",
                "-t0",
            ]
            if emit_olean:
                argv += ["-o", Path(name).with_suffix(".olean").name]
            argv.append(name)
            return run(argv, timeout=600).stdout

        statement = lean_run("Statement.lean", False, True)
        support = lean_run("ProofSupport.lean", False, True)
        proof = lean_run("Proof.lean", True, False)
        return {"statement": statement, "support": support, "proof": proof}


def main() -> None:
    if sys.flags.optimize:
        fail("Python assertions must remain enabled")

    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    validation_blocker = load(HERE / "validation-blocker.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("base revision drifted")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("base tree drifted")
    for relative, expected in EXPECTED_INPUTS.items():
        if sha256(ROOT / relative) != expected:
            fail(f"reconciled input drifted: {relative}")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    if not (
        target["execution_rank"] == 255
        and target["baseline"] == "L0"
        and target["rework_required"] is True
        and target["legacy_artifacts_accepted"] is False
        and target["lifecycle_mode"] == "planned"
        and target["theorem_complete"] is False
    ):
        fail("target authority no longer records the planned uniform-L0 boundary")

    items = {row["id"]: row for row in execution["items"]}
    release_item = items[ITEM]
    validation_item = items["S56-M-0594-VALIDATION"]
    if release_item != {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 255,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0594-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }:
        fail("release DAG item drifted")
    if validation_item["state"] != "[_]" or validation_item["attempts"] != 1:
        fail("validation dependency projection drifted")

    if statement["declaration"] != "Stage1Instances.THM_M_0594.WhitneyEmbeddingTarget":
        fail("canonical declaration drifted")
    if statement["elaborated_expression_sha256"] != EXPRESSION_SHA256:
        fail("canonical expression drifted")
    if registry["root_obligation_id"] != "M0594-ROOT":
        fail("root obligation drifted")
    if registry["denominator_sha256"] != DENOMINATOR_SHA256:
        fail("registry denominator drifted")
    if graphs["registry_denominator_sha256"] != DENOMINATOR_SHA256:
        fail("typed-graph denominator drifted")
    closure = graphs["closure_boundary"]
    root = next(row for row in graphs["nodes"] if row["obligation_id"] == "M0594-ROOT")
    observed_vector = {
        "H": root["human_debt"],
        "M": root["machine_debt"],
        "R": root["readability_debt"],
    }
    if observed_vector != ROOT_VECTOR:
        fail("root vector drifted")
    if closure["root_closed"] is not False:
        fail("authoritative graph unexpectedly closes the root")
    if closure["audit_complete"] is not False or closure["theorem_complete"] is not False:
        fail("authoritative graph unexpectedly records a terminal decision")
    if closure["remaining_root_cut_set"] != AUTHORITATIVE_OPEN_CUT:
        fail("authoritative root cut drifted")

    if intake["canonical_formal_target"]["declaration_or_expression"] is not None:
        fail("release reconciliation gap changed: intake projection is no longer stale")
    if intake["canonical_formal_target"]["gate_state"] != "open_pending_statement_phase":
        fail("release reconciliation gap changed: intake gate state")

    if sha256(HERE / "validation-receipt.json") != VALIDATION_RECEIPT_SHA256:
        fail("validation receipt hash drifted")
    if not (
        validation["item_id"] == validation_item["id"]
        and validation["base_revision"] == VALIDATION_REVISION
        and validation["support_state"] == "provisional_worker_selftest"
        and validation["proposed_state"] == "[_]"
        and validation["accepted"] is False
        and validation["release_grade"] is False
        and validation["verdict"] == "blocked"
        and validation["accepted_receipt_ids"] == []
        and validation["accepted_closed_obligation_ids"] == []
        and validation["result"]["root_kernel_closed"] is False
        and validation["result"]["audit_complete"] is False
        and validation["result"]["theorem_complete"] is False
    ):
        fail("validation receipt no longer supports the negative release decision")
    if validation["authoritative_remaining_root_cut_set"] != AUTHORITATIVE_OPEN_CUT:
        fail("validation authoritative cut drifted")
    if validation["provisional_remaining_root_cut_set"] != PROVISIONAL_OPEN_CUT:
        fail("validation provisional cut drifted")
    if validation_blocker["first_failed_gate"] != (
        "dependency.S56-M-0594-PROOF.master_acceptance"
    ):
        fail("nested validation dependency failure drifted")

    if not (
        proof_receipt["accepted"] is False
        and proof_receipt["accepted_closed_obligation_ids"] == []
        and proof_receipt["provisionally_closed_obligation_ids"]
        == ["M0594-L-TOPOLOGICAL"]
        and proof_receipt["result"]["root_closed"] is False
        and proof_receipt["result"]["theorem_complete"] is False
    ):
        fail("partial proof receipt drifted")

    validation_ancestor = run(
        ["/usr/bin/git", "merge-base", "--is-ancestor", VALIDATION_REVISION, "HEAD"],
        expected_exit=0,
        timeout=60,
    )
    if validation_ancestor.stdout:
        fail("unexpected output from validation ancestor check")
    bound_validation_inputs = [
        "Stage1_Instances/THM-M-0594/Statement.lean",
        "Stage1_Instances/THM-M-0594/AnchorAudit.lean",
        "Stage1_Instances/THM-M-0594/ObligationTree.lean",
        "Stage1_Instances/THM-M-0594/ProofSupport.lean",
        "Stage1_Instances/THM-M-0594/ProofBoundary.lean",
        "Stage1_Instances/THM-M-0594/Proof.lean",
        "Stage1_Instances/THM-M-0594/statement.json",
        "Stage1_Instances/THM-M-0594/anchor_candidates.json",
        "Stage1_Instances/THM-M-0594/obligation-registry.json",
        "Stage1_Instances/THM-M-0594/typed-graphs.json",
        "Stage1_Instances/THM-M-0594/validation-specs.json",
        "Stage1_Instances/THM-M-0594/proof-receipt.json",
    ]
    if git("diff", "--name-only", f"{VALIDATION_REVISION}..HEAD", "--", *bound_validation_inputs):
        fail("a bound validation theorem input changed after its receipt")
    stale_validation = run(
        [
            "/usr/bin/python3",
            "-I",
            "-B",
            f"Stage1_Instances/{THEOREM}/check_validation.py",
            "--probe",
        ],
        expected_exit=1,
        timeout=60,
    )
    if "AssertionError" not in stale_validation.stdout or "rev-parse" not in stale_validation.stdout:
        fail("historical validation checker did not fail at its freshness assertion")

    for name in (
        "Statement.lean",
        "AnchorAudit.lean",
        "ObligationTree.lean",
        "ProofSupport.lean",
        "ProofBoundary.lean",
        "Proof.lean",
        "Validation.lean",
    ):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = source.replace("#print sorries", "")
        if PROHIBITED.search(source):
            fail(f"prohibited proof device in {name}")
    proof_source = code_without_comments((HERE / "Proof.lean").read_text(encoding="utf-8"))
    for premise in ("smooth", "proper", "injective", "immersion"):
        if premise not in proof_source:
            fail(f"conditional root boundary no longer exposes {premise}")

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    if mathlib_entry["rev"] != MATHLIB_REVISION:
        fail("mathlib manifest revision drifted")
    if not (LEAN_ROOT / ".lake").is_symlink():
        fail("pinned dependency symlink missing")
    mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
    if git("rev-parse", "HEAD", cwd=mathlib) != MATHLIB_REVISION:
        fail("mathlib checkout revision drifted")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != MATHLIB_TREE:
        fail("mathlib checkout tree drifted")
    if git("status", "--porcelain=v1", "--untracked-files=no", cwd=mathlib):
        fail("mathlib tracked worktree is dirty")
    whitney_source = (
        mathlib / "Mathlib" / "Geometry" / "Manifold" / "WhitneyEmbedding.lean"
    ).read_text(encoding="utf-8")
    if "[CompactSpace M]" not in whitney_source:
        fail("pinned compact endpoint boundary disappeared")
    if "Prove the weak Whitney embedding theorem" not in whitney_source:
        fail("pinned unrestricted-theorem TODO boundary disappeared")

    outputs = narrow_replay()
    support_declarations = (
        "exists_compact_exhaustion",
        "exists_global_smooth_bump_covering",
        "isEmbedding_of_isProperMap_of_injective",
    )
    proof_declarations = (
        "properInjectiveEuclideanMap_isEmbedding",
        "whitneyEmbeddingTarget_of_properInjectiveImmersion",
    )
    for declaration in support_declarations:
        if printed_axioms(outputs["support"], declaration) != EXPECTED_AXIOMS:
            fail(f"support axiom profile drifted: {declaration}")
    for declaration in proof_declarations:
        if printed_axioms(outputs["proof"], declaration) != EXPECTED_AXIOMS:
            fail(f"proof axiom profile drifted: {declaration}")
    if outputs["proof"].count("Declarations are sorry-free!") != 2:
        fail("partial proof sorry reports drifted")
    if "error:" in "\n".join(outputs.values()).lower():
        fail("narrow Lean replay emitted an error")

    if spec["schema_version"] != "stage1-release-spec/1.0":
        fail("release spec schema drifted")
    if spec["item_id"] != ITEM or spec["expected_decision"]["verdict"] != "blocked":
        fail("release spec decision drifted")
    if len(spec.get("recipes", [])) != 1:
        fail("release spec must contain exactly one recipe")
    recipe = spec["recipes"][0]
    expected_recipe = {
        "recipe_id": "S56-M-0594-RELEASE-current-base-reconciliation-v1",
        "cwd": ".",
        "argv": [
            "/usr/bin/python3",
            "-I",
            "-B",
            f"Stage1_Instances/{THEOREM}/check_release.py",
            "--worker-packet",
            ".stage1-worker-selftest.json",
        ],
        "env_allowlist": {
            "HOME": (
                "explicitly variable worker home used only to resolve the "
                "content-hashed pinned toolchain root"
            ),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_NUM_THREADS": "1",
        },
        "timeout_seconds": 600,
        "network_policy": "denied during the narrow Lean replay",
        "expected_exit": 0,
        "expected_outputs": [
            {
                "path_or_stream": "stdout",
                "semantic_hash_policy": (
                    "sha256:51f617d0388300c9f49c493e07c9444336127620e8371136beb95e23c1900767 "
                    "over the exact six-line UTF-8 PASS/BLOCKED summary with a final newline"
                ),
            }
        ],
        "covered_obligation_ids": [
            "M0594-ROOT",
            "M0594-C-GLOBAL",
            "M0594-L-TOPOLOGICAL",
        ],
        "covered_declarations": [
            "Stage1Instances.THM_M_0594.WhitneyEmbeddingTarget",
            "Stage1Instances.THM_M_0594.properInjectiveEuclideanMap_isEmbedding",
            "Stage1Instances.THM_M_0594.whitneyEmbeddingTarget_of_properInjectiveImmersion",
        ],
        "coverage_boundary": (
            "The recipe re-elaborates the exact statement and existing partial or "
            "conditional bodies at trust zero, then derives a fail-closed release "
            "decision from current structured authority. It does not implement the "
            "missing global construction or qualify as a cold independent release run."
        ),
    }
    if recipe != expected_recipe:
        fail("release recipe contract drifted")
    actual_summary_sha256 = hashlib.sha256(
        ("\n".join(SUMMARY_LINES) + "\n").encode()
    ).hexdigest()
    if actual_summary_sha256 != SUMMARY_SHA256:
        fail("release semantic output hash drifted")

    if not (
        decision["schema_version"] == "stage1-release-decision/1.0"
        and decision["item_id"] == ITEM
        and decision["theorem_id"] == THEOREM
        and decision["base_revision"] == BASE_REVISION
        and decision["base_tree"] == BASE_TREE
        and decision["support_state"] == "provisional_worker_selftest"
        and decision["proposed_state"] == "[_]"
        and decision["accepted"] is False
        and decision["release_grade"] is False
        and decision["release_accepted"] is False
        and decision["verdict"] == "blocked"
        and decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
        and decision["accepted_receipt_ids"] == []
        and decision["accepted_closed_obligation_ids"] == []
    ):
        fail("release decision identity or boundary drifted")
    dependency = decision["dependency"]
    if not (
        dependency["item_id"] == validation["item_id"]
        and dependency["receipt_id"] == validation["receipt_id"]
        and dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
        and dependency["accepted"] is False
        and dependency["release_grade"] is False
        and dependency["master_accepted"] is False
    ):
        fail("release dependency reconciliation drifted")
    if decision["root_vector"]["accepted_before"] != ROOT_VECTOR:
        fail("release before vector drifted")
    if decision["root_vector"]["accepted_after"] != ROOT_VECTOR:
        fail("release after vector drifted")
    if decision["terminal_decisions"] != {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
        "release_accepted": False,
    }:
        fail("terminal decisions drifted")
    if decision["first_failed_gate"]["node_gate"] != (
        "dependency.S56-M-0594-VALIDATION.master_acceptance"
    ):
        fail("first release gate drifted")
    if decision["first_failed_theorem_gate"]["node_gate"] != "M0594-C-GLOBAL":
        fail("first theorem gate drifted")
    if decision["authoritative_remaining_root_cut_set"] != AUTHORITATIVE_OPEN_CUT:
        fail("decision authoritative cut drifted")
    if decision["provisional_remaining_root_cut_set"] != PROVISIONAL_OPEN_CUT:
        fail("decision provisional cut drifted")
    required_cut_fragments = (
        "S56-M-0594-VALIDATION",
        "M0594-C-GLOBAL",
        "AUDIT-Z",
        "H0 primary-source",
        "R0 node-specific",
        "transitive declaration",
        "empty-cache network-denied cold build",
        "SBOM and license",
        "Two signed attestations",
        "minimal verifier",
        "Deterministic content-addressed release bundle",
    )
    release_cut = "\n".join(decision["remaining_release_cut_set"])
    for fragment in required_cut_fragments:
        if fragment not in release_cut:
            fail(f"remaining release cut omits {fragment!r}")

    if not (
        receipt["schema_version"] == "stage1-node-receipt/1.0"
        and receipt["item_id"] == ITEM
        and receipt["base_revision"] == BASE_REVISION
        and receipt["base_tree"] == BASE_TREE
        and receipt["accepted"] is False
        and receipt["release_grade"] is False
        and receipt["verdict"] == "blocked"
        and receipt["accepted_receipt_ids"] == []
        and receipt["accepted_closed_obligation_ids"] == []
        and receipt["result"]["root_kernel_closed"] is False
        and receipt["result"]["audit_complete"] is False
        and receipt["result"]["theorem_complete"] is False
        and receipt["result"]["release_accepted"] is False
    ):
        fail("release receipt boundary drifted")
    for relative, expected in receipt["inputs"].items():
        path = ROOT / relative if "/" in relative else HERE / relative
        if sha256(path) != expected:
            fail(f"receipt input drifted: {relative}")
    if receipt["recipe"] != recipe:
        fail("release receipt recipe differs from the release specification")
    if receipt["changed_paths"] != CHANGED_PATHS:
        fail("release receipt changed paths drifted")
    if receipt["known_failures"] != decision["known_failures"]:
        fail("release decision and receipt failures disagree")
    recorded_environment = receipt["environment"]
    if recorded_environment["lean_executable_sha256"] != LEAN_SHA256:
        fail("receipt Lean executable identity drifted")
    if recorded_environment["lake_executable_sha256"] != LAKE_SHA256:
        fail("receipt Lake executable identity drifted")
    if recorded_environment["python_executable_sha256"] != PYTHON_SHA256:
        fail("receipt Python executable identity drifted")
    if recorded_environment["git_executable_sha256"] != GIT_SHA256:
        fail("receipt Git executable identity drifted")
    if recorded_environment["bwrap_executable_sha256"] != BWRAP_SHA256:
        fail("receipt Bubblewrap executable identity drifted")
    if recorded_environment["network_used"] is not False:
        fail("release receipt must not claim network use")
    if recorded_environment["lake_mutated"] is not False:
        fail("release receipt must record no Lake mutation")
    worktree_record = decision["worktree_classification"]
    symlink_target = os.readlink(LEAN_ROOT / ".lake")
    symlink_target_sha256 = hashlib.sha256(symlink_target.encode()).hexdigest()
    if worktree_record["preexisting_untracked_symlink_target_sha256"] != (
        symlink_target_sha256
    ):
        fail("recorded dependency symlink target identity drifted")
    if worktree_record["network_used"] is not False:
        fail("release decision must not claim network use")
    if worktree_record["lake_mutated"] is not False:
        fail("release decision must record no Lake mutation")

    status = git("status", "--short", "--untracked-files=all")
    status_lines = status.splitlines()
    if "?? Formalizations/Lean/.lake" not in status_lines:
        fail("pre-existing automation .lake symlink is missing from worktree classification")
    actual_changed = sorted(
        line[3:]
        for line in status_lines
        if line[3:] != "Formalizations/Lean/.lake"
    )
    expected_changed = sorted(
        relative for relative in CHANGED_PATHS if (ROOT / relative).exists()
    )
    if actual_changed != expected_changed:
        fail(f"scoped changed paths disagree: {actual_changed!r}")

    if args.worker_packet is not None:
        packet_path = args.worker_packet
        if not packet_path.is_absolute():
            packet_path = ROOT / packet_path
        packet = load(packet_path)
        if set(packet) != {
            "item_id",
            "changed_paths",
            "commands",
            "output_summary",
            "base_revision",
            "known_failures",
            "state",
        }:
            fail("worker packet fields drifted")
        if packet["item_id"] != ITEM or packet["state"] != "[_]":
            fail("worker packet identity or state drifted")
        if packet["base_revision"] != BASE_REVISION:
            fail("worker packet base drifted")
        if packet["changed_paths"] != CHANGED_PATHS:
            fail("worker packet changed paths drifted")
        if packet["known_failures"] != decision["known_failures"]:
            fail("worker packet failures drifted")
        if packet["output_summary"] != "\n".join(SUMMARY_LINES):
            fail("worker packet output summary drifted")
        if packet["commands"][-1] != {
            "argv": recipe["argv"],
            "cwd": ".",
            "exit_code": 0,
            "output_summary": "exact six-line PASS/BLOCKED summary",
        }:
            fail("worker packet release command drifted")

    for relative in expected_changed:
        assert_text_hygiene(ROOT / relative)
    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
