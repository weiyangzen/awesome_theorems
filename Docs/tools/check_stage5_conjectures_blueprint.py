#!/usr/bin/env python3
"""Validate and materialise the Stage5 conjecture BOOT authorities.

The canonical Blueprint manager owns checklist state.  This ongoing checker is
deliberately read-only during ordinary operation; ``--materialize-boot-data``
is the one deterministic preparer used before the signed BOOT handoff.  It
derives the closed workset, provider/profile registries and execution schemas
from the pinned strict-conjecture inventory, non-credit-bearing occurrence pool,
and current manager spec.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from typing import Any
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[2]
BLUEPRINT = ROOT / "Docs/Stage5_Conjectures_Blueprint.md"
GANTT = ROOT / "Docs/Stage5_Conjectures_Gantt.md"
EVIDENCE = ROOT / "Docs/evidence/stage5_conjectures"
MANAGER = ROOT / "Docs/tools/manage_stage5_proof_debt_blueprints.py"
SCHEMA_CONTRACT = ROOT / "scripts/stage5_boot_schema_contract.py"
PROGRAM = "stage5-conjecture-proof-debt/2.0"
BLUEPRINT_SCHEMA = "awesome-theorems/stage5-conjectures-blueprint/2.0"
TRANSPORT = "tmux_codex_tui"
GOAL_COMMAND = "/goal"
MODEL = "gpt-5.6-sol"
EFFORT = "ultra"
SERVICE_TIER = "default"
PROVIDER = "sub2api"
WORKSET = EVIDENCE / "workset-5.6.json"
WORKSET_RECEIPT = EVIDENCE / "workset-5.6-receipt.json"
EXECUTION_SPEC = EVIDENCE / "execution-spec.json"
FOUNDATION_PROFILES = EVIDENCE / "foundation-profiles.json"
PROVIDER_REGISTRY = EVIDENCE / "provider-registry.json"


class CheckError(RuntimeError):
    pass


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise CheckError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def manager() -> Any:
    return load_module(MANAGER, "stage5_conjecture_manager_for_checker")


@lru_cache(maxsize=1)
def schema_contract() -> Any:
    return load_module(SCHEMA_CONTRACT, "stage5_conjecture_schema_contract")


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode()
    except (TypeError, ValueError) as exc:
        raise CheckError("value is not canonical finite JSON") from exc


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest_file(path: Path) -> str:
    return digest(path.read_bytes())


def strict_json(raw: bytes, label: str) -> Any:
    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise CheckError(f"{label}: duplicate JSON key {key!r}")
            result[key] = value
        return result
    def reject(value: str) -> Any:
        raise CheckError(f"{label}: non-finite JSON number {value}")
    try:
        return json.loads(raw, object_pairs_hook=pairs_hook, parse_constant=reject)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CheckError(f"{label}: invalid strict UTF-8 JSON") from exc


def sealed(body: dict[str, Any]) -> dict[str, Any]:
    result = dict(body)
    result["authority_sha256"] = digest(canonical(body))
    return result


def verify_seal(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not isinstance(value.get("authority_sha256"), str):
        raise CheckError(f"{label}: malformed authority seal")
    body = dict(value)
    authority = body.pop("authority_sha256")
    if digest(canonical(body)) != authority:
        raise CheckError(f"{label}: authority seal mismatch")
    return value


def parse_blueprint(path: Path | None = None) -> tuple[dict[str, Any], list[dict[str, Any]], bytes]:
    m = manager()
    expected = m.expected_tasks(m.CONJECTURE)
    source_path = BLUEPRINT if path is None else path
    raw = source_path.read_bytes()
    # Once BOOT has been accepted, this ongoing checker is the authority for
    # mutable TARGET cursors.  Keep the manager's immutable row/DAG checks but
    # explicitly admit the authenticated progress cursor instead of applying
    # the one-time pristine-bootstrap rule to every later tick.
    tasks = m.parse_blueprint(
        m.CONJECTURE, raw, expected,
        allow_progress_cursor=True,
        allow_superseded_authority_for_invalidation=True,
        allow_immutable_row_drift=False,
    )
    if any(
        (task.item_id, task.title, task.dependencies, task.owned_paths, task.gate)
        != (template.item_id, template.title, template.dependencies, template.owned_paths, template.gate)
        for task, template in zip(tasks, expected)
    ):
        raise CheckError("immutable conjecture checklist row differs from generated authority")
    text = raw.decode("utf-8")
    block = text.split(m.SPEC_BEGIN, 1)[1].split(m.SPEC_END, 1)[0].strip()
    if not block.startswith("```json\n") or not block.endswith("\n```"):
        raise CheckError("execution specification fence differs")
    observed = strict_json(block[8:-4].encode(), "execution specification")
    spec = m.spec_object(m.CONJECTURE)
    if observed != spec:
        raise CheckError("embedded conjecture execution specification is stale")
    validate_spec(spec)
    rows = [{"item_id": t.item_id, "state": t.state, "title": t.title,
             "dependencies": list(t.dependencies), "owned_paths": list(t.owned_paths),
             "gate": t.gate} for t in tasks]
    target_rows = [row for row in rows if row["item_id"].endswith("-TARGET")]
    intake_rows = [row for row in rows if row["item_id"].startswith("S5CON-POOL-") and row["item_id"].endswith("-INTAKE")]
    common_clauses = (
        ("task-local tmux server/socket/session", "one task-local tmux"),
        ("private writable CODEX_HOME",),
        ("thread",),
        ("exactly one submitted /goal", "exactly one active /goal"),
        ("may never claim another mathematical ID", "or claim another mathematical ID", "no worker may claim another mathematical ID"),
        ("no generation may inspect another task root",),
    )
    resolution_clauses = (
        ("durable registry of genuinely distinct mathematical approach families",),
        ("mark theorem-equivalent missing-lemma routes blocked",),
        ("adversarially audit every candidate",),
        ("Finite checks, special cases, reductions, failed routes and polished summaries remain unfinished",),
    )
    for row in target_rows:
        for alternatives in common_clauses + resolution_clauses:
            if not any(clause in row["gate"] for clause in alternatives):
                raise CheckError(f"{row['item_id']}: worker bijection clause missing: {alternatives[0]}")
    intake_clauses = (
        ("source occurrence is not a strict conjecture credit",),
        ("FULL-CATALOG-IDENTITY",),
        ("separately reviewed append-only Stage5/Stage6 migration",),
        ("intake x means adjudication complete, never conjecture proved/refuted",),
    )
    for row in intake_rows:
        for alternatives in common_clauses + intake_clauses:
            if not any(clause in row["gate"] for clause in alternatives):
                raise CheckError(f"{row['item_id']}: worker bijection clause missing: {alternatives[0]}")
    return spec, rows, raw


def validate_spec(spec: dict[str, Any]) -> None:
    required = {
        "schema_version": "awesome-theorems/stage5-proof-debt-execution-spec/2.0",
        "program": PROGRAM, "blueprint_schema": BLUEPRINT_SCHEMA,
        "authoritative_blueprint": "Docs/Stage5_Conjectures_Blueprint.md",
        "gantt_projection": "Docs/Stage5_Conjectures_Gantt.md",
        "runtime_root": ".ops/stage5-conjectures-execution-v2",
        "shared_runtime_root": None, "worker_transport": TRANSPORT,
        "goal_command": GOAL_COMMAND,
    }
    for key, expected in required.items():
        if spec.get(key) != expected:
            raise CheckError(f"execution specification {key} differs")
    route = spec.get("route_policy", {})
    if {key: route.get(key) for key in ("provider", "model", "reasoning_effort", "service_tier")} != {
        "provider": PROVIDER, "model": MODEL,
        "reasoning_effort": EFFORT, "service_tier": SERVICE_TIER,
    }:
        raise CheckError("frozen Codex route differs")
    if "default_limits" in spec or "default_host_headroom" in spec:
        raise CheckError("concurrency defaults are forbidden; use an explicit operator prompt")
    contract = spec.get("concurrency_prompt_contract")
    required_dimensions = {
        "logical_claims", "service_records", "agent_executions", "startup_reservations",
        "launch_fanout_per_wave", "live_transports", "authenticated_goals", "running_turns",
        "outbound_request_starts_per_window", "in_flight_requests", "integration", "validators",
        "exact_path_conflicts",
    }
    if not isinstance(contract, dict) or set(contract.get("required_dimensions", [])) != required_dimensions:
        raise CheckError("complete prompt concurrency dimension contract is missing")
    if contract.get("value_source") != "explicit_execution_prompt_only" or contract.get("missing_policy") != "fail_closed_before_materialization_or_launch":
        raise CheckError("prompt must be explicit and fail closed before side effects")
    coordination = spec.get("coordination_authority", {})
    if "caps" in coordination or coordination.get("concurrency_prompt_contract") != contract:
        raise CheckError("program-local coordination must bind the prompt contract, not frozen caps")
    if spec.get("shared_runtime_root") is not None or "shared_coordination" in spec:
        raise CheckError("conjecture contains shared runtime authority")
    if coordination.get("root") != ".ops/stage5-conjectures-execution-v2/epochs/stage5-conjecture-occurrence-pool-v2":
        raise CheckError("conjecture coordination root differs")
    if "no combined total" not in str(spec.get("program_coordination", {}).get("no_cross_program_pool", "")):
        raise CheckError("cross-program capacity prohibition is missing")
    forbidden = set(spec.get("forbidden_transports", []))
    expected_forbidden = {"codex_app_server", "app_server_json_rpc", "codex_exec", "shared_codex_daemon", "shared_tmux_server", "shared_writable_CODEX_HOME", "no_tmux_codex", "docker_worker_transport", "container_worker_transport"}
    if forbidden != expected_forbidden:
        raise CheckError("forbidden transport set differs")
    if spec.get("worker_runtime_boundary", {}).get("worker_container_transport") != "forbidden":
        raise CheckError("Docker/container worker transport is not forbidden")
    m = manager()
    intake = spec.get("conjecture_occurrence_intake_contract")
    if (
        not isinstance(intake, dict)
        or intake.get("source_occurrence_denominator") != m.CONJECTURE_POOL_COUNT
        or intake.get("target_item_range") != ["S5CON-POOL-00000001-INTAKE", "S5CON-POOL-00014865-INTAKE"]
        or intake.get("pool_id_range") != ["S5POOL-00000001", "S5POOL-00014865"]
        or intake.get("authority") != m.CONJECTURE_POOL_MANIFEST.relative_to(ROOT).as_posix()
        or "do not attempt a proof" not in intake.get("short_goal_clause", "")
        or "never" not in intake.get("completion_rule", "")
        or "append-only Stage5 catalog and Stage6 alias migration" not in intake.get("promotion_rule", "")
    ):
        raise CheckError("conjecture occurrence intake contract differs")
    bundle = spec.get("source_bundle", {}).get("bindings", {})
    if (
        bundle.get("conjecture_pool_manifest_sha256") != m.CONJECTURE_POOL_MANIFEST_SHA256
        or bundle.get("conjecture_pool_occurrences_sha256") != m.CONJECTURE_POOL_OCCURRENCES_SHA256
        or bundle.get("conjecture_pool_identity_registry_sha256") != m.CONJECTURE_POOL_IDENTITIES_SHA256
        or bundle.get("conjecture_pool_source_occurrence_count") != m.CONJECTURE_POOL_COUNT
        or "no strict credit" not in bundle.get("conjecture_pool_semantic_boundary", "")
    ):
        raise CheckError("conjecture source-occurrence bundle differs")
    proof_search = spec.get("conjecture_proof_search_prompt")
    if proof_search != m.conjecture_proof_search_prompt_contract():
        raise CheckError("conjecture proof-search prompt contract differs")
    source = proof_search.get("source", {})
    extraction = ROOT / str(source.get("extraction_path", ""))
    if (
        source.get("repository") != m.CROUZEIX_PROMPT_REPOSITORY
        or source.get("commit") != m.CROUZEIX_PROMPT_COMMIT
        or source.get("blob_sha1") != m.CROUZEIX_PROMPT_BLOB_SHA1
        or source.get("file_sha256") != m.CROUZEIX_PROMPT_SHA256
        or not extraction.is_file() or extraction.is_symlink()
        or digest_file(extraction) != source.get("extraction_sha256")
    ):
        raise CheckError("pinned Crouzeix prompt/extraction binding differs")
    adaptation = proof_search.get("execution_adaptation", {})
    if (
        proof_search.get("resolution_roots") != ["Claim", "Not Claim"]
        or adaptation.get("upstream_multiagent_shape") != "not imported"
        or {adaptation.get(key) for key in ("child_agents", "collaboration_tools", "hidden_concurrency")} != {"forbidden"}
        or proof_search.get("approach_registry", {}).get("required") is not True
        or set(proof_search.get("approach_registry", {}).get("state_enum", [])) != {"live", "blocked", "refuted", "merged"}
        or "comparable in strength" not in proof_search.get("blocked_route_policy", "")
        or "exact-polarity" not in proof_search.get("completion_rule", "")
        or "TARGET unresolved" not in proof_search.get("unfinished_rule", "")
    ):
        raise CheckError("conjecture proof-search semantics differ")


def _task_authority(row: dict[str, Any]) -> str:
    m = manager()
    return m.sha256_bytes(m.canonical({"item_id": row["item_id"], "title": row["title"],
                                      "dependencies": row["dependencies"], "owned_paths": row["owned_paths"], "gate": row["gate"]}))


def render_boot_data(
    *,
    parsed: tuple[dict[str, Any], list[dict[str, Any]], bytes] | None = None,
) -> dict[Path, bytes]:
    """Return deterministic BOOT artifacts without mutating the workspace."""
    spec, rows, blueprint_raw = parse_blueprint() if parsed is None else parsed
    m = manager()
    joined = m.strict_inventory()
    occurrences = m.conjecture_occurrence_inventory()
    if (
        len(joined) != m.CONJECTURE_STRICT_TARGET_COUNT
        or len(occurrences) != m.CONJECTURE_POOL_COUNT
        or sum(row["item_id"].endswith("-TARGET") for row in rows) != m.CONJECTURE_STRICT_TARGET_COUNT
        or sum(row["item_id"].startswith("S5CON-POOL-") and row["item_id"].endswith("-INTAKE") for row in rows) != m.CONJECTURE_POOL_COUNT
    ):
        raise CheckError("conjecture inventory/cardinality differs")
    if len(rows) != len(m.expected_tasks(m.CONJECTURE)):
        raise CheckError("conjecture checklist cardinality differs")
    by_item = {row["item_id"]: row for row in rows}
    aliases = m.stage6_aliases()
    members: list[dict[str, Any]] = []
    profiles: list[dict[str, Any]] = []
    for entry in joined:
        record = entry["record"]
        stage_id = record["stage_claim_id"]
        target = f"S5CON-{m.claim_number(stage_id)}-TARGET"
        if target not in by_item:
            raise CheckError(f"{stage_id}: TARGET missing")
        alias = aliases[stage_id]
        formal = record.get("formal_statement") if isinstance(record.get("formal_statement"), dict) else {}
        member = {
            "member_id": stage_id, "member_kind": "strict_resolution",
            "stage_claim_id": stage_id, "pool_id": None, "variant_id": record.get("variant_id"),
            "family_id": record.get("family_id"), "stage6_alias": alias,
            "cohort": m.conjecture_cohort(entry), "provider_id": "formal-conjectures-2270d31e",
            "record_sha256": digest(canonical(record)),
            "semantic_payload_sha256": record.get("semantic_payload_sha256"),
            "statement_sha256": record.get("statement_sha256"),
            "formal_type_sha256": record.get("formal_type_sha256"),
            "display_name": record.get("display_name"), "qualified_name": record.get("qualified_name"),
            "module": record.get("module"), "source_id": record.get("source_id"),
            "source_locator": record.get("locator") or formal.get("locator"),
            "formal_statement": formal, "target_item_id": target,
            "strict_credit": True, "independent_current_open_verified": None,
            "execution_admission": "strict_resolution",
            "target_task_authority_sha256": _task_authority(by_item[target]),
            "internal_subchecklist": ["INTAKE", "STATEMENT", "STATUS", "FRONTIER", "EXPLORE", "RESOLUTION", "HUMAN", "LEAN", "READABLE", "VALIDATE", "RELEASE"],
            "worker_bijection": "one conjecture, one TARGET, one task-local tmux, one private CODEX_HOME, one thread, one active /goal",
        }
        member["workset_record_sha256"] = digest(canonical({
            "member_kind": member["member_kind"],
            "record_sha256": member["record_sha256"],
            "target_item_id": member["target_item_id"],
            "target_task_authority_sha256": member["target_task_authority_sha256"],
        }))
        members.append(member)
        axioms = formal.get("axioms", []) if isinstance(formal.get("axioms"), list) else []
        profile_body = {"stage_claim_id": stage_id, "profile_version": 1,
                        "status": "boot_baseline_requires_exact_per_declaration_replay_before_acceptance",
                        "lean_toolchain_sha256": digest_file(ROOT / "Formalizations/Lean/lean-toolchain"),
                        "provider_id": "formal-conjectures-2270d31e", "allowed_transitive_axiom_names": sorted(set(axioms) - {"sorryAx"}),
                        "allowed_bodyless_foundation_declarations": [], "per_name_justifications": {}}
        profile = sealed(profile_body); profiles.append(profile)
    for occurrence in occurrences:
        pool_id = occurrence["pool_id"]
        target = f"S5CON-POOL-{pool_id.removeprefix('S5POOL-')}-INTAKE"
        if target not in by_item:
            raise CheckError(f"{pool_id}: intake TARGET missing")
        member = {
            "member_id": pool_id, "member_kind": "source_occurrence_intake",
            "stage_claim_id": None, "pool_id": pool_id, "stage6_alias": None,
            "stable_source_key": occurrence.get("stable_source_key"),
            "source_native_id": occurrence.get("source_native_id"),
            "source_kind": occurrence.get("kind"), "source_status": occurrence.get("source_status"),
            "statement_presence": occurrence.get("statement_presence"),
            "record_path": occurrence.get("record_path"),
            "record_sha256": occurrence.get("canonical_record_sha256"),
            "occurrence_authority_sha256": occurrence.get("authority_sha256"),
            "cohort": m.conjecture_occurrence_cohort(occurrence),
            "provider_id": "conjecturebench-357bcb1a",
            "strict_credit": False, "independent_current_open_verified": False,
            "execution_admission": occurrence.get("execution_admission"),
            "target_item_id": target,
            "target_task_authority_sha256": _task_authority(by_item[target]),
            "internal_subchecklist": ["INTAKE", "STATEMENT-EXACTIFICATION", "STATUS", "RIGHTS", "IMPORTANCE", "FULL-CATALOG-IDENTITY", "ADJUDICATION"],
            "worker_bijection": "one source occurrence, one intake TARGET, one task-local tmux, one private CODEX_HOME, one thread, one active /goal",
        }
        member["workset_record_sha256"] = digest(canonical({
            "member_kind": member["member_kind"],
            "record_sha256": member["record_sha256"],
            "target_item_id": member["target_item_id"],
            "target_task_authority_sha256": member["target_task_authority_sha256"],
        }))
        members.append(member)
    ids = [x["member_id"] for x in members]
    workset = sealed({"schema_version": "awesome-theorems/stage5-conjecture-workset/1.0", "program": PROGRAM,
                      "base_release": "5.6", "target_count": m.CONJECTURE_TOTAL_TARGET_COUNT,
                      "strict_resolution_target_count": m.CONJECTURE_STRICT_TARGET_COUNT,
                      "source_occurrence_intake_target_count": m.CONJECTURE_POOL_COUNT,
                      "task_count": len(rows),
                      "strict_source_path": "Docs/catalog/v5/releases/5.6/Strict_Conjecture_Ledger.json",
                      "strict_source_sha256": m.STRICT_SOURCE_SHA256, "strict_source_authority_sha256": m.STRICT_AUTHORITY_SHA256,
                      "occurrence_source_path": m.CONJECTURE_POOL_OCCURRENCES.relative_to(ROOT).as_posix(),
                      "occurrence_source_sha256": m.CONJECTURE_POOL_OCCURRENCES_SHA256,
                      "occurrence_manifest_sha256": m.CONJECTURE_POOL_MANIFEST_SHA256,
                      "occurrence_identity_registry_sha256": m.CONJECTURE_POOL_IDENTITIES_SHA256,
                      "semantic_boundary": "1425 strict resolution identities plus 14865 non-credit-bearing source-occurrence intake targets; occurrence intake x is adjudication only",
                      "stage6_registry_path": m.STAGE6_REGISTRY.relative_to(ROOT).as_posix(),
                      "stage6_registry_sha256": m.STAGE6_REGISTRY_SHA256, "stage6_registry_authority_sha256": m.STAGE6_REGISTRY_AUTHORITY_SHA256,
                      "member_id_set_sha256": digest(canonical(sorted(ids))), "member_record_set_sha256": digest(canonical(sorted(x["workset_record_sha256"] for x in members))),
                      "checklist_dag_sha256": digest(canonical([{"item_id": x["item_id"], "dependencies": x["dependencies"], "owned_paths": x["owned_paths"], "task_authority_sha256": _task_authority(x)} for x in rows])),
                      "members": members})
    workset_raw = json.dumps(workset, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
    provider = sealed({"schema_version": "awesome-theorems/stage5-provider-registry/1.0", "program": PROGRAM, "providers": [
        {"provider_id": "mathlib-8a178386", "kind": "pinned_lean_provider", "revision": "8a178386ffc0f5fef0b77738bb5449d50efeea95", "source_registry_id": "SRC-MATH-V5-MATHLIB-8A178386", "trust": "Lean4 kernel replay at trust=0 plus exact declaration body/dependency/axiom audit"},
        {"provider_id": "formal-conjectures-2270d31e", "kind": "pinned_statement_provider_not_proof_authority", "revision": "2270d31e8dd611521f979de6d86da364930b7669", "source_registry_id": "SRC-MATH-V5-FORMAL-CONJECTURES-2270D31E", "trust": "exact statement/source bytes only; sorryAx and source claims provide no proof closure"},
        {"provider_id": "conjecturebench-357bcb1a", "kind": "pinned_source_occurrence_provider_not_status_identity_or_proof_authority", "revision": m.CONJECTURE_POOL_SOURCE_COMMIT, "source_registry_id": "SRC-MATH-V5-CONJECTUREBENCH-357BCB1A", "trust": "exact source record/status observation/rights metadata only; inclusion is not independent current-open, semantic-identity or proof evidence"},
    ]})
    provider_raw = json.dumps(provider, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
    foundation = sealed({"schema_version": "awesome-theorems/stage5-foundation-profile-registry/1.0", "program": PROGRAM, "profile_count": len(profiles), "provider_registry_sha256": digest(provider_raw), "profiles": profiles})
    foundation_raw = json.dumps(foundation, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
    receipt = sealed({"schema_version": "awesome-theorems/stage5-conjecture-workset-receipt/1.1", "program": PROGRAM,
                      "workset_path": WORKSET.relative_to(ROOT).as_posix(), "workset_sha256": digest(workset_raw),
                      "target_count": m.CONJECTURE_TOTAL_TARGET_COUNT,
                      "strict_resolution_target_count": m.CONJECTURE_STRICT_TARGET_COUNT,
                      "source_occurrence_intake_target_count": m.CONJECTURE_POOL_COUNT,
                      "member_id_set_sha256": workset["member_id_set_sha256"], "member_record_set_sha256": workset["member_record_set_sha256"],
                      # This receipt authenticates immutable execution authority,
                      # not the mutable checklist cursor.  Cursor byte digests
                      # belong exclusively to append-only transition receipts.
                      "execution_spec_sha256": digest(canonical(spec)),
                      "manager_sha256": digest_file(MANAGER), "source_bundle_sha256": spec["source_bundle"]["sha256"], "checklist_dag_sha256": workset["checklist_dag_sha256"]})
    contract = schema_contract()
    outputs = {
        WORKSET: workset_raw,
        WORKSET_RECEIPT: json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n",
        EXECUTION_SPEC: json.dumps(spec, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n",
        PROVIDER_REGISTRY: provider_raw,
        FOUNDATION_PROFILES: foundation_raw,
    }
    outputs.update({
        EVIDENCE / filename: contract.expected_boot_schema_bytes("conjecture", filename)
        for filename in contract.BOOT_SCHEMA_FILENAMES
    })
    return outputs


def materialize_boot_data() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    for path, raw in render_boot_data().items():
        path.write_bytes(raw)


def validate_boot_data(specification: dict[str, Any], rows: list[dict[str, Any]], blueprint_raw: bytes) -> dict[str, Any]:
    expected_files = [WORKSET, WORKSET_RECEIPT, EXECUTION_SPEC, FOUNDATION_PROFILES, PROVIDER_REGISTRY, *(EVIDENCE / f for f in schema_contract().BOOT_SCHEMA_FILENAMES)]
    missing = [p.relative_to(ROOT).as_posix() for p in expected_files if not p.is_file() or p.is_symlink()]
    if missing:
        raise CheckError(f"missing BOOT data files: {missing}")
    # Reconstruct the complete canonical BOOT bundle.  This is intentionally
    # byte-exact: a re-sealed workset that changes one member's strict/intake
    # class, record binding, target, or task authority must not pass merely by
    # preserving aggregate counts and self-reported set digests.
    expected_bundle = render_boot_data(
        parsed=(specification, rows, blueprint_raw)
    )
    drift = [
        path.relative_to(ROOT).as_posix()
        for path, expected_raw in expected_bundle.items()
        if path.read_bytes() != expected_raw
    ]
    if drift:
        raise CheckError(f"BOOT data differs from exact reconstructed authority: {drift}")
    observed = strict_json(EXECUTION_SPEC.read_bytes(), "execution-spec.json")
    if observed != specification:
        raise CheckError("execution-spec.json differs from embedded specification")
    workset = verify_seal(strict_json(WORKSET.read_bytes(), "workset"), "workset")
    receipt = verify_seal(strict_json(WORKSET_RECEIPT.read_bytes(), "workset receipt"), "workset receipt")
    provider = verify_seal(strict_json(PROVIDER_REGISTRY.read_bytes(), "provider registry"), "provider registry")
    profiles = verify_seal(strict_json(FOUNDATION_PROFILES.read_bytes(), "foundation profiles"), "foundation profiles")
    members = workset.get("members")
    m = manager()
    if not isinstance(members, list) or len(members) != m.CONJECTURE_TOTAL_TARGET_COUNT or workset.get("target_count") != m.CONJECTURE_TOTAL_TARGET_COUNT:
        raise CheckError("workset target cardinality differs")
    ids = [member.get("member_id") for member in members if isinstance(member, dict)]
    if len(ids) != m.CONJECTURE_TOTAL_TARGET_COUNT or len(set(ids)) != m.CONJECTURE_TOTAL_TARGET_COUNT or workset.get("member_id_set_sha256") != digest(canonical(sorted(ids))):
        raise CheckError("workset member identity/set digest differs")
    if workset.get("task_count") != len(rows):
        raise CheckError("workset task cardinality differs")
    expected_dag = digest(canonical([
        {
            "item_id": row["item_id"],
            "dependencies": row["dependencies"],
            "owned_paths": row["owned_paths"],
            "task_authority_sha256": _task_authority(row),
        }
        for row in rows
    ]))
    member_records = [member.get("workset_record_sha256") for member in members if isinstance(member, dict)]
    if (
        workset.get("checklist_dag_sha256") != expected_dag
        or workset.get("member_record_set_sha256") != digest(canonical(sorted(member_records)))
    ):
        raise CheckError("workset DAG/member-record binding differs")
    if (
        receipt.get("workset_sha256") != digest_file(WORKSET)
        or receipt.get("execution_spec_sha256") != digest(canonical(specification))
        or receipt.get("schema_version") != "awesome-theorems/stage5-conjecture-workset-receipt/1.1"
        or "blueprint_sha256" in receipt
        or receipt.get("manager_sha256") != digest_file(MANAGER)
        or receipt.get("source_bundle_sha256") != specification["source_bundle"]["sha256"]
        or receipt.get("checklist_dag_sha256") != expected_dag
        or receipt.get("member_id_set_sha256") != workset.get("member_id_set_sha256")
        or receipt.get("member_record_set_sha256") != workset.get("member_record_set_sha256")
        or receipt.get("target_count") != m.CONJECTURE_TOTAL_TARGET_COUNT
        or receipt.get("strict_resolution_target_count") != m.CONJECTURE_STRICT_TARGET_COUNT
        or receipt.get("source_occurrence_intake_target_count") != m.CONJECTURE_POOL_COUNT
        or workset.get("strict_resolution_target_count") != m.CONJECTURE_STRICT_TARGET_COUNT
        or workset.get("source_occurrence_intake_target_count") != m.CONJECTURE_POOL_COUNT
        or workset.get("strict_source_sha256") != m.STRICT_SOURCE_SHA256
        or workset.get("strict_source_authority_sha256") != m.STRICT_AUTHORITY_SHA256
        or workset.get("occurrence_source_sha256") != m.CONJECTURE_POOL_OCCURRENCES_SHA256
        or workset.get("occurrence_manifest_sha256") != m.CONJECTURE_POOL_MANIFEST_SHA256
        or workset.get("occurrence_identity_registry_sha256") != m.CONJECTURE_POOL_IDENTITIES_SHA256
    ):
        raise CheckError("workset receipt binding differs")
    if provider.get("program") != PROGRAM or len(provider.get("providers", [])) != 3:
        raise CheckError("provider registry differs")
    if profiles.get("program") != PROGRAM or profiles.get("profile_count") != m.CONJECTURE_STRICT_TARGET_COUNT or len(profiles.get("profiles", [])) != m.CONJECTURE_STRICT_TARGET_COUNT:
        raise CheckError("foundation profile cardinality differs")
    contract = schema_contract()
    for filename in contract.BOOT_SCHEMA_FILENAMES:
        contract.validate_boot_schema_document(strict_json((EVIDENCE / filename).read_bytes(), filename), program_kind="conjecture", schema_filename=filename)
    return {"workset_sha256": digest_file(WORKSET), "workset_authority_sha256": workset["authority_sha256"], "execution_spec_sha256": digest(canonical(specification)), "blueprint_sha256": digest(blueprint_raw)}


def validate() -> dict[str, Any]:
    spec, rows, raw = parse_blueprint()
    validate_boot_data(spec, rows, raw)
    return {"valid": True, "program": PROGRAM, "transport": TRANSPORT, "goal_command": GOAL_COMMAND,
            "items": len(rows), "targets": manager().CONJECTURE_TOTAL_TARGET_COUNT,
            "strict_resolution_targets": manager().CONJECTURE_STRICT_TARGET_COUNT,
            "source_occurrence_intake_targets": manager().CONJECTURE_POOL_COUNT,
            "states": {"not_done": sum(r["state"] == " " for r in rows), "handoff_waiting_master": sum(r["state"] == "_" for r in rows), "master_accepted": sum(r["state"] == "x" for r in rows)}, "route": spec["route_policy"], "runtime_root": spec["runtime_root"], "blueprint_sha256": digest(raw)}


def main(argv: list[str] | None = None) -> int:
    parser = __import__("argparse").ArgumentParser(description=__doc__)
    parser.add_argument("--materialize-boot-data", action="store_true")
    parser.add_argument("--no-gantt", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.materialize_boot_data:
            materialize_boot_data()
        spec, rows, raw = parse_blueprint()
        evidence = validate_boot_data(spec, rows, raw)
        print(json.dumps({**validate(), **evidence}, ensure_ascii=False, sort_keys=True))
        return 0
    except (CheckError, OSError, ValueError, KeyError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
