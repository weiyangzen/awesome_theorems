#!/usr/bin/env python3
"""Focused tests for the Stage1 Codex app-server client."""

from __future__ import annotations

import argparse
from collections import deque
import importlib.util
import json
import os
from pathlib import Path
import signal
import tempfile
import textwrap
import time
import unittest


MODULE_PATH = Path(__file__).with_name("stage1_app_server_client.py")
SPEC = importlib.util.spec_from_file_location("stage1_app_server_client_under_test", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
client = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(client)


def catalog_row() -> dict[str, object]:
    return {
        "id": "gpt-5.6-sol",
        "model": "gpt-5.6-sol",
        "supportedReasoningEfforts": [{"reasoningEffort": "ultra"}],
        "additionalSpeedTiers": ["fast"],
        "serviceTiers": [
            {"id": "priority", "name": "Fast", "description": "fast lane"}
        ],
    }


class ContractTests(unittest.TestCase):
    def test_runtime_args_are_exact_and_do_not_fallback(self) -> None:
        valid = argparse.Namespace(
            model="gpt-5.6-sol", effort="ultra", service_tier="priority"
        )
        client.require_exact_runtime_args(valid)
        for field, value in (
            ("model", "gpt-5.5"),
            ("effort", "max"),
            ("service_tier", "default"),
        ):
            invalid = argparse.Namespace(**vars(valid))
            setattr(invalid, field, value)
            with self.assertRaisesRegex(client.ProtocolError, "fallback is forbidden"):
                client.require_exact_runtime_args(invalid)

    def test_catalog_requires_priority_to_mean_fast(self) -> None:
        self.assertEqual(
            client.model_contract(
                [catalog_row()], "gpt-5.6-sol", "ultra", "priority"
            )["model"],
            "gpt-5.6-sol",
        )
        wrong = catalog_row()
        wrong["serviceTiers"] = [{"id": "priority", "name": "Default"}]
        with self.assertRaisesRegex(client.ProtocolError, "not advertised as Fast"):
            client.model_contract([wrong], "gpt-5.6-sol", "ultra", "priority")

        missing_fast = catalog_row()
        missing_fast["additionalSpeedTiers"] = []
        with self.assertRaisesRegex(client.ProtocolError, "Fast speed capability"):
            client.model_contract([missing_fast], "gpt-5.6-sol", "ultra", "priority")

    def test_server_request_responses_are_schema_shaped(self) -> None:
        connection = object.__new__(client.AppServerConnection)
        responses: list[tuple[object, dict[str, object]]] = []
        connection.respond = lambda request_id, result: responses.append((request_id, result))
        connection.handle_server_request(
            {
                "id": "input",
                "method": "item/tool/requestUserInput",
                "params": {"questions": [{"id": "choice"}]},
            }
        )
        connection.handle_server_request(
            {
                "id": "permissions",
                "method": "item/permissions/requestApproval",
                "params": {},
            }
        )
        self.assertEqual(responses[0], ("input", {"answers": {"choice": {"answers": []}}}))
        self.assertEqual(
            responses[1],
            ("permissions", {"permissions": {}, "scope": "turn"}),
        )

    def test_model_reroute_notification_is_always_rejected(self) -> None:
        for to_model in ("gpt-5.6", "gpt-5.6-sol"):
            with self.subTest(to_model=to_model), self.assertRaisesRegex(
                client.ProtocolError, "model reroute is forbidden"
            ):
                client.AppServerConnection.require_no_model_reroute(
                    {
                        "method": "model/rerouted",
                        "params": {
                            "threadId": "thread-1",
                            "turnId": "turn-1",
                            "fromModel": "gpt-5.6-sol",
                            "toModel": to_model,
                            "reason": "highRiskCyberActivity",
                        },
                    }
                )

    def test_model_reroute_is_rejected_while_waiting_for_response(self) -> None:
        connection = object.__new__(client.AppServerConnection)
        connection.next_id = 1
        connection.timeout = 1.0
        connection.pending_responses = {}
        connection.notifications = deque()
        connection.send = lambda _message: None
        connection.read_message = lambda _deadline: {
            "method": "model/rerouted",
            "params": {
                "threadId": "thread-1",
                "turnId": "turn-1",
                "fromModel": "gpt-5.6-sol",
                "toModel": "gpt-5.6",
                "reason": "highRiskCyberActivity",
            },
        }
        with self.assertRaisesRegex(client.ProtocolError, "model reroute is forbidden"):
            connection.request("model/list", {})


class ScriptedAppServer:
    """A tiny protocol peer; it performs no Codex work."""

    def __init__(
        self,
        path: Path,
        transcript: Path,
        *,
        continue_once: bool = False,
        server_request: bool = False,
    ) -> None:
        mode = "continue" if continue_once else "complete"
        request_mode = "request" if server_request else "none"
        source = f"""\
            #!/usr/bin/env python3
            import json, sys
            transcript = {str(transcript)!r}
            mode = {mode!r}
            request_mode = {request_mode!r}
            thread_id = "thread-1"
            objective = None
            turn_count = 0
            goal_get_count = 0
            messages = []
            def send(value):
                print(json.dumps(value, separators=(",", ":")), flush=True)
            def record(value):
                with open(transcript, "w", encoding="utf-8") as handle:
                    json.dump(value, handle)
            for line in sys.stdin:
                message = json.loads(line)
                messages.append(message)
                record(messages)
                method = message.get("method")
                request_id = message.get("id")
                if request_id == "srv-1" and "result" in message:
                    continue
                if method == "initialized":
                    continue
                if method == "initialize":
                    send({{"id": request_id, "result": {{}}}})
                elif method == "model/list":
                    send({{"id": request_id, "result": {{"data": [{json.dumps(catalog_row())}]}}}})
                elif method == "thread/start":
                    params = message["params"]
                    send({{"id": request_id, "result": {{
                        "thread": {{"id": thread_id}},
                        "cwd": params["cwd"],
                        "model": params["model"],
                        "reasoningEffort": params["config"]["model_reasoning_effort"],
                        "serviceTier": params["serviceTier"],
                        "approvalPolicy": params["approvalPolicy"],
                        "sandbox": {{
                            "type": "workspaceWrite",
                            "writableRoots": [],
                            "networkAccess": False,
                            "excludeTmpdirEnvVar": False,
                            "excludeSlashTmp": False,
                        }},
                    }}}})
                elif method == "thread/goal/set":
                    objective = message["params"]["objective"]
                    send({{"id": request_id, "result": {{"goal": {{
                        "threadId": thread_id, "objective": objective,
                        "status": "active", "tokensUsed": 0,
                        "timeUsedSeconds": 0, "createdAt": 1, "updatedAt": 1,
                    }}}}}})
                elif method == "thread/goal/get":
                    goal_get_count += 1
                    status = "active" if goal_get_count == 1 or (mode == "continue" and goal_get_count < 3) else "complete"
                    send({{"id": request_id, "result": {{"goal": {{
                        "threadId": thread_id, "objective": objective,
                        "status": status, "tokensUsed": 0,
                        "timeUsedSeconds": 0, "createdAt": 1, "updatedAt": 1,
                    }}}}}})
                elif method == "turn/start":
                    turn_count += 1
                    turn_id = f"turn-{{turn_count}}"
                    response_turn_id = f"response-{{turn_count}}"
                    if request_mode == "request" and turn_count == 1:
                        send({{"id": "srv-1", "method": "currentTime/read", "params": {{"threadId": thread_id}}}})
                    send({{"method": "turn/started", "params": {{
                        "threadId": "other-thread",
                        "turn": {{"id": "other-turn", "status": "inProgress", "items": []}},
                    }}}})
                    send({{"method": "turn/started", "params": {{
                        "threadId": thread_id,
                        "turn": {{"id": turn_id, "status": "inProgress", "items": []}},
                    }}}})
                    send({{"id": request_id, "result": {{"turn": {{"id": response_turn_id}}}}}})
                    send({{"method": "turn/completed", "params": {{
                        "threadId": thread_id,
                        "turn": {{"id": turn_id, "status": "completed", "items": []}},
                    }}}})
                    if mode == "continue" and turn_count == 1:
                        turn_count += 1
                        turn_id = f"turn-{{turn_count}}"
                        send({{"method": "turn/started", "params": {{
                            "threadId": thread_id,
                            "turn": {{"id": turn_id, "status": "inProgress", "items": []}},
                        }}}})
                        send({{"method": "turn/completed", "params": {{
                            "threadId": thread_id,
                            "turn": {{"id": turn_id, "status": "completed", "items": []}},
                        }}}})
        """
        path.write_text(textwrap.dedent(source), encoding="utf-8")
        path.chmod(0o755)


class SignalAppServer:
    """Protocol peer that leaves one child for process-group cleanup checks."""

    def __init__(self, path: Path, child_pid: Path) -> None:
        source = f"""\
            #!/usr/bin/env python3
            import os, signal, subprocess, sys, time
            child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
            with open({str(child_pid)!r}, "w", encoding="utf-8") as handle:
                handle.write(str(child.pid))
            signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
            while True:
                time.sleep(1)
        """
        path.write_text(textwrap.dedent(source), encoding="utf-8")
        path.chmod(0o755)


class FlowTests(unittest.TestCase):
    def run_flow(
        self, *, continue_once: bool = False, server_request: bool = False
    ) -> tuple[int, dict[str, object], list[dict[str, object]]]:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            workspace = root / "workspace"
            workspace.mkdir()
            prompt = root / "prompt.txt"
            prompt.write_text("Implement the assigned item.\n", encoding="utf-8")
            objective = root / "objective.txt"
            objective.write_text("Complete exactly S56-M-0001-INTAKE.\n", encoding="utf-8")
            status = root / "status.json"
            log = root / "server.log"
            transcript = root / "transcript.json"
            server = root / "codex"
            ScriptedAppServer(
                server,
                transcript,
                continue_once=continue_once,
                server_request=server_request,
            )
            args = argparse.Namespace(
                workspace=workspace,
                prompt=prompt,
                objective=objective,
                status=status,
                log=log,
                codex=str(server),
                model="gpt-5.6-sol",
                effort="ultra",
                service_tier="priority",
                timeout=5.0,
            )
            result = client.run_worker(args)
            state = json.loads(status.read_text(encoding="utf-8"))
            transcript_data = json.loads(transcript.read_text(encoding="utf-8"))
            return result, state, transcript_data

    def test_real_order_and_required_runtime_fields(self) -> None:
        result, state, transcript = self.run_flow()
        self.assertEqual(result, 0)
        methods = [message.get("method") for message in transcript if "method" in message]
        self.assertLess(methods.index("thread/start"), methods.index("thread/goal/set"))
        self.assertLess(methods.index("thread/goal/set"), methods.index("thread/goal/get"))
        self.assertLess(methods.index("thread/goal/get"), methods.index("turn/start"))
        start = next(message for message in transcript if message.get("method") == "thread/start")
        self.assertFalse(start["params"]["allowProviderModelFallback"])
        self.assertEqual(start["params"]["model"], "gpt-5.6-sol")
        self.assertEqual(start["params"]["serviceTier"], "priority")
        self.assertEqual(start["params"]["config"]["model_reasoning_effort"], "ultra")
        self.assertEqual(start["params"]["sandbox"], "workspace-write")
        self.assertEqual(start["params"]["runtimeWorkspaceRoots"], [state["workspace"]])
        self.assertFalse(start["params"]["config"]["features"]["code_mode"])
        self.assertFalse(start["params"]["config"]["features"]["code_mode_host"])
        self.assertFalse(start["params"]["config"]["features"]["code_mode_only"])
        goal_set = next(
            message for message in transcript if message.get("method") == "thread/goal/set"
        )
        self.assertEqual(goal_set["params"]["status"], "active")
        self.assertEqual(state["state"], "finished")
        self.assertEqual(state["goal"]["status"], "complete")
        self.assertEqual(state["turn_start_response_id"], "response-1")
        self.assertEqual(state["turn_id"], "turn-1")
        self.assertIsInstance(state["client_start_ticks"], int)
        self.assertIsInstance(state["app_server_start_ticks"], int)
        self.assertEqual(
            state["runtime_contract"]["sandbox"],
            {
                "type": "workspaceWrite",
                "writableRoots": [],
                "networkAccess": False,
                "excludeTmpdirEnvVar": False,
                "excludeSlashTmp": False,
            },
        )
        self.assertIs(state["runtime_contract"]["network_access"], False)
        self.assertEqual(
            state["runtime_contract"]["app_server_argv"],
            [
                "app-server", "--stdio", "--enable", "goals",
                "--disable", "code_mode",
                "--disable", "code_mode_host",
                "--disable", "code_mode_only",
            ],
        )

    def test_active_goal_automatically_starts_continuation_turn(self) -> None:
        result, state, transcript = self.run_flow(continue_once=True)
        self.assertEqual(result, 0)
        turns = [message for message in transcript if message.get("method") == "turn/start"]
        self.assertEqual(len(turns), 1)
        self.assertEqual(state["continuation_count"], 1)
        self.assertEqual(state["turn_id"], "turn-2")
        self.assertEqual(turns[0]["params"]["model"], "gpt-5.6-sol")
        self.assertEqual(turns[0]["params"]["effort"], "ultra")
        self.assertEqual(turns[0]["params"]["serviceTier"], "priority")
        self.assertEqual(
            turns[0]["params"]["sandboxPolicy"],
            {
                "type": "workspaceWrite",
                "writableRoots": [state["workspace"]],
                "networkAccess": False,
                "excludeTmpdirEnvVar": False,
                "excludeSlashTmp": False,
            },
        )

    def test_recorded_app_server_continuation_is_not_client_started(self) -> None:
        first_id = "619e2d6b-cd13-4d92-8f3f-16804c86e154"
        continuation_id = "32a2c7e4-9bfb-4cc0-a6aa-8484d3a8528f"
        connection = object.__new__(client.AppServerConnection)
        connection.timeout = 1.0
        connection.notifications = deque(
            [
                {
                    "method": "turn/completed",
                    "params": {
                        "threadId": "thread-1",
                        "turn": {"id": first_id, "status": "completed", "items": []},
                    },
                },
                {
                    "method": "thread/status/changed",
                    "params": {"threadId": "thread-1", "status": {"type": "idle"}},
                },
                {
                    "method": "turn/started",
                    "params": {
                        "threadId": "other-thread",
                        "turn": {"id": "wrong", "status": "inProgress", "items": []},
                    },
                },
                {
                    "method": "turn/started",
                    "params": {
                        "threadId": "thread-1",
                        "turn": {
                            "id": continuation_id,
                            "status": "inProgress",
                            "items": [],
                        },
                    },
                },
            ]
        )
        connection.deferred_notifications = deque()
        completed = connection.wait_for_turn("thread-1", first_id)
        self.assertEqual(completed["id"], first_id)
        self.assertEqual(
            connection.wait_for_goal_continuation("thread-1"), continuation_id
        )

    def test_initial_turn_uses_started_event_id_not_response_id(self) -> None:
        response_id = "019f6964-3c2e-7423-948d-476c54d017e9"
        event_id = "619e2d6b-cd13-4d92-8f3f-16804c86e154"
        connection = object.__new__(client.AppServerConnection)
        connection.timeout = 1.0
        connection.notifications = deque(
            [
                {
                    "method": "turn/started",
                    "params": {
                        "threadId": "other-thread",
                        "turn": {"id": response_id, "status": "inProgress"},
                    },
                },
                {
                    "method": "turn/started",
                    "params": {
                        "threadId": "thread-1",
                        "turn": {"id": event_id, "status": "inProgress"},
                    },
                },
                {
                    "method": "turn/completed",
                    "params": {
                        "threadId": "thread-1",
                        "turn": {"id": event_id, "status": "completed", "items": []},
                    },
                },
            ]
        )
        connection.deferred_notifications = deque()
        actual_id = connection.wait_for_turn_started("thread-1")
        self.assertNotEqual(actual_id, response_id)
        self.assertEqual(actual_id, event_id)
        self.assertEqual(connection.wait_for_turn("thread-1", actual_id)["id"], event_id)
        self.assertEqual(len(connection.deferred_notifications), 1)

    def test_turn_wait_retains_already_buffered_future_events(self) -> None:
        initial_id = "initial"
        continuation_id = "continuation"
        connection = object.__new__(client.AppServerConnection)
        connection.timeout = 1.0
        connection.notifications = deque(
            [
                {
                    "method": "turn/started",
                    "params": {
                        "threadId": "thread-1",
                        "turn": {"id": continuation_id, "status": "inProgress"},
                    },
                },
                {
                    "method": "turn/completed",
                    "params": {
                        "threadId": "thread-1",
                        "turn": {"id": initial_id, "status": "completed"},
                    },
                },
            ]
        )
        connection.deferred_notifications = deque()
        self.assertEqual(connection.wait_for_turn("thread-1", initial_id)["id"], initial_id)
        self.assertEqual(
            connection.wait_for_goal_continuation("thread-1"), continuation_id
        )

    def test_server_request_is_answered_while_waiting_for_response(self) -> None:
        result, _state, transcript = self.run_flow(server_request=True)
        self.assertEqual(result, 0)
        response = next(message for message in transcript if message.get("id") == "srv-1")
        self.assertIsInstance(response["result"]["currentTimeAt"], int)


class ProcessGroupTests(unittest.TestCase):
    def test_interrupt_forwards_signal_to_app_server_group(self) -> None:
        connection = object.__new__(client.AppServerConnection)
        connection.interrupted_signal = None
        connection.process = type("Process", (), {"pid": 1234, "poll": lambda self: None})()
        calls: list[tuple[int, int]] = []
        original = os.killpg
        try:
            os.killpg = lambda pid, signum: calls.append((pid, signum))  # type: ignore[assignment]
            connection.interrupt(signal.SIGTERM)
        finally:
            os.killpg = original
        self.assertEqual(connection.interrupted_signal, signal.SIGTERM)
        self.assertEqual(calls, [(1234, signal.SIGTERM)])

    def test_close_signals_group_even_when_leader_already_exited(self) -> None:
        connection = object.__new__(client.AppServerConnection)
        connection.closed = False
        connection.selector = type("Selector", (), {"close": lambda self: None})()
        connection.log = type("Log", (), {"close": lambda self: None})()
        connection.process = type(
            "Process",
            (),
            {
                "pid": 4321,
                "stdin": None,
                "stdout": None,
                "poll": lambda self: 0,
            },
        )()
        calls: list[tuple[int, int]] = []
        original_killpg = os.killpg
        original_exists = client.AppServerConnection._group_exists
        try:
            os.killpg = lambda pid, signum: calls.append((pid, signum))  # type: ignore[assignment]
            client.AppServerConnection._group_exists = lambda self: False
            connection.close()
        finally:
            os.killpg = original_killpg
            client.AppServerConnection._group_exists = original_exists
        self.assertEqual(calls, [(4321, signal.SIGTERM)])

    def test_close_reaps_app_server_and_its_child_process_group(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            server = root / "server"
            child_pid_path = root / "child.pid"
            SignalAppServer(server, child_pid_path)
            connection = client.AppServerConnection([str(server)], root / "log", 2.0)
            deadline = time.monotonic() + 2
            while not child_pid_path.exists() and time.monotonic() < deadline:
                time.sleep(0.01)
            child_pid = int(child_pid_path.read_text(encoding="utf-8"))
            app_server_pid = connection.process.pid
            connection.close()
            self.assertFalse(Path(f"/proc/{app_server_pid}").exists())
            deadline = time.monotonic() + 2
            while Path(f"/proc/{child_pid}").exists() and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertFalse(Path(f"/proc/{child_pid}").exists())


if __name__ == "__main__":
    unittest.main()
