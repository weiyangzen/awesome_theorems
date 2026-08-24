"""Independent and mutation-oriented tests for Stage5 mathematics release 5.5."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from Docs.catalog.v5.tools import check_math_catalog_v5_5 as checker


class MathCatalogV55Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[4]
        cls.result = checker.verify(cls.root, boundary="auto")
        cls.documents = cls.result["documents"]
        cls.parent = cls.result["parent"]
        cls.new_rows = cls.result["new_rows"]
        cls.expected = {name: cls.documents[name] for name in checker.RELEASE_FILES}

    def test_staged_or_published_release_passes_independent_checker(self) -> None:
        self.assertIn(self.result["boundary"], {"prepublish", "published"})
        self.assertEqual(checker.main(["--repo-root", str(self.root), "--auto-boundary", "--quiet"]), 0)

    def test_pending_source_review_cannot_be_promoted(self) -> None:
        source = {
            "decision": "pending",
            "truth_apt": True,
            "context_complete": True,
            "importance_tier": "high",
            "current_open_as_of_review": True,
        }
        row = {"importance_tier": "high"}
        with self.assertRaises(checker.CheckError):
            checker.check_source_review_gate(source, row, 0)

    def test_question_promotion_mutation_is_rejected(self) -> None:
        mutation = copy.deepcopy(self.result["curation"])
        row = next(item for item in mutation["candidate_dispositions"] if item["decision"] == "accept")
        row["question_to_assertion_promotion_performed"] = True
        row["row_sha256"] = checker.row_hash(row)
        mutation["authority_sha256"] = checker.hash_without(mutation, "authority_sha256")
        original_load = checker.load_json

        def load_mutated(root: Path, relative_path: Path | str, *, canonical_file: bool = True):
            if Path(relative_path) == checker.CURATION_REL:
                return mutation
            return original_load(root, relative_path, canonical_file=canonical_file)

        with mock.patch.object(checker, "load_json", side_effect=load_mutated):
            with self.assertRaises(checker.CheckError):
                checker.check_curation(
                    self.root, self.parent["Claim_Catalog.json"]["records"],
                    self.result["source_authorities"],
                )

    def test_duplicate_strict_credit_is_rejected(self) -> None:
        mutation = copy.deepcopy(self.documents)
        strict = mutation["Strict_Conjecture_Ledger.json"]
        strict["strict_credits"].append(copy.deepcopy(strict["strict_credits"][-1]))
        with self.assertRaises(checker.CheckError):
            checker.validate_strict_catalog_symmetry(mutation, len(self.new_rows))

    def test_parent_prefix_mutation_is_rejected(self) -> None:
        child = copy.deepcopy(self.documents["Claim_Catalog.json"]["records"])
        parent = self.parent["Claim_Catalog.json"]["records"]
        checker.validate_parent_prefix(child, parent, "test catalog")
        child[0]["stage_claim_id"] = "S5-CLM-99999999"
        with self.assertRaises(checker.CheckError):
            checker.validate_parent_prefix(child, parent, "test catalog")

    def test_origin_id_gap_is_rejected(self) -> None:
        mutation = copy.deepcopy(self.new_rows)
        mutation[0]["variant_id"] = "ATV-00007586"
        with self.assertRaises(checker.CheckError):
            checker.validate_dense_origin_ids(mutation)

    def test_strict_catalog_asymmetry_is_rejected(self) -> None:
        mutation = copy.deepcopy(self.documents)
        mutation["Strict_Conjecture_Ledger.json"]["strict_credits"].pop()
        with self.assertRaises(checker.CheckError):
            checker.validate_strict_catalog_symmetry(mutation, len(self.new_rows))

    def test_manifest_extra_file_is_rejected(self) -> None:
        mutation = copy.deepcopy(self.result["manifest"])
        mutation["artifacts"].append({
            "path": "Unlisted_Extra.json", "sha256": "0" * 64,
            "size_bytes": 3, "row_count": 0,
        })
        with self.assertRaises(checker.CheckError):
            checker.validate_manifest_inventory_shape(mutation)

    def test_current_sneak_publish_is_rejected(self) -> None:
        mutation = checker.seal({
            "schema_version": "awesome-theorems/stage5-current-release/5.5",
            "release": "5.5",
            "manifest_path": "releases/5.4/Release_Manifest.json",
            "manifest_sha256": checker.PARENT_MANIFEST_SHA256,
            "release_root_sha256": checker.PARENT_RELEASE_ROOT,
        })
        with self.assertRaises(checker.CheckError):
            checker.validate_current_pointer(self.root, mutation, self.result["manifest"], "auto")

    def test_foreign_repository_root_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(checker.CheckError):
                checker.verify(Path(temporary), boundary="auto")

    def test_duplicate_json_keys_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            path = root / "duplicate.json"
            path.write_text('{"a":1,"a":2}\n', encoding="utf-8")
            with self.assertRaises(checker.CheckError):
                checker.load_json(root, Path("duplicate.json"), canonical_file=False)

    def test_symlinked_authoritative_input_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            target = root / "target.json"
            target.write_text('{}\n', encoding="utf-8")
            (root / "alias.json").symlink_to(target)
            with self.assertRaises(checker.CheckError):
                checker.safe_path(root, Path("alias.json"))

    def test_source_kind_and_path_allowlist_is_closed(self) -> None:
        self.assertTrue(checker.source_path_is_allowed(
            "aimpl", "Docs/catalog/v5/curation/aimpl_v5_5/review-ledger.jsonl"
        ))
        self.assertFalse(checker.source_path_is_allowed(
            "aimpl", "Docs/catalog/v5/curation/oeis_v5_5/v1/reviews/review-00.jsonl"
        ))
        self.assertFalse(checker.source_path_is_allowed(
            "conjecturebench", "Docs/catalog/v5/curation/conjecturebench_v5_5/strict-review-ledger-302.jsonl"
        ))

    def test_origin_claim_closed_schema_rejects_extra_field(self) -> None:
        mutation = copy.deepcopy(self.new_rows)
        mutation[0]["unsealed_extra"] = True
        with self.assertRaises(checker.CheckError):
            checker.validate_origin_rows(mutation, self.new_rows)

    def test_receipt_is_deterministic_and_sealed(self) -> None:
        receipt = self.result["receipt"]
        checker.verify_seal(receipt, "test receipt")
        rebuilt = checker.acceptance_receipt(
            self.root, self.result["manifest"], self.result["curation"],
            self.result["important"], self.result["frontier"], len(self.new_rows),
        )
        self.assertEqual(receipt, rebuilt)


if __name__ == "__main__":
    unittest.main()
