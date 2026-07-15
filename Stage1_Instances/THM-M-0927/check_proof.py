#!/usr/bin/env python3
"""Fail-closed proof-phase checks for S56-M-0927-PROOF."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


if not __debug__:
    raise SystemExit("check_proof.py must run without Python optimization")


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0927-PROOF"
THEOREM = "THM-M-0927"
BASE_REVISION = "4d389eb47e043f6f44925a418baee0d034f764ba"
BASE_TREE = "64faabd76665273032b8cb1554b90655b5c94256"
EXPRESSION_SHA256 = "0a05e8c4976c01759ef82d364afc86f498f700edc1a0fcb3f8935765992b5a2f"
DENOMINATOR_SHA256 = "96eb539e67048140003ad8ed68e84ef0fd1daa215803f7915908af2999c373de"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TERMINAL_BLOB = "9e9a9f050354f828a54fb235846405987daa4971"
TERMINAL_SOURCE_SHA256 = "e3a6e5160e654dfb4c5594c66a624fa7a5edffa4c1b839d992be7d1ba2dd7ac3"
TERMINAL_BODY_SHA256 = "e3e11b1c82c6f3718202d10bc5fe89a811e4c0890b0dcd535014a2a6f1385814"
TERMINAL_OLEAN_SHA256 = "4d72dd79c76182da4a00619140ff0d127c815f32c258a9ea3b23e28cf345d88b"
PROVISIONAL_IDS = [
    "M0927-ROOT",
    "M0927-T-ROOT-COMPOSE",
    "M0927-T-FUNCTION-BINET",
    "M0927-S-FUNCTION-TRANSPORT",
    "M0927-S-RADICAL-TRANSPORT",
]
UNVERIFIED_PLAN_IDS = [
    "DECOMP-M0927-T-FUNCTION-BINET",
    "DECOMP-M0927-B-INITIAL-CASES",
    "DECOMP-M0927-C-RHS-SOLUTION",
    "DECOMP-M0927-L-PHI-SOLUTION",
    "DECOMP-M0927-L-PSI-SOLUTION",
    "DECOMP-M0927-L-FIB-SOLUTION",
    "DECOMP-M0927-T-POINTWISE-BINET",
    "DECOMP-M0927-S-RADICAL-TRANSPORT",
]
REMAINING_ASSURANCE_CUT = [
    "M0927-X-SOURCE",
    "M0927-S-FOUNDATION",
    "M0927-X-PROVENANCE",
    "M0927-X-EVIDENCE",
    "M0927-X-TRUST",
    "M0927-X-READABLE",
    "M0927-X-WORKFLOW",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


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


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def run(
    argv: list[str], *, cwd: Path, env: dict[str, str] | None = None,
    timeout: int = 180,
) -> str:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        timeout=timeout, check=False,
    )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


def without_comments_and_strings(source: str) -> str:
    out: list[str] = []
    index = 0
    depth = 0
    quoted = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                out.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                out.extend("  ")
                index += 2
            else:
                out.append("\n" if char == "\n" else " ")
                index += 1
        elif quoted:
            out.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            index += 1
        elif pair == "/-":
            depth = 1
            out.extend("  ")
            index += 2
        elif pair == "--":
            end = source.find("\n", index)
            if end == -1:
                out.extend(" " * (len(source) - index))
                index = len(source)
            else:
                out.extend(" " * (end - index))
                index = end
        elif char == '"':
            quoted = True
            out.append(" ")
            index += 1
        else:
            out.append(char)
            index += 1
    assert depth == 0 and not quoted
    return "".join(out)


def run_lean() -> str:
    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink(), "worker must reuse the automation-provided pinned .lake link"
    lake_target = lake_link.resolve(strict=True)
    lake_target_stat = lake_target.stat()
    mathlib_head = git("rev-parse", "HEAD", cwd=MATHLIB)
    mathlib_status = git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB)
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT
    ).strip()
    lean_bin = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    base_env = os.environ | {
        "LEAN_PATH": lean_path,
        "LC_ALL": "C",
        "LANG": "C",
        "NO_COLOR": "1",
        "TZ": "UTC",
    }
    with tempfile.TemporaryDirectory(prefix="thm-m-0927-proof-") as temporary:
        temp_path = Path(temporary)
        run(
            [lean_bin, "--trust=0", "Statement.lean", "-o", str(temp_path / "Statement.olean")],
            cwd=HERE, env=base_env,
        )
        local_env = base_env | {"LEAN_PATH": temporary + os.pathsep + lean_path}
        run(
            [lean_bin, "--trust=0", "ObligationTree.lean", "-o",
             str(temp_path / "ObligationTree.olean")],
            cwd=HERE, env=local_env,
        )
        output = run([lean_bin, "--trust=0", "Proof.lean"], cwd=HERE, env=local_env)
    assert lake_link.resolve(strict=True) == lake_target
    assert lake_target.stat() == lake_target_stat
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == mathlib_head
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == (
        mathlib_status
    )
    return output


def check_lean_output(output: str) -> None:
    declarations = (
        "Real.coe_fib_eq'",
        "Stage1Instances.THM_M_0927.Proof.functionBinet_proof",
        "Stage1Instances.THM_M_0927.Proof.binetFormula_proof",
    )
    expected_axioms = ["propext", "Classical.choice", "Quot.sound"]
    for declaration in declarations:
        pattern = re.escape(f"'{declaration}' depends on axioms:") + r"\s*\[([^]]*)\]"
        match = re.search(pattern, output)
        assert match is not None, declaration
        axioms = [part.strip() for part in match.group(1).split(",") if part.strip()]
        assert axioms == expected_axioms, (declaration, axioms)
    assert output.count("Declarations are sorry-free!") == len(declarations)
    assert "declaration uses 'sorry'" not in output and "sorryAx" not in output


def main() -> None:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1546
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0927-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["deliverable"] == "Implement or pin/import the required proof bodies without placeholders."
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0927-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    local_dag = load(HERE / "task-dag.json")
    receipt = load(HERE / "proof-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0927.BinetFormulaTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["root_node_id"] == registry["root_obligation_id"] == "M0927-ROOT"
    assert graphs["closure_boundary"]["minimal_open_machine_proof_cut_sets"] == [
        ["M0927-T-FUNCTION-BINET"]
    ]
    composition = graphs["composition_certificates"][0]
    assert composition["declaration"].endswith("root_of_terminal_packages")
    assert composition["required_child_ids"] == PROVISIONAL_IDS[1:]
    plans = graphs["unverified_decomposition_plans"]
    assert [plan["plan_id"] for plan in plans] == UNVERIFIED_PLAN_IDS
    assert all(
        plan["status"] == "source_body_decomposition_unverified_as_child_to_parent_composition"
        for plan in plans
    )
    local_proof = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_proof["state"] == "open" and local_dag["accepted_states"] == []

    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments_and_strings(proof)) is None
    for marker in (
        "import ObligationTree",
        "theorem functionBinet_proof : ObligationTree.FunctionNamedRootPackage",
        "using Real.coe_fib_eq'",
        "theorem binetFormula_proof : BinetFormulaTarget",
        "ObligationTree.root_of_terminal_packages",
        "ObligationTree.rootComposition_checked",
        "ObligationTree.functionToPointwiseTransport_checked",
        "ObligationTree.namedRootToRadicalTransport_checked",
        "assert_no_sorry Real.coe_fib_eq'",
        "#print axioms binetFormula_proof",
    ):
        assert marker in proof, marker

    terminal_source = MATHLIB / "Mathlib/NumberTheory/Real/GoldenRatio.lean"
    terminal_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/NumberTheory/Real/GoldenRatio.olean"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("rev-parse", "HEAD:Mathlib/NumberTheory/Real/GoldenRatio.lean", cwd=MATHLIB) == (
        TERMINAL_BLOB
    )
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert hash_slice(terminal_source, 180, 195) == TERMINAL_BODY_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["phase"] == "proof" and receipt["intent"] == "prove"
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["validator_inputs"]["check_proof_sha256"] == sha256(
        HERE / "check_proof.py"
    )
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["proof_body"]["terminal_body_slice_sha256"] == TERMINAL_BODY_SHA256
    root_evidence = receipt["root_evidence"]
    assert root_evidence["exact_declaration_evidence_ids"] == PROVISIONAL_IDS
    assert root_evidence["internal_per_node_composition_credit"] is False
    assert root_evidence["unverified_decomposition_plan_ids"] == UNVERIFIED_PLAN_IDS
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["remaining_assurance_cut_set"] == REMAINING_ASSURANCE_CUT
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    lean_log_path = os.environ.get("THM_M_0927_LEAN_LOG")
    lean_output = (
        Path(lean_log_path).read_text(encoding="utf-8") if lean_log_path else run_lean()
    )
    check_lean_output(lean_output)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "M0927-T-FUNCTION-BINET" in validation
    assert "provisional `M0-W`" in validation
    assert "theorem_complete=false" in validation
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0927 proof phase: pinned function body and exact root composition checked")
    print("axioms: propext, Classical.choice, Quot.sound; no sorries")
    print("theorem_complete=false; accepted state unchanged")


if __name__ == "__main__":
    main()
