#!/usr/bin/env python3
"""Cross-check THM-M-0861 statement metadata, receipt, and worker packet."""

from pathlib import Path
import hashlib
import json
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
OWNED = Path(__file__).parent
STATEMENT = OWNED / "Statement.lean"
METADATA = OWNED / "statement.json"
RECEIPT = OWNED / "statement-receipt.json"
PACKET = ROOT / ".stage1-worker-selftest.json"
ITEM_ID = "S56-M-0861-STATEMENT"
THEOREM_ID = "THM-M-0861"
EXPRESSION_SHA256 = "4e7919ed3b44379a42d69ef88cfb5e512248eccfe755392723cb6769c4f8e197"
EXPECTED_CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0861/Statement.lean",
    "Stage1_Instances/THM-M-0861/check_statement.py",
    "Stage1_Instances/THM-M-0861/check_statement_artifacts.py",
    "Stage1_Instances/THM-M-0861/statement-receipt.json",
    "Stage1_Instances/THM-M-0861/statement-validation.md",
    "Stage1_Instances/THM-M-0861/statement.json",
]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_checker() -> dict:
    result = subprocess.run(
        ["python3", "-B", str(OWNED / "check_statement.py")],
        cwd=ROOT / "Formalizations" / "Lean",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
    )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return json.loads(result.stdout)


def main() -> None:
    metadata = read_json(METADATA)
    receipt = read_json(RECEIPT)
    packet = read_json(PACKET)
    checker = run_checker()

    statement_sha256 = hashlib.sha256(STATEMENT.read_bytes()).hexdigest()
    assert metadata["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM_ID
    assert metadata["theorem_id"] == receipt["theorem_id"] == THEOREM_ID
    assert packet["state"] == receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False
    assert metadata["statement_elaborated"] is True
    assert metadata["theorem_proved"] is False
    assert metadata["audit_complete"] is False
    assert metadata["theorem_complete"] is False
    assert receipt["audit_complete"] is False
    assert receipt["theorem_complete"] is False
    assert checker["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert metadata["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["statement_fingerprints"] == [f"sha256:{EXPRESSION_SHA256}"]
    assert checker["statement_file_sha256"] == statement_sha256
    assert metadata["canonical_formal_target"]["statement_file_sha256"] == statement_sha256
    assert receipt["statement_file_sha256"] == statement_sha256
    assert checker["mathlib_revision"] == receipt["environment"]["mathlib_revision"]
    assert checker["direct_imports"] == metadata["direct_imports"] == receipt["direct_imports"]
    assert set(checker["minimal_import_deletion_failures"]) == set(checker["direct_imports"])
    assert len(set(checker["mutation_expression_sha256"].values())) == 4
    assert packet["base_revision"] == receipt["base_revision"]
    assert packet["changed_paths"] == EXPECTED_CHANGED_PATHS
    assert receipt["changed_paths"] == EXPECTED_CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert not receipt["accepted_receipt_ids"]
    print(
        "statement artifact check: ok "
        f"({THEOREM_ID}; expression {EXPRESSION_SHA256}; provisional M3)"
    )


if __name__ == "__main__":
    main()
