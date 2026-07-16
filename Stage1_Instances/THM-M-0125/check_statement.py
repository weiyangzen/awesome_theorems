#!/usr/bin/env python3
"""Validate the fail-closed statement boundary for THM-M-0125."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0125"
THEOREM_ID = "THM-M-0125"
ITEM_ID = "S56-M-0125-STATEMENT"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0125/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0125/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0125/source_statement_crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0125/statement-receipt.json",
}
EXPECTED_ROLE_HASHES = {
    "statement_record": "a62bbef664d3b40d46a601307d2309970c9b901037e0ded22d33896b26966da8",
    "statement_source": "703b821642de7156e91648769418c1008114452fd227917da0dfab5eb6d0301a",
    "source_crosswalk": "ac17f736a03d24333ccd52a2859d5199443b82c750bf822399f78dfa7be24188",
}
EXPECTED_ROLE_BLOBS = {
    "statement_record": "ecad0f2eab95ef99b2e10a3dd6316c58fe5a83ca",
    "statement_source": "75e1f493705537b6e575bfa002e7a93018380f0a",
    "source_crosswalk": "c39f0599b9c2cf6fe20aaf1e58590f660cdd3eaf",
}
EXPECTED_AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": "fb6cd286dc5c47e22d754ab73e5162986e98a18b5bc6d8e7213ae5d39b4256d1",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "skills/execute-stage1-rev56/SKILL.md": "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_SUPPORT_HASHES = {
    "Stage1_Instances/THM-M-0125/dependency-reuse-ledger.json": (
        "6d2e96000aea3f060a4862c3544b0befd9249f7bbe623dec6b15993e1ec83a65"
    ),
    "Stage1_Instances/THM-M-0125/intake.json": (
        "60571d758e44688b959028a28c70e160091e63a8b02ee634509296987d338f85"
    ),
    "Stage1_Instances/THM-M-0125/statement-blocker.md": (
        "b5bd05b469d276e81534d2ff5ab261661e94b31d3e659ec5c776e0b793fcf70f"
    ),
    "Stage1_Instances/THM-M-0125/statement-phase-blocker-2026-07-17-head-1cc6aa61-slot92.md": (
        "e8158c8f5bd3d47ca139db12f648ad1c6d1beeef917491652bf7f4aff23ecc56"
    ),
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_044.lean": (
        "30198b949c774f5de2e19cbcda28d60fe03962698e9a9a7ed9f2acc301028f52"
    ),
    "Docs/researches/math_theorems.md": (
        "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29"
    ),
}
DIRECT_IMPORTS = (
    "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
    "Mathlib.Analysis.Calculus.Deriv.Basic",
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
    r"(?:GrossZagier|CanonicalTarget|StatementShape|ExpectedFormula)",
    flags=re.MULTILINE | re.IGNORECASE,
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


def digest(relative: str) -> str:
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
        fail("statement validator requires Python assertions enabled")
    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("repository HEAD differs from the claimed worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("repository base tree differs from the claimed worker base")
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
    if target.get("execution_rank") != 44 or target.get("lifecycle_mode") != "planned":
        fail("target manifest identity or lifecycle changed")
    if target.get("legacy_artifacts_accepted") is not False:
        fail("legacy evidence unexpectedly acquired acceptance")

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    expected_item = (
        "- [ ] `S56-M-0125-STATEMENT` / `THM-M-0125` / `statement`: "
        "Elaborate the exact Lean 4 target with the minimal pinned imports. {attempts=0}"
    )
    if blueprint.count(expected_item) != 1:
        fail("task-state authority no longer contains the exact open statement item once")
    expected_dependency = (
        "Depends: `S56-M-0125-INTAKE`. Owned paths: "
        "`Stage1_Instances/THM-M-0125`. Gate: rev-5.6 node-specific receipt and master acceptance."
    )
    if expected_dependency not in blueprint:
        fail("task-state dependency or owned path changed")

    theorem_dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    node = next(
        row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM_ID
    )
    if node.get("v2_execution_rank") != 278 or node.get("topological_layer") != 0:
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
    if validators != ["Stage1_Instances/THM-M-0125/check_statement.py"]:
        fail("validator candidate selection is not exactly one path")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("statement contract unexpectedly permits blocked phase closure")
    if phase.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        fail("statement contract unexpectedly treats negative findings as the deliverable")


def validate_ledger() -> None:
    ledger = load("Stage1_Instances/THM-M-0125/dependency-reuse-ledger.json")
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
    if ledger.get("claim_order") != {
        "v2_execution_rank": 278,
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


def validate_statement_boundary() -> None:
    statement = load(ROLE_PATHS["statement_record"])
    source = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    blocker = (
        HERE / "statement-phase-blocker-2026-07-17-head-1cc6aa61-slot92.md"
    ).read_text(encoding="utf-8")
    intake = load("Stage1_Instances/THM-M-0125/intake.json")
    legacy = (
        ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_044.lean"
    ).read_text(encoding="utf-8")

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
        "blocked_pending_source_variant_and_normalization_freeze"
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
        fail("boundary source unexpectedly declares a canonical Gross-Zagier target")
    checks = tuple(re.findall(r"^#check ([^\s]+)$", source, re.MULTILINE))
    if checks != ("WeierstrassCurve", "HasDerivAt"):
        fail("boundary interface probes changed")

    combined = crosswalk + "\n" + blocker
    required_terms = (
        "Gross-Zagier",
        "I.(6.3)",
        "I.(7.3)",
        "V.(2.1)",
        "declares no",
        "phase_accepted=false",
    )
    if any(term not in combined for term in required_terms):
        fail("source ambiguity or non-credit boundary is incomplete")
    if "Gross-Zagier" not in str(intake.get("canonical_statement")):
        fail("intake-selected source family changed")
    if "structure GrossZagierStatementData" not in legacy:
        fail("legacy discovery declaration changed")
    if "def expectedFormula" not in legacy:
        fail("legacy abstract formula boundary changed")


def validate_receipt() -> None:
    receipt = load(ROLE_PATHS["phase_receipt"])
    required = {
        "schema_version",
        "receipt_id",
        "item_id",
        "theorem_id",
        "phase",
        "intent",
        "base_revision",
        "base_tree",
        "inputs",
        "support_state",
        "proposed_state",
        "accepted",
        "verdict",
        "selftest_status",
        "selftest_result",
        "known_failures",
        "first_failed_gate",
        "retry_condition",
        "status_boundary",
        "audit_complete",
        "theorem_complete",
        "invalidation_inputs",
        "statement_fingerprints",
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
    selftest = receipt.get("selftest_result", {})
    if selftest.get("exit_code") != 0 or selftest.get("phase_predicate_passed") is not False:
        fail("phase receipt confuses packet self-test with phase acceptance")
    if not selftest.get("commands"):
        fail("phase receipt has no exact self-test commands")
    if receipt.get("statement_fingerprints") != []:
        fail("phase receipt invents a statement fingerprint")
    if receipt.get("first_failed_gate") != (
        "S02-EXACT-TARGET.source_variant_and_normalization_unfrozen"
    ):
        fail("phase receipt first failed gate changed")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("phase receipt falsely closes a terminal decision")
    inputs = receipt.get("inputs", {})
    if inputs.get("parent_inspection_order") != []:
        fail("phase receipt parent inspection order changed")
    if inputs.get("provider_acceptance_inherited") is not False:
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
    expected_packet_fields = {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    if set(packet) != expected_packet_fields:
        fail("worker packet fields changed")
    if packet.get("item_id") != ITEM_ID or packet.get("state") != "[_]":
        fail("worker packet identity or state changed")
    if packet.get("base_revision") != BASE_REVISION:
        fail("worker packet base changed")
    if packet.get("commands") != selftest.get("commands"):
        fail("worker packet commands differ from the phase receipt")
    if packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet known failures differ from the phase receipt")
    expected_changed = [
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0125/Statement.lean",
        "Stage1_Instances/THM-M-0125/check_statement.py",
        "Stage1_Instances/THM-M-0125/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0125/source_statement_crosswalk.md",
        "Stage1_Instances/THM-M-0125/statement-phase-blocker-2026-07-17-head-1cc6aa61-slot92.md",
        "Stage1_Instances/THM-M-0125/statement-receipt.json",
        "Stage1_Instances/THM-M-0125/statement.json",
    ]
    if packet.get("changed_paths") != expected_changed:
        fail("worker packet changed-path inventory changed")


def semantic_result(*, verified: bool, error: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "phase": "statement",
        "status": "blocked" if verified else "failed",
        "verdict": "blocked" if verified else "repair_required",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": (
            "S02-EXACT-TARGET.source_variant_and_normalization_unfrozen"
            if verified
            else "S01-ARTIFACTS"
        ),
        "open_obligations": 5,
        "stale_inputs": [],
        "blocked": verified,
        "message": (
            "Negative statement boundary self-tested: the source variant, normalization, "
            "canonical Lean target, expression fingerprint, checked transports, and four "
            "mutation classes remain open."
            if verified
            else f"negative statement packet validation failed: {error}"
        ),
    }
    return result


def main() -> None:
    try:
        validate_authority()
        validate_ledger()
        validate_statement_boundary()
        validate_receipt()
    except Exception as error:
        print(json.dumps(semantic_result(verified=False, error=str(error)), sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    print(json.dumps(semantic_result(verified=True), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
