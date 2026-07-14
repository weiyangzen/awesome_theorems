#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, and claim checks for THM-M-1271 proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1271-PROOF"
THEOREM = "THM-M-1271"
BASE_REVISION = "799262a53af4c03d919b758421e149ffc158d472"
BASE_TREE = "c95932dffb536335b0a3f5c962f13966e755cbde"
TARGET_EXPRESSION = "686a7f777a77c3f91504e4c48cd3d0fab19ef802ce3df1751dc4288e62592d7b"
REGISTRY_DENOMINATOR = "2f6d1a3dc9064aff967ba0cf8443ff438e9cb99e0b2d34994252e6410d2d75bc"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
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


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 164
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["depends_on"] == ["S56-M-1271-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["state"] == "[ ]"
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    without_comments = re.sub(r"/-.*?-/", "", proof, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    assert prohibited.search(without_comments) is None
    for fragment in (
        "theorem pathHeight_attained",
        "isCompact_Icc.exists_sSup_image_eq",
        "theorem exists_valueSequence_at_mountainPassLevel",
        "exists_seq_tendsto_sInf hheights hbdd",
        "pathHeight_attained hC1",
        "theorem mountainPassCriticalPackage_of_psSequence",
        "(produce :",
        "#print axioms pathHeight_attained",
        "#print axioms exists_valueSequence_at_mountainPassLevel",
    ):
        assert fragment in proof, fragment

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == TARGET_EXPRESSION
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR
    assert graphs["registry_denominator_sha256"] == REGISTRY_DENOMINATOR
    assert graphs["closure_boundary"]["root_closed"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["canonical_target_expression_sha256"] == TARGET_EXPRESSION
    assert receipt["registry_denominator_sha256"] == REGISTRY_DENOMINATOR
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), filename
    assert receipt["closed_obligation_ids"] == ["M1271-C-PATH-MAX"]
    assert receipt["partial_progress"] == {
        "obligation_id": "M1271-C-PS-SEQUENCE",
        "obligation_closed": False,
        "checked_component": "functional_value_convergence_only",
    }
    assert receipt["result"]["root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False

    assert blocker["outcome"] == "partial_proof_progress_root_blocked"
    assert blocker["proof_body_added"] is True
    assert blocker["closed_obligation_ids"] == ["M1271-C-PATH-MAX"]
    assert blocker["first_failed_gate"].startswith("M1271-C-PS-SEQUENCE")
    assert blocker["root_closed"] is blocker["theorem_complete"] is False
    assert blocker["remaining_root_cut_set"] == [
        "M1271-C-PS-SEQUENCE", "M1271-T-CRITICAL", "M1271-ROOT"
    ]

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
    actual = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1271 partial proof: path-height attainment checked")
    print("closed frozen obligation: M1271-C-PATH-MAX (provisional)")
    print("root closure: open (M2); theorem_complete=false")


if __name__ == "__main__":
    main()
