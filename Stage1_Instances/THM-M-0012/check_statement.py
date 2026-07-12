#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0012 statement."""

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
NAMESPACE = "Stage1Instances.THM_M_0012"
THEOREM_ID = "THM-M-0012"
ITEM_ID = "S56-M-0012-STATEMENT"
CANONICAL = "FundamentalTheoremOfAlgebraTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedNonconstantHypothesis",
    "mutationChangedDomainToReal",
    "mutationChangedBinderScope",
    "mutationExcludedLinearBoundary",
)
BOUNDARIES = ("zero_not_nonconstant", "C_not_nonconstant", "X_nonconstant")
TRANSPORTS = (
    "nonconstant_iff_degree_pos",
    "fundamentalTheoremOfAlgebraTarget_iff_positiveDegreeRootTarget",
    "fundamentalTheoremOfAlgebraTarget_iff_evaluationRootTarget",
)
DIRECT_IMPORTS = ("Mathlib.Analysis.Complex.Polynomial.Basic",)
PRINT_MARKER = "#print FundamentalTheoremOfAlgebraTarget"
EXPECTED_EXPRESSION_SHA256 = "d14207f425a984b6daefaa986d8351a1543f58b7631d1c842e51a3ef2392ba74"
EXPECTED_STATEMENT_FILE_SHA256 = "fce52766380ace58b4b202f267b8a3640f74655d0cacdea897de01bcf956ee46"
EXPECTED_LEAN_OUTPUT_SHA256 = "ab27dc109625b6fb4102e6284d11eba1f2eb1f57619de91ca79adacb21b9dcee"


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
        rf"def {qualified} : Prop :=\n(?P<expression>.*)\Z", result.stdout, re.DOTALL
    )
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip(), result.stdout


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    actual_imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if actual_imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {actual_imports!r}")

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative statement item identity changed")
    if item["depends_on"] != ["S56-M-0012-INTAKE"]:
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
    survivors = [name for name in DECLARATIONS[1:] if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    for name in BOUNDARIES + TRANSPORTS:
        if not re.search(rf"^(theorem|def) {re.escape(name)}\b", source_text, re.MULTILINE):
            raise SystemExit(f"missing boundary or transport declaration: {name}")

    expression_hash = sha256_bytes(canonical.encode("utf-8"))
    if EXPECTED_EXPRESSION_SHA256 != "TO_BE_RECONCILED" and (
        expression_hash != EXPECTED_EXPRESSION_SHA256
    ):
        raise SystemExit("elaborated expression changed without reconciliation")

    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    if statement_file_hash != EXPECTED_STATEMENT_FILE_SHA256:
        raise SystemExit("statement source changed without reconciliation")
    if lean_output_hash != EXPECTED_LEAN_OUTPUT_SHA256:
        raise SystemExit("canonical Lean output changed without reconciliation")

    statement = load(SOURCE.with_name("statement.json"))
    receipt = load(SOURCE.with_name("statement-receipt.json"))
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
        raise SystemExit("receipt statement source fingerprint is stale")
    if receipt["lean_output_sha256"] != lean_output_hash:
        raise SystemExit("receipt Lean-output fingerprint is stale")
    if tuple(receipt["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("receipt direct-import record is stale")

    manifest = load(LEAN_DIR / "lake-manifest.json")
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    payload = {
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "statement_file_sha256": statement_file_hash,
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "transports": list(TRANSPORTS),
        "validated_boundaries": list(BOUNDARIES),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
