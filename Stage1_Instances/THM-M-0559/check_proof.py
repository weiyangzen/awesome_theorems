#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0559 partial proof packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0559-PROOF"
THEOREM = "THM-M-0559"
BASE_REVISION = "00f98378e8c1c63097871ae62aeed895d83b0cb4"
BASE_TREE = "4f2396db6d6d1c2b9948f401079f136dd0ed8f16"
DENOMINATOR = "040c9f0d06a8432b0cf5768d43391f143d820754686514252ce484f53d3446fc"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
IMPLEMENTED = ["M0559-B-EMPTY"]
PARTIAL_PROGRESS = ["M0559-N-COMPONENTS", "M0559-B-EMPTY"]
CUT = ["M0559-N-COMPONENTS", "M0559-T-FORWARD"]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
    f"Stage1_Instances/{THEOREM}/proof-progress.md",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
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
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 607
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0559-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert item["deliverable"] == (
        "Implement or pin/import the required proof bodies without placeholders."
    )

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "theorem joined_of_component_eq",
        "theorem exists_preimage_joined",
        "theorem joined_of_map_joined",
        "theorem components_surjective_iff",
        "theorem components_injective_iff",
        "theorem components_bijective_iff",
        "theorem nonempty_zerothHomotopy_iff",
        "theorem nonempty_iff_of_components_bijective",
        "theorem empty_branch",
        "letI : IsEmpty Y := not_nonempty_iff.mp hy",
        "h.toHomotopyEquiv",
        "#print axioms empty_branch",
        "#print sorries empty_branch",
    ):
        assert marker in proof, marker
    assert "theorem whitehead" not in proof.lower()

    fingerprints = {
        row["obligation_id"]: row["statement_fingerprint"]
        for row in registry["obligations"]
    }
    expected_fingerprint = {
        obligation_id: fingerprints[obligation_id]
        for obligation_id in PARTIAL_PROGRESS
    }
    assert registry["denominator_sha256"] == DENOMINATOR
    assert graphs["registry_denominator_sha256"] == DENOMINATOR
    assert graphs["closure_boundary"]["remaining_root_cut_set"] == CUT
    assert graphs["closure_boundary"]["root_machine_debt"] == "M4"
    assert graphs["closure_boundary"]["theorem_complete"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == blocker["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert receipt["base_revision"] == blocker["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == blocker["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["accepted"] is False
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["provisionally_implemented_obligation_ids"] == IMPLEMENTED
    assert receipt["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS
    assert blocker["provisionally_implemented_obligation_ids"] == IMPLEMENTED
    assert blocker["partial_progress_toward_obligation_ids"] == PARTIAL_PROGRESS
    assert receipt["obligation_statement_fingerprints"] == expected_fingerprint
    assert blocker["obligation_statement_fingerprints"] == expected_fingerprint
    assert receipt["remaining_root_cut_set"] == blocker["remaining_root_cut_set"] == CUT
    assert receipt["result"]["root_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert blocker["root_closed"] is False
    assert blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False
    assert blocker["phase_self_tested"] is True
    assert blocker["new_auxiliary_bodies_added"] is True
    assert blocker["preexisting_body_revalidated"] is True

    recipe = receipt["recipe"]
    assert recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0
    assert recipe["covered_obligation_ids"] == ["M0559-B-EMPTY"]
    assert recipe["partial_coverage_obligation_ids"] == ["M0559-N-COMPONENTS"]
    assert len(recipe["covered_declarations"]) == 9
    assert len(receipt["exact_declarations"]) == 9
    assert receipt["result"]["output_sha256"] == (
        "d336d5ec59027bcf61f6b5aafcc9353b0dcbdbec620d438180ae9a1b2dc19917"
    )
    assert receipt["result"]["output_bytes"] == 1413

    inputs = receipt["inputs"]
    for key, name in (
        ("statement_source_sha256", "Statement.lean"),
        ("obligation_tree_source_sha256", "ObligationTree.lean"),
        ("proof_source_sha256", "Proof.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit-receipt.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert inputs[key] == sha256(HERE / name), key
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert inputs["registry_denominator_sha256"] == DENOMINATOR

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("status", "--short", cwd=mathlib) == ""

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]

    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
    )
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0559 proof packet: B-EMPTY implementation candidate checked")
    print("root remains open M4; component and exact-forward cut preserved")


if __name__ == "__main__":
    main()
