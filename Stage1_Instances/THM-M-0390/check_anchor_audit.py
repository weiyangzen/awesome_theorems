#!/usr/bin/env python3
"""Offline semantic validator for S56-M-0390-ANCHOR_AUDIT."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
FLT_REGULAR = LEAN_ROOT / ".lake" / "packages" / "flt-regular"

ITEM_ID = "S56-M-0390-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0390"
PHASE = "anchor_audit"
BASE_REVISION = "c5037228977a81948bbd6119e1728b4b65b9924e"
BASE_TREE = "78b2627e717156dffe240bea12d14205af667d2a"
GRAPH_SHA256 = "fb17743ff737fd3c528467b6f992a7235a36f0842b528e57de3e4c6d660d3518"
CONTEXT_SHA256 = "a615cea5c684a96055d1d5bb30bdcfccbc499a62f7fcfac3490551cb836c1598"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
PROTOCOL_SHA256 = "23d9ebc8a74f9852fee448b53961722461e08f4d574ff053ff5f3a4aa782e013"
AUDIT_SHA256 = "9e3f908f9f4a44ec5c64b36815fe6248a7b897f2bcf635cbe3fdaecb05bf9a96"
EVIDENCE_SHA256 = "bd6573899e9001f029cbb8b9799f5a5fde886599aabf8b8d7e582a898e369a84"
LEDGER_SHA256 = "b49908cf145002558185fc4b8ccb26cbb763c0db4ffb32d0c7e945d67fbb8960"
STATEMENT_SHA256 = "b54a002f18aba974c2a675bcfe17551d80eb482a9fdf745c0d4b3c85afaf33f3"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
FLT_REGULAR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"

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


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{name} is not a JSON object")
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


def validate() -> None:
    audit = load("anchor-audit.json")
    protocol = load("discovery-protocol.json")
    evidence = load("discovery-evidence.json")
    ledger = load("dependency-reuse-ledger.json")
    receipt = load("anchor-audit-receipt.json")
    contract = json.loads((ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json").read_text())
    theorem_dag = json.loads((ROOT / "Docs/Stage1_Theorem_DAG_v2.json").read_text())
    targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())

    require(output("git", "rev-parse", "HEAD") == BASE_REVISION, "repository revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE, "repository tree drift")
    require(sha256(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") == CONTRACT_SHA256,
            "phase contract drift")
    require(sha256(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") == GRAPH_SHA256,
            "theorem DAG drift")
    require(sha256(HERE / "Statement.lean") == STATEMENT_SHA256, "canonical statement drift")
    require(sha256(HERE / "discovery-protocol.json") == PROTOCOL_SHA256,
            "discovery protocol drift")
    require(sha256(HERE / "anchor-audit.json") == AUDIT_SHA256, "anchor inventory drift")
    require(sha256(HERE / "discovery-evidence.json") == EVIDENCE_SHA256,
            "discovery evidence drift")
    require(sha256(HERE / "dependency-reuse-ledger.json") == LEDGER_SHA256,
            "dependency ledger drift")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    require(target["execution_rank"] == 4, "target execution rank drift")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "target assurance baseline drift")
    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    require(node["v2_execution_rank"] == 4, "v2 execution rank drift")
    require(node["phase_states"][PHASE] == "[_]", "authoritative phase is not [_]")
    require(node["direct_hard_parents"] == [] and node["transitive_hard_ancestors"] == [],
            "hard-parent closure is no longer empty")
    require(node["direct_reuse_hint_ids"] == [], "reuse-hint closure drift")
    require(node["shared_lemma_group_ids"] == ["SHARED-MODULE-32f9c9eb1b52d871"],
            "shared-group closure drift")
    require(node["dependency_context_sha256"] == CONTEXT_SHA256, "context digest drift")

    require(ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1",
            "wrong dependency ledger schema")
    require(ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256, "ledger graph mismatch")
    require(ledger["dependency_context_sha256"] == CONTEXT_SHA256, "ledger context mismatch")
    require(ledger["repository_revision"] == BASE_REVISION, "ledger revision mismatch")
    require(ledger["claim_order"] == {
        "v2_execution_rank": 4,
        "phase_layer": 2,
        "phase_item_id": ITEM_ID,
    }, "claim order mismatch")
    for field in ("direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
                  "reuse_hint_ids", "parent_inspection_order", "inspections"):
        require(ledger[field] == [], f"declared empty closure drift at {field}")
    require(ledger["shared_group_ids"] == ["SHARED-MODULE-32f9c9eb1b52d871"],
            "ledger shared-group mismatch")
    require(len(ledger["reuse_decisions"]) == 1, "shared group is not classified exactly once")
    decision = ledger["reuse_decisions"][0]
    require(decision["source_id"] == "SHARED-MODULE-32f9c9eb1b52d871",
            "wrong shared-group decision")
    require(decision["provider_theorem_id"] == "THM-M-0133", "wrong inspected group member")
    require(decision["decision"] == "not_applicable", "weak group incorrectly reused")
    require(decision["context_digest"] == CONTEXT_SHA256, "decision context mismatch")
    require(ledger["unresolved_compatibility_obligations"] == [],
            "unresolved compatibility obligation remains")
    for artifact in decision["inspected_provider_artifacts"]:
        path = ROOT / artifact["path"]
        require(path.is_file() and not path.is_symlink(), f"provider artifact missing: {path}")
        require(sha256(path) == artifact["sha256"], f"provider SHA drift: {path}")
        require(output("git", "rev-parse", f"HEAD:{artifact['path']}") == artifact["git_blob"],
                f"provider Git blob drift: {path}")

    require(protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0",
            "wrong discovery protocol schema")
    require(protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID,
            "protocol identity mismatch")
    require(protocol["precommitted_before_replay"] is True, "protocol is not precommitted")
    require(protocol["saturation_claim"] is False, "protocol overclaims saturation")
    require([row["lane"] for row in protocol["ordered_search_lanes"]] == ORDERED_LANES,
            "protocol lane order mismatch")

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
            require(path.is_file() and not path.is_symlink(), f"evidence path missing: {path}")
            require(sha256(path) == artifact["sha256"], f"evidence SHA drift: {path}")
            if str(artifact["path"]).startswith("Formalizations/Lean/.lake/packages/mathlib/"):
                package_path = str(artifact["path"]).removeprefix(
                    "Formalizations/Lean/.lake/packages/mathlib/"
                )
                actual_blob = output("git", "rev-parse", f"HEAD:{package_path}", cwd=MATHLIB)
            else:
                actual_blob = output("git", "rev-parse", f"HEAD:{artifact['path']}")
            require(actual_blob == artifact["git_blob"], f"evidence Git blob drift: {path}")

    require(audit["schema_version"] == "stage1-anchor-audit/1.0", "wrong audit schema")
    require(audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID,
            "audit identity mismatch")
    require(audit["phase"] == PHASE and audit["execution_rank"] == 4
            and audit["phase_layer"] == 2, "audit claim order mismatch")
    require(audit["canonical_statement_file_sha256"] == STATEMENT_SHA256,
            "audit statement binding mismatch")
    require(audit["discovery_protocol"]["sha256"] == PROTOCOL_SHA256,
            "audit protocol binding mismatch")
    require(audit["search_order_completed"] == ORDERED_LANES, "audit search order mismatch")
    candidates = audit["candidates"]
    require(len(candidates) == 6, "candidate inventory size drift")
    require(len({candidate["id"] for candidate in candidates}) == len(candidates),
            "duplicate candidate identity")
    require(all(normalize_classification(candidate["classification"]) in MACHINE_STATES
                for candidate in candidates), "candidate classification incomplete")
    for candidate in candidates:
        require(all(candidate.get(field) for field in (
            "exact_type", "normalized_match", "toolchain", "dependency_feasibility",
            "proof_body", "placeholder_axiom_unsafe_oracle_status"
        )), f"candidate provenance/trust classification incomplete: {candidate['id']}")
        if normalize_classification(candidate["classification"]) in {"M4", "M5"}:
            require(candidate.get("blocker") and candidate.get("reopen_event"),
                    f"negative candidate lacks blocker/reopen event: {candidate['id']}")
    require(all(candidate["completion_credit"] is False for candidate in candidates),
            "candidate improperly receives proof credit")
    formal_conjectures = next(candidate for candidate in candidates
                              if candidate["id"] == "formal-conjectures-catalan")
    require(formal_conjectures["classification"] == "M5",
            "placeholder candidate is not M5")
    require(formal_conjectures["source_sha256"] ==
            "4d6a944a1cec1df6928207be2cdf44ad0b1e7bdc89263f9812fc93037f6b152c",
            "external source binding drift")
    coverage = audit["classification_coverage"]
    require(coverage["classified_candidates"] == coverage["inventory_size"] == 6,
            "candidate classification coverage incomplete")
    require(coverage["prescribed_lanes_completed"] == coverage["prescribed_lane_count"] == 7,
            "prescribed lane coverage incomplete")
    require(coverage["complete_for_inventory_version"] is True,
            "inventory version is not completely classified")
    require(coverage["discovery_saturation_claimed"] is False,
            "audit overclaims discovery saturation")
    require(coverage["exact_terminal_candidate_found"] is False,
            "audit contradicts exact-candidate boundary")
    require(audit["root_machine_classification"] == "M3", "root M state drift")
    require(audit["audit_complete"] is False and audit["theorem_complete"] is False,
            "anchor phase overclaims terminal completion")

    phase_contract = next(row for row in contract["phases"] if row["phase"] == PHASE)
    required_fields = [pointer.removeprefix("/") for pointer in
                       phase_contract["phase_receipt_required_fields"]]
    for field in required_fields:
        if "/" not in field:
            require(field in receipt, f"receipt missing required field {field}")
    require(receipt["schema_version"] == "stage1-node-receipt/1.0",
            "wrong receipt schema")
    require(receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID,
            "receipt identity mismatch")
    require(receipt["phase"] == PHASE and receipt["intent"] == "audit",
            "receipt phase or intent mismatch")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE,
            "receipt base mismatch")
    require(receipt["proposed_state"] == "[_]" and receipt["accepted"] is False,
            "worker receipt claims acceptance")
    require(receipt["verdict"] == "no_state_change", "unexpected worker verdict")
    require(receipt["selftest_status"] == "passed",
            "receipt does not record a passed self-test")
    require(receipt["selftest_result"]["exit_code"] == 0
            and receipt["selftest_result"]["commands"], "receipt self-test result incomplete")
    require(receipt["discovery_protocol_sha256"] == PROTOCOL_SHA256,
            "receipt protocol binding mismatch")
    inventory_result = receipt["candidate_inventory_result"]
    require(inventory_result["classification_complete"] is True
            and inventory_result["ordered_lanes_complete"] is True,
            "receipt phase predicate incomplete")
    require(inventory_result["root_proof_credit"] is False,
            "receipt improperly claims proof credit")
    require(receipt["audit_complete"] is False and receipt["theorem_complete"] is False,
            "receipt overclaims terminal completion")
    require(receipt["known_failures"] and receipt["first_failed_gate"]
            and receipt["retry_condition"] and receipt["invalidation_inputs"],
            "receipt boundary or freshness data missing")

    require(output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION,
            "mathlib revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE,
            "mathlib tree drift")
    require(output("git", "status", "--short", cwd=MATHLIB) == "",
            "mathlib worktree is dirty")
    require(output("git", "rev-parse", "HEAD", cwd=FLT_REGULAR) == FLT_REGULAR_REVISION,
            "flt-regular revision drift")
    require(output("git", "status", "--short", cwd=FLT_REGULAR) == "",
            "flt-regular worktree is dirty")
    mathlib_docs = (MATHLIB / "docs/1000.yaml").read_text(encoding="utf-8")
    require("Q174955:\n  title: Mihăilescu's theorem\n\n" in mathlib_docs,
            "mathlib docs row gained a declaration or changed")
    polynomial = (MATHLIB / "Mathlib/NumberTheory/FLT/Polynomial.lean").read_text(
        encoding="utf-8"
    )
    require("theorem Polynomial.flt_catalan" in polynomial
            and "a.natDegree = 0 ∧ b.natDegree = 0 ∧ c.natDegree = 0" in polynomial,
            "polynomial candidate source drift")


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
            "A01-A03 proven for the content-bound six-candidate inventory and all seven ordered "
            "lanes; the empty hard-parent closure and weak shared group are audited without reuse."
        ),
    ), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
