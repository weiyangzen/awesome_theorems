#!/usr/bin/env python3
"""Elaborate THM-M-0648 and distinguish its structural mutations."""

from pathlib import Path
import hashlib
import json
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
SOURCE = Path(__file__).with_name("Statement.lean")
NAMESPACE = "Stage1Instances.THM_M_0648"
DECLARATIONS = [
    "CanonicalTarget",
    "mutationDownwardOnly",
    "mutationRemovedDistinguishedSet",
    "mutationUpwardEquivalentModelOnly",
]


def expression(declaration: str) -> str:
    source = SOURCE.read_text(encoding="utf-8")
    marker = f"#print {NAMESPACE}.CanonicalTarget"
    source = source.replace(marker, f"#print {NAMESPACE}.{declaration}")
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(source)
        temporary = Path(handle.name)
    try:
        run = subprocess.run(
            ["lake", "env", "lean", str(temporary)], cwd=LEAN_ROOT, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
    finally:
        temporary.unlink()
    if run.returncode:
        print(run.stdout, end="")
        raise SystemExit(run.returncode)
    match = re.search(r" : FirstOrder\.Language .* Prop :=\n(?P<expression>.*)\Z", run.stdout, re.DOTALL)
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip()


def main() -> None:
    code = "\n".join(line.split("--", 1)[0] for line in SOURCE.read_text().splitlines())
    if re.search(r"\b(sorry|admit|axiom)\b|sorryAx", code):
        raise SystemExit("forbidden proof-gap declaration in Statement.lean")
    expressions = {name: expression(name) for name in DECLARATIONS}
    canonical = expressions[DECLARATIONS[0]]
    survivors = [name for name in DECLARATIONS[1:] if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")
    manifest = json.loads((LEAN_ROOT / "lake-manifest.json").read_text())
    print(json.dumps({
        "statement_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "statement_file_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "killed_mutations": DECLARATIONS[1:],
        "toolchain": (LEAN_ROOT / "lean-toolchain").read_text().strip(),
        "mathlib_revision": next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib"),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
