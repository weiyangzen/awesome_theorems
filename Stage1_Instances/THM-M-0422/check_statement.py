#!/usr/bin/env python3
"""Validate the fail-closed statement boundary for THM-M-0422."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0422"
THEOREM_ID = "THM-M-0422"
ITEM_ID = "S56-M-0422-STATEMENT"
BASE_REVISION = "778c2db4855d48868391ea236f702e592067e798"
BASE_TREE = "27abf0ec82dad50561a14d1db471126fb7ac8665"
GRAPH_SHA256 = "9db2a7cc29bf218211004677abe45ce1742f597405c2d879675dbc66542c4c8b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0422/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0422/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0422/source_statement_crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0422/statement-receipt.json",
}
EXPECTED_ROLE_HASHES = {
    "statement_record": "4de972a0b7328acd5468ef4683ed3066fe6a714b71f971d51921641c869b9a4b",
    "statement_source": "17fc5d0fa4b78a71ccf24ccf12d670a47ad9ac401496ee90687d85249473f607",
    "source_crosswalk": "1eef588fd4e8a065b1306e0b1fe8f1ee1862980478cd9d253c741bdd19830b2e",
}
EXPECTED_ROLE_BLOBS = {
    "statement_record": "9f492d6b372aebbc0acda20e9603740e98092abf",
    "statement_source": "4f3961c2576c84fbc7cfea2b723f4996b1088cbe",
    "source_crosswalk": "dae3fcd578be94d38a5d92e2fa57c5d937db7fd4",
}
EXPECTED_AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": "af9c686849cec4da9f2680c70bb0eb7e78330681c2b422d0100de43b32c85aee",
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
    "Stage1_Instances/THM-M-0422/intake.json": (
        "78247cba50601ccafed6ff3dd3cf760c32163dbbeeb971af1008d2bf1b0fc5d5"
    ),
    "Stage1_Instances/THM-M-0422/dependency-reuse-ledger.json": (
        "4466257fb768a31ecef6bdbe08894d25691674354897fbb7db76c6f0e0e54fd4"
    ),
    "Stage1_Instances/THM-M-0422/statement-blocker.md": (
        "49710ae59f34adf3c07c66ecd642d241a9e4d840cf374c91056b53dfac7a09dc"
    ),
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_077.lean": (
        "9854d3f2d827c935f2df569fc67fd639f6213404c7555b9711c33d99bcd6da6b"
    ),
    "Docs/researches/math_theorems.md": (
        "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29"
    ),
}
MATHLIB_INTERFACES = {
    "FieldTheory/Galois/Abelian.lean": (
        "2747cc67b1e0af6a0ae3ec5213262f5adfef331c1fa00f973654a14122b121b9"
    ),
    "NumberTheory/NumberField/AdeleRing.lean": (
        "bb3b2448d9bd4febf74e78760d8927406ca49c8117362fdf2a3f752b3efebdd8"
    ),
    "Topology/Algebra/IsOpenUnits.lean": (
        "c6699fcb90e5cb3f5ac7244a39b3c23e1ce6eb24bd9ad17afdcd1e37e82188dd"
    ),
}
DIRECT_IMPORTS = (
    "Mathlib.FieldTheory.Galois.Abelian",
    "Mathlib.NumberTheory.NumberField.AdeleRing",
    "Mathlib.Topology.Algebra.IsOpenUnits",
)
CHECKS = (
    "IsAbelianGalois",
    "NumberField.AdeleRing",
    "NumberField.AdeleRing.algebraMap_injective",
    "NumberField.AdeleRing.principalSubgroup",
    "IsOpenUnits",
)
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)
CANONICAL_DECLARATION = re.compile(
    r"^[ \t]*(?:def|theorem|lemma|example|abbrev|opaque|axiom)\s+"
    r"(?:GlobalClassField|ClassFieldTheory|CanonicalTarget|StatementShape)",
    flags=re.MULTILINE | re.IGNORECASE,
)


def fail(message: str) -> NoReturn:
    print(f"THM-M-0422 statement validator: {message}", file=sys.stderr)
    raise SystemExit(1)


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


def digest(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def git_blob(relative: str) -> str:
    data = (ROOT / relative).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git(*argv: str) -> str:
    result = subprocess.run(
        ["git", *argv],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
    )
    if result.returncode:
        fail(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


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
    if target.get("execution_rank") != 77 or target.get("lifecycle_mode") != "planned":
        fail("target manifest identity or lifecycle changed")
    if target.get("legacy_artifacts_accepted") is not False:
        fail("legacy evidence unexpectedly acquired acceptance")

    execution = load("Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row.get("id") == ITEM_ID)
    expected_item = {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 77,
        "phase": "statement",
        "layer": 1,
        "state": "[ ]",
        "depends_on": ["S56-M-0422-INTAKE"],
        "owned_paths": ["Stage1_Instances/THM-M-0422"],
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
    if node.get("v2_execution_rank") != 303 or node.get("topological_layer") != 0:
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
    selected = {}
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
    if validators != ["Stage1_Instances/THM-M-0422/check_statement.py"]:
        fail("validator candidate selection is not exactly one target-owned path")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("statement contract unexpectedly permits blocked phase closure")
    if phase.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        fail("statement contract unexpectedly treats negative findings as the deliverable")

    changed = subprocess.run(
        ["git", "status", "--porcelain", "--", "Stage1_Instances/THM-M-0422"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    if changed.returncode:
        fail("could not inspect the target-owned worktree delta")
    actual_changed = sorted(
        line[3:] for line in changed.stdout.splitlines() if len(line) > 3
    )
    expected_changed = sorted(
        [
            "Stage1_Instances/THM-M-0422/Statement.lean",
            "Stage1_Instances/THM-M-0422/check_statement.py",
            "Stage1_Instances/THM-M-0422/dependency-reuse-ledger.json",
            "Stage1_Instances/THM-M-0422/statement-blocker.md",
            "Stage1_Instances/THM-M-0422/statement-receipt.json",
            "Stage1_Instances/THM-M-0422/statement.json",
        ]
    )
    if actual_changed != expected_changed:
        fail("target-owned worktree delta differs from the handoff inventory")


def validate_ledger() -> None:
    ledger = load("Stage1_Instances/THM-M-0422/dependency-reuse-ledger.json")
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
            fail(f"empty dependency ledger field {field} changed")
    if ledger.get("schema_version") != "stage1-dependency-reuse-ledger/1.1":
        fail("dependency ledger schema changed")
    if ledger.get("consumer_theorem_id") != THEOREM_ID:
        fail("dependency ledger owner changed")
    if ledger.get("observed_theorem_dag_sha256") != GRAPH_SHA256:
        fail("dependency ledger graph binding changed")
    if ledger.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency ledger context binding changed")
    if ledger.get("repository_revision") != BASE_REVISION:
        fail("dependency ledger revision changed")
    closure = ledger.get("closure_audit", {})
    if closure.get("parent_inspection_order") != []:
        fail("parent inspection order is not the exact empty closure")
    if closure.get("status") != "empty_complete_closure_audited":
        fail("empty dependency closure is not marked audited")


def validate_statement_boundary() -> None:
    statement = load(ROLE_PATHS["statement_record"])
    source = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    blocker = (HERE / "statement-blocker.md").read_text(encoding="utf-8")
    intake = load("Stage1_Instances/THM-M-0422/intake.json")
    legacy = (
        ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_077.lean"
    ).read_text(encoding="utf-8")
    mathlib_root = ROOT / "Formalizations/Lean/.lake/packages/mathlib/Mathlib"

    for role, expected in EXPECTED_ROLE_HASHES.items():
        if digest(ROLE_PATHS[role]) != expected:
            fail(f"selected artifact bytes changed: {role}")
        if git_blob(ROLE_PATHS[role]) != EXPECTED_ROLE_BLOBS[role]:
            fail(f"selected artifact Git blob changed: {role}")
    for relative, expected in MATHLIB_INTERFACES.items():
        actual = hashlib.sha256((mathlib_root / relative).read_bytes()).hexdigest()
        if actual != expected:
            fail(f"pinned mathlib interface changed: {relative}")

    if statement.get("schema_version") != "stage1-statement/1.0":
        fail("statement record schema changed")
    if statement.get("item_id") != ITEM_ID or statement.get("theorem_id") != THEOREM_ID:
        fail("statement record identity changed")
    if statement.get("canonical_claim_status") != (
        "blocked_on_missing_source_faithful_lean_objects"
    ):
        fail("missing-interface blocker is no longer explicit")
    if statement.get("canonical_statement") != intake.get("canonical_statement"):
        fail("statement record does not preserve the intake's compound root")
    formal = statement.get("canonical_formal_target", {})
    if formal.get("declaration_or_expression") is not None:
        fail("a canonical Lean declaration or expression was invented")
    if formal.get("elaborated_expression_sha256") is not None:
        fail("a missing expression fingerprint was invented")
    if formal.get("statement_file_sha256") != EXPECTED_ROLE_HASHES["statement_source"]:
        fail("statement boundary source hash is stale")
    if tuple(statement.get("direct_imports", [])) != DIRECT_IMPORTS:
        fail("statement boundary imports changed")
    mutations = statement.get("mutation_tests", {})
    if mutations.get("executed") != [] or mutations.get("status") != (
        "blocked_without_canonical_expression"
    ):
        fail("mutation blocker boundary changed")
    if statement.get("statement_elaborated") is not False:
        fail("statement record falsely claims exact target elaboration")
    if statement.get("audit_complete") is not False or statement.get("theorem_complete") is not False:
        fail("statement record falsely closes a terminal decision")

    imports = tuple(re.findall(r"^import ([^\s]+)$", source, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        fail("boundary source direct imports disagree")
    if PROHIBITED.search(source):
        fail("boundary source contains a prohibited placeholder or trust construct")
    if CANONICAL_DECLARATION.search(source):
        fail("boundary source unexpectedly declares a canonical class-field target")
    checks = tuple(re.findall(r"^#check ([^\s]+)$", source, re.MULTILINE))
    if checks != CHECKS:
        fail("boundary interface probes changed")

    combined = crosswalk + "\n" + blocker
    for term in (
        "global reciprocity",
        "existence",
        "idele norm map",
        "global Artin map",
        "inclusion-reversing",
        "not the induced topology",
    ):
        if term not in combined:
            fail(f"source or interface boundary omits {term!r}")
    for term in (
        "structure ClassFieldReciprocityData",
        "Extension : Type",
        "reciprocityKernel",
        "Function.Bijective data.reciprocityKernel",
    ):
        if term not in legacy:
            fail("legacy abstract-interface evidence changed")
    topology_source = (mathlib_root / "Topology/Algebra/IsOpenUnits.lean").read_text(
        encoding="utf-8"
    )
    if "the topology on ideles is not the induced topology from adeles" not in topology_source:
        fail("pinned mathlib no longer carries the idele-topology boundary")


def validate_receipt() -> None:
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
        fail("phase receipt schema changed")
    if receipt.get("item_id") != ITEM_ID or receipt.get("theorem_id") != THEOREM_ID:
        fail("phase receipt identity changed")
    if receipt.get("phase") != "statement" or receipt.get("intent") != "audit":
        fail("phase receipt phase or intent changed")
    if receipt.get("base_revision") != BASE_REVISION or receipt.get("base_tree") != BASE_TREE:
        fail("phase receipt base changed")
    if receipt.get("accepted") is not False or receipt.get("verdict") != "blocked":
        fail("phase receipt no longer preserves the negative verdict")
    if receipt.get("proposed_state") != "[_]" or receipt.get("selftest_status") != "passed":
        fail("phase receipt does not preserve the self-tested negative handoff")
    if receipt.get("statement_fingerprints") != []:
        fail("phase receipt invents a statement fingerprint")
    if receipt.get("first_failed_gate") != (
        "S02-EXACT-TARGET.missing_source_faithful_lean_objects"
    ):
        fail("phase receipt first failed gate changed")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("phase receipt falsely closes a terminal decision")
    if receipt.get("inputs", {}).get("parent_inspection_order") != []:
        fail("phase receipt parent inspection order changed")
    if receipt.get("inputs", {}).get("provider_acceptance_inherited") is not False:
        fail("phase receipt transfers provider acceptance")

    bindings = receipt.get("artifact_bindings", {})
    if set(bindings) != set(ROLE_PATHS):
        fail("phase receipt selected role bindings are incomplete")
    for role in EXPECTED_ROLE_HASHES:
        binding = bindings.get(role, {})
        if binding.get("role") != role or binding.get("path") != ROLE_PATHS[role]:
            fail(f"phase receipt role binding changed: {role}")
        if binding.get("sha256") != EXPECTED_ROLE_HASHES[role]:
            fail(f"phase receipt SHA-256 binding changed: {role}")
        if binding.get("git_blob") != EXPECTED_ROLE_BLOBS[role]:
            fail(f"phase receipt Git-blob binding changed: {role}")
    self_binding = bindings.get("phase_receipt", {})
    if self_binding.get("path") != ROLE_PATHS["phase_receipt"]:
        fail("phase receipt self-binding path changed")
    if self_binding.get("sha256") is not None or self_binding.get("git_blob") is not None:
        fail("phase receipt self-binding must remain scheduler-owned and acyclic")

    support_bindings = receipt.get("support_bindings", {})
    expected_support_bindings = {
        "dependency_reuse_ledger": (
            "Stage1_Instances/THM-M-0422/dependency-reuse-ledger.json",
            "4466257fb768a31ecef6bdbe08894d25691674354897fbb7db76c6f0e0e54fd4",
            "082bb084130c359f4d1465ca184a12c960cd3bdf",
        ),
        "statement_blocker": (
            "Stage1_Instances/THM-M-0422/statement-blocker.md",
            "49710ae59f34adf3c07c66ecd642d241a9e4d840cf374c91056b53dfac7a09dc",
            "0ff4eebb1f49322b4773426daca1f705afff3091",
        ),
    }
    if set(support_bindings) != set(expected_support_bindings):
        fail("phase receipt support bindings are incomplete")
    for role, (path, sha256, blob) in expected_support_bindings.items():
        binding = support_bindings[role]
        if binding != {"path": path, "sha256": sha256, "git_blob": blob}:
            fail(f"phase receipt support binding changed: {role}")

    packet = load(".stage1-worker-selftest.json")
    if packet.get("item_id") != ITEM_ID or packet.get("state") != "[_]":
        fail("worker packet identity or state changed")
    if packet.get("base_revision") != BASE_REVISION:
        fail("worker packet base changed")
    if packet.get("commands") != receipt.get("selftest_result", {}).get("commands"):
        fail("worker packet commands differ from the phase receipt")
    if packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet known failures differ from the phase receipt")
    if packet.get("changed_paths") != [
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0422/Statement.lean",
        "Stage1_Instances/THM-M-0422/check_statement.py",
        "Stage1_Instances/THM-M-0422/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0422/statement-blocker.md",
        "Stage1_Instances/THM-M-0422/statement-receipt.json",
        "Stage1_Instances/THM-M-0422/statement.json",
    ]:
        fail("worker packet changed-path inventory changed")


def main() -> None:
    validate_authority()
    validate_ledger()
    validate_statement_boundary()
    validate_receipt()
    semantic = {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "phase": "statement",
        "status": "blocked",
        "verdict": "blocked",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": "S02-EXACT-TARGET.missing_source_faithful_lean_objects",
        "open_obligations": 5,
        "stale_inputs": [],
        "blocked": True,
        "message": (
            "Negative statement boundary self-tested: source-faithful class-field objects, "
            "an exact Lean expression and fingerprint, checked transports, and four mutation "
            "classes remain open."
        ),
    }
    print(json.dumps(semantic, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
