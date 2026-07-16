#!/usr/bin/env python3
"""Offline semantic validator for S56-M-0148-ANCHOR_AUDIT."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM_ID = "S56-M-0148-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0148"
PHASE = "anchor_audit"
BASE_REVISION = "307c34d30fc3763c82a944a142ae922b48ff18aa"
BASE_TREE = "ef45ba442c71959db78ad146a023bcf32946a53f"
GRAPH_SHA256 = "8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
PROTOCOL_SHA256 = "358a5fe2c951993d4bac9dc57573ed7d35504acec10937ad5d096210c292e62f"
EVIDENCE_SHA256 = "00e1ac8e17ec07d0bbe9ad3e86d0f4ac35819d883953d721c4e1b45d630132e4"
LEDGER_SHA256 = "a61a966c948da57335087bf6bac0d98015d29acd65d9a405fa8029baed638582"
AUDIT_SHA256 = "f6015d12dae644c0b9237bf56fe44d450fee6f7fccb93c637997d3d117fcd7c5"
VALIDATION_SHA256 = "bae6371aa8ad29997f5d6b47657f2b603a60fd076283a43b3e2a0f701ae232c1"
STATEMENT_SHA256 = "dc927360172cd822b1532b3070c916a7e5c2ee7ff7d98954ea94f8c78e8b4846"
STATEMENT_RECORD_SHA256 = "9104f6f1a895b246f273d886e79e41ccf328786c34ceba09006b0d236eacd3ba"
STATEMENT_RECEIPT_SHA256 = "2b7def3418e259ab2368a843084f67cca3bbafef6faa496f63913a5573800694"
LEGACY_SHA256 = "4f1c156407bc7c2d4c24d8007e82357558e5ae16c842569da9bdbc2e3eb93212"
LEGACY_ORIGIN = "16d227cffb7cb7d9e8392b6c0ff8211e498e1330"
LEGACY_ORIGIN_TREE = "4f823e2d768f1b3542a8462acec7cadc24a6c9e5"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"

ORDERED_LANES = [
    "repo_local",
    "pinned_mathlib",
    "official_primary_projects",
    "other_immutable_public_projects",
    "statement_only_collections",
    "historical_or_other_provers",
    "primary_human_sources",
]
MACHINE_STATES = {"M0-L", "M0-W", "M0-P", "M1", "M2", "M3", "M4", "M5"}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
    f"Stage1_Instances/{THEOREM_ID}/dependency-reuse-ledger.json",
    f"Stage1_Instances/{THEOREM_ID}/discovery-evidence.json",
    f"Stage1_Instances/{THEOREM_ID}/discovery-protocol.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_object(path: Path) -> str:
    return hashlib.sha1(b"blob " + str(path.stat().st_size).encode() + b"\0" + path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path} is not a JSON object")
    return value


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def normalize_classification(value: str) -> str:
    for state in sorted(MACHINE_STATES, key=len, reverse=True):
        if value == state or value.startswith(state + "_") or value.startswith(state + " "):
            return state
    raise AssertionError(f"unsupported classification {value!r}")


def resolve_evidence_artifact(artifact: dict) -> tuple[Path, Path, str]:
    relative = str(artifact["path"])
    prefix = "Formalizations/Lean/.lake/packages/mathlib/"
    if relative.startswith(prefix):
        package_relative = Path(relative.removeprefix(prefix))
        return ROOT / relative, MATHLIB, str(package_relative)
    return ROOT / relative, ROOT, relative


def validate_receipt_fields(receipt: dict, contract: dict) -> None:
    phase_contract = next(row for row in contract["phases"] if row["phase"] == PHASE)
    for pointer in phase_contract["phase_receipt_required_fields"]:
        value: object = receipt
        for token in pointer.strip("/").split("/"):
            require(isinstance(value, dict) and token in value,
                    f"receipt missing required pointer {pointer}")
            value = value[token]


def validate_role_bindings(receipt: dict) -> None:
    role_paths = {
        "anchor_inventory": {f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json"},
        "discovery_evidence": {f"Stage1_Instances/{THEOREM_ID}/discovery-evidence.json"},
        "phase_receipt": {f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json"},
    }
    bindings = receipt["selected_artifact_bindings"]
    require(len(bindings) == 3, "selected artifact role cardinality drift")
    require({binding["role"] for binding in bindings} == set(role_paths),
            "selected artifact roles drift")
    for binding in bindings:
        require(binding["path"] in role_paths[binding["role"]],
                f"wrong path for role {binding['role']}")
        if binding["role"] != "phase_receipt":
            path = ROOT / binding["path"]
            require(sha256(path) == binding["sha256"], f"role SHA drift: {path}")
            require(git_object(path) == binding["git_blob"], f"role Git object drift: {path}")
        else:
            require(binding["sha256"] is None and binding["git_blob"] is None,
                    "self-referential receipt must defer its own binding")


def validate_worker_packet(receipt: dict) -> None:
    packet_path = ROOT / ".stage1-worker-selftest.json"
    require(packet_path.is_file() and not packet_path.is_symlink(),
            "worker self-test packet is missing")
    packet = load(packet_path)
    require(set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }, "worker packet fields drift")
    require(packet["item_id"] == ITEM_ID and packet["state"] == "[_]",
            "worker packet identity/state drift")
    require(packet["base_revision"] == BASE_REVISION, "worker packet base drift")
    require(set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS,
            "worker changed-path scope drift")
    require(packet["commands"] == receipt["selftest_result"]["commands"],
            "worker and receipt command lists differ")
    require(packet["known_failures"] == receipt["known_failures"],
            "worker and receipt failure boundaries differ")
    require(packet["output_summary"] == receipt["selftest_result"]["output_summary"],
            "worker and receipt summaries differ")


def validate() -> None:
    protocol = load(HERE / "discovery-protocol.json")
    evidence = load(HERE / "discovery-evidence.json")
    ledger = load(HERE / "dependency-reuse-ledger.json")
    audit = load(HERE / "anchor-audit.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement_record = load(HERE / "statement.json")
    statement_receipt = load(HERE / "statement-receipt.json")
    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    theorem_dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    receipt_candidates = [
        HERE / "anchor-audit-receipt.json",
        HERE / "anchor_audit_receipt.json",
        HERE / "anchor-receipt.json",
    ]
    validator_candidates = [HERE / "check_anchor_audit.py", HERE / "check_anchor.py"]
    require([path.name for path in receipt_candidates if path.exists()]
            == ["anchor-audit-receipt.json"], "phase receipt cardinality drift")
    require([path.name for path in validator_candidates if path.exists()]
            == ["check_anchor_audit.py"], "phase validator cardinality drift")
    require(not (HERE / "AnchorAudit.lean").exists(),
            "conditional machine-candidate probe appeared without an audited binding")

    require(output("git", "rev-parse", "HEAD") == BASE_REVISION, "repository revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE, "repository tree drift")
    require(sha256(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") == CONTRACT_SHA256,
            "phase contract drift")
    require(sha256(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") == GRAPH_SHA256,
            "theorem DAG drift")
    require(sha256(HERE / "Statement.lean") == STATEMENT_SHA256, "statement probe drift")
    require(sha256(HERE / "statement.json") == STATEMENT_RECORD_SHA256,
            "statement record drift")
    require(sha256(HERE / "statement-receipt.json") == STATEMENT_RECEIPT_SHA256,
            "statement receipt drift")
    require(sha256(HERE / "discovery-protocol.json") == PROTOCOL_SHA256,
            "discovery protocol drift")
    require(sha256(HERE / "discovery-evidence.json") == EVIDENCE_SHA256,
            "discovery evidence drift")
    require(sha256(HERE / "dependency-reuse-ledger.json") == LEDGER_SHA256,
            "dependency ledger drift")
    require(sha256(HERE / "anchor-audit.json") == AUDIT_SHA256,
            "anchor inventory drift")
    require(sha256(HERE / "anchor-audit-validation.md") == VALIDATION_SHA256,
            "validation record drift")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    require(target["execution_rank"] == 28, "target execution rank drift")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "target assurance baseline drift")
    require(target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False,
            "target lifecycle boundary drift")
    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    require(node["v2_execution_rank"] == 265, "v2 execution rank drift")
    require(node["phase_states"]["statement"] == "[_]"
            and node["phase_states"][PHASE] == "[ ]", "authoritative phase frontier drift")
    require(node["direct_hard_parents"] == [] and node["transitive_hard_ancestors"] == [],
            "hard-parent closure is no longer empty")
    require(node["direct_reuse_hint_ids"] == [] and node["shared_lemma_group_ids"] == [],
            "hint/shared context is no longer empty")
    require(node["dependency_context_sha256"] == CONTEXT_SHA256, "context digest drift")

    require(ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1",
            "wrong dependency ledger schema")
    require(ledger["consumer_theorem_id"] == THEOREM_ID, "ledger consumer drift")
    require(ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256,
            "ledger graph mismatch")
    require(ledger["dependency_context_sha256"] == CONTEXT_SHA256,
            "ledger context mismatch")
    require(ledger["repository_revision"] == BASE_REVISION, "ledger revision mismatch")
    require(ledger["claim_order"] == {
        "v2_execution_rank": 265,
        "phase_layer": 2,
        "phase_item_id": ITEM_ID,
    }, "claim order mismatch")
    for field in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "parent_inspection_order",
        "inspections", "reuse_decisions", "unresolved_compatibility_obligations",
    ):
        require(ledger[field] == [], f"declared empty context drift at {field}")
    require(ledger["closure_audit"]["status"] == "empty_declared_context_inspected",
            "empty closure was not audited")

    require(protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0",
            "wrong discovery protocol schema")
    require(protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID,
            "protocol identity mismatch")
    require(protocol["precommitted_before_replay"] is True, "protocol is not precommitted")
    require(protocol["saturation_claim"] is False, "protocol overclaims saturation")
    require(protocol["canonical_target"]["declaration"] is None
            and protocol["canonical_target"]["normalized_claim"] is None,
            "protocol invents a canonical target")
    require([row["lane"] for row in protocol["ordered_search_lanes"]] == ORDERED_LANES,
            "protocol lane order mismatch")
    require(len(protocol["alias_families"]) >= 18, "alias family is incomplete")
    for field in (
        "credentials_policy", "expected_negative_result_evidence", "network_policy",
        "immutable_refresh_policy",
    ):
        require(protocol.get(field), f"protocol lacks {field}")

    require(evidence["schema_version"] == "stage1-anchor-discovery-evidence/1.0",
            "wrong discovery evidence schema")
    require(evidence["item_id"] == ITEM_ID and evidence["theorem_id"] == THEOREM_ID,
            "evidence identity mismatch")
    require(evidence["inventory_version"] == protocol["inventory_version"],
            "inventory version mismatch")
    require(evidence["network_used_for_replay"] is False, "offline replay used network")
    lane_results = evidence["ordered_lane_results"]
    require([row["lane"] for row in lane_results] == ORDERED_LANES,
            "evidence lane order mismatch")
    for row in lane_results:
        require(all(row.get(field) for field in (
            "query_or_source", "revision", "result", "access_boundary", "reopen_condition",
        )), f"incomplete lane result: {row['lane']}")
        require(isinstance(row.get("evidence"), list) and row["evidence"],
                f"unbound lane result: {row['lane']}")
        for artifact in row["evidence"]:
            path, repository, repository_path = resolve_evidence_artifact(artifact)
            require(path.is_file() and not path.is_symlink(), f"evidence missing: {path}")
            require(sha256(path) == artifact["sha256"], f"evidence SHA drift: {path}")
            require(output("git", "rev-parse", f"HEAD:{repository_path}", cwd=repository)
                    == artifact["git_blob"], f"evidence Git blob drift: {path}")

    require(audit["schema_version"] == "stage1-anchor-audit/1.0",
            "wrong audit schema")
    require(audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID,
            "audit identity mismatch")
    require(audit["phase"] == PHASE and audit["intent"] == "audit",
            "audit phase/intent drift")
    require(audit["execution_rank"] == 28 and audit["v2_execution_rank"] == 265
            and audit["phase_layer"] == 2, "audit claim order mismatch")
    require(audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE,
            "audit base mismatch")
    require(audit["canonical_target"]["declaration"] is None
            and audit["canonical_target"]["statement_status"] == "blocked_unfrozen",
            "audit invents a canonical target")
    require(audit["discovery_protocol"]["sha256"] == PROTOCOL_SHA256,
            "audit protocol binding mismatch")
    require(audit["discovery_evidence"]["sha256"] == EVIDENCE_SHA256,
            "audit evidence binding mismatch")
    require(audit["dependency_reuse_context"]["sha256"] == LEDGER_SHA256,
            "audit ledger binding mismatch")
    require(audit["search_order_completed"] == ORDERED_LANES,
            "audit search order mismatch")
    candidates = audit["candidates"]
    require(len(candidates) == 7, "candidate inventory size drift")
    require(len({candidate["candidate_id"] for candidate in candidates}) == len(candidates),
            "duplicate candidate identity")
    for candidate in candidates:
        require(normalize_classification(candidate["classification"]) in MACHINE_STATES,
                f"candidate classification invalid: {candidate['candidate_id']}")
        require(all(candidate.get(field) for field in (
            "exact_type", "normalized_match", "toolchain", "dependency_feasibility",
            "proof_body", "placeholder_axiom_unsafe_oracle_status", "blocker", "reopen_event",
        )), f"candidate provenance/classification incomplete: {candidate['candidate_id']}")
        require(candidate["completion_credit"] is False,
                f"candidate improperly receives proof credit: {candidate['candidate_id']}")
    require({normalize_classification(row["classification"]) for row in candidates}
            == {"M3", "M4", "M5"}, "unexpected candidate state set")
    access = next(row for row in candidates
                  if row["candidate_id"] == "M0148-C06-PUBLIC-CODE-AND-REGISTRY-ACCESS-FAILURES")
    require(access["classification"] == "M5", "access failures are not M5")
    legacy = next(row for row in candidates
                  if row["candidate_id"] == "M0148-C02-LEGACY-PARAMETERIZED-STATEMENT-SHAPES")
    require(legacy["origin_revision"] == LEGACY_ORIGIN
            and legacy["origin_tree"] == LEGACY_ORIGIN_TREE,
            "legacy origin binding drift")
    require(legacy["source_sha256"] == LEGACY_SHA256, "legacy source binding drift")
    coverage = audit["classification_coverage"]
    require(coverage["classified_candidates"] == coverage["inventory_size"] == 7,
            "candidate classification coverage incomplete")
    require(coverage["prescribed_lanes_completed"] == coverage["prescribed_lane_count"] == 7,
            "prescribed lane coverage incomplete")
    require(coverage["complete_for_inventory_version"] is True,
            "inventory version is not completely classified")
    require(coverage["discovery_saturation_claimed"] is False,
            "audit overclaims discovery saturation")
    require(coverage["exact_terminal_candidate_found"] is False
            and coverage["candidate_comparison_limited_by_unfrozen_statement"] is True,
            "audit contradicts exact-target boundary")
    require(audit["root_machine_classification"] == "M4", "root M state drift")
    require(audit["known_failures"] and audit["first_failed_theorem_gate"]
            and audit["reopen_condition"], "audit lacks failure/reopen boundary")
    require(audit["audit_complete"] is False and audit["theorem_complete"] is False,
            "anchor phase overclaims terminal completion")

    require(statement_record["canonical_formal_target"]["declaration_or_expression"] is None,
            "statement record unexpectedly has a target")
    require(statement_record["status"] == "blocked_unfrozen",
            "statement blocker status drift")
    require(statement_receipt["schema_version"] == "stage1-node-receipt/1.0"
            and statement_receipt["item_id"] == "S56-M-0148-STATEMENT",
            "statement receipt identity drift")
    require(statement_receipt["accepted"] is False
            and statement_receipt["verdict"] == "blocked",
            "statement receipt acceptance boundary drift")

    validate_receipt_fields(receipt, contract)
    require(receipt["schema_version"] == "stage1-node-receipt/1.0",
            "wrong receipt schema")
    require(receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID,
            "receipt identity mismatch")
    require(receipt["phase"] == PHASE and receipt["intent"] == "audit",
            "receipt phase/intent mismatch")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE,
            "receipt base mismatch")
    require(receipt["proposed_state"] == "[_]" and receipt["accepted"] is False,
            "worker receipt claims acceptance")
    require(receipt["verdict"] == "no_state_change", "unexpected worker verdict")
    require(receipt["selftest_status"] == "passed"
            and receipt["selftest_result"]["exit_code"] == 0
            and receipt["selftest_result"]["commands"],
            "receipt self-test result incomplete")
    require(receipt["discovery_protocol_sha256"] == PROTOCOL_SHA256,
            "receipt protocol binding mismatch")
    result = receipt["candidate_inventory_result"]
    require(result["classified"] == result["inventory_size"] == 7
            and result["classification_complete"] is True
            and result["ordered_lanes_complete"] is True,
            "receipt phase predicate incomplete")
    require(result["discovery_saturation_claimed"] is False
            and result["canonical_target_frozen"] is False
            and result["exact_terminal_candidate_found"] is False
            and result["root_proof_credit"] is False,
            "receipt overclaims candidate or proof state")
    require(result["accepted_root_machine_state"] == "M4", "receipt root M state drift")
    require(receipt["known_failures"] and receipt["first_failed_gate"]
            and receipt["retry_condition"] and receipt["invalidation_inputs"],
            "receipt boundary/freshness data missing")
    require(receipt["audit_complete"] is False and receipt["theorem_complete"] is False,
            "receipt overclaims terminal completion")
    validate_role_bindings(receipt)

    validation_binding = receipt["inputs"]["discovery_evidence"][3]
    require(validation_binding["path"].endswith("anchor-audit-validation.md"),
            "validation record binding path drift")
    require(validation_binding["sha256"] == VALIDATION_SHA256,
            "validation record receipt SHA drift")
    require(validation_binding["git_blob"] == git_object(HERE / "anchor-audit-validation.md"),
            "validation record receipt Git object drift")

    validator_binding = receipt["validator_binding"]
    require(validator_binding["path"] == f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
            "validator path drift")
    require(validator_binding["sha256"] == sha256(Path(__file__)),
            "validator SHA binding drift")
    require(validator_binding["git_blob"] == git_object(Path(__file__)),
            "validator Git object binding drift")
    require(validator_binding["declared_argv"] == [
        "/usr/bin/python3", "-I", "-B",
        f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
    ], "validator argv drift")
    require(validator_binding["stdout_schema"] == "stage1-validator-semantic-result/1.0",
            "validator stdout schema drift")
    validate_worker_packet(receipt)

    require(output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION,
            "mathlib revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE,
            "mathlib tree drift")
    require(output("git", "status", "--short", cwd=MATHLIB) == "",
            "mathlib worktree is dirty")
    require(output("git", "show", f"{LEGACY_ORIGIN}:Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_028.lean")
            == (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_028.lean").read_text(encoding="utf-8").rstrip("\n"),
            "legacy source no longer equals its immutable origin")
    require(output("git", "show", "-s", "--format=%T", LEGACY_ORIGIN) == LEGACY_ORIGIN_TREE,
            "legacy origin tree drift")

    legacy_source = (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_028.lean").read_text(
        encoding="utf-8"
    )
    for marker in (
        "def ExplicitFieldStatementShape : Prop",
        "def StatementShape",
        "def mmpExternalAnchorAudit : List MMPExternalAnchorAudit",
        "theorem mmpExternalAnchorAudit_length : mmpExternalAnchorAudit.length = 10",
        "theorem mmpExternalAnchorAudit_no_lakeClosureFeasible",
        "2026-05-01 unauthenticated REST code search returned 401 Requires authentication.",
        "2026-05-01 direct curl to the query URL timed out after 30 seconds",
        "def mmpKnownTheoremBranchBlocker",
        "mmpKnownTheoremBranchBlocker.repoLocalClosed = false",
    ):
        require(marker in legacy_source, f"legacy evidence marker missing: {marker}")

    algebraic_geometry = MATHLIB / "Mathlib/AlgebraicGeometry"
    query = re.compile(
        r"Mori|\bMMP\b|minimal[ _-]?model|extremal[ _-]?ray|Mori[ _-]?(?:cone|fiber|fibre)|"
        r"birational[ _-]?classification|cone[ _-]?theorem|contraction[ _-]?theorem|"
        r"Kawamata|Shokurov|BCHM|log[ _-]?canonical|Q[ _-]?factorial",
        re.IGNORECASE,
    )
    material_hits = []
    for path in algebraic_geometry.rglob("*.lean"):
        if query.search(path.read_text(encoding="utf-8")):
            material_hits.append(str(path.relative_to(MATHLIB)))
    require(material_hits == [], f"pinned mathlib target-term search changed: {material_hits}")


def semantic_result(*, passed: bool, message: str) -> dict:
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "phase": PHASE,
        "status": "passed" if passed else "failed",
        "verdict": "phase_accepted" if passed else "repair_required",
        "phase_accepted": passed,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": passed,
        "first_failed_gate": None if passed else "ANCHOR-AUDIT-SEMANTIC-CHECK",
        "open_obligations": 0 if passed else 1,
        "stale_inputs": [],
        "blocked": False,
        "message": message,
    }


def main() -> int:
    try:
        validate()
    except Exception as exc:  # Exactly one typed JSON object is emitted on failure too.
        print(json.dumps(semantic_result(passed=False, message=str(exc)), sort_keys=True))
        return 1
    print(json.dumps(semantic_result(
        passed=True,
        message=(
            "A01-A03 proven for the content-bound seven-record inventory and all seven ordered "
            "lanes; the empty dependency context is audited and no exact target or proof credit "
            "is invented."
        ),
    ), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
