"""Mutation-oriented regression tests for Stage5 mathematics release 5.4."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from Docs.catalog.v5.tools import check_math_catalog_v5_4 as checker
from Docs.catalog.v5.tools import generate_math_catalog_v5_4 as generator


class MathCatalogV54Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        checker.check_parent_release()
        cls.manifest, cls.documents = checker.check_release_package()
        cls.schema, cls.inputs = checker.check_authorities(cls.manifest)
        _rows, cls.source_by_id = checker.source_indexes()
        cls.parent_catalog = checker.load_json(checker.PARENT_DIR / "Claim_Catalog.json")
        cls.curation, cls.accepted = checker.check_curation(cls.parent_catalog, cls.source_by_id)
        first_ledger = cls.accepted[0]
        cls.first_claim = checker.expected_claim_row(
            first_ledger,
            cls.source_by_id[first_ledger["source_record_id"]],
            checker.load_json(checker.PARENT_DIR / "Claim_ID_Registry.json")["authority_sha256"],
            cls.curation,
        )

    def test_staged_release_passes_independent_checker(self) -> None:
        current_release = checker.load_json(checker.CURRENT_PATH).get("release")
        if current_release == "5.3":
            arguments = ["--prepublish"]
        elif current_release == "5.4":
            arguments = []
        else:
            self.fail(f"unexpected Current_Release state: {current_release!r}")
        self.assertEqual(checker.main(arguments), 0)

    def test_exact_round_robin_selection(self) -> None:
        selected, remaining = checker.replay_residual_selection(self.parent_catalog, self.source_by_id)
        self.assertEqual(len(selected), 500)
        self.assertEqual(len(remaining), 231)
        self.assertEqual(
            dict(sorted(__import__("collections").Counter(checker.module_root(source) for _row, source in selected).items())),
            checker.EXPECTED_ROOT_COUNTS,
        )

    def test_three_identity_gate_mutations_are_rejected(self) -> None:
        first = {
            "source_record_id": "TEST-A",
            "formal_type": "A   → B",
            "formal_type_sha256": "1" * 64,
            "declaration": "Mathlib.Test.first",
        }
        normalized_type_collision = {
            "source_record_id": "TEST-B",
            "formal_type": "A → B",
            "formal_type_sha256": "2" * 64,
            "declaration": "Mathlib.Test.second",
        }
        with self.assertRaises(checker.CheckError):
            checker.enforce_three_identity_gates([({}, first), ({}, normalized_type_collision)], [])

        normalized_name_collision = copy.deepcopy(normalized_type_collision)
        normalized_name_collision["formal_type"] = "C → D"
        normalized_name_collision["declaration"] = "Ｍａｔｈｌｉｂ．Ｔｅｓｔ．ＦＩＲＳＴ"
        with self.assertRaises(checker.CheckError):
            checker.enforce_three_identity_gates([({}, first), ({}, normalized_name_collision)], [])

        parent = [{"formal_statement": {
            "formal_type": first["formal_type"],
            "formal_type_sha256": first["formal_type_sha256"],
            "declaration": first["declaration"],
        }}]
        with self.assertRaises(checker.CheckError):
            checker.enforce_three_identity_gates([({}, first)], parent)

    def test_literal_lemma_never_grants_quota(self) -> None:
        mutation = copy.deepcopy(self.accepted[0])
        mutation["declaration_kind"] = "lemma"
        mutation["source_syntax_kind"] = "lemma"
        with self.assertRaises(checker.CheckError):
            checker.validate_literal_theorem_credits([mutation])

    def test_deep_schema_rejects_nested_extra_field(self) -> None:
        mutation = copy.deepcopy(self.first_claim)
        mutation["proof_evidence"]["unsealed_extra"] = True
        with self.assertRaises(checker.CheckError):
            checker.validate_schema_instance(mutation, self.schema, self.schema)

    def test_theorem_selection_mutation_invalidates_source_payload(self) -> None:
        mutation = copy.deepcopy(self.first_claim)
        mutation["theorem_selection"]["display_label"] += " mutated"
        with self.assertRaises(checker.CheckError):
            checker.validate_record_payload_hashes(mutation)

    def test_parent_prefix_mutation_is_detectable(self) -> None:
        parent = checker.load_json(checker.PARENT_DIR / "Claim_Catalog.json")["records"]
        child = copy.deepcopy(self.documents["Claim_Catalog.json"]["records"])
        checker.validate_parent_prefix(child, parent, "test catalog")
        child[0]["stage_claim_id"] = "S5-CLM-99999999"
        with self.assertRaises(checker.CheckError):
            checker.validate_parent_prefix(child, parent, "test catalog")

    def test_manifest_root_and_combined_row_counts(self) -> None:
        inventory = self.manifest["artifacts"]
        self.assertEqual(checker.release_root(inventory), self.manifest["release_root_sha256"])
        counts = {row["path"]: row["row_count"] for row in inventory}
        self.assertEqual(counts["Coverage_Ledger.json"], 5_961)
        self.assertEqual(counts["Strict_Conjecture_Ledger.json"], 1_001)
        mutation = copy.deepcopy(inventory)
        mutation[0]["size_bytes"] += 1
        self.assertNotEqual(checker.release_root(mutation), self.manifest["release_root_sha256"])

    def test_artifact_hash_size_and_root_mutations_fail_closed(self) -> None:
        cases = []
        bad_hash = copy.deepcopy(self.manifest)
        bad_hash["artifacts"][0]["sha256"] = "0" * 64
        cases.append(bad_hash)
        bad_size = copy.deepcopy(self.manifest)
        bad_size["artifacts"][0]["size_bytes"] += 1
        cases.append(bad_size)
        bad_root = copy.deepcopy(self.manifest)
        bad_root["release_root_sha256"] = "f" * 64
        cases.append(bad_root)
        for mutation in cases:
            with self.subTest(mutation=mutation["release_root_sha256"]):
                with self.assertRaises(checker.CheckError):
                    checker.validate_release_inventory(mutation, self.documents, checker.RELEASE_DIR)

    def test_source_registry_conflict_fails_closed(self) -> None:
        registry = checker.load_json(checker.SOURCE_REGISTRY_PATH)
        checker.validate_source_registry(registry)
        for field, value in (("sha256", "0" * 64), ("size_bytes", 1), ("record_count", 1_499)):
            mutation = copy.deepcopy(registry)
            mutation["sources"][0]["asset"][field] = value
            with self.subTest(field=field):
                with self.assertRaises(checker.CheckError):
                    checker.validate_source_registry(mutation)
        source_row_mutation = copy.deepcopy(registry)
        source_row_mutation["sources"][0]["title"] += " conflicting rewrite"
        with self.assertRaises(checker.CheckError):
            checker.validate_source_registry(source_row_mutation)

    def test_current_pointer_parent_and_target_mutations_fail_closed(self) -> None:
        parent = checker.authenticated_parent_pointer()
        checker.validate_current_pointer(parent, self.manifest, prepublish=True)
        target = checker.expected_target_pointer(self.manifest)
        checker.validate_current_pointer(target, self.manifest, prepublish=True)
        checker.validate_current_pointer(target, self.manifest, prepublish=False)
        with self.assertRaises(checker.CheckError):
            checker.validate_current_pointer(parent, self.manifest, prepublish=False)
        for field, value in (
            ("release", "5.2"),
            ("release_root_sha256", "0" * 64),
            ("manifest_sha256", "1" * 64),
            ("manifest_path", "releases/5.3/Release_Manifest.json"),
        ):
            mutation = copy.deepcopy(target)
            mutation[field] = value
            mutation["authority_sha256"] = checker.hash_without(mutation, "authority_sha256")
            with self.subTest(field=field):
                with self.assertRaises(checker.CheckError):
                    checker.validate_current_pointer(mutation, self.manifest, prepublish=False)
        stale_authority = copy.deepcopy(target)
        stale_authority["authority_sha256"] = "2" * 64
        with self.assertRaises(checker.CheckError):
            checker.validate_current_pointer(stale_authority, self.manifest, prepublish=False)

    def test_id_ranges_are_closed_and_contiguous(self) -> None:
        rows = self.documents["Claim_Catalog.json"]["records"][3_600:]
        self.assertEqual([row["variant_id"] for row in rows], [f"ATV-{n:08d}" for n in range(7_085, 7_585)])
        self.assertEqual([row["family_id"] for row in rows], [f"ATF-{n:08d}" for n in range(6_855, 7_355)])

    def test_coverage_supersession_mutation_is_rejected(self) -> None:
        mutation = copy.deepcopy(self.documents["Coverage_Ledger.json"])
        mutation["candidate_dispositions"][-1]["supersedes_candidate_key"] = "missing-parent"
        new_rows = [
            checker.expected_claim_row(
                row,
                self.source_by_id[row["source_record_id"]],
                checker.load_json(checker.PARENT_DIR / "Claim_ID_Registry.json")["authority_sha256"],
                self.curation,
            )
            for row in self.accepted
        ]
        with self.assertRaises(checker.CheckError):
            checker.check_coverage(mutation, self.curation, new_rows)

    def test_staged_directory_publish_is_atomic_and_immutable(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "releases" / "5.4"
            payloads = {"a.json": b"a\n", "b.json": b"b\n"}
            generator.publish_directory(target, payloads)
            self.assertEqual({path.name for path in target.iterdir()}, set(payloads))
            generator.publish_directory(target, payloads)
            (target / "a.json").write_bytes(b"tampered\n")
            with self.assertRaises(generator.GenerationError):
                generator.publish_directory(target, payloads)

    def test_parent_cas_promotes_staged_pointer_in_temp_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            v5_root = Path(temporary) / "v5"
            parent_dir = v5_root / "releases" / "5.3"
            release_dir = v5_root / "releases" / "5.4"
            readable_dir = v5_root / "readable" / "5.4"
            parent_dir.mkdir(parents=True)
            release_dir.mkdir(parents=True)
            readable_dir.mkdir(parents=True)
            for name in (generator.MANIFEST_NAME, "Claim_ID_Registry.json"):
                shutil.copy2(generator.PARENT_DIR / name, parent_dir / name)
            package = {"staged.json": b"staged\n"}
            (release_dir / "staged.json").write_bytes(package["staged.json"])
            (readable_dir / "readable.md").write_bytes(b"readable\n")
            current_path = v5_root / "Current_Release.json"
            current_path.write_bytes(generator.encoded_document(generator.authenticated_parent_pointer()))
            target = generator.seal({
                "schema_version": "awesome-theorems/stage5-current-release/5.4",
                "release": "5.4",
                "manifest_path": "releases/5.4/Release_Manifest.json",
                "manifest_sha256": "3" * 64,
                "release_root_sha256": "4" * 64,
            })
            with mock.patch.multiple(
                generator,
                V5_ROOT=v5_root,
                PARENT_DIR=parent_dir,
                RELEASE_DIR=release_dir,
                READABLE_DIR=readable_dir,
                CURRENT_PATH=current_path,
                LOCK_PATH=v5_root / ".Current_Release.lock",
            ), mock.patch.object(generator, "validate_readable_projection", return_value=None):
                generator.publish_current(package, target, "4" * 64)
                self.assertEqual(generator.load_json(current_path), target)
                self.assertEqual(generator.verify_current_cas(package, "4" * 64, target), "already_current")

    def test_exclusive_lock_blocks_second_process_in_temp_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            v5_root = Path(temporary)
            lock_path = v5_root / ".Current_Release.lock"
            with mock.patch.multiple(generator, V5_ROOT=v5_root, LOCK_PATH=lock_path):
                with generator.exclusive_writer_lock():
                    script = (
                        "import fcntl,os,sys; "
                        f"fd=os.open({str(lock_path)!r},os.O_RDWR|os.O_CREAT,0o644); "
                        "\ntry:\n fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)\nexcept BlockingIOError:\n sys.exit(0)\nsys.exit(1)"
                    )
                    result = subprocess.run([sys.executable, "-c", script], check=False)
                    self.assertEqual(result.returncode, 0)

    def test_readable_tamper_is_rejected_by_detailed_renderer(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            readable = Path(temporary) / "5.4"
            shutil.copytree(checker.READABLE_DIR, readable)
            path = readable / "Theorem_List.md"
            text_value = path.read_text(encoding="utf-8")
            text_value = text_value.replace(
                "## S5-CLM-00003485", "## S5-CLM-99999999", 1
            )
            path.write_text(text_value, encoding="utf-8")
            with self.assertRaises(checker.CheckError):
                checker.validate_readable_structure(readable, self.documents)
        checker.check_readable(self.documents)


if __name__ == "__main__":
    unittest.main()
