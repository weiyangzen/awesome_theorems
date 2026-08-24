#!/usr/bin/env python3
"""Adversarial tests for the Stage3 v3 authority and atomic monitoring projection."""

from __future__ import annotations

from collections import Counter
from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = _load_module(
    "check_stage3_blueprint_for_tests", ROOT / "Docs" / "tools" / "check_stage3_blueprint.py"
)
generator = _load_module(
    "generate_stage3_surfaces_for_tests", ROOT / "Docs" / "tools" / "generate_stage3_surfaces.py"
)


class Stage3BlueprintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.blueprint = (ROOT / "Docs" / "Stage3_Blueprint.md").read_bytes().decode("utf-8")
        cls.gantt = (ROOT / "Docs" / "Stage3_Gantt.md").read_bytes().decode("utf-8")
        cls.status = (ROOT / "Docs" / "Stage3_Status.json").read_bytes().decode("utf-8")
        cls.kanban = (ROOT / "Docs" / "Stage3_Kanban.md").read_bytes().decode("utf-8")
        cls.tasks = checker.parse_tasks(cls.blueprint)
        cls.metadata = checker.parse_surface_metadata(cls.gantt, "Gantt")

    def assert_invalid(
        self,
        *,
        blueprint: str | None = None,
        gantt: str | None = None,
        status: str | None = None,
        kanban: str | None = None,
        runtime_snapshot: str | None = None,
        cleanup_receipt: str | None = None,
    ) -> None:
        with self.assertRaises(checker.ValidationError):
            checker.validate_texts(
                self.blueprint if blueprint is None else blueprint,
                self.gantt if gantt is None else gantt,
                self.status if status is None else status,
                self.kanban if kanban is None else kanban,
                runtime_snapshot,
                cleanup_receipt,
            )

    def replace_field(self, item_id: str, field: str, value: str, *, blueprint: str | None = None) -> str:
        source = self.blueprint if blueprint is None else blueprint
        pattern = re.compile(
            rf"(^- \[[ _x]\] `{re.escape(item_id)}` .*? \| {re.escape(field)}=)([^|]*?)(?= \|)",
            flags=re.MULTILINE,
        )
        mutated, count = pattern.subn(rf"\g<1>{value}", source, count=1)
        self.assertEqual(count, 1, f"could not mutate {item_id}.{field}")
        return mutated

    def replace_state(self, item_id: str, state: str) -> str:
        pattern = re.compile(rf"^- \[[ _x]\] (`{re.escape(item_id)}`)", flags=re.MULTILINE)
        mutated, count = pattern.subn(rf"- [{state}] \1", self.blueprint, count=1)
        self.assertEqual(count, 1)
        return mutated

    def checklist_row(self, item_id: str) -> str:
        return next(line for line in self.blueprint.splitlines() if line.startswith("- [") and f"`{item_id}`" in line)

    def monitor_row(self, item_id: str) -> str:
        return next(line for line in self.gantt.splitlines() if line.startswith(f'| `"{item_id}"` |'))

    def mutate_all_metadata(self, key: str, replacement: str) -> tuple[str, str, str]:
        old = self.metadata[key]
        self.assertIsInstance(old, str)
        self.assertNotEqual(old, replacement)
        return (
            self.gantt.replace(old, replacement),
            self.status.replace(old, replacement),
            self.kanban.replace(old, replacement),
        )

    def runtime_snapshot_payload(
        self,
        blueprint: str | None = None,
        tasks: dict[str, object] | None = None,
    ) -> dict[str, object]:
        blueprint = self.blueprint if blueprint is None else blueprint
        tasks = self.tasks if tasks is None else tasks
        spec_digest = checker.sha256_text(
            checker.exact_marked_region(
                blueprint, checker.SPEC_BEGIN, checker.SPEC_END, "execution specification"
            )
        )
        ready_ids = checker.planning_projection(tasks)["frontiers"]["implementation_ready"]
        observed_at = "2026-08-09T22:40:00Z"

        def evidence(source: str, evidence_payload: dict[str, object]) -> dict[str, object]:
            return {
                "source": source,
                "payload": evidence_payload,
                "sha256": checker.canonical_json_sha256(evidence_payload),
            }

        def spec_binding(kind: str, limit: int, reason: str, field: str) -> dict[str, object]:
            evidence_payload = {
                "field": field,
                "limit": limit,
                "execution_spec_region_sha256": spec_digest,
            }
            return {
                "kind": kind,
                "limit": limit,
                "reason": reason,
                "evidence": evidence(
                    "Docs/Stage3_Blueprint.md#STAGE3-EXECUTION-SPEC", evidence_payload
                ),
            }

        def observed_binding(
            kind: str,
            limit: int,
            reason: str | None,
            basis: str,
            extra: dict[str, object] | None = None,
        ) -> dict[str, object]:
            evidence_payload = {"limit": limit, "observed_at": observed_at, "basis": basis}
            evidence_payload.update(extra or {})
            return {
                "kind": kind,
                "limit": limit,
                "reason": reason,
                "evidence": evidence(
                    f".ops/stage3-execution-v1/status/admission/{kind}.json", evidence_payload
                ),
            }

        eligible_payload = {
            "ids": ready_ids,
            "limit": len(ready_ids),
            "raw_blueprint_sha256": checker.sha256_text(blueprint),
        }
        effective_bindings = [
            spec_binding("logical_cap", 6, "frozen logical ceiling", "requested logical-claim ceiling"),
            observed_binding("logical_available", 6, "logical cap minus nonoccupancy claims", "logical_cap_minus_nonoccupancy_claims"),
            spec_binding("authenticated_live_cap", 6, "frozen live ceiling", "authenticated-live and running-turn ceilings"),
            spec_binding("running_turn_cap", 6, "frozen running ceiling", "authenticated-live and running-turn ceilings"),
            spec_binding("requested", 6, "operator-requested ceiling", "requested logical-claim ceiling"),
            {
                "kind": "eligible",
                "limit": len(ready_ids),
                "reason": "exact dependency-ready frontier",
                "evidence": evidence(
                    "Docs/Stage3_Blueprint.md#STAGE3-EXECUTION-CHECKLIST", eligible_payload
                ),
            },
            observed_binding(
                "host_resource", 6, "fixture host observation", "host headroom allows six",
                {
                    "available_ram_bytes": 32 * 1024**3,
                    "free_disk_bytes": 200 * 1024**3,
                    "load_1m": 1.0,
                    "swap_exhausted": False,
                    "pid_limit": 4096,
                    "pid_usage": 128,
                    "pid_source": "fixture-cgroup",
                },
            ),
            observed_binding("conflict", 6, None, "no path conflict", {"conflicting_pairs": []}),
            observed_binding(
                "external_limit", 6, None, "provider rate observation allows six",
                {"decisions": [{"name": "fixture-provider", "decision": "allow", "limit": 6, "observed_at": observed_at}]},
            ),
            observed_binding(
                "route", 6, None, "route observation allows six",
                {"routes": [{"route_id": "fixture-route", "available": True, "limit": 6, "observed_at": observed_at}]},
            ),
            observed_binding(
                "validator", 6, None, "validator leases allow six claims",
                {"lease_target": 4, "active_leases": 0},
            ),
            observed_binding(
                "budget", 6, None, "pump budget allows six",
                {
                    "pump_started_at": "2026-08-09T22:39:30Z",
                    "pump_deadline_at": "2026-08-09T22:41:00Z",
                    "remaining_seconds": 60,
                },
            ),
        ]

        target_reason_text = "eligible frontier reduces the requested target"
        target_reason_payload = {
            "kind": "dependency",
            "reason": target_reason_text,
            "observed_at": observed_at,
            "admitted_target": len(ready_ids),
            "requested_target": 6,
        }
        occupancy_reason_text = "fixture records no admitted live or starting claim"
        occupancy_reason_payload = {
            "kind": "no_progress",
            "reason": occupancy_reason_text,
            "observed_at": observed_at,
            "occupancy": 0,
            "admitted_target": len(ready_ids),
            "pump_started_at": "2026-08-09T22:39:30Z",
            "pump_deadline_at": "2026-08-09T22:41:00Z",
            "reconciliation_iteration": 3,
            "no_progress_limit": 3,
        }
        payload = {
            "schema_version": checker.RUNTIME_SCHEMA,
            "snapshot_id": "pending",
            "blueprint_version": checker.VERSION,
            "raw_blueprint_sha256": checker.sha256_text(blueprint),
            "execution_spec_region_sha256": spec_digest,
            "observed_at": observed_at,
            "last_progress": None,
            "cleanup_state": "not_started",
            "cleanup_arm": None,
            "admission": {
                "logical_claim_target": 6,
                "startup_reservation_target": 4,
                "authenticated_live_target": 6,
                "running_turn_target": 6,
                "admitted_target": len(ready_ids),
                "eligible_ready_count": len(ready_ids),
                "requested_target": 6,
                "host_admissible_target": 6,
                "master_integration_target": 1,
                "cpu_validator_lease_target": 4,
                "active_cpu_validator_leases": 0,
                "effective_target_bindings": effective_bindings,
                "underfill_stop_reason": {
                    "kind": "dependency",
                    "reason": target_reason_text,
                    "evidence": evidence(
                        ".ops/stage3-execution-v1/status/admission/target-reduction.json",
                        target_reason_payload,
                    ),
                },
                "occupancy_underfill_reason": {
                    "kind": "no_progress",
                    "reason": occupancy_reason_text,
                    "evidence": evidence(
                        ".ops/stage3-execution-v1/status/admission/occupancy-underfill.json",
                        occupancy_reason_payload,
                    ),
                },
            },
            "items": [
                {
                    "id": item_id,
                    "claim_id": None,
                    "run_id": None,
                    "owner": None,
                    "observation_evidence": {
                        "source": f".ops/stage3-execution-v1/status/items/{item_id}.json",
                        "sha256": "a" * 64,
                        "observed_at": observed_at,
                        "payload": {},
                    },
                    "startup": None,
                    "startup_evidence": None,
                    "live": False,
                    "live_evidence": None,
                    "running": False,
                    "handoff": None,
                    "integration": None,
                    "repair": None,
                    "runtime_block": None,
                    "timing": checker.unavailable_timing(),
                }
                for item_id in sorted(tasks)
            ],
        }
        self.refresh_runtime_id(payload)
        return payload

    @staticmethod
    def refresh_runtime_id(payload: dict[str, object]) -> None:
        items = payload["items"]
        admission = payload["admission"]
        occupancy = sum(
            item["live"] is True
            or item["startup"] in (checker.STARTUP_STATES - {"reserved"})
            for item in items
        )
        nonoccupancy_claims = sum(
            item["claim_id"] is not None
            and item["live"] is not True
            and item["startup"] not in (checker.STARTUP_STATES - {"reserved"})
            for item in items
        )
        logical_available = max(0, admission["logical_claim_target"] - nonoccupancy_claims)
        logical_binding = next(
            binding
            for binding in admission["effective_target_bindings"]
            if binding["kind"] == "logical_available"
        )
        logical_binding["limit"] = logical_available
        logical_binding["evidence"]["payload"]["limit"] = logical_available
        logical_binding["evidence"]["sha256"] = checker.canonical_json_sha256(
            logical_binding["evidence"]["payload"]
        )
        target_reason = admission["underfill_stop_reason"]
        if target_reason is not None:
            target_reason["evidence"]["payload"] = {
                "kind": target_reason["kind"],
                "reason": target_reason["reason"],
                "observed_at": payload["observed_at"],
                "admitted_target": admission["admitted_target"],
                "requested_target": admission["requested_target"],
            }
            target_reason["evidence"]["sha256"] = checker.canonical_json_sha256(
                target_reason["evidence"]["payload"]
            )
        occupancy_reason = admission["occupancy_underfill_reason"]
        if occupancy < admission["admitted_target"]:
            if occupancy_reason is None:
                reason_text = "fixture records an admitted occupancy underfill"
                occupancy_reason = {
                    "kind": "no_progress",
                    "reason": reason_text,
                    "evidence": {
                        "source": ".ops/stage3-execution-v1/status/admission/occupancy-underfill.json",
                        "payload": {},
                        "sha256": "",
                    },
                }
                admission["occupancy_underfill_reason"] = occupancy_reason
            occupancy_reason["evidence"]["payload"] = {
                "kind": occupancy_reason["kind"],
                "reason": occupancy_reason["reason"],
                "observed_at": payload["observed_at"],
                "occupancy": occupancy,
                "admitted_target": admission["admitted_target"],
                "pump_started_at": "2026-08-09T22:39:30Z",
                "pump_deadline_at": "2026-08-09T22:41:00Z",
                "reconciliation_iteration": 3,
                "no_progress_limit": 3,
            }
            occupancy_reason["evidence"]["sha256"] = checker.canonical_json_sha256(
                occupancy_reason["evidence"]["payload"]
            )
        else:
            admission["occupancy_underfill_reason"] = None
        for item in items:
            if item["live_evidence"] is not None:
                route = item["live_evidence"]["route"]
                item["live_evidence"]["route_sha256"] = checker.canonical_json_sha256(route)
            observation_payload = checker.runtime_observation_payload(item)
            observation_digest = checker.canonical_json_sha256(observation_payload)
            item["observation_evidence"] = {
                "source": checker.runtime_observation_source(item),
                "sha256": observation_digest,
                "observed_at": payload["observed_at"],
                "payload": observation_payload,
            }
            if item["startup_evidence"] is not None:
                item["startup_evidence"]["identity_evidence_sha256"] = observation_digest
            if item["live_evidence"] is not None:
                item["live_evidence"]["identity_evidence_sha256"] = observation_digest
        payload["snapshot_id"] = checker.content_addressed_id("stage3-runtime", payload, "snapshot_id")

    @staticmethod
    def live_evidence(item_id: str, claim_id: str, run_id: str) -> dict[str, object]:
        task_root = f".ops/stage3-execution-v1/tasks/{claim_id}/{run_id}"
        route = {
            "provider": "openai",
            "model": "fixture-model",
            "reasoning_effort": "medium",
            "service_tier": "priority",
        }
        return {
            "authenticated_at": "2026-08-09T22:39:59Z",
            "identity_evidence_sha256": "b" * 64,
            "tmux_socket": f"{task_root}/tmux.sock",
            "session": "stage3-fixture",
            "pane_pid": 12345,
            "process_start_ticks": 67890,
            "cwd": f"{task_root}/work",
            "codex_home": f"{task_root}/codex-home",
            "thread_id": "thread-fixture",
            "goal_id": "goal-fixture",
            "goal_status": "active",
            "goal_item_id": item_id,
            "goal_claim_id": claim_id,
            "goal_objective": f"Complete {item_id} for claim {claim_id}",
            "route": route,
            "route_sha256": checker.canonical_json_sha256(route),
            "process_observed_at": "2026-08-09T22:40:00Z",
            "process_alive": True,
        }

    @staticmethod
    def startup_evidence(*, stale: bool = False) -> dict[str, object]:
        return {
            "state_entered_at": "2026-08-09T22:35:00Z",
            "deadline_at": "2026-08-09T22:39:00Z" if stale else "2026-08-09T22:50:00Z",
            "identity_evidence_sha256": "d" * 64,
            "process_identity": None,
        }

    @staticmethod
    def encode_runtime(payload: dict[str, object]) -> str:
        return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    def all_accepted_blueprint(self) -> str:
        return re.sub(r"^- \[[ _]\] (`S3-)", r"- [x] \1", self.blueprint, flags=re.MULTILINE)

    @staticmethod
    def cleanup_verifier_bytes() -> bytes:
        return b"#!/usr/bin/env python3\n# deterministic cleanup verifier fixture\n"

    def pre_cleanup_receipt_payload(self, blueprint: str) -> dict[str, object]:
        tasks = checker.parse_tasks(blueprint)
        runtime_payload = self.runtime_snapshot_payload(blueprint, tasks)
        runtime_text = self.encode_runtime(runtime_payload)
        runtime = checker.parse_runtime_snapshot(runtime_text, tasks, blueprint)
        generated_at = "2026-08-09T22:40:00Z"
        metadata = checker.build_projection_metadata(
            blueprint,
            generated_at,
            runtime_snapshot_sha256=checker.sha256_text(runtime_text),
            runtime_snapshot_id=runtime["snapshot_id"],
        )
        archived = {
            "gantt": generator.generate_gantt(tasks, metadata, runtime),
            "status": generator.generate_status(tasks, metadata, runtime),
            "kanban": generator.generate_kanban(tasks, metadata, runtime),
        }
        checker.validate_texts(
            blueprint,
            archived["gantt"],
            archived["status"],
            archived["kanban"],
            runtime_text,
        )
        teardown_inventory = {
            "cron": [{
                "begin_marker": "# BEGIN AWESOME_THEOREMS_STAGE3_EXECUTION_V1",
                "end_marker": "# END AWESOME_THEOREMS_STAGE3_EXECUTION_V1",
            }],
            "scheduler": [{
                "pid": 4242,
                "process_start_ticks": 8675309,
                "cwd": ".",
                "argv": ["python3", "scripts/stage3_execution_scheduler.py"],
            }],
            "task_processes": [],
            "tmux_sockets": [],
            "locks": [".ops/stage3-execution-v1/locks/scheduler.lock"],
            "runtime_root": [".ops/stage3-execution-v1/"],
        }
        payload = {
            "schema_version": checker.PRE_CLEANUP_RECEIPT_SCHEMA,
            "receipt_id": "pending",
            "state": "cleanup_pending",
            "armed_at": "2026-08-09T22:40:00Z",
            "blueprint_path": "Docs/Stage3_Blueprint.md",
            "blueprint_version": checker.VERSION,
            "raw_blueprint_sha256": checker.sha256_text(blueprint),
            "execution_spec_region_sha256": checker.sha256_text(
                checker.exact_marked_region(
                    blueprint, checker.SPEC_BEGIN, checker.SPEC_END, "execution specification"
                )
            ),
            "rel005_state": "master_accepted",
            "all_other_items_master_accepted": True,
            "unfinished": {"not_done": 0, "self_tested": 0},
            "queues_empty": {"handoff": True, "integration": True, "repair": True, "checkpoint": True},
            "teardown_inventory": teardown_inventory,
            "teardown_inventory_sha256": checker.canonical_json_sha256(teardown_inventory),
            "final_pre_teardown_projection": {
                "snapshot_id": metadata["snapshot_id"],
                "projection_input_sha256": metadata["projection_input_sha256"],
                "generated_at": generated_at,
                "surfaces": {
                    name: {
                        "path": {
                            "gantt": "Docs/Stage3_Gantt.md",
                            "status": "Docs/Stage3_Status.json",
                            "kanban": "Docs/Stage3_Kanban.md",
                        }[name],
                        "sha256": checker.sha256_text(text),
                        "text": text,
                    }
                    for name, text in archived.items()
                },
                "runtime_snapshot": {
                    "path": ".ops/stage3-execution-v1/status/runtime-snapshot.json",
                    "snapshot_id": runtime["snapshot_id"],
                    "sha256": checker.sha256_text(runtime_text),
                    "text": runtime_text,
                },
            },
        }
        payload["receipt_id"] = checker.content_addressed_id(
            "stage3-pre-cleanup", payload, "receipt_id"
        )
        return payload

    def cleanup_receipt_payload(
        self,
        blueprint: str,
        pre_cleanup_text: str,
        verifier_script_bytes: bytes,
    ) -> dict[str, object]:
        controller = {
            "runtime_root": ".ops/stage3-execution-v1/",
            "cron_begin_marker": "# BEGIN AWESOME_THEOREMS_STAGE3_EXECUTION_V1",
            "cron_end_marker": "# END AWESOME_THEOREMS_STAGE3_EXECUTION_V1",
        }
        pre_cleanup = json.loads(pre_cleanup_text)
        queries = {
            key: {
                "query": checker.CLEANUP_QUERY_NAMES[key],
                "targets": pre_cleanup["teardown_inventory"][key],
                "raw_result": [],
                "absent": True,
            }
            for key in checker.CLEANUP_ABSENCE_KEYS
        }
        stdout_payload = {
            "schema_version": "stage3-cleanup-absence/1.0",
            "controller_identity": controller,
            "observed_at": "2026-08-09T22:42:01Z",
            "inventory_sha256": pre_cleanup["teardown_inventory_sha256"],
            "queries": queries,
        }
        stdout = checker._canonical_json_bytes(stdout_payload).decode("utf-8") + "\n"
        command = {
            "argv": [
                "python3",
                "scripts/stage3_execution_cleanup.py",
                "--verify-absence",
                "--format=json",
            ],
            "cwd": ".",
            "started_at": "2026-08-09T22:42:00Z",
            "finished_at": "2026-08-09T22:42:01Z",
            "exit_code": 0,
            "stdout": stdout,
            "stdout_sha256": checker.sha256_text(stdout),
            "stdout_payload_sha256": checker.canonical_json_sha256(stdout_payload),
            "stderr": "",
            "stderr_sha256": checker.sha256_text(""),
        }
        payload = {
            "schema_version": checker.CLEANUP_RECEIPT_SCHEMA,
            "receipt_id": "pending",
            "teardown_completed_at": "2026-08-09T22:40:00Z",
            "verified_at": "2026-08-09T22:42:01Z",
            "issued_at": "2026-08-09T22:42:01Z",
            "required_cadence_seconds": 120,
            "blueprint_path": "Docs/Stage3_Blueprint.md",
            "blueprint_version": checker.VERSION,
            "raw_blueprint_sha256": checker.sha256_text(blueprint),
            "execution_spec_region_sha256": checker.sha256_text(
                checker.exact_marked_region(
                    blueprint, checker.SPEC_BEGIN, checker.SPEC_END, "execution specification"
                )
            ),
            "all_checklist_items_master_accepted": True,
            "pre_cleanup": {
                "path": "Docs/evidence/stage3_pre_cleanup.json",
                "receipt_id": pre_cleanup["receipt_id"],
                "sha256": checker.sha256_text(pre_cleanup_text),
            },
            "controller_identity": controller,
            "verifier": {
                "identity": "external-canonical-master-fixture",
                "independent_of_controller": True,
                "script_path": "scripts/stage3_execution_cleanup.py",
                "script_sha256": checker.sha256_bytes(verifier_script_bytes),
                "commands": [command],
            },
            "unfinished": {"not_done": 0, "self_tested": 0},
            "queues_empty": {"handoff": True, "integration": True, "repair": True, "checkpoint": True},
            "absence_recheck": queries,
        }
        payload["receipt_id"] = checker.content_addressed_id("stage3-cleanup", payload, "receipt_id")
        return payload

    @staticmethod
    def encode_cleanup(payload: dict[str, object]) -> str:
        return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    def cleanup_projection_fixture(self) -> tuple[str, str, bytes, str, dict[Path, str]]:
        blueprint = self.all_accepted_blueprint()
        tasks = checker.parse_tasks(blueprint)
        checker.validate_graph(tasks)
        pre_cleanup_text = self.encode_cleanup(self.pre_cleanup_receipt_payload(blueprint))
        verifier_bytes = self.cleanup_verifier_bytes()
        receipt_text = self.encode_cleanup(
            self.cleanup_receipt_payload(blueprint, pre_cleanup_text, verifier_bytes)
        )
        receipt = checker.parse_cleanup_receipt(
            receipt_text,
            blueprint,
            tasks,
            pre_cleanup_receipt_text=pre_cleanup_text,
            verifier_script_bytes=verifier_bytes,
        )
        metadata = checker.build_projection_metadata(
            blueprint,
            "2026-08-09T22:43:00Z",
            cleanup_receipt_sha256=checker.sha256_text(receipt_text),
            cleanup_receipt_id=receipt["receipt_id"],
        )
        outputs = {
            generator.STATUS: generator.generate_status(tasks, metadata, None, receipt),
            generator.KANBAN: generator.generate_kanban(tasks, metadata, None, receipt),
            generator.GANTT: generator.generate_gantt(tasks, metadata, None),
        }
        return blueprint, pre_cleanup_text, verifier_bytes, receipt_text, outputs

    def release_validation_fixture(self, blueprint: str) -> str:
        tasks = checker.parse_tasks(blueprint)
        repeated_output = "9" * 64
        runs = []
        for runner_id, fill in (("runner-a", "a"), ("runner-b", "b")):
            runs.append(
                {
                    "runner_id": runner_id,
                    "network": "denied",
                    "cache": "private_empty",
                    "argv_sha256": fill * 64,
                    "inputs_sha256": "c" * 64,
                    "outputs_sha256": repeated_output,
                    "raw_log_sha256": "d" * 64,
                    "exit_code": 0,
                    "passed": True,
                }
            )
        payload = {
            "schema_version": checker.RELEASE_VALIDATION_SCHEMA,
            "receipt_id": "pending",
            "blueprint_version": checker.VERSION,
            "raw_blueprint_sha256": checker.sha256_text(blueprint),
            "execution_spec_region_sha256": checker.sha256_text(
                checker.exact_marked_region(
                    blueprint, checker.SPEC_BEGIN, checker.SPEC_END, "execution specification"
                )
            ),
            "acceptance_contract_sha256": "e" * 64,
            "accepted_repository_merkle": {
                "algorithm": "sha256-framed-path-mode-bytes-v1",
                "entry_count": 400,
                "sha256": "f" * 64,
            },
            "item_master_receipts": {item_id: "1" * 64 for item_id in tasks},
            "matrix_runs": runs,
            "all_passed": True,
        }
        payload["receipt_id"] = checker.content_addressed_id(
            "stage3-release-validation", payload, "receipt_id"
        )
        return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"

    # Positive authority and projection checks.

    def test_current_files_pass_with_dynamic_counts(self) -> None:
        result = checker.validate_texts(self.blueprint, self.gantt, self.status, self.kanban)
        counts = Counter(task.state for task in self.tasks.values())
        self.assertEqual(result["total"], len(self.tasks))
        self.assertEqual(result["not_done"], counts[" "])
        self.assertEqual(result["self_tested"], counts["_"])
        self.assertEqual(result["master_accepted"], counts["x"])

    def test_v3_versions_and_shared_metadata_are_exact(self) -> None:
        payload = json.loads(self.status)
        self.assertEqual(checker.VERSION, "stage3-list-completion/3.0")
        self.assertEqual(payload["schema_version"], "stage3-execution-status/3.0")
        self.assertEqual(payload["metadata"], self.metadata)
        self.assertEqual(checker.parse_surface_metadata(self.kanban, "Kanban"), self.metadata)

    def test_gantt_has_one_complete_row_per_id(self) -> None:
        rows = checker.parse_gantt_monitor(self.gantt)
        self.assertEqual(len(rows), len(self.tasks))
        self.assertEqual({row["id"] for row in rows}, set(self.tasks))
        self.assertTrue(all(set(row) == checker.STATUS_ITEM_KEYS for row in rows))

    def test_current_timing_is_all_unscheduled(self) -> None:
        payload = json.loads(self.status)
        self.assertTrue(all(item["timing"] == checker.unavailable_timing() for item in payload["items"]))
        self.assertIn("Projection snapshot generated :milestone", self.gantt)

    def test_planning_and_runtime_unavailable_are_distinct(self) -> None:
        payload = json.loads(self.status)
        self.assertGreater(len(payload["planning"]["dependency_blocked"]), 0)
        self.assertEqual(payload["runtime"]["availability"], "runtime_unavailable")
        for key, value in payload["runtime"].items():
            if key not in {"availability", "cleanup_state"}:
                self.assertIsNone(value, key)
        self.assertEqual(payload["runtime"]["cleanup_state"], "not_started")

    def test_check_mode_reuses_existing_timestamp_exactly(self) -> None:
        self.assertEqual(generator.choose_generation_time(None), self.metadata["generated_at"])
        expected = generator.expected_outputs(generated_at=self.metadata["generated_at"])
        self.assertEqual(expected[generator.GANTT], self.gantt)
        self.assertEqual(expected[generator.STATUS], self.status)
        self.assertEqual(expected[generator.KANBAN], self.kanban)

    def test_same_name_gantt_naming_rule(self) -> None:
        self.assertEqual(
            checker.gantt_companion_path(Path("Docs/Stage_3_AR_Blueprint.md")),
            Path("Docs/Stage_3_AR_Gantt.md"),
        )
        self.assertEqual(
            checker.gantt_companion_path(Path("Docs/Stage3_Blueprint.md")),
            Path("Docs/Stage3_Gantt.md"),
        )
        self.assertEqual(checker.gantt_companion_path(Path("Docs/Plan.md")), Path("Docs/Plan_Gantt.md"))
        self.assertEqual(generator.GANTT, ROOT / "Docs" / "Stage3_Gantt.md")

    def test_self_tested_transition_reaches_human_integration_column(self) -> None:
        tasks = dict(self.tasks)
        tasks["S3-AUTH-002"] = replace(tasks["S3-AUTH-002"], state="_")
        kanban = generator.generate_kanban(tasks, self.metadata, None)
        self.assertIn("- `S3-AUTH-002` — planning integration-ready", kanban)
        gantt = generator.generate_gantt(tasks, self.metadata, None)
        rows = {row["id"]: row for row in checker.parse_gantt_monitor(gantt)}
        self.assertEqual(rows["S3-AUTH-002"]["state"], "self_tested")

    # Checklist grammar, graph, ownership, and semantic-DAG mutations.

    def test_duplicate_id_is_rejected(self) -> None:
        row = self.checklist_row("S3-PHY-001")
        self.assert_invalid(blueprint=self.blueprint.replace(checker.END, row + "\n" + checker.END))

    def test_stable_item_manifest_rejects_deleted_id(self) -> None:
        row = self.checklist_row("S3-MATH-010")
        self.assert_invalid(blueprint=self.blueprint.replace(row + "\n", "", 1))

    def test_direct_master_acceptance_without_runtime_or_receipt_is_rejected(self) -> None:
        blueprint = self.replace_state("S3-AUTH-002", "x")
        tasks = checker.parse_tasks(blueprint)
        metadata = checker.build_projection_metadata(blueprint, "2026-08-09T22:43:00Z")
        with self.assertRaises(checker.ValidationError):
            checker.validate_texts(
                blueprint,
                generator.generate_gantt(tasks, metadata, None),
                generator.generate_status(tasks, metadata, None),
                generator.generate_kanban(tasks, metadata, None),
            )

    def test_long_placeholder_cannot_replace_a_v3_gate(self) -> None:
        self.assert_invalid(
            blueprint=self.replace_field("S3-CAT-016", "gate", "X" * 400)
        )

    def test_each_frozen_v3_clause_is_required(self) -> None:
        original = self.tasks["S3-M38-035"].gate
        weakened = original.replace("native_decide", "native tactic")
        self.assertNotEqual(original, weakened)
        self.assert_invalid(blueprint=self.replace_field("S3-M38-035", "gate", weakened))

    def test_missing_dependency_is_rejected(self) -> None:
        self.assert_invalid(blueprint=self.replace_field("S3-PHY-019", "depends_on", "S3-PHY-999"))

    def test_cycle_is_rejected(self) -> None:
        self.assert_invalid(blueprint=self.replace_field("S3-AUTH-001", "depends_on", "S3-REL-005"))

    def test_unsupported_checkbox_is_rejected(self) -> None:
        open_id = next(item_id for item_id, task in self.tasks.items() if task.state == " ")
        self.assert_invalid(blueprint=self.blueprint.replace(f"- [ ] `{open_id}`", f"- [X] `{open_id}`", 1))

    def test_noncanonical_checkbox_cursor_inside_marker_is_rejected(self) -> None:
        for cursor in (
            "* [ ] S3-SHADOW-001",
            "+ [x] S3-SHADOW-001",
            "  - [_] S3-SHADOW-001",
            "    - [ ] S3-SHADOW-001",
            "\t- [x] S3-SHADOW-001",
            "    1. [ ] S3-SHADOW-001",
            "> - [ ] S3-SHADOW-001",
            "> > * [x] S3-SHADOW-001",
        ):
            with self.subTest(cursor=cursor):
                mutated = self.blueprint.replace(checker.END, cursor + "\n" + checker.END, 1)
                self.assert_invalid(blueprint=mutated)

    def test_competing_checkbox_cursor_outside_marker_is_rejected(self) -> None:
        for suffix in (
            "* [ ] S3-SHADOW-001",
            "- shadow parent\n    - [ ] nested mutable shadow",
            "- shadow parent\n\t- [x] nested mutable shadow",
        ):
            with self.subTest(suffix=suffix):
                self.assert_invalid(blueprint=self.blueprint + "\n" + suffix + "\n")

    def test_advanced_item_requires_accepted_dependencies(self) -> None:
        item_id = next(
            item_id
            for item_id, task in self.tasks.items()
            if task.state == " " and any(self.tasks[dependency].state != "x" for dependency in task.dependencies)
        )
        self.assert_invalid(blueprint=self.replace_state(item_id, "_"))

    def test_absolute_owned_path_is_rejected(self) -> None:
        self.assert_invalid(blueprint=self.replace_field("S3-PHY-001", "owned_paths", "/tmp/not-owned.json"))

    def test_duplicate_owned_path_is_rejected(self) -> None:
        source_path = self.tasks["S3-PHY-001"].owned_paths[0]
        self.assert_invalid(blueprint=self.replace_field("S3-PHY-002", "owned_paths", source_path))

    def test_noncanonical_owned_path_alias_is_rejected(self) -> None:
        canonical = self.tasks["S3-PHY-001"].owned_paths[0]
        parent, name = canonical.rsplit("/", 1)
        aliased = f"{parent}/./{name}"
        self.assert_invalid(blueprint=self.replace_field("S3-PHY-002", "owned_paths", aliased))

    def test_rel004_activation_dependency_is_exact(self) -> None:
        required = ("S3-EXE-015", "S3-ENV-002", "S3-AUD-005")
        self.assertEqual(self.tasks["S3-REL-004"].dependencies, required)
        for removed in required:
            with self.subTest(removed=removed):
                dependencies = [dependency for dependency in required if dependency != removed]
                self.assert_invalid(
                    blueprint=self.replace_field("S3-REL-004", "depends_on", ",".join(dependencies))
                )

    def test_post_activation_roots_directly_depend_on_rel004(self) -> None:
        for item_id in ("S3-ENV-003", "S3-CAT-001", "S3-BEN-001", "S3-M38-001"):
            with self.subTest(item_id=item_id):
                dependencies = [dependency for dependency in self.tasks[item_id].dependencies if dependency != "S3-REL-004"]
                self.assert_invalid(blueprint=self.replace_field(item_id, "depends_on", ",".join(dependencies) or "-"))

    def test_release_join_cannot_drop_activation_or_terminal(self) -> None:
        dependencies = [dependency for dependency in self.tasks["S3-REL-001"].dependencies if dependency != "S3-REL-004"]
        self.assert_invalid(blueprint=self.replace_field("S3-REL-001", "depends_on", ",".join(dependencies)))

    def test_release_review_requires_audit_input(self) -> None:
        dependencies = [dependency for dependency in self.tasks["S3-REL-003"].dependencies if dependency != "S3-AUD-005"]
        self.assert_invalid(blueprint=self.replace_field("S3-REL-003", "depends_on", ",".join(dependencies)))

    def test_rel005_has_only_rel003_as_direct_dependency(self) -> None:
        self.assert_invalid(blueprint=self.replace_field("S3-REL-005", "depends_on", "S3-REL-003,S3-REL-004"))

    def test_rel005_ancestry_must_cover_every_other_id(self) -> None:
        dependencies = [dependency for dependency in self.tasks["S3-EXE-001"].dependencies if dependency != "S3-AUTH-003"]
        self.assert_invalid(blueprint=self.replace_field("S3-EXE-001", "depends_on", ",".join(dependencies)))

    def test_m38_review_packet_requires_premise_policy(self) -> None:
        for required in ("S3-AUD-004", "S3-AUD-005", "S3-M38-023"):
            with self.subTest(required=required):
                dependencies = [
                    dependency for dependency in self.tasks["S3-M38-029"].dependencies if dependency != required
                ]
                self.assert_invalid(
                    blueprint=self.replace_field("S3-M38-029", "depends_on", ",".join(dependencies))
                )

    def test_m38_cold_replay_requires_both_environment_gates(self) -> None:
        dependencies = [dependency for dependency in self.tasks["S3-M38-033"].dependencies if dependency != "S3-ENV-007"]
        self.assert_invalid(blueprint=self.replace_field("S3-M38-033", "depends_on", ",".join(dependencies)))

    def test_m38_release_requires_final_environment_acceptance(self) -> None:
        for required in ("S3-M38-066", "S3-ENV-008"):
            with self.subTest(required=required):
                dependencies = [
                    dependency for dependency in self.tasks["S3-M38-034"].dependencies if dependency != required
                ]
                self.assert_invalid(
                    blueprint=self.replace_field("S3-M38-034", "depends_on", ",".join(dependencies))
                )

    def test_only_m38_release_owns_current_validation_pointer(self) -> None:
        pointer = "THM-M-0387/receipts/current-validation.json"
        owners = [task.item_id for task in self.tasks.values() if pointer in task.owned_paths]
        self.assertEqual(owners, ["S3-M38-034"])
        paths = ",".join((*self.tasks["S3-M38-033"].owned_paths, pointer))
        self.assert_invalid(blueprint=self.replace_field("S3-M38-033", "owned_paths", paths))

    def test_six_review_master_gate_is_exact(self) -> None:
        dependencies = list(self.tasks["S3-M38-066"].dependencies[:-1])
        self.assert_invalid(blueprint=self.replace_field("S3-M38-066", "depends_on", ",".join(dependencies)))

    def test_execution_spec_table_is_exact_key_typed_and_runtime_bound(self) -> None:
        parsed = checker.parse_execution_spec(self.blueprint)
        self.assertEqual(parsed.logical_claim_ceiling, 6)
        self.assertEqual(parsed.launch_fanout, 2)
        self.assertEqual(parsed.cadence_seconds, 120)
        mutations = (
            ("six active logical claims", "seven active logical claims"),
            ("two per wave", "three per wave"),
            (
                "| execution skill build | `b3ehive/1.5.0+codex.20260809210355` |",
                "| execution skill build | `b3ehive/1.5.0+codex.badbuild` |",
            ),
            (checker.EXPECTED_EXECUTION_SPEC_ROWS["execution skill SHA256"], "`" + "0" * 64 + "`"),
        )
        for old, new in mutations:
            with self.subTest(old=old):
                with self.assertRaises(checker.ValidationError):
                    checker.parse_execution_spec(self.blueprint.replace(old, new, 1))

    def test_aud004_source_report_digest_table_is_exact_and_content_bound(self) -> None:
        gap_text = (
            ROOT / "Docs" / "reviews" / "Stage3_Blueprint_Gap_Review_2026-08-10.md"
        ).read_bytes().decode("utf-8")
        report_bytes = {path: (ROOT / path).read_bytes() for path in checker.BOUND_SOURCE_REPORTS}
        checker.validate_gap_review_source_reports(gap_text, report_bytes)
        first_path = checker.BOUND_SOURCE_REPORTS[0]
        tampered_bytes = dict(report_bytes)
        tampered_bytes[first_path] += b"\n"
        with self.assertRaises(checker.ValidationError):
            checker.validate_gap_review_source_reports(gap_text, tampered_bytes)
        recorded = checker.sha256_bytes(report_bytes[first_path])
        with self.assertRaises(checker.ValidationError):
            checker.validate_gap_review_source_reports(
                gap_text.replace(recorded, "0" * 64, 1), report_bytes
            )
        row = next(line for line in gap_text.splitlines() if first_path in line)
        for mutated in (
            gap_text.replace(row + "\n", "", 1),
            gap_text.replace(row, row + "\n" + row, 1),
        ):
            with self.assertRaises(checker.ValidationError):
                checker.validate_gap_review_source_reports(mutated, report_bytes)

    def test_v3_audit_and_semantic_delta_are_content_bound(self) -> None:
        report_bytes = {path: (ROOT / path).read_bytes() for path in checker.V3_BOUND_REPORTS}
        checker.validate_v3_bound_reports(self.blueprint, report_bytes)
        first_path = checker.V3_BOUND_REPORTS[0]
        tampered = dict(report_bytes)
        tampered[first_path] += b"\n"
        with self.assertRaises(checker.ValidationError):
            checker.validate_v3_bound_reports(self.blueprint, tampered)

    # Projection freshness, completeness, and authority mutations.

    def test_gantt_cannot_be_a_second_cursor(self) -> None:
        for cursor in ("- [ ]", "* [x]", "+ [_]", "  - [X]", "    - [ ]", "\t- [x]", "1. [ ]", "> - [ ]"):
            with self.subTest(cursor=cursor):
                self.assert_invalid(gantt=self.gantt + f"\n{cursor} S3-SHADOW-001\n")

    def test_kanban_cannot_be_a_second_cursor(self) -> None:
        for cursor in ("- [x]", "* [ ]", "+ [_]", "   - [X]", "    - [ ]", "\t- [x]", "1) [ ]", "> * [x]"):
            with self.subTest(cursor=cursor):
                self.assert_invalid(kanban=self.kanban + f"\n{cursor} S3-SHADOW-001\n")

    def test_gantt_missing_monitor_row_is_rejected(self) -> None:
        row = self.monitor_row("S3-PHY-019")
        self.assert_invalid(gantt=self.gantt.replace(row + "\n", "", 1))

    def test_gantt_duplicate_monitor_row_is_rejected(self) -> None:
        row = self.monitor_row("S3-PHY-019")
        self.assert_invalid(gantt=self.gantt.replace(checker.GANTT_MONITOR_END, row + "\n" + checker.GANTT_MONITOR_END))

    def test_gantt_missing_monitor_field_is_rejected(self) -> None:
        row = self.monitor_row("S3-PHY-019")
        cells = row[2:-2].split(" | ")
        del cells[6]
        malformed = "| " + " | ".join(cells) + " |"
        self.assert_invalid(gantt=self.gantt.replace(row, malformed, 1))

    def test_status_missing_item_field_is_rejected(self) -> None:
        payload = json.loads(self.status)
        del payload["items"][0]["owner"]
        self.assert_invalid(status=json.dumps(payload))

    def test_status_duplicate_json_field_is_rejected(self) -> None:
        duplicate = self.status.replace(
            '"schema_version": "stage3-execution-status/3.0",',
            '"schema_version": "stage3-execution-status/3.0",\n  "schema_version": "stage3-execution-status/3.0",',
            1,
        )
        self.assert_invalid(status=duplicate)

    def test_status_numeric_types_and_gantt_json_cells_are_canonical(self) -> None:
        for replacement in (False, 0.0):
            with self.subTest(replacement=replacement):
                payload = json.loads(self.status)
                payload["counts"]["self_tested"] = replacement
                mutated = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
                self.assert_invalid(status=mutated)
        escaped = self.gantt.replace('`"S3-AUD-001"`', '`"\\u00533-AUD-001"`', 1)
        self.assertNotEqual(escaped, self.gantt)
        self.assert_invalid(gantt=escaped)

    def test_status_item_state_drift_is_rejected(self) -> None:
        payload = json.loads(self.status)
        payload["items"][0]["state"] = "not_done" if payload["items"][0]["state"] != "not_done" else "master_accepted"
        self.assert_invalid(status=json.dumps(payload))

    def test_stale_raw_blueprint_digest_is_rejected_even_if_shared(self) -> None:
        gantt, status, kanban = self.mutate_all_metadata("raw_blueprint_sha256", "0" * 64)
        self.assert_invalid(gantt=gantt, status=status, kanban=kanban)

    def test_stale_spec_region_digest_is_rejected_even_if_shared(self) -> None:
        gantt, status, kanban = self.mutate_all_metadata("execution_spec_region_sha256", "1" * 64)
        self.assert_invalid(gantt=gantt, status=status, kanban=kanban)

    def test_stale_projection_input_digest_is_rejected_even_if_shared(self) -> None:
        gantt, status, kanban = self.mutate_all_metadata("projection_input_sha256", "2" * 64)
        self.assert_invalid(gantt=gantt, status=status, kanban=kanban)

    def test_cross_surface_metadata_mismatch_is_rejected(self) -> None:
        changed = self.metadata["generated_at"].replace("Z", "") + "Z-invalid"
        self.assert_invalid(kanban=self.kanban.replace(self.metadata["generated_at"], changed, 1))

    def test_invalid_generated_at_is_rejected(self) -> None:
        gantt, status, kanban = self.mutate_all_metadata("generated_at", "2026-08-10")
        self.assert_invalid(gantt=gantt, status=status, kanban=kanban)

    def test_generation_milestone_must_match_shared_timestamp(self) -> None:
        self.assert_invalid(gantt=self.gantt.replace("Projection snapshot generated :milestone", "Projection guessed :milestone", 1))

    def test_gantt_and_kanban_reject_extra_semantic_prose(self) -> None:
        self.assert_invalid(gantt=self.gantt + "All 168 tasks completed on 2026-01-01.\n")
        injected = self.kanban.replace(
            "## Runtime snapshot", "All 168 tasks are live and accepted.\n\n## Runtime snapshot", 1
        )
        self.assert_invalid(kanban=injected)

    def test_gantt_rejects_extra_mermaid_task_and_kanban_extra_heading(self) -> None:
        closing = "```\n\n## Unscheduled task timing"
        fabricated = (
            "    Fabricated task :fake, 2099-01-01T00:00:00, 10d\n"
            "```\n\n## Unscheduled task timing"
        )
        self.assert_invalid(gantt=self.gantt.replace(closing, fabricated, 1))
        self.assert_invalid(kanban=self.kanban + "\n## Fabricated live\n\n- `S3-AUTH-001`\n")

    def test_gantt_unscheduled_narrative_count_must_match_rows(self) -> None:
        expected = f"Every task is `unscheduled` in this {len(self.tasks)}-item snapshot"
        self.assertIn(expected, self.gantt)
        self.assert_invalid(gantt=self.gantt.replace(expected, "Every task is `unscheduled` in this 999-item snapshot", 1))

    def test_invented_timing_is_rejected(self) -> None:
        payload = json.loads(self.status)
        payload["items"][0]["timing"]["start"] = "2026-08-09T22:00:00Z"
        self.assert_invalid(status=json.dumps(payload))

    def test_runtime_unavailable_cannot_be_reported_as_zero(self) -> None:
        payload = json.loads(self.status)
        payload["runtime"]["authenticated_live_goals"] = 0
        self.assert_invalid(status=json.dumps(payload))

    def test_planning_blockers_cannot_be_moved_into_runtime(self) -> None:
        payload = json.loads(self.status)
        payload["runtime"]["dependency_blocked"] = len(payload["planning"]["dependency_blocked"])
        self.assert_invalid(status=json.dumps(payload))

    def test_kanban_must_cover_every_item(self) -> None:
        self.assertIn("- `S3-AUTH-002`", self.kanban)
        self.assert_invalid(kanban=self.kanban.replace("- `S3-AUTH-002`\n", "", 1))

    def test_kanban_must_distinguish_runtime_unavailable(self) -> None:
        phrase = "`runtime_unavailable`; every worker runtime count and lifecycle value is `null`, never an invented zero."
        self.assert_invalid(kanban=self.kanban.replace(phrase, "Runtime lanes: zero."))

    def test_kanban_runtime_count_table_must_match_status(self) -> None:
        self.assert_invalid(
            kanban=self.kanban.replace("| `authenticated_live_goals` | `null` |", "| `authenticated_live_goals` | `999` |", 1)
        )

    def test_kanban_planning_blocker_suffix_must_match_dag(self) -> None:
        source = "- `S3-BEN-001` — blockers: `S3-REL-004`"
        self.assertIn(source, self.kanban)
        self.assert_invalid(kanban=self.kanban.replace(source, "- `S3-BEN-001` — blockers: `S3-AUTH-001`", 1))

    def test_kanban_cleanup_narrative_must_match_receipt_state(self) -> None:
        source = "Terminal `cleanup_state` is `not_started` from the optional durable cleanup receipt."
        self.assertIn(source, self.kanban)
        self.assert_invalid(kanban=self.kanban.replace(source, "Terminal `cleanup_state` is `complete` from the optional durable cleanup receipt.", 1))

    # Strict optional runtime-snapshot interface.

    def test_strict_runtime_snapshot_can_drive_observed_projection(self) -> None:
        runtime_text = self.encode_runtime(self.runtime_snapshot_payload())
        outputs = generator.expected_outputs(
            generated_at="2026-08-09T22:41:00Z", runtime_snapshot_text=runtime_text
        )
        result = checker.validate_texts(
            self.blueprint,
            outputs[generator.GANTT],
            outputs[generator.STATUS],
            outputs[generator.KANBAN],
            runtime_text,
        )
        self.assertEqual(result["total"], len(self.tasks))
        status = json.loads(outputs[generator.STATUS])
        self.assertEqual(status["runtime"]["availability"], "observed")
        self.assertEqual(status["runtime"]["authenticated_live_goals"], 0)
        self.assertTrue(all(item["live"] is False for item in status["items"]))

    def test_runtime_snapshot_live_identity_and_counts_project(self) -> None:
        payload = self.runtime_snapshot_payload()
        open_id = next(item_id for item_id, task in self.tasks.items() if task.state == " ")
        item = next(item for item in payload["items"] if item["id"] == open_id)
        item.update(
            {
                "claim_id": "claim-fixture-1",
                "run_id": "run-fixture-1",
                "owner": "fixture-worker",
                "startup": None,
                "live": True,
                "live_evidence": self.live_evidence(open_id, "claim-fixture-1", "run-fixture-1"),
                "running": True,
            }
        )
        self.refresh_runtime_id(payload)
        runtime_text = self.encode_runtime(payload)
        outputs = generator.expected_outputs(
            generated_at="2026-08-09T22:42:00Z", runtime_snapshot_text=runtime_text
        )
        checker.validate_texts(
            self.blueprint,
            outputs[generator.GANTT],
            outputs[generator.STATUS],
            outputs[generator.KANBAN],
            runtime_text,
        )
        status = json.loads(outputs[generator.STATUS])
        self.assertEqual(status["runtime"]["logical_claims"], 1)
        self.assertEqual(status["runtime"]["authenticated_live_goals"], 1)
        self.assertEqual(status["runtime"]["running_turns"], 1)

    def test_recorded_runtime_timing_is_rendered_as_exact_mermaid_task(self) -> None:
        payload = self.runtime_snapshot_payload()
        item = payload["items"][0]
        timing_source_payload = {
            "start": "2026-08-09T22:00:00Z",
            "end": "2026-08-09T22:30:00Z",
            "duration_seconds": 1800,
        }
        item["timing"] = {
            "status": "recorded",
            **timing_source_payload,
            "source": {
                "path": ".ops/stage3-execution-v1/ledgers/claims.json",
                "payload": timing_source_payload,
                "sha256": checker.canonical_json_sha256(timing_source_payload),
            },
        }
        self.refresh_runtime_id(payload)
        runtime_text = self.encode_runtime(payload)
        outputs = generator.expected_outputs(
            generated_at="2026-08-09T22:41:00Z", runtime_snapshot_text=runtime_text
        )
        mermaid_id = "timing_" + item["id"].lower().replace("-", "_")
        expected_row = (
            f"    {item['id']} :{mermaid_id}, 2026-08-09T22:00:00, "
            "2026-08-09T22:30:00"
        )
        self.assertEqual(outputs[generator.GANTT].count(expected_row), 1)
        checker.validate_texts(
            self.blueprint,
            outputs[generator.GANTT],
            outputs[generator.STATUS],
            outputs[generator.KANBAN],
            runtime_text,
        )

    def test_runtime_snapshot_rejects_duplicate_claim_and_run_identity(self) -> None:
        payload = self.runtime_snapshot_payload()
        for item in payload["items"][:2]:
            item.update(
                {
                    "claim_id": "duplicate-claim",
                    "run_id": "duplicate-run",
                    "owner": "fixture-worker",
                }
            )
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_runtime_observation_payload_digest_and_claim_path_are_exact(self) -> None:
        for mutation in ("payload", "sha256", "source"):
            with self.subTest(mutation=mutation):
                payload = self.runtime_snapshot_payload()
                item = payload["items"][0]
                if mutation == "payload":
                    item["observation_evidence"]["payload"]["running"] = True
                elif mutation == "sha256":
                    item["observation_evidence"]["sha256"] = "0" * 64
                else:
                    item["observation_evidence"]["source"] = (
                        ".ops/stage3-execution-v1/status/reconciliation.json"
                    )
                payload["snapshot_id"] = checker.content_addressed_id(
                    "stage3-runtime", payload, "snapshot_id"
                )
                with self.assertRaises(checker.ValidationError):
                    checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_startup_deadline_and_process_liveness_are_evidence_bound(self) -> None:
        open_id = checker.planning_projection(self.tasks)["frontiers"]["implementation_ready"][0]
        for mutation in ("long_deadline", "dead_process"):
            with self.subTest(mutation=mutation):
                payload = self.runtime_snapshot_payload()
                item = next(item for item in payload["items"] if item["id"] == open_id)
                claim_id = "claim-startup-fixture"
                run_id = "run-startup-fixture"
                task_root = f".ops/stage3-execution-v1/tasks/{claim_id}/{run_id}"
                process = {
                    "tmux_socket": f"{task_root}/tmux.sock",
                    "session": "startup-fixture",
                    "pane_pid": 22334,
                    "process_start_ticks": 77889,
                    "cwd": f"{task_root}/work",
                    "codex_home": f"{task_root}/codex-home",
                    "observed_at": payload["observed_at"],
                    "alive": mutation != "dead_process",
                }
                item.update(
                    {
                        "claim_id": claim_id,
                        "run_id": run_id,
                        "owner": "fixture-worker",
                        "startup": "goal_submitted",
                        "startup_evidence": {
                            "state_entered_at": "2026-08-09T22:31:00Z",
                            "deadline_at": (
                                "2026-08-09T22:50:00Z"
                                if mutation == "long_deadline"
                                else "2026-08-09T22:40:00Z"
                            ),
                            "identity_evidence_sha256": "0" * 64,
                            "process_identity": process,
                        },
                    }
                )
                self.refresh_runtime_id(payload)
                with self.assertRaises(checker.ValidationError):
                    checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_live_goal_route_and_simultaneous_identity_uniqueness_are_enforced(self) -> None:
        ready = checker.planning_projection(self.tasks)["frontiers"]["implementation_ready"]
        self.assertGreaterEqual(len(ready), 2)
        payload = self.runtime_snapshot_payload()
        for index, item_id in enumerate(ready[:2]):
            claim_id = f"claim-live-{index}"
            run_id = f"run-live-{index}"
            item = next(item for item in payload["items"] if item["id"] == item_id)
            item.update(
                {
                    "claim_id": claim_id,
                    "run_id": run_id,
                    "owner": f"worker-{index}",
                    "live": True,
                    "running": index == 0,
                    "live_evidence": self.live_evidence(item_id, claim_id, run_id),
                }
            )
        self.refresh_runtime_id(payload)
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

        payload = self.runtime_snapshot_payload()
        accepted_id = next(item_id for item_id, task in self.tasks.items() if task.state == "x")
        accepted = next(item for item in payload["items"] if item["id"] == accepted_id)
        accepted.update(
            {
                "claim_id": "claim-terminal-history",
                "run_id": "run-terminal-history",
                "owner": "worker-terminal-history",
                "handoff": "finished",
                "integration": "accepted",
            }
        )
        self.refresh_runtime_id(payload)
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

        payload = self.runtime_snapshot_payload()
        item_id = ready[0]
        item = next(item for item in payload["items"] if item["id"] == item_id)
        item.update(
            {
                "claim_id": "claim-route",
                "run_id": "run-route",
                "owner": "worker-route",
                "live": True,
                "live_evidence": self.live_evidence(item_id, "claim-route", "run-route"),
            }
        )
        item["live_evidence"]["goal_claim_id"] = "wrong-claim"
        self.refresh_runtime_id(payload)
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_accepted_runtime_and_integration_product_states_are_terminal(self) -> None:
        payload = self.runtime_snapshot_payload()
        accepted_id = next(item_id for item_id, task in self.tasks.items() if task.state == "x")
        accepted = next(item for item in payload["items"] if item["id"] == accepted_id)
        accepted.update(
            {
                "claim_id": "claim-accepted-repair",
                "run_id": "run-accepted-repair",
                "owner": "worker-accepted",
                "handoff": "harvested",
                "integration": "failed",
                "repair": "active",
                "runtime_block": {"kind": "validator", "reason": "fixture failure"},
            }
        )
        self.refresh_runtime_id(payload)
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_checkbox_state_and_runtime_product_state_cannot_diverge(self) -> None:
        payload = self.runtime_snapshot_payload()
        ready_id = checker.planning_projection(self.tasks)["frontiers"]["implementation_ready"][0]
        ready = next(item for item in payload["items"] if item["id"] == ready_id)
        ready.update(
            {
                "claim_id": "claim-premature-accept",
                "run_id": "run-premature-accept",
                "owner": "worker-premature-accept",
                "handoff": "harvested",
                "integration": "accepted",
            }
        )
        self.refresh_runtime_id(payload)
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

        payload = self.runtime_snapshot_payload()
        accepted_id = next(item_id for item_id, task in self.tasks.items() if task.state == "x")
        accepted = next(item for item in payload["items"] if item["id"] == accepted_id)
        accepted.update(
            {
                "claim_id": "claim-history-only",
                "run_id": "run-history-only",
                "owner": "worker-history-only",
            }
        )
        self.refresh_runtime_id(payload)
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

        payload = self.runtime_snapshot_payload()
        ready = checker.planning_projection(self.tasks)["frontiers"]["implementation_ready"][:2]
        for index, item_id in enumerate(ready):
            item = next(item for item in payload["items"] if item["id"] == item_id)
            item.update(
                {
                    "claim_id": f"claim-integration-{index}",
                    "run_id": f"run-integration-{index}",
                    "owner": f"worker-integration-{index}",
                    "handoff": "harvested",
                    "integration": "integrating",
                }
            )
        self.refresh_runtime_id(payload)
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_runtime_cleanup_transition_requires_bound_precleanup_arm(self) -> None:
        payload = self.runtime_snapshot_payload()
        payload["cleanup_state"] = "teardown"
        self.refresh_runtime_id(payload)
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_bound_cleanup_pending_runtime_transition_is_observable(self) -> None:
        blueprint = self.all_accepted_blueprint()
        tasks = checker.parse_tasks(blueprint)
        pre_cleanup_text = self.encode_cleanup(self.pre_cleanup_receipt_payload(blueprint))
        pre_cleanup = json.loads(pre_cleanup_text)
        payload = self.runtime_snapshot_payload(blueprint, tasks)
        payload["cleanup_state"] = "cleanup_pending"
        payload["cleanup_arm"] = {
            "path": "Docs/evidence/stage3_pre_cleanup.json",
            "receipt_id": pre_cleanup["receipt_id"],
            "sha256": checker.sha256_text(pre_cleanup_text),
        }
        self.refresh_runtime_id(payload)
        parsed = checker.parse_runtime_snapshot(
            self.encode_runtime(payload),
            tasks,
            blueprint,
            pre_cleanup_receipt_text=pre_cleanup_text,
        )
        self.assertEqual(parsed["cleanup_state"], "cleanup_pending")

    def test_dynamic_limiters_are_derived_from_structured_observations(self) -> None:
        for kind, field, value in (
            ("host_resource", "available_ram_bytes", 1),
            ("external_limit", "decision", "block"),
        ):
            with self.subTest(kind=kind):
                payload = self.runtime_snapshot_payload()
                binding = next(
                    binding
                    for binding in payload["admission"]["effective_target_bindings"]
                    if binding["kind"] == kind
                )
                if kind == "host_resource":
                    binding["evidence"]["payload"][field] = value
                else:
                    binding["evidence"]["payload"]["decisions"][0][field] = value
                binding["evidence"]["sha256"] = checker.canonical_json_sha256(
                    binding["evidence"]["payload"]
                )
                payload["snapshot_id"] = checker.content_addressed_id(
                    "stage3-runtime", payload, "snapshot_id"
                )
                with self.assertRaises(checker.ValidationError):
                    checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_occupancy_stop_reason_binds_pump_guard_and_iteration(self) -> None:
        payload = self.runtime_snapshot_payload()
        evidence = payload["admission"]["occupancy_underfill_reason"]["evidence"]
        evidence["payload"]["reconciliation_iteration"] = 2
        evidence["sha256"] = checker.canonical_json_sha256(evidence["payload"])
        payload["snapshot_id"] = checker.content_addressed_id(
            "stage3-runtime", payload, "snapshot_id"
        )
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_recorded_timing_source_is_content_bound(self) -> None:
        payload = self.runtime_snapshot_payload()
        item = payload["items"][0]
        source_payload = {
            "start": "2026-08-09T22:00:00Z",
            "end": "2026-08-09T22:30:00Z",
            "duration_seconds": 1800,
        }
        item["timing"] = {
            "status": "recorded",
            **source_payload,
            "source": {
                "path": ".ops/stage3-execution-v1/ledgers/claims.json",
                "payload": dict(source_payload),
                "sha256": checker.canonical_json_sha256(source_payload),
            },
        }
        self.refresh_runtime_id(payload)
        item["timing"]["source"]["payload"]["start"] = "2026-08-09T21:59:59Z"
        item["timing"]["source"]["sha256"] = checker.canonical_json_sha256(
            item["timing"]["source"]["payload"]
        )
        self.refresh_runtime_id(payload)
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_active_runtime_has_a_separate_current_freshness_profile(self) -> None:
        payload = self.runtime_snapshot_payload()
        item_id = checker.planning_projection(self.tasks)["frontiers"]["implementation_ready"][0]
        item = next(item for item in payload["items"] if item["id"] == item_id)
        item.update(
            {
                "claim_id": "claim-freshness",
                "run_id": "run-freshness",
                "owner": "worker-freshness",
                "live": True,
                "live_evidence": self.live_evidence(
                    item_id, "claim-freshness", "run-freshness"
                ),
            }
        )
        self.refresh_runtime_id(payload)
        parsed = checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)
        checker.validate_runtime_fresh_now(
            parsed,
            self.blueprint,
            now=checker.datetime.strptime("2026-08-09T22:42:00Z", "%Y-%m-%dT%H:%M:%SZ"),
        )
        with self.assertRaises(checker.ValidationError):
            checker.validate_runtime_fresh_now(
                parsed,
                self.blueprint,
                now=checker.datetime.strptime("2026-08-09T23:00:00Z", "%Y-%m-%dT%H:%M:%SZ"),
            )

    def test_runtime_snapshot_rejects_path_escaping_claim_and_run_components(self) -> None:
        for key, value in (("claim_id", "../../escape"), ("run_id", "run/../../escape")):
            with self.subTest(key=key):
                payload = self.runtime_snapshot_payload()
                open_id = next(item_id for item_id, task in self.tasks.items() if task.state == " ")
                item = next(item for item in payload["items"] if item["id"] == open_id)
                item.update(
                    {
                        "claim_id": "safe-claim",
                        "run_id": "safe-run",
                        "owner": "fixture-worker",
                        key: value,
                        "live": True,
                    }
                )
                self.refresh_runtime_id(payload)
                with self.assertRaises(checker.ValidationError):
                    checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_runtime_snapshot_rejects_reserved_or_starting_live_lane(self) -> None:
        payload = self.runtime_snapshot_payload()
        payload["items"][0].update(
            {
                "claim_id": "claim-fixture-1",
                "run_id": "run-fixture-1",
                "owner": "fixture-worker",
                "startup": "reserved",
                "live": True,
            }
        )
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_runtime_snapshot_rejects_finished_live_lane(self) -> None:
        payload = self.runtime_snapshot_payload()
        payload["items"][0].update(
            {
                "claim_id": "claim-fixture-1",
                "run_id": "run-fixture-1",
                "owner": "fixture-worker",
                "handoff": "finished",
                "live": True,
            }
        )
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_runtime_snapshot_rejects_accepted_item_occupying_live_capacity(self) -> None:
        payload = self.runtime_snapshot_payload()
        accepted_id = next(item_id for item_id, task in self.tasks.items() if task.state == "x")
        item = next(item for item in payload["items"] if item["id"] == accepted_id)
        item.update(
            {
                "claim_id": "claim-fixture-accepted",
                "run_id": "run-fixture-accepted",
                "owner": "fixture-worker",
                "live": True,
            }
        )
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_runtime_snapshot_missing_field_is_rejected(self) -> None:
        payload = self.runtime_snapshot_payload()
        del payload["items"][0]["owner"]
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_self_tested_runtime_snapshot_requires_harvested_handoff(self) -> None:
        tasks = dict(self.tasks)
        tasks["S3-AUTH-002"] = replace(tasks["S3-AUTH-002"], state="_")
        payload = self.runtime_snapshot_payload()
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), tasks)

    def test_runtime_snapshot_requires_global_underfill_reason(self) -> None:
        payload = self.runtime_snapshot_payload()
        payload["admission"]["underfill_stop_reason"] = None
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_runtime_snapshot_cannot_lower_effective_target_to_zero_without_reason(self) -> None:
        payload = self.runtime_snapshot_payload()
        payload["admission"]["admitted_target"] = 0
        payload["admission"]["underfill_stop_reason"] = None
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_runtime_snapshot_rejects_target_overrun(self) -> None:
        payload = self.runtime_snapshot_payload()
        open_id = next(item_id for item_id, task in self.tasks.items() if task.state == " ")
        item = next(item for item in payload["items"] if item["id"] == open_id)
        item.update(
            {
                "claim_id": "claim-fixture-overrun",
                "run_id": "run-fixture-overrun",
                "owner": "fixture-worker",
                "live": True,
                "running": True,
            }
        )
        payload["admission"]["logical_claim_target"] = 0
        payload["admission"]["admitted_target"] = 0
        payload["admission"]["underfill_stop_reason"] = None
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_runtime_snapshot_rejects_spoofed_configured_ceiling(self) -> None:
        payload = self.runtime_snapshot_payload()
        payload["admission"]["logical_claim_target"] = 7
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_runtime_snapshot_enforces_startup_reservation_ceiling(self) -> None:
        payload = self.runtime_snapshot_payload()
        open_ids = [item_id for item_id, task in self.tasks.items() if task.state == " "][:5]
        for index, item_id in enumerate(open_ids):
            item = next(item for item in payload["items"] if item["id"] == item_id)
            item.update(
                {
                    "claim_id": f"claim-startup-{index}",
                    "run_id": f"run-startup-{index}",
                    "owner": f"fixture-worker-{index}",
                    "startup": "reserved",
                }
            )
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_runtime_snapshot_duplicate_id_is_rejected(self) -> None:
        payload = self.runtime_snapshot_payload()
        payload["items"][1]["id"] = payload["items"][0]["id"]
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_runtime_snapshot_live_without_identity_is_rejected(self) -> None:
        payload = self.runtime_snapshot_payload()
        payload["items"][0]["live"] = True
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_runtime_snapshot_id_rejects_markdown_injection(self) -> None:
        payload = self.runtime_snapshot_payload()
        payload["snapshot_id"] = "evil`\n* [ ] S3-SHADOW-001\n`"
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    def test_runtime_snapshot_future_observation_cannot_be_projected(self) -> None:
        payload = self.runtime_snapshot_payload()
        payload["observed_at"] = "2099-01-01T00:10:00Z"
        self.refresh_runtime_id(payload)
        runtime_text = self.encode_runtime(payload)
        with self.assertRaises((checker.ValidationError, generator.CHECKER.ValidationError)):
            generator.expected_outputs(
                generated_at="2099-01-01T00:09:59Z",
                runtime_snapshot_text=runtime_text,
            )

    def test_runtime_reason_markdown_is_safely_encoded(self) -> None:
        payload = self.runtime_snapshot_payload()
        payload["admission"]["underfill_stop_reason"]["reason"] = "pipe | tick ` and\n* [ ] shadow"
        self.refresh_runtime_id(payload)
        runtime_text = self.encode_runtime(payload)
        outputs = generator.expected_outputs(
            generated_at="2026-08-09T22:41:00Z", runtime_snapshot_text=runtime_text
        )
        self.assertNotRegex(outputs[generator.KANBAN], checker.MUTABLE_CHECKBOX_RE)
        checker.validate_texts(
            self.blueprint,
            outputs[generator.GANTT],
            outputs[generator.STATUS],
            outputs[generator.KANBAN],
            runtime_text,
        )

    def test_generator_prewrite_validation_rejects_invalid_renderer(self) -> None:
        original = generator.generate_kanban
        try:
            generator.generate_kanban = lambda *args, **kwargs: original(*args, **kwargs) + "\n* [ ] shadow\n"
            with self.assertRaises(generator.CHECKER.ValidationError):
                generator.expected_outputs(generated_at="2026-08-09T22:41:00Z")
        finally:
            generator.generate_kanban = original

    def test_default_runtime_snapshot_discovery_and_explicit_override(self) -> None:
        original = checker.RUNTIME_SNAPSHOT
        try:
            with tempfile.TemporaryDirectory() as directory:
                canonical = Path(directory) / "runtime-snapshot.json"
                checker.RUNTIME_SNAPSHOT = canonical
                self.assertIsNone(checker.resolve_runtime_snapshot_path(None))
                canonical.write_text("{}\n", encoding="utf-8")
                self.assertEqual(checker.resolve_runtime_snapshot_path(None), canonical)
                override = Path(directory) / "fixture.json"
                self.assertEqual(checker.resolve_runtime_snapshot_path(override), override)
        finally:
            checker.RUNTIME_SNAPSHOT = original

    def test_runtime_digest_staleness_is_rejected(self) -> None:
        runtime_text = self.encode_runtime(self.runtime_snapshot_payload())
        outputs = generator.expected_outputs(
            generated_at="2026-08-09T22:43:00Z", runtime_snapshot_text=runtime_text
        )
        actual_digest = checker.sha256_text(runtime_text)
        gantt = outputs[generator.GANTT].replace(actual_digest, "f" * 64)
        status = outputs[generator.STATUS].replace(actual_digest, "f" * 64)
        kanban = outputs[generator.KANBAN].replace(actual_digest, "f" * 64)
        with self.assertRaises(checker.ValidationError):
            checker.validate_texts(self.blueprint, gantt, status, kanban, runtime_text)

    # Durable post-cleanup receipt projection.

    def test_terminal_completion_profile_distinguishes_transition_and_receipt(self) -> None:
        blueprint = self.all_accepted_blueprint()
        tasks = checker.parse_tasks(blueprint)
        metadata = checker.build_projection_metadata(blueprint, "2026-08-09T22:43:00Z")
        transitional = {
            generator.GANTT: generator.generate_gantt(tasks, metadata, None),
            generator.STATUS: generator.generate_status(tasks, metadata, None),
            generator.KANBAN: generator.generate_kanban(tasks, metadata, None),
        }
        with self.assertRaises(checker.ValidationError):
            checker.validate_texts(
                blueprint,
                transitional[generator.GANTT],
                transitional[generator.STATUS],
                transitional[generator.KANBAN],
            )

        blueprint, pre_cleanup_text, verifier_bytes, receipt_text, outputs = (
            self.cleanup_projection_fixture()
        )
        release_validation_text = self.release_validation_fixture(blueprint)
        checker.validate_texts(
            blueprint,
            outputs[generator.GANTT],
            outputs[generator.STATUS],
            outputs[generator.KANBAN],
            None,
            receipt_text,
            pre_cleanup_text,
            verifier_bytes,
            release_validation_text,
            require_complete=True,
        )

    def test_terminal_completion_rejects_missing_or_stale_fixed_matrix_receipt(self) -> None:
        blueprint, pre_cleanup_text, verifier_bytes, receipt_text, outputs = (
            self.cleanup_projection_fixture()
        )
        with self.assertRaises(checker.ValidationError):
            checker.validate_texts(
                blueprint,
                outputs[generator.GANTT],
                outputs[generator.STATUS],
                outputs[generator.KANBAN],
                None,
                receipt_text,
                pre_cleanup_text,
                verifier_bytes,
                require_complete=True,
            )
        release_text = self.release_validation_fixture(blueprint)
        stale = release_text.replace(checker.sha256_text(blueprint), "0" * 64, 1)
        with self.assertRaises(checker.ValidationError):
            checker.validate_texts(
                blueprint,
                outputs[generator.GANTT],
                outputs[generator.STATUS],
                outputs[generator.KANBAN],
                None,
                receipt_text,
                pre_cleanup_text,
                verifier_bytes,
                stale,
                require_complete=True,
            )

    def test_cleanup_receipt_roundtrip_survives_absent_runtime_root(self) -> None:
        blueprint, pre_cleanup_text, verifier_bytes, receipt_text, outputs = self.cleanup_projection_fixture()
        result = checker.validate_texts(
            blueprint,
            outputs[generator.GANTT],
            outputs[generator.STATUS],
            outputs[generator.KANBAN],
            None,
            receipt_text,
            pre_cleanup_text,
            verifier_bytes,
        )
        self.assertEqual(result["master_accepted"], result["total"])
        status = json.loads(outputs[generator.STATUS])
        self.assertEqual(status["runtime"]["availability"], "runtime_unavailable")
        self.assertEqual(status["runtime"]["cleanup_state"], "complete")
        self.assertEqual(
            status["metadata"]["cleanup_receipt_sha256"], checker.sha256_text(receipt_text)
        )
        # No .ops input is consulted: the durable receipt remains terminal evidence after scoped teardown.

    def test_cleanup_receipt_tamper_makes_projection_stale(self) -> None:
        blueprint, pre_cleanup_text, verifier_bytes, receipt_text, outputs = self.cleanup_projection_fixture()
        payload = json.loads(receipt_text)
        payload["verifier"]["commands"][0]["stdout_sha256"] = "3" * 64
        tampered = self.encode_cleanup(payload)
        with self.assertRaises(checker.ValidationError):
            checker.validate_texts(
                blueprint,
                outputs[generator.GANTT],
                outputs[generator.STATUS],
                outputs[generator.KANBAN],
                None,
                tampered,
                pre_cleanup_text,
                verifier_bytes,
            )

    def test_cleanup_receipt_presence_must_match_projection_metadata(self) -> None:
        blueprint = self.all_accepted_blueprint()
        tasks = checker.parse_tasks(blueprint)
        pre_cleanup_text = self.encode_cleanup(self.pre_cleanup_receipt_payload(blueprint))
        verifier_bytes = self.cleanup_verifier_bytes()
        receipt_text = self.encode_cleanup(
            self.cleanup_receipt_payload(blueprint, pre_cleanup_text, verifier_bytes)
        )
        metadata = checker.build_projection_metadata(blueprint, "2026-08-09T22:43:00Z")
        status = generator.generate_status(tasks, metadata, None, None)
        kanban = generator.generate_kanban(tasks, metadata, None, None)
        gantt = generator.generate_gantt(tasks, metadata, None)
        with self.assertRaises(checker.ValidationError):
            checker.validate_texts(
                blueprint, gantt, status, kanban, None, receipt_text, pre_cleanup_text, verifier_bytes
            )

    def test_runtime_snapshot_and_terminal_cleanup_receipt_are_mutually_exclusive(self) -> None:
        with self.assertRaises(checker.ValidationError):
            checker.build_projection_metadata(
                self.blueprint,
                "2026-08-09T22:43:00Z",
                runtime_snapshot_sha256="4" * 64,
                runtime_snapshot_id="stage3-runtime/" + "5" * 64,
                cleanup_receipt_sha256="6" * 64,
                cleanup_receipt_id="stage3-cleanup/" + "7" * 64,
            )
        blueprint, pre_cleanup_text, verifier_bytes, receipt_text, outputs = self.cleanup_projection_fixture()
        runtime_text = self.encode_runtime(self.runtime_snapshot_payload())
        with self.assertRaises(checker.ValidationError):
            checker.validate_texts(
                blueprint,
                outputs[generator.GANTT],
                outputs[generator.STATUS],
                outputs[generator.KANBAN],
                runtime_text,
                receipt_text,
                pre_cleanup_text,
                verifier_bytes,
            )
        with self.assertRaises(generator.CHECKER.ValidationError):
            generator._validated_inputs(runtime_text, receipt_text)

    def test_cleanup_receipt_is_rejected_before_all_items_are_accepted(self) -> None:
        pre_cleanup_text = self.encode_cleanup(self.pre_cleanup_receipt_payload(self.blueprint))
        verifier_bytes = self.cleanup_verifier_bytes()
        receipt_text = self.encode_cleanup(
            self.cleanup_receipt_payload(self.blueprint, pre_cleanup_text, verifier_bytes)
        )
        with self.assertRaises(checker.ValidationError):
            checker.parse_cleanup_receipt(
                receipt_text,
                self.blueprint,
                self.tasks,
                pre_cleanup_receipt_text=pre_cleanup_text,
                verifier_script_bytes=verifier_bytes,
            )

    def test_cleanup_receipt_requires_full_cadence_wait(self) -> None:
        blueprint = self.all_accepted_blueprint()
        tasks = checker.parse_tasks(blueprint)
        pre_cleanup_text = self.encode_cleanup(self.pre_cleanup_receipt_payload(blueprint))
        verifier_bytes = self.cleanup_verifier_bytes()
        payload = self.cleanup_receipt_payload(blueprint, pre_cleanup_text, verifier_bytes)
        payload["verified_at"] = "2026-08-09T22:41:00Z"
        payload["issued_at"] = "2026-08-09T22:41:00Z"
        with self.assertRaises(checker.ValidationError):
            checker.parse_cleanup_receipt(
                self.encode_cleanup(payload),
                blueprint,
                tasks,
                pre_cleanup_receipt_text=pre_cleanup_text,
                verifier_script_bytes=verifier_bytes,
            )

    def test_cleanup_receipt_requires_external_successful_command_evidence(self) -> None:
        blueprint = self.all_accepted_blueprint()
        tasks = checker.parse_tasks(blueprint)
        pre_cleanup_text = self.encode_cleanup(self.pre_cleanup_receipt_payload(blueprint))
        verifier_bytes = self.cleanup_verifier_bytes()
        payload = self.cleanup_receipt_payload(blueprint, pre_cleanup_text, verifier_bytes)
        payload["verifier"]["independent_of_controller"] = False
        with self.assertRaises(checker.ValidationError):
            checker.parse_cleanup_receipt(
                self.encode_cleanup(payload),
                blueprint,
                tasks,
                pre_cleanup_receipt_text=pre_cleanup_text,
                verifier_script_bytes=verifier_bytes,
            )

    def test_cleanup_receipt_rejects_noop_or_unrelated_verifier_argv(self) -> None:
        blueprint, pre_cleanup_text, verifier_bytes, receipt_text, _outputs = self.cleanup_projection_fixture()
        tasks = checker.parse_tasks(blueprint)
        payload = json.loads(receipt_text)
        payload["verifier"]["commands"][0]["argv"] = ["true"]
        payload["receipt_id"] = checker.content_addressed_id("stage3-cleanup", payload, "receipt_id")
        with self.assertRaises(checker.ValidationError):
            checker.parse_cleanup_receipt(
                self.encode_cleanup(payload),
                blueprint,
                tasks,
                pre_cleanup_receipt_text=pre_cleanup_text,
                verifier_script_bytes=verifier_bytes,
            )

    def test_cleanup_receipt_rejects_forged_structured_absence_output(self) -> None:
        blueprint, pre_cleanup_text, verifier_bytes, receipt_text, _outputs = self.cleanup_projection_fixture()
        tasks = checker.parse_tasks(blueprint)
        payload = json.loads(receipt_text)
        command = payload["verifier"]["commands"][0]
        stdout_payload = json.loads(command["stdout"])
        stdout_payload["queries"]["runtime_root"] = {
            "query": checker.CLEANUP_QUERY_NAMES["runtime_root"],
            "raw_result": [".ops/stage3-execution-v1"],
            "absent": False,
        }
        command["stdout"] = checker._canonical_json_bytes(stdout_payload).decode("utf-8") + "\n"
        command["stdout_sha256"] = checker.sha256_text(command["stdout"])
        command["stdout_payload_sha256"] = checker.canonical_json_sha256(stdout_payload)
        payload["absence_recheck"] = stdout_payload["queries"]
        payload["receipt_id"] = checker.content_addressed_id("stage3-cleanup", payload, "receipt_id")
        with self.assertRaises(checker.ValidationError):
            checker.parse_cleanup_receipt(
                self.encode_cleanup(payload),
                blueprint,
                tasks,
                pre_cleanup_receipt_text=pre_cleanup_text,
                verifier_script_bytes=verifier_bytes,
            )

    def test_cleanup_receipt_rejects_verifier_script_digest_drift(self) -> None:
        blueprint, pre_cleanup_text, verifier_bytes, receipt_text, _outputs = self.cleanup_projection_fixture()
        tasks = checker.parse_tasks(blueprint)
        payload = json.loads(receipt_text)
        payload["verifier"]["script_sha256"] = "9" * 64
        payload["receipt_id"] = checker.content_addressed_id("stage3-cleanup", payload, "receipt_id")
        with self.assertRaises(checker.ValidationError):
            checker.parse_cleanup_receipt(
                self.encode_cleanup(payload),
                blueprint,
                tasks,
                pre_cleanup_receipt_text=pre_cleanup_text,
                verifier_script_bytes=verifier_bytes,
            )

    def test_cleanup_receipt_requires_canonical_pre_cleanup_file(self) -> None:
        blueprint, _pre_cleanup_text, verifier_bytes, receipt_text, _outputs = self.cleanup_projection_fixture()
        tasks = checker.parse_tasks(blueprint)
        original = checker.PRE_CLEANUP_RECEIPT
        try:
            with tempfile.TemporaryDirectory() as directory:
                checker.PRE_CLEANUP_RECEIPT = Path(directory) / "missing.json"
                with self.assertRaises(checker.ValidationError):
                    checker.parse_cleanup_receipt(
                        receipt_text,
                        blueprint,
                        tasks,
                        verifier_script_bytes=verifier_bytes,
                    )
        finally:
            checker.PRE_CLEANUP_RECEIPT = original

    def test_pre_cleanup_receipt_rejects_wrong_state_and_stale_blueprint_digest(self) -> None:
        blueprint = self.all_accepted_blueprint()
        tasks = checker.parse_tasks(blueprint)
        for key, value in (("state", "not_started"), ("raw_blueprint_sha256", "8" * 64)):
            with self.subTest(key=key):
                payload = self.pre_cleanup_receipt_payload(blueprint)
                payload[key] = value
                payload["receipt_id"] = checker.content_addressed_id(
                    "stage3-pre-cleanup", payload, "receipt_id"
                )
                with self.assertRaises(checker.ValidationError):
                    checker.parse_pre_cleanup_receipt(self.encode_cleanup(payload), blueprint, tasks)

    def test_pre_cleanup_receipt_rejects_projection_digest_id_mismatch(self) -> None:
        blueprint = self.all_accepted_blueprint()
        tasks = checker.parse_tasks(blueprint)
        payload = self.pre_cleanup_receipt_payload(blueprint)
        payload["final_pre_teardown_projection"]["projection_input_sha256"] = "7" * 64
        payload["receipt_id"] = checker.content_addressed_id(
            "stage3-pre-cleanup", payload, "receipt_id"
        )
        with self.assertRaises(checker.ValidationError):
            checker.parse_pre_cleanup_receipt(self.encode_cleanup(payload), blueprint, tasks)

    def test_pre_cleanup_receipt_binds_exact_archived_projection_bytes(self) -> None:
        blueprint = self.all_accepted_blueprint()
        tasks = checker.parse_tasks(blueprint)
        payload = self.pre_cleanup_receipt_payload(blueprint)
        gantt = payload["final_pre_teardown_projection"]["surfaces"]["gantt"]
        gantt["text"] += "False terminal claim.\n"
        gantt["sha256"] = checker.sha256_text(gantt["text"])
        payload["receipt_id"] = checker.content_addressed_id(
            "stage3-pre-cleanup", payload, "receipt_id"
        )
        with self.assertRaises(checker.ValidationError):
            checker.parse_pre_cleanup_receipt(self.encode_cleanup(payload), blueprint, tasks)

    def test_cleanup_verifier_observation_must_finish_with_the_command(self) -> None:
        blueprint, pre_cleanup_text, verifier_bytes, receipt_text, _outputs = (
            self.cleanup_projection_fixture()
        )
        tasks = checker.parse_tasks(blueprint)
        payload = json.loads(receipt_text)
        payload["verifier"]["commands"][0]["finished_at"] = "2026-08-09T22:42:00Z"
        payload["receipt_id"] = checker.content_addressed_id(
            "stage3-cleanup", payload, "receipt_id"
        )
        with self.assertRaises(checker.ValidationError):
            checker.parse_cleanup_receipt(
                self.encode_cleanup(payload),
                blueprint,
                tasks,
                pre_cleanup_receipt_text=pre_cleanup_text,
                verifier_script_bytes=verifier_bytes,
            )

    def test_cleanup_receipt_rejects_stale_pre_cleanup_reference(self) -> None:
        blueprint, pre_cleanup_text, verifier_bytes, receipt_text, _outputs = self.cleanup_projection_fixture()
        tasks = checker.parse_tasks(blueprint)
        payload = json.loads(receipt_text)
        payload["pre_cleanup"]["sha256"] = "6" * 64
        payload["receipt_id"] = checker.content_addressed_id("stage3-cleanup", payload, "receipt_id")
        with self.assertRaises(checker.ValidationError):
            checker.parse_cleanup_receipt(
                self.encode_cleanup(payload),
                blueprint,
                tasks,
                pre_cleanup_receipt_text=pre_cleanup_text,
                verifier_script_bytes=verifier_bytes,
            )

    def test_runtime_snapshot_cannot_self_declare_cleanup_complete(self) -> None:
        payload = self.runtime_snapshot_payload()
        payload["cleanup_state"] = "complete"
        with self.assertRaises(checker.ValidationError):
            checker.parse_runtime_snapshot(self.encode_runtime(payload), self.tasks)

    # Atomic filesystem and commit-surface order.

    def test_generation_time_reuse_requires_all_three_existing_surfaces_to_validate(self) -> None:
        generated_at = "2026-08-09T22:41:00Z"
        outputs = generator.expected_outputs(generated_at=generated_at)
        original_paths = (generator.GANTT, generator.STATUS, generator.KANBAN)
        try:
            with tempfile.TemporaryDirectory() as directory:
                directory_path = Path(directory)
                generator.GANTT = directory_path / "Stage3_Gantt.md"
                generator.STATUS = directory_path / "Stage3_Status.json"
                generator.KANBAN = directory_path / "Stage3_Kanban.md"
                valid = {
                    generator.GANTT: outputs[original_paths[0]],
                    generator.STATUS: outputs[original_paths[1]],
                    generator.KANBAN: outputs[original_paths[2]],
                }
                for path, text in valid.items():
                    path.write_text(text, encoding="utf-8")
                self.assertEqual(
                    generator.choose_generation_time(None, blueprint_text=self.blueprint), generated_at
                )
                corruptions = {
                    generator.GANTT: valid[generator.GANTT] + "False completion.\n",
                    generator.STATUS: "[" + valid[generator.STATUS][1:],
                    generator.KANBAN: valid[generator.KANBAN].replace(
                        "## Runtime snapshot", "False live claim.\n\n## Runtime snapshot", 1
                    ),
                }
                for target, corrupted in corruptions.items():
                    with self.subTest(target=target.name):
                        for path, text in valid.items():
                            path.write_text(text, encoding="utf-8")
                        target.write_text(corrupted, encoding="utf-8")
                        self.assertNotEqual(
                            generator.choose_generation_time(None, blueprint_text=self.blueprint),
                            generated_at,
                        )
        finally:
            generator.GANTT, generator.STATUS, generator.KANBAN = original_paths

    def test_projection_writer_lock_rejects_a_second_writer_and_direct_writes(self) -> None:
        with generator._projection_writer_lock():
            with self.assertRaises(generator.CHECKER.ValidationError):
                with generator._projection_writer_lock():
                    self.fail("second writer unexpectedly acquired the projection lock")
        with self.assertRaises(ValueError):
            generator.write_outputs({path: path.name for path in generator.OUTPUT_ORDER})

    def test_input_change_before_gantt_prevents_commit_marker(self) -> None:
        calls: list[Path] = []
        checks = 0
        original_assert = generator._assert_projection_inputs_unchanged
        original_replace = generator._atomic_replace
        try:
            def controlled_assert(_inputs, _runtime_path):
                nonlocal checks
                checks += 1
                if checks == 2:
                    raise generator.CHECKER.ValidationError("injected source change")

            generator._assert_projection_inputs_unchanged = controlled_assert
            generator._atomic_replace = lambda path, _content: calls.append(path)
            inputs = generator.ProjectionInputSnapshot(None, b"", None, None, None, None)
            with self.assertRaises(generator.CHECKER.ValidationError):
                generator._commit_outputs(
                    {path: path.name for path in generator.OUTPUT_ORDER},
                    inputs,
                    None,
                )
        finally:
            generator._assert_projection_inputs_unchanged = original_assert
            generator._atomic_replace = original_replace
        self.assertEqual(calls, [generator.STATUS, generator.KANBAN])

    def test_postcommit_projection_drift_is_rejected(self) -> None:
        original_assert = generator._assert_projection_inputs_unchanged
        original_replace = generator._atomic_replace
        original_check = generator._check_outputs
        try:
            generator._assert_projection_inputs_unchanged = lambda *_args: None
            generator._atomic_replace = lambda *_args: None
            generator._check_outputs = lambda *_args, **_kwargs: ["Docs/Stage3_Status.json"]
            inputs = generator.ProjectionInputSnapshot(None, b"", None, None, None, None)
            with self.assertRaises(generator.CHECKER.ValidationError):
                generator._commit_outputs(
                    {path: path.name for path in generator.OUTPUT_ORDER}, inputs, None
                )
        finally:
            generator._assert_projection_inputs_unchanged = original_assert
            generator._atomic_replace = original_replace
            generator._check_outputs = original_check

    def test_atomic_replace_failure_preserves_existing_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "surface.md"
            target.write_text("old\n", encoding="utf-8")

            def fail_replace(_source, _target):
                raise OSError("injected replace failure")

            with self.assertRaises(OSError):
                generator._atomic_replace(target, "new\n", replace_func=fail_replace)
            self.assertEqual(target.read_text(encoding="utf-8"), "old\n")
            self.assertEqual(list(Path(directory).glob(".surface.md.*.tmp")), [])

    def test_projection_write_order_places_gantt_last(self) -> None:
        calls: list[Path] = []
        generator.write_outputs(
            {path: path.name for path in generator.OUTPUT_ORDER},
            writer=lambda path, _content: calls.append(path),
        )
        self.assertEqual(calls, [generator.STATUS, generator.KANBAN, generator.GANTT])

    def test_pre_gantt_failure_never_replaces_gantt(self) -> None:
        calls: list[Path] = []

        def fail_on_kanban(path: Path, _content: str) -> None:
            calls.append(path)
            if path == generator.KANBAN:
                raise OSError("injected Kanban failure")

        with self.assertRaises(OSError):
            generator.write_outputs(
                {path: path.name for path in generator.OUTPUT_ORDER},
                writer=fail_on_kanban,
            )
        self.assertEqual(calls, [generator.STATUS, generator.KANBAN])
        self.assertNotIn(generator.GANTT, calls)


if __name__ == "__main__":
    unittest.main()
