#!/usr/bin/env python3
"""Mutation and replay tests for the Stage5 v5.2 curation authority."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "Docs/tools/build_openconjecture_curation_v5_2.py"
LEDGER_PATH = (
    ROOT / "Docs/catalog/v5/curation/OpenConjecture_Curation_v5_2.json"
)

SPEC = importlib.util.spec_from_file_location(
    "build_openconjecture_curation_v5_2", BUILDER_PATH
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import OpenConjecture curation builder")
builder = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = builder
SPEC.loader.exec_module(builder)


class OpenConjectureCurationV52Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract, _registry, source_row, cls.parent = (
            builder.verify_versioned_authorities(
                builder.DEFAULT_CONTRACT_PATH,
                builder.DEFAULT_SOURCE_REGISTRY_PATH,
                builder.DEFAULT_PARENT_CATALOG_PATH,
            )
        )
        cls.pool, _pool_by_hash, cls.source_hashes = (
            builder.load_and_verify_source_assets(
                cls.contract,
                source_row,
                builder.DEFAULT_FULL_PATH,
                builder.DEFAULT_ELIGIBLE_PATH,
            )
        )
        cls.pool_by_id = {int(row["id"]): row for row in cls.pool}
        (
            cls.reviews,
            cls.fragment_hash_by_id,
            cls.shard_by_id,
        ) = builder.load_reviews(builder.DEFAULT_REVIEW_PATHS, cls.pool)
        cls.links, cls.missing_context, cls.cross = builder.load_cross_dedupe(
            builder.DEFAULT_CROSS_DEDUPE_PATH,
            cls.reviews,
            cls.pool_by_id,
            cls.shard_by_id,
            cls.parent,
        )
        cls.rebuilt = builder.build_curation()
        cls.rebuilt_bytes = builder.encoded_document(cls.rebuilt)
        cls.actual_bytes = LEDGER_PATH.read_bytes()
        cls.actual = json.loads(cls.actual_bytes.decode("utf-8"))

    def test_committed_ledger_is_current_canonical_and_self_sealed(self) -> None:
        self.assertEqual(self.actual_bytes, self.rebuilt_bytes)
        self.assertTrue(self.actual_bytes.endswith(b"\n"))
        self.assertNotIn(b"\n", self.actual_bytes[:-1])
        self.assertEqual(
            self.actual["authority_sha256"], builder.artifact_authority(self.actual)
        )
        builder.validate_generated_ledger(self.actual, self.contract, self.pool)

    def test_exact_partition_credit_and_contiguous_allocations(self) -> None:
        rows = self.actual["candidate_dispositions"]
        accepted = [
            row
            for row in rows
            if row["disposition"] == "accepted_new_strict_open_claim"
        ]
        self.assertEqual(len(rows), 889)
        self.assertEqual(len(accepted), 600)
        self.assertEqual(len(rows) - len(accepted), 289)
        self.assertEqual(
            sorted(row["selected_rank"] for row in accepted), list(range(1, 601))
        )
        ranked = sorted(accepted, key=lambda row: row["selected_rank"])
        self.assertEqual(ranked[0]["target_variant_id"], "ATV-00005985")
        self.assertEqual(ranked[0]["target_s5_id"], "S5-CLM-00005985")
        self.assertEqual(ranked[-1]["target_variant_id"], "ATV-00006584")
        self.assertEqual(ranked[-1]["target_s5_id"], "S5-CLM-00006584")
        self.assertEqual(len({row["semantic_key"] for row in accepted}), 600)
        self.assertTrue(
            all(
                row["grants_catalog_entry"]
                and row["grants_strict_conjecture_credit"]
                for row in accepted
            )
        )
        self.assertTrue(
            all(
                row["selected_rank"] is None
                and row["target_variant_id"] is None
                and row["target_s5_id"] is None
                and row["grants_catalog_entry"] is False
                and row["grants_strict_conjecture_credit"] is False
                for row in rows
                if row not in accepted
            )
        )

    def test_selection_replays_category_seed_then_global_fill(self) -> None:
        selected, seeded = builder.select_candidates(
            self.reviews,
            self.pool_by_id,
            set(self.links),
            self.missing_context,
        )
        actual = sorted(
            (
                (row["selected_rank"], row["source_record_id"])
                for row in self.actual["candidate_dispositions"]
                if row["selected_rank"] is not None
            )
        )
        self.assertEqual([record_id for _rank, record_id in actual], selected)
        self.assertEqual(len(seeded), self.actual["counts"]["category_seeded"])
        self.assertEqual(self.actual["counts"]["category_seeded"], 87)
        self.assertEqual(self.actual["counts"]["global_rank_fill"], 513)
        self.assertTrue(
            all(self.pool_by_id[record_id]["primary_category"] for record_id in seeded)
        )
        viable = {
            record_id
            for record_id, review in self.reviews.items()
            if builder._base_review_eligible(review, self.pool_by_id[record_id])
            and record_id not in self.links
            and record_id not in self.missing_context
        }
        self.assertEqual(len(viable), 601)
        ranked_out = [
            row
            for row in self.actual["candidate_dispositions"]
            if row["reason_code"] == "ranked_beyond_exact_600"
        ]
        self.assertEqual([row["source_record_id"] for row in ranked_out], [4556])

    def test_cross_dedupe_and_missing_context_are_applied(self) -> None:
        rows = {
            row["source_record_id"]: row
            for row in self.actual["candidate_dispositions"]
        }
        for record_id in self.missing_context:
            self.assertEqual(
                rows[record_id]["disposition"], "rejected_incoherent_source_block"
            )
            self.assertEqual(
                rows[record_id]["reason_code"],
                "cross_audit_missing_context_for_whole_exact_source_block",
            )
        for record_id, (semantic_key, variant_id) in self.links.items():
            row = rows[record_id]
            self.assertEqual(row["duplicate_of_semantic_key"], semantic_key)
            self.assertEqual(row["duplicate_of_variant_id"], variant_id)
            # Candidate 4532 is deliberately subject to the stronger
            # missing-context rejection while retaining its duplicate link.
            if record_id not in self.missing_context:
                self.assertEqual(row["disposition"], "rejected_semantic_duplicate")
        needs_split = {
            record_id
            for record_id, review in self.reviews.items()
            if review["decision"] == "needs_split"
        }
        self.assertEqual(len(needs_split), 31)
        self.assertTrue(
            all(
                rows[record_id]["disposition"]
                == "rejected_incoherent_source_block"
                for record_id in needs_split
            )
        )

    def test_review_payloads_and_fragment_hashes_are_bound(self) -> None:
        rows = {
            row["source_record_id"]: row
            for row in self.actual["candidate_dispositions"]
        }
        for record_id, review in self.reviews.items():
            row = rows[record_id]
            expected_semantic = builder.final_semantic_key(review)
            self.assertEqual(row["semantic_key"], expected_semantic)
            self.assertEqual(
                row["semantic_key_payload_sha256"],
                builder.sha256_bytes(
                    builder.canonical_json_bytes(
                        {
                            "semantic_key": expected_semantic,
                            "atomic_statement_summary": review[
                                "atomic_statement_summary"
                            ],
                        }
                    )
                ),
            )
            self.assertEqual(
                row["review_fragment_sha256"], self.fragment_hash_by_id[record_id]
            )
        for record_id in (2362, 2420, 2610, 2418, 2417, 810):
            self.assertTrue(self.reviews[record_id]["semantic_key"].startswith("nonclaim/"))
            self.assertEqual(
                self.reviews[record_id]["atomic_statement_summary"],
                self.reviews[record_id]["notes"],
            )

    def test_source_admission_rejects_rights_version_body_label_and_confidence_mutations(self) -> None:
        requirements, arxiv_re = builder._source_requirements(self.contract)
        source = copy.deepcopy(self.pool[0])
        self.assertTrue(builder.source_is_eligible(source, requirements, arxiv_re))
        mutations = (
            {"license_family": "cc_by_nc"},
            {"publication_text_allowed": False},
            {"text_withheld": True},
            {"body_tex": "   "},
            {"latest_label": "not_a_conjecture"},
            {"latest_label_model": "different-model"},
            {"latest_label_confidence": 0.899999},
            {
                "arxiv_id": "2605.20453",
                "source_url": "https://arxiv.org/e-print/2605.20453",
            },
            {"source_url": "https://example.invalid/not-the-versioned-id"},
        )
        for updates in mutations:
            with self.subTest(updates=updates):
                mutated = copy.deepcopy(source)
                mutated.update(updates)
                self.assertFalse(
                    builder.source_is_eligible(mutated, requirements, arxiv_re)
                )

    def test_review_alignment_and_null_acceptance_mutations_fail(self) -> None:
        original_rows = [
            json.loads(line)
            for line in builder.DEFAULT_REVIEW_PATHS[0].read_text(
                encoding="utf-8"
            ).splitlines()
        ]
        mutations = []
        bad_hash = copy.deepcopy(original_rows)
        bad_hash[0]["content_hash"] = "0" * 64
        mutations.append(bad_hash)
        null_accept = copy.deepcopy(original_rows)
        accepted_index = next(
            index for index, row in enumerate(null_accept) if row["decision"] == "accept"
        )
        null_accept[accepted_index]["semantic_key"] = None
        null_accept[accepted_index]["atomic_statement_summary"] = None
        mutations.append(null_accept)
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory) / "review-a.jsonl"
            for rows in mutations:
                temporary.write_bytes(
                    b"".join(
                        builder.canonical_json_bytes(row) + b"\n" for row in rows
                    )
                )
                paths = (temporary, *builder.DEFAULT_REVIEW_PATHS[1:])
                with self.assertRaises(builder.CurationError):
                    builder.load_reviews(paths, self.pool)

    def test_cross_dedupe_overlap_parent_and_context_mutations_fail(self) -> None:
        mutations: list[dict[str, object]] = []
        overlap = copy.deepcopy(self.cross)
        overlap["groups"][0]["duplicate_candidate_ids"].append(
            overlap["groups"][0]["duplicate_candidate_ids"][0]
        )
        mutations.append(overlap)
        bad_parent = copy.deepcopy(self.cross)
        parent_group = next(
            group for group in bad_parent["groups"] if "parent_variant_id" in group
        )
        parent_group["parent_variant_id"] = "ATV-99999999"
        mutations.append(bad_parent)
        bad_context = copy.deepcopy(self.cross)
        bad_context["missing_context_ids"].append(1_000_000)
        mutations.append(bad_context)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cross-dedupe.json"
            for value in mutations:
                path.write_bytes(builder.encoded_document(value))
                with self.assertRaises(builder.CurationError):
                    builder.load_cross_dedupe(
                        path,
                        self.reviews,
                        self.pool_by_id,
                        self.shard_by_id,
                        self.parent,
                    )

    def test_resealed_rights_and_rank_mutations_still_fail(self) -> None:
        rights_mutation = copy.deepcopy(self.actual)
        rights_row = rights_mutation["candidate_dispositions"][0]
        rights_row["rights_payload_sha256"] = "0" * 64
        rights_row["row_sha256"] = builder.hash_without(rights_row, "row_sha256")
        rights_mutation["authority_sha256"] = builder.artifact_authority(
            rights_mutation
        )
        with self.assertRaises(builder.CurationError):
            builder.validate_generated_ledger(
                rights_mutation, self.contract, self.pool
            )

        rank_mutation = copy.deepcopy(self.actual)
        accepted = [
            row
            for row in rank_mutation["candidate_dispositions"]
            if row["selected_rank"] is not None
        ]
        accepted[1]["selected_rank"] = accepted[0]["selected_rank"]
        accepted[1]["target_variant_id"] = accepted[0]["target_variant_id"]
        accepted[1]["target_s5_id"] = accepted[0]["target_s5_id"]
        accepted[1]["row_sha256"] = builder.hash_without(
            accepted[1], "row_sha256"
        )
        rank_mutation["authority_sha256"] = builder.artifact_authority(rank_mutation)
        with self.assertRaises(builder.CurationError):
            builder.validate_generated_ledger(rank_mutation, self.contract, self.pool)

    def test_cli_check_is_read_only_and_passes(self) -> None:
        before = LEDGER_PATH.read_bytes()
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
            "PASS build_openconjecture_curation_v5_2 (checked)", result.stdout
        )
        self.assertEqual(LEDGER_PATH.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
