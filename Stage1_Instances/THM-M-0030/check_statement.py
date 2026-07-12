#!/usr/bin/env python3
"""Elaborate, fingerprint, and mutation-test the THM-M-0030 statement."""

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
NAMESPACE = "Stage1Instances.THM_M_0030"
THEOREM_ID = "THM-M-0030"
ITEM_ID = "S56-M-0030-STATEMENT"
CANONICAL = "KrullIntersectionTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedPropernessHypothesis",
    "mutationChangedDomainToField",
    "mutationChangedBinderScope",
    "mutationExcludedBottomIdeal",
)
TRANSPORTS = ("krullIntersectionTarget_iff_membershipTarget",)
BOUNDARIES = ("topIdeal_is_counterboundary", "bottomIdeal_is_in_scope")
DIRECT_IMPORTS = (
    "Mathlib.RingTheory.Ideal.Operations",
    "Mathlib.RingTheory.LocalRing.Defs",
    "Mathlib.RingTheory.Noetherian.Defs",
)
PRINT_MARKER = "#print KrullIntersectionTarget"
EXPECTED_EXPRESSION_SHA256 = "53389852e2c0875086c2c28cb4a60448670ee29145e13d86b4b1ad3e9df8861e"
EXPECTED_STATEMENT_FILE_SHA256 = "737a2cf8a656d39617aecf8aa7d8b2bb3d5739807ea34f6e75dbb833f3c6978e"
EXPECTED_LEAN_OUTPUT_SHA256 = "26a2d4c8d7d8483e6e70bda65fa23251554cd7a3a85f30e7ac3ec1cc9801ef3a"
EXPECTED_IMPORT_HASHES = {
    "Mathlib.RingTheory.Ideal.Operations": "b2eea143191f8a7aad35c34eb664a8b4e251438fb8fe6a1095aea81befcecea9",
    "Mathlib.RingTheory.LocalRing.Defs": "a1bd9c72c95745af2c58f093cecf1a2d344982e130a877273a3a55968902b55f",
    "Mathlib.RingTheory.Noetherian.Defs": "a0e5c5a1aceb564f885573d5c51ec124be20abbd19fabc6af8c798b637530f0b",
}
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
    expression = match.group("expression").strip()
    if "⋯" in expression or "sorryAx" in result.stdout:
        raise SystemExit(f"truncated or placeholder-bearing expression for {declaration}")
    return expression, result.stdout


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    actual_imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if actual_imports != DIRECT_IMPORTS:
        raise SystemExit(f"direct imports changed: {actual_imports!r}")
    if "Mathlib.RingTheory.Filtration" in source_text:
        raise SystemExit("proof-bearing Krull intersection module crossed the statement boundary")

    deletion_failures: dict[str, str] = {}
    for module in DIRECT_IMPORTS:
        probe = source_text.replace(f"import {module}\n", "", 1)
        result = run_text(probe)
        if result.returncode == 0:
            raise SystemExit(f"direct import is redundant under deletion probe: {module}")
        diagnostic = next(
            (
                line.strip()
                for line in result.stdout.splitlines()
                if "unknown" in line.lower() or "synthinstancefailed" in line.lower()
            ),
            "Lean rejected the deletion probe",
        )
        deletion_failures[module] = diagnostic

    execution_path = ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json"
    blueprint_path = ROOT / "Docs" / "Stage1_Blueprint_rev-5.6.md"
    if sha256_bytes(blueprint_path.read_bytes()) != EXPECTED_BLUEPRINT_SHA256:
        raise SystemExit("authoritative blueprint hash changed")
    if sha256_bytes(execution_path.read_bytes()) != EXPECTED_EXECUTION_DAG_SHA256:
        raise SystemExit("authoritative execution DAG hash changed")
    execution = load(execution_path)
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if item["theorem_id"] != THEOREM_ID or item["phase"] != "statement" or item["layer"] != 1:
        raise SystemExit("authoritative statement item identity changed")
    if item["depends_on"] != ["S56-M-0030-INTAKE"]:
        raise SystemExit("authoritative statement dependency changed")
    if item["owned_paths"] != [f"Stage1_Instances/{THEOREM_ID}"]:
        raise SystemExit("authoritative statement ownership changed")

    dag = load(SOURCE.with_name("task-dag.json"))
    local_task = next(row for row in dag["tasks"] if row["id"] == ITEM_ID)
    if local_task["state"] != "open" or local_task["evidence_ids"] != []:
        raise SystemExit("worker must not accept or mutate authoritative statement state")
    if "master acceptance" not in local_task.get("first_blocker", ""):
        raise SystemExit("local statement handoff boundary is stale")

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
    if receipt.get("schema_version") != "stage1-provisional-receipt/1.0":
        raise SystemExit("receipt schema changed")
    if receipt.get("item_id") != ITEM_ID or receipt.get("theorem_id") != THEOREM_ID:
        raise SystemExit("receipt identity changed")
    if receipt.get("phase") != "statement" or receipt.get("intent") != "statement":
        raise SystemExit("receipt phase or intent changed")
    if receipt.get("accepted") is not False or receipt.get("proposed_state") != "[_]":
        raise SystemExit("worker receipt may not claim master acceptance")
    if receipt.get("verdict") != "no_state_change":
        raise SystemExit("worker receipt verdict changed")
    if receipt.get("accepted_receipt_ids") != []:
        raise SystemExit("worker receipt may not add accepted receipts")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        raise SystemExit("worker receipt may not claim completion")
    instance_formal = instance.get("canonical_formal_target", {})
    if instance.get("theorem_id") != THEOREM_ID or instance.get("root_vector") != {
        "H": "H1", "M": "M3", "R": "R3"
    }:
        raise SystemExit("instance identity or debt vector changed")
    if instance_formal.get("module") != f"Stage1_Instances/{THEOREM_ID}/Statement.lean":
        raise SystemExit("instance canonical module is stale")
    if instance_formal.get("declaration_or_expression") != f"{NAMESPACE}.{CANONICAL}":
        raise SystemExit("instance canonical declaration is stale")
    if instance_formal.get("elaborated_expression_hash") != f"sha256:{EXPECTED_EXPRESSION_SHA256}":
        raise SystemExit("instance canonical expression fingerprint is stale")
    if instance.get("alternate_encodings", [{}])[0].get("checked_witness") != f"{NAMESPACE}.{TRANSPORTS[0]}":
        raise SystemExit("instance checked transport is stale")
    if instance.get("accepted_receipt_ids") != [] or instance.get("accepted_proof_state") != []:
        raise SystemExit("worker instance may not claim accepted proof state")
    if instance.get("audit_complete") is not False or instance.get("theorem_complete") is not False:
        raise SystemExit("worker instance may not claim completion")
    formal = statement["canonical_formal_target"]
    if tuple(statement["direct_imports"]) != DIRECT_IMPORTS:
        raise SystemExit("structured statement direct imports are stale")
    if formal["elaborated_expression_sha256"] != expression_hash:
        raise SystemExit("structured statement expression fingerprint is stale")
    if formal["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("structured statement source fingerprint is stale")
    if formal["fully_explicit_expression"] != " ".join(canonical.split()):
        raise SystemExit("persisted fully explicit expression is stale")
    if receipt["statement_fingerprints"] != [f"sha256:{expression_hash}"]:
        raise SystemExit("receipt expression fingerprint is stale")
    if receipt["statement_file_sha256"] != statement_file_hash:
        raise SystemExit("receipt statement source fingerprint is stale")
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
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.strip()
    tree = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, check=True, text=True,
        capture_output=True,
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
    if packet["commands"] != receipt["worker_packet_commands"]:
        raise SystemExit("worker packet command list is stale")
    if packet["known_failures"] != receipt["known_failures"]:
        raise SystemExit("worker packet known failures are stale")
    if packet["output_summary"] != receipt["worker_output_summary"]:
        raise SystemExit("worker packet output summary is stale")
    actual_changed = {".stage1-worker-selftest.json"}
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT, check=True, text=True, capture_output=True,
    ).stdout.splitlines()
    for line in status:
        relative = line[3:]
        if relative == "Formalizations/Lean/.lake":
            continue
        if relative == ".stage1-worker-selftest.json":
            continue
        if not relative.startswith(f"Stage1_Instances/{THEOREM_ID}/"):
            raise SystemExit(f"unexpected changed path outside worker ownership: {relative}")
        actual_changed.add(relative)
    if set(packet["changed_paths"]) != actual_changed:
        raise SystemExit("worker packet changed paths do not match git status")

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
        ["git", "rev-parse", "HEAD"], cwd=mathlib, check=True, text=True,
        capture_output=True,
    ).stdout.strip()
    actual_tree = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, check=True, text=True,
        capture_output=True,
    ).stdout.strip()
    if actual_revision != EXPECTED_MATHLIB_REVISION or actual_tree != EXPECTED_MATHLIB_TREE:
        raise SystemExit("materialized mathlib revision or tree changed")
    environment = statement["environment_fingerprint"]
    if environment["mathlib_revision"] != actual_revision or environment["mathlib_tree"] != actual_tree:
        raise SystemExit("structured mathlib environment is stale")
    if environment["lean_toolchain_file_sha256"] != EXPECTED_TOOLCHAIN_SHA256:
        raise SystemExit("structured toolchain hash is stale")
    if environment["lake_manifest_sha256"] != EXPECTED_MANIFEST_SHA256:
        raise SystemExit("structured manifest hash is stale")
    for module, expected in EXPECTED_IMPORT_HASHES.items():
        path = mathlib / (module.replace(".", "/") + ".lean")
        if sha256_bytes(path.read_bytes()) != expected:
            raise SystemExit(f"direct import source changed: {module}")

    payload = {
        "direct_imports": list(DIRECT_IMPORTS),
        "expression_sha256": expression_hash,
        "import_deletion_failures": deletion_failures,
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
