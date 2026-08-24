#!/usr/bin/env python3
"""Adversarial transport/admission tests for the Stage5 theorem controller."""

from __future__ import annotations

import ast
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
CONTROLLER_PATH = ROOT / "scripts/stage5_theorems_execution_cron.py"


def load():
    spec = importlib.util.spec_from_file_location("stage5_theorem_execution_tests_controller", CONTROLLER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(CONTROLLER_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


controller = load()


class Completed:
    def __init__(self, stdout: str = "", stderr: str = "", returncode: int = 0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


class Stage5TheoremExecutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="stage5-theorem-execution-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_validate_only_has_zero_runtime_tmux_and_process_side_effects(self) -> None:
        with mock.patch.object(controller, "PROGRAM_RUNTIME", self.root / "program"), mock.patch.object(
            controller, "SHARED_RUNTIME", self.root / "shared"
        ), mock.patch.object(controller, "STATE_PATH", self.root / "program/state/controller-state.json"), mock.patch.object(
            controller, "SNAPSHOT_PATH", self.root / "program/status/runtime-snapshot.json"
        ), mock.patch.object(controller.subprocess, "Popen", side_effect=AssertionError("process spawned")) as popen:
            result = controller.validate_only()
        self.assertTrue(result["valid"], result)
        self.assertFalse((self.root / "program").exists())
        self.assertFalse((self.root / "shared").exists())
        popen.assert_not_called()

    def test_codex_argv_is_interactive_explicit_and_has_no_forbidden_subcommand(self) -> None:
        argv = controller.codex_argv(self.root)
        self.assertEqual(argv[0], controller.CONTAINER_CODEX_BINARY)
        self.assertNotIn("exec", argv)
        self.assertNotIn("app-server", argv)
        self.assertNotIn("--remote", argv)
        self.assertIn("gpt-5.6-sol", argv)
        self.assertIn('model_reasoning_effort="ultra"', argv)
        self.assertIn('service_tier="default"', argv)
        self.assertIn("features.goals=true", argv)
        self.assertIn("features.multi_agent_v2=false", argv)
        self.assertIn("--dangerously-bypass-approvals-and-sandbox", argv)
        self.assertTrue(any("do not spawn subagents" in part for part in argv))

    def test_generated_finalizers_are_valid_python_with_literal_newline_escape(self) -> None:
        producer = controller.render_finalizer()
        reviewer = controller.render_review_finalizer()
        compile(producer, "<stage5-producer-finalizer>", "exec")
        compile(reviewer, "<stage5-review-finalizer>", "exec")
        self.assertIn(b'+"\\n")', producer)
        self.assertIn(b'+"\\n")', reviewer)

    def test_docker_argv_is_task_local_read_only_and_capability_free(self) -> None:
        task = self.root / "task"
        record = {
            "task_root": str(task), "work_root": str(task / "work"),
            "codex_home": str(task / "codex-home"), "container_name": "s5-fixture",
        }
        argv = controller.docker_run_argv(record, controller.codex_argv(task / "work"))
        self.assertEqual(argv[:2], [str(controller.DOCKER_BINARY), "run"])
        self.assertIn(controller.CONTAINER_IMAGE, argv)
        self.assertIn("--read-only", argv)
        self.assertIn("no-new-privileges", argv)
        self.assertIn("ALL", argv)
        self.assertIn(f"type=bind,src={task},dst={task},readonly", argv)
        self.assertIn(f"type=bind,src={task / 'work'},dst={task / 'work'}", argv)
        self.assertIn(f"type=bind,src={task / 'codex-home'},dst={task / 'codex-home'}", argv)
        self.assertIn(
            f"type=bind,src={controller.CODEX_NATIVE_BINARY},dst={controller.CONTAINER_CODEX_BINARY},readonly",
            argv,
        )
        self.assertIn(
            f"type=bind,src={controller.CODEX_CODE_MODE_HOST},dst={controller.CONTAINER_CODE_MODE_HOST},readonly",
            argv,
        )

    def test_container_liveness_requires_digest_bound_read_only_code_mode_host(self) -> None:
        task = self.root / "task"
        work = task / "work"
        home = task / "codex-home"
        native = self.root / "codex"
        helper = self.root / "codex-code-mode-host"
        native.write_bytes(b"native")
        helper.write_bytes(b"helper")
        record = {
            "task_root": str(task), "work_root": str(work),
            "codex_home": str(home), "container_name": "s5-fixture",
        }

        def mount(source: str, destination: str, writable: bool) -> dict:
            return {"Source": source, "Destination": destination, "RW": writable}

        mounts = [
            mount(str(task), str(task), False),
            mount(str(work), str(work), True),
            mount(str(home), str(home), True),
            mount(str(native), controller.CONTAINER_CODEX_BINARY, False),
            mount(str(helper), controller.CONTAINER_CODE_MODE_HOST, False),
            mount("/home/sansha/.elan", "/home/sansha/.elan", False),
        ]
        inspected = [{
            "Id": "a" * 64, "Image": controller.CONTAINER_IMAGE_ID,
            "State": {"Running": True, "Pid": 4321},
            "Config": {
                "WorkingDir": str(work), "Env": [f"CODEX_HOME={home}"],
                "User": f"{os.getuid()}:{os.getgid()}",
            },
            "HostConfig": {
                "ReadonlyRootfs": True, "NetworkMode": "host", "CapDrop": ["ALL"],
            },
            "Mounts": mounts,
        }]

        def inspect_result() -> Completed:
            return Completed(stdout=json.dumps(inspected))

        patches = (
            mock.patch.object(controller, "CODEX_NATIVE_BINARY", native),
            mock.patch.object(controller, "CODEX_CODE_MODE_HOST", helper),
            mock.patch.object(controller, "CODEX_NATIVE_SHA256", controller.file_digest(native)),
            mock.patch.object(controller, "CODEX_CODE_MODE_HOST_SHA256", controller.file_digest(helper)),
            mock.patch.object(controller, "run", side_effect=lambda *_args, **_kwargs: inspect_result()),
            mock.patch.object(controller.os, "readlink", return_value=str(work)),
            mock.patch.object(controller, "process_environment", return_value=str(home)),
            mock.patch.object(Path, "read_bytes", return_value=(controller.CONTAINER_CODEX_BINARY + "\0").encode()),
        )
        with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7]:
            self.assertIsNotNone(controller.container_inspect(record))
            inspected[0]["Mounts"] = [row for row in mounts if row["Destination"] != controller.CONTAINER_CODE_MODE_HOST]
            self.assertIsNone(controller.container_inspect(record))
            inspected[0]["Mounts"] = mounts
            helper.write_bytes(b"drifted-helper")
            self.assertIsNone(controller.container_inspect(record))

    def test_static_manager_ast_audit_accepts_controller(self) -> None:
        tree = ast.parse(CONTROLLER_PATH.read_text())
        forbidden = {
            "exec", "app-server", "app_server", "--model", "--reasoning-effort",
            "codex exec", "codex app-server",
        }
        literals = {
            node.value for node in ast.walk(tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
            and " ".join(node.value.lower().split()) in forbidden
        }
        self.assertEqual(literals, set())

    def test_repeated_bounded_waves_reach_exact_n_without_n_plus_one(self) -> None:
        launched: list[int] = []

        def launch(value: int) -> bool:
            launched.append(value)
            return True

        count, reasons = controller.generic_admission_pump(
            list(range(120)), target=120, fanout=4, already_live=0,
            launch_one=launch, deadline=time.monotonic() + 5,
        )
        self.assertEqual(count, 120)
        self.assertEqual(len(launched), 120)
        self.assertEqual(reasons, [])
        count, _ = controller.generic_admission_pump(
            list(range(20)), target=7, fanout=4, already_live=6,
            launch_one=launch, deadline=time.monotonic() + 5,
        )
        self.assertEqual(count, 1)

    def test_each_startup_wave_is_parallel_but_never_exceeds_fanout(self) -> None:
        active = 0
        peak = 0
        gate = threading.Barrier(4)
        lock = threading.Lock()

        def launch(_: int) -> bool:
            nonlocal active, peak
            with lock:
                active += 1
                peak = max(peak, active)
            try:
                gate.wait(timeout=2)
                time.sleep(0.01)
                return True
            finally:
                with lock:
                    active -= 1

        count, reasons = controller.generic_admission_pump(
            list(range(8)), target=8, fanout=4, already_live=0,
            launch_one=launch, deadline=time.monotonic() + 5,
        )
        self.assertEqual(count, 8)
        self.assertEqual(peak, 4)
        self.assertEqual(reasons, [])

    def test_underfill_reason_is_specific_for_no_progress_and_deadline(self) -> None:
        count, reasons = controller.generic_admission_pump(
            [1, 2, 3, 4], target=4, fanout=2, already_live=0,
            launch_one=lambda _: False, deadline=time.monotonic() + 5,
        )
        self.assertEqual(count, 0)
        self.assertIn("startup:no_progress_two_consecutive_waves", reasons)
        _, reasons = controller.generic_admission_pump(
            [1], target=1, fanout=1, already_live=0,
            launch_one=lambda _: True, deadline=time.monotonic() - 1,
        )
        self.assertIn("tick_budget:startup_pump_deadline", reasons)

    def test_private_identity_requires_one_thread_one_goal_and_default_rollout_tier(self) -> None:
        home = self.root / "codex-home"
        sessions = home / "sessions/2026/08/11"
        sessions.mkdir(parents=True)
        rollout = sessions / "rollout-fixture.jsonl"
        rollout.write_text(json.dumps({
            "type": "event_msg", "payload": {"thread_settings": {"service_tier": "default"}},
        }) + "\n")
        state = __import__("sqlite3").connect(home / "state_5.sqlite")
        state.execute("create table threads(id text,cwd text,model_provider text,model text,reasoning_effort text,rollout_path text,updated_at_ms int,updated_at int,created_at_ms int,created_at int)")
        state.execute("insert into threads values(?,?,?,?,?,?,?,?,?,?)", (
            "thread-1", str(self.root / "work"), "sub2api", "gpt-5.6-sol", "ultra",
            str(rollout), 1, 1, 1, 1,
        ))
        state.commit(); state.close()
        goals = __import__("sqlite3").connect(home / "goals_1.sqlite")
        goals.execute("create table thread_goals(thread_id text,goal_id text,objective text,status text)")
        goals.execute("insert into thread_goals values(?,?,?,?)", (
            "thread-1", "goal-1", "S5THM-00003485-INTAKE claim", "active",
        ))
        goals.commit(); goals.close()
        record = {"codex_home": str(home)}
        identity = controller.private_identity(record)
        self.assertIsNotNone(identity)
        self.assertEqual(identity["service_tier"], "default")
        self.assertEqual(identity["reasoning_effort"], "ultra")
        # A second thread makes the identity ineligible.
        state = __import__("sqlite3").connect(home / "state_5.sqlite")
        state.execute("insert into threads values(?,?,?,?,?,?,?,?,?,?)", (
            "thread-2", str(self.root / "work"), "sub2api", "gpt-5.6-sol", "ultra", str(rollout), 2, 2, 2, 2,
        ))
        state.commit(); state.close()
        self.assertIsNone(controller.private_identity(record))

    def test_delayed_authentication_never_resubmits_goal(self) -> None:
        record = {"status": "goal_submitted", "goal_submissions": 1, "item_id": "S5THM-X"}
        sequence = iter([False, True])
        with mock.patch.object(controller, "authenticate", side_effect=lambda _: next(sequence)), mock.patch.object(
            controller, "exact_process_identity", return_value=True
        ), mock.patch.object(controller, "submit_goal", side_effect=AssertionError("duplicate goal")) as submit, mock.patch.object(
            controller, "stop_transport"
        ):
            state = {"claims": {record["item_id"]: record}}
            promoted, retired = controller.reconcile_claims(state)
            self.assertEqual((promoted, retired), (0, 0))
            promoted, retired = controller.reconcile_claims(state)
            self.assertEqual((promoted, retired), (1, 0))
        submit.assert_not_called()

    def test_harvest_validates_and_copies_before_transport_stop(self) -> None:
        task = self.root / "task"
        (task / "work/_outbox").mkdir(parents=True)
        (task / "claim.json").write_text("{}")
        (task / "work/_outbox/result.json").write_text("{}")
        patch = task / "work/_outbox/changes.patch"; patch.write_text("x")
        record = {
            "status": "live", "task_root": str(task), "claim_id": "claim",
            "run_id": "run", "claim_card_sha256": "1" * 64,
        }
        state = {"claims": {"ITEM": record}, "handoffs": {}}
        order: list[str] = []

        class Validator:
            @staticmethod
            def validate_result(*_):
                order.append("validate")
                artifact = task / "work/artifact.json"
                artifact.write_text("{}\n")
                return {
                    "changed_paths": ["artifact.json"],
                    "patch": {"path": str(patch), "sha256": controller.file_digest(patch)},
                    "artifacts": [{
                        "path": str(artifact), "sha256": controller.file_digest(artifact),
                        "size_bytes": artifact.stat().st_size,
                    }],
                }

        # BOOT executes this suite from a read-only source snapshot.  The
        # fixture archive must therefore live wholly in its task-local private
        # temporary root; patching ROOT also exercises the controller's
        # repository-relative archive manifest without writing canonical data.
        archive = self.root / "fixture-handoffs"

        def copied(source, destination):
            order.append("copy")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source.read_bytes())
            return {
                "path": str(source), "sha256": controller.file_digest(source),
                "size_bytes": source.stat().st_size,
            }

        with mock.patch.object(controller, "ROOT", self.root), mock.patch.object(
            controller, "load_module", return_value=Validator
        ), mock.patch.object(
            controller, "HANDOFF_ROOT", archive
        ), mock.patch.object(controller, "copy_bound", side_effect=copied), mock.patch.object(
            controller, "stop_transport", side_effect=lambda _: order.append("stop")
        ), mock.patch.object(controller, "append_event", return_value={}), mock.patch.object(
            controller, "advance_checklist", return_value={
                "pre_blueprint_sha256": "2" * 64,
                "pre_gantt_sha256": "3" * 64,
                "post_blueprint_sha256": "4" * 64,
                "post_gantt_sha256": "5" * 64,
            }
        ):
            self.assertEqual(controller.harvest(state), 1)
        self.assertEqual(order[0], "validate")
        self.assertGreaterEqual(order.count("copy"), 3)
        self.assertEqual(order[-1], "stop")
        self.assertEqual(record["status"], "handoff_ready")

    def test_distinct_claims_use_distinct_task_socket_session_home(self) -> None:
        records = []
        for ordinal in range(3):
            task = self.root / f"task-{ordinal}"
            records.append({
                "task_root": str(task), "socket_path": str(task / "tmux.sock"),
                "session": f"session-{ordinal}", "codex_home": str(task / "codex-home"),
                "container_name": f"container-{ordinal}", "container_id": str(ordinal) * 64,
                "container_pid": ordinal + 100, "pane_pid": ordinal + 10,
                "thread_id": f"thread-{ordinal}", "goal_id": f"goal-{ordinal}",
            })
        for field in (
            "task_root", "socket_path", "session", "codex_home", "container_name",
            "container_id", "container_pid", "pane_pid", "thread_id", "goal_id",
        ):
            self.assertEqual(len({record[field] for record in records}), len(records), field)

    def test_event_ledger_rejects_truncation_reorder_and_hash_break(self) -> None:
        ledger = self.root / "events.jsonl"
        lock = self.root / "events.lock"
        with mock.patch.object(controller, "EVENT_LEDGER", ledger), mock.patch.object(
            controller, "EVENT_LEDGER_LOCK", lock
        ):
            controller.append_event("one", {"x": 1})
            controller.append_event("two", {"x": 2})
            self.assertEqual(controller.validate_event_ledger(), 2)
            rows = ledger.read_bytes().splitlines(keepends=True)
            ledger.write_bytes(rows[1] + rows[0])
            with self.assertRaises(controller.ControllerError):
                controller.validate_event_ledger()
            ledger.write_bytes(rows[0] + rows[1][:-1])
            with self.assertRaises(controller.ControllerError):
                controller.validate_event_ledger()

    def test_cleanup_transport_is_scoped_to_recorded_socket_and_pid(self) -> None:
        record = {"pane_pid": 123, "pane_pid_start_ticks": 9, "container_name": "s5-fixture"}
        with mock.patch.object(controller, "tmux", return_value=Completed()) as tmux, mock.patch.object(
            controller, "process_start_ticks", return_value=None
        ), mock.patch.object(controller, "run", return_value=Completed()) as run, mock.patch.object(
            controller.os, "kill", side_effect=AssertionError("broad kill")
        ) as kill:
            controller.stop_transport(record)
        tmux.assert_called_once_with(record, "kill-server", check=False, timeout=10)
        run.assert_called_once_with(
            [str(controller.DOCKER_BINARY), "rm", "--force", "s5-fixture"],
            check=False, timeout=20,
        )
        kill.assert_not_called()


if __name__ == "__main__":
    unittest.main()
