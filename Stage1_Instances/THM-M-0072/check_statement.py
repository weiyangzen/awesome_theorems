#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0072 statement."""

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
NAMESPACE = "Stage1Instances.THM_M_0072"
THEOREM_ID = "THM-M-0072"
ITEM_ID = "S56-M-0072-STATEMENT"
CANONICAL = "ThompsonTransferLemmaTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedNoIndexTwoHypothesis",
    "mutationChangedDomainToCommutativeGroups",
    "mutationChangedBinderScope",
    "mutationChangedOrderBoundary",
)
BOUNDARIES = ("insideMaximal_hasConjugate",)
TRANSPORTS = (
    "thompsonTransferLemmaTarget_iff_outsideMaximalTarget",
    "thompsonTransferLemmaTarget_iff_ambientOrderTarget",
)
DIRECT_IMPORTS = ("Mathlib.GroupTheory.Sylow",)
PRINT_MARKER = "#print ThompsonTransferLemmaTarget"
EXPECTED_EXPRESSION_SHA256 = "c8a89538bd8b492ba31ce5d516a0f8fefef70a550e1d2fe74e39a4cba7849051"
EXPECTED_STATEMENT_FILE_SHA256 = "0e9a35c7d2a9eaafb2aa6f8357277e9bf1e79e9a5e88500bda6cd8300a6757aa"
EXPECTED_LEAN_OUTPUT_SHA256 = "64a08c83e76713e0ddc881b86a59fefc160219ffb237c443cdf9b8eb7b0481d6"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


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
        rf"def {qualified}(?:\.\{{u\}})? : Prop :=\n(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip(), result.stdout


def check_transport_types() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    marker = "#check thompsonTransferLemmaTarget_iff_outsideMaximalTarget"
    checks = """#check (thompsonTransferLemmaTarget_iff_outsideMaximalTarget :
  ThompsonTransferLemmaTarget <-> OutsideMaximalTarget)
#check (thompsonTransferLemmaTarget_iff_ambientOrderTarget :
  ThompsonTransferLemmaTarget <-> AmbientOrderTarget)"""
    if source_text.count(marker) != 1:
        raise SystemExit("transport #check marker must occur exactly once")
    result = run_text(source_text.replace(marker, checks))
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit("checked transport type drift")


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    actual_imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if actual_imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {actual_imports!r}")

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative statement item identity changed")
    if item["depends_on"] != ["S56-M-0072-INTAKE"]:
        raise SystemExit("authoritative statement dependency changed")
    if item["owned_paths"] != [f"Stage1_Instances/{THEOREM_ID}"]:
        raise SystemExit("authoritative statement ownership changed")

    expressions: dict[str, str] = {}
    canonical_output = ""
    for declaration in DECLARATIONS:
        expression, output = elaborate_expression(declaration)
        expressions[declaration] = expression
        if declaration == CANONICAL:
            canonical_output = output
    canonical = expressions[CANONICAL]
    if len(set(expressions.values())) != len(expressions):
        raise SystemExit("canonical target and structural mutations are not pairwise distinct")

    for name in BOUNDARIES + TRANSPORTS:
        if not re.search(rf"^theorem {re.escape(name)}\b", source_text, re.MULTILINE):
            raise SystemExit(f"missing boundary or transport declaration: {name}")
    check_transport_types()

    without_import = source_text.replace(f"import {DIRECT_IMPORTS[0]}\n", "", 1)
    if run_text(without_import).returncode == 0:
        raise SystemExit(f"direct import is redundant: {DIRECT_IMPORTS[0]}")

    expression_hash = sha256_bytes(canonical.encode("utf-8"))
    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    expected = (
        EXPECTED_EXPRESSION_SHA256,
        EXPECTED_STATEMENT_FILE_SHA256,
        EXPECTED_LEAN_OUTPUT_SHA256,
    )
    actual = (expression_hash, statement_file_hash, lean_output_hash)
    if "TO_BE_RECONCILED" not in expected and actual != expected:
        raise SystemExit("statement fingerprints changed without reconciliation")

    statement_path = SOURCE.with_name("statement.json")
    receipt_path = SOURCE.with_name("statement-receipt.json")
    if statement_path.exists() and receipt_path.exists():
        statement = load(statement_path)
        receipt = load(receipt_path)
        instance = load(SOURCE.with_name("instance.json"))
        formal = statement["canonical_formal_target"]
        if formal["elaborated_expression_sha256"] != expression_hash:
            raise SystemExit("structured statement expression fingerprint is stale")
        if formal["statement_file_sha256"] != statement_file_hash:
            raise SystemExit("structured statement source fingerprint is stale")
        if instance["canonical_formal_target"]["elaborated_expression_hash"] != (
            f"sha256:{expression_hash}"
        ):
            raise SystemExit("instance expression fingerprint is stale")
        if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
            raise SystemExit("receipt expression fingerprint is stale")
        if receipt["statement_file_sha256"] != statement_file_hash:
            raise SystemExit("receipt source fingerprint is stale")
        if receipt["lean_output_sha256"] != lean_output_hash:
            raise SystemExit("receipt Lean-output fingerprint is stale")
        if statement["item_id"] != receipt["item_id"] or receipt["item_id"] != ITEM_ID:
            raise SystemExit("statement item identity is stale")
        if statement["theorem_id"] != receipt["theorem_id"] or receipt["theorem_id"] != THEOREM_ID:
            raise SystemExit("statement theorem identity is stale")
        if statement["lifecycle"] != "planned" or receipt["proposed_state"] != "[_]":
            raise SystemExit("unexpected statement lifecycle or proposal state")
        if not statement["statement_elaborated"] or statement["theorem_proved"] or statement["theorem_complete"]:
            raise SystemExit("statement completion boundary is stale")
        if receipt["accepted"] or receipt["audit_complete"] or receipt["theorem_complete"]:
            raise SystemExit("provisional receipt overclaims accepted or terminal state")
        if tuple(statement["direct_imports"]) != DIRECT_IMPORTS or tuple(receipt["direct_imports"]) != DIRECT_IMPORTS:
            raise SystemExit("structured direct imports are stale")
        statement_transports = tuple(row["checked_witness"].rsplit(".", 1)[-1] for row in statement["checked_alternate_encodings"])
        receipt_transports = tuple(row["witness"].rsplit(".", 1)[-1] for row in receipt["checked_transports"])
        if statement_transports != TRANSPORTS or receipt_transports != TRANSPORTS:
            raise SystemExit("structured transport inventories are stale")
        mutation_names = tuple(row["declaration"] for row in statement["mutation_tests"]["killed"])
        receipt_mutations = tuple(row["declaration"] for row in receipt["mutation_tests"])
        if mutation_names != DECLARATIONS[1:] or receipt_mutations != DECLARATIONS[1:]:
            raise SystemExit("structured mutation inventories are stale")
        packet = load(ROOT / ".stage1-worker-selftest.json")
        if packet["item_id"] != ITEM_ID or packet["theorem_id"] != THEOREM_ID or packet["state"] != "[_]":
            raise SystemExit("worker packet identity or state is stale")
        if packet["changed_paths"] != receipt["changed_paths"]:
            raise SystemExit("worker packet and receipt changed-path inventories differ")
        if packet["known_failures"] != receipt["known_failures"]:
            raise SystemExit("worker packet and receipt known-failure inventories differ")
        for relative, recorded in receipt["source_inputs"].items():
            if recorded != "sha256:" + sha256_bytes((ROOT / relative).read_bytes()):
                raise SystemExit(f"stale receipt source hash: {relative}")
        worker_hashes = receipt["worker_input_hashes"]
        if worker_hashes["lean_toolchain"] != "sha256:" + sha256_bytes((LEAN_DIR / "lean-toolchain").read_bytes()):
            raise SystemExit("stale receipt lean-toolchain hash")
        if worker_hashes["lake_manifest"] != "sha256:" + sha256_bytes((LEAN_DIR / "lake-manifest.json").read_bytes()):
            raise SystemExit("stale receipt lake-manifest hash")
        sylow_source = LEAN_DIR / ".lake/packages/mathlib/Mathlib/GroupTheory/Sylow.lean"
        if worker_hashes["Mathlib.GroupTheory.Sylow"] != "sha256:" + sha256_bytes(sylow_source.read_bytes()):
            raise SystemExit("stale receipt Sylow-source hash")

    manifest = load(LEAN_DIR / "lake-manifest.json")
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit(f"unexpected mathlib revision: {mathlib_revision}")
    payload = {
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "removed_direct_import_failed": True,
        "statement_file_sha256": statement_file_hash,
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "transports": list(TRANSPORTS),
        "validated_boundaries": list(BOUNDARIES),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
