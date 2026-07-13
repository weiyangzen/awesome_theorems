#!/usr/bin/env python3
"""Cross-check the THM-M-0484 statement record, receipt, and worker packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM_ID = "S56-M-0484-STATEMENT"
THEOREM_ID = "THM-M-0484"
BASE_REVISION = "be8701e88e791545c16a262edd1909486d5cef4b"
EXPRESSION_SHA256 = "6bd6024bd44d0bd9c50f6425b9ce5fdaecaf783ac84d32688717d3bde3151aea"
SOURCE_SHA256 = "1baec8791288b46d6df61e060be07aa190ac1d0424229595523a095e8259c8dc"
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0484/README.md",
    "Stage1_Instances/THM-M-0484/Statement.lean",
    "Stage1_Instances/THM-M-0484/check_intake.py",
    "Stage1_Instances/THM-M-0484/check_statement.py",
    "Stage1_Instances/THM-M-0484/check_statement_artifacts.py",
    "Stage1_Instances/THM-M-0484/instance.json",
    "Stage1_Instances/THM-M-0484/scope-map.md",
    "Stage1_Instances/THM-M-0484/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0484/statement-receipt.json",
    "Stage1_Instances/THM-M-0484/statement-validation.md",
    "Stage1_Instances/THM-M-0484/statement.json",
    "Stage1_Instances/THM-M-0484/validation.md",
]
PROHIBITED = (
    "sorry", "admit", "sorryAx", "axiom ", "constant ", "opaque ", "unsafe ",
    "TODO", "FIXME", "placeholder",
)


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(result, dict)
    return result


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    statement = load(HERE / "statement.json")
    receipt = load(HERE / "statement-receipt.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    authority = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in authority["items"] if row["id"] == ITEM_ID)
    assert item["theorem_id"] == THEOREM_ID and item["execution_rank"] == 1365
    assert item["phase"] == "statement" and item["layer"] == 1
    assert item["state"] in {"[ ]", "[_]"} and item["depends_on"] == ["S56-M-0484-INTAKE"]
    local_task = next(row for row in dag["tasks"] if row["id"] == ITEM_ID)
    assert local_task["state"] == "open" and local_task["evidence_ids"] == []

    assert statement["item_id"] == receipt["item_id"] == ITEM_ID
    assert statement["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert statement["lifecycle_mode"] == instance["lifecycle_mode"] == "planned"
    assert statement["statement_elaborated"] is True
    assert statement["theorem_proved"] is statement["audit_complete"] is False
    assert statement["theorem_complete"] is instance["theorem_complete"] is False
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0484.LucasLehmerTestTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == SOURCE_SHA256 == sha256(HERE / "Statement.lean")
    assert formal["direct_imports"] == ["Mathlib.NumberTheory.LucasLehmer"]
    assert instance["canonical_formal_target"]["elaborated_expression_hash"] == (
        f"sha256:{EXPRESSION_SHA256}"
    )

    assert receipt["phase"] == receipt["intent"] == "statement"
    assert receipt["receipt_class"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False and receipt["base_revision"] == BASE_REVISION
    for relative, tagged_digest in receipt["source_inputs"].items():
        integrated = subprocess.check_output(
            ["git", "show", f"{BASE_REVISION}:{relative}"], cwd=ROOT
        )
        assert tagged_digest == f"sha256:{hashlib.sha256(integrated).hexdigest()}", (
            f"integrated statement input hash changed: {relative}"
        )
    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=mathlib, text=True
    ).strip() == receipt["worker_input_hashes"]["mathlib_revision"]
    assert subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, text=True
    ).strip() == receipt["worker_input_hashes"]["mathlib_tree"]
    assert receipt["statement_fingerprints"] == [f"sha256:{EXPRESSION_SHA256}"]
    assert receipt["statement_file_sha256"] == SOURCE_SHA256
    assert receipt["changed_paths"] == CHANGED_PATHS
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R4",
    }
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["proof_body_locations"] == receipt["canonical_obligation_ids"] == []
    assert receipt["typed_graph_changes"] == receipt["composition_certificates"] == []
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["selftest_result"] == "pass"

    successor_files = {
        "AnchorAudit.lean", "anchor-audit.json", "anchor-audit-receipt.json",
        "anchor-audit-validation.md", "check_anchor_audit.py", "check_intake.py",
        "check_statement_artifacts.py",
    }
    actual_changed: set[str] = set()
    status = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all", "--", str(HERE)],
        cwd=ROOT,
        text=True,
    )
    for line in status.splitlines():
        relative = line[3:] if line[:2] == "??" else line[2:].lstrip()
        assert relative.startswith(f"Stage1_Instances/{THEOREM_ID}/")
        if Path(relative).name not in successor_files:
            actual_changed.add(relative)
    assert actual_changed == set()

    lean = (HERE / "Statement.lean").read_text(encoding="utf-8")
    assert all(token not in lean for token in PROHIBITED)
    for path in HERE.iterdir():
        if not path.is_file():
            continue
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    if args.worker_packet is not None:
        packet = load(args.worker_packet.resolve())
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == receipt["base_revision"]
        assert packet["changed_paths"] == receipt["changed_paths"]
        assert packet["commands"] == receipt["worker_packet_commands"]
        assert packet["known_failures"] == receipt["known_failures"]
        assert packet["output_summary"] == receipt["output_summary"]

    print(
        "statement artifact check: ok "
        "(THM-M-0484 exact target; four mutations; pending master acceptance)"
    )


if __name__ == "__main__":
    main()
