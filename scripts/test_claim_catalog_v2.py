#!/usr/bin/env python3
"""Coverage and mutation tests for the lossless Stage2 claim catalog."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "Docs" / "tools" / "generate_claim_catalog_v2.py"
SPEC = importlib.util.spec_from_file_location("generate_claim_catalog_v2", GENERATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot import the Catalog v2 generator")
generator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = generator
SPEC.loader.exec_module(generator)


def load(name: str) -> dict:
    return json.loads((ROOT / "Docs" / "catalog" / name).read_text(encoding="utf-8"))


class ClaimCatalogV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = load("Source_Records_v2.json")
        cls.registry = load("Claim_ID_Registry_v2.json")
        cls.relations = load("Claim_Relations_v2.json")
        cls.catalog = load("Claim_Catalog_v2.json")
        cls.schema = load("Claim_Record_Schema_v2.json")
        cls.candidates = generator.parse_all_sources()
        cls.snapshot = generator.source_snapshot()

    def record_errors(self, record: dict) -> list[jsonschema.ValidationError]:
        definition = {
            "ATO": "ato_record",
            "ATF": "atf_record",
            "ATS": "ats_record",
            "ATV": "atv_record",
        }[record["record_type"]]
        validator = jsonschema.Draft202012Validator(
            {
                "$schema": self.schema["$schema"],
                "$defs": self.schema["$defs"],
                "$ref": f"#/$defs/{definition}",
            },
            format_checker=jsonschema.FormatChecker(),
        )
        return list(validator.iter_errors(record))

    def test_deterministic_generator_check_is_read_only_and_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(GENERATOR_PATH), "--check"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("PASS catalog deterministic check", result.stdout)

    def test_lossless_counts_and_unique_typed_ids(self) -> None:
        self.assertEqual(self.source["counts"]["current_occurrences"], 3338)
        self.assertEqual(self.registry["counts"]["legacy_aliases"], 3262)
        self.assertEqual(self.registry["counts"]["families_current"], 3119)
        self.assertEqual(self.registry["counts"]["senses_current"], 3338)
        self.assertEqual(self.registry["counts"]["variants_current"], 3338)
        self.assertEqual(self.catalog["counts"]["schema_records"], 13133)

        ids = [record["record_id"] for record in self.catalog["records"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(
            {record["record_type"] for record in self.catalog["records"]},
            {"ATO", "ATF", "ATS", "ATV"},
        )
        self.assertTrue(all(generator.ID_PATTERN.fullmatch(identifier) for identifier in ids))

    def test_exact_duplicates_are_relations_and_hamming_keeps_both_sources(self) -> None:
        counts = self.relations["counts"]
        self.assertEqual(counts["legacy_exact_clusters"], 74)
        self.assertEqual(counts["legacy_exact_extra_occurrences"], 76)
        self.assertEqual(counts["legacy_exact_cross_discipline_clusters"], 1)
        self.assertTrue(all(
            cluster["review_state"] == "unreviewed"
            and cluster["identity_assertion"] is False
            for cluster in self.relations["legacy_exact_match_clusters"]
        ))

        hamming = self.relations["hamming_dual_provenance_audit"]
        self.assertTrue(hamming["passed"])
        self.assertEqual(hamming["disciplines"], ["数学", "计算机科学"])
        self.assertEqual(len(hamming["occurrence_ids"]), 2)
        self.assertEqual(len(set(hamming["occurrence_ids"])), 2)
        self.assertEqual(len(hamming["variant_ids"]), 2)
        self.assertFalse(hamming["semantic_merge_performed"])

    def test_legacy_aliases_are_unique_single_target_snapshot_pointers(self) -> None:
        aliases = self.registry["legacy_aliases"]
        variant_ids = {row["variant_id"] for row in self.registry["variants"]}
        self.assertEqual(len(aliases), 3262)
        self.assertEqual(len({row["alias_id"] for row in aliases}), 3262)
        self.assertTrue(all(row["resolution_cardinality"] == 1 for row in aliases))
        self.assertTrue(all(row["target_variant_id"] in variant_ids for row in aliases))
        self.assertTrue(all(row["semantic_equivalence_reviewed"] is False for row in aliases))

    def test_invalid_legacy_alias_target_is_rejected(self) -> None:
        aliases = copy.deepcopy(self.registry["legacy_aliases"])
        aliases[0]["target_variant_id"] = "ATV-99999999"
        with self.assertRaises(generator.CatalogError):
            generator.build_id_registry(
                self.snapshot,
                self.source,
                self.registry["families"],
                self.registry["senses"],
                self.registry["variants"],
                aliases,
                self.registry,
            )

    def test_authority_tamper_and_idempotency_corruption_fail_closed(self) -> None:
        dropped = copy.deepcopy(self.source)
        dropped["records"].pop(0)
        with self.assertRaises(generator.CatalogError):
            generator.compatible_previous_source_records(dropped)

        corrupted = copy.deepcopy(self.registry)
        corrupted["families"][0]["idempotency_request_sha256"] = "0" * 64
        with self.assertRaises(generator.CatalogError):
            generator.compatible_previous_registry(corrupted)

        generator.seal_authority(
            "awesome-theorems/claim-id-registry-authority/v2", corrupted
        )
        with self.assertRaises(generator.CatalogError):
            generator.build_allocations(self.source, corrupted)

    def test_erased_tombstone_cannot_reuse_or_rebind_an_old_alias(self) -> None:
        erased = copy.deepcopy(self.source)
        erased["records"] = erased["records"][1:]
        erased["counts"]["allocated_occurrences"] -= 1
        erased["counts"]["current_occurrences"] -= 1
        erased["counts"]["current_by_discipline"]["数学"] -= 1
        generator.seal_authority("awesome-theorems/source-records-authority/v2", erased)

        rebuilt = generator.build_source_records(
            copy.deepcopy(self.candidates), self.snapshot, erased
        )
        first_key = self.source["records"][0]["occurrence_key_sha256"]
        replacement = next(
            row for row in rebuilt["records"] if row["occurrence_key_sha256"] == first_key
        )
        self.assertEqual(replacement["occurrence_id"], "ATO-00003339")
        self.assertNotEqual(replacement["occurrence_id"], "ATO-00000001")
        with self.assertRaises(generator.CatalogError):
            generator.build_allocations(rebuilt, self.registry)

    def test_unequal_title_anchor_cannot_force_an_existing_occurrence_key(self) -> None:
        candidates = copy.deepcopy(self.candidates)
        victim = candidates[0]
        victim.name = "Mutation-only unequal title anchor"
        victim.occurrence_anchor_sha256 = generator.stable_digest(
            "awesome-theorems/occurrence-title-anchor/v2",
            {
                "source_path": victim.source_file,
                "parser": victim.parser,
                "normalized_title": generator.normalize_title_key(victim.name),
            },
        )
        victim.occurrence_key_sha256 = self.source["records"][0]["occurrence_key_sha256"]
        with self.assertRaises(generator.CatalogError):
            generator.build_source_records(candidates, self.snapshot, self.source)

    def test_malformed_redirect_and_split_are_rejected(self) -> None:
        with self.assertRaises(generator.CatalogError):
            generator.validate_redirects([{}], {
                row["record_id"] for row in self.catalog["records"]
            })
        with self.assertRaises(generator.CatalogError):
            generator.validate_splits([{}], {
                row["record_id"] for row in self.catalog["records"]
            })

    def test_reorder_and_status_edit_preserve_all_occurrence_ids(self) -> None:
        expected = {
            row["occurrence_key_sha256"]: row["occurrence_id"]
            for row in self.source["records"]
            if row["lifecycle"] == "current"
        }
        reordered = generator.build_source_records(
            list(reversed(copy.deepcopy(self.candidates))),
            self.snapshot,
            self.source,
        )
        actual = {
            row["occurrence_key_sha256"]: row["occurrence_id"]
            for row in reordered["records"]
            if row["lifecycle"] == "current"
        }
        self.assertEqual(actual, expected)

        edited_candidates = copy.deepcopy(self.candidates)
        target = edited_candidates[len(edited_candidates) // 2]
        target.formal_status = "mutation-only status edit"
        edited = generator.build_source_records(edited_candidates, self.snapshot, self.source)
        edited_ids = {
            row["occurrence_key_sha256"]: row["occurrence_id"]
            for row in edited["records"]
            if row["lifecycle"] == "current"
        }
        self.assertEqual(edited_ids, expected)

    def test_duplicate_group_reverse_and_category_edit_preserve_identity(self) -> None:
        groups: dict[str, list[int]] = {}
        for index, candidate in enumerate(self.candidates):
            groups.setdefault(candidate.occurrence_anchor_sha256, []).append(index)
        indexes = next(
            values
            for values in groups.values()
            if len(values) >= 2
            and len({
                generator.canonical_json_bytes(self.candidates[index].raw_fields())
                for index in values
            }) == len(values)
        )
        left, right = indexes[:2]
        mutated = copy.deepcopy(self.candidates)
        mutated[left].occurrence_key_sha256, mutated[right].occurrence_key_sha256 = (
            mutated[right].occurrence_key_sha256,
            mutated[left].occurrence_key_sha256,
        )
        mutated[left].subcategory = "mutation-only category edit"

        rebuilt = generator.build_source_records(mutated, self.snapshot, self.source)
        original_by_key = {
            row["occurrence_key_sha256"]: row["occurrence_id"]
            for row in self.source["records"]
        }
        rebuilt_by_ordinal = {
            row["current_locator"]["global_source_ordinal"]: row["occurrence_id"]
            for row in rebuilt["records"]
            if row["lifecycle"] == "current"
        }
        for index in (left, right):
            self.assertEqual(
                rebuilt_by_ordinal[self.candidates[index].global_source_ordinal],
                original_by_key[self.candidates[index].occurrence_key_sha256],
            )

    def test_byte_identical_front_insertion_does_not_steal_old_occurrence_id(self) -> None:
        candidates = copy.deepcopy(self.candidates)
        anchor_counts: dict[str, int] = {}
        for candidate in candidates:
            anchor_counts[candidate.occurrence_anchor_sha256] = (
                anchor_counts.get(candidate.occurrence_anchor_sha256, 0) + 1
            )
        target_index = next(
            index
            for index, candidate in enumerate(candidates)
            if anchor_counts[candidate.occurrence_anchor_sha256] == 1
            and any(
                later.source_file == candidate.source_file
                and later.source_record_ordinal > candidate.source_record_ordinal
                and anchor_counts[later.occurrence_anchor_sha256] == 1
                for later in candidates
            )
        )
        target = candidates[target_index]
        old_record = next(
            row
            for row in self.source["records"]
            if row["occurrence_key_sha256"] == target.occurrence_key_sha256
        )
        old_source_ordinal = target.current_locator["source_record_ordinal"]
        old_global_ordinal = target.current_locator["global_source_ordinal"]
        old_line_start = target.current_locator["line_start"]
        old_byte_start = target.current_locator["byte_start"]
        line_delta = target.current_locator["line_end"] - old_line_start + 1
        byte_delta = len(target.raw_text.encode("utf-8"))

        inserted = copy.deepcopy(target)
        inserted.occurrence_id = ""
        for candidate in candidates:
            locator = candidate.current_locator
            if locator["global_source_ordinal"] >= old_global_ordinal:
                locator["global_source_ordinal"] += 1
                candidate.global_source_ordinal += 1
            if (
                candidate.source_file == target.source_file
                and locator["source_record_ordinal"] >= old_source_ordinal
            ):
                locator["source_record_ordinal"] += 1
                candidate.source_record_ordinal += 1
                if locator["line_start"] >= old_line_start:
                    locator["line_start"] += line_delta
                    locator["line_end"] += line_delta
                    candidate.line_start += line_delta
                    candidate.line_end += line_delta
                if locator["byte_start"] >= old_byte_start:
                    locator["byte_start"] += byte_delta
                    locator["byte_end_exclusive"] += byte_delta
                    candidate.byte_start += byte_delta
                    candidate.byte_end_exclusive += byte_delta

        disambiguator = {
            "statement": generator.normalize_text(target.statement),
            "proposer": generator.normalize_text(target.proposer),
            "proposed_time": generator.normalize_text(target.proposed_time),
            "source_domain": generator.normalize_text(target.source_domain),
        }
        disambiguator_sha256 = generator.stable_digest(
            "awesome-theorems/occurrence-disambiguator/v3", disambiguator
        )
        category_anchor = generator.normalize_text(target.subcategory).casefold()
        for slot, candidate in enumerate((inserted, target), start=1):
            candidate.occurrence_key_sha256 = generator.stable_digest(
                "awesome-theorems/occurrence-key/v3",
                {
                    "title_anchor_sha256": target.occurrence_anchor_sha256,
                    "disambiguator_sha256": disambiguator_sha256,
                    "category_anchor": category_anchor,
                    "duplicate_slot": slot,
                },
            )
        mutated = [*candidates[:target_index], inserted, *candidates[target_index:]]
        rebuilt = generator.build_source_records(mutated, self.snapshot, self.source)
        current = [row for row in rebuilt["records"] if row["lifecycle"] == "current"]
        preserved = next(row for row in current if row["occurrence_id"] == old_record["occurrence_id"])
        allocated = next(row for row in current if row["occurrence_id"] == "ATO-00003339")
        self.assertEqual(
            preserved["current_locator"]["source_record_ordinal"], old_source_ordinal + 1
        )
        self.assertEqual(
            allocated["current_locator"]["source_record_ordinal"], old_source_ordinal
        )
        self.assertEqual(preserved["birth_locator"], old_record["birth_locator"])
        families, senses, variants, allocation = generator.build_allocations(
            rebuilt, self.registry
        )
        old_allocation = next(
            row
            for row in self.registry["senses"]
            if row["bootstrap_occurrence_id"] == old_record["occurrence_id"]
        )
        old_variant = next(
            row
            for row in self.registry["variants"]
            if row["bootstrap_occurrence_id"] == old_record["occurrence_id"]
        )
        self.assertEqual(
            allocation[old_record["occurrence_id"]]["sense_id"], old_allocation["sense_id"]
        )
        self.assertEqual(
            allocation[old_record["occurrence_id"]]["variant_id"], old_variant["variant_id"]
        )
        self.assertEqual(allocation["ATO-00003339"]["sense_id"], "ATS-00003339")
        self.assertEqual(allocation["ATO-00003339"]["variant_id"], "ATV-00003339")
        self.assertEqual(len(senses), 3339)
        self.assertEqual(len(variants), 3339)
        rebuilt_registry = generator.build_id_registry(
            self.snapshot,
            rebuilt,
            families,
            senses,
            variants,
            copy.deepcopy(self.registry["legacy_aliases"]),
            self.registry,
        )
        self.assertEqual(rebuilt_registry["namespace_high_watermarks"]["ATO"], 3339)
        self.assertEqual(rebuilt_registry["namespace_high_watermarks"]["ATS"], 3339)
        self.assertEqual(rebuilt_registry["namespace_high_watermarks"]["ATV"], 3339)

    def test_name_correction_preserves_occurrence_id_and_birth_locator(self) -> None:
        candidates = copy.deepcopy(self.candidates)
        anchor_counts: dict[str, int] = {}
        for candidate in candidates:
            anchor_counts[candidate.occurrence_anchor_sha256] = (
                anchor_counts.get(candidate.occurrence_anchor_sha256, 0) + 1
            )
        target = next(
            candidate
            for candidate in candidates
            if anchor_counts[candidate.occurrence_anchor_sha256] == 1
        )
        old_record = next(
            row
            for row in self.source["records"]
            if row["occurrence_key_sha256"] == target.occurrence_key_sha256
        )
        target.name = "Mutation-only corrected canonical source title"
        target.occurrence_anchor_sha256 = generator.stable_digest(
            "awesome-theorems/occurrence-title-anchor/v2",
            {
                "source_path": target.source_file,
                "parser": target.parser,
                "normalized_title": generator.normalize_title_key(target.name),
            },
        )
        target.occurrence_key_sha256 = generator.stable_digest(
            "awesome-theorems/occurrence-key/v3",
            {"title_anchor_sha256": target.occurrence_anchor_sha256},
        )
        rebuilt = generator.build_source_records(candidates, self.snapshot, self.source)
        preserved = next(
            row
            for row in rebuilt["records"]
            if row["occurrence_id"] == old_record["occurrence_id"]
            and row["lifecycle"] == "current"
        )
        self.assertEqual(preserved["raw_fields"]["name"], target.name)
        self.assertEqual(preserved["birth_locator"], old_record["birth_locator"])
        self.assertEqual(
            preserved["occurrence_key_sha256"], old_record["occurrence_key_sha256"]
        )
        families, senses, variants, allocation = generator.build_allocations(
            rebuilt, self.registry
        )
        old_sense = next(
            row
            for row in self.registry["senses"]
            if row["bootstrap_occurrence_id"] == old_record["occurrence_id"]
        )
        old_variant = next(
            row
            for row in self.registry["variants"]
            if row["bootstrap_occurrence_id"] == old_record["occurrence_id"]
        )
        self.assertEqual(
            allocation[old_record["occurrence_id"]]["sense_id"], old_sense["sense_id"]
        )
        self.assertEqual(
            allocation[old_record["occurrence_id"]]["variant_id"], old_variant["variant_id"]
        )
        self.assertEqual(len(families), 3120)
        old_family = next(
            row for row in families if row["family_id"] == old_sense["family_id"]
        )
        new_family = next(
            row
            for row in families
            if row["family_id"] == allocation[old_record["occurrence_id"]]["family_id"]
        )
        self.assertEqual(old_family["lifecycle"], "retired")
        self.assertEqual(old_family["member_occurrence_ids"], [])
        self.assertIn(
            old_record["occurrence_id"],
            old_family["historical_member_occurrence_ids"],
        )
        self.assertEqual(new_family["family_id"], "ATF-00003120")
        self.assertEqual(new_family["lifecycle"], "current")
        rebuilt_registry = generator.build_id_registry(
            self.snapshot,
            rebuilt,
            families,
            senses,
            variants,
            copy.deepcopy(self.registry["legacy_aliases"]),
            self.registry,
        )
        before_aliases = {
            row["alias_id"]: row["target_variant_id"]
            for row in self.registry["legacy_aliases"]
            if row["target_occurrence_id"] == old_record["occurrence_id"]
        }
        after_aliases = {
            row["alias_id"]: row["target_variant_id"]
            for row in rebuilt_registry["legacy_aliases"]
            if row["target_occurrence_id"] == old_record["occurrence_id"]
        }
        self.assertEqual(after_aliases, before_aliases)
        self.assertEqual(rebuilt_registry["namespace_high_watermarks"]["ATF"], 3120)

    def test_front_insertion_allocates_only_max_plus_one(self) -> None:
        inserted = copy.deepcopy(self.candidates[0])
        inserted.name = "Catalog v2 mutation-only front insertion"
        inserted.statement = "This synthetic fixture has a unique immutable occurrence key."
        inserted.raw_text = inserted.name + "\n" + inserted.statement + "\n"
        inserted.occurrence_anchor_sha256 = generator.stable_digest(
            "awesome-theorems/occurrence-title-anchor/v2",
            {
                "source_path": inserted.source_file,
                "parser": inserted.parser,
                "normalized_title": generator.normalize_title_key(inserted.name),
            },
        )
        inserted.occurrence_key_sha256 = generator.stable_digest(
            "awesome-theorems/test/front-insertion/v2",
            {"name": inserted.name, "statement": inserted.statement},
        )
        inserted.current_locator = copy.deepcopy(inserted.current_locator)
        inserted.current_locator["raw_block_sha256"] = generator.sha256_bytes(
            inserted.raw_text.encode("utf-8")
        )
        inserted.occurrence_id = ""

        records = generator.build_source_records(
            [inserted, *copy.deepcopy(self.candidates)],
            self.snapshot,
            self.source,
        )
        self.assertEqual(inserted.occurrence_id, "ATO-00003339")
        old_by_key = {
            row["occurrence_key_sha256"]: row["occurrence_id"]
            for row in self.source["records"]
        }
        new_by_key = {
            row["occurrence_key_sha256"]: row["occurrence_id"]
            for row in records["records"]
        }
        self.assertTrue(all(new_by_key[key] == value for key, value in old_by_key.items()))

        families, senses, variants, allocation = generator.build_allocations(
            records, self.registry
        )
        self.assertEqual(allocation[inserted.occurrence_id]["family_id"], "ATF-00003120")
        self.assertEqual(allocation[inserted.occurrence_id]["sense_id"], "ATS-00003339")
        self.assertEqual(allocation[inserted.occurrence_id]["variant_id"], "ATV-00003339")
        self.assertEqual(len(families), 3120)
        self.assertEqual(len(senses), 3339)
        self.assertEqual(len(variants), 3339)

    def test_bootstrap_drop_and_duplicate_id_are_rejected(self) -> None:
        with self.assertRaises(generator.CatalogError):
            generator.validate_bootstrap(
                self.candidates[:-1],
                self.source,
                self.registry,
                self.relations,
                False,
            )

        duplicated = copy.deepcopy(self.source)
        duplicated["records"][1]["occurrence_id"] = duplicated["records"][0]["occurrence_id"]
        with self.assertRaises(generator.CatalogError):
            generator.validate_bootstrap(
                self.candidates,
                duplicated,
                self.registry,
                self.relations,
                True,
            )

    def test_status_axes_cannot_be_collapsed(self) -> None:
        record = copy.deepcopy(next(
            row for row in self.catalog["records"] if row["record_type"] == "ATV"
        ))
        del record["statuses"]["external_formalization"]
        self.assertTrue(self.record_errors(record))

    def test_license_is_top_level_separate_and_unknown_blocks_benchmark(self) -> None:
        jsonschema.Draft202012Validator.check_schema(self.schema)
        representatives = {
            record_type: next(
                row for row in self.catalog["records"]
                if row["record_type"] == record_type
            )
            for record_type in ("ATO", "ATF", "ATS", "ATV")
        }
        for record in representatives.values():
            self.assertNotIn("rights", record["provenance"])
            self.assertEqual(record["license"]["status"], "unknown")
            self.assertIsNone(record["license"]["spdx_expression"])
            self.assertEqual(record["license"]["evidence_refs"], [])
            self.assertIn(
                "rights_unresolved",
                record["benchmark_eligibility"]["blocking_reasons"],
            )
            self.assertFalse(self.record_errors(record))

            missing_license = copy.deepcopy(record)
            del missing_license["license"]
            self.assertTrue(self.record_errors(missing_license))

            missing_blocker = copy.deepcopy(record)
            missing_blocker["benchmark_eligibility"]["blocking_reasons"].remove(
                "rights_unresolved"
            )
            self.assertTrue(self.record_errors(missing_blocker))

            unsupported_clearance = copy.deepcopy(record)
            unsupported_clearance["license"]["status"] = "cleared"
            self.assertTrue(self.record_errors(unsupported_clearance))

        eligible_with_unknown_license = copy.deepcopy(representatives["ATV"])
        eligible_with_unknown_license["benchmark_eligibility"]["status"] = (
            "eligible_for_task_derivation"
        )
        self.assertTrue(self.record_errors(eligible_with_unknown_license))

    def test_open_conjecture_requires_exact_scope_date_and_sources(self) -> None:
        record = copy.deepcopy(next(
            row for row in self.catalog["records"] if row["record_type"] == "ATV"
        ))
        record["claim_kind"].update(
            current_kind="conjecture", atomicity="atomic", truth_apt="truth_apt"
        )
        record["statuses"]["human_truth"].update(
            status="open", as_of=None, source_refs=[], scope_note=""
        )
        record["exact_statement"].update(
            completeness="source_prose", binders=[], hypotheses=[], conclusion=None, scope=None
        )
        self.assertTrue(self.record_errors(record))

    def test_raw_verified_label_never_grants_truth_formal_or_repo_credit(self) -> None:
        records = [
            row
            for row in self.catalog["records"]
            if row["record_type"] == "ATV"
            and any(
                field["field_name"] == "formal_status" and field["raw_value"] == "已验证"
                for field in row["source_status_raw"]
            )
        ]
        self.assertTrue(records)
        for record in records:
            self.assertEqual(record["statuses"]["human_truth"]["status"], "unknown")
            self.assertEqual(record["statuses"]["external_formalization"]["status"], "unknown")
            self.assertEqual(record["statuses"]["repo_integration"]["status"], "unknown")
            self.assertNotEqual(record["benchmark_eligibility"]["status"], "eligible")

    def test_m0133_m0387_statement_collision_fails_closed(self) -> None:
        clusters = self.relations["stage1_statement_identity_collision_candidates"]
        self.assertEqual(len(clusters), 1)
        collision = clusters[0]
        self.assertEqual(
            {member["legacy_alias_id"] for member in collision["members"]},
            {"THM-M-0133", "THM-M-0387"},
        )
        self.assertTrue(collision["canonical_statement_text_equal"])
        self.assertFalse(collision["all_declared_fingerprints_well_formed"])
        self.assertFalse(collision["identity_assertion"])
        self.assertFalse(collision["redirect_created"])
        self.assertTrue(collision["review_required"])


if __name__ == "__main__":
    unittest.main()
