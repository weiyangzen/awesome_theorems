#!/usr/bin/env python3
"""Cross-check THM-M-0957 statement metadata against fresh elaboration."""

from pathlib import Path
import hashlib
import json
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0957-STATEMENT"
THEOREM_ID = "THM-M-0957"
BASE_REVISION = "b56df790fc94c5366cf919a6fe5411d06b427c59"
EXPRESSION_SHA256 = "e611db43ce6f3419553e3ebe0fe85a3ce89e4d3930b3842f5a09be8a7683d2ed"
BUNDLE_SHA256 = "dd54684a60e69f61c8feaf6588eae6a1c9aa5931b5f68297badf39e72aed6671"
SOURCE_SHA256 = "b4bda6c926b0568d8b244623c12b4784651d55a9eb7df9d9ba3f512ed2cd9e46"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0957/Statement.lean",
    "Stage1_Instances/THM-M-0957/check_statement.py",
    "Stage1_Instances/THM-M-0957/check_statement_artifacts.py",
    "Stage1_Instances/THM-M-0957/statement-receipt.json",
    "Stage1_Instances/THM-M-0957/statement-validation.md",
    "Stage1_Instances/THM-M-0957/statement.json",
}
AUTHORITY_INPUTS = (
    "Docs/Stage1_Targets_rev-5.6.json",
    "Docs/Stage1_Blueprint_rev-5.6.md",
    "Docs/Stage1_Execution_DAG_rev-5.6.json",
    "skills/execute-stage1-rev56/SKILL.md",
    "Docs/Blueprint_Guidelines.md",
    "Formalizations/Lean/lean-toolchain",
    "Formalizations/Lean/lake-manifest.json",
    "Stage1_Instances/THM-M-0957/instance.json",
    "Stage1_Instances/THM-M-0957/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0957/scope-map.md",
    "Stage1_Instances/THM-M-0957/task-dag.json",
    "Stage1_Instances/THM-M-0957/intake-receipt.json",
)


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
    if formal["statement_bundle_sha256"] != BUNDLE_SHA256:
        raise SystemExit("statement bundle hash is stale")
    if formal["statement_file_sha256"] != SOURCE_SHA256:
        raise SystemExit("statement source hash is stale")
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
    if packet["base_revision"] != receipt["base_revision"] or packet["base_revision"] != BASE_REVISION:
        raise SystemExit("worker base revision mismatch")
    if packet["state"] != "[_]" or receipt["proposed_state"] != "[_]":
        raise SystemExit("worker state must remain provisional")
    if receipt["accepted"] or statement["theorem_complete"] or receipt["theorem_complete"]:
        raise SystemExit("statement evidence cannot claim acceptance or theorem completion")
    if set(packet["changed_paths"]) != CHANGED_PATHS:
        raise SystemExit("worker changed_paths mismatch")
    if set(receipt["changed_paths"]) != CHANGED_PATHS:
        raise SystemExit("receipt changed_paths mismatch")
    if packet["known_failures"] != receipt["known_failures"]:
        raise SystemExit("worker and receipt known_failures disagree")

    source_hashes = receipt["source_inputs"]
    for relative in AUTHORITY_INPUTS:
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
    if subprocess.check_output(
        ["git", "status", "--short"], cwd=mathlib_dir, text=True
    ):
        raise SystemExit("pinned mathlib worktree is dirty")

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
        raise SystemExit("fresh statement bundle disagrees with metadata")
    if payload["statement_file_sha256"] != SOURCE_SHA256:
        raise SystemExit("fresh source hash disagrees with metadata")
    if payload["lean_output_sha256"] != receipt["lean_output_sha256"]:
        raise SystemExit("fresh Lean output disagrees with receipt")
    if payload["direct_imports"] != receipt["direct_imports"]:
        raise SystemExit("fresh direct import list disagrees with receipt")
    if payload["mathlib_revision"] != environment["mathlib_revision"]:
        raise SystemExit("fresh mathlib revision disagrees with receipt")

    print(
        "statement artifact check: ok "
        "(THM-M-0957; provisional; theorem_complete false)"
    )


if __name__ == "__main__":
    main()
