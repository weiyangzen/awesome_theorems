#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0927-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import subprocess
import sys
import tempfile


if not __debug__:
    raise SystemExit("release validation requires Python assertions")

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0927"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0927-RELEASE"
THEOREM = "THM-M-0927"
BASE_REVISION = "062e0b530c644c6d9c62556518568dd91a7374cd"
BASE_TREE = "0879a3d554dc3011e1c5b513107c330547ea185c"
VALIDATION_BASE = "c93e664d3a7e0383b037cfa2d5e47ba14adfb2cb"
ROOT_VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
EXPRESSION_SHA256 = "0a05e8c4976c01759ef82d364afc86f498f700edc1a0fcb3f8935765992b5a2f"
DENOMINATOR_SHA256 = "96eb539e67048140003ad8ed68e84ef0fd1daa215803f7915908af2999c373de"
PROOF_RECEIPT_SHA256 = "d84a1cb91e15c73ecbf00a917f9ebab56bd0a58d107fc9a10ba2ef3915ffc8b7"
VALIDATION_RECEIPT_SHA256 = "7b059a27adf7bf35809c669fc4c8bb14abb5df962d48b5be717ac5ba7a93f430"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
TERMINAL_BLOB = "9e9a9f050354f828a54fb235846405987daa4971"
TERMINAL_SOURCE_SHA256 = "e3a6e5160e654dfb4c5594c66a624fa7a5edffa4c1b839d992be7d1ba2dd7ac3"
TERMINAL_BODY_SHA256 = "e3e11b1c82c6f3718202d10bc5fe89a811e4c0890b0dcd535014a2a6f1385814"
TERMINAL_OLEAN_SHA256 = "4d72dd79c76182da4a00619140ff0d127c815f32c258a9ea3b23e28cf345d88b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

INVENTORY_IDS = [
    "M0927-ROOT", "M0927-S-INTERFACE", "M0927-S-BOUNDARY",
    "M0927-S-FUNCTION-TRANSPORT", "M0927-S-RADICAL-TRANSPORT",
    "M0927-S-FOUNDATION", "M0927-N-ROOT-SPELLING",
    "M0927-N-FUNCTION-POINTWISE", "M0927-L-RECURRENCE-DEFINITION",
    "M0927-L-FIB-SOLUTION", "M0927-L-PHI-SOLUTION",
    "M0927-L-PSI-SOLUTION", "M0927-C-RHS-SOLUTION",
    "M0927-B-INITIAL-CASES", "M0927-B-INITIAL-ZERO",
    "M0927-B-INITIAL-ONE", "M0927-X-RECURRENCE-UNIQUENESS",
    "M0927-T-FUNCTION-BINET", "M0927-T-POINTWISE-BINET",
    "M0927-T-ROOT-COMPOSE", "M0927-X-SOURCE", "M0927-X-PROVENANCE",
    "M0927-X-EVIDENCE", "M0927-X-TRUST", "M0927-X-READABLE",
    "M0927-X-WORKFLOW",
]
AUTHORITATIVE_CUT = [
    "M0927-T-FUNCTION-BINET", "M0927-X-SOURCE", "M0927-S-FOUNDATION",
    "M0927-X-PROVENANCE", "M0927-X-EVIDENCE", "M0927-X-TRUST",
    "M0927-X-READABLE", "M0927-X-WORKFLOW",
]
VALIDATION_ASSURANCE_CUT = AUTHORITATIVE_CUT[1:]
UNVERIFIED_PLAN_IDS = [
    "DECOMP-M0927-T-FUNCTION-BINET", "DECOMP-M0927-B-INITIAL-CASES",
    "DECOMP-M0927-C-RHS-SOLUTION", "DECOMP-M0927-L-PHI-SOLUTION",
    "DECOMP-M0927-L-PSI-SOLUTION", "DECOMP-M0927-L-FIB-SOLUTION",
    "DECOMP-M0927-T-POINTWISE-BINET", "DECOMP-M0927-S-RADICAL-TRANSPORT",
]
UNRECONCILED_IDS = [
    "M0927-ROOT", "M0927-T-FUNCTION-BINET", "M0927-B-INITIAL-CASES",
    "M0927-C-RHS-SOLUTION", "M0927-L-PHI-SOLUTION",
    "M0927-L-PSI-SOLUTION", "M0927-L-FIB-SOLUTION",
    "M0927-T-POINTWISE-BINET", "M0927-S-RADICAL-TRANSPORT",
    "M0927-X-SOURCE", "M0927-S-FOUNDATION", "M0927-X-PROVENANCE",
    "M0927-X-EVIDENCE", "M0927-X-TRUST", "M0927-X-READABLE",
    "M0927-X-WORKFLOW",
]
PROOF_DECLARATIONS = (
    "Real.coe_fib_eq'",
    "Stage1Instances.THM_M_0927.Proof.functionBinet_proof",
    "Stage1Instances.THM_M_0927.Proof.binetFormula_proof",
)
VALIDATION_DECLARATION = (
    "Stage1Instances.THM_M_0927.Validation.independentlyRecomposedBinetFormula"
)

EXPECTED_INPUTS = {
    "README.md": "1f03059b628318458d1767b57158b6622e788eb14adba7fa488f912dac83fedf",
    "instance.json": "18fc4a8a74fd092cce4138e64c68a803e16736826262e4ce3e453d6b61693613",
    "task-dag.json": "a23b73fe4200528e269ccd7072e1917187d78207b0f525716df9a090f350df50",
    "Statement.lean": "72172fb6015846b808a81dfc4995767dec5381de5845f68c47cbc5fdb2eeed8d",
    "ObligationTree.lean": "b254d92e1398b4b8f144d9be31339370dd427e333998857d279c80d09debf347",
    "Proof.lean": "340f937f1222e786c41d145d8bd29ac13600eec770a1c53628eb897106f0eafb",
    "Validation.lean": "2f8bdfdd947f35f7bb2036c345a5b508f7ec929ab261df4db3549bc3df113109",
    "statement.json": "4649bc7f024d4dfd353d857ada5829b963c08da5549e060f63e9f6416a37bf95",
    "anchor-audit.json": "166999961169125272df80df7948f19be2e31b67fc072c8ae6b66286487a1933",
    "obligation-registry.json": "93d2f3f4b48d713ace523b2049ff2aa9505f40f4332a30ca13a5f1bafdc9b05c",
    "typed-graphs.json": "3a4aca9e328628b5513e9aa788eae132fd0827ead3ace586c403b5a577888c87",
    "source-statement-crosswalk.md": "a364820431fd8335f6ba7ea588286ed2a34c5fc657e92a2bd58e79681efd0061",
    "obligation-tree.md": "a56a8a17f8d5dca45f34fbb9253a041a9910b21b4793bda6f6e5f431a0686109",
    "proof-receipt.json": PROOF_RECEIPT_SHA256,
    "proof-validation.md": "f0bab569b45b0a9db2f07e9ee8f34929a38d4f53d03916842e12422166da4504",
    "validation-spec.json": "fed228530b88fe7a849ff88abeb67c6e4b4e0d46839a12bce385f3524702c660",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "0327571941127a85cf3ad284f3c1f9590b1766838d6eaeaa5d0f5b2367f75e34",
    "validation-phase.md": "e54aefa9e7f610dd318820c973b1130a4ee9ffd83a936f031a8ca6b8c37f53f9",
}
EXPECTED_AUTHORITY = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "c295df9844ba7f5638993017844f11a6f92ef8579aa85c08fd79a63a8f282e66",
    "Docs/Stage1_Blueprint_rev-5.6.md": "5fd2a2a1c3ec335d3b73b37182546bfbdc89d97b0353ddd67eddb7b4d47c505b",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_RELEASE = {
    "release-spec.json": "4250e2795f835d6c096f830ebb05368836c98a7f0e5d7b2315161a8a3374b42e",
    "release-decision.json": "f7da64f22cf8a266ffdb143c8e1649e2c0eda63b852157ae1d26767bdc001b69",
    "release-validation.md": "b054333c5e83de09e362983c669242db28ada4308d15c3b5d14494a3033ccbd9",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = (
    "PASS current-head direct Lean replay: exact root and differential root are sorry-free at trust zero",
    "PASS release reconciliation: authority, inputs, provisional receipts, registry, graph, and dependency state agree",
    "BLOCKED dependency.S56-M-0927-VALIDATION.master_acceptance",
    "BLOCKED authoritative reconciliation: accepted root remains H1/M3/R4 with zero accepted receipts",
    "BLOCKED AUDIT-Z and THEOREM-Z: H0/R0, trust, hermetic, and independent gates are open",
    "BLOCKED S56-10.6-HERMETIC-COLD-EMPTY-CACHE: current replay uses shared warm pinned artifacts",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
)
KNOWN_FAILURES = [
    "S56-M-0927-VALIDATION and every transitive phase receipt remain provisional [_], not dependency-ordered master accepted or release-grade.",
    "The authoritative planned instance remains H1/M3/R4 with accepted_proof_state=[]; the local task DAG remains open and the typed graph has zero accepted obligations or receipts.",
    "The integrated validation recipe is snapshot-bound to c93e664d3a7e0383b037cfa2d5e47ba14adfb2cb and is not current release evidence; this release phase instead performs a fresh current-head bounded replay.",
    "The frozen graph predates provisional Proof.lean, still treats M0927-T-FUNCTION-BINET as open, and contains eight unverified internal decomposition plans without exact child-to-parent certificates.",
    "The primary-source crosswalk is not independently accepted H0, and no required node has independently accepted R0 evidence.",
    "The observed axiom set has no accepted theorem-specific foundation policy, and complete transitive declaration, source-origin, compiled-artifact, TCB, computation, SBOM, archive, and license closure are absent.",
    "The current direct Lean replay reuses the automation-provided shared warm pinned artifacts; there is no immutable clean input, empty-cache cold offline restoration, two distinct signed runners, independently implemented minimal verifier, protected release CI, or deterministic release bundle.",
    "Accepted state remains H1/M3/R4 with audit_complete=false and theorem_complete=false; no M0-W/E0/E1, AUDIT-Z, THEOREM-Z, release, or theorem-completion credit is granted.",
]


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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_slice(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1:end])).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900, expected_exit: int = 0,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    assert result.returncode == expected_exit, (
        f"command exited {result.returncode}, expected {expected_exit}: {argv!r}\n"
        f"{result.stdout}"
    )
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["/usr/bin/git", *args], cwd=cwd).stdout.strip()


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms:") + r"\s*\[([^]]*)]",
        output, re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def current_direct_replay() -> dict[str, object]:
    account_home = Path(pwd.getpwuid(os.getuid()).pw_dir)
    toolchain_root = account_home / ".elan/toolchains/leanprover--lean4---v4.29.0"
    lean = toolchain_root / "bin/lean"
    assert sha256(lean) == LEAN_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"]).stdout

    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink()
    lake_target = lake_link.resolve(strict=True)
    before_stat = lake_target.stat()
    dependency_roots = [
        (lake_link / "packages" / name / ".lake/build/lib/lean").resolve()
        for name in (
            "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
            "LeanSearchClient", "plausible", "mathlib",
        )
    ]
    local_root = (lake_link / "build/lib/lean").resolve()
    assert all(path.is_dir() for path in [*dependency_roots, local_root])
    lean_path = ":".join(
        [*(str(path) for path in dependency_roots), str(local_root),
         str(toolchain_root / "lib/lean")]
    )
    base_env = {
        "HOME": str(account_home),
        "PATH": f"{toolchain_root / 'bin'}:/usr/bin:/bin",
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC",
        "NO_COLOR": "1", "LEAN_NUM_THREADS": "1",
    }

    mathlib = lake_link / "packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=mathlib) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    terminal = mathlib / "Mathlib/NumberTheory/Real/GoldenRatio.lean"
    terminal_olean = mathlib / ".lake/build/lib/lean/Mathlib/NumberTheory/Real/GoldenRatio.olean"
    assert git(
        "rev-parse", "HEAD:Mathlib/NumberTheory/Real/GoldenRatio.lean", cwd=mathlib
    ) == TERMINAL_BLOB
    assert sha256(terminal) == TERMINAL_SOURCE_SHA256
    assert hash_slice(terminal, 180, 195) == TERMINAL_BODY_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert sha256(mathlib / "LICENSE") == MATHLIB_LICENSE_SHA256

    with tempfile.TemporaryDirectory(prefix="stage1-m0927-release-", dir="/tmp") as name:
        tmp = Path(name)
        for filename in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            shutil.copy2(HERE / filename, tmp / filename)

        def elaborate(filename: str, module_path: str, emit: bool) -> str:
            source = tmp / filename
            argv = [str(lean), "--trust=0", "-t0"]
            if emit:
                argv += ["-o", str(source.with_suffix(".olean"))]
            argv.append(str(source))
            env = dict(base_env)
            env["LEAN_PATH"] = module_path
            return run(argv, cwd=tmp, env=env).stdout

        statement = elaborate("Statement.lean", lean_path, True)
        local_path = f"{tmp}:{lean_path}"
        tree = elaborate("ObligationTree.lean", local_path, True)
        proof = elaborate("Proof.lean", local_path, True)
        validation = elaborate("Validation.lean", local_path, False)

    assert lake_link.resolve(strict=True) == lake_target
    assert lake_target.stat() == before_stat
    assert proof.count("Declarations are sorry-free!") == 3
    assert validation.count("Declarations are sorry-free!") == 4
    for declaration in PROOF_DECLARATIONS:
        assert reported_axioms(proof, declaration) == EXPECTED_AXIOMS
    assert reported_axioms(validation, VALIDATION_DECLARATION) == EXPECTED_AXIOMS
    combined = "\n".join((statement, tree, proof, validation))
    assert "declaration uses 'sorry'" not in combined and "sorryAx" not in combined
    assert "error:" not in combined.lower()

    closure = re.search(
        r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+).*?"
        r"VALIDATION_CLOSURE axioms=\[([^]]*)].*?"
        r"VALIDATION_CLOSURE unexpected_bodyless=\[([^]]*)].*?"
        r"VALIDATION_CLOSURE unsafe=\[([^]]*)]",
        validation, re.DOTALL,
    )
    assert closure is not None
    assert {part.strip() for part in closure.group(3).split(",") if part.strip()} == EXPECTED_AXIOMS
    assert closure.group(4).strip() == "" and closure.group(5).strip() == ""

    semantic_output = {
        "statement": {
            "mutation_type_mismatches": statement.count("Type mismatch"),
            "axiom_reports": statement.count("depends on axioms:"),
            "canonical_target_printed": (
                "def Stage1Instances.THM_M_0927.BinetFormulaTarget : Prop" in statement
            ),
        },
        "tree": {
            "checked_interfaces": tree.count("Stage1Instances.THM_M_0927.ObligationTree."),
            "axiom_reports": tree.count("depends on axioms:"),
            "sorry_free_reports": tree.count("Declarations are sorry-free!"),
        },
        "proof": {
            "axioms": {
                declaration: sorted(reported_axioms(proof, declaration))
                for declaration in PROOF_DECLARATIONS
            },
            "sorry_free_reports": proof.count("Declarations are sorry-free!"),
        },
        "validation": {
            "axioms": {
                declaration: sorted(reported_axioms(validation, declaration))
                for declaration in (*PROOF_DECLARATIONS, VALIDATION_DECLARATION)
            },
            "sorry_free_reports": validation.count("Declarations are sorry-free!"),
            "closure_declaration_count": int(closure.group(1)),
            "closure_module_count": int(closure.group(2)),
            "closure_bodyless_nonaxioms": [],
            "closure_unsafe_declarations": [],
        },
    }
    semantic_output_sha256 = hashlib.sha256(
        json.dumps(semantic_output, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    expected_semantic_output_sha256 = (
        "cdbc68363fe801659406f37cd8f5cb50bb751a3f074ec6a794735815239eeaf8"
    )
    if semantic_output_sha256 != expected_semantic_output_sha256:
        print(
            json.dumps(
                {
                    "observed_semantic_output_sha256": semantic_output_sha256,
                    "semantic_output": semantic_output,
                },
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        raise AssertionError("direct-replay semantic output drifted")
    return {
        "semantic_output_sha256": semantic_output_sha256,
        "proof_sorry_free_reports": 3,
        "validation_sorry_free_reports": 4,
        "closure_declaration_count": int(closure.group(1)),
        "closure_module_count": int(closure.group(2)),
    }


def main() -> None:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for filename, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / filename) == expected, f"release input drifted: {filename}"
    for relative, expected in EXPECTED_AUTHORITY.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    for filename, expected in EXPECTED_RELEASE.items():
        assert sha256(HERE / filename) == expected, f"release artifact drifted: {filename}"

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1546 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0927-VALIDATION"
    )
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 1546,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": [validation_item["id"]],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    assert instance["lifecycle"] == tasks["lifecycle"] == "planned"
    assert instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert tasks["accepted_states"] == [] and all(row["state"] == "open" for row in tasks["tasks"])
    local_release = next(row for row in tasks["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open" and local_release["evidence_ids"] == []
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["root_node_id"] == registry["root_obligation_id"] == "M0927-ROOT"
    assert graphs["closure_boundary"] == {
        "accepted_closed_obligations": [], "root_closed": False,
        "accepted_root_machine_debt": "M3", "audit_complete": False,
        "theorem_complete": False,
        "minimal_open_machine_proof_cut_sets": [["M0927-T-FUNCTION-BINET"]],
        "remaining_root_cut_set": AUTHORITATIVE_CUT,
        "reason": (
            "The exact pinned function theorem remains an audited candidate rather than an "
            "installed proof-phase child. Source, trust, evidence, readability, validation, "
            "release, and master acceptance remain open."
        ),
    }
    assert [row["plan_id"] for row in graphs["unverified_decomposition_plans"]] == UNVERIFIED_PLAN_IDS

    assert sha256(HERE / "proof-receipt.json") == PROOF_RECEIPT_SHA256
    assert proof["accepted"] is False and proof["proposed_state"] == "[_]"
    assert proof["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is proof["result"]["theorem_complete"] is False
    assert proof["remaining_assurance_cut_set"] == VALIDATION_ASSURANCE_CUT
    assert proof["root_evidence"]["unverified_decomposition_plan_ids"] == UNVERIFIED_PLAN_IDS
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked" and validation["accepted_receipt_ids"] == []
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == "dependency.S56-M-0927-PROOF.master_acceptance"
    assert validation["remaining_root_cut_set"] == VALIDATION_ASSURANCE_CUT

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == packet["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["decision_id"] == receipt["decision_id"] == receipt["receipt_id"]
    assert decision["proposed_state"] == receipt["proposed_state"] == packet["state"] == "[_]"
    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["accepted"] is receipt["accepted"] is False
    assert receipt["master_accepted"] is receipt["release_grade"] is receipt["release_accepted"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector"]["accepted_before"] == ROOT_VECTOR
    assert decision["root_vector"]["accepted_after"] == ROOT_VECTOR
    assert decision["accepted_receipt_ids"] == decision["accepted_closed_obligation_ids"] == []
    assert decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked", "release_accepted": False,
    }
    assert decision["first_failed_gate"]["node_gate"] == (
        "dependency.S56-M-0927-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_reproduction_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert decision["authoritative_remaining_root_cut_set"] == AUTHORITATIVE_CUT
    assert decision["unreconciled_architecture_obligation_ids"] == UNRECONCILED_IDS
    assert decision["canonical_obligation_ids"] == INVENTORY_IDS
    assert decision["evidence_reconciliation"]["current_warm_trust_zero_exact_root_replay"] is True
    for key in (
        "dependency_master_acceptance", "authoritative_graph_reconciliation",
        "accepted_exact_root_m0w_e1", "audit_inventory_reconciliation",
        "pinpoint_h0_review", "independent_r0_review", "accepted_foundation_profile",
        "complete_provenance_trust_tcb_sbom_and_license_closure",
        "immutable_clean_release_input", "hermetic_cold_offline_replay",
        "independent_signed_runner_attestations", "independent_minimal_verifier",
        "protected_ci_mutation_gates", "deterministic_release_bundle", "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key

    expected_dependency = {
        "item_id": validation_item["id"], "scheduler_projection": "[_]",
        "receipt_id": validation["receipt_id"], "receipt_sha256": VALIDATION_RECEIPT_SHA256,
        "support_state": "provisional_worker_selftest", "accepted": False,
        "release_grade": False, "master_accepted": False, "verdict": "blocked",
        "receipt_base_revision": VALIDATION_BASE, "current_snapshot_recipe_replayable": False,
    }
    assert decision["dependency"] == receipt["dependency"] == expected_dependency
    assert receipt["accepted_receipt_ids"] == receipt["accepted_closed_obligation_ids"] == []
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["result"]["root_vector_before"] == ROOT_VECTOR
    assert receipt["result"]["root_vector_after"] == ROOT_VECTOR
    assert receipt["result"]["authoritative_remaining_root_cut_set"] == AUTHORITATIVE_CUT
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False

    assert spec["argv"] == [
        "/usr/bin/python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0 and spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]
    assert spec["coverage_kind"] == "negative_release_reconciliation_no_closure_credit"
    assert receipt["recipe"] == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
            "covered_obligation_ids", "covered_declarations",
        )
    }

    for relative, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == expected, relative
    expected_binding_paths = {
        *(f"Stage1_Instances/{THEOREM}/{name}" for name in EXPECTED_INPUTS),
        *EXPECTED_AUTHORITY,
    }
    assert set(receipt["input_bindings"]) == expected_binding_paths
    for relative, expected in receipt["release_artifact_bindings"].items():
        assert sha256(ROOT / relative) == expected, relative
    assert set(receipt["release_artifact_bindings"]) == {
        f"Stage1_Instances/{THEOREM}/{name}" for name in EXPECTED_RELEASE
    }

    observation = current_direct_replay()
    replay = receipt["current_direct_replay"]
    assert replay["semantic_output_sha256"] == observation["semantic_output_sha256"]
    for key in (
        "proof_sorry_free_reports", "validation_sorry_free_reports",
        "closure_declaration_count", "closure_module_count",
    ):
        assert replay[key] == observation[key], key
    assert replay["observed_axioms"] == sorted(EXPECTED_AXIOMS)
    assert replay["closure_bodyless_nonaxioms"] == replay["closure_unsafe_declarations"] == []

    assert decision["known_failures"] == receipt["known_failures"] == packet["known_failures"] == KNOWN_FAILURES
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert set(receipt["repository_state"]["changed_paths"]) == CHANGED_PATHS
    assert "truthfully blocked" in packet["output_summary"]
    assert "audit_complete=false" in packet["output_summary"]
    assert "theorem_complete=false" in packet["output_summary"]

    actual = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
    }
    actual.discard("Formalizations/Lean/.lake")
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
    assert (LEAN_ROOT / ".lake").is_symlink()
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H1, M3, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "accepts no receipt", "current-head direct replay",
    ):
        assert fragment in handoff, fragment

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
