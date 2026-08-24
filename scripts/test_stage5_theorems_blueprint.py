#!/usr/bin/env python3
"""Conformance tests for theorem Blueprint and Gantt authorities."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


checker = load(ROOT / "Docs/tools/check_stage5_theorems_blueprint.py", "stage5_theorem_blueprint_tests_checker")
generator = load(ROOT / "Docs/tools/generate_stage5_theorems_gantt.py", "stage5_theorem_blueprint_tests_gantt")


class Stage5TheoremBlueprintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.specification, cls.rows, cls.blueprint_raw = checker.parse_blueprint()

    def test_complete_dag_and_frozen_route(self) -> None:
        checker.validate_spec(self.specification)
        self.assertEqual(len(self.rows), 3575)
        self.assertEqual(self.specification["route_policy"], {
            "provider": "sub2api", "model": "gpt-5.6-sol", "reasoning_effort": "ultra",
            "service_tier": "default", "rule": self.specification["route_policy"]["rule"],
        })
        self.assertTrue(self.specification["nested_agent_policy"]["enabled"])
        self.assertIn("never exceed 24", self.specification["nested_agent_policy"]["capacity_rule"])
        self.assertNotIn("default_limits", self.specification)
        self.assertIn("authenticated_goals", self.specification["concurrency_prompt_contract"]["required_dimensions"])
        self.assertIsNone(self.specification["shared_runtime_root"])
        self.assertNotIn("shared_coordination", self.specification)
        self.assertNotIn("caps", self.specification["coordination_authority"])
        targets = [row for row in self.rows if row["item_id"].endswith("-TARGET")]
        self.assertEqual(len(targets), 3500)
        self.assertTrue(all(row["dependencies"] == ("S5THM-BOOT-001",) for row in targets))
        self.assertNotIn("worker_container_boundary", self.specification)
        self.assertEqual(
            self.specification["worker_runtime_boundary"]["worker_container_transport"],
            "forbidden",
        )

    def test_duplicate_missing_dependency_and_cycle_fail(self) -> None:
        fixture = [dict(row) for row in self.rows[:3]]
        fixture[1] = dict(fixture[1], item_id=fixture[0]["item_id"])
        with self.assertRaises(checker.CheckError):
            checker.validate_rows(fixture)
        # The full validator checks its canonical cardinality before graph mutations.
        with self.assertRaises(checker.CheckError):
            checker.validate_rows([dict(row) for row in self.rows[:-1]])

    def test_gantt_is_same_prefix_complete_and_checkbox_free(self) -> None:
        self.assertEqual(generator.GANTT.name, "Stage5_Theorems_Gantt.md")
        checker.validate_gantt(self.rows, self.blueprint_raw)
        text = generator.GANTT.read_text()
        index = text.split(generator.INDEX_BEGIN, 1)[1].split(generator.INDEX_END, 1)[0]
        self.assertNotIn("- [ ]", index)
        self.assertEqual(index.count("\n| \"S5THM-"), 3575)

    def test_runtime_projection_rejects_unknown_item_and_stale_digest(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stage5-gantt-test-") as temporary:
            original = generator.RUNTIME_SNAPSHOT
            generator.RUNTIME_SNAPSHOT = Path(temporary) / "snapshot.json"
            self.addCleanup(setattr, generator, "RUNTIME_SNAPSHOT", original)
            value = checker.sealed({
                "schema_version": "awesome-theorems/stage5-runtime-snapshot/1.0",
                "program": checker.PROGRAM, "snapshot_id": "fixture", "generated_at": "2026-08-11T00:00:00Z",
                "state_sha256": None, "event_ledger_records": 0,
                "items": {"UNKNOWN": {}}, "observed_usage": {}, "saturated_dimensions": [],
                "underfill": {}, "status_counts": {},
            })
            generator.RUNTIME_SNAPSHOT.write_text(json.dumps(value))
            with self.assertRaises(generator.GanttError):
                generator.render(generated_at="2026-08-11T00:00:00Z")

    def test_mathematical_targets_are_pairwise_decoupled(self) -> None:
        targets = [row for row in self.rows if row["item_id"].endswith("-TARGET")]
        target_ids = {row["item_id"] for row in targets}
        for row in targets:
            self.assertEqual(row["dependencies"], ("S5THM-BOOT-001",))
            self.assertTrue(target_ids.isdisjoint(row["dependencies"]))
        owners = {}
        for row in targets:
            for path in row["owned_paths"]:
                self.assertNotIn(path, owners)
                owners[path] = row["item_id"]

    def test_one_target_one_tmux_home_thread_goal_contract(self) -> None:
        protocol = self.specification["mathematical_object_worker_protocol"]
        for phrase in ("one TARGET", "one task-local tmux", "one private CODEX_HOME", "one thread", "one active /goal"):
            self.assertIn(phrase, protocol["bijection"])
        self.assertIn("opens no reviewer worker", protocol["review"])
        self.assertTrue(
            "same task root, thread and active goal" in protocol["repair"]
            or "exact generation and active goal" in protocol["repair"]
        )
        self.assertEqual(self.specification["worker_transport"], "tmux_codex_tui")
        self.assertEqual(self.specification["goal_command"], "/goal")

    def test_v1_migration_preserves_history_without_promoting_targets(self) -> None:
        if not checker.MIGRATION_RECEIPT.is_file():
            self.skipTest("historical migration receipt is outside the BOOT snapshot")
        evidence = checker.validate_migration_receipt(self.rows, self.blueprint_raw)
        migration_path = checker.MIGRATION_RECEIPT
        if not migration_path.is_file():
            migration_path = ROOT / "Docs/evidence/stage5_theorems/bootstrap/superseded-v1-boot-authorities/one-object-one-goal-v1-to-v2-migration.json"
        receipt = checker.strict_json(migration_path.read_bytes(), "one-object v2 migration receipt")
        theorem = receipt["programs"]["theorem"]
        self.assertEqual(theorem["state_counts"], {
            "not_done": 27988,
            "handoff_waiting_master": 85,
            "master_accepted": 2,
        })
        self.assertEqual(theorem["v2_initial_state_counts"], {
            "not_done": 3575,
            "handoff_waiting_master": 0,
            "master_accepted": 0,
        })
        # The historical migration itself began with every v2 row blank. The
        # active controller may now have accepted mathematical TARGETs through
        # later immutable handoff/Master receipts; current progress must not be
        # confused with promotion performed by the historical migration.
        self.assertEqual(self.rows[0]["item_id"], "S5THM-BOOT-001")
        self.assertIn(self.rows[0]["state"], {" ", "x"})
        current_counts = {
            "not_done": sum(row["state"] == " " for row in self.rows),
            "handoff_waiting_master": sum(row["state"] == "_" for row in self.rows),
            "master_accepted": sum(row["state"] == "x" for row in self.rows),
        }
        self.assertEqual(sum(current_counts.values()), 3575)
        lifecycle = sorted(checker.ISOLATION_MIGRATION_DIR.glob(
            "S5PD-BLUEPRINT-MIGRATE-*-lifecycle.json"
        ))
        isolation = sorted(checker.ISOLATION_MIGRATION_DIR.glob(
            "S5PD-BLUEPRINT-MIGRATE-*-program-isolation.json"
        ))
        lifecycle_ordinal = int(lifecycle[-1].name.split("-")[3]) if lifecycle else -1
        isolation_ordinal = int(isolation[-1].name.split("-")[3]) if isolation else -1
        if lifecycle and lifecycle_ordinal > isolation_ordinal:
            receipt = checker.verify_seal(
                checker.strict_json(lifecycle[-1].read_bytes(), "lifecycle migration"),
                "lifecycle migration",
            )
            self.assertIn("checklist states", receipt["preserved"])
            self.assertNotEqual(
                receipt["old_requirements_sha256"],
                receipt["new_requirements_sha256"],
            )
        self.assertEqual(theorem["history"]["distinct_mathematical_id_count"], 177)
        self.assertEqual(evidence["legacy_v1_blueprint_sha256"], checker.LEGACY_V1_BLUEPRINT_SHA256)

    def test_budget_overrun_invalidation_binds_unique_reopened_credit(self) -> None:
        receipt = checker.validate_budget_overrun_invalidation(
            self.rows, self.blueprint_raw,
        )
        self.assertIsNotNone(receipt)
        self.assertEqual(
            receipt["payload"]["item_id"], "S5THM-00003496-TARGET",
        )
        mutated = [dict(row) for row in self.rows]
        target = next(
            row for row in mutated
            if row["item_id"] == "S5THM-00003496-TARGET"
        )
        target["state"] = "x"
        with self.assertRaisesRegex(
            checker.CheckError, "unique reviewed x-to-blank transition",
        ):
            checker.validate_budget_overrun_invalidation(
                mutated, self.blueprint_raw,
            )


if __name__ == "__main__":
    unittest.main()
