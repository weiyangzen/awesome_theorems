#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0115 statement."""

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
NAMESPACE = "Stage1Instances.THMM0115"
THEOREM_ID = "THM-M-0115"
ITEM_ID = "S56-M-0115-STATEMENT"
CANONICAL = "GrothendieckRiemannRochExpandedTarget"
MUTATIONS = (
    "MutationRemovedProperness",
    "MutationChangedBaseDomain",
    "MutationChangedAlphaBinderScope",
    "MutationOnlyZeroClass",
)
TRANSPORTS = ("grothendieckRiemannRochTarget_iff_expanded",)
DIRECT_IMPORTS = (
    "Mathlib.AlgebraicGeometry.Morphisms.Proper",
    "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
)
PRINT_MARKER = "#print GrothendieckRiemannRochExpandedTarget"
EXPECTED_EXPRESSION_SHA256 = "eada246ab2968c378c5b6c31c2ffd84c10873d9206b499457c451ae3848c160e"
EXPECTED_STATEMENT_FILE_SHA256 = "26648a8514a0a9240c831132918c9ad0f735eb7accce33f2287a45961394d538"
EXPECTED_LEAN_OUTPUT_SHA256 = "bfff4eb71b922d3feaf598391d55b7e404d8fe5ebbd7c8a5691ce128288a52cf"
PRINT_AXIOMS_MARKER = "#print axioms grothendieckRiemannRochTarget_iff_expanded"
FORBIDDEN = re.compile(
    r"(^|[^A-Za-z_])(sorry|admit|sorryAx|axiom|constant|opaque|unsafe|"
    r"implemented_by|native_decide)([^A-Za-z_]|$)"
)


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
        env={**os.environ, "LC_ALL": "C", "TZ": "UTC"},
    )


def run_text(source: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", encoding="utf-8", dir=SOURCE.parent, delete=False
    ) as handle:
        handle.write(source)
        temporary = Path(handle.name)
    try:
        return run_lean(temporary)
    finally:
        temporary.unlink()


def check_import_minimality(source: str) -> None:
    replacements = (
        (DIRECT_IMPORTS[0], "Mathlib.AlgebraicGeometry.Morphisms.Separated", "IsProper"),
        (DIRECT_IMPORTS[1], "Mathlib.AlgebraicGeometry.Morphisms.RingHomProperties", "Smooth"),
    )
    for imported, weaker_import, required_name in replacements:
        reduced = source.replace(f"import {imported}\n", f"import {weaker_import}\n", 1)
        with tempfile.NamedTemporaryFile(
            "w", suffix=".lean", encoding="utf-8", dir=SOURCE.parent, delete=False
        ) as handle:
            handle.write(reduced)
            temporary = Path(handle.name)
        try:
            result = subprocess.run(
                ["lake", "env", "lean", str(temporary)],
                cwd=LEAN_DIR,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
                env={**os.environ, "LC_ALL": "C", "TZ": "UTC"},
            )
            if result.returncode == 0 or not (
                "Unknown identifier" in result.stdout and required_name in result.stdout
            ):
                raise SystemExit(f"direct import is not verified minimal: {imported}")
        finally:
            temporary.unlink()


def elaborate_expression(declaration: str) -> tuple[str, str]:
    source = SOURCE.read_text(encoding="utf-8")
    if source.count(PRINT_MARKER) != 1:
        raise SystemExit("canonical #print marker must occur exactly once")
    if declaration != CANONICAL:
        source = source.replace(PRINT_AXIOMS_MARKER, "")
    source = source.replace(PRINT_MARKER, f"#print {declaration}")
    result = run_text(source)
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
    if FORBIDDEN.search(source_text):
        raise SystemExit("prohibited Lean construct in statement source")
    if "#check_failure" not in source_text or "#print axioms" not in source_text:
        raise SystemExit("mutation or axiom probes are missing")
    actual_imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if actual_imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {actual_imports!r}")

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement":
        raise SystemExit("authoritative statement identity changed")
    if item["layer"] != 1 or item["depends_on"] != ["S56-M-0115-INTAKE"]:
        raise SystemExit("authoritative statement dependency changed")
    if item["owned_paths"] != [f"Stage1_Instances/{THEOREM_ID}"]:
        raise SystemExit("authoritative statement ownership changed")

    expressions: dict[str, str] = {}
    canonical_output = ""
    for declaration in (CANONICAL,) + MUTATIONS:
        expression, output = elaborate_expression(declaration)
        expressions[declaration] = expression
        if declaration == CANONICAL:
            canonical_output = output

    check_import_minimality(source_text)

    canonical = expressions[CANONICAL]
    survivors = [name for name in MUTATIONS if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    for name in TRANSPORTS:
        if not re.search(rf"^theorem {re.escape(name)}\b", source_text, re.MULTILINE):
            raise SystemExit(f"missing checked statement transport: {name}")

    check_failures = re.findall(
        r"^#check_failure \(show GrothendieckRiemannRochTarget\.\{u, v\} from (\w+)\)$",
        source_text,
        re.MULTILINE,
    )
    if tuple(check_failures) != ("hRemoved", "hDomain", "hScope", "hBoundary"):
        raise SystemExit("the four exact-type mutation probes changed")

    expression_hash = sha256_bytes(canonical.encode("utf-8"))
    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    for label, expected, actual in (
        ("expression", EXPECTED_EXPRESSION_SHA256, expression_hash),
        ("statement source", EXPECTED_STATEMENT_FILE_SHA256, statement_file_hash),
        ("Lean output", EXPECTED_LEAN_OUTPUT_SHA256, lean_output_hash),
    ):
        if expected != "TO_BE_RECONCILED" and expected != actual:
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
    input_hashes = receipt["nonrelease_input_hashes"]
    if input_hashes["statement_lean_sha256"] != statement_file_hash:
        raise SystemExit("receipt nonrelease statement hash is stale")
    if input_hashes["check_statement_py_sha256"] != sha256_bytes(Path(__file__).read_bytes()):
        raise SystemExit("receipt nonrelease validator hash is stale")
    if input_hashes["statement_json_sha256"] != sha256_bytes(STATEMENT.read_bytes()):
        raise SystemExit("receipt nonrelease statement-record hash is stale")
    validation = SOURCE.with_name("statement-validation.md")
    readme = SOURCE.with_name("README.md")
    if input_hashes["statement_validation_md_sha256"] != sha256_bytes(validation.read_bytes()):
        raise SystemExit("receipt nonrelease validation-record hash is stale")
    if input_hashes["readme_sha256"] != sha256_bytes(readme.read_bytes()):
        raise SystemExit("receipt nonrelease README hash is stale")

    manifest = load(LEAN_DIR / "lake-manifest.json")
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"]
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
