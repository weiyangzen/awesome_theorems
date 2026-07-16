#!/usr/bin/env python3
"""Offline semantic validator for S56-M-0412-ANCHOR_AUDIT."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"

ITEM_ID = "S56-M-0412-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0412"
PHASE = "anchor_audit"
BASE_REVISION = "307c34d30fc3763c82a944a142ae922b48ff18aa"
BASE_TREE = "ef45ba442c71959db78ad146a023bcf32946a53f"
GRAPH_SHA256 = "8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
PROTOCOL_SHA256 = "94ec324d608a2b477b37667a4e5251ca8d8a81dfed6048e381e15e657843f429"
EVIDENCE_SHA256 = "37870224f20aa917a30f6e9312635a4b0ef1bb6898df3963d2b329502fb65f12"
AUDIT_SHA256 = "bac3854ea0523b4b7b977e71a2f81924d69a72e353b0cc8fd6f7f9b2e85f919f"
LEDGER_SHA256 = "8f7891dcf05086049e9bd6ba2b423b3a1f4b69f9b24c8bf1061a667498c1f4eb"
STATEMENT_SHA256 = "1c4ca90f92ad2d74e7e6abe4124b57e623a8218312ed88f38626ae0b096edd65"
ANCHOR_PROBE_SHA256 = "1b499ebc61f5deb9b9ab4cfc869192061333599540b8a9b777d7377dc6042908"
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    require(isinstance(value, dict), f"{path} is not a JSON object")
    return value


def output(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, result.stderr or f"command failed: {args}")
    return result.stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def pointer(document: dict, raw: str) -> object:
    value: object = document
    for component in raw.removeprefix("/").split("/"):
        require(isinstance(value, dict) and component in value, f"missing pointer {raw}")
        value = value[component]
    return value


def normalize_classification(value: str) -> str:
    for state in sorted(MACHINE_STATES, key=len, reverse=True):
        if value == state or value.startswith(state + "_") or value.startswith(state + " "):
            return state
    raise AssertionError(f"unsupported machine classification {value!r}")


def tracked_blob(path: str, *, package: bool = False) -> str:
    if package:
        return output("git", "rev-parse", f"HEAD:{path}", cwd=MATHLIB)
    return output("git", "rev-parse", f"HEAD:{path}")


def validate() -> None:
    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "discovery-protocol.json")
    evidence = load(HERE / "discovery-evidence.json")
    ledger = load(HERE / "dependency-reuse-ledger.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    contract_path = ROOT / "Docs" / "Stage1_Phase_Acceptance_Contracts.json"
    graph_path = ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json"
    targets_path = ROOT / "Docs" / "Stage1_Targets_rev-5.6.json"
    contract = load(contract_path)
    theorem_dag = load(graph_path)
    targets = load(targets_path)

    require(output("git", "rev-parse", "HEAD") == BASE_REVISION, "repository revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE, "repository tree drift")
    require(sha256(contract_path) == CONTRACT_SHA256, "phase contract drift")
    require(sha256(graph_path) == GRAPH_SHA256, "theorem DAG drift")
    require(sha256(HERE / "Statement.lean") == STATEMENT_SHA256, "statement boundary drift")
    require(sha256(HERE / "AnchorAudit.lean") == ANCHOR_PROBE_SHA256,
            "anchor probe source drift")
    require(sha256(HERE / "discovery-protocol.json") == PROTOCOL_SHA256,
            "discovery protocol drift")
    require(sha256(HERE / "discovery-evidence.json") == EVIDENCE_SHA256,
            "discovery evidence drift")
    require(sha256(HERE / "anchor-audit.json") == AUDIT_SHA256, "anchor inventory drift")
    require(sha256(HERE / "dependency-reuse-ledger.json") == LEDGER_SHA256,
            "dependency ledger drift")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    require(target["execution_rank"] == 21, "target execution rank drift")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "target assurance baseline drift")
    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    require(node["v2_execution_rank"] == 259, "v2 execution rank drift")
    require(node["phase_states"][PHASE] == "[ ]", "authoritative phase state drift")
    require(node["phase_attempts"][PHASE] == 0, "authoritative phase attempts drift")
    require(node["direct_hard_parents"] == node["transitive_hard_ancestors"] == [],
            "hard-parent closure is no longer empty")
    require(node["direct_reuse_hint_ids"] == node["shared_lemma_group_ids"] == [],
            "nonhard reuse context is no longer empty")
    require(node["dependency_context_sha256"] == CONTEXT_SHA256, "context digest drift")

    require(ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1",
            "wrong dependency ledger schema")
    require(ledger["consumer_theorem_id"] == THEOREM_ID, "ledger theorem mismatch")
    require(ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256, "ledger graph mismatch")
    require(ledger["dependency_context_sha256"] == CONTEXT_SHA256, "ledger context mismatch")
    require(ledger["repository_revision"] == BASE_REVISION, "ledger revision mismatch")
    require(ledger["claim_order"] == {
        "v2_execution_rank": 259,
        "phase_layer": 2,
        "phase_item_id": ITEM_ID,
    }, "claim order mismatch")
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
        require(ledger[field] == [], f"declared empty dependency context drift at {field}")
    require(ledger["closure_audit"]["status"] == "complete_for_declared_context",
            "empty closure was not audited")
    require(ledger["closure_audit"]["accepted_reuse"] == [],
            "empty closure improperly consumes reuse")

    require(protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0",
            "wrong discovery protocol schema")
    require(protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID,
            "protocol identity mismatch")
    require(protocol["precommitted_before_replay"] is True, "protocol is not precommitted")
    require(protocol["saturation_claim"] is False, "protocol overclaims saturation")
    require(protocol["canonical_target"]["status"] == "unresolved_source_identity",
            "protocol invents a canonical target")
    require(protocol["canonical_target"]["declaration"] is None
            and protocol["canonical_target"]["normalized_claim"] is None,
            "protocol invents a declaration or normalized claim")
    require([row["lane"] for row in protocol["ordered_search_lanes"]] == ORDERED_LANES,
            "protocol lane order mismatch")
    require(protocol["network_policy"].startswith("denied for replay"),
            "protocol weakens the replay network boundary")

    require(evidence["schema_version"] == "stage1-anchor-discovery-evidence/1.0",
            "wrong discovery evidence schema")
    require(evidence["item_id"] == ITEM_ID and evidence["theorem_id"] == THEOREM_ID,
            "evidence identity mismatch")
    require(evidence["network_used_for_replay"] is False, "offline replay used network")
    lane_results = evidence["ordered_lane_results"]
    require([row["lane"] for row in lane_results] == ORDERED_LANES,
            "evidence lane order mismatch")
    for row in lane_results:
        require(all(row.get(field) for field in (
            "query_or_source", "revision", "result", "access_boundary", "reopen_condition"
        )), f"incomplete lane result: {row['lane']}")
        require(isinstance(row.get("evidence"), list) and row["evidence"],
                f"unbound lane result: {row['lane']}")
        for artifact in row["evidence"]:
            path = ROOT / artifact["path"]
            require(path.is_file() and not path.is_symlink(), f"missing evidence: {path}")
            require(sha256(path) == artifact["sha256"], f"evidence SHA drift: {path}")
            if artifact["path"].startswith("Formalizations/Lean/.lake/packages/mathlib/"):
                relative = artifact["path"].removeprefix(
                    "Formalizations/Lean/.lake/packages/mathlib/"
                )
                actual_blob = tracked_blob(relative, package=True)
            else:
                actual_blob = tracked_blob(artifact["path"])
            require(actual_blob == artifact["git_blob"], f"evidence Git blob drift: {path}")

    require(audit["schema_version"] == "stage1-anchor-audit/1.0", "wrong audit schema")
    require(audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID,
            "audit identity mismatch")
    require(audit["phase"] == PHASE and audit["intent"] == "audit",
            "audit phase or intent mismatch")
    require(audit["execution_rank"] == 21 and audit["v2_execution_rank"] == 259
            and audit["phase_layer"] == 2, "audit claim order mismatch")
    require(audit["canonical_target"]["status"] == "unresolved_source_identity",
            "audit invents a canonical target")
    require(audit["canonical_target"]["declaration"] is None
            and audit["canonical_target"]["statement_fingerprints"] == [],
            "audit invents declaration identity")
    require(audit["discovery_protocol"]["sha256"] == PROTOCOL_SHA256,
            "audit protocol binding mismatch")
    require(audit["discovery_evidence"]["sha256"] == EVIDENCE_SHA256,
            "audit evidence binding mismatch")
    require(audit["dependency_reuse_context"]["sha256"] == LEDGER_SHA256,
            "audit ledger binding mismatch")
    require(audit["search_order_completed"] == ORDERED_LANES, "audit search order mismatch")
    require(audit["anchor_probe_source"]["sha256"] == ANCHOR_PROBE_SHA256,
            "audit anchor probe binding mismatch")
    require(len(audit["anchor_probe_source"]["checked_declarations"]) == 6,
            "anchor probe declaration inventory drift")
    candidates = audit["candidates"]
    require(len(candidates) == 6, "candidate inventory size drift")
    require(len({candidate["id"] for candidate in candidates}) == len(candidates),
            "duplicate candidate identity")
    require(all(normalize_classification(candidate["classification"]) in MACHINE_STATES
                for candidate in candidates), "candidate classification incomplete")
    required_candidate_fields = (
        "project",
        "revision",
        "exact_type",
        "normalized_match",
        "toolchain",
        "dependency_feasibility",
        "transitive_dependency_boundary",
        "proof_body",
        "proof_body_provenance",
        "placeholder_axiom_unsafe_oracle_status",
        "license",
        "blocker",
        "reopen_event",
    )
    for candidate in candidates:
        require(isinstance(candidate.get("declarations"), list),
                f"candidate declarations are malformed: {candidate['id']}")
        require(isinstance(candidate.get("direct_dependencies"), list),
                f"candidate dependencies are malformed: {candidate['id']}")
        for field in required_candidate_fields:
            require(field in candidate and candidate[field] not in ("", []),
                    f"candidate lacks {field}: {candidate['id']}")
        require(candidate["completion_credit"] is False,
                f"candidate improperly receives proof credit: {candidate['id']}")
    legacy = next(row for row in candidates if row["id"] == "repo-legacy-abstract-statement-shape")
    require(legacy["classification"] == "M3" and legacy["terminal_declaration"] is None,
            "legacy abstract wrapper is overcredited")
    support = next(row for row in candidates if row["id"] == "mathlib-weierstrass-support")
    require(support["classification"] == "M2" and support["terminal_declaration"] is None,
            "mathlib support is overcredited")
    historical = next(
        row for row in candidates if row["id"] == "historical-nagell-lutz-identity-hypothesis"
    )
    require(historical["classification"] == "M5", "identity substitution is not M5")
    coverage = audit["classification_coverage"]
    require(coverage["classified_candidates"] == coverage["inventory_size"] == 6,
            "candidate classification coverage incomplete")
    require(coverage["prescribed_lanes_completed"] == coverage["prescribed_lane_count"] == 7,
            "prescribed lane coverage incomplete")
    require(coverage["complete_for_inventory_version"] is True,
            "inventory is not completely classified")
    require(coverage["discovery_saturation_claimed"] is False,
            "audit overclaims discovery saturation")
    require(coverage["exact_terminal_candidate_found"] is False
            and coverage["canonical_target_resolved"] is False,
            "audit contradicts the negative target boundary")
    require(audit["root_machine_classification"] == "M4", "root M state drift")
    require(audit["human_source_classification"] == "H5"
            and audit["readability_classification"] == "R4", "root H/R state drift")
    require(audit["audit_complete"] is False and audit["theorem_complete"] is False,
            "anchor phase overclaims terminal completion")

    phase_contract = next(row for row in contract["phases"] if row["phase"] == PHASE)
    for raw in phase_contract["phase_receipt_required_fields"]:
        pointer(receipt, raw)
    require(receipt["schema_version"] == "stage1-node-receipt/1.0",
            "wrong receipt schema")
    require(receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID,
            "receipt identity mismatch")
    require(receipt["phase"] == PHASE and receipt["intent"] == "audit",
            "receipt phase or intent mismatch")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE,
            "receipt base mismatch")
    require(receipt["proposed_state"] == "[_]" and receipt["accepted"] is False,
            "worker receipt claims master acceptance")
    require(receipt["verdict"] == "accepted", "unexpected worker verdict")
    require(receipt["selftest_status"] == "passed", "receipt lacks passed self-test")
    require(receipt["selftest_result"]["exit_code"] == 0
            and receipt["selftest_result"]["commands"], "receipt self-test is incomplete")
    require(receipt["discovery_protocol_sha256"] == PROTOCOL_SHA256,
            "receipt protocol binding mismatch")
    inventory_result = receipt["candidate_inventory_result"]
    require(inventory_result["classification_complete"] is True
            and inventory_result["ordered_lanes_complete"] is True,
            "receipt phase predicate is incomplete")
    require(inventory_result["canonical_target_resolved"] is False
            and inventory_result["root_proof_credit"] is False,
            "receipt overcredits the unresolved target")
    require(receipt["audit_complete"] is False and receipt["theorem_complete"] is False,
            "receipt overclaims terminal completion")
    require(receipt["known_failures"] and receipt["first_failed_gate"]
            and receipt["retry_condition"] and receipt["invalidation_inputs"],
            "receipt boundary or freshness data missing")

    require(output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION,
            "mathlib revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE,
            "mathlib tree drift")
    require(output("git", "status", "--short", "--untracked-files=all", cwd=MATHLIB) == "",
            "mathlib worktree is dirty")
    docs = (MATHLIB / "docs" / "1000.yaml").read_text(encoding="utf-8")
    require("Q3527132:\n  title: Nagell–Lutz theorem\n\n" in docs,
            "mathlib Nagell-Lutz docs row changed or gained a declaration")


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
    except Exception as exc:
        print(json.dumps(semantic_result(passed=False, message=str(exc)), sort_keys=True))
        return 1
    print(json.dumps(semantic_result(
        passed=True,
        message=(
            "A01-A03 proven for the content-bound six-candidate inventory and all seven ordered "
            "lanes; the empty dependency closure is audited with no reuse or acceptance transfer."
        ),
    ), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
