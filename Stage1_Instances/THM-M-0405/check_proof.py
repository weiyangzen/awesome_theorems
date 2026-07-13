#!/usr/bin/env python3
"""Fail-closed source and evidence checks for S56-M-0405-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0405-PROOF"
THEOREM = "THM-M-0405"
BASE_REVISION = "4683af33601abf1185b47caafb86ccd3ddc30158"
BASE_TREE = "9b49ee18fec214315592ea125d7049e4ea668740"
DENOMINATOR_SHA256 = "cd9daee4b82734d1e98e216a6371bd83f3fcff1a181e79381773133a6b9da793"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
PARTIAL_PROGRESS_IDS = [
    "M0405-N-PAIR-NORMALIZATION",
    "M0405-T-LUCAS-ADAPTER",
    "M0405-T-LEHMER-ADAPTER",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
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
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 18
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0405-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "theorem ne_of_ratioNotRootOfUnity",
        "theorem coe_discriminant (L : LucasPair)",
        "theorem term_zero (L : LucasPair)",
        "theorem term_one (L : LucasPair)",
        "theorem sq_sub_sq_ne_zero (L : LehmerPair)",
        "theorem coe_squaredEvenDenominator (L : LehmerPair)",
        "theorem term_one (L : LehmerPair)",
        "theorem term_two (L : LehmerPair)",
        "#print axioms LehmerPair.term_two",
        "M0405_PROOF_AXIOM_AUDIT_END",
    ):
        assert marker in proof, marker
    assert "theorem proof : Statement" not in proof

    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["status_observed_after_freeze"] == {
        "closed_obligations": [],
        "root_machine_debt": "M4",
    }
    closure = graphs["closure_boundary"]
    assert closure["root_machine_debt"] == "M4"
    assert closure["closed_obligations"] == []
    assert closure["minimal_open_root_cut_set"] == ["M0405-X-BHV-BRIDGE"]
    assert closure["theorem_complete"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "no_state_change"
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["supported_obligation_ids"] == []
    assert receipt["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS_IDS
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
        ("proof_validation_sha256", "proof-validation.md"),
        ("proof_blocker_sha256", "proof-blocker.json"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == ["M0405-X-BHV-BRIDGE"]

    assert blocker["proof_body_added"] is True
    assert blocker["partial_proof_receipt_id"] == receipt["receipt_id"]
    assert blocker["supported_obligation_ids"] == []
    assert blocker["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS_IDS
    assert blocker["root_closed"] is False and blocker["theorem_complete"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    if selftest_path.exists():
        packet = load(selftest_path)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]
        status = subprocess.check_output(
            ["git", "status", "--short", "--untracked-files=all"],
            cwd=ROOT,
            text=True,
        )
        actual_changes = {
            line[3:] for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "zero frozen obligations are claimed closed" in validation
    assert "not theorem completion" in validation
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0405 proof evidence: hashes, pin, scope, and open-root boundary agree")


if __name__ == "__main__":
    main()
