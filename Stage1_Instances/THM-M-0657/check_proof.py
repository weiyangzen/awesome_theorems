#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, and claim checks for THM-M-0657 proof."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0657-PROOF"
THEOREM = "THM-M-0657"
BASE_REVISION = "be35cd8f5123e9d06247b12859f3843bdd90c66f"
BASE_TREE = "a275a21a449fbcbd6c2333f5cfe737e906b20db6"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
DENOMINATOR_SHA256 = (
    "22647d29b16c9d77f04719fe51238e427dab88b5fd6c57dfab8ac599c627ce44"
)
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
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 702
    assert item["phase"] == "proof" and item["layer"] == 4
    assert item["depends_on"] == ["S56-M-0657-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["state"] == "[ ]"
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b|"
        r"\b(?:implemented_by|native_decide|run_tac)\b",
        re.MULTILINE,
    )
    without_comments = re.sub(r"/-.*?-/", "", proof, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    assert prohibited.search(without_comments) is None
    for marker in (
        "theorem hasModelCardinality_of_uncountably_categorical",
        "theorem infinitePart_categorical",
        "theorem infinitePart_isComplete",
        "(T ∪ L.infiniteTheory).IsComplete",
        "theorem categoricalWithExistence_of_categorical",
        "def UncountableCategoricityTransfer : Prop",
        "theorem morleyCategoricityTarget_of_categoricalTransfer",
        "(huniq : UncountableCategoricityTransfer.{u, v, w})",
        "assert_no_sorry infinitePart_isComplete",
        "#print axioms morleyCategoricityTarget_of_categoricalTransfer",
    ):
        assert marker in proof, marker
    assert "theorem morleyCategoricityTarget :" not in proof

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"]["root_closed"] is False
    assert graphs["closure_boundary"]["root_machine_classification"] == "M3"

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["provisionally_closed_obligation_ids"] == [
        "M0657-L-COMPLETENESS",
        "M0657-C-EXISTENCE",
    ]
    assert receipt["accepted_closed_obligation_ids"] == []
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    for binding in receipt["obligation_bindings"]:
        row = by_id[binding["obligation_id"]]
        assert binding["registry_statement_fingerprint"] == row["statement_fingerprint"]
        assert binding["acceptance_state"] == (
            "provisional_worker_selftest_pending_master_reconciliation"
        )
    assert {row["obligation_id"] for row in receipt["obligation_bindings"]} == {
        "M0657-L-COMPLETENESS",
        "M0657-C-EXISTENCE",
    }
    assert len(receipt["exact_declarations"]) == 5
    assert receipt["result"]["root_closed"] is False
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["inputs"]["lean_toolchain_sha256"] == sha256(
        ROOT / "Formalizations/Lean/lean-toolchain"
    )
    assert receipt["inputs"]["lake_manifest_sha256"] == sha256(
        ROOT / "Formalizations/Lean/lake-manifest.json"
    )

    assert blocker["outcome"] == "partial_proof_progress_root_blocked"
    assert blocker["proof_body_added"] is True
    assert blocker["provisionally_closed_obligation_ids"] == (
        receipt["provisionally_closed_obligation_ids"]
    )
    assert blocker["accepted_closed_obligation_ids"] == []
    assert blocker["first_failed_gate"].startswith("M0657-C-MORLEY-RANK")
    assert blocker["root_closed"] is blocker["theorem_complete"] is False

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
    )
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0657 partial proof: two frozen obligations checked")
    print("provisional closure: M0657-L-COMPLETENESS, M0657-C-EXISTENCE")
    print("accepted closure: none; root open M3; theorem_complete=false")


if __name__ == "__main__":
    main()
