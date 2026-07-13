#!/usr/bin/env python3
"""Cross-check THM-M-0890 statement metadata, receipt, and worker packet."""

from pathlib import Path
import hashlib
import json
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0890-STATEMENT"
THEOREM_ID = "THM-M-0890"
BASE_REVISION = "46a0f2a3ea74765a0467c489264b838ffbb70675"
EXPRESSION_SHA256 = "512ebe658ca83b7fb4bb3d3565122d065e3bc6e589898b4f3cf74ab2e12ea54d"
STATEMENT_SOURCE_SHA256 = "beb6cbe0437f78f26188cc3ed1ebe82bed84d2a07f1f8ea1abd78468740a787f"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0890/README.md",
    "Stage1_Instances/THM-M-0890/Statement.lean",
    "Stage1_Instances/THM-M-0890/check_statement.py",
    "Stage1_Instances/THM-M-0890/check_statement_artifacts.py",
    "Stage1_Instances/THM-M-0890/instance.json",
    "Stage1_Instances/THM-M-0890/scope-map.md",
    "Stage1_Instances/THM-M-0890/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0890/statement-receipt.json",
    "Stage1_Instances/THM-M-0890/statement-validation.md",
    "Stage1_Instances/THM-M-0890/statement.json",
    "Stage1_Instances/THM-M-0890/task-dag.json",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    statement = load(HERE / "statement.json")
    receipt = load(HERE / "statement-receipt.json")
    instance = load(HERE / "instance.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    if digest(HERE / "Statement.lean") != STATEMENT_SOURCE_SHA256:
        raise SystemExit("Statement.lean hash is stale")
    formal = statement["canonical_formal_target"]
    if formal["elaborated_expression_sha256"] != EXPRESSION_SHA256:
        raise SystemExit("statement expression hash is stale")
    if formal["statement_file_sha256"] != STATEMENT_SOURCE_SHA256:
        raise SystemExit("statement source hash is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{EXPRESSION_SHA256}"]:
        raise SystemExit("receipt expression hash is stale")
    if receipt["statement_file_sha256"] != STATEMENT_SOURCE_SHA256:
        raise SystemExit("receipt source hash is stale")
    if packet["item_id"] != receipt["item_id"] or packet["item_id"] != ITEM_ID:
        raise SystemExit("worker item identity mismatch")
    if receipt["theorem_id"] != statement["theorem_id"] or receipt["theorem_id"] != THEOREM_ID:
        raise SystemExit("theorem identity mismatch")
    if packet["state"] != "[_]" or receipt["proposed_state"] != "[_]":
        raise SystemExit("worker state must remain provisional")
    if packet["base_revision"] != receipt["base_revision"] or packet["base_revision"] != BASE_REVISION:
        raise SystemExit("base revision mismatch")
    if receipt["accepted"] or statement["theorem_complete"] or receipt["theorem_complete"]:
        raise SystemExit("statement evidence cannot claim acceptance or theorem completion")
    if set(packet["changed_paths"]) != CHANGED_PATHS:
        raise SystemExit("worker changed_paths mismatch")
    if set(receipt["changed_paths"]) != CHANGED_PATHS:
        raise SystemExit("receipt changed_paths mismatch")
    if packet["known_failures"] != receipt["known_failures"]:
        raise SystemExit("worker and receipt known_failures mismatch")
    if instance["root_vector"] != {"H": "H1", "M": "M3", "R": "R4"}:
        raise SystemExit("instance vector does not reflect statement-only M3")
    if instance["canonical_statement"] != statement["canonical_statement"]:
        raise SystemExit("instance and statement canonical claims disagree")

    for relative, tagged in receipt["source_inputs"].items():
        expected = f"sha256:{digest(ROOT / relative)}"
        if tagged != expected:
            raise SystemExit(f"receipt source hash is stale: {relative}")
    for relative, tagged in receipt["changed_artifact_hashes"].items():
        if relative == ".stage1-worker-selftest.json" or relative.endswith("statement-receipt.json"):
            continue
        expected = f"sha256:{digest(ROOT / relative)}"
        if tagged != expected:
            raise SystemExit(f"receipt changed-artifact hash is stale: {relative}")

    result = subprocess.run(
        ["python3", str(HERE / "check_statement.py")],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=240,
    )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    payload = json.loads(result.stdout)
    if payload["elaborated_expression_sha256"] != EXPRESSION_SHA256:
        raise SystemExit("fresh elaborated expression disagrees with metadata")
    if payload["statement_file_sha256"] != STATEMENT_SOURCE_SHA256:
        raise SystemExit("fresh statement source disagrees with metadata")
    if payload["killed_mutations"] != [
        "mutationRemovedPositiveDegree",
        "mutationRationalSpectralDomain",
        "mutationExistentialGraphScope",
        "mutationDegreeAtLeastTwo",
    ]:
        raise SystemExit("mutation inventory mismatch")

    print("statement artifact check: ok (THM-M-0890; provisional M3; theorem_complete false)")


if __name__ == "__main__":
    main()
