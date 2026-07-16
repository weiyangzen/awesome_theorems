#!/usr/bin/env python3
"""Validate THM-M-0444's fail-closed statement evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0444"
ITEM_ID = "S56-M-0444-STATEMENT"
THEOREM_ID = "THM-M-0444"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
FAILED_GATE = "S02-EXACT-TARGET.primary_source_statement_identity_unfrozen"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0444/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0444/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0444/source_statement_crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0444/statement-receipt.json",
}
EXPECTED_ROLE_HASHES = {
    "statement_record": "5cc0f5238a583df68986480dc7312a61960e58f7fda24625621227cb2856d116",
    "statement_source": "a2ae08205993d371e97f7ccbb2fe9a700b7eff377c276d25b8187d9a6671cf39",
    "source_crosswalk": "20a16fabd57063b67b54c8e01f4e0461ceacf0e9668d6849a1ea4ff40db26640",
}
EXPECTED_ROLE_BLOBS = {
    "statement_record": "d93d785172f9a6b7eac50c3f10145c4485f7f69b",
    "statement_source": "2c710cc552e93cf6aa3d9e57acf5200f6925a9c5",
    "source_crosswalk": "5cbfde9cd7dc67aa23418d06942fa0f4762108a5",
}
EXPECTED_AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": "fb6cd286dc5c47e22d754ab73e5162986e98a18b5bc6d8e7213ae5d39b4256d1",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_SUPPORT_HASHES = {
    "Stage1_Instances/THM-M-0444/intake.json": "7ee08b41629add299b7013428c614b3635b4d78d7da9f3edc0fd5c5de7bc28cd",
    "Stage1_Instances/THM-M-0444/statement-blocker.md": "4b7d6c536f1bda14908639da894b0a5808f4194ff95d4559d702b029d633248e",
    "Stage1_Instances/THM-M-0444/dependency-reuse-ledger.json": "ba35c5d5079eb1f7a1e6ea3ea7c9f1f561a1ff0cd466c4eb25eeceb402ecc022",
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_090.lean": "50c776ffe34f43a11629d861b17bf95368ba96d71072d40e0f34c568e9b75fb2",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
}
DIRECT_IMPORTS = (
    "Mathlib.FieldTheory.AbsoluteGaloisGroup",
    "Mathlib.RingTheory.DedekindDomain.SelmerGroup",
)
SUBSTRATE_IMPORT_HASHES = {
    "Mathlib.FieldTheory.AbsoluteGaloisGroup": "38daa87cc8e19a26540c69cb76c798395e409b563ccabd3344e2012b0b3e6fcd",
    "Mathlib.RingTheory.DedekindDomain.SelmerGroup": "238f31314887756c132820f486e2658e8055d11b14ff45bf2fbafa44f08a3137",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)
DECLARATION = re.compile(
    r"^[ \t]*(?:def|theorem|lemma|example|abbrev|opaque|axiom|structure|class|inductive)\s+",
    flags=re.MULTILINE,
)


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def load(relative: str) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate JSON key {key!r} in {relative}")
            result[key] = value
        return result

    value = json.loads(
        (ROOT / relative).read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicates,
    )
    if not isinstance(value, dict):
        fail(f"{relative} must contain one JSON object")
    return value


def sha256(relative: str) -> str:
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
    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("repository HEAD differs from the claimed worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("repository tree differs from the claimed worker base")
    for relative, expected in EXPECTED_AUTHORITY_HASHES.items():
        if sha256(relative) != expected:
            fail(f"authority input changed: {relative}")
    for relative, expected in EXPECTED_SUPPORT_HASHES.items():
        if sha256(relative) != expected:
            fail(f"support input changed: {relative}")

    targets = load("Docs/Stage1_Targets_rev-5.6.json")
    target = next(
        row for row in targets["targets"] if row.get("theorem_id") == THEOREM_ID
    )
    if (
        target.get("execution_rank") != 90
        or target.get("lifecycle_mode") != "planned"
        or target.get("legacy_artifacts_accepted") is not False
        or target.get("theorem_complete") is not False
    ):
        fail("target manifest identity or boundary changed")

    execution = load("Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row.get("id") == ITEM_ID)
    expected_item = {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 90,
        "phase": "statement",
        "layer": 1,
        "state": "[ ]",
        "depends_on": ["S56-M-0444-INTAKE"],
        "owned_paths": ["Stage1_Instances/THM-M-0444"],
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
    if node.get("v2_execution_rank") != 314 or node.get("topological_layer") != 0:
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
    if validators != ["Stage1_Instances/THM-M-0444/check_statement.py"]:
        fail("validator candidate selection is not exactly one path")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("statement contract unexpectedly permits blocked phase closure")
    if phase.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        fail("statement contract unexpectedly treats negative findings as the deliverable")


def validate_ledger() -> None:
    ledger = load("Stage1_Instances/THM-M-0444/dependency-reuse-ledger.json")
    expected_empty_fields = (
        "direct_parent_ids",
        "transitive_ancestor_ids",
        "hard_edge_ids",
        "reuse_hint_ids",
        "shared_group_ids",
        "inspections",
        "reuse_decisions",
        "unresolved_compatibility_obligations",
    )
    if any(ledger.get(field) != [] for field in expected_empty_fields):
        fail("dependency ledger is not the exact empty context")
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
    closure = ledger.get("closure_audit", {})
    if (
        closure.get("parent_inspection_order") != []
        or closure.get("status") != "empty_complete_closure_audited"
    ):
        fail("dependency closure audit changed")


def validate_statement_boundary() -> None:
    statement = load(ROLE_PATHS["statement_record"])
    source = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    blocker = (HERE / "statement-blocker.md").read_text(encoding="utf-8")
    intake = load("Stage1_Instances/THM-M-0444/intake.json")
    legacy = (
        ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_090.lean"
    ).read_text(encoding="utf-8")

    for role, expected in EXPECTED_ROLE_HASHES.items():
        if sha256(ROLE_PATHS[role]) != expected:
            fail(f"selected artifact bytes changed: {role}")
        if git_blob(ROLE_PATHS[role]) != EXPECTED_ROLE_BLOBS[role]:
            fail(f"selected artifact Git blob changed: {role}")

    if statement.get("schema_version") != "stage1-statement/1.0":
        fail("statement record schema changed")
    if statement.get("item_id") != ITEM_ID or statement.get("theorem_id") != THEOREM_ID:
        fail("statement record identity changed")
    if statement.get("canonical_claim_status") != "blocked_pending_primary_source_statement_identification":
        fail("statement ambiguity is no longer explicit")
    formal = statement.get("canonical_formal_target", {})
    if statement.get("canonical_statement") is not None:
        fail("a canonical mathematical statement was invented")
    for field in (
        "declaration_or_expression",
        "elaborated_expression_sha256",
        "environment_fingerprint_sha256",
    ):
        if formal.get(field) is not None:
            fail("a canonical expression or fingerprint was invented")
    if formal.get("statement_file_sha256") != EXPECTED_ROLE_HASHES["statement_source"]:
        fail("statement source binding is stale")
    if tuple(statement.get("direct_imports", [])) != DIRECT_IMPORTS:
        fail("structured direct imports changed")
    mutations = statement.get("mutation_tests")
    if mutations != {
        "removed_hypothesis": "undefined_without_canonical_statement",
        "changed_domain": "undefined_without_canonical_statement",
        "changed_binder_scope": "undefined_without_canonical_statement",
        "boundary_case": "undefined_without_canonical_statement",
    }:
        fail("undefined mutation boundary changed")
    if statement.get("statement_elaborated") is not False:
        fail("statement record falsely claims exact target elaboration")
    if statement.get("audit_complete") is not False or statement.get("theorem_complete") is not False:
        fail("statement record falsely closes a terminal decision")
    context = statement.get("dependency_reuse_audit", {})
    if (
        context.get("graph_sha256") != GRAPH_SHA256
        or context.get("dependency_context_sha256") != CONTEXT_SHA256
        or context.get("parent_inspection_order") != []
        or context.get("reuse_decisions") != []
    ):
        fail("statement dependency audit changed")

    imports = tuple(re.findall(r"^import ([^\s]+)$", source, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        fail("boundary source direct imports changed")
    if PROHIBITED.search(source):
        fail("boundary source contains a prohibited placeholder or trust construct")
    if DECLARATION.search(source):
        fail("boundary source unexpectedly declares a target or local object model")
    checks = tuple(re.findall(r"^#check ([^\s]+)$", source, re.MULTILINE))
    if checks != ("Field.absoluteGaloisGroup", "IsDedekindDomain.selmerGroup"):
        fail("boundary interface probes changed")

    combined = crosswalk + "\n" + blocker
    for term in (
        "construction of an Euler system",
        "Frobenius convention",
        "no exact canonical Lean target",
        "parent_inspection_order",
    ):
        if term not in combined:
            fail("source ambiguity or dependency boundary is incomplete")
    if intake.get("canonical_statement") is not None:
        fail("intake unexpectedly supplies a canonical statement")
    if "structure KolyvaginEulerSystemConstructionData" not in legacy:
        fail("legacy abstract construction interface changed")
    if "def StatementShape" not in legacy:
        fail("legacy StatementShape discovery declaration changed")
    if "deliberately weaker than a terminal theorem" not in legacy:
        fail("legacy non-credit boundary changed")

    mathlib = ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib"
    if git("-C", str(mathlib), "rev-parse", "HEAD") != "8a178386ffc0f5fef0b77738bb5449d50efeea95":
        fail("materialized mathlib revision changed")
    if git("-C", str(mathlib), "rev-parse", "HEAD^{tree}") != "bdc39a3123201dae413a9d9be56ec242c19e5c2b":
        fail("materialized mathlib tree changed")
    environment = statement.get("environment_fingerprint", {})
    if environment.get("lean_toolchain") != "leanprover/lean4:v4.29.0":
        fail("structured Lean toolchain changed")
    if environment.get("mathlib_revision") != "8a178386ffc0f5fef0b77738bb5449d50efeea95":
        fail("structured mathlib revision changed")
    for module, expected in SUBSTRATE_IMPORT_HASHES.items():
        relative = (
            "Formalizations/Lean/.lake/packages/mathlib/"
            + module.replace(".", "/")
            + ".lean"
        )
        if sha256(relative) != expected:
            fail(f"pinned substrate import changed: {module}")


def validate_receipt_and_packet() -> None:
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
    if receipt.get("selftest_result", {}).get("exit_code") != 0:
        fail("phase receipt self-test exit changed")
    commands = receipt.get("selftest_result", {}).get("commands")
    if not isinstance(commands, list) or not commands:
        fail("phase receipt has no exact commands")
    if receipt.get("statement_fingerprints") != []:
        fail("phase receipt invents a statement fingerprint")
    if receipt.get("first_failed_gate") != FAILED_GATE:
        fail("phase receipt first failed gate changed")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("phase receipt falsely closes a terminal decision")
    if receipt.get("inputs", {}).get("parent_inspection_order") != []:
        fail("phase receipt parent inspection order changed")
    if receipt.get("inputs", {}).get("provider_acceptance_inherited") is not False:
        fail("phase receipt transfers provider acceptance")
    if receipt.get("claim_order") != {
        "v2_execution_rank": 314,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        fail("phase receipt claim order changed")

    bindings = receipt.get("artifact_bindings", {})
    if set(bindings) != set(ROLE_PATHS):
        fail("phase receipt selected role bindings are incomplete")
    for role in EXPECTED_ROLE_HASHES:
        binding = bindings.get(role, {})
        if binding != {
            "role": role,
            "path": ROLE_PATHS[role],
            "sha256": EXPECTED_ROLE_HASHES[role],
            "git_blob": EXPECTED_ROLE_BLOBS[role],
        }:
            fail(f"phase receipt role binding changed: {role}")
    self_binding = bindings.get("phase_receipt", {})
    if self_binding.get("path") != ROLE_PATHS["phase_receipt"]:
        fail("phase receipt self-binding path changed")
    if self_binding.get("sha256") is not None or self_binding.get("git_blob") is not None:
        fail("phase receipt self-binding must remain scheduler-owned and acyclic")

    validator_binding = receipt.get("inputs", {}).get("statement_validator", {})
    if validator_binding != {
        "path": "Stage1_Instances/THM-M-0444/check_statement.py",
        "sha256": sha256("Stage1_Instances/THM-M-0444/check_statement.py"),
        "git_blob": git_blob("Stage1_Instances/THM-M-0444/check_statement.py"),
        "status": "worker_owned_not_present_at_base_requires_current_base_revalidation",
    }:
        fail("phase receipt validator binding is stale")

    packet = load(".stage1-worker-selftest.json")
    expected_packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    if set(packet) != expected_packet_fields:
        fail("worker packet fields changed")
    if packet.get("item_id") != ITEM_ID or packet.get("state") != "[_]":
        fail("worker packet identity or state changed")
    if packet.get("base_revision") != BASE_REVISION:
        fail("worker packet base changed")
    if packet.get("commands") != commands:
        fail("worker packet commands differ from the phase receipt")
    if packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet known failures differ from the phase receipt")
    if packet.get("changed_paths") != receipt.get("changed_paths"):
        fail("worker packet changed paths differ from the phase receipt")


def check() -> None:
    validate_authority()
    validate_ledger()
    validate_statement_boundary()
    validate_receipt_and_packet()


def semantic_result(*, failed: bool = False, message: str = "") -> dict[str, Any]:
    if failed:
        return {
            "schema_version": "stage1-validator-semantic-result/1.0",
            "item_id": ITEM_ID,
            "theorem_id": THEOREM_ID,
            "phase": "statement",
            "status": "failed",
            "verdict": "repair_required",
            "phase_accepted": False,
            "audit_complete": False,
            "theorem_complete": False,
            "phase_predicate_proven": False,
            "first_failed_gate": "S01-ARTIFACTS.negative_evidence_validation",
            "open_obligations": 5,
            "stale_inputs": [],
            "blocked": False,
            "message": message,
        }
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
        "message": (
            "Negative statement evidence is internally consistent, but no exact source-"
            "authorized proposition, expression fingerprint, checked transport, or mutation "
            "suite exists; S56-M-0444-STATEMENT remains open."
        ),
    }


def main() -> None:
    try:
        check()
    except Exception as error:
        print(
            json.dumps(
                semantic_result(failed=True, message=str(error)),
                ensure_ascii=True,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        raise SystemExit(1)
    print(
        json.dumps(
            semantic_result(),
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
