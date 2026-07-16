#!/usr/bin/env python3
"""Run one fail-closed Stage1 worker through the Codex app-server JSONL API."""

from __future__ import annotations

import argparse
from collections import deque
import codecs
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import time
from typing import Any, NoReturn


CLIENT_NAME = "awesome_theorems_stage1"
CLIENT_VERSION = "1.0.0"
DEFAULT_MODEL = "gpt-5.6-sol"
DEFAULT_EFFORT = "ultra"
DEFAULT_SERVICE_TIER = "priority"
RUNTIME_MODEL = "gpt-5.6-sol"
RUNTIME_EFFORT = "ultra"
RUNTIME_SERVICE_TIER = "priority"
RUNTIME_SANDBOX = "workspace-write"
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
RUNTIME_SANDBOX_CONTRACT = {
    "type": "workspaceWrite",
    "writableRoots": [],
    "networkAccess": False,
    "excludeTmpdirEnvVar": False,
    "excludeSlashTmp": False,
}
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


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


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
            message = json.loads(line)
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
    if row.get("model") != model:
        raise ProtocolError(f"model/list entry would alias or reroute requested model {model!r}")
    efforts = {
        option.get("reasoningEffort")
        for option in row.get("supportedReasoningEfforts", [])
        if isinstance(option, dict)
    }
    if effort not in efforts:
        raise ProtocolError(f"model {model!r} does not advertise reasoning effort {effort!r}")
    speed_tiers = row.get("additionalSpeedTiers")
    if not isinstance(speed_tiers, list) or "fast" not in speed_tiers:
        raise ProtocolError(f"model {model!r} does not advertise the Fast speed capability")
    tiers = {
        option.get("id"): option
        for option in row.get("serviceTiers", [])
        if isinstance(option, dict) and isinstance(option.get("id"), str)
    }
    tier = tiers.get(service_tier)
    if tier is None:
        raise ProtocolError(f"model {model!r} does not advertise service tier {service_tier!r}")
    if service_tier == RUNTIME_SERVICE_TIER and tier.get("name") != "Fast":
        raise ProtocolError("service tier 'priority' is not advertised as Fast")
    return row


def require_runtime_contract(
    result: dict[str, Any],
    workspace: Path,
    model: str,
    effort: str,
    service_tier: str,
) -> str:
    thread = result.get("thread")
    if not isinstance(thread, dict) or not isinstance(thread.get("id"), str):
        raise ProtocolError("thread/start did not return a thread id")
    actual = {
        "cwd": result.get("cwd"),
        "model": result.get("model"),
        "reasoningEffort": result.get("reasoningEffort"),
        "serviceTier": result.get("serviceTier"),
        "approvalPolicy": result.get("approvalPolicy"),
        "sandbox": result.get("sandbox"),
    }
    expected = {
        "cwd": str(workspace),
        "model": model,
        "reasoningEffort": effort,
        "serviceTier": service_tier,
        "approvalPolicy": "never",
        "sandbox": RUNTIME_SANDBOX_CONTRACT,
    }
    if actual != expected:
        raise ProtocolError(f"thread/start runtime contract mismatch: expected {expected}, got {actual}")
    return thread["id"]


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
) -> dict[str, Any]:
    return {
        "threadId": thread_id,
        "input": [{"type": "text", "text": text}],
        "cwd": str(workspace),
        "model": model,
        "effort": effort,
        "serviceTier": service_tier,
        "approvalPolicy": "never",
        "approvalsReviewer": "user",
        "sandboxPolicy": {
            "type": "workspaceWrite",
            "writableRoots": [str(workspace)],
            "networkAccess": False,
            "excludeTmpdirEnvVar": False,
            "excludeSlashTmp": False,
        },
    }


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
    prompt = args.prompt.read_text(encoding="utf-8")
    objective = args.objective.read_text(encoding="utf-8").strip()
    if not prompt.strip() or not objective:
        raise ProtocolError("worker prompt and goal objective must be nonempty")
    status_path = args.status.resolve()
    log_path = args.log.resolve()
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
        "workspace": str(workspace),
        "state": "starting",
        "continuation_count": 0,
    }
    atomic_write(status_path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")
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
        catalog = connection.request("model/list", {"includeHidden": True, "limit": 100})
        models = catalog.get("data")
        if not isinstance(models, list):
            raise ProtocolError("model/list returned a malformed catalog")
        advertised = model_contract(models, args.model, args.effort, args.service_tier)
        start = connection.request(
            "thread/start",
            {
                "model": args.model,
                "cwd": str(workspace),
                "approvalPolicy": "never",
                "approvalsReviewer": "user",
                "sandbox": RUNTIME_SANDBOX,
                "runtimeWorkspaceRoots": [str(workspace)],
                "serviceTier": args.service_tier,
                "config": {
                    "model_reasoning_effort": args.effort,
                    "service_tier": args.service_tier,
                    "features": {
                        "goals": True,
                        "code_mode": False,
                        "code_mode_host": False,
                        "code_mode_only": False,
                    },
                },
                "allowProviderModelFallback": False,
                "serviceName": CLIENT_NAME,
            },
        )
        thread_id = require_runtime_contract(
            start, workspace, args.model, args.effort, args.service_tier
        )
        set_result = connection.request(
            "thread/goal/set",
            {"threadId": thread_id, "objective": objective, "status": ACTIVE_GOAL_STATUS},
        )
        goal = require_goal(set_result.get("goal"), thread_id, objective)
        if goal.get("status") != ACTIVE_GOAL_STATUS:
            raise ProtocolError("thread/goal/set did not create the exact active goal")
        get_result = connection.request("thread/goal/get", {"threadId": thread_id})
        confirmed = require_goal(get_result.get("goal"), thread_id, objective)
        if not same_goal_identity(confirmed, goal):
            raise ProtocolError("thread/goal/get did not confirm the newly persisted goal")
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
        atomic_write(status_path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")

        turn_result = connection.request(
            "turn/start",
            turn_params(
                thread_id,
                prompt,
                workspace,
                args.model,
                args.effort,
                args.service_tier,
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
        while True:
            state["turn_id"] = turn_id
            atomic_write(status_path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")
            completed = connection.wait_for_turn(thread_id, turn_id)
            goal_result = connection.request("thread/goal/get", {"threadId": thread_id})
            goal_after = require_goal(goal_result.get("goal"), thread_id, objective)
            state.update({"turn": completed, "goal": goal_after})
            if completed.get("status") != "completed":
                state["state"] = "failed"
                state["error"] = f"turn ended with status {completed.get('status')!r}"
                atomic_write(status_path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")
                return 1
            if goal_after.get("status") in TERMINAL_GOAL_STATUSES:
                state["state"] = "finished"
                atomic_write(status_path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")
                return 0 if goal_after.get("status") == SUCCESSFUL_GOAL_STATUS else 1
            state["continuation_count"] = int(state["continuation_count"]) + 1
            state["state"] = "live"
            atomic_write(status_path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")
            turn_id = connection.wait_for_goal_continuation(thread_id)
    except BaseException as exc:
        state.update({"state": "failed", "error": str(exc)})
        atomic_write(status_path, json.dumps(state, ensure_ascii=False, indent=2) + "\n")
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
    parser.add_argument("--codex", default="codex")
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
