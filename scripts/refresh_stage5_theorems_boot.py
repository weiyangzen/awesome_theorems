#!/usr/bin/env python3
"""Archive the superseded theorem BOOT/activation chain after a CAS migration.

It never preserves mathematical acceptance across a changed execution
authority, starts no worker, and refuses any active runtime or cron marker.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
MANAGER_PATH = ROOT / "Docs/tools/manage_stage5_proof_debt_blueprints.py"
PREPARE_PATH = ROOT / "scripts/prepare_stage5_theorems_boot.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def main() -> int:
    m = load(MANAGER_PATH, "stage5_manager_for_boot_refresh")
    p = load(PREPARE_PATH, "stage5_prepare_for_boot_refresh")
    program = m.THEOREM
    expected = m.expected_tasks(program)
    bp_raw, bp_guard = m.regular_file_bytes(program.blueprint, "theorem Blueprint")
    gantt_raw, gantt_guard = m.regular_file_bytes(program.gantt, "theorem Gantt")
    current = m.parse_blueprint(program, bp_raw, expected,
                                allow_boot_transition=True,
                                allow_superseded_authority_for_invalidation=True,
                                allow_immutable_row_drift=True)
    boot_id = f"{program.task_prefix}-BOOT-001"
    if current[0].item_id != boot_id or any(t.state != " " for t in current):
        raise RuntimeError("refresh requires the reviewed migration to have invalidated every theorem row")
    if m.read_user_crontab().find(program.cron_marker_begin) >= 0 or m.read_user_crontab().find(program.cron_marker_end) >= 0:
        raise RuntimeError("refresh refuses an installed theorem cron marker")
    for candidate in (ROOT / program.runtime_root, ROOT / m.SHARED_RUNTIME_ROOT):
        if os.path.lexists(candidate):
            raise RuntimeError(f"refresh refuses runtime surface {candidate.relative_to(ROOT)}")
    receipt_paths = (*m.boot_receipt_paths(program), ROOT / "Docs/evidence/stage5_theorems/execution/controller-activation.json")
    old_receipts = []
    for path in receipt_paths:
        if not path.exists() and not path.is_symlink():
            continue
        raw, guard = m.regular_file_bytes(path, f"old BOOT receipt {path.name}")
        old_receipts.append({"path": path.relative_to(ROOT).as_posix(),
                             "sha256": sha(raw), "authority_sha256": json.loads(raw)["authority_sha256"],
                             "bytes": len(raw), "guard": guard})
    blank = [task.with_state(" ") for task in expected]
    new_bp = m.render_blueprint(program, blank)
    new_gantt = m.render_gantt(program, new_bp, blank,
                               datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ"))
    migrations = sorted((ROOT / "Docs/evidence/stage5_shared_execution/blueprint-migrations").glob("S5PD-BLUEPRINT-MIGRATE-*-program-isolation.json"))
    if not migrations:
        raise RuntimeError("refresh requires a sealed program-isolation migration receipt")
    latest_migration = migrations[-1].relative_to(ROOT).as_posix()
    body = {
        "schema_version": "awesome-theorems/stage5-theorem-boot-refresh/1.0",
        "migration_id": f"S5THM-BOOT-REFRESH-{len(migrations):06d}",
        "reason": "the accepted BOOT and controller activation predate the reviewed 24-worker gpt-5.6-sol/ultra/default authority and its controller-accounted subagent boundary",
        "program": program.version,
        "latest_program_isolation_receipt": latest_migration,
        "pre_blueprint_sha256": sha(bp_raw), "pre_gantt_sha256": sha(gantt_raw),
        "post_blueprint_sha256": sha(new_bp), "post_gantt_sha256": sha(new_gantt),
        "mathematical_rows_advanced": 0,
        "superseded_receipts": [{k:v for k,v in x.items() if k != "guard"} for x in old_receipts],
        "worker_launches": 0, "cron_present": False, "runtime_present": False,
        "refreshed_at": datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    payload = canonical(body)
    signatures = []
    for role, ordinal in (("producer", 0), ("reviewer", 0), ("reviewer", 1), ("master", 0)):
        key_id, principal, expected_role = p.role_identity(role, ordinal)
        key = p.load_private_key(key_id, principal, expected_role)
        signatures.append({"role": role, "principal_id": principal, "key_id": key_id,
                           "signature_algorithm": "Ed25519", "signed_payload_sha256": sha(payload),
                           "signature": key.sign(payload).hex()})
    receipt = dict(body, signatures=signatures)
    receipt["authority_sha256"] = sha(canonical(receipt))
    archive = ROOT / "Docs/evidence/stage5_theorems/bootstrap/superseded" / receipt["authority_sha256"]
    if archive.exists(): raise RuntimeError("refresh archive already exists")
    archive.mkdir(parents=True)
    (archive / "refresh.json").write_bytes(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n")
    for item in old_receipts:
        target = archive / "old" / Path(item["path"]).name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / item["path"]).read_bytes())
    with m.manager_mutation_lock():
        m.recover_batch_transactions()
        for path, guard in ((program.blueprint, bp_guard), (program.gantt, gantt_guard), *[(ROOT / x["path"], x["guard"]) for x in old_receipts]):
            m.validate_file_expectation(path, guard)
        m.atomic_batch_write(
            [(program.blueprint, new_bp), (program.gantt, new_gantt)],
            expected_old={program.blueprint: bp_guard, program.gantt: gantt_guard},
            guards={ROOT / x["path"]: x["guard"] for x in old_receipts},
            precommit_validator=lambda: None,
        )
    for path in receipt_paths:
        if path.exists() or path.is_symlink():
            path.unlink()
    print(json.dumps({"refreshed": True, "archive": str((archive / "refresh.json").relative_to(ROOT)),
                      "post_blueprint_sha256": sha(new_bp), "post_gantt_sha256": sha(new_gantt)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
