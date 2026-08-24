#!/usr/bin/env python3
"""Exact BOOT contracts for the three Stage5 execution JSON Schemas.

The bootstrap manager must not accept a schema merely because its root object
has ``additionalProperties: false``.  Such a check admits vacuous documents
and leaves nested records open.  This module freezes the complete, recursively
closed schema bytes for theorem and conjecture execution artifacts and exposes
small validation helpers for the manager to call.

The module intentionally has no dependency on the bootstrap manager or on a
third-party JSON Schema implementation.  It validates the schema *document*
against a reviewed canonical contract; the accepted ongoing controller is
responsible for validating claim/result/acceptance instances against it.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from types import MappingProxyType
from typing import Any, Mapping


JSON_SCHEMA_DRAFT = "https://json-schema.org/draft/2020-12/schema"
BOOT_SCHEMA_FILENAMES = (
    "claim-card.schema.json",
    "worker-result.schema.json",
    "master-acceptance.schema.json",
)
BOOT_PROGRAM_KINDS = frozenset({"theorem", "conjecture"})

_SHA256_PATTERN = r"^[0-9a-f]{64}$"
_SAFE_ID_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9._:@-]{0,199}$"
_MODE_PATTERN = r"^[A-Z][A-Z0-9-]{0,63}$"
_ENV_NAME_PATTERN = r"^[A-Za-z_][A-Za-z0-9_]*$"
_CONCURRENCY_DIMENSIONS = (
    "logical_claims",
    "service_records",
    "agent_executions",
    "startup_reservations",
    "launch_fanout_per_wave",
    "live_transports",
    "authenticated_goals",
    "running_turns",
    "outbound_request_starts_per_window",
    "in_flight_requests",
    "integration",
    "validators",
    "exact_path_conflicts",
)


class BootSchemaContractError(ValueError):
    """A candidate BOOT schema is not the exact reviewed contract."""


def canonical_json_bytes(value: Any) -> bytes:
    """Return the repository's canonical JSON encoding."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _string(*, min_length: int = 1, pattern: str | None = None,
            enum: tuple[str, ...] | None = None, const: str | None = None,
            format_: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"type": "string"}
    if min_length:
        result["minLength"] = min_length
    if pattern is not None:
        result["pattern"] = pattern
    if enum is not None:
        result["enum"] = list(enum)
    if const is not None:
        result["const"] = const
    if format_ is not None:
        result["format"] = format_
    return result


def _integer(*, minimum: int = 0, maximum: int | None = None,
             const: int | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"type": "integer", "minimum": minimum}
    if maximum is not None:
        result["maximum"] = maximum
    if const is not None:
        result["const"] = const
    return result


def _boolean(*, const: bool | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"type": "boolean"}
    if const is not None:
        result["const"] = const
    return result


def _array(
    items: dict[str, Any], *, min_items: int = 0, unique: bool = False
) -> dict[str, Any]:
    result: dict[str, Any] = {"type": "array", "items": items}
    if min_items:
        result["minItems"] = min_items
    if unique:
        result["uniqueItems"] = True
    return result


def _closed_object(properties: Mapping[str, dict[str, Any]]) -> dict[str, Any]:
    copied = dict(properties)
    return {
        "type": "object",
        "additionalProperties": False,
        "required": list(copied),
        "properties": copied,
    }


def _schema_root(schema_id: str, properties: Mapping[str, dict[str, Any]]) -> dict[str, Any]:
    body = _closed_object(properties)
    return {
        "$schema": JSON_SCHEMA_DRAFT,
        "$id": schema_id,
        "type": body["type"],
        "additionalProperties": body["additionalProperties"],
        "required": body["required"],
        "properties": body["properties"],
    }


def _schema_id(program_kind: str, stem: str) -> str:
    return (
        "https://awesome-theorems.invalid/schemas/"
        f"stage5-{program_kind}-{stem}-1.0.json"
    )


def _sha256() -> dict[str, Any]:
    return _string(pattern=_SHA256_PATTERN)


def _safe_id() -> dict[str, Any]:
    return _string(pattern=_SAFE_ID_PATTERN)


def _mode() -> dict[str, Any]:
    return _string(pattern=_MODE_PATTERN)


def _path() -> dict[str, Any]:
    # Path canonicality and ownership are semantic controller gates.  The
    # schema still prevents null/number/object substitutions and empty paths.
    return _string()


def _instant() -> dict[str, Any]:
    return _string(format_="date-time", pattern=r"^.+Z$")


def _environment_entry() -> dict[str, Any]:
    return _closed_object(
        {
            "name": _string(pattern=_ENV_NAME_PATTERN),
            "value": _string(min_length=0),
        }
    )


def _command_contract() -> dict[str, Any]:
    return _closed_object(
        {
            "command_id": _safe_id(),
            "cwd": _path(),
            "argv": _array(_string(), min_items=1),
            "environment": _array(_environment_entry(), unique=True),
            "timeout_seconds": _integer(minimum=1),
            "network": _string(enum=("denied", "allowed_by_policy")),
        }
    )


def _read_only_file() -> dict[str, Any]:
    return _closed_object(
        {
            "path": _path(),
            "sha256": _sha256(),
            "size_bytes": _integer(minimum=0),
        }
    )


def _concurrency_vector() -> dict[str, Any]:
    """Return the closed prompt vector used by theorem claim identities."""

    properties: dict[str, dict[str, Any]] = {}
    for dimension in _CONCURRENCY_DIMENSIONS:
        if dimension == "service_records":
            properties[dimension] = _string(const="not_applicable")
        elif dimension == "exact_path_conflicts":
            properties[dimension] = _integer(minimum=0)
        else:
            properties[dimension] = _integer(minimum=1)
    return _closed_object(properties)


def _execution_identity() -> dict[str, Any]:
    return _closed_object(
        {
            "lane_id": _safe_id(),
            "generation_id": _safe_id(),
            "prompt_epoch": _safe_id(),
            "prompt_digest": _sha256(),
            "execution_spec_sha256": _sha256(),
            "requested_concurrency": _concurrency_vector(),
            "resolved_concurrency": _concurrency_vector(),
        }
    )


def _conjecture_proof_search_prompt() -> dict[str, Any]:
    source = _closed_object({
        "repository": _string(const="jinshanmu/CrouzeixConjecture"),
        "commit": _string(const="f9d5c8d39bece41ceedf6346ef50ad1fb393260e"),
        "blob_sha1": _string(const="5b2705db56787157fadbfd9416522feb69b4ad95"),
        "file": _string(const="crouzeix_conjecture_prompt.txt"),
        "file_sha256": _string(const="0a0c3000b81efc4d9edc65ec3cd1d53df0d4e69b24bfee9fe0860301d853d6fc"),
        "extraction_path": _string(const="Docs/researches/Stage5_Crouzeix_Prompt_Extraction.md"),
        "extraction_sha256": _sha256(),
        "evidence_scope": _string(),
    })
    adaptation = _closed_object({
        "worker_topology": _string(),
        "upstream_multiagent_shape": _string(const="not imported"),
        "route_parallelism": _string(),
        "child_agents": _string(const="forbidden"),
        "collaboration_tools": _string(const="forbidden"),
        "hidden_concurrency": _string(const="forbidden"),
    })
    registry = _closed_object({
        "required": _boolean(const=True),
        "group_by": _string(),
        "minimum_fields": _array(_string(), min_items=1, unique=True),
        "state_enum": _array(_string(), min_items=1, unique=True),
        "durable_surfaces": _array(_path(), min_items=1, unique=True),
    })
    return _closed_object({
        "schema_version": _string(const="awesome-theorems/stage5-conjecture-proof-search-prompt/1.0"),
        "source": source,
        "execution_adaptation": adaptation,
        "resolution_roots": _array(_string(), min_items=2, unique=True),
        "approach_registry": registry,
        "search_loop": _array(_string(), min_items=1, unique=True),
        "blocked_route_policy": _string(),
        "adversarial_audit": _array(_string(), min_items=1, unique=True),
        "nonclosure_evidence": _array(_string(), min_items=1, unique=True),
        "completion_rule": _string(),
        "unfinished_rule": _string(),
        "short_goal_clause": _string(),
    })


def _conjecture_occurrence_intake_contract() -> dict[str, Any]:
    """Closed worker-visible contract for non-credit occurrence intake."""

    return _closed_object({
        "schema_version": _string(const="awesome-theorems/stage5-conjecture-occurrence-intake/1.0"),
        "source_occurrence_denominator": _integer(minimum=14865, maximum=14865, const=14865),
        "target_item_range": _array(_string(), min_items=2, unique=True),
        "pool_id_range": _array(_string(), min_items=2, unique=True),
        "authority": _path(),
        "identity_registry": _path(),
        "semantic_boundary": _string(),
        "short_goal_clause": _string(),
        "internal_subchecklist": _array(_string(), min_items=1, unique=True),
        "relation_kind_enum": _array(_string(), min_items=1, unique=True),
        "completion_rule": _string(),
        "promotion_rule": _string(),
    })


def _conjecture_work_contract() -> dict[str, Any]:
    """A closed discriminated union: exactly one task semantics is present."""

    return {
        "oneOf": [
            _closed_object({
                "kind": _string(const="strict_resolution_proof_search"),
                "strict_resolution_proof_search": _conjecture_proof_search_prompt(),
            }),
            _closed_object({
                "kind": _string(const="source_occurrence_intake"),
                "source_occurrence_intake": _conjecture_occurrence_intake_contract(),
            }),
        ]
    }


def _conjecture_typed_outcome() -> dict[str, Any]:
    """Return the exact result/acceptance discriminator for conjecture work."""

    return {
        "oneOf": [
            _closed_object({
                "kind": _string(const="strict_resolution"),
                "polarity": _string(enum=("Claim", "Not Claim")),
                "human_resolution_sha256": _sha256(),
                "lean_root_sha256": _sha256(),
                "machine_cut_set_empty": _boolean(const=True),
                "readability_cut_set_empty": _boolean(const=True),
            }),
            _closed_object({
                "kind": _string(const="source_occurrence_intake"),
                "status_review_sha256": _sha256(),
                "rights_review_sha256": _sha256(),
                "importance_review_sha256": _sha256(),
                "identity_relation": _string(enum=(
                    "exact_existing", "equivalent", "subsumed",
                    "special_case", "same_family", "new_identity",
                    "split_required", "pointer_only", "status_quarantine",
                    "rights_quarantine",
                )),
                "identity_crosswalk_sha256": _sha256(),
                "strict_credit_granted": _boolean(const=False),
                "stage5_claim_id_allocated": _boolean(const=False),
                "stage6_alias_allocated": _boolean(const=False),
            }),
        ]
    }


def _conjecture_workset_member() -> dict[str, Any]:
    return _closed_object({
        "member_id": _safe_id(),
        "member_kind": _string(enum=(
            "strict_resolution", "source_occurrence_intake",
        )),
        "target_item_id": _safe_id(),
        "workset_record_sha256": _sha256(),
        "source_record_sha256": _sha256(),
    })


def _worker_result_schema(program_kind: str) -> dict[str, Any]:
    command_outcome = _closed_object(
        {
            "command_id": _safe_id(),
            "argv_sha256": _sha256(),
            "exit_code": _integer(minimum=0, const=0),
            "passed": _boolean(const=True),
            "stdout_sha256": _sha256(),
            "stderr_sha256": _sha256(),
            "started_at": _instant(),
            "finished_at": _instant(),
        }
    )
    patch = _closed_object(
        {
            "path": _path(),
            "sha256": _sha256(),
            "size_bytes": _integer(minimum=1),
        }
    )
    artifact = _closed_object(
        {
            "path": _path(),
            "sha256": _sha256(),
            "size_bytes": _integer(minimum=0),
            "media_type": _string(),
        }
    )
    properties = {
            "schema_version": _string(
                const="awesome-theorems/stage5-proof-debt-worker-result/1.0"
            ),
            "program": _string(),
            "claim_id": _safe_id(),
            "run_id": _safe_id(),
            "item_id": _safe_id(),
            "mode": _mode(),
            "claim_card_sha256": _sha256(),
            "baseline_sha256": _sha256(),
            "status": _string(const="self_tested"),
            "changed_paths": _array(_path(), min_items=1, unique=True),
            "patch": patch,
            "command_outcomes": _array(command_outcome, min_items=1, unique=True),
            "artifacts": _array(artifact, min_items=1, unique=True),
            "completed_at": _instant(),
            "authority_sha256": _sha256(),
        }
    if program_kind == "conjecture":
        properties["typed_outcome"] = _conjecture_typed_outcome()
    return _schema_root(
        _schema_id(program_kind, "worker-result"),
        properties,
    )


def _claim_card_schema(program_kind: str, worker_schema_sha256: str) -> dict[str, Any]:
    contract_version = "1.1"
    baseline = _closed_object(
        {
            "execution_spec_sha256": _sha256(),
            "blueprint_sha256": _sha256(),
            "source_bundle_sha256": _sha256(),
            "dependency_state_sha256": _sha256(),
            "owned_paths_baseline_sha256": _sha256(),
        }
    )
    artifact_policy = _closed_object(
        {
            "allowed_paths": _array(_path(), min_items=1, unique=True),
            "required_paths": _array(_path(), min_items=1, unique=True),
            "forbidden_paths": _array(_path(), min_items=1, unique=True),
        }
    )
    result_schema = _closed_object(
        {
            "path": _string(
                const=(
                    f"Docs/evidence/stage5_{program_kind}s/"
                    "worker-result.schema.json"
                )
            ),
            "schema_id": _string(
                const=_schema_id(program_kind, "worker-result")
            ),
            "sha256": _string(
                pattern=_SHA256_PATTERN, const=worker_schema_sha256
            ),
        }
    )
    resource_budget = _closed_object(
        {
            "model_input_tokens": _integer(minimum=1),
            "model_output_tokens": _integer(minimum=1),
            "model_turns": _string(const="unbounded"),
            "external_launches": _integer(minimum=1),
            "wall_seconds": _integer(minimum=1),
            "cpu_seconds": _integer(minimum=1),
        }
    )
    retry_budget = _closed_object(
        {
            "attempt": _integer(minimum=1),
            "max_attempts": _integer(minimum=1),
        }
    )
    properties = {
            "schema_version": _string(
                const=f"awesome-theorems/stage5-proof-debt-claim-card/{contract_version}"
            ),
            "program": _string(),
            "claim_id": _safe_id(),
            "run_id": _safe_id(),
            "item_id": _safe_id(),
            "mode": _mode(),
            "dependencies": _array(_safe_id(), unique=True),
            "baseline": baseline,
            "deadline": _instant(),
            "task_root": _path(),
            "canonical_repository_root": _string(),
            "canonical_write_policy": _string(const="forbidden"),
            "writable_paths": _array(_path(), min_items=1, unique=True),
            "read_only_bootstrap_files": _array(
                _read_only_file(), min_items=1, unique=True
            ),
            "deliverable": _string(),
            "validation_commands": _array(
                _command_contract(), min_items=1, unique=True
            ),
            "artifact_policy": artifact_policy,
            "result_schema": result_schema,
            "resource_budget": resource_budget,
            "retry_budget": retry_budget,
        }
    if program_kind == "conjecture":
        properties["execution_identity"] = _execution_identity()
        properties["workset_member"] = _conjecture_workset_member()
        properties["work_contract"] = _conjecture_work_contract()
    # The execution controller being repaired in Stage5 is theorem-scoped.
    # Make a theorem claim independently auditable against its exact prompt/vector.
    if program_kind == "theorem":
        properties["execution_identity"] = _execution_identity()
        properties["execution_policy"] = _closed_object({
            "execution_limits": _closed_object({
                "generation_lifetime_seconds": _integer(minimum=1, const=1209600),
                "model_input_tokens": _integer(minimum=1),
                "model_output_tokens": _integer(minimum=1),
                "model_turns": _string(const="unbounded"),
                "cpu_seconds": _integer(minimum=1),
                "external_launches": _integer(minimum=1),
            }),
            "recovery": _closed_object({
                "startup_attempts_per_generation": _integer(minimum=1),
                "provider_attempts_per_request": _integer(minimum=1),
                "repair_attempts_per_failure_identity": _integer(minimum=1),
                "generation_replacements_per_work_item": _integer(minimum=1, const=60),
                "backoff_initial_seconds": _integer(minimum=1, const=60),
                "backoff_max_seconds": _integer(minimum=1, const=3600),
                "backoff_multiplier": _integer(minimum=1, const=2),
                "backoff_jitter_ratio": {"type":"number","minimum":0,"maximum":0.2},
                "retry_after_precedence": _string(const="provider_retry_after_then_exponential"),
                "breaker_failure_classes": _array(_string(), min_items=1, unique=True),
                "breaker_scope": _string(const="provider"),
                "breaker_failure_threshold": _integer(minimum=1, const=3),
                "breaker_cooldown_seconds": _integer(minimum=1, const=1800),
            }),
        })
        properties["generation_lineage"] = _closed_object({
            "replacement_ordinal": _integer(minimum=0, maximum=60),
            "replacement_cap": _integer(minimum=1, const=60),
            "previous_generation_id": {"type":["string","null"]},
        })
    schema_id = _schema_id(program_kind, "claim-card")
    schema_id = schema_id.removesuffix("-1.0.json") + "-1.1.json"
    return _schema_root(schema_id, properties)


def _master_acceptance_schema(program_kind: str) -> dict[str, Any]:
    master = _closed_object(
        {
            "principal_id": _safe_id(),
            "decision_id": _safe_id(),
            "authentication_sha256": _sha256(),
        }
    )
    handoff = _closed_object(
        {
            "claim_id": _safe_id(),
            "run_id": _safe_id(),
            "claim_card_sha256": _sha256(),
            "worker_result_sha256": _sha256(),
            "baseline_sha256": _sha256(),
            "patch_sha256": _sha256(),
            "immutable_archive_path": _path(),
            "immutable_archive_sha256": _sha256(),
        }
    )
    review_decision = _closed_object(
        {
            "reviewer_id": _safe_id(),
            "decision": _string(const="accepted"),
            "decision_receipt_path": _path(),
            "decision_receipt_sha256": _sha256(),
        }
    )
    integrated_file = _closed_object(
        {
            "path": _path(),
            "sha256": _sha256(),
            "size_bytes": _integer(minimum=0),
        }
    )
    integration = _closed_object(
        {
            "pre_tree_sha256": _sha256(),
            "post_tree_sha256": _sha256(),
            "integrated_bytes_sha256": _sha256(),
            "integrated_files": _array(integrated_file, min_items=1, unique=True),
        }
    )
    validation_gate = _closed_object(
        {
            "gate_id": _safe_id(),
            "command_sha256": _sha256(),
            "exit_code": _integer(minimum=0, const=0),
            "passed": _boolean(const=True),
            "stdout_sha256": _sha256(),
            "stderr_sha256": _sha256(),
        }
    )
    transition = _closed_object(
        {
            "from": _string(const="handoff_waiting_master"),
            "to": _string(const="master_accepted"),
            "pre_blueprint_sha256": _sha256(),
            "post_blueprint_sha256": _sha256(),
            "post_gantt_sha256": _sha256(),
        }
    )
    properties = {
            "schema_version": _string(
                const="awesome-theorems/stage5-proof-debt-master-acceptance/1.0"
            ),
            "program": _string(),
            "item_id": _safe_id(),
            "mode": _mode(),
            "master": master,
            "handoff": handoff,
            "review_decisions": _array(
                review_decision, min_items=1, unique=True
            ),
            "integration": integration,
            "validation_gates": _array(
                validation_gate, min_items=1, unique=True
            ),
            "state_transition": transition,
            "accepted_at": _instant(),
            "authority_sha256": _sha256(),
        }
    if program_kind == "conjecture":
        properties["workset_member"] = _conjecture_workset_member()
        properties["accepted_outcome"] = _conjecture_typed_outcome()
    return _schema_root(
        _schema_id(program_kind, "master-acceptance"),
        properties,
    )


def _build_contracts() -> dict[str, dict[str, dict[str, Any]]]:
    result: dict[str, dict[str, dict[str, Any]]] = {}
    for program_kind in sorted(BOOT_PROGRAM_KINDS):
        worker = _worker_result_schema(program_kind)
        worker_digest = _sha256_bytes(canonical_json_bytes(worker))
        result[program_kind] = {
            "claim-card.schema.json": _claim_card_schema(
                program_kind, worker_digest
            ),
            "worker-result.schema.json": worker,
            "master-acceptance.schema.json": _master_acceptance_schema(
                program_kind
            ),
        }
    return result


_CONTRACTS = _build_contracts()
_BUILT_SCHEMA_SHA256 = {
    program_kind: {
        filename: _sha256_bytes(canonical_json_bytes(schema))
        for filename, schema in schemas.items()
    }
    for program_kind, schemas in _CONTRACTS.items()
}

# These literals are a review surface, not values trusted from candidate BOOT
# artifacts.  A source edit that changes a schema must update the digest in the
# same reviewed manager migration.
BOOT_SCHEMA_SHA256 = MappingProxyType(
    {
        "conjecture": MappingProxyType(
            {
                "claim-card.schema.json": "ab37e7ef931c5ea2c842246f932fe7319158b82351c3f7d3ed9e61621919303d",
                "worker-result.schema.json": "c84eb15d048fc783432c1db562882bcae88fdc154b8518cbe9776b32cb023fcc",
                "master-acceptance.schema.json": "1ae41547b6c05a997cc38a22aedca36e6164f0c785c15e1ca2276233522adf11",
            }
        ),
        "theorem": MappingProxyType(
            {
                "claim-card.schema.json": "a6cd5cc5d21d9933ecc322119dec8d6e22c824e0205b4e24eb960c33dde575ae",
                "worker-result.schema.json": "ceaba4fa8819c84a2507223a7126651e0f9728a3a6a94cd5eacbb88a151036c4",
                "master-acceptance.schema.json": "fddfee017babbc7320907769277c1300fa78cc65c5391a85e3c711559f363b6b",
            }
        ),
    }
)


def _assert_recursively_closed(schema: dict[str, Any], path: str = "$") -> None:
    if not schema:
        raise RuntimeError(f"empty schema at {path}")
    if "oneOf" in schema:
        if set(schema) != {"oneOf"} or not isinstance(schema["oneOf"], list) or len(schema["oneOf"]) < 2:
            raise RuntimeError(f"malformed closed union at {path}")
        for index, branch in enumerate(schema["oneOf"]):
            if not isinstance(branch, dict):
                raise RuntimeError(f"union branch is not an object at {path}[{index}]")
            _assert_recursively_closed(branch, f"{path}.oneOf[{index}]")
        return
    type_value = schema.get("type")
    if not isinstance(type_value, (str, list)):
        raise RuntimeError(f"schema lacks an explicit type at {path}")
    if isinstance(type_value, list):
        if set(type_value) != {"string", "null"}:
            raise RuntimeError(f"unsupported union schema at {path}")
        return
    if type_value == "object":
        if schema.get("additionalProperties") is not False:
            raise RuntimeError(f"object schema is open at {path}")
        properties = schema.get("properties")
        required = schema.get("required")
        if not isinstance(properties, dict) or not properties:
            raise RuntimeError(f"object schema has no properties at {path}")
        if not isinstance(required, list) or required != list(properties):
            raise RuntimeError(f"object schema required fields drift at {path}")
        for name, child in properties.items():
            if not isinstance(child, dict):
                raise RuntimeError(f"property schema is not an object at {path}.{name}")
            _assert_recursively_closed(child, f"{path}.{name}")
    elif type_value == "array":
        items = schema.get("items")
        if not isinstance(items, dict):
            raise RuntimeError(f"array item schema is missing at {path}")
        _assert_recursively_closed(items, f"{path}[]")
    elif type_value not in {"string", "integer", "boolean", "number"}:
        raise RuntimeError(f"unsupported schema type {type_value!r} at {path}")


for _program_contracts in _CONTRACTS.values():
    for _contract in _program_contracts.values():
        if set(_contract) != {
            "$schema", "$id", "type", "additionalProperties", "required", "properties"
        }:
            raise RuntimeError("BOOT schema root fields drifted")
        _assert_recursively_closed(_contract)


def _validated_selector(program_kind: str, schema_filename: str) -> tuple[str, str]:
    if program_kind not in BOOT_PROGRAM_KINDS:
        raise BootSchemaContractError(
            f"unknown BOOT program kind {program_kind!r}; expected theorem or conjecture"
        )
    if schema_filename not in BOOT_SCHEMA_FILENAMES:
        raise BootSchemaContractError(
            f"unknown BOOT schema filename {schema_filename!r}"
        )
    return program_kind, schema_filename


def _verify_frozen_digests() -> None:
    observed = {
        kind: dict(rows) for kind, rows in BOOT_SCHEMA_SHA256.items()
    }
    if observed != _BUILT_SCHEMA_SHA256:
        raise RuntimeError(
            "stage5 BOOT schema source and frozen SHA-256 table differ"
        )


def expected_boot_schema(program_kind: str, schema_filename: str) -> dict[str, Any]:
    """Return an independent copy of one exact reviewed schema document."""

    kind, filename = _validated_selector(program_kind, schema_filename)
    _verify_frozen_digests()
    return deepcopy(_CONTRACTS[kind][filename])


def expected_boot_schema_bytes(program_kind: str, schema_filename: str) -> bytes:
    """Return the canonical bytes that determine the accepted schema digest."""

    return canonical_json_bytes(expected_boot_schema(program_kind, schema_filename))


def expected_boot_schema_sha256(program_kind: str, schema_filename: str) -> str:
    """Return the frozen canonical SHA-256 for one schema."""

    kind, filename = _validated_selector(program_kind, schema_filename)
    _verify_frozen_digests()
    return BOOT_SCHEMA_SHA256[kind][filename]


def _json_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, str):
        return "string"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _first_difference(expected: Any, observed: Any, path: str = "$") -> str:
    expected_type = _json_type(expected)
    observed_type = _json_type(observed)
    if expected_type != observed_type:
        return f"{path}: expected {expected_type}, observed {observed_type}"
    if isinstance(expected, dict):
        expected_keys = set(expected)
        observed_keys = set(observed)
        missing = sorted(expected_keys - observed_keys)
        extra = sorted(observed_keys - expected_keys)
        if missing or extra:
            return f"{path}: missing keys={missing}, extra keys={extra}"
        for key in sorted(expected):
            if expected[key] != observed[key]:
                return _first_difference(expected[key], observed[key], f"{path}.{key}")
    elif isinstance(expected, list):
        if len(expected) != len(observed):
            return f"{path}: expected {len(expected)} entries, observed {len(observed)}"
        for index, (expected_item, observed_item) in enumerate(zip(expected, observed)):
            if expected_item != observed_item:
                return _first_difference(
                    expected_item, observed_item, f"{path}[{index}]"
                )
    elif expected != observed:
        return f"{path}: expected {expected!r}, observed {observed!r}"
    return f"{path}: canonical JSON bytes differ"


def validate_boot_schema_document(
    document: Any, *, program_kind: str, schema_filename: str
) -> str:
    """Validate one parsed schema and return its frozen canonical SHA-256.

    Equality is canonical-byte equality rather than Python's loose value
    equality, so JSON ``false`` cannot be substituted by numeric ``0``.
    """

    kind, filename = _validated_selector(program_kind, schema_filename)
    expected = expected_boot_schema(kind, filename)
    if not isinstance(document, dict):
        raise BootSchemaContractError(
            f"{filename}: schema document must be a JSON object"
        )
    try:
        observed_bytes = canonical_json_bytes(document)
    except (TypeError, ValueError) as exc:
        raise BootSchemaContractError(
            f"{filename}: schema document is not strict finite JSON"
        ) from exc
    expected_bytes = canonical_json_bytes(expected)
    if observed_bytes != expected_bytes:
        detail = _first_difference(expected, document)
        raise BootSchemaContractError(
            f"{filename}: schema differs from the exact {kind} BOOT contract; {detail}"
        )
    digest = _sha256_bytes(observed_bytes)
    if digest != BOOT_SCHEMA_SHA256[kind][filename]:
        raise BootSchemaContractError(f"{filename}: frozen schema digest mismatch")
    return digest


def _strict_json_loads(raw: bytes | str, label: str) -> Any:
    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise BootSchemaContractError(
                    f"{label}: duplicate JSON key {key!r}"
                )
            result[key] = value
        return result

    def reject_constant(value: str) -> Any:
        raise BootSchemaContractError(
            f"{label}: non-finite JSON number {value}"
        )

    if isinstance(raw, bytes):
        try:
            raw = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise BootSchemaContractError(f"{label}: invalid UTF-8 JSON") from exc
    try:
        return json.loads(
            raw,
            object_pairs_hook=pairs_hook,
            parse_constant=reject_constant,
        )
    except BootSchemaContractError:
        raise
    except (TypeError, json.JSONDecodeError) as exc:
        raise BootSchemaContractError(f"{label}: invalid strict JSON") from exc


def validate_boot_schema_bytes(
    raw: bytes | str, *, program_kind: str, schema_filename: str
) -> str:
    """Strictly parse and validate one candidate schema byte string."""

    document = _strict_json_loads(raw, schema_filename)
    return validate_boot_schema_document(
        document, program_kind=program_kind, schema_filename=schema_filename
    )


def validate_boot_schema_set(
    documents: Mapping[str, Any], *, program_kind: str
) -> dict[str, str]:
    """Validate the exact three-file BOOT schema set."""

    _validated_selector(program_kind, BOOT_SCHEMA_FILENAMES[0])
    observed_names = set(documents)
    expected_names = set(BOOT_SCHEMA_FILENAMES)
    if observed_names != expected_names:
        raise BootSchemaContractError(
            "BOOT schema set differs; "
            f"missing={sorted(expected_names - observed_names)}, "
            f"extra={sorted(observed_names - expected_names)}"
        )
    return {
        filename: validate_boot_schema_document(
            documents[filename],
            program_kind=program_kind,
            schema_filename=filename,
        )
        for filename in BOOT_SCHEMA_FILENAMES
    }


__all__ = [
    "BOOT_PROGRAM_KINDS",
    "BOOT_SCHEMA_FILENAMES",
    "BOOT_SCHEMA_SHA256",
    "BootSchemaContractError",
    "canonical_json_bytes",
    "expected_boot_schema",
    "expected_boot_schema_bytes",
    "expected_boot_schema_sha256",
    "validate_boot_schema_bytes",
    "validate_boot_schema_document",
    "validate_boot_schema_set",
]
