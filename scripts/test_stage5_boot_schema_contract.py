#!/usr/bin/env python3
"""Mutation tests for the exact Stage5 BOOT schema contracts."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import stage5_boot_schema_contract as contract


try:
    from jsonschema.validators import Draft202012Validator
except ImportError:  # pragma: no cover - the contract itself is stdlib-only
    Draft202012Validator = None


KINDS_AND_FILES = tuple(
    (kind, filename)
    for kind in sorted(contract.BOOT_PROGRAM_KINDS)
    for filename in contract.BOOT_SCHEMA_FILENAMES
)


class Stage5BootSchemaContractTests(unittest.TestCase):
    def assert_rejected(self, document: object, kind: str, filename: str) -> None:
        with self.assertRaises(contract.BootSchemaContractError):
            contract.validate_boot_schema_document(
                document, program_kind=kind, schema_filename=filename
            )

    def test_all_six_exact_contracts_validate_and_match_frozen_digest(self) -> None:
        observed: set[str] = set()
        for kind, filename in KINDS_AND_FILES:
            with self.subTest(kind=kind, filename=filename):
                schema = contract.expected_boot_schema(kind, filename)
                digest = contract.validate_boot_schema_document(
                    schema, program_kind=kind, schema_filename=filename
                )
                self.assertEqual(
                    digest, contract.expected_boot_schema_sha256(kind, filename)
                )
                self.assertEqual(
                    digest,
                    hashlib.sha256(
                        contract.canonical_json_bytes(schema)
                    ).hexdigest(),
                )
                self.assertRegex(digest, r"^[0-9a-f]{64}$")
                observed.add(digest)
        self.assertEqual(len(observed), 6)

    def test_schema_documents_are_recursively_typed_and_closed(self) -> None:
        def walk(schema: object, path: str) -> None:
            self.assertIsInstance(schema, dict, path)
            self.assertTrue(schema, path)
            if "oneOf" in schema:
                self.assertEqual(set(schema), {"oneOf"}, path)
                self.assertGreaterEqual(len(schema["oneOf"]), 2, path)
                for index, branch in enumerate(schema["oneOf"]):
                    walk(branch, f"{path}.oneOf[{index}]")
                return
            self.assertIn("type", schema, path)
            schema_type = schema["type"]
            if isinstance(schema_type, list):
                self.assertEqual(schema_type, ["string", "null"], path)
                return
            self.assertIn(schema_type, {"object", "array", "string", "integer", "number", "boolean"}, path)
            if schema_type == "object":
                self.assertIs(schema.get("additionalProperties"), False, path)
                properties = schema.get("properties")
                required = schema.get("required")
                self.assertIsInstance(properties, dict, path)
                self.assertTrue(properties, path)
                self.assertEqual(required, list(properties), path)
                for name, child in properties.items():
                    walk(child, f"{path}.{name}")
            elif schema_type == "array":
                self.assertIn("items", schema, path)
                walk(schema["items"], f"{path}[]")

        root_keys = {
            "$schema", "$id", "type", "additionalProperties", "required", "properties"
        }
        for kind, filename in KINDS_AND_FILES:
            with self.subTest(kind=kind, filename=filename):
                schema = contract.expected_boot_schema(kind, filename)
                self.assertEqual(set(schema), root_keys)
                walk(schema, "$")

    @unittest.skipIf(Draft202012Validator is None, "jsonschema is not installed")
    def test_all_contracts_are_valid_draft_2020_12_schemas(self) -> None:
        for kind, filename in KINDS_AND_FILES:
            with self.subTest(kind=kind, filename=filename):
                Draft202012Validator.check_schema(
                    contract.expected_boot_schema(kind, filename)
                )

    def test_expected_schema_returns_an_independent_copy(self) -> None:
        first = contract.expected_boot_schema("theorem", "claim-card.schema.json")
        first["properties"]["program"]["type"] = "integer"
        second = contract.expected_boot_schema("theorem", "claim-card.schema.json")
        self.assertEqual(second["properties"]["program"]["type"], "string")

    def test_theorem_claim_identity_is_closed_without_changing_conjecture_v1(self) -> None:
        theorem = contract.expected_boot_schema("theorem", "claim-card.schema.json")
        conjecture = contract.expected_boot_schema("conjecture", "claim-card.schema.json")
        self.assertEqual(
            theorem["properties"]["schema_version"]["const"],
            "awesome-theorems/stage5-proof-debt-claim-card/1.1",
        )
        self.assertIn("execution_identity", theorem["required"])
        identity = theorem["properties"]["execution_identity"]
        self.assertFalse(identity["additionalProperties"])
        self.assertEqual(
            identity["properties"]["requested_concurrency"]["properties"]
            ["service_records"]["type"],
            "string",
        )
        self.assertEqual(
            conjecture["properties"]["schema_version"]["const"],
            "awesome-theorems/stage5-proof-debt-claim-card/1.1",
        )
        self.assertIn("execution_identity", conjecture["properties"])
        self.assertIn("work_contract", conjecture["required"])
        work_contract = conjecture["properties"]["work_contract"]
        self.assertEqual(len(work_contract["oneOf"]), 2)
        proof_branch = work_contract["oneOf"][0]
        prompt = proof_branch["properties"]["strict_resolution_proof_search"]
        self.assertFalse(prompt["additionalProperties"])
        self.assertEqual(
            prompt["properties"]["source"]["properties"]["repository"]["const"],
            "jinshanmu/CrouzeixConjecture",
        )
        intake_branch = work_contract["oneOf"][1]
        self.assertEqual(
            intake_branch["properties"]["kind"]["const"],
            "source_occurrence_intake",
        )
        self.assertNotIn("strict_resolution_proof_search", intake_branch["properties"])

    def test_conjecture_worker_result_has_exact_typed_outcome_branches(self) -> None:
        schema = contract.expected_boot_schema(
            "conjecture", "worker-result.schema.json"
        )
        self.assertIn("typed_outcome", schema["required"])
        branches = schema["properties"]["typed_outcome"]["oneOf"]
        self.assertEqual(
            [branch["properties"]["kind"]["const"] for branch in branches],
            ["strict_resolution", "source_occurrence_intake"],
        )
        strict = branches[0]
        self.assertEqual(
            set(strict["properties"]),
            {
                "kind", "polarity", "human_resolution_sha256",
                "lean_root_sha256", "machine_cut_set_empty",
                "readability_cut_set_empty",
            },
        )
        intake = branches[1]
        self.assertEqual(
            set(intake["properties"]),
            {
                "kind", "status_review_sha256", "rights_review_sha256",
                "importance_review_sha256", "identity_relation",
                "identity_crosswalk_sha256", "strict_credit_granted",
                "stage5_claim_id_allocated", "stage6_alias_allocated",
            },
        )
        for field in (
            "strict_credit_granted", "stage5_claim_id_allocated",
            "stage6_alias_allocated",
        ):
            self.assertIs(intake["properties"][field]["const"], False)

        theorem = contract.expected_boot_schema(
            "theorem", "worker-result.schema.json"
        )
        self.assertNotIn("typed_outcome", theorem["properties"])

    def test_object_key_order_does_not_change_the_contract(self) -> None:
        for kind, filename in KINDS_AND_FILES:
            with self.subTest(kind=kind, filename=filename):
                schema = contract.expected_boot_schema(kind, filename)
                reordered = {
                    key: schema[key] for key in reversed(tuple(schema))
                }
                self.assertEqual(
                    contract.validate_boot_schema_document(
                        reordered,
                        program_kind=kind,
                        schema_filename=filename,
                    ),
                    contract.expected_boot_schema_sha256(kind, filename),
                )

    def test_vacuous_root_closed_schema_is_rejected_for_every_contract(self) -> None:
        # This has the exact shallow shape previously accepted by the manager.
        for kind, filename in KINDS_AND_FILES:
            with self.subTest(kind=kind, filename=filename):
                expected = contract.expected_boot_schema(kind, filename)
                vacuous = {
                    "$schema": contract.JSON_SCHEMA_DRAFT,
                    "$id": expected["$id"],
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["x"],
                    "properties": {"x": {}},
                }
                self.assert_rejected(vacuous, kind, filename)

    def test_nested_extra_property_is_rejected_even_when_nested_required_matches(self) -> None:
        mutation_paths = {
            "claim-card.schema.json": ("baseline",),
            "worker-result.schema.json": ("patch",),
            "master-acceptance.schema.json": ("master",),
        }
        for kind, filename in KINDS_AND_FILES:
            with self.subTest(kind=kind, filename=filename):
                mutated = contract.expected_boot_schema(kind, filename)
                nested = mutated["properties"][mutation_paths[filename][0]]
                nested["properties"]["unreviewed_extra"] = {"type": "string"}
                nested["required"].append("unreviewed_extra")
                self.assert_rejected(mutated, kind, filename)

    def test_nested_object_cannot_be_opened(self) -> None:
        nested_fields = {
            "claim-card.schema.json": "artifact_policy",
            "worker-result.schema.json": "patch",
            "master-acceptance.schema.json": "integration",
        }
        for kind, filename in KINDS_AND_FILES:
            with self.subTest(kind=kind, filename=filename):
                mutated = contract.expected_boot_schema(kind, filename)
                mutated["properties"][nested_fields[filename]][
                    "additionalProperties"
                ] = True
                self.assert_rejected(mutated, kind, filename)

    def test_missing_nested_property_type_is_rejected(self) -> None:
        def target(schema: dict, filename: str) -> dict:
            if filename == "claim-card.schema.json":
                return schema["properties"]["baseline"]["properties"][
                    "blueprint_sha256"
                ]
            if filename == "worker-result.schema.json":
                return schema["properties"]["patch"]["properties"]["sha256"]
            return schema["properties"]["integration"]["properties"][
                "integrated_files"
            ]["items"]["properties"]["sha256"]

        for kind, filename in KINDS_AND_FILES:
            with self.subTest(kind=kind, filename=filename):
                mutated = contract.expected_boot_schema(kind, filename)
                target(mutated, filename).pop("type")
                self.assert_rejected(mutated, kind, filename)

    def test_required_field_deletion_and_reordering_are_rejected(self) -> None:
        for kind, filename in KINDS_AND_FILES:
            with self.subTest(kind=kind, filename=filename):
                missing = contract.expected_boot_schema(kind, filename)
                missing["required"].pop()
                self.assert_rejected(missing, kind, filename)

                reordered = contract.expected_boot_schema(kind, filename)
                reordered["required"] = list(reversed(reordered["required"]))
                self.assert_rejected(reordered, kind, filename)

    def test_false_cannot_be_substituted_by_numeric_zero(self) -> None:
        for kind, filename in KINDS_AND_FILES:
            with self.subTest(kind=kind, filename=filename):
                mutated = contract.expected_boot_schema(kind, filename)
                mutated["additionalProperties"] = 0
                # Python considers False == 0; canonical JSON must not.
                self.assertEqual(False, 0)
                self.assert_rejected(mutated, kind, filename)

    def test_schema_ids_and_program_kinds_cannot_cross_bind(self) -> None:
        for filename in contract.BOOT_SCHEMA_FILENAMES:
            with self.subTest(filename=filename):
                theorem = contract.expected_boot_schema("theorem", filename)
                self.assert_rejected(theorem, "conjecture", filename)
        with self.assertRaises(contract.BootSchemaContractError):
            contract.expected_boot_schema("other", "claim-card.schema.json")
        with self.assertRaises(contract.BootSchemaContractError):
            contract.expected_boot_schema("theorem", "other.schema.json")

    def test_exact_three_file_set_is_required(self) -> None:
        valid = {
            filename: contract.expected_boot_schema("theorem", filename)
            for filename in contract.BOOT_SCHEMA_FILENAMES
        }
        digests = contract.validate_boot_schema_set(valid, program_kind="theorem")
        self.assertEqual(set(digests), set(contract.BOOT_SCHEMA_FILENAMES))

        missing = dict(valid)
        missing.pop("worker-result.schema.json")
        with self.assertRaises(contract.BootSchemaContractError):
            contract.validate_boot_schema_set(missing, program_kind="theorem")

        extra = dict(valid)
        extra["unreviewed.schema.json"] = {}
        with self.assertRaises(contract.BootSchemaContractError):
            contract.validate_boot_schema_set(extra, program_kind="theorem")

    def test_strict_byte_parser_rejects_duplicate_keys_and_nonfinite_numbers(self) -> None:
        schema = contract.expected_boot_schema("theorem", "claim-card.schema.json")
        raw = contract.canonical_json_bytes(schema)
        self.assertEqual(
            contract.validate_boot_schema_bytes(
                raw,
                program_kind="theorem",
                schema_filename="claim-card.schema.json",
            ),
            contract.expected_boot_schema_sha256(
                "theorem", "claim-card.schema.json"
            ),
        )

        duplicate = b'{"x":1,"x":1}'
        with self.assertRaisesRegex(
            contract.BootSchemaContractError, "duplicate JSON key"
        ):
            contract.validate_boot_schema_bytes(
                duplicate,
                program_kind="theorem",
                schema_filename="claim-card.schema.json",
            )

        nonfinite = b'{"x":NaN}'
        with self.assertRaisesRegex(
            contract.BootSchemaContractError, "non-finite JSON number"
        ):
            contract.validate_boot_schema_bytes(
                nonfinite,
                program_kind="theorem",
                schema_filename="claim-card.schema.json",
            )

    def test_readable_json_encoding_of_exact_schema_also_validates(self) -> None:
        schema = contract.expected_boot_schema(
            "conjecture", "master-acceptance.schema.json"
        )
        pretty = json.dumps(schema, ensure_ascii=False, indent=2) + "\n"
        contract.validate_boot_schema_bytes(
            pretty,
            program_kind="conjecture",
            schema_filename="master-acceptance.schema.json",
        )

    def test_conjecture_master_acceptance_binds_member_and_typed_outcome(self) -> None:
        schema = contract.expected_boot_schema(
            "conjecture", "master-acceptance.schema.json"
        )
        properties = schema["properties"]
        self.assertIn("workset_member", properties)
        self.assertIn("accepted_outcome", properties)
        branches = properties["accepted_outcome"]["oneOf"]
        self.assertEqual(
            [branch["properties"]["kind"]["const"] for branch in branches],
            ["strict_resolution", "source_occurrence_intake"],
        )
        intake = branches[1]["properties"]
        for field in (
            "strict_credit_granted", "stage5_claim_id_allocated",
            "stage6_alias_allocated",
        ):
            self.assertIs(intake[field]["const"], False)


if __name__ == "__main__":
    unittest.main()
