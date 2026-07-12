#!/usr/bin/env python3
"""Validate the exact THM-M-1356 statement and its statement mutations."""

from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
NAMESPACE = "Stage1Instances.THM_M_1356"
CANONICAL = "RouthHurwitzTarget"
MUTATIONS = [
    "mutationRemovedPositiveLeadingCoefficient",
    "mutationChangedCoefficientDomain",
    "mutationChangedBinderScope",
    "mutationAllowsZeroDegree",
]


def run_lean(source: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(source)],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
    )


def expression(declaration: str) -> str:
    text = SOURCE.read_text(encoding="utf-8")
    marker = f"#print {NAMESPACE}.{CANONICAL}"
    if marker not in text:
        raise SystemExit("canonical #print marker missing")
    text = text.replace(marker, f"#print {NAMESPACE}.{declaration}")
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        result = run_lean(temporary)
    finally:
        temporary.unlink()
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    match = re.search(r" : Prop :=\n(?P<expression>.*)\Z", result.stdout, re.DOTALL)
    if not match:
        raise SystemExit(f"could not serialize {declaration}")
    return match.group("expression").strip()


def import_minimality() -> dict[str, str]:
    text = SOURCE.read_text(encoding="utf-8")
    imports = [line for line in text.splitlines() if line.startswith("import ")]
    failures = {}
    for line in imports:
        candidate = text.replace(line + "\n", "", 1)
        with tempfile.NamedTemporaryFile(
            "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
        ) as handle:
            handle.write(candidate)
            temporary = Path(handle.name)
        try:
            result = run_lean(temporary)
        finally:
            temporary.unlink()
        if result.returncode == 0:
            raise SystemExit(f"direct import is redundant: {line.removeprefix('import ')}")
        first_error = next(
            (row for row in result.stdout.splitlines() if "error" in row),
            "Lean rejected the import-deletion fixture",
        )
        failures[line.removeprefix("import ")] = first_error
    return failures


def main() -> None:
    expressions = {name: expression(name) for name in [CANONICAL, *MUTATIONS]}
    canonical = expressions[CANONICAL]
    survivors = [name for name in MUTATIONS if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text())
    payload = {
        "elaborated_expression_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "statement_file_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "killed_mutations": MUTATIONS,
        "minimal_import_deletion_failures": import_minimality(),
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text().strip(),
        "mathlib_revision": next(
            package["rev"]
            for package in manifest["packages"]
            if package["name"] == "mathlib"
        ),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
