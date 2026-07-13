#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0476 statement."""

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
NAMESPACE = "Stage1Instances.THM_M_0476"
THEOREM_ID = "THM-M-0476"
ITEM_ID = "S56-M-0476-STATEMENT"
CANONICAL = "WilsonTheoremTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedPrimeHypothesis",
    "mutationChangedDomainToUInt64",
    "mutationChangedPrimeBinderScope",
    "mutationIncludedCompositeFour",
)
TRANSPORT = "wilsonTheoremTarget_iff_factTarget"
DIRECT_IMPORTS = (
    "Mathlib.Data.Nat.Factorial.Basic",
    "Mathlib.Data.Nat.Prime.Defs",
    "Mathlib.Data.ZMod.Defs",
)
PRINT_MARKER = "#print WilsonTheoremTarget"
EXPECTED_EXPRESSION_SHA256 = "ee76edb160426d3e8d95b11bfedca7febcfe915f50007e042875c922ebc8a4ac"
EXPECTED_STATEMENT_FILE_SHA256 = "3903de3f1e1cdd6d2f048917005da8f2b744d6726507d09120661e79d217dff9"
EXPECTED_LEAN_OUTPUT_SHA256 = "7e576582dd36ba221200e4a924df57486e73e4868a41c9466d6476e01766a207"
EXPECTED_IMPORT_SHA256 = {
    "Mathlib.Data.Nat.Factorial.Basic":
        "5978ee423d84693e2f488fc0ef1566508499581c0afdd7f0b0d2c3c4ce0b94f3",
    "Mathlib.Data.Nat.Prime.Defs":
        "fb7b8f26c48fdb96c39d264574b70ba382d700a9a97a06ee41bb05377dfc68a4",
    "Mathlib.Data.ZMod.Defs":
        "d8817b7d6b21da3f09e2d97ac52a01dbd2adf0104c9376f8f7e3f1e1d02bd837",
}
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
EXPECTED_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_BASE_REVISION = "be8701e88e791545c16a262edd1909486d5cef4b"
EXPECTED_BASE_TREE = "78b0a751473bf6d71f453a6aad18b130268a3428"
EXPECTED_BLUEPRINT_SHA256 = "201ff7722835a8360e3400c6f173b1e6684462b46ce5ed02e6b37ba51baf81bb"
EXPECTED_EXECUTION_DAG_SHA256 = "0e2192895bfd08136cf7d965e1c9d942ff0d040568b72552bc7869c5801b41fb"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, text=True, capture_output=True
    ).stdout.strip()


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=120,
    )


def run_text(text: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", encoding="utf-8", delete=False
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        return run_lean(temporary)
    finally:
        temporary.unlink()


def elaborate_expression(declaration: str) -> tuple[str, str]:
    text = SOURCE.read_text(encoding="utf-8")
    if text.count(PRINT_MARKER) != 1:
        raise SystemExit("canonical #print marker must occur exactly once")
    text = text.replace(PRINT_MARKER, f"#print {declaration}")
    result = run_text(text)
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    qualified = re.escape(f"{NAMESPACE}.{declaration}")
    match = re.search(
        rf"def {qualified} : Prop :=\n(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip(), result.stdout


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {imports!r}")

    deletion_exits = {}
    for direct_import in DIRECT_IMPORTS:
        result = run_text(source_text.replace(f"import {direct_import}\n", "", 1))
        if result.returncode == 0:
            raise SystemExit(f"direct import is redundant: {direct_import}")
        deletion_exits[direct_import] = result.returncode

    statement_body = re.sub(r"^import [^\n]+\n", "", source_text, flags=re.MULTILINE)
    single_import_exits = {}
    for direct_import in DIRECT_IMPORTS:
        result = run_text(f"import {direct_import}\n{statement_body}")
        if result.returncode == 0:
            raise SystemExit(f"one direct import unexpectedly provides all vocabulary: {direct_import}")
        single_import_exits[direct_import] = result.returncode

    blueprint = ROOT / "Docs" / "Stage1_Blueprint_rev-5.6.md"
    execution_path = ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json"
    if sha256_bytes(blueprint.read_bytes()) != EXPECTED_BLUEPRINT_SHA256:
        raise SystemExit("authoritative blueprint hash changed")
    if sha256_bytes(execution_path.read_bytes()) != EXPECTED_EXECUTION_DAG_SHA256:
        raise SystemExit("authoritative execution DAG hash changed")
    execution = load(execution_path)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative statement item identity changed")
    if item["state"] != "[ ]" or item["depends_on"] != ["S56-M-0476-INTAKE"]:
        raise SystemExit("authoritative statement state or dependency changed")
    if item["owned_paths"] != [f"Stage1_Instances/{THEOREM_ID}"]:
        raise SystemExit("authoritative statement ownership changed")
    intake_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0476-INTAKE"
    )
    if intake_item["state"] != "[_]":
        raise SystemExit("statement predecessor is not provisionally self-tested")

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
    if not re.search(rf"^theorem {TRANSPORT}\b", source_text, re.MULTILINE):
        raise SystemExit("checked transport declaration is missing")

    expression_hash = sha256_bytes(canonical.encode("utf-8"))
    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    if expression_hash != EXPECTED_EXPRESSION_SHA256:
        raise SystemExit(f"elaborated expression changed: {expression_hash}")
    if statement_file_hash != EXPECTED_STATEMENT_FILE_SHA256:
        raise SystemExit("statement source changed without reconciliation")
    if lean_output_hash != EXPECTED_LEAN_OUTPUT_SHA256:
        raise SystemExit("canonical Lean output changed without reconciliation")

    statement = load(SOURCE.with_name("statement.json"))
    receipt = load(SOURCE.with_name("statement-receipt.json"))
    instance = load(SOURCE.with_name("instance.json"))
    dag = load(SOURCE.with_name("task-dag.json"))
    if statement["theorem_id"] != THEOREM_ID or receipt["theorem_id"] != THEOREM_ID:
        raise SystemExit("statement theorem identities disagree")
    if instance["theorem_id"] != THEOREM_ID or dag["theorem_id"] != THEOREM_ID:
        raise SystemExit("dossier theorem identities disagree")
    if statement["item_id"] != ITEM_ID or receipt["item_id"] != ITEM_ID:
        raise SystemExit("statement item identities disagree")
    if receipt["proposed_state"] != "[_]" or receipt["accepted"] is not False:
        raise SystemExit("worker receipt must remain provisional and unaccepted")
    if statement["accepted_receipt_ids"] or receipt["accepted_receipt_ids"]:
        raise SystemExit("worker statement cannot claim an accepted receipt")
    if any(record.get("audit_complete") for record in (statement, receipt, instance, dag)):
        raise SystemExit("statement phase cannot claim audit completion")
    if any(record.get("theorem_complete") for record in (statement, receipt, instance, dag)):
        raise SystemExit("statement phase cannot claim theorem completion")
    superseded = receipt["supersedes_worker_receipts"]
    if [row["receipt_id"] for row in superseded] != ["S56-M-0476-INTAKE-WORKER-20260713"]:
        raise SystemExit("historical intake projection supersession is not explicit")
    local_task = next(row for row in dag["tasks"] if row["id"] == ITEM_ID)
    if local_task["state"] != "open" or local_task["authoritative_state"] != "[ ]":
        raise SystemExit("worker must leave the local and authoritative statement state open")
    formal = statement["canonical_formal_target"]
    if tuple(statement["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("structured direct imports are stale")
    environment = statement["environment_fingerprint"]
    if environment["authoritative_blueprint_sha256"] != EXPECTED_BLUEPRINT_SHA256:
        raise SystemExit("statement blueprint fingerprint is stale")
    if environment["execution_dag_sha256"] != EXPECTED_EXECUTION_DAG_SHA256:
        raise SystemExit("statement execution DAG fingerprint is stale")
    if formal["elaborated_expression_sha256"] != expression_hash:
        raise SystemExit("structured expression fingerprint is stale")
    if formal["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("structured source fingerprint is stale")
    ascii_expression = " ".join(canonical.split()).replace("∀", "forall").replace("→", "->")
    if formal["fully_explicit_expression"] != ascii_expression:
        raise SystemExit("persisted fully explicit expression is stale")
    instance_formal = instance["canonical_formal_target"]
    if instance_formal["elaborated_expression_hash"] != f"sha256:{expression_hash}":
        raise SystemExit("instance expression fingerprint is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
        raise SystemExit("receipt expression fingerprint is stale")
    if receipt["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("receipt source fingerprint is stale")
    if receipt["lean_output_sha256"] != lean_output_hash:
        raise SystemExit("receipt Lean-output fingerprint is stale")
    for relative, expected_hash in receipt["owned_artifact_sha256"].items():
        if relative.endswith("/statement-receipt.json"):
            if expected_hash != "self_referential_excluded_from_provisional_digest":
                raise SystemExit("receipt self-reference policy changed")
        elif sha256_bytes((ROOT / relative).read_bytes()) != expected_hash:
            raise SystemExit(f"owned artifact fingerprint is stale: {relative}")

    if git("rev-parse", "HEAD") != EXPECTED_BASE_REVISION:
        raise SystemExit("base revision changed")
    if git("rev-parse", "HEAD^{tree}") != EXPECTED_BASE_TREE:
        raise SystemExit("base tree changed")
    if receipt["base_revision"] != EXPECTED_BASE_REVISION or receipt["base_tree"] != EXPECTED_BASE_TREE:
        raise SystemExit("receipt base revision or tree is stale")

    packet = load(ROOT / ".stage1-worker-selftest.json")
    required_packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    if set(packet) != required_packet_fields:
        raise SystemExit("worker packet fields changed")
    if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
        raise SystemExit("worker packet item or state is stale")
    if packet["base_revision"] != receipt["base_revision"]:
        raise SystemExit("worker packet base revision is stale")
    if packet["changed_paths"] != receipt["changed_paths"]:
        raise SystemExit("worker packet changed paths are stale")
    if packet["known_failures"] != receipt["known_failures"]:
        raise SystemExit("worker packet known failures are stale")
    status_output = subprocess.run(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout
    status_paths = {row[3:] for row in status_output.splitlines() if row}
    if status_paths != set(packet["changed_paths"]) | {"Formalizations/Lean/.lake"}:
        raise SystemExit("worker packet does not cover the complete scoped worktree change set")

    manifest = load(LEAN_DIR / "lake-manifest.json")
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    mathlib = LEAN_DIR / ".lake" / "packages" / "mathlib"
    if (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip() != EXPECTED_TOOLCHAIN:
        raise SystemExit("Lean toolchain pin changed")
    if sha256_bytes((LEAN_DIR / "lean-toolchain").read_bytes()) != EXPECTED_TOOLCHAIN_SHA256:
        raise SystemExit("Lean toolchain hash changed")
    if sha256_bytes((LEAN_DIR / "lake-manifest.json").read_bytes()) != EXPECTED_MANIFEST_SHA256:
        raise SystemExit("Lake manifest hash changed")
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit("mathlib manifest revision changed")
    if git("rev-parse", "HEAD", cwd=mathlib) != EXPECTED_MATHLIB_REVISION:
        raise SystemExit("materialized mathlib revision changed")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != EXPECTED_MATHLIB_TREE:
        raise SystemExit("materialized mathlib tree changed")
    if git("status", "--short", cwd=mathlib):
        raise SystemExit("materialized mathlib source is dirty")
    for direct_import, expected_hash in EXPECTED_IMPORT_SHA256.items():
        import_path = mathlib / (direct_import.replace(".", "/") + ".lean")
        if sha256_bytes(import_path.read_bytes()) != expected_hash:
            raise SystemExit(f"direct import source changed: {direct_import}")

    payload = {
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "import_deletion_exits": deletion_exits,
        "single_import_exits": single_import_exits,
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "statement_file_sha256": statement_file_hash,
        "toolchain": EXPECTED_TOOLCHAIN,
        "transports": [TRANSPORT],
        "validated_boundaries": [
            "p = 2 remains included",
            "the broadened composite-p=4 mutation is kernel-refuted",
        ],
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
