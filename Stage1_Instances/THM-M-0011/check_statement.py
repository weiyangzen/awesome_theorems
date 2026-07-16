#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0011 statement packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0011"
THEOREM_ID = "THM-M-0011"
ITEM_ID = "S56-M-0011-STATEMENT"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
FAILED_GATE = "S02-EXACT-TARGET.source_statement_identity"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0011/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0011/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0011/source_statement_crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0011/statement-receipt.json",
}
EXPECTED_ROLE_HASHES = {
    "statement_record": "11eaf50d1705cecbea6985a169c31fa07b761ef6b0cef6bbfce0c06cce725f81",
    "statement_source": "d08488ca253c4aa1970e0e5e5053e7c0629436eea41f47890868549e909620ff",
    "source_crosswalk": "400ff7c438501457dbb05fde86797d121b8569ea2bb229085e812d15d7aac87a",
}
EXPECTED_ROLE_BLOBS = {
    "statement_record": "237deed7c265b2c4dc863e467ebe31623a1950c6",
    "statement_source": "04da0aa1ec101a29bb415530df20c1d45b137321",
    "source_crosswalk": "7008c76410b14753576b26a51eccb02cf12ad702",
}
EXPECTED_AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": "fb6cd286dc5c47e22d754ab73e5162986e98a18b5bc6d8e7213ae5d39b4256d1",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "80b2ad4e2943128eeff5b4b2446dc0057a978de003d9c90140567d2f32aca5af",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_SUPPORT_HASHES = {
    "Stage1_Instances/THM-M-0011/intake.json": "cc27300eadedced160c47dc87ae683b8dc3f0f81e603cc55895e3225b725bf06",
    "Stage1_Instances/THM-M-0011/statement-blocker.md": "f564328b781c967c7afd51d7c1d4561c0330cd43bad4a32817752ef84152a9b6",
    "Stage1_Instances/THM-M-0011/dependency-reuse-ledger.json": "bb084c4fb0d2bf78f6ff263def2c9c938aa67ccf04b8c1f4c886b0cf7b17aae9",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_104.lean": "64de9ae48c5f0b6902fea34f1f24a445f3a17deb4d8617738e813510c74f7b7a",
    "Formalizations/Lean/.lake/packages/mathlib/Mathlib/Algebra/Category/ModuleCat/Descent.lean": "dac6c87bd1a670bb875089061f357d2026118e9408ada42d6ad6070bc831d477",
}
DIRECT_IMPORT = "Mathlib.Algebra.Category.ModuleCat.Descent"
CHECKS = (
    "ModuleCat.extendScalars",
    "ModuleCat.preservesFiniteLimits_extendScalars_of_flat",
    "ModuleCat.reflectsIsomorphisms_extendScalars_of_faithfullyFlat",
    "comonadicExtendScalars",
)
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    re.MULTILINE,
)
CANONICAL_DECLARATION = re.compile(
    r"^[ \t]*(?:def|theorem|lemma|example|abbrev|opaque|axiom)\s+"
    r".*(?:Target|Statement|DescentShape)",
    re.MULTILINE | re.IGNORECASE,
)


def fail(message: str) -> NoReturn:
    raise ValueError(message)


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


def sha256(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def git_blob(relative: str) -> str:
    data = (ROOT / relative).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git(*argv: str) -> str:
    result = subprocess.run(
        ["/usr/bin/git", *argv],
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
        fail("validator requires Python assertions to remain enabled")
    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("repository HEAD differs from the worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("repository base tree differs from the receipt")
    for relative, expected in EXPECTED_AUTHORITY_HASHES.items():
        if sha256(relative) != expected:
            fail(f"authority input changed: {relative}")
    for relative, expected in EXPECTED_SUPPORT_HASHES.items():
        if sha256(relative) != expected:
            fail(f"support input changed: {relative}")

    manifest = load("Docs/Stage1_Targets_rev-5.6.json")
    target = next(
        row for row in manifest["targets"] if row.get("theorem_id") == THEOREM_ID
    )
    if target.get("execution_rank") != 104 or target.get("lifecycle_mode") != "planned":
        fail("target manifest identity or lifecycle changed")
    if target.get("baseline") != "L0" or target.get("rework_required") is not True:
        fail("uniform L0 rework boundary changed")
    if target.get("legacy_artifacts_accepted") is not False:
        fail("legacy evidence unexpectedly acquired acceptance")

    execution = load("Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row.get("id") == ITEM_ID)
    if item != {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 104,
        "phase": "statement",
        "layer": 1,
        "state": "[ ]",
        "depends_on": ["S56-M-0011-INTAKE"],
        "owned_paths": ["Stage1_Instances/THM-M-0011"],
        "deliverable": "Elaborate the exact Lean 4 target with the minimal pinned imports.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }:
        fail("authoritative statement item changed")

    dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in dag["theorems"] if row.get("theorem_id") == THEOREM_ID)
    if node.get("v2_execution_rank") != 320 or node.get("topological_layer") != 0:
        fail("v2 claim order changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency context changed")
    if node.get("phase_states", {}).get("intake") != "[_]":
        fail("intake predecessor observation changed")
    if node.get("phase_states", {}).get("statement") != "[ ]":
        fail("statement authority state changed")
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
    if validators != ["Stage1_Instances/THM-M-0011/check_statement.py"]:
        fail("validator candidate selection is not exactly one path")
    if phase.get("intent") != "audit" or phase.get("layer") != 1:
        fail("statement intent or layer changed")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("statement contract unexpectedly permits blocked phase closure")
    if phase.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        fail("negative finding unexpectedly became phase-completing")
    if [row.get("gate_id") for row in phase.get("semantic_gates", [])] != [
        "S01-ARTIFACTS",
        "S02-EXACT-TARGET",
        "S03-MUTATIONS",
    ]:
        fail("statement semantic gate set changed")


def validate_ledger() -> None:
    ledger = load("Stage1_Instances/THM-M-0011/dependency-reuse-ledger.json")
    if ledger.get("schema_version") != "stage1-dependency-reuse-ledger/1.1":
        fail("dependency ledger schema changed")
    if ledger.get("consumer_theorem_id") != THEOREM_ID:
        fail("dependency ledger owner changed")
    if ledger.get("observed_theorem_dag_sha256") != GRAPH_SHA256:
        fail("dependency ledger graph binding changed")
    if ledger.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency ledger context binding changed")
    if ledger.get("repository_revision") != BASE_REVISION:
        fail("dependency ledger base changed")
    if ledger.get("claim_order") != {
        "v2_execution_rank": 320,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        fail("dependency ledger claim order changed")
    for field in (
        "direct_parent_ids",
        "transitive_ancestor_ids",
        "hard_edge_ids",
        "reuse_hint_ids",
        "shared_group_ids",
        "parent_inspection_order",
        "inspections",
        "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        if ledger.get(field) != []:
            fail(f"empty dependency ledger field {field} changed")
    closure = ledger.get("closure_audit", {})
    if closure.get("inspection_order") != []:
        fail("empty parent inspection order changed")
    if closure.get("status") != "empty_complete_closure_audited":
        fail("empty closure audit status changed")


def validate_statement_boundary() -> None:
    record = load(ROLE_PATHS["statement_record"])
    intake = load("Stage1_Instances/THM-M-0011/intake.json")
    source = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    blocker = (HERE / "statement-blocker.md").read_text(encoding="utf-8")
    legacy = (
        ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_104.lean"
    ).read_text(encoding="utf-8")

    for role, expected in EXPECTED_ROLE_HASHES.items():
        if sha256(ROLE_PATHS[role]) != expected:
            fail(f"selected artifact bytes changed: {role}")
        if git_blob(ROLE_PATHS[role]) != EXPECTED_ROLE_BLOBS[role]:
            fail(f"selected artifact Git blob changed: {role}")

    if record.get("schema_version") != "stage1-statement/1.0":
        fail("statement record schema changed")
    if record.get("item_id") != ITEM_ID or record.get("theorem_id") != THEOREM_ID:
        fail("statement record identity changed")
    if record.get("canonical_claim_status") != "blocked_source_statement_identity_unresolved":
        fail("source ambiguity is no longer explicit")
    if record.get("canonical_statement") is not None:
        fail("a canonical mathematical statement was invented")
    formal = record.get("canonical_formal_target", {})
    for field in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_sha256",
        "environment_expression_fingerprint",
    ):
        if formal.get(field) is not None:
            fail(f"a canonical target field was invented: {field}")
    if record.get("statement_fingerprints") != [] or record.get("alternate_encodings") != []:
        fail("a statement fingerprint or transport was invented")
    if record.get("candidate_surface_probe", {}).get("direct_imports") != [DIRECT_IMPORT]:
        fail("candidate probe import record changed")
    if tuple(record.get("candidate_surface_probe", {}).get("checked_vocabulary", [])) != CHECKS:
        fail("candidate probe vocabulary record changed")
    mutations = record.get("mutation_tests", {})
    if set(mutations) != {
        "removed_hypothesis",
        "changed_domain",
        "changed_binder_scope",
        "boundary_case",
    }:
        fail("statement mutation inventory is incomplete")
    if any(
        value != {"status": "not_run_missing_canonical_target", "passed": False}
        for value in mutations.values()
    ):
        fail("statement record falsely claims a mutation result")
    if record.get("first_failed_gate") != FAILED_GATE:
        fail("statement record first failed gate changed")
    if any(
        record.get(field) is not False
        for field in (
            "statement_elaborated",
            "phase_predicate_proven",
            "phase_accepted",
            "audit_complete",
            "theorem_complete",
        )
    ):
        fail("statement record overstates acceptance or completion")

    imports = re.findall(r"^import ([^\s]+)$", source, re.MULTILINE)
    if imports != [DIRECT_IMPORT]:
        fail("boundary probe does not have exactly the recorded direct import")
    checks = tuple(re.findall(r"^#check ([^\s]+)$", source, re.MULTILINE))
    if checks != CHECKS:
        fail("boundary probe checked vocabulary changed")
    if PROHIBITED.search(source):
        fail("boundary probe contains a prohibited trust construct")
    if CANONICAL_DECLARATION.search(source):
        fail("boundary probe unexpectedly declares a canonical formula")

    if intake.get("canonical_formal_target", {}).get("gate_state") != (
        "blocked_pending_primary_source_disambiguation"
    ):
        fail("intake source-identity boundary changed")
    if intake.get("canonical_statement") is not None:
        fail("intake unexpectedly claims a canonical statement")
    required_terms = (
        "Exact premise and boundary mapping",
        "Required resolution",
        "no statement or proof credit",
        "H2",
        "S02-EXACT-TARGET",
        "phase_accepted=false",
    )
    combined = crosswalk + "\n" + blocker
    if any(term not in combined for term in required_terms):
        fail("crosswalk or blocker omits the fail-closed statement boundary")
    if "def ModuleCategoryDescentShape" not in legacy or "def StatementShape" not in legacy:
        fail("legacy discovery boundary changed")
    if "not the terminal flat descent theorem" not in legacy:
        fail("legacy non-credit warning changed")


def validate_receipt_and_packet() -> None:
    receipt = load(ROLE_PATHS["phase_receipt"])
    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row.get("phase") == "statement")
    required = {
        pointer.removeprefix("/")
        for pointer in phase.get("phase_receipt_required_fields", [])
        if isinstance(pointer, str) and pointer.count("/") == 1
    }
    if not required <= set(receipt):
        fail("phase receipt omits a contract-required field")
    if receipt.get("schema_version") != "stage1-node-receipt/1.0":
        fail("phase receipt schema changed")
    if (
        receipt.get("item_id"),
        receipt.get("theorem_id"),
        receipt.get("phase"),
        receipt.get("intent"),
    ) != (ITEM_ID, THEOREM_ID, "statement", "audit"):
        fail("phase receipt identity changed")
    if receipt.get("base_revision") != BASE_REVISION or receipt.get("base_tree") != BASE_TREE:
        fail("phase receipt base changed")
    if receipt.get("accepted") is not False or receipt.get("verdict") != "blocked":
        fail("phase receipt does not preserve blocked semantics")
    if receipt.get("proposed_state") != "[_]" or receipt.get("selftest_status") != "passed":
        fail("phase receipt does not preserve the self-tested handoff")
    result = receipt.get("selftest_result", {})
    if result.get("exit_code") != 0 or result.get("phase_predicate_passed") is not False:
        fail("receipt confuses blocker self-test with phase predicate success")
    if not isinstance(result.get("commands"), list) or not result["commands"]:
        fail("phase receipt has no exact command list")
    if receipt.get("statement_fingerprints") != []:
        fail("phase receipt invents a statement fingerprint")
    if receipt.get("mutation_tests") != load(ROLE_PATHS["statement_record"])["mutation_tests"]:
        fail("receipt and statement mutation boundaries disagree")
    if receipt.get("first_failed_gate") != FAILED_GATE:
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
        fail("worker packet base changed")
    if packet.get("commands") != result.get("commands"):
        fail("worker packet commands differ from phase receipt")
    if packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet known failures differ from phase receipt")
    expected_changed = [
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0011/Statement.lean",
        "Stage1_Instances/THM-M-0011/check_statement.py",
        "Stage1_Instances/THM-M-0011/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0011/source_statement_crosswalk.md",
        "Stage1_Instances/THM-M-0011/statement-blocker.md",
        "Stage1_Instances/THM-M-0011/statement-receipt.json",
        "Stage1_Instances/THM-M-0011/statement.json",
    ]
    if packet.get("changed_paths") != expected_changed:
        fail("worker packet changed-path inventory changed")


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
        "first_failed_gate": FAILED_GATE,
        "open_obligations": 5,
        "stale_inputs": [],
        "blocked": True,
        "message": message,
    }


def main() -> None:
    try:
        validate_authority()
        validate_ledger()
        validate_statement_boundary()
        validate_receipt_and_packet()
    except Exception as error:
        print(
            json.dumps(
                {
                    **semantic_result(message=f"negative statement packet failed: {error}"),
                    "status": "failed",
                    "verdict": "repair_required",
                    "first_failed_gate": "S01-ARTIFACTS",
                    "blocked": False,
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        raise SystemExit(1)
    print(
        json.dumps(
            semantic_result(
                message=(
                    "The target-owned packet truthfully proves that the broad flat-descent "
                    "source phrase has no source-selected exact Lean proposition; statement "
                    "acceptance remains blocked."
                )
            ),
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
