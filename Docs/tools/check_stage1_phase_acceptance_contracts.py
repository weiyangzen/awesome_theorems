#!/usr/bin/env python3
"""Validate the authoritative Stage1 seven-phase master-acceptance contract."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "Docs" / "Stage1_Phase_Acceptance_Contracts.json"
CONTRACT_SHA256 = "1bd6739c15fb424c53095401553ca3224f1398c9ba5a84e8a9a6382daed8b849"

PHASES = (
    "intake",
    "statement",
    "anchor_audit",
    "obligation_tree",
    "proof",
    "validation",
    "release",
)
PHASE_METADATA = {
    "intake": (0, "INTAKE", "intake"),
    "statement": (1, "STATEMENT", "audit"),
    "anchor_audit": (2, "ANCHOR_AUDIT", "audit"),
    "obligation_tree": (3, "OBLIGATION_TREE", "audit"),
    "proof": (4, "PROOF", "prove"),
    "validation": (5, "VALIDATION", "validate"),
    "release": (6, "RELEASE", "release"),
}
WORKER_VERDICTS = (
    "accepted",
    "accepted_audit_only",
    "no_state_change",
    "blocked",
    "rejected",
)
REVIEW_VERDICTS = ("phase_accepted", "repair_required", "rejected")
REQUIRED_RECEIPT_FIELDS = {
    "/schema_version",
    "/receipt_id",
    "/item_id",
    "/theorem_id",
    "/phase",
    "/intent",
    "/base_revision",
    "/base_tree",
    "/inputs",
    "/support_state",
    "/proposed_state",
    "/accepted",
    "/verdict",
    "/selftest_status",
    "/selftest_result/exit_code",
    "/selftest_result/commands",
    "/known_failures",
    "/first_failed_gate",
    "/retry_condition",
    "/status_boundary",
    "/audit_complete",
    "/theorem_complete",
    "/invalidation_inputs",
}
SEMANTIC_CHECKS = {
    "artifact_roles_resolved",
    "candidate_classification_complete",
    "composition_certificates_valid",
    "content_hashes_match",
    "dependency_context_complete",
    "discovery_protocol_complete",
    "json_fields_equal",
    "json_fields_present",
    "kernel_proof_replay_passes",
    "lean_exact_target_replay",
    "mutation_suite_passes",
    "obligation_registry_complete",
    "prohibited_constructs_absent",
    "public_reconciliation_clean",
    "release_protocol_passes",
    "reuse_ledger_valid",
    "terminal_decisions_consistent",
    "trust_provenance_recomputed",
    "typed_graphs_valid",
    "validation_recipes_all_pass",
}

TOP_LEVEL_KEYS = {
    "schema_version",
    "authority_id",
    "requirements_authority",
    "task_state_authority",
    "phase_order",
    "state_protocol",
    "verdict_protocol",
    "artifact_resolution",
    "validator_selection",
    "review_runtime",
    "common_master_gates",
    "source_references",
    "phases",
}
PHASE_KEYS = {
    "phase",
    "layer",
    "item_suffix",
    "intent",
    "completion_semantics",
    "phase_acceptance_claim",
    "phase_acceptance_does_not_claim",
    "worker_verdicts_eligible_for_review",
    "raw_blocked_can_close_phase",
    "classified_negative_findings_may_satisfy_deliverable",
    "truthful_negative_boundary",
    "audit_boundary",
    "theorem_boundary",
    "required_artifact_roles",
    "phase_receipt_required_fields",
    "validator_candidates",
    "semantic_gates",
    "source_reference_ids",
}


class ContractError(ValueError):
    """Raised when the acceptance authority is incomplete or unsafe."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def exact_keys(value: Any, expected: set[str], context: str) -> dict[str, Any]:
    require(isinstance(value, dict), f"{context} must be an object")
    require(set(value) == expected, f"{context} has invalid fields: {sorted(set(value) ^ expected)}")
    return value


def string_list(value: Any, context: str, *, nonempty: bool = True) -> list[str]:
    require(isinstance(value, list), f"{context} must be a list")
    require(not nonempty or bool(value), f"{context} must not be empty")
    require(
        all(isinstance(item, str) and item for item in value),
        f"{context} must contain nonempty strings",
    )
    require(len(value) == len(set(value)), f"{context} contains duplicates")
    return value


def source_reference_map(data: dict[str, Any], root: Path) -> dict[str, dict[str, Any]]:
    references = data.get("source_references")
    require(isinstance(references, list) and references, "source_references must be nonempty")
    result: dict[str, dict[str, Any]] = {}
    for index, value in enumerate(references):
        row = exact_keys(
            value,
            {"reference_id", "path", "line_start", "line_end", "required_phrases"},
            f"source_references[{index}]",
        )
        reference_id = row["reference_id"]
        require(isinstance(reference_id, str) and reference_id, "source reference id is empty")
        require(reference_id not in result, f"duplicate source reference: {reference_id}")
        relative = row["path"]
        require(isinstance(relative, str) and relative, f"{reference_id} path is empty")
        pure = PurePosixPath(relative)
        require(not pure.is_absolute() and ".." not in pure.parts, f"{reference_id} path is unsafe")
        path = root / pure
        require(path.is_file() and not path.is_symlink(), f"{reference_id} source is missing or unsafe")
        start, end = row["line_start"], row["line_end"]
        require(
            isinstance(start, int) and not isinstance(start, bool) and start >= 1,
            f"{reference_id} line_start is invalid",
        )
        require(
            isinstance(end, int) and not isinstance(end, bool) and end >= start,
            f"{reference_id} line_end is invalid",
        )
        lines = path.read_text(encoding="utf-8").splitlines()
        require(end <= len(lines), f"{reference_id} line range is stale")
        excerpt = "\n".join(lines[start - 1 : end])
        for phrase in string_list(row["required_phrases"], f"{reference_id} required_phrases"):
            require(phrase in excerpt, f"{reference_id} no longer contains required phrase: {phrase}")
        result[reference_id] = row
    return result


def validate_reference_ids(value: Any, references: dict[str, Any], context: str) -> list[str]:
    ids = string_list(value, context)
    require(set(ids) <= set(references), f"{context} names an unknown source reference")
    return ids


def validate_state_protocol(value: Any) -> None:
    row = exact_keys(
        value,
        {
            "not_done",
            "worker_self_tested",
            "master_accepted",
            "worker_transition",
            "master_transition",
            "phase_acceptance_scope",
            "unfinished_states",
        },
        "state_protocol",
    )
    require(row["not_done"] == "[ ]", "not_done symbol changed")
    require(row["worker_self_tested"] == "[_]", "worker_self_tested symbol changed")
    require(row["master_accepted"] == "[x]", "master_accepted symbol changed")
    require(row["worker_transition"] == "[ ] -> [_]", "worker transition is not fail-closed")
    require(row["master_transition"] == "[_] -> [x]", "master transition is not fail-closed")
    require(
        row["phase_acceptance_scope"] == "phase_evidence_and_typed_deliverable_only",
        "phase acceptance scope conflates theorem completion",
    )
    require(row["unfinished_states"] == ["[ ]", "[_]"], "unfinished state vocabulary changed")


def validate_verdict_protocol(value: Any) -> None:
    row = exact_keys(
        value,
        {
            "closed_worker_vocabulary",
            "closed_review_vocabulary",
            "preserve_worker_verdict",
            "worker_verdict_is_not_master_verdict",
            "blocked_policy",
            "no_state_change_policy",
            "accepted_audit_only_policy",
            "terminal_flags",
        },
        "verdict_protocol",
    )
    require(tuple(row["closed_worker_vocabulary"]) == WORKER_VERDICTS, "worker verdict vocabulary changed")
    require(tuple(row["closed_review_vocabulary"]) == REVIEW_VERDICTS, "review verdict vocabulary changed")
    require(row["preserve_worker_verdict"] is True, "worker verdict must be immutable")
    require(row["worker_verdict_is_not_master_verdict"] is True, "worker and master verdicts are conflated")
    blocked = exact_keys(
        row["blocked_policy"],
        {"raw_blocked_can_close_phase", "raw_blocked_auto_promotes", "required_action"},
        "blocked_policy",
    )
    require(blocked["raw_blocked_can_close_phase"] is False, "raw blocked may not close a phase")
    require(blocked["raw_blocked_auto_promotes"] is False, "raw blocked may not auto-promote")
    require(
        blocked["required_action"] == "remain_worker_self_tested_and_emit_repair_or_blocker",
        "blocked action is unsafe",
    )
    no_change = exact_keys(
        row["no_state_change_policy"],
        {"can_be_reviewed", "phase_closure_condition"},
        "no_state_change_policy",
    )
    require(no_change["can_be_reviewed"] is True, "no_state_change evidence cannot be discarded")
    require(
        no_change["phase_closure_condition"] == "master_independently_proves_the_phase_completion_predicate",
        "no_state_change is being treated as automatic acceptance",
    )
    audit_only = exact_keys(
        row["accepted_audit_only_policy"],
        {"allowed_phases", "phase_can_close", "audit_complete", "theorem_complete"},
        "accepted_audit_only_policy",
    )
    require(audit_only["allowed_phases"] == ["release"], "accepted_audit_only escaped release")
    require(audit_only["phase_can_close"] is True, "accepted_audit_only must be able to close release")
    require(audit_only["audit_complete"] is True, "accepted_audit_only must mean AUDIT-Z")
    require(audit_only["theorem_complete"] is False, "accepted_audit_only manufactured theorem completion")
    require(row["terminal_flags"] == ["audit_complete", "theorem_complete"], "terminal flags changed")


def validate_artifact_resolution(value: Any) -> None:
    row = exact_keys(
        value,
        {
            "owner_root_pattern",
            "selected_artifact_binding_fields",
            "matching_path_never_implies_compliance",
            "aliases_are_candidates_only",
            "selected_files_must_be_head_tracked",
            "selected_files_must_not_be_symlinks",
            "selected_files_must_be_read_once_and_hash_bound",
            "per_item_role_map_required",
            "per_item_role_map_owner",
            "per_item_role_map_schema",
            "per_item_role_map_path_pattern",
            "per_item_role_map_required_fields",
            "per_item_role_map_publication",
            "worker_phase_receipt_schema",
            "worker_phase_receipt_required_fields",
            "master_acceptance_receipt_schema",
            "missing_or_ambiguous_role_action",
        },
        "artifact_resolution",
    )
    require(row["owner_root_pattern"] == "Stage1_Instances/{theorem_id}", "owner root pattern changed")
    require(
        row["selected_artifact_binding_fields"] == ["role", "path", "sha256", "git_blob"],
        "artifact binding is not content-addressed",
    )
    for field in (
        "matching_path_never_implies_compliance",
        "aliases_are_candidates_only",
        "selected_files_must_be_head_tracked",
        "selected_files_must_not_be_symlinks",
        "selected_files_must_be_read_once_and_hash_bound",
        "per_item_role_map_required",
    ):
        require(row[field] is True, f"artifact rule disabled: {field}")
    require(row["per_item_role_map_owner"] == "scheduler_master_lane", "per-item role map is not authority-owned")
    require(
        row["per_item_role_map_schema"] == "stage1-phase-artifact-role-map/1.0",
        "per-item role-map schema changed",
    )
    require(
        row["per_item_role_map_path_pattern"]
        == ".cron/stage1-v2-app-server/role-maps/{item_id}.json",
        "per-item role-map path changed",
    )
    require(
        row["per_item_role_map_required_fields"]
        == [
            "/schema_version",
            "/item_id",
            "/theorem_id",
            "/phase",
            "/base_revision",
            "/contract_sha256",
            "/artifacts",
        ],
        "per-item role map lacks an exact identity or artifact binding",
    )
    require(
        row["per_item_role_map_publication"] == "before_review_claim",
        "per-item role map must be frozen before independent review",
    )
    require(row["worker_phase_receipt_schema"] == "stage1-node-receipt/1.0", "worker receipt schema changed")
    receipt_fields = set(string_list(row["worker_phase_receipt_required_fields"], "worker receipt fields"))
    require(receipt_fields == REQUIRED_RECEIPT_FIELDS, "worker receipt minimum fields changed")
    require(
        row["master_acceptance_receipt_schema"] == "stage1-master-phase-acceptance/1.0",
        "master receipt schema changed",
    )
    require(row["missing_or_ambiguous_role_action"] == "fail_closed", "artifact ambiguity must fail closed")


def validate_validator_selection(value: Any) -> None:
    row = exact_keys(
        value,
        {
            "owner",
            "selection_source",
            "worker_or_reviewer_may_select_argv",
            "require_exactly_one_candidate",
            "candidate_must_exist_at_worker_base",
            "candidate_head_blob_must_equal_worker_base_blob",
            "argv_templates",
            "cwd",
            "shell_interpolation",
            "repo_write_access",
            "isolated_scratch_write_access",
            "network_policy",
            "exit_zero_is_sufficient",
            "semantic_result_required",
            "missing_or_ambiguous_action",
        },
        "validator_selection",
    )
    require(row["owner"] == "scheduler_master_lane", "validator owner is not the master lane")
    require(row["selection_source"] == "this_contract_at_authoritative_head", "validator source is mutable")
    require(row["worker_or_reviewer_may_select_argv"] is False, "worker-selected argv is forbidden")
    require(row["require_exactly_one_candidate"] is True, "validator selection is ambiguous")
    require(row["candidate_must_exist_at_worker_base"] is True, "worker-created validator could be accepted")
    require(
        row["candidate_head_blob_must_equal_worker_base_blob"] is True,
        "worker-modified validator could be accepted",
    )
    templates = row["argv_templates"]
    require(
        templates
        == {
            "python": ["/usr/bin/python3", "-I", "-B", "{validator_path}"],
            "bash": ["/usr/bin/bash", "{validator_path}"],
        },
        "validator argv templates are not exact",
    )
    require(row["cwd"] == ".", "validator cwd changed")
    require(row["shell_interpolation"] is False, "shell interpolation is forbidden")
    require(row["repo_write_access"] is False, "review validator may not write the repository")
    require(row["isolated_scratch_write_access"] is True, "review validators need isolated scratch")
    require(row["network_policy"] == "denied", "review replay network must be denied")
    require(row["exit_zero_is_sufficient"] is False, "exit zero cannot erase a negative verdict")
    require(row["semantic_result_required"] is True, "validator semantic result is mandatory")
    require(row["missing_or_ambiguous_action"] == "fail_closed", "missing validator must fail closed")


def validate_review_runtime(value: Any) -> None:
    row = exact_keys(
        value,
        {
            "protocol",
            "per_item_goal_required",
            "model",
            "reasoning_effort",
            "service_tier",
            "catalog_label",
            "repo_access",
            "scratch_access",
            "network_access",
            "shared_total_concurrency_limit",
        },
        "review_runtime",
    )
    require(row["protocol"] == "codex-app-server-jsonl", "review must use Codex app-server")
    require(row["per_item_goal_required"] is True, "review must have a persisted /goal")
    require(row["model"] == "gpt-5.6-sol", "review model changed")
    require(row["reasoning_effort"] == "ultra", "review effort changed")
    require(row["service_tier"] == "default", "review service tier changed")
    require(row["catalog_label"] == "Default", "default catalog label changed")
    require(row["repo_access"] == "read_only", "review repository must be read-only")
    require(row["scratch_access"] == "isolated_writable", "review scratch must be isolated")
    require(row["network_access"] is False, "review network must be disabled")
    require(row["shared_total_concurrency_limit"] == 0, "implementation/review total concurrency must be frozen at zero")


def validate_artifact_roles(value: Any, phase: str) -> None:
    require(isinstance(value, list) and value, f"{phase} artifact roles must be nonempty")
    roles: set[str] = set()
    for index, item in enumerate(value):
        row = exact_keys(
            item,
            {
                "role",
                "requirement",
                "cardinality",
                "resolution",
                "path_candidates",
                "binding_pointer",
                "aliases_are_candidates_only",
                "content_requirements",
            },
            f"{phase}.required_artifact_roles[{index}]",
        )
        role = row["role"]
        require(isinstance(role, str) and role and role not in roles, f"{phase} has duplicate artifact role")
        roles.add(role)
        require(row["requirement"] in {"required", "conditional"}, f"{phase}/{role} requirement is invalid")
        require(row["cardinality"] in {"exactly_one", "one_or_more"}, f"{phase}/{role} cardinality is invalid")
        require(
            row["resolution"] in {"path_candidates", "receipt_bound_paths"},
            f"{phase}/{role} resolution is invalid",
        )
        paths = string_list(
            row["path_candidates"],
            f"{phase}/{role} path_candidates",
            nonempty=row["resolution"] == "path_candidates",
        )
        for path in paths:
            pure = PurePosixPath(path.format(theorem_id="THM-M-0001"))
            require(
                not pure.is_absolute()
                and ".." not in pure.parts
                and tuple(pure.parts[:2]) == ("Stage1_Instances", "THM-M-0001"),
                f"{phase}/{role} path candidate escapes theorem ownership",
            )
        if row["resolution"] == "receipt_bound_paths":
            require(paths == [], f"{phase}/{role} receipt-bound role must not guess paths")
            require(
                isinstance(row["binding_pointer"], str) and row["binding_pointer"].startswith("/inputs/"),
                f"{phase}/{role} binding pointer is invalid",
            )
        else:
            require(row["binding_pointer"] is None, f"{phase}/{role} path role has an unexpected pointer")
        require(row["aliases_are_candidates_only"] is True, f"{phase}/{role} aliases imply compliance")
        string_list(row["content_requirements"], f"{phase}/{role} content requirements")
    require("phase_receipt" in roles, f"{phase} lacks a phase receipt role")


def validate_validator_candidates(value: Any, phase: str, selection: dict[str, Any]) -> None:
    require(isinstance(value, list) and value, f"{phase} validator candidates must be nonempty")
    seen: set[str] = set()
    for index, item in enumerate(value):
        row = exact_keys(
            item,
            {"path_pattern", "language", "argv_template", "candidate_only"},
            f"{phase}.validator_candidates[{index}]",
        )
        path = row["path_pattern"]
        require(isinstance(path, str) and path not in seen, f"{phase} validator path is invalid or duplicate")
        seen.add(path)
        expanded = PurePosixPath(path.format(theorem_id="THM-M-0001"))
        require(
            tuple(expanded.parts[:2]) == ("Stage1_Instances", "THM-M-0001")
            and ".." not in expanded.parts,
            f"{phase} validator escapes theorem ownership",
        )
        language = row["language"]
        require(language in {"python", "bash"}, f"{phase} validator language is invalid")
        require(
            row["argv_template"] == selection["argv_templates"][language],
            f"{phase} validator argv is not scheduler-derived",
        )
        require(row["candidate_only"] is True, f"{phase} validator filename implies authority")


def validate_semantic_gates(value: Any, phase: str, references: dict[str, Any]) -> None:
    require(isinstance(value, list) and value, f"{phase} semantic gates must be nonempty")
    gate_ids: set[str] = set()
    for index, item in enumerate(value):
        row = exact_keys(
            item,
            {"gate_id", "check", "parameters", "source_reference_ids"},
            f"{phase}.semantic_gates[{index}]",
        )
        gate_id = row["gate_id"]
        require(isinstance(gate_id, str) and gate_id and gate_id not in gate_ids, f"{phase} gate id is invalid")
        gate_ids.add(gate_id)
        require(row["check"] in SEMANTIC_CHECKS, f"{phase}/{gate_id} uses unknown machine check")
        require(isinstance(row["parameters"], dict) and row["parameters"], f"{phase}/{gate_id} parameters missing")
        validate_reference_ids(row["source_reference_ids"], references, f"{phase}/{gate_id} references")


def validate_contract_digest(path: Path, canonical: str) -> None:
    """Bind production validation to the reviewed, authoritative contract bytes."""
    if path.resolve() != CONTRACT.resolve():
        return
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    require(
        digest == CONTRACT_SHA256,
        "authoritative acceptance contract digest changed without validator review",
    )


def validate_phase(
    value: Any,
    expected_phase: str,
    references: dict[str, Any],
    selection: dict[str, Any],
) -> None:
    row = exact_keys(value, PHASE_KEYS, f"phase {expected_phase}")
    layer, suffix, intent = PHASE_METADATA[expected_phase]
    require(row["phase"] == expected_phase, f"phase order mismatch at {expected_phase}")
    require(row["layer"] == layer, f"{expected_phase} layer is wrong")
    require(row["item_suffix"] == suffix, f"{expected_phase} item suffix is wrong")
    require(row["intent"] == intent, f"{expected_phase} intent is wrong")
    require(isinstance(row["completion_semantics"], str) and row["completion_semantics"], f"{expected_phase} completion semantics missing")
    require(isinstance(row["phase_acceptance_claim"], str) and row["phase_acceptance_claim"], f"{expected_phase} acceptance claim missing")
    string_list(row["phase_acceptance_does_not_claim"], f"{expected_phase} nonclaims")
    eligible = string_list(row["worker_verdicts_eligible_for_review"], f"{expected_phase} eligible verdicts")
    require(set(eligible) <= set(WORKER_VERDICTS), f"{expected_phase} uses unknown worker verdict")
    require("blocked" not in eligible and "rejected" not in eligible, f"{expected_phase} reviews a raw failure as closable")
    if expected_phase == "release":
        require("accepted_audit_only" in eligible, "release must admit accepted_audit_only")
    else:
        require("accepted_audit_only" not in eligible, f"accepted_audit_only escaped release into {expected_phase}")
    require(row["raw_blocked_can_close_phase"] is False, f"raw blocked closes {expected_phase}")
    require(
        isinstance(row["classified_negative_findings_may_satisfy_deliverable"], bool),
        f"{expected_phase} negative-evidence boundary is not explicit",
    )
    require(
        isinstance(row["truthful_negative_boundary"], str) and row["truthful_negative_boundary"],
        f"{expected_phase} truthful-negative boundary missing",
    )
    audit = exact_keys(
        row["audit_boundary"],
        {"phase_acceptance_implies_audit_complete", "allowed_audit_complete_values", "condition"},
        f"{expected_phase}.audit_boundary",
    )
    theorem = exact_keys(
        row["theorem_boundary"],
        {"phase_acceptance_implies_theorem_complete", "allowed_theorem_complete_values", "condition"},
        f"{expected_phase}.theorem_boundary",
    )
    require(isinstance(audit["phase_acceptance_implies_audit_complete"], bool), f"{expected_phase} audit implication invalid")
    require(isinstance(theorem["phase_acceptance_implies_theorem_complete"], bool), f"{expected_phase} theorem implication invalid")
    require(
        isinstance(audit["allowed_audit_complete_values"], list)
        and audit["allowed_audit_complete_values"]
        and set(audit["allowed_audit_complete_values"]) <= {True, False},
        f"{expected_phase} audit values invalid",
    )
    require(
        isinstance(theorem["allowed_theorem_complete_values"], list)
        and theorem["allowed_theorem_complete_values"]
        and set(theorem["allowed_theorem_complete_values"]) <= {True, False},
        f"{expected_phase} theorem values invalid",
    )
    require(isinstance(audit["condition"], str) and audit["condition"], f"{expected_phase} audit condition missing")
    require(isinstance(theorem["condition"], str) and theorem["condition"], f"{expected_phase} theorem condition missing")
    if expected_phase == "release":
        require(audit["phase_acceptance_implies_audit_complete"] is True, "accepted release must complete AUDIT-Z")
        require(audit["allowed_audit_complete_values"] == [True], "release may not close with an incomplete audit")
        require(theorem["phase_acceptance_implies_theorem_complete"] is False, "release [x] is not necessarily THEOREM-Z")
        require(theorem["allowed_theorem_complete_values"] == [False, True], "release must preserve both terminal outcomes")
    else:
        require(audit["phase_acceptance_implies_audit_complete"] is False, f"{expected_phase} manufactured AUDIT-Z")
        require(theorem["phase_acceptance_implies_theorem_complete"] is False, f"{expected_phase} manufactured THEOREM-Z")
    if expected_phase in {"proof", "validation", "statement"}:
        require(
            row["classified_negative_findings_may_satisfy_deliverable"] is False,
            f"{expected_phase} accepts a negative result as its positive deliverable",
        )
    validate_artifact_roles(row["required_artifact_roles"], expected_phase)
    phase_fields = set(string_list(row["phase_receipt_required_fields"], f"{expected_phase} receipt fields"))
    require(REQUIRED_RECEIPT_FIELDS <= phase_fields, f"{expected_phase} receipt drops common authority fields")
    validate_validator_candidates(row["validator_candidates"], expected_phase, selection)
    validate_semantic_gates(row["semantic_gates"], expected_phase, references)
    validate_reference_ids(row["source_reference_ids"], references, f"{expected_phase} source references")


def validate_common_gates(value: Any, references: dict[str, Any]) -> None:
    require(isinstance(value, list) and value, "common_master_gates must be nonempty")
    ids: set[str] = set()
    for index, item in enumerate(value):
        row = exact_keys(
            item,
            {"gate_id", "requirement", "source_reference_ids", "failure_action"},
            f"common_master_gates[{index}]",
        )
        gate_id = row["gate_id"]
        require(isinstance(gate_id, str) and gate_id and gate_id not in ids, "common gate id is invalid")
        ids.add(gate_id)
        require(isinstance(row["requirement"], str) and row["requirement"], f"{gate_id} requirement missing")
        validate_reference_ids(row["source_reference_ids"], references, f"{gate_id} references")
        require(row["failure_action"] in {"remain_[_]", "rollback_and_remain_[_]"}, f"{gate_id} failure action is unsafe")
    required = {
        "G01-SSOT-CAS",
        "G02-TOPOLOGY",
        "G03-ARTIFACT-BINDING",
        "G04-INDEPENDENT-REVIEW",
        "G05-AUTHORITY-REPLAY",
        "G06-SEMANTIC-VERDICT",
        "G07-REV56-RECOMPUTE",
        "G08-V2-CONTEXT",
        "G09-FRESHNESS",
        "G10-RECONCILIATION",
        "G11-ATOMIC-PAUSE",
        "G12-MASTER-RECEIPT",
    }
    require(ids == required, "common master gate coverage is incomplete")


def validate_contract(data: Any, *, root: Path = ROOT) -> dict[str, Any]:
    contract = exact_keys(data, TOP_LEVEL_KEYS, "contract")
    require(contract["schema_version"] == "stage1-phase-acceptance-contracts/1.0", "schema version changed")
    require(contract["authority_id"] == "stage1-v2-seven-phase-master-acceptance", "authority id changed")
    require(contract["requirements_authority"] == "Docs/Stage1_Blueprint_rev-5.6.md", "requirements authority changed")
    require(contract["task_state_authority"] == "Docs/Stage1_Blueprint_v2.md", "task-state authority changed")
    require(tuple(contract["phase_order"]) == PHASES, "phase order changed")
    references = source_reference_map(contract, root)
    validate_state_protocol(contract["state_protocol"])
    validate_verdict_protocol(contract["verdict_protocol"])
    validate_artifact_resolution(contract["artifact_resolution"])
    validate_validator_selection(contract["validator_selection"])
    validate_review_runtime(contract["review_runtime"])
    validate_common_gates(contract["common_master_gates"], references)
    phases = contract["phases"]
    require(isinstance(phases, list) and len(phases) == len(PHASES), "contract must define exactly seven phases")
    for phase, value in zip(PHASES, phases):
        validate_phase(value, phase, references, contract["validator_selection"])
    return contract


def load_contract(path: Path = CONTRACT) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ContractError(f"cannot read acceptance contract: {exc}") from exc
    require(isinstance(value, dict), "acceptance contract must contain an object")
    return value


def validate_file(path: Path = CONTRACT, *, root: Path = ROOT) -> dict[str, Any]:
    value = load_contract(path)
    canonical = json.dumps(value, ensure_ascii=True, indent=2) + "\n"
    require(path.read_text(encoding="utf-8") == canonical, "acceptance contract is not canonical JSON")
    validate_contract_digest(path, canonical)
    return validate_contract(value, root=root)


def fail(message: str) -> NoReturn:
    raise SystemExit(f"check_stage1_phase_acceptance_contracts: {message}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, default=CONTRACT)
    args = parser.parse_args()
    try:
        value = validate_file(args.contract)
    except ContractError as exc:
        fail(str(exc))
    print(
        "check_stage1_phase_acceptance_contracts: ok "
        f"({len(value['phases'])} phases, {len(value['common_master_gates'])} common gates, "
        f"{len(value['source_references'])} source references)"
    )


if __name__ == "__main__":
    main()
