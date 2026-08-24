"""Mutation-oriented tests for the independent Stage5 5.6 checker."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from Docs.catalog.v5.tools import check_math_catalog_v5_6 as checker


class MathCatalogV56Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[4]
        # The same release test suite must remain valid on both sides of the
        # authenticated compare-and-swap.  The checker accepts only the exact
        # 5.5 parent or exact 5.6 target pointer in auto mode.
        cls.result = checker.verify(cls.root, boundary="auto")
        cls.parent = cls.result["parent"]
        cls.documents = cls.result["documents"]
        cls.authorities = cls.result["authorities"]
        cls.new_rows = cls.result["new_rows"]
        cls.manifest = cls.result["manifest"]
        cls.release_payloads = {
            name: (cls.root / checker.RELEASE_REL / name).read_bytes()
            for name in checker.RELEASE_FILES
        }

    def test_baseline_cli_is_read_only_and_does_not_import_generator(self) -> None:
        current = self.root / checker.CURRENT_REL
        receipt = self.root / checker.RECEIPT_REL
        before_current = current.read_bytes()
        before_receipt = receipt.read_bytes() if receipt.exists() else None
        self.assertEqual(
            checker.main(["--repo-root", str(self.root), "--auto", "--quiet"]), 0
        )
        self.assertEqual(current.read_bytes(), before_current)
        self.assertEqual(receipt.read_bytes() if receipt.exists() else None, before_receipt)
        source = (self.root / checker.CHECKER_REL).read_text(encoding="utf-8")
        self.assertNotIn("import generate_math_catalog_v5_6", source)
        self.assertIn(self.result["boundary"], {"prepublish", "published"})

    def test_all_parent_prefix_surfaces_are_immutable(self) -> None:
        cases = (
            ("Claim_Catalog.json", "records"),
            ("Theorem_List.json", "records"),
            ("Open_Claim_List.json", "records"),
            ("Claim_ID_Registry.json", "families"),
            ("Claim_ID_Registry.json", "senses"),
            ("Claim_ID_Registry.json", "variants"),
            ("Stage5_Claim_ID_Registry.json", "mappings"),
            ("Migration_v4_to_v5.json", "migrations"),
            ("Coverage_Ledger.json", "candidate_dispositions"),
            ("Strict_Conjecture_Ledger.json", "strict_credits"),
            ("Strict_Conjecture_Ledger.json", "credit_corrections"),
        )
        for name, key in cases:
            with self.subTest(name=name, key=key):
                documents = dict(self.documents)
                document = dict(documents[name])
                rows = list(document[key])
                rows[0] = {"tampered_parent_object": True}
                document[key] = rows
                documents[name] = document
                with self.assertRaises(checker.CheckError):
                    checker.validate_parent_prefixes(documents, self.parent)

    def test_dense_identity_ranges_reject_duplicates_gaps_and_out_of_range(self) -> None:
        mutations = (
            (0, "variant_id", "ATV-00008011"),
            (1, "occurrence_id", "ATO-00008012"),
            (2, "sense_id", "ATS-00009999"),
            (3, "family_id", "ATF-00007782"),
            (4, "stage_claim_id", "S5-CLM-00000001"),
        )
        for index, field, value in mutations:
            with self.subTest(field=field):
                rows = list(self.new_rows)
                row = dict(rows[index])
                row[field] = value
                rows[index] = row
                with self.assertRaises(checker.CheckError):
                    checker.validate_dense_origin_ids(rows)

    def test_exactly_1000_credits_and_lemma_is_one_theorem_record(self) -> None:
        syntax = [row["formal_statement"]["source_syntax_kind"] for row in self.new_rows]
        self.assertEqual(syntax.count("theorem"), 629)
        self.assertEqual(syntax.count("lemma"), 371)
        self.assertTrue(all(row["claim_kind"] == "theorem" for row in self.new_rows))
        self.assertEqual(len({row["source_locator"]["source_record_id"] for row in self.new_rows}), 1000)

        short = copy.deepcopy(self.authorities["allocation"])
        short["accepted_rows"].pop()
        short["authority_sha256"] = checker.hash_without(short, "authority_sha256")
        with self.assertRaises(checker.CheckError):
            checker.validate_allocation(short, self.authorities["selection"])

        duplicate = copy.deepcopy(self.authorities["allocation"])
        duplicate["accepted_rows"][1] = copy.deepcopy(duplicate["accepted_rows"][0])
        duplicate["authority_sha256"] = checker.hash_without(duplicate, "authority_sha256")
        with self.assertRaises(checker.CheckError):
            checker.validate_allocation(duplicate, self.authorities["selection"])

        putnam = copy.deepcopy(self.authorities["allocation"])
        putnam["counts"]["putnam_credits"] = 1
        putnam["authority_sha256"] = checker.hash_without(putnam, "authority_sha256")
        with self.assertRaises(checker.CheckError):
            checker.validate_allocation(putnam, self.authorities["selection"])

    def test_source_proof_and_allocation_binding_mutations_are_rejected(self) -> None:
        ledger = self.authorities["allocation_rows"][0]
        allocation_sha = checker.file_sha(self.root / checker.ALLOCATION_REL)
        mutations = (
            ("uses_sorry", lambda row: row["proof_evidence"].__setitem__("uses_sorry", True)),
            ("sorryAx", lambda row: row["proof_evidence"]["batch_axiom_dependency_union"].append("sorryAx")),
            ("proof_state", lambda row: row["proof_evidence"].__setitem__("formal_proof_state", "unchecked")),
            ("source_id", lambda row: row["source_locator"].__setitem__("source_record_id", "ML4-FOREIGN")),
            ("source_index", lambda row: row["source_locator"].__setitem__("record_index", 0)),
            ("source_sha", lambda row: row["provenance"].__setitem__("source_record_sha256", "0" * 64)),
            ("declaration", lambda row: row["formal_statement"].__setitem__("declaration", "Mutated.name")),
            ("formal_type", lambda row: row["formal_statement"].__setitem__("formal_type", "False")),
            ("ledger_row", lambda row: row["curator_disposition"].__setitem__("curation_row_sha256", "0" * 64)),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                row = copy.deepcopy(self.new_rows[0])
                mutate(row)
                with self.assertRaises(checker.CheckError):
                    checker.validate_origin_row(
                        row, ledger, self.authorities["source_rows"], self.authorities["schema"],
                        self.authorities["allocation"]["authority_sha256"], allocation_sha,
                    )

    @staticmethod
    def identity_row(formal_type: str, declaration: str, *, exact: str | None = None):
        return {"formal_statement": {
            "formal_type": formal_type,
            "formal_type_sha256": exact or checker.digest(formal_type.encode("utf-8")),
            "declaration": declaration,
        }}

    def test_three_identity_gates_reject_parent_and_batch_conflicts(self) -> None:
        child = self.identity_row("Alpha   Beta", "Fresh.name")
        exact = child["formal_statement"]["formal_type_sha256"]
        parent_cases = (
            {"formal_statement": {"formal_type_sha256": exact}},
            {"formal_statement": {"formal_type": "Alpha Beta"}},
            {"formal_statement": {"declaration": "ＦＲＥＳＨ.NAME"}},
        )
        for parent in parent_cases:
            with self.subTest(parent=parent):
                with self.assertRaises(checker.CheckError):
                    checker.validate_three_identity_gates([parent], [child])

        batch_cases = (
            (self.identity_row("Gamma", "One"), self.identity_row("Gamma", "Two")),
            (self.identity_row("Delta   Epsilon", "Three"),
             self.identity_row("Delta Epsilon", "Four")),
            (self.identity_row("Zeta", "Case.Name"),
             self.identity_row("Eta", "ＣＡＳＥ.name")),
        )
        for first, second in batch_cases:
            with self.subTest(batch=(first, second)):
                with self.assertRaises(checker.CheckError):
                    checker.validate_three_identity_gates([], [first, second])

    def test_all_five_duplicate_losers_are_forbidden(self) -> None:
        expected = {
            "ML4-E57250D080C0DC008AB4", "ML4-FF1EC4354BB7B9D2ACFA",
            "ML4-5DDE00D07425BDCCD751", "ML4-58EEAAF294BB4BE8F298",
            "ML4-4F4AEBB481A1F0C355CE",
        }
        self.assertEqual(self.authorities["loser_ids"], expected)
        for loser in expected:
            row = copy.deepcopy(self.new_rows[0])
            row["source_locator"]["source_record_id"] = loser
            with self.subTest(loser=loser), self.assertRaises(checker.CheckError):
                checker.validate_no_duplicate_losers([row], expected)

    def test_pinned_authority_and_premature_credit_mutations_are_rejected(self) -> None:
        schema = copy.deepcopy(self.authorities["schema"])
        schema["title"] = "tampered"
        schema["authority_sha256"] = checker.hash_without(schema, "authority_sha256")
        with self.assertRaises(checker.CheckError):
            checker.validate_schema(schema)

        contract = copy.deepcopy(self.authorities["contract"])
        contract["quantity_gates"]["origin_theorems_exact"] = 999
        contract["authority_sha256"] = checker.hash_without(contract, "authority_sha256")
        with self.assertRaises(checker.CheckError):
            checker.validate_contract(self.root, contract, self.authorities)

        registry = copy.deepcopy(self.authorities["source_registry"])
        registry["counts"]["selected_release_rows"] = 999
        registry["authority_sha256"] = checker.hash_without(registry, "authority_sha256")
        with self.assertRaises(checker.CheckError):
            checker.validate_source_registry(
                registry, self.authorities["selection"], self.authorities["allocation"],
                self.authorities["generator_receipt"], self.root,
            )

        parent_receipt = copy.deepcopy(self.authorities["parent_receipt"])
        parent_receipt["parent_release_root_sha256"] = "0" * 64
        parent_receipt["authority_sha256"] = checker.hash_without(
            parent_receipt, "authority_sha256")
        with self.assertRaises(checker.CheckError):
            checker.validate_parent_receipt(self.root, parent_receipt, self.parent)

        selection = copy.deepcopy(self.authorities["selection"])
        selected = next(row for row in selection["candidate_dispositions"]
                        if row["selected_for_joint_release_transaction"])
        selected["grants_theorem_credit"] = True
        selected["row_sha256"] = checker.row_hash(selected)
        selection["authority_sha256"] = checker.hash_without(selection, "authority_sha256")
        with self.assertRaises(checker.CheckError):
            checker.validate_selection(
                selection, self.authorities["qualified"], self.authorities["accepted"],
                self.authorities["source_rows"],
            )

        generator_receipt = copy.deepcopy(self.authorities["generator_receipt"])
        generator_receipt["counts"]["theorem_credits_granted_by_receipt"] = 1
        generator_receipt["authority_sha256"] = checker.hash_without(
            generator_receipt, "authority_sha256")
        with self.assertRaises(checker.CheckError):
            checker.validate_candidate_receipts(
                self.authorities["inventory"], generator_receipt,
                self.authorities["selection_receipt"], self.authorities["selection"],
            )

        selection_receipt = copy.deepcopy(self.authorities["selection_receipt"])
        selection_receipt["credit_boundary"]["theorem_credits_granted"] = 1
        selection_receipt["authority_sha256"] = checker.hash_without(
            selection_receipt, "authority_sha256")
        with self.assertRaises(checker.CheckError):
            checker.validate_candidate_receipts(
                self.authorities["inventory"], self.authorities["generator_receipt"],
                selection_receipt, self.authorities["selection"],
            )

    def test_manifest_sha_size_row_count_root_and_shape_mutations_are_rejected(self) -> None:
        mutations = []
        extra = copy.deepcopy(self.manifest)
        extra["artifacts"].append({
            "path": "Extra.json", "sha256": "0" * 64, "size_bytes": 1, "row_count": 0,
        })
        mutations.append(("extra", extra))
        for field, value in (("sha256", "0" * 64), ("size_bytes", 1), ("row_count", 1)):
            mutation = copy.deepcopy(self.manifest)
            mutation["artifacts"][0][field] = value
            mutations.append((field, mutation))
        root = copy.deepcopy(self.manifest)
        root["release_root_sha256"] = "0" * 64
        mutations.append(("root", root))
        order = copy.deepcopy(self.manifest)
        order["artifacts"][0], order["artifacts"][1] = order["artifacts"][1], order["artifacts"][0]
        mutations.append(("order", order))
        for label, mutation in mutations:
            with self.subTest(label=label), self.assertRaises(checker.CheckError):
                checker.validate_manifest_bindings(
                    mutation, self.documents, self.release_payloads)

    def test_manifest_counts_and_nested_quality_must_match_catalog(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["counts"]["variants"] = 9_008
        manifest["authority_sha256"] = checker.hash_without(manifest, "authority_sha256")
        with self.assertRaises(checker.CheckError):
            checker.validate_manifest_semantics(
                manifest, self.documents, self.parent, self.authorities,
                self.result["authoritative_inputs"],
            )

        documents = dict(self.documents)
        catalog = dict(documents["Claim_Catalog.json"])
        catalog["quality_qualification"] = copy.deepcopy(catalog["quality_qualification"])
        catalog["quality_qualification"]["origin_5_6"]["human_semantic_uniqueness_claimed"] = True
        documents["Claim_Catalog.json"] = catalog
        with self.assertRaises(checker.CheckError):
            checker.validate_manifest_semantics(
                self.manifest, documents, self.parent, self.authorities,
                self.result["authoritative_inputs"],
            )

    def test_current_pointer_boundary_truth_table(self) -> None:
        parent = checker.authenticated_parent_pointer()
        target = checker.expected_target_pointer(
            self.result["manifest_file_sha256"], self.manifest["release_root_sha256"])
        self.assertEqual(checker.validate_current_pointer(
            parent, self.manifest, self.result["manifest_file_sha256"], "prepublish"),
            "prepublish")
        self.assertEqual(checker.validate_current_pointer(
            target, self.manifest, self.result["manifest_file_sha256"], "published"),
            "published")
        self.assertEqual(checker.validate_current_pointer(
            parent, self.manifest, self.result["manifest_file_sha256"], "auto"),
            "prepublish")
        self.assertEqual(checker.validate_current_pointer(
            target, self.manifest, self.result["manifest_file_sha256"], "auto"),
            "published")
        with self.assertRaises(checker.CheckError):
            checker.validate_current_pointer(
                target, self.manifest, self.result["manifest_file_sha256"], "prepublish")
        with self.assertRaises(checker.CheckError):
            checker.validate_current_pointer(
                parent, self.manifest, self.result["manifest_file_sha256"], "published")
        hybrid = checker.seal({
            "schema_version": "awesome-theorems/stage5-current-release/5.6",
            "release": "5.6", "manifest_path": "releases/5.6/Release_Manifest.json",
            "manifest_sha256": checker.PARENT_MANIFEST_SHA,
            "release_root_sha256": checker.PARENT_ROOT,
        })
        with self.assertRaises(checker.CheckError):
            checker.validate_current_pointer(
                hybrid, self.manifest, self.result["manifest_file_sha256"], "auto")

    def test_receipt_is_deterministic_sealed_scoped_and_transaction_gated(self) -> None:
        receipt = self.result["receipt"]
        checker.verify_seal(receipt, "test receipt")
        self.assertEqual(receipt, checker.acceptance_receipt(self.root, self.result))
        self.assertEqual(receipt["manifest_file_sha256"], self.result["manifest_file_sha256"])
        self.assertEqual(receipt["manifest_authority_sha256"], self.manifest["authority_sha256"])
        self.assertEqual(receipt["counts"], self.manifest["counts"])
        self.assertEqual(receipt["findings"], [])
        self.assertFalse(receipt["quality_boundary"]["origin_5_6"]
                         ["human_semantic_uniqueness_claimed"])
        self.assertEqual(receipt["checker_file_sha256"],
                         checker.file_sha(self.root / checker.CHECKER_REL))
        with self.assertRaises(checker.CheckError):
            checker.acceptance_receipt(self.root, {"transaction_authenticated": False})

    def test_duplicate_json_symlink_and_foreign_root_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            duplicate = root / "duplicate.json"
            duplicate.write_text('{"a":1,"a":2}\n', encoding="utf-8")
            with self.assertRaises(checker.CheckError):
                checker.load_json(root, Path("duplicate.json"), canonical_file=False)
            target = root / "target.json"
            target.write_text('{}\n', encoding="utf-8")
            (root / "alias.json").symlink_to(target)
            with self.assertRaises(checker.CheckError):
                checker.safe_path(root, Path("alias.json"))
            with self.assertRaises(checker.CheckError):
                checker.verify(root, boundary="auto")


if __name__ == "__main__":
    unittest.main()
