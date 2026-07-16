#!/usr/bin/env python3
"""Focused tests for the Stage1 Codex app-server client."""

from __future__ import annotations

import argparse
from collections import deque
import hashlib
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


def other_catalog_row(suffix: str = "one") -> dict[str, object]:
    row = catalog_row()
    row["id"] = f"other-{suffix}"
    row["model"] = f"other-{suffix}"
    return row


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def review_binding(prompt: str, objective: str) -> dict[str, object]:
    return {
        "schema_version": client.REVIEW_BINDING_SCHEMA,
        "claim_id": "20260716T120000Z-review-0123456789ab",
        "item_id": "S56-M-0001-INTAKE",
        "theorem_id": "THM-M-0001",
        "phase": "intake",
        "base_revision": "a" * 40,
        "blueprint_sha256": "b" * 64,
        "theorem_dag_sha256": "c" * 64,
        "prompt_sha256": sha256_text(prompt),
        "objective_sha256": sha256_text(objective),
        "artifact_digests": {"Stage1_Instances/THM-M-0001/intake-receipt.json": "d" * 64},
        "validator_recipe_sha256s": ["e" * 64],
        "output_schema": client.REVIEW_OUTPUT_SCHEMA,
    }


def review_output(binding: dict[str, object]) -> dict[str, object]:
    return {
        "schema_version": client.REVIEW_OUTPUT_SCHEMA,
        "claim_id": binding["claim_id"],
        "item_id": binding["item_id"],
        "theorem_id": binding["theorem_id"],
        "phase": binding["phase"],
        "worker_verdict": "no_state_change",
        "review_verdict": "phase_accepted",
        "audit_complete": False,
        "theorem_complete": False,
        "root_state": None,
        "first_failed_gate": None,
        "retry_condition": None,
        "status_boundary": "The intake evidence is accepted; theorem closure remains open.",
        "artifact_findings": [],
        "reviewed_artifact_sha256s": binding["artifact_digests"],
        "validator_recipe_sha256s": binding["validator_recipe_sha256s"],
    }


class ContractTests(unittest.TestCase):
    def test_runtime_args_are_exact_and_do_not_fallback(self) -> None:
        valid = argparse.Namespace(
            model="gpt-5.6-sol", effort="ultra", service_tier="priority",
            lane="implementation", binding=None,
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

    def test_lane_and_binding_arguments_are_fail_closed(self) -> None:
        valid = argparse.Namespace(
            model="gpt-5.6-sol",
            effort="ultra",
            service_tier="priority",
            lane="review",
            binding=Path("binding.json"),
        )
        client.require_exact_runtime_args(valid)
        valid.lane = "other"
        with self.assertRaisesRegex(client.ProtocolError, "unsupported app-server lane"):
            client.require_exact_runtime_args(valid)
        valid.lane = "implementation"
        with self.assertRaisesRegex(client.ProtocolError, "must not receive"):
            client.require_exact_runtime_args(valid)

    def test_review_binding_requires_exact_fields_and_input_hashes(self) -> None:
        prompt = "Review exactly one item.\n"
        objective = "Review S56-M-0001-INTAKE."
        value = review_binding(prompt, objective)
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "binding.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            loaded, digest = client.require_review_binding(
                path, sha256_text(prompt), sha256_text(objective)
            )
            self.assertEqual(loaded, value)
            self.assertEqual(digest, sha256_text(client.canonical_json(value)))
            value["prompt_sha256"] = "0" * 64
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaisesRegex(client.ProtocolError, "input digest mismatch"):
                client.require_review_binding(
                    path, sha256_text(prompt), sha256_text(objective)
                )

    def test_review_output_rejects_wrong_identity_keys_and_digests(self) -> None:
        binding = review_binding("prompt", "objective")
        for field, mutation in (
            ("claim_id", lambda value: value.update(claim_id="wrong")),
            ("keys", lambda value: value.update(extra=True)),
            (
                "digests",
                lambda value: value.update(reviewed_artifact_sha256s={"x": "f" * 64}),
            ),
        ):
            with self.subTest(field=field):
                value = review_output(binding)
                mutation(value)
                with self.assertRaises(client.ProtocolError):
                    client.require_review_output(value, binding)

    def test_review_output_rejects_open_worker_verdict_and_impossible_terminal_flags(self) -> None:
        binding = review_binding("prompt", "objective")
        for name, mutation in (
            ("worker_verdict", lambda value: value.update(worker_verdict="invented")),
            ("audit_before_release", lambda value: value.update(audit_complete=True)),
            (
                "theorem_before_release",
                lambda value: value.update(audit_complete=True, theorem_complete=True),
            ),
        ):
            with self.subTest(name=name):
                value = review_output(binding)
                mutation(value)
                with self.assertRaises(client.ProtocolError):
                    client.require_review_output(value, binding)

        binding["item_id"] = "S56-M-0001-RELEASE"
        binding["phase"] = "release"
        value = review_output(binding)
        with self.assertRaises(client.ProtocolError):
            client.require_review_output(value, binding)
        value.update(worker_verdict="accepted_audit_only", audit_complete=True)
        self.assertEqual(client.require_review_output(value, binding), value)

    def test_review_binding_requires_canonical_base_revision(self) -> None:
        prompt = "prompt"
        objective = "objective"
        for revision in ("a" * 39, "A" * 40, "a" * 64, "HEAD"):
            with self.subTest(revision=revision), tempfile.TemporaryDirectory() as raw:
                value = review_binding(prompt, objective)
                value["base_revision"] = revision
                path = Path(raw) / "binding.json"
                path.write_text(json.dumps(value), encoding="utf-8")
                with self.assertRaisesRegex(client.ProtocolError, "identity or input"):
                    client.require_review_binding(
                        path, sha256_text(prompt), sha256_text(objective)
                    )

    def test_review_binding_requires_canonical_unique_posix_artifact_paths(self) -> None:
        prompt = "prompt"
        objective = "objective"
        for relative in ("a//b", "a/./b", "a\\b", "/a/b", "a/../b"):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as raw:
                value = review_binding(prompt, objective)
                value["artifact_digests"] = {relative: "d" * 64}
                path = Path(raw) / "binding.json"
                path.write_text(json.dumps(value), encoding="utf-8")
                with self.assertRaisesRegex(client.ProtocolError, "artifact or validator"):
                    client.require_review_binding(
                        path, sha256_text(prompt), sha256_text(objective)
                    )

        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "binding.json"
            encoded = json.dumps(review_binding(prompt, objective))
            encoded = encoded.replace(
                '"artifact_digests": {"Stage1_Instances/THM-M-0001/intake-receipt.json": "'
                + "d" * 64
                + '"}',
                '"artifact_digests": {"a/b": "'
                + "d" * 64
                + '", "a/b": "'
                + "e" * 64
                + '"}',
            )
            path.write_text(encoded, encoding="utf-8")
            with self.assertRaisesRegex(client.ProtocolError, "duplicate JSON name"):
                client.require_review_binding(
                    path, sha256_text(prompt), sha256_text(objective)
                )

    def test_review_output_schema_is_exact(self) -> None:
        schema = client.REVIEW_OUTPUT_JSON_SCHEMA
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["required"]), client.REVIEW_OUTPUT_FIELDS)
        self.assertEqual(set(schema["properties"]), client.REVIEW_OUTPUT_FIELDS)

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

        alias = catalog_row()
        alias["id"] = "provider-alias"
        with self.assertRaisesRegex(client.ProtocolError, "alias or reroute"):
            client.model_contract([alias], "gpt-5.6-sol", "ultra", "priority")

        duplicate = catalog_row()
        duplicate["serviceTiers"] = [
            {"id": "priority", "name": "Default"},
            {"id": "priority", "name": "Fast"},
        ]
        with self.assertRaisesRegex(client.ProtocolError, "exactly once"):
            client.model_contract([duplicate], "gpt-5.6-sol", "ultra", "priority")

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

    def test_app_server_duplicate_json_members_are_rejected(self) -> None:
        connection = object.__new__(client.AppServerConnection)
        connection.process = type("Process", (), {"stdout": object()})()
        connection.stdout_buffer = '{"id":1,"result":{},"result":{"thread":{}}}\n'
        connection.stdout_decoder = None
        with self.assertRaisesRegex(client.ProtocolError, "duplicate JSON name 'result'"):
            connection.read_message(time.monotonic() + 1)


class ScriptedAppServer:
    """A tiny protocol peer; it performs no Codex work."""

    def __init__(
        self,
        path: Path,
        transcript: Path,
        *,
        continue_once: bool = False,
        server_request: bool = False,
        review: bool = False,
        review_output_value: dict[str, object] | None = None,
        history_mode: str = "valid",
        persisted_objective: str | None = None,
        resume_mode: str = "valid",
        catalog_mode: str = "valid",
    ) -> None:
        mode = "continue" if continue_once else "complete"
        request_mode = "request" if server_request else "none"
        lane_mode = "review" if review else "implementation"
        review_output_json = json.dumps(review_output_value, sort_keys=True, separators=(",", ":"))
        source = f"""\
            #!/usr/bin/env python3
            import json, sys
            transcript = {str(transcript)!r}
            mode = {mode!r}
            request_mode = {request_mode!r}
            lane_mode = {lane_mode!r}
            history_mode = {history_mode!r}
            resume_mode = {resume_mode!r}
            catalog_mode = {catalog_mode!r}
            review_output_json = {review_output_json!r}
            target_catalog = {catalog_row()!r}
            other_catalog_one = {other_catalog_row("one")!r}
            other_catalog_two = {other_catalog_row("two")!r}
            thread_id = "thread-1"
            objective = {persisted_objective!r}
            turn_count = 0
            goal_get_count = 0
            prompt = None
            turn_ids = []
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
                    cursor = message["params"].get("cursor")
                    if catalog_mode == "second_page":
                        result = ({{"data": [other_catalog_one], "nextCursor": "page-2"}}
                                  if cursor is None else
                                  {{"data": [target_catalog], "nextCursor": None}})
                    elif catalog_mode == "cursor_cycle":
                        result = ({{"data": [other_catalog_one], "nextCursor": "cycle"}}
                                  if cursor is None else
                                  {{"data": [other_catalog_two], "nextCursor": "cycle"}})
                    elif catalog_mode == "duplicate_model":
                        result = {{"data": [target_catalog],
                                  "nextCursor": "page-2" if cursor is None else None}}
                    elif catalog_mode == "missing_next_cursor":
                        result = {{"data": [target_catalog]}}
                    elif catalog_mode == "data_not_list":
                        result = {{"data": {{}}, "nextCursor": None}}
                    elif catalog_mode == "row_not_object":
                        result = {{"data": ["not-a-model"], "nextCursor": None}}
                    elif catalog_mode == "bad_cursor":
                        result = {{"data": [other_catalog_one], "nextCursor": 7}}
                    else:
                        result = {{"data": [target_catalog], "nextCursor": None}}
                    send({{"id": request_id, "result": result}})
                elif method == "thread/start":
                    params = message["params"]
                    sandbox = ({{"type": "readOnly", "networkAccess": False}}
                               if lane_mode == "review" else {{
                                   "type": "workspaceWrite", "writableRoots": [],
                                   "networkAccess": False, "excludeTmpdirEnvVar": False,
                                   "excludeSlashTmp": False,
                               }})
                    send({{"id": request_id, "result": {{
                        "thread": {{"id": thread_id}},
                        "cwd": params["cwd"],
                        "model": params["model"],
                        "reasoningEffort": params["config"]["model_reasoning_effort"],
                        "serviceTier": params["serviceTier"],
                        "approvalPolicy": params["approvalPolicy"],
                        "approvalsReviewer": params["approvalsReviewer"],
                        "sandbox": sandbox,
                        "runtimeWorkspaceRoots": params["runtimeWorkspaceRoots"],
                    }}}})
                elif method == "thread/resume":
                    params = message["params"]
                    sandbox = ({{"type": "readOnly", "networkAccess": False}}
                               if lane_mode == "review" else {{
                                   "type": "workspaceWrite", "writableRoots": [],
                                   "networkAccess": False, "excludeTmpdirEnvVar": False,
                                   "excludeSlashTmp": False,
                               }})
                    send({{"id": request_id, "result": {{
                        "thread": {{"id": ("wrong-thread"
                                            if resume_mode == "wrong_thread"
                                            else thread_id)}},
                        "cwd": ("/wrong" if resume_mode == "wrong_runtime"
                                else params["cwd"]),
                        "model": ("gpt-5.6" if resume_mode == "wrong_model"
                                  else params["model"]),
                        "reasoningEffort": ("max" if resume_mode == "wrong_effort"
                                            else params["config"]["model_reasoning_effort"]),
                        "serviceTier": ("default" if resume_mode == "wrong_tier"
                                        else params["serviceTier"]),
                        "approvalPolicy": params["approvalPolicy"],
                        "approvalsReviewer": params["approvalsReviewer"],
                        "sandbox": sandbox,
                        "runtimeWorkspaceRoots": ([] if resume_mode == "wrong_roots"
                                                  else params["runtimeWorkspaceRoots"]),
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
                    status = ("blocked" if resume_mode == "terminal_goal" and goal_get_count == 1
                              else "active" if goal_get_count == 1 or (mode == "continue" and goal_get_count < 3)
                              else "complete")
                    send({{"id": request_id, "result": {{"goal": {{
                        "threadId": thread_id,
                        "objective": ("wrong objective"
                                      if resume_mode == "wrong_goal"
                                      else objective),
                        "status": status, "tokensUsed": 0,
                        "timeUsedSeconds": 0, "createdAt": 1, "updatedAt": 1,
                    }}}}}})
                elif method == "turn/start":
                    prompt = message["params"]["input"][0]["text"]
                    turn_count += 1
                    turn_id = f"turn-{{turn_count}}"
                    turn_ids.append(turn_id)
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
                        turn_ids.append(turn_id)
                        send({{"method": "turn/started", "params": {{
                            "threadId": thread_id,
                            "turn": {{"id": turn_id, "status": "inProgress", "items": []}},
                        }}}})
                        send({{"method": "turn/completed", "params": {{
                            "threadId": thread_id,
                            "turn": {{"id": turn_id, "status": "completed", "items": []}},
                        }}}})
                elif method == "thread/turns/list":
                    turns = []
                    for index, recorded_id in enumerate(turn_ids):
                        items = []
                        if index == 0:
                            items.append({{
                                "id": "user-1", "type": "userMessage",
                                "content": [{{"type": "text", "text": prompt}}],
                            }})
                        if index == len(turn_ids) - 1:
                            items.append({{
                                "id": "agent-1", "type": "agentMessage",
                                "phase": ("commentary" if history_mode == "commentary"
                                          else "final_answer"),
                                "text": review_output_json,
                            }})
                        if history_mode == "file_change":
                            items.append({{"id": "file-1", "type": "fileChange", "status": "completed", "changes": []}})
                        if history_mode == "command_execution":
                            items.append({{
                                "id": "command-1", "type": "commandExecution",
                                "command": "true", "commandActions": [], "cwd": "/tmp",
                                "status": "completed",
                            }})
                        if history_mode == "reasoning":
                            items.append({{
                                "id": "reasoning-1", "type": "reasoning",
                                "summary": [], "content": [],
                            }})
                        turns.append({{
                            "id": recorded_id,
                            "status": "completed",
                            "itemsView": "summary" if history_mode == "summary" else "full",
                            "items": items,
                        }})
                    if history_mode == "bad_output":
                        turns[-1]["items"][-1]["text"] = "not json"
                    if history_mode == "intermediate_final":
                        turns[0]["items"].append(turns[-1]["items"].pop())
                    send({{"id": request_id, "result": {{
                        "data": turns,
                        "nextCursor": "more" if history_mode == "paginated" else None,
                        "backwardsCursor": ("earlier"
                                            if history_mode == "backwards_paginated"
                                            else None),
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
        self,
        *,
        continue_once: bool = False,
        server_request: bool = False,
        lane: str = client.IMPLEMENTATION_LANE,
        history_mode: str = "valid",
        binding_mutator: object | None = None,
        output_mutator: object | None = None,
        thread_id: str | None = None,
        persisted_objective: str | None = None,
        resume_mode: str = "valid",
        catalog_mode: str = "valid",
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
            binding_path = root / "binding.json"
            binding_value: dict[str, object] | None = None
            output_value: dict[str, object] | None = None
            if lane == client.REVIEW_LANE:
                prompt_text = prompt.read_text(encoding="utf-8")
                objective_text = objective.read_text(encoding="utf-8").strip()
                binding_value = review_binding(prompt_text, objective_text)
                if binding_mutator is not None:
                    binding_mutator(binding_value)
                binding_path.write_text(json.dumps(binding_value), encoding="utf-8")
                output_value = review_output(binding_value)
                if output_mutator is not None:
                    output_mutator(output_value)
            ScriptedAppServer(
                server,
                transcript,
                continue_once=continue_once,
                server_request=server_request,
                review=lane == client.REVIEW_LANE,
                review_output_value=output_value,
                history_mode=history_mode,
                persisted_objective=persisted_objective,
                resume_mode=resume_mode,
                catalog_mode=catalog_mode,
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
                lane=lane,
                binding=binding_path if lane == client.REVIEW_LANE else None,
                thread_id=thread_id,
                timeout=5.0,
            )
            result = client.run_worker(args)
            state = json.loads(status.read_text(encoding="utf-8"))
            transcript_data = json.loads(transcript.read_text(encoding="utf-8"))
            return result, state, transcript_data

    def test_model_catalog_target_on_second_page_is_used(self) -> None:
        result, state, transcript = self.run_flow(catalog_mode="second_page")
        self.assertEqual(result, 0)
        requests = [
            message for message in transcript if message.get("method") == "model/list"
        ]
        self.assertEqual(len(requests), 2)
        self.assertEqual(
            requests[0]["params"], {"includeHidden": True, "limit": 100}
        )
        self.assertEqual(
            requests[1]["params"],
            {"includeHidden": True, "limit": 100, "cursor": "page-2"},
        )
        self.assertEqual(state["model_catalog_entry"]["id"], "gpt-5.6-sol")

    def test_model_catalog_rejects_cursor_cycles_and_duplicate_models(self) -> None:
        for mode, message in (
            ("cursor_cycle", "cursor cycle"),
            ("duplicate_model", "duplicate model identity"),
        ):
            with self.subTest(mode=mode), self.assertRaisesRegex(
                client.ProtocolError, message
            ):
                self.run_flow(catalog_mode=mode)

    def test_model_catalog_rejects_malformed_page_structure(self) -> None:
        for mode, message in (
            ("missing_next_cursor", "malformed catalog page"),
            ("data_not_list", "malformed catalog page"),
            ("row_not_object", "malformed catalog model"),
            ("bad_cursor", "malformed nextCursor"),
        ):
            with self.subTest(mode=mode), self.assertRaisesRegex(
                client.ProtocolError, message
            ):
                self.run_flow(catalog_mode=mode)

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
        self.assertNotIn("outputSchema", turns[0]["params"])

    def test_resume_reuses_exact_persisted_goal_without_overwriting_it(self) -> None:
        objective = "Complete exactly S56-M-0001-INTAKE."
        result, state, transcript = self.run_flow(
            thread_id="thread-1",
            persisted_objective=objective,
        )
        self.assertEqual(result, 0)
        methods = [message.get("method") for message in transcript if "method" in message]
        self.assertIn("thread/resume", methods)
        self.assertNotIn("thread/start", methods)
        self.assertNotIn("thread/goal/set", methods)
        self.assertLess(methods.index("thread/resume"), methods.index("thread/goal/get"))
        self.assertLess(methods.index("thread/goal/get"), methods.index("turn/start"))
        resume = next(
            message for message in transcript if message.get("method") == "thread/resume"
        )
        self.assertEqual(
            resume["params"],
            {
                "threadId": "thread-1",
                "model": "gpt-5.6-sol",
                "cwd": state["workspace"],
                "approvalPolicy": "never",
                "approvalsReviewer": "user",
                "sandbox": "workspace-write",
                "runtimeWorkspaceRoots": [state["workspace"]],
                "serviceTier": "priority",
                "config": {
                    "model_reasoning_effort": "ultra",
                    "service_tier": "priority",
                    "features": {
                        "goals": True,
                        "code_mode": False,
                        "code_mode_host": False,
                        "code_mode_only": False,
                    },
                },
                "excludeTurns": True,
            },
        )
        self.assertNotIn("allowProviderModelFallback", resume["params"])
        self.assertTrue(state["resumed"])
        self.assertEqual(state["thread_id"], "thread-1")
        self.assertEqual(state["goal"]["objective"], objective)

    def test_fresh_thread_records_not_resumed(self) -> None:
        result, state, transcript = self.run_flow()
        self.assertEqual(result, 0)
        self.assertFalse(state["resumed"])
        self.assertTrue(
            any(message.get("method") == "thread/goal/set" for message in transcript)
        )

    def test_resume_rejects_wrong_thread_goal_runtime_or_terminal_goal(self) -> None:
        objective = "Complete exactly S56-M-0001-INTAKE."
        for mode, message in (
            ("wrong_thread", "wrong thread"),
            ("wrong_goal", "goal identity changed"),
            ("wrong_runtime", "runtime contract mismatch"),
            ("wrong_roots", "runtime contract mismatch"),
            ("wrong_model", "runtime contract mismatch"),
            ("wrong_effort", "runtime contract mismatch"),
            ("wrong_tier", "runtime contract mismatch"),
            ("terminal_goal", "exact active goal"),
        ):
            with self.subTest(mode=mode), self.assertRaisesRegex(
                client.ProtocolError, message
            ):
                self.run_flow(
                    thread_id="thread-1",
                    persisted_objective=objective,
                    resume_mode=mode,
                )

    def test_review_resume_preserves_read_only_runtime(self) -> None:
        objective = "Complete exactly S56-M-0001-INTAKE."
        result, state, transcript = self.run_flow(
            lane=client.REVIEW_LANE,
            thread_id="thread-1",
            persisted_objective=objective,
        )
        self.assertEqual(result, 0)
        resume = next(
            message for message in transcript if message.get("method") == "thread/resume"
        )
        self.assertEqual(resume["params"]["sandbox"], "read-only")
        self.assertEqual(resume["params"]["runtimeWorkspaceRoots"], [])
        self.assertEqual(resume["params"]["config"]["model_reasoning_effort"], "ultra")
        self.assertEqual(resume["params"]["serviceTier"], "priority")
        self.assertTrue(state["resumed"])

    def test_review_lane_is_read_only_and_persists_bound_evidence(self) -> None:
        result, state, transcript = self.run_flow(lane=client.REVIEW_LANE)
        self.assertEqual(result, 0)
        start = next(message for message in transcript if message.get("method") == "thread/start")
        self.assertEqual(start["params"]["sandbox"], "read-only")
        self.assertEqual(start["params"]["runtimeWorkspaceRoots"], [])
        turn = next(message for message in transcript if message.get("method") == "turn/start")
        self.assertEqual(
            turn["params"]["sandboxPolicy"],
            {"type": "readOnly", "networkAccess": False},
        )
        self.assertNotIn("writableRoots", turn["params"]["sandboxPolicy"])
        self.assertEqual(turn["params"]["outputSchema"], client.REVIEW_OUTPUT_JSON_SCHEMA)
        history_request = next(
            message for message in transcript if message.get("method") == "thread/turns/list"
        )
        self.assertEqual(history_request["params"]["itemsView"], "full")
        self.assertEqual(history_request["params"]["sortDirection"], "asc")
        self.assertEqual(history_request["params"]["limit"], 1)

        prompt = "Implement the assigned item.\n"
        objective = "Complete exactly S56-M-0001-INTAKE."
        binding = review_binding(prompt, objective)
        output = review_output(binding)
        output_text = json.dumps(output, sort_keys=True, separators=(",", ":"))
        self.assertEqual(state["lane"], "review")
        self.assertEqual(state["binding"], binding)
        self.assertEqual(
            state["binding_sha256"], sha256_text(client.canonical_json(binding))
        )
        self.assertEqual(state["prompt_sha256"], sha256_text(prompt))
        self.assertEqual(state["objective_sha256"], sha256_text(objective))
        self.assertEqual(
            state["turn_input_sha256"],
            sha256_text(client.canonical_json([{"type": "text", "text": prompt}])),
        )
        self.assertEqual(state["review_output"], output)
        self.assertEqual(state["review_output_text"], output_text)
        self.assertEqual(state["review_output_sha256"], sha256_text(output_text))
        self.assertEqual(
            state["review_output_canonical_sha256"],
            sha256_text(client.canonical_json(output)),
        )
        self.assertEqual(
            state["full_turn_history_sha256"],
            sha256_text(client.canonical_json(state["full_turn_history"])),
        )

    def test_review_lane_rejects_missing_binding_before_starting_server(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            workspace = root / "workspace"
            workspace.mkdir()
            prompt = root / "prompt"
            prompt.write_text("Review.\n", encoding="utf-8")
            objective = root / "objective"
            objective.write_text("Review one item.\n", encoding="utf-8")
            args = argparse.Namespace(
                workspace=workspace,
                prompt=prompt,
                objective=objective,
                status=root / "status",
                log=root / "log",
                codex=str(root / "must-not-run"),
                model="gpt-5.6-sol",
                effort="ultra",
                service_tier="priority",
                lane="review",
                binding=None,
                thread_id=None,
                timeout=5.0,
            )
            with self.assertRaisesRegex(client.ProtocolError, "requires --binding"):
                client.run_worker(args)
            self.assertFalse(args.status.exists())

    def test_review_lane_rejects_stale_binding_before_starting_server(self) -> None:
        with self.assertRaisesRegex(client.ProtocolError, "input digest mismatch"):
            self.run_flow(
                lane=client.REVIEW_LANE,
                binding_mutator=lambda value: value.update(prompt_sha256="0" * 64),
            )

    def test_review_lane_rejects_malformed_histories_and_output(self) -> None:
        for mode, message in (
            ("file_change", "non-read-only item"),
            ("command_execution", "non-read-only item"),
            ("reasoning", "non-read-only item"),
            ("commentary", "commentary or unphased"),
            ("summary", "identity or status mismatch"),
            ("bad_output", "not JSON"),
            ("paginated", "complete turn page"),
            ("backwards_paginated", "complete turn page"),
        ):
            with self.subTest(mode=mode), self.assertRaisesRegex(
                client.ProtocolError, message
            ):
                self.run_flow(lane=client.REVIEW_LANE, history_mode=mode)

    def test_review_lane_rejects_final_answer_before_last_turn(self) -> None:
        with self.assertRaisesRegex(client.ProtocolError, "last turn"):
            self.run_flow(
                lane=client.REVIEW_LANE,
                continue_once=True,
                history_mode="intermediate_final",
            )

    def test_review_lane_rejects_malformed_review_json_contract(self) -> None:
        for name, mutator in (
            ("identity", lambda value: value.update(item_id="S56-M-9999-INTAKE")),
            ("keys", lambda value: value.update(extra="forbidden")),
            (
                "digests",
                lambda value: value.update(reviewed_artifact_sha256s={"wrong": "f" * 64}),
            ),
        ):
            with self.subTest(name=name), self.assertRaises(client.ProtocolError):
                self.run_flow(
                    lane=client.REVIEW_LANE,
                    output_mutator=mutator,
                )

    def test_review_history_rejects_duplicate_final_json_members(self) -> None:
        prompt = "Review exactly one item."
        binding = review_binding(prompt, "objective")
        output = review_output(binding)
        encoded = json.dumps(output, separators=(",", ":"))
        encoded = encoded.replace(
            '"claim_id":"' + str(binding["claim_id"]) + '"',
            '"claim_id":"wrong","claim_id":"' + str(binding["claim_id"]) + '"',
            1,
        )
        history = {
            "data": [
                {
                    "id": "turn-1",
                    "status": "completed",
                    "itemsView": "full",
                    "items": [
                        {"type": "userMessage", "content": [{"type": "text", "text": prompt}]},
                        {"type": "agentMessage", "phase": "final_answer", "text": encoded},
                    ],
                }
            ],
            "nextCursor": None,
            "backwardsCursor": None,
        }
        with self.assertRaisesRegex(client.ProtocolError, "duplicate JSON name"):
            client.require_full_review_history(history, ["turn-1"], prompt, binding)

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


class DurableWriteTests(unittest.TestCase):
    def test_atomic_write_replaces_existing_file_and_leaves_no_temporary(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            target = root / "status.json"
            target.write_text("old", encoding="utf-8")
            client.atomic_write(target, "new\n")
            self.assertEqual(target.read_text(encoding="utf-8"), "new\n")
            self.assertEqual(list(root.glob(".status.json.*.tmp")), [])

    def test_atomic_write_refuses_symlink_destination(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            victim = root / "victim"
            victim.write_text("unchanged", encoding="utf-8")
            target = root / "status.json"
            target.symlink_to(victim)
            with self.assertRaisesRegex(client.ProtocolError, "not a regular file"):
                client.atomic_write(target, "forbidden")
            self.assertEqual(victim.read_text(encoding="utf-8"), "unchanged")

    def test_atomic_write_refuses_symlinked_parent(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            real_parent = root / "real"
            real_parent.mkdir()
            alias_parent = root / "alias"
            alias_parent.symlink_to(real_parent, target_is_directory=True)
            target = alias_parent / "status.json"
            with self.assertRaisesRegex(client.ProtocolError, "missing or unsafe"):
                client.atomic_write(target, "forbidden")
            self.assertFalse((real_parent / "status.json").exists())

    def test_atomic_write_ignores_stale_pid_named_temporary(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            target = root / "status.json"
            stale = root / f".status.json.{os.getpid()}.tmp"
            stale.write_text("stale", encoding="utf-8")
            client.atomic_write(target, "new\n")
            self.assertEqual(target.read_text(encoding="utf-8"), "new\n")
            self.assertEqual(stale.read_text(encoding="utf-8"), "stale")

    def test_review_binding_refuses_symlink(self) -> None:
        prompt = "prompt"
        objective = "objective"
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            real = root / "real.json"
            real.write_text(
                json.dumps(review_binding(prompt, objective)), encoding="utf-8"
            )
            alias = root / "binding.json"
            alias.symlink_to(real)
            with self.assertRaisesRegex(client.ProtocolError, "missing or unsafe"):
                client.require_review_binding(
                    alias, sha256_text(prompt), sha256_text(objective)
                )

    def test_review_binding_refuses_symlinked_parent(self) -> None:
        prompt = "prompt"
        objective = "objective"
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            real_parent = root / "real"
            real_parent.mkdir()
            (real_parent / "binding.json").write_text(
                json.dumps(review_binding(prompt, objective)), encoding="utf-8"
            )
            alias_parent = root / "alias"
            alias_parent.symlink_to(real_parent, target_is_directory=True)
            with self.assertRaisesRegex(client.ProtocolError, "missing or unsafe"):
                client.require_review_binding(
                    alias_parent / "binding.json",
                    sha256_text(prompt),
                    sha256_text(objective),
                )

    def test_regular_text_reader_refuses_prompt_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            real = root / "real.txt"
            real.write_text("prompt", encoding="utf-8")
            alias = root / "prompt.txt"
            alias.symlink_to(real)
            with self.assertRaisesRegex(client.ProtocolError, "worker prompt is missing or unsafe"):
                client.read_regular_text(alias, "worker prompt")

    def test_regular_text_reader_refuses_symlinked_prompt_parent(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            real_parent = root / "real"
            real_parent.mkdir()
            (real_parent / "prompt.txt").write_text("prompt", encoding="utf-8")
            alias_parent = root / "alias"
            alias_parent.symlink_to(real_parent, target_is_directory=True)
            with self.assertRaisesRegex(client.ProtocolError, "worker prompt is missing or unsafe"):
                client.read_regular_text(alias_parent / "prompt.txt", "worker prompt")

    def test_run_worker_refuses_symlinked_status_parent_before_server_start(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            workspace = root / "workspace"
            workspace.mkdir()
            prompt = root / "prompt"
            prompt.write_text("Implement.\n", encoding="utf-8")
            objective = root / "objective"
            objective.write_text("Complete one item.\n", encoding="utf-8")
            real_parent = root / "real-status"
            real_parent.mkdir()
            alias_parent = root / "status-alias"
            alias_parent.symlink_to(real_parent, target_is_directory=True)
            args = argparse.Namespace(
                workspace=workspace,
                prompt=prompt,
                objective=objective,
                status=alias_parent / "status.json",
                log=root / "server.log",
                codex=str(root / "must-not-run"),
                model="gpt-5.6-sol",
                effort="ultra",
                service_tier="priority",
                lane="implementation",
                binding=None,
                thread_id=None,
                timeout=5.0,
            )
            with self.assertRaisesRegex(client.ProtocolError, "status destination.*unsafe"):
                client.run_worker(args)
            self.assertFalse((real_parent / "status.json").exists())

    def test_run_worker_does_not_resolve_status_symlink_before_atomic_write(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            workspace = root / "workspace"
            workspace.mkdir()
            prompt = root / "prompt"
            prompt.write_text("Implement.\n", encoding="utf-8")
            objective = root / "objective"
            objective.write_text("Complete one item.\n", encoding="utf-8")
            victim = root / "victim.json"
            victim.write_text("unchanged", encoding="utf-8")
            status = root / "status.json"
            status.symlink_to(victim)
            args = argparse.Namespace(
                workspace=workspace,
                prompt=prompt,
                objective=objective,
                status=status,
                log=root / "server.log",
                codex=str(root / "must-not-run"),
                model="gpt-5.6-sol",
                effort="ultra",
                service_tier="priority",
                lane="implementation",
                binding=None,
                thread_id=None,
                timeout=5.0,
            )
            with self.assertRaisesRegex(client.ProtocolError, "not a regular file"):
                client.run_worker(args)
            self.assertEqual(victim.read_text(encoding="utf-8"), "unchanged")


if __name__ == "__main__":
    unittest.main()
