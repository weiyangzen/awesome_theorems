#!/usr/bin/env python3
"""Fail-closed source and evidence checks for S56-M-1007-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1007-PROOF"
THEOREM = "THM-M-1007"
BASE_REVISION = "8f22279fd1216cdfb5676c758e6bdb08e0ba3e01"
BASE_TREE = "d2e9e68da52ecfcfe15a9c48ac2262400e602667"
EXPRESSION_SHA256 = "3b1a82b3fc0ce70be489e8a49279e3f29cfe244f7a50c28f5c4e5de26894cf38"
DENOMINATOR_SHA256 = "0a29c34a938eeb9ddb91009316aabe1be97f16a7606fbc6da3c3aea7429e87cf"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROOF_SHA256 = "6a8f198527b1f8f915e979991a0e89a06b1728a1bf9e191910a6c63660ecb6c5"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/README.md",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-blocker-2026-07-14.json",
    f"Stage1_Instances/{THEOREM}/proof-execution.md",
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


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker-2026-07-14.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 287
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["phase"] == "proof" and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-1007-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)[ \t]+|\bextern[ \t]+",
        re.MULTILINE,
    )
    for path in sorted(HERE.glob("*.lean")):
        source = without_comments(path.read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, path

    proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
    assert sha256(HERE / "Proof.lean") == PROOF_SHA256
    for marker in (
        "theorem memLp_truncate",
        "theorem iIndepSet_largeJump",
        "theorem summable_largeJump_of_seriesConverges",
        "theorem seriesConverges_iff_of_eventuallyEq",
        "theorem iIndepFun_centeredTruncate",
        "theorem variance_centeredTruncate",
        "theorem ae_seriesConverges_centered_of_variance_summable",
        "theorem ae_seriesConverges_truncate_of_mean_variance",
        "theorem threeSeries_sufficiency",
        "theorem obligationTree_sufficiency",
        "#print axioms measurable_centeredTruncationFunction",
        "#print axioms seriesConverges_centered_iff",
        "#print axioms threeSeries_sufficiency",
        "#print axioms obligationTree_sufficiency",
    ):
        assert marker in proof, marker
    assert "KolmogorovThreeSeriesTarget := by" not in proof

    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    boundary = graphs["closure_boundary"]
    assert boundary["closed_obligations"] == [] and boundary["root_closed"] is False
    assert boundary["theorem_complete"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == PROOF_SHA256
    assert receipt["proof_body"]["checked_declaration_count"] == 33
    assert receipt["proof_body"]["total_theorem_lemma_count"] == 33
    assert receipt["proof_body"]["new_theorem_lemma_count"] == 26
    assert len(receipt["exact_declarations"]) == 33
    assert receipt["provisionally_closed_proof_obligation_ids"] == [
        "M1007-T-SUFFICIENCY"
    ]
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["recipe"]["covered_ids"] == [
        "M1007-C-TRUNC-PROPS",
        "M1007-C-EVENT-INDEP",
        "M1007-B-LARGE-JUMP-NEC",
        "M1007-B-LARGE-JUMP-SUFF",
        "M1007-T-EVENTUAL",
        "M1007-N-CENTER",
        "M1007-L-BOUNDED-SUFF",
        "M1007-T-SUFFICIENCY",
    ]
    assert receipt["result"]["root_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["provisional_mathematical_remaining_cut"] == [
        "M1007-L-BOUNDED-NEC"
    ]
    assert receipt["authoritative_graph_open_cut_set_unchanged"] == (
        boundary["remaining_root_cut_set"]
    )
    assert receipt["known_failures"] == packet["known_failures"]

    assert blocker["proof_source_sha256"] == PROOF_SHA256
    assert blocker["checked_declaration_count"] == 33
    assert blocker["outcome"] == "partial_proof_root_blocked"
    assert blocker["root_closed"] is False
    assert blocker["provisionally_closed_proof_obligation_ids"] == [
        "M1007-T-SUFFICIENCY"
    ]
    assert blocker["accepted_closed_obligation_ids"] == []
    assert blocker["provisional_mathematical_remaining_cut"] == (
        receipt["provisional_mathematical_remaining_cut"]
    )
    assert blocker["authoritative_graph_open_cut_set_unchanged"] == (
        boundary["remaining_root_cut_set"]
    )

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]

    status = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=ROOT,
    ).decode("utf-8")
    actual_changes = {
        entry[3:] for entry in status.split("\0") if entry
        if entry[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    for path in [ROOT / path for path in CHANGED_PATHS]:
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1007 proof phase: 33 declarations and evidence are consistent")
    print("exact target sufficiency is proved; bounded-series necessity and root remain open")
    print("theorem_complete=false")


if __name__ == "__main__":
    main()
