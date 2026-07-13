#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0856 statement."""

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
NAMESPACE = "Stage1Instances.THM_M_0856"
THEOREM_ID = "THM-M-0856"
ITEM_ID = "S56-M-0856-STATEMENT"
CANONICAL = "TutteOneFactorTarget"
MUTATIONS = (
    "mutationRemovedFiniteness",
    "mutationChangedDomainToCompleteGraphs",
    "mutationChangedGraphBinderScope",
    "mutationExcludedEmptyCarrier",
)
TRANSPORTS = (
    "tutteOneFactorTarget_iff_expanded",
    "tutteOneFactorTarget_iff_noTutteViolatorTarget",
)
DIRECT_IMPORT = "Mathlib.Combinatorics.SimpleGraph.Matching"
PROOF_IMPORT = "Mathlib.Combinatorics.SimpleGraph.Tutte"
PRINT_MARKER = f"#print {NAMESPACE}.{CANONICAL}"
EXPECTED_EXPRESSION_SHA256 = "5364250d1d4e132aaf1d5ce8ad5425369546963189991202f49b2fcf65095bae"
EXPECTED_STATEMENT_FILE_SHA256 = "cd7ec3e97a02ccc24578de4431a1a8ebf0e9572f9616b271b67f145d72fbedce"
EXPECTED_LEAN_OUTPUT_SHA256 = "7f4494f834dd6a0f7edd67a666bdcf84d644d6b5ae3b878f6a398baa7b6f1c3b"
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def digest(value: bytes) -> str:
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
        "w", suffix=".lean", encoding="utf-8", dir=SOURCE.parent, delete=False
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        return run_lean(temporary)
    finally:
        temporary.unlink()


def expression(declaration: str) -> tuple[str, str]:
    source_text = SOURCE.read_text(encoding="utf-8")
    if source_text.count(PRINT_MARKER) != 1:
        raise SystemExit("canonical #print marker must occur exactly once")
    source_text = source_text.replace(PRINT_MARKER, f"#print {NAMESPACE}.{declaration}")
    result = run_text(source_text)
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    qualified = re.escape(f"{NAMESPACE}.{declaration}")
    match = re.search(
        rf"def {qualified}(?:\.\{{[^\n]+\}})? : Prop :=\n(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not serialize {declaration}")
    serialized = match.group("expression").strip()
    if "?m." in serialized or "sorryAx" in serialized:
        raise SystemExit(f"invalid elaborated expression for {declaration}")
    return serialized, result.stdout


def check_forbidden_constructs(source_text: str) -> None:
    without_comments = re.sub(r"/-.*?-/", "", source_text, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b")
    match = forbidden.search(without_comments)
    if match:
        raise SystemExit(f"forbidden Lean construct: {match.group(0)}")


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    check_forbidden_constructs(source_text)

    imports = re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE)
    if imports != [DIRECT_IMPORT]:
        raise SystemExit(f"direct imports changed: {imports!r}")
    if PROOF_IMPORT in source_text:
        raise SystemExit("proof-bearing Tutte module must not be imported by the statement")

    deletion_fixture = source_text.replace(f"import {DIRECT_IMPORT}\n", "", 1)
    deleted_import = run_text(deletion_fixture)
    if deleted_import.returncode == 0:
        raise SystemExit("the sole direct import is redundant")

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    expected_identity = {
        "theorem_id": THEOREM_ID,
        "phase": "statement",
        "layer": 1,
        "depends_on": ["S56-M-0856-INTAKE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM_ID}"],
    }
    for key, expected in expected_identity.items():
        if item[key] != expected:
            raise SystemExit(f"authoritative statement {key} changed")

    serialized: dict[str, str] = {}
    outputs: dict[str, str] = {}
    for declaration in (CANONICAL, *MUTATIONS):
        serialized[declaration], outputs[declaration] = expression(declaration)
    canonical = serialized[CANONICAL]
    survivors = [name for name in MUTATIONS if serialized[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    for name in TRANSPORTS:
        if not re.search(rf"^theorem {re.escape(name)}\b", source_text, re.MULTILINE):
            raise SystemExit(f"missing checked statement transport: {name}")

    expression_sha256 = digest(canonical.encode())
    statement_sha256 = digest(SOURCE.read_bytes())
    lean_output_sha256 = digest(outputs[CANONICAL].encode())
    reconciled = {
        "expression": (expression_sha256, EXPECTED_EXPRESSION_SHA256),
        "statement": (statement_sha256, EXPECTED_STATEMENT_FILE_SHA256),
        "lean output": (lean_output_sha256, EXPECTED_LEAN_OUTPUT_SHA256),
    }
    for label, (actual, expected) in reconciled.items():
        if actual != expected:
            raise SystemExit(f"{label} changed without reconciliation")

    manifest = load(LEAN_DIR / "lake-manifest.json")
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"]
        if package["name"] == "mathlib"
    )
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit("mathlib revision changed")
    toolchain = (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip()
    if toolchain != EXPECTED_TOOLCHAIN:
        raise SystemExit("Lean toolchain changed")

    payload = {
        "direct_import": DIRECT_IMPORT,
        "elaborated_expression_sha256": expression_sha256,
        "killed_mutations": list(MUTATIONS),
        "lean_output_sha256": lean_output_sha256,
        "mathlib_revision": mathlib_revision,
        "minimal_import_deletion_exit": deleted_import.returncode,
        "mutation_expression_sha256": {
            name: digest(serialized[name].encode()) for name in MUTATIONS
        },
        "statement_file_sha256": statement_sha256,
        "toolchain": toolchain,
        "transports": list(TRANSPORTS),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
