#!/usr/bin/env python3
"""Fail-closed source, receipt, blocker, and worker-packet checks for THM-M-1065."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1065-PROOF"
THEOREM = "THM-M-1065"
BASE_REVISION = "72a35d5f64e32233c0bc77a57e47bd078475ad74"
BASE_TREE = "a80eb91ed5629dee62d031e78bc87b509cf8e6eb"
STATEMENT_EXPRESSION = "b257ceb188a0b84aab11fd389b5df322129c283dbc38f5c226900a4fec5cebd0"
DENOMINATOR_SHA256 = "d5e21a3abc7d96576d5aeba4b8377a8ef8d92136b5ed448f9f28723f00d91ac2"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
RECEIPT = "proof-receipt-2026-07-15-head-72a35d5f-slot53.json"
BLOCKER = "proof-blocker-2026-07-15-head-72a35d5f-slot53.json"
VALIDATION = "proof-validation-2026-07-15-head-72a35d5f-slot53.md"
PARTIAL_PROGRESS_IDS = [
    "M1065-C-SPACE",
    "M1065-L-X-LAWS",
    "M1065-L-X-INDEP",
    "M1065-L-Y-LAWS",
    "M1065-L-Y-INDEP",
    "M1065-L-EVENT-MEAS",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/check_proof_evidence.py",
    f"Stage1_Instances/{THEOREM}/{BLOCKER}",
    f"Stage1_Instances/{THEOREM}/{RECEIPT}",
    f"Stage1_Instances/{THEOREM}/{VALIDATION}",
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
    receipt = load(HERE / RECEIPT)
    blocker = load(HERE / BLOCKER)
    packet = load(ROOT / ".stage1-worker-selftest.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 507
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-1065-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for fragment in (
        "theorem exists_commonIIDSequences",
        "theorem measurableSet_discrepancyEvent",
        "Finset.measurableSet_biUnion",
        "#print axioms exists_commonIIDSequences",
        "#print axioms measurableSet_discrepancyEvent",
    ):
        assert fragment in proof, fragment

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
        STATEMENT_EXPRESSION
    )
    assert registry["root_obligation_id"] == "M1065-ROOT"
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    denominator = registry["frozen_denominators"]
    computed_denominator = hashlib.sha256(
        json.dumps(denominator, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert computed_denominator == DENOMINATOR_SHA256
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    for obligation_id in PARTIAL_PROGRESS_IDS:
        assert by_id[obligation_id]["statement_fingerprint"].startswith(
            "planned:v1:sha256:"
        )
        assert by_id[obligation_id]["terminal_proof_body_id"] is None
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M4"
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=mathlib) == ""

    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is False and receipt["verdict"] == "no_state_change"
    assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["inputs"]["proof_sha256"] == sha256(proof_path)
    assert receipt["inputs"]["check_proof_sh_sha256"] == sha256(HERE / "check_proof.sh")
    assert receipt["supported_obligation_ids"] == []
    assert receipt["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS_IDS
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == [
        "M1065-C-SPACE",
        "M1065-L-BLOCK-COUPLING",
        "M1065-L-MAXIMAL-TAIL",
    ]

    assert blocker["item_id"] == ITEM and blocker["theorem_id"] == THEOREM
    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert blocker["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS_IDS
    assert blocker["provisionally_closed_obligation_ids"] == []
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    validation = (HERE / VALIDATION).read_text(encoding="utf-8")
    assert "zero frozen" in validation and "theorem_complete=false" in validation
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1065 partial proof evidence: two local bodies checked")
    print("closed frozen obligations: none; root remains open M4")
    print("theorem_complete=false; accepted state unchanged")


if __name__ == "__main__":
    main()
