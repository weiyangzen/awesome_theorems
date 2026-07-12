#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0034 statement."""

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
NAMESPACE = "Stage1Instances.THM_M_0034"
THEOREM_ID = "THM-M-0034"
ITEM_ID = "S56-M-0034-STATEMENT"
CANONICAL = "QuillenSuslinTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedFiniteGeneration",
    "mutationChangedDomainToCommRing",
    "mutationChangedBinderScope",
    "mutationIncludedZeroVariables",
)
DIRECT_IMPORTS = (
    "Mathlib.Algebra.Module.Projective",
    "Mathlib.Algebra.MvPolynomial.Basic",
    "Mathlib.RingTheory.Finiteness.Defs",
)
PRINT_MARKER = "#print QuillenSuslinTarget"
EXPECTED_EXPRESSION_SHA256 = "d80cc9860ed5a53c81a0851b4dc8e702aa5a23d448f373ae6d68ed0c9b5604b1"
EXPECTED_STATEMENT_FILE_SHA256 = "cfdfeabe825f5b7936905cee310c2306dba8b18a4b25281fb09c7d10719b79e8"
EXPECTED_LEAN_OUTPUT_SHA256 = "d46e6e6eb71154cf0111b0bc9c35ad1f685ff751634cff457c20a497525c9f6f"
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
EXPECTED_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_BLUEPRINT_SHA256 = "6255ad28de4d483812ad666de286b14c6d2b455aa170c36721e49e031af134b1"
EXPECTED_EXECUTION_DAG_SHA256 = "523bba367128b6089036523b827909c2a8e8af553914964847855e057f492586"
EXPECTED_IMPORT_HASHES = {
    "Mathlib.Algebra.Module.Projective": "43ea6a534f5db642eef41d8138f8b2bf579b13bba8353612f6b40c8c32d1471b",
    "Mathlib.Algebra.MvPolynomial.Basic": "b74bd9ea40166361eabbb6d3131b7cbb49be2dbb08423bfd9647ca7f56eaf23c",
    "Mathlib.RingTheory.Finiteness.Defs": "b655f724f2043f555274767269a6a3a4df4865e644ddc42b55791dc8ee64cabe",
}
EXPECTED_RECEIPT_EXPRESSION_SHA256 = (
    "sha256:d80cc9860ed5a53c81a0851b4dc8e702aa5a23d448f373ae6d68ed0c9b5604b1"
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


def elaborate_expression(declaration: str) -> tuple[str, str]:
    source = SOURCE.read_text(encoding="utf-8")
    if source.count(PRINT_MARKER) != 1:
        raise SystemExit("canonical #print marker must occur exactly once")
    source = source.replace(PRINT_MARKER, f"#print {declaration}")
    result = run_text(source)
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    qualified = re.escape(f"{NAMESPACE}.{declaration}")
    match = re.search(
        rf"def {qualified}\.\{{u, v\}} : Prop :=\n(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip(), result.stdout


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    imports = tuple(re.findall(r"^import ([^\s]+)$", source, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {imports!r}")

    deletion_failures = {}
    for module in DIRECT_IMPORTS:
        probe = source.replace(f"import {module}\n", "", 1)
        result = run_text(probe)
        if result.returncode == 0:
            raise SystemExit(f"direct import is redundant: {module}")
        diagnostic = next(
            (line.strip() for line in result.stdout.splitlines() if "unknown" in line.lower()),
            "Lean rejected the deletion probe",
        )
        deletion_failures[module] = diagnostic

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    if sha256_bytes((ROOT / "Docs" / "Stage1_Blueprint_rev-5.6.md").read_bytes()) != EXPECTED_BLUEPRINT_SHA256:
        raise SystemExit("authoritative blueprint fingerprint changed")
    if sha256_bytes((ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json").read_bytes()) != EXPECTED_EXECUTION_DAG_SHA256:
        raise SystemExit("authoritative execution DAG fingerprint changed")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative statement item identity changed")
    if item["depends_on"] != ["S56-M-0034-INTAKE"]:
        raise SystemExit("authoritative statement dependency changed")
    if item["owned_paths"] != [f"Stage1_Instances/{THEOREM_ID}"]:
        raise SystemExit("authoritative statement ownership changed")

    expressions = {}
    canonical_output = ""
    for declaration in DECLARATIONS:
        expression, output = elaborate_expression(declaration)
        expressions[declaration] = expression
        if declaration == CANONICAL:
            canonical_output = output
    canonical = expressions[CANONICAL]
    survivors = [name for name in DECLARATIONS[1:] if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")
    if len(set(expressions.values())) != len(expressions):
        raise SystemExit("two statement identities unexpectedly share an explicit expression")

    expression_hash = sha256_bytes(canonical.encode("utf-8"))
    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    expected = {
        "expression": EXPECTED_EXPRESSION_SHA256,
        "statement": EXPECTED_STATEMENT_FILE_SHA256,
        "output": EXPECTED_LEAN_OUTPUT_SHA256,
    }
    actual = {
        "expression": expression_hash,
        "statement": statement_file_hash,
        "output": lean_output_hash,
    }
    for kind, value in expected.items():
        if value != actual[kind]:
            raise SystemExit(f"{kind} fingerprint changed without reconciliation")

    statement = load(SOURCE.with_name("statement.json"))
    receipt = load(SOURCE.with_name("statement-receipt.json"))
    instance = load(SOURCE.with_name("instance.json"))
    dag = load(SOURCE.with_name("task-dag.json"))
    if not statement["item_id"] == receipt["item_id"] == ITEM_ID:
        raise SystemExit("statement item identity is stale")
    if not statement["theorem_id"] == receipt["theorem_id"] == instance["theorem_id"] == THEOREM_ID:
        raise SystemExit("statement theorem identity is stale")
    if tuple(statement["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("statement direct-import record is stale")
    formal = statement["canonical_formal_target"]
    if formal["elaborated_expression_sha256"] != expression_hash:
        raise SystemExit("structured expression fingerprint is stale")
    if formal["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("structured source fingerprint is stale")
    if formal["fully_explicit_expression"] != canonical:
        raise SystemExit("structured explicit expression is stale")
    if receipt["statement_fingerprints"] != [EXPECTED_RECEIPT_EXPRESSION_SHA256]:
        raise SystemExit("receipt expression fingerprint is stale")
    if receipt["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("receipt source fingerprint is stale")
    if receipt["lean_output_sha256"] != lean_output_hash:
        raise SystemExit("receipt Lean-output fingerprint is stale")
    if tuple(receipt["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("receipt direct-import record is stale")
    if not receipt["root_vector_before"] == receipt["root_vector_after"] == instance["root_vector"]:
        raise SystemExit("statement debt vector is inconsistent")
    if receipt["audit_complete"] or receipt["theorem_complete"]:
        raise SystemExit("statement receipt overclaims completion")
    instance_formal = instance["canonical_formal_target"]
    if instance_formal["module"] != f"Stage1_Instances/{THEOREM_ID}/Statement.lean":
        raise SystemExit("instance canonical module is stale")
    if instance_formal["declaration_or_expression"] != f"{NAMESPACE}.{CANONICAL}":
        raise SystemExit("instance canonical declaration is stale")
    if instance_formal["elaborated_expression_hash"] != f"sha256:{expression_hash}":
        raise SystemExit("instance expression fingerprint is stale")
    revisions = instance["source_revisions"]
    if revisions["authoritative_blueprint_sha256"] != EXPECTED_BLUEPRINT_SHA256:
        raise SystemExit("instance blueprint fingerprint is stale")
    if revisions["execution_dag_sha256"] != EXPECTED_EXECUTION_DAG_SHA256:
        raise SystemExit("instance execution DAG fingerprint is stale")
    authority = receipt["authority_inputs"]
    if authority["Docs/Stage1_Blueprint_rev-5.6.md"] != f"sha256:{EXPECTED_BLUEPRINT_SHA256}":
        raise SystemExit("receipt blueprint fingerprint is stale")
    if authority["Docs/Stage1_Execution_DAG_rev-5.6.json"] != f"sha256:{EXPECTED_EXECUTION_DAG_SHA256}":
        raise SystemExit("receipt execution DAG fingerprint is stale")
    statement_task = next(task for task in dag["tasks"] if task["id"] == ITEM_ID)
    if statement_task["state"] != "open" or statement_task["depends_on"] != ["S56-M-0034-INTAKE"]:
        raise SystemExit("local statement task boundary changed")

    toolchain_path = LEAN_DIR / "lean-toolchain"
    manifest_path = LEAN_DIR / "lake-manifest.json"
    if toolchain_path.read_text(encoding="utf-8").strip() != EXPECTED_TOOLCHAIN:
        raise SystemExit("Lean toolchain changed")
    if sha256_bytes(toolchain_path.read_bytes()) != EXPECTED_TOOLCHAIN_SHA256:
        raise SystemExit("Lean toolchain fingerprint changed")
    if sha256_bytes(manifest_path.read_bytes()) != EXPECTED_MANIFEST_SHA256:
        raise SystemExit("lake manifest fingerprint changed")
    manifest = load(manifest_path)
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit("mathlib manifest revision changed")
    mathlib = LEAN_DIR / ".lake" / "packages" / "mathlib"
    tree = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, check=True, text=True,
        capture_output=True,
    ).stdout.strip()
    if tree != EXPECTED_MATHLIB_TREE:
        raise SystemExit("mathlib tree changed")
    for module, digest in EXPECTED_IMPORT_HASHES.items():
        path = mathlib / (module.replace(".", "/") + ".lean")
        if sha256_bytes(path.read_bytes()) != digest:
            raise SystemExit(f"direct import source changed: {module}")

    payload = {
        "deletion_failures": deletion_failures,
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "fully_explicit_expression": canonical,
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "statement_file_sha256": statement_file_hash,
        "toolchain": EXPECTED_TOOLCHAIN,
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
