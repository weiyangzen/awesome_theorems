#!/usr/bin/env python3
"""Offline semantic validator for S56-M-0123-ANCHOR_AUDIT."""

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

ITEM_ID = "S56-M-0123-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0123"
PHASE = "anchor_audit"
BASE_REVISION = "307c34d30fc3763c82a944a142ae922b48ff18aa"
BASE_TREE = "ef45ba442c71959db78ad146a023bcf32946a53f"
GRAPH_SHA256 = "8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
PROTOCOL_SHA256 = "3956fd123be76286d5d8b35311eb98adea2320992b1c634c4a8460440d6c4fa8"
AUDIT_SHA256 = "75c729e9697c84b66a2f0c2c11d5c86000417c995f9bdce62fbb5faeef354938"
EVIDENCE_SHA256 = "bcb9d67d5f8f0a2d1c1e8a6e0805961c046bc3c464d67c25d067e81e1a633d5b"
LEDGER_SHA256 = "f8b4b17d7e93fa40ac7d19408f9b9da1f438958ed7dcf28bba350062477c58c5"
STATEMENT_SHA256 = "62c3d5936d64ed2225d239246ac8139663bc4f722f896625b94bb9a11e59ca8f"
PROBE_SHA256 = "f86d7581c09d1b4ab226287514146783612cb7b2fe4fdb1d3103650f96da2ea0"
EXPRESSION_SHA256 = "9fa3c7a0bff55098e7cc234793cb06ec1628e84e003ddb273a6dc47094f58dbd"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
ATLAS_REVISION = "34ffed396f376454c1a9b297f3fd74c5c801fb50"
ATLAS_SOURCE_SHA256 = "b5aca9ae03c178c908fdf0e28d4dd8672643b16390b25e9b9771882726ed8f01"

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
PROHIBITED_PROBE = re.compile(
    r"(^|[^A-Za-z_])(sorry|admit|sorryAx|axiom|constant|opaque|unsafe|"
    r"implemented_by|native_decide)([^A-Za-z_]|$)"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{name} is not a JSON object")
    return value


def load_path(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} is not a JSON object")
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


def verify_repo_artifact(artifact: dict) -> None:
    path = ROOT / artifact["path"]
    require(path.is_file() and not path.is_symlink(), f"evidence path missing: {path}")
    require(sha256(path) == artifact["sha256"], f"evidence SHA drift: {path}")
    require(output("git", "rev-parse", f"HEAD:{artifact['path']}") == artifact["git_blob"],
            f"evidence Git blob drift: {path}")


def verify_mathlib_artifact(artifact: dict) -> None:
    prefix = "Formalizations/Lean/.lake/packages/mathlib/"
    require(artifact["path"].startswith(prefix), "mathlib artifact path is outside package")
    relative = artifact["path"].removeprefix(prefix)
    path = MATHLIB / relative
    require(path.is_file() and not path.is_symlink(), f"mathlib evidence missing: {path}")
    require(sha256(path) == artifact["sha256"], f"mathlib SHA drift: {path}")
    require(output("git", "rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == artifact["git_blob"],
            f"mathlib Git blob drift: {path}")


def validate() -> None:
    audit = load("anchor-audit.json")
    protocol = load("discovery-protocol.json")
    evidence = load("discovery-evidence.json")
    ledger = load("dependency-reuse-ledger.json")
    receipt = load("anchor-audit-receipt.json")
    contract = load_path(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    theorem_dag = load_path(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    execution_dag = load_path(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load_path(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    statement = load("statement.json")
    statement_receipt = load("statement-receipt.json")

    require(output("git", "rev-parse", "HEAD") == BASE_REVISION, "repository revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE, "repository tree drift")
    require(sha256(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") == CONTRACT_SHA256,
            "phase contract drift")
    require(sha256(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") == GRAPH_SHA256,
            "theorem DAG drift")
    require(sha256(HERE / "Statement.lean") == STATEMENT_SHA256, "canonical statement drift")
    require(sha256(HERE / "AnchorAudit.lean") == PROBE_SHA256, "anchor probe drift")
    require(sha256(HERE / "discovery-protocol.json") == PROTOCOL_SHA256,
            "discovery protocol drift")
    require(sha256(HERE / "anchor-audit.json") == AUDIT_SHA256, "anchor inventory drift")
    require(sha256(HERE / "discovery-evidence.json") == EVIDENCE_SHA256,
            "discovery evidence drift")
    require(sha256(HERE / "dependency-reuse-ledger.json") == LEDGER_SHA256,
            "dependency ledger drift")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    require(target["execution_rank"] == 42, "target execution rank drift")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "target assurance baseline drift")
    task = next(row for row in execution_dag["items"] if row["id"] == ITEM_ID)
    require(task == {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 42,
        "phase": PHASE,
        "layer": 2,
        "state": "[ ]",
        "depends_on": ["S56-M-0123-STATEMENT"],
        "owned_paths": [f"Stage1_Instances/{THEOREM_ID}"],
        "deliverable": "Audit mathlib and external Lean 4 candidates at immutable revisions.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }, "authoritative task identity, state, dependency, or ownership drift")
    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    require(node["v2_execution_rank"] == 276 and node["topological_layer"] == 0,
            "v2 claim rank drift")
    require(node["phase_states"][PHASE] == "[ ]", "authoritative phase is no longer [ ]")
    require(node["phase_states"]["statement"] == "[_]", "statement observation drift")
    require(node["direct_hard_parents"] == [] and node["transitive_hard_ancestors"] == [],
            "hard-parent closure is no longer empty")
    require(node["direct_reuse_hint_ids"] == [] and node["shared_lemma_group_ids"] == [],
            "reuse context is no longer empty")
    require(node["dependency_context_sha256"] == CONTEXT_SHA256, "context digest drift")

    require(ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1",
            "wrong dependency ledger schema")
    require(ledger["consumer_theorem_id"] == THEOREM_ID, "wrong ledger consumer")
    require(ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256, "ledger graph mismatch")
    require(ledger["dependency_context_sha256"] == CONTEXT_SHA256, "ledger context mismatch")
    require(ledger["repository_revision"] == BASE_REVISION, "ledger revision mismatch")
    require(ledger["claim_order"] == {
        "v2_execution_rank": 276,
        "phase_layer": 2,
        "phase_item_id": ITEM_ID,
    }, "claim order mismatch")
    empty_fields = (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "parent_inspection_order", "inspections",
        "reuse_decisions", "unresolved_compatibility_obligations",
    )
    require(all(ledger[field] == [] for field in empty_fields),
            "declared empty dependency/reuse context drift")
    require(ledger["closure_audit"]["status"] == "complete_for_declared_context",
            "empty closure audit is incomplete")
    require(ledger["closure_audit"]["accepted_reuse"] == [],
            "empty context unexpectedly claims reuse")

    require(protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0",
            "wrong discovery protocol schema")
    require(protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID,
            "protocol identity mismatch")
    require(protocol["precommitted_before_replay"] is True, "protocol is not precommitted")
    require(protocol["saturation_claim"] is False, "protocol overclaims saturation")
    require([row["lane"] for row in protocol["ordered_search_lanes"]] == ORDERED_LANES,
            "protocol lane order mismatch")
    require(protocol["canonical_target"]["expression_sha256"] == EXPRESSION_SHA256,
            "protocol statement fingerprint mismatch")

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
            if artifact["path"].startswith("Formalizations/Lean/.lake/packages/mathlib/"):
                verify_mathlib_artifact(artifact)
            else:
                verify_repo_artifact(artifact)
    atlas_lane = next(row for row in lane_results
                      if row["lane"] == "other_immutable_public_projects")
    atlas_source = atlas_lane["external_source"]
    require(atlas_lane["revision"] == f"facebookresearch/atlas-lean@{ATLAS_REVISION}",
            "Atlas revision drift")
    require(atlas_source["sha256"] == ATLAS_SOURCE_SHA256, "Atlas source digest drift")
    require("by sorry" in atlas_source["terminal_body_excerpt"],
            "Atlas placeholder boundary drift")

    require(audit["schema_version"] == "stage1-anchor-audit/1.0", "wrong audit schema")
    require(audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID,
            "audit identity mismatch")
    require(audit["phase"] == PHASE and audit["intent"] == "audit",
            "audit phase or intent mismatch")
    require(audit["execution_rank"] == 42 and audit["v2_execution_rank"] == 276
            and audit["phase_layer"] == 2, "audit claim order mismatch")
    require(audit["canonical_target"]["source_sha256"] == STATEMENT_SHA256 and
            audit["canonical_target"]["expression_sha256"] == EXPRESSION_SHA256,
            "audit statement binding mismatch")
    require(audit["search_order_completed"] == ORDERED_LANES,
            "audit search order mismatch")
    require(audit["dependency_reuse_context"]["parent_inspection_order"] == [] and
            audit["dependency_reuse_context"]["accepted_reuse"] == [],
            "audit empty parent/reuse context drift")
    candidates = audit["candidates"]
    require(len(candidates) == 10, "candidate inventory size drift")
    require(len({candidate["candidate_id"] for candidate in candidates}) == len(candidates),
            "duplicate candidate identity")
    require({candidate["lane"] for candidate in candidates} == set(ORDERED_LANES),
            "candidate inventory does not cover every lane")
    require(all(normalize_classification(candidate["classification"]) in MACHINE_STATES
                for candidate in candidates), "candidate classification incomplete")
    for candidate in candidates:
        require(all(candidate.get(field) for field in (
            "exact_type", "normalized_match", "toolchain", "dependency_feasibility",
            "terminal_proof_body_provenance", "placeholder_axiom_unsafe_oracle_status",
            "blocker", "reopen_condition",
        )), f"candidate provenance/trust classification incomplete: {candidate['candidate_id']}")
        require(candidate["exact_root_closed"] is False and
                candidate["completion_credit"] is False,
                f"candidate improperly receives root credit: {candidate['candidate_id']}")
    require(all(normalize_classification(candidate["classification"])
                not in {"M0-L", "M0-W", "M0-P", "M1"}
                for candidate in candidates), "inventory improperly credits root closure")
    atlas = next(candidate for candidate in candidates
                 if candidate["candidate_id"] == "M0123-C07-ATLAS-FALTINGS-PLACEHOLDER")
    require(atlas["revision"] == ATLAS_REVISION and atlas["file_sha256"] == ATLAS_SOURCE_SHA256,
            "Atlas candidate binding drift")
    require(atlas["classification"] == "M5" and "by sorry" in
            atlas["terminal_proof_body_provenance"], "Atlas candidate is not rejected M5")
    coverage = audit["classification_coverage"]
    require(coverage["classified_candidates"] == coverage["inventory_size"] == 10,
            "candidate classification coverage incomplete")
    require(coverage["prescribed_lanes_completed"] ==
            coverage["prescribed_lane_count"] == 7, "prescribed lane coverage incomplete")
    require(coverage["complete_for_inventory_version"] is True,
            "inventory version is not completely classified")
    require(coverage["discovery_saturation_claimed"] is False,
            "audit overclaims discovery saturation")
    require(coverage["exact_terminal_candidate_found"] is False,
            "audit contradicts exact-candidate boundary")
    require(audit["root_decision"]["classification_before"] ==
            audit["root_decision"]["classification_after_proposed"] == "M3",
            "root machine classification drift")
    require(audit["root_decision"]["kernel_closed"] is False and
            audit["root_decision"]["repo_local_integration_debt"] is False,
            "root decision overclaims closure or integration debt")
    require(audit["root_vector_before"] == audit["root_vector_after_proposed"] == {
        "human": "H4", "machine": "M3", "readability": "R3",
    }, "root vector changed without evidence")
    require(audit["inventory_complete"] is True and audit["theorem_proved"] is False and
            audit["audit_complete"] is False and audit["theorem_complete"] is False and
            audit["accepted_receipt_ids"] == [], "audit overclaims terminal state")

    formal = statement["canonical_formal_target"]
    require(formal["declaration_or_expression"] ==
            "Stage1Instances.THM_M_0123.MordellTarget", "canonical declaration drift")
    require(formal["elaborated_expression_sha256"] == EXPRESSION_SHA256,
            "canonical expression drift")
    require(formal["statement_file_sha256"] == STATEMENT_SHA256,
            "statement record source drift")
    require(statement_receipt["statement_fingerprints"] == [f"sha256:{EXPRESSION_SHA256}"],
            "statement receipt fingerprint drift")

    phase_contract = next(row for row in contract["phases"] if row["phase"] == PHASE)
    for pointer in phase_contract["phase_receipt_required_fields"]:
        current: object = receipt
        for component in pointer.strip("/").split("/"):
            require(isinstance(current, dict) and component in current,
                    f"receipt missing required field {pointer}")
            current = current[component]
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
    require(receipt["verdict"] == "no_state_change", "unexpected worker verdict")
    require(receipt["selftest_status"] == "passed", "receipt self-test did not pass")
    require(receipt["selftest_result"]["exit_code"] == 0 and
            receipt["selftest_result"]["commands"], "receipt self-test result incomplete")
    require(receipt["discovery_protocol_sha256"] == PROTOCOL_SHA256,
            "receipt protocol binding mismatch")
    inventory_result = receipt["candidate_inventory_result"]
    require(inventory_result["classification_complete"] is True and
            inventory_result["ordered_lanes_complete"] is True,
            "receipt phase predicate incomplete")
    require(inventory_result["root_proof_credit"] is False,
            "receipt improperly claims proof credit")
    require(receipt["audit_complete"] is False and receipt["theorem_complete"] is False,
            "receipt overclaims terminal completion")
    require(receipt["known_failures"] and receipt["first_failed_gate"] and
            receipt["retry_condition"] and receipt["invalidation_inputs"],
            "receipt boundary or freshness data missing")

    probe = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    require(PROHIBITED_PROBE.search(probe) is None,
            "prohibited Lean construct in target-owned anchor probe")
    checked = set(re.findall(r"^#check (.+)$", probe, re.MULTILINE))
    expected_checks = {
        "NumberField", "Scheme", "SmoothOfRelativeDimension", "IsProper", "geometrically",
        "CategoryTheory.Sheaf.H", "Northcott.finite_le", "AddCommGroup.fg_of_descent'",
    }
    require(expected_checks <= checked, f"missing Lean probes: {sorted(expected_checks - checked)}")
    require("#print axioms checked_northcott_sublevel" in probe,
            "missing support axiom probe")

    require(output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION,
            "mathlib revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE,
            "mathlib tree drift")
    require(output("git", "status", "--short", "--untracked-files=no", cwd=MATHLIB) == "",
            "mathlib tracked worktree is dirty")
    docs = (MATHLIB / "docs/1000.yaml").read_text(encoding="utf-8")
    row = docs[docs.index("Q240950:"):docs.index("Q241868:")]
    require("title: Faltings's theorem" in row and "decl:" not in row and "decls:" not in row,
            "Faltings documentation row gained a declaration")
    package_search = subprocess.run(
        ["rg", "-n", "-i",
         "Faltings|MordellConjecture|Mordell conjecture|FaltingsTheorem|faltings_theorem",
         str(LEAN_ROOT / ".lake" / "packages"), "-g", "*.lean", "-g", "*.md",
         "-g", "*.yaml", "-g", "*.json"],
        text=True, capture_output=True,
    )
    require(package_search.returncode == 0, "pinned package search failed")
    matches = [line for line in package_search.stdout.splitlines() if line.strip()]
    require(any("mathlib/docs/1000.yaml:249:" in line and "Faltings's theorem" in line
                for line in matches), "pinned package search lost the Faltings docs row")
    require(all(("mathlib/docs/1000.yaml" in line or
                 "mathlib/Mathlib/GroupTheory/Descent.lean" in line)
                for line in matches), "pinned package closure gained an unclassified source match")


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
    except Exception as exc:  # Emit exactly one typed JSON result, including failures.
        print(json.dumps(semantic_result(passed=False, message=str(exc)), sort_keys=True))
        return 1
    print(json.dumps(semantic_result(
        passed=True,
        message=(
            "A01-A03 proven for the content-bound ten-candidate inventory and all seven ordered "
            "lanes; the empty hard-parent/reuse closure is audited without acceptance transfer."
        ),
    ), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
