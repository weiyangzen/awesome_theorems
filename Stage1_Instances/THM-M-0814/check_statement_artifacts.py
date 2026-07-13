#!/usr/bin/env python3
"""Cross-check THM-M-0814 statement metadata against fresh elaboration."""

from pathlib import Path
import hashlib
import json
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0814-STATEMENT"
THEOREM_ID = "THM-M-0814"
EXPRESSION_SHA256 = "f9fc7813f437ebcd4b2b7327373dd76134d651c1624d2a06f689e84ec571a21e"
BUNDLE_SHA256 = "c51536f6da5240e392e1b0b52d040f3c678cdbd84f275c9531dece910b2dbbeb"
SOURCE_SHA256 = "e2493ef46f9bdd5c8d0b30069efaf27b7ad0f69781d4c4c7317b94a63a06755b"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0814/README.md",
    "Stage1_Instances/THM-M-0814/Statement.lean",
    "Stage1_Instances/THM-M-0814/check_intake.py",
    "Stage1_Instances/THM-M-0814/check_statement.py",
    "Stage1_Instances/THM-M-0814/check_statement_artifacts.py",
    "Stage1_Instances/THM-M-0814/instance.json",
    "Stage1_Instances/THM-M-0814/intake-receipt.json",
    "Stage1_Instances/THM-M-0814/scope-map.md",
    "Stage1_Instances/THM-M-0814/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0814/statement-receipt.json",
    "Stage1_Instances/THM-M-0814/statement-validation.md",
    "Stage1_Instances/THM-M-0814/statement.json",
    "Stage1_Instances/THM-M-0814/task-dag.json",
    "Stage1_Instances/THM-M-0814/validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def main() -> None:
    statement = load(HERE / "statement.json")
    receipt = load(HERE / "statement-receipt.json")
    instance = load(HERE / "instance.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    if hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest() != SOURCE_SHA256:
        raise SystemExit("Statement.lean hash is stale")
    formal = statement["canonical_formal_target"]
    if formal["elaborated_expression_sha256"] != EXPRESSION_SHA256:
        raise SystemExit("statement expression hash is stale")
    if formal["statement_bundle_sha256"] != BUNDLE_SHA256:
        raise SystemExit("statement bundle hash is stale")
    if formal["statement_file_sha256"] != SOURCE_SHA256:
        raise SystemExit("statement source hash is stale")
    if instance["canonical_formal_target"]["elaborated_expression_hash"] != f"sha256:{EXPRESSION_SHA256}":
        raise SystemExit("instance expression hash is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{EXPRESSION_SHA256}"]:
        raise SystemExit("receipt expression hash is stale")
    if receipt["statement_bundle_sha256"] != BUNDLE_SHA256:
        raise SystemExit("receipt bundle hash is stale")
    if receipt["statement_file_sha256"] != SOURCE_SHA256:
        raise SystemExit("receipt source hash is stale")
    if packet["item_id"] != receipt["item_id"] or packet["item_id"] != ITEM_ID:
        raise SystemExit("worker item identity mismatch")
    if receipt["theorem_id"] != statement["theorem_id"] or receipt["theorem_id"] != THEOREM_ID:
        raise SystemExit("theorem identity mismatch")
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

    for relative in (
        "Docs/Blueprint_Guidelines.md",
        "Formalizations/Lean/lean-toolchain",
        "Formalizations/Lean/lake-manifest.json",
    ):
        expected = f"sha256:{hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()}"
        if source_hashes[relative] != expected:
            raise SystemExit(f"receipt source hash is stale: {relative}")

    environment = receipt["environment"]
    mathlib_dir = LEAN_DIR / ".lake" / "packages" / "mathlib"
    for module, expected_hash in environment["direct_import_source_sha256"].items():
        module_path = mathlib_dir / (module.replace(".", "/") + ".lean")
        if hashlib.sha256(module_path.read_bytes()).hexdigest() != expected_hash:
            raise SystemExit(f"direct import source hash is stale: {module}")
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=mathlib_dir, text=True
    ).strip()
    tree = subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib_dir, text=True
    ).strip()
    if revision != environment["mathlib_revision"] or tree != environment["mathlib_tree"]:
        raise SystemExit("mathlib revision or tree is stale")

    result = subprocess.run(
        ["python3", "-B", str(HERE / "check_statement.py")],
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
    if payload["statement_bundle_sha256"] != BUNDLE_SHA256:
        raise SystemExit("fresh helper bundle disagrees with metadata")
    if payload["statement_file_sha256"] != SOURCE_SHA256:
        raise SystemExit("fresh source hash disagrees with metadata")
    print("statement artifact check: ok (THM-M-0814; provisional; theorem_complete false)")


if __name__ == "__main__":
    main()
