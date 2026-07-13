#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0028-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0028-PROOF"
THEOREM = "THM-M-0028"
BASE_REVISION = "7d0965498598e684e3e3d0a01836c2bf36a02959"
BASE_TREE = "753e16a89fce09f051af066f8b58d3e6b2722ade"
EXPRESSION_SHA256 = "89e7e911ed4a5b75c153d824133091ad74ba20a0ecab19bd609b23a54badbee4"
DENOMINATOR_SHA256 = "65d02abdd95b23837143f3a9562ea2ae68a7f0e32f917af40827e25b2aec121b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_SOURCE_SHA256 = "a0e5c5a1aceb564f885573d5c51ec124be20abbd19fabc6af8c798b637530f0b"
MATHLIB_SOURCE_BLOB = "66ddf1f73601e7dbeb04e37b95fcc61e34ee3c14"
CLOSED_IDS = [
    "M0028-ROOT",
    "M0028-T-ROOT-COMPOSE",
    "M0028-B-FG-NOETHERIAN",
    "M0028-B-NOETHERIAN-CHAIN",
    "M0028-X-FG-BODY",
    "M0028-X-CHAIN-BODY",
    "M0028-N-RING-REGULAR",
    "M0028-D-NOETHERIAN-CLASS",
    "M0028-N-CHAIN-IFF",
    "M0028-N-NOETHERIAN-WF",
    "M0028-L-FG-COMPACT",
    "M0028-C-LATTICE-WF",
    "M0028-L-WF-CHAIN",
    "M0028-L-PREORDER-CHAIN",
    "M0028-L-PARTIAL-EQUALITY",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip() == BASE_REVISION
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True
    ).strip() == BASE_TREE

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 1073
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0028-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import ObligationTree",
        "theorem finiteGenerationToNoetherian : FiniteGenerationToNoetherian.{u}",
        "(isNoetherianRing_iff_ideal_fg R).mpr hfg",
        "theorem noetherianToChainStabilization : NoetherianToChainStabilization.{u}",
        "monotone_stabilizes_iff_noetherian.mpr hNoetherian f",
        "theorem idealAscendingChainTheorem_direct : IdealAscendingChainTarget.{u}",
        "theorem idealAscendingChainTheorem_via_frozen_composition",
        "root_of_bridges finiteGenerationToNoetherian noetherianToChainStabilization",
        "#print sorries isNoetherianRing_iff_ideal_fg",
        "#print axioms idealAscendingChainTheorem_via_frozen_composition",
    ):
        assert marker in proof, marker

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["closed_obligation_ids"] == CLOSED_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
    assert receipt["inputs"]["obligation_tree_sha256"] == sha256(HERE / "ObligationTree.lean")
    assert receipt["inputs"]["obligation_registry_sha256"] == sha256(
        HERE / "obligation-registry.json"
    )
    assert receipt["inputs"]["typed_graphs_sha256"] == sha256(HERE / "typed-graphs.json")
    assert receipt["inputs"]["anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
    assert receipt["inputs"]["check_proof_sh_sha256"] == sha256(HERE / "check_proof.sh")
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["theorem_complete"] is False

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0028-ROOT"
    architecture_ids = {
        row["obligation_id"]
        for row in registry["obligations"]
        if row["machine_eligibility"] == "required"
        and not row["obligation_id"].startswith("M0028-S-")
    }
    assert architecture_ids == set(CLOSED_IDS)
    assert receipt["recipe"]["covered_ids"] == CLOSED_IDS

    proof_pairs = {
        (edge["from"], edge["to"])
        for edge in graphs["graphs"]["proof"]["edges"]
        if edge["type"] == "proof_requires"
    }
    assert proof_pairs == {
        ("M0028-ROOT", "M0028-T-ROOT-COMPOSE"),
        ("M0028-T-ROOT-COMPOSE", "M0028-B-FG-NOETHERIAN"),
        ("M0028-T-ROOT-COMPOSE", "M0028-B-NOETHERIAN-CHAIN"),
    }

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    source_rel = Path("Mathlib/RingTheory/Noetherian/Defs.lean")
    source = mathlib / source_rel
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=mathlib, text=True
    ).strip() == MATHLIB_REVISION
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, text=True
    ).strip() == MATHLIB_TREE
    assert subprocess.check_output(
        ["git", "rev-parse", f"HEAD:{source_rel}"], cwd=mathlib, text=True
    ).strip() == MATHLIB_SOURCE_BLOB
    assert not subprocess.check_output(
        ["git", "status", "--porcelain=v1"], cwd=mathlib, text=True
    ).strip()
    assert sha256(source) == MATHLIB_SOURCE_SHA256
    source_lines = source.read_bytes().splitlines(keepends=True)
    terminal_body = b"".join(source_lines[158:162] + source_lines[192:204])
    assert hashlib.sha256(terminal_body).hexdigest() == (
        receipt["proof_body"]["terminal_body_sha256"]
    )
    source_text = source.read_text(encoding="utf-8")
    chain_start = source_text.index("theorem monotone_stabilizes_iff_noetherian")
    chain_end = source_text.index("variable [IsNoetherian R M]")
    fg_start = source_text.index("theorem isNoetherianRing_iff_ideal_fg")
    fg_end = source_text.index("lemma Ideal.fg_of_isNoetherianRing")
    terminals = without_comments(
        source_text[chain_start:chain_end] + source_text[fg_start:fg_end]
    )
    assert prohibited.search(terminals) is None
    for marker in (
        "rw [isNoetherian_iff', wellFoundedGT_iff_monotone_chain_condition]",
        "isNoetherianRing_iff.trans isNoetherian_def",
    ):
        assert marker in terminals, marker

    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not claim theorem completion" in validation
    assert "M0-W" in validation and "M0028-S-FOUNDATION" in validation
    for path in (proof_path, HERE / "check_proof.py", HERE / "check_proof.sh"):
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0028 proof phase: exact pinned M0-W bodies close the frozen machine route")


if __name__ == "__main__":
    main()
