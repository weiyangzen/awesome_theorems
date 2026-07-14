#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, blocker, and packet checks for THM-M-1119."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1119-PROOF"
THEOREM = "THM-M-1119"
BASE_REVISION = "9584b263a758e0dbab59344389554570dcf2e535"
BASE_TREE = "d4ea7039d087ff41783f81c4f1b35c2817dd6a1b"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
STATEMENT_SHA256 = "f020e5b38de3a85f6efa0272c98271c1fe49aa2194e21918342a23b58a4e3b86"
OBLIGATION_TREE_SHA256 = "ff16eff998fa1e9e4403957f9fc834017d1db317ee910dbb099b769b40b46483"
REGISTRY_SHA256 = "a3a097dc5a79e99538d11b337f170307b456b7f1b493e27e6ea857f7c356b42c"
GRAPHS_SHA256 = "34080853d80041ae752080c71879ec715e520ef74ef9dbd4fac4de5b30d49604"
ANCHOR_SHA256 = "500174fb30ba9488e294e616c60a71204d5855781a7cbbc33740cbcab1125723"
PROOF_SHA256 = "f20a21a4783a61350b40e54ad2e45d9660b648d0684009a595077fda7fa0b242"
SCRIPT_SHA256 = "c4ee228090c1de04a1241235a5681596ad75ec98da8923b6793468c4ab37a059"
VALIDATION_SHA256 = "12075d97f18b594a6e001f0f254132637df4de75d6af189b53c407b49da715ed"
BLOCKER_SHA256 = "3881527c43bf1b5d4841f20c190130af17742b927058b1555046c9915d7594c6"
DENOMINATOR_SHA256 = "fa2c6bc00cb54723662b9dd9796c6b2d04a61865670ed8a15560655429ecbb3c"
RECEIPT_ID = "S56-M-1119-PROOF-partial-20260715T063146+0800"
PARTIAL_IDS = ["M1119-S-DEFINITIONS", "M1119-S-BOUNDARY", "M1119-N-MONOTONE"]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-blocker-current.json",
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


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker-current.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 559
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["attempts"] == 0
    assert item["depends_on"] == ["S56-M-1119-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1119-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for fragment in (
        "theorem openGraph_mono",
        "theorem originInInfiniteCluster_mono",
        "theorem measurable_originInInfiniteCluster",
        "theorem one_mem_positiveParameters",
        "theorem criticalProbability_le_one",
        "theorem percolationProbability_zero",
        "theorem zero_not_mem_positiveParameters",
        "#print axioms Stage1Instances.THM_M_1119.criticalProbability_le_one",
        "#print axioms Stage1Instances.THM_M_1119.zero_not_mem_positiveParameters",
    ):
        assert fragment in proof, fragment

    expected_hashes = {
        "Statement.lean": STATEMENT_SHA256,
        "ObligationTree.lean": OBLIGATION_TREE_SHA256,
        "obligation-registry.json": REGISTRY_SHA256,
        "typed-graphs.json": GRAPHS_SHA256,
        "anchor-audit.json": ANCHOR_SHA256,
        "Proof.lean": PROOF_SHA256,
        "check_proof.sh": SCRIPT_SHA256,
        "proof-validation.md": VALIDATION_SHA256,
        "proof-blocker-current.json": BLOCKER_SHA256,
    }
    for name, digest in expected_hashes.items():
        assert sha256(HERE / name) == digest, name

    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M1119-ROOT"
    fingerprints = {row[0]: row[7] for row in registry["obligations"]}
    expected_fingerprints = {key: fingerprints[key] for key in PARTIAL_IDS}

    assert receipt["receipt_id"] == blocker["partial_proof_receipt_id"] == RECEIPT_ID
    assert receipt["item_id"] == blocker["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert receipt["base_revision"] == blocker["base_revision"] == packet["base_revision"]
    assert receipt["base_tree"] == blocker["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert blocker["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert receipt["obligation_statement_fingerprints"] == expected_fingerprints
    assert receipt["supported_obligation_ids"] == []
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert blocker["provisionally_closed_obligation_ids"] == []
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False
    assert blocker["proof_body_added"] is True
    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["proof_body"]["source_sha256"] == PROOF_SHA256
    assert receipt["inputs"]["check_proof_sh_sha256"] == SCRIPT_SHA256
    assert receipt["inputs"]["proof_validation_sha256"] == VALIDATION_SHA256
    assert receipt["inputs"]["proof_blocker_sha256"] == BLOCKER_SHA256

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

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
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1119 partial proof phase: graph, measurability, and endpoints checked")
    print("closed frozen obligations: none; exact Kesten root remains open M4")
    print("theorem_complete=false; accepted state unchanged")


if __name__ == "__main__":
    main()
