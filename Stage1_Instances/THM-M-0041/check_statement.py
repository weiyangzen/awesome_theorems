#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0041 statement."""

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
BOUNDARY = Path(__file__).with_name("BoundaryProbe.lean")
THEOREM_ID = "THM-M-0041"
ITEM_ID = "S56-M-0041-STATEMENT"
NAMESPACE = "Stage1Instances.THM_M_0041"
CANONICAL = "CayleyHamiltonTarget"
PRINT_MARKER = f"#print {NAMESPACE}.{CANONICAL}"
DECLARATIONS = (
    CANONICAL,
    "mutationChangedDomainToField",
    "mutationChangedMatrixBinderScope",
    "mutationExcludedBoundaries",
)
DIRECT_IMPORTS = (
    "Mathlib.Algebra.Polynomial.AlgebraMap",
    "Mathlib.LinearAlgebra.Matrix.Determinant.Basic",
)
EXPECTED_EXPRESSION_SHA256 = "5aad8415af4578ca43d0ec58eee038ed4470dce17896766215d3bf9f49d8e711"
EXPECTED_STATEMENT_SHA256 = "3b218c1a96922399bb8ed2d852d556422a92901dca10efdd431a677eaefd2b0b"
EXPECTED_BOUNDARY_SHA256 = "ba5758ff5c612108e203007c0b5e04fe239697771540114c4e3938f370135e3e"
EXPECTED_LEAN_OUTPUT_SHA256 = "eccdbbe3150ca0d246e8381821b5b2f3740fbe4a2927c5f239507c781564ffdc"
EXPECTED_IMPORT_HASHES = {
    "Mathlib.Algebra.Polynomial.AlgebraMap":
        "e6db579a99dcbed160c598103c215d07807699dac1fce406db7bbc37b38de228",
    "Mathlib.LinearAlgebra.Matrix.Determinant.Basic":
        "18fd46c88d720a62e6ffc03b220827109dd812caa3a7f51683bb36265aaa9bd8",
}
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
EXPECTED_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_BLUEPRINT_SHA256 = "6255ad28de4d483812ad666de286b14c6d2b455aa170c36721e49e031af134b1"
EXPECTED_EXECUTION_DAG_SHA256 = "523bba367128b6089036523b827909c2a8e8af553914964847855e057f492586"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(path)], cwd=LEAN_DIR, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
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


def explicit_expression(declaration: str) -> tuple[str, str]:
    text = SOURCE.read_text(encoding="utf-8")
    if text.count(PRINT_MARKER) != 1:
        raise SystemExit("canonical #print marker must occur exactly once")
    text = text.replace(PRINT_MARKER, f"#print {NAMESPACE}.{declaration}")
    result = run_text(text)
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    qualified = re.escape(f"{NAMESPACE}.{declaration}")
    match = re.search(
        rf"def {qualified}(?:\.\{{u, v\}})? : Prop :=\n(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip(), result.stdout


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {imports!r}")
    if "Mathlib.LinearAlgebra.Matrix.Charpoly.Basic" in source_text:
        raise SystemExit("proof-bearing charpoly feature module crossed statement boundary")
    candidate_checks = re.findall(
        r"^#check_failure Matrix\.aeval_self_charpoly$", source_text, re.MULTILINE
    )
    if candidate_checks != ["#check_failure Matrix.aeval_self_charpoly"]:
        raise SystemExit("candidate theorem name escaped the negative availability check")

    canonical_header = (
        "def CayleyHamiltonTarget : Prop :=\n"
        "  forall {R : Type u} [CommRing R] {n : Type v}"
    )
    removed_header = (
        "def CayleyHamiltonTarget : Prop :=\n"
        "  forall {R : Type u} {n : Type v}"
    )
    if source_text.count(canonical_header) != 1:
        raise SystemExit("could not construct the removed-CommRing mutation")
    removed_comm_ring = source_text.replace(canonical_header, removed_header, 1)
    removed_result = run_text(removed_comm_ring)
    if removed_result.returncode == 0:
        raise SystemExit("removed CommRing hypothesis unexpectedly elaborated")
    removed_diagnostic = next(
        (line.strip() for line in removed_result.stdout.splitlines()
         if "failed to synthesize" in line.lower() or "application type mismatch" in line.lower()),
        "Lean rejected the removed-CommRing mutation",
    )

    deletion_failures: dict[str, str] = {}
    for module in DIRECT_IMPORTS:
        probe = source_text.replace(f"import {module}\n", "", 1)
        result = run_text(probe)
        if result.returncode == 0:
            raise SystemExit(f"direct import is redundant: {module}")
        diagnostic = next(
            (line.strip() for line in result.stdout.splitlines()
             if "unknown" in line.lower() or "failed to synthesize" in line.lower()),
            "Lean rejected the deletion probe",
        )
        deletion_failures[module] = diagnostic

    boundary_result = run_lean(BOUNDARY)
    if boundary_result.returncode or boundary_result.stdout:
        print(boundary_result.stdout, end="")
        raise SystemExit("empty-index or zero-ring boundary probe failed")
    if sha256_bytes(BOUNDARY.read_bytes()) != EXPECTED_BOUNDARY_SHA256:
        raise SystemExit("boundary source changed without reconciliation")

    blueprint = ROOT / "Docs" / "Stage1_Blueprint_rev-5.6.md"
    execution_path = ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json"
    if sha256_bytes(blueprint.read_bytes()) != EXPECTED_BLUEPRINT_SHA256:
        raise SystemExit("authoritative blueprint changed")
    if sha256_bytes(execution_path.read_bytes()) != EXPECTED_EXECUTION_DAG_SHA256:
        raise SystemExit("authoritative execution DAG changed")
    execution = load(execution_path)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if (item["theorem_id"], item["phase"], item["layer"]) != (THEOREM_ID, "statement", 1):
        raise SystemExit("authoritative statement identity changed")
    if item["depends_on"] != ["S56-M-0041-INTAKE"]:
        raise SystemExit("authoritative statement dependency changed")
    if item["owned_paths"] != [f"Stage1_Instances/{THEOREM_ID}"]:
        raise SystemExit("authoritative statement ownership changed")

    expressions: dict[str, str] = {}
    canonical_output = ""
    for declaration in DECLARATIONS:
        expression, output = explicit_expression(declaration)
        expressions[declaration] = expression
        if declaration == CANONICAL:
            canonical_output = output
    canonical = expressions[CANONICAL]
    if "timeout" in canonical_output.lower() or "heartbeat" in canonical_output.lower():
        raise SystemExit("canonical Lean run contains a timeout or heartbeat diagnostic")
    survivors = [name for name in DECLARATIONS[1:] if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")

    expression_hash = sha256_bytes(canonical.encode("utf-8"))
    statement_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    if expression_hash != EXPECTED_EXPRESSION_SHA256:
        raise SystemExit("elaborated expression changed without reconciliation")
    if statement_hash != EXPECTED_STATEMENT_SHA256:
        raise SystemExit("statement source changed without reconciliation")
    if lean_output_hash != EXPECTED_LEAN_OUTPUT_SHA256:
        raise SystemExit("canonical Lean output changed without reconciliation")

    statement = load(SOURCE.with_name("statement.json"))
    receipt = load(SOURCE.with_name("statement-receipt.json"))
    instance = load(SOURCE.with_name("instance.json"))
    formal = statement["canonical_formal_target"]
    if formal["elaborated_expression_sha256"] != expression_hash:
        raise SystemExit("statement expression fingerprint is stale")
    if formal["statement_file_sha256"] != statement_hash:
        raise SystemExit("statement source fingerprint is stale")
    if formal["serialization"] != (
        "The normalized fully explicit pp.universes=true/pp.explicit=true expression is "
        "reproducibly emitted by Statement.lean; its exact bytes are bound by the expression "
        "and Lean-output SHA-256 values."
    ):
        raise SystemExit("statement serialization policy is stale")
    if statement["boundary_probe_sha256"] != EXPECTED_BOUNDARY_SHA256:
        raise SystemExit("statement boundary fingerprint is stale")
    if tuple(statement["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("statement direct-import inventory is stale")
    if instance["canonical_formal_target"]["elaborated_expression_hash"] != f"sha256:{expression_hash}":
        raise SystemExit("instance expression fingerprint is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
        raise SystemExit("receipt expression fingerprint is stale")
    if receipt["statement_file_sha256"] != statement_hash:
        raise SystemExit("receipt source fingerprint is stale")
    if receipt["lean_output_sha256"] != lean_output_hash:
        raise SystemExit("receipt Lean-output fingerprint is stale")
    if receipt["boundary_probe_sha256"] != EXPECTED_BOUNDARY_SHA256:
        raise SystemExit("receipt boundary fingerprint is stale")

    packet = load(ROOT / ".stage1-worker-selftest.json")
    packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    if set(packet) != packet_fields:
        raise SystemExit("worker packet fields changed")
    if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
        raise SystemExit("worker packet item or state is stale")
    if packet["base_revision"] != receipt["base_revision"]:
        raise SystemExit("worker packet base revision is stale")
    if packet["changed_paths"] != receipt["changed_paths"]:
        raise SystemExit("worker packet changed paths are stale")
    if packet["known_failures"] != receipt["known_failures"]:
        raise SystemExit("worker packet known failures are stale")

    toolchain_path = LEAN_DIR / "lean-toolchain"
    manifest_path = LEAN_DIR / "lake-manifest.json"
    manifest = load(manifest_path)
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    mathlib = LEAN_DIR / ".lake" / "packages" / "mathlib"
    if toolchain_path.read_text(encoding="utf-8").strip() != EXPECTED_TOOLCHAIN:
        raise SystemExit("Lean toolchain pin changed")
    if sha256_bytes(toolchain_path.read_bytes()) != EXPECTED_TOOLCHAIN_SHA256:
        raise SystemExit("toolchain file changed")
    if sha256_bytes(manifest_path.read_bytes()) != EXPECTED_MANIFEST_SHA256:
        raise SystemExit("Lake manifest changed")
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit("manifest mathlib revision changed")
    actual_revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=mathlib, text=True
    ).strip()
    actual_tree = subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, text=True
    ).strip()
    if (actual_revision, actual_tree) != (EXPECTED_MATHLIB_REVISION, EXPECTED_MATHLIB_TREE):
        raise SystemExit("materialized mathlib revision or tree changed")
    for module, expected in EXPECTED_IMPORT_HASHES.items():
        path = mathlib / (module.replace(".", "/") + ".lean")
        if sha256_bytes(path.read_bytes()) != expected:
            raise SystemExit(f"direct import source changed: {module}")

    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True).strip()
    if (receipt["base_revision"], receipt["base_tree"]) != (head, tree):
        raise SystemExit("receipt base revision or tree is stale")

    print(json.dumps({
        "boundary_probe_sha256": EXPECTED_BOUNDARY_SHA256,
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "import_deletion_failures": deletion_failures,
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "statement_file_sha256": statement_hash,
        "toolchain": EXPECTED_TOOLCHAIN,
        "removed_hypothesis_failure": removed_diagnostic,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
