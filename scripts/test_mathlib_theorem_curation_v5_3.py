#!/usr/bin/env python3
"""Replay and mutation tests for the Stage5 v5.3 mathlib curation."""

from __future__ import annotations

from collections import Counter
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "Docs/tools/build_mathlib_theorem_curation_v5_3.py"
CURATION_PATH = (
    ROOT / "Docs/catalog/v5/curation/Mathlib_Theorem_Curation_v5_3.json"
)

SPEC = importlib.util.spec_from_file_location(
    "build_mathlib_theorem_curation_v5_3", BUILDER_PATH
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import v5.3 mathlib curation builder")
builder = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = builder
SPEC.loader.exec_module(builder)


class MathlibTheoremCurationV53Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        (
            cls.registry,
            cls.receipt,
            cls.registry_authority,
            cls.receipt_authority,
        ) = builder.load_versioned_bindings()
        cls.source, cls.source_rows, cls.source_payload = builder.load_source()
        (
            cls.parent_manifest,
            cls.parent_catalog,
            cls.parent_rows,
            _manifest_payload,
            _catalog_payload,
        ) = builder.load_parent()
        cls.source_by_id = {
            row["source_record_id"]: row for row in cls.source_rows
        }
        (
            cls.source_links,
            cls.parent_links,
            cls.viable,
        ) = builder.resolve_duplicates(cls.source_rows, cls.parent_rows)
        cls.selected, cls.seed_ids = builder.select_balanced(cls.viable)
        cls.rebuilt = builder.build_curation()
        cls.rebuilt_bytes = builder.encoded_document(cls.rebuilt)
        cls.actual_bytes = CURATION_PATH.read_bytes()
        cls.actual = json.loads(cls.actual_bytes.decode("utf-8"))

    def test_committed_authority_is_current_canonical_and_sealed(self) -> None:
        self.assertEqual(self.actual_bytes, self.rebuilt_bytes)
        self.assertTrue(self.actual_bytes.endswith(b"\n"))
        self.assertNotIn(b"\n", self.actual_bytes[:-1])
        self.assertEqual(
            self.actual["authority_sha256"], builder.artifact_authority(self.actual)
        )
        self.assertEqual(
            self.actual["source_registry_authority_sha256"],
            self.registry_authority,
        )
        self.assertEqual(
            self.actual["parent_receipt_authority_sha256"], self.receipt_authority
        )
        builder.validate_generated(
            self.actual,
            self.source_rows,
            self.parent_rows,
            self.registry_authority,
            self.receipt_authority,
        )

    def test_all_1500_rows_have_one_exact_terminal_disposition(self) -> None:
        rows = self.actual["candidate_dispositions"]
        counts = self.actual["counts"]
        by_disposition = Counter(row["disposition"] for row in rows)
        self.assertEqual(len(rows), 1500)
        self.assertEqual(len({row["source_record_id"] for row in rows}), 1500)
        self.assertEqual(counts["eligible_literal_theorems"], 1235)
        self.assertEqual(counts["pre_eligibility_excluded_lemmas"], 265)
        self.assertEqual(counts["accepted"], 500)
        self.assertEqual(counts["nonaccepted_eligible"], 735)
        self.assertEqual(counts["nonaccepted_total"], 1000)
        self.assertEqual(
            by_disposition,
            Counter(
                {
                    "accepted_new_kernel_checked_theorem": 500,
                    "eligible_not_selected": 731,
                    "rejected_nonliteral_lemma": 265,
                    "rejected_source_semantic_duplicate": 4,
                }
            ),
        )

    def test_accepted_rows_are_literal_sorry_free_theorems_with_contiguous_ids(self) -> None:
        accepted = sorted(
            (
                row
                for row in self.actual["candidate_dispositions"]
                if row["disposition"] == "accepted_new_kernel_checked_theorem"
            ),
            key=lambda row: row["accepted_rank"],
        )
        self.assertEqual(len(accepted), 500)
        self.assertEqual([row["accepted_rank"] for row in accepted], list(range(1, 501)))
        self.assertEqual(accepted[0]["target_variant_id"], "ATV-00006585")
        self.assertEqual(accepted[0]["target_s5_id"], "S5-CLM-00006585")
        self.assertEqual(accepted[-1]["target_variant_id"], "ATV-00007084")
        self.assertEqual(accepted[-1]["target_s5_id"], "S5-CLM-00007084")
        for row in accepted:
            source = self.source_by_id[row["source_record_id"]]
            self.assertEqual(source["declaration_kind"], "theorem")
            self.assertEqual(source["source_syntax_kind"], "theorem")
            self.assertEqual(source["formal_proof_state"], "kernel_checked_sorry_free")
            self.assertFalse(source["proof_evidence"]["uses_sorry"])
            self.assertNotIn(
                "sorryAx", source["proof_evidence"]["batch_axiom_dependency_union"]
            )
            self.assertTrue(row["grants_catalog_entry"])
            self.assertTrue(row["grants_theorem_credit"])
        self.assertEqual(len({row["declaration"] for row in accepted}), 500)
        self.assertEqual(len({row["formal_type_sha256"] for row in accepted}), 500)
        self.assertEqual(len({row["semantic_key"] for row in accepted}), 500)

    def test_all_deduplicated_docs_1000_theorems_are_seeded_first(self) -> None:
        raw_docs = [
            row
            for row in self.source_rows
            if row["declaration_kind"] == "theorem"
            and builder.DOCS_SIGNAL in builder.importance_signal_kinds(row)
        ]
        self.assertEqual(len(raw_docs), 181)
        self.assertEqual(len(self.seed_ids), 180)
        accepted = sorted(
            (
                row
                for row in self.actual["candidate_dispositions"]
                if row["accepted_rank"] is not None
            ),
            key=lambda row: row["accepted_rank"],
        )
        first_phase_ids = {row["source_record_id"] for row in accepted[:180]}
        self.assertEqual(first_phase_ids, self.seed_ids)
        self.assertTrue(
            all(
                row["reason_code"] == "selected_docs_1000_priority_seed"
                for row in accepted[:180]
            )
        )
        self.assertTrue(
            all(
                builder.DOCS_SIGNAL
                in builder.importance_signal_kinds(
                    self.source_by_id[row["source_record_id"]]
                )
                for row in accepted[:180]
            )
        )
        self.assertTrue(
            all(
                builder.DOCS_SIGNAL
                not in builder.importance_signal_kinds(
                    self.source_by_id[row["source_record_id"]]
                )
                for row in accepted[180:]
            )
        )

    def test_phase_two_replays_bytewise_module_root_sweeps(self) -> None:
        accepted_ids = [
            row["source_record_id"]
            for row in sorted(
                (
                    row
                    for row in self.actual["candidate_dispositions"]
                    if row["accepted_rank"] is not None
                ),
                key=lambda row: row["accepted_rank"],
            )
        ]
        self.assertEqual(
            accepted_ids, [row["source_record_id"] for row in self.selected]
        )
        fill = self.selected[180:]
        self.assertEqual(len(fill), 320)
        self.assertTrue(
            all(
                builder.MODULE_MAIN_SIGNAL in builder.importance_signal_kinds(row)
                for row in fill
            )
        )
        dispositions = {
            row["source_record_id"]: row
            for row in self.actual["candidate_dispositions"]
        }
        self.assertTrue(
            all(
                dispositions[row["source_record_id"]]["reason_code"]
                == "selected_module_main_round_robin_fill"
                for row in fill
            )
        )
        fill_counts = Counter(builder.module_root(row) for row in fill)
        self.assertEqual(len(fill_counts), 21)
        self.assertEqual(max(fill_counts.values()), 24)
        self.assertEqual(
            self.actual["counts"]["module_main_balanced_fill"], 320
        )
        self.assertEqual(
            self.actual["counts"]["selected_by_module_root"]["Analysis"], 75
        )

    def test_three_formal_type_components_have_exact_canonical_links(self) -> None:
        expected_rank_links = {38: 36, 378: 327, 618: 617, 619: 617}
        source_by_rank = {row["selection_rank"]: row for row in self.source_rows}
        rows_by_source = {
            row["source_record_id"]: row
            for row in self.actual["candidate_dispositions"]
        }
        self.assertEqual(len(self.source_links), 4)
        for losing_rank, canonical_rank in expected_rank_links.items():
            loser = source_by_rank[losing_rank]
            canonical = source_by_rank[canonical_rank]
            self.assertEqual(
                self.source_links[loser["source_record_id"]],
                canonical["source_record_id"],
            )
            disposition = rows_by_source[loser["source_record_id"]]
            self.assertEqual(
                disposition["disposition"], "rejected_source_semantic_duplicate"
            )
            self.assertEqual(
                disposition["canonical_source_record_id"],
                canonical["source_record_id"],
            )
            self.assertEqual(
                disposition["duplicate_of_semantic_key"],
                builder.semantic_key(canonical),
            )
            self.assertEqual(disposition["dedupe_confidence"], "exact")
            self.assertIsNone(disposition["accepted_rank"])
        self.assertEqual(self.parent_links, {})

    def test_whitespace_normalized_formal_type_duplicate_is_rejected(self) -> None:
        canonical, loser = sorted(
            (copy.deepcopy(row) for row in self.viable[:2]),
            key=builder.duplicate_winner_rank,
        )
        loser["formal_type"] = canonical["formal_type"] + " "
        loser["formal_type_sha256"] = builder.sha256_bytes(
            loser["formal_type"].encode("utf-8")
        )
        self.assertNotEqual(
            loser["formal_type_sha256"], canonical["formal_type_sha256"]
        )
        self.assertEqual(
            builder.normalized_formal_type(loser["formal_type"]),
            builder.normalized_formal_type(canonical["formal_type"]),
        )

        mutated_sources = [
            loser if row["source_record_id"] == loser["source_record_id"] else row
            for row in self.source_rows
        ]
        source_links, parent_links, viable = builder.resolve_duplicates(
            mutated_sources, self.parent_rows
        )
        self.assertEqual(parent_links, {})
        self.assertEqual(
            source_links[loser["source_record_id"]], canonical["source_record_id"]
        )
        self.assertNotIn(
            loser["source_record_id"],
            {row["source_record_id"] for row in viable},
        )

        rows, _selected, _seed_ids, _source_links, _parent_links = (
            builder.build_candidate_rows(mutated_sources, self.parent_rows)
        )
        disposition = next(
            row for row in rows if row["source_record_id"] == loser["source_record_id"]
        )
        self.assertEqual(
            disposition["disposition"], "rejected_source_semantic_duplicate"
        )
        self.assertEqual(
            disposition["duplicate_of_semantic_key"], builder.semantic_key(canonical)
        )
        self.assertIn("whitespace normalization", disposition["dedupe_rationale"])

    def test_parent_exact_identity_mutation_is_excluded(self) -> None:
        source = next(
            row for row in self.viable if row["source_record_id"] in self.seed_ids
        )
        parent = copy.deepcopy(self.parent_rows)
        parent[0]["formal_type_sha256"] = source["formal_type_sha256"]
        source_links, parent_links, viable = builder.resolve_duplicates(
            self.source_rows, parent
        )
        self.assertNotIn(source["source_record_id"], source_links)
        self.assertEqual(
            parent_links[source["source_record_id"]], parent[0]["variant_id"]
        )
        self.assertNotIn(source["source_record_id"], {row["source_record_id"] for row in viable})

    def test_truth_gate_and_source_byte_mutations_fail(self) -> None:
        mutated = copy.deepcopy(self.source_rows[0])
        mutated["proof_evidence"]["uses_sorry"] = True
        with self.assertRaises(builder.CurationError):
            builder.validate_truth_gate(mutated, "mutated")

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "mathlib.json"
            path.write_bytes(self.source_payload + b" ")
            with self.assertRaises(builder.CurationError):
                builder.load_source(path)

    def test_resealed_row_and_selection_mutations_still_fail(self) -> None:
        payload_mutation = copy.deepcopy(self.actual)
        row = payload_mutation["candidate_dispositions"][0]
        row["rights_payload_sha256"] = "0" * 64
        row["row_sha256"] = builder.hash_without(row, "row_sha256")
        payload_mutation["authority_sha256"] = builder.artifact_authority(
            payload_mutation
        )
        with self.assertRaises(builder.CurationError):
            builder.validate_generated(
                payload_mutation,
                self.source_rows,
                self.parent_rows,
                self.registry_authority,
                self.receipt_authority,
            )

        selection_mutation = copy.deepcopy(self.actual)
        selected = next(
            row
            for row in selection_mutation["candidate_dispositions"]
            if row["accepted_rank"] is not None
        )
        selected["reason_code"] = "forged_selection_reason"
        selected["row_sha256"] = builder.hash_without(selected, "row_sha256")
        selection_mutation["authority_sha256"] = builder.artifact_authority(
            selection_mutation
        )
        with self.assertRaises(builder.CurationError):
            builder.validate_generated(
                selection_mutation,
                self.source_rows,
                self.parent_rows,
                self.registry_authority,
                self.receipt_authority,
            )

    def test_cli_check_is_read_only_and_passes(self) -> None:
        before = CURATION_PATH.read_bytes()
        result = subprocess.run(
            [sys.executable, str(BUILDER_PATH), "--check"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn(
            "PASS build_mathlib_theorem_curation_v5_3 (checked)", result.stdout
        )
        self.assertEqual(CURATION_PATH.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
