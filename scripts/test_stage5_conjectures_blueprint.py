#!/usr/bin/env python3
"""Conformance tests for the independent Stage5 conjecture Blueprint."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
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


checker = load(ROOT / "Docs/tools/check_stage5_conjectures_blueprint.py", "stage5_conjecture_blueprint_tests_checker")
generator = load(ROOT / "Docs/tools/generate_stage5_conjectures_gantt.py", "stage5_conjecture_blueprint_tests_gantt")


class Stage5ConjectureBlueprintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.specification, cls.rows, cls.blueprint_raw = checker.parse_blueprint()

    def test_complete_inventory_route_and_independent_cap(self) -> None:
        self.assertEqual(len(self.rows), 16622)
        self.assertEqual(sum(row["item_id"].endswith("-TARGET") for row in self.rows), 1425)
        self.assertEqual(
            sum(row["item_id"].startswith("S5CON-POOL-") for row in self.rows),
            14865,
        )
        checker.validate_spec(self.specification)
        self.assertEqual(self.specification["route_policy"]["provider"], "sub2api")
        self.assertEqual(self.specification["route_policy"]["model"], "gpt-5.6-sol")
        self.assertNotIn("default_limits", self.specification)
        self.assertIn("authenticated_goals", self.specification["concurrency_prompt_contract"]["required_dimensions"])
        self.assertIsNone(self.specification["shared_runtime_root"])
        self.assertEqual(self.specification["worker_transport"], "tmux_codex_tui")
        self.assertEqual(self.specification["goal_command"], "/goal")

    def test_targets_are_pairwise_decoupled(self) -> None:
        targets = [
            row for row in self.rows
            if row["item_id"].endswith("-TARGET")
            or row["item_id"].startswith("S5CON-POOL-")
        ]
        owners: dict[str, str] = {}
        for row in targets:
            self.assertEqual(row["dependencies"], ["S5CON-BOOT-001"])
            for path in row["owned_paths"]:
                self.assertNotIn(path, owners)
                owners[path] = row["item_id"]

    def test_workset_receipt_authenticates_immutable_dag_not_cursor(self) -> None:
        outputs = checker.render_boot_data(
            parsed=(self.specification, self.rows, self.blueprint_raw)
        )
        receipt = json.loads(outputs[checker.WORKSET_RECEIPT])
        self.assertEqual(
            receipt["schema_version"],
            "awesome-theorems/stage5-conjecture-workset-receipt/1.1",
        )
        self.assertNotIn("blueprint_sha256", receipt)
        self.assertEqual(
            receipt["checklist_dag_sha256"],
            json.loads(outputs[checker.WORKSET])["checklist_dag_sha256"],
        )

    def test_gantt_is_same_prefix_and_complete(self) -> None:
        self.assertEqual(generator.GANTT.name, "Stage5_Conjectures_Gantt.md")
        text = generator.GANTT.read_text(encoding="utf-8")
        marker = "<!-- STAGE5-PROOF-DEBT-GANTT-METADATA:BEGIN -->"
        end = "<!-- STAGE5-PROOF-DEBT-GANTT-METADATA:END -->"
        generated_at = json.loads(text.split(marker, 1)[1].split(end, 1)[0].strip()[8:-4])["generated_at"]
        self.assertEqual(text.encode(), generator.render(generated_at))
        self.assertEqual(text.count("\n| \"S5CON-"), 16622)
        self.assertNotIn("- [ ]", text)

    def test_one_object_worker_contract(self) -> None:
        protocol = self.specification["mathematical_object_worker_protocol"]
        for phrase in ("one TARGET", "one task-local tmux", "one private CODEX_HOME", "one thread", "one active /goal"):
            self.assertIn(phrase, protocol["bijection"])
        self.assertIn("opens no reviewer worker", protocol["review"])
        self.assertTrue(
            "same task root, thread and active goal" in protocol["repair"]
            or "exact generation and active goal" in protocol["repair"]
        )

    def test_crouzeix_method_is_bound_without_importing_multiagent_execution(self) -> None:
        prompt = self.specification["conjecture_proof_search_prompt"]
        source = prompt["source"]
        self.assertEqual(source["repository"], "jinshanmu/CrouzeixConjecture")
        self.assertEqual(source["commit"], "f9d5c8d39bece41ceedf6346ef50ad1fb393260e")
        self.assertEqual(source["file_sha256"], "0a0c3000b81efc4d9edc65ec3cd1d53df0d4e69b24bfee9fe0860301d853d6fc")
        self.assertEqual(prompt["resolution_roots"], ["Claim", "Not Claim"])
        self.assertTrue(prompt["approach_registry"]["required"])
        self.assertEqual(prompt["execution_adaptation"]["child_agents"], "forbidden")
        self.assertEqual(prompt["execution_adaptation"]["upstream_multiagent_shape"], "not imported")
        targets = [row for row in self.rows if row["item_id"].endswith("-TARGET")]
        self.assertTrue(all("theorem-equivalent missing-lemma routes blocked" in row["gate"] for row in targets))
        self.assertTrue(all("adversarially audit every candidate" in row["gate"] for row in targets))
        text = self.blueprint_raw.decode("utf-8")
        self.assertIn("Injected conjecture proof-search discipline", text)
        self.assertNotIn("gpt-5.6-sol-wm", text)

    def test_occurrence_intake_is_non_credit_bearing_and_not_proof_search(self) -> None:
        intake = self.specification["conjecture_occurrence_intake_contract"]
        self.assertEqual(intake["source_occurrence_denominator"], 14865)
        self.assertIn("do not attempt a proof", intake["short_goal_clause"])
        rows = [row for row in self.rows if row["item_id"].startswith("S5CON-POOL-")]
        self.assertEqual(len(rows), 14865)
        for row in (rows[0], rows[len(rows) // 2], rows[-1]):
            self.assertTrue(row["item_id"].endswith("-INTAKE"))
            self.assertIn("not a strict conjecture credit", row["gate"])
            self.assertIn("intake x means adjudication complete", row["gate"])
            self.assertNotIn("conjecture proved/refuted.", row["title"])


if __name__ == "__main__":
    unittest.main()
