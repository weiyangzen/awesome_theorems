#!/usr/bin/env python3
"""Elaborate THM-M-0484, fingerprint it, and reject statement mutations."""

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
NAMESPACE = "Stage1Instances.THM_M_0484"
CANONICAL = "LucasLehmerTestTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedLowerBound",
    "mutationChangedDomainToPrimeExponent",
    "mutationChangedLowerBoundScope",
    "mutationIncludedExponentTwo",
)
DIRECT_IMPORTS = ("Mathlib.NumberTheory.LucasLehmer",)
PRINT_MARKER = "#print LucasLehmerTestTarget"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_EXPRESSION_SHA256 = "6bd6024bd44d0bd9c50f6425b9ce5fdaecaf783ac84d32688717d3bde3151aea"
EXPECTED_SOURCE_SHA256 = "1baec8791288b46d6df61e060be07aa190ac1d0424229595523a095e8259c8dc"


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def run_text(source: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", encoding="utf-8", delete=False
    ) as handle:
        handle.write(source)
        temporary = Path(handle.name)
    try:
        return run_lean(temporary)
    finally:
        temporary.unlink()


def explicit_expression(declaration: str) -> tuple[str, str]:
    source = SOURCE.read_text(encoding="utf-8")
    if source.count(PRINT_MARKER) != 1:
        raise SystemExit("canonical #print marker must occur exactly once")
    source = source.replace(PRINT_MARKER, f"#print {declaration}")
    result = run_text(source)
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    match = re.search(
        rf"def {re.escape(NAMESPACE)}\.{re.escape(declaration)} : Prop :=\n"
        rf"(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip(), result.stdout


def check_direct_import() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    without_import = source.replace(f"import {DIRECT_IMPORTS[0]}\n", "", 1)
    result = run_text(without_import)
    if result.returncode == 0:
        raise SystemExit("declared import is redundant for the statement module")
    return result.returncode


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    imports = tuple(re.findall(r"^import (\S+)$", source, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {imports!r}")
    if "set_option autoImplicit false" not in source:
        raise SystemExit("fixed autoImplicit option missing")

    expressions: dict[str, str] = {}
    outputs: dict[str, str] = {}
    for declaration in DECLARATIONS:
        expressions[declaration], outputs[declaration] = explicit_expression(declaration)
    canonical = expressions[CANONICAL]
    survivors = [name for name in DECLARATIONS[1:] if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")
    expression_sha256 = hashlib.sha256(canonical.encode()).hexdigest()
    source_sha256 = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if expression_sha256 != EXPECTED_EXPRESSION_SHA256:
        raise SystemExit(f"canonical expression drifted: {expression_sha256}")
    if source_sha256 != EXPECTED_SOURCE_SHA256:
        raise SystemExit(f"statement source drifted: {source_sha256}")

    ordinary = run_lean(SOURCE)
    if ordinary.returncode:
        print(ordinary.stdout, end="")
        raise SystemExit(ordinary.returncode)

    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text(encoding="utf-8"))
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit(f"unexpected mathlib revision: {mathlib_revision}")

    mathlib_source = (
        LEAN_DIR / ".lake/packages/mathlib/Mathlib/NumberTheory/LucasLehmer.lean"
    )
    result = {
        "expression_sha256": expression_sha256,
        "statement_file_sha256": source_sha256,
        "lean_output_sha256": hashlib.sha256(ordinary.stdout.encode()).hexdigest(),
        "mutation_expression_sha256": {
            name: hashlib.sha256(expressions[name].encode()).hexdigest()
            for name in DECLARATIONS[1:]
        },
        "killed_mutations": list(DECLARATIONS[1:]),
        "minimal_direct_imports": list(imports),
        "removing_direct_import_exit": check_direct_import(),
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "lake_manifest_sha256": hashlib.sha256(
            (LEAN_DIR / "lake-manifest.json").read_bytes()
        ).hexdigest(),
        "mathlib_revision": mathlib_revision,
        "mathlib_source_sha256": hashlib.sha256(mathlib_source.read_bytes()).hexdigest(),
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
