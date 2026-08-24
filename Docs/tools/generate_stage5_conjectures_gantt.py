#!/usr/bin/env python3
"""Render the same-prefix conjecture Gantt from Blueprint plus local snapshot."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MANAGER_PATH = ROOT / "Docs/tools/manage_stage5_proof_debt_blueprints.py"
BLUEPRINT = ROOT / "Docs/Stage5_Conjectures_Blueprint.md"
GANTT = ROOT / "Docs/Stage5_Conjectures_Gantt.md"
RUNTIME = ROOT / ".ops/stage5-conjectures-execution-v2/epochs/stage5-conjecture-occurrence-pool-v2/status/runtime-snapshot.json"
PROMPT = ROOT / "Docs/evidence/stage5_conjectures/execution/concurrency-prompt.json"


def load_manager():
    spec = importlib.util.spec_from_file_location("stage5_conjecture_manager_for_gantt", MANAGER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("manager unavailable")
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
    return module


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def atomic_write(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with open(fd, "wb", closefd=True) as stream:
            stream.write(raw); stream.flush()
        __import__("os").replace(temporary, path)
    finally:
        if Path(temporary).exists(): Path(temporary).unlink()


def snapshot_loader(program):
    if not RUNTIME.exists():
        return None, None
    raw = RUNTIME.read_bytes()
    value = json.loads(raw)
    if not isinstance(value, dict) or value.get("program") != program.version:
        raise RuntimeError("conjecture runtime snapshot program differs")
    authority = value.get("authority_sha256")
    body = dict(value); body.pop("authority_sha256", None)
    if not isinstance(authority, str) or digest(json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()) != authority:
        raise RuntimeError("conjecture runtime snapshot seal differs")
    if (
        value.get("schema_version") != "awesome-theorems/stage5-runtime-snapshot/2.0"
        or value.get("runtime_authority_epoch") != manager_epoch()
    ):
        return None, None
    # A pool migration refreshes the explicit prompt's spec binding.  A
    # snapshot created under the predecessor prompt remains historical and
    # must not project statuses into the all-blank successor Blueprint.
    if PROMPT.is_file() and value.get("prompt_digest") != digest(PROMPT.read_bytes()):
        return None, None
    manager = load_manager()
    raw_blueprint = BLUEPRINT.read_bytes()
    expected = manager.expected_tasks(manager.CONJECTURE)
    specification = manager.spec_object(manager.CONJECTURE)
    workset = ROOT / "Docs/evidence/stage5_conjectures/workset-5.6.json"
    if (
        value.get("blueprint_sha256") != digest(raw_blueprint)
        or value.get("execution_spec_sha256") != digest(manager.canonical(specification))
        or value.get("checklist_dag_sha256") != digest(manager.canonical(manager.checklist_dag_object(expected)))
        or not workset.is_file()
        or value.get("workset_sha256") != digest(workset.read_bytes())
    ):
        return None, None
    return value, digest(raw)


def manager_epoch() -> str:
    manager = load_manager()
    return manager.CONJECTURE_RUNTIME_AUTHORITY_EPOCH


def render(generated_at: str | None = None) -> bytes:
    manager = load_manager()
    manager.runtime_snapshot = snapshot_loader
    expected = manager.expected_tasks(manager.CONJECTURE)
    raw = BLUEPRINT.read_bytes()
    # BOOT acceptance is complete; the ongoing checker owns later mutable
    # cursor transitions.  Permit that authenticated progress cursor while
    # retaining all immutable row/DAG and digest checks.
    tasks = manager.parse_blueprint(
        manager.CONJECTURE, raw, expected,
        allow_progress_cursor=True,
        allow_superseded_authority_for_invalidation=True,
        allow_immutable_row_drift=False,
    )
    if generated_at is None:
        generated_at = datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    return manager.render_gantt(manager.CONJECTURE, raw, tasks, generated_at)


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--validate-only", action="store_true"); args = parser.parse_args()
    try:
        if args.validate_only:
            old = GANTT.read_text(encoding="utf-8"); marker = "<!-- STAGE5-PROOF-DEBT-GANTT-METADATA:BEGIN -->"
            generated = json.loads(old.split(marker, 1)[1].split("<!-- STAGE5-PROOF-DEBT-GANTT-METADATA:END -->", 1)[0].strip()[8:-4])["generated_at"]
            if old.encode("utf-8") != render(generated): raise RuntimeError("conjecture Gantt is stale")
            manager = load_manager()
            print(json.dumps({"valid": True, "gantt": str(GANTT.relative_to(ROOT)), "items": len(manager.expected_tasks(manager.CONJECTURE))}, sort_keys=True)); return 0
        atomic_write(GANTT, render())
        print(json.dumps({"valid": True, "gantt": str(GANTT.relative_to(ROOT))}, sort_keys=True)); return 0
    except (OSError, ValueError, KeyError, RuntimeError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)})); return 1


if __name__ == "__main__": raise SystemExit(main())
