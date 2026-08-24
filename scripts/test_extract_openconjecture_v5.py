#!/usr/bin/env python3
"""Tests for the rights-safe OpenConjecture Stage5 source pool."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "Docs/tools/extract_openconjecture_v5.py"
POOL_PATH = (
    REPO_ROOT
    / "Docs/catalog/v5/sources/openconjecture-fa03d85-cc-by-real-conf090.jsonl"
)

SPEC = importlib.util.spec_from_file_location("extract_openconjecture_v5", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
extractor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(extractor)


def source_record(**updates: object) -> dict[str, object]:
    record: dict[str, object] = {
        "id": 1,
        "arxiv_id": "2601.00001v1",
        "title": "Example conjecture",
        "published_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
        "authors": ["A. Author"],
        "categories": ["math.NT"],
        "primary_category": "math.NT",
        "doi": "",
        "journal_ref": "",
        "comments": "",
        "abs_url": "https://arxiv.org/abs/2601.00001v1",
        "pdf_url": "https://arxiv.org/pdf/2601.00001v1",
        "source_url": "https://arxiv.org/e-print/2601.00001v1",
        "license_url": extractor.REQUIRED_LICENSE_URL,
        "source_file": "main.tex",
        "index_in_file": 1,
        "start_line": 10,
        "end_line": 12,
        "body_tex": "Every example has the desired property.",
        "plain_text": "Every example has the desired property.",
        "content_hash": "1" * 64,
        "normalized_license_url": extractor.REQUIRED_NORMALIZED_LICENSE_URL,
        "license_family": extractor.REQUIRED_LICENSE_FAMILY,
        "publication_decision": "publish_text",
        "publication_text_allowed": True,
        "publication_text_reason": "creativecommons_license_treated_as_publishable",
        "publication_policy_version": extractor.REQUIRED_PUBLICATION_POLICY,
        "latest_label_model": extractor.REQUIRED_LABEL_MODEL,
        "latest_label": extractor.REQUIRED_LABEL,
        "latest_label_confidence": 0.95,
        "latest_interestingness_score": 0.8,
        "latest_interestingness_confidence": 0.9,
        "latest_interestingness_rationale": "",
        "latest_viability_score": 0.5,
        "latest_viability_confidence": 0.5,
        "latest_viability_rationale": "",
        "latest_assessment_version": extractor.REQUIRED_ASSESSMENT_VERSION,
        "latest_label_rationale": "",
        "latest_evidence_snippet": "",
        "latest_labeled_at": "2026-07-12T00:00:00Z",
        "text_withheld": False,
    }
    record.update(updates)
    return record


class OpenConjectureExtractorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pool_bytes = POOL_PATH.read_bytes()
        cls.pool = [json.loads(line) for line in cls.pool_bytes.splitlines()]

    def test_vendored_pool_digest_and_cardinality(self) -> None:
        self.assertEqual(
            extractor.sha256_bytes(self.pool_bytes),
            "8a698e3af53ca0605a2a8ecd2e3a9944ad84157440a86f3c319effaf9792c6ce",
        )
        self.assertEqual(len(self.pool), extractor.EXPECTED_ELIGIBLE_AFTER_DEDUPE)
        self.assertEqual(len({row["content_hash"] for row in self.pool}), len(self.pool))

    def test_vendored_pool_is_canonical_and_rights_safe(self) -> None:
        self.assertEqual(self.pool_bytes, extractor.encode_pool(self.pool))
        self.assertEqual(
            [row["content_hash"] for row in self.pool],
            sorted(row["content_hash"] for row in self.pool),
        )
        for row in self.pool:
            self.assertTrue(extractor.is_eligible(row))
            self.assertEqual(row["license_family"], "cc_by")
            self.assertFalse(row["text_withheld"])

    def test_release_selection_is_exact_and_deterministic(self) -> None:
        first = extractor.select_release_rows(self.pool)
        second = extractor.select_release_rows(reversed(self.pool))
        self.assertEqual(first, second)
        self.assertEqual(len(first), 600)
        self.assertEqual(len({row["content_hash"] for row in first}), 600)
        self.assertGreaterEqual(
            min(float(row["latest_interestingness_score"]) for row in first), 0.55
        )

    def test_admission_rejects_wrong_rights_status_and_empty_text(self) -> None:
        self.assertTrue(extractor.is_eligible(source_record()))
        self.assertFalse(extractor.is_eligible(source_record(license_family="cc_by_nc")))
        self.assertFalse(extractor.is_eligible(source_record(publication_text_allowed=False)))
        self.assertFalse(extractor.is_eligible(source_record(body_tex="  ")))
        self.assertFalse(extractor.is_eligible(source_record(latest_label_confidence=0.89)))
        self.assertFalse(
            extractor.is_eligible(
                source_record(
                    arxiv_id="2601.00001",
                    source_url="https://arxiv.org/e-print/2601.00001",
                )
            )
        )

    def test_duplicate_prefers_latest_arxiv_version(self) -> None:
        first = source_record(
            id=1,
            arxiv_id="2601.00001v1",
            source_url="https://arxiv.org/e-print/2601.00001v1",
        )
        latest = source_record(
            id=2,
            arxiv_id="2601.00001v3",
            source_url="https://arxiv.org/e-print/2601.00001v3",
        )
        with mock.patch.object(extractor, "EXPECTED_ELIGIBLE_BEFORE_DEDUPE", 2), mock.patch.object(
            extractor, "EXPECTED_ELIGIBLE_AFTER_DEDUPE", 1
        ):
            pool = extractor.build_pool([first, latest])
        self.assertEqual([row["id"] for row in pool], [2])

    def test_pinned_input_hash_and_mutation_are_enforced(self) -> None:
        record = source_record()
        payload = extractor.canonical_json_line(record)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.jsonl"
            path.write_bytes(payload)
            with mock.patch.object(extractor, "UPSTREAM_SIZE_BYTES", len(payload)), mock.patch.object(
                extractor, "UPSTREAM_SHA256", extractor.sha256_bytes(payload)
            ), mock.patch.object(extractor, "UPSTREAM_RECORDS", 1):
                self.assertEqual(extractor.load_upstream(path), [record])
                path.write_bytes(payload + b" ")
                with self.assertRaises(extractor.ExtractionError):
                    extractor.load_upstream(path)


if __name__ == "__main__":
    unittest.main()
