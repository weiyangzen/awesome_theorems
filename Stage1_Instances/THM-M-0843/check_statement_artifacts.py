#!/usr/bin/env python3
"""Cross-check THM-M-0843 statement metadata against fresh elaboration."""

from pathlib import Path
import hashlib
import json
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0843-STATEMENT"
EXPRESSION_SHA256 = "3fe13f3562cb642e45e467687508ac44f945e9848ff53d22b9cf068d7ec11219"
SOURCE_SHA256 = "6afd11f23d5245eaa4c487ad4484249b517f6fcf4f99373a2f437d5307aee9ec"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0843/README.md",
    "Stage1_Instances/THM-M-0843/Statement.lean",
    "Stage1_Instances/THM-M-0843/check_statement.py",
    "Stage1_Instances/THM-M-0843/check_statement_artifacts.py",
    "Stage1_Instances/THM-M-0843/scope-map.md",
    "Stage1_Instances/THM-M-0843/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0843/statement-receipt.json",
    "Stage1_Instances/THM-M-0843/statement-validation.md",
    "Stage1_Instances/THM-M-0843/statement.json",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def main() -> None:
    statement = load(HERE / "statement.json")
    receipt = load(HERE / "statement-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    if hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() != SOURCE_SHA256:
        raise SystemExit("Statement.lean hash is stale")
    formal = statement["canonical_formal_target"]
    if formal["elaborated_expression_sha256"] != EXPRESSION_SHA256:
        raise SystemExit("statement expression hash is stale")
    if formal["statement_file_sha256"] != SOURCE_SHA256:
        raise SystemExit("statement source hash is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{EXPRESSION_SHA256}"]:
        raise SystemExit("receipt expression hash is stale")
    if receipt["statement_file_sha256"] != SOURCE_SHA256:
        raise SystemExit("receipt source hash is stale")
    if packet["item_id"] != receipt["item_id"] or packet["item_id"] != ITEM_ID:
        raise SystemExit("worker item identity mismatch")
    if packet["state"] != "[_]" or receipt["proposed_state"] != "[_]":
        raise SystemExit("worker state must remain provisional")
    if receipt["accepted"] or statement["theorem_complete"] or receipt["theorem_complete"]:
        raise SystemExit("statement evidence cannot claim acceptance or theorem completion")
    if set(packet["changed_paths"]) != CHANGED_PATHS:
        raise SystemExit("worker changed_paths mismatch")
    if set(receipt["changed_paths"]) != CHANGED_PATHS:
        raise SystemExit("receipt changed_paths mismatch")

    source_hashes = receipt["source_inputs"]
    for relative in (
        "Docs/Stage1_Targets_rev-5.6.json",
        "Docs/Stage1_Blueprint_rev-5.6.md",
        "Docs/Stage1_Execution_DAG_rev-5.6.json",
        "skills/execute-stage1-rev56/SKILL.md",
    ):
        expected = f"sha256:{hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()}"
        if source_hashes[relative] != expected:
            raise SystemExit(f"receipt source hash is stale: {relative}")

    result = subprocess.run(
        ["python3", str(HERE / "check_statement.py")],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
    )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    payload = json.loads(result.stdout)
    if payload["elaborated_expression_sha256"] != EXPRESSION_SHA256:
        raise SystemExit("fresh elaborated expression disagrees with metadata")
    if payload["statement_file_sha256"] != SOURCE_SHA256:
        raise SystemExit("fresh source hash disagrees with metadata")
    print("statement artifact check: ok (THM-M-0843; provisional; theorem_complete false)")


if __name__ == "__main__":
    main()
