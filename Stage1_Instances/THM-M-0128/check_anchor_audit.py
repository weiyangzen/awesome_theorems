#!/usr/bin/env python3
"""Offline semantic validator for S56-M-0128-ANCHOR_AUDIT."""

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

ITEM_ID = "S56-M-0128-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0128"
PHASE = "anchor_audit"
BASE_REVISION = "74d4c272070069bc62df15798895293b4795940a"
BASE_TREE = "6693e584a3d529077306168fe38abd693d210ef0"
GRAPH_SHA256 = "cb4b83c4c4a5474fce51f98098f1421315fe7f1bd8cd52205932e57eced9f675"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
PROTOCOL_SHA256 = "6751522d8738c42a62b3fbd00897d5bede9c31ef326b1740fee1d0164418f088"
EVIDENCE_SHA256 = "fa79564716fa732a0a305d68e39548d2315c57fd59b77240fd97117688e60f94"
AUDIT_SHA256 = "f6f69a13beeac092647c46629df749294219694e2bdffbc61e57f54fb0f19802"
LEDGER_SHA256 = "48e1c1a5ab7a6c4153e549de3c5962565952a9b2b36e0fa130f2cc4a1b25f23b"
ANCHOR_LEAN_SHA256 = "bc6f35625575ec4187c3e2155865e2d342bfb65cc431d732b73ba5ea654deef7"
STATEMENT_SHA256 = "6fe3fb36ed8ed662a05599e39fdc8f8d41bfb7c1732de6b0051ab4eeb18623e4"
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
REQUIRED_RESULT_FIELDS = {
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    require(isinstance(value, dict), f"{path} must contain one JSON object")
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


def validate_binding(binding: dict, *, allow_external_mathlib: bool = False) -> None:
    relative = binding.get("path")
    require(isinstance(relative, str) and relative, "evidence binding lacks a path")
    path = ROOT / relative
    require(path.is_file() and not path.is_symlink(), f"evidence path missing or unsafe: {relative}")
    require(sha256(path) == binding.get("sha256"), f"evidence SHA drift: {relative}")
    if allow_external_mathlib and relative.startswith("Formalizations/Lean/.lake/packages/mathlib/"):
        package_path = relative.removeprefix("Formalizations/Lean/.lake/packages/mathlib/")
        actual_blob = output("git", "rev-parse", f"HEAD:{package_path}", cwd=MATHLIB)
    elif relative.startswith("Stage1_Instances/THM-M-0128/") and relative in {
        "Stage1_Instances/THM-M-0128/anchor-audit.json",
        "Stage1_Instances/THM-M-0128/discovery-evidence.json",
        "Stage1_Instances/THM-M-0128/discovery-protocol.json",
        "Stage1_Instances/THM-M-0128/AnchorAudit.lean",
        "Stage1_Instances/THM-M-0128/dependency-reuse-ledger.json",
    }:
        actual_blob = git_blob(path)
    else:
        actual_blob = output("git", "rev-parse", f"HEAD:{relative}")
    require(actual_blob == binding.get("git_blob"), f"evidence Git blob drift: {relative}")


def validate() -> None:
    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "discovery-protocol.json")
    evidence = load(HERE / "discovery-evidence.json")
    ledger = load(HERE / "dependency-reuse-ledger.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    theorem_dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    require(output("git", "rev-parse", "HEAD") == BASE_REVISION, "repository revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE, "repository tree drift")
    require(sha256(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") == CONTRACT_SHA256,
            "phase contract drift")
    require(sha256(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") == GRAPH_SHA256,
            "theorem DAG drift")
    require(sha256(HERE / "Statement.lean") == STATEMENT_SHA256, "statement source drift")
    require(sha256(HERE / "discovery-protocol.json") == PROTOCOL_SHA256,
            "discovery protocol drift")
    require(sha256(HERE / "discovery-evidence.json") == EVIDENCE_SHA256,
            "discovery evidence drift")
    require(sha256(HERE / "anchor-audit.json") == AUDIT_SHA256,
            "anchor inventory drift")
    require(sha256(HERE / "dependency-reuse-ledger.json") == LEDGER_SHA256,
            "dependency ledger drift")
    require(sha256(HERE / "AnchorAudit.lean") == ANCHOR_LEAN_SHA256,
            "anchor probe source drift")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    require(target["execution_rank"] == 46, "target execution rank drift")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "target assurance baseline drift")
    require(target["theorem_complete"] is False, "target manifest overclaims completion")
    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    require(node["v2_execution_rank"] == 280, "v2 execution rank drift")
    require(node["phase_states"][PHASE] == "[ ]", "anchor phase is no longer worker-claimable")
    require(node["phase_states"]["statement"] == "[_]", "statement predecessor state drift")
    require(node["direct_hard_parents"] == [] and node["transitive_hard_ancestors"] == [],
            "hard-parent closure is no longer empty")
    require(node["direct_reuse_hint_ids"] == [] and node["shared_lemma_group_ids"] == [],
            "reuse context is no longer empty")
    require(node["dependency_context_sha256"] == CONTEXT_SHA256, "context digest drift")

    expected_ledger = {
        "schema_version": "stage1-dependency-reuse-ledger/1.1",
        "consumer_theorem_id": THEOREM_ID,
        "observed_theorem_dag_sha256": GRAPH_SHA256,
        "dependency_context_sha256": CONTEXT_SHA256,
        "repository_revision": BASE_REVISION,
        "claim_order": {
            "v2_execution_rank": 280,
            "phase_layer": 2,
            "phase_item_id": ITEM_ID,
        },
        "direct_parent_ids": [],
        "transitive_ancestor_ids": [],
        "hard_edge_ids": [],
        "reuse_hint_ids": [],
        "shared_group_ids": [],
        "parent_inspection_order": [],
        "inspections": [],
        "reuse_decisions": [],
        "unresolved_compatibility_obligations": [],
    }
    require(ledger == expected_ledger, "dependency ledger is not the exact empty audited context")

    require(protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0",
            "wrong discovery protocol schema")
    require(protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID,
            "protocol identity mismatch")
    require(protocol["precommitted_before_replay"] is True, "protocol is not precommitted")
    require(protocol["saturation_claim"] is False, "protocol overclaims saturation")
    require(protocol["canonical_target"]["declaration"] is None,
            "protocol invents a canonical target")
    require([row["lane"] for row in protocol["ordered_search_lanes"]] == ORDERED_LANES,
            "protocol lane order mismatch")
    for field in ("alias_families", "namespace_and_declaration_queries"):
        require(isinstance(protocol.get(field), list) and protocol[field],
                f"protocol lacks {field}")
    require(all(protocol.get(field) for field in (
        "access_credentials_policy", "expected_negative_result_evidence", "network_policy",
        "immutable_refresh_policy")), "protocol lacks access or refresh policy")

    require(evidence["schema_version"] == "stage1-anchor-discovery-evidence/1.0",
            "wrong discovery evidence schema")
    require(evidence["item_id"] == ITEM_ID and evidence["theorem_id"] == THEOREM_ID,
            "evidence identity mismatch")
    require(evidence["network_used_for_replay"] is False, "replay used network")
    lanes = evidence["ordered_lane_results"]
    require([row["lane"] for row in lanes] == ORDERED_LANES, "evidence lane order mismatch")
    for row in lanes:
        require(all(row.get(field) for field in (
            "query_or_source", "revision", "result", "access_boundary", "reopen_condition"
        )), f"incomplete lane result: {row['lane']}")
        require(isinstance(row.get("evidence"), list) and row["evidence"],
                f"unbound lane result: {row['lane']}")
        for binding in row["evidence"]:
            validate_binding(binding, allow_external_mathlib=True)
    require("no saturation" in evidence["classification_boundary"].lower()
            or "no search saturation" in evidence["classification_boundary"].lower(),
            "evidence boundary omits saturation limit")

    require(audit["schema_version"] == "stage1-anchor-audit/1.0", "wrong audit schema")
    require(audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID,
            "audit identity mismatch")
    require(audit["phase"] == PHASE and audit["execution_rank"] == 46
            and audit["v2_execution_rank"] == 280 and audit["phase_layer"] == 2,
            "audit claim order mismatch")
    require(audit["canonical_target"]["status"] == "not_frozen"
            and audit["canonical_target"]["declaration"] is None,
            "audit invents an exact target")
    require(audit["discovery_protocol"]["sha256"] == PROTOCOL_SHA256,
            "audit protocol binding mismatch")
    require(audit["discovery_evidence"]["sha256"] == EVIDENCE_SHA256,
            "audit evidence binding mismatch")
    require(audit["dependency_reuse_context"]["sha256"] == LEDGER_SHA256,
            "audit ledger binding mismatch")
    require(audit["search_order_completed"] == ORDERED_LANES, "audit lane order mismatch")
    candidates = audit["candidates"]
    require(len(candidates) == len({row["id"] for row in candidates}) == 7,
            "candidate inventory identity or size drift")
    require({row["search_lane"] for row in candidates} <= set(ORDERED_LANES),
            "candidate names an unknown lane")
    for candidate in candidates:
        require(normalize_classification(candidate["classification"]) in MACHINE_STATES,
                f"invalid candidate classification: {candidate['id']}")
        require(all(field in candidate for field in (
            "exact_type", "normalized_match", "toolchain", "dependency_feasibility",
            "proof_body", "placeholder_axiom_unsafe_oracle_status", "blocker",
            "reopen_event", "completion_credit"
        )), f"candidate provenance/trust classification incomplete: {candidate['id']}")
        require(candidate["completion_credit"] is False,
                f"candidate improperly receives root credit: {candidate['id']}")
    require(next(row for row in candidates if row["id"] ==
                 "M0128-C04-KBUZZARD-CLASS-FIELD-THEORY")["classification"] == "M5",
            "wrong external ClassFieldTheory classification")
    require(next(row for row in candidates if row["id"] ==
                 "M0128-C05-LOCAL-CLASS-FIELD-THEORY")["classification"] == "M5",
            "wrong LocalClassFieldTheory classification")
    coverage = audit["classification_coverage"]
    require(coverage["classified_candidates"] == coverage["inventory_size"] == 7,
            "candidate classification coverage incomplete")
    require(coverage["prescribed_lanes_completed"] == coverage["prescribed_lane_count"] == 7,
            "prescribed lane coverage incomplete")
    require(coverage["complete_for_inventory_version"] is True,
            "inventory is not completely classified")
    require(coverage["discovery_saturation_claimed"] is False,
            "audit overclaims discovery saturation")
    require(coverage["fresh_public_discovery_access_limited"] is True,
            "audit hides public discovery access limit")
    require(coverage["exact_terminal_candidate_found"] is False,
            "audit contradicts exact-candidate boundary")
    require(audit["root_vector_before"] == audit["root_vector_after"] == {
        "H": "H2", "M": "M4", "R": "R4"
    }, "root debt vector was improperly upgraded")
    require(audit["audit_complete"] is False and audit["theorem_complete"] is False,
            "anchor audit overclaims terminal completion")
    require(audit["accepted_receipt_ids"] == [], "audit invents accepted receipts")

    phase_contract = next(row for row in contract["phases"] if row["phase"] == PHASE)
    require(phase_contract["layer"] == 2 and phase_contract["intent"] == "audit",
            "phase contract drift")
    required_fields = {pointer.split("/")[1]
                       for pointer in phase_contract["phase_receipt_required_fields"]}
    require(required_fields <= set(receipt), "receipt lacks a contract-required root field")
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
    require(receipt["selftest_result"]["exit_code"] == 0
            and receipt["selftest_result"]["commands"], "receipt self-test commands missing")
    require(receipt["discovery_protocol_sha256"] == PROTOCOL_SHA256,
            "receipt protocol binding mismatch")
    result = receipt["candidate_inventory_result"]
    require(result["classification_complete"] is True
            and result["ordered_lanes_complete"] is True,
            "receipt phase predicate incomplete")
    require(result["root_proof_credit"] is False
            and result["discovery_saturation_claimed"] is False,
            "receipt overclaims proof or saturation")
    require(receipt["audit_complete"] is False and receipt["theorem_complete"] is False,
            "receipt overclaims terminal completion")
    require(receipt["known_failures"] and receipt["first_failed_gate"]
            and receipt["retry_condition"] and receipt["invalidation_inputs"],
            "receipt boundary or freshness data missing")
    require(receipt["dependency_context"]["parent_inspection_order"] == [],
            "receipt parent inspection order drift")
    require(receipt["dependency_context"]["provider_acceptance_inherited"] is False,
            "receipt inherits provider acceptance")

    for name in (
        "task_state_authority", "assurance_authority", "phase_contract", "theorem_dag",
        "target_manifest", "execution_skill", "statement_source", "statement_receipt",
        "discovery_protocol", "anchor_inventory", "anchor_probe_source",
        "dependency_reuse_ledger",
    ):
        validate_binding(receipt["inputs"][name], allow_external_mathlib=True)
    for binding in receipt["inputs"]["discovery_evidence"]:
        validate_binding(binding, allow_external_mathlib=True)
    require(receipt["inputs"]["statement_receipt"]["acceptance_inherited"] is False,
            "statement receipt acceptance was inherited")

    require(packet["item_id"] == ITEM_ID and packet["state"] == "[_]",
            "worker packet identity or state mismatch")
    require(packet["base_revision"] == BASE_REVISION, "worker packet base drift")
    require(packet["commands"] == receipt["selftest_result"]["commands"],
            "packet and receipt command records disagree")
    require(packet["known_failures"] == receipt["known_failures"],
            "packet and receipt known failures disagree")
    require(set(packet["changed_paths"]) == set(receipt["changed_paths"]),
            "packet and receipt changed paths disagree")
    require(receipt["inputs"]["anchor_validator"] == {
        "path": "Stage1_Instances/THM-M-0128/check_anchor_audit.py",
        "sha256": sha256(HERE / "check_anchor_audit.py"),
        "git_blob": git_blob(HERE / "check_anchor_audit.py"),
    }, "receipt validator binding mismatch")

    probe_source = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "#check NumberField.IsCMField",
        "#check NumberField.AdeleRing",
        "#check NumberField.AdeleRing.algebraMap_injective",
        "#print axioms NumberField.AdeleRing.algebraMap_injective",
    ):
        require(marker in probe_source, f"anchor probe lost {marker}")
    stripped = re.sub(r"/-.*?-/", "", probe_source, flags=re.DOTALL)
    stripped = re.sub(r"--.*", "", stripped)
    require(not re.search(
        r"\b(?:sorry|admit|sorryAx|axiom|opaque|unsafe|implemented_by|native_decide)\b",
        stripped,
    ), "anchor probe contains a prohibited construct")
    require(not re.search(r"^(?:def|theorem|lemma|example)\s+", stripped, re.MULTILINE),
            "anchor probe invents a target declaration")

    require(output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION,
            "mathlib revision drift")
    require(output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE,
            "mathlib tree drift")
    require(output("git", "status", "--short", cwd=MATHLIB) == "",
            "mathlib worktree is dirty")

    lean = subprocess.run(
        [
            "env", "LEAN_NUM_THREADS=1", "LC_ALL=C", "TZ=UTC", "timeout",
            "--foreground", "--kill-after=5s", "300s", "lake", "env", "lean",
            "../../Stage1_Instances/THM-M-0128/AnchorAudit.lean",
        ],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=315,
        check=False,
    )
    require(lean.returncode == 0, f"Lean probe failed: {lean.stderr}{lean.stdout}")
    combined = lean.stderr + lean.stdout
    require("NumberField.IsCMField" in combined and "NumberField.AdeleRing" in combined,
            "Lean probe omitted object anchors")
    require("'NumberField.AdeleRing.algebraMap_injective' depends on axioms: "
            "[propext, Classical.choice, Quot.sound]" in combined,
            "Lean support-lemma axiom boundary drift")


def semantic_result(*, passed: bool, message: str) -> dict:
    result = {
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
    require(set(result) == REQUIRED_RESULT_FIELDS, "semantic result field drift")
    return result


def main() -> int:
    try:
        validate()
    except Exception as exc:  # Emit exactly one typed JSON object on every path.
        print(json.dumps(
            semantic_result(passed=False, message=str(exc)),
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        ))
        return 1
    print(json.dumps(
        semantic_result(
            passed=True,
            message=(
                "A01-A03 proven for seven content-bound candidate groups and all seven ordered "
                "lanes; the empty dependency closure is audited, public discovery limits are "
                "explicit, and no exact root, proof credit, AUDIT-Z, or THEOREM-Z is claimed."
            ),
        ),
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
