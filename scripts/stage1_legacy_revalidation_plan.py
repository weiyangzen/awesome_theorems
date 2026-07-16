#!/usr/bin/env python3
"""Create a read-only, content-addressed plan for legacy Stage1 ``[_]`` items.

This tool only selects historical worker-self-tested items for future
revalidation.  It does not execute a validator, launch a worker, publish a
receipt, or change any repository state.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, NoReturn

import stage1_legacy_migration_inventory as migration


ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT_PATH = migration.BLUEPRINT_PATH
CONTRACT_PATH = migration.CONTRACT_PATH
THEOREM_DAG_PATH = "Docs/Stage1_Theorem_DAG_v2.json"
PLAN_SCHEMA = "stage1-legacy-revalidation-plan/1.0"
LANE_SCHEMA = "stage1-legacy-revalidation-lane/1.0"
MAX_SAMPLES = 50
PHASES = (
    "intake",
    "statement",
    "anchor_audit",
    "obligation_tree",
    "proof",
    "validation",
    "release",
)
PHASE_SUFFIXES = {
    "intake": "INTAKE",
    "statement": "STATEMENT",
    "anchor_audit": "ANCHOR_AUDIT",
    "obligation_tree": "OBLIGATION_TREE",
    "proof": "PROOF",
    "validation": "VALIDATION",
    "release": "RELEASE",
}
REQUIRED_STEPS = (
    "fresh_self_test",
    "new_contract_receipt",
    "new_provenance",
    "independent_review",
    "master_replay",
)
CHECKLIST_BEGIN = "<!-- STAGE1-EXECUTION-CHECKLIST:BEGIN -->"
CHECKLIST_END = "<!-- STAGE1-EXECUTION-CHECKLIST:END -->"
CHECKLIST_ROW_RE = re.compile(
    r"^- (?P<state>\[[_x ]\]) `(?P<item>S56-M-[0-9]{4}-"
    r"(?:INTAKE|STATEMENT|ANCHOR_AUDIT|OBLIGATION_TREE|PROOF|VALIDATION|RELEASE))`"
    r" / `(?P<theorem>THM-M-[0-9]{4})` / `(?P<phase>"
    + "|".join(PHASES)
    + r")`:.*?\{attempts=(?P<attempts>[0-9]+)\}$",
    re.MULTILINE,
)
THEOREM_RE = re.compile(r"^THM-M-[0-9]{4}$")


class PlanError(RuntimeError):
    """An input is not strong enough to support a trustworthy plan."""


def fail(message: str) -> NoReturn:
    raise PlanError(message)


def _embedded_digest(value: dict[str, Any], field: str, label: str) -> str:
    claimed = value.get(field)
    if not isinstance(claimed, str) or not migration.SHA256_RE.fullmatch(claimed):
        fail(f"{label} lacks a canonical {field}")
    unhashed = dict(value)
    del unhashed[field]
    actual = migration.sha256_bytes(migration.canonical_json(unhashed))
    if actual != claimed:
        fail(f"{label} {field} does not bind its content")
    return claimed


def _read_regular_file(path: Path, label: str) -> bytes:
    """Read one stable regular file and reject a symlink at the leaf."""

    absolute = Path(os.path.abspath(os.fspath(path)))
    try:
        descriptor = os.open(absolute, os.O_RDONLY | os.O_NOFOLLOW)
    except OSError as exc:
        raise PlanError(f"{label} is missing or unsafe") from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            fail(f"{label} is not a regular file")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        identity_before = (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
        )
        identity_after = (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
        )
        if identity_before != identity_after:
            fail(f"{label} changed while it was being read")
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _strict_json(data: bytes, label: str) -> dict[str, Any]:
    try:
        return migration.strict_json(data, label)
    except migration.InventoryError as exc:
        raise PlanError(str(exc)) from exc


def _parse_blueprint(blob: migration.GitBlob) -> dict[str, dict[str, Any]]:
    try:
        text = blob.data.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise PlanError("authoritative blueprint is not UTF-8") from exc
    if text.count(CHECKLIST_BEGIN) != 1 or text.count(CHECKLIST_END) != 1:
        fail("authoritative blueprint must contain exactly one execution checklist")
    begin = text.index(CHECKLIST_BEGIN) + len(CHECKLIST_BEGIN)
    end = text.index(CHECKLIST_END, begin)
    rows: dict[str, dict[str, Any]] = {}
    for match in CHECKLIST_ROW_RE.finditer(text[begin:end]):
        row = match.groupdict()
        item_id = row["item"]
        phase = row["phase"]
        theorem_id = row["theorem"]
        expected = f"S56-{theorem_id.removeprefix('THM-')}-{PHASE_SUFFIXES[phase]}"
        if item_id != expected:
            fail(f"blueprint item identity is noncanonical: {item_id}")
        if item_id in rows:
            fail(f"authoritative blueprint duplicates item {item_id}")
        rows[item_id] = {
            "item_id": item_id,
            "theorem_id": theorem_id,
            "phase": phase,
            "state": row["state"],
            "attempts": int(row["attempts"]),
        }
    if not rows:
        fail("authoritative blueprint checklist is empty")
    return rows


def _validate_contract(contract: dict[str, Any]) -> None:
    if contract.get("schema_version") != "stage1-phase-acceptance-contracts/1.0":
        fail("acceptance contract schema is unsupported")
    if contract.get("task_state_authority") != BLUEPRINT_PATH:
        fail("acceptance contract names the wrong task-state authority")
    if contract.get("phase_order") != list(PHASES):
        fail("acceptance contract phase order is not the seven-stage order")
    protocol = contract.get("state_protocol")
    if not isinstance(protocol, dict) or protocol.get("worker_self_tested") != "[_]":
        fail("acceptance contract does not preserve the [_] state boundary")
    if protocol.get("master_accepted") != "[x]":
        fail("acceptance contract does not preserve the [x] state boundary")
    phase_rows = contract.get("phases")
    if not isinstance(phase_rows, list):
        fail("acceptance contract lacks phase definitions")
    found: dict[str, str] = {}
    for row in phase_rows:
        if not isinstance(row, dict):
            fail("acceptance contract contains a malformed phase definition")
        phase, suffix = row.get("phase"), row.get("item_suffix")
        if phase in found:
            fail(f"acceptance contract duplicates phase {phase}")
        if isinstance(phase, str) and isinstance(suffix, str):
            found[phase] = suffix
    if found != PHASE_SUFFIXES:
        fail("acceptance contract phase identities are incomplete or noncanonical")


def _parse_theorem_dag(
    blob: migration.GitBlob,
    blueprint: migration.GitBlob,
    blueprint_rows: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    dag = _strict_json(blob.data, "HEAD theorem DAG")
    if dag.get("schema_version") != "stage1-theorem-dag/2.0":
        fail("theorem DAG schema is unsupported")
    if dag.get("requirements_source") != BLUEPRINT_PATH:
        fail("theorem DAG names the wrong authoritative blueprint")
    snapshot = dag.get("legacy_state_snapshot")
    if not isinstance(snapshot, dict):
        fail("theorem DAG lacks its authoritative state snapshot")
    if snapshot.get("authoritative_blueprint") != BLUEPRINT_PATH:
        fail("theorem DAG snapshot names the wrong blueprint")
    if snapshot.get("authoritative_blueprint_sha256") != blueprint.sha256:
        fail("theorem DAG snapshot is stale relative to the blueprint")

    theorem_rows = dag.get("theorems")
    if not isinstance(theorem_rows, list) or not theorem_rows:
        fail("theorem DAG has no theorem records")
    metadata: dict[str, dict[str, Any]] = {}
    projected: dict[str, dict[str, Any]] = {}
    seen_ranks: set[int] = set()
    for row in theorem_rows:
        if not isinstance(row, dict):
            fail("theorem DAG contains a malformed theorem record")
        theorem_id = row.get("theorem_id")
        rank = row.get("v2_execution_rank")
        states = row.get("phase_states")
        attempts = row.get("phase_attempts")
        context = row.get("dependency_context_sha256")
        if not isinstance(theorem_id, str) or not THEOREM_RE.fullmatch(theorem_id):
            fail("theorem DAG contains a malformed theorem identity")
        if theorem_id in metadata:
            fail(f"theorem DAG duplicates {theorem_id}")
        if isinstance(rank, bool) or not isinstance(rank, int) or rank <= 0:
            fail(f"theorem DAG has an invalid v2 rank for {theorem_id}")
        if rank in seen_ranks:
            fail(f"theorem DAG duplicates v2 rank {rank}")
        if not isinstance(states, dict) or set(states) != set(PHASES):
            fail(f"theorem DAG phase states are incomplete for {theorem_id}")
        if not isinstance(attempts, dict) or set(attempts) != set(PHASES):
            fail(f"theorem DAG phase attempts are incomplete for {theorem_id}")
        if not isinstance(context, str) or not migration.SHA256_RE.fullmatch(context):
            fail(f"theorem DAG lacks a dependency-context digest for {theorem_id}")
        seen_ranks.add(rank)
        metadata[theorem_id] = {
            "v2_execution_rank": rank,
            "dependency_context_sha256": context,
        }
        for phase in PHASES:
            state = states[phase]
            attempt = attempts[phase]
            if state not in {"[ ]", "[_]", "[x]"}:
                fail(f"theorem DAG has an invalid phase state for {theorem_id}")
            if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 0:
                fail(f"theorem DAG has invalid attempts for {theorem_id}/{phase}")
            item_id = f"S56-{theorem_id.removeprefix('THM-')}-{PHASE_SUFFIXES[phase]}"
            projected[item_id] = {
                "item_id": item_id,
                "theorem_id": theorem_id,
                "phase": phase,
                "state": state,
                "attempts": attempt,
            }
    if projected != blueprint_rows:
        missing = sorted(set(blueprint_rows) - set(projected))
        extra = sorted(set(projected) - set(blueprint_rows))
        mismatch = sorted(
            item_id
            for item_id in set(projected) & set(blueprint_rows)
            if projected[item_id] != blueprint_rows[item_id]
        )
        detail = (missing + extra + mismatch)[:3]
        fail("theorem DAG does not exactly project the blueprint: " + ",".join(detail))
    if snapshot.get("item_count") != len(blueprint_rows):
        fail("theorem DAG snapshot item count is stale")
    state_counts = dict(sorted(Counter(row["state"] for row in blueprint_rows.values()).items()))
    if snapshot.get("item_state_counts") != state_counts:
        fail("theorem DAG snapshot state counts are stale")
    return metadata


def _verify_inventory(
    value: dict[str, Any],
    *,
    reader: migration.HeadReader,
    blueprint_binding: dict[str, Any],
    contract_binding: dict[str, Any],
    blueprint_rows: dict[str, dict[str, Any]],
    expected_authority_mode: str,
) -> list[dict[str, Any]]:
    if value.get("schema_version") != migration.INVENTORY_SCHEMA:
        fail("legacy inventory schema is unsupported")
    inventory_sha256 = _embedded_digest(value, "inventory_sha256", "legacy inventory")
    if value.get("generated_from_revision") != reader.revision:
        fail("legacy inventory revision differs from authoritative HEAD")
    if value.get("generated_from_tree") != reader.tree:
        fail("legacy inventory tree differs from authoritative HEAD")
    if value.get("authority_mode") != expected_authority_mode:
        fail("legacy inventory contract authority mode is inconsistent")
    if value.get("authoritative_for_acceptance") is not False:
        fail("legacy inventory improperly claims acceptance authority")
    if value.get("mutates_repository") is not False:
        fail("legacy inventory does not declare read-only behavior")
    if value.get("executes_validators") is not False:
        fail("legacy inventory was not produced by the static-only lane")
    if value.get("blueprint") != blueprint_binding:
        fail("legacy inventory does not bind the current blueprint blob")
    if value.get("contract") != contract_binding:
        fail("legacy inventory does not bind the selected acceptance contract")

    items = value.get("items")
    if not isinstance(items, list) or not items:
        fail("legacy inventory contains no items")
    if value.get("item_count") != len(items):
        fail("legacy inventory item count is inconsistent")
    expected_ids = {
        item_id for item_id, row in blueprint_rows.items() if row["state"] == "[_]"
    }
    by_id: dict[str, dict[str, Any]] = {}
    status_counts: Counter[tuple[str, str]] = Counter()
    phase_counts: Counter[str] = Counter()
    ready_count = 0
    for item in items:
        if not isinstance(item, dict):
            fail("legacy inventory contains a malformed item")
        if item.get("schema_version") != migration.ITEM_SCHEMA:
            fail("legacy inventory contains an unsupported item schema")
        _embedded_digest(item, "item_sha256", f"inventory item {item.get('item_id')}")
        item_id = item.get("item_id")
        if not isinstance(item_id, str) or item_id in by_id:
            fail("legacy inventory contains a missing or duplicate item identity")
        row = blueprint_rows.get(item_id)
        if row is None or row["state"] != "[_]":
            fail(f"legacy inventory item is not authoritative [_]: {item_id}")
        expected_identity = {
            "theorem_id": row["theorem_id"],
            "phase": row["phase"],
            "attempts": row["attempts"],
            "authoritative_state": "[_]",
            "authority_revision": reader.revision,
            "authority_tree": reader.tree,
            "blueprint": blueprint_binding,
            "contract": contract_binding,
            "acceptance_claimed": False,
        }
        for field, expected in expected_identity.items():
            if item.get(field) != expected:
                fail(f"legacy inventory item {item_id} has inconsistent {field}")
        classes = item.get("classifications")
        if not isinstance(classes, list):
            fail(f"legacy inventory item {item_id} lacks classifications")
        categories: set[str] = set()
        all_clear = True
        for classification in classes:
            if not isinstance(classification, dict):
                fail(f"legacy inventory item {item_id} has a malformed classification")
            category = classification.get("category")
            status_value = classification.get("status")
            if category not in migration.CLASSIFICATIONS or category in categories:
                fail(f"legacy inventory item {item_id} has invalid classifications")
            if status_value not in migration.STATUS:
                fail(f"legacy inventory item {item_id} has an invalid status")
            if not isinstance(classification.get("reasons"), list) or not isinstance(
                classification.get("bindings"), list
            ):
                fail(f"legacy inventory item {item_id} has malformed classification evidence")
            categories.add(category)
            status_counts[(category, status_value)] += 1
            all_clear = all_clear and status_value == "clear"
        if categories != set(migration.CLASSIFICATIONS):
            fail(f"legacy inventory item {item_id} has incomplete classifications")
        if item.get("migration_ready") is not all_clear:
            fail(f"legacy inventory item {item_id} has a false migration-ready summary")
        ready_count += int(all_clear)
        phase_counts[row["phase"]] += 1
        by_id[item_id] = item
    if set(by_id) != expected_ids:
        fail("legacy inventory does not exactly cover authoritative [_] items")
    expected_phase_counts = dict(sorted(phase_counts.items()))
    if value.get("phase_counts") != expected_phase_counts:
        fail("legacy inventory phase counts are inconsistent")
    expected_classification_counts = {
        category: {
            status_value: status_counts[(category, status_value)]
            for status_value in ("blocked", "clear", "unknown")
        }
        for category in migration.CLASSIFICATIONS
    }
    if value.get("classification_counts") != expected_classification_counts:
        fail("legacy inventory classification counts are inconsistent")
    if value.get("migration_ready_count") != ready_count:
        fail("legacy inventory migration-ready count is inconsistent")
    # Retain the digest lookup in the verified object for lane construction.
    if value["inventory_sha256"] != inventory_sha256:
        fail("legacy inventory digest changed during verification")
    return list(by_id.values())


def _select_stratified(
    items: list[dict[str, Any]],
    theorem_metadata: dict[str, dict[str, Any]],
    limit: int,
    *,
    required_item_ids: tuple[str, ...] = (),
) -> list[dict[str, Any]]:
    strata: dict[str, list[dict[str, Any]]] = {phase: [] for phase in PHASES}
    for item in items:
        theorem_id = item["theorem_id"]
        if theorem_id not in theorem_metadata:
            fail(f"inventory theorem is absent from the theorem DAG: {theorem_id}")
        strata[item["phase"]].append(item)
    for phase in PHASES:
        strata[phase].sort(
            key=lambda item: (
                theorem_metadata[item["theorem_id"]]["v2_execution_rank"],
                item["item_id"],
            )
        )

    by_id = {item["item_id"]: item for item in items}
    selected = [by_id[item_id] for item_id in required_item_ids]
    selected_ids = set(required_item_ids)
    offsets = {phase: 0 for phase in PHASES}
    while len(selected) < limit:
        advanced = False
        for phase in PHASES:
            while (
                offsets[phase] < len(strata[phase])
                and strata[phase][offsets[phase]]["item_id"] in selected_ids
            ):
                offsets[phase] += 1
            if offsets[phase] < len(strata[phase]):
                item = strata[phase][offsets[phase]]
                selected.append(item)
                selected_ids.add(item["item_id"])
                offsets[phase] += 1
                advanced = True
                if len(selected) == limit:
                    break
        if not advanced:
            break
    return sorted(
        selected,
        key=lambda item: (
            PHASES.index(item["phase"]),
            theorem_metadata[item["theorem_id"]]["v2_execution_rank"],
            item["item_id"],
        ),
    )


def build_plan(
    root: Path,
    inventory_path: Path,
    *,
    revision: str = "HEAD",
    candidate_contract: Path | None = None,
    limit: int = MAX_SAMPLES,
    required_item_ids: list[str] | tuple[str, ...] = (),
) -> dict[str, Any]:
    """Validate immutable inputs and return a deterministic planning document."""

    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= MAX_SAMPLES:
        fail(f"sample limit must be between 1 and {MAX_SAMPLES}")
    try:
        reader = migration.HeadReader(root, revision)
        blueprint = reader.blob(BLUEPRINT_PATH)
        theorem_dag = reader.blob(THEOREM_DAG_PATH)
        if blueprint is None:
            fail("authoritative HEAD lacks the Stage1 v2 blueprint")
        if theorem_dag is None:
            fail("authoritative HEAD lacks the Stage1 theorem DAG")
        contract, contract_binding, head_owned_contract = migration.load_contract(
            reader, candidate_contract
        )
    except migration.InventoryError as exc:
        raise PlanError(str(exc)) from exc

    _validate_contract(contract)
    blueprint_rows = _parse_blueprint(blueprint)
    theorem_metadata = _parse_theorem_dag(theorem_dag, blueprint, blueprint_rows)
    inventory_bytes = _read_regular_file(inventory_path, "legacy inventory")
    inventory = _strict_json(inventory_bytes, "legacy inventory")
    authority_mode = "authoritative_head" if head_owned_contract else "candidate_preflight"
    verified_items = _verify_inventory(
        inventory,
        reader=reader,
        blueprint_binding=blueprint.binding(),
        contract_binding=contract_binding,
        blueprint_rows=blueprint_rows,
        expected_authority_mode=authority_mode,
    )
    if not isinstance(required_item_ids, (list, tuple)):
        fail("required item ids must be an ordered list")
    required = tuple(required_item_ids)
    if (
        any(not isinstance(item_id, str) for item_id in required)
        or len(required) != len(set(required))
        or len(required) > limit
    ):
        fail("required item ids are malformed, duplicated, or exceed the plan limit")
    verified_ids = {item["item_id"] for item in verified_items}
    missing_required = sorted(set(required) - verified_ids)
    if missing_required:
        fail(
            "required item is not an authoritative [_] inventory row: "
            + ", ".join(missing_required)
        )
    required = tuple(
        item["item_id"]
        for item in sorted(
            (item for item in verified_items if item["item_id"] in set(required)),
            key=lambda item: (
                PHASES.index(item["phase"]),
                theorem_metadata[item["theorem_id"]]["v2_execution_rank"],
                item["item_id"],
            ),
        )
    )
    selected = _select_stratified(
        verified_items,
        theorem_metadata,
        limit,
        required_item_ids=required,
    )
    if not selected:
        fail("there are no authoritative [_] items to revalidate")

    source_digests = {
        "blueprint_sha256": blueprint.sha256,
        "theorem_dag_sha256": theorem_dag.sha256,
        "contract_sha256": contract_binding["sha256"],
        "inventory_sha256": inventory["inventory_sha256"],
    }
    lanes: list[dict[str, Any]] = []
    for item in selected:
        theorem = theorem_metadata[item["theorem_id"]]
        classification_statuses = {
            entry["category"]: entry["status"] for entry in item["classifications"]
        }
        lane = {
            "schema_version": LANE_SCHEMA,
            "item_id": item["item_id"],
            "theorem_id": item["theorem_id"],
            "phase": item["phase"],
            "phase_layer": PHASES.index(item["phase"]),
            "v2_execution_rank": theorem["v2_execution_rank"],
            "attempts_at_plan_base": item["attempts"],
            "authoritative_state": "[_]",
            "required_steps": list(REQUIRED_STEPS),
            "step_outcomes": {step: "unknown" for step in REQUIRED_STEPS},
            "state_transition": "none",
            "acceptance_claimed": False,
            "promotes_to_master_accepted": False,
            "executes_validators": False,
            "launches_workers": False,
            "mutates_repository": False,
            "legacy_migration_ready_observation": item["migration_ready"],
            "legacy_classification_statuses": classification_statuses,
            "authority_revision": reader.revision,
            "authority_tree": reader.tree,
            "bindings": {
                **source_digests,
                "inventory_item_sha256": item["item_sha256"],
                "dependency_context_sha256": theorem["dependency_context_sha256"],
            },
        }
        lane["lane_sha256"] = migration.sha256_bytes(migration.canonical_json(lane))
        lanes.append(lane)

    eligible_counts = Counter(item["phase"] for item in verified_items)
    selected_counts = Counter(item["phase"] for item in selected)
    plan = {
        "schema_version": PLAN_SCHEMA,
        "generated_from_revision": reader.revision,
        "generated_from_tree": reader.tree,
        "authority_mode": authority_mode,
        "head_owned_contract": head_owned_contract,
        "planning_only": True,
        "authoritative_for_acceptance": False,
        "mutates_repository": False,
        "executes_validators": False,
        "launches_workers": False,
        "writes_ssot": False,
        "writes_todo": False,
        "writes_claims": False,
        "writes_paused_state": False,
        "state_transition": "none",
        "acceptance_claimed": False,
        "source_bindings": {
            "blueprint": blueprint.binding(),
            "theorem_dag": theorem_dag.binding(),
            "contract": contract_binding,
            "inventory": {
                "schema_version": inventory["schema_version"],
                "inventory_sha256": inventory["inventory_sha256"],
                "json_bytes_sha256": migration.sha256_bytes(inventory_bytes),
                "size": len(inventory_bytes),
            },
        },
        "selection_policy": {
            "hard_max_samples": MAX_SAMPLES,
            "requested_limit": limit,
            "authoritative_state_filter": "[_]",
            "phase_order": list(PHASES),
            "phase_layers": {phase: index for index, phase in enumerate(PHASES)},
            "allocation": "stable_round_robin_across_nonempty_phase_strata",
            "within_phase_order": ["v2_execution_rank", "item_id"],
            "output_order": ["phase_layer", "v2_execution_rank", "item_id"],
            "classification_counts_do_not_imply_acceptance": True,
        },
        "required_item_ids": list(required),
        "eligible_item_count": len(verified_items),
        "selected_item_count": len(lanes),
        "eligible_phase_counts": {
            phase: eligible_counts[phase] for phase in PHASES
        },
        "selected_phase_counts": {
            phase: selected_counts[phase] for phase in PHASES
        },
        "required_steps": list(REQUIRED_STEPS),
        "lanes": lanes,
    }
    plan["plan_sha256"] = migration.sha256_bytes(migration.canonical_json(plan))
    return plan


def _write_external_output(root: Path, output: Path, payload: bytes) -> None:
    repository = root.resolve()
    absolute = Path(os.path.abspath(os.fspath(output)))
    parent = absolute.parent.resolve()
    try:
        absolute.resolve(strict=False).relative_to(repository)
    except ValueError:
        pass
    else:
        fail("output path must be outside the repository")
    if not parent.is_dir():
        fail("output parent directory does not exist")
    if absolute.is_symlink() or (absolute.exists() and not absolute.is_file()):
        fail("output path is unsafe")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{absolute.name}.", suffix=".tmp", dir=parent
    )
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, absolute)
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        try:
            os.unlink(temporary_name)
        except OSError:
            pass
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--revision", default="HEAD")
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument(
        "--candidate-contract",
        type=Path,
        help="explicit uncommitted contract for non-authoritative planning preflight",
    )
    parser.add_argument("--limit", type=int, default=MAX_SAMPLES)
    parser.add_argument(
        "--required-item",
        action="append",
        default=[],
        help="authoritative [_] item id that must be included within the bounded plan",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="optional output path outside the repository; stdout is the default",
    )
    args = parser.parse_args()
    plan = build_plan(
        args.repo,
        args.inventory,
        revision=args.revision,
        candidate_contract=args.candidate_contract,
        limit=args.limit,
        required_item_ids=args.required_item,
    )
    payload = (
        json.dumps(plan, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")
    if args.output is None:
        print(payload.decode("utf-8"), end="")
    else:
        _write_external_output(args.repo, args.output, payload)


if __name__ == "__main__":
    try:
        main()
    except PlanError as exc:
        raise SystemExit(f"stage1_legacy_revalidation_plan: {exc}") from None
