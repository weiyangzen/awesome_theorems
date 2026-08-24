#!/usr/bin/env python3
"""Stage5 conjecture execution: one independent tmux/Codex goal per conjecture.

This is a program-local controller.  It does not import or inspect theorem
runtime state.  Every admitted TARGET owns a fresh task root, tmux socket and
server/session, writable Codex home, process tree, thread and one `/goal`.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
from pathlib import PurePosixPath
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import tarfile
import time
import tomllib
import uuid
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = ROOT / "Docs/Stage5_Conjectures_Blueprint.md"
GANTT = ROOT / "Docs/Stage5_Conjectures_Gantt.md"
CHECKER = ROOT / "Docs/tools/check_stage5_conjectures_blueprint.py"
CLAIM_CHECKER = ROOT / "scripts/check_stage5_conjecture_claim.py"
HANDOFF_TRANSITION = ROOT / "scripts/stage5_conjecture_handoff_transition.py"
HISTORICAL_RUNTIME = ROOT / ".ops/stage5-conjectures-execution-v2"
RUNTIME_AUTHORITY_EPOCH = "stage5-conjecture-occurrence-pool-v2"
RUNTIME = HISTORICAL_RUNTIME / "epochs" / RUNTIME_AUTHORITY_EPOCH
SCHEDULER_LOCK = ROOT / ".ops/stage5-conjectures-execution-v2.scheduler.lock"
EVIDENCE = ROOT / "Docs/evidence/stage5_conjectures"
HANDOFF_QUEUE = RUNTIME / "handoffs"
HANDOFF_ARCHIVE = ROOT / "Docs/evidence/stage5_conjectures/execution/handoffs"
MASTER_ACCEPTANCES = ROOT / "Docs/evidence/stage5_conjectures/execution/acceptances"
INTEGRATION_QUEUE = RUNTIME / "integration"
HARVEST_LEDGER = RUNTIME / "ledgers/harvested-handoffs.jsonl"
STATE = RUNTIME / "state/controller-state.json"
EVENTS = RUNTIME / "ledgers/events.jsonl"
EVENT_LOCK = RUNTIME / "locks/events.lock"
LEASE_LOCK = RUNTIME / "locks/request-leases.lock"
REQUESTS = RUNTIME / "ledgers/request-leases.jsonl"
TURNS = RUNTIME / "ledgers/turn-leases.jsonl"
PROGRAM = "stage5-conjecture-proof-debt/2.0"
TRANSPORT = "tmux_codex_tui"
GOAL_COMMAND = "/goal"
PROVIDER = "sub2api"
MODEL = "gpt-5.6-sol"
EFFORT = "ultra"
SERVICE_TIER = "default"
CONCURRENCY_PROMPT = EVIDENCE / "execution/concurrency-prompt.json"
CONCURRENCY_SCHEMA = "awesome-theorems/stage5-concurrency-prompt/2.0"
CONCURRENCY_DIMENSIONS = frozenset({"logical_claims", "service_records", "agent_executions", "startup_reservations", "launch_fanout_per_wave", "live_transports", "authenticated_goals", "running_turns", "outbound_request_starts_per_window", "in_flight_requests", "integration", "validators", "exact_path_conflicts"})
COOLDOWN = 120
AUTH = Path(os.environ.get("STAGE5_BOOT_AUTH", "/home/sansha/.codex/auth.json"))
CONFIG = Path(os.environ.get("STAGE5_BOOT_CONFIG", "/home/sansha/.codex/config.toml"))
CODEX = Path("/home/sansha/.local/node_modules/.bin/codex")
TASKS_NAMESPACE_RE = re.compile(
    re.escape(str(ROOT / ".ops"))
    + r"/stage5-(?:theorems|conjectures)-execution-v2/(?:epochs/[^/]+/)?tasks/"
      r"[^\s'\";|&\]\[{}()<>]*"
)
RELATIVE_TASK_ESCAPE_RE = re.compile(r"(?<![A-Za-z0-9_.-])\.\./\.\.(?:/|(?=[\s'\";|&)]|$))")


class ControllerError(RuntimeError):
    pass


def _regular(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ControllerError(f"{label}: missing regular file")
    return path.read_bytes()


def _copy_immutable(source: Path, destination: Path, label: str) -> str:
    raw = _regular(source, label)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink():
        raise ControllerError(f"{label}: destination is a symlink")
    if destination.exists():
        if not destination.is_file() or destination.read_bytes() != raw:
            raise ControllerError(f"{label}: immutable destination conflict")
    else:
        atomic_write(destination, raw, 0o444)
    return digest(raw)


def _expect_immutable(source: Path, destination: Path, label: str) -> str:
    """Verify a previously published immutable copy without repairing it."""
    source_raw = _regular(source, label)
    destination_raw = _regular(destination, label)
    if destination_raw != source_raw:
        raise ControllerError(f"{label}: immutable destination conflict")
    return digest(source_raw)


def _new_handoff_destination(destination: Path) -> None:
    """Require a wholly absent content-addressed destination before publish."""
    current = destination
    while not current.exists() and not current.is_symlink():
        if current == ROOT or current.parent == current:
            break
        current = current.parent
    if current.is_symlink() or not current.is_dir():
        raise ControllerError("immutable handoff destination has an unsafe ancestor")


def _publish_handoff_tree(
    destination: Path,
    sources: list[tuple[Path, Path, str]],
    manifest_raw: bytes,
) -> None:
    """Crash-safely publish one complete immutable handoff directory.

    A fresh tree is fully written under a sibling staging directory and then
    exposed with one directory rename.  A stale staging directory is never
    treated as authority and is replaced on retry.  Existing final trees are
    replay-only: every byte must already match exactly.
    """
    if destination.exists() or destination.is_symlink():
        if destination.is_symlink() or not destination.is_dir():
            raise ControllerError("immutable handoff destination is unsafe")
        for source, relative, label in sources:
            _expect_immutable(source, destination / relative, label)
        if _regular(destination / "harvest-manifest.json", "harvest manifest") != manifest_raw:
            raise ControllerError("harvest manifest conflict")
        return
    _new_handoff_destination(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = destination.parent / f".{destination.name}.staging"
    if staging.exists() or staging.is_symlink():
        if staging.is_symlink() or not staging.is_dir():
            raise ControllerError("immutable handoff staging destination is unsafe")
        shutil.rmtree(staging)
    staging.mkdir(mode=0o700)
    try:
        for source, relative, label in sources:
            _copy_immutable(source, staging / relative, label)
        atomic_write(staging / "harvest-manifest.json", manifest_raw, 0o444)
        for current, _, files in os.walk(staging, topdown=False):
            for name in files:
                with (Path(current) / name).open("rb") as stream:
                    os.fsync(stream.fileno())
            descriptor = os.open(current, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
        try:
            staging.rename(destination)
        except FileExistsError:
            # Another identical publisher may have won the content-addressed
            # name.  Never merge trees; verify the complete winner instead.
            if destination.is_symlink() or not destination.is_dir():
                raise ControllerError("immutable handoff publish conflict")
            shutil.rmtree(staging)
            for source, relative, label in sources:
                _expect_immutable(source, destination / relative, label)
            if _regular(destination / "harvest-manifest.json", "harvest manifest") != manifest_raw:
                raise ControllerError("harvest manifest conflict")
    except BaseException:
        if staging.exists() and not staging.is_symlink():
            shutil.rmtree(staging)
        raise


def _safe_relative(value: str, label: str) -> Path:
    """Return one canonical POSIX relative path with no escape components."""
    if not isinstance(value, str):
        raise ControllerError(f"{label}: expected a string path")
    path = PurePosixPath(value)
    if (
        not value or path.is_absolute() or value != path.as_posix()
        or "." in path.parts or ".." in path.parts
    ):
        raise ControllerError(f"{label}: unsafe relative path {value!r}")
    return Path(*path.parts)


def _result_artifacts(
    result: dict[str, Any], claim: dict[str, Any], work: Path,
) -> list[dict[str, Any]]:
    """Close the worker artifact list over the claim's ordered ownership."""
    writable = list(claim.get("writable_paths", []))
    changed = list(result.get("changed_paths", []))
    if changed != writable:
        raise ControllerError("worker changed paths differ from exact claim ownership")
    canonical = [
        _safe_relative(value, "claim writable path").as_posix()
        for value in writable
    ]
    if canonical != writable or len(canonical) != len(set(canonical)):
        raise ControllerError("claim writable paths are duplicate or non-canonical")
    rows = result.get("artifacts")
    if not isinstance(rows, list) or len(rows) != len(canonical):
        raise ControllerError("worker result artifacts differ from exact claim ownership")
    by_relative: dict[str, dict[str, Any]] = {}
    work_absolute = work.absolute()
    if work != work_absolute:
        raise ControllerError("task work root is not canonical absolute")
    for row in rows:
        if not isinstance(row, dict):
            raise ControllerError("worker result artifact is not an object")
        source_value = row.get("path")
        if not isinstance(source_value, str):
            raise ControllerError("worker result artifact path is missing")
        source = Path(source_value)
        if not source.is_absolute() or source_value != os.path.normpath(source_value):
            raise ControllerError("worker result artifact path is not canonical absolute")
        try:
            relative = source.relative_to(work_absolute).as_posix()
        except ValueError as exc:
            raise ControllerError("worker result artifact escapes the task work root") from exc
        relative = _safe_relative(relative, "worker result artifact").as_posix()
        if source != work / _safe_relative(relative, "worker result artifact"):
            raise ControllerError("worker result artifact path differs from canonical ownership")
        if relative in by_relative:
            raise ControllerError("worker result has duplicate artifact paths")
        by_relative[relative] = row
    if set(by_relative) != set(canonical):
        raise ControllerError("worker result artifacts differ from exact claim ownership")
    artifacts: list[dict[str, Any]] = []
    for relative in canonical:
        row = by_relative[relative]
        source = work / _safe_relative(relative, "owned artifact")
        raw = _regular(source, f"required owned file {relative}")
        if not raw:
            raise ControllerError(f"required owned file {relative} is empty")
        if (
            row.get("sha256") != digest(raw)
            or row.get("size_bytes") != len(raw)
            or not isinstance(row.get("media_type"), str)
            or not row["media_type"]
        ):
            raise ControllerError(f"worker result artifact bytes differ: {relative}")
        artifacts.append({
            "path": relative,
            "source_path": row["path"],
            "archive_path": f"artifacts/{relative}",
            "sha256": digest(raw),
            "size_bytes": len(raw),
            "media_type": row["media_type"],
        })
    return artifacts


def _patch_paths(raw: bytes, writable: list[str]) -> None:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ControllerError("changes.patch is not UTF-8") from exc
    found: set[str] = set()
    pairs = re.findall(r"^diff --git a/(.+) b/(.+)$", text, re.MULTILINE)
    if pairs:
        for old, new in pairs:
            for value in (old, new):
                if value != "/dev/null": found.add(value)
    else:
        old_path: str | None = None
        for line in text.splitlines():
            if line.startswith("--- "): old_path = line[4:].split("\t", 1)[0]
            elif line.startswith("+++ ") and old_path is not None:
                for value in (old_path, line[4:].split("\t", 1)[0]):
                    if value != "/dev/null": found.add(value.removeprefix("a/").removeprefix("b/"))
                old_path = None
    cleaned: set[str] = set()
    for value in found:
        value = value.removeprefix("a/").removeprefix("b/"); path = PurePosixPath(value)
        if not value or path.is_absolute() or value != path.as_posix() or ".." in path.parts:
            raise ControllerError(f"changes.patch: unsafe path {value!r}")
        if path.parts[0] in {".git", ".ops", "Docs"}: raise ControllerError(f"changes.patch: forbidden path {value!r}")
        cleaned.add(value)
    if cleaned != set(writable): raise ControllerError("changes.patch paths differ from exact claim ownership")


def _find_result(root: Path) -> Path | None:
    candidates = [root / "result.json", root / "work/result.json", root / "work/_outbox/result.json"]
    present = [path for path in candidates if path.exists() or path.is_symlink()]
    if len(present) > 1:
        raws = [_regular(path, "worker result") for path in present]
        if any(raw != raws[0] for raw in raws[1:]): raise ControllerError("multiple conflicting worker results")
    return present[0] if present else None


def _command_fragments(value: Any) -> list[str]:
    fragments: list[str] = []
    if isinstance(value, dict):
        if value.get("type") == "custom_tool_call" and isinstance(value.get("input"), str):
            fragments.append(value["input"])
        if value.get("type") == "CommandExecution" and isinstance(value.get("command"), list):
            fragments.append("\n".join(str(part) for part in value["command"]))
        for child in value.values():
            if isinstance(child, (dict, list)):
                fragments.extend(_command_fragments(child))
    elif isinstance(value, list):
        for child in value:
            fragments.extend(_command_fragments(child))
    return fragments


def session_access_violation(record: dict[str, Any]) -> str | None:
    """Reject current-generation commands naming any predecessor or sibling task."""
    sessions = Path(record.get("codex_home", "")) / "sessions"
    if not sessions.exists(): return None
    if sessions.is_symlink() or not sessions.is_dir(): return "task_boundary:session_ledger_not_real_directory"
    own_root = os.path.normpath(str(Path(record["task_root"])))
    for path in sorted(sessions.rglob("*.jsonl")):
        if path.is_symlink() or not path.is_file(): return "task_boundary:session_ledger_not_regular"
        try:
            with path.open("r", encoding="utf-8", errors="replace") as stream:
                for line_number, line in enumerate(stream, 1):
                    try: event = json.loads(line)
                    except json.JSONDecodeError: continue
                    for text in _command_fragments(event):
                        for match in TASKS_NAMESPACE_RE.finditer(text):
                            referenced = os.path.normpath(match.group(0).rstrip(".,:"))
                            if referenced != own_root and not referenced.startswith(own_root + os.sep):
                                relative = Path(referenced).relative_to(ROOT).as_posix()
                                return f"task_boundary:foreign_task_root_reference:{relative}:{line_number}"
                        if RELATIVE_TASK_ESCAPE_RE.search(text):
                            return f"task_boundary:relative_task_root_escape:{path.name}:{line_number}"
        except OSError as exc:
            return f"task_boundary:session_ledger_unreadable:{exc.__class__.__name__}"
    return None


def task_boundary_violation(record: dict[str, Any]) -> str | None:
    """Reject work-tree and current-session cross-generation coupling."""
    work = Path(record["work_root"])
    if not work.is_dir() or work.is_symlink():
        return "task_boundary:missing_or_symlink_work_root"
    for path in work.rglob("*"):
        if path.name == ".git":
            return f"task_boundary:nested_git:{path.relative_to(work)}"
        if path.is_symlink() and path.is_dir():
            return f"task_boundary:symlink_directory:{path.relative_to(work)}"
    for candidate in work.rglob("*"):
        if not candidate.is_dir() or candidate.name.startswith("_"):
            continue
        names = {child.name for child in candidate.iterdir()}
        if {"lakefile.toml", "lean-toolchain"}.issubset(names) and ("README.md" in names or ".git" in names):
            return f"task_boundary:repository_sentinel:{candidate.relative_to(work)}"
    return session_access_violation(record)


def _append_harvest(body: dict[str, Any]) -> None:
    HARVEST_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with HARVEST_LEDGER.open("a+") as stream:
        stream.write(json.dumps(seal(body), sort_keys=True) + "\n"); stream.flush(); os.fsync(stream.fileno())


def harvest_record(record: dict[str, Any], specification: dict[str, Any]) -> bool:
    if record.get("status") not in {"materialized", "goal_submitted", "live", "handoff_ready"}: return False
    violation = task_boundary_violation(record)
    if violation:
        record["status"] = "generation_retire_required"; record["terminal_reason"] = "task_boundary_violation"; record["retired_reason"] = violation; record["harvest_error"] = "task boundary violation makes result ineligible"
        append_event("generation_retire_required", {k: record.get(k) for k in ("item_id", "claim_id", "run_id", "retired_reason")})
        return False
    root = Path(record["task_root"]); result_path = _find_result(root)
    if result_path is None: return False
    claim_path = root / "claim.json"
    try:
        validator = claim_checker_module(); result = validator.validate_result(result_path, claim_path); claim = json.loads(_regular(claim_path, "claim card")); patch_path = Path(result["patch"]["path"]); patch_raw = _regular(patch_path, "worker patch"); _patch_paths(patch_raw, result["changed_paths"])
        work = root / "work"
        artifacts = _result_artifacts(result, claim, work)
        baseline = result["baseline_sha256"]; patch_sha = result["patch"]["sha256"]; claim_id = result["claim_id"]; archive = HANDOFF_ARCHIVE / claim_id / baseline / patch_sha; queue = HANDOFF_QUEUE / claim_id / baseline / patch_sha
        file_set = sorted([
            ["claim.json", file_digest(claim_path), claim_path.stat().st_size],
            ["result.json", file_digest(result_path), result_path.stat().st_size],
            ["changes.patch", digest(patch_raw), len(patch_raw)],
            *[[artifact["archive_path"], artifact["sha256"], artifact["size_bytes"]] for artifact in artifacts],
        ])
        body = {"schema_version": "awesome-theorems/stage5-harvest-manifest/1.1", "program": PROGRAM, "item_id": result["item_id"], "claim_id": claim_id, "run_id": result["run_id"], "task_root": str(root), "baseline_sha256": baseline, "patch_sha256": patch_sha, "changed_paths": list(result["changed_paths"]), "artifacts": artifacts, "file_set": file_set, "file_set_sha256": digest(canonical(file_set)), "archive": archive.relative_to(ROOT).as_posix(), "queue": queue.relative_to(ROOT).as_posix()}; manifest = seal(body); manifest_raw = json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
        sources = [
            (claim_path, Path("claim.json"), "claim archive"),
            (result_path, Path("result.json"), "result archive"),
            (patch_path, Path("changes.patch"), "patch archive"),
            *[
                (
                    work / _safe_relative(artifact["path"], "owned artifact"),
                    _safe_relative(artifact["archive_path"], "archive artifact"),
                    "artifact archive",
                )
                for artifact in artifacts
            ],
        ]
        for destination_root in (archive, queue):
            _publish_handoff_tree(destination_root, sources, manifest_raw)
        entry = INTEGRATION_QUEUE / f"{result['item_id']}--{claim_id}--{result['run_id']}.json"; entry_body = seal({"schema_version": "awesome-theorems/stage5-integration-entry/1.0", "program": PROGRAM, "item_id": result["item_id"], "claim_id": claim_id, "run_id": result["run_id"], "queue": str(queue.relative_to(ROOT)), "baseline_sha256": baseline, "patch_sha256": patch_sha}); entry_raw = json.dumps(entry_body, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
        if entry.exists() and _regular(entry, "integration entry") != entry_raw: raise ControllerError("integration entry conflict")
        if not entry.exists(): atomic_write(entry, entry_raw, 0o444)
        _append_harvest(body); record.update({"status": "handoff_ready", "handoff": {"archive": str(archive), "queue": str(queue), "manifest_sha256": digest(manifest_raw)}, "handoff_ready_at": now()}); stop_record(record); append_event("handoff_harvested", {k: record.get(k) for k in ("item_id", "claim_id", "run_id", "handoff_ready_at", "handoff")}); return True
    except Exception as exc:
        record["harvest_error"] = str(exc); return False


def harvest_state(state: dict[str, Any], specification: dict[str, Any]) -> int:
    harvested = sum(
        1 for record in state.get("claims", {}).values()
        if record.get("runtime_authority_epoch") == RUNTIME_AUTHORITY_EPOCH
        and harvest_record(record, specification)
    )
    if harvested: save_state(state)
    return harvested


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def seal(body: dict[str, Any]) -> dict[str, Any]:
    value = dict(body)
    value["authority_sha256"] = digest(canonical(body))
    return value


def verify(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or not isinstance(value.get("authority_sha256"), str):
        raise ControllerError(f"{label}: malformed authority")
    body = dict(value); authority = body.pop("authority_sha256")
    if digest(canonical(body)) != authority:
        raise ControllerError(f"{label}: authority mismatch")
    return value


def checker_module():
    spec = importlib.util.spec_from_file_location("stage5_conjecture_blueprint_checker", CHECKER)
    if spec is None or spec.loader is None:
        raise ControllerError("conjecture checker unavailable")
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
    return module


def claim_checker_module():
    spec = importlib.util.spec_from_file_location("stage5_conjecture_claim_validator", CLAIM_CHECKER)
    if spec is None or spec.loader is None: raise ControllerError("conjecture claim validator unavailable")
    module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
    return module


def handoff_transition_module():
    spec = importlib.util.spec_from_file_location(
        "stage5_conjecture_handoff_pipeline", HANDOFF_TRANSITION
    )
    if spec is None or spec.loader is None:
        raise ControllerError("conjecture handoff transition unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_program() -> tuple[dict[str, Any], list[dict[str, Any]], bytes]:
    module = checker_module()
    specification, rows, raw = module.parse_blueprint()
    module.validate()
    return specification, rows, raw


def load_concurrency_prompt(path: Path, specification: dict[str, Any]) -> tuple[dict[str, Any], str]:
    raw = _regular(path, "concurrency prompt")
    value = json.loads(raw)
    if not isinstance(value, dict) or value.get("schema_version") != CONCURRENCY_SCHEMA or value.get("program") != PROGRAM:
        raise ControllerError("explicit concurrency prompt schema/program differs")
    body = dict(value); authority = body.pop("authority_sha256", None)
    if not isinstance(authority, str) or digest(canonical(body)) != authority:
        raise ControllerError("explicit concurrency prompt seal differs")
    vector = value.get("concurrency")
    if not isinstance(vector, dict) or frozenset(vector) != CONCURRENCY_DIMENSIONS:
        raise ControllerError("prompt must provide the complete concurrency vector")
    for key, item in vector.items():
        if item != "not_applicable" and (isinstance(item, bool) or not isinstance(item, int) or item < 0):
            raise ControllerError(f"prompt concurrency dimension {key} is invalid")
    if value.get("policy_epoch") != "stage5-conjecture-concurrency-prompt-2026-08-16-sol-lifecycle-3":
        raise ControllerError("stale concurrency prompt policy epoch")
    if value.get("execution_spec_sha256") != digest(canonical(specification)):
        raise ControllerError("explicit concurrency prompt is not bound to the authoritative execution specification")
    contract = specification.get("concurrency_prompt_contract")
    if not isinstance(contract, dict):
        raise ControllerError("authoritative concurrency prompt contract is missing")
    if value.get("source") != "explicit operator prompt fixture; not a controller or Blueprint default":
        raise ControllerError("explicit concurrency prompt source boundary differs")
    if value.get("execution_limits") != contract.get("execution_limits"):
        raise ControllerError("explicit concurrency prompt execution limits differ from the specification")
    if value.get("recovery") != contract.get("recovery"):
        raise ControllerError("explicit concurrency prompt recovery policy differs from the specification")
    if value.get("request_window_seconds") != 120:
        raise ControllerError("explicit concurrency prompt request window differs")
    return value, digest(raw)


def atomic_write(path: Path, raw: bytes, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        os.chmod(temporary, mode); os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try: os.fsync(directory)
        finally: os.close(directory)
    finally:
        if os.path.exists(temporary): os.unlink(temporary)


def atomic_json(path: Path, value: Any, mode: int = 0o600) -> None:
    atomic_write(path, json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n", mode)


def load_state(create: bool = True) -> dict[str, Any]:
    if not STATE.exists():
        if not create: return {"claims": {}, "generation_history": []}
        value = seal({"schema_version": "awesome-theorems/stage5-conjecture-v2-state/1.0", "program": PROGRAM, "runtime_authority_epoch": RUNTIME_AUTHORITY_EPOCH, "claims": {}, "generation_history": [], "updated_at": now()})
        atomic_json(STATE, value); return value
    return verify(json.loads(STATE.read_text()), "conjecture controller state")


def save_state(state: dict[str, Any]) -> None:
    body = dict(state); body.pop("authority_sha256", None); body["updated_at"] = now(); atomic_json(STATE, seal(body))


@contextmanager
def scheduler_guard(nonblocking: bool = True):
    """Serialize controller transitions with reviewed Blueprint migrations."""
    SCHEDULER_LOCK.parent.mkdir(parents=True, exist_ok=True)
    with SCHEDULER_LOCK.open("a+") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | (fcntl.LOCK_NB if nonblocking else 0))
        except BlockingIOError as exc:
            raise ControllerError("conjecture scheduler transition already in progress") from exc
        try:
            yield
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def tmux(record: dict[str, Any], *args: str, check: bool = True, input_text: str | None = None, timeout: float = 30) -> subprocess.CompletedProcess[str]:
    # Relative socket + task-root cwd keeps the Unix socket task-local and
    # avoids any accidental shared server namespace.
    return subprocess.run(["/usr/bin/tmux", "-S", "tmux.sock", *args], cwd=record["task_root"], input=input_text, text=True, capture_output=True, check=check, timeout=timeout)


def proc_ticks(pid: int) -> int | None:
    try: return int(Path(f"/proc/{pid}/stat").read_text().split(") ", 1)[1].split()[19])
    except (OSError, ValueError, IndexError): return None


def proc_env(pid: int, key: str) -> str | None:
    try:
        for entry in Path(f"/proc/{pid}/environ").read_bytes().split(b"\0"):
            if entry.startswith(key.encode() + b"="): return entry.split(b"=", 1)[1].decode()
    except (OSError, UnicodeDecodeError): pass
    return None


def proc_cmdline(pid: int) -> str:
    try: return Path(f"/proc/{pid}/cmdline").read_bytes().replace(b"\0", b" ").decode()
    except (OSError, UnicodeDecodeError): return ""


def append_event(event: str, payload: dict[str, Any]) -> None:
    RUNTIME.joinpath("ledgers").mkdir(parents=True, exist_ok=True); RUNTIME.joinpath("locks").mkdir(parents=True, exist_ok=True)
    with EVENT_LOCK.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        lines = [line for line in EVENTS.read_text().splitlines() if line] if EVENTS.exists() else []
        body = {"schema_version": "awesome-theorems/stage5-conjecture-v2-event/1.0", "seq": len(lines)+1, "event_id": str(uuid.uuid4()), "event": event, "program": PROGRAM, "at": now(), "previous_record_sha256": digest(lines[-1].encode()) if lines else None, "payload": payload}
        with EVENTS.open("a") as stream:
            stream.write(json.dumps(seal(body), sort_keys=True) + "\n"); stream.flush(); os.fsync(stream.fileno())
        fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def acquire_leases(record: dict[str, Any], vector: dict[str, Any]) -> None:
    RUNTIME.joinpath("ledgers").mkdir(parents=True, exist_ok=True); RUNTIME.joinpath("locks").mkdir(parents=True, exist_ok=True)
    with LEASE_LOCK.open("a+") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        for path, kind in ((REQUESTS, "outbound_request"), (TURNS, "running_turn")):
            rows = [json.loads(line) for line in path.read_text().splitlines() if line] if path.exists() else []
            cap_key = "outbound_request_starts_per_window" if kind == "outbound_request" else "running_turns"
            cap = vector.get(cap_key)
            if not isinstance(cap, int) or isinstance(cap, bool) or cap <= 0:
                raise ControllerError(f"explicit prompt cap is invalid for {kind}")
            now_epoch = time.time()
            if kind == "outbound_request":
                in_window = sum(
                    row.get("status") == "leased"
                    and now_epoch - float(row.get("acquired_epoch", 0)) < 120
                    for row in rows if isinstance(row, dict)
                )
                if in_window >= cap:
                    raise ControllerError("outbound request-start window is saturated")
            elif sum(row.get("status") == "leased" for row in rows if isinstance(row, dict)) >= cap:
                raise ControllerError("running-turn prompt cap is saturated")
            if any(row.get("status") == "leased" and row.get("run_id") == record["run_id"] for row in rows):
                raise ControllerError(f"duplicate {kind} lease refused")
            acquired = time.time()
            value = seal({"schema_version": "awesome-theorems/stage5-conjecture-v2-lease/1.0", "kind": kind, "program": PROGRAM, "item_id": record["item_id"], "claim_id": record["claim_id"], "run_id": record["run_id"], "execution_id": record["run_id"], "lease_id": str(uuid.uuid4()), "status": "leased", "prompt_cap_dimension": cap_key, "prompt_cap": cap, "acquired_epoch": acquired, "acquired_at": datetime.fromtimestamp(acquired, timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ"), "expires_at": datetime.fromtimestamp(acquired + 900, timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")})
            with path.open("a") as stream:
                stream.write(json.dumps(value, sort_keys=True) + "\n"); stream.flush(); os.fsync(stream.fileno())
            record[f"{kind}_lease_id"] = value["lease_id"]
        fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def codex_argv(work: Path) -> list[str]:
    return [str(CODEX), "-C", str(work), "-c", "features.goals=true", "--no-alt-screen", "-m", MODEL, "-c", f"model_reasoning_effort={EFFORT}", "-c", f"service_tier={SERVICE_TIER}", "-c", f"model_provider={PROVIDER}"]


def bootstrap_home(home: Path) -> None:
    if not AUTH.is_file() or AUTH.is_symlink() or not CONFIG.is_file() or CONFIG.is_symlink(): raise ControllerError("Codex credentials/config unavailable")
    source = tomllib.loads(CONFIG.read_text()); providers = source.get("model_providers", {}); provider = providers.get(PROVIDER) or providers.get("OpenAI")
    if not isinstance(provider, dict) or not isinstance(provider.get("base_url"), str): raise ControllerError("provider config incomplete")
    home.mkdir(parents=True, exist_ok=False, mode=0o700); shutil.copyfile(AUTH, home / "auth.json"); os.chmod(home / "auth.json", 0o600)
    config = f'model_provider = "{PROVIDER}"\nmodel = "{MODEL}"\nmodel_reasoning_effort = "{EFFORT}"\nservice_tier = "{SERVICE_TIER}"\napproval_policy = "never"\nsandbox_mode = "danger-full-access"\nnetwork_access = "enabled"\n[model_providers.{PROVIDER}]\nname = {json.dumps(provider.get("name", PROVIDER))}\nbase_url = {json.dumps(provider["base_url"])}\nwire_api = "responses"\nsupports_websockets = {str(bool(provider.get("supports_websockets", False))).lower()}\nrequires_openai_auth = {str(bool(provider.get("requires_openai_auth", True))).lower()}\n[features]\ngoals = true\nmulti_agent = false\nmulti_agent_v2 = false\n'
    atomic_write(home / "config.toml", config.encode(), 0o600)


def materialize(
    item: dict[str, Any], specification: dict[str, Any], blueprint_raw: bytes,
    generation_id: str | None = None, lane_id: str | None = None,
    prompt: dict[str, Any] | None = None, prompt_digest: str | None = None,
) -> dict[str, Any]:
    claim_id = f"{item['item_id']}--worker"; run_id = generation_id or f"r-{int(time.time())}-{uuid.uuid4().hex[:8]}"; root = RUNTIME / "tasks" / claim_id / run_id; work = root / "work"; home = root / "codex-home"
    root.mkdir(parents=True, exist_ok=False, mode=0o700); work.mkdir(mode=0o700)
    for rel in item["owned_paths"]: (work / rel).parent.mkdir(parents=True, exist_ok=True)
    # Bind a small, immutable, program-local bootstrap set.  The claim schema
    # requires every read-only input to carry its digest and size; omitting it
    # would make a freshly admitted conjecture claim unverifiable at harvest.
    workset_value = json.loads(_regular(EVIDENCE / "workset-5.6.json", "workset"))
    workset_members = [
        member for member in workset_value.get("members", [])
        if isinstance(member, dict) and member.get("target_item_id") == item["item_id"]
    ] if isinstance(workset_value, dict) else []
    if len(workset_members) != 1:
        raise ControllerError("exact workset member binding is missing or ambiguous")
    workset_member = workset_members[0]
    source_record_sha = workset_member.get("record_sha256")
    if not isinstance(source_record_sha, str) or not re.fullmatch(r"[0-9a-f]{64}", source_record_sha):
        raise ControllerError("workset member source-record digest differs")
    workset_member_binding = {
        "member_id": workset_member["member_id"],
        "member_kind": workset_member["member_kind"],
        "target_item_id": workset_member["target_item_id"],
        "workset_record_sha256": workset_member["workset_record_sha256"],
        "source_record_sha256": source_record_sha,
    }
    exact_member_raw = json.dumps(workset_member, ensure_ascii=False, sort_keys=True, indent=2).encode() + b"\n"
    exact_member_path = work / "_baseline/workset-member.json"
    atomic_write(exact_member_path, exact_member_raw, 0o444)
    copy_paths = [
        (BLUEPRINT, "Stage5_Conjectures_Blueprint.md"),
        (EVIDENCE / "workset-5.6-receipt.json", "workset-5.6-receipt.json"),
        (EVIDENCE / "execution-spec.json", "execution-spec.json"),
        (EVIDENCE / "foundation-profiles.json", "foundation-profiles.json"),
        (EVIDENCE / "provider-registry.json", "provider-registry.json"),
        (EVIDENCE / "claim-card.schema.json", "claim-card.schema.json"),
        (EVIDENCE / "worker-result.schema.json", "worker-result.schema.json"),
        (EVIDENCE / "master-acceptance.schema.json", "master-acceptance.schema.json"),
        (CONCURRENCY_PROMPT, "concurrency-prompt.json"),
        (ROOT / "Docs/catalog/v5/pools/Current_Pool_Release.json", "Current_Pool_Release.json"),
        (ROOT / "Docs/catalog/v5/pools/conjecturebench-357bcb1a/Pool_Manifest.json", "Pool_Manifest.json"),
    ]
    bootstrap_files: list[dict[str, Any]] = [{"path": "_baseline/workset-member.json", "sha256": digest(exact_member_raw), "size_bytes": len(exact_member_raw)}]
    if workset_member.get("member_kind") == "source_occurrence_intake":
        archive_path = ROOT / "Docs/catalog/v5/sources/conjecturebench-357bcb1a-full-source.tar.gz"
        pool_path = ROOT / "Docs/catalog/v5/pools/conjecturebench-357bcb1a/Source_Occurrence_Pool.jsonl"
        pool_rows = [json.loads(line) for line in _regular(pool_path, "occurrence pool").splitlines()]
        occurrences = [row for row in pool_rows if row.get("pool_id") == workset_member.get("pool_id")]
        if len(occurrences) != 1:
            raise ControllerError("exact occurrence source record is missing or ambiguous")
        occurrence = occurrences[0]
        top = "conjecture-bench-357bcb1a1daf93917d42e8206ceaa55645729a09"
        member_name = f"{top}/{occurrence['record_path']}"
        with tarfile.open(archive_path, "r:gz") as archive:
            member_info = archive.getmember(member_name)
            if not member_info.isfile() or member_info.issym() or member_info.islnk():
                raise ControllerError("occurrence source archive member is unsafe")
            stream = archive.extractfile(member_info)
            if stream is None:
                raise ControllerError("occurrence source archive member is unreadable")
            source_value = json.loads(stream.read())
        if occurrence.get("kind") == "family":
            index = occurrence.get("family_container_index")
            records = source_value.get("records") if isinstance(source_value, dict) else None
            if isinstance(index, bool) or not isinstance(index, int) or not isinstance(records, list) or not 0 <= index < len(records):
                raise ControllerError("occurrence family record pointer differs")
            source_value = records[index]
        source_raw = canonical(source_value)
        if digest(source_raw) != workset_member.get("record_sha256"):
            raise ControllerError("occurrence source record digest differs from the workset")
        source_path = work / "_baseline/source-record.json"
        atomic_write(source_path, source_raw + b"\n", 0o444)
        bootstrap_files.append({
            "path": "_baseline/source-record.json",
            "sha256": file_digest(source_path),
            "size_bytes": source_path.stat().st_size,
        })
    for source, name in copy_paths:
        if source.is_symlink() or not source.is_file():
            raise ControllerError(f"missing conjecture bootstrap file: {source}")
        target = work / "_baseline" / name
        atomic_write(target, source.read_bytes(), 0o444)
        bootstrap_files.append({"path": f"_baseline/{name}", "sha256": file_digest(target), "size_bytes": target.stat().st_size})
    bootstrap_home(home)
    maxima = specification["operator_budget_policy"]["finite_initial_allowances"]["per_claim_maxima"]
    owned = list(item["owned_paths"])
    search_prompt = specification.get("conjecture_proof_search_prompt")
    if not isinstance(search_prompt, dict):
        raise ControllerError("conjecture proof-search prompt contract is missing")
    intake_contract = specification.get("conjecture_occurrence_intake_contract")
    if not isinstance(intake_contract, dict):
        raise ControllerError("conjecture occurrence-intake contract is missing")
    is_intake = bool(re.fullmatch(r"S5CON-POOL-[0-9]{8}-INTAKE", item["item_id"]))
    work_contract = (
        {"kind": "source_occurrence_intake", "source_occurrence_intake": intake_contract}
        if is_intake
        else {"kind": "strict_resolution_proof_search", "strict_resolution_proof_search": search_prompt}
    )
    if prompt is None:
        prompt, prompt_digest = load_concurrency_prompt(CONCURRENCY_PROMPT, specification)
    if not isinstance(prompt_digest, str) or re.fullmatch(r"[0-9a-f]{64}", prompt_digest) is None:
        raise ControllerError("claim concurrency prompt digest is missing or inconsistent")
    requested_concurrency = prompt.get("concurrency")
    if not isinstance(requested_concurrency, dict) or frozenset(requested_concurrency) != CONCURRENCY_DIMENSIONS:
        raise ControllerError("claim concurrency vector is incomplete")
    budget: dict[str, int | str] = {}
    for key in ("model_input_tokens", "model_output_tokens", "model_turns", "external_launches", "wall_seconds", "cpu_seconds"):
        value = maxima.get(key)
        if key == "model_turns":
            if value != "unbounded":
                raise ControllerError("model_turns must be explicitly unbounded")
            budget[key] = "unbounded"
        else:
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ControllerError(f"invalid finite per-claim budget: {key}")
            budget[key] = value
    card = {
        "schema_version": "awesome-theorems/stage5-proof-debt-claim-card/1.1",
        "program": PROGRAM, "claim_id": claim_id, "run_id": run_id,
        "item_id": item["item_id"], "mode": ("POOL-INTAKE" if item["item_id"].startswith("S5CON-POOL-") else "TARGET-TARGET"),
        "dependencies": list(item["dependencies"]),
        "baseline": {
            "execution_spec_sha256": digest(canonical(specification)),
            "blueprint_sha256": digest(blueprint_raw),
            "source_bundle_sha256": specification["source_bundle"]["sha256"],
            "dependency_state_sha256": digest(canonical([[x, "master_accepted"] for x in item["dependencies"]])),
            "owned_paths_baseline_sha256": digest(canonical([[x, None] for x in owned])),
        },
        "deadline": "2027-08-12T00:00:00Z", "task_root": str(root),
        "canonical_repository_root": str(ROOT), "canonical_write_policy": "forbidden",
        "writable_paths": owned, "read_only_bootstrap_files": bootstrap_files,
        "deliverable": item["title"] + ". " + item["gate"],
        "execution_identity": {
            "lane_id": lane_id or item["item_id"],
            "generation_id": run_id,
            "prompt_epoch": prompt["policy_epoch"],
            "prompt_digest": prompt_digest,
            "execution_spec_sha256": digest(canonical(specification)),
            "requested_concurrency": dict(requested_concurrency),
            "resolved_concurrency": dict(requested_concurrency),
        },
        "workset_member": workset_member_binding,
        "work_contract": work_contract,
        "validation_commands": [{"command_id": "claim-self-check", "cwd": ".", "argv": ["/usr/bin/python3", "-I", "-B", "-c", "pass"], "environment": [], "timeout_seconds": 30, "network": "denied"}],
        "artifact_policy": {"allowed_paths": owned, "required_paths": owned, "forbidden_paths": ["Docs/Stage5_Conjectures_Blueprint.md", "Docs/Stage5_Conjectures_Gantt.md", "Docs/catalog", ".git", ".ops"]},
        "result_schema": {"path": "Docs/evidence/stage5_conjectures/worker-result.schema.json", "schema_id": "https://awesome-theorems.invalid/schemas/stage5-conjecture-worker-result-1.0.json", "sha256": file_digest(EVIDENCE / "worker-result.schema.json")},
        "resource_budget": budget,
        "retry_budget": {"attempt": 1, "max_attempts": 3},
    }
    # Claim-card schema is deliberately an unsealed immutable document; its
    # byte digest is bound by the worker result.  Adding an authority field
    # here would violate the closed schema and make every future claim
    # unverifiable.
    atomic_json(root / "claim.json", card, 0o444)
    return {"item_id": item["item_id"], "claim_id": claim_id, "run_id": run_id, "generation_id": run_id, "lane_id": lane_id or item["item_id"], "task_root": str(root), "work_root": str(work), "codex_home": str(home), "socket_path": str(root / "tmux.sock"), "socket_argument": "tmux.sock", "session": "s5con-" + digest(f"{claim_id}/{run_id}".encode())[:20], "status": "materialized", "goal_submissions": 0}


def build_goal_objective(record: dict[str, Any], token: str) -> str:
    """Build the sole short goal from the immutable claim-card contract."""
    claim_path = Path(record["task_root"]) / "claim.json"
    card = json.loads(_regular(claim_path, "claim card"))
    work_contract = card.get("work_contract")
    if not isinstance(work_contract, dict):
        raise ControllerError("claim-card work contract is missing")
    kind = work_contract.get("kind")
    contract = work_contract.get(str(kind))
    clause = contract.get("short_goal_clause") if isinstance(contract, dict) else None
    if not isinstance(clause, str) or not clause.strip():
        raise ControllerError("claim-card work-mode short goal clause is missing")
    objective = (
        f"/goal Execute only {record['item_id']} as {record['claim_id']}. "
        "Read immutable ../claim.json and obey its exact deliverable, work-mode protocol, "
        "ownership, validation, evidence and budget. Work only in this task root; never inspect "
        "another task root or mathematical ID, and never use collaboration tools, child agents or "
        f"child threads. {clause} Complete and self-test the target-local handoff. {token}"
    )
    if len(objective.encode("utf-8")) > 768:
        raise ControllerError("/goal objective exceeds the 768-byte short-goal boundary")
    return objective


def submit(record: dict[str, Any], vector: dict[str, Any]) -> None:
    if record.get("goal_submissions") != 0: raise ControllerError("duplicate /goal refused")
    target = f"{record['session']}:0.0"
    tmux(record, "-f", "/dev/null", "new-session", "-d", "-s", record["session"], "-c", record["work_root"], "env", "-u", "CODEX_CI", "-u", "CODEX_THREAD_ID", "-u", "CODEX_REMOTE_PAYLOAD", f"CODEX_HOME={record['codex_home']}", *codex_argv(Path(record["work_root"])))
    record["pane_pid"] = int(tmux(record, "display-message", "-p", "-t", target, "#{pane_pid}").stdout.strip()); record["pane_pid_start_ticks"] = proc_ticks(record["pane_pid"])
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        pane = tmux(record, "capture-pane", "-p", "-J", "-t", target, check=False).stdout.lower()
        if "trust" in pane and ("yes" in pane or "enter" in pane): tmux(record, "send-keys", "-t", target, "Enter")
        if ">" in pane or "ask codex" in pane: break
        time.sleep(.5)
    token = "GOAL_READY_" + digest(f"{record['claim_id']}/{record['run_id']}".encode())[:24].upper()
    objective = build_goal_objective(record, token)
    tmux(record, "load-buffer", "-b", "goal", "-", input_text=objective); tmux(record, "paste-buffer", "-b", "goal", "-t", target)
    for _ in range(120):
        if token in tmux(record, "capture-pane", "-p", "-J", "-t", target, check=False).stdout: break
        time.sleep(.25)
    else: raise ControllerError("goal completion token not visible")
    acquire_leases(record, vector); tmux(record, "send-keys", "-t", target, "Enter"); record["goal_submissions"] = 1; record["status"] = "goal_submitted"; record["goal_token"] = token; append_event("goal_submitted", {k: record.get(k) for k in ("item_id", "claim_id", "run_id", "session", "pane_pid", "pane_pid_start_ticks", "goal_token")})


def identity(record: dict[str, Any]) -> dict[str, Any] | None:
    db = Path(record["codex_home"]) / "state_5.sqlite"; goals = Path(record["codex_home"]) / "goals_1.sqlite"
    if not db.is_file() or not goals.is_file(): return None
    try:
        c = sqlite3.connect(f"file:{db}?mode=ro", uri=True); thread = c.execute("select id,cwd,model_provider,model,reasoning_effort from threads order by rowid desc limit 1").fetchone(); c.close()
        g = sqlite3.connect(f"file:{goals}?mode=ro", uri=True); goal = g.execute("select goal_id,objective,status from thread_goals where thread_id=?", (thread[0],)).fetchone() if thread else None; g.close()
        if not thread or not goal: return None
        return {"thread_id": thread[0], "cwd": thread[1], "provider": thread[2], "model": thread[3], "reasoning_effort": thread[4], "goal_id": goal[0], "goal_objective": goal[1], "goal_status": goal[2]}
    except sqlite3.Error: return None


def authenticate(record: dict[str, Any]) -> bool:
    pid = int(record["pane_pid"]); argv = proc_cmdline(pid); ident = identity(record)
    if proc_ticks(pid) != record.get("pane_pid_start_ticks") or proc_env(pid, "CODEX_HOME") != record["codex_home"] or f"-c service_tier={SERVICE_TIER}" not in argv or f"-c model_provider={PROVIDER}" not in argv: return False
    if not ident or ident["cwd"] != record["work_root"] or ident["provider"] != PROVIDER or ident["model"] != MODEL or ident["reasoning_effort"] != EFFORT or ident["goal_status"] != "active": return False
    if record["item_id"] not in ident["goal_objective"] or record["claim_id"] not in ident["goal_objective"]: return False
    record.update(ident); record["service_tier"] = SERVICE_TIER; record["status"] = "live"; record["authenticated_at"] = now(); append_event("claim_live", {k: record.get(k) for k in ("item_id", "claim_id", "run_id", "thread_id", "goal_id", "pane_pid")}); return True


def reconcile_record(record: dict[str, Any]) -> str:
    """Retire only this generation when its goal or task boundary is terminal."""
    violation = task_boundary_violation(record)
    if violation:
        record["status"] = "generation_retire_required"
        record["terminal_reason"] = "task_boundary_violation"
        record["retired_reason"] = violation
        append_event("generation_retire_required", {k: record.get(k) for k in ("item_id", "claim_id", "run_id", "retired_reason")})
        return record["status"]
    ident = identity(record)
    if not ident:
        return record.get("status", "unknown")
    record.update(ident)
    if ident["goal_status"] == "active":
        return "live" if authenticate(record) else record.get("status", "goal_submitted")
    if ident["goal_status"] in {"blocked", "complete", "completed", "failed", "stopped"}:
        record["status"] = "generation_retire_required"
        record["terminal_reason"] = "goal_terminal"
        record["retired_reason"] = f"goal_terminal:{ident['goal_status']}"
        append_event("generation_retire_required", {k: record.get(k) for k in ("item_id", "claim_id", "run_id", "retired_reason")})
    return record["status"]


def stop_record(record: dict[str, Any]) -> None:
    try: tmux(record, "kill-server", check=False, timeout=10)
    except Exception: pass
    socket_value = record.get("socket_argument", "tmux.sock")
    socket_path = Path(record["task_root"]) / socket_value
    try:
        if socket_path.is_socket() and not socket_path.is_symlink():
            socket_path.unlink()
    except OSError:
        pass
    record["transport_stopped_at"] = now()


def fence_orphaned_generations(state: dict[str, Any]) -> int:
    """Stop only controller-owned task-local tmux roots lost from the registry."""
    tasks_root = RUNTIME / "tasks"
    if not tasks_root.is_dir():
        return 0
    current = {str(v.get("task_root")) for v in state.get("claims", {}).values()
               if v.get("status") in {"materialized", "goal_submitted", "live", "generation_retire_required"}}
    fenced = 0
    for claim_dir in sorted(tasks_root.glob("*--worker")):
        if not claim_dir.is_dir():
            continue
        for run_root in sorted(p for p in claim_dir.iterdir() if p.is_dir()):
            if str(run_root) in current:
                continue
            claim_path, socket_path = run_root / "claim.json", run_root / "tmux.sock"
            if not claim_path.is_file() or not socket_path.is_socket() or socket_path.is_symlink():
                continue
            try:
                card = json.loads(claim_path.read_text())
                if card.get("claim_id") != claim_dir.name:
                    continue
                record = {"task_root": str(run_root), "socket_argument": "tmux.sock"}
                tmux(record, "kill-server", check=False, timeout=10)
                if socket_path.is_socket() and not socket_path.is_symlink():
                    socket_path.unlink()
                append_event("orphan_generation_fenced", {
                    "item_id": card.get("item_id"), "claim_id": card.get("claim_id"),
                    "run_id": card.get("run_id"), "task_root": str(run_root),
                })
                fenced += 1
            except (OSError, ValueError, json.JSONDecodeError):
                continue
    return fenced


def append_runtime_snapshot(state: dict[str, Any], prompt: dict[str, Any] | None = None, prompt_digest: str | None = None) -> None:
    """Write the program-local snapshot with the same schema used by Gantt."""
    claims = state.get("claims", {})
    specification, rows, blueprint_raw = load_program()
    workset_raw = _regular(EVIDENCE / "workset-5.6.json", "workset")
    current_epoch = state.get("runtime_authority_epoch")
    items = {}
    for item_id, value in claims.items():
        if value.get("runtime_authority_epoch") != RUNTIME_AUTHORITY_EPOCH:
            continue
        status = value.get("status", "unknown")
        worker = {
            "claim_id": value.get("claim_id"), "run_id": value.get("run_id"),
            "owner": "codex-worker", "status": status,
            "startup": status in {"materialized", "goal_submitted"},
            "live": status == "live", "running": status == "live",
            "tmux_socket": value.get("socket_path", str(Path(value.get("task_root", "")) / "tmux.sock")),
            "tmux_session": value.get("session"), "codex_home": value.get("codex_home"),
            "thread_id": value.get("thread_id"), "goal_id": value.get("goal_id"),
            "provider": value.get("provider"), "model": value.get("model"),
            "reasoning_effort": value.get("reasoning_effort"), "service_tier": value.get("service_tier"),
            "budget": value.get("budget"), "handoff": value.get("handoff"),
        }
        # The manager's same-name Gantt consumes this flat runtime projection;
        # keep the worker identity explicit while preserving one row per TARGET.
        items[item_id] = {**worker, "claim_id": worker["claim_id"], "run_id": worker["run_id"], "owner": worker["owner"], "status": worker["status"], "startup": worker["startup"], "live": worker["live"], "running": worker["running"], "handoff": worker["handoff"], "block": value.get("underfill"), "integration": value.get("integration"), "repair": value.get("repair"),
                          "timing": {"status": "recorded" if value.get("goal_submitted_at") else "unscheduled", "start": value.get("goal_submitted_at"), "end": value.get("authenticated_at"), "duration_seconds": None, "source": "controller-state" if value.get("goal_submitted_at") else None}}
    active = [v for v in claims.values() if v.get("runtime_authority_epoch") == RUNTIME_AUTHORITY_EPOCH and v.get("status") in {"materialized", "goal_submitted", "live"}]
    observed = {"logical_claims": len(active), "starting_lanes": sum(v.get("status") in {"materialized", "goal_submitted"} for v in active), "authenticated_live_goals": sum(v.get("status") == "live" for v in active), "running_turns": sum(v.get("status") == "live" for v in active), "canonical_integrations": 0, "lean_build_validators": 0, "external_launches_this_wave": state.get("external_launches_this_wave", 0), "in_flight_requests": 0, "outstanding_requests": sum(v.get("status") in {"goal_submitted", "live"} for v in active), "unauthorized_continuations": state.get("unauthorized_continuations", 0), "breaker": state.get("breaker", {"state": "closed"})}
    vector = prompt.get("concurrency") if prompt else None
    live_cap = vector.get("authenticated_goals") if isinstance(vector, dict) and isinstance(vector.get("authenticated_goals"), int) else None
    body = {"schema_version": "awesome-theorems/stage5-runtime-snapshot/2.0", "program": PROGRAM, "runtime_authority_epoch": RUNTIME_AUTHORITY_EPOCH, "snapshot_id": str(uuid.uuid4()), "generated_at": now(), "state_sha256": digest(canonical(state)), "blueprint_sha256": digest(blueprint_raw), "execution_spec_sha256": digest(canonical(specification)), "checklist_dag_sha256": digest(canonical([{"item_id": row["item_id"], "dependencies": row["dependencies"], "owned_paths": row["owned_paths"], "task_authority_sha256": digest(canonical({"item_id": row["item_id"], "title": row["title"], "dependencies": row["dependencies"], "owned_paths": row["owned_paths"], "gate": row["gate"]}))} for row in rows])), "workset_sha256": digest(workset_raw), "items": items, "prompt_epoch": prompt.get("policy_epoch") if prompt else state.get("prompt_epoch"), "prompt_digest": prompt_digest if prompt_digest is not None else state.get("prompt_digest"), "requested_concurrency": vector if vector is not None else state.get("requested_concurrency"), "effective_concurrency": state.get("effective_concurrency", vector), "observed_usage": observed, "saturated_dimensions": [k for k,v in observed.items() if k in {"logical_claims", "starting_lanes", "authenticated_live_goals", "running_turns"} and isinstance(live_cap, int) and v >= live_cap], "underfill": state.get("underfill", {"authenticated_live_goal_slots": (max(0, live_cap-observed["authenticated_live_goals"]) if isinstance(live_cap, int) else None), "binding_reasons": (["BOOT_not_accepted", "controller_not_activated"] if prompt else ["concurrency_prompt_required"])}), "status_counts": {"live": observed["authenticated_live_goals"], "starting": observed["starting_lanes"]}}
    atomic_json(RUNTIME / "status/runtime-snapshot.json", seal(body), 0o644)
    # The generated Gantt is refreshed only after the complete state snapshot.
    generator_path = ROOT / "Docs/tools/generate_stage5_conjectures_gantt.py"
    spec = importlib.util.spec_from_file_location("stage5_conjecture_gantt_projection", generator_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec); sys.modules[spec.name] = module; spec.loader.exec_module(module)
        atomic_write(GANTT, module.render())


def validate_only(concurrency_prompt: Path | None = None) -> dict[str, Any]:
    try: spec, rows, raw = load_program()
    except Exception as exc: return {"valid": False, "errors": [str(exc)], "program": PROGRAM, "transport": TRANSPORT}
    if concurrency_prompt is None:
        return {"valid": False, "errors": ["concurrency prompt is required"], "program": PROGRAM, "transport": TRANSPORT}
    try: prompt, prompt_digest = load_concurrency_prompt(concurrency_prompt, spec)
    except Exception as exc: return {"valid": False, "errors": [str(exc)], "program": PROGRAM, "transport": TRANSPORT}
    target_count = sum(row["item_id"].endswith("-TARGET") for row in rows)
    intake_count = sum(row["item_id"].startswith("S5CON-POOL-") and row["item_id"].endswith("-INTAKE") for row in rows)
    return {"valid": True, "errors": [], "program": PROGRAM, "items": len(rows), "execution_members": target_count + intake_count, "strict_resolution_targets": target_count, "source_occurrence_intake_targets": intake_count, "transport": TRANSPORT, "goal_command": GOAL_COMMAND, "route": {"provider": PROVIDER, "model": MODEL, "reasoning_effort": EFFORT, "service_tier": SERVICE_TIER}, "concurrency_prompt": {"path": str(concurrency_prompt), "digest": prompt_digest, "epoch": prompt.get("policy_epoch"), "requested": prompt["concurrency"]}, "runtime_presence": RUNTIME.exists()}


def _reserve_workers_locked(concurrency_prompt: Path) -> dict[str, Any]:
    specification, rows, raw = load_program()
    prompt, prompt_digest = load_concurrency_prompt(concurrency_prompt, specification)
    vector = prompt["concurrency"]
    worker_cap_dimensions = (
        "logical_claims", "agent_executions", "startup_reservations",
        "live_transports", "authenticated_goals", "running_turns",
        "outbound_request_starts_per_window", "in_flight_requests",
    )
    caps = [vector.get(key) for key in worker_cap_dimensions]
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in caps):
        raise ControllerError("complete worker-cap vector is invalid")
    fanout = vector.get("launch_fanout_per_wave")
    if not isinstance(fanout, int) or isinstance(fanout, bool) or fanout < 0:
        raise ControllerError("launch fanout prompt cap is invalid")
    cap = min(caps)
    if cap == 0 or fanout == 0:
        raise ControllerError("explicit concurrency prompt admits zero worker launches")
    if vector.get("exact_path_conflicts") != 0:
        raise ControllerError("nonzero exact-path-conflict budget is forbidden")
    if specification.get("operator_budget_policy", {}).get("worker_launch_authorized") is not True:
        raise ControllerError("worker launch is not authorized by the embedded operator policy")
    if specification.get("operator_budget_policy", {}).get("external_spend_authorized") is not True:
        raise ControllerError("external spend is not authorized by the embedded operator policy")
    if rows[0]["state"] != "x": raise ControllerError("conjecture BOOT must be Master accepted before worker launch")
    RUNTIME.mkdir(parents=True, exist_ok=True); state = load_state()
    if state.get("runtime_authority_epoch") != RUNTIME_AUTHORITY_EPOCH:
        raise ControllerError("controller state belongs to a historical runtime authority epoch")
    harvested = harvest_state(state, specification); orphaned = fence_orphaned_generations(state)
    for record in state.get("claims", {}).values():
        if record.get("runtime_authority_epoch") != RUNTIME_AUTHORITY_EPOCH: continue
        if record.get("status") in {"materialized", "goal_submitted", "live"}: reconcile_record(record)
    for old in state.get("claims", {}).values():
        if old.get("runtime_authority_epoch") != RUNTIME_AUTHORITY_EPOCH: continue
        if old.get("status") == "generation_retire_required":
            stop_record(old); old["status"] = "retired"; old["retired_epoch"] = time.time(); state.setdefault("generation_history", []).append(dict(old))
    active = [v for v in state.get("claims", {}).values() if v.get("runtime_authority_epoch") == RUNTIME_AUTHORITY_EPOCH and v.get("status") in {"materialized", "goal_submitted", "live"}]
    if len(active) >= cap:
        append_runtime_snapshot(state, prompt, prompt_digest); save_state(state)
        return {"complete": True, "result": {"valid": True, "launched": 0, "claims": active, "prompt_digest": prompt_digest}}
    claimed = {v["item_id"] for v in state.get("claims", {}).values() if v.get("runtime_authority_epoch") == RUNTIME_AUTHORITY_EPOCH and v.get("status") not in {"retired", "stopped", "finished"}}
    targets = [row for row in rows if (row["item_id"].endswith("-TARGET") or (row["item_id"].startswith("S5CON-POOL-") and row["item_id"].endswith("-INTAKE"))) and row["state"] == " " and row["item_id"] not in claimed][:max(0, cap-len(active))]
    reservations = [{"item": item, "lane_id": item["item_id"], "generation_id": f"r-{int(time.time())}-{uuid.uuid4().hex[:8]}"} for item in targets]
    if not reservations:
        append_runtime_snapshot(state, prompt, prompt_digest); save_state(state)
        return {"complete": True, "result": {"valid": True, "launched": 0, "claims": [], "prompt_digest": prompt_digest}}
    state["reservations"] = [{"lane_id": r["lane_id"], "generation_id": r["generation_id"], "prompt_epoch": prompt["policy_epoch"], "status": "reserved"} for r in reservations]
    state["requested_concurrency"] = dict(vector); state["effective_concurrency"] = dict(vector); state["prompt_epoch"] = prompt["policy_epoch"]; state["prompt_digest"] = prompt_digest
    save_state(state)
    return {
        "complete": False,
        "specification": specification,
        "blueprint_raw": raw,
        "prompt": prompt,
        "prompt_digest": prompt_digest,
        "vector": vector,
        "fanout": fanout,
        "reservations": reservations,
        "orphaned": orphaned,
        "harvested": harvested,
    }


def _cancel_reservations_locked(plan: dict[str, Any], reason: str) -> None:
    state = load_state()
    expected = {
        (row["lane_id"], row["generation_id"])
        for row in plan["reservations"]
    }
    retained = []
    for row in state.get("reservations", []):
        identity = (row.get("lane_id"), row.get("generation_id")) if isinstance(row, dict) else None
        if identity in expected:
            continue
        retained.append(row)
    state["reservations"] = retained
    state.setdefault("underfill", {}).setdefault("binding_reasons", []).append(
        f"admission_wave:{reason}"
    )
    save_state(state)


def _admit_reserved(plan: dict[str, Any]) -> list[dict[str, Any]]:
    specification = plan["specification"]
    raw = plan["blueprint_raw"]
    prompt = plan["prompt"]
    prompt_digest = plan["prompt_digest"]
    vector = plan["vector"]
    reservations = plan["reservations"]
    def admit(reservation: dict[str, Any]) -> dict[str, Any]:
        try:
            rec = materialize(
                reservation["item"], specification, raw,
                reservation["generation_id"], reservation["lane_id"],
                prompt, prompt_digest,
            )
            submit(rec, vector); authenticate(rec)
            rec.update({"prompt_epoch": prompt["policy_epoch"], "prompt_digest": prompt_digest, "runtime_authority_epoch": RUNTIME_AUTHORITY_EPOCH})
            return rec
        except Exception as exc:
            return {"item_id": reservation["item"]["item_id"], "lane_id": reservation["lane_id"], "generation_id": reservation["generation_id"], "status": "retired", "launch_error": str(exc)}
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=min(plan["fanout"], len(reservations)), thread_name_prefix="stage5con-admit") as executor:
        for future in as_completed([executor.submit(admit, reservation) for reservation in reservations]): results.append(future.result())
    return results


def _merge_admissions_locked(plan: dict[str, Any], results: list[dict[str, Any]]) -> dict[str, Any]:
    state = load_state()
    expected_reservations = {
        (row["lane_id"], row["generation_id"])
        for row in plan["reservations"]
    }
    observed_reservations = {
        (row.get("lane_id"), row.get("generation_id"))
        for row in state.get("reservations", [])
        if isinstance(row, dict) and row.get("status") == "reserved"
    }
    if observed_reservations != expected_reservations:
        for record in results:
            if record.get("status") not in {"retired", "stopped", "finished"}:
                stop_record(record)
        raise ControllerError("durable startup reservation set changed before admission merge")
    successful = []
    for rec in results:
        if rec.get("status") == "retired":
            state.setdefault("underfill", {}).setdefault("binding_reasons", []).append(f"startup:{rec.get('item_id')}:{rec.get('launch_error','failed')}")
        else:
            state.setdefault("claims", {})[rec["item_id"]] = rec; successful.append(rec)
    state["reservations"] = []
    state["requested_concurrency"] = dict(plan["vector"]); state["effective_concurrency"] = dict(plan["vector"]); state["prompt_epoch"] = plan["prompt"]["policy_epoch"]; state["prompt_digest"] = plan["prompt_digest"]
    append_runtime_snapshot(state, plan["prompt"], plan["prompt_digest"]); save_state(state)
    return {"valid": True, "launched": len(successful), "claims": successful, "underfill": state.get("underfill", {}), "orphaned_fenced": plan["orphaned"], "harvested": plan["harvested"], "prompt_digest": plan["prompt_digest"]}


def _master_reconciliation_pending(record: dict[str, Any]) -> bool:
    """Return whether one durable claim still needs Master reconciliation."""
    status = record.get("status")
    if status == "handoff_ready":
        return True
    if status != "master_accepted":
        return False
    try:
        entry = INTEGRATION_QUEUE / (
            f"{record['item_id']}--{record['claim_id']}--{record['run_id']}.json"
        )
    except KeyError:
        return True
    if entry.exists() or entry.is_symlink():
        return True
    item_id = record.get("item_id")
    if not isinstance(item_id, str):
        return True
    integration = record.get("integration")
    if not isinstance(integration, dict):
        return True
    acceptance_path = integration.get("acceptance_path")
    acceptance_sha256 = integration.get("acceptance_sha256")
    accepted_at = integration.get("accepted_at")
    if not isinstance(acceptance_path, str):
        return True
    acceptance = Path(acceptance_path)
    try:
        relative = acceptance.relative_to(MASTER_ACCEPTANCES / item_id)
    except ValueError:
        return True
    try:
        acceptance_value = verify(
            json.loads(_regular(acceptance, "Master acceptance")),
            "Master acceptance",
        )
    except (ControllerError, OSError, ValueError, json.JSONDecodeError):
        return True
    handoff = acceptance_value.get("handoff", {})
    integration_value = acceptance_value.get("integration", {})
    return not (
        len(relative.parts) == 3
        and relative.suffix == ".json"
        and acceptance.is_file()
        and not acceptance.is_symlink()
        and acceptance_value.get("program") == PROGRAM
        and acceptance_value.get("item_id") == item_id
        and handoff.get("claim_id") == record.get("claim_id")
        and handoff.get("run_id") == record.get("run_id")
        and relative.parts[0] == handoff.get("baseline_sha256")
        and relative.parts[1] == integration_value.get("post_tree_sha256")
        and relative.name
        == f"{acceptance_value.get('authority_sha256')}.json"
        and isinstance(acceptance_sha256, str)
        and re.fullmatch(r"[0-9a-f]{64}", acceptance_sha256) is not None
        and file_digest(acceptance) == acceptance_sha256
        and isinstance(accepted_at, str)
        and accepted_at == acceptance_value.get("accepted_at")
    )


def _integration_candidates(
    rows: list[dict[str, Any]], state: dict[str, Any],
) -> list[str]:
    """Return deterministic current-epoch Master work after revalidation."""
    claims = state.get("claims", {})
    if not isinstance(claims, dict):
        raise ControllerError("controller claim ledger is malformed")
    row_ids = {row["item_id"] for row in rows}
    return [
        item_id for item_id, record in sorted(claims.items())
        if item_id in row_ids
        and isinstance(record, dict)
        and record.get("runtime_authority_epoch") == RUNTIME_AUTHORITY_EPOCH
        and _master_reconciliation_pending(record)
    ]


def run_master_pipeline(concurrency_prompt: Path) -> dict[str, Any]:
    """Consume harvested handoffs under the explicit integration ceiling.

    Transition/acceptance functions acquire the shared scheduler lock per
    item, so this orchestration deliberately runs before admission acquires
    that lock.  A failure leaves the immutable handoff queued and does not
    block unrelated items within the same prompt-bounded wave.
    """
    specification, rows, _ = load_program()
    prompt, prompt_digest = load_concurrency_prompt(
        concurrency_prompt, specification
    )
    cap = prompt["concurrency"].get("integration")
    if isinstance(cap, bool) or not isinstance(cap, int) or cap < 0:
        raise ControllerError("integration prompt cap is invalid")
    boot_rows = [row for row in rows if row.get("item_id") == "S5CON-BOOT-001"]
    if len(boot_rows) != 1 or boot_rows[0].get("state") != "x":
        raise ControllerError(
            "conjecture BOOT must be Master accepted before integration"
        )
    state = load_state(False)
    claims = state.get("claims", {})
    if not isinstance(claims, dict):
        raise ControllerError("controller claim ledger is malformed")
    if claims and state.get("runtime_authority_epoch") != RUNTIME_AUTHORITY_EPOCH:
        raise ControllerError(
            "controller state belongs to a historical runtime authority epoch"
        )
    candidates = _integration_candidates(rows, state)
    integrated: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    if cap == 0 or not candidates:
        return {
            "prompt_digest": prompt_digest,
            "cap": cap,
            "eligible": len(candidates),
            "underfill": max(0, cap - len(candidates)),
            "integrated": integrated,
            "errors": errors,
        }
    transitioner = handoff_transition_module()
    selected = candidates[:cap]
    for item_id in selected:
        try:
            _, current_rows, _ = load_program()
            current_boot = [
                row for row in current_rows
                if row.get("item_id") == "S5CON-BOOT-001"
            ]
            if len(current_boot) != 1 or current_boot[0].get("state") != "x":
                raise ControllerError(
                    "conjecture BOOT changed before integration"
                )
            current_state = load_state(False)
            if (
                current_state.get("claims")
                and current_state.get("runtime_authority_epoch")
                != RUNTIME_AUTHORITY_EPOCH
            ):
                raise ControllerError(
                    "controller state changed to a historical runtime authority epoch"
                )
            current_candidates = _integration_candidates(
                current_rows, current_state
            )
            if item_id not in current_candidates:
                # An earlier item in this wave may have completed or superseded
                # this exact run.  Treat that as an idempotent no-op, never as
                # permission to operate on the stale initial record.
                continue
            state_name = {
                row["item_id"]: row["state"] for row in current_rows
            }.get(item_id)
            record = current_state.get("claims", {}).get(item_id, {})
            if state_name == "x" or record.get("status") == "master_accepted":
                outcome = transitioner.reconcile_acceptance(item_id)
            else:
                if state_name == " ":
                    transitioner.transition(item_id)
                    state_name = "_"
                if state_name != "_":
                    raise ControllerError(
                        f"{item_id}: handoff cursor is not transitionable"
                    )
                outcome = transitioner.master_accept(item_id)
            integrated.append(outcome)
        except Exception as exc:
            errors.append({"item_id": item_id, "error": str(exc)})
    return {
        "prompt_digest": prompt_digest,
        "cap": cap,
        "eligible": len(candidates),
        "underfill": max(0, cap - len(selected)),
        "integrated": integrated,
        "errors": errors,
    }


def launch_workers(concurrency_prompt: Path) -> dict[str, Any]:
    integration = run_master_pipeline(concurrency_prompt)
    with scheduler_guard():
        plan = _reserve_workers_locked(concurrency_prompt)
    if plan["complete"]:
        return {**plan["result"], "integration": integration}
    try:
        results = _admit_reserved(plan)
    except BaseException as exc:
        with scheduler_guard():
            _cancel_reservations_locked(plan, type(exc).__name__)
        raise
    with scheduler_guard():
        return {**_merge_admissions_locked(plan, results), "integration": integration}

def _status_locked() -> dict[str, Any]:
    state = load_state(False); harvested = 0
    if state.get("claims"):
        try:
            specification, _, _ = load_program(); harvested = harvest_state(state, specification)
        except Exception:
            harvested = 0
    orphaned = fence_orphaned_generations(state); claims = list(state.get("claims", {}).values())
    for record in claims:
        if record.get("status") in {"materialized", "goal_submitted", "live"}:
            reconcile_record(record)
    # Before BOOT acceptance this command must remain observational.  Creating
    # even an empty controller state would poison the runtime-absence gate.
    if RUNTIME.exists():
        append_runtime_snapshot(state)
        save_state(state)
    return {"program": PROGRAM, "transport": TRANSPORT, "claims": claims, "live": sum(v.get("status") == "live" for v in claims), "orphaned_fenced": orphaned, "harvested": harvested, "concurrency_prompt_required": True}


def status() -> dict[str, Any]:
    with scheduler_guard():
        return _status_locked()


def _stop_locked() -> dict[str, Any]:
    state = load_state(False); stopped = 0
    for record in state.get("claims", {}).values():
        if record.get("status") in {"materialized", "goal_submitted", "live"}: stop_record(record); record["status"] = "stopped"; stopped += 1
    if RUNTIME.exists(): append_runtime_snapshot(state); save_state(state)
    return {"stopped": stopped}


def stop() -> dict[str, Any]:
    with scheduler_guard():
        return _stop_locked()


def main() -> int:
    parser = argparse.ArgumentParser(); group = parser.add_mutually_exclusive_group(required=True); group.add_argument("--validate-only", action="store_true"); group.add_argument("--launch-workers", action="store_true"); group.add_argument("--tick", action="store_true"); group.add_argument("--status", action="store_true"); group.add_argument("--stop", action="store_true")
    parser.add_argument("--concurrency-prompt", type=Path)
    args = parser.parse_args()
    try:
        if args.validate_only:
            result = validate_only(args.concurrency_prompt)
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0 if result.get("valid") is True else 1
        elif args.launch_workers or args.tick:
            if args.concurrency_prompt is None: raise ControllerError("concurrency prompt is required")
            result = launch_workers(args.concurrency_prompt)
        elif args.status: result = status()
        else: result = stop()
    except (ControllerError, OSError, sqlite3.Error, RuntimeError) as exc: print(json.dumps({"valid": False, "error": str(exc)})); return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
