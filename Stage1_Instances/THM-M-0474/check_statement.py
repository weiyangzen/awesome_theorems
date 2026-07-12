#!/usr/bin/env python3
"""Elaborate THM-M-0474, fingerprint it, and reject structural mutations."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
NAMESPACE = "Stage1Instances.THM_M_0474"
CANONICAL = "FermatLittleTheoremTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedCoprimeHypothesis",
    "mutationChangedDomainToIntegerModEq",
    "mutationChangedBaseBinderScope",
    "mutationExcludedPrimeTwo",
)
DIRECT_IMPORTS = (
    "Mathlib.Data.Nat.ModEq",
    "Mathlib.Data.Nat.Prime.Defs",
)
PRINT_MARKER = "#print FermatLittleTheoremTarget"
THEOREM_ID = "THM-M-0474"
ITEM_ID = "S56-M-0474-STATEMENT"
EXPRESSION_SHA256 = "5475969fd23513d3b98134a6aaa747675a32a899f38be773a23cb330f2f590e8"
OWNED_FILES = {
    "IntakeProbe.lean",
    "README.md",
    "Statement.lean",
    "check_intake.py",
    "check_statement.py",
    "instance.json",
    "intake-receipt.json",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "statement-receipt.json",
    "statement-validation.md",
    "AnchorAudit.lean",
    "anchor-audit.json",
    "check_anchor_audit.py",
    "anchor-audit-validation.md",
    "anchor-audit-receipt.json",
    "statement.json",
    "task-dag.json",
    "validation.md",
}
CHANGED_OWNED_FILES = (
    "Statement.lean",
    "check_intake.py",
    "check_statement.py",
    "instance.json",
    "README.md",
    "scope-map.md",
    "source-statement-crosswalk.md",
    "statement-receipt.json",
    "statement-validation.md",
    "statement.json",
    "validation.md",
)
CHANGED_PATHS = {".stage1-worker-selftest.json"} | {
    f"Stage1_Instances/{THEOREM_ID}/{name}" for name in CHANGED_OWNED_FILES
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def run_text(text: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile("w", suffix=".lean", encoding="utf-8", delete=False) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        return run_lean(temporary)
    finally:
        temporary.unlink()


def elaborate_expression(declaration: str) -> tuple[str, str]:
    text = SOURCE.read_text(encoding="utf-8")
    assert text.count(PRINT_MARKER) == 1, "canonical #print marker must occur exactly once"
    text = text.replace(PRINT_MARKER, f"#print {declaration}")
    result = run_text(text)
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    qualified = re.escape(f"{NAMESPACE}.{declaration}")
    match = re.search(rf"def {qualified} : Prop :=\n(?P<expression>.*)\Z", result.stdout, re.DOTALL)
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip(), result.stdout


def check_minimal_imports() -> dict[str, int]:
    target = (
        "def ImportProbe : Prop := forall (p a : Nat), p.Prime -> a.Coprime p -> "
        "a ^ (p - 1) ≡ 1 [MOD p]\n"
    )
    exits: dict[str, int] = {}
    for omitted in DIRECT_IMPORTS:
        imports = "".join(f"import {name}\n" for name in DIRECT_IMPORTS if name != omitted)
        result = run_text(imports + target)
        exits[omitted] = result.returncode
        if result.returncode == 0:
            raise SystemExit(f"declared import is redundant for the target: {omitted}")
    return exits


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    actual_imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if actual_imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {actual_imports!r}")

    statement = load(SOURCE.with_name("statement.json"))
    receipt = load(SOURCE.with_name("statement-receipt.json"))
    instance = load(SOURCE.with_name("instance.json"))
    dag = load(SOURCE.with_name("task-dag.json"))
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    selftest = load(ROOT / ".stage1-worker-selftest.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    task = next(row for row in dag["tasks"] if row["id"] == ITEM_ID)

    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative execution item identity changed")
    if item["depends_on"] != ["S56-M-0474-INTAKE"] or item["owned_paths"] != [
        f"Stage1_Instances/{THEOREM_ID}"
    ]:
        raise SystemExit("statement dependency or ownership changed")
    if task["state"] != "open" or task["depends_on"] != item["depends_on"]:
        raise SystemExit("worker must not mutate the authoritative local task state")
    if any(record["theorem_id"] != THEOREM_ID for record in (statement, receipt, instance)):
        raise SystemExit("dossier theorem IDs disagree")
    if statement["item_id"] != receipt["item_id"] or receipt["item_id"] != ITEM_ID:
        raise SystemExit("statement item IDs disagree")
    if selftest["state"] != "[_]":
        raise SystemExit("root self-test is not provisional")
    if selftest["item_id"] == ITEM_ID:
        if set(receipt["changed_paths"]) != set(selftest["changed_paths"]) or set(
            selftest["changed_paths"]
        ) != CHANGED_PATHS:
            raise SystemExit("statement changed-path handoff is incomplete")
    elif selftest["item_id"] != "S56-M-0474-ANCHOR_AUDIT":
        raise SystemExit("root self-test covers neither this statement nor its direct successor")
    if set(instance["owned_artifacts"]) != OWNED_FILES:
        raise SystemExit("instance artifact inventory is stale")
    actual_files = {path.name for path in SOURCE.parent.iterdir() if path.is_file()}
    if actual_files != OWNED_FILES:
        raise SystemExit("owned directory contains an unrecorded or missing file")
    if any(record["theorem_complete"] for record in (statement, receipt, instance, dag, selftest)):
        raise SystemExit("statement phase cannot claim theorem completion")
    if statement["accepted_receipt_ids"] or receipt["accepted_receipt_ids"]:
        raise SystemExit("worker statement receipt cannot be accepted")

    expressions: dict[str, str] = {}
    canonical_output = ""
    for declaration in DECLARATIONS:
        expression, output = elaborate_expression(declaration)
        expressions[declaration] = expression
        if declaration == CANONICAL:
            canonical_output = output

    canonical = expressions[CANONICAL]
    survivors = [name for name in DECLARATIONS[1:] if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    missing_import_exits = check_minimal_imports()
    expression_hash = sha256_bytes(canonical.encode("utf-8"))
    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    if expression_hash != EXPRESSION_SHA256:
        raise SystemExit("elaborated expression changed without reconciliation")
    formal = statement["canonical_formal_target"]
    instance_formal = instance["canonical_formal_target"]
    if formal["elaborated_expression_sha256"] != expression_hash:
        raise SystemExit("statement expression fingerprint is stale")
    if tuple(formal["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("statement direct-import record is stale")
    if tuple(receipt["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("receipt direct-import record is stale")
    if instance_formal["elaborated_expression_hash"] != f"sha256:{expression_hash}":
        raise SystemExit("instance expression fingerprint is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
        raise SystemExit("receipt expression fingerprint is stale")
    if formal["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("statement source fingerprint is stale")
    if receipt["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("receipt source fingerprint is stale")
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    if receipt["lean_output_sha256"] != lean_output_hash:
        raise SystemExit("receipt Lean-output fingerprint is stale")
    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text(encoding="utf-8"))
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    if mathlib_revision != statement["environment_fingerprint"]["mathlib_revision"]:
        raise SystemExit("statement mathlib revision is stale")
    if mathlib_revision != receipt["worker_input_hashes"]["mathlib_revision"]:
        raise SystemExit("receipt mathlib revision is stale")
    payload = {
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "missing_import_exits": missing_import_exits,
        "statement_file_sha256": statement_file_hash,
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
