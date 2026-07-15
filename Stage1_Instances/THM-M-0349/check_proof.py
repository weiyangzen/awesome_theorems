#!/usr/bin/env python3
"""Fail-closed source, pin, receipt, blocker, and packet checks for THM-M-0349."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0349-PROOF"
THEOREM = "THM-M-0349"
BASE_REVISION = "3a40b1969f841e07036db5c4d7f03e97c7c57949"
BASE_TREE = "404cccc598c2d4c8831d55138df788f0438ddce8"
TARGET_EXPRESSION_SHA256 = (
    "5f80bebbbf59938add2cb517d6b6219f7a7a22ad8f09586d01e508db2e2ac908"
)
DENOMINATOR_SHA256 = (
    "559befd6c5ac888249539d74acc96e0a274afa52e3b2e0683c05dc010cd3185d"
)
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
SUPPORTED_IDS: list[str] = []
PARTIAL_IDS = ["M0349-C-POLYNOMIAL", "M0349-L-L2"]
CUT_SET = ["M0349-P-EXISTENCE", "M0349-P-BOUND"]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
    f"Stage1_Instances/{THEOREM}/proof-execution.md",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
}


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result: dict[str, object] = {}
    for key, value in pairs:
        assert key not in result, ("duplicate JSON key", key)
        result[key] = value
    return result


def load(path: Path) -> dict:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys
    )
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def strip_lean_comments_and_strings(source: str) -> str:
    """Erase nested block comments, line comments, and string/char contents."""
    out: list[str] = []
    index = 0
    block_depth = 0
    in_string = False
    in_char = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if block_depth:
            if pair == "/-":
                block_depth += 1
                out.extend("  ")
                index += 2
            elif pair == "-/":
                block_depth -= 1
                out.extend("  ")
                index += 2
            else:
                out.append("\n" if char == "\n" else " ")
                index += 1
            continue
        if in_string or in_char:
            out.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif in_string and char == '"':
                in_string = False
            elif in_char and char == "'":
                in_char = False
            index += 1
            continue
        if pair == "/-":
            block_depth = 1
            out.extend("  ")
            index += 2
        elif pair == "--":
            end = source.find("\n", index)
            if end == -1:
                out.extend(" " * (len(source) - index))
                index = len(source)
            else:
                out.extend(" " * (end - index))
                index = end
        elif char == '"':
            in_string = True
            out.append(" ")
            index += 1
        elif char == "'" and index + 2 < len(source) and source[index + 2] == "'":
            in_char = True
            out.append(" ")
            index += 1
        else:
            out.append(char)
            index += 1
    assert block_depth == 0 and not in_string and not in_char
    return "".join(out)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 842
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0349-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0349-OBLIGATION_TREE"
    )
    assert predecessor["state"] == "[_]"

    stripped = strip_lean_comments_and_strings(proof)
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    match = prohibited.search(stripped)
    assert match is None, match.group(0) if match else None
    for fragment in (
        "theorem conjugateMultiplier_memℓp_two",
        "noncomputable def conjugateSequence",
        "theorem norm_conjugateSequence_le",
        "noncomputable def conjugateL2",
        "theorem fourierCoeff_conjugateL2",
        "theorem norm_conjugateL2_le",
        "theorem conjugate_l2_bound",
        "#print axioms conjugate_l2_bound",
    ):
        assert fragment in proof, fragment

    assert instance["canonical_formal_target"]["elaborated_expression_hash"] == (
        f"sha256:{TARGET_EXPRESSION_SHA256}"
    )
    assert registry["root_obligation_id"] == "M0349-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "theorem_complete": False,
        "minimal_open_root_cut": CUT_SET,
    }
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    assert by_id["M0349-L-L2"]["statement_fingerprint"] == (
        "planned:v1:sha256:d3f6b52f65d299c55d4112258fa7d93e3e89ae59017e4aa822975f4f34198af7"
    )
    assert by_id["M0349-C-POLYNOMIAL"]["statement_fingerprint"] == (
        "planned:v1:sha256:68b8b0979b7e8b33ebd0729d9d88130fc60066f5673dbe2a888f12e131f868d1"
    )
    assert by_id["M0349-L-L2"]["terminal_proof_body_id"] is None
    graph_by_id = {row["obligation_id"]: row for row in graphs["nodes"]}
    l2_node = graph_by_id["M0349-L-L2"]
    assert l2_node["formal_target"] == "planned exact L2 estimate"
    assert l2_node["owned_sources"] == [] and l2_node["evidence_ids"] == []

    canonical_lake = (ROOT / "Formalizations/Lean/.lake").resolve()
    mathlib = canonical_lake / "packages/mathlib"
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
    assert receipt["canonical_target_expression_sha256"] == TARGET_EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    assert receipt["supported_obligation_ids"] == SUPPORTED_IDS
    assert receipt["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert receipt["provisionally_closed_obligation_ids"] == SUPPORTED_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("check_proof_py_sha256", "check_proof.py"),
        ("check_proof_sh_sha256", "check_proof.sh"),
        ("proof_execution_sha256", "proof-execution.md"),
        ("proof_blocker_sha256", "proof-blocker.json"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename), key
    assert receipt["inputs"]["lean_toolchain_sha256"] == sha256(
        ROOT / "Formalizations/Lean/lean-toolchain"
    )
    assert receipt["inputs"]["lake_manifest_sha256"] == sha256(
        ROOT / "Formalizations/Lean/lake-manifest.json"
    )
    assert receipt["result"]["axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["remaining_root_cut_set"] == CUT_SET
    assert receipt["recipe"]["covered_obligation_ids"] == []
    assert receipt["recipe"]["candidate_progress_toward_obligation_ids"] == [
        "M0349-L-L2"
    ]
    assert receipt["root_vector_reconciliation"]["selected_by_weaker_status_rule"] == (
        {"H": "H3", "M": "M4", "R": "R4"}
    )

    assert blocker["item_id"] == ITEM and blocker["theorem_id"] == THEOREM
    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert blocker["supported_obligation_ids"] == SUPPORTED_IDS
    assert blocker["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert blocker["provisionally_closed_obligation_ids"] == SUPPORTED_IDS
    assert blocker["accepted_closed_obligation_ids"] == []
    assert blocker["root_closed"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False

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
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    execution_text = (HERE / "proof-execution.md").read_text(encoding="utf-8")
    assert "self-tested progress toward that node" in execution_text
    assert "theorem_complete=false" in execution_text
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0349 proof phase: concrete L2 candidate and evidence checked")
    print("no obligation provisionally closed; accepted state unchanged")
    print("root remains open; theorem_complete=false")


if __name__ == "__main__":
    main()
