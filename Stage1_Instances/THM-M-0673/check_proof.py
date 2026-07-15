#!/usr/bin/env python3
"""Fail-closed source, pin, graph, receipt, and handoff checks for THM-M-0673."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations/Lean"
MATHLIB = LEAN_ROOT / ".lake/packages/mathlib"
ITEM = "S56-M-0673-PROOF"
THEOREM = "THM-M-0673"
BASE_REVISION = "310be814cb307a91263e232acf691a6b3eded70e"
BASE_TREE = "947289604e1bf9c317b6dc3dd174d3f8fb54ba0e"
TARGET_EXPRESSION = "3b541698da0e2b40d0cef5ea0f03ebd62538d330293e4e393ce053e000906cba"
DENOMINATOR = "4266ee40d8be778685c48d8781aab55dd6d57301e7d9ded13523ea4353c58fe6"
REGISTRY_SEMANTIC = "aefa3236248ea7500e3dd48e01e953f978f8425c78ac11103364ce9cabce3e77"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_SOURCE = "ba32a045647e55dee5bc5b4534ede125eb6cc7bef523aec77dea5e980dfacd54"
MATHLIB_BLOB = "8c436697c7c071261251d3369b70e3882d46673a"
MATHLIB_OLEAN = "1ee005283e38f3d6a64eb931f3452702a4a9ba33e2fc850ef48cf665008e2865"
MATHLIB_LICENSE = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"

OBSERVED_IDS = [
    "M0673-ROOT",
    "M0673-T-ADAPTER",
    "M0673-A-SENTENCE",
    "M0673-A-FORMULA",
    "M0673-A-BOUNDED",
]
SOURCE_MAPPED_IDS = [
    "M0673-B-FALSUM",
    "M0673-B-EQUALITY",
    "M0673-B-RELATION",
    "M0673-B-IMPLICATION",
    "M0673-B-UNIVERSAL",
    "M0673-T-TERM",
    "M0673-C-PRESTRUCTURE",
    "M0673-L-FUNMAP",
    "M0673-L-QUOT-EQ",
    "M0673-L-QUOT-REL",
    "M0673-L-ULTRAFILTER-IMP",
    "M0673-L-QUOT-FORALL",
    "M0673-T-SNOC",
    "M0673-C-EPSILON",
    "M0673-L-EVENTUAL-SET",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def strip_comments_and_strings(source: str) -> str:
    output: list[str] = []
    depth = 0
    index = 0
    while index < len(source):
        if source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            index += 1
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        elif source[index] == '"':
            output.append('""')
            index += 1
            while index < len(source):
                if source[index] == "\\":
                    index += 2
                elif source[index] == '"':
                    index += 1
                    break
                else:
                    index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0
    return "".join(output)


def actual_changed_paths() -> set[str]:
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
    )
    return {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }


def main() -> None:
    receipt = load(HERE / "proof-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    instance = load(HERE / "instance.json")
    local_tasks = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 717,
        "phase": "proof",
        "layer": 4,
        "state": "[ ]",
        "depends_on": ["S56-M-0673-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0673-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"
    assert next(row for row in local_tasks["tasks"] if row["id"] == ITEM)["state"] == "open"
    assert local_tasks["accepted_states"] == []

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == TARGET_EXPRESSION
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR
    assert registry["registry_sha256"] == graphs["registry_sha256"] == REGISTRY_SEMANTIC
    required_machine = registry["frozen_denominators"]["required_machine"]
    assert required_machine == OBSERVED_IDS + SOURCE_MAPPED_IDS
    assert graphs["closure_boundary"]["accepted_closed_obligations"] == []
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["root_machine_debt"] == "M3"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(strip_comments_and_strings(proof)) is None
    for marker in (
        "import ObligationTree",
        "theorem boundedFormulaRealize_pinned",
        "FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast",
        "theorem formulaRealize_via_frozen",
        "formula_of_bounded boundedFormulaRealize_pinned",
        "theorem sentenceRealize_via_frozen",
        "sentence_of_formula formulaRealize_via_frozen",
        "theorem terminalRoot_via_frozen",
        "terminal_of_sentence sentenceRealize_via_frozen",
        "theorem losSentence_via_frozen",
        "root_of_terminal terminalRoot_via_frozen",
        "theorem losSentence_pinned",
        "FirstOrder.Language.Ultraproduct.sentence_realize phi",
        "assert_no_sorry boundedFormulaRealize_pinned",
        "#print axioms losSentence_via_frozen",
        "NameSet.transitivelyUsedConstants",
        "PROOF_CLOSURE bodyless_nonaxioms=",
        "PROOF_CLOSURE unsafe=",
    ):
        assert marker in proof, marker

    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    source = MATHLIB / "Mathlib/ModelTheory/Ultraproducts.lean"
    assert git("rev-parse", "HEAD:Mathlib/ModelTheory/Ultraproducts.lean", cwd=MATHLIB) == MATHLIB_BLOB
    assert sha256(source) == MATHLIB_SOURCE
    lines = source.read_bytes().splitlines(keepends=True)
    assert sha256_bytes(b"".join(lines[93:144])) == receipt["proof_body"]["bounded_terminal_body_sha256"]
    assert sha256_bytes(b"".join(lines[151:158])) == receipt["proof_body"]["sentence_terminal_body_sha256"]
    olean = MATHLIB / ".lake/build/lib/lean/Mathlib/ModelTheory/Ultraproducts.olean"
    assert sha256(olean) == MATHLIB_OLEAN and olean.stat().st_size == 50344
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE
    assert sha256(LEAN_ROOT / "lake-manifest.json") == "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
    assert sha256(LEAN_ROOT / "lean-toolchain") == "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target"]["expression_sha256"] == TARGET_EXPRESSION
    assert receipt["registry_denominator_sha256"] == DENOMINATOR
    assert receipt["registry_sha256"] == REGISTRY_SEMANTIC
    assert receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
    assert receipt["inputs"]["check_proof_py_sha256"] == sha256(Path(__file__))
    assert receipt["inputs"]["check_proof_sh_sha256"] == sha256(HERE / "check_proof.sh")
    assert receipt["inputs"]["proof_validation_sha256"] == sha256(HERE / "proof-validation.md")
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("obligation_tree_receipt_sha256", "obligation-tree-receipt.json"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["kernel_inhabited_obligation_ids_observed"] == OBSERVED_IDS
    assert receipt["source_mapped_not_individually_closed_ids"] == SOURCE_MAPPED_IDS
    assert receipt["closed_obligation_ids_proposed"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["validation_action"]["axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["validation_action"]["transitive_declaration_closure_count"] == 5088
    assert receipt["validation_action"]["transitive_module_count"] == 192
    assert receipt["validation_action"]["transitive_bodyless_nonaxioms"] == []
    assert receipt["validation_action"]["transitive_unsafe_declarations"] == []
    result = receipt["result"]
    assert result["root_kernel_inhabitant_observed"] is True
    assert result["exact_root_frozen_composition_observed"] is True
    assert result["accepted_root_closed"] is result["accepted_state_changed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    actual = actual_changed_paths()
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == actual == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["commands"]
    for relative in actual:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, relative
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), relative

    print("PASS THM-M-0673 proof phase: exact pinned root and frozen composition checked")
    print(f"proof sha256: {sha256(HERE / 'Proof.lean')}")
    print("provisional proof state only; accepted H1/M3/R4 and theorem_complete remain unchanged")


if __name__ == "__main__":
    main()
