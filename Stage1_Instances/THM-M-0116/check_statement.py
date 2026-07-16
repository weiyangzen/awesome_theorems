#!/usr/bin/env python3
"""Validate the truthful negative statement packet for THM-M-0116."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0116"
ITEM_ID = "S56-M-0116-STATEMENT"
THEOREM_ID = "THM-M-0116"
BASE_REVISION = "307c34d30fc3763c82a944a142ae922b48ff18aa"
BASE_TREE = "ef45ba442c71959db78ad146a023bcf32946a53f"
GRAPH_SHA256 = "8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0116/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0116/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0116/source-statement-crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0116/statement-receipt.json",
}
EXPECTED_ROLE_HASHES = {
    "statement_record": "1afd57928c3832167a0ded39de974b1f74fc468c69d4ecaf5d0f8167492c3d92",
    "statement_source": "d4eaffad0956faa2007216583512d5a7ddc1f888f6472feb040db1b987532da5",
    "source_crosswalk": "0afb81148a3196b36b435639a31655d98758efd7f9ac1f5f7485619f18555d5b",
}
EXPECTED_ROLE_BLOBS = {
    "statement_record": "1a9fc50fa0272ea31fd7ae68f79e707ac8e5f060",
    "statement_source": "9407ab309c2108efea394b039188688c33b671e6",
    "source_crosswalk": "94d7a7644d834993297dbdd59890850111871d5c",
}
EXPECTED_AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": "2a5bc7d397e03969aac1a9f8f21b437152b8ef63ef453055acf67857ced628b5",
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
    "Stage1_Instances/THM-M-0116/dependency-reuse-ledger.json": (
        "bf6b8b9ee7a068165a70fc585e0563cd0deac6d4002940300560a9f222f712dc"
    ),
    "Stage1_Instances/THM-M-0116/statement-phase-blocker-2026-07-17-head-307c34d3-slot59.md": (
        "91f6696088d13779cfcd30b5bdb3377342bdb881680d8862aa47b22471028989"
    ),
    "Stage1_Instances/THM-M-0116/statement-blocker.json": (
        "c29baceebc1c5603741e78f4f82a65e3c270988511f70b24589baab8d416eaae"
    ),
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_036.lean": (
        "4fe36fb20b2b80a169d1d78753d81bdbaf423acc1de8fc8d1d2346b6b5410964"
    ),
    "Docs/researches/math_theorems.md": (
        "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29"
    ),
}
DIRECT_IMPORTS = (
    "Mathlib.AlgebraicGeometry.AlgClosed.Basic",
    "Mathlib.AlgebraicGeometry.Morphisms.Proper",
    "Mathlib.AlgebraicGeometry.Morphisms.Smooth",
    "Mathlib.AlgebraicGeometry.ProjectiveSpectrum.Proper",
    "Mathlib.GroupTheory.Finiteness",
    "Mathlib.RingTheory.PicardGroup",
)
EXPECTED_CHECKS = (
    "Scheme",
    "Spec",
    "IsAlgClosed",
    "IsProper",
    "Smooth",
    "SmoothOfRelativeDimension",
    "Proj.toSpecZero",
    "AddCon",
    "AddCon.Quotient",
    "AddGroup.FG",
    "CommRing.Pic",
)
EXPECTED_FAILURE_CHECKS = (
    "NeronSeveriGroup",
    "AlgebraicGeometry.IsProjective",
)
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)
CANONICAL_DECLARATION = re.compile(
    r"^[ \t]*(?:def|theorem|lemma|example|abbrev|opaque|axiom)\s+.*"
    r"(?:Neron|Severi|CanonicalTarget|StatementTarget)",
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

    target = next(
        row
        for row in load("Docs/Stage1_Targets_rev-5.6.json")["targets"]
        if row.get("theorem_id") == THEOREM_ID
    )
    if target.get("execution_rank") != 36 or target.get("lifecycle_mode") != "planned":
        fail("target manifest identity or lifecycle changed")
    if target.get("legacy_artifacts_accepted") is not False:
        fail("legacy evidence unexpectedly acquired acceptance")

    execution = load("Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row.get("id") == ITEM_ID)
    if item != {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 36,
        "phase": "statement",
        "layer": 1,
        "state": "[ ]",
        "depends_on": ["S56-M-0116-INTAKE"],
        "owned_paths": ["Stage1_Instances/THM-M-0116"],
        "deliverable": "Elaborate the exact Lean 4 target with the minimal pinned imports.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }:
        fail("authoritative statement item changed")

    theorem_dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    node = next(
        row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM_ID
    )
    if node.get("v2_execution_rank") != 271 or node.get("topological_layer") != 0:
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
    if validators != ["Stage1_Instances/THM-M-0116/check_statement.py"]:
        fail("validator candidate selection is not exactly one path")
    if phase.get("intent") != "audit":
        fail("statement contract intent changed")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("statement contract unexpectedly permits blocked phase closure")
    if phase.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        fail("statement contract unexpectedly treats negative findings as the deliverable")

    changed = subprocess.run(
        ["/usr/bin/git", "status", "--porcelain", "--", "Stage1_Instances/THM-M-0116"],
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
            "Stage1_Instances/THM-M-0116/Statement.lean",
            "Stage1_Instances/THM-M-0116/check_statement.py",
            "Stage1_Instances/THM-M-0116/dependency-reuse-ledger.json",
            "Stage1_Instances/THM-M-0116/statement-phase-blocker-2026-07-17-head-307c34d3-slot59.md",
            "Stage1_Instances/THM-M-0116/statement-receipt.json",
            "Stage1_Instances/THM-M-0116/statement.json",
        ]
    )
    if actual_changed != expected_changed:
        fail("target-owned worktree delta differs from the handoff inventory")


def validate_ledger() -> None:
    ledger = load("Stage1_Instances/THM-M-0116/dependency-reuse-ledger.json")
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
    if closure.get("claim_order") != {
        "v2_execution_rank": 271,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        fail("ledger claim order changed")
    if closure.get("provider_acceptance_inherited") is not False:
        fail("ledger transfers provider acceptance")


def validate_statement_boundary() -> None:
    statement = load(ROLE_PATHS["statement_record"])
    source = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    blocker = (HERE / "statement-phase-blocker-2026-07-17-head-307c34d3-slot59.md").read_text(
        encoding="utf-8"
    )
    repository_source = (ROOT / "Docs/researches/math_theorems.md").read_text(
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
    if statement.get("canonical_claim_status") != "human_claim_frozen_lean_target_blocked":
        fail("statement blocker classification changed")
    if "Neron-Severi group" not in statement.get("canonical_statement", ""):
        fail("frozen human statement changed")
    formal = statement.get("canonical_formal_target", {})
    for field in (
        "declaration_or_expression",
        "elaborated_expression_sha256",
        "environment_expression_fingerprint",
    ):
        if formal.get(field) is not None:
            fail(f"statement record invented formal target field {field}")
    if tuple(statement.get("direct_imports", [])) != DIRECT_IMPORTS:
        fail("statement boundary imports changed")
    if statement.get("checked_alternate_encodings") != []:
        fail("statement record invents a checked transport")
    if statement.get("statement_fingerprints") != []:
        fail("statement record invents a fingerprint")
    mutations = statement.get("mutation_tests", {})
    if mutations.get("executed") != [] or mutations.get("status") != "blocked_without_canonical_expression":
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
        fail("boundary source unexpectedly declares a canonical target")
    checks = tuple(re.findall(r"^#check ([^\s]+)$", source, re.MULTILINE))
    failures = tuple(re.findall(r"^#check_failure ([^\s]+)$", source, re.MULTILINE))
    if checks != EXPECTED_CHECKS or failures != EXPECTED_FAILURE_CHECKS:
        fail("boundary interface probes changed")
    required_terms = (
        "algebraic equivalence",
        "projectivity",
        "Neron-Severi quotient",
        "provider",
        "no canonical",
    )
    combined = crosswalk + "\n" + blocker + "\n" + source
    if any(term not in combined for term in required_terms):
        fail("source or non-reuse boundary is incomplete")
    if "塞韦里群有限生成定理" not in repository_source or "Néron-Severi群有限生成" not in repository_source:
        fail("repository source record changed")


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
    if receipt.get("claim_order") != {
        "v2_execution_rank": 271,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        fail("phase receipt claim order changed")
    if receipt.get("accepted") is not False or receipt.get("verdict") != "blocked":
        fail("phase receipt no longer preserves the negative verdict")
    if receipt.get("proposed_state") != "[_]" or receipt.get("selftest_status") != "passed":
        fail("phase receipt does not preserve the self-tested negative handoff")
    result = receipt.get("selftest_result", {})
    if result.get("exit_code") != 0 or result.get("phase_predicate_passed") is not False:
        fail("phase receipt confuses packet self-test with phase completion")
    if not isinstance(result.get("commands"), list) or not result["commands"]:
        fail("phase receipt lacks exact self-test commands")
    if receipt.get("statement_fingerprints") != []:
        fail("phase receipt invents a statement fingerprint")
    if receipt.get("first_failed_gate") != (
        "S02-EXACT-TARGET.missing_projective_surface_and_concrete_neron_severi_interfaces"
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

    packet = load(".stage1-worker-selftest.json")
    if packet.get("item_id") != ITEM_ID or packet.get("state") != "[_]":
        fail("worker packet identity or state changed")
    if packet.get("base_revision") != BASE_REVISION:
        fail("worker packet base changed")
    if packet.get("commands") != result.get("commands"):
        fail("worker packet commands differ from the phase receipt")
    if packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet known failures differ from the phase receipt")
    if packet.get("changed_paths") != [
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0116/Statement.lean",
        "Stage1_Instances/THM-M-0116/check_statement.py",
        "Stage1_Instances/THM-M-0116/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0116/statement-phase-blocker-2026-07-17-head-307c34d3-slot59.md",
        "Stage1_Instances/THM-M-0116/statement-receipt.json",
        "Stage1_Instances/THM-M-0116/statement.json",
    ]:
        fail("worker packet changed-path inventory changed")


def semantic_result(*, message: str, status: str = "blocked") -> dict[str, Any]:
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "phase": "statement",
        "status": status,
        "verdict": "blocked" if status == "blocked" else "repair_required",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": (
            "S02-EXACT-TARGET.missing_projective_surface_and_concrete_neron_severi_interfaces"
            if status == "blocked"
            else "S01-ARTIFACTS"
        ),
        "open_obligations": 6,
        "stale_inputs": [],
        "blocked": status == "blocked",
        "message": message,
    }


def main() -> None:
    try:
        validate_authority()
        validate_ledger()
        validate_statement_boundary()
        validate_receipt()
    except Exception as error:
        print(
            json.dumps(
                semantic_result(
                    message=f"negative statement packet validation failed: {error}",
                    status="failed",
                ),
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        raise SystemExit(1)
    print(
        json.dumps(
            semantic_result(
                message=(
                    "Negative statement boundary self-tested: the exact Neron-Severi target, "
                    "expression fingerprint, checked transports, and four mutations remain blocked."
                )
            ),
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
