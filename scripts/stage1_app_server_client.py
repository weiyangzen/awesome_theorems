#!/usr/bin/env python3
"""Run one fail-closed Stage1 worker through the Codex app-server JSONL API."""

from __future__ import annotations

import argparse
from collections import deque
import codecs
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import selectors
import signal
import stat
import subprocess
import sys
import time
from typing import Any, NoReturn


CLIENT_NAME = "awesome_theorems_stage1"
CLIENT_VERSION = "1.0.0"
DEFAULT_MODEL = "gpt-5.6-sol"
DEFAULT_EFFORT = "ultra"
DEFAULT_SERVICE_TIER = "default"
RUNTIME_MODEL = "gpt-5.6-sol"
RUNTIME_EFFORT = "ultra"
RUNTIME_SERVICE_TIER = "default"
IMPLEMENTATION_LANE = "implementation"
REVIEW_LANE = "review"
LANES = {IMPLEMENTATION_LANE, REVIEW_LANE}
REVIEW_BINDING_SCHEMA = "stage1-app-server-review-binding/1.0"
REVIEW_OUTPUT_SCHEMA = "stage1-master-review-output/1.0"
REVIEW_VERDICTS = {"phase_accepted", "repair_required", "rejected"}
WORKER_VERDICTS = {"accepted", "accepted_audit_only", "no_state_change", "blocked", "rejected"}
REVIEW_BINDING_FIELDS = {
    "schema_version",
    "claim_id",
    "item_id",
    "theorem_id",
    "phase",
    "base_revision",
    "blueprint_sha256",
    "theorem_dag_sha256",
    "prompt_sha256",
    "objective_sha256",
    "artifact_digests",
    "validator_recipe_sha256s",
    "output_schema",
}
REVIEW_OUTPUT_FIELDS = {
    "schema_version",
    "claim_id",
    "item_id",
    "theorem_id",
    "phase",
    "worker_verdict",
    "review_verdict",
    "audit_complete",
    "theorem_complete",
    "root_state",
    "first_failed_gate",
    "retry_condition",
    "status_boundary",
    "artifact_findings",
    "reviewed_artifact_sha256s",
    "validator_recipe_sha256s",
}
REVIEW_OUTPUT_JSON_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "additionalProperties": False,
    "required": sorted(REVIEW_OUTPUT_FIELDS),
    "properties": {
        "schema_version": {"const": REVIEW_OUTPUT_SCHEMA},
        "claim_id": {
            "type": "string",
            "pattern": r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,199}$",
        },
        "item_id": {"type": "string", "pattern": r"^S56-M-[0-9]{4}-[A-Z_]+$"},
        "theorem_id": {"type": "string", "pattern": r"^THM-M-[0-9]{4}$"},
        "phase": {
            "type": "string",
            "enum": [
                "intake",
                "statement",
                "anchor_audit",
                "obligation_tree",
                "proof",
                "validation",
                "release",
            ],
        },
        "worker_verdict": {"type": "string", "enum": sorted(WORKER_VERDICTS)},
        "review_verdict": {"type": "string", "enum": sorted(REVIEW_VERDICTS)},
        "audit_complete": {"type": "boolean"},
        "theorem_complete": {"type": "boolean"},
        "root_state": {"type": ["string", "null"]},
        "first_failed_gate": {"type": ["string", "null"]},
        "retry_condition": {"type": ["string", "null"]},
        "status_boundary": {"type": "string", "minLength": 1},
        "artifact_findings": {
            "type": "array",
            "items": {"type": "string", "minLength": 1},
        },
        "reviewed_artifact_sha256s": {
            "type": "object",
            "additionalProperties": {"type": "string", "pattern": r"^[0-9a-f]{64}$"},
        },
        "validator_recipe_sha256s": {
            "type": "array",
            "items": {"type": "string", "pattern": r"^[0-9a-f]{64}$"},
        },
    },
}
IMPLEMENTATION_SANDBOX = "workspace-write"
REVIEW_SANDBOX = "read-only"
APP_SERVER_FEATURE_ARGS = [
    "--enable",
    "goals",
    "--disable",
    "code_mode",
    "--disable",
    "code_mode_host",
    "--disable",
    "code_mode_only",
]
IMPLEMENTATION_SANDBOX_CONTRACT = {
    "type": "workspaceWrite",
    "writableRoots": [],
    "networkAccess": False,
    "excludeTmpdirEnvVar": False,
    "excludeSlashTmp": False,
}
REVIEW_SANDBOX_CONTRACT = {"type": "readOnly", "networkAccess": False}
# Compatibility names retained for the implementation scheduler.
RUNTIME_SANDBOX = IMPLEMENTATION_SANDBOX
RUNTIME_SANDBOX_CONTRACT = IMPLEMENTATION_SANDBOX_CONTRACT
ACTIVE_GOAL_STATUS = "active"
TERMINAL_GOAL_STATUSES = {
    "blocked",
    "usageLimited",
    "budgetLimited",
    "complete",
}
SUCCESSFUL_GOAL_STATUS = "complete"
TURN_TERMINAL_STATUSES = {"completed", "interrupted", "failed"}


class ProtocolError(RuntimeError):
    """Raised when app-server does not prove the requested worker contract."""


class WorkerInterrupted(ProtocolError):
    """Raised after an operator signal requests orderly worker shutdown."""


def fail(message: str) -> NoReturn:
    raise SystemExit(f"stage1_app_server_client: {message}")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


DIRECTORY_OPEN_FLAGS = (
    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
)


def open_parent_directory(
    path: Path, label: str, *, create: bool = False
) -> tuple[int, str]:
    """Open every parent component without ever following a symlink."""
    components = path.parts[1:] if path.is_absolute() else path.parts
    if (
        not components
        or components[-1] in {"", ".", ".."}
        or any(component in {"", ".", ".."} for component in components)
    ):
        raise ProtocolError(f"{label} path is not canonical or safe")
    try:
        descriptor = os.open("/" if path.is_absolute() else ".", DIRECTORY_OPEN_FLAGS)
    except OSError as exc:
        raise ProtocolError(f"{label} is missing or unsafe") from exc
    try:
        for component in components[:-1]:
            try:
                child_descriptor = os.open(
                    component, DIRECTORY_OPEN_FLAGS, dir_fd=descriptor
                )
            except FileNotFoundError:
                if not create:
                    raise
                try:
                    os.mkdir(component, 0o700, dir_fd=descriptor)
                except FileExistsError:
                    pass
                else:
                    os.fsync(descriptor)
                child_descriptor = os.open(
                    component, DIRECTORY_OPEN_FLAGS, dir_fd=descriptor
                )
            os.close(descriptor)
            descriptor = child_descriptor
        return descriptor, components[-1]
    except OSError as exc:
        os.close(descriptor)
        raise ProtocolError(f"{label} is missing or unsafe") from exc


def require_safe_status_destination(path: Path) -> None:
    parent_descriptor, target_name = open_parent_directory(
        path, "status destination", create=True
    )
    try:
        try:
            target_stat = os.stat(
                target_name, dir_fd=parent_descriptor, follow_symlinks=False
            )
        except FileNotFoundError:
            return
        if not stat.S_ISREG(target_stat.st_mode):
            raise ProtocolError("status destination is not a regular file")
    finally:
        os.close(parent_descriptor)


def atomic_write(path: Path, text: str) -> None:
    """Replace one status file durably, including its directory entry."""
    parent_descriptor, target_name = open_parent_directory(
        path, "status destination", create=True
    )
    temporary_name: str | None = None
    try:
        try:
            target_stat = os.stat(target_name, dir_fd=parent_descriptor, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            if not stat.S_ISREG(target_stat.st_mode):
                raise ProtocolError("status destination is not a regular file")
        for _ in range(128):
            temporary_name = f".{path.name}.{os.getpid()}.{os.urandom(8).hex()}.tmp"
            try:
                descriptor = os.open(
                    temporary_name,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                    0o600,
                    dir_fd=parent_descriptor,
                )
                break
            except FileExistsError:
                temporary_name = None
        else:
            raise ProtocolError("could not allocate a unique status temporary file")
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(
                temporary_name,
                target_name,
                src_dir_fd=parent_descriptor,
                dst_dir_fd=parent_descriptor,
            )
            temporary_name = None
            os.fsync(parent_descriptor)
        finally:
            if temporary_name is not None:
                try:
                    os.unlink(temporary_name, dir_fd=parent_descriptor)
                except FileNotFoundError:
                    pass
    finally:
        os.close(parent_descriptor)


def status_write(path: Path, state: dict[str, Any]) -> None:
    atomic_write(path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")


def read_regular_text(path: Path, label: str) -> str:
    parent_descriptor, name = open_parent_directory(path, label)
    try:
        descriptor = os.open(
            name,
            os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0),
            dir_fd=parent_descriptor,
        )
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode):
            os.close(descriptor)
            raise ProtocolError(f"{label} is missing or unsafe")
        with os.fdopen(descriptor, "r", encoding="utf-8") as handle:
            return handle.read()
    except (OSError, UnicodeDecodeError) as exc:
        raise ProtocolError(f"{label} is missing or unsafe") from exc
    finally:
        os.close(parent_descriptor)


def object_without_duplicate_names(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, member in pairs:
        if key in value:
            raise ProtocolError(f"JSON object contains duplicate JSON name {key!r}")
        value[key] = member
    return value


def canonical_artifact_path(value: Any) -> str | None:
    if not isinstance(value, str) or not value or "\\" in value or "\0" in value:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        return None
    if not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        return None
    return path.as_posix()


def require_review_binding(
    path: Path | None, prompt_sha256: str, objective_sha256: str
) -> tuple[dict[str, Any], str]:
    if path is None:
        raise ProtocolError("review lane requires --binding")
    binding_text = read_regular_text(path, "review binding")
    try:
        binding = json.loads(binding_text, object_pairs_hook=object_without_duplicate_names)
    except json.JSONDecodeError as exc:
        raise ProtocolError("review binding is not valid JSON") from exc
    if not isinstance(binding, dict) or set(binding) != REVIEW_BINDING_FIELDS:
        raise ProtocolError("review binding fields are not canonical")
    if (
        binding.get("schema_version") != REVIEW_BINDING_SCHEMA
        or binding.get("output_schema") != REVIEW_OUTPUT_SCHEMA
        or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,199}", str(binding.get("claim_id", "")))
        is None
        or re.fullmatch(r"S56-M-[0-9]{4}-[A-Z_]+", str(binding.get("item_id", ""))) is None
        or re.fullmatch(r"THM-M-[0-9]{4}", str(binding.get("theorem_id", ""))) is None
        or binding["item_id"][6:10] != binding["theorem_id"][6:10]
        or binding.get("phase")
        not in {"intake", "statement", "anchor_audit", "obligation_tree", "proof", "validation", "release"}
        or re.fullmatch(r"[0-9a-f]{40}", str(binding.get("base_revision", ""))) is None
        or not is_sha256(binding.get("blueprint_sha256"))
        or not is_sha256(binding.get("theorem_dag_sha256"))
        or binding.get("prompt_sha256") != prompt_sha256
        or binding.get("objective_sha256") != objective_sha256
    ):
        raise ProtocolError("review binding identity or input digest mismatch")
    artifact_digests = binding.get("artifact_digests")
    recipe_digests = binding.get("validator_recipe_sha256s")
    artifact_paths = (
        [canonical_artifact_path(relative) for relative in artifact_digests]
        if isinstance(artifact_digests, dict)
        else []
    )
    if (
        not isinstance(artifact_digests, dict)
        or not artifact_digests
        or any(relative is None for relative in artifact_paths)
        or len(set(artifact_paths)) != len(artifact_paths)
        or any(
            not is_sha256(digest)
            for relative, digest in artifact_digests.items()
        )
        or not isinstance(recipe_digests, list)
        or not recipe_digests
        or len(set(recipe_digests)) != len(recipe_digests)
        or any(not is_sha256(digest) for digest in recipe_digests)
    ):
        raise ProtocolError("review binding artifact or validator digests are malformed")
    digest = sha256_text(canonical_json(binding))
    return binding, digest


def require_review_output(value: Any, binding: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != REVIEW_OUTPUT_FIELDS:
        raise ProtocolError("review output fields are not canonical")
    if (
        value.get("schema_version") != REVIEW_OUTPUT_SCHEMA
        or value.get("claim_id") != binding["claim_id"]
        or value.get("item_id") != binding["item_id"]
        or value.get("theorem_id") != binding["theorem_id"]
        or value.get("phase") != binding["phase"]
        or value.get("worker_verdict") not in WORKER_VERDICTS
        or value.get("review_verdict") not in REVIEW_VERDICTS
        or not isinstance(value.get("audit_complete"), bool)
        or not isinstance(value.get("theorem_complete"), bool)
        or not isinstance(value.get("status_boundary"), str)
        or not value["status_boundary"]
        or value.get("root_state") is not None
        and not isinstance(value.get("root_state"), str)
        or value.get("first_failed_gate") is not None
        and not isinstance(value.get("first_failed_gate"), str)
        or value.get("retry_condition") is not None
        and not isinstance(value.get("retry_condition"), str)
    ):
        raise ProtocolError("review output identity, verdict, or status fields are malformed")
    findings = value.get("artifact_findings")
    if (
        not isinstance(findings, list)
        or any(not isinstance(row, str) or not row for row in findings)
        or value.get("reviewed_artifact_sha256s") != binding["artifact_digests"]
        or value.get("validator_recipe_sha256s") != binding["validator_recipe_sha256s"]
        or value["theorem_complete"]
        and not value["audit_complete"]
        or binding["phase"] != "release"
        and (value["audit_complete"] or value["theorem_complete"])
        or binding["phase"] == "release"
        and value["review_verdict"] == "phase_accepted"
        and not value["audit_complete"]
        or value["worker_verdict"] == "accepted_audit_only"
        and (binding["phase"] != "release" or not value["audit_complete"] or value["theorem_complete"])
        or value["review_verdict"] == "phase_accepted"
        and value["first_failed_gate"] is not None
        or value["review_verdict"] != "phase_accepted"
        and value["first_failed_gate"] is None
    ):
        raise ProtocolError("review output findings or content bindings are malformed")
    return value


def require_full_review_history(
    result: dict[str, Any], turn_ids: list[str], prompt: str, binding: dict[str, Any]
) -> tuple[list[dict[str, Any]], dict[str, Any], str]:
    turns = result.get("data")
    if (
        not isinstance(turns, list)
        or "nextCursor" not in result
        or result["nextCursor"] is not None
        or "backwardsCursor" not in result
        or result["backwardsCursor"] is not None
    ):
        raise ProtocolError("thread/turns/list did not return one complete turn page")
    if len(turns) != len(turn_ids):
        raise ProtocolError("full review turn history has missing or extra turns")
    expected_input = [{"type": "text", "text": prompt}]
    allowed_item_types = {"userMessage", "agentMessage"}
    final_messages: list[tuple[int, dict[str, Any]]] = []
    for index, (turn, turn_id) in enumerate(zip(turns, turn_ids)):
        if (
            not isinstance(turn, dict)
            or turn.get("id") != turn_id
            or turn.get("status") != "completed"
            or turn.get("itemsView") != "full"
            or not isinstance(turn.get("items"), list)
        ):
            raise ProtocolError("full review turn history identity or status mismatch")
        items = turn["items"]
        if any(not isinstance(item, dict) or not isinstance(item.get("type"), str) for item in items):
            raise ProtocolError("full review turn history contains a malformed item")
        if any(item["type"] not in allowed_item_types for item in items):
            raise ProtocolError("read-only review history contains a non-read-only item")
        user_messages = [item for item in items if item["type"] == "userMessage"]
        if index == 0:
            if len(user_messages) != 1 or user_messages[0].get("content") != expected_input:
                raise ProtocolError("full review history does not bind the exact turn input")
        elif user_messages:
            raise ProtocolError("server-created review continuation contains unexpected user input")
        final_messages.extend(
            (index, item)
            for item in items
            if item["type"] == "agentMessage" and item.get("phase") == "final_answer"
        )
        if any(item["type"] == "agentMessage" and item.get("phase") != "final_answer" for item in items):
            raise ProtocolError("review history contains a commentary or unphased agentMessage")
    if (
        len(final_messages) != 1
        or final_messages[0][0] != len(turns) - 1
        or not isinstance(final_messages[0][1].get("text"), str)
    ):
        raise ProtocolError("review must emit exactly one final_answer in the last turn")
    output_text = final_messages[0][1]["text"]
    try:
        parsed = json.loads(output_text, object_pairs_hook=object_without_duplicate_names)
    except json.JSONDecodeError as exc:
        raise ProtocolError("final review agentMessage is not JSON") from exc
    output = require_review_output(parsed, binding)
    return turns, output, output_text


def process_start_ticks(pid: int) -> int:
    """Bind status to this exact Linux process instance, not just a PID."""
    try:
        fields = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8").split()
        return int(fields[21])
    except (OSError, ValueError, IndexError) as exc:
        raise ProtocolError(f"cannot bind app-server process identity for pid {pid}") from exc


def require_exact_runtime_args(args: argparse.Namespace) -> None:
    actual = (args.model, args.effort, args.service_tier)
    expected = (RUNTIME_MODEL, RUNTIME_EFFORT, RUNTIME_SERVICE_TIER)
    if actual != expected:
        raise ProtocolError(
            "runtime fallback is forbidden: expected "
            f"model={expected[0]} effort={expected[1]} service_tier={expected[2]}, "
            f"got model={actual[0]} effort={actual[1]} service_tier={actual[2]}"
        )
    if args.lane not in LANES:
        raise ProtocolError(f"unsupported app-server lane {args.lane!r}")
    if args.lane == IMPLEMENTATION_LANE and args.binding is not None:
        raise ProtocolError("implementation lane must not receive a review binding")


def lane_sandbox(lane: str) -> tuple[str, dict[str, Any]]:
    if lane == IMPLEMENTATION_LANE:
        return IMPLEMENTATION_SANDBOX, IMPLEMENTATION_SANDBOX_CONTRACT
    if lane == REVIEW_LANE:
        return REVIEW_SANDBOX, REVIEW_SANDBOX_CONTRACT
    raise ProtocolError(f"unsupported app-server lane {lane!r}")


class AppServerConnection:
    """One JSONL app-server connection with request/notification demultiplexing."""

    def __init__(self, command: list[str], log_path: Path, timeout: float) -> None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        self.log = log_path.open("a", encoding="utf-8")
        try:
            self.process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=self.log,
                text=True,
                bufsize=1,
                start_new_session=True,
            )
        except BaseException:
            self.log.close()
            raise
        if self.process.stdin is None or self.process.stdout is None:
            self.close()
            raise ProtocolError("app-server pipes were not created")
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.process.stdout, selectors.EVENT_READ)
        self.timeout = timeout
        self.next_id = 1
        self.notifications: deque[dict[str, Any]] = deque()
        self.deferred_notifications: deque[dict[str, Any]] = deque()
        self.pending_responses: dict[str, dict[str, Any]] = {}
        self.stdout_buffer = ""
        self.stdout_decoder = codecs.getincrementaldecoder("utf-8")()
        self.interrupted_signal: int | None = None
        self.closed = False

    @staticmethod
    def _id_key(value: Any) -> str:
        return json.dumps(value, sort_keys=True, separators=(",", ":"))

    def interrupt(self, signum: int) -> None:
        if self.interrupted_signal is None:
            self.interrupted_signal = signum
        self._signal_group(signum)

    def _signal_group(self, signum: int) -> None:
        try:
            os.killpg(self.process.pid, signum)
        except ProcessLookupError:
            pass

    def _group_exists(self) -> bool:
        try:
            os.killpg(self.process.pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        return True

    def close(self) -> None:
        if self.closed:
            return
        self.closed = True
        try:
            if self.process.stdin is not None:
                try:
                    self.process.stdin.close()
                except OSError:
                    pass
            self._signal_group(signal.SIGTERM)
            child_wait_expired = False
            if self.process.poll() is None:
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self._signal_group(signal.SIGKILL)
                    self.process.wait(timeout=5)
            if self._group_exists():
                deadline = time.monotonic() + 5
                while self._group_exists() and time.monotonic() < deadline:
                    time.sleep(0.01)
                child_wait_expired = self._group_exists()
            if child_wait_expired:
                raise ProtocolError("app-server process group did not terminate cleanly")
        finally:
            self.selector.close()
            if self.process.stdout is not None:
                self.process.stdout.close()
            self.log.close()

    def send(self, message: dict[str, Any]) -> None:
        if self.interrupted_signal is not None:
            raise WorkerInterrupted(f"received signal {self.interrupted_signal}")
        if self.process.poll() is not None:
            raise ProtocolError(f"app-server exited before send (exit={self.process.returncode})")
        assert self.process.stdin is not None
        try:
            self.process.stdin.write(
                json.dumps(message, ensure_ascii=False, separators=(",", ":")) + "\n"
            )
            self.process.stdin.flush()
        except (BrokenPipeError, OSError) as exc:
            raise ProtocolError("app-server closed its input stream") from exc

    def respond(self, request_id: Any, result: dict[str, Any]) -> None:
        self.send({"id": request_id, "result": result})

    def respond_error(self, request_id: Any, code: int, message: str) -> None:
        self.send({"id": request_id, "error": {"code": code, "message": message}})

    def request(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        request_id = self.next_id
        self.next_id += 1
        self.send({"id": request_id, "method": method, "params": params})
        key = self._id_key(request_id)
        deadline = time.monotonic() + self.timeout
        while True:
            cached = self.pending_responses.pop(key, None)
            if cached is not None:
                return self._response_result(method, cached)
            message = self.read_message(deadline)
            if "id" in message and "method" in message:
                self.handle_server_request(message)
                continue
            if "id" in message:
                response_key = self._id_key(message["id"])
                if response_key == key:
                    return self._response_result(method, message)
                self.pending_responses[response_key] = message
                continue
            if "method" in message:
                self.require_no_model_reroute(message)
                self.notifications.append(message)
                continue
            raise ProtocolError("app-server emitted a malformed JSON-RPC message")

    @staticmethod
    def _response_result(method: str, message: dict[str, Any]) -> dict[str, Any]:
        if "error" in message:
            raise ProtocolError(f"{method} failed: {message['error']}")
        result = message.get("result")
        if not isinstance(result, dict):
            raise ProtocolError(f"{method} returned a malformed result")
        return result

    def read_message(self, deadline: float) -> dict[str, Any]:
        assert self.process.stdout is not None
        while "\n" not in self.stdout_buffer:
            if self.interrupted_signal is not None:
                raise WorkerInterrupted(f"received signal {self.interrupted_signal}")
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ProtocolError("timed out waiting for app-server")
            events = self.selector.select(remaining)
            if self.interrupted_signal is not None:
                raise WorkerInterrupted(f"received signal {self.interrupted_signal}")
            if not events:
                raise ProtocolError("timed out waiting for app-server")
            try:
                chunk = os.read(self.process.stdout.fileno(), 65_536)
            except OSError as exc:
                raise ProtocolError("failed to read app-server output") from exc
            if not chunk:
                return_code = self.process.poll()
                raise ProtocolError(f"app-server closed its stream (exit={return_code})")
            try:
                self.stdout_buffer += self.stdout_decoder.decode(chunk)
            except UnicodeDecodeError as exc:
                raise ProtocolError("app-server emitted invalid UTF-8") from exc
        line, self.stdout_buffer = self.stdout_buffer.split("\n", 1)
        try:
            message = json.loads(line, object_pairs_hook=object_without_duplicate_names)
        except json.JSONDecodeError as exc:
            raise ProtocolError("app-server emitted non-JSON output") from exc
        if not isinstance(message, dict):
            raise ProtocolError("app-server emitted a non-object message")
        return message

    def handle_server_request(self, message: dict[str, Any]) -> None:
        """Resolve requests that can occur despite approvalPolicy=never."""
        request_id = message.get("id")
        method = message.get("method")
        params = message.get("params")
        if request_id is None or not isinstance(method, str) or not isinstance(params, dict):
            raise ProtocolError("app-server emitted a malformed server request")
        if method in {
            "item/commandExecution/requestApproval",
            "item/fileChange/requestApproval",
        }:
            self.respond(request_id, {"decision": "cancel"})
        elif method in {"applyPatchApproval", "execCommandApproval"}:
            self.respond(request_id, {"decision": "abort"})
        elif method == "item/tool/requestUserInput":
            questions = params.get("questions")
            if not isinstance(questions, list):
                raise ProtocolError("requestUserInput server request has malformed questions")
            answers = {
                question["id"]: {"answers": []}
                for question in questions
                if isinstance(question, dict) and isinstance(question.get("id"), str)
            }
            if len(answers) != len(questions):
                raise ProtocolError("requestUserInput server request has malformed question ids")
            self.respond(request_id, {"answers": answers})
        elif method == "mcpServer/elicitation/request":
            self.respond(request_id, {"action": "cancel", "content": None})
        elif method == "item/permissions/requestApproval":
            # Grant no additional permissions. This is the schema-valid,
            # fail-closed response for a noninteractive execution worker.
            self.respond(request_id, {"permissions": {}, "scope": "turn"})
        elif method == "item/tool/call":
            self.respond(request_id, {"success": False, "contentItems": []})
        elif method == "currentTime/read":
            self.respond(request_id, {"currentTimeAt": int(time.time())})
        else:
            self.respond_error(request_id, -32601, f"unsupported server request: {method}")
            raise ProtocolError(f"unsupported app-server request {method!r}")

    def next_notification(self, deadline: float) -> dict[str, Any]:
        while True:
            if self.notifications:
                message = self.notifications.popleft()
                self.require_no_model_reroute(message)
                return message
            message = self.read_message(deadline)
            if "id" in message and "method" in message:
                self.handle_server_request(message)
                continue
            if "id" in message:
                self.pending_responses[self._id_key(message["id"])] = message
                continue
            if "method" in message:
                self.require_no_model_reroute(message)
                return message
            raise ProtocolError("app-server emitted a malformed JSON-RPC message")

    @staticmethod
    def require_no_model_reroute(message: dict[str, Any]) -> None:
        if message.get("method") != "model/rerouted":
            return
        params = message.get("params")
        if not isinstance(params, dict):
            raise ProtocolError("model/rerouted returned malformed params")
        raise ProtocolError(
            "model reroute is forbidden: "
            f"expected {RUNTIME_MODEL!r}, got from={params.get('fromModel')!r} "
            f"to={params.get('toModel')!r}"
        )

    @staticmethod
    def _notification_turn(
        message: dict[str, Any], method: str, thread_id: str
    ) -> dict[str, Any] | None:
        if message.get("method") != method:
            return None
        params = message.get("params")
        if not isinstance(params, dict) or params.get("threadId") != thread_id:
            return None
        turn = params.get("turn")
        if not isinstance(turn, dict) or not isinstance(turn.get("id"), str):
            raise ProtocolError(f"{method} returned a malformed turn")
        return turn

    def wait_for_notification_turn(
        self, method: str, thread_id: str, turn_id: str | None = None
    ) -> dict[str, Any]:
        """Find a turn event while retaining every unrelated notification."""
        deadline = time.monotonic() + self.timeout
        retained: deque[dict[str, Any]] = deque()
        matched: dict[str, Any] | None = None
        while self.deferred_notifications:
            message = self.deferred_notifications.popleft()
            turn = self._notification_turn(message, method, thread_id)
            if matched is None and turn is not None and (
                turn_id is None or turn.get("id") == turn_id
            ):
                matched = turn
            else:
                retained.append(message)
        self.deferred_notifications = retained
        if matched is not None:
            return matched

        while True:
            message = self.next_notification(deadline)
            turn = self._notification_turn(message, method, thread_id)
            if turn is not None and (turn_id is None or turn.get("id") == turn_id):
                return turn
            self.deferred_notifications.append(message)

    def wait_for_turn_started(self, thread_id: str) -> str:
        """Return the server event ID; a turn/start response ID is not authoritative."""
        return self.wait_for_notification_turn("turn/started", thread_id)["id"]

    def wait_for_turn(self, thread_id: str, turn_id: str) -> dict[str, Any]:
        turn = self.wait_for_notification_turn("turn/completed", thread_id, turn_id)
        status = turn.get("status")
        if status not in TURN_TERMINAL_STATUSES:
            raise ProtocolError(f"turn/completed carried nonterminal status {status!r}")
        return turn

    def wait_for_goal_continuation(self, thread_id: str) -> str:
        """Return the next server-created turn id for this active goal."""
        return self.wait_for_turn_started(thread_id)


def model_contract(
    models: list[dict[str, Any]], model: str, effort: str, service_tier: str
) -> dict[str, Any]:
    matches = [
        entry
        for entry in models
        if isinstance(entry, dict) and (entry.get("model") == model or entry.get("id") == model)
    ]
    if len(matches) != 1:
        raise ProtocolError(
            f"requested model {model!r} must have exactly one model/list entry; found {len(matches)}"
        )
    row = matches[0]
    if row.get("model") != model or row.get("id") != model:
        raise ProtocolError(f"model/list entry would alias or reroute requested model {model!r}")
    efforts = {
        option.get("reasoningEffort")
        for option in row.get("supportedReasoningEfforts", [])
        if isinstance(option, dict)
    }
    if effort not in efforts:
        raise ProtocolError(f"model {model!r} does not advertise reasoning effort {effort!r}")
    if service_tier != RUNTIME_SERVICE_TIER:
        raise ProtocolError(
            f"model {model!r} requested unsupported service tier {service_tier!r}"
        )
    # The app-server catalog exposes the baseline `default` tier implicitly.
    # Rows such as priority/Fast describe optional acceleration, not a reason to
    # reroute a default request. An explicit default row must not contradict the
    # baseline identity if a future catalog starts emitting one.
    tier_rows = row.get("serviceTiers", [])
    if not isinstance(tier_rows, list) or any(not isinstance(option, dict) for option in tier_rows):
        raise ProtocolError(f"model {model!r} returned malformed service tier metadata")
    explicit_defaults = [option for option in tier_rows if option.get("id") == service_tier]
    if len(explicit_defaults) > 1:
        raise ProtocolError(
            f"model {model!r} advertises service tier {service_tier!r} more than once"
        )
    if explicit_defaults and explicit_defaults[0].get("name") not in {None, "Default"}:
        raise ProtocolError("service tier 'default' has a contradictory catalog label")
    return row


def load_model_catalog(connection: AppServerConnection) -> list[dict[str, Any]]:
    """Load the complete catalog while rejecting ambiguous pages or identities."""
    models: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_models: set[str] = set()
    seen_cursors: set[str] = set()
    cursor: str | None = None
    while True:
        params: dict[str, Any] = {"includeHidden": True, "limit": 100}
        if cursor is not None:
            params["cursor"] = cursor
        page = connection.request("model/list", params)
        rows = page.get("data")
        if not isinstance(rows, list) or "nextCursor" not in page:
            raise ProtocolError("model/list returned a malformed catalog page")
        for row in rows:
            if not isinstance(row, dict):
                raise ProtocolError("model/list returned a malformed catalog model")
            row_id = row.get("id")
            row_model = row.get("model")
            if not isinstance(row_id, str) or not row_id:
                raise ProtocolError("model/list returned a malformed catalog model id")
            if not isinstance(row_model, str) or not row_model:
                raise ProtocolError("model/list returned a malformed catalog model name")
            if row_id in seen_ids or row_model in seen_models:
                raise ProtocolError(
                    "model/list returned a duplicate model identity: "
                    f"id={row_id!r} model={row_model!r}"
                )
            seen_ids.add(row_id)
            seen_models.add(row_model)
            models.append(row)
        next_cursor = page["nextCursor"]
        if next_cursor is None:
            return models
        if not isinstance(next_cursor, str) or not next_cursor:
            raise ProtocolError("model/list returned a malformed nextCursor")
        if next_cursor in seen_cursors:
            raise ProtocolError(f"model/list returned a cursor cycle at {next_cursor!r}")
        seen_cursors.add(next_cursor)
        cursor = next_cursor


def require_runtime_contract(
    result: dict[str, Any],
    workspace: Path,
    model: str,
    effort: str,
    service_tier: str,
    lane: str = IMPLEMENTATION_LANE,
    expected_thread_id: str | None = None,
) -> str:
    thread = result.get("thread")
    if not isinstance(thread, dict) or not isinstance(thread.get("id"), str):
        raise ProtocolError("thread start/resume did not return a thread id")
    actual = {
        "cwd": result.get("cwd"),
        "model": result.get("model"),
        "reasoningEffort": result.get("reasoningEffort"),
        "serviceTier": result.get("serviceTier"),
        "approvalPolicy": result.get("approvalPolicy"),
        "approvalsReviewer": result.get("approvalsReviewer"),
        "sandbox": result.get("sandbox"),
        "runtimeWorkspaceRoots": result.get("runtimeWorkspaceRoots"),
    }
    _, sandbox_contract = lane_sandbox(lane)
    expected = {
        "cwd": str(workspace),
        "model": model,
        "reasoningEffort": effort,
        "serviceTier": service_tier,
        "approvalPolicy": "never",
        "approvalsReviewer": "user",
        "sandbox": sandbox_contract,
        "runtimeWorkspaceRoots": []
        if lane == REVIEW_LANE
        else [str(workspace)],
    }
    if actual != expected:
        raise ProtocolError(f"thread runtime contract mismatch: expected {expected}, got {actual}")
    if expected_thread_id is not None and thread["id"] != expected_thread_id:
        raise ProtocolError(
            "thread/resume returned the wrong thread: "
            f"expected {expected_thread_id!r}, got {thread['id']!r}"
        )
    return thread["id"]


def thread_runtime_params(
    workspace: Path,
    model: str,
    effort: str,
    service_tier: str,
    lane: str,
) -> dict[str, Any]:
    sandbox_mode, _ = lane_sandbox(lane)
    return {
        "model": model,
        "cwd": str(workspace),
        "approvalPolicy": "never",
        "approvalsReviewer": "user",
        "sandbox": sandbox_mode,
        "runtimeWorkspaceRoots": [] if lane == REVIEW_LANE else [str(workspace)],
        "serviceTier": service_tier,
        "config": {
            "model_reasoning_effort": effort,
            "service_tier": service_tier,
            "features": {
                "goals": True,
                "code_mode": False,
                "code_mode_host": False,
                "code_mode_only": False,
            },
        },
    }


def require_goal(value: Any, thread_id: str, objective: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ProtocolError("app-server returned a malformed goal")
    if value.get("threadId") != thread_id or value.get("objective") != objective:
        raise ProtocolError("app-server goal identity changed")
    status = value.get("status")
    if status != ACTIVE_GOAL_STATUS and status not in TERMINAL_GOAL_STATUSES:
        raise ProtocolError(f"app-server returned unsupported goal status {status!r}")
    return value


def same_goal_identity(left: dict[str, Any], right: dict[str, Any]) -> bool:
    """Goal reads may legitimately update counters/timestamps between requests."""
    return all(left.get(field) == right.get(field) for field in ("threadId", "objective", "status"))


def turn_params(
    thread_id: str,
    text: str,
    workspace: Path,
    model: str,
    effort: str,
    service_tier: str,
    lane: str = IMPLEMENTATION_LANE,
) -> dict[str, Any]:
    _, sandbox_contract = lane_sandbox(lane)
    if lane == IMPLEMENTATION_LANE:
        turn_sandbox = dict(sandbox_contract)
        turn_sandbox["writableRoots"] = [str(workspace)]
    else:
        turn_sandbox = dict(sandbox_contract)
    params = {
        "threadId": thread_id,
        "input": [{"type": "text", "text": text}],
        "cwd": str(workspace),
        "model": model,
        "effort": effort,
        "serviceTier": service_tier,
        "approvalPolicy": "never",
        "approvalsReviewer": "user",
        "sandboxPolicy": turn_sandbox,
    }
    if lane == REVIEW_LANE:
        params["outputSchema"] = REVIEW_OUTPUT_JSON_SCHEMA
    return params


def install_signal_handlers(connection: AppServerConnection) -> dict[int, Any]:
    previous: dict[int, Any] = {}

    def handler(signum: int, _frame: Any) -> None:
        connection.interrupt(signum)

    for signum in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        previous[signum] = signal.signal(signum, handler)
    return previous


def restore_signal_handlers(previous: dict[int, Any]) -> None:
    for signum, handler in previous.items():
        signal.signal(signum, handler)


def run_worker(args: argparse.Namespace) -> int:
    require_exact_runtime_args(args)
    workspace = args.workspace.resolve()
    if not workspace.is_dir():
        raise ProtocolError(f"worker workspace is not a directory: {workspace}")
    prompt = read_regular_text(args.prompt, "worker prompt")
    objective = read_regular_text(args.objective, "goal objective").strip()
    if not prompt.strip() or not objective:
        raise ProtocolError("worker prompt and goal objective must be nonempty")
    status_path = args.status
    require_safe_status_destination(status_path)
    log_path = args.log.resolve()
    prompt_sha256 = sha256_text(prompt)
    objective_sha256 = sha256_text(objective)
    binding: dict[str, Any] | None = None
    binding_sha256: str | None = None
    if args.lane == REVIEW_LANE:
        binding, binding_sha256 = require_review_binding(
            args.binding, prompt_sha256, objective_sha256
        )
    sandbox_mode, sandbox_contract = lane_sandbox(args.lane)
    app_server_argv = ["app-server", "--stdio", *APP_SERVER_FEATURE_ARGS]
    command = [args.codex, *app_server_argv]
    connection = AppServerConnection(command, log_path, args.timeout)
    previous_handlers = install_signal_handlers(connection)
    state: dict[str, Any] = {
        "protocol": "codex-app-server-jsonl",
        "client_pid": os.getpid(),
        "client_start_ticks": process_start_ticks(os.getpid()),
        "app_server_pid": connection.process.pid,
        "app_server_start_ticks": process_start_ticks(connection.process.pid),
        "model": args.model,
        "reasoning_effort": args.effort,
        "service_tier": args.service_tier,
        "lane": args.lane,
        "workspace": str(workspace),
        "prompt_sha256": prompt_sha256,
        "objective_sha256": objective_sha256,
        "turn_input_sha256": sha256_text(
            canonical_json([{"type": "text", "text": prompt}])
        ),
        "binding": binding,
        "binding_sha256": binding_sha256,
        "resumed": args.thread_id is not None,
        "state": "starting",
        "continuation_count": 0,
    }
    status_write(status_path, state)
    try:
        connection.request(
            "initialize",
            {
                "clientInfo": {
                    "name": CLIENT_NAME,
                    "title": "Awesome Theorems Stage1 Executor",
                    "version": CLIENT_VERSION,
                },
                "capabilities": {"experimentalApi": True},
            },
        )
        connection.send({"method": "initialized", "params": {}})
        models = load_model_catalog(connection)
        advertised = model_contract(models, args.model, args.effort, args.service_tier)
        state["model_catalog_entry_sha256"] = sha256_text(canonical_json(advertised))
        runtime_params = thread_runtime_params(
            workspace,
            args.model,
            args.effort,
            args.service_tier,
            args.lane,
        )
        if args.thread_id is None:
            start_method = "thread/start"
            start_params = {
                **runtime_params,
                "allowProviderModelFallback": False,
                "serviceName": CLIENT_NAME,
            }
        else:
            # The generated ThreadResumeParams schema has no fallback flag.
            # Reasserting the exact model plus checking the response and every
            # model/rerouted notification is the protocol's fail-closed path.
            start_method = "thread/resume"
            start_params = {
                **runtime_params,
                "threadId": args.thread_id,
                "excludeTurns": True,
            }
        start = connection.request(start_method, start_params)
        thread_id = require_runtime_contract(
            start,
            workspace,
            args.model,
            args.effort,
            args.service_tier,
            args.lane,
            args.thread_id,
        )
        if args.thread_id is None:
            set_result = connection.request(
                "thread/goal/set",
                {
                    "threadId": thread_id,
                    "objective": objective,
                    "status": ACTIVE_GOAL_STATUS,
                },
            )
            goal = require_goal(set_result.get("goal"), thread_id, objective)
            if goal.get("status") != ACTIVE_GOAL_STATUS:
                raise ProtocolError("thread/goal/set did not create the exact active goal")
            get_result = connection.request("thread/goal/get", {"threadId": thread_id})
            confirmed = require_goal(get_result.get("goal"), thread_id, objective)
            if not same_goal_identity(confirmed, goal):
                raise ProtocolError("thread/goal/get did not confirm the newly persisted goal")
        else:
            get_result = connection.request("thread/goal/get", {"threadId": thread_id})
            confirmed = require_goal(get_result.get("goal"), thread_id, objective)
            if confirmed.get("status") != ACTIVE_GOAL_STATUS:
                raise ProtocolError("thread/resume did not recover the exact active goal")
        state.update(
            {
                "state": "live",
                "thread_id": thread_id,
                "goal": confirmed,
                "model_catalog_entry": advertised,
                "runtime_contract": {
                    "model": start.get("model"),
                    "reasoning_effort": start.get("reasoningEffort"),
                    "service_tier": start.get("serviceTier"),
                    "cwd": start.get("cwd"),
                    "sandbox": start.get("sandbox"),
                    "network_access": start.get("sandbox", {}).get("networkAccess")
                    if isinstance(start.get("sandbox"), dict)
                    else None,
                    "app_server_argv": app_server_argv,
                },
            }
        )
        if state["runtime_contract"]["sandbox"] != sandbox_contract:
            raise ProtocolError("persisted lane sandbox contract mismatch")
        status_write(status_path, state)

        turn_result = connection.request(
            "turn/start",
            turn_params(
                thread_id,
                prompt,
                workspace,
                args.model,
                args.effort,
                args.service_tier,
                args.lane,
            ),
        )
        turn = turn_result.get("turn")
        if not isinstance(turn, dict):
            raise ProtocolError("turn/start did not acknowledge the turn")
        response_turn_id = turn.get("id")
        if response_turn_id is not None and not isinstance(response_turn_id, str):
            raise ProtocolError("turn/start returned a malformed response turn id")
        turn_id = connection.wait_for_turn_started(thread_id)
        state["turn_start_response_id"] = response_turn_id
        turn_ids: list[str] = []
        while True:
            turn_ids.append(turn_id)
            state["turn_id"] = turn_id
            state["turn_ids"] = turn_ids
            status_write(status_path, state)
            completed = connection.wait_for_turn(thread_id, turn_id)
            goal_result = connection.request("thread/goal/get", {"threadId": thread_id})
            goal_after = require_goal(goal_result.get("goal"), thread_id, objective)
            state.update({"turn": completed, "goal": goal_after})
            if completed.get("status") != "completed":
                state["state"] = "failed"
                state["error"] = f"turn ended with status {completed.get('status')!r}"
                status_write(status_path, state)
                return 1
            if goal_after.get("status") in TERMINAL_GOAL_STATUSES:
                if args.lane == REVIEW_LANE and goal_after.get("status") == SUCCESSFUL_GOAL_STATUS:
                    assert binding is not None
                    history = connection.request(
                        "thread/turns/list",
                        {
                            "threadId": thread_id,
                            "itemsView": "full",
                            "sortDirection": "asc",
                            "limit": max(len(turn_ids), 1),
                        },
                    )
                    turns, review_output, output_text = require_full_review_history(
                        history, turn_ids, prompt, binding
                    )
                    state.update(
                        {
                            "full_turn_history": turns,
                            "full_turn_history_sha256": sha256_text(canonical_json(turns)),
                            "review_output": review_output,
                            "review_output_text": output_text,
                            "review_output_sha256": sha256_text(output_text),
                            "review_output_canonical_sha256": sha256_text(
                                canonical_json(review_output)
                            ),
                        }
                    )
                state["state"] = "finished"
                status_write(status_path, state)
                return 0 if goal_after.get("status") == SUCCESSFUL_GOAL_STATUS else 1
            state["continuation_count"] = int(state["continuation_count"]) + 1
            state["state"] = "live"
            status_write(status_path, state)
            turn_id = connection.wait_for_goal_continuation(thread_id)
    except BaseException as exc:
        state.update({"state": "failed", "error": str(exc)})
        status_write(status_path, state)
        raise
    finally:
        restore_signal_handlers(previous_handlers)
        connection.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--objective", type=Path, required=True)
    parser.add_argument("--status", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--lane", choices=sorted(LANES), required=True)
    parser.add_argument("--binding", type=Path)
    parser.add_argument("--thread-id")
    parser.add_argument(
        "--codex",
        default=str(Path.home() / ".local" / "bin" / "codex"),
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--effort", default=DEFAULT_EFFORT)
    parser.add_argument("--service-tier", default=DEFAULT_SERVICE_TIER)
    parser.add_argument("--timeout", type=float, default=86_400.0)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    return args


def main() -> None:
    try:
        raise SystemExit(run_worker(parse_args()))
    except (OSError, ProtocolError, json.JSONDecodeError) as exc:
        fail(str(exc))


if __name__ == "__main__":
    main()
