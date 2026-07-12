#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0025 statement."""

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
NAMESPACE = "Stage1Instances.THM_M_0025"
THEOREM_ID = "THM-M-0025"
ITEM_ID = "S56-M-0025-STATEMENT"
CANONICAL = "HilbertBasisTheoremTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedNoetherianHypothesis",
    "mutationChangedDomainToField",
    "mutationChangedBinderScope",
    "mutationExcludedZeroRing",
)
TRANSPORTS = ("hilbertBasisTheoremTarget_iff_idealFiniteGenerationTarget",)
BOUNDARIES = ("subsingleton_boundary_has_no_nontrivial",)
BOUNDARY_PROBE = SOURCE.with_name("BoundaryProbe.lean")
DIRECT_IMPORTS = (
    "Mathlib.Algebra.Polynomial.Basic",
    "Mathlib.RingTheory.Noetherian.Defs",
)
PRINT_MARKER = "#print HilbertBasisTheoremTarget"
EXPECTED_EXPRESSION_SHA256 = "9bb5ed6dd01550f3481d4a66e1d81009272b717997f9752ff422029da2828564"
EXPECTED_STATEMENT_FILE_SHA256 = "d629f0c46384939ddcbaa4c35c3e1c75bb41d39ec3b79cb7355c174028186f6c"
EXPECTED_LEAN_OUTPUT_SHA256 = "d805957a55784cf248c6128716f7533d30dbd909925f07b029d49aa1c65c1b02"
EXPECTED_BOUNDARY_PROBE_SHA256 = "ba87d3d82c98a50e53bb3ef60c5038af0b72d5690c568ddefeaf21fe11c5e093"
EXPECTED_IMPORT_HASHES = {
    "Mathlib.Algebra.Polynomial.Basic": "496e0db20f617473734767d6ae3ab6dd52bac0fec1264e0272353ae7701e4643",
    "Mathlib.RingTheory.Noetherian.Defs": "a0e5c5a1aceb564f885573d5c51ec124be20abbd19fabc6af8c798b637530f0b",
}
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
EXPECTED_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_BLUEPRINT_SHA256 = "001dd6c3c6ccc1b1910f0c51201f534f9e37c29df4f5d09a894f1cf30aa116eb"
EXPECTED_EXECUTION_DAG_SHA256 = "203319f482338106f0e568a85379df8a0434a560b7778b2a7137621df00af3d3"


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


def run_text(text: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", encoding="utf-8", delete=False
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        return run_lean(temporary)
    finally:
        temporary.unlink()


def elaborate_expression(declaration: str) -> tuple[str, str]:
    text = SOURCE.read_text(encoding="utf-8")
    if text.count(PRINT_MARKER) != 1:
        raise SystemExit("canonical #print marker must occur exactly once")
    text = text.replace(PRINT_MARKER, f"#print {declaration}")
    result = run_text(text)
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    qualified = re.escape(f"{NAMESPACE}.{declaration}")
    match = re.search(
        rf"def {qualified}(?:\.\{{u\}})? : Prop :=\n(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip(), result.stdout


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    actual_imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if actual_imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {actual_imports!r}")
    if "Mathlib.RingTheory.Polynomial.Basic" in source_text:
        raise SystemExit("proof-bearing Hilbert basis module crossed the statement boundary")

    deletion_failures: dict[str, str] = {}
    for module in DIRECT_IMPORTS:
        probe = source_text.replace(f"import {module}\n", "", 1)
        result = run_text(probe)
        if result.returncode == 0:
            raise SystemExit(f"direct import is redundant under deletion probe: {module}")
        diagnostic = next(
            (line.strip() for line in result.stdout.splitlines() if "unknown" in line.lower()),
            "Lean rejected the deletion probe",
        )
        deletion_failures[module] = diagnostic

    boundary_result = run_lean(BOUNDARY_PROBE)
    if boundary_result.returncode or boundary_result.stdout:
        print(boundary_result.stdout, end="")
        raise SystemExit("concrete zero-ring boundary probe failed or produced diagnostics")
    if sha256_bytes(BOUNDARY_PROBE.read_bytes()) != EXPECTED_BOUNDARY_PROBE_SHA256:
        raise SystemExit("boundary probe source changed without reconciliation")

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    if sha256_bytes((ROOT / "Docs" / "Stage1_Blueprint_rev-5.6.md").read_bytes()) != EXPECTED_BLUEPRINT_SHA256:
        raise SystemExit("authoritative blueprint hash changed")
    if sha256_bytes((ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json").read_bytes()) != EXPECTED_EXECUTION_DAG_SHA256:
        raise SystemExit("authoritative execution DAG hash changed")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative statement item identity changed")
    if item["depends_on"] != ["S56-M-0025-INTAKE"]:
        raise SystemExit("authoritative statement dependency changed")
    if item["owned_paths"] != [f"Stage1_Instances/{THEOREM_ID}"]:
        raise SystemExit("authoritative statement ownership changed")

    expressions: dict[str, str] = {}
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

    for name in TRANSPORTS + BOUNDARIES:
        if not re.search(rf"^theorem {re.escape(name)}\b", source_text, re.MULTILINE):
            raise SystemExit(f"missing transport or boundary declaration: {name}")

    expression_hash = sha256_bytes(canonical.encode("utf-8"))
    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    if expression_hash != EXPECTED_EXPRESSION_SHA256:
        raise SystemExit("elaborated expression changed without reconciliation")
    if statement_file_hash != EXPECTED_STATEMENT_FILE_SHA256:
        raise SystemExit("statement source changed without reconciliation")
    if lean_output_hash != EXPECTED_LEAN_OUTPUT_SHA256:
        raise SystemExit("canonical Lean output changed without reconciliation")

    statement = load(SOURCE.with_name("statement.json"))
    receipt = load(SOURCE.with_name("statement-receipt.json"))
    instance = load(SOURCE.with_name("instance.json"))
    formal = statement["canonical_formal_target"]
    if tuple(statement["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("structured statement direct imports are stale")
    if formal["elaborated_expression_sha256"] != expression_hash:
        raise SystemExit("structured statement expression fingerprint is stale")
    if formal["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("structured statement source fingerprint is stale")
    if statement["boundary_probe_sha256"] != EXPECTED_BOUNDARY_PROBE_SHA256:
        raise SystemExit("structured boundary probe fingerprint is stale")
    normalized_explicit = " ".join(canonical.split())
    if formal["fully_explicit_expression"] != normalized_explicit:
        raise SystemExit("persisted fully explicit expression is stale")
    if instance["canonical_formal_target"]["elaborated_expression_hash"] != f"sha256:{expression_hash}":
        raise SystemExit("instance expression fingerprint is stale")
    revisions = instance["source_revisions"]
    if revisions["authoritative_blueprint_sha256"] != EXPECTED_BLUEPRINT_SHA256:
        raise SystemExit("instance blueprint hash is stale")
    if revisions["execution_dag_sha256"] != EXPECTED_EXECUTION_DAG_SHA256:
        raise SystemExit("instance execution DAG hash is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
        raise SystemExit("receipt expression fingerprint is stale")
    if receipt["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("receipt statement source fingerprint is stale")
    if receipt["boundary_probe_sha256"] != EXPECTED_BOUNDARY_PROBE_SHA256:
        raise SystemExit("receipt boundary probe fingerprint is stale")
    if receipt["lean_output_sha256"] != lean_output_hash:
        raise SystemExit("receipt Lean-output fingerprint is stale")
    if tuple(receipt["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("receipt direct-import record is stale")
    expected_mutations = [
        {"kind": kind, "declaration": declaration}
        for kind, declaration in zip(
            ("removed_hypothesis", "changed_domain", "changed_binder_scope", "boundary_case"),
            DECLARATIONS[1:],
        )
    ]
    if statement["mutation_tests"]["killed"] != expected_mutations:
        raise SystemExit("structured mutation inventory is stale")
    if [item["declaration"] for item in receipt["mutation_tests"]] != list(DECLARATIONS[1:]):
        raise SystemExit("receipt mutation inventory is stale")
    if statement["checked_alternate_encodings"][0]["checked_witness"] != f"{NAMESPACE}.{TRANSPORTS[0]}":
        raise SystemExit("structured transport inventory is stale")
    if receipt["checked_transports"] != [f"{NAMESPACE}.{TRANSPORTS[0]}"]:
        raise SystemExit("receipt transport inventory is stale")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
        text=True, capture_output=True,
    ).stdout.strip()
    tree = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, check=True,
        text=True, capture_output=True,
    ).stdout.strip()
    if receipt["base_revision"] != head or receipt["base_tree"] != tree:
        raise SystemExit("receipt base revision or tree is stale")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    required_packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    if set(packet) != required_packet_fields:
        raise SystemExit("worker packet fields changed")
    if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
        raise SystemExit("worker packet item or state is stale")
    if packet["base_revision"] != receipt["base_revision"]:
        raise SystemExit("worker packet base revision is stale")
    if packet["changed_paths"] != receipt["changed_paths"]:
        raise SystemExit("worker packet changed paths are stale")
    if packet["known_failures"] != receipt["known_failures"]:
        raise SystemExit("worker packet known failures are stale")

    manifest = load(LEAN_DIR / "lake-manifest.json")
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    mathlib = LEAN_DIR / ".lake" / "packages" / "mathlib"
    toolchain = (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip()
    if toolchain != EXPECTED_TOOLCHAIN:
        raise SystemExit("Lean toolchain pin changed")
    if sha256_bytes((LEAN_DIR / "lean-toolchain").read_bytes()) != EXPECTED_TOOLCHAIN_SHA256:
        raise SystemExit("Lean toolchain file hash changed")
    if sha256_bytes((LEAN_DIR / "lake-manifest.json").read_bytes()) != EXPECTED_MANIFEST_SHA256:
        raise SystemExit("Lake manifest hash changed")
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit("mathlib manifest revision changed")
    actual_revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=mathlib, check=True,
        text=True, capture_output=True,
    ).stdout.strip()
    actual_tree = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, check=True,
        text=True, capture_output=True,
    ).stdout.strip()
    if actual_revision != EXPECTED_MATHLIB_REVISION or actual_tree != EXPECTED_MATHLIB_TREE:
        raise SystemExit("materialized mathlib revision or tree changed")
    environment = receipt["environment"]
    if environment["mathlib_revision"] != actual_revision or environment["mathlib_tree"] != actual_tree:
        raise SystemExit("receipt mathlib environment is stale")
    if environment["lean_toolchain_sha256"] != EXPECTED_TOOLCHAIN_SHA256:
        raise SystemExit("receipt toolchain hash is stale")
    if environment["lake_manifest_sha256"] != EXPECTED_MANIFEST_SHA256:
        raise SystemExit("receipt manifest hash is stale")
    structured_environment = statement["environment_fingerprint"]
    if structured_environment["mathlib_revision"] != actual_revision:
        raise SystemExit("statement mathlib revision is stale")
    if structured_environment["mathlib_tree"] != actual_tree:
        raise SystemExit("statement mathlib tree is stale")
    if structured_environment["lean_toolchain_file_sha256"] != EXPECTED_TOOLCHAIN_SHA256:
        raise SystemExit("statement toolchain hash is stale")
    if structured_environment["lake_manifest_sha256"] != EXPECTED_MANIFEST_SHA256:
        raise SystemExit("statement manifest hash is stale")
    for module, expected in EXPECTED_IMPORT_HASHES.items():
        path = mathlib / (module.replace(".", "/") + ".lean")
        if sha256_bytes(path.read_bytes()) != expected:
            raise SystemExit(f"direct import source changed: {module}")

    payload = {
        "direct_imports": list(DIRECT_IMPORTS),
        "import_deletion_failures": deletion_failures,
        "expression_sha256": expression_hash,
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "statement_file_sha256": statement_file_hash,
        "toolchain": toolchain,
        "transports": list(TRANSPORTS),
        "validated_boundaries": list(BOUNDARIES),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
