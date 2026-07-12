#!/usr/bin/env python3
"""Validate the frozen THM-M-0843 statement and structural mutations."""

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
NAMESPACE = "Stage1Instances.THM_M_0843"
CANONICAL = "SzemerediRegularityTarget"
MUTATIONS = [
    "mutationRemovedPositiveTolerance",
    "mutationRationalTolerance",
    "mutationExistentialLowerBound",
    "mutationPositiveLowerBoundOnly",
]
DIRECT_IMPORTS = [
    "Mathlib.Combinatorics.SimpleGraph.Regularity.Bound",
    "Mathlib.Combinatorics.SimpleGraph.Regularity.Uniform",
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


def elaborate(source: Path) -> str:
    result = run_lean(source)
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


def expression(declaration: str) -> tuple[str, str]:
    source_text = SOURCE.read_text(encoding="utf-8")
    marker = f"#print {NAMESPACE}.{CANONICAL}"
    if source_text.count(marker) != 1:
        raise SystemExit("canonical #print marker is missing or ambiguous")
    source_text = source_text.replace(marker, f"#print {NAMESPACE}.{declaration}")
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", dir=SOURCE.parent, delete=False, encoding="utf-8"
    ) as handle:
        handle.write(source_text)
        temporary = Path(handle.name)
    try:
        output = elaborate(temporary)
    finally:
        temporary.unlink()
    match = re.search(r" : Prop :=\n(?P<expression>.*)\Z", output, re.DOTALL)
    if not match:
        raise SystemExit(f"could not serialize {declaration}")
    result = match.group("expression").strip()
    if "?m." in result:
        raise SystemExit(f"unresolved metavariable in {declaration}")
    return result, output


def import_deletion_source(source_text: str, module: str) -> str:
    """Make an import-deletion fixture whose failure concerns target vocabulary."""
    candidate = source_text.replace(f"import {module}\n", "", 1)
    transport_start = candidate.index(
        "/-- The effective target implies the conventional existential-bound form. -/"
    )
    mutation_start = candidate.index(
        "/-! Structural mutations used only by the statement-identity checker. -/"
    )
    candidate = candidate[:transport_start] + candidate[mutation_start:]
    candidate = re.sub(
        r"\n#print axioms Stage1Instances\.THM_M_0843\."
        r"szemerediRegularityTarget_implies_existentialBoundTarget\n",
        "\n",
        candidate,
    )
    return candidate


def check_minimal_imports(source_text: str) -> dict[str, str]:
    actual_imports = [
        line.removeprefix("import ")
        for line in source_text.splitlines()
        if line.startswith("import ")
    ]
    if actual_imports != DIRECT_IMPORTS:
        raise SystemExit(f"unexpected direct imports: {actual_imports}")

    failures = {}
    for module in DIRECT_IMPORTS:
        candidate = import_deletion_source(source_text, module)
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
            raise SystemExit(f"direct import is redundant: {module}")
        failures[module] = {
            "exit_code": str(result.returncode),
            "output_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
        }
    return failures


def check_forbidden_constructs(source_text: str) -> None:
    without_comments = re.sub(r"/-.*?-\/", "", source_text, flags=re.DOTALL)
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
    import_failures = check_minimal_imports(source_text)

    serialized = {}
    outputs = {}
    for declaration in [CANONICAL, *MUTATIONS]:
        serialized[declaration], outputs[declaration] = expression(declaration)
    canonical = serialized[CANONICAL]
    survivors = [name for name in MUTATIONS if serialized[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text(encoding="utf-8"))
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"]
        if package["name"] == "mathlib"
    )
    payload = {
        "direct_imports": DIRECT_IMPORTS,
        "elaborated_expression_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "killed_mutations": MUTATIONS,
        "lean_output_sha256": hashlib.sha256(
            outputs[CANONICAL].encode()
        ).hexdigest(),
        "mathlib_revision": mathlib_revision,
        "minimal_import_deletion_failures": import_failures,
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
