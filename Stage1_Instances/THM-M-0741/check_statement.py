#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0741 statement."""

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
NAMESPACE = "Stage1Instances.THM_M_0741"
THEOREM_ID = "THM-M-0741"
ITEM_ID = "S56-M-0741-STATEMENT"
CANONICAL = "HaltingProblemUndecidable"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedEffectivity",
    "mutationChangedDomainToPrograms",
    "mutationChangedBinderScope",
    "mutationChangedBoundaryToSelfInput",
)
BOUNDARIES = ("zero_halts", "rfind_succ_does_not_halt")
TRANSPORT = "haltingProblemUndecidable_iff_expanded"
DIRECT_IMPORT = "Mathlib.Computability.Halting"
WEAKER_IMPORT = "Mathlib.Computability.PartrecCode"
PRINT_MARKER = "#print HaltingProblemUndecidable"
EXPECTED_EXPRESSION_SHA256 = "1a96ad274a14ef0c7285734258d28a7ff6e49febe1470bfbb957d757a92e718c"
EXPECTED_STATEMENT_FILE_SHA256 = "79e8f14fa5219760ef0fa3b26c95ebe40916f0ed2881a6491fce36944398d4c7"
EXPECTED_LEAN_OUTPUT_SHA256 = "497f631dcf379ceda776d1fa348273e291933508150eb51857d647a9f6cb579e"
EXPECTED_BASE_REVISION = "d05520867fab3367a9b61b9544c3e12241204f54"
EXPECTED_BASE_TREE = "fb2cfc62077d5b53e9938632cd6361dd60872067"
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
EXPECTED_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_IMPORT_SHA256 = "c2a073a05c631e7fc957577a66025e9ac36dac741f9aa865e0f053b17f0c85de"


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


def explicit_expression(declaration: str) -> tuple[str, str]:
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
        rf"def {qualified} : Prop :=\n(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"could not extract explicit expression for {declaration}")
    return match.group("expression").strip(), result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, text=True, capture_output=True
    ).stdout.strip()


def check_reconciled(actual: str, expected: str, label: str) -> None:
    if actual != expected:
        raise SystemExit(f"{label} changed without reconciliation: {actual}")


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    imports = re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE)
    if imports != [DIRECT_IMPORT]:
        raise SystemExit(f"direct imports changed: {imports!r}")

    weaker = run_text(source_text.replace(DIRECT_IMPORT, WEAKER_IMPORT, 1))
    if weaker.returncode == 0 or "Unknown identifier `ComputablePred`" not in weaker.stdout:
        raise SystemExit("minimal-import negative probe did not reject ComputablePred")

    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative statement item identity changed")
    if item["state"] != "[ ]" or item["depends_on"] != ["S56-M-0741-INTAKE"]:
        raise SystemExit("authoritative statement state or dependency changed")
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
    survivors = [name for name in DECLARATIONS[1:] if expressions[name] == canonical]
    if survivors:
        raise SystemExit(f"statement mutation survived: {', '.join(survivors)}")
    for name in BOUNDARIES + (TRANSPORT,):
        if not re.search(rf"^(theorem|def) {re.escape(name)}\b", source_text, re.MULTILINE):
            raise SystemExit(f"missing boundary or transport declaration: {name}")

    expression_hash = sha256_bytes(canonical.encode("utf-8"))
    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    check_reconciled(expression_hash, EXPECTED_EXPRESSION_SHA256, "elaborated expression")
    check_reconciled(statement_file_hash, EXPECTED_STATEMENT_FILE_SHA256, "statement source")
    check_reconciled(lean_output_hash, EXPECTED_LEAN_OUTPUT_SHA256, "canonical Lean output")

    statement = load(SOURCE.with_name("statement.json"))
    receipt = load(SOURCE.with_name("statement-receipt.json"))
    instance = load(SOURCE.with_name("instance.json"))
    formal = statement["canonical_formal_target"]
    if statement["direct_imports"] != [DIRECT_IMPORT]:
        raise SystemExit("structured direct imports are stale")
    if formal["elaborated_expression_sha256"] != expression_hash:
        raise SystemExit("structured expression fingerprint is stale")
    if formal["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("structured source fingerprint is stale")
    if formal["fully_explicit_expression"] != " ".join(canonical.split()):
        raise SystemExit("persisted fully explicit expression is stale")
    instance_formal = instance["canonical_formal_target"]
    if instance_formal["elaborated_expression_hash"] != f"sha256:{expression_hash}":
        raise SystemExit("instance expression fingerprint is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
        raise SystemExit("receipt expression fingerprint is stale")
    if receipt["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("receipt source fingerprint is stale")
    if receipt["lean_output_sha256"] != lean_output_hash:
        raise SystemExit("receipt Lean-output fingerprint is stale")

    if git("rev-parse", "HEAD") != EXPECTED_BASE_REVISION:
        raise SystemExit("base revision changed")
    if git("rev-parse", "HEAD^{tree}") != EXPECTED_BASE_TREE:
        raise SystemExit("base tree changed")
    if receipt["base_revision"] != EXPECTED_BASE_REVISION or receipt["base_tree"] != EXPECTED_BASE_TREE:
        raise SystemExit("receipt base identity is stale")

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
    if (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip() != EXPECTED_TOOLCHAIN:
        raise SystemExit("Lean toolchain pin changed")
    if sha256_bytes((LEAN_DIR / "lean-toolchain").read_bytes()) != EXPECTED_TOOLCHAIN_SHA256:
        raise SystemExit("Lean toolchain hash changed")
    if sha256_bytes((LEAN_DIR / "lake-manifest.json").read_bytes()) != EXPECTED_MANIFEST_SHA256:
        raise SystemExit("Lake manifest hash changed")
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        raise SystemExit("mathlib manifest revision changed")
    if git("rev-parse", "HEAD", cwd=mathlib) != EXPECTED_MATHLIB_REVISION:
        raise SystemExit("materialized mathlib revision changed")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != EXPECTED_MATHLIB_TREE:
        raise SystemExit("materialized mathlib tree changed")
    import_path = mathlib / (DIRECT_IMPORT.replace(".", "/") + ".lean")
    if sha256_bytes(import_path.read_bytes()) != EXPECTED_IMPORT_SHA256:
        raise SystemExit("direct import source changed")

    payload = {
        "direct_imports": [DIRECT_IMPORT],
        "expression_sha256": expression_hash,
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "minimal_import_negative_exit": weaker.returncode,
        "statement_file_sha256": statement_file_hash,
        "toolchain": EXPECTED_TOOLCHAIN,
        "transports": [TRANSPORT],
        "validated_boundaries": list(BOUNDARIES),
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
