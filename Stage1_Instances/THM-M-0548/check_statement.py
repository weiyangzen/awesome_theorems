#!/usr/bin/env python3
"""Validate the truthful negative statement packet for THM-M-0548."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0548"
ITEM_ID = "S56-M-0548-STATEMENT"
THEOREM_ID = "THM-M-0548"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0548/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0548/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0548/source_statement_crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0548/statement-receipt.json",
}
EXPECTED_ROLE_HASHES = {
    "statement_record": "54a5d5d216cc19ff1a23fd6681ced9b19c2576f4d16eb59b9e39d072eb18ace6",
    "statement_source": "c70ec17e76aa2dff0ad5aac5597df7220478c96f6fcdc90b1dada916721f4895",
    "source_crosswalk": "ae24060d042591ba3e8011649731faaab2aa7a0e2e4a58d961e73f46f4d41121",
}
EXPECTED_ROLE_BLOBS = {
    "statement_record": "57fd6e00f0e629db4d1c4e71ff14ab67cfe40526",
    "statement_source": "a33aa5a31e6138b729489dec6976ab34547fad40",
    "source_crosswalk": "c346ee2da4713facdd902b84e744e457bebd8dc6",
}
EXPECTED_AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": "fb6cd286dc5c47e22d754ab73e5162986e98a18b5bc6d8e7213ae5d39b4256d1",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "skills/execute-stage1-rev56/SKILL.md": "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_SUPPORT_HASHES = {
    "Stage1_Instances/THM-M-0548/dependency-reuse-ledger.json": (
        "dcceb771cd12594c3fb9558443cfc26b33d2e96c9fc963f0c124d9d648b348bb"
    ),
    "Stage1_Instances/THM-M-0548/statement-blocker.md": (
        "bd502a3d85d5b29a4bea7238f8a1413bd43af66830c7b0ca95c05fa9df1a19a3"
    ),
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_120.lean": (
        "9f69cf532d8a8131b980fe03fd76d78a91d9b131f2cec3efd986fb4531435f56"
    ),
}
DIRECT_IMPORTS = (
    "Mathlib.AlgebraicTopology.SingularHomology.Basic",
    "Mathlib.Topology.Category.TopCat.Sphere",
    "Mathlib.Topology.Homotopy.LocallyContractible",
)
EXPECTED_CHECKS = (
    "Stage1Instances.THM_M_0548.SubsetHypotheses",
    "Stage1Instances.THM_M_0548.OrdinaryComplementSingularHomology",
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
    r"(?:AlexanderDuality|CanonicalTarget|StatementShape)",
    flags=re.MULTILINE | re.IGNORECASE,
)


class ValidatorError(ValueError):
    pass


def fail(message: str) -> NoReturn:
    raise ValidatorError(message)


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
        check=False,
    )
    if result.returncode:
        fail(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def validate_authority() -> None:
    if sys.flags.optimize != 0:
        fail("statement validator requires normal Python semantics")
    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("repository HEAD differs from the claimed worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("repository tree differs from the claimed worker base")
    for relative, expected in EXPECTED_AUTHORITY_HASHES.items():
        if digest(relative) != expected:
            fail(f"authority or pinned-environment input changed: {relative}")
    for relative, expected in EXPECTED_SUPPORT_HASHES.items():
        if digest(relative) != expected:
            fail(f"support input changed: {relative}")

    targets = load("Docs/Stage1_Targets_rev-5.6.json")
    target = next(
        row for row in targets["targets"] if row.get("theorem_id") == THEOREM_ID
    )
    if target.get("execution_rank") != 120 or target.get("lifecycle_mode") != "planned":
        fail("target manifest identity or lifecycle changed")
    if target.get("legacy_artifacts_accepted") is not False:
        fail("legacy evidence unexpectedly acquired acceptance")

    execution = load("Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row.get("id") == ITEM_ID)
    expected_item = {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 120,
        "phase": "statement",
        "layer": 1,
        "state": "[ ]",
        "depends_on": ["S56-M-0548-INTAKE"],
        "owned_paths": ["Stage1_Instances/THM-M-0548"],
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
    if node.get("v2_execution_rank") != 336 or node.get("topological_layer") != 0:
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
    if validators != ["Stage1_Instances/THM-M-0548/check_statement.py"]:
        fail("validator candidate selection is not exactly one path")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("statement contract unexpectedly permits blocked phase closure")
    if phase.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        fail("statement contract unexpectedly treats a negative finding as the deliverable")
    if [row.get("gate_id") for row in phase.get("semantic_gates", [])] != [
        "S01-ARTIFACTS",
        "S02-EXACT-TARGET",
        "S03-MUTATIONS",
    ]:
        fail("statement semantic gate set changed")

    changed = subprocess.run(
        ["git", "status", "--porcelain", "--", "Stage1_Instances/THM-M-0548"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    if changed.returncode:
        fail("could not inspect the target-owned worktree delta")
    actual_changed = sorted(line[3:] for line in changed.stdout.splitlines() if len(line) > 3)
    expected_changed = sorted(
        [
            "Stage1_Instances/THM-M-0548/Statement.lean",
            "Stage1_Instances/THM-M-0548/check_statement.py",
            "Stage1_Instances/THM-M-0548/dependency-reuse-ledger.json",
            "Stage1_Instances/THM-M-0548/source_statement_crosswalk.md",
            "Stage1_Instances/THM-M-0548/statement-blocker.md",
            "Stage1_Instances/THM-M-0548/statement-receipt.json",
            "Stage1_Instances/THM-M-0548/statement.json",
        ]
    )
    if actual_changed != expected_changed:
        fail("target-owned worktree delta differs from the handoff inventory")


def validate_ledger() -> None:
    ledger = load("Stage1_Instances/THM-M-0548/dependency-reuse-ledger.json")
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
        fail("empty closure is not marked completely audited")
    if closure.get("claim_order") != {
        "v2_execution_rank": 336,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        fail("claim-order binding changed")


def validate_statement_boundary() -> None:
    statement = load(ROLE_PATHS["statement_record"])
    source = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    blocker = (HERE / "statement-blocker.md").read_text(encoding="utf-8")
    repository_source = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    legacy = (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_120.lean").read_text(
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
    if statement.get("canonical_claim_status") != (
        "blocked_on_primary_source_and_claim_disambiguation"
    ):
        fail("statement ambiguity is no longer explicit")
    formal = statement.get("canonical_formal_target", {})
    if statement.get("canonical_statement") is not None:
        fail("a canonical mathematical statement was invented")
    for field in (
        "declaration_or_expression",
        "elaborated_expression_sha256",
        "environment_expression_fingerprint",
    ):
        if formal.get(field) is not None:
            fail(f"a missing canonical target field was invented: {field}")
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
        fail("boundary source unexpectedly declares a canonical Alexander-duality target")
    checks = tuple(re.findall(r"^#check ([^\s]+)$", source, re.MULTILINE))
    if checks != EXPECTED_CHECKS:
        fail("boundary interface probes changed")
    required_terms = (
        "coefficient",
        "reduced",
        "grading",
        "naturality",
        "phase_accepted=false",
    )
    combined = crosswalk + "\n" + blocker
    if any(term not in combined for term in required_terms):
        fail("source ambiguity or non-credit boundary is incomplete")
    if "**亚历山大对偶**" not in repository_source or "陈述: 球面中子空间的对偶" not in repository_source:
        fail("repository source record changed")
    legacy_terms = (
        "subsetReducedCohomology",
        "dualityIso",
        "StatementShape",
        "alexanderDualityMissingAPILeaves_repoLocalClosed_eq",
        "formalization_debt",
    )
    if any(term not in legacy for term in legacy_terms):
        fail("legacy non-closure boundary changed")


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
    if (
        receipt.get("proposed_state") != "[_]"
        or receipt.get("support_state") != "provisional_worker_selftest_blocked"
        or receipt.get("selftest_status") != "passed"
        or receipt.get("selftest_result", {}).get("phase_predicate_passed") is not False
    ):
        fail("phase receipt does not preserve the self-tested negative handoff")
    if receipt.get("statement_fingerprints") != []:
        fail("phase receipt invents a statement fingerprint")
    if receipt.get("first_failed_gate") != "S02-EXACT-TARGET.source_statement_ambiguity":
        fail("phase receipt first failed gate changed")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("phase receipt falsely closes a terminal decision")
    if receipt.get("owner") != "Stage1 rev-5.6 execution lane":
        fail("phase receipt owner changed")
    if not receipt.get("validated_at") or not receipt.get("review_due"):
        fail("phase receipt freshness metadata is incomplete")
    if not receipt.get("supersession_state") or not receipt.get("incident_path"):
        fail("phase receipt maintenance metadata is incomplete")
    debt = receipt.get("debt_vector", {})
    if debt.get("before") != debt.get("after") or debt.get("after") != {
        "human": "H1", "machine": "M3", "readability": "R3"
    }:
        fail("phase receipt debt boundary changed")
    if receipt.get("inputs", {}).get("parent_inspection_order") != []:
        fail("phase receipt parent inspection order changed")
    if receipt.get("inputs", {}).get("provider_acceptance_inherited") is not False:
        fail("phase receipt transfers provider acceptance")
    expected_mutations = {
        "removed_hypothesis",
        "changed_domain",
        "changed_binder_scope",
        "boundary_case",
    }
    mutation_rows = receipt.get("mutation_tests", [])
    if {row.get("kind") for row in mutation_rows if isinstance(row, dict)} != expected_mutations:
        fail("phase receipt mutation classes are incomplete")
    if any(row.get("passed") is not False for row in mutation_rows):
        fail("phase receipt falsely passes a statement mutation")

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
    for role, relative in (
        ("dependency_reuse_ledger", "Stage1_Instances/THM-M-0548/dependency-reuse-ledger.json"),
        ("statement_blocker", "Stage1_Instances/THM-M-0548/statement-blocker.md"),
    ):
        binding = support_bindings.get(role, {})
        if binding.get("path") != relative:
            fail(f"phase receipt support path changed: {role}")
        if binding.get("sha256") != digest(relative):
            fail(f"phase receipt support SHA-256 binding changed: {role}")
        if binding.get("git_blob") != git_blob(relative):
            fail(f"phase receipt support Git-blob binding changed: {role}")
    validator_binding = support_bindings.get("statement_validator", {})
    if validator_binding.get("path") != "Stage1_Instances/THM-M-0548/check_statement.py":
        fail("phase receipt validator support path changed")
    if validator_binding.get("sha256") is not None or validator_binding.get("git_blob") is not None:
        fail("worker receipt must not pretend its new validator is already HEAD selected")

    packet = load(".stage1-worker-selftest.json")
    packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    if set(packet) != packet_fields:
        fail("worker packet field set changed")
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
        "Stage1_Instances/THM-M-0548/Statement.lean",
        "Stage1_Instances/THM-M-0548/check_statement.py",
        "Stage1_Instances/THM-M-0548/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0548/source_statement_crosswalk.md",
        "Stage1_Instances/THM-M-0548/statement-blocker.md",
        "Stage1_Instances/THM-M-0548/statement-receipt.json",
        "Stage1_Instances/THM-M-0548/statement.json",
    ]:
        fail("worker packet changed-path inventory changed")
    if receipt.get("changed_paths") != packet.get("changed_paths"):
        fail("phase receipt changed paths differ from the worker packet")


def semantic_result(*, message: str) -> dict[str, Any]:
    return {
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
        "first_failed_gate": "S02-EXACT-TARGET.source_statement_ambiguity",
        "open_obligations": 4,
        "stale_inputs": [],
        "blocked": True,
        "message": message,
    }


def main() -> None:
    try:
        validate_authority()
        validate_ledger()
        validate_statement_boundary()
        validate_receipt()
    except Exception as error:
        result = {
            **semantic_result(message=f"negative statement packet validation failed: {error}"),
            "status": "failed",
            "verdict": "repair_required",
            "first_failed_gate": "S01-ARTIFACTS",
            "blocked": False,
        }
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    result = semantic_result(
        message=(
            "The target-owned packet truthfully proves that the source wording does not select "
            "one exact Alexander-duality proposition; statement acceptance remains blocked."
        )
    )
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
