#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, blocker, and packet checks for THM-M-1070."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-1070-PROOF"
THEOREM = "THM-M-1070"
BASE_REVISION = "111bbeb1a210ae4e8525a4342012921ab60e466f"
BASE_TREE = "8f705aa79622bf1e9be0665ae1254313df21b4f6"
TARGET_EXPRESSION = "8e1440de837395201d12a0f2085afe0c03d2504e99240b68154595fc2f8cffc1"
DENOMINATOR = "c5866f4be491aa8209171938c78c36bde996941a27c87686d2a109d6679c5aa9"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PARTIAL_IDS = [
    "M1070-L-PROBABILITY",
    "M1070-L-MEASURABLE",
    "M1070-L-ZERO",
    "M1070-L-INDEPENDENT",
    "M1070-L-STATIONARY",
    "M1070-L-STOCH-CONT",
]
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
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 512
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-1070-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-1070-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for fragment in (
        "theorem isLevyProcess_of_clauses",
        "theorem clauses_of_isLevyProcess",
        "theorem isLevyProcess_zero",
        "theorem zeroMeasure_not_isLevyProcess",
        "iIndepFun_const P hP",
        "#print axioms isLevyProcess_zero",
        "#print axioms zeroMeasure_not_isLevyProcess",
    ):
        assert fragment in proof, fragment

    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    assert registry["root_obligation_id"] == "M1070-ROOT"
    assert by_id["M1070-ROOT"]["statement_fingerprint"] == (
        f"lean-expression-sha256:{TARGET_EXPRESSION}"
    )
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR
    for obligation_id in PARTIAL_IDS:
        assert by_id[obligation_id]["statement_fingerprint"].startswith("planned:v1:sha256:")
        assert by_id[obligation_id]["terminal_proof_body_id"] is None
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["root_machine_debt"] == "M3"
    assert closure["remaining_root_cut_set"] == [
        "M1070-L-INDEPENDENT",
        "M1070-L-STATIONARY",
        "M1070-L-STOCH-CONT",
    ]

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
    assert receipt["canonical_target_expression_sha256"] == TARGET_EXPRESSION
    assert receipt["registry_denominator_sha256"] == DENOMINATOR
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
        ("check_proof_sh_sha256", "check_proof.sh"),
        ("proof_validation_sha256", "proof-validation.md"),
        ("proof_blocker_sha256", "proof-blocker.json"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == closure["remaining_root_cut_set"]

    assert blocker["item_id"] == ITEM and blocker["theorem_id"] == THEOREM
    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert blocker["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert blocker["provisionally_closed_obligation_ids"] == []
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is blocker["proof_phase_complete"] is False

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "zero frozen obligations are provisionally or accepted closed" in validation
    assert "theorem completion is" not in validation.lower()
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-1070 partial proof phase: zero-process body and countermodel checked")
    print("closed frozen obligations: none; root remains open M3")
    print("theorem_complete=false; accepted state unchanged")


if __name__ == "__main__":
    main()
