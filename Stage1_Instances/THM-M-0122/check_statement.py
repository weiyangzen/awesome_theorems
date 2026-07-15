#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0122 statement."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
STATEMENT = Path(__file__).with_name("statement.json")
RECEIPT = Path(__file__).with_name("statement-receipt.json")
NAMESPACE = "Stage1Instances.THMM0122"
THEOREM_ID = "THM-M-0122"
ITEM_ID = "S56-M-0122-STATEMENT"
CANONICAL = "FaltingsTarget"
MUTATIONS = (
    "MutationRemovedGenusHypothesis",
    "MutationRemovedNumberField",
    "MutationChangedCurveBinderScope",
    "MutationIncludesGenusOne",
)
TRANSPORTS = (
    "faltingsTarget_iff_expanded",
    "finite_rationalPoint_iff_finite_over",
    "faltingsTarget_iff_over",
)
DIRECT_IMPORTS = (
    "Mathlib.AlgebraicGeometry.Geometrically.Basic",
    "Mathlib.AlgebraicGeometry.Modules.Sheaf",
    "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
    "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Basic",
    "Mathlib.CategoryTheory.Abelian.GrothendieckCategory.HasExt",
    "Mathlib.CategoryTheory.Sites.SheafCohomology.Basic",
    "Mathlib.NumberTheory.NumberField.Basic",
    "Mathlib.Topology.Sheaves.Abelian",
)
PRINT_MARKER = "#print FaltingsTarget"
EXPECTED_EXPRESSION_SHA256 = "f3e5f585b30ab9543bc47551d0d91c695523bace26fdb5484869add319ef7dac"
EXPECTED_STATEMENT_FILE_SHA256 = "824c2d9410bbf3117fa6340e4259f9a3a7df6ff892c4b7cc6dad94a03ab437e8"
EXPECTED_LEAN_OUTPUT_SHA256 = "82b09c5ebb5b8a560f76cc37361d67faf46d8ca8555ce1b4fe5d730f0fb7271b"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "TZ": "UTC"})
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_DIR,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def run_text(text: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", encoding="utf-8", dir=SOURCE.parent, delete=False
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
        rf"def {qualified}(?:\.\{{[^\n]*\}})? : Prop :=\n"
        rf"(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
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
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement":
        raise SystemExit("authoritative statement identity changed")
    if item["layer"] != 1 or item["depends_on"] != ["S56-M-0122-INTAKE"]:
        raise SystemExit("authoritative statement dependency changed")
    if item["owned_paths"] != [f"Stage1_Instances/{THEOREM_ID}"]:
        raise SystemExit("authoritative statement ownership changed")

    declarations = (CANONICAL,) + MUTATIONS
    expressions: dict[str, str] = {}
    canonical_output = ""
    for declaration in declarations:
        expression, output = elaborate_expression(declaration)
        expressions[declaration] = expression
        if declaration == CANONICAL:
            canonical_output = output

    canonical = expressions[CANONICAL]
    survivors = [name for name in MUTATIONS if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")
    if len(set(expressions.values())) != len(expressions):
        raise SystemExit("two statement or mutation expressions unexpectedly coincide")

    for name in TRANSPORTS:
        if not re.search(rf"^theorem {re.escape(name)}\b", source_text, re.MULTILINE):
            raise SystemExit(f"missing checked statement transport: {name}")

    check_failures = re.findall(
        r"^#check_failure \(show FaltingsTarget\.\{u\} from (\w+)\)$",
        source_text,
        re.MULTILINE,
    )
    if tuple(check_failures) != ("hRemoved", "hDomain", "hScope", "hBoundary"):
        raise SystemExit("the four exact-type mutation probes changed")

    expression_hash = sha256_bytes(canonical.encode("utf-8"))
    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))

    expected = (
        ("expression", EXPECTED_EXPRESSION_SHA256, expression_hash),
        ("statement source", EXPECTED_STATEMENT_FILE_SHA256, statement_file_hash),
        ("Lean output", EXPECTED_LEAN_OUTPUT_SHA256, lean_output_hash),
    )
    for label, pinned, actual in expected:
        if pinned != "TO_BE_RECONCILED" and pinned != actual:
            raise SystemExit(f"{label} changed without reconciliation")

    statement = load(STATEMENT)
    receipt = load(RECEIPT)
    formal = statement["canonical_formal_target"]
    if formal["elaborated_expression_sha256"] != expression_hash:
        raise SystemExit("statement expression fingerprint is stale")
    if formal["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("statement source fingerprint is stale")
    if tuple(statement["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("statement direct-import record is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
        raise SystemExit("receipt expression fingerprint is stale")
    if receipt["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("receipt source fingerprint is stale")
    if receipt["lean_output_sha256"] != lean_output_hash:
        raise SystemExit("receipt Lean-output fingerprint is stale")
    if tuple(receipt["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("receipt direct-import record is stale")

    manifest = load(LEAN_DIR / "lake-manifest.json")
    mathlib_revision = next(
        package["rev"]
        for package in manifest["packages"]
        if package["name"] == "mathlib"
    )
    payload = {
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "killed_mutations": list(MUTATIONS),
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "statement_file_sha256": statement_file_hash,
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "transports": list(TRANSPORTS),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
