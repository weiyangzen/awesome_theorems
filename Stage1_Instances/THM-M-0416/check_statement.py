#!/usr/bin/env python3
"""Elaborate THM-M-0416, fingerprint it, and reject statement mutations."""

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
NAMESPACE = "Stage1Instances.THM_M_0416"


def elaborate(source: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(source)], cwd=LEAN_DIR, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )


def expression(declaration: str) -> str:
    text = SOURCE.read_text()
    marker = f"#print {NAMESPACE}.DirichletUnitTheoremTarget"
    text = text.replace(marker, f"#print {NAMESPACE}.{declaration}")
    with tempfile.NamedTemporaryFile("w", suffix=".lean", dir=SOURCE.parent, delete=False) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        result = elaborate(temporary)
    finally:
        temporary.unlink()
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    match = re.search(r" : Prop :=\n(?P<expression>.*)\Z", result.stdout, re.DOTALL)
    if not match:
        raise SystemExit(f"could not extract expression for {declaration}")
    return match.group("expression").strip()


def removed_hypothesis_must_fail() -> None:
    original = SOURCE.read_text()
    mutated = original.replace(
        "∀ (K : Type u) [Field K] [NumberField K],",
        "∀ (K : Type u) [Field K],",
        1,
    )
    if mutated == original:
        raise SystemExit("removed-hypothesis mutation was not applied")
    with tempfile.NamedTemporaryFile("w", suffix=".lean", dir=SOURCE.parent, delete=False) as handle:
        handle.write(mutated)
        temporary = Path(handle.name)
    try:
        result = elaborate(temporary)
    finally:
        temporary.unlink()
    if result.returncode == 0:
        raise SystemExit("statement mutation survived: removed NumberField hypothesis")


def main() -> None:
    canonical = expression("DirichletUnitTheoremTarget")
    for mutation in (
        "mutationChangedDomain", "mutationChangedBinderScope", "mutationExcludesRankZero"
    ):
        if expression(mutation) == canonical:
            raise SystemExit(f"statement mutation survived: {mutation}")
    removed_hypothesis_must_fail()
    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text())
    print(json.dumps({
        "statement_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "killed_mutations": [
            "removed NumberField hypothesis", "changed arbitrary field to Rat",
            "changed universal field binder to existential", "excluded rank-zero fields",
        ],
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text().strip(),
        "mathlib_revision": next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib"),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
