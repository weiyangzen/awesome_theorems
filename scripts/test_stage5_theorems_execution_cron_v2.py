#!/usr/bin/env python3
"""Focused conformance tests for the v2 tmux-only theorem launcher."""
from __future__ import annotations

import ast
import importlib.util
import json
import sqlite3
import hashlib
import subprocess
from contextlib import AbstractContextManager, ExitStack
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts/stage5_theorems_execution_cron_v2.py"
SUCCESSOR_TOOL_PATH = ROOT / "scripts/accept_stage5_theorem_controller_successor.py"


def load():
    spec = importlib.util.spec_from_file_location("stage5_theorem_v2_controller_test", PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


controller = load()


def load_successor_tool():
    spec = importlib.util.spec_from_file_location(
        "stage5_theorem_successor_tool_test", SUCCESSOR_TOOL_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(SUCCESSOR_TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sealed_prompt(specification, concurrency=None, **overrides):
    vector = concurrency or {
        "logical_claims": 24,
        "service_records": "not_applicable",
        "agent_executions": 24,
        "startup_reservations": 24,
        "launch_fanout_per_wave": 4,
        "live_transports": 24,
        "authenticated_goals": 24,
        "running_turns": 24,
        "outbound_request_starts_per_window": 24,
        "in_flight_requests": 24,
        "integration": 1,
        "validators": 4,
        "exact_path_conflicts": 0,
    }
    body = {
        "schema_version": controller.CONCURRENCY_SCHEMA,
        "program": controller.PROGRAM,
        "policy_epoch": "stage5-concurrency-prompt-2026-08-14-balanced-4",
        "execution_spec_sha256": controller.digest(controller.canonical(specification)),
        "operator_identity": f"codex-user-goal:{controller.GOAL_THREAD_ID}",
        "operator_goal_thread_id": controller.GOAL_THREAD_ID,
        "operator_goal_objective_sha256": controller.GOAL_OBJECTIVE_SHA256,
        "request_window_seconds": 120,
        "concurrency": vector,
        "source": "explicit operator prompt test fixture",
        "execution_limits": {"generation_lifetime_seconds":1209600,"model_input_tokens":2000000,"model_output_tokens":500000,"model_turns":"unbounded","cpu_seconds":1209600,"external_launches":4},
        "recovery": {"startup_attempts_per_generation":1,"provider_attempts_per_request":60,"repair_attempts_per_failure_identity":3,"generation_replacements_per_work_item":60,"backoff_initial_seconds":60,"backoff_max_seconds":3600,"backoff_multiplier":2,"backoff_jitter_ratio":0.2,"retry_after_precedence":"provider_retry_after_then_exponential","breaker_failure_classes":["http_429","http_503","provider_unavailable"],"breaker_scope":"provider","breaker_failure_threshold":3,"breaker_cooldown_seconds":1800},
        **overrides,
    }
    return {**body, "authority_sha256": controller.digest(controller.canonical(body))}


class V2ControllerTests(unittest.TestCase):
    @staticmethod
    def budget_binding(*, generations=10):
        maxima = {
            "model_input_tokens": 100, "model_output_tokens": 50,
            "model_turns": "unbounded", "external_launches": 4,
            "wall_seconds": 1000, "cpu_seconds": 1000,
            "generation_lifetime_seconds": 1000,
            "generation_replacements_per_work_item": 60,
        }
        effective = {
            key: generations * maxima[key] for key in controller.BUDGET_DIMENSIONS
        }
        return {
            "authority": {"per_claim_maxima": maxima},
            "renewal": {"authority_sha256": "r" * 64},
            "effective_allowances": effective,
            "authority_chain_sha256": "a" * 64,
            "goal": {},
        }

    def test_budget_legacy_import_is_conservative_and_hash_chained(self):
        with tempfile.TemporaryDirectory(prefix="stage5-budget-ledger-") as temporary:
            original = controller.BUDGET_LEDGER
            controller.BUDGET_LEDGER = Path(temporary) / "operator-budget.jsonl"
            state = {
                "reservations": [
                    {"generation_id":"g1"}, {"generation_id":"g2"},
                    {"generation_id":"g2"},
                ],
            }
            try:
                accounting = controller.ensure_budget_accounting(
                    state, self.budget_binding(),
                )
                self.assertEqual(accounting["reservation_count"], 2)
                self.assertEqual(accounting["reserved_totals"], {
                    "model_input_tokens": 200, "model_output_tokens": 100,
                    "external_launches": 8, "wall_seconds": 2000,
                    "cpu_seconds": 2000,
                })
                rows = controller._read_budget_ledger()
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]["kind"], "legacy_import")
                self.assertEqual(
                    accounting["ledger_head_sha256"],
                    controller.digest(controller._budget_record_raw(rows[0])[:-1]),
                )
            finally:
                controller.BUDGET_LEDGER = original

    def test_budget_reservation_fails_before_overcommit(self):
        with tempfile.TemporaryDirectory(prefix="stage5-budget-cap-") as temporary:
            original = controller.BUDGET_LEDGER
            controller.BUDGET_LEDGER = Path(temporary) / "operator-budget.jsonl"
            binding = self.budget_binding(generations=1)
            state = {"reservations": []}
            first = {
                "item_id":"A", "claim_id":"A--worker", "generation_id":"g1",
                "lane_id":"A", "prompt_digest":"p" * 64,
            }
            second = {**first, "item_id":"B", "claim_id":"B--worker", "generation_id":"g2", "lane_id":"B"}
            try:
                controller.ensure_budget_accounting(state, binding)
                controller.reserve_generation_budget(state, first, binding)
                with self.assertRaisesRegex(controller.ControllerError, "insufficient"):
                    controller.reserve_generation_budget(state, second, binding)
                self.assertEqual(len(controller._read_budget_ledger()), 2)
            finally:
                controller.BUDGET_LEDGER = original

    def test_budget_write_ahead_reservation_recovers_without_refund(self):
        with tempfile.TemporaryDirectory(prefix="stage5-budget-wal-") as temporary:
            original = controller.BUDGET_LEDGER
            controller.BUDGET_LEDGER = Path(temporary) / "operator-budget.jsonl"
            binding = self.budget_binding(generations=3)
            state = {"reservations": []}
            try:
                controller.ensure_budget_accounting(state, binding)
                stale = json.loads(json.dumps(state))
                record = {
                    "item_id":"A", "claim_id":"A--worker", "generation_id":"g1",
                    "lane_id":"A", "prompt_digest":"p" * 64,
                }
                controller.reserve_generation_budget(state, record, binding)
                recovered = controller.ensure_budget_accounting(stale, binding)
                self.assertEqual(recovered["reservation_count"], 1)
                self.assertEqual(recovered["reserved_totals"]["external_launches"], 4)
                self.assertEqual(recovered["ledger_seq"], 2)
            finally:
                controller.BUDGET_LEDGER = original

    def test_generation_budget_violation_uses_billable_uncached_tokens(self):
        record = {
            "execution_limits": {
                "model_input_tokens": 100, "model_output_tokens": 50,
                "external_launches": 4, "generation_lifetime_seconds": 1000,
            },
        }
        with mock.patch.object(controller, "measured_generation_usage", return_value={
            "goal_registry":{"time_used_seconds":10},
            "rollout_tokens":{"billable_input_tokens":101,"output_tokens":5},
            "external_launches":1,
        }):
            self.assertEqual(
                controller.generation_budget_violation(record),
                "model_input_token_budget_exceeded",
            )

    def test_rollout_usage_skips_null_token_info(self):
        with tempfile.TemporaryDirectory(prefix="stage5-budget-null-token-") as temporary:
            home = Path(temporary)
            sessions = home / "sessions/2026/08/17"
            sessions.mkdir(parents=True)
            events = [
                {"type":"event_msg", "payload":{"type":"token_count", "info":None}},
                {
                    "type":"event_msg",
                    "payload":{
                        "type":"token_count",
                        "info":{"total_token_usage":{
                            "input_tokens":17, "cached_input_tokens":7,
                            "output_tokens":3, "reasoning_output_tokens":2,
                        }},
                    },
                },
            ]
            (sessions / "rollout-test.jsonl").write_text(
                "\n".join(json.dumps(event) for event in events) + "\n",
            )
            self.assertEqual(
                controller._rollout_token_usage({"codex_home":str(home)}),
                {
                    "input_tokens":17, "cached_input_tokens":7,
                    "output_tokens":3, "reasoning_output_tokens":2,
                    "billable_input_tokens":10,
                },
            )

    def test_master_integration_runs_outside_scheduler_and_reconciles(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-master-phase-") as temporary:
            root = Path(temporary)
            queue = root / "integration"
            queue.mkdir()
            (queue / "A.json").write_text("{}")
            state = {"claims": {}}
            lock_held = False

            class Guard(AbstractContextManager):
                def __enter__(self):
                    nonlocal lock_held
                    self.assertion = not lock_held
                    lock_held = True
                    return self

                def __exit__(self, *args):
                    nonlocal lock_held
                    lock_held = False

            def integrate(limit):
                self.assertFalse(lock_held)
                self.assertEqual(limit, 1)
                return [{"item_id": "A"}]

            original_queue = controller.INTEGRATION_QUEUE
            controller.INTEGRATION_QUEUE = queue
            try:
                with (
                    mock.patch.object(controller, "scheduler_guard", side_effect=lambda *args, **kwargs: Guard()),
                    mock.patch.object(controller, "load_state", return_value=state),
                    mock.patch.object(controller, "save_state"),
                    mock.patch.object(controller, "_repair_still_blocking", return_value=False),
                    mock.patch.object(controller, "integrate_ready_handoffs", side_effect=integrate),
                    mock.patch.object(controller, "reconcile_integrated_handoffs") as reconcile,
                ):
                    result = controller.run_bounded_master_integration(1, {})
                self.assertEqual(result, [{"item_id": "A"}])
                self.assertEqual(state["active_integrations"], 0)
                self.assertEqual(state["integrations"], [{"item_id": "A"}])
                reconcile.assert_called_once_with(state, {})
            finally:
                controller.INTEGRATION_QUEUE = original_queue

    def test_superseded_internal_type_error_does_not_pin_integration_queue(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-repair-retry-") as temporary:
            root = Path(temporary)
            original_runtime = controller.RUNTIME
            controller.RUNTIME = root
            entry = root / "integration/A.json"
            repair = root / "repair/A.json.repair.json"
            entry.parent.mkdir(); repair.parent.mkdir()
            entry.write_text("{}")
            body = {
                "schema_version":"fixture", "reason":"unhashable type: 'list'",
            }
            repair.write_text(json.dumps(controller.seal(body)))
            try:
                self.assertFalse(controller._repair_still_blocking(entry))
            finally:
                controller.RUNTIME = original_runtime

    def test_master_phase_precedes_provider_breaker_early_return(self):
        source = PATH.read_text(encoding="utf-8")
        pump = source.split("def _launch_workers_pump", 1)[1]
        self.assertLess(
            pump.index("run_bounded_master_integration"),
            pump.index("if breaker_open:"),
        )

    def test_maintenance_mode_cannot_harvest_or_integrate(self):
        vector = sealed_prompt({})["concurrency"]
        prompt = sealed_prompt({}, concurrency=vector)
        state = {"claims": {}, "breaker": {"state": "open"}}
        guard = mock.MagicMock(__enter__=lambda value: value, __exit__=lambda *args: None)
        specification = {"scheduler": {"tick_budget_seconds": 5, "startup_deadline_seconds": 5}}
        intent = {"payload": {"action": "paused_reconcile_fence_and_refill_only"}}
        with ExitStack() as stack:
            stack.enter_context(mock.patch.object(controller, "load_program", return_value=(specification, [{"state":"x"}], b"bp")))
            stack.enter_context(mock.patch.object(controller, "load_concurrency_prompt", return_value=(prompt, "p" * 64)))
            stack.enter_context(mock.patch.object(controller, "validate_claim_schema_prompt_identity"))
            stack.enter_context(mock.patch.object(controller, "validate_operator_authority", return_value={}))
            stack.enter_context(mock.patch.object(controller, "semantic_revoked_master_acceptances", return_value={}))
            stack.enter_context(mock.patch.object(controller, "ensure_budget_accounting", return_value={}))
            stack.enter_context(mock.patch.object(controller, "validate_concurrency_vector", return_value=vector))
            stack.enter_context(mock.patch.object(controller, "validate_execution_policy", return_value=(prompt["execution_limits"], prompt["recovery"])))
            stack.enter_context(mock.patch.object(controller, "materialize_runtime_authority"))
            stack.enter_context(mock.patch.object(controller, "scheduler_guard", return_value=guard))
            stack.enter_context(mock.patch.object(controller, "load_state", return_value=state))
            stack.enter_context(mock.patch.object(controller, "provider_breaker_is_open", return_value=True))
            stack.enter_context(mock.patch.object(controller, "rebuild_provider_retry_schedule", return_value=0))
            harvest = stack.enter_context(mock.patch.object(controller, "harvest_state"))
            stack.enter_context(mock.patch.object(controller, "fence_orphaned_generations", return_value=0))
            stack.enter_context(mock.patch.object(controller, "update_provider_breaker_from_records"))
            stack.enter_context(mock.patch.object(controller, "gate_pre_submission_generations_for_breaker"))
            stack.enter_context(mock.patch.object(controller, "refresh_half_open_probe_set"))
            stack.enter_context(mock.patch.object(controller, "save_state"))
            integrate = stack.enter_context(mock.patch.object(controller, "run_bounded_master_integration"))
            stack.enter_context(mock.patch.object(controller, "concurrency_usage", return_value={key:0 for key in controller.CONCURRENCY_DIMENSIONS if key != "service_records"} | {"service_records":"not_applicable"}))
            stack.enter_context(mock.patch.object(controller, "append_runtime_snapshot"))
            result = controller._launch_workers_pump(
                controller.CONCURRENCY_PROMPT, maintenance_intent=intent,
            )
        harvest.assert_not_called()
        integrate.assert_not_called()
        self.assertEqual(result["harvested"], 0)
        self.assertEqual(result["integrated"], 0)

    def test_master_acceptance_fences_live_replacement_without_regressing_work(self):
        state = {"claims": {"A": {
            "item_id":"A", "claim_id":"A--worker", "run_id":"g2",
            "generation_id":"g2", "lane_id":"A", "status":"live",
        }}}
        with mock.patch.object(controller, "append_event"), mock.patch.object(controller, "save_state"):
            retiring = controller.retire_generations_for_master_accepted_items(state, {"A"})
        self.assertEqual(len(retiring), 1)
        self.assertEqual(state["claims"]["A"]["status"], "generation_retire_required")

        with (
            mock.patch.object(controller, "scheduler_guard", return_value=mock.MagicMock(__enter__=lambda s: s, __exit__=lambda *a: None)),
            mock.patch.object(controller, "load_state", return_value=state),
            mock.patch.object(controller, "stop_record"),
            mock.patch.object(controller, "append_event"),
            mock.patch.object(controller, "save_state"),
        ):
            controller.finalize_master_accepted_retirement(retiring[0])
        self.assertEqual(state["claims"]["A"]["status"], "master_accepted")
        self.assertEqual(state["generation_history"][-1]["generation_status"], "retired")

    def test_unaccepted_conflicting_handoff_is_never_auto_superseded(self):
        source = PATH.read_text(encoding="utf-8")
        self.assertIn("item_id not in blueprint_accepted", source)
        self.assertIn("master_acceptance_sha256", source)
        self.assertIn("superseded-handoff.json", source)

    def test_pump_reloads_blueprint_after_master_phase_before_admission(self):
        source = PATH.read_text(encoding="utf-8")
        pump = source.split("def _launch_workers_pump", 1)[1]
        master = pump.index("run_bounded_master_integration")
        reload = pump.index("specification, rows, raw = load_program()", master)
        breaker = pump.index("if breaker_open:", master)
        self.assertLess(master, reload)
        self.assertLess(reload, breaker)

    def test_live_lane_audit_seals_exact_identity_and_policy_checks(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-live-audit-") as temporary:
            original_runtime = controller.RUNTIME
            controller.RUNTIME = Path(temporary) / "runtime"
            task = controller.RUNTIME / "tasks/A--worker/g0"
            work, home = task / "work", task / "codex-home"
            work.mkdir(parents=True); home.mkdir()
            record = {
                "item_id":"A", "claim_id":"A--worker", "status":"live",
                "run_id":"g0", "generation_id":"g0", "lane_id":"A",
                "task_root":str(task), "work_root":str(work), "codex_home":str(home),
                "socket_path":str(task / "tmux.sock"), "session":"s0",
                "pane_pid":123, "pane_pid_start_ticks":456,
                "thread_id":"t0", "goal_id":"goal0", "goal_submissions":1,
                "generation_started_at":1000.0, "generation_deadline_epoch":1210600.0,
                "replacement_ordinal":0, "recovery":{"generation_replacements_per_work_item":60},
                "provider":controller.PROVIDER, "model":controller.MODEL,
                "reasoning_effort":controller.EFFORT, "service_tier":controller.SERVICE_TIER,
            }
            prompt = sealed_prompt({})
            identity = {"thread_id":"t0", "goal_id":"goal0", "goal_status":"active", "cwd":str(work)}
            try:
                with (
                    mock.patch.object(Path, "is_socket", return_value=True),
                    mock.patch.object(controller, "process_ticks", return_value=456),
                    mock.patch.object(controller, "process_env", return_value=str(home)),
                    mock.patch.object(Path, "resolve", return_value=work),
                    mock.patch.object(controller, "private_registry_cardinality", return_value=(1, 1)),
                    mock.patch.object(controller, "private_identity", return_value=identity),
                ):
                    audit = controller.build_live_lane_audit({"claims":{"A":record}}, prompt, "d" * 64)
                self.assertTrue(audit["all_checks_pass"], audit)
                self.assertEqual(audit["observed_live"], 1)
                self.assertIs(controller.verify_seal(audit, "fixture live audit"), audit)
            finally:
                controller.RUNTIME = original_runtime

    def test_private_identity_requires_exactly_one_thread_and_goal(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-private-cardinality-") as temporary:
            home = Path(temporary)
            state = sqlite3.connect(home / "state_5.sqlite")
            state.execute("create table threads(id text,cwd text,model_provider text,model text,reasoning_effort text)")
            state.executemany("insert into threads values(?,?,?,?,?)", [
                ("t1","/work","sub2api","gpt-5.6-sol","ultra"),
                ("t2","/work","sub2api","gpt-5.6-sol","ultra"),
            ]); state.commit(); state.close()
            goals = sqlite3.connect(home / "goals_1.sqlite")
            goals.execute("create table thread_goals(thread_id text,goal_id text,objective text,status text)")
            goals.execute("insert into thread_goals values('t1','g1','fixture','active')")
            goals.commit(); goals.close()
            record = {"codex_home":str(home), "status":"live", "item_id":"A", "claim_id":"A--worker", "run_id":"r1"}
            self.assertIsNone(controller.private_identity(record))
            self.assertEqual(controller.private_registry_cardinality(record), (2, 1))
            with mock.patch.object(controller, "task_boundary_violation", return_value=None), mock.patch.object(controller, "append_event"):
                self.assertEqual(controller.reconcile_record(record), "generation_retire_required")
            self.assertEqual(record["terminal_reason"], "private_registry_cardinality_violation")

    def test_registry_cardinality_is_boundary_disposition(self):
        record = {
            "terminal_reason": "private_registry_cardinality_violation",
            "retired_reason": "private_registry_cardinality:threads=3:goals=1",
        }
        self.assertEqual(
            controller._terminal_disposition_kind(record, RuntimeError("child thread")),
            "boundary_invalid",
        )

    def test_codex_argv_disables_nested_agent_surfaces(self):
        argv = controller.codex_argv(Path("/tmp/task-local-work"))
        self.assertIn("-c", argv)
        for flag in (
            "features.multi_agent=false",
            "features.multi_agent_v2=false",
            "features.plugins=false",
            "features.remote_plugin=false",
            "features.recommended_plugins=false",
        ):
            self.assertIn(flag, argv)
        thread_cap = "features.multi_agent_v2.max_concurrent_threads_per_session=1"
        mode_hint = (
            "features.multi_agent_v2.multi_agent_mode_hint_text="
            + json.dumps(controller.MULTI_AGENT_MODE_HINT)
        )
        task_boundary = (
            "developer_instructions="
            + json.dumps(controller.TASK_LOCAL_DEVELOPER_INSTRUCTIONS)
        )
        self.assertEqual(argv.count(thread_cap), 1)
        self.assertEqual(argv.count(mode_hint), 1)
        self.assertEqual(argv.count(task_boundary), 1)
        self.assertIn("controller admission as a separate claim", controller.MULTI_AGENT_MODE_HINT)
        self.assertIn("Do not spawn child threads", controller.MULTI_AGENT_MODE_HINT)
        self.assertIn("`../claim.json`", controller.TASK_LOCAL_DEVELOPER_INSTRUCTIONS)
        self.assertIn("`../changes.patch`", controller.TASK_LOCAL_DEVELOPER_INSTRUCTIONS)
        self.assertIn("`rg --files .`", controller.TASK_LOCAL_DEVELOPER_INSTRUCTIONS)
        self.assertIn("Never run `git -C`", controller.TASK_LOCAL_DEVELOPER_INSTRUCTIONS)

    def test_admission_pump_lock_rejects_overlapping_invocations(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-pump-lock-") as temporary:
            original = controller.ADMISSION_PUMP_LOCK
            controller.ADMISSION_PUMP_LOCK = Path(temporary) / "pump.lock"
            try:
                with controller.admission_pump_guard():
                    with self.assertRaisesRegex(controller.ControllerError, "admission pump already"):
                        with controller.admission_pump_guard():
                            pass
            finally:
                controller.ADMISSION_PUMP_LOCK = original

    def test_activation_contract_requires_cron_log_parent(self):
        source = PATH.read_text(encoding="utf-8")
        self.assertIn('(RUNTIME / "logs").mkdir', source)
        self.assertIn('or not (RUNTIME / "logs").is_dir()', source)

    def test_replacement_ledger_is_per_item_and_deduplicates_current_history(self):
        initial = {"item_id":"A", "generation_id":"g0"}
        first_replacement = {"item_id":"A", "generation_id":"g1"}
        state = {
            "generation_history": [initial, first_replacement],
            "claims": {"A": dict(first_replacement)},
        }
        self.assertEqual(controller.generation_ids_for_item(state, "A"), ["g0", "g1"])
        self.assertEqual(controller.replacement_count_for_item(state, "A"), 1)
        self.assertEqual(controller.next_replacement_ordinal(state, "A"), 2)
        self.assertEqual(controller.previous_generation_id_for_item(state, "A"), "g1")

    def test_pre_goal_startup_failures_do_not_consume_theorem_replacements(self):
        state = {
            "generation_history": [
                {"item_id":"A", "generation_id":"startup-1", "goal_submissions":0},
                {"item_id":"A", "generation_id":"goal-1", "goal_submissions":1},
                {"item_id":"A", "generation_id":"startup-2", "goal_submissions":0},
            ],
            "claims": {},
        }
        self.assertEqual(controller.generation_ids_for_item(state, "A"), ["goal-1"])
        self.assertEqual(controller.replacement_count_for_item(state, "A"), 0)
        self.assertEqual(controller.next_replacement_ordinal(state, "A"), 1)
        self.assertTrue(controller.replacement_admissible(state, "A", 60))

    def test_inflated_pre_goal_ordinal_is_fenced_before_refill(self):
        current = {
            "item_id":"A", "generation_id":"startup-3",
            "goal_submissions":0, "status":"tmux_started",
            "replacement_ordinal":7,
        }
        state = {
            "generation_history": [
                {"item_id":"A", "generation_id":"goal-0", "goal_submissions":1},
                {"item_id":"A", "generation_id":"goal-1", "goal_submissions":1},
                {"item_id":"A", "generation_id":"startup-2", "goal_submissions":0},
            ],
            "claims": {"A": current},
        }
        self.assertEqual(controller.next_replacement_ordinal(state, "A"), 2)
        self.assertEqual(
            controller.pre_goal_replacement_ordinal_violation(state, current),
            "pre_goal_replacement_ordinal_spent_by_startup_noise",
        )
        current["replacement_ordinal"] = 2
        self.assertIsNone(
            controller.pre_goal_replacement_ordinal_violation(state, current),
        )

    def test_sixtieth_replacement_is_allowed_and_sixty_first_is_refused(self):
        before_sixtieth = {
            "generation_history": [
                {"item_id":"A", "generation_id":f"g{index}"}
                for index in range(60)
            ],
            "claims": {},
        }
        self.assertEqual(controller.replacement_count_for_item(before_sixtieth, "A"), 59)
        self.assertEqual(controller.next_replacement_ordinal(before_sixtieth, "A"), 60)
        self.assertTrue(controller.replacement_admissible(before_sixtieth, "A", 60))
        after_sixtieth = {
            "generation_history": [
                {"item_id":"A", "generation_id":f"g{index}"}
                for index in range(61)
            ],
            "claims": {},
        }
        self.assertEqual(controller.replacement_count_for_item(after_sixtieth, "A"), 60)
        self.assertEqual(controller.next_replacement_ordinal(after_sixtieth, "A"), 61)
        self.assertFalse(controller.replacement_admissible(after_sixtieth, "A", 60))

    def test_typed_retirement_reason_survives_transport_cleanup(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-retire-reason-") as temporary:
            record = {
                "item_id":"A", "generation_id":"g1", "run_id":"g1",
                "task_root":temporary, "status":"generation_retire_required",
                "retired_reason":"provider_breaker_open_before_goal_submission",
            }
            state = {"claims":{"A":dict(record)}}
            with (
                mock.patch.object(controller, "stop_record"),
                mock.patch.object(controller, "release_request_leases"),
                mock.patch.object(controller, "append_event"),
                mock.patch.object(controller, "save_state"),
            ):
                controller.retire_launch_failure(state, record, controller.ControllerError("retire"))
            self.assertEqual(
                state["claims"]["A"]["retired_reason"],
                "provider_breaker_open_before_goal_submission",
            )

    def test_successor_generation_rejects_global_ordinal_as_retry_attempt(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-lineage-") as temporary:
            root = Path(temporary)
            card = {
                "execution_policy": {"recovery": {"generation_replacements_per_work_item": 60}},
                "generation_lineage": {"replacement_ordinal": 203, "replacement_cap": 60, "previous_generation_id": None},
                "retry_budget": {"attempt": 203, "max_attempts": 60},
            }
            (root / "claim.json").write_text(json.dumps(card))
            record = {
                "status":"live", "service_tier":controller.SERVICE_TIER,
                "prompt_digest":"p", "task_root":str(root), "replacement_ordinal":203,
            }
            self.assertEqual(
                controller.successor_generation_violation(record, {}, "p"),
                "invalid_per_item_generation_lineage",
            )

    def test_successor_generation_retires_stale_item_validator(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-validator-epoch-") as temporary:
            root = Path(temporary)
            baseline = root / "work/_baseline"
            baseline.mkdir(parents=True)
            stale = b"# stale semantic gate\n"
            (baseline / "check_stage5_theorem_item.py").write_bytes(stale)
            card = {
                "execution_policy": {"recovery": {"generation_replacements_per_work_item": 60}},
                "generation_lineage": {
                    "replacement_ordinal": 0, "replacement_cap": 60,
                    "previous_generation_id": None,
                },
                "retry_budget": {"attempt": 1, "max_attempts": 61},
                "read_only_bootstrap_files": [{
                    "path": "_baseline/check_stage5_theorem_item.py",
                    "sha256": controller.digest(stale), "size_bytes": len(stale),
                }],
            }
            (root / "claim.json").write_text(json.dumps(card))
            record = {
                "status": "live", "service_tier": controller.SERVICE_TIER,
                "task_root": str(root), "replacement_ordinal": 0,
            }
            self.assertEqual(
                controller.successor_generation_violation(record, {}, "p"),
                "stale_item_validator_sha256",
            )

    def test_current_session_foreign_task_root_reference_retires_and_blocks_harvest(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-session-boundary-") as temporary:
            task = Path(temporary) / "runtime/tasks/S5THM-00000001-TARGET--worker/r-1-aaaa"
            work = task / "work"; home = task / "codex-home"; sessions = home / "sessions"
            work.mkdir(parents=True); sessions.mkdir(parents=True)
            foreign = controller.ROOT / ".ops/stage5-theorems-execution-v2/tasks/S5THM-00000002-TARGET--worker/r-2-bbbb/work"
            event = {"payload": {"type": "custom_tool_call", "input": f'const r = await tools.exec_command({{"cmd":"find {foreign} -type f"}});'}}
            (sessions / "rollout.jsonl").write_text(json.dumps(event) + "\n")
            record = {"item_id":"S5THM-00000001-TARGET", "claim_id":"S5THM-00000001-TARGET--worker", "run_id":"r-1-aaaa", "task_root":str(task), "work_root":str(work), "codex_home":str(home), "status":"live"}
            violation = controller.session_access_violation(record)
            self.assertIn("foreign_task_root_reference", violation or "")
            with mock.patch.object(controller, "append_event"):
                self.assertFalse(controller.harvest_record(record, {}))
            self.assertEqual(record["status"], "generation_retire_required")
            self.assertIn("foreign_task_root_reference", record["retired_reason"])

    def test_apply_patch_may_delete_inherited_foreign_path_but_not_add_or_execute_it(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-checkpoint-patch-boundary-") as temporary:
            task = controller.ROOT / ".ops/stage5-theorems-execution-v2/tasks/S5THM-00000001-TARGET--worker/r-current/work"
            task_root = task.parent
            home = Path(temporary) / "codex-home"
            sessions = home / "sessions"
            sessions.mkdir(parents=True)
            foreign = controller.ROOT / ".ops/stage5-theorems-execution-v2/tasks/S5THM-00000001-TARGET--worker/r-predecessor/work/_baseline/check.py"
            current = task / "_baseline/check.py"
            deleted = (
                'const patch = "*** Begin Patch\\n*** Update File: receipt.json\\n'
                f'-  \\\"argv\\\": \\\"{foreign}\\\",\\n'
                f'+  \\\"argv\\\": \\\"{current}\\\"\\n'
                '*** End Patch"; text(await tools.apply_patch(patch));'
            )
            path = sessions / "rollout.jsonl"
            record = {"task_root":str(task_root), "work_root":str(task), "codex_home":str(home)}
            path.write_text(json.dumps({"payload":{"type":"custom_tool_call","input":deleted}}) + "\n")
            self.assertIsNone(controller.session_access_violation(record))

            added_foreign = deleted.replace(str(current), str(foreign))
            path.write_text(json.dumps({"payload":{"type":"custom_tool_call","input":added_foreign}}) + "\n")
            self.assertIn("foreign_task_root_reference", controller.session_access_violation(record) or "")

            executed = f'const r = await tools.exec_command({{"cmd":"find {foreign}"}});'
            path.write_text(json.dumps({"payload":{"type":"custom_tool_call","input":executed}}) + "\n")
            self.assertIn("foreign_task_root_reference", controller.session_access_violation(record) or "")

    def test_current_session_own_task_subpaths_are_allowed_but_parent_escape_is_not(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-session-own-") as temporary:
            task = Path(temporary) / "runtime/tasks/S5THM-00000001-TARGET--worker/r-1-aaaa"
            work = task / "work"; home = task / "codex-home"; sessions = home / "sessions"
            work.mkdir(parents=True); sessions.mkdir(parents=True)
            own_event = {"payload": {"type": "custom_tool_call", "input": f'const r = await tools.exec_command({{"cmd":"find {work} -type f"}});'}}
            path = sessions / "rollout.jsonl"; path.write_text(json.dumps(own_event) + "\n")
            record = {"task_root":str(task), "work_root":str(work), "codex_home":str(home)}
            self.assertIsNone(controller.session_access_violation(record))
            escape = {"payload": {"type": "CommandExecution", "command": ["/bin/bash", "-lc", "find ../.. -type f"]}}
            path.write_text(json.dumps(escape) + "\n")
            self.assertIn("relative_task_root_escape", controller.session_access_violation(record) or "")

    def test_current_session_canonical_checkout_reference_is_forbidden(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-session-canonical-") as temporary:
            task = controller.ROOT / ".ops/stage5-theorems-execution-v2/tasks/S5THM-00000001-TARGET--worker/r-1-aaaa"
            home = Path(temporary) / "codex-home"; sessions = home / "sessions"
            sessions.mkdir(parents=True)
            event = {"payload": {"type": "custom_tool_call", "input": f'const r=await tools.exec_command({{"cmd":"rg theorem {controller.ROOT}/Formalizations/Lean/.lake/packages/mathlib"}});'}}
            (sessions / "rollout.jsonl").write_text(json.dumps(event) + "\n")
            record = {"task_root":str(task), "work_root":str(task / "work"), "codex_home":str(home)}
            self.assertIn("canonical_root_reference", controller.session_access_violation(record) or "")

    def test_current_session_escaped_suffix_after_exact_own_root_is_allowed(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-session-escaped-own-") as temporary:
            task = controller.ROOT / ".ops/stage5-theorems-execution-v2/tasks/S5THM-00000001-TARGET--worker/r-1-aaaa"
            home = Path(temporary) / "codex-home"; sessions = home / "sessions"
            sessions.mkdir(parents=True)
            event = {"payload": {"type": "CommandExecution", "command": [
                "/bin/bash", "-lc", f"claim={task}\\:; test -n \"$claim\"",
            ]}}
            (sessions / "rollout.jsonl").write_text(json.dumps(event) + "\n")
            record = {"task_root":str(task), "work_root":str(task / "work"), "codex_home":str(home)}
            self.assertIsNone(controller.session_access_violation(record))

    def test_current_session_exact_sed_redaction_literal_is_not_a_canonical_read(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-session-redaction-") as temporary:
            task = controller.ROOT / ".ops/stage5-theorems-execution-v2/tasks/S5THM-00000001-TARGET--worker/r-1-aaaa"
            home = Path(temporary) / "codex-home"; sessions = home / "sessions"
            sessions.mkdir(parents=True)
            redactor = f"env | sed -E 's#({controller.ROOT})[^: ]*#<canonical-path-redacted>#g'"
            event = {"payload": {"type": "CommandExecution", "command": ["/bin/bash", "-lc", redactor]}}
            path = sessions / "rollout.jsonl"; path.write_text(json.dumps(event) + "\n")
            record = {"task_root":str(task), "work_root":str(task / "work"), "codex_home":str(home)}
            self.assertIsNone(controller.session_access_violation(record))
            event["payload"]["command"][-1] += f"; find {controller.ROOT}/Formalizations/Lean -type f"
            path.write_text(json.dumps(event) + "\n")
            self.assertIn("canonical_root_reference", controller.session_access_violation(record) or "")

    def test_current_session_task_local_patchcheck_parent_path_is_allowed(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-session-patchcheck-") as temporary:
            task = Path(temporary) / "runtime/tasks/S5THM-00000001-TARGET--worker/r-1-aaaa"
            work = task / "work"; home = task / "codex-home"; sessions = home / "sessions"
            work.mkdir(parents=True); sessions.mkdir(parents=True)
            event = {"payload": {"type": "CommandExecution", "command": ["/bin/bash", "-lc", "(cd _outbox/patchcheck && git apply --check ../../../changes.patch)"]}}
            (sessions / "rollout.jsonl").write_text(json.dumps(event) + "\n")
            record = {"task_root":str(task), "work_root":str(work), "codex_home":str(home)}
            self.assertIsNone(controller.session_access_violation(record))

    def test_current_session_task_local_replay_patch_is_allowed_by_resolved_cwd(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-session-replay-patch-") as temporary:
            task = Path(temporary) / "runtime/tasks/S5THM-00000001-TARGET--worker/r-1-aaaa"
            work = task / "work"; replay = work / ".replay-audit"
            home = task / "codex-home"; sessions = home / "sessions"
            replay.mkdir(parents=True); sessions.mkdir(parents=True)
            tool_input = (
                'const res = await tools.exec_command({' 
                'cmd:"git apply --check ../../changes.patch",'
                f'workdir:{json.dumps(str(replay))}'
                '}); text(JSON.stringify(res));'
            )
            event = {"payload": {"type": "custom_tool_call", "input": tool_input}}
            path = sessions / "rollout.jsonl"
            path.write_text(json.dumps(event) + "\n")
            record = {"task_root":str(task), "work_root":str(work), "codex_home":str(home)}
            self.assertIsNone(controller.session_access_violation(record))

            completed = {"payload": {"type":"CommandExecution", "command":[
                "/bin/bash", "-lc", "git apply --check ../../changes.patch",
            ], "cwd": replay.as_uri()}}
            path.write_text(json.dumps(completed) + "\n")
            self.assertIsNone(controller.session_access_violation(record))

    def test_replay_patch_exception_fails_closed_for_wrong_or_missing_cwd(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-session-replay-fence-") as temporary:
            task = Path(temporary) / "runtime/tasks/S5THM-00000001-TARGET--worker/r-1-aaaa"
            work = task / "work"; home = task / "codex-home"; sessions = home / "sessions"
            work.mkdir(parents=True); sessions.mkdir(parents=True)
            record = {"task_root":str(task), "work_root":str(work), "codex_home":str(home)}
            path = sessions / "rollout.jsonl"

            missing_cwd = {"payload":{"type":"CommandExecution", "command":[
                "/bin/bash", "-lc", "git apply --check ../../changes.patch",
            ]}}
            path.write_text(json.dumps(missing_cwd) + "\n")
            self.assertIn("relative_task_root_escape", controller.session_access_violation(record) or "")

            wrong_cwd = dict(missing_cwd)
            wrong_cwd = json.loads(json.dumps(wrong_cwd))
            wrong_cwd["payload"]["cwd"] = work.as_uri()
            path.write_text(json.dumps(wrong_cwd) + "\n")
            self.assertIn("relative_task_root_escape", controller.session_access_violation(record) or "")

            foreign = task.parent / "r-2-bbbb" / "work/.replay-audit"
            foreign_cwd = json.loads(json.dumps(missing_cwd))
            foreign_cwd["payload"]["cwd"] = foreign.as_uri()
            path.write_text(json.dumps(foreign_cwd) + "\n")
            self.assertIn("relative_task_root_escape", controller.session_access_violation(record) or "")

    def test_complete_goal_is_terminal_and_never_reauthenticated(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-complete-") as temporary:
            home = Path(temporary) / "home"
            home.mkdir()
            state = sqlite3.connect(home / "state_5.sqlite")
            state.executescript("create table threads(id text,cwd text,model_provider text,model text,reasoning_effort text); insert into threads values('thread-1','/work','sub2api','gpt-5.6-sol','ultra');")
            state.commit(); state.close()
            goals = sqlite3.connect(home / "goals_1.sqlite")
            goals.executescript("create table thread_goals(thread_id text,goal_id text,objective text,status text); insert into thread_goals values('thread-1','goal-1','S5THM-00003485-TARGET claim','complete');")
            goals.commit(); goals.close()
            (Path(temporary) / "work").mkdir()
            record = {"item_id":"S5THM-00003485-TARGET", "claim_id":"S5THM-00003485-TARGET--worker", "run_id":"run-1", "task_root":temporary, "codex_home":str(home), "work_root":str(Path(temporary) / "work"), "status":"live", "session":"fixture", "pane_pid":1, "pane_pid_start_ticks":1}
            with mock.patch.object(controller, "terminal_reason", return_value="goal_terminal"), mock.patch.object(controller, "append_event"):
                self.assertEqual(controller.reconcile_record(record), "generation_retire_required")
            self.assertEqual(record["terminal_reason"], "goal_terminal")

    def test_nested_repository_copy_is_a_task_boundary_violation(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-boundary-") as temporary:
            work = Path(temporary) / "work"
            nested = work / ".tmp-foundation-src"
            nested.mkdir(parents=True)
            (nested / ".git").mkdir()
            (nested / "lakefile.toml").write_text("name = 'fixture'\n")
            (nested / "lean-toolchain").write_text("v4.0.0\n")
            (nested / "README.md").write_text("fixture\n")
            record = {"item_id":"S5THM-00003489-TARGET", "claim_id":"S5THM-00003489-TARGET--worker", "run_id":"run-1", "work_root":str(work), "status":"live"}
            self.assertIn("task_boundary", controller.task_boundary_violation(record) or "")

    def test_validate_only_is_read_only_and_route_is_frozen(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-validate-"):
            before = controller.RUNTIME.exists()
            with (
                mock.patch.object(
                    controller, "active_operator_goal",
                    return_value={
                        "thread_id": controller.GOAL_THREAD_ID,
                        "goal_id": "test-active-goal",
                        "status": "active",
                    },
                ),
                mock.patch.object(
                    controller, "validate_controller_successor_acceptance",
                    return_value={"authority_sha256":"s" * 64},
                ),
                mock.patch.object(
                    controller, "validate_activation",
                    return_value={"authority_sha256":"a" * 64},
                ),
            ):
                result = controller.validate_only(controller.CONCURRENCY_PROMPT)
            self.assertTrue(result["valid"], result)
            self.assertEqual(result["concurrency_prompt"]["requested"]["authenticated_goals"], 24)
            self.assertEqual(result["controller_successor_authority_sha256"], "s" * 64)
            self.assertEqual(result["activation_authority_sha256"], "a" * 64)
            self.assertEqual(controller.RUNTIME.exists(), before)

    def test_validate_only_fails_closed_on_successor_or_activation(self):
        goal = {"thread_id":controller.GOAL_THREAD_ID,"goal_id":"g","status":"active"}
        with (
            mock.patch.object(controller, "active_operator_goal", return_value=goal),
            mock.patch.object(
                controller, "validate_controller_successor_acceptance",
                side_effect=controller.ControllerError("successor invalid"),
            ),
        ):
            result = controller.validate_only(controller.CONCURRENCY_PROMPT)
        self.assertFalse(result["valid"])
        self.assertIn("successor invalid", result["errors"])
        with (
            mock.patch.object(controller, "active_operator_goal", return_value=goal),
            mock.patch.object(
                controller, "validate_controller_successor_acceptance",
                return_value={"authority_sha256":"s" * 64},
            ),
            mock.patch.object(
                controller, "validate_activation",
                side_effect=controller.ControllerError("activation invalid"),
            ),
        ):
            result = controller.validate_only(controller.CONCURRENCY_PROMPT)
        self.assertFalse(result["valid"])
        self.assertIn("activation invalid", result["errors"])

    def test_maintenance_intent_has_durable_one_use_consumption(self):
        with tempfile.TemporaryDirectory(prefix="stage5-maintenance-consume-") as temporary:
            original_intent = controller.CONTROLLER_SUCCESSOR_MAINTENANCE_INTENT
            original_consumptions = controller.CONTROLLER_SUCCESSOR_MAINTENANCE_CONSUMPTIONS
            root = Path(temporary)
            controller.CONTROLLER_SUCCESSOR_MAINTENANCE_INTENT = root / "intent.json"
            controller.CONTROLLER_SUCCESSOR_MAINTENANCE_CONSUMPTIONS = root / "consumptions"
            controller.CONTROLLER_SUCCESSOR_MAINTENANCE_INTENT.write_text("{}\n")
            intent = {
                "authority_sha256":"1" * 64,
                "payload": {
                    "action":"paused_reconcile_fence_and_refill_only",
                    "candidate_artifacts": {"controller_sha256":"2" * 64},
                },
            }
            try:
                receipt = controller.consume_controller_successor_maintenance_intent(intent)
                self.assertEqual(receipt["intent_authority_sha256"], "1" * 64)
                with self.assertRaisesRegex(controller.ControllerError, "already consumed"):
                    controller.consume_controller_successor_maintenance_intent(intent)
            finally:
                controller.CONTROLLER_SUCCESSOR_MAINTENANCE_INTENT = original_intent
                controller.CONTROLLER_SUCCESSOR_MAINTENANCE_CONSUMPTIONS = original_consumptions

    def test_live_manifest_binds_each_claim_spec_prompt_and_vector(self):
        successor = load_successor_tool()
        specification, _, _ = controller.load_program()
        prompt, prompt_sha = controller.load_concurrency_prompt(
            controller.CONCURRENCY_PROMPT, specification,
        )
        spec_sha = controller.digest(controller.canonical(specification))
        spec_file_sha = controller.file_digest(controller.EVIDENCE / "execution-spec.json")
        with tempfile.TemporaryDirectory(prefix="stage5-live-manifest-") as temporary:
            claims = {}
            for index in range(24):
                item_id = f"ITEM-{index:02d}"
                run_id = f"run-{index:02d}"
                task = Path(temporary) / item_id / run_id
                baseline = task / "work/_baseline"
                baseline.mkdir(parents=True)
                (baseline / "fixture.txt").write_text("fixture")
                item_checker_bytes = controller.ITEM_CHECKER_PATH.read_bytes()
                (baseline / "check_stage5_theorem_item.py").write_bytes(
                    item_checker_bytes,
                )
                item_checker_sha = controller.digest(item_checker_bytes)
                claim = {
                    "item_id":item_id, "claim_id":f"{item_id}--worker",
                    "run_id":run_id, "task_root":str(task),
                    "baseline":{"execution_spec_sha256":spec_sha},
                    "execution_identity":{
                        "lane_id":item_id, "generation_id":run_id,
                        "execution_spec_sha256":spec_sha,
                        "prompt_epoch":prompt["policy_epoch"],
                        "prompt_digest":prompt_sha,
                        "requested_concurrency":prompt["concurrency"],
                        "resolved_concurrency":prompt["concurrency"],
                    },
                    "read_only_bootstrap_files":[
                        {"path":"_baseline/execution-spec.json","sha256":spec_file_sha,"size_bytes":1},
                        {"path":"_baseline/concurrency-prompt.json","sha256":prompt_sha,"size_bytes":1},
                        {"path":"_baseline/check_stage5_theorem_item.py","sha256":item_checker_sha,"size_bytes":len(item_checker_bytes)},
                    ],
                }
                (task / "claim.json").write_text(json.dumps(claim))
                claims[item_id] = {
                    "item_id":item_id, "claim_id":f"{item_id}--worker",
                    "run_id":run_id, "generation_id":run_id, "lane_id":item_id,
                    "status":"live", "task_root":str(task), "goal_submissions":1,
                    "thread_id":f"thread-{index}", "goal_id":f"goal-{index}",
                    "prompt_epoch":prompt["policy_epoch"], "prompt_digest":prompt_sha,
                }
            rows = successor.live_manifest(
                {"claims":claims}, specification, prompt, prompt_sha,
            )
            self.assertEqual(len(rows), 24)
            self.assertTrue(all(row["execution_spec_sha256"] == spec_sha for row in rows))
            self.assertTrue(all(
                row["baseline_item_checker_sha256"]
                == controller.file_digest(controller.ITEM_CHECKER_PATH)
                for row in rows
            ))
            bad = Path(claims["ITEM-00"]["task_root"]) / "claim.json"
            value = json.loads(bad.read_text())
            value["execution_identity"]["prompt_digest"] = "0" * 64
            bad.write_text(json.dumps(value))
            with self.assertRaisesRegex(successor.MigrationError, "identity is incomplete"):
                successor.live_manifest({"claims":claims}, specification, prompt, prompt_sha)

    def test_complete_prompt_is_spec_and_goal_bound(self):
        specification, _, _ = controller.load_program()
        with tempfile.TemporaryDirectory(prefix="stage5-v2-prompt-") as temporary:
            path = Path(temporary) / "prompt.json"
            prompt = sealed_prompt(specification)
            path.write_text(json.dumps(prompt))
            value, prompt_digest = controller.load_concurrency_prompt(path, specification)
            self.assertEqual(value["concurrency"]["authenticated_goals"], 24)
            self.assertEqual(prompt_digest, hashlib.sha256(path.read_bytes()).hexdigest())
            prompt["operator_goal_objective_sha256"] = "0" * 64
            body = dict(prompt); body.pop("authority_sha256")
            prompt["authority_sha256"] = controller.digest(controller.canonical(body))
            path.write_text(json.dumps(prompt))
            with self.assertRaisesRegex(controller.ControllerError, "goal binding differs"):
                controller.load_concurrency_prompt(path, specification)

    def test_prompt_rejects_omission_and_illegal_not_applicable(self):
        specification, _, _ = controller.load_program()
        vector = sealed_prompt(specification)["concurrency"]
        missing = dict(vector); missing.pop("validators")
        with self.assertRaisesRegex(controller.ControllerError, "complete concurrency vector"):
            controller.validate_concurrency_vector(missing)
        illegal = dict(vector); illegal["validators"] = "not_applicable"
        with self.assertRaisesRegex(controller.ControllerError, "validators is applicable"):
            controller.validate_concurrency_vector(illegal)

    def test_prompt_rejects_fanout_above_request_cap(self):
        specification, _, _ = controller.load_program()
        vector = sealed_prompt(specification)["concurrency"]
        vector = dict(vector); vector["launch_fanout_per_wave"] = 121
        with self.assertRaisesRegex(controller.ControllerError, "fanout exceeds"):
            controller.validate_concurrency_vector(vector)

    def test_prompt_rejects_duplicate_and_non_finite_json_before_side_effects(self):
        specification, _, _ = controller.load_program()
        with tempfile.TemporaryDirectory(prefix="stage5-v2-strict-prompt-") as temporary:
            path = Path(temporary) / "prompt.json"
            path.write_text('{"schema_version":"x","schema_version":"y"}')
            with self.assertRaisesRegex(controller.ControllerError, "duplicate JSON key"):
                controller.load_concurrency_prompt(path, specification)
            path.write_text('{"value":NaN}')
            with self.assertRaisesRegex(controller.ControllerError, "non-finite JSON number"):
                controller.load_concurrency_prompt(path, specification)

    def test_dynamic_dag_projection_orders_and_builds_frontier_before_filters(self):
        rows = [
            {"item_id": "BOOT", "state": "x", "dependencies": ()},
            {"item_id": "A", "state": " ", "dependencies": ("BOOT",)},
            {"item_id": "B", "state": " ", "dependencies": ("BOOT",)},
            {"item_id": "C", "state": " ", "dependencies": ("A",)},
            {"item_id": "D", "state": "_", "dependencies": ("B",)},
        ]
        projection = controller.dag_projection(rows, {"B"})
        self.assertEqual(projection["accepted_ids"], ["BOOT"])
        self.assertEqual(projection["active_ids"], ["B"])
        self.assertEqual(projection["dependency_clear_frontier"], ["A"])
        self.assertEqual(projection["ordered_ids"], ["BOOT", "B", "A", "C", "D"])

    def test_claimability_comes_only_from_explicit_item_modes(self):
        specification = {"item_modes": [
            {"execution_class": "codex_tui_claim", "id_regex": "TARGET-[0-9]+"},
            {"execution_class": "master_only", "id_regex": "MASTER"},
        ]}
        rows = [
            {"item_id": "TARGET-1"}, {"item_id": "MASTER"}, {"item_id": "TARGET-X"},
        ]
        self.assertEqual(controller.claimable_item_ids(specification, rows), {"TARGET-1"})

    def test_exact_path_conflicts_include_prefix_overlap(self):
        self.assertTrue(controller.paths_conflict(["a/b"], ["a/b/c.json"]))
        self.assertTrue(controller.paths_conflict(["a/b.json"], ["a/b.json"]))
        self.assertFalse(controller.paths_conflict(["a/b.json"], ["a/c.json"]))

    def test_admission_availability_keeps_dimensions_independent(self):
        prompt = {"concurrency": sealed_prompt({})["concurrency"]}
        state = {"claims": {
            "A": {"lane_id": "A", "status": "live"},
            "B": {"lane_id": "B", "status": "goal_submitted"},
            "C": {"lane_id": "C", "status": "reserved"},
        }}
        lease = {"request_starts_per_window": 7, "in_flight_requests": 2, "running_turns": 1}
        slots, usage, reasons = controller.admission_availability(
            state, prompt, lease_usage=lease,
        )
        self.assertEqual(usage["logical_claims"], 3)
        self.assertEqual(usage["agent_executions"], 3)
        self.assertEqual(usage["startup_reservations"], 2)
        self.assertEqual(usage["live_transports"], 2)
        self.assertEqual(usage["authenticated_goals"], 1)
        self.assertEqual(usage["running_turns"], 1)
        self.assertEqual(usage["in_flight_requests"], 2)
        self.assertEqual(slots, 17)
        self.assertEqual(reasons, [])

    def test_request_window_can_bind_before_in_flight_cap(self):
        prompt = {"concurrency": sealed_prompt({})["concurrency"]}
        state = {"claims": {}}
        lease = {"request_starts_per_window": 12, "in_flight_requests": 0, "running_turns": 0}
        slots, _, reasons = controller.admission_availability(
            state, prompt, lease_usage=lease,
        )
        self.assertEqual(slots, 12)
        self.assertEqual(reasons, [])

    def test_one_invocation_pumps_six_waves_to_24_fixture_workers(self):
        prompt = sealed_prompt({})
        specification = {
            "scheduler": {"tick_budget_seconds": 100, "startup_deadline_seconds": 180},
            "item_modes": [{"execution_class": "codex_tui_claim", "id_regex": "TARGET-[0-9]+"}],
        }
        rows = [{
            "item_id": "BOOT", "state": "x", "dependencies": (),
            "owned_paths": (), "title": "boot", "gate": "accepted",
        }] + [{
            "item_id": f"TARGET-{index}", "state": " ", "dependencies": ("BOOT",),
            "owned_paths": (f"claims/{index}.json",), "title": f"target {index}",
            "gate": "fixture",
        } for index in range(24)]
        with tempfile.TemporaryDirectory(prefix="stage5-v2-pump-") as temporary:
            root = Path(temporary)
            originals = {
                "RUNTIME": controller.RUNTIME, "STATE_PATH": controller.STATE_PATH,
                "SCHEDULER_LOCK": controller.SCHEDULER_LOCK,
                "ADMISSION_PUMP_LOCK": controller.ADMISSION_PUMP_LOCK,
            }
            controller.RUNTIME = root / "runtime"
            controller.STATE_PATH = controller.RUNTIME / "state/controller-state.json"
            controller.SCHEDULER_LOCK = root / "scheduler.lock"
            controller.ADMISSION_PUMP_LOCK = root / "admission-pump.lock"

            def materialize(item, specification, raw, ordinal, **kwargs):
                generation = kwargs["generation_id"]
                claim = item["item_id"] + "--worker"
                task = controller.RUNTIME / "tasks" / claim / generation
                return {
                    "item_id": item["item_id"], "claim_id": claim,
                    "run_id": generation, "generation_id": generation,
                    "lane_id": kwargs["lane_id"], "task_root": str(task),
                    "work_root": str(task / "work"), "codex_home": str(task / "codex-home"),
                    "socket_path": str(task / "tmux.sock"), "socket_argument": "tmux.sock",
                    "session": "fixture", "status": "materialized",
                    "goal_submissions": 0, "ordinal": ordinal,
                }

            def submit(record, prompt, on_transition=None, invocation_deadline=None):
                record.update({"status": "live", "goal_submissions": 1})
                if on_transition:
                    on_transition(record)

            try:
                budget_patchers = [
                    mock.patch.object(controller, "ensure_budget_accounting", return_value={}),
                    mock.patch.object(controller, "reserve_generation_budget"),
                ]
                for patcher in budget_patchers:
                    patcher.start()
                try:
                    with (
                    mock.patch.object(controller, "load_program", return_value=(specification, rows, b"blueprint")),
                    mock.patch.object(controller, "load_concurrency_prompt", return_value=(prompt, "d" * 64)),
                    mock.patch.object(controller, "validate_claim_schema_prompt_identity"),
                    mock.patch.object(controller, "validate_activation"),
                    mock.patch.object(controller, "validate_operator_authority", return_value={"authority": {}, "goal": {}}),
                    mock.patch.object(controller, "semantic_revoked_master_acceptances", return_value={}),
                    mock.patch.object(controller, "materialize_runtime_authority"),
                    mock.patch.object(controller, "harvest_state", return_value=0),
                    mock.patch.object(controller, "run_bounded_master_integration", return_value=[]),
                    mock.patch.object(controller, "fence_orphaned_generations", return_value=0),
                    mock.patch.object(controller, "reconcile_record", side_effect=lambda record: record["status"]),
                    mock.patch.object(controller, "materialize_claim", side_effect=materialize),
                    mock.patch.object(controller, "submit_goal", side_effect=submit),
                    mock.patch.object(controller, "request_lease_usage", return_value={"request_starts_per_window": 0, "in_flight_requests": 0, "running_turns": 0}),
                    mock.patch.object(controller, "append_runtime_snapshot"),
                    ):
                        result = controller.launch_workers(root / "prompt.json")
                finally:
                    for patcher in reversed(budget_patchers):
                        patcher.stop()
                self.assertEqual(result["launched"], 24)
                self.assertEqual(result["waves"], 6)
                self.assertEqual(result["observed_usage"]["authenticated_goals"], 24)
                self.assertEqual(len({claim["generation_id"] for claim in result["claims"]}), 24)
            finally:
                for name, value in originals.items():
                    setattr(controller, name, value)

    def test_submitted_starting_lanes_do_not_turn_wave_fanout_into_total_cap(self):
        prompt = {"concurrency": sealed_prompt({})["concurrency"]}
        claims = {
            str(index): {
                "lane_id": str(index), "run_id": str(index),
                "status": "goal_submitted",
            }
            for index in range(4)
        }
        slots, usage, reasons = controller.admission_availability(
            {"claims": claims}, prompt,
            lease_usage={"request_starts_per_window": 4, "in_flight_requests": 4, "running_turns": 4},
        )
        self.assertEqual(usage["startup_reservations"], 4)
        self.assertEqual(slots, 20)
        self.assertEqual(reasons, [])

    def test_current_claim_schema_has_closed_prompt_identity(self):
        self.assertIsNone(controller.validate_claim_schema_prompt_identity())
        schema = json.loads((controller.EVIDENCE / "claim-card.schema.json").read_text())
        identity = schema["properties"]["execution_identity"]
        self.assertFalse(identity["additionalProperties"])
        for field in ("requested_concurrency", "resolved_concurrency"):
            self.assertEqual(
                set(identity["properties"][field]["required"]),
                set(controller.CONCURRENCY_DIMENSIONS),
            )

    def test_launch_surface_is_interactive_tmux_only(self):
        tree = ast.parse(PATH.read_text(encoding="utf-8"))
        source = PATH.read_text(encoding="utf-8").lower()
        self.assertNotIn("docker run", source)
        self.assertNotIn("codex exec", source)
        self.assertNotIn('"app-server"', source)
        self.assertIn("tmux", source)
        self.assertIn("/goal", source)
        self.assertNotIn('or "pasted content" in pane.lower()', source)
        self.assertIn("if token in pane: break", source)
        self.assertIn("short-objective limit", source)
        self.assertIn('"»" in pane or "›" in pane', source)
        self.assertIsNotNone(tree)
        self.assertEqual(controller.PROGRAM, "stage5-theorem-proof-debt/2.0")
        self.assertEqual(controller.RUNTIME.name, "stage5-theorems-execution-v2")
        with mock.patch.object(
            controller, "active_operator_goal",
            return_value={
                "thread_id": controller.GOAL_THREAD_ID,
                "goal_id": "test-active-goal",
                "status": "active",
            },
        ), mock.patch.object(
            controller, "validate_controller_successor_acceptance",
            return_value={"authority_sha256":"s" * 64},
        ), mock.patch.object(
            controller, "validate_activation",
            return_value={"authority_sha256":"a" * 64},
        ):
            self.assertTrue(controller.validate_only(controller.CONCURRENCY_PROMPT)["valid"])

    def test_status_and_stop_do_not_create_absent_runtime(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-observe-") as temporary:
            original_runtime, original_state, original_scheduler_lock = controller.RUNTIME, controller.STATE_PATH, controller.SCHEDULER_LOCK
            controller.RUNTIME = Path(temporary) / "absent-runtime"
            controller.STATE_PATH = controller.RUNTIME / "state/controller-state.json"
            controller.SCHEDULER_LOCK = Path(temporary) / "scheduler.lock"
            try:
                self.assertEqual(controller.status()["claims"], [])
                self.assertEqual(controller.stop()["stopped"], 0)
                self.assertFalse(controller.RUNTIME.exists())
            finally:
                controller.RUNTIME, controller.STATE_PATH, controller.SCHEDULER_LOCK = original_runtime, original_state, original_scheduler_lock

    def test_status_is_read_only_and_never_harvests_or_integrates(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-read-status-") as temporary:
            root = Path(temporary)
            originals = controller.RUNTIME, controller.STATE_PATH, controller.SCHEDULER_LOCK
            controller.RUNTIME = root / "runtime"
            controller.STATE_PATH = controller.RUNTIME / "state/controller-state.json"
            controller.SCHEDULER_LOCK = root / "scheduler.lock"
            controller.RUNTIME.mkdir(parents=True)
            controller.save_state({"claims":{"A":{"item_id":"A", "status":"live"}}})
            before = controller.STATE_PATH.read_bytes()
            try:
                with (
                    mock.patch.object(controller, "harvest_state", side_effect=AssertionError("harvested")),
                    mock.patch.object(controller, "_integrate_once", side_effect=AssertionError("integrated")),
                    mock.patch.object(controller, "append_runtime_snapshot", side_effect=AssertionError("projected")),
                ):
                    result = controller.status()
                self.assertEqual(result["live"], 1)
                self.assertEqual(controller.STATE_PATH.read_bytes(), before)
            finally:
                controller.RUNTIME, controller.STATE_PATH, controller.SCHEDULER_LOCK = originals

    def test_stop_record_only_removes_its_task_local_socket(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-socket-") as temporary:
            task = Path(temporary)
            socket_path = task / "tmux.sock"
            # A non-socket file must never be unlinked by cleanup.
            socket_path.write_text("sentinel")
            controller.stop_record({"task_root": str(task), "socket_argument": "tmux.sock"})
            self.assertTrue(socket_path.exists())

    def test_orphan_fencing_is_registry_and_socket_local(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-fence-") as temporary:
            original_runtime = controller.RUNTIME
            controller.RUNTIME = Path(temporary) / "runtime"
            orphan = controller.RUNTIME / "tasks" / "S5THM-99999999-TARGET--worker" / "r-old"
            orphan.mkdir(parents=True)
            (orphan / "claim.json").write_text('{"claim_id":"S5THM-99999999-TARGET--worker","item_id":"S5THM-99999999-TARGET","run_id":"r-old"}')
            # A regular file is deliberately not treated as a tmux socket.
            (orphan / "tmux.sock").write_text("sentinel")
            try:
                self.assertEqual(controller.fence_orphaned_generations({"claims": {}}), 0)
                self.assertTrue((orphan / "tmux.sock").exists())
            finally:
                controller.RUNTIME = original_runtime

    def test_provider_503_is_a_route_failure(self):
        self.assertEqual(
            controller.classify_terminal_pane(
                "unexpected status 503 Service Unavailable: Service temporarily unavailable"
            ),
            "provider_unavailable",
        )
        self.assertEqual(
            controller.classify_terminal_pane("Selected model is at capacity"),
            "model_capacity",
        )
        self.assertEqual(
            controller.classify_terminal_pane("Goal completed"),
            "goal_terminal",
        )

    def test_backoff_sequence_jitter_bounds_and_cap(self):
        recovery = sealed_prompt({})["recovery"]
        self.assertEqual(
            [controller.backoff_delay(recovery, attempt) for attempt in range(1, 8)],
            [60, 120, 240, 480, 960, 1920, 3600],
        )
        self.assertEqual(controller.backoff_delay(recovery, 1, 0.8), 48)
        self.assertEqual(controller.backoff_delay(recovery, 1, 1.2), 72)
        self.assertEqual(controller.backoff_delay(recovery, 20, 1.2), 3600)

    def test_breaker_opens_once_at_three_and_cooldown_does_not_slide(self):
        recovery = sealed_prompt({})["recovery"]
        state = {}
        with mock.patch.object(controller.time, "time", return_value=1000.0):
            for index in range(3):
                controller.update_provider_breaker(state, {
                    "run_id": f"g{index}", "terminal_reason":"provider_unavailable",
                    "recovery": recovery,
                })
        self.assertEqual(state["breaker"]["state"], "open")
        self.assertEqual(state["breaker"]["cooldown_until"], 2800.0)
        with mock.patch.object(controller.time, "time", return_value=1100.0):
            controller.update_provider_breaker(state, {
                "run_id":"g3", "terminal_reason":"provider_unavailable", "recovery":recovery,
            })
        self.assertEqual(state["breaker"]["cooldown_until"], 2800.0)
        self.assertTrue(controller.provider_breaker_is_open(state, 2799.9))
        self.assertFalse(controller.provider_breaker_is_open(state, 2800.0))
        self.assertEqual(state["breaker"]["state"], "half_open")
        self.assertEqual(state["breaker"]["consecutive_failures"], 0)

    def test_open_breaker_gates_only_generations_before_goal_submission(self):
        state = {"claims": {
            "A": {"status":"tmux_started"},
            "B": {"status":"goal_pasted"},
            "C": {"status":"goal_submitted"},
            "D": {"status":"live"},
        }}
        self.assertEqual(controller.gate_pre_submission_generations_for_breaker(state, True), 2)
        for item_id in ("A", "B"):
            self.assertEqual(state["claims"][item_id]["status"], "generation_retire_required")
            self.assertEqual(
                state["claims"][item_id]["retired_reason"],
                "provider_breaker_open_before_goal_submission",
            )
        self.assertEqual(state["claims"]["C"]["status"], "goal_submitted")
        self.assertEqual(state["claims"]["D"]["status"], "live")

    def test_half_open_inconclusive_probes_release_only_after_all_terminal(self):
        state = {
            "breaker":{"state":"half_open","probe_generation_ids":["a","b"]},
            "claims":{
                "A":{"generation_id":"a","status":"retired"},
                "B":{"generation_id":"b","status":"live"},
            },
        }
        self.assertFalse(controller.refresh_half_open_probe_set(state))
        self.assertEqual(state["breaker"]["probe_generation_ids"], ["a", "b"])
        state["claims"]["B"]["status"] = "retired"
        self.assertTrue(controller.refresh_half_open_probe_set(state))
        self.assertEqual(state["breaker"]["probe_generation_ids"], [])
        self.assertEqual(state["breaker"]["inconclusive_probe_waves"], 1)

    def test_half_open_requires_completed_response_from_exact_probe(self):
        recovery = sealed_prompt({})["recovery"]
        state = {"breaker": {
            "provider":controller.PROVIDER, "state":"half_open",
            "consecutive_failures":0, "half_open_started_at":1000.0,
            "probe_generation_ids":["probe"], "last_signal_at":900.0,
        }}
        old = {"run_id":"old", "generation_id":"old", "status":"live", "recovery":recovery}
        probe = {"run_id":"probe", "generation_id":"probe", "status":"live", "recovery":recovery}
        with mock.patch.object(controller, "provider_response_completed_at", return_value=1100.0):
            controller.update_provider_breaker(state, old)
        self.assertEqual(state["breaker"]["state"], "half_open")
        with mock.patch.object(controller, "provider_response_completed_at", return_value=None):
            controller.update_provider_breaker(state, probe)
        self.assertEqual(state["breaker"]["state"], "half_open")
        with mock.patch.object(controller, "provider_response_completed_at", return_value=1100.0):
            controller.update_provider_breaker(state, probe)
        self.assertEqual(state["breaker"]["state"], "closed")
        self.assertEqual(state["breaker"]["closed_reason"], "provider_response_completed")

    def test_provider_registry_signal_helpers_distinguish_success_and_429(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-provider-signals-") as temporary:
            home = Path(temporary)
            logs = sqlite3.connect(home / "logs_2.sqlite")
            logs.execute("create table logs(ts integer, target text, feedback_log_body text)")
            logs.executemany("insert into logs values(?,?,?)", [
                (100, 'codex_api::sse::responses', 'SSE event: {"type":"response.created"}'),
                (122, 'unrelated', 'SSE event: {"type":"response.completed","response":{"status":"completed","error":null,"incomplete_details":null}}'),
                (123, 'codex_api::sse::responses', 'SSE event: {"type":"response.completed","response":{"status":"completed","error":null,"incomplete_details":null}}'),
            ]); logs.commit(); logs.close()
            history = sqlite3.connect(home / "thread_history_1.sqlite")
            history.execute("create table thread_turns(status text,error_json text,completed_at integer)")
            history.execute("insert into thread_turns values('failed','{\"message\":\"exceeded retry limit\",\"codexErrorInfo\":{\"responseTooManyFailedAttempts\":{\"httpStatusCode\":429}}}',140)")
            history.commit(); history.close()
            record = {"codex_home":str(home)}
            self.assertEqual(controller.provider_response_completed_at(record), 123.0)
            self.assertEqual(controller.provider_failure_completed_at(record), 140.0)

    def test_structured_429_retires_active_probe_before_goal_registry_propagates(self):
        recovery = sealed_prompt({})["recovery"]
        state = {"breaker":{"provider":controller.PROVIDER,"state":"half_open","consecutive_failures":0,"probe_generation_ids":["g0"]}}
        record = {"item_id":"A","run_id":"g0","generation_id":"g0","status":"live","recovery":recovery}
        with mock.patch.object(controller, "provider_failure_completed_at", return_value=1000.0):
            controller.update_provider_breaker(state, record)
        self.assertEqual(record["status"], "generation_retire_required")
        self.assertEqual(record["terminal_reason"], "provider_unavailable")
        self.assertEqual(state["breaker"]["consecutive_failures"], 1)

    def test_provider_signals_are_applied_in_completion_order(self):
        recovery = sealed_prompt({})["recovery"]
        state = {"breaker":{"provider":controller.PROVIDER,"state":"closed","consecutive_failures":0}}
        records = [
            {"run_id":"late-failure","generation_id":"late-failure","terminal_reason":"provider_unavailable","recovery":recovery},
            {"run_id":"early-failure","generation_id":"early-failure","terminal_reason":"provider_unavailable","recovery":recovery},
            {"run_id":"middle-success","generation_id":"middle-success","status":"live","recovery":recovery},
        ]
        signals = {
            "late-failure": (300.0, "failure"),
            "early-failure": (100.0, "failure"),
            "middle-success": (200.0, "success"),
        }
        with mock.patch.object(controller, "provider_signal", side_effect=lambda record, fallback_at=None: signals[record["run_id"]]):
            controller.update_provider_breaker_from_records(state, records)
        # failure, success reset, failure => one consecutive failure, not two.
        self.assertEqual(state["breaker"]["state"], "closed")
        self.assertEqual(state["breaker"]["consecutive_failures"], 1)

    def test_per_item_retry_due_comes_from_durable_history(self):
        state = {
            "generation_history": [
                {"item_id":"A", "generation_id":"g0", "terminal_reason":"provider_unavailable", "next_retry_at":100.0},
                {"item_id":"A", "generation_id":"g1", "terminal_reason":"provider_unavailable", "next_retry_at":240.0},
            ],
            "claims": {"A":{"item_id":"A", "generation_id":"g1", "terminal_reason":"provider_unavailable", "next_retry_at":240.0}},
        }
        self.assertEqual(controller.next_retry_at_for_item(state, "A"), 240.0)

    def test_newer_success_clears_older_provider_retry_due(self):
        state = {
            "generation_history": [
                {"item_id":"A", "generation_id":"g0", "terminal_reason":"provider_unavailable", "next_retry_at":1000.0},
                {"item_id":"A", "generation_id":"g1", "terminal_reason":"goal_terminal"},
            ],
            "claims": {"A":{"item_id":"A", "generation_id":"g1", "terminal_reason":"goal_terminal"}},
        }
        self.assertIsNone(controller.next_retry_at_for_item(state, "A"))

    def test_provider_backoff_streak_is_per_item_not_global_breaker_count(self):
        recovery = sealed_prompt({})["recovery"]
        state = {
            "generation_history": [
                {"item_id":"A", "generation_id":"a0", "run_id":"a0", "terminal_reason":"provider_unavailable", "recovery":recovery, "retired_epoch":1000.0},
                {"item_id":"B", "generation_id":"b0", "run_id":"b0", "terminal_reason":"provider_unavailable", "recovery":recovery, "retired_epoch":1000.0},
            ],
            "claims": {},
        }
        self.assertEqual(controller.provider_failure_streak_for_item(state, "A", "a0"), 1)
        self.assertEqual(controller.provider_failure_streak_for_item(state, "B", "b0"), 1)
        controller.rebuild_provider_retry_schedule(state)
        for record in state["generation_history"]:
            self.assertEqual(record["provider_failure_streak"], 1)
            self.assertGreaterEqual(record["next_retry_at"], 1048.0)
            self.assertLessEqual(record["next_retry_at"], 1072.0)

    def test_second_provider_failure_for_same_item_uses_120_second_base(self):
        recovery = sealed_prompt({})["recovery"]
        state = {
            "generation_history": [
                {"item_id":"A", "generation_id":"a0", "run_id":"a0", "terminal_reason":"provider_unavailable", "recovery":recovery, "retired_epoch":1000.0},
                {"item_id":"A", "generation_id":"a1", "run_id":"a1", "terminal_reason":"provider_unavailable", "recovery":recovery, "retired_epoch":2000.0},
            ],
            "claims": {},
        }
        self.assertEqual(controller.provider_failure_streak_for_item(state, "A", "a1"), 2)
        controller.rebuild_provider_retry_schedule(state)
        second = state["generation_history"][1]
        self.assertGreaterEqual(second["next_retry_at"], 2096.0)
        self.assertLessEqual(second["next_retry_at"], 2144.0)

    def test_claim_materialization_binds_read_only_bootstrap_files(self):
        source = PATH.read_text(encoding="utf-8")
        self.assertIn('"read_only_bootstrap_files":bootstrap_files', source)
        self.assertNotIn('"read_only_bootstrap_files":[]', source)
        self.assertIn('work / "_baseline/Stage5_Theorems_Blueprint.md",', source)
        self.assertIn("blueprint_raw,", source)
        self.assertNotIn('copy_file(BLUEPRINT, work / "_baseline/Stage5_Theorems_Blueprint.md")', source)

    def test_task_local_finalizer_is_materialized_and_result_writer_is_not_hand_authored(self):
        source = PATH.read_text(encoding="utf-8")
        self.assertIn("def render_finalizer()", source)
        self.assertIn('work / "_baseline/finalize.py"', source)
        self.assertIn('atomic_write(work / "_baseline/finalize.py", render_finalizer(), 0o555)', source)
        self.assertIn('sha(canonical(command["argv"]))', source)
        self.assertIn('TASK / "changes.patch"', source)
        self.assertIn("run only `python3 _baseline/finalize.py`", source)
        self.assertIn("complete run python3 _baseline/finalize.py", source)
        self.assertIn("complete-target-semantic-proof-debt", source)
        self.assertNotIn('"-c","pass"', source)
        self.assertIn("item_checker().validate_target", source)
        self.assertIn('str(work),"--no-lean"', source)
        self.assertIn('copy_checkpoint_bootstrap(', source)

    def test_task_local_finalizer_derives_result_from_real_bytes_and_command(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-finalizer-") as temporary:
            task = Path(temporary) / "task"
            work = task / "work"
            baseline = work / "_baseline"
            owned = work / "Docs/proof.md"
            baseline.mkdir(parents=True)
            owned.parent.mkdir(parents=True)
            owned.write_text("# Verified proof\n\nActual artifact bytes.\n", encoding="utf-8")
            finalizer = baseline / "finalize.py"
            finalizer.write_bytes(controller.render_finalizer())
            finalizer.chmod(0o555)
            command = {
                "command_id": "fixture-validation",
                "cwd": str(work),
                "argv": [
                    "/usr/bin/python3", "-c",
                    "import pathlib; print(pathlib.Path('Docs/proof.md').read_text())",
                ],
                "environment": [],
                "timeout_seconds": 30,
                "network": "denied",
            }
            claim = {
                "program": controller.PROGRAM,
                "claim_id": "S5THM-TEST--worker",
                "run_id": "r-finalizer-test",
                "item_id": "S5THM-TEST-TARGET",
                "mode": "TARGET-TARGET",
                "task_root": str(task),
                "writable_paths": ["Docs/proof.md"],
                "validation_commands": [command],
                "baseline": {"fixture": "exact"},
            }
            claim_path = task / "claim.json"
            claim_path.write_text(
                json.dumps(claim, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                ["/usr/bin/python3", str(finalizer)], cwd=work,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr.decode())
            patch_path = task / "changes.patch"
            result_path = work / "_outbox/result.json"
            result = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(result["claim_card_sha256"], controller.file_digest(claim_path))
            self.assertEqual(
                result["baseline_sha256"],
                controller.digest(controller.canonical(claim["baseline"])),
            )
            self.assertEqual(result["changed_paths"], claim["writable_paths"])
            self.assertEqual(result["patch"]["path"], str(patch_path))
            self.assertEqual(result["patch"]["sha256"], controller.file_digest(patch_path))
            self.assertEqual(result["artifacts"][0]["path"], str(owned))
            self.assertEqual(result["artifacts"][0]["sha256"], controller.file_digest(owned))
            outcome = result["command_outcomes"][0]
            self.assertEqual(
                outcome["argv_sha256"],
                controller.digest(controller.canonical(command["argv"])),
            )
            self.assertTrue(outcome["passed"])
            self.assertEqual(outcome["exit_code"], 0)
            unsigned = dict(result)
            authority = unsigned.pop("authority_sha256")
            self.assertEqual(authority, controller.digest(controller.canonical(unsigned)))
            controller._patch_paths(patch_path.read_bytes(), claim["writable_paths"])

    def test_checkpoint_bootstrap_requires_complete_content_binding(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-checkpoint-bootstrap-") as temporary:
            root = Path(temporary)
            original_runtime = controller.RUNTIME
            controller.RUNTIME = root / "runtime"
            item_id = "S5THM-00003493-TARGET"
            generation_id = "r-predecessor-aaaa"
            checkpoint_dir = controller.RUNTIME / "checkpoints" / item_id / generation_id
            artifact_path = checkpoint_dir / "artifacts/Docs/proof.md"
            artifact_path.parent.mkdir(parents=True)
            artifact_raw = b"durable proof progress\n"
            artifact_path.write_bytes(artifact_raw)
            body = {
                "schema_version": "awesome-theorems/stage5-terminal-disposition/1.0",
                "program": controller.PROGRAM,
                "item_id": item_id,
                "claim_id": f"{item_id}--worker",
                "run_id": generation_id,
                "generation_id": generation_id,
                "checkpoint_sequence": 2,
                "checkpoint_reusable": True,
                "artifact_manifest": [
                    {
                        "path": "Docs/proof.md",
                        "sha256": controller.digest(artifact_raw),
                        "size_bytes": len(artifact_raw),
                        "reusable": True,
                    },
                    {
                        "path": "Docs/not-reusable.md",
                        "sha256": "0" * 64,
                        "size_bytes": 0,
                        "reusable": False,
                    },
                ],
            }
            checkpoint = controller.seal(body)
            checkpoint_dir.with_suffix(".json").parent.mkdir(parents=True, exist_ok=True)
            checkpoint_dir.with_suffix(".json").write_text(
                json.dumps(checkpoint, sort_keys=True), encoding="utf-8",
            )
            try:
                work = root / "valid-work"
                work.mkdir()
                copied = controller.copy_checkpoint_bootstrap(work, item_id, generation_id)
                self.assertIsNotNone(copied)
                self.assertEqual(copied["artifact_count"], 1)
                copied_artifact = work / "_baseline/checkpoints" / generation_id / "artifacts/Docs/proof.md"
                self.assertEqual(copied_artifact.read_bytes(), artifact_raw)
                self.assertFalse(
                    (work / "_baseline/checkpoints" / generation_id / "artifacts/Docs/not-reusable.md").exists()
                )

                artifact_path.write_bytes(b"tampered\n")
                rejected_work = root / "rejected-work"
                rejected_work.mkdir()
                self.assertIsNone(
                    controller.copy_checkpoint_bootstrap(rejected_work, item_id, generation_id)
                )
                self.assertFalse((rejected_work / "_baseline/checkpoints").exists())
            finally:
                controller.RUNTIME = original_runtime

    def test_checkpoint_bootstrap_rejects_wrong_lineage_without_copy(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-checkpoint-lineage-") as temporary:
            root = Path(temporary)
            original_runtime = controller.RUNTIME
            controller.RUNTIME = root / "runtime"
            item_id = "S5THM-00003493-TARGET"
            generation_id = "r-predecessor-bbbb"
            target = controller.RUNTIME / "checkpoints" / item_id / f"{generation_id}.json"
            target.parent.mkdir(parents=True)
            target.write_text(json.dumps(controller.seal({
                "program": controller.PROGRAM,
                "item_id": item_id,
                "run_id": "different-run",
                "generation_id": generation_id,
                "checkpoint_reusable": True,
                "artifact_manifest": [],
            })), encoding="utf-8")
            try:
                work = root / "work"
                work.mkdir()
                self.assertIsNone(controller.copy_checkpoint_bootstrap(work, item_id, generation_id))
                self.assertFalse((work / "_baseline/checkpoints").exists())
                self.assertIsNone(controller.copy_checkpoint_bootstrap(work, item_id, None))
            finally:
                controller.RUNTIME = original_runtime

    def test_worker_preflight_skips_lean_but_master_still_compiles(self):
        source = PATH.read_text(encoding="utf-8")
        self.assertIn('str(work),"--no-lean"', source)
        self.assertIn("do not invoke Lean, Lake or Elan", source)
        self.assertIn("do not clone,", source)
        self.assertIn("fetch or reconstruct any repository", source)
        self.assertIn("Master alone performs ", source)
        self.assertIn("provider-native trust-zero Lean compilation after harvest", source)
        self.assertIn("provider-native trust-zero Lean compilation", source)
        self.assertIn("`_baseline/provider-kernel-route.json`", source)
        self.assertIn("must actively import its exact `lean_module`", source)
        self.assertIn("type_of% <qualified_declaration>", source)
        self.assertIn("Independently prove ", source)
        self.assertIn('"Obey immutable ../claim.json; work only here. Use writable_paths and _baseline. "', source)
        self.assertIn('"No parent/canonical/other-task access, child threads, collaboration, clone, fetch, "', source)
        self.assertIn('"complete run python3 _baseline/finalize.py; it writes _outbox/result.json and "', source)
        self.assertIn('"../changes.patch. Finish with the completion token "', source)
        self.assertNotIn("all result paths must be absolute inside this generation", source)
        self.assertGreaterEqual(source.count("compile_files=True"), 2)

    def test_semantic_revocation_replay_is_monotone_across_stronger_validators(self):
        source = PATH.read_text(encoding="utf-8")
        self.assertIn(
            "invalidated semantic generation now passes its frozen replay", source,
        )
        self.assertIn(
            "diagnostic wording is not a cross-version authority", source,
        )
        self.assertNotIn(
            "semantic credit invalidation replay failure differs", source,
        )

    def test_revoked_master_receipt_cannot_resurrect_runtime_credit(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-revoked-receipt-") as temporary:
            root = Path(temporary)
            archive = root / "handoffs"
            integration = root / "integration"
            runtime = root / "runtime"
            archive.mkdir(); integration.mkdir(); runtime.mkdir()
            item_id = "S5THM-00003528-TARGET"
            run_id = "r-revoked"
            receipt_path = archive / item_id / "claim" / run_id / "master-integration.json"
            receipt_path.parent.mkdir(parents=True)
            receipt = controller.seal({
                "item_id": item_id, "accepted_at": "2026-08-17T12:16:40Z",
                "handoff": {"run_id": run_id, "patch_sha256": "a" * 64},
            })
            receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
            receipt_sha = controller.file_digest(receipt_path)
            state = {"claims": {item_id: {
                "item_id": item_id, "run_id": run_id,
                "status": "master_accepted", "work_state": "master_accepted",
                "master_accepted_at": "2026-08-17T12:16:40Z",
                "integration": {"acceptance_path": str(receipt_path)},
            }}}
            originals = (
                controller.HANDOFF_ARCHIVE, controller.INTEGRATION_QUEUE,
                controller.RUNTIME,
            )
            controller.HANDOFF_ARCHIVE = archive
            controller.INTEGRATION_QUEUE = integration
            controller.RUNTIME = runtime
            try:
                with (
                    mock.patch.object(controller, "save_state"),
                ):
                    self.assertEqual(controller.reconcile_integrated_handoffs(
                        state, {(item_id, run_id, receipt_sha): {
                            "replay_failure_sha256": "b" * 64,
                        }},
                    ), 1)
                record = state["claims"][item_id]
                self.assertEqual(record["status"], "invalidated")
                self.assertEqual(record["work_state"], "not_done")
                self.assertEqual(
                    record["invalidated_master_acceptance_sha256"], receipt_sha,
                )
                self.assertNotIn("master_accepted_at", record)
                self.assertNotIn("integration", record)
            finally:
                (
                    controller.HANDOFF_ARCHIVE, controller.INTEGRATION_QUEUE,
                    controller.RUNTIME,
                ) = originals

    def test_missing_pinned_formal_conjectures_provider_fails_closed(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-provider-") as temporary:
            work = Path(temporary) / "work"
            work.mkdir()
            item = {"item_id": "S5THM-00003514-TARGET"}
            original_root = controller.ROOT
            controller.ROOT = Path(temporary) / "canonical"
            try:
                with self.assertRaisesRegex(controller.ControllerError, "provider source checkout unavailable"):
                    controller.copy_provider_sources(work, item)
            finally:
                controller.ROOT = original_root

    def test_materializes_exact_provider_kernel_routes_for_both_catalogs(self):
        cases = (
            (
                "S5THM-00003485-TARGET",
                "formal-conjectures-2270d31e",
                "leanprover/lean4:v4.27.0",
                "Formalizations/Lean/.lake/packages/formal-conjectures",
            ),
            (
                "S5THM-00006585-TARGET",
                "mathlib-8a178386",
                "leanprover/lean4:v4.29.0",
                "Formalizations/Lean",
            ),
        )
        with tempfile.TemporaryDirectory(prefix="stage5-v2-provider-routes-") as temporary:
            for item_id, provider_id, toolchain, environment in cases:
                with self.subTest(provider=provider_id):
                    work = Path(temporary) / provider_id
                    work.mkdir()
                    controller.copy_provider_sources(work, {"item_id": item_id})
                    route_path = work / "_baseline/provider-kernel-route.json"
                    route = controller.verify_seal(
                        controller.strict_json(route_path.read_bytes(), "provider route"),
                        "provider route",
                    )
                    self.assertEqual(route["provider_id"], provider_id)
                    self.assertEqual(route["toolchain"], toolchain)
                    self.assertEqual(route["master_environment"], environment)
                    self.assertEqual(route["proof_authority"], "claim_owned_root_only")
                    self.assertFalse(route["provider_body_authority"])
                    source_root = (
                        work / "_baseline/provider-sources" / provider_id / route["revision"]
                    )
                    self.assertTrue(any(path.is_file() for path in source_root.rglob("*.lean")))

    def test_launch_failure_is_registered_and_retired_before_retry(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-launch-recovery-") as temporary:
            original_runtime, original_state = controller.RUNTIME, controller.STATE_PATH
            controller.RUNTIME = Path(temporary) / "runtime"
            controller.STATE_PATH = controller.RUNTIME / "state/controller-state.json"
            controller.RUNTIME.mkdir(parents=True)
            record = {
                "item_id": "S5THM-00003485-TARGET",
                "claim_id": "S5THM-00003485-TARGET--worker",
                "run_id": "r-failed-aaaa",
                "task_root": str(controller.RUNTIME / "tasks" / "claim" / "r-failed-aaaa"),
                "socket_argument": "tmux.sock",
                "status": "materialized",
            }
            state = controller.load_state()
            with mock.patch.object(controller, "stop_record"), mock.patch.object(controller, "append_event"):
                controller.retire_launch_failure(state, record, controller.ControllerError("registry timeout"))
            persisted = controller.load_state(False)
            self.assertEqual(persisted["claims"][record["item_id"]]["status"], "retired")
            self.assertIn("launch_failed", persisted["claims"][record["item_id"]]["retired_reason"])
            self.assertEqual(len(persisted["generation_history"]), 1)
            controller.RUNTIME, controller.STATE_PATH = original_runtime, original_state

    def test_terminal_retirement_persists_typed_disposition_before_fencing(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-terminal-disposition-") as temporary:
            original_runtime, original_state = controller.RUNTIME, controller.STATE_PATH
            controller.RUNTIME = Path(temporary) / "runtime"
            controller.STATE_PATH = controller.RUNTIME / "state/controller-state.json"
            controller.RUNTIME.mkdir(parents=True)
            record = {
                "item_id": "S5THM-00003493-TARGET",
                "claim_id": "S5THM-00003493-TARGET--worker",
                "run_id": "r-terminal-aaaa",
                "generation_id": "r-terminal-aaaa",
                "lane_id": "S5THM-00003493-TARGET",
                "task_root": str(controller.RUNTIME / "tasks" / "claim" / "r-terminal-aaaa"),
                "status": "generation_retire_required",
                "terminal_reason": "goal_terminal",
                "retired_reason": "goal_terminal:complete:goal_terminal",
                "prompt_epoch": "epoch",
                "prompt_digest": "a" * 64,
                "execution_spec_sha256": "b" * 64,
                "replacement_ordinal": 2,
                "previous_generation_id": "r-terminal-prev",
            }
            state = {"claims": {}, "generation_history": []}
            with (
                mock.patch.object(controller, "stop_record"),
                mock.patch.object(controller, "append_event"),
                mock.patch.object(controller, "save_state"),
            ):
                controller.retire_launch_failure(state, record, controller.ControllerError("missing worker result"))
            receipt = record["terminal_disposition"]
            self.assertEqual(receipt["kind"], "proof_blocked_with_evidence")
            self.assertFalse(receipt["master_credit"])
            path = Path(receipt["path"])
            self.assertTrue(path.is_file())
            body = controller.verify_seal(controller.strict_json(path.read_bytes(), "terminal disposition"), "terminal disposition")
            self.assertEqual(body["run_id"], "r-terminal-aaaa")
            self.assertFalse(body["master_credit"])
            self.assertEqual(body["repair_diagnostic"]["source"], "retirement_error")
            self.assertEqual(body["repair_diagnostic"]["text"], "missing worker result")
            self.assertEqual(
                body["repair_diagnostic"]["text_sha256"],
                controller.digest(b"missing worker result"),
            )
            self.assertFalse(body["repair_diagnostic"]["truncated"])
            self.assertEqual(state["generation_history"][0]["checkpoint"]["sha256"], receipt["sha256"])
            controller.RUNTIME, controller.STATE_PATH = original_runtime, original_state

    def test_checkpoint_preserves_bounded_redacted_master_validation_diagnostic(self):
        with tempfile.TemporaryDirectory(prefix="stage5-v2-checkpoint-diagnostic-") as temporary:
            original_runtime, original_state = controller.RUNTIME, controller.STATE_PATH
            controller.RUNTIME = Path(temporary) / "runtime"
            controller.STATE_PATH = controller.RUNTIME / "state/controller-state.json"
            task = controller.RUNTIME / "tasks/claim/r-validation-aaaa"
            work = task / "work"
            owned = "Stage5_Theorem_Instances/S5-CLM-00003504/build-validation.md"
            (work / owned).parent.mkdir(parents=True)
            (work / owned).write_text("diagnostic fixture\n")
            master_error = (
                f"Lean trust-zero elaboration failed: {work}/Formalizations/Proof.lean:17:3: "
                f"canonical={controller.ROOT}/Formalizations/Lean; " + "x" * 5000
            )
            record = {
                "item_id":"S5THM-00003504-TARGET",
                "claim_id":"S5THM-00003504-TARGET--worker",
                "run_id":"r-validation-aaaa",
                "generation_id":"r-validation-aaaa",
                "lane_id":"S5THM-00003504-TARGET",
                "task_root":str(task), "work_root":str(work),
                "status":"generation_retire_required",
                "terminal_reason":"goal_terminal",
                "retired_reason":"goal_terminal:complete:goal_terminal",
                "harvest_error":master_error,
                "prompt_epoch":"epoch", "prompt_digest":"a" * 64,
                "execution_spec_sha256":"b" * 64,
                "replacement_ordinal":3, "previous_generation_id":"r-prev",
                "owned_paths":[owned],
            }
            try:
                with mock.patch.object(controller, "append_event"):
                    body = controller.write_terminal_disposition(
                        record, controller.ControllerError(record["retired_reason"]),
                    )
                diagnostic = body["repair_diagnostic"]
                self.assertEqual(diagnostic["source"], "harvest_error")
                self.assertTrue(diagnostic["truncated"])
                self.assertEqual(len(diagnostic["text"]), 4000)
                self.assertIn("<work_root>/Formalizations/Proof.lean", diagnostic["text"])
                self.assertIn("canonical=<canonical_root>/Formalizations/Lean", diagnostic["text"])
                self.assertNotIn(str(task), diagnostic["text"])
                self.assertNotIn(str(controller.ROOT), diagnostic["text"])
                self.assertEqual(
                    diagnostic["text_sha256"],
                    controller.digest(diagnostic["text"].encode("utf-8")),
                )
                checkpoint = Path(record["checkpoint"]["path"])
                persisted = controller.verify_seal(
                    controller.strict_json(checkpoint.read_bytes(), "diagnostic checkpoint"),
                    "diagnostic checkpoint",
                )
                self.assertEqual(persisted["repair_diagnostic"], diagnostic)
            finally:
                controller.RUNTIME, controller.STATE_PATH = original_runtime, original_state


if __name__ == "__main__":
    unittest.main()
