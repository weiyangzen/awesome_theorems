#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, blocker, and worker-packet checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0651-PROOF"
THEOREM = "THM-M-0651"
BASE_REVISION = "48fb6596b1844f4183c411142415d872ff21e842"
BASE_TREE = "eb8dfff0e90b5ce5b11ac2096777060d62874064"
TARGET_EXPRESSION_SHA256 = (
    "789c281a89ba5947476cb2189ae3e216de0eeaa0b5d016549489d8c1553d8c43"
)
DENOMINATOR_SHA256 = (
    "e739a3f3ee963205d34582d0879d767e928e26670f557de0871addcc176f3805"
)
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PARTIAL_IDS = ["M0651-L-ENUM", "M0651-L-DENSE", "M0651-B-ARITY0"]
CUT_SET = ["M0651-L-ENUM", "M0651-L-DENSE", "M0651-L-HENKIN", "M0651-L-OMIT"]
DECLARATIONS = [
    "Stage1Instances.THM_M_0651.ProofLemmas.countable_symbols",
    "Stage1Instances.THM_M_0651.ProofLemmas.countable_finite_arity_syntax",
    "Stage1Instances.THM_M_0651.ProofLemmas.exists_surjective_formula_schedule",
    "Stage1Instances.THM_M_0651.ProofLemmas.countable_avoidance_requirements",
    "Stage1Instances.THM_M_0651.ProofLemmas.zero_arity_formula_requirement_inhabited",
    "Stage1Instances.THM_M_0651.ProofLemmas.zero_arity_tuple_requirement_inhabited",
    "Stage1Instances.THM_M_0651.ProofLemmas.exists_surjective_avoidance_schedule",
    "Stage1Instances.THM_M_0651.ProofLemmas.exists_consistent_avoidance_extension",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/ProofLemmas.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-execution-2026-07-15-slot64.md",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-recheck-2026-07-15-head-48fb6596-slot64.json",
}


def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
    result: dict[str, object] = {}
    for key, value in pairs:
        assert key not in result, f"duplicate JSON key: {key}"
        result[key] = value
    return result


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def strip_comments_and_strings(source: str) -> str:
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


def main() -> None:
    proof_path = HERE / "ProofLemmas.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    recheck = load(HERE / "proof-recheck-2026-07-15-head-48fb6596-slot64.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 697
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0651-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0651-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(strip_comments_and_strings(proof)) is None
    for marker in (
        "theorem exists_surjective_avoidance_schedule",
        "def IsolatesExact",
        "def IsNonprincipalExact",
        "theorem exists_consistent_avoidance_extension",
        "Theory.models_formula_iff_onTheory_models_equivSentence",
        "Theory.models_iff_not_satisfiable",
        "assert_no_sorry exists_consistent_avoidance_extension",
        "#print axioms exists_consistent_avoidance_extension",
    ):
        assert marker in proof, marker

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == TARGET_EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M0651-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M4"
    assert closure["remaining_root_cut_set"] == CUT_SET
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    for obligation_id in PARTIAL_IDS:
        assert by_id[obligation_id]["statement_fingerprint"].startswith("architecture:v1:sha256:")
        assert by_id[obligation_id]["terminal_proof_body_id"] is None

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["canonical_target_expression_sha256"] == TARGET_EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["exact_declarations"] == DECLARATIONS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["supported_obligation_ids"] == []
    assert receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    result = receipt["result"]
    assert result["exit_code"] == 0
    assert result["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert result["partial_declarations_kernel_closed"] is True
    assert result["root_kernel_closed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == CUT_SET

    assert recheck["item_id"] == ITEM and recheck["theorem_id"] == THEOREM
    assert recheck["partial_proof_receipt_id"] == receipt["receipt_id"]
    assert recheck["outcome"] == "partial_proof_self_tested_root_blocked"
    assert recheck["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert recheck["provisionally_closed_obligation_ids"] == []
    assert recheck["root_closed"] is recheck["audit_complete"] is False
    assert recheck["theorem_complete"] is False

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changed = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    execution_text = (HERE / "proof-execution-2026-07-15-slot64.md").read_text()
    assert "zero frozen obligations closed" in execution_text
    assert "theorem_complete=false" in execution_text
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0651 proof phase: eight partial proof bodies and evidence checked")
    print("closed frozen obligations: none; exact root remains open at M4")
    print("theorem_complete=false; accepted state unchanged")


if __name__ == "__main__":
    main()
