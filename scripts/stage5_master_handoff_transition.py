#!/usr/bin/env python3
"""Atomically publish theorem handoff cursors (``[ ]`` -> ``[_]``).

This is deliberately narrower than Master acceptance: it validates a
content-addressed worker handoff, prepares a post-transition Blueprint and
same-name Gantt, and commits both together with a transition receipt.  It
never applies a worker patch to the canonical checkout and never writes
``[x]``.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = ROOT / "Docs/Stage5_Theorems_Blueprint.md"
GANTT = ROOT / "Docs/Stage5_Theorems_Gantt.md"
EVIDENCE = ROOT / "Docs/evidence/stage5_theorems/execution/transitions"
RUNTIME = ROOT / ".ops/stage5-theorems-execution-v2"
PROGRAM = "stage5-theorem-proof-debt/2.0"


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode()


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def seal(value: dict) -> dict:
    body = dict(value)
    body["authority_sha256"] = digest(canonical(value))
    return body


def atomic(path: Path, raw: bytes, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def load_controller():
    path = ROOT / "scripts/stage5_theorems_execution_cron_v2.py"
    spec = importlib.util.spec_from_file_location("stage5_theorem_controller", path)
    if not spec or not spec.loader:
        raise RuntimeError("cannot load theorem controller")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def result_and_claim(controller, item_id: str) -> tuple[Path, Path, dict]:
    state = controller.load_state(False)
    record = state.get("claims", {}).get(item_id)
    if not isinstance(record, dict) or record.get("status") != "handoff_ready":
        raise RuntimeError(f"{item_id}: no harvested handoff_ready record")
    archive = Path(record["handoff"]["archive"])
    task_root = Path(record["task_root"])
    # The strict worker-result validator requires the original task-local
    # claim root because artifact paths intentionally point into that root.
    # The immutable archive is checked separately below and is the receipt's
    # durable handoff identity.
    result_path, claim_path = task_root / "work/_outbox/result.json", task_root / "claim.json"
    result = controller.claim_checker().validate_result(
        result_path, claim_path
    )
    if result["item_id"] != item_id or result["status"] != "self_tested":
        raise RuntimeError(f"{item_id}: worker result is not exact self-tested handoff")
    if digest((archive / "result.json").read_bytes()) != digest(result_path.read_bytes()):
        raise RuntimeError(f"{item_id}: archived result differs from source result")
    return result_path, claim_path, record


def prepare_gantt(controller, post_blueprint: bytes) -> bytes:
    fd, name = tempfile.mkstemp(prefix=".Stage5_Theorems_Blueprint.", dir=BLUEPRINT.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(post_blueprint)
        path = ROOT / "Docs/tools/generate_stage5_theorems_gantt.py"
        spec = importlib.util.spec_from_file_location("stage5_theorem_gantt_transition", path)
        if not spec or not spec.loader:
            raise RuntimeError("cannot load theorem Gantt generator")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.render(blueprint_path=temporary)
    finally:
        temporary.unlink(missing_ok=True)


def transition(item_id: str) -> dict:
    controller = load_controller()
    _, claim_path, record = result_and_claim(controller, item_id)
    pre_blueprint = BLUEPRINT.read_bytes()
    marker = f"- [ ] `{item_id}`".encode()
    replacement = f"- [_] `{item_id}`".encode()
    if pre_blueprint.count(marker) != 1:
        raise RuntimeError(f"{item_id}: expected exactly one blank authoritative row")
    post_blueprint = pre_blueprint.replace(marker, replacement, 1)
    if f"- [_] `{item_id}`".encode() not in post_blueprint:
        raise RuntimeError(f"{item_id}: failed to prepare underscore cursor")
    post_gantt = prepare_gantt(controller, post_blueprint)
    result_path = Path(record["handoff"]["archive"]) / "result.json"
    manifest_path = Path(record["handoff"]["archive"]) / "harvest-manifest.json"
    patch_sha = record["handoff"]["manifest_sha256"]
    handoff_archive = str(Path(record["handoff"]["archive"]).relative_to(ROOT))
    receipt_body = {
        "schema_version": "awesome-theorems/stage5-handoff-transition/1.0",
        "program": PROGRAM,
        "item_id": item_id,
        "state_transition": {"from": "not_done", "to": "handoff_waiting_master",
                              "pre_blueprint_sha256": digest(pre_blueprint),
                              "post_blueprint_sha256": digest(post_blueprint),
                              "post_gantt_sha256": digest(post_gantt)},
        "handoff": {"claim_id": record["claim_id"], "run_id": record["run_id"],
                    "claim_card_sha256": digest(claim_path.read_bytes()),
                    "worker_result_sha256": digest(result_path.read_bytes()),
                    "harvest_manifest_path": str(manifest_path.relative_to(ROOT)),
                    "harvest_manifest_sha256": digest(manifest_path.read_bytes()),
                    "immutable_archive": handoff_archive,
                    "patch_sha256": result_sha(result_path)},
        "canonical_integration": {"integrated": False,
                                   "canonical_write": "forbidden_until_master_acceptance"},
        "prepared_at": datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "transition_id": f"S5PD-HANDOFF-{item_id}-{uuid.uuid4().hex[:12]}",
    }
    receipt = seal(receipt_body)
    receipt_raw = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
    receipt_path = EVIDENCE / item_id / f"{digest(receipt_raw)}.json"
    # Prepare all bytes before publishing any destination.  The receipt is
    # content-addressed and therefore idempotent on retry.
    atomic(receipt_path, receipt_raw, 0o444)
    atomic(BLUEPRINT, post_blueprint)
    atomic(GANTT, post_gantt)
    return {"valid": True, "item_id": item_id, "state": "handoff_waiting_master",
            "receipt": str(receipt_path.relative_to(ROOT)),
            "post_blueprint_sha256": digest(post_blueprint),
            "post_gantt_sha256": digest(post_gantt)}


def result_sha(result_path: Path) -> str:
    value = json.loads(result_path.read_text())
    return value["patch"]["sha256"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("item_id", nargs="+")
    args = parser.parse_args()
    try:
        outputs = [transition(item_id) for item_id in args.item_id]
    except Exception as exc:
        import traceback
        traceback.print_exc()
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps({"valid": True, "transitions": outputs}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
