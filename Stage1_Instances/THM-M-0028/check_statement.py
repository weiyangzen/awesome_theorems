#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0028 statement."""

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
BOUNDARY_PROBE = SOURCE.with_name("BoundaryProbe.lean")
NAMESPACE = "Stage1Instances.THM_M_0028"
THEOREM_ID = "THM-M-0028"
ITEM_ID = "S56-M-0028-STATEMENT"
CANONICAL = "IdealAscendingChainTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedFiniteGenerationHypothesis",
    "mutationChangedDomainToField",
    "mutationChangedBinderScope",
    "mutationExcludedZeroRing",
)
TRANSPORTS = (
    "idealAscendingChainTarget_iff_regularSubmoduleAscendingChainTarget",
    "idealAscendingChainTarget_iff_monotoneIdealSequenceTarget",
)
BOUNDARIES = ("subsingleton_boundary_has_no_nontrivial",)
DIRECT_IMPORTS = ("Mathlib.RingTheory.Finiteness.Defs",)
PRINT_MARKER = "#print IdealAscendingChainTarget"
EXPECTED_EXPRESSION_SHA256 = "89e7e911ed4a5b75c153d824133091ad74ba20a0ecab19bd609b23a54badbee4"
EXPECTED_STATEMENT_FILE_SHA256 = "db7cbc8250aa905f1d8a2686ab14e9b31eeeba3409179d22e7169627df02f3a7"
EXPECTED_LEAN_OUTPUT_SHA256 = "5907fd942bbcc236601dd57eef9e94a77df02cfbd0fc6a1606b38de078d256ce"
EXPECTED_BOUNDARY_PROBE_SHA256 = "e7f784feb3b8205bc6a81008b696e53317d63a6beccb69f5b49354ae75a15425"
EXPECTED_IMPORT_HASH = "b655f724f2043f555274767269a6a3a4df4865e644ddc42b55791dc8ee64cabe"
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
EXPECTED_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_BLUEPRINT_SHA256 = "ae0055f65665bc05a0fa8ee2eed39566b036e65a2119be2fa6e4cecd5c1966a9"
EXPECTED_EXECUTION_DAG_SHA256 = "d9506f42dd2de7f8a28e12b9e780931938d99fdc66f42a6698d4032b29a465d1"


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
    result = run_text(source.replace(PRINT_MARKER, f"#print {declaration}"))
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    qualified = re.escape(f"{NAMESPACE}.{declaration}")
    match = re.search(
        rf"def {qualified}(?:\.\{{u\}})? : Prop :=\n(?P<expression>.*)\Z",
        result.stdout, re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip(), result.stdout


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {imports!r}")
    deletion = run_text(source_text.replace(f"import {DIRECT_IMPORTS[0]}\n", "", 1))
    if deletion.returncode == 0:
        raise SystemExit("direct import survived the deletion probe")
    smaller_import = run_text(
        source_text.replace(
            f"import {DIRECT_IMPORTS[0]}", "import Mathlib.RingTheory.Ideal.Defs", 1
        )
    )
    if smaller_import.returncode == 0:
        raise SystemExit("target unexpectedly elaborated with the smaller Ideal.Defs import")

    boundary = run_lean(BOUNDARY_PROBE)
    if boundary.returncode or boundary.stdout:
        print(boundary.stdout, end="")
        raise SystemExit("concrete zero-ring boundary probe failed or produced diagnostics")
    if sha256_bytes(BOUNDARY_PROBE.read_bytes()) != EXPECTED_BOUNDARY_PROBE_SHA256:
        raise SystemExit("boundary probe source changed without reconciliation")

    blueprint = ROOT / "Docs" / "Stage1_Blueprint_rev-5.6.md"
    execution_path = ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json"
    if sha256_bytes(blueprint.read_bytes()) != EXPECTED_BLUEPRINT_SHA256:
        raise SystemExit("authoritative blueprint hash changed")
    if sha256_bytes(execution_path.read_bytes()) != EXPECTED_EXECUTION_DAG_SHA256:
        raise SystemExit("authoritative execution DAG hash changed")
    execution = load(execution_path)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative statement identity changed")
    if item["depends_on"] != ["S56-M-0028-INTAKE"]:
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
    survivors = [name for name in DECLARATIONS[1:] if expressions[name] == expressions[CANONICAL]]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")
    for name in TRANSPORTS + BOUNDARIES:
        if not re.search(rf"^theorem {re.escape(name)}\b", source_text, re.MULTILINE):
            raise SystemExit(f"missing statement witness: {name}")

    expression_hash = sha256_bytes(expressions[CANONICAL].encode("utf-8"))
    source_hash = sha256_bytes(SOURCE.read_bytes())
    output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    if expression_hash != EXPECTED_EXPRESSION_SHA256:
        raise SystemExit("elaborated expression changed without reconciliation")
    if source_hash != EXPECTED_STATEMENT_FILE_SHA256:
        raise SystemExit("statement source changed without reconciliation")
    if output_hash != EXPECTED_LEAN_OUTPUT_SHA256:
        raise SystemExit("canonical Lean output changed without reconciliation")

    statement = load(SOURCE.with_name("statement.json"))
    receipt = load(SOURCE.with_name("statement-receipt.json"))
    instance = load(SOURCE.with_name("instance.json"))
    formal = statement["canonical_formal_target"]
    if tuple(statement["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("structured direct imports are stale")
    if formal["elaborated_expression_sha256"] != expression_hash:
        raise SystemExit("structured expression fingerprint is stale")
    if formal["statement_file_sha256"] != source_hash:
        raise SystemExit("structured source fingerprint is stale")
    if formal["fully_explicit_expression"] != " ".join(expressions[CANONICAL].split()):
        raise SystemExit("persisted explicit expression is stale")
    if statement["boundary_probe_sha256"] != EXPECTED_BOUNDARY_PROBE_SHA256:
        raise SystemExit("structured boundary fingerprint is stale")
    if instance["canonical_formal_target"]["elaborated_expression_hash"] != f"sha256:{expression_hash}":
        raise SystemExit("instance expression fingerprint is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
        raise SystemExit("receipt expression fingerprint is stale")
    if receipt["statement_file_sha256"] != source_hash or receipt["lean_output_sha256"] != output_hash:
        raise SystemExit("receipt source or output fingerprint is stale")
    expected_mutations = [
        {"kind": kind, "declaration": declaration}
        for kind, declaration in zip(
            ("removed_hypothesis", "changed_domain", "changed_binder_scope", "boundary_case"),
            DECLARATIONS[1:],
        )
    ]
    if statement["mutation_tests"]["killed"] != expected_mutations:
        raise SystemExit("structured mutation inventory is stale")
    if [row["declaration"] for row in receipt["mutation_tests"]] != list(DECLARATIONS[1:]):
        raise SystemExit("receipt mutation inventory is stale")
    witnesses = [f"{NAMESPACE}.{name}" for name in TRANSPORTS]
    if [row["checked_witness"] for row in statement["checked_alternate_encodings"]] != witnesses:
        raise SystemExit("structured transport inventory is stale")
    if receipt["checked_transports"] != witnesses:
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
    packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    if set(packet) != packet_fields:
        raise SystemExit("worker packet fields changed")
    if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
        raise SystemExit("worker packet identity changed")
    if packet["base_revision"] != receipt["base_revision"]:
        raise SystemExit("worker packet base revision is stale")
    if packet["changed_paths"] != receipt["changed_paths"]:
        raise SystemExit("worker packet changed paths are stale")
    if packet["known_failures"] != receipt["known_failures"]:
        raise SystemExit("worker packet known failures are stale")

    manifest = load(LEAN_DIR / "lake-manifest.json")
    mathlib_revision = next(row["rev"] for row in manifest["packages"] if row["name"] == "mathlib")
    mathlib = LEAN_DIR / ".lake" / "packages" / "mathlib"
    toolchain = (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip()
    actual_revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=mathlib, check=True,
        text=True, capture_output=True,
    ).stdout.strip()
    actual_tree = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, check=True,
        text=True, capture_output=True,
    ).stdout.strip()
    if toolchain != EXPECTED_TOOLCHAIN:
        raise SystemExit("Lean toolchain pin changed")
    if sha256_bytes((LEAN_DIR / "lean-toolchain").read_bytes()) != EXPECTED_TOOLCHAIN_SHA256:
        raise SystemExit("Lean toolchain hash changed")
    if sha256_bytes((LEAN_DIR / "lake-manifest.json").read_bytes()) != EXPECTED_MANIFEST_SHA256:
        raise SystemExit("Lake manifest hash changed")
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit("manifest mathlib revision changed")
    if actual_revision != EXPECTED_MATHLIB_REVISION or actual_tree != EXPECTED_MATHLIB_TREE:
        raise SystemExit("materialized mathlib revision or tree changed")
    import_path = mathlib / "Mathlib/RingTheory/Finiteness/Defs.lean"
    if sha256_bytes(import_path.read_bytes()) != EXPECTED_IMPORT_HASH:
        raise SystemExit("direct import source changed")

    print(json.dumps({
        "boundary_probe_sha256": EXPECTED_BOUNDARY_PROBE_SHA256,
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "import_deletion_exit": deletion.returncode,
        "smaller_import_exit": smaller_import.returncode,
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": output_hash,
        "mathlib_revision": actual_revision,
        "statement_file_sha256": source_hash,
        "toolchain": toolchain,
        "transports": list(TRANSPORTS),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
