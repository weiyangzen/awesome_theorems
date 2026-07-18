#!/usr/bin/env python3
"""Focused fail-closed tests for the Stage1 target inspection CLI."""

from __future__ import annotations

import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


MODULE = Path(__file__).with_name("stage1_target.py")
SPEC = importlib.util.spec_from_file_location("stage1_target_under_test", MODULE)
assert SPEC is not None and SPEC.loader is not None
target = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(target)


class Stage1TargetTests(unittest.TestCase):
    def write_dag(self, value: dict) -> Path:
        temporary = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False)
        self.addCleanup(Path(temporary.name).unlink, missing_ok=True)
        with temporary:
            json.dump(value, temporary)
        return Path(temporary.name)

    def test_theorem_dag_schema_must_be_exactly_2_1(self) -> None:
        for schema in ("stage1-theorem-dag/2.0", "stage1-theorem-dag/2.2"):
            with self.subTest(schema=schema):
                path = self.write_dag({"schema_version": schema, "theorems": []})
                with (
                    mock.patch.object(target, "THEOREM_DAG", path),
                    self.assertRaisesRegex(SystemExit, "expected stage1-theorem-dag/2.1"),
                ):
                    target.load_theorem_dag()

    def test_check_also_enforces_theorem_dag_schema(self) -> None:
        with (
            mock.patch.object(target, "load_theorem_dag") as load_dag,
            mock.patch("sys.stdout", io.StringIO()),
        ):
            target.command_check([{"baseline": "L0"}] * 1546)
        load_dag.assert_called_once_with()

    def test_show_rejects_a_stale_focus_projection(self) -> None:
        theorem_id = "THM-M-0001"
        projection = {
            "receipt_sha256": None,
            "phase_permissions": {"intake": True},
            "execution_disposition": "research_required",
        }
        dag = {
            "schema_version": target.THEOREM_DAG_SCHEMA,
            "theorems": [{
                "theorem_id": theorem_id,
                "v2_execution_rank": 1,
                "focus_eligibility": projection,
            }],
        }
        targets = [{"theorem_id": theorem_id, "target_lane": "legacy"}]
        with (
            mock.patch.object(target, "load_theorem_dag", return_value=dag),
            mock.patch.object(
                target.focus_eligibility,
                "load_focus_eligibility",
                return_value={**projection, "valid": False},
            ) as evaluate,
            self.assertRaisesRegex(SystemExit, "projection is stale"),
        ):
            target.command_show(targets, theorem_id)
        evaluate.assert_called_once_with(
            target.ROOT, theorem_id, expected_projection_sha256=None
        )

    def test_next_uses_live_focus_and_skips_current_denials(self) -> None:
        allowed_id = "THM-M-0001"
        denied_id = "THM-M-0002"
        allowed_projection = {
            "receipt_sha256": None,
            "execution_disposition": "research_required",
            "phase_permissions": {"intake": True},
        }
        denied_projection = copy.deepcopy(allowed_projection)
        denied_projection["phase_permissions"]["intake"] = False
        dag = {
            "schema_version": target.THEOREM_DAG_SCHEMA,
            "theorems": [
                {
                    "theorem_id": denied_id,
                    "v2_execution_rank": 1,
                    "focus_eligibility": denied_projection,
                },
                {
                    "theorem_id": allowed_id,
                    "v2_execution_rank": 2,
                    "focus_eligibility": allowed_projection,
                },
            ],
        }
        targets = [
            {"theorem_id": allowed_id, "name": "Allowed"},
            {"theorem_id": denied_id, "name": "Denied"},
        ]

        def current_focus(_root, theorem_id, *, expected_projection_sha256=None):
            node = next(row for row in dag["theorems"] if row["theorem_id"] == theorem_id)
            return copy.deepcopy(node["focus_eligibility"])

        output = io.StringIO()
        with (
            mock.patch.object(target, "load_theorem_dag", return_value=dag),
            mock.patch.object(
                target.focus_eligibility,
                "load_focus_eligibility",
                side_effect=current_focus,
            ) as evaluate,
            mock.patch("sys.stdout", output),
        ):
            target.command_next(targets, 1, 1)
        self.assertEqual(output.getvalue(), "0002\tTHM-M-0001\tresearch_required\tAllowed\n")
        self.assertEqual(evaluate.call_count, 2)


if __name__ == "__main__":
    unittest.main()
