#!/usr/bin/env python3
"""Stage5 theorem task-local tmux/Codex goal execution controller."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import difflib
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import signal
import sqlite3
import stat
import subprocess
import sys
import tempfile
import threading
import time
import tomllib
import uuid
from typing import Any, Callable, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "Docs/tools/check_stage5_theorems_blueprint.py"
GANTT_GENERATOR_PATH = ROOT / "Docs/tools/generate_stage5_theorems_gantt.py"
CLAIM_CHECKER_PATH = ROOT / "scripts/check_stage5_theorem_claim.py"
ITEM_CHECKER_PATH = ROOT / "scripts/check_stage5_theorem_item.py"
BOOT_MANAGER_PATH = ROOT / "Docs/tools/manage_stage5_proof_debt_blueprints.py"
PORTABILITY_FIXTURES = ROOT / "scripts/fixtures/stage5_theorem_claim"
BLUEPRINT = ROOT / "Docs/Stage5_Theorems_Blueprint.md"
GANTT = ROOT / "Docs/Stage5_Theorems_Gantt.md"
EVIDENCE = ROOT / "Docs/evidence/stage5_theorems"
WORKSET = EVIDENCE / "workset-5.6.json"
EXECUTION_SPEC = EVIDENCE / "execution-spec.json"
PROGRAM_RUNTIME = ROOT / ".ops/stage5-theorems-execution-v1"
SHARED_RUNTIME = ROOT / ".ops/stage5-proof-debt-shared-v1"
STATE_PATH = PROGRAM_RUNTIME / "state/controller-state.json"
EVENT_LEDGER = PROGRAM_RUNTIME / "ledgers/events.jsonl"
EVENT_LEDGER_LOCK = PROGRAM_RUNTIME / "locks/events.lock"
SNAPSHOT_PATH = PROGRAM_RUNTIME / "status/runtime-snapshot.json"
SCHEDULER_LOCK = PROGRAM_RUNTIME / "locks/scheduler.lock"
INVOCATION_LOCK = PROGRAM_RUNTIME / "locks/invocation.lock"
ACTIVATION_RECEIPT = EVIDENCE / "execution/controller-activation.json"
HANDOFF_ROOT = EVIDENCE / "execution/handoffs"
REVIEW_ROOT = EVIDENCE / "execution/reviews"
ACCEPTANCE_ROOT = EVIDENCE / "execution/acceptances"
OPERATOR_AUTHORITY = ROOT / "Docs/evidence/stage5_shared_execution/operator-budget-v1.json"
OPERATOR_TRUST_ROOT = ROOT / "Docs/evidence/stage5_shared_execution/operator-budget-trust-root-v1.json"
PROGRAM = "stage5-theorem-proof-debt/1.0"
TRANSPORT = "tmux_codex_tui"
PROVIDER = "sub2api"
MODEL = "gpt-5.6-sol"
EFFORT = "ultra"
SERVICE_TIER = "default"
GOAL_THREAD_ID = "019fe8d5-f4f1-7820-af7a-b7a365cddf65"
GOAL_OBJECTIVE_SHA256 = "301dcadce72069b44fe3af1960b2684ee74127cabb44ac8da6b87d5e0856fb3e"
OPERATOR_TRUST_ROOT_SHA256 = "6950ac8f647e851496f21e610243510e9a29835e5c1638f0081802ead3159b45"
OPERATOR_AUTHORITY_SHA256 = "3cdd2496a45549a99caccc9da58a827bd37c49c836aedc1d1a7502bb1ac89917"
SHARED_AUTHORITY_SHA256 = "0f5d5bbe6c87bf3cfa9398a86a6eeea8650f751fdaa4a531f20e8e57c5402dc3"
CRON_BEGIN = "# BEGIN AWESOME_THEOREMS_STAGE5_THEOREMS_EXECUTION_V1"
CRON_END = "# END AWESOME_THEOREMS_STAGE5_THEOREMS_EXECUTION_V1"
CRON_COMMAND = (
    "*/2 * * * * cd /home/sansha/Github/awesome_theorems && "
    "/usr/bin/python3 /home/sansha/Github/awesome_theorems/scripts/stage5_theorems_execution_cron.py "
    "--tick >> /home/sansha/Github/awesome_theorems/.ops/stage5-theorems-execution-v1/logs/cron.log 2>&1"
)
AUTH_SOURCE = Path("/home/sansha/.codex/auth.json")
CONFIG_SOURCE = Path("/home/sansha/.codex/config.toml")
GOALS_DB = Path("/home/sansha/.codex/goals_1.sqlite")
DOCKER_BINARY = Path("/usr/bin/docker")
DOCKER_BINARY_SHA256 = "7ed12b00293d64742419a6601ae97960a367a0ce97c88b06e3278cc0a409557b"
CONTAINER_IMAGE = "ubuntu@sha256:561618e2c15bf2397621dd04f96926663a3b5616c189cf7e38db7e82f5c538ea"
CONTAINER_IMAGE_ID = "sha256:561618e2c15bf2397621dd04f96926663a3b5616c189cf7e38db7e82f5c538ea"
CODEX_NATIVE_BINARY = Path(
    "/home/sansha/.local/node_modules/@openai/codex-linux-x64/"
    "vendor/x86_64-unknown-linux-musl/bin/codex"
)
CODEX_NATIVE_SHA256 = "cb0a15567e9a60a5820d54b0f6ae86d504dc3805c1eab21a47f70e3eb7b73a40"
CODEX_CODE_MODE_HOST = CODEX_NATIVE_BINARY.with_name("codex-code-mode-host")
CODEX_CODE_MODE_HOST_SHA256 = "00ecf5d040865b97884c488883abd342581c2a432debe7a54e4646bceee3d2d6"
CONTAINER_CODEX_BINARY = "/opt/awesome-theorems/codex"
CONTAINER_CODE_MODE_HOST = "/opt/awesome-theorems/codex-code-mode-host"
WORKER_DEVELOPER_INSTRUCTIONS = (
    "This is one isolated Stage5 worker claim. Do not call collaboration tools, "
    "do not spawn subagents, and do not create child threads under any circumstances. "
    "Work directly on the single active goal and use only the task-local work root."
)
MAX_LOG_BYTES = 64 * 1024 * 1024
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@-]{0,199}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
CONTAINER_ID_RE = re.compile(r"^[0-9a-f]{64}$")
EVENT_APPEND_LOCK = threading.Lock()
STARTING_STATUSES = {
    "producer_reserved", "review_reserved", "repair_reserved", "materialized",
    "tmux_started", "goal_pasted", "followup_pasted", "goal_submitted",
}
ACTIVE_STATUSES = STARTING_STATUSES | {"live"}


class ControllerError(RuntimeError):
    pass


class MasterValidationError(ControllerError):
    pass


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ControllerError("value is not canonical finite JSON") from exc


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def sealed(unsigned: dict[str, Any]) -> dict[str, Any]:
    result = dict(unsigned)
    result["authority_sha256"] = digest(canonical(unsigned))
    return result


def verify_seal(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ControllerError(f"{label}: expected object")
    authority = value.get("authority_sha256")
    body = dict(value)
    body.pop("authority_sha256", None)
    if not isinstance(authority, str) or not SHA_RE.fullmatch(authority):
        raise ControllerError(f"{label}: missing authority")
    if digest(canonical(body)) != authority:
        raise ControllerError(f"{label}: authority mismatch")
    return value


def atomic_write(path: Path, raw: bytes, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def atomic_json(path: Path, value: Any, mode: int = 0o644) -> None:
    atomic_write(
        path,
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False).encode("utf-8") + b"\n",
        mode,
    )


def strict_json(path: Path, label: str) -> Any:
    if path.is_symlink() or not path.is_file():
        raise ControllerError(f"{label}: missing regular file {path}")
    raw = path.read_bytes()

    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            if key in result:
                raise ControllerError(f"{label}: duplicate key {key!r}")
            result[key] = value
        return result

    def constant(value: str) -> Any:
        raise ControllerError(f"{label}: non-finite number {value}")

    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ControllerError(f"{label}: invalid strict JSON") from exc


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ControllerError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def projection_candidate(
    item_id: str, expected_state: str, wanted_state: str,
) -> tuple[bytes, bytes, bytes, bytes, dict[str, Any]]:
    if (expected_state, wanted_state) not in {(" ", "_"), ("_", "x")}:
        raise ControllerError("unsupported checklist transition")
    module = checker()
    specification, rows, old_blueprint = module.parse_blueprint()
    module.validate_spec(specification)
    matches = [row for row in rows if row["item_id"] == item_id]
    if len(matches) != 1 or matches[0]["state"] != expected_state:
        raise ControllerError(
            f"{item_id}: transition expected {expected_state!r} current state differs"
        )
    by_id = {row["item_id"]: row for row in rows}
    if any(by_id[dependency]["state"] != "x" for dependency in matches[0]["dependencies"]):
        raise ControllerError(f"{item_id}: dependency is not Master accepted")
    prefix = f"- [{expected_state}] `{item_id}` "
    replacement = f"- [{wanted_state}] `{item_id}` "
    text = old_blueprint.decode("utf-8")
    if text.count(prefix) != 1:
        raise ControllerError(f"{item_id}: authoritative checklist row identity differs")
    new_blueprint = text.replace(prefix, replacement, 1).encode("utf-8")
    with tempfile.TemporaryDirectory(prefix="stage5-transition-") as directory:
        candidate = Path(directory) / "Stage5_Theorems_Blueprint.md"
        candidate.write_bytes(new_blueprint)
        candidate_spec, candidate_rows, parsed_raw = module.parse_blueprint(candidate)
        module.validate_spec(candidate_spec)
        if parsed_raw != new_blueprint:
            raise ControllerError("candidate Blueprint parse bytes differ")
        candidate_row = next(row for row in candidate_rows if row["item_id"] == item_id)
        if candidate_row["state"] != wanted_state:
            raise ControllerError("candidate checklist transition did not round-trip")
        generator = load_module(
            GANTT_GENERATOR_PATH, "stage5_theorem_gantt_for_state_transition"
        )
        new_gantt = generator.render(blueprint_path=candidate)
    old_gantt = GANTT.read_bytes()
    return old_blueprint, old_gantt, new_blueprint, new_gantt, candidate_row


def commit_projection_pair(
    old_blueprint: bytes, old_gantt: bytes, new_blueprint: bytes, new_gantt: bytes,
    *, guard_sha256: dict[Path, str] | None = None,
) -> None:
    manager = load_module(BOOT_MANAGER_PATH, "stage5_atomic_projection_transaction")
    blueprint_guard = manager.regular_file_expectation(BLUEPRINT)
    gantt_guard = manager.regular_file_expectation(GANTT)
    if (
        blueprint_guard is None or blueprint_guard.sha256 != digest(old_blueprint)
        or gantt_guard is None or gantt_guard.sha256 != digest(old_gantt)
    ):
        raise ControllerError("projection compare-and-swap baseline changed")
    guards: dict[Path, Any] = {}
    for path, expected_sha in (guard_sha256 or {}).items():
        expectation = manager.regular_file_expectation(path)
        if expectation is None or expectation.sha256 != expected_sha:
            raise ControllerError(f"transition guard differs: {path}")
        guards[path] = expectation
    with manager.manager_mutation_lock():
        manager.recover_batch_transactions()
        manager.atomic_batch_write(
            [(BLUEPRINT, new_blueprint), (GANTT, new_gantt)],
            expected_old={BLUEPRINT: blueprint_guard, GANTT: gantt_guard},
            guards=guards or {},
        )


def advance_checklist(
    item_id: str, expected_state: str, wanted_state: str,
    *, guard_sha256: dict[Path, str] | None = None,
) -> dict[str, str]:
    old_blueprint, old_gantt, new_blueprint, new_gantt, _ = projection_candidate(
        item_id, expected_state, wanted_state
    )
    commit_projection_pair(
        old_blueprint, old_gantt, new_blueprint, new_gantt,
        guard_sha256=guard_sha256,
    )
    return {
        "pre_blueprint_sha256": digest(old_blueprint),
        "pre_gantt_sha256": digest(old_gantt),
        "post_blueprint_sha256": digest(new_blueprint),
        "post_gantt_sha256": digest(new_gantt),
    }


def checker() -> Any:
    return load_module(CHECKER_PATH, "stage5_theorem_checker_for_controller")


def process_start_ticks(pid: int) -> int | None:
    try:
        raw = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8")
        right = raw.rfind(")")
        return int(raw[right + 2:].split()[19])
    except (OSError, ValueError, IndexError):
        return None


def process_environment(pid: int, key: str) -> str | None:
    try:
        prefix = key.encode() + b"="
        values = [part[len(prefix):] for part in Path(f"/proc/{pid}/environ").read_bytes().split(b"\0") if part.startswith(prefix)]
        return values[0].decode("utf-8") if len(values) == 1 else None
    except (OSError, UnicodeDecodeError):
        return None


def run(
    argv: Sequence[str], *, cwd: Path | None = None, input_text: str | None = None,
    check: bool = True, timeout: float = 30,
) -> subprocess.CompletedProcess[str]:
    try:
        options: dict[str, Any] = {
            "cwd": cwd, "text": True, "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE, "check": False, "timeout": timeout,
            "close_fds": True,
        }
        if input_text is None:
            options["stdin"] = subprocess.DEVNULL
        else:
            options["input"] = input_text
        completed = subprocess.run(list(argv), **options)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ControllerError(f"command failed to start or timed out: {argv[:3]}") from exc
    if check and completed.returncode != 0:
        raise ControllerError(
            f"command failed exit={completed.returncode}: {argv[:3]}; stderr={completed.stderr[-1000:]!r}"
        )
    return completed


class FileLock:
    def __init__(self, path: Path, *, blocking: bool = True):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.stream = path.open("a+")
        operation = fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB)
        try:
            fcntl.flock(self.stream, operation)
        except BlockingIOError as exc:
            self.stream.close()
            raise ControllerError("scheduler lease is already held") from exc

    def close(self) -> None:
        if not self.stream.closed:
            fcntl.flock(self.stream, fcntl.LOCK_UN)
            self.stream.close()

    def __enter__(self) -> "FileLock":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


def append_event(event: str, payload: dict[str, Any]) -> dict[str, Any]:
    with EVENT_APPEND_LOCK:
        with FileLock(EVENT_LEDGER_LOCK):
            EVENT_LEDGER.parent.mkdir(parents=True, exist_ok=True)
            previous = None
            sequence = 1
            if EVENT_LEDGER.exists():
                last = None
                with EVENT_LEDGER.open("rb") as stream:
                    for raw in stream:
                        if raw.strip():
                            last = json.loads(raw)
                if last is not None:
                    previous = last["record_sha256"]
                    sequence = int(last["sequence"]) + 1
            body = {
                "schema_version": "awesome-theorems/stage5-controller-event/1.0",
                "program": PROGRAM,
                "sequence": sequence,
                "event_id": str(uuid.uuid4()),
                "event": event,
                "at": now(),
                "previous_record_sha256": previous,
                "payload": payload,
            }
            record = dict(body)
            record["record_sha256"] = digest(canonical(body))
            descriptor = os.open(
                EVENT_LEDGER,
                os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_CLOEXEC,
                0o600,
            )
            try:
                os.write(descriptor, canonical(record) + b"\n")
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
            return record


def validate_event_ledger() -> int:
    if not EVENT_LEDGER.exists():
        return 0
    previous = None
    sequence = 0
    seen: set[str] = set()
    with EVENT_LEDGER.open("rb") as stream:
        for line_number, raw in enumerate(stream, 1):
            if not raw.endswith(b"\n"):
                raise ControllerError("event ledger has a truncated terminal record")
            try:
                record = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ControllerError(f"event ledger line {line_number} is invalid") from exc
            body = dict(record)
            observed = body.pop("record_sha256", None)
            if (
                set(record) != {
                    "schema_version", "program", "sequence", "event_id", "event", "at",
                    "previous_record_sha256", "payload", "record_sha256",
                }
                or record["schema_version"] != "awesome-theorems/stage5-controller-event/1.0"
                or record["program"] != PROGRAM
                or record["sequence"] != sequence + 1
                or record["previous_record_sha256"] != previous
                or observed != digest(canonical(body))
                or record["event_id"] in seen
            ):
                raise ControllerError(f"event ledger chain differs at line {line_number}")
            sequence += 1
            previous = observed
            seen.add(record["event_id"])
    return sequence


def default_state(specification_sha256: str) -> dict[str, Any]:
    return {
        "schema_version": "awesome-theorems/stage5-controller-state/1.0",
        "program": PROGRAM,
        "execution_spec_sha256": specification_sha256,
        "created_at": now(),
        "updated_at": now(),
        "claims": {},
        "handoffs": {},
        "reviews": {},
        "integrations": {},
        "repairs": {},
        "underfill_reasons": [],
        "last_tick": None,
        "last_progress": None,
        "cleanup": {"status": "not_authorized"},
    }


def load_state(specification_sha256: str, *, create: bool) -> dict[str, Any]:
    if not STATE_PATH.exists():
        if not create:
            return default_state(specification_sha256)
        state = default_state(specification_sha256)
        atomic_json(STATE_PATH, sealed(state), 0o600)
        return state
    state = verify_seal(strict_json(STATE_PATH, "controller state"), "controller state")
    if state.get("schema_version") != "awesome-theorems/stage5-controller-state/1.0":
        raise ControllerError("controller state schema differs")
    if state.get("program") != PROGRAM or state.get("execution_spec_sha256") != specification_sha256:
        raise ControllerError("controller state authority differs")
    return state


def save_state(state: dict[str, Any]) -> None:
    state = dict(state)
    state.pop("authority_sha256", None)
    state["updated_at"] = now()
    atomic_json(STATE_PATH, sealed(state), 0o600)


def active_operator_goal() -> dict[str, Any]:
    if not GOALS_DB.is_file():
        raise ControllerError("operator goal registry is unavailable")
    try:
        connection = sqlite3.connect(f"file:{GOALS_DB}?mode=ro", uri=True, timeout=2)
        row = connection.execute(
            "select goal_id,objective,status,token_budget,tokens_used,created_at_ms,updated_at_ms "
            "from thread_goals where thread_id=?", (GOAL_THREAD_ID,),
        ).fetchone()
        connection.close()
    except sqlite3.Error as exc:
        raise ControllerError("operator goal registry query failed") from exc
    if row is None or row[2] != "active" or digest(row[1].encode("utf-8")) != GOAL_OBJECTIVE_SHA256:
        raise ControllerError("exact operator goal is absent, inactive, or changed")
    return {
        "thread_id": GOAL_THREAD_ID, "goal_id": row[0], "status": row[2],
        "objective_sha256": GOAL_OBJECTIVE_SHA256, "token_budget": row[3],
        "tokens_used": row[4], "created_at_ms": row[5], "updated_at_ms": row[6],
    }


def operator_authentication_sha256() -> str:
    goal = active_operator_goal()
    return digest(canonical({
        "thread_id": goal["thread_id"], "goal_id": goal["goal_id"],
        "status": goal["status"], "objective_sha256": goal["objective_sha256"],
    }))


def expected_trust_root() -> dict[str, Any]:
    return {
        "schema_version": "awesome-theorems/stage5-operator-goal-trust-root/1.0",
        "operator_identity": f"codex-user-goal:{GOAL_THREAD_ID}",
        "authority_mode": "local_codex_active_goal_registry_binding",
        "thread_id": GOAL_THREAD_ID,
        "objective_sha256": GOAL_OBJECTIVE_SHA256,
        "verification": "controller requires the exact active local Codex goal thread/objective/status before activation and each launch; this is a pinned local operator instruction binding, not a cryptographic signature or price attestation",
        "renewal": "requires a new explicit user instruction and reviewed authority migration",
    }


def validate_operator_authority() -> dict[str, Any]:
    trust = strict_json(OPERATOR_TRUST_ROOT, "operator trust root")
    if trust != expected_trust_root() or digest(canonical(trust)) != OPERATOR_TRUST_ROOT_SHA256:
        raise ControllerError("operator trust-root bytes differ")
    authority = verify_seal(strict_json(OPERATOR_AUTHORITY, "operator budget authority"), "operator budget authority")
    if authority.get("authority_sha256") != OPERATOR_AUTHORITY_SHA256:
        raise ControllerError("operator budget authority digest differs")
    if authority.get("goal_thread_id") != GOAL_THREAD_ID or authority.get("goal_objective_sha256") != GOAL_OBJECTIVE_SHA256:
        raise ControllerError("operator budget goal binding differs")
    if authority.get("trust_root_sha256") != OPERATOR_TRUST_ROOT_SHA256:
        raise ControllerError("operator budget trust binding differs")
    if authority.get("billing_binding") != {
        "provider": PROVIDER, "model": MODEL, "reasoning_effort": EFFORT,
        "service_tier": SERVICE_TIER, "monetary_price": "unknown_not_zero",
    }:
        raise ControllerError("operator budget route/billing binding differs")
    allowance = authority.get("program_allowances", {}).get(PROGRAM)
    if not isinstance(allowance, dict):
        raise ControllerError("theorem program allowance is absent")
    for key in ("model_input_tokens", "model_output_tokens", "model_turns", "external_launches", "wall_seconds", "cpu_seconds"):
        if not isinstance(allowance.get(key), int) or isinstance(allowance[key], bool) or allowance[key] <= 0:
            raise ControllerError(f"operator allowance {key} is not positive finite")
    active_operator_goal()
    return authority


def bootstrap_state() -> str:
    module = checker()
    _, rows, _ = module.parse_blueprint()
    return rows[0]["state"]


def load_program() -> tuple[dict[str, Any], list[dict[str, Any]], bytes]:
    module = checker()
    specification, rows, blueprint_raw = module.parse_blueprint()
    module.validate_spec(specification)
    module.validate_boot_data(specification, rows, blueprint_raw)
    return specification, rows, blueprint_raw


def tool_path(name: str) -> str | None:
    resolved = shutil.which(name)
    return str(Path(resolved).resolve()) if resolved else None


def validate_static_transport(source: str) -> list[str]:
    errors: list[str] = []
    prohibited_command_shapes = (
        "codex" + " " + ("e" + "xec"),
        "codex" + " " + "app" + "-server",
        "app" + "-server",
        "--" + "remote",
    )
    for value in prohibited_command_shapes:
        if value in source:
            errors.append(f"prohibited worker transport literal present: {value}")
    if "tmux_codex_tui" not in source or '"/goal "' not in source:
        errors.append("interactive tmux/goal transport surfaces are incomplete")
    return errors


def validate_portability_fixtures() -> list[dict[str, Any]]:
    required = {
        "repository_name", "blueprint_path", "gantt_path", "item_prefix",
        "item_id", "language", "validator_argv", "provider", "model",
        "reasoning_effort", "service_tier",
    }
    rows: list[dict[str, Any]] = []
    if PORTABILITY_FIXTURES.is_symlink() or not PORTABILITY_FIXTURES.is_dir():
        raise ControllerError("two-repository portability fixture root is unavailable")
    for path in sorted(PORTABILITY_FIXTURES.glob("*_repo.json")):
        value = strict_json(path, f"portability fixture {path.name}")
        if not isinstance(value, dict) or set(value) != required:
            raise ControllerError(f"portability fixture fields differ: {path.name}")
        if (
            not all(isinstance(value[key], str) and value[key] for key in required - {"validator_argv"})
            or not isinstance(value["validator_argv"], list)
            or not value["validator_argv"]
            or any(not isinstance(part, str) or not part for part in value["validator_argv"])
            or not value["item_id"].startswith(value["item_prefix"] + "-")
        ):
            raise ControllerError(f"portability fixture values differ: {path.name}")
        blueprint = PurePosixPath(value["blueprint_path"])
        gantt = PurePosixPath(value["gantt_path"])
        expected_stem = (
            blueprint.stem[:-len("Blueprint")] + "Gantt"
            if blueprint.stem.endswith("Blueprint")
            else blueprint.stem + "_Gantt"
        )
        expected = blueprint.with_name(expected_stem + blueprint.suffix)
        if gantt != expected:
            raise ControllerError(f"portability fixture Gantt mapping differs: {path.name}")
        rows.append(value)
    if len(rows) != 2:
        raise ControllerError("exactly two portability fixture repositories are required")
    varying = (
        "repository_name", "blueprint_path", "item_prefix", "language",
        "validator_argv", "provider", "model", "reasoning_effort", "service_tier",
    )
    for key in varying:
        if canonical(rows[0][key]) == canonical(rows[1][key]):
            raise ControllerError(f"portability fixtures do not differ in {key}")
    forbidden = {ROOT.name, "S5THM", PROVIDER, MODEL, EFFORT, SERVICE_TIER}
    if any(token in canonical(rows).decode("utf-8") for token in forbidden):
        raise ControllerError("portability fixtures contain canonical-project residue")
    return rows


def validate_only() -> dict[str, Any]:
    before = {
        "runtime": PROGRAM_RUNTIME.exists(), "shared_runtime": SHARED_RUNTIME.exists(),
        "state": STATE_PATH.exists(), "snapshot": SNAPSHOT_PATH.exists(),
    }
    errors: list[str] = []
    try:
        specification, rows, blueprint_raw = load_program()
    except Exception as exc:
        specification, rows, blueprint_raw = {}, [], b""
        errors.append(f"program:{exc}")
    route = specification.get("route_policy", {}) if specification else {}
    if route.get("provider") != PROVIDER or route.get("model") != MODEL or route.get("reasoning_effort") != EFFORT or route.get("service_tier") != SERVICE_TIER:
        errors.append("route does not resolve to sub2api/gpt-5.6-sol/ultra/default")
    limits = specification.get("default_limits", {}) if specification else {}
    if any(limits.get(key) != 120 for key in ("logical_claims", "authenticated_live_goals", "running_turns")):
        errors.append("120-way caps differ")
    boundary = specification.get("worker_container_boundary", {}) if specification else {}
    if boundary.get("codex_binary") != {
        "host_path": str(CODEX_NATIVE_BINARY), "container_path": CONTAINER_CODEX_BINARY,
        "sha256": CODEX_NATIVE_SHA256, "mount_mode": "read_only",
    }:
        errors.append("native Codex binary specification binding differs")
    if boundary.get("codex_code_mode_host") != {
        "host_path": str(CODEX_CODE_MODE_HOST), "container_path": CONTAINER_CODE_MODE_HOST,
        "sha256": CODEX_CODE_MODE_HOST_SHA256, "mount_mode": "read_only",
        "required_for_tool_execution": True,
    }:
        errors.append("Codex code-mode host specification binding differs")
    codex = tool_path("codex")
    tmux = tool_path("tmux")
    # BOOT runs this validation from a sealed read-only snapshot with a clean
    # environment.  User-local Codex credentials, the operator goal registry,
    # and activation-time binaries are intentionally outside that snapshot.
    # Their absence is readiness telemetry here; activation and every tick use
    # runtime_preflight() as the hard gate.
    source = Path(__file__).read_text(encoding="utf-8")
    errors.extend(validate_static_transport(source))
    try:
        validate_portability_fixtures()
    except Exception as exc:
        errors.append(f"portability:{exc}")
    if STATE_PATH.exists():
        try:
            state = load_state(digest(canonical(specification)), create=False)
            validate_event_ledger()
            if not isinstance(state.get("claims"), dict):
                errors.append("controller claim state is malformed")
        except Exception as exc:
            errors.append(f"runtime:{exc}")
    boot = rows[0]["state"] if rows else None
    authority = {"materialized": OPERATOR_AUTHORITY.is_file() and OPERATOR_TRUST_ROOT.is_file(), "active_goal": False}
    if authority["materialized"]:
        try:
            validate_operator_authority()
            authority["active_goal"] = True
        except Exception as exc:
            authority["error"] = str(exc)
    after = {
        "runtime": PROGRAM_RUNTIME.exists(), "shared_runtime": SHARED_RUNTIME.exists(),
        "state": STATE_PATH.exists(), "snapshot": SNAPSHOT_PATH.exists(),
    }
    if after != before:
        errors.append("validate-only changed runtime presence")
    return {
        "valid": not errors,
        "errors": errors,
        "program": PROGRAM,
        "items": len(rows),
        "blueprint_sha256": digest(blueprint_raw) if blueprint_raw else None,
        "boot_state": {" ": "not_done", "_": "handoff_waiting_master", "x": "master_accepted"}.get(boot),
        "activation_ready": boot == "x" and authority.get("active_goal") is True,
        "transport": TRANSPORT,
        "goal_command": "/goal",
        "route": route,
        "caps": limits,
        "tools": {"codex": codex, "tmux": tmux},
        "operator_authority": authority,
        "runtime_presence_before": before,
        "runtime_presence_after": after,
    }


def runtime_preflight() -> dict[str, Any]:
    """Validate every host-local prerequisite required before external spend."""
    codex = tool_path("codex")
    tmux_binary = tool_path("tmux")
    if codex is None:
        raise ControllerError("Codex TUI binary is unavailable")
    if tmux_binary is None:
        raise ControllerError("tmux binary is unavailable")
    if AUTH_SOURCE.is_symlink() or not AUTH_SOURCE.is_file():
        raise ControllerError("Codex credential source is unavailable")
    if CONFIG_SOURCE.is_symlink() or not CONFIG_SOURCE.is_file():
        raise ControllerError("Codex provider config source is unavailable")
    for path, expected, label in (
        (DOCKER_BINARY, DOCKER_BINARY_SHA256, "Docker binary"),
        (CODEX_NATIVE_BINARY, CODEX_NATIVE_SHA256, "native Codex binary"),
        (CODEX_CODE_MODE_HOST, CODEX_CODE_MODE_HOST_SHA256, "Codex code-mode host"),
    ):
        if path.is_symlink() or not path.is_file() or file_digest(path) != expected:
            raise ControllerError(f"{label} is unavailable or digest-mismatched")
    image = run(
        [str(DOCKER_BINARY), "image", "inspect", CONTAINER_IMAGE, "--format", "{{.Id}}"],
        timeout=20,
    ).stdout.strip()
    if image != CONTAINER_IMAGE_ID:
        raise ControllerError("pinned worker container image identity differs")
    authority = validate_operator_authority()
    return {
        "codex": codex, "tmux": tmux_binary, "docker": str(DOCKER_BINARY),
        "container_image": CONTAINER_IMAGE, "authority": authority,
    }


def require_canonical_root() -> None:
    if ROOT != Path("/home/sansha/Github/awesome_theorems"):
        raise ControllerError("state-changing action requires the canonical repository root")


def codex_provider_config() -> dict[str, Any]:
    if CONFIG_SOURCE.is_symlink() or not CONFIG_SOURCE.is_file():
        raise ControllerError("Codex provider config source is unavailable")
    try:
        document = tomllib.loads(CONFIG_SOURCE.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ControllerError("Codex provider config source is invalid") from exc
    provider = document.get("model_providers", {}).get(PROVIDER)
    if not isinstance(provider, dict):
        raise ControllerError("selected provider config is absent")
    expected_keys = ("name", "base_url", "wire_api", "supports_websockets")
    if any(key not in provider for key in expected_keys) or provider["wire_api"] != "responses":
        raise ControllerError("selected provider config is incomplete")
    return {key: provider[key] for key in expected_keys}


def minimal_codex_config() -> bytes:
    provider = codex_provider_config()
    base_url = json.dumps(provider["base_url"])
    name = json.dumps(provider["name"])
    return (
        f'model_provider = "{PROVIDER}"\n'
        f'model = "{MODEL}"\n'
        f'model_reasoning_effort = "{EFFORT}"\n'
        f'service_tier = "{SERVICE_TIER}"\n'
        'approval_policy = "never"\n'
        'sandbox_mode = "danger-full-access"\n'
        'network_access = "enabled"\n\n'
        f'developer_instructions = {json.dumps(WORKER_DEVELOPER_INSTRUCTIONS)}\n\n'
        f'[model_providers.{PROVIDER}]\n'
        f'name = {name}\n'
        f'base_url = {base_url}\n'
        'wire_api = "responses"\n'
        f'supports_websockets = {str(bool(provider["supports_websockets"])).lower()}\n\n'
        '[features]\n'
        'goals = true\n'
        'multi_agent = false\n'
        'multi_agent_v2 = false\n'
        'prevent_idle_sleep = true\n'
    ).encode("utf-8")


def bootstrap_codex_home(home: Path) -> None:
    if not AUTH_SOURCE.is_file() or AUTH_SOURCE.is_symlink():
        raise ControllerError("Codex credential source is unavailable")
    home.mkdir(parents=True, exist_ok=False, mode=0o700)
    shutil.copyfile(AUTH_SOURCE, home / "auth.json")
    os.chmod(home / "auth.json", 0o600)
    atomic_write(home / "config.toml", minimal_codex_config(), 0o600)


def codex_argv(work_root: Path) -> list[str]:
    return [
        CONTAINER_CODEX_BINARY, "-C", str(work_root), "-c", "features.goals=true",
        "-c", "features.multi_agent=false", "-c", "features.multi_agent_v2=false",
        "-c", f'developer_instructions={json.dumps(WORKER_DEVELOPER_INSTRUCTIONS)}',
        "--no-alt-screen", "-m", MODEL,
        "-c", f'model_reasoning_effort="{EFFORT}"',
        "-c", f'service_tier="{SERVICE_TIER}"',
        "-c", f'model_provider="{PROVIDER}"',
        "--dangerously-bypass-approvals-and-sandbox",
    ]


def codex_resume_argv(work_root: Path, thread_id: str) -> list[str]:
    if not isinstance(thread_id, str) or not SAFE_ID_RE.fullmatch(thread_id):
        raise ControllerError("repair resume thread identity is unsafe")
    return [
        CONTAINER_CODEX_BINARY, "resume", thread_id, "-C", str(work_root),
        "-c", "features.goals=true", "-c", "features.multi_agent=false",
        "-c", "features.multi_agent_v2=false",
        "-c", f'developer_instructions={json.dumps(WORKER_DEVELOPER_INSTRUCTIONS)}',
        "--no-alt-screen", "-m", MODEL,
        "-c", f'model_reasoning_effort="{EFFORT}"',
        "-c", f'service_tier="{SERVICE_TIER}"',
        "-c", f'model_provider="{PROVIDER}"',
        "--dangerously-bypass-approvals-and-sandbox",
    ]


def safe_relative(value: str) -> Path:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or value != path.as_posix() or ".." in path.parts:
        raise ControllerError(f"unsafe repository-relative path {value!r}")
    return Path(*path.parts)


def copy_bound(source: Path, destination: Path) -> dict[str, Any]:
    if source.is_symlink() or not source.is_file():
        raise ControllerError(f"bootstrap input is unavailable: {source}")
    raw = source.read_bytes()
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_CLOEXEC, 0o444)
    try:
        os.write(descriptor, raw)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    os.chmod(destination, 0o444)
    if os.stat(source).st_ino == os.stat(destination).st_ino:
        raise ControllerError("bootstrap copy shares an inode")
    return {"path": source.relative_to(ROOT).as_posix(), "sha256": digest(raw), "size_bytes": len(raw)}


def publish_directory(staging: Path, destination: Path) -> None:
    """Publish one fully materialized controller-owned archive atomically."""
    if destination.exists() or destination.is_symlink():
        raise ControllerError(f"archive destination already exists: {destination}")
    for directory in sorted(
        [staging, *(path for path in staging.rglob("*") if path.is_dir() and not path.is_symlink())],
        key=lambda path: len(path.parts), reverse=True,
    ):
        descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    os.rename(staging, destination)
    descriptor = os.open(destination.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def expect_archived_file(path: Path, expected_sha: str, expected_size: int | None = None) -> None:
    if path.is_symlink() or not path.is_file() or file_digest(path) != expected_sha:
        raise ControllerError(f"archived file differs: {path}")
    if expected_size is not None and path.stat().st_size != expected_size:
        raise ControllerError(f"archived file size differs: {path}")


def workset_members() -> dict[str, dict[str, Any]]:
    value = verify_seal(strict_json(WORKSET, "theorem workset"), "theorem workset")
    members = value.get("members")
    if not isinstance(members, list) or len(members) != 3500:
        raise ControllerError("theorem workset members differ")
    return {member["stage_claim_id"]: member for member in members}


def item_stage_claim(item_id: str) -> str | None:
    match = re.fullmatch(r"S5THM-([0-9]{8})-[A-Z0-9-]+", item_id)
    return f"S5-CLM-{match.group(1)}" if match else None


def render_finalizer() -> bytes:
    # A task helper is generated as inert bytes and run by the worker.  It only
    # reads the immutable card, validates exact owned files, executes the card's
    # explicit commands, and emits the closed result/patch inside the task root.
    return b'''#!/usr/bin/env python3
import difflib,hashlib,json,os,pathlib,subprocess,sys,datetime
task=pathlib.Path(__file__).resolve().parent
claim=json.loads((task/"claim.json").read_text())
if pathlib.Path(claim["task_root"]).resolve()!=task:raise SystemExit("task root identity differs")
work=task/"work"
def sha(raw):return hashlib.sha256(raw).hexdigest()
artifacts=[];patch=[]
for relative in claim["writable_paths"]:
 path=work/relative
 if path.is_symlink() or not path.is_file():raise SystemExit("missing owned file: "+relative)
 raw=path.read_bytes()
 if path.suffix==".json":json.loads(raw)
 artifacts.append({"path":str(path),"sha256":sha(raw),"size_bytes":len(raw),"media_type":"application/json" if path.suffix==".json" else "text/plain"})
 text=raw.decode("utf-8")
 patch.extend(difflib.unified_diff([],text.splitlines(True),fromfile="/dev/null",tofile="b/"+relative))
patch_raw="".join(patch).encode()
outbox=work/"_outbox";outbox.mkdir(exist_ok=True)
patch_path=outbox/"changes.patch";patch_path.write_bytes(patch_raw)
outcomes=[]
for command in claim["validation_commands"]:
 started=datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
 env={row["name"]:row["value"] for row in command["environment"]}
 completed=subprocess.run(command["argv"],cwd=work/command["cwd"],env={**os.environ,**env},stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=command["timeout_seconds"])
 finished=datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
 outcomes.append({"command_id":command["command_id"],"argv_sha256":sha(json.dumps(command["argv"],sort_keys=True,separators=(",",":")).encode()),"exit_code":completed.returncode,"passed":completed.returncode==0,"stdout_sha256":sha(completed.stdout),"stderr_sha256":sha(completed.stderr),"started_at":started,"finished_at":finished})
 if completed.returncode:raise SystemExit("validation failed: "+command["command_id"])
unsigned={"schema_version":"awesome-theorems/stage5-proof-debt-worker-result/1.0","program":claim["program"],"claim_id":claim["claim_id"],"run_id":claim["run_id"],"item_id":claim["item_id"],"mode":claim["mode"],"claim_card_sha256":sha((task/"claim.json").read_bytes()),"baseline_sha256":sha(json.dumps(claim["baseline"],ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()),"status":"self_tested","changed_paths":claim["writable_paths"],"patch":{"path":str(patch_path),"sha256":sha(patch_raw),"size_bytes":len(patch_raw)},"command_outcomes":outcomes,"artifacts":artifacts,"completed_at":datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")}
unsigned["authority_sha256"]=sha(json.dumps(unsigned,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode())
(outbox/"result.json").write_text(json.dumps(unsigned,ensure_ascii=False,sort_keys=True,indent=2)+"\\n")
print("SELF_TESTED",claim["item_id"],unsigned["authority_sha256"])
'''


def item_mode(item_id: str) -> str:
    if item_id == "S5THM-PROGRAM-RELEASE":
        return "PROGRAM-RELEASE"
    if item_id.startswith("S5THM-SHARD-"):
        return "SHARD"
    if item_id == "S5THM-AGG-001":
        return "AGG"
    if item_id == "S5THM-QA-001":
        return "QA"
    match = re.fullmatch(r"S5THM-[0-9]{8}-(.+)", item_id)
    if match:
        return "TARGET-" + match.group(1)
    raise ControllerError(f"unsupported claim mode: {item_id}")


def validation_command(item: dict[str, Any]) -> list[dict[str, Any]]:
    owned = item["owned_paths"]
    if not owned:
        raise ControllerError(f"{item['item_id']}: claim has no writable path")
    if re.fullmatch(r"S5THM-[0-9]{8}-(INTAKE|STATEMENT|ANCHOR|TREE|MACHINE|READABLE|VALIDATE|RELEASE)", item["item_id"]):
        argv = [
            "/usr/bin/python3", "-I", "-B",
            str(Path("_baseline/check_stage5_theorem_item.py")),
            "--claim-card", str(Path("../claim.json")), "--work-root", ".",
        ]
        command_id = "stage5-phase-gate"
        timeout = 900
    else:
        first = owned[0]
        argv = ["/usr/bin/python3", "-I", "-B", "-c", (
            "import json,pathlib;json.loads(pathlib.Path(" + repr(first) + ").read_text())"
            if first.endswith(".json") else
            "import pathlib;assert pathlib.Path(" + repr(first) + ").is_file()"
        )]
        command_id = "owned-artifact-parse"
        timeout = 30
    return [{
        "command_id": command_id,
        "cwd": ".",
        "argv": argv,
        "environment": [{"name": "PYTHONDONTWRITEBYTECODE", "value": "1"}],
        "timeout_seconds": timeout,
        "network": "denied",
    }]


def materialize_claim(
    specification: dict[str, Any], item: dict[str, Any], blueprint_raw: bytes,
    state: dict[str, Any], members: dict[str, dict[str, Any]], *, attempt: int = 1,
) -> dict[str, Any]:
    item_id = item["item_id"]
    claim_id = f"{item_id}--producer"
    run_id = f"r-{int(time.time())}-{uuid.uuid4().hex[:8]}"
    if not SAFE_ID_RE.fullmatch(claim_id) or not SAFE_ID_RE.fullmatch(run_id):
        raise ControllerError("claim/run identity is unsafe")
    task_root = PROGRAM_RUNTIME / "tasks" / claim_id / run_id
    work_root = task_root / "work"
    codex_home = task_root / "codex-home"
    task_root.mkdir(parents=True, exist_ok=False, mode=0o700)
    work_root.mkdir(mode=0o700)
    for owned in item["owned_paths"]:
        canonical_owned = ROOT / safe_relative(owned)
        if os.path.lexists(canonical_owned):
            raise ControllerError(f"{item_id}: canonical owned path already exists")
        path = work_root / safe_relative(owned)
        path.parent.mkdir(parents=True, exist_ok=True)
    bootstrap_sources = [
        WORKSET,
        EVIDENCE / "workset-5.6-receipt.json",
        EXECUTION_SPEC,
        EVIDENCE / "provider-registry.json",
        EVIDENCE / "foundation-profiles.json",
    ]
    read_only = [
        copy_bound(source, work_root / source.relative_to(ROOT)) for source in bootstrap_sources
    ]
    baseline_blueprint = work_root / "_baseline/Stage5_Theorems_Blueprint.md"
    baseline_blueprint.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(baseline_blueprint, blueprint_raw, 0o444)
    read_only.append({
        "path": "_baseline/Stage5_Theorems_Blueprint.md",
        "sha256": digest(blueprint_raw), "size_bytes": len(blueprint_raw),
    })
    item_checker = work_root / "_baseline/check_stage5_theorem_item.py"
    atomic_write(item_checker, ITEM_CHECKER_PATH.read_bytes(), 0o444)
    read_only.append({
        "path": "_baseline/check_stage5_theorem_item.py",
        "sha256": file_digest(item_checker), "size_bytes": item_checker.stat().st_size,
    })
    stage_claim = item_stage_claim(item_id)
    member = members.get(stage_claim) if stage_claim else None
    if stage_claim and member is None:
        raise ControllerError(f"{item_id}: workset member is absent")
    member_path = work_root / "_claim/member.json"
    member_path.parent.mkdir(parents=True, exist_ok=True)
    member_value = sealed({
        "schema_version": "awesome-theorems/stage5-task-member/1.0",
        "program": PROGRAM, "item_id": item_id, "stage_claim_id": stage_claim,
        "member": member,
    })
    atomic_json(member_path, member_value, 0o444)
    read_only.append({
        "path": "_claim/member.json", "sha256": file_digest(member_path),
        "size_bytes": member_path.stat().st_size,
    })
    by_id = {row["item_id"]: row for row in checker().parse_blueprint()[1]}
    dependency_artifacts: list[dict[str, Any]] = []
    for dependency in item["dependencies"]:
        if dependency == "S5THM-BOOT-001":
            # BOOT authority is already represented by the individually copied
            # and SHA-bound workset/spec/profile/provider/schema inputs above;
            # duplicating that same multi-megabyte bundle as one dependency
            # snapshot would add no provenance and multiply disk use by 120.
            continue
        dependency_row = by_id[dependency]
        for relative in dependency_row["owned_paths"]:
            source = ROOT / safe_relative(relative)
            if source.is_symlink() or not source.is_file():
                raise ControllerError(f"{item_id}: accepted dependency artifact is absent: {relative}")
            copy_path = Path("_dependencies") / dependency / safe_relative(relative)
            copied = copy_bound(source, work_root / copy_path)
            dependency_artifacts.append({
                "dependency_id": dependency, "path": copy_path.as_posix(),
                "sha256": copied["sha256"], "size_bytes": copied["size_bytes"],
            })
            read_only.append({
                "path": copy_path.as_posix(), "sha256": copied["sha256"],
                "size_bytes": copied["size_bytes"],
            })
    dependency_manifest_path = work_root / "_claim/dependency-artifacts.json"
    dependency_manifest = sealed({
        "schema_version": "awesome-theorems/stage5-dependency-artifacts/1.0",
        "program": PROGRAM, "item_id": item_id,
        "dependencies": list(item["dependencies"]), "artifacts": dependency_artifacts,
    })
    atomic_json(dependency_manifest_path, dependency_manifest, 0o444)
    read_only.append({
        "path": "_claim/dependency-artifacts.json",
        "sha256": file_digest(dependency_manifest_path),
        "size_bytes": dependency_manifest_path.stat().st_size,
    })
    # Read-only inputs are byte-checked again at harvest.  Parent directories
    # remain searchable/writable so an item whose exact ownership lives under
    # Docs can still create its declared file; replacing a bootstrap file makes
    # claim validation fail closed.
    bootstrap_codex_home(codex_home)
    source_bundle = specification["source_bundle"]["sha256"]
    dependency_state = [[dependency, "master_accepted"] for dependency in item["dependencies"]]
    owned_baseline = [[path, None] for path in item["owned_paths"]]
    maxima = specification["operator_budget_policy"]["finite_initial_allowances"]["per_claim_maxima"]
    resource_budget = {
        "model_input_tokens": min(2000000, maxima["model_input_tokens"]),
        "model_output_tokens": min(500000, maxima["model_output_tokens"]),
        "model_turns": min(1000, maxima["model_turns"]),
        "external_launches": min(4, maxima["external_launches"]),
        "wall_seconds": min(7200, maxima["wall_seconds"]),
        "cpu_seconds": min(14400, maxima["cpu_seconds"]),
    }
    claim = {
        "schema_version": "awesome-theorems/stage5-proof-debt-claim-card/1.0",
        "program": PROGRAM,
        "claim_id": claim_id,
        "run_id": run_id,
        "item_id": item_id,
        "mode": item_mode(item_id),
        "dependencies": list(item["dependencies"]),
        "baseline": {
            "execution_spec_sha256": digest(canonical(specification)),
            "blueprint_sha256": digest(blueprint_raw),
            "source_bundle_sha256": source_bundle,
            "dependency_state_sha256": digest(canonical(dependency_state)),
            "owned_paths_baseline_sha256": digest(canonical(owned_baseline)),
        },
        "deadline": datetime.fromtimestamp(time.time() + 7200, timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "task_root": str(task_root),
        "canonical_repository_root": str(ROOT),
        "canonical_write_policy": "forbidden",
        "writable_paths": list(item["owned_paths"]),
        "read_only_bootstrap_files": read_only,
        "deliverable": item["title"] + ". " + item["gate"],
        "validation_commands": validation_command(item),
        "artifact_policy": {
            "allowed_paths": list(item["owned_paths"]),
            "required_paths": list(item["owned_paths"]),
            "forbidden_paths": [
                "Docs/Stage5_Theorems_Blueprint.md", "Docs/Stage5_Theorems_Gantt.md",
                "Docs/catalog", ".git", ".ops",
            ],
        },
        "result_schema": {
            "path": "Docs/evidence/stage5_theorems/worker-result.schema.json",
            "schema_id": "https://awesome-theorems.invalid/schemas/stage5-theorem-worker-result-1.0.json",
            "sha256": file_digest(EVIDENCE / "worker-result.schema.json"),
        },
        "resource_budget": resource_budget,
        "retry_budget": {"attempt": attempt, "max_attempts": 3},
    }
    atomic_json(task_root / "claim.json", claim, 0o444)
    atomic_write(task_root / "finalize.py", render_finalizer(), 0o555)
    claim_record = {
        "claim_id": claim_id, "run_id": run_id, "item_id": item_id, "role": "producer",
        "task_root": str(task_root), "work_root": str(work_root), "codex_home": str(codex_home),
        "socket_argument": "tmux.sock", "socket_path": str(task_root / "tmux.sock"),
        "session": ("s5-" + hashlib.sha256(f"{claim_id}/{run_id}".encode()).hexdigest()[:20]),
        "container_name": ("s5-" + hashlib.sha256(f"container/{claim_id}/{run_id}".encode()).hexdigest()[:24]),
        "status": "materialized", "materialized_at": now(),
        "claim_card_sha256": file_digest(task_root / "claim.json"),
        "goal_submissions": 0, "route": {
            "provider": PROVIDER, "model": MODEL, "reasoning_effort": EFFORT, "service_tier": SERVICE_TIER,
        },
        "budget": resource_budget,
        "attempt": attempt,
    }
    state["claims"][item_id] = claim_record
    append_event("claim_materialized", {
        "item_id": item_id, "claim_id": claim_id, "run_id": run_id,
        "task_root": str(task_root), "claim_card_sha256": claim_record["claim_card_sha256"],
    })
    return claim_record


def tmux(record: dict[str, Any], *arguments: str, input_text: str | None = None, check: bool = True, timeout: float = 30) -> subprocess.CompletedProcess[str]:
    binary = tool_path("tmux")
    if binary is None:
        raise ControllerError("tmux binary is unavailable")
    # The socket argument is deliberately relative and the client/server cwd is
    # the exact task root.  This preserves task locality while staying below
    # sockaddr_un's 108-byte path limit for the long frozen runtime root.
    return run(
        [binary, "-S", record["socket_argument"], *arguments],
        cwd=Path(record["task_root"]), input_text=input_text, check=check, timeout=timeout,
    )


def docker_run_argv(record: dict[str, Any], codex: Sequence[str]) -> list[str]:
    task_root = record["task_root"]
    work_root = record["work_root"]
    codex_home = record["codex_home"]
    return [
        str(DOCKER_BINARY), "run", "--rm", "--interactive", "--tty",
        "--name", record["container_name"], "--hostname", record["container_name"],
        "--user", f"{os.getuid()}:{os.getgid()}", "--network", "host",
        "--security-opt", "no-new-privileges", "--cap-drop", "ALL",
        "--pids-limit", "256", "--memory", "1536m", "--cpus", "2",
        "--read-only", "--tmpfs", "/tmp:rw,nosuid,nodev,size=512m",
        "--mount", f"type=bind,src={task_root},dst={task_root},readonly",
        "--mount", f"type=bind,src={work_root},dst={work_root}",
        "--mount", f"type=bind,src={codex_home},dst={codex_home}",
        "--mount", "type=bind,src=/usr,dst=/usr,readonly",
        "--mount", "type=bind,src=/lib,dst=/lib,readonly",
        "--mount", "type=bind,src=/lib64,dst=/lib64,readonly",
        "--mount", f"type=bind,src={CODEX_NATIVE_BINARY},dst={CONTAINER_CODEX_BINARY},readonly",
        "--mount", f"type=bind,src={CODEX_CODE_MODE_HOST},dst={CONTAINER_CODE_MODE_HOST},readonly",
        "--mount", "type=bind,src=/home/sansha/.elan,dst=/home/sansha/.elan,readonly",
        "--env", f"CODEX_HOME={codex_home}", "--workdir", work_root,
        CONTAINER_IMAGE, *codex,
    ]


def container_inspect(record: dict[str, Any]) -> dict[str, Any] | None:
    name = record.get("container_name")
    if not isinstance(name, str) or not SAFE_ID_RE.fullmatch(name):
        return None
    completed = run(
        [str(DOCKER_BINARY), "container", "inspect", name], check=False, timeout=10,
    )
    if completed.returncode != 0:
        return None
    try:
        values = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return None
    if not isinstance(values, list) or len(values) != 1 or not isinstance(values[0], dict):
        return None
    value = values[0]
    state = value.get("State")
    config = value.get("Config")
    host_config = value.get("HostConfig")
    mounts = value.get("Mounts")
    if not all(isinstance(part, dict) for part in (state, config, host_config)) or not isinstance(mounts, list):
        return None
    mount_map = {
        row.get("Destination"): row
        for row in mounts if isinstance(row, dict) and isinstance(row.get("Destination"), str)
    }
    task_root = record["task_root"]
    work_root = record["work_root"]
    codex_home = record["codex_home"]
    task_mount = mount_map.get(task_root, {})
    work_mount = mount_map.get(work_root, {})
    home_mount = mount_map.get(codex_home, {})
    codex_mount = mount_map.get(CONTAINER_CODEX_BINARY, {})
    code_mode_mount = mount_map.get(CONTAINER_CODE_MODE_HOST, {})
    elan_mount = mount_map.get("/home/sansha/.elan", {})
    expected_env = f"CODEX_HOME={record['codex_home']}"
    try:
        pinned_worker_binaries_match = (
            not CODEX_NATIVE_BINARY.is_symlink()
            and CODEX_NATIVE_BINARY.is_file()
            and file_digest(CODEX_NATIVE_BINARY) == CODEX_NATIVE_SHA256
            and not CODEX_CODE_MODE_HOST.is_symlink()
            and CODEX_CODE_MODE_HOST.is_file()
            and file_digest(CODEX_CODE_MODE_HOST) == CODEX_CODE_MODE_HOST_SHA256
        )
    except OSError:
        pinned_worker_binaries_match = False
    if (
        not pinned_worker_binaries_match
        or
        value.get("Image") != CONTAINER_IMAGE_ID
        or state.get("Running") is not True
        or config.get("WorkingDir") != record["work_root"]
        or expected_env not in config.get("Env", [])
        or config.get("User") != f"{os.getuid()}:{os.getgid()}"
        or host_config.get("ReadonlyRootfs") is not True
        or host_config.get("NetworkMode") != "host"
        or "ALL" not in host_config.get("CapDrop", [])
        or task_mount.get("Source") != task_root or task_mount.get("RW") is not False
        or work_mount.get("Source") != work_root or work_mount.get("RW") is not True
        or home_mount.get("Source") != codex_home or home_mount.get("RW") is not True
        or codex_mount.get("Source") != str(CODEX_NATIVE_BINARY) or codex_mount.get("RW") is not False
        or code_mode_mount.get("Source") != str(CODEX_CODE_MODE_HOST) or code_mode_mount.get("RW") is not False
        or elan_mount.get("Source") != "/home/sansha/.elan" or elan_mount.get("RW") is not False
    ):
        return None
    container_id = value.get("Id")
    pid = state.get("Pid")
    if not isinstance(container_id, str) or not CONTAINER_ID_RE.fullmatch(container_id) or not isinstance(pid, int) or pid <= 0:
        return None
    try:
        container_cwd = Path(os.readlink(f"/proc/{pid}/cwd")).resolve()
        command = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
    except OSError:
        return None
    if (
        container_cwd != Path(record["work_root"]).resolve()
        or process_environment(pid, "CODEX_HOME") != record["codex_home"]
        or not command or command[0].decode("utf-8", errors="replace") != CONTAINER_CODEX_BINARY
    ):
        return None
    return {"container_id": container_id, "container_pid": pid}


def start_tmux(record: dict[str, Any]) -> None:
    task_root = Path(record["task_root"])
    work_root = Path(record["work_root"])
    resume_thread_id = record.get("resume_thread_id")
    argv = (
        codex_resume_argv(work_root, resume_thread_id)
        if isinstance(resume_thread_id, str)
        else codex_argv(work_root)
    )
    environment = [
        "/usr/bin/env", "-u", "CODEX_CI", "-u", "CODEX_THREAD_ID", "-u", "CODEX_REMOTE_PAYLOAD",
        f"CODEX_HOME={record['codex_home']}", *docker_run_argv(record, argv),
    ]
    tmux(
        record, "-f", "/dev/null", "new-session", "-d", "-s", record["session"],
        "-c", str(work_root), *environment, timeout=30,
    )
    pane_pid_text = tmux(
        record, "display-message", "-p", "-t", f"{record['session']}:0.0", "#{pane_pid}",
    ).stdout.strip()
    try:
        pane_pid = int(pane_pid_text)
    except ValueError as exc:
        raise ControllerError("tmux returned an invalid pane PID") from exc
    start_ticks = process_start_ticks(pane_pid)
    if start_ticks is None:
        raise ControllerError("cannot authenticate tmux pane process start time")
    if process_environment(pane_pid, "CODEX_HOME") != record["codex_home"]:
        raise ControllerError("tmux pane lacks the exact private CODEX_HOME")
    container = None
    for _ in range(100):
        container = container_inspect(record)
        if container is not None:
            break
        if process_start_ticks(pane_pid) != start_ticks:
            raise ControllerError("Docker TUI launcher died before container identity appeared")
        time.sleep(0.1)
    if container is None:
        raise ControllerError("worker container identity did not appear")
    container_ticks = process_start_ticks(container["container_pid"])
    if container_ticks is None:
        raise ControllerError("cannot authenticate container Codex PID start time")
    record.update({
        "pane_pid": pane_pid, "pane_pid_start_ticks": start_ticks,
        **container, "container_pid_start_ticks": container_ticks,
        "codex_argv": argv, "status": "tmux_started", "tmux_started_at": now(),
    })
    append_event("tmux_started", {
        "item_id": record["item_id"], "claim_id": record["claim_id"],
        "socket_path": record["socket_path"], "session": record["session"],
        "pane_pid": pane_pid, "pane_pid_start_ticks": start_ticks,
        "container_id": record["container_id"], "container_pid": record["container_pid"],
        "container_pid_start_ticks": record["container_pid_start_ticks"],
    })


def capture(record: dict[str, Any]) -> str:
    return tmux(
        record, "capture-pane", "-p", "-J", "-t", f"{record['session']}:0.0",
        check=False,
    ).stdout


def goal_text(record: dict[str, Any]) -> str:
    token = "GOAL_READY_" + digest(f"{record['claim_id']}/{record['run_id']}".encode())[:32].upper()
    record["goal_completion_token"] = token
    task_root = Path(record["task_root"])
    if record.get("role") == "reviewer":
        return (
            f"/goal Independently review Stage5 theorem item {record['item_id']} as claim "
            f"{record['claim_id']} only. Read immutable {task_root / 'review-card.json'} "
            f"sha256:{record['claim_card_sha256']}. Inspect every copied producer artifact "
            f"against the item gate. Work only in {record['work_root']}; never write the "
            f"canonical checkout or Blueprint. Write review-report.json as instructed, then "
            f"run /usr/bin/python3 {task_root / 'review-finalize.py'} and leave "
            f"{record['work_root']}/_outbox/review-decision.json. Exactly one goal. {token}"
        )
    return (
        f"/goal Execute Stage5 theorem item {record['item_id']} as claim {record['claim_id']} only. "
        f"Read immutable {task_root / 'claim.json'} sha256:{record['claim_card_sha256']}. "
        f"Work only in {record['work_root']}; never write the canonical checkout or Blueprint. "
        f"Satisfy the complete card, then run /usr/bin/python3 {task_root / 'finalize.py'} and leave "
        f"{record['work_root']}/_outbox/result.json. Exactly one goal. {token}"
    )


def render_review_finalizer() -> bytes:
    return b'''#!/usr/bin/env python3
import datetime,hashlib,json,pathlib
task=pathlib.Path(__file__).resolve().parent
card=json.loads((task/"review-card.json").read_text())
work=task/"work";report_path=work/"review-report.json"
report=json.loads(report_path.read_text())
if set(report)!={"decision","findings","reviewed_artifacts"}:raise SystemExit("review report fields differ")
if report["decision"] not in {"accepted","rejected"}:raise SystemExit("review decision differs")
if not isinstance(report["findings"],list) or any(not isinstance(x,str) or not x for x in report["findings"]):raise SystemExit("review findings differ")
expected=[x["path"] for x in card["artifacts"]]
if report["reviewed_artifacts"]!=expected:raise SystemExit("review coverage differs")
def sha(raw):return hashlib.sha256(raw).hexdigest()
for item in card["artifacts"]:
 path=work/item["copy_path"]
 raw=path.read_bytes()
 if path.is_symlink() or len(raw)!=item["size_bytes"] or sha(raw)!=item["sha256"]:raise SystemExit("review input changed: "+item["path"])
unsigned={"schema_version":"awesome-theorems/stage5-review-decision/1.0","program":card["program"],"item_id":card["item_id"],"producer_claim_id":card["producer_claim_id"],"reviewer_claim_id":card["reviewer_claim_id"],"reviewer_run_id":card["reviewer_run_id"],"handoff_manifest_sha256":card["handoff_manifest_sha256"],"decision":report["decision"],"findings":report["findings"],"reviewed_artifacts":card["artifacts"],"completed_at":datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")}
unsigned["authority_sha256"]=sha(json.dumps(unsigned,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode())
out=work/"_outbox";out.mkdir(exist_ok=True)
(out/"review-decision.json").write_text(json.dumps(unsigned,ensure_ascii=False,sort_keys=True,indent=2)+"\\n")
print("REVIEWED",card["item_id"],unsigned["decision"],unsigned["authority_sha256"])
'''


def materialize_review_claim(
    item: dict[str, Any], producer_record: dict[str, Any], state: dict[str, Any],
    *, ordinal: int | None = None,
) -> dict[str, Any]:
    item_id = item["item_id"]
    handoff = producer_record.get("handoff")
    if not isinstance(handoff, dict):
        raise ControllerError(f"{item_id}: producer handoff is absent")
    archive = ROOT / handoff["path"]
    manifest_path = archive / "manifest.json"
    manifest = verify_seal(strict_json(manifest_path, "handoff manifest"), "handoff manifest")
    if file_digest(manifest_path) != handoff["manifest_sha256"]:
        raise ControllerError(f"{item_id}: handoff manifest changed")
    required = review_requirement(item_id)
    ledger_before = state["reviews"].get(item_id, {})
    decisions_before = ledger_before.get("decisions", []) if isinstance(ledger_before, dict) else []
    if ordinal is None:
        ordinal = len(decisions_before) + 1
    if not 1 <= ordinal <= required:
        raise ControllerError(f"{item_id}: reviewer ordinal differs")
    claim_id = f"{item_id}--reviewer-{ordinal:02d}"
    run_id = f"rv-{int(time.time())}-{uuid.uuid4().hex[:8]}"
    task_root = PROGRAM_RUNTIME / "tasks" / claim_id / run_id
    work_root = task_root / "work"
    codex_home = task_root / "codex-home"
    task_root.mkdir(parents=True, mode=0o700)
    work_root.mkdir(mode=0o700)
    artifacts: list[dict[str, Any]] = []
    for artifact in manifest.get("artifacts", []):
        source = ROOT / artifact["archive_path"]
        copy_path = Path("review-input") / safe_relative(artifact["path"])
        copied = copy_bound(source, work_root / copy_path)
        if copied["sha256"] != artifact["sha256"]:
            raise ControllerError(f"{item_id}: archived producer artifact differs")
        artifacts.append({
            "path": artifact["path"], "copy_path": copy_path.as_posix(),
            "sha256": artifact["sha256"], "size_bytes": artifact["size_bytes"],
        })
    card = {
        "schema_version": "awesome-theorems/stage5-review-card/1.0",
        "program": PROGRAM, "item_id": item_id,
        "producer_claim_id": producer_record["claim_id"],
        "reviewer_claim_id": claim_id, "reviewer_run_id": run_id,
        "reviewer_ordinal": ordinal, "required_reviewers": required,
        "reviewer_role": "domain" if ordinal == 1 else "fresh-reader",
        "task_root": str(task_root), "work_root": str(work_root),
        "canonical_repository_root": str(ROOT), "canonical_write_policy": "forbidden",
        "handoff_manifest_path": handoff["path"] + "/manifest.json",
        "handoff_manifest_sha256": handoff["manifest_sha256"],
        "item_gate": item["gate"], "owned_paths": list(item["owned_paths"]),
        "artifacts": artifacts,
        "report_contract": {
            "path": "review-report.json", "decision": ["accepted", "rejected"],
            "required_fields": ["decision", "findings", "reviewed_artifacts"],
        },
    }
    atomic_json(task_root / "review-card.json", card, 0o444)
    atomic_write(task_root / "review-finalize.py", render_review_finalizer(), 0o555)
    bootstrap_codex_home(codex_home)
    record = {
        "claim_id": claim_id, "run_id": run_id, "item_id": item_id,
        "role": "reviewer", "producer_record": producer_record,
        "task_root": str(task_root), "work_root": str(work_root),
        "codex_home": str(codex_home), "socket_argument": "tmux.sock",
        "socket_path": str(task_root / "tmux.sock"),
        "session": "s5r-" + digest(f"{claim_id}/{run_id}".encode())[:20],
        "container_name": "s5r-" + digest(f"container/{claim_id}/{run_id}".encode())[:24],
        "status": "materialized", "materialized_at": now(),
        "claim_card_sha256": file_digest(task_root / "review-card.json"),
        "goal_submissions": 0,
        "route": {"provider": PROVIDER, "model": MODEL, "reasoning_effort": EFFORT, "service_tier": SERVICE_TIER},
        "budget": producer_record["budget"],
    }
    state["claims"][item_id] = record
    ledger = state["reviews"].setdefault(item_id, {
        "status": "review_pending", "required": required, "decisions": [],
    })
    ledger.update({
        "status": "review_materialized", "required": required,
        "claim_id": claim_id, "run_id": run_id, "ordinal": ordinal,
    })
    append_event("review_materialized", {
        "item_id": item_id, "claim_id": claim_id, "run_id": run_id,
        "handoff_manifest_sha256": handoff["manifest_sha256"],
    })
    return record


def review_requirement(item_id: str) -> int:
    return 2 if item_id.endswith("-READABLE") else 1


def idle_composer_ready(pane: str) -> bool:
    lowered = pane.lower()
    if "press enter to continue" in lowered or "yes, i trust" in lowered:
        return False
    return ("openai codex" in lowered or "codex" in lowered) and (">" in pane or "ask codex" in lowered)


def submit_goal(record: dict[str, Any]) -> None:
    if record.get("goal_submissions") != 0:
        raise ControllerError("duplicate goal submission refused")
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        pane = capture(record)
        lowered = pane.lower()
        if "press enter to continue" in lowered or "yes, i trust" in lowered:
            tmux(record, "send-keys", "-t", f"{record['session']}:0.0", "Enter")
            time.sleep(1)
            continue
        if idle_composer_ready(pane):
            break
        time.sleep(0.5)
    else:
        raise ControllerError(f"Codex idle composer did not appear: {capture(record)[-2000:]!r}")
    goal = goal_text(record)
    buffer_name = "goal-" + digest(record["claim_id"].encode())[:12]
    tmux(record, "load-buffer", "-b", buffer_name, "-", input_text=goal)
    tmux(record, "paste-buffer", "-b", buffer_name, "-t", f"{record['session']}:0.0")
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if record["goal_completion_token"] in capture(record):
            break
        time.sleep(0.25)
    else:
        raise ControllerError("complete goal paste token was not observed; partial input is not submitted")
    record["status"] = "goal_pasted"
    append_event("goal_pasted", {
        "item_id": record["item_id"], "claim_id": record["claim_id"],
        "completion_token": record["goal_completion_token"], "goal_sha256": digest(goal.encode()),
    })
    tmux(record, "send-keys", "-t", f"{record['session']}:0.0", "Enter")
    tmux(record, "delete-buffer", "-b", buffer_name, check=False)
    record["goal_submissions"] = 1
    record["goal_submitted_at"] = now()
    record["status"] = "goal_submitted"
    append_event("goal_submitted", {
        "item_id": record["item_id"], "claim_id": record["claim_id"],
        "goal_submissions": 1,
    })


def submit_followup(record: dict[str, Any]) -> None:
    """Submit one ordinary repair turn to the original thread/active goal."""
    if record.get("goal_submissions") != 1 or not record.get("resume_thread_id"):
        raise ControllerError("repair follow-up requires exactly one existing goal")
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        pane = capture(record)
        lowered = pane.lower()
        if "press enter to continue" in lowered or "yes, i trust" in lowered:
            tmux(record, "send-keys", "-t", f"{record['session']}:0.0", "Enter")
            time.sleep(1)
            continue
        if idle_composer_ready(pane):
            break
        time.sleep(0.5)
    else:
        raise ControllerError(f"Codex repair composer did not appear: {capture(record)[-2000:]!r}")
    attempt = int(record.get("repair_attempt", 0))
    token = "FOLLOWUP_READY_" + digest(
        f"{record['claim_id']}/{record['run_id']}/{attempt}".encode()
    )[:32].upper()
    feedback_path = Path(record["work_root"]) / "_repair" / f"attempt-{attempt:02d}.json"
    prompt = (
        f"Repair Stage5 theorem item {record['item_id']} for the existing claim "
        f"{record['claim_id']} and existing active goal. Read immutable reviewer feedback "
        f"{feedback_path}. Correct only the original owned paths in {record['work_root']}, "
        f"rerun /usr/bin/python3 {Path(record['task_root']) / 'finalize.py'}, and leave a new "
        f"_outbox/result.json. This is a follow-up turn; do not create or submit another /goal. {token}"
    )
    buffer_name = "repair-" + digest(f"{record['claim_id']}/{attempt}".encode())[:12]
    tmux(record, "load-buffer", "-b", buffer_name, "-", input_text=prompt)
    tmux(record, "paste-buffer", "-b", buffer_name, "-t", f"{record['session']}:0.0")
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if token in capture(record):
            break
        time.sleep(0.25)
    else:
        raise ControllerError("complete repair paste token was not observed")
    record["status"] = "followup_pasted"
    append_event("repair_followup_pasted", {
        "item_id": record["item_id"], "claim_id": record["claim_id"],
        "repair_attempt": attempt, "completion_token": token,
        "prompt_sha256": digest(prompt.encode()),
    })
    tmux(record, "send-keys", "-t", f"{record['session']}:0.0", "Enter")
    tmux(record, "delete-buffer", "-b", buffer_name, check=False)
    record["followup_submissions"] = int(record.get("followup_submissions", 0)) + 1
    record["goal_submitted_at"] = now()
    record["status"] = "goal_submitted"
    append_event("repair_followup_submitted", {
        "item_id": record["item_id"], "claim_id": record["claim_id"],
        "repair_attempt": attempt, "goal_submissions": 1,
        "followup_submissions": record["followup_submissions"],
    })


def exact_process_identity(record: dict[str, Any]) -> bool:
    pid = record.get("pane_pid")
    if not isinstance(pid, int) or process_start_ticks(pid) != record.get("pane_pid_start_ticks"):
        return False
    try:
        cwd = Path(os.readlink(f"/proc/{pid}/cwd")).resolve()
    except OSError:
        return False
    if cwd != Path(record["work_root"]).resolve():
        return False
    if process_environment(pid, "CODEX_HOME") != record["codex_home"]:
        return False
    container = container_inspect(record)
    if (
        container is None
        or container.get("container_id") != record.get("container_id")
        or container.get("container_pid") != record.get("container_pid")
        or process_start_ticks(container["container_pid"])
        != record.get("container_pid_start_ticks")
    ):
        return False
    sessions = tmux(record, "has-session", "-t", record["session"], check=False)
    return sessions.returncode == 0 and Path(record["socket_path"]).is_socket()


def last_service_tier(rollout: Path) -> str | None:
    observed = None
    try:
        with rollout.open("rb") as stream:
            for raw in stream:
                if b"service_tier" not in raw:
                    continue
                value = json.loads(raw)
                payload = value.get("payload") if isinstance(value, dict) else None
                settings = payload.get("thread_settings") if isinstance(payload, dict) else None
                if isinstance(settings, dict) and isinstance(settings.get("service_tier"), str):
                    observed = settings["service_tier"]
    except (OSError, json.JSONDecodeError):
        return None
    return observed


def private_identity(record: dict[str, Any]) -> dict[str, Any] | None:
    home = Path(record["codex_home"])
    state_db = home / "state_5.sqlite"
    goals_db = home / "goals_1.sqlite"
    if not state_db.is_file() or not goals_db.is_file():
        return None
    try:
        state = sqlite3.connect(f"file:{state_db}?mode=ro", uri=True, timeout=1)
        count = state.execute("select count(*) from threads").fetchone()[0]
        row = state.execute(
            "select id,cwd,model_provider,model,reasoning_effort,rollout_path "
            "from threads order by coalesce(updated_at_ms,updated_at,created_at_ms,created_at) desc limit 1"
        ).fetchone()
        state.close()
        if count != 1 or row is None:
            return None
        goals = sqlite3.connect(f"file:{goals_db}?mode=ro", uri=True, timeout=1)
        goal_count = goals.execute("select count(*) from thread_goals").fetchone()[0]
        goal = goals.execute(
            "select goal_id,objective,status from thread_goals where thread_id=?", (row[0],),
        ).fetchone()
        goals.close()
        if goal_count != 1 or goal is None:
            return None
        rollout = Path(row[5])
        try:
            rollout.relative_to(home / "sessions")
        except ValueError:
            return None
        service_tier = last_service_tier(rollout)
        return {
            "thread_id": row[0], "cwd": row[1], "provider": row[2], "model": row[3],
            "reasoning_effort": row[4], "rollout_path": str(rollout),
            "service_tier": service_tier, "goal_id": goal[0],
            "goal_objective": goal[1], "goal_status": goal[2],
        }
    except (sqlite3.Error, OSError):
        return None


def authenticated_identity(record: dict[str, Any]) -> dict[str, Any] | None:
    """Return a pure read-only proof for a currently authenticated live lane."""
    if not exact_process_identity(record):
        return None
    identity = private_identity(record)
    if identity is None:
        return None
    try:
        cwd_matches = Path(identity["cwd"]).resolve() == Path(record["work_root"]).resolve()
    except (KeyError, OSError):
        return None
    expected = {
        "provider": PROVIDER, "model": MODEL, "reasoning_effort": EFFORT,
        "service_tier": SERVICE_TIER, "goal_status": "active",
    }
    objective = identity.get("goal_objective")
    if (
        not cwd_matches
        or any(identity.get(key) != value for key, value in expected.items())
        or not isinstance(objective, str)
        or record["item_id"] not in objective
        or record["claim_id"] not in objective
    ):
        return None
    return identity


def authenticate(record: dict[str, Any]) -> bool:
    if not exact_process_identity(record):
        raise ControllerError("tmux/PID/start/cwd/private-home identity differs")
    identity = private_identity(record)
    if identity is None:
        return False
    if Path(identity["cwd"]).resolve() != Path(record["work_root"]).resolve():
        raise ControllerError("private thread cwd differs")
    expected = {
        "provider": PROVIDER, "model": MODEL, "reasoning_effort": EFFORT,
        "service_tier": SERVICE_TIER,
    }
    for key, value in expected.items():
        if identity.get(key) != value:
            raise ControllerError(f"resolved route {key} differs: {identity.get(key)!r}")
    if record["item_id"] not in identity["goal_objective"] or record["claim_id"] not in identity["goal_objective"]:
        raise ControllerError("goal objective does not bind item and claim")
    record.update(identity)
    if identity["goal_status"] != "active":
        record["status"] = "goal_submitted"
        return False
    record["status"] = "live"
    record["authenticated_at"] = record.get("authenticated_at") or now()
    append_event("claim_live", {
        "item_id": record["item_id"], "claim_id": record["claim_id"],
        "thread_id": record["thread_id"], "goal_id": record["goal_id"],
        "provider": PROVIDER, "model": MODEL, "reasoning_effort": EFFORT,
        "service_tier": SERVICE_TIER, "goal_submissions": 1,
        "pane_pid": record["pane_pid"], "pane_pid_start_ticks": record["pane_pid_start_ticks"],
    })
    return True


def stop_transport(record: dict[str, Any]) -> None:
    try:
        tmux(record, "kill-server", check=False, timeout=10)
    except (ControllerError, KeyError):
        pass
    name = record.get("container_name")
    if isinstance(name, str) and SAFE_ID_RE.fullmatch(name):
        run([str(DOCKER_BINARY), "rm", "--force", name], check=False, timeout=20)
    pid = record.get("pane_pid")
    if isinstance(pid, int) and process_start_ticks(pid) == record.get("pane_pid_start_ticks"):
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass


def launch(record: dict[str, Any], *, authentication_deadline: float = 90) -> None:
    start_tmux(record)
    if record.get("resume_thread_id"):
        submit_followup(record)
    else:
        submit_goal(record)
    deadline = time.monotonic() + authentication_deadline
    while time.monotonic() < deadline:
        if authenticate(record):
            return
        if not exact_process_identity(record):
            raise ControllerError("Codex TUI died during authentication")
        time.sleep(1)
    # Healthy, exact identity remains starting and a later reconciliation may
    # promote it without a duplicate goal submission.
    if not exact_process_identity(record):
        raise ControllerError("startup deadline expired after identity loss")
    record["status"] = "goal_submitted"
    record["startup_deadline_reason"] = "registry_authentication_delayed"


def readiness(rows: list[dict[str, Any]], state: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    by_id = {row["item_id"]: row for row in rows}
    ready: list[dict[str, Any]] = []
    blocked: dict[str, str] = {}
    claimed = {
        item_id for item_id, record in state["claims"].items()
        if record.get("status") not in {"retired", "launch_failed"}
        or int(record.get("attempt", 1)) >= 3
    }
    for row in rows:
        if row["state"] != " " or row["item_id"] in claimed or row["item_id"] == "S5THM-BOOT-001":
            continue
        missing = [dependency for dependency in row["dependencies"] if by_id[dependency]["state"] != "x"]
        if missing:
            blocked[row["item_id"]] = "dependency:" + ",".join(missing[:4])
        else:
            ready.append(row)
    return ready, blocked


def host_admission(state: dict[str, Any], limits: dict[str, Any]) -> tuple[int, list[str]]:
    active = [claim for claim in state["claims"].values() if claim.get("status") in ACTIVE_STATUSES]
    live = sum(claim.get("status") == "live" for claim in active)
    starting = sum(claim.get("status") in STARTING_STATUSES for claim in active)
    logical = int(limits["logical_claims"]) - len(active)
    running = int(limits["authenticated_live_goals"]) - live - starting
    startup = int(limits["starting_lanes"]) - starting
    reasons: list[str] = []
    memory_available = int(Path("/proc/meminfo").read_text().split("MemAvailable:", 1)[1].split()[0]) * 1024
    disk_available = shutil.disk_usage(ROOT).free
    load1 = os.getloadavg()[0]
    if memory_available < 8 * 1024**3:
        reasons.append(f"host:available_memory_bytes={memory_available}<8589934592")
    if disk_available < 20 * 1024**3:
        reasons.append(f"host:available_disk_bytes={disk_available}<21474836480")
    if load1 > 48.0:
        reasons.append(f"host:load1={load1:.3f}>48")
    if reasons:
        return 0, reasons
    slots = max(0, min(logical, running, startup))
    if slots == 0:
        if logical <= 0:
            reasons.append(f"cap:logical_claims={limits['logical_claims']}")
        if running <= 0:
            reasons.append(
                f"cap:authenticated_live_goals_reserved={live + starting}/"
                f"{limits['authenticated_live_goals']}"
            )
        if startup <= 0:
            reasons.append(
                f"startup:starting_lanes={starting}/{limits['starting_lanes']}"
            )
    return slots, reasons


def generic_admission_pump(
    eligible: Sequence[Any], *, target: int, fanout: int, already_live: int,
    launch_one: Callable[[Any], bool], deadline: float,
) -> tuple[int, list[str]]:
    """Bounded repeated-wave pump used by real and fixture launchers."""
    if min(target, fanout, already_live) < 0 or fanout == 0:
        raise ControllerError("admission pump arguments are invalid")
    launched_live = 0
    reasons: list[str] = []
    cursor = 0
    no_progress = 0
    while already_live + launched_live < target and cursor < len(eligible):
        if time.monotonic() >= deadline:
            reasons.append("tick_budget:startup_pump_deadline")
            break
        wave = eligible[cursor:cursor + min(fanout, target - already_live - launched_live)]
        cursor += len(wave)
        # One wave is intentionally parallel; fanout bounds simultaneous
        # startup pressure while the outer loop remains a repeated-wave pump.
        # launch_one owns per-lane error capture, so a failed future contributes
        # no progress and cannot abort sibling starts.
        with ThreadPoolExecutor(max_workers=len(wave), thread_name_prefix="s5-start") as executor:
            futures = [executor.submit(launch_one, item) for item in wave]
            outcomes = []
            for future in futures:
                try:
                    outcomes.append(bool(future.result()))
                except Exception:
                    outcomes.append(False)
        progress = sum(outcomes)
        launched_live += progress
        no_progress = 0 if progress else no_progress + 1
        if no_progress >= 2:
            reasons.append("startup:no_progress_two_consecutive_waves")
            break
    if already_live + launched_live < target and cursor >= len(eligible):
        reasons.append("dependency:no_additional_eligible_claim")
    return launched_live, reasons


def timestamp_age_seconds(value: Any) -> float | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return max(0.0, time.time() - parsed.timestamp())


def reconcile_claims(
    state: dict[str, Any], *, startup_deadline_seconds: int = 180,
) -> tuple[int, int]:
    def retire(item_id: str, record: dict[str, Any], reason: str) -> None:
        nonlocal retired
        stop_transport(record)
        role = record.get("role")
        if role == "reviewer" and isinstance(record.get("producer_record"), dict):
            producer = record["producer_record"]
            producer["status"] = "handoff_ready"
            state["claims"][item_id] = producer
            previous = state["reviews"].get(item_id, {})
            state["reviews"][item_id] = {
                "status": "review_launch_failed", "error": reason, "updated_at": now(),
                "required": review_requirement(item_id),
                "decisions": previous.get("decisions", []) if isinstance(previous, dict) else [],
            }
        elif record.get("resume_thread_id"):
            record["status"] = "repair_pending"
            record["retire_reason"] = reason
            state["claims"][item_id] = record
            repair = state["repairs"].setdefault(item_id, {})
            repair.update({"status": "repair_pending", "error": reason, "updated_at": now()})
        else:
            record["status"] = "retired"
            record["retire_reason"] = reason
        retired += 1
        append_event("claim_retired", {
            "item_id": item_id, "claim_id": record.get("claim_id"),
            "role": role, "reason": reason,
        })

    promoted = 0
    retired = 0
    for item_id, record in list(state["claims"].items()):
        status = record.get("status")
        if status in {"goal_submitted", "live"}:
            try:
                was_live = status == "live"
                current_live = authenticate(record)
                if current_live and not was_live:
                    promoted += 1
                elif not current_live and was_live:
                    record["status"] = "goal_submitted"
            except ControllerError as exc:
                retire(item_id, record, str(exc))
                continue
            age = timestamp_age_seconds(record.get("goal_submitted_at"))
            if (
                record.get("status") == "goal_submitted"
                and age is not None and age >= startup_deadline_seconds
            ):
                reason = f"startup authentication deadline exceeded ({startup_deadline_seconds}s)"
                retire(item_id, record, reason)
        elif status in STARTING_STATUSES - {"goal_submitted"}:
            age = timestamp_age_seconds(
                record.get("tmux_started_at") or record.get("materialized_at")
                or record.get("reserved_at")
            )
            if age is not None and age >= startup_deadline_seconds:
                reason = f"incomplete startup deadline exceeded ({startup_deadline_seconds}s)"
                retire(item_id, record, reason)
    return promoted, retired


def queue_repair(
    state: dict[str, Any], review: dict[str, Any], findings: list[str], *, source: str,
) -> dict[str, Any]:
    producer = dict(review["producer_record"])
    item_id = producer["item_id"]
    previous = state["repairs"].get(item_id, {})
    attempt = int(previous.get("attempt", 0)) + 1
    failure_identity = digest(canonical({
        "item_id": item_id, "handoff": producer["handoff"]["manifest_sha256"],
        "source": source, "findings": findings,
    }))
    if attempt > 3:
        repair = {
            "status": "repair_exhausted", "attempt": attempt - 1,
            "failure_identity": failure_identity, "source": source,
            "findings": findings, "updated_at": now(),
        }
        state["repairs"][item_id] = repair
        producer["status"] = "repair_exhausted"
        state["claims"][item_id] = producer
        append_event("repair_exhausted", {"item_id": item_id, **repair})
        return repair
    work_root = Path(producer["work_root"])
    repair_dir = work_root / "_repair"
    repair_dir.mkdir(parents=True, exist_ok=True)
    feedback_path = repair_dir / f"attempt-{attempt:02d}.json"
    feedback = sealed({
        "schema_version": "awesome-theorems/stage5-repair-feedback/1.0",
        "program": PROGRAM, "item_id": item_id,
        "producer_claim_id": producer["claim_id"],
        "producer_run_id": producer["run_id"], "attempt": attempt,
        "failure_identity": failure_identity, "source": source,
        "findings": findings, "created_at": now(),
    })
    atomic_json(feedback_path, feedback, 0o444)
    outbox = work_root / "_outbox"
    if outbox.exists() and not outbox.is_symlink():
        history = work_root / "_history" / f"before-repair-{attempt:02d}"
        history.parent.mkdir(parents=True, exist_ok=True)
        if history.exists() or history.is_symlink():
            raise ControllerError(f"{item_id}: repair history target already exists")
        os.replace(outbox, history)
    producer.update({
        "status": "repair_pending", "repair_attempt": attempt,
        "repair_failure_identity": failure_identity,
        "resume_thread_id": producer.get("thread_id"),
        "resume_goal_id": producer.get("goal_id"),
        "followup_submissions": int(producer.get("followup_submissions", 0)),
    })
    if not producer.get("resume_thread_id") or not producer.get("resume_goal_id"):
        raise ControllerError(f"{item_id}: repair lacks original thread/goal identity")
    repair = {
        "status": "repair_pending", "attempt": attempt,
        "failure_identity": failure_identity, "source": source,
        "findings": findings,
        "feedback_path": feedback_path.relative_to(ROOT).as_posix(),
        "feedback_sha256": file_digest(feedback_path), "updated_at": now(),
    }
    state["repairs"][item_id] = repair
    state["reviews"][item_id] = {
        "status": "repair_pending", "superseded_review": {
            "path": review.get("path"), "manifest_sha256": review.get("manifest_sha256"),
            "decision_sha256": review.get("decision_sha256"),
        }, "updated_at": now(),
    }
    state["claims"][item_id] = producer
    append_event("repair_queued", {"item_id": item_id, **repair})
    return repair


def validate_review_decision(
    path: Path, card_path: Path, record: dict[str, Any],
) -> dict[str, Any]:
    card = strict_json(card_path, "review card")
    decision = verify_seal(strict_json(path, "review decision"), "review decision")
    required = {
        "schema_version", "program", "item_id", "producer_claim_id",
        "reviewer_claim_id", "reviewer_run_id", "handoff_manifest_sha256",
        "decision", "findings", "reviewed_artifacts", "completed_at",
        "authority_sha256",
    }
    if (
        set(decision) != required
        or decision.get("schema_version") != "awesome-theorems/stage5-review-decision/1.0"
        or decision.get("program") != PROGRAM
        or decision.get("item_id") != record["item_id"]
        or decision.get("producer_claim_id") != card.get("producer_claim_id")
        or decision.get("reviewer_claim_id") != record["claim_id"]
        or decision.get("reviewer_run_id") != record["run_id"]
        or decision.get("handoff_manifest_sha256") != card.get("handoff_manifest_sha256")
        or decision.get("decision") not in {"accepted", "rejected"}
        or not isinstance(decision.get("findings"), list)
        or any(not isinstance(value, str) or not value for value in decision["findings"])
        or decision.get("reviewed_artifacts") != card.get("artifacts")
    ):
        raise ControllerError(f"{record['item_id']}: review decision binding differs")
    return decision


def harvest_review(state: dict[str, Any], record: dict[str, Any]) -> bool:
    task_root = Path(record["task_root"])
    decision_path = task_root / "work/_outbox/review-decision.json"
    if not decision_path.is_file() or decision_path.is_symlink():
        return False
    card_path = task_root / "review-card.json"
    decision = validate_review_decision(decision_path, card_path, record)
    decision_sha = file_digest(decision_path)
    archive = (
        REVIEW_ROOT / record["item_id"] / record["claim_id"] /
        record["run_id"] / decision_sha
    )
    report_path = task_root / "work/review-report.json"
    manifest = sealed({
        "schema_version": "awesome-theorems/stage5-review-archive/1.0",
        "program": PROGRAM, "item_id": record["item_id"],
        "producer_claim_id": decision["producer_claim_id"],
        "reviewer_claim_id": record["claim_id"], "reviewer_run_id": record["run_id"],
        "thread_id": record.get("thread_id"), "goal_id": record.get("goal_id"),
        "provider": record.get("provider"), "model": record.get("model"),
        "reasoning_effort": record.get("reasoning_effort"),
        "service_tier": record.get("service_tier"),
        "decision": decision["decision"], "decision_sha256": decision_sha,
        "reviewer_ordinal": strict_json(card_path, "review card")["reviewer_ordinal"],
        "handoff_manifest_sha256": decision["handoff_manifest_sha256"],
        "archive_path": archive.relative_to(ROOT).as_posix(), "harvested_at": now(),
    })
    if archive.exists() or archive.is_symlink():
        if archive.is_symlink() or not archive.is_dir():
            raise ControllerError(f"{record['item_id']}: review archive is unsafe")
        expect_archived_file(archive / "review-card.json", file_digest(card_path))
        expect_archived_file(archive / "review-decision.json", decision_sha)
        expect_archived_file(archive / "review-report.json", file_digest(report_path))
        observed = strict_json(archive / "manifest.json", "existing review manifest")
        comparable = dict(manifest); comparable["harvested_at"] = observed.get("harvested_at")
        body = dict(comparable); body.pop("authority_sha256", None)
        comparable["authority_sha256"] = digest(canonical(body))
        if observed != comparable:
            raise ControllerError(f"{record['item_id']}: existing review archive differs")
        manifest = observed
    else:
        archive.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".review-staging-", dir=archive.parent))
        try:
            copy_bound(card_path, staging / "review-card.json")
            copy_bound(decision_path, staging / "review-decision.json")
            copy_bound(report_path, staging / "review-report.json")
            atomic_json(staging / "manifest.json", manifest, 0o444)
            publish_directory(staging, archive)
        finally:
            if staging.exists():
                shutil.rmtree(staging)
    review_decision = {
        "status": "accepted" if decision["decision"] == "accepted" else "rejected",
        "decision": decision["decision"],
        "path": archive.relative_to(ROOT).as_posix(),
        "manifest_sha256": file_digest(archive / "manifest.json"),
        "decision_sha256": decision_sha,
        "producer_record": record["producer_record"],
        "reviewer_claim_id": record["claim_id"], "reviewer_run_id": record["run_id"],
        "thread_id": record.get("thread_id"), "goal_id": record.get("goal_id"),
        "findings": list(decision["findings"]),
        "reviewer_ordinal": manifest["reviewer_ordinal"],
    }
    previous = state["reviews"].get(record["item_id"], {})
    previous_decisions = previous.get("decisions", []) if isinstance(previous, dict) else []
    decisions = [*previous_decisions, review_decision]
    if len({row["reviewer_ordinal"] for row in decisions}) != len(decisions):
        raise ControllerError(f"{record['item_id']}: duplicate reviewer ordinal")
    required = review_requirement(record["item_id"])
    if len(decisions) > required:
        raise ControllerError(f"{record['item_id']}: too many reviewer decisions")
    producer = record["producer_record"]
    if decision["decision"] == "rejected":
        status = "rejected"
    elif len(decisions) == required:
        status = "review_ready"
    else:
        status = "review_partial"
    review = {
        "status": status, "required": required, "decisions": decisions,
        "producer_record": producer, "updated_at": now(),
    }
    state["reviews"][record["item_id"]] = review
    if status == "review_partial":
        producer["status"] = "handoff_ready"
        state["claims"][record["item_id"]] = producer
    else:
        record["status"] = status
        record["review"] = review
    stop_transport(record)
    append_event("review_harvested_before_transport_stop", {
        "item_id": record["item_id"], "decision": decision["decision"],
        "review_manifest_sha256": review_decision["manifest_sha256"],
        "reviewer_ordinal": review_decision["reviewer_ordinal"],
        "collected": len(decisions), "required": required,
    })
    if decision["decision"] == "rejected":
        queue_repair(
            state, review, list(decision["findings"]), source="independent_reviewer",
        )
    return True


def harvest(state: dict[str, Any]) -> int:
    validator = load_module(CLAIM_CHECKER_PATH, "stage5_theorem_claim_checker_for_harvest")
    harvested = 0
    for item_id, record in list(state["claims"].items()):
        if record.get("status") not in {"goal_submitted", "live"}:
            continue
        if record.get("role") == "reviewer":
            if harvest_review(state, record):
                harvested += 1
            continue
        task_root = Path(record["task_root"])
        result_path = task_root / "work/_outbox/result.json"
        if not result_path.is_file() or result_path.is_symlink():
            continue
        result = validator.validate_result(result_path, task_root / "claim.json")
        result_sha = file_digest(result_path)
        patch_path = Path(result["patch"]["path"])
        archive = HANDOFF_ROOT / item_id / record["claim_id"] / record["run_id"] / result_sha
        archived_artifacts: list[dict[str, Any]] = []
        for artifact in result["artifacts"]:
            source = Path(artifact["path"])
            relative = source.relative_to(task_root / "work")
            if relative.as_posix() not in result["changed_paths"]:
                raise ControllerError(f"{item_id}: artifact is outside exact changed paths")
            archived_artifacts.append({
                "path": relative.as_posix(), "sha256": artifact["sha256"],
                "size_bytes": artifact["size_bytes"],
                "archive_path": (archive / "artifacts" / relative).relative_to(ROOT).as_posix(),
            })
        manifest = sealed({
            "schema_version": "awesome-theorems/stage5-handoff-archive/1.0",
            "program": PROGRAM, "item_id": item_id, "claim_id": record["claim_id"],
            "run_id": record["run_id"], "claim_card_sha256": record["claim_card_sha256"],
            "worker_result_sha256": result_sha, "patch_sha256": result["patch"]["sha256"],
            "archive_path": archive.relative_to(ROOT).as_posix(), "harvested_at": now(),
            "artifacts": archived_artifacts,
        })
        if archive.exists() or archive.is_symlink():
            if archive.is_symlink() or not archive.is_dir():
                raise ControllerError(f"{item_id}: handoff archive is unsafe")
            expect_archived_file(archive / "claim.json", record["claim_card_sha256"])
            expect_archived_file(archive / "result.json", result_sha)
            expect_archived_file(archive / "changes.patch", result["patch"]["sha256"], result["patch"]["size_bytes"])
            for artifact in archived_artifacts:
                expect_archived_file(
                    ROOT / artifact["archive_path"], artifact["sha256"], artifact["size_bytes"],
                )
            observed = strict_json(archive / "manifest.json", "existing handoff manifest")
            comparable = dict(manifest); comparable["harvested_at"] = observed.get("harvested_at")
            body = dict(comparable); body.pop("authority_sha256", None)
            comparable["authority_sha256"] = digest(canonical(body))
            if observed != comparable:
                raise ControllerError(f"{item_id}: existing handoff archive differs")
            manifest = observed
        else:
            archive.parent.mkdir(parents=True, exist_ok=True)
            staging = Path(tempfile.mkdtemp(prefix=".handoff-staging-", dir=archive.parent))
            try:
                copy_bound(task_root / "claim.json", staging / "claim.json")
                copy_bound(result_path, staging / "result.json")
                copy_bound(patch_path, staging / "changes.patch")
                for artifact, archived in zip(result["artifacts"], archived_artifacts):
                    copied = copy_bound(
                        Path(artifact["path"]), staging / "artifacts" / safe_relative(archived["path"]),
                    )
                    if copied["sha256"] != artifact["sha256"]:
                        raise ControllerError(f"{item_id}: artifact changed during archival")
                atomic_json(staging / "manifest.json", manifest, 0o444)
                publish_directory(staging, archive)
            finally:
                if staging.exists():
                    shutil.rmtree(staging)
        manifest_sha = file_digest(archive / "manifest.json")
        if not record.get("repair_attempt"):
            transition = advance_checklist(
                item_id, " ", "_", guard_sha256={
                    archive / "manifest.json": manifest_sha,
                    archive / "result.json": result_sha,
                    archive / "changes.patch": result["patch"]["sha256"],
                },
            )
        else:
            current_row = next(
                row for row in checker().parse_blueprint()[1]
                if row["item_id"] == item_id
            )
            if current_row["state"] != "_":
                raise ControllerError(f"{item_id}: repair harvest requires underscore state")
            transition = {
                "pre_blueprint_sha256": file_digest(BLUEPRINT),
                "pre_gantt_sha256": file_digest(GANTT),
                "post_blueprint_sha256": file_digest(BLUEPRINT),
                "post_gantt_sha256": file_digest(GANTT),
            }
        record["status"] = "handoff_ready"
        record["handoff"] = {
            "path": archive.relative_to(ROOT).as_posix(),
            "manifest_sha256": manifest_sha,
            "worker_result_sha256": result_sha,
            "transition": transition,
        }
        state["handoffs"][item_id] = record["handoff"]
        if item_id in state.get("repairs", {}):
            state["repairs"][item_id]["status"] = "repair_handoff_ready"
            state["repairs"][item_id]["handoff_manifest_sha256"] = manifest_sha
            state["repairs"][item_id]["updated_at"] = now()
            state["reviews"][item_id] = {
                "status": "repair_handoff_ready",
                "handoff_manifest_sha256": manifest_sha,
                "updated_at": now(),
            }
        stop_transport(record)
        harvested += 1
        append_event("handoff_harvested_before_transport_stop", {
            "item_id": item_id, **record["handoff"],
        })
    return harvested


def canonical_parent(path: Path) -> None:
    try:
        relative = path.relative_to(ROOT)
    except ValueError as exc:
        raise ControllerError(f"integration path escapes canonical root: {path}") from exc
    current = ROOT
    for part in relative.parts[:-1]:
        current = current / part
        if current.exists() or current.is_symlink():
            if current.is_symlink() or not current.is_dir():
                raise ControllerError(f"integration parent is unsafe: {current}")
        else:
            current.mkdir(mode=0o755)


def publish_exact(source: Path, destination: Path, expected_sha: str) -> dict[str, Any]:
    if source.is_symlink() or not source.is_file() or file_digest(source) != expected_sha:
        raise ControllerError(f"integration source differs: {source}")
    canonical_parent(destination)
    if destination.exists() or destination.is_symlink():
        if destination.is_symlink() or not destination.is_file() or file_digest(destination) != expected_sha:
            raise ControllerError(f"integration refuses conflicting canonical bytes: {destination}")
    else:
        copy_bound(source, destination)
    return {
        "path": destination.relative_to(ROOT).as_posix(),
        "sha256": expected_sha, "size_bytes": destination.stat().st_size,
    }


def preflight_publish_exact(source: Path, destination: Path, expected_sha: str) -> None:
    if source.is_symlink() or not source.is_file() or file_digest(source) != expected_sha:
        raise ControllerError(f"integration source differs: {source}")
    relative = destination.relative_to(ROOT)
    current = ROOT
    for part in relative.parts[:-1]:
        current = current / part
        if current.exists() or current.is_symlink():
            if current.is_symlink() or not current.is_dir():
                raise ControllerError(f"integration parent is unsafe: {current}")
    if destination.exists() or destination.is_symlink():
        if destination.is_symlink() or not destination.is_file() or file_digest(destination) != expected_sha:
            raise ControllerError(f"integration refuses conflicting canonical bytes: {destination}")


def validate_staged_artifacts(
    item: dict[str, Any], artifacts: list[dict[str, Any]], producer: dict[str, Any],
) -> dict[str, Any]:
    PROGRAM_RUNTIME.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="master-validation-", dir=PROGRAM_RUNTIME) as directory:
        staged = Path(directory) / "work"
        staged.mkdir()
        claim_path = Path(producer["task_root"]) / "claim.json"
        claim = strict_json(claim_path, "producer claim for Master validation")
        if file_digest(claim_path) != producer["claim_card_sha256"]:
            raise ControllerError(f"{item['item_id']}: producer claim changed")
        for readonly in claim["read_only_bootstrap_files"]:
            source = Path(producer["work_root"]) / safe_relative(readonly["path"])
            destination = staged / safe_relative(readonly["path"])
            copied = copy_bound(source, destination)
            if (
                copied["sha256"] != readonly["sha256"]
                or copied["size_bytes"] != readonly["size_bytes"]
            ):
                raise ControllerError(f"{item['item_id']}: Master read-only input differs")
        for artifact in artifacts:
            source = ROOT / artifact["archive_path"]
            destination = staged / safe_relative(artifact["path"])
            copied = copy_bound(source, destination)
            if copied["sha256"] != artifact["sha256"]:
                raise ControllerError(f"{item['item_id']}: staged artifact differs")
            os.chmod(destination, 0o644)
        command = validation_command(item)[0]
        if command["command_id"] == "stage5-phase-gate":
            argv = [
                "/usr/bin/python3", "-I", "-B", str(ITEM_CHECKER_PATH),
                "--claim-card", str(claim_path), "--work-root", str(staged),
            ]
        else:
            argv = command["argv"]
        completed = run(
            argv, cwd=staged / command["cwd"], check=False,
            timeout=command["timeout_seconds"],
        )
    return {
        "gate_id": command["command_id"],
        "command_sha256": digest(canonical(argv)),
        "exit_code": completed.returncode, "passed": completed.returncode == 0,
        "stdout_sha256": digest(completed.stdout.encode()),
        "stderr_sha256": digest(completed.stderr.encode()),
    }


def tree_digest(paths: Sequence[str]) -> str:
    rows = []
    for relative in paths:
        path = ROOT / safe_relative(relative)
        rows.append([relative, file_digest(path) if path.is_file() and not path.is_symlink() else None])
    return digest(canonical(rows))


def master_integrate(
    item: dict[str, Any], review: dict[str, Any], state: dict[str, Any],
) -> dict[str, Any]:
    item_id = item["item_id"]
    producer = review["producer_record"]
    handoff = producer["handoff"]
    handoff_root = ROOT / handoff["path"]
    handoff_manifest_path = handoff_root / "manifest.json"
    handoff_manifest = verify_seal(
        strict_json(handoff_manifest_path, "handoff manifest"), "handoff manifest"
    )
    decisions = review.get("decisions")
    required_reviews = review_requirement(item_id)
    if (
        review.get("status") != "review_ready" or review.get("required") != required_reviews
        or not isinstance(decisions, list) or len(decisions) != required_reviews
    ):
        raise ControllerError(f"{item_id}: required review decision set is incomplete")
    review_manifests: list[tuple[Path, dict[str, Any], dict[str, Any]]] = []
    for ordinal, decision in enumerate(decisions, 1):
        review_root = ROOT / decision["path"]
        review_manifest_path = review_root / "manifest.json"
        review_manifest = verify_seal(
            strict_json(review_manifest_path, "review manifest"), "review manifest"
        )
        if (
            decision.get("reviewer_ordinal") != ordinal
            or decision.get("decision") != "accepted"
            or file_digest(review_manifest_path) != decision["manifest_sha256"]
            or review_manifest.get("reviewer_ordinal") != ordinal
            or review_manifest.get("decision") != "accepted"
            or review_manifest.get("handoff_manifest_sha256") != handoff["manifest_sha256"]
            or review_manifest.get("producer_claim_id") != producer["claim_id"]
            or review_manifest.get("reviewer_claim_id") == producer["claim_id"]
            or review_manifest.get("thread_id") == producer.get("thread_id")
            or review_manifest.get("goal_id") == producer.get("goal_id")
        ):
            raise ControllerError(f"{item_id}: reviewer {ordinal} authority differs")
        review_manifests.append((review_manifest_path, review_manifest, decision))
    reviewer_claims = [row[1]["reviewer_claim_id"] for row in review_manifests]
    reviewer_threads = [row[1]["thread_id"] for row in review_manifests]
    reviewer_goals = [row[1]["goal_id"] for row in review_manifests]
    if any(len(values) != len(set(values)) for values in (reviewer_claims, reviewer_threads, reviewer_goals)):
        raise ControllerError(f"{item_id}: reviewer identities are not pairwise independent")
    if file_digest(handoff_manifest_path) != handoff["manifest_sha256"]:
        raise ControllerError(f"{item_id}: producer handoff manifest differs")
    result = strict_json(handoff_root / "result.json", "archived worker result")
    claim = strict_json(handoff_root / "claim.json", "archived claim")
    expected_paths = list(item["owned_paths"])
    artifacts = handoff_manifest.get("artifacts")
    if (
        not isinstance(artifacts, list)
        or [artifact.get("path") for artifact in artifacts] != expected_paths
        or result.get("changed_paths") != expected_paths
        or claim.get("writable_paths") != expected_paths
    ):
        raise ControllerError(f"{item_id}: integrated ownership differs")
    for artifact in artifacts:
        source = ROOT / artifact["archive_path"]
        destination = ROOT / safe_relative(artifact["path"])
        preflight_publish_exact(source, destination, artifact["sha256"])
    gate = validate_staged_artifacts(item, artifacts, producer)
    if not gate["passed"]:
        raise MasterValidationError(f"{item_id}: Master validation failed")
    pre_tree = claim["baseline"]["owned_paths_baseline_sha256"]
    integrated_files = [{
        "path": artifact["path"], "sha256": artifact["sha256"],
        "size_bytes": artifact["size_bytes"],
    } for artifact in artifacts]
    post_tree = digest(canonical([
        [artifact["path"], artifact["sha256"]] for artifact in artifacts
    ]))
    old_blueprint, old_gantt, new_blueprint, new_gantt, _ = projection_candidate(
        item_id, "_", "x"
    )
    baseline_sha = result["baseline_sha256"]
    review_decision_sha = digest(canonical([
        decision["decision_sha256"] for _, _, decision in review_manifests
    ]))
    acceptance = sealed({
        "schema_version": "awesome-theorems/stage5-proof-debt-master-acceptance/1.0",
        "program": PROGRAM, "item_id": item_id, "mode": item_mode(item_id),
        "master": {
            "principal_id": f"codex-user-goal:{GOAL_THREAD_ID}",
            "decision_id": f"master-{item_id.lower()}-{post_tree[:16]}",
            "authentication_sha256": operator_authentication_sha256(),
        },
        "handoff": {
            "claim_id": producer["claim_id"], "run_id": producer["run_id"],
            "claim_card_sha256": producer["claim_card_sha256"],
            "worker_result_sha256": handoff["worker_result_sha256"],
            "baseline_sha256": baseline_sha,
            "patch_sha256": handoff_manifest["patch_sha256"],
            "immutable_archive_path": handoff["path"],
            "immutable_archive_sha256": handoff["manifest_sha256"],
        },
        "review_decisions": [{
            "reviewer_id": manifest["reviewer_claim_id"], "decision": "accepted",
            "decision_receipt_path": decision["path"] + "/review-decision.json",
            "decision_receipt_sha256": decision["decision_sha256"],
        } for _, manifest, decision in review_manifests],
        "integration": {
            "pre_tree_sha256": pre_tree, "post_tree_sha256": post_tree,
            "integrated_bytes_sha256": digest(canonical(integrated_files)),
            "integrated_files": integrated_files,
        },
        "validation_gates": [gate],
        "state_transition": {
            "from": "handoff_waiting_master", "to": "master_accepted",
            "pre_blueprint_sha256": digest(old_blueprint),
            "post_blueprint_sha256": digest(new_blueprint),
            "post_gantt_sha256": digest(new_gantt),
        },
        "accepted_at": now(),
    })
    acceptance_path = (
        ACCEPTANCE_ROOT / item_id / baseline_sha / post_tree /
        review_decision_sha / f"{digest(old_blueprint)}.json"
    )
    if acceptance_path.exists() or acceptance_path.is_symlink():
        observed = strict_json(acceptance_path, "existing Master acceptance")
        # accepted_at is fixed by the first durable attempt; all other fields
        # must be identical before it may be reused.
        comparable = dict(acceptance); comparable["accepted_at"] = observed.get("accepted_at")
        body = dict(comparable); body.pop("authority_sha256", None)
        comparable["authority_sha256"] = digest(canonical(body))
        if observed != comparable:
            raise ControllerError(f"{item_id}: existing Master acceptance differs")
        acceptance = observed
    else:
        atomic_json(acceptance_path, acceptance, 0o444)
    validator = load_module(CLAIM_CHECKER_PATH, "stage5_acceptance_validator_for_master")
    validator.validate_acceptance(acceptance_path)
    published = []
    for artifact in artifacts:
        source = ROOT / artifact["archive_path"]
        destination = ROOT / safe_relative(artifact["path"])
        published.append(publish_exact(source, destination, artifact["sha256"]))
    if tree_digest(expected_paths) != post_tree:
        raise ControllerError(f"{item_id}: Master published tree differs")
    if published != integrated_files:
        raise ControllerError(f"{item_id}: Master publication manifest differs")
    transition = advance_checklist(
        item_id, "_", "x", guard_sha256={
            acceptance_path: file_digest(acceptance_path),
            handoff_manifest_path: handoff["manifest_sha256"],
            **{path: decision["manifest_sha256"] for path, _, decision in review_manifests},
            **{ROOT / row["path"]: row["sha256"] for row in integrated_files},
        },
    )
    integrated = {
        "status": "master_accepted", "acceptance_path": acceptance_path.relative_to(ROOT).as_posix(),
        "acceptance_sha256": file_digest(acceptance_path), "transition": transition,
    }
    state["integrations"][item_id] = integrated
    state["claims"][item_id]["status"] = "master_accepted"
    append_event("master_integrated", {"item_id": item_id, **integrated})
    return integrated


def row_index(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {row["item_id"]: row for row in rows}


def integration_candidates(
    rows: list[dict[str, Any]], state: dict[str, Any], *, limit: int,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    by_id = row_index(rows)
    selected: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for item_id, review in state["reviews"].items():
        row = by_id.get(item_id)
        if (
            row is not None and row["state"] == "_"
            and review.get("status") == "review_ready"
            and all(by_id[dependency]["state"] == "x" for dependency in row["dependencies"])
            and state["integrations"].get(item_id, {}).get("status") != "master_accepted"
        ):
            selected.append((row, review))
            if len(selected) >= limit:
                break
    return selected


def review_candidates(
    rows: list[dict[str, Any]], state: dict[str, Any], *, limit: int,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    by_id = row_index(rows)
    selected: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for item_id, record in state["claims"].items():
        row = by_id.get(item_id)
        if (
            row is not None and row["state"] == "_"
            and record.get("role") == "producer"
            and record.get("status") == "handoff_ready"
            and state["reviews"].get(item_id, {}).get("status") not in {
                "review_reserved", "review_materialized", "review_ready", "rejected",
            }
            and all(by_id[dependency]["state"] == "x" for dependency in row["dependencies"])
        ):
            selected.append((row, record))
            if len(selected) >= limit:
                break
    return selected


def repair_candidates(
    rows: list[dict[str, Any]], state: dict[str, Any], *, limit: int,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    by_id = row_index(rows)
    selected: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for item_id, repair in state["repairs"].items():
        row = by_id.get(item_id)
        record = state["claims"].get(item_id)
        if (
            row is not None and row["state"] == "_"
            and repair.get("status") == "repair_pending"
            and isinstance(record, dict) and record.get("status") == "repair_pending"
        ):
            selected.append((row, record))
            if len(selected) >= limit:
                break
    return selected


def reserve_role_work(
    state: dict[str, Any], rows: list[dict[str, Any]], slots: int,
) -> tuple[list[tuple[str, dict[str, Any], dict[str, Any]]], int]:
    reservations: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    for row, record in repair_candidates(rows, state, limit=slots):
        record["status"] = "repair_reserved"
        record["reserved_at"] = now()
        state["repairs"][row["item_id"]]["status"] = "repair_reserved"
        reservations.append(("repair", row, record))
    remaining = slots - len(reservations)
    if remaining > 0:
        for row, record in review_candidates(rows, state, limit=remaining):
            previous = state["reviews"].get(row["item_id"], {})
            decisions = previous.get("decisions", []) if isinstance(previous, dict) else []
            required = review_requirement(row["item_id"])
            record["status"] = "review_reserved"
            state["reviews"][row["item_id"]] = {
                "status": "review_reserved", "producer_claim_id": record["claim_id"],
                "reserved_at": now(), "required": required,
                "decisions": decisions, "ordinal": len(decisions) + 1,
            }
            reservations.append(("review", row, record))
    return reservations, slots - len(reservations)


def snapshot(state: dict[str, Any], rows: list[dict[str, Any]], underfill: list[str]) -> dict[str, Any]:
    items: dict[str, Any] = {}
    status_counts = Counter()
    for item_id, record in state["claims"].items():
        status = record.get("status", "unknown")
        status_counts[status] += 1
        role_name = "reviewer" if record.get("role") == "reviewer" else "producer"
        role_records: dict[str, Any] = {role_name: record}
        if role_name == "reviewer" and isinstance(record.get("producer_record"), dict):
            role_records["producer"] = record["producer_record"]
        review_ledger = state["reviews"].get(item_id, {})
        if isinstance(review_ledger, dict):
            for decision in review_ledger.get("decisions", []):
                if isinstance(decision, dict):
                    ordinal = int(decision.get("reviewer_ordinal", 0))
                    role_records[f"reviewer-{ordinal:02d}"] = decision
        roles = {}
        for role, role_record in role_records.items():
            role_status = role_record.get("status", "unknown")
            roles[role] = {
                "claim_id": role_record.get("claim_id"),
                "run_id": role_record.get("run_id"),
                "owner": "codex-worker", "status": role_status,
                "startup": role_status in STARTING_STATUSES,
                "live": role_status == "live", "running": role_status == "live",
                "thread_id": role_record.get("thread_id"),
                "goal_id": role_record.get("goal_id"),
                "provider": role_record.get("provider"), "model": role_record.get("model"),
                "reasoning_effort": role_record.get("reasoning_effort"),
                "service_tier": role_record.get("service_tier"),
                "budget": role_record.get("budget"),
                "handoff": role_record.get("handoff"),
                "decision": role_record.get("decision") or (
                    role_record.get("review", {}).get("decision")
                    if isinstance(role_record.get("review"), dict) else None
                ),
            }
        block = None
        if status in STARTING_STATUSES:
            block = {"kind": "startup", "reason": record.get("startup_deadline_reason")}
        repair = state["repairs"].get(item_id)
        integration = state["integrations"].get(item_id)
        if isinstance(repair, dict) and repair.get("status") == "repair_exhausted":
            block = {"kind": "repair", "reason": "repair_attempts_exhausted"}
        elif isinstance(integration, dict) and integration.get("status") == "integration_failed":
            block = {"kind": "integration", "reason": integration.get("error")}
        items[item_id] = {
            "roles": roles, "block": block,
            "integration": integration, "repair": repair,
            "timing": {
                "status": "recorded" if record.get("materialized_at") else "unscheduled",
                "start": record.get("materialized_at"),
                "end": record.get("authenticated_at"),
                "duration_seconds": None,
                "source": "controller-state" if record.get("materialized_at") else None,
            },
        }
    active = [record for record in state["claims"].values() if record.get("status") in ACTIVE_STATUSES]
    observed = {
        "logical_claims": len(active),
        "starting_lanes": sum(record.get("status") in STARTING_STATUSES for record in active),
        "authenticated_live_goals": sum(record.get("status") == "live" for record in active),
        "running_turns": sum(record.get("status") == "live" for record in active),
        "canonical_integrations": len(state["integrations"]),
        "lean_build_validators": 0,
        "external_launches_this_wave": state.get("external_launches_this_wave", 0),
    }
    unsigned = {
        "schema_version": "awesome-theorems/stage5-runtime-snapshot/1.0",
        "program": PROGRAM,
        "snapshot_id": str(uuid.uuid4()),
        "generated_at": now(),
        "state_sha256": file_digest(STATE_PATH) if STATE_PATH.exists() else None,
        "event_ledger_records": validate_event_ledger(),
        "items": items,
        "observed_usage": observed,
        "saturated_dimensions": [key for key, value in observed.items() if key in {
            "logical_claims", "starting_lanes", "authenticated_live_goals", "running_turns"
        } and value >= {"logical_claims": 120, "starting_lanes": 8, "authenticated_live_goals": 120, "running_turns": 120}[key]],
        "underfill": {
            "authenticated_live_goal_slots": max(0, 120 - observed["authenticated_live_goals"]),
            "binding_reasons": sorted(set(underfill)),
        },
        "status_counts": dict(sorted(status_counts.items())),
    }
    return sealed(unsigned)


def refresh_projection(state: dict[str, Any], rows: list[dict[str, Any]], underfill: list[str]) -> None:
    state["underfill_reasons"] = sorted(set(underfill))
    save_state(state)
    atomic_json(SNAPSHOT_PATH, snapshot(state, rows, underfill), 0o644)
    generator = load_module(GANTT_GENERATOR_PATH, "stage5_theorem_gantt_for_controller")
    generator.atomic_write(GANTT, generator.render())


def tick() -> dict[str, Any]:
    require_canonical_root()
    check_result = validate_only()
    if not check_result["valid"]:
        raise ControllerError(f"validate-only failed: {check_result['errors']}")
    if bootstrap_state() != "x":
        raise ControllerError("BOOT is not Master accepted")
    validate_activation_receipt()
    runtime_preflight()
    specification, rows, blueprint_raw = load_program()
    specification_sha = digest(canonical(specification))
    started = time.monotonic()
    tick_id = str(uuid.uuid4())
    tick_budget = int(specification["scheduler"]["tick_budget_seconds"])
    deadline = started + tick_budget
    startup_deadline = int(specification["scheduler"]["startup_deadline_seconds"])
    harvested = promoted = retired = 0
    with FileLock(SCHEDULER_LOCK, blocking=False):
        state = load_state(specification_sha, create=True)
        validate_event_ledger()
        active_tick = state.get("active_tick")
        if (
            isinstance(active_tick, dict)
            and active_tick.get("tick_id") != tick_id
            and (timestamp_age_seconds(active_tick.get("started_at")) or 0) < tick_budget + 30
        ):
            raise ControllerError("another bounded scheduler invocation is active")
        state["active_tick"] = {"tick_id": tick_id, "started_at": now()}
        save_state(state)

    # Harvest and authentication inspect task files, SQLite registries and tmux
    # outside the repository scheduler lease.  The durable active_tick token
    # prevents a second cron invocation from racing and expires after one
    # bounded tick budget plus recovery grace; no lock descriptor is inherited.
    harvested = harvest(state)
    promoted, retired = reconcile_claims(
        state, startup_deadline_seconds=startup_deadline,
    )
    state["last_tick"] = now()
    if harvested or promoted or retired:
        state["last_progress"] = state["last_tick"]
    state["external_launches_this_wave"] = 0
    with FileLock(SCHEDULER_LOCK):
        save_state(state)

    # Harvest can advance blank rows to underscore, so all later dependency and
    # integration choices use a fresh authoritative parse.
    specification, rows, blueprint_raw = load_program()
    integrated = 0
    integration_failures: list[str] = []
    for item, review in integration_candidates(
        rows, state, limit=int(specification["default_limits"]["integration"]),
    ):
        if time.monotonic() >= deadline:
            break
        try:
            master_integrate(item, review, state)
            integrated += 1
            state["last_progress"] = now()
        except MasterValidationError as exc:
            integration_failures.append(f"validator:{item['item_id']}:{exc}")
            queue_repair(
                state, review, [str(exc)], source="master_validation",
            )
        except ControllerError as exc:
            state["integrations"][item["item_id"]] = {
                "status": "integration_failed", "error": str(exc), "updated_at": now(),
            }
            integration_failures.append(f"integration:{item['item_id']}:{exc}")
            append_event("master_integration_failed", {
                "item_id": item["item_id"], "error": str(exc),
            })
    if integrated:
        specification, rows, blueprint_raw = load_program()
    with FileLock(SCHEDULER_LOCK):
        save_state(state)

    # The scheduler lease is closed before every task preparation and TUI
    # startup. Repeated reserve/launch/merge cycles make starting_lanes a
    # pressure bound rather than a hidden steady-state cap of eight.
    launch_failures: list[str] = []
    fanout = int(specification["default_limits"]["launch_fanout_per_wave"])
    members = workset_members()
    total_reserved = 0
    total_authenticated = 0
    underfill: list[str] = []

    def launch_one(record: dict[str, Any]) -> bool:
        try:
            validate_operator_authority()
            launch(record, authentication_deadline=min(90, max(1, deadline - time.monotonic())))
            return record.get("status") == "live"
        except Exception as exc:
            record["status"] = "launch_failed"
            record["launch_error"] = str(exc)
            stop_transport(record)
            launch_failures.append(f"startup:{record['item_id']}:{exc}")
            return False

    while time.monotonic() < deadline:
        with FileLock(SCHEDULER_LOCK):
            state = load_state(specification_sha, create=False)
            if state.get("active_tick", {}).get("tick_id") != tick_id:
                raise ControllerError("scheduler invocation ownership changed")
            # A previous wave may have become authentic while this invocation
            # was outside the lease; promote it before computing fresh slots.
            ready, dependency_blocks = readiness(rows, state)
            slots, admission_reasons = host_admission(
                state, specification["default_limits"]
            )
            live_before = sum(
                record.get("status") == "live"
                for record in state["claims"].values()
            )
            if live_before >= int(specification["default_limits"]["authenticated_live_goals"]):
                underfill = []
                save_state(state)
                break
            role_reservations, producer_slots = reserve_role_work(
                state, rows, slots,
            )
            producer_rows = ready[:producer_slots]
            for item in producer_rows:
                previous = state["claims"].get(item["item_id"], {})
                attempt = min(3, int(previous.get("attempt", 0)) + 1)
                state["claims"][item["item_id"]] = {
                    "item_id": item["item_id"], "role": "producer",
                    "status": "producer_reserved", "reserved_at": now(),
                    "attempt": attempt,
                }
            reserved_work = role_reservations + [
                ("producer", item, state["claims"][item["item_id"]])
                for item in producer_rows
            ]
            reservations: list[dict[str, Any]] = []
            if reserved_work:
                state["last_progress"] = now()
            save_state(state)

        if not reserved_work:
            underfill = admission_reasons or list(dependency_blocks.values())[:120]
            if not underfill:
                underfill = ["dependency:no_additional_eligible_claim"]
            break

        # Slow task-root preparation and credential bootstrap happen outside
        # the scheduler lease. Each reservation is already durable.
        for role, item, reserved in reserved_work:
            try:
                if role == "producer":
                    record = materialize_claim(
                        specification, item, blueprint_raw, state, members,
                        attempt=int(reserved["attempt"]),
                    )
                elif role == "review":
                    record = materialize_review_claim(item, reserved, state)
                else:
                    record = reserved
                    record["status"] = "materialized"
                    state["repairs"][item["item_id"]]["status"] = "repair_launching"
                reservations.append(record)
            except Exception as exc:
                launch_failures.append(f"materialize:{item['item_id']}:{exc}")
                if role == "review":
                    reserved["status"] = "handoff_ready"
                    state["claims"][item["item_id"]] = reserved
                    state["reviews"][item["item_id"]] = {
                        "status": "review_launch_failed", "error": str(exc),
                        "updated_at": now(),
                    }
                elif role == "repair":
                    reserved["status"] = "repair_pending"
                    state["claims"][item["item_id"]] = reserved
                    state["repairs"][item["item_id"]]["status"] = "repair_pending"
                    state["repairs"][item["item_id"]]["error"] = str(exc)
                else:
                    reserved["status"] = "launch_failed"
                    reserved["launch_error"] = str(exc)
                    state["claims"][item["item_id"]] = reserved

        total_reserved += len(reservations)
        if not reservations:
            with FileLock(SCHEDULER_LOCK):
                save_state(state)
            underfill = launch_failures or ["startup:all_materializations_failed"]
            break
        launched, pump_reasons = generic_admission_pump(
            reservations,
            target=min(
                int(specification["default_limits"]["authenticated_live_goals"]),
                live_before + len(reservations),
            ),
            fanout=fanout,
            already_live=live_before,
            launch_one=launch_one,
            deadline=deadline,
        )
        total_authenticated += launched
        with FileLock(SCHEDULER_LOCK):
            state = load_state(specification_sha, create=False)
            for record in reservations:
                if record.get("status") == "launch_failed" and record.get("role") == "reviewer":
                    producer = record["producer_record"]
                    producer["status"] = "handoff_ready"
                    state["claims"][record["item_id"]] = producer
                    state["reviews"][record["item_id"]] = {
                        "status": "review_launch_failed",
                        "error": record.get("launch_error"), "updated_at": now(),
                    }
                elif record.get("status") == "launch_failed" and record.get("resume_thread_id"):
                    record["status"] = "repair_pending"
                    state["claims"][record["item_id"]] = record
                    state["repairs"][record["item_id"]]["status"] = "repair_pending"
                    state["repairs"][record["item_id"]]["error"] = record.get("launch_error")
                else:
                    state["claims"][record["item_id"]] = record
            state["external_launches_this_wave"] = len(reservations)
            if launched:
                state["last_progress"] = now()
            save_state(state)
        underfill = launch_failures + pump_reasons
        if pump_reasons:
            break

    if time.monotonic() >= deadline:
        underfill.append("tick_budget:startup_pump_deadline")
    with FileLock(SCHEDULER_LOCK):
        state = load_state(specification_sha, create=False)
        live_final = sum(
            record.get("status") == "live"
            for record in state["claims"].values()
        )
        if live_final < int(specification["default_limits"]["authenticated_live_goals"]):
            ready_after, dependency_after = readiness(rows, state)
            _, final_admission = host_admission(
                state, specification["default_limits"]
            )
            underfill.extend(final_admission)
            if not underfill:
                underfill.extend(
                    list(dependency_after.values())[:120]
                    or ["dependency:no_additional_eligible_claim"]
                )
        underfill.extend(integration_failures)
        state.pop("active_tick", None)
        refresh_projection(state, rows, sorted(set(underfill)))
    return {
        "valid": True, "harvested": harvested, "promoted": promoted, "retired": retired,
        "integrated": integrated,
        "reserved": total_reserved, "authenticated_this_tick": total_authenticated,
        "launch_failures": launch_failures, "underfill_reasons": sorted(set(underfill)),
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def read_crontab() -> str:
    completed = run(["/usr/bin/crontab", "-l"], check=False, timeout=10)
    if completed.returncode == 0:
        return completed.stdout
    if completed.returncode == 1 and "no crontab" in completed.stderr.lower():
        return ""
    raise ControllerError("cannot read current user crontab")


def install_cron() -> dict[str, Any]:
    require_canonical_root()
    if bootstrap_state() != "x":
        raise ControllerError("activation requires BOOT=x")
    authority = runtime_preflight()["authority"]
    specification, rows, _ = load_program()
    before = read_crontab()
    if CRON_BEGIN in before or CRON_END in before:
        raise ControllerError("theorem cron marker already exists")
    if "AWESOME_THEOREMS_STAGE5_CONJECTURES_EXECUTION_V1" in before:
        raise ControllerError("conjecture controller activation is not authorized")
    block = CRON_BEGIN + "\n" + CRON_COMMAND + "\n" + CRON_END + "\n"
    after = before + ("" if not before or before.endswith("\n") else "\n") + block
    completed = run(["/usr/bin/crontab", "-"], input_text=after, timeout=10)
    if completed.returncode != 0 or read_crontab() != after:
        raise ControllerError("crontab compare-and-set verification failed")
    try:
        PROGRAM_RUNTIME.mkdir(parents=True, exist_ok=True)
        SHARED_RUNTIME.mkdir(parents=True, exist_ok=True)
        receipt = sealed({
            "schema_version": "awesome-theorems/stage5-controller-activation/1.0",
            "program": PROGRAM,
            "activated_at": now(),
            "pre_crontab_sha256": digest(before.encode()),
            "post_crontab_sha256": digest(after.encode()),
            "cron_command_sha256": digest(CRON_COMMAND.encode()),
            "controller_sha256": file_digest(Path(__file__)),
            "execution_spec_sha256": digest(canonical(specification)),
            "shared_authority_sha256": SHARED_AUTHORITY_SHA256,
            "operator_authority_sha256": authority["authority_sha256"],
            "operator_goal": active_operator_goal(),
        })
        atomic_json(ACTIVATION_RECEIPT, receipt)
        append_event("controller_activated", {
            "activation_receipt_sha256": file_digest(ACTIVATION_RECEIPT),
            "cron_command_sha256": digest(CRON_COMMAND.encode()),
        })
        validate_activation_receipt()
        return receipt
    except Exception as exc:
        # Restore only when no third party changed the exact post-write bytes.
        # Otherwise fail closed without overwriting concurrent crontab edits.
        current = read_crontab()
        if current != after:
            raise ControllerError(
                f"activation failed and crontab changed concurrently; rollback refused: {exc}"
            ) from exc
        rollback = run(["/usr/bin/crontab", "-"], input_text=before, timeout=10)
        if read_crontab() != before or rollback.returncode != 0:
            raise ControllerError(
                f"activation failed and exact crontab rollback failed: {exc}"
            ) from exc
        if ACTIVATION_RECEIPT.exists() and not ACTIVATION_RECEIPT.is_symlink():
            ACTIVATION_RECEIPT.unlink()
        raise ControllerError(f"activation failed; original crontab restored: {exc}") from exc


def validate_activation_receipt() -> dict[str, Any]:
    receipt = verify_seal(
        strict_json(ACTIVATION_RECEIPT, "controller activation receipt"),
        "controller activation receipt",
    )
    specification, _, _ = load_program()
    current_cron = read_crontab()
    block = CRON_BEGIN + "\n" + CRON_COMMAND + "\n" + CRON_END + "\n"
    if (
        receipt.get("schema_version") != "awesome-theorems/stage5-controller-activation/1.0"
        or receipt.get("program") != PROGRAM
        or receipt.get("controller_sha256") != file_digest(Path(__file__))
        or receipt.get("execution_spec_sha256") != digest(canonical(specification))
        or receipt.get("cron_command_sha256") != digest(CRON_COMMAND.encode())
        or receipt.get("post_crontab_sha256") != digest(current_cron.encode())
        or current_cron.count(CRON_BEGIN) != 1
        or current_cron.count(CRON_END) != 1
        or block not in current_cron
        or receipt.get("operator_authority_sha256") != OPERATOR_AUTHORITY_SHA256
    ):
        raise ControllerError("controller activation receipt/current state differs")
    return receipt


def status() -> dict[str, Any]:
    specification, rows, _ = load_program()
    specification_sha = digest(canonical(specification))
    state = load_state(specification_sha, create=False)
    claims = list(state["claims"].values())
    authenticated = [
        record for record in claims
        if record.get("status") == "live" and authenticated_identity(record) is not None
    ]
    activated = False
    activation_error = None
    if ACTIVATION_RECEIPT.is_file() and not ACTIVATION_RECEIPT.is_symlink():
        try:
            validate_activation_receipt()
            activated = True
        except ControllerError as exc:
            activation_error = str(exc)
    return {
        "program": PROGRAM,
        "boot_state": {" ": "not_done", "_": "handoff_waiting_master", "x": "master_accepted"}[rows[0]["state"]],
        "activated": activated, "activation_error": activation_error,
        "logical_claims": sum(record.get("status") in ACTIVE_STATUSES for record in claims),
        "historical_claim_records": len(claims),
        "starting": sum(record.get("status") in STARTING_STATUSES for record in claims),
        "authenticated_live": len(authenticated),
        "handoff_ready": sum(record.get("status") == "handoff_ready" for record in claims),
        "launch_failed": sum(record.get("status") == "launch_failed" for record in claims),
        "underfill_reasons": state.get("underfill_reasons", []),
        "route": specification["route_policy"],
        "caps": specification["default_limits"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--validate-only", action="store_true")
    action.add_argument("--tick", action="store_true")
    action.add_argument("--activate", action="store_true")
    action.add_argument("--status", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        if arguments.validate_only:
            result = validate_only()
        elif arguments.tick:
            result = tick()
        elif arguments.activate:
            result = install_cron()
        else:
            result = status()
    except (ControllerError, OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result.get("valid", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
