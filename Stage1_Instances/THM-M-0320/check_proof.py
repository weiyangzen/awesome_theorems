#!/usr/bin/env python3
"""Fail-closed source and provenance checks for S56-M-0320-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0320-PROOF"
THEOREM = "THM-M-0320"
BASE = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
ROOT_DECL = "Stage1Instances.THM_M_0320.kakutaniFixedPoint"
ALLOWED = {"propext", "choice", "Quot.sound"}


def load(path: Path) -> dict:
    def unique(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, (path, "duplicate key", key)
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_lean(source: str) -> str:
    out: list[str] = []
    i = 0
    depth = 0
    string = False
    escaped = False
    while i < len(source):
        pair = source[i:i + 2]
        ch = source[i]
        if depth:
            if pair == "/-":
                depth += 1
                out.extend("  ")
                i += 2
            elif pair == "-/":
                depth -= 1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if ch == "\n" else " ")
                i += 1
        elif string:
            out.append("\n" if ch == "\n" else " ")
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                string = False
            i += 1
        elif pair == "/-":
            depth = 1
            out.extend("  ")
            i += 2
        elif pair == "--":
            end = source.find("\n", i)
            if end < 0:
                out.extend(" " * (len(source) - i))
                i = len(source)
            else:
                out.extend(" " * (end - i))
                i = end
        elif ch == '"':
            string = True
            out.append(" ")
            i += 1
        else:
            out.append(ch)
            i += 1
    assert depth == 0 and not string
    return "".join(out)


assert subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
).strip() == BASE

execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item["theorem_id"] == THEOREM
assert item["phase"] == "proof" and item["layer"] == 4
assert item["state"] == "[ ]"
assert item["depends_on"] == ["S56-M-0320-OBLIGATION_TREE"]
assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

source = load(HERE / "brouwer-source.json")
assert source["item_id"] == ITEM and source["theorem_id"] == THEOREM
assert source["source_module"] == "Gametheory.Brouwer"
assert source["source_declaration"] == "Brouwer"
for relative, expected in source["source_path_sha256"].items():
    assert sha256(ROOT / relative) == expected, relative
license_path = ROOT / source["upstream"]["license_path"]
assert sha256(license_path) == source["upstream"]["license_sha256"]
assert source["upstream"]["license"] == "MIT"

proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
graph = (HERE / "GraphBridgeProof.lean").read_text(encoding="utf-8")
clean = strip_lean(proof + "\n" + graph)
for pattern in (
    r"\bsorry\b",
    r"\badmit\b",
    r"\bsorryAx\b",
    r"(^|\n)\s*(axiom|constant|opaque)\s+",
    r"(^|\n)\s*unsafe\s+",
    r"\bimplemented_by\b",
    r"\bnative_decide\b",
    r"\brun_tac\b",
):
    assert re.search(pattern, clean, re.MULTILINE) is None, pattern

assert "theorem closedGraphKakutaniCore : ClosedGraphKakutaniCore := by" in proof
assert "theorem kakutaniFixedPoint : KakutaniFixedPointTarget :=" in proof
assert "root_of_closedGraph_packages closedGraphKakutaniCore" in proof
assert "upperHemicontinuityClosedGraphBridge" in proof
assert "assert_no_sorry Brouwer" in proof
assert "assert_no_sorry closedGraphKakutaniCore" in proof
assert "assert_no_sorry kakutaniFixedPoint" in proof
assert ROOT_DECL.rsplit(".", 1)[1] in proof

receipt = load(HERE / "proof-receipt.json")
assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
assert receipt["base_revision"] == BASE
assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
assert receipt["canonical_declaration"] == ROOT_DECL
assert set(receipt["kernel_axioms"]) == ALLOWED
assert receipt["theorem_complete"] is False
assert receipt["accepted_receipt_ids"] == []
assert receipt["proof_source_sha256"] == sha256(HERE / "Proof.lean")
assert receipt["brouwer_source_sha256"] == sha256(HERE / "brouwer-source.json")
assert receipt["changed_paths"] == [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0320/BrouwerSource.lean",
    "Stage1_Instances/THM-M-0320/Proof.lean",
    "Stage1_Instances/THM-M-0320/brouwer-source.json",
    "Stage1_Instances/THM-M-0320/check_proof.py",
    "Stage1_Instances/THM-M-0320/check_proof.sh",
    "Stage1_Instances/THM-M-0320/proof-receipt.json",
    "Stage1_Instances/THM-M-0320/proof-validation-2026-07-15-slot69.md",
]

packet = load(ROOT / ".stage1-worker-selftest.json")
assert packet["item_id"] == ITEM and packet["state"] == "[_]"
assert packet["base_revision"] == BASE
assert packet["known_failures"]
assert set(packet["changed_paths"]) == set(receipt["changed_paths"])

status = subprocess.check_output(
    ["git", "status", "--short", "--untracked-files=all"],
    cwd=ROOT,
    text=True,
).splitlines()
actual_changed: set[str] = set()
for line in status:
    path = line[3:]
    if path == "Formalizations/Lean/.lake":
        continue
    if path == ".stage1-worker-selftest.json" or path.startswith(
        f"Stage1_Instances/{THEOREM}/"
    ):
        actual_changed.add(path)
    else:
        raise AssertionError(("unexpected changed path", line))
assert actual_changed == set(receipt["changed_paths"]), (
    actual_changed,
    receipt["changed_paths"],
)

print("PASS S56-M-0320-PROOF source, provenance, receipt, and packet invariants")
