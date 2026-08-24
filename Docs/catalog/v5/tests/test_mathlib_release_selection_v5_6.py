"""Mutation tests for the 5.6 non-credit mathlib selection operand."""

from __future__ import annotations

import copy
from pathlib import Path
import subprocess
import sys
import unittest

from Docs.catalog.v5.tools import check_mathlib_release_selection_v5_6 as checker


class MathlibReleaseSelectionV56Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[4]
        cls.result = checker.verify(cls.root)
        cls.selection = cls.result["selection"]

    def reseal(self, document: dict) -> None:
        for row in document["candidate_dispositions"]:
            row["row_sha256"] = checker.hash_without(row, "row_sha256")
        document["authority_sha256"] = checker.hash_without(document, "authority_sha256")

    def test_independent_replay_passes(self) -> None:
        self.assertEqual(checker.main(["--repo-root", str(self.root), "--quiet"]), 0)

    def test_acceptance_receipt_is_deterministic(self) -> None:
        observed = checker.load_json(self.root, checker.SELECTION_RECEIPT_REL)
        expected = checker.acceptance_receipt(self.root, self.result)
        self.assertEqual(observed, expected)
        checker.verify_seal(observed, "test selection receipt")

    def test_all_1561_rows_have_exact_noncredit_dispositions(self) -> None:
        rows = self.selection["candidate_dispositions"]
        self.assertEqual(len(rows), 1561)
        self.assertEqual(
            {row["disposition"] for row in rows},
            {
                "selected_for_joint_5_6_release_transaction",
                "terminal_ready_unselected_in_5_6",
                "preserved_semantic_variant_review_quarantine",
            },
        )
        self.assertTrue(
            all(
                row["grants_catalog_entry"] is False
                and row["grants_theorem_credit"] is False
                and row["target_variant_id"] is None
                and row["target_s5_id"] is None
                for row in rows
            )
        )

    def test_final_generator_does_not_require_zero_credit_putnam_operand(self) -> None:
        generator = self.root / "Docs/catalog/v5/tools/generate_math_catalog_v5_6.py"
        result = subprocess.run(
            [sys.executable, str(generator), "--check"],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("theorem=3500", result.stdout)
        allocation = checker.load_json(
            self.root,
            Path("Docs/catalog/v5/curation/mathlib_reserve_v5_6/Mathlib_Release_Allocation_v5_6.json"),
        )
        self.assertEqual(allocation["counts"]["putnam_credits"], 0)
        self.assertEqual(allocation["counts"]["theorem_credits"], 1000)

    def test_selected_row_cannot_grant_early_credit(self) -> None:
        mutation = copy.deepcopy(self.selection)
        row = next(item for item in mutation["candidate_dispositions"] if item["selected_for_joint_release_transaction"])
        row["grants_theorem_credit"] = True
        self.reseal(mutation)
        with self.assertRaises(checker.CheckError):
            checker.verify(self.root, selection_override=mutation)

    def test_selected_row_cannot_allocate_an_id(self) -> None:
        mutation = copy.deepcopy(self.selection)
        row = next(item for item in mutation["candidate_dispositions"] if item["selected_for_joint_release_transaction"])
        row["target_variant_id"] = "ATV-00008010"
        self.reseal(mutation)
        with self.assertRaises(checker.CheckError):
            checker.verify(self.root, selection_override=mutation)

    def test_quarantine_row_cannot_be_promoted(self) -> None:
        mutation = copy.deepcopy(self.selection)
        row = next(item for item in mutation["candidate_dispositions"] if item["disposition"] == "preserved_semantic_variant_review_quarantine")
        row["disposition"] = "selected_for_joint_5_6_release_transaction"
        row["selected_for_joint_release_transaction"] = True
        row["accepted_rank"] = 1001
        self.reseal(mutation)
        with self.assertRaises(checker.CheckError):
            checker.verify(self.root, selection_override=mutation)

    def test_ready_terminal_row_cannot_replace_priority_selection(self) -> None:
        mutation = copy.deepcopy(self.selection)
        selected = next(item for item in mutation["candidate_dispositions"] if item["accepted_rank"] == 1)
        terminal = next(item for item in mutation["candidate_dispositions"] if item["disposition"] == "terminal_ready_unselected_in_5_6")
        terminal["disposition"] = selected["disposition"]
        terminal["reason_code"] = selected["reason_code"]
        terminal["selection_phase"] = selected["selection_phase"]
        terminal["accepted_rank"] = selected["accepted_rank"]
        terminal["selected_for_joint_release_transaction"] = True
        selected["disposition"] = "terminal_ready_unselected_in_5_6"
        selected["reason_code"] = "release_cap_reached_after_documentation_priority_and_balanced_sweep"
        selected["selection_phase"] = None
        selected["accepted_rank"] = None
        selected["selected_for_joint_release_transaction"] = False
        self.reseal(mutation)
        with self.assertRaises(checker.CheckError):
            checker.verify(self.root, selection_override=mutation)

    def test_hidden_truncation_policy_cannot_change(self) -> None:
        mutation = copy.deepcopy(self.selection)
        mutation["selection_policy"]["hidden_truncation"] = True
        self.reseal(mutation)
        with self.assertRaises(checker.CheckError):
            checker.verify(self.root, selection_override=mutation)

    def test_candidate_denominator_cannot_drop_a_row(self) -> None:
        mutation = copy.deepcopy(self.selection)
        mutation["candidate_dispositions"].pop()
        self.reseal(mutation)
        with self.assertRaises(checker.CheckError):
            checker.verify(self.root, selection_override=mutation)


if __name__ == "__main__":
    unittest.main()
