#!/usr/bin/env python3
"""Validate the exact THM-M-0861 statement and structural mutations."""

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
NAMESPACE = "Stage1Instances.THM_M_0861"
CANONICAL = "KonigEdgeColoringTarget"
MUTATIONS = [
    "mutationRemovedBipartiteHypothesis",
    "mutationFiniteAmbientDomains",
    "mutationGlobalBipartitionScope",
    "mutationPositiveMaximumDegreeOnly",
]
DIRECT_IMPORTS = [
    "Mathlib.Combinatorics.Graph.Basic",
    "Mathlib.Data.Set.Card",
]


def run_lean(source: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(source)],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
    )


def expression(declaration: str) -> tuple[str, str]:
    text = SOURCE.read_text(encoding="utf-8")
    marker = f"#print {NAMESPACE}.{CANONICAL}"
    if text.count(marker) != 1:
        raise SystemExit("canonical #print marker is missing or ambiguous")
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
    serialized = match.group("expression").strip()
    if "?m." in serialized:
        raise SystemExit(f"unresolved metavariable in {declaration}")
    return serialized, result.stdout


def import_minimality(source_text: str) -> dict[str, dict[str, str | int]]:
    actual_imports = [
        line.removeprefix("import ")
        for line in source_text.splitlines()
        if line.startswith("import ")
    ]
    if actual_imports != DIRECT_IMPORTS:
        raise SystemExit(f"unexpected direct imports: {actual_imports}")

    failures = {}
    for module in DIRECT_IMPORTS:
        candidate = source_text.replace(f"import {module}\n", "", 1)
        fixture_name = f"ImportWithout{module.rsplit('.', 1)[-1]}.lean"
        temporary = SOURCE.parent / fixture_name
        if temporary.exists():
            raise SystemExit(f"import-deletion fixture already exists: {temporary}")
        temporary.write_text(candidate, encoding="utf-8")
        try:
            result = run_lean(temporary)
        finally:
            temporary.unlink()
        if result.returncode == 0:
            raise SystemExit(f"direct import is redundant: {module}")
        normalized_output = result.stdout.replace(str(temporary), "<fixture>")
        first_error = next(
            (line for line in normalized_output.splitlines() if "error" in line),
            "Lean rejected the import-deletion fixture",
        )
        failures[module] = {
            "exit_code": result.returncode,
            "first_error": first_error,
            "output_sha256": hashlib.sha256(normalized_output.encode()).hexdigest(),
        }
    return failures


def check_forbidden_constructs(source_text: str) -> None:
    without_comments = re.sub(r"/-.*?-/", "", source_text, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    forbidden = re.compile(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b"
    )
    match = forbidden.search(without_comments)
    if match:
        raise SystemExit(f"forbidden Lean construct: {match.group(0)}")


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    check_forbidden_constructs(source_text)

    serialized = {}
    outputs = {}
    for declaration in [CANONICAL, *MUTATIONS]:
        serialized[declaration], outputs[declaration] = expression(declaration)
    canonical = serialized[CANONICAL]
    survivors = [name for name in MUTATIONS if serialized[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text(encoding="utf-8"))
    payload = {
        "direct_imports": DIRECT_IMPORTS,
        "elaborated_expression_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "killed_mutations": MUTATIONS,
        "lean_output_sha256": hashlib.sha256(outputs[CANONICAL].encode()).hexdigest(),
        "mathlib_revision": next(
            package["rev"] for package in manifest["packages"]
            if package["name"] == "mathlib"
        ),
        "minimal_import_deletion_failures": import_minimality(source_text),
        "mutation_expression_sha256": {
            name: hashlib.sha256(serialized[name].encode()).hexdigest()
            for name in MUTATIONS
        },
        "statement_file_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "toolchain": (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip(),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
