#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0032 statement."""

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
NAMESPACE = "Stage1Instances.THM_M_0032"
THEOREM_ID = "THM-M-0032"
ITEM_ID = "S56-M-0032-STATEMENT"
CANONICAL = "AuslanderBuchsbaumUFDTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedRegularityHypothesis",
    "mutationChangedDomainToField",
    "mutationChangedBinderScope",
    "mutationExcludedFieldBoundary",
)
TRANSPORT = "auslanderBuchsbaumUFDTarget_iff_explicitRegularityTarget"
DIRECT_IMPORT = "Mathlib.RingTheory.RegularLocalRing.Defs"
PRINT_MARKER = "#print AuslanderBuchsbaumUFDTarget"
EXPECTED_EXPRESSION_SHA256 = "199d16d669438ea6e1cd556adbc4a9475805acf048379e01ae1a1f75f453a8d8"
EXPECTED_STATEMENT_FILE_SHA256 = "5391ab5cef4895413e28fcabe5a3e23e7b93aeea643c1fbae991223c34c07f3a"
EXPECTED_LEAN_OUTPUT_SHA256 = "2a26d392cff0eab1fc3a25aed89898827f02c059f9dc7c4f21748ab0c86637d1"
EXPECTED_IMPORT_SHA256 = "3031d9946232a1d726a4556d0674632345b0877f049a23c104c495f5b2128c6f"
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
EXPECTED_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_BASE_REVISION = "94f6abf9359f26384e0f68bef694dc5b9aae624c"
EXPECTED_BASE_TREE = "e0083f4f402c93febe4419b51498afa8ecf81c06"
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


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, text=True, capture_output=True
    ).stdout.strip()


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    imports = re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE)
    if imports != [DIRECT_IMPORT]:
        raise SystemExit(f"direct imports changed: {imports!r}")

    deletion = run_text(source_text.replace(f"import {DIRECT_IMPORT}\n", "", 1))
    if deletion.returncode == 0:
        raise SystemExit("the sole direct import is redundant under deletion probe")

    blueprint = ROOT / "Docs" / "Stage1_Blueprint_rev-5.6.md"
    execution_path = ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json"
    if sha256_bytes(blueprint.read_bytes()) != EXPECTED_BLUEPRINT_SHA256:
        raise SystemExit("authoritative blueprint hash changed")
    if sha256_bytes(execution_path.read_bytes()) != EXPECTED_EXECUTION_DAG_SHA256:
        raise SystemExit("authoritative execution DAG hash changed")
    execution = load(execution_path)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative statement item identity changed")
    if item["state"] != "[ ]" or item["depends_on"] != ["S56-M-0032-INTAKE"]:
        raise SystemExit("authoritative statement state or dependency changed")
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
    if not re.search(rf"^theorem {TRANSPORT}\b", source_text, re.MULTILINE):
        raise SystemExit("checked transport declaration is missing")

    expression_hash = sha256_bytes(canonical.encode("utf-8"))
    statement_file_hash = sha256_bytes(SOURCE.read_bytes())
    lean_output_hash = sha256_bytes(canonical_output.encode("utf-8"))
    if expression_hash != EXPECTED_EXPRESSION_SHA256:
        raise SystemExit(f"elaborated expression changed: {expression_hash}")
    if statement_file_hash != EXPECTED_STATEMENT_FILE_SHA256:
        raise SystemExit("statement source changed without reconciliation")
    if lean_output_hash != EXPECTED_LEAN_OUTPUT_SHA256:
        raise SystemExit("canonical Lean output changed without reconciliation")

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
    if instance["canonical_formal_target"]["elaborated_expression_hash"] != f"sha256:{expression_hash}":
        raise SystemExit("instance expression fingerprint is stale")
    revisions = instance["source_revisions"]
    if revisions["authoritative_blueprint_sha256"] != EXPECTED_BLUEPRINT_SHA256:
        raise SystemExit("instance blueprint fingerprint is stale")
    if revisions["execution_dag_sha256"] != EXPECTED_EXECUTION_DAG_SHA256:
        raise SystemExit("instance execution DAG fingerprint is stale")
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
        "import_deletion_exit": deletion.returncode,
        "killed_mutations": list(DECLARATIONS[1:]),
        "lean_output_sha256": lean_output_hash,
        "mathlib_revision": mathlib_revision,
        "statement_file_sha256": statement_file_hash,
        "toolchain": EXPECTED_TOOLCHAIN,
        "transports": [TRANSPORT],
        "validated_boundaries": ["Rat is a regular local field"],
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
