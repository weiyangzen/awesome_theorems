#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0487 statement."""

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
NAMESPACE = "Stage1Instances.THM_M_0487"
CANONICAL = "WeakGoldbachTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedOddHypothesis",
    "mutationChangedDomainToFinEight",
    "mutationChangedBinderScope",
    "mutationIncludedFiveBoundary",
)
TRANSPORTS = (
    "weakGoldbachTarget_iff_reversedEqualityWeakGoldbachTarget",
    "weakGoldbachTarget_iff_integerWeakGoldbachTarget",
)
BOUNDARIES = (
    "five_excluded",
    "five_not_three_prime_sum",
    "mutationIncludedFiveBoundary_is_false",
    "mutationChangedDomainToFinEight_is_true",
    "seven_included",
    "seven_repeated_prime_representation",
    "eight_not_odd",
)
DIRECT_IMPORTS = (
    "Mathlib.Algebra.Ring.Int.Parity",
    "Mathlib.Data.Nat.Prime.Defs",
)
PRINT_MARKER = "#print WeakGoldbachTarget"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_EXPRESSION_SHA256 = "29ac94dd615869191754270061d8fe7123991d403a07bbdf27a09f706665e703"


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
    exits = []
    for direct_import in DIRECT_IMPORTS:
        result = run_text(source.replace(f"import {direct_import}\n", "", 1))
        if result.returncode == 0:
            raise SystemExit(f"declared direct import is redundant: {direct_import}")
        exits.append(result.returncode)
    return min(exits)


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    imports = tuple(re.findall(r"^import (\S+)$", source, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {imports!r}")
    if "set_option autoImplicit false" not in source:
        raise SystemExit("fixed autoImplicit option missing")

    expressions: dict[str, str] = {}
    for declaration in DECLARATIONS:
        expressions[declaration], _ = explicit_expression(declaration)
    canonical = expressions[CANONICAL]
    survivors = [name for name in DECLARATIONS[1:] if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    for declaration in TRANSPORTS + BOUNDARIES:
        if not re.search(
            rf"^theorem {re.escape(declaration)}\b", source, re.MULTILINE
        ):
            raise SystemExit(f"missing transport or boundary declaration: {declaration}")

    ordinary = run_lean(SOURCE)
    if ordinary.returncode:
        print(ordinary.stdout, end="")
        raise SystemExit(ordinary.returncode)

    expression_hash = hashlib.sha256(canonical.encode()).hexdigest()
    if expression_hash != EXPECTED_EXPRESSION_SHA256:
        raise SystemExit("canonical elaborated expression changed")

    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text(encoding="utf-8"))
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit(f"unexpected mathlib revision: {mathlib_revision}")

    mathlib_source = LEAN_DIR / ".lake/packages/mathlib/Mathlib/Data/Nat/Prime/Defs.lean"
    result = {
        "direct_imports": list(imports),
        "expression_sha256": expression_hash,
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": hashlib.sha256(ordinary.stdout.encode()).hexdigest(),
        "mathlib_revision": mathlib_revision,
        "mathlib_source_sha256": hashlib.sha256(mathlib_source.read_bytes()).hexdigest(),
        "mutation_expression_sha256": {
            name: hashlib.sha256(expressions[name].encode()).hexdigest()
            for name in DECLARATIONS[1:]
        },
        "removing_direct_import_exit": check_direct_import(),
        "statement_file_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "transports": list(TRANSPORTS),
        "validated_boundaries": list(BOUNDARIES),
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
