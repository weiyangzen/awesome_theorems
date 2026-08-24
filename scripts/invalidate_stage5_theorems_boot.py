#!/usr/bin/env python3
"""Archive and invalidate the unactivated Stage5 theorem BOOT acceptance.

This one-shot migration is intentionally narrower than ordinary execution.  It
may move BOOT from Master accepted back to blank only while no activation,
runtime, worker, mathematical handoff, or mathematical checklist progress
exists.  The old signed chain is copied into a content-addressed archive before
the Blueprint/Gantt compare-and-swap, then the four active BOOT receipt names
are renamed into that archive so a repaired BOOT can use fresh identities.
"""

from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANAGER_PATH = ROOT / "Docs/tools/manage_stage5_proof_debt_blueprints.py"
PREPARE_PATH = ROOT / "scripts/prepare_stage5_theorems_boot.py"
ACTIVATION = ROOT / "Docs/evidence/stage5_theorems/execution/controller-activation.json"
PROGRAM_RUNTIME = ROOT / ".ops/stage5-theorems-execution-v1"
SHARED_RUNTIME = ROOT / ".ops/stage5-proof-debt-shared-v1"
SCHEMA = "awesome-theorems/stage5-boot-reviewed-invalidation/1.0"
COMPLETE_SCHEMA = "awesome-theorems/stage5-boot-reviewed-invalidation-complete/1.0"


class InvalidationError(RuntimeError):
    pass


def load(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise InvalidationError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def exclusive(path: Path, raw: bytes, mode: int = 0o444) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(
        path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, mode,
    )
    try:
        view = memoryview(raw)
        while view:
            written = os.write(descriptor, view)
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False,
    ).encode("utf-8") + b"\n"


def main() -> int:
    manager = load(MANAGER_PATH, "stage5_manager_for_boot_invalidation")
    prepare = load(PREPARE_PATH, "stage5_prepare_for_boot_invalidation")
    program = manager.THEOREM
    expected = manager.expected_tasks(program)
    blueprint_raw, blueprint_guard = manager.regular_file_bytes(
        program.blueprint, "accepted theorem Blueprint"
    )
    gantt_raw, gantt_guard = manager.regular_file_bytes(
        program.gantt, "accepted theorem Gantt"
    )
    current = manager.parse_blueprint(
        program,
        blueprint_raw,
        expected,
        allow_boot_transition=True,
        allow_superseded_authority_for_invalidation=True,
    )
    if current[0].state != "x" or any(task.state != " " for task in current[1:]):
        raise InvalidationError(
            "invalidation requires BOOT=x and every mathematical row blank"
        )
    if any(path.exists() or path.is_symlink() for path in (PROGRAM_RUNTIME, SHARED_RUNTIME)):
        raise InvalidationError("invalidation refuses runtime presence")
    if ACTIVATION.exists() or ACTIVATION.is_symlink():
        activation = manager.strict_json_loads(ACTIVATION.read_bytes(), "active controller activation")
        if not isinstance(activation, dict) or activation.get("program") != program.version:
            raise InvalidationError("invalidation refuses unrelated activation receipt")
        ACTIVATION.unlink()
    cron = manager.read_user_crontab()
    if program.cron_marker_begin in cron or program.cron_marker_end in cron:
        raise InvalidationError("invalidation refuses installed theorem cron markers")

    handoff, handoff_acceptance, review, acceptance = manager.boot_receipt_paths(program)
    active_paths = (handoff, handoff_acceptance, review, acceptance)
    records: list[dict[str, Any]] = []
    guards: dict[Path, Any] = {
        program.blueprint: blueprint_guard,
        program.gantt: gantt_guard,
    }
    for path in active_paths:
        raw, guard = manager.regular_file_bytes(path, f"active BOOT receipt {path.name}")
        value = manager.strict_json_loads(raw, path.name)
        if not isinstance(value, dict) or not isinstance(value.get("authority_sha256"), str):
            raise InvalidationError(f"active BOOT receipt is malformed: {path.name}")
        records.append({
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": manager.sha256_bytes(raw),
            "authority_sha256": value["authority_sha256"],
            "size_bytes": len(raw),
        })
        guards[path] = guard
    text = blueprint_raw.decode("utf-8")
    spec_block = text.split(manager.SPEC_BEGIN, 1)[1].split(manager.SPEC_END, 1)[0].strip()
    if not spec_block.startswith("```json\n") or not spec_block.endswith("\n```"):
        raise InvalidationError("superseded execution specification fence differs")
    old_spec = manager.strict_json_loads(spec_block[8:-4], "superseded theorem execution specification")
    if (
        not isinstance(old_spec, dict)
        or old_spec.get("program") != program.version
        or old_spec.get("authoritative_blueprint") != program.blueprint.relative_to(ROOT).as_posix()
        or old_spec.get("gantt_projection") != program.gantt.relative_to(ROOT).as_posix()
    ):
        raise InvalidationError("superseded execution specification identity differs")
    old_spec_sha256 = manager.sha256_bytes(manager.canonical(old_spec))
    handoff_value, _ = manager.sealed_boot_receipt(
        handoff, manager.BOOT_HANDOFF_FIELDS, manager.BOOT_HANDOFF_SCHEMA, "active BOOT handoff"
    )
    handoff_acceptance_value, _ = manager.sealed_boot_receipt(
        handoff_acceptance,
        manager.BOOT_HANDOFF_ACCEPTANCE_FIELDS,
        manager.BOOT_HANDOFF_ACCEPTANCE_SCHEMA,
        "active BOOT handoff acceptance",
    )
    review_value, _ = manager.sealed_boot_receipt(
        review, manager.BOOT_REVIEW_FIELDS, manager.BOOT_REVIEW_SCHEMA, "active BOOT review"
    )
    acceptance_value = manager.strict_json_loads(acceptance.read_bytes(), "active BOOT acceptance")
    acceptance_unsigned = dict(acceptance_value)
    acceptance_authority = acceptance_unsigned.pop("authority_sha256", None)
    if (
        not isinstance(acceptance_value, dict)
        or not isinstance(acceptance_authority, str)
        or manager.sha256_bytes(manager.canonical(acceptance_unsigned)) != acceptance_authority
    ):
        raise InvalidationError("active BOOT acceptance canonical seal differs")
    old_manager_sha256 = handoff_value.get("manager_sha256")
    if (
        not isinstance(old_manager_sha256, str)
        or handoff_value.get("execution_spec_sha256") != old_spec_sha256
        or handoff_value.get("blueprint_sha256") != handoff_acceptance_value.get("pre_blueprint_sha256")
        or handoff_acceptance_value.get("handoff_authority_sha256")
        != handoff_value.get("authority_sha256")
        or review_value.get("handoff_acceptance_authority_sha256")
        != handoff_acceptance_value.get("authority_sha256")
        or acceptance_value.get("handoff_authority_sha256")
        != handoff_value.get("authority_sha256")
        or acceptance_value.get("handoff_acceptance_authority_sha256")
        != handoff_acceptance_value.get("authority_sha256")
        or acceptance_value.get("review_authority_sha256")
        != review_value.get("authority_sha256")
        or acceptance_value.get("manager_sha256") != old_manager_sha256
        or acceptance_value.get("post_blueprint_sha256") != manager.sha256_bytes(blueprint_raw)
    ):
        raise InvalidationError("superseded BOOT receipts do not bind one old manager/spec/Blueprint chain")
    trust_keys, trust_guard = manager.boot_trust_keys(program)
    guards[manager.boot_trust_root_path(program)] = trust_guard
    manager.validate_signed_boot_document(
        handoff_value,
        manager.BOOT_HANDOFF_FIELDS,
        manager.BOOT_HANDOFF_SCHEMA,
        "superseded BOOT handoff",
        trust_keys,
        "producer",
    )
    manager.validate_signed_boot_document(
        review_value,
        manager.BOOT_REVIEW_FIELDS,
        manager.BOOT_REVIEW_SCHEMA,
        "superseded BOOT review",
        trust_keys,
        "master",
    )
    signed_attestations = [
        (handoff_value.get("producer_attestation"), "producer"),
        (review_value.get("master_attestation"), "master"),
    ]
    for locator in review_value.get("reviewer_decisions", []):
        decision_path = ROOT / locator["path"]
        decision, decision_guard = manager.sealed_boot_receipt(
            decision_path,
            manager.BOOT_DECISION_FIELDS,
            manager.BOOT_DECISION_SCHEMA,
            "superseded BOOT reviewer decision",
        )
        if (
            decision_guard.sha256 != locator.get("sha256")
            or decision.get("handoff_acceptance_authority_sha256")
            != handoff_acceptance_value.get("authority_sha256")
        ):
            raise InvalidationError("superseded reviewer decision chain differs")
        manager.validate_signed_boot_document(
            decision,
            manager.BOOT_DECISION_FIELDS,
            manager.BOOT_DECISION_SCHEMA,
            "superseded BOOT reviewer decision",
            trust_keys,
            "reviewer",
        )
        signed_attestations.append((decision.get("reviewer_attestation"), "reviewer"))
    principals = []
    for attestation, role in signed_attestations:
        if (
            not isinstance(attestation, dict)
            or attestation.get("manager_sha256") != old_manager_sha256
            or attestation.get("execution_spec_sha256") != old_spec_sha256
        ):
            raise InvalidationError("superseded BOOT role attestation authority differs")
        principals.append(manager.validate_signed_boot_document(
            attestation,
            manager.BOOT_ROLE_FIELDS,
            manager.BOOT_ROLE_SCHEMA,
            f"superseded BOOT {role} attestation",
            trust_keys,
            role,
        ))
    if len(principals) != 4 or len(set(principals)) != 4:
        raise InvalidationError("superseded BOOT principals are not four-way distinct")
    decision_paths: list[Path] = []
    for locator in review_value.get("reviewer_decisions", []):
        path = ROOT / locator["path"]
        raw, guard = manager.regular_file_bytes(path, "old BOOT reviewer decision")
        if manager.sha256_bytes(raw) != locator["sha256"]:
            raise InvalidationError("old reviewer decision digest differs")
        decision_paths.append(path)
        records.append({
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": locator["sha256"],
            "authority_sha256": manager.strict_json_loads(raw, path.name)["authority_sha256"],
            "size_bytes": len(raw),
        })
        guards[path] = guard

    blank = [task.with_state(" ") for task in expected]
    manager.validate_task_set(program, blank)
    new_blueprint = manager.render_blueprint(program, blank)
    if manager.parse_blueprint(program, new_blueprint, blank) != blank:
        raise InvalidationError("repaired all-blank Blueprint did not round-trip")
    new_gantt = manager.render_gantt(program, new_blueprint, blank, timestamp())
    defects = [
        {
            "id": "worker-inner-bwrap-denied-by-host-apparmor",
            "evidence": "every task-local workspace-write command, including /bin/true, failed before execution because kernel.apparmor_restrict_unprivileged_userns=1 denied bwrap uid_map/setpcap; zero worker result was produced",
        },
        {
            "id": "worker-single-thread-invariant-not-enforced",
            "evidence": "features.multi_agent=false and features.multi_agent_v2=false did not override the host-injected proactive multi-agent developer mode; authenticated primary goals spawned child threads and therefore ceased to satisfy the exactly-one-thread liveness gate",
        },
        {
            "id": "worker-code-mode-host-helper-not-mounted",
            "evidence": "the container mounted the pinned native Codex executable but omitted its sibling codex-code-mode-host helper; every worker tool call failed with os error 2, so the canary produced zero result manifests and zero handoffs despite having one authenticated thread and active goal",
        },
        {
            "id": "worker-generated-finalizer-newline-was-invalid-python",
            "evidence": "the helper-mounted canary executed tools, wrote a checker-valid INTAKE artifact and passed its phase gate, but the generated finalize.py embedded an interpreted newline inside a quoted string and failed to parse at line 30; therefore it produced zero result manifests and zero handoffs",
        },
    ]
    body = {
        "schema_version": SCHEMA,
        "program": program.version,
        "migration_id": "S5THM-BOOT-INVALIDATE-001",
        "reason": "the activated controller failed production runtime conformance; its cron was removed, every task-local transport was retired, activation/runtime were archived without mathematical progress, and the exact BOOT artifact binding must be invalidated before container-isolated repair",
        "defects": defects,
        "mathematical_rows_advanced": 0,
        "activation_present": False,
        "runtime_present": False,
        "cron_marker_present": False,
        "old_manager_sha256": manager.manager_code_sha256(),
        "old_controller_sha256": manager.sha256_bytes(
            (ROOT / "scripts/stage5_theorems_execution_cron.py").read_bytes()
        ),
        "pre_blueprint_sha256": manager.sha256_bytes(blueprint_raw),
        "pre_gantt_sha256": manager.sha256_bytes(gantt_raw),
        "post_blueprint_sha256": manager.sha256_bytes(new_blueprint),
        "post_gantt_sha256": manager.sha256_bytes(new_gantt),
        "superseded_records": sorted(records, key=lambda row: row["path"]),
        "reviewed_at": timestamp(),
    }
    payload = manager.canonical(body)
    signatures = []
    identities = (
        ("producer", 0), ("reviewer", 0), ("reviewer", 1), ("master", 0),
    )
    for role, ordinal in identities:
        key_id, principal, _ = prepare.role_identity(role, ordinal)
        key = prepare.load_private_key(key_id, principal, role)
        signatures.append({
            "role": role, "principal_id": principal, "key_id": key_id,
            "signature_algorithm": "Ed25519",
            "signed_payload_sha256": manager.sha256_bytes(payload),
            "signature": key.sign(payload).hex(),
        })
    receipt = {**body, "signatures": signatures}
    receipt["authority_sha256"] = manager.sha256_bytes(manager.canonical(receipt))
    migration_id = receipt["authority_sha256"]
    archive = (
        manager.boot_evidence_root(program) / "bootstrap" / "superseded" /
        migration_id
    )
    if archive.exists() or archive.is_symlink():
        raise InvalidationError("content-addressed invalidation archive already exists")
    archive.mkdir(parents=True, mode=0o755)
    for path in (*active_paths, *decision_paths):
        relative = path.relative_to(ROOT).as_posix().replace("/", "__")
        exclusive(archive / "sealed-inputs" / relative, path.read_bytes())
    exclusive(archive / "invalidation.json", json_bytes(receipt))

    def precommit() -> None:
        if any(path.exists() or path.is_symlink() for path in (ACTIVATION, PROGRAM_RUNTIME, SHARED_RUNTIME)):
            raise InvalidationError("activation/runtime appeared before invalidation commit")
        for path, guard in guards.items():
            manager.validate_file_expectation(path, guard)

    with manager.manager_mutation_lock():
        manager.recover_batch_transactions()
        manager.atomic_batch_write(
            [(program.blueprint, new_blueprint), (program.gantt, new_gantt)],
            expected_old={program.blueprint: blueprint_guard, program.gantt: gantt_guard},
            guards={path: guard for path, guard in guards.items() if path not in {program.blueprint, program.gantt}},
            precommit_validator=precommit,
        )
    originals = archive / "active-originals"
    originals.mkdir(mode=0o755)
    for path in active_paths:
        destination = originals / path.name
        os.rename(path, destination)
    key_id, principal, _ = prepare.role_identity("master", 0)
    complete_body = {
        "schema_version": COMPLETE_SCHEMA,
        "program": program.version,
        "invalidation_authority_sha256": migration_id,
        "post_blueprint_sha256": manager.sha256_bytes(program.blueprint.read_bytes()),
        "post_gantt_sha256": manager.sha256_bytes(program.gantt.read_bytes()),
        "active_receipts_absent": all(not path.exists() and not path.is_symlink() for path in active_paths),
        "completed_at": timestamp(),
        "master_principal_id": principal,
        "key_id": key_id,
    }
    complete_payload = manager.canonical(complete_body)
    key = prepare.load_private_key(key_id, principal, "master")
    complete = {
        **complete_body,
        "signed_payload_sha256": manager.sha256_bytes(complete_payload),
        "signature": key.sign(complete_payload).hex(),
    }
    complete["authority_sha256"] = manager.sha256_bytes(manager.canonical(complete))
    exclusive(archive / "complete.json", json_bytes(complete))
    print(json.dumps({
        "valid": True,
        "archive": archive.relative_to(ROOT).as_posix(),
        "invalidation_authority_sha256": migration_id,
        "boot_state": "not_done",
        "mathematical_rows_advanced": 0,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (InvalidationError, OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
