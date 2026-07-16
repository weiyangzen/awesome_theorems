#!/usr/bin/env python3
"""Validate and semantically report the THM-M-0547 statement phase."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0547"
LEAN_DIR = ROOT / "Formalizations" / "Lean"
SOURCE = HERE / "Statement.lean"
THEOREM_ID = "THM-M-0547"
ITEM_ID = "S56-M-0547-STATEMENT"
NAMESPACE = "Stage1Instances.THM_M_0547"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
CANONICAL = "LefschetzDualityTarget"
DECLARATIONS = (
    CANONICAL,
    "mutationRemovedOrientation",
    "mutationChangedToAbsoluteHomology",
    "mutationChangedBinderScope",
    "mutationBoundaryDegreeZeroOnly",
)
TRANSPORT = "lefschetzDualityTarget_iff_expanded"
PRINT_MARKER = f"#print {NAMESPACE}.{CANONICAL}"
DIRECT_IMPORTS = (
    "Mathlib.Geometry.Manifold.IsManifold.InteriorBoundary",
)
IMPORT_FILES = {
    DIRECT_IMPORTS[0]: "Mathlib/Geometry/Manifold/IsManifold/InteriorBoundary.lean",
}
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0547/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0547/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0547/source-statement-crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0547/statement-receipt.json",
}
EXPECTED_ROLE_HASHES = {
    "statement_record": "1b0e95fef6ead36589820437ef17d81ca857e69b262abe1fed4b4e5d617f6bd1",
    "statement_source": "9407665d6bdcc3ff384daa6f16600b5555776641837fbabedc6da7b80f9a5268",
    "source_crosswalk": "2fac48a1deb8df39afc969993bbb4bfe202fc3ce48939f5b0f28a7a1983a8470",
}
EXPECTED_ROLE_BLOBS = {
    "statement_record": "01aa0fe8e65b8ec7ac1c14458b2728e08f2e6b79",
    "statement_source": "ec7660c38fd5e1dc3a3d30ea157175f721ea2dcd",
    "source_crosswalk": "000c32d717d15e7533eacf56e79aed9a5d02354c",
}
EXPECTED_EXPRESSION_HASHES = {
    CANONICAL: "f7166d14cb6a1a04db1f715a0fcbcf5598e9c7811390e8aa5d14c3f09ddbbde5",
    "mutationRemovedOrientation": "a7bae7b8dc2a63b261c78586d5eae70b6335b7fba3347a4583408c5f5290ce8c",
    "mutationChangedToAbsoluteHomology": "e5eea1b6bb26e21d772e528a3e84f267993a542fcdf8840c4ad0ca2b41a2298c",
    "mutationChangedBinderScope": "f79cb73595de19e225c495c329db0842eace0a907672c1eae4e76caa4d1ec2fd",
    "mutationBoundaryDegreeZeroOnly": "2ea6971db47b085f1d0a21ea1ce87a62a9a3bf0438a5355c38bf08162370adad",
}
EXPECTED_AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": "fb6cd286dc5c47e22d754ab73e5162986e98a18b5bc6d8e7213ae5d39b4256d1",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "skills/execute-stage1-rev56/SKILL.md": "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_SUPPORT_HASHES = {
    "Stage1_Instances/THM-M-0547/dependency-reuse-ledger.json": (
        "a23d66f6f118e01ecd18f410cbc3457088551a5f54116aa2c450250dd632dd8b"
    ),
    "Docs/researches/math_theorems.md": (
        "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29"
    ),
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_119.lean": (
        "07c14a7a1e29fab03f7cece730d9cb074af4dbd541cff7466a496b00fda9e7ef"
    ),
}
EXPECTED_IMPORT_HASHES = {
    DIRECT_IMPORTS[0]: "0ba9d2e50ad50079275858286bf254da15b1845c08bd07ab49d5a45e317b995a",
}
EXPECTED_TOOLCHAIN = "leanprover/lean4:v4.29.0"
EXPECTED_MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0547/Statement.lean",
    "Stage1_Instances/THM-M-0547/check_statement.py",
    "Stage1_Instances/THM-M-0547/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0547/source-statement-crosswalk.md",
    "Stage1_Instances/THM-M-0547/statement-receipt.json",
    "Stage1_Instances/THM-M-0547/statement.json",
]
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)


def fail(message: str) -> NoReturn:
    print(f"THM-M-0547 statement validator: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(relative: str) -> str:
    return sha256_bytes((ROOT / relative).read_bytes())


def git_blob(relative: str) -> str:
    data = (ROOT / relative).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def load(relative: str) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate JSON key {key!r} in {relative}")
            result[key] = value
        return result

    try:
        value = json.loads(
            (ROOT / relative).read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicates,
        )
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {relative}: {error}")
    if not isinstance(value, dict):
        fail(f"expected one JSON object in {relative}")
    return value


def git(*argv: str) -> str:
    result = subprocess.run(
        ["git", *argv], cwd=ROOT, capture_output=True, text=True, timeout=20
    )
    if result.returncode:
        fail(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", "--trust=0", str(path)],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )


def run_text(text: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile(
        "w", suffix=".lean", encoding="utf-8", dir=HERE, delete=False
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        return run_lean(temporary)
    finally:
        temporary.unlink()


def elaborate_expression(declaration: str) -> str:
    source = SOURCE.read_text(encoding="utf-8")
    if source.count(PRINT_MARKER) != 1:
        fail("canonical print marker must occur exactly once")
    result = run_text(source.replace(PRINT_MARKER, f"#print {NAMESPACE}.{declaration}"))
    if result.returncode:
        sys.stderr.write(result.stdout)
        fail(f"Lean failed while printing {declaration}")
    qualified = re.escape(f"{NAMESPACE}.{declaration}")
    match = re.search(
        rf"def {qualified}(?:\.\{{[^}}]+\}})? : Prop :=\n(?P<expression>.*)\Z",
        result.stdout,
        re.DOTALL,
    )
    if not match:
        fail(f"could not extract the fully explicit expression for {declaration}")
    return match.group("expression").strip()


def validate_authority() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("repository HEAD differs from the claimed worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("repository tree differs from the claimed worker base")
    for relative, expected in EXPECTED_AUTHORITY_HASHES.items():
        if digest(relative) != expected:
            fail(f"authority input changed: {relative}")
    for relative, expected in EXPECTED_SUPPORT_HASHES.items():
        if digest(relative) != expected:
            fail(f"support input changed: {relative}")

    targets = load("Docs/Stage1_Targets_rev-5.6.json")
    target = next(
        row for row in targets["targets"] if row.get("theorem_id") == THEOREM_ID
    )
    if target.get("execution_rank") != 119 or target.get("lifecycle_mode") != "planned":
        fail("target manifest identity or lifecycle changed")
    if target.get("baseline") != "L0" or target.get("rework_required") is not True:
        fail("target assurance baseline changed")
    if target.get("legacy_artifacts_accepted") is not False:
        fail("legacy evidence unexpectedly acquired acceptance")

    execution = load("Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row.get("id") == ITEM_ID)
    expected_item = {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 119,
        "phase": "statement",
        "layer": 1,
        "state": "[ ]",
        "depends_on": ["S56-M-0547-INTAKE"],
        "owned_paths": ["Stage1_Instances/THM-M-0547"],
        "deliverable": "Elaborate the exact Lean 4 target with the minimal pinned imports.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    if item != expected_item:
        fail("authoritative statement item changed")

    theorem_dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    node = next(
        row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM_ID
    )
    if node.get("v2_execution_rank") != 335 or node.get("topological_layer") != 0:
        fail("v2 claim order changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency context changed")
    for field in (
        "direct_hard_parents",
        "transitive_hard_ancestors",
        "direct_reuse_hint_ids",
        "shared_lemma_group_ids",
    ):
        if node.get(field) != []:
            fail(f"theorem dependency field {field} is no longer empty")

    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row.get("phase") == "statement")
    selected: dict[str, str] = {}
    for role in phase["required_artifact_roles"]:
        candidates = [
            candidate.format(theorem_id=THEOREM_ID)
            for candidate in role["path_candidates"]
            if (ROOT / candidate.format(theorem_id=THEOREM_ID)).is_file()
        ]
        if len(candidates) != 1:
            fail(f"role {role['role']} is missing or ambiguous")
        selected[role["role"]] = candidates[0]
    if selected != ROLE_PATHS:
        fail("statement artifact-role selection changed")
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    if validators != ["Stage1_Instances/THM-M-0547/check_statement.py"]:
        fail("validator candidate selection is not exactly one HEAD path")
    receipt_required = {
        pointer.rsplit("/", 1)[-1]
        for pointer in phase.get("phase_receipt_required_fields", [])
        if pointer.count("/") == 1
    }
    if not receipt_required <= {
        "schema_version", "receipt_id", "item_id", "theorem_id", "phase",
        "intent", "base_revision", "base_tree", "inputs", "support_state",
        "proposed_state", "accepted", "verdict", "selftest_status",
        "known_failures", "first_failed_gate", "retry_condition",
        "status_boundary", "audit_complete", "theorem_complete",
        "invalidation_inputs", "statement_fingerprints", "mutation_tests",
    }:
        fail("HEAD statement receipt contract gained an unsupported top-level field")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("statement contract unexpectedly permits blocked phase closure")
    if phase.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        fail("statement contract unexpectedly treats a negative finding as completion")


def validate_ledger() -> None:
    ledger = load("Stage1_Instances/THM-M-0547/dependency-reuse-ledger.json")
    for field in (
        "direct_parent_ids",
        "transitive_ancestor_ids",
        "hard_edge_ids",
        "reuse_hint_ids",
        "shared_group_ids",
        "inspections",
        "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        if ledger.get(field) != []:
            fail(f"empty dependency-ledger field {field} changed")
    if ledger.get("schema_version") != "stage1-dependency-reuse-ledger/1.1":
        fail("dependency-ledger schema changed")
    if ledger.get("consumer_theorem_id") != THEOREM_ID:
        fail("dependency-ledger owner changed")
    if ledger.get("observed_theorem_dag_sha256") != GRAPH_SHA256:
        fail("dependency-ledger graph binding changed")
    if ledger.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency-ledger context binding changed")
    if ledger.get("repository_revision") != BASE_REVISION:
        fail("dependency-ledger revision changed")
    closure = ledger.get("closure_audit", {})
    if closure.get("parent_inspection_order") != []:
        fail("parent inspection order is not the exact empty closure")
    if closure.get("status") != "empty_complete_closure_audited":
        fail("empty dependency closure is not marked completely audited")


def validate_environment() -> None:
    manifest = load("Formalizations/Lean/lake-manifest.json")
    if (LEAN_DIR / "lean-toolchain").read_text(encoding="utf-8").strip() != EXPECTED_TOOLCHAIN:
        fail("Lean toolchain pin changed")
    mathlib_revision = next(
        package["rev"] for package in manifest["packages"] if package["name"] == "mathlib"
    )
    if mathlib_revision != EXPECTED_MATHLIB_REVISION:
        fail("Lake manifest mathlib revision changed")
    mathlib = LEAN_DIR / ".lake" / "packages" / "mathlib"
    if not mathlib.is_dir():
        fail("canonical pinned mathlib artifact is missing")
    revision = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=mathlib, text=True, timeout=20
    ).strip()
    tree = subprocess.check_output(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib, text=True, timeout=20
    ).strip()
    if (revision, tree) != (EXPECTED_MATHLIB_REVISION, EXPECTED_MATHLIB_TREE):
        fail("materialized mathlib revision or tree changed")
    for module, relative in IMPORT_FILES.items():
        if sha256_bytes((mathlib / relative).read_bytes()) != EXPECTED_IMPORT_HASHES[module]:
            fail(f"direct-import source changed: {module}")


def validate_statement() -> dict[str, str]:
    source_text = SOURCE.read_text(encoding="utf-8")
    imports = tuple(re.findall(r"^import ([^\s]+)$", source_text, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        fail(f"direct imports changed: {imports!r}")
    if PROHIBITED.search(source_text):
        fail("Statement.lean contains a prohibited placeholder or trust construct")
    if source_text.count("#check_failure") != 5:
        fail("exact-type mutation rejection fixture count changed")
    if not re.search(rf"^theorem {TRANSPORT}\b", source_text, re.MULTILINE):
        fail("checked target expansion is missing")

    expressions = {name: elaborate_expression(name) for name in DECLARATIONS}
    if len(set(expressions.values())) != len(expressions):
        fail("canonical target and mutations are not pairwise distinct")
    hashes = {name: sha256_bytes(value.encode("utf-8")) for name, value in expressions.items()}
    if hashes != EXPECTED_EXPRESSION_HASHES:
        fail("canonical or mutation expression fingerprint changed")

    for direct_import in DIRECT_IMPORTS:
        deletion = run_text(source_text.replace(f"import {direct_import}\n", "", 1))
        if deletion.returncode == 0:
            fail(f"direct-import deletion unexpectedly elaborated: {direct_import}")

    statement = load(ROLE_PATHS["statement_record"])
    if statement.get("schema_version") != "stage1-statement/1.0":
        fail("statement record schema changed")
    if statement.get("item_id") != ITEM_ID or statement.get("theorem_id") != THEOREM_ID:
        fail("statement record identity changed")
    formal = statement.get("canonical_formal_target", {})
    if formal.get("declaration_or_expression") != f"{NAMESPACE}.{CANONICAL}":
        fail("canonical declaration binding changed")
    if formal.get("elaborated_expression_sha256") != hashes[CANONICAL]:
        fail("statement expression fingerprint is stale")
    if formal.get("statement_file_sha256") != digest(ROLE_PATHS["statement_source"]):
        fail("statement source fingerprint is stale")
    if tuple(statement.get("direct_imports", [])) != DIRECT_IMPORTS:
        fail("statement import record is stale")
    if statement.get("statement_elaborated") is not True:
        fail("statement record does not assert elaboration")
    if statement.get("theorem_proved") is not False:
        fail("statement record falsely claims a proof")
    if statement.get("audit_complete") is not False or statement.get("theorem_complete") is not False:
        fail("statement record falsely closes a terminal gate")
    killed = statement.get("mutation_tests", {}).get("killed", [])
    if {row.get("kind") for row in killed} != {
        "removed_hypothesis", "changed_domain", "changed_binder_scope", "boundary_case"
    }:
        fail("four required mutation classes are not recorded")
    if {row.get("declaration"): row.get("expression_sha256") for row in killed} != {
        name: hashes[name] for name in DECLARATIONS[1:]
    }:
        fail("statement mutation fingerprints are stale")

    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    required_crosswalk_terms = (
        "compact integral form",
        "Function.Bijective",
        "I.boundary M",
        "No declaration or acceptance state is reused",
        "H0",
        "q > n",
    )
    if any(term not in crosswalk for term in required_crosswalk_terms):
        fail("source crosswalk omits a required statement or status boundary")

    for role, expected in EXPECTED_ROLE_HASHES.items():
        if digest(ROLE_PATHS[role]) != expected:
            fail(f"selected artifact bytes changed: {role}")
        if git_blob(ROLE_PATHS[role]) != EXPECTED_ROLE_BLOBS[role]:
            fail(f"selected artifact Git blob changed: {role}")
    return hashes


def validate_receipt(hashes: dict[str, str]) -> None:
    receipt = load(ROLE_PATHS["phase_receipt"])
    required = {
        "schema_version", "receipt_id", "item_id", "theorem_id", "phase",
        "intent", "base_revision", "base_tree", "inputs", "support_state",
        "proposed_state", "accepted", "verdict", "selftest_status",
        "selftest_result", "known_failures", "first_failed_gate",
        "retry_condition", "status_boundary", "audit_complete",
        "theorem_complete", "invalidation_inputs", "statement_fingerprints",
        "mutation_tests",
    }
    if not required <= set(receipt):
        fail("phase receipt omits contract-required fields")
    if receipt.get("schema_version") != "stage1-node-receipt/1.0":
        fail("phase-receipt schema changed")
    if receipt.get("item_id") != ITEM_ID or receipt.get("theorem_id") != THEOREM_ID:
        fail("phase-receipt identity changed")
    if receipt.get("phase") != "statement" or receipt.get("intent") != "audit":
        fail("phase-receipt phase or intent changed")
    if receipt.get("base_revision") != BASE_REVISION or receipt.get("base_tree") != BASE_TREE:
        fail("phase-receipt base changed")
    if receipt.get("proposed_state") != "[_]" or receipt.get("accepted") is not False:
        fail("phase-receipt worker/master boundary changed")
    if receipt.get("verdict") != "accepted" or receipt.get("selftest_status") != "passed":
        fail("phase-receipt worker self-test is not finalized")
    if receipt.get("selftest_result", {}).get("exit_code") != 0:
        fail("phase-receipt self-test exit code is not successful")
    commands = receipt.get("selftest_result", {}).get("commands")
    if not isinstance(commands, list) or not commands:
        fail("phase-receipt self-test commands are empty")
    if receipt.get("statement_fingerprints") != [f"sha256:{hashes[CANONICAL]}"]:
        fail("phase-receipt statement fingerprint is stale")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("phase-receipt falsely closes a terminal decision")
    if receipt.get("first_failed_gate") is not None:
        fail("successful statement self-test records a failed phase gate")
    inputs = receipt.get("inputs", {})
    if inputs.get("parent_inspection_order") != [] or inputs.get("inspected_parent_ids") != []:
        fail("phase-receipt parent closure is not the exact empty order")
    if inputs.get("provider_acceptance_inherited") is not False:
        fail("phase-receipt transfers provider acceptance")

    bindings = receipt.get("artifact_bindings", {})
    if set(bindings) != set(ROLE_PATHS):
        fail("phase-receipt selected role bindings are incomplete")
    for role in EXPECTED_ROLE_HASHES:
        binding = bindings.get(role, {})
        if binding.get("role") != role or binding.get("path") != ROLE_PATHS[role]:
            fail(f"phase-receipt role binding changed: {role}")
        if binding.get("sha256") != EXPECTED_ROLE_HASHES[role]:
            fail(f"phase-receipt SHA-256 binding changed: {role}")
        if binding.get("git_blob") != EXPECTED_ROLE_BLOBS[role]:
            fail(f"phase-receipt Git-blob binding changed: {role}")
    self_binding = bindings.get("phase_receipt", {})
    if self_binding.get("path") != ROLE_PATHS["phase_receipt"]:
        fail("phase-receipt self-binding path changed")
    if self_binding.get("sha256") is not None or self_binding.get("git_blob") is not None:
        fail("phase-receipt self-binding must remain scheduler-owned and acyclic")

    packet = load(".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }:
        fail("worker packet fields changed")
    if packet.get("item_id") != ITEM_ID or packet.get("state") != "[_]":
        fail("worker packet identity or state changed")
    if packet.get("base_revision") != BASE_REVISION:
        fail("worker packet base changed")
    if packet.get("commands") != commands:
        fail("worker packet commands differ from the phase receipt")
    if packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet known failures differ from the phase receipt")
    if packet.get("changed_paths") != EXPECTED_CHANGED_PATHS:
        fail("worker packet changed-path inventory changed")
    if receipt.get("changed_paths") != EXPECTED_CHANGED_PATHS:
        fail("phase-receipt changed-path inventory changed")


def validate_worktree() -> None:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    if result.returncode:
        fail("could not inspect worker worktree delta")
    actual = sorted(
        line[3:] for line in result.stdout.splitlines()
        if len(line) > 3 and line[3:] != "Formalizations/Lean/.lake"
    )
    if actual != sorted(EXPECTED_CHANGED_PATHS):
        fail(f"worker worktree delta differs from handoff inventory: {actual!r}")
    for relative in EXPECTED_CHANGED_PATHS:
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            fail(f"handoff path is missing or symlinked: {relative}")
        data = path.read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            fail(f"handoff path has invalid bytes or final newline: {relative}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            fail(f"handoff path has trailing whitespace: {relative}")


def main() -> None:
    validate_authority()
    validate_ledger()
    validate_environment()
    hashes = validate_statement()
    validate_receipt(hashes)
    validate_worktree()
    semantic = {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "phase": "statement",
        "status": "passed",
        "verdict": "accepted",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": True,
        "first_failed_gate": None,
        "open_obligations": 0,
        "stale_inputs": [],
        "blocked": False,
        "message": (
            "Statement predicate self-tested: exact target, checked expansion, four mutation "
            "classes, minimal pinned imports, environment, artifact bindings, and empty parent "
            "closure passed. Master acceptance remains separate."
        ),
    }
    print(json.dumps(semantic, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
