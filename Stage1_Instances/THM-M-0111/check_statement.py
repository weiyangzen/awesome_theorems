#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0111 statement-phase packet."""

from __future__ import annotations

import hashlib
import json
import calendar
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0111"
THEOREM_ID = "THM-M-0111"
ITEM_ID = "S56-M-0111-STATEMENT"
BASE_REVISION = "778c2db4855d48868391ea236f702e592067e798"
BASE_TREE = "27abf0ec82dad50561a14d1db471126fb7ac8665"
GRAPH_SHA256 = "9db2a7cc29bf218211004677abe45ce1742f597405c2d879675dbc66542c4c8b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
FAILED_GATE = (
    "S02-EXACT-TARGET.native_kahler_de_rham_comparison_and_"
    "projective_holomorphic_embedding_interfaces"
)
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0111/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0111/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0111/source_statement_crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0111/statement-receipt.json",
}
EXPECTED_CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0111/Statement.lean",
    "Stage1_Instances/THM-M-0111/check_statement.py",
    "Stage1_Instances/THM-M-0111/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0111/statement-phase-blocker-2026-07-17-head-778c2db48-slot51.md",
    "Stage1_Instances/THM-M-0111/statement-receipt.json",
    "Stage1_Instances/THM-M-0111/statement.json",
]
EXPECTED_ROLE_HASHES = {
    "statement_record": "6c67b71c30367a9fea6084c0b6636772e20175348f856d1f6b13e772f8d90897",
    "statement_source": "c93f124192ebeb5acf5230575f6ecca1cda5683650f26de7f92df647bf0d0405",
    "source_crosswalk": "f1fd87406e748f568ce0e5e5fcd3882b3a63065e15bfd0c4aa3e95f0cab9d49e",
}
EXPECTED_ROLE_BLOBS = {
    "statement_record": "498ad739f5b9550f032a5abc74ef0230c1f9013b",
    "statement_source": "40d04eaa02ac4bc4f04b2bf85553c49ea5ebbf9a",
    "source_crosswalk": "82fe89de34088981cc3c5964c197694a036e98ff",
}
EXPECTED_AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": "af9c686849cec4da9f2680c70bb0eb7e78330681c2b422d0100de43b32c85aee",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "b5fa80e17e2f16bcdbf80e7f07e8bb4fabdccb4e8eed77dc86a5e256ed30b1af",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_SUPPORT_HASHES = {
    "Stage1_Instances/THM-M-0111/dependency-reuse-ledger.json": (
        "49da65f8d9b28fa9f3a945042ac94c2c6dfca588781e6c368a900dbe6ecb528e"
    ),
    "Stage1_Instances/THM-M-0111/statement-phase-blocker-2026-07-17-head-778c2db48-slot51.md": (
        "ca02bb289ffa545bef1ad1bfb7a3b9e46ed91fdb7ccb7b5dc5b365fc0bfdccfc"
    ),
    "Stage1_Instances/THM-M-0111/intake.json": (
        "ec26f636672eb4ea2b511fa460a6bd37a036ac1e40d77e214f590911decb4537"
    ),
    "Stage1_Instances/THM-M-0111/scope.md": (
        "65738f0512a44c22e035e4d81c1532abee090977aa8e3e0edad16887d67c1f95"
    ),
}
DIRECT_IMPORTS = (
    "Mathlib.Geometry.Manifold.Complex",
    "Mathlib.LinearAlgebra.Projectivization.Basic",
)
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)
CANONICAL_DECLARATION = re.compile(
    r"^[ \t]*(?:def|theorem|lemma|example|opaque|axiom)\s+"
    r"(?:Kodaira|CanonicalTarget|StatementShape|HodgeManifold)",
    flags=re.MULTILINE | re.IGNORECASE,
)
SEMANTIC = {
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
    "first_failed_gate": FAILED_GATE,
    "open_obligations": 7,
    "stale_inputs": [],
    "blocked": True,
    "message": (
        "Native exact-target expressibility remains blocked; the negative packet "
        "and empty dependency closure are internally consistent and byte-bound."
    ),
}


def fail(message: str) -> NoReturn:
    print(f"THM-M-0111 statement validator: {message}", file=sys.stderr)
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
    try:
        return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    except OSError as error:
        fail(f"cannot read {relative}: {error}")


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
        check=False,
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

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    item_line = (
        "- [ ] `S56-M-0111-STATEMENT` / `THM-M-0111` / `statement`: "
        "Elaborate the exact Lean 4 target with the minimal pinned imports. {attempts=0}"
    )
    predecessor_line = (
        "- [_] `S56-M-0111-INTAKE` / `THM-M-0111` / `intake`: "
        "Create the theorem dossier, scope map, and source-statement crosswalk. {attempts=1}"
    )
    if blueprint.count(item_line) != 1 or blueprint.count(predecessor_line) != 1:
        fail("sole task-state authority no longer has the exact assigned cursor")

    target = next(
        row
        for row in load("Docs/Stage1_Targets_rev-5.6.json")["targets"]
        if row.get("theorem_id") == THEOREM_ID
    )
    if target.get("execution_rank") != 24 or target.get("lifecycle_mode") != "planned":
        fail("target manifest identity or lifecycle changed")
    if target.get("legacy_artifacts_accepted") is not False:
        fail("legacy evidence unexpectedly acquired acceptance")

    execution = load("Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row.get("id") == ITEM_ID)
    expected_item = {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 24,
        "phase": "statement",
        "layer": 1,
        "state": "[ ]",
        "depends_on": ["S56-M-0111-INTAKE"],
        "owned_paths": ["Stage1_Instances/THM-M-0111"],
        "deliverable": "Elaborate the exact Lean 4 target with the minimal pinned imports.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    if item != expected_item:
        fail("authoritative statement item changed")
    predecessor = next(
        row for row in execution["items"] if row.get("id") == "S56-M-0111-INTAKE"
    )
    if predecessor.get("state") != "[_]" or predecessor.get("attempts") != 1:
        fail("predecessor state changed")

    node = next(
        row
        for row in load("Docs/Stage1_Theorem_DAG_v2.json")["theorems"]
        if row.get("theorem_id") == THEOREM_ID
    )
    if node.get("v2_execution_rank") != 261 or node.get("topological_layer") != 0:
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
    if validators != ["Stage1_Instances/THM-M-0111/check_statement.py"]:
        fail("validator candidate selection is not exactly one path")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("statement contract unexpectedly permits blocked phase closure")
    if phase.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        fail("statement contract unexpectedly treats a negative finding as closure")

    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    if status.returncode:
        fail("could not inspect worker delta")
    actual_changed: list[str] = []
    for line in status.stdout.splitlines():
        relative = line[3:]
        if relative == "Formalizations/Lean/.lake":
            continue
        if not relative.startswith("Stage1_Instances/THM-M-0111/"):
            if relative != ".stage1-worker-selftest.json":
                fail(f"unexpected changed path outside worker ownership: {relative}")
        actual_changed.append(relative)
    if sorted(actual_changed) != EXPECTED_CHANGED_PATHS:
        fail("worker delta differs from the exact handoff inventory")


def validate_ledger() -> None:
    ledger = load("Stage1_Instances/THM-M-0111/dependency-reuse-ledger.json")
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
    if closure != {
        "parent_inspection_order": [],
        "complete_closure_inspected": True,
        "inspection_count": 0,
        "provider_acceptance_inherited": False,
        "result": "empty_context_audited",
    }:
        fail("empty dependency closure audit changed")


def validate_statement_boundary() -> None:
    statement = load(ROLE_PATHS["statement_record"])
    source = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    blocker = (HERE / "statement-phase-blocker-2026-07-17-head-778c2db48-slot51.md").read_text(
        encoding="utf-8"
    )
    for role, expected in EXPECTED_ROLE_HASHES.items():
        if digest(ROLE_PATHS[role]) != expected:
            fail(f"selected artifact bytes changed: {role}")
        if git_blob(ROLE_PATHS[role]) != EXPECTED_ROLE_BLOBS[role]:
            fail(f"selected artifact Git blob changed: {role}")

    if statement.get("schema_version") != "stage1-statement/1.0":
        fail("statement record schema changed")
    if statement.get("item_id") != ITEM_ID or statement.get("theorem_id") != THEOREM_ID:
        fail("statement record identity changed")
    if statement.get("canonical_statement") is not None:
        fail("an unresolved source normalization was promoted to a canonical statement")
    if not isinstance(statement.get("received_claim_boundary"), str):
        fail("statement record lost the received mathematical boundary")
    if statement.get("canonical_formal_target") is not None:
        fail("a canonical Lean target was invented")
    if statement.get("elaborated_expression_sha256") is not None:
        fail("a missing expression fingerprint was invented")
    if statement.get("environment_fingerprint_for_canonical_target") is not None:
        fail("a missing target environment fingerprint was invented")
    if statement.get("statement_fingerprints") != [] or statement.get("credited_transports") != []:
        fail("statement record invents a fingerprint or transport")
    if statement.get("minimal_imports_proven") is not False:
        fail("statement record invents canonical-target import minimality")
    expected_mutations = {
        "removed_hypothesis": "not_executable_without_a_canonical_formal_target",
        "changed_domain": "not_executable_without_a_canonical_formal_target",
        "changed_binder_scope": "not_executable_without_a_canonical_formal_target",
        "boundary_case": "not_executable_without_a_canonical_formal_target",
    }
    if statement.get("mutation_tests") != expected_mutations:
        fail("statement mutation blocker inventory changed")
    if statement.get("first_failed_gate") != FAILED_GATE:
        fail("statement record first failed gate changed")
    if any(
        statement.get(field) is not False
        for field in (
            "statement_elaborated",
            "phase_predicate_proven",
            "phase_accepted",
            "audit_complete",
            "theorem_complete",
        )
    ):
        fail("statement record overstates acceptance or completion")
    context = statement.get("dependency_context", {})
    if context.get("parent_inspection_order") != []:
        fail("statement record parent inspection order changed")
    if context.get("provider_acceptance_inherited") is not False:
        fail("statement record transfers provider acceptance")

    imports = tuple(re.findall(r"^import ([^\s]+)$", source, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        fail("probe direct imports changed")
    if tuple(statement.get("candidate_surface_probe", {}).get("direct_imports", [])) != DIRECT_IMPORTS:
        fail("probe import record is stale")
    if PROHIBITED.search(source):
        fail("statement probe contains a proof escape or trust construct")
    if CANONICAL_DECLARATION.search(source):
        fail("statement probe unexpectedly declares a canonical target")
    required_checks = (
        "#check ModelWithCorners",
        "#check IsManifold",
        "#check MDifferentiable",
        "#check CompactSpace",
        "#check Projectivization",
        "#check CandidateComplexProjectiveCarrier",
        "#check_failure (inferInstance : TopologicalSpace (CandidateComplexProjectiveCarrier 1))",
        "#check Topology.IsClosedEmbedding",
    )
    if any(check not in source for check in required_checks):
        fail("candidate interface probe is incomplete")
    combined = crosswalk + "\n" + blocker
    for phrase in (
        "integral Kahler class",
        "holomorphic embedding",
        "uninterpreted propositions",
        "2*pi",
        "target-scoped blocker",
    ):
        if phrase not in combined:
            fail("source/boundary crosswalk is incomplete")


def validate_receipt_and_packet() -> None:
    receipt = load(ROLE_PATHS["phase_receipt"])
    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row.get("phase") == "statement")
    required = {
        pointer.removeprefix("/")
        for pointer in phase["phase_receipt_required_fields"]
        if pointer.count("/") == 1
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
        fail("phase receipt base identity changed")
    validated_at = receipt.get("validated_at")
    if not isinstance(validated_at, str) or not validated_at.endswith("Z"):
        fail("phase receipt validation timestamp is malformed")
    try:
        validated_epoch = calendar.timegm(time.strptime(validated_at, "%Y-%m-%dT%H:%M:%SZ"))
    except ValueError:
        fail("phase receipt validation timestamp is malformed")
    if validated_epoch > time.time() + 300:
        fail("phase receipt validation timestamp is in the future")
    if validated_epoch < 1784230275:
        fail("phase receipt predates the persisted worker goal")
    if not isinstance(receipt.get("receipt_id"), str) or not receipt["receipt_id"]:
        fail("phase receipt lacks an identity")
    if receipt.get("acceptance_authority") != "Stage1 integration lane":
        fail("phase receipt acceptance authority changed")
    if receipt.get("accepted") is not False or receipt.get("verdict") != "blocked":
        fail("phase receipt overstates acceptance")
    if receipt.get("support_state") != "provisional_worker_selftest":
        fail("phase receipt support state changed")
    if receipt.get("proposed_state") != "[_]" or receipt.get("selftest_status") != "passed":
        fail("phase receipt does not preserve a self-tested negative handoff")
    if receipt.get("first_failed_gate") != FAILED_GATE:
        fail("phase receipt first failed gate changed")
    if receipt.get("statement_fingerprints") != []:
        fail("phase receipt invents a statement fingerprint")
    if receipt.get("mutation_tests") != load(ROLE_PATHS["statement_record"])["mutation_tests"]:
        fail("receipt and statement mutation boundaries disagree")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("phase receipt overstates a terminal decision")
    if receipt.get("semantic_result") != SEMANTIC:
        fail("receipt and validator semantic result disagree")
    result = receipt.get("selftest_result", {})
    if result.get("exit_code") != 0 or not isinstance(result.get("commands"), list):
        fail("phase receipt lacks a successful exact command inventory")
    if not result["commands"]:
        fail("phase receipt command inventory is empty")
    if not isinstance(result.get("output_summary"), str) or not result["output_summary"]:
        fail("phase receipt lacks a self-test output summary")
    for field in ("known_failures", "invalidation_inputs"):
        value = receipt.get(field)
        if (
            not isinstance(value, list)
            or not value
            or any(not isinstance(row, str) or not row for row in value)
        ):
            fail(f"phase receipt {field} is malformed")
    for field in ("retry_condition", "status_boundary"):
        if not isinstance(receipt.get(field), str) or not receipt[field]:
            fail(f"phase receipt {field} is malformed")

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

    packet = load(".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }:
        fail("worker packet field set changed")
    if packet.get("item_id") != ITEM_ID or packet.get("state") != "[_]":
        fail("worker packet identity or state changed")
    if packet.get("base_revision") != BASE_REVISION:
        fail("worker packet base revision changed")
    if packet.get("commands") != result["commands"]:
        fail("worker packet and receipt command records disagree")
    if packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet and receipt known failures disagree")
    if packet.get("changed_paths") != EXPECTED_CHANGED_PATHS:
        fail("worker packet changed-path inventory changed")


def validate_semantic_shape() -> None:
    allowed = {
        "schema_version",
        "item_id",
        "theorem_id",
        "phase",
        "status",
        "verdict",
        "phase_accepted",
        "audit_complete",
        "theorem_complete",
        "phase_predicate_proven",
        "first_failed_gate",
        "open_obligations",
        "stale_inputs",
        "blocked",
        "message",
    }
    required = allowed - {"message"}
    if set(SEMANTIC) not in (required, allowed):
        fail("validator semantic result does not use the exact scheduler field set")
    if SEMANTIC["schema_version"] != "stage1-validator-semantic-result/1.0":
        fail("validator semantic schema changed")
    for field in (
        "phase_accepted",
        "audit_complete",
        "theorem_complete",
        "phase_predicate_proven",
        "blocked",
    ):
        if not isinstance(SEMANTIC[field], bool):
            fail(f"validator semantic field {field} is not boolean")
    if (
        not isinstance(SEMANTIC["open_obligations"], int)
        or isinstance(SEMANTIC["open_obligations"], bool)
        or SEMANTIC["open_obligations"] < 0
    ):
        fail("validator semantic open_obligations is malformed")
    stale = SEMANTIC["stale_inputs"]
    if not isinstance(stale, list) or len(stale) != len(set(stale)):
        fail("validator semantic stale_inputs is malformed")


def main() -> None:
    validate_authority()
    validate_ledger()
    validate_statement_boundary()
    validate_receipt_and_packet()
    validate_semantic_shape()
    print(json.dumps(SEMANTIC, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
