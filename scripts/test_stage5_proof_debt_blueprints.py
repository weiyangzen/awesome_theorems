#!/usr/bin/env python3
"""Mutation tests for the one-time Stage5 proof-debt Blueprint scaffold.

These tests deliberately exercise the bootstrap manager, not the future
receipt-bound execution controller installed by ``S5THM/S5CON-BOOT-001``.
Large sealed catalog inputs are read as bytes for mutation tests; the Markdown,
DAG, Gantt, and transaction tests use tiny repository-local fixtures so a test
run never rewrites either authoritative Stage5 Blueprint.
"""

from __future__ import annotations

from contextlib import contextmanager, redirect_stderr, redirect_stdout
from dataclasses import replace
import copy
import importlib.util
import io
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest import mock

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


ROOT = Path(__file__).resolve().parents[1]
MANAGER_PATH = ROOT / "Docs" / "tools" / "manage_stage5_proof_debt_blueprints.py"


def _load_manager():
    spec = importlib.util.spec_from_file_location(
        "manage_stage5_proof_debt_blueprints_for_tests", MANAGER_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {MANAGER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


manager = _load_manager()

LONG_GATE = (
    "Independent fixture validation binds exact immutable bytes, dependencies, "
    "ownership, and acceptance evidence; a file-presence claim is insufficient."
)


class Stage5ProofDebtBootstrapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.theorem_source_raw = manager.THEOREM_SOURCE.read_bytes()
        cls.strict_document = json.loads(manager.STRICT_SOURCE.read_text(encoding="utf-8"))
        cls.open_document = json.loads(manager.OPEN_SOURCE.read_text(encoding="utf-8"))
        cls.stage5_current_raw = manager.STAGE5_CURRENT.read_bytes()
        cls.stage5_manifest_raw = manager.STAGE5_MANIFEST.read_bytes()
        cls.stage5_current_document = json.loads(cls.stage5_current_raw)
        cls.stage5_manifest_document = json.loads(cls.stage5_manifest_raw)
        cls.stage6_current_raw = manager.STAGE6_CURRENT.read_bytes()
        cls.stage6_registry_raw = manager.STAGE6_REGISTRY.read_bytes()

    def setUp(self) -> None:
        manager.validate_stage5_release_chain.cache_clear()
        manager.validate_m0387_negative_fixture.cache_clear()
        manager.stage6_aliases.cache_clear()
        self.addCleanup(manager.validate_stage5_release_chain.cache_clear)
        self.addCleanup(manager.validate_m0387_negative_fixture.cache_clear)
        self.addCleanup(manager.stage6_aliases.cache_clear)
        # Keeping the temporary tree below ROOT preserves the manager's strict
        # repository-relative path checks without changing its module globals.
        self.temp = tempfile.TemporaryDirectory(
            prefix=".stage5-scaffold-test-", dir=ROOT / "Docs"
        )
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        docs = self.root
        relative_runtime = (self.root / "runtime").relative_to(ROOT).as_posix()
        self.program = manager.Program(
            kind="theorem",
            blueprint=docs / "Fixture_Theorems_Blueprint.md",
            gantt=docs / "Fixture_Theorems_Gantt.md",
            version="fixture-theorem/1.0",
            schema="fixture/theorem-blueprint/1.0",
            task_prefix="S5THM",
            target_count=1,
            phase_count=1,
            runtime_root=relative_runtime,
            cron_marker_begin="# BEGIN FIXTURE_THEOREM",
            cron_marker_end="# END FIXTURE_THEOREM",
        )
        self.tasks = self._tasks(self.program, "fixture/theorem")
        manager.validate_task_set(self.program, self.tasks, expected_initial=True)
        self.blueprint_raw = manager.render_blueprint(self.program, self.tasks)
        self.gantt_raw = manager.render_gantt(
            self.program, self.blueprint_raw, self.tasks, "2026-08-10T00:00:00Z"
        )

    @staticmethod
    def _tasks(program, owned_root: str) -> list:
        prefix = program.task_prefix
        return [
            manager.Task(
                f"{prefix}-BOOT-001",
                "fixture canonical-Master bootstrap",
                (),
                (f"{owned_root}/bootstrap.json",),
                LONG_GATE,
            ),
            manager.Task(
                f"{prefix}-00000001-TARGET",
                "fixture exact target work",
                (f"{prefix}-BOOT-001",),
                (f"{owned_root}/work.json",),
                LONG_GATE,
            ),
            manager.Task(
                f"{prefix}-PROGRAM-RELEASE",
                "fixture terminal release",
                (f"{prefix}-00000001-TARGET",),
                (f"{owned_root}/release.json",),
                LONG_GATE,
            ),
        ]

    def _write_baseline(self, program=None, tasks=None) -> tuple[bytes, bytes]:
        program = self.program if program is None else program
        tasks = self.tasks if tasks is None else tasks
        raw = manager.render_blueprint(program, tasks)
        gantt = manager.render_gantt(
            program, raw, tasks, "2026-08-10T00:00:00Z"
        )
        program.blueprint.parent.mkdir(parents=True, exist_ok=True)
        program.blueprint.write_bytes(raw)
        program.gantt.write_bytes(gantt)
        return raw, gantt

    def _single_new_transaction(self, before: set[Path]) -> Path:
        after = set(manager.DOCS.glob(f"{manager.BOOTSTRAP_TRANSACTION_PREFIX}*"))
        created = after - before
        self.assertEqual(len(created), 1, sorted(map(str, created)))
        transaction = created.pop()
        self.addCleanup(
            lambda: manager.cleanup_transaction(transaction) if transaction.exists() else None
        )
        return transaction

    def _assert_blueprint_rejected(self, raw: bytes) -> None:
        with self.assertRaises(manager.BlueprintError):
            manager.parse_blueprint(self.program, raw, self.tasks)

    @staticmethod
    def _json_bytes(value: object) -> bytes:
        return json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")

    @staticmethod
    def _signed_document(unsigned: dict, key: Ed25519PrivateKey) -> dict:
        payload = manager.canonical(unsigned)
        result = dict(unsigned)
        result["signed_payload_sha256"] = manager.sha256_bytes(payload)
        result["signature"] = key.sign(payload).hex()
        result["authority_sha256"] = manager.sha256_bytes(
            manager.canonical(result)
        )
        return result

    @staticmethod
    def _boot_attestation(
        program, *, role: str, principal: str, key_id: str,
        claim_id: str, run_id: str, key: Ed25519PrivateKey,
    ) -> dict:
        unsigned = {
            "schema_version": manager.BOOT_ROLE_SCHEMA,
            "program": program.version,
            "role": role,
            "principal_id": principal,
            "key_id": key_id,
            "principal_context": "external",
            "claim_id": claim_id,
            "run_id": run_id,
            "item_id": f"{program.task_prefix}-BOOT-001",
            "manager_sha256": manager.manager_code_sha256(),
            "source_bundle_sha256": manager.source_bundle_sha256(program),
            "execution_spec_sha256": manager.sha256_bytes(
                manager.canonical(manager.spec_object(program))
            ),
            "observed_at": "2026-08-11T00:00:00Z",
            "signature_algorithm": "Ed25519",
        }
        return Stage5ProofDebtBootstrapTests._signed_document(unsigned, key)

    def _stage5_chain_with_documents(self, current: dict, manifest: dict) -> None:
        def bound(path, _expected_sha):
            if path == manager.STAGE5_CURRENT:
                return current
            if path == manager.STAGE5_MANIFEST:
                return manifest
            raise AssertionError(f"unexpected bound path: {path}")

        manager.validate_stage5_release_chain.cache_clear()
        try:
            with (
                mock.patch.object(manager, "validate_canonical_root"),
                mock.patch.object(manager, "read_bound_json", side_effect=bound),
            ):
                manager.validate_stage5_release_chain()
        finally:
            manager.validate_stage5_release_chain.cache_clear()

    def test_stage5_current_and_manifest_raw_sha_mutations_are_rejected(self) -> None:
        cases = (
            ("current", "STAGE5_CURRENT", self.stage5_current_raw),
            ("manifest", "STAGE5_MANIFEST", self.stage5_manifest_raw),
        )
        for label, attribute, raw in cases:
            with self.subTest(label=label):
                path = self.root / f"{label}.json"
                path.write_bytes(raw + b"\n")
                manager.validate_stage5_release_chain.cache_clear()
                with (
                    mock.patch.object(manager, attribute, path),
                    mock.patch.object(manager, "validate_canonical_root"),
                ):
                    with self.assertRaisesRegex(manager.BlueprintError, "SHA drift"):
                        manager.validate_stage5_release_chain()
        manager.validate_stage5_release_chain.cache_clear()

    def test_stage5_current_member_and_manifest_artifact_binding_mutations_are_rejected(self) -> None:
        current = copy.deepcopy(self.stage5_current_document)
        current["release"] = "5.5"
        with self.assertRaisesRegex(manager.BlueprintError, "authority chain drift"):
            self._stage5_chain_with_documents(current, self.stage5_manifest_document)

        manifest_member = copy.deepcopy(self.stage5_manifest_document)
        manifest_member["release"] = "5.5"
        with self.assertRaisesRegex(manager.BlueprintError, "authority chain drift"):
            self._stage5_chain_with_documents(
                self.stage5_current_document, manifest_member
            )

        for field, value in (
            ("sha256", "0" * 64),
            ("row_count", 3499),
            ("path", "Renamed_Theorem_List.json"),
        ):
            with self.subTest(field=field):
                manifest = copy.deepcopy(self.stage5_manifest_document)
                binding = next(
                    row for row in manifest["artifacts"] if row["path"] == "Theorem_List.json"
                )
                binding[field] = value
                with self.assertRaisesRegex(manager.BlueprintError, "manifest binding drift"):
                    self._stage5_chain_with_documents(self.stage5_current_document, manifest)

    def test_manifest_strict_row_count_uses_ledger_semantics_not_effective_credit_count(self) -> None:
        strict = self.strict_document
        semantic_rows = len(strict["strict_credits"]) + len(strict["credit_corrections"])
        self.assertEqual(semantic_rows, 1426)
        binding = next(
            row
            for row in self.stage5_manifest_document["artifacts"]
            if row["path"] == "Strict_Conjecture_Ledger.json"
        )
        self.assertEqual(binding["row_count"], semantic_rows)
        self._stage5_chain_with_documents(
            self.stage5_current_document, self.stage5_manifest_document
        )

        manifest = copy.deepcopy(self.stage5_manifest_document)
        binding = next(
            row
            for row in manifest["artifacts"]
            if row["path"] == "Strict_Conjecture_Ledger.json"
        )
        binding["row_count"] = len(strict["strict_credits"])
        with self.assertRaisesRegex(manager.BlueprintError, "manifest binding drift"):
            self._stage5_chain_with_documents(self.stage5_current_document, manifest)

    def test_source_bundle_digest_is_canonical_program_specific_and_gantt_bound(self) -> None:
        theorem_bundle = manager.source_bundle_object(manager.THEOREM)
        conjecture_bundle = manager.source_bundle_object(manager.CONJECTURE)
        self.assertEqual(
            manager.source_bundle_sha256(manager.THEOREM),
            manager.sha256_bytes(manager.canonical(theorem_bundle)),
        )
        self.assertNotEqual(theorem_bundle, conjecture_bundle)
        self.assertEqual(
            conjecture_bundle["crouzeix_prompt_commit"],
            "f9d5c8d39bece41ceedf6346ef50ad1fb393260e",
        )
        self.assertEqual(
            conjecture_bundle["crouzeix_prompt_sha256"],
            "0a0c3000b81efc4d9edc65ec3cd1d53df0d4e69b24bfee9fe0860301d853d6fc",
        )
        self.assertNotEqual(
            manager.source_bundle_sha256(manager.THEOREM),
            manager.source_bundle_sha256(manager.CONJECTURE),
        )
        expected_keys = {
            "stage5_current_sha256",
            "stage5_manifest_sha256",
            "stage5_release_root_sha256",
            "stage6_current_sha256",
            "stage6_manifest_sha256",
            "stage6_release_root_sha256",
            "stage6_registry_sha256",
            "stage6_migration_sha256",
        }
        self.assertTrue(expected_keys <= theorem_bundle.keys())

        gantt = self.gantt_raw.decode("utf-8")
        metadata_text = gantt.split(manager.GANTT_META_BEGIN, 1)[1].split(
            manager.GANTT_META_END, 1
        )[0].strip()
        metadata = json.loads(metadata_text[8:-4])
        self.assertEqual(
            metadata.get("source_bundle_sha256"),
            manager.source_bundle_sha256(self.program),
        )

    def test_embedded_marker_values_do_not_break_generated_roundtrip(self) -> None:
        parsed = manager.parse_blueprint(self.program, self.blueprint_raw, self.tasks)
        self.assertEqual(parsed, self.tasks)

        text = self.blueprint_raw.decode("utf-8")
        duplicate_line = text.replace(
            "\n" + manager.CHECKLIST_BEGIN + "\n",
            "\n" + manager.CHECKLIST_BEGIN + "\n" + manager.CHECKLIST_BEGIN + "\n",
            1,
        )
        self.assertNotEqual(duplicate_line, text)
        self._assert_blueprint_rejected(duplicate_line.encode("utf-8"))

    def test_operator_budget_boundary_is_initially_fail_closed(self) -> None:
        spec = manager.spec_object(self.program)
        budget = spec.get("operator_budget", spec.get("operator_budget_policy"))
        self.assertIsInstance(budget, dict)
        assert isinstance(budget, dict)
        encoded = json.dumps(budget, sort_keys=True).lower()
        self.assertIn("null", encoded, "initial operator authority/budget must be absent")
        self.assertIn("launch", encoded)
        self.assertIn("spend", encoded)
        self.assertRegex(encoded, r"fail[ _-]closed")
        self.assertIn("positive", encoded)

    def _single_conjecture_tasks(self) -> list:
        joined = next(
            {"credit": credit, "record": record}
            for credit in self.strict_document["strict_credits"]
            for record in self.open_document["records"]
            if credit["stage_claim_id"] == record["stage_claim_id"]
        )
        tasks, _ = manager.conjecture_target_tasks([joined])
        return tasks

    def test_conjecture_is_one_target_with_internal_resolution_subchecklist(self) -> None:
        tasks = self._single_conjecture_tasks()
        self.assertEqual(len(tasks), 1)
        target = tasks[0]
        self.assertTrue(target.item_id.endswith("-TARGET"))
        self.assertEqual(target.dependencies, ("S5CON-BOOT-001",))
        self.assertIn("task-local tmux server/socket/session", target.gate)
        self.assertIn("exactly one submitted /goal", target.gate)
        self.assertIn("or claim another mathematical ID", target.gate)
        self.assertIn("durable registry of genuinely distinct mathematical approach families", target.gate)
        self.assertIn("theorem-equivalent missing-lemma routes blocked", target.gate)
        self.assertIn("adversarially audit every candidate", target.gate)
        self.assertEqual(manager.CONJECTURE.phase_count, 1)
        self.assertIn("RESOLUTION", manager.phase_section(manager.CONJECTURE))
        prompt = manager.conjecture_proof_search_prompt_contract()
        self.assertEqual(prompt["resolution_roots"], ["Claim", "Not Claim"])
        self.assertEqual(prompt["execution_adaptation"]["child_agents"], "forbidden")
        self.assertTrue(prompt["approach_registry"]["required"])

    def test_status_transition_is_owned_only_by_release(self) -> None:
        tasks = self._single_conjecture_tasks()
        owners = [
            task
            for task in tasks
            if any(path.endswith("/status-transition.json") for path in task.owned_paths)
        ]
        self.assertEqual(len(owners), 1)
        target = owners[0]
        self.assertTrue(target.item_id.endswith("-TARGET"))
        self.assertIn("canonical Master", target.gate)

    def test_item_modes_cover_all_known_phases_and_unknown_phase_is_rejected(self) -> None:
        spec = manager.spec_object(manager.CONJECTURE)
        modes = spec["item_modes"]
        target_modes = [mode for mode in modes if mode["mode_id"] == "TARGET"]
        self.assertEqual(len(target_modes), 1)
        self.assertEqual(target_modes[0]["phase"], "TARGET")

        known = self._single_conjecture_tasks()
        fixture_program = replace(
            manager.CONJECTURE,
            version="fixture-conjecture/1.0",
            target_count=1,
        )
        boot = manager.global_tasks(fixture_program)
        manager.validate_task_set(
            fixture_program, boot + known + [
                manager.Task(
                    "S5CON-PROGRAM-RELEASE", "terminal", tuple(t.item_id for t in known),
                    ("fixture/conjecture/program-release.json",), LONG_GATE,
                )
            ]
        )
        unknown = manager.Task(
            "S5CON-00003486-UNKNOWN", "unknown fixture phase",
            (known[-1].item_id,), ("fixture/conjecture/unknown.json",), LONG_GATE,
        )
        with self.assertRaisesRegex(manager.BlueprintError, "(?i)(unknown|phase|item mode)"):
            manager.validate_task_set(
                fixture_program,
                boot + known + [unknown, manager.Task(
                    "S5CON-PROGRAM-RELEASE", "terminal", (unknown.item_id,),
                    ("fixture/conjecture/program-release.json",), LONG_GATE,
                )],
            )

    def test_sealed_v5_source_and_member_byte_mutations_are_rejected(self) -> None:
        cases = {
            "source_suffix": self.theorem_source_raw + b"\n",
            "member_identity": self.theorem_source_raw.replace(
                b"S5-CLM-", b"S5-XLM-", 1
            ),
        }
        self.assertNotEqual(cases["member_identity"], self.theorem_source_raw)
        for label, raw in cases.items():
            with self.subTest(label=label):
                path = self.root / f"Theorem_List-{label}.json"
                path.write_bytes(raw)
                with mock.patch.object(manager, "THEOREM_SOURCE", path):
                    with self.assertRaisesRegex(manager.BlueprintError, "SHA drift"):
                        manager.theorem_inventory()

    def test_v5_theorem_member_invariants_reject_resealed_projection_drift(self) -> None:
        document = json.loads(self.theorem_source_raw)
        ids = list(document["stage_claim_ids"])
        ids[0] = ids[1]
        document["stage_claim_ids"] = ids
        with (
            mock.patch.object(manager, "validate_stage5_release_chain"),
            mock.patch.object(manager, "read_bound_json", return_value=document),
        ):
            with self.assertRaisesRegex(
                manager.BlueprintError, "sealed theorem inventory invariants"
            ):
                manager.theorem_inventory()

    def test_sealed_v6_source_and_registry_member_mutations_are_rejected(self) -> None:
        current = self.root / "Current_Release.json"
        current.write_bytes(self.stage6_current_raw + b"\n")
        manager.stage6_aliases.cache_clear()
        with mock.patch.object(manager, "STAGE6_CURRENT", current):
            with self.assertRaisesRegex(manager.BlueprintError, "SHA drift"):
                manager.stage6_aliases()

        registry_raw = self.stage6_registry_raw.replace(
            b'"parent_s5_claim_id":"S5-CLM-',
            b'"parent_s5_claim_id":"S5-XLM-',
            1,
        )
        self.assertIsNot(registry_raw, self.stage6_registry_raw)
        self.assertEqual(len(registry_raw), len(self.stage6_registry_raw))
        registry = self.root / "Stage6_ID_Registry.json"
        registry.write_bytes(registry_raw)
        manager.stage6_aliases.cache_clear()
        try:
            with mock.patch.object(manager, "STAGE6_REGISTRY", registry):
                with self.assertRaisesRegex(manager.BlueprintError, "SHA drift"):
                    manager.stage6_aliases()
        finally:
            manager.stage6_aliases.cache_clear()

    def test_v6_current_and_registry_member_invariants_reject_resealed_drift(self) -> None:
        current = json.loads(self.stage6_current_raw)
        current["release"] = "7.0"

        def current_drift(path, _expected_sha):
            return current if path == manager.STAGE6_CURRENT else {}

        manager.stage6_aliases.cache_clear()
        with (
            mock.patch.object(manager, "validate_stage5_release_chain"),
            mock.patch.object(manager, "read_bound_json", side_effect=current_drift),
        ):
            with self.assertRaisesRegex(manager.BlueprintError, "authority chain drift"):
                manager.stage6_aliases()

        registry = json.loads(self.stage6_registry_raw)
        registry["claims"][0]["lifecycle"] = "historical"
        documents = {
            manager.STAGE6_CURRENT: json.loads(self.stage6_current_raw),
            manager.STAGE6_MANIFEST: json.loads(manager.STAGE6_MANIFEST.read_bytes()),
            manager.STAGE6_REGISTRY: registry,
            manager.STAGE6_MIGRATION: json.loads(manager.STAGE6_MIGRATION.read_bytes()),
        }
        manager.stage6_aliases.cache_clear()
        try:
            with (
                mock.patch.object(manager, "validate_stage5_release_chain"),
                mock.patch.object(
                    manager,
                    "read_bound_json",
                    side_effect=lambda path, _expected_sha: documents[path],
                ),
            ):
                with self.assertRaisesRegex(
                    manager.BlueprintError, "not one-to-one current"
                ):
                    manager.stage6_aliases()
        finally:
            manager.stage6_aliases.cache_clear()

    def _strict_leak_fixture(self, leaked_id: str) -> tuple[dict, dict, dict]:
        by_id = {
            row["stage_claim_id"]: row for row in self.open_document["records"]
        }
        leaked_record = by_id[leaked_id]
        strict = dict(self.strict_document)
        credits = list(strict["strict_credits"])
        replacement = dict(credits[0])
        replacement["stage_claim_id"] = leaked_id
        replacement["variant_id"] = leaked_record["variant_id"]
        replacement["origin_release"] = leaked_record["origin_release"]
        replacement["semantic_key"] = leaked_record.get(
            "semantic_key",
            "formal-conjectures-semantic/"
            + str(leaked_record["semantic_payload_sha256"]),
        )
        replacement_body = dict(replacement)
        replacement_body.pop("row_sha256", None)
        replacement["row_sha256"] = manager.sha256_bytes(
            manager.canonical(replacement_body)
        )
        credits[0] = replacement
        strict["strict_credits"] = credits
        aliases = {
            credit["stage_claim_id"]: {
                "stage6_claim_id": "S6-CLM-00000001",
                "stage6_variant_id": "S6-VAR-00000001",
                "parent_variant_id": by_id[credit["stage_claim_id"]]["variant_id"],
                "current_resolution_kind": "current",
                "terminal_stage6_claim_ids": ["S6-CLM-00000001"],
            }
            for credit in credits
        }
        return strict, self.open_document, aliases

    def test_revoked_credit_cannot_leak_into_strict_workset(self) -> None:
        strict, open_doc, aliases = self._strict_leak_fixture("S5-CLM-00005311")
        mutated_digest = manager.set_digest(
            row["stage_claim_id"] for row in strict["strict_credits"]
        )

        def bound(path, _expected_sha):
            return strict if path == manager.STRICT_SOURCE else open_doc

        with (
            mock.patch.object(manager, "validate_stage5_release_chain"),
            mock.patch.object(manager, "read_bound_json", side_effect=bound),
            mock.patch.object(manager, "stage6_aliases", return_value=aliases),
            mock.patch.object(manager, "STRICT_ID_SET_SHA256", mutated_digest),
        ):
            with self.assertRaisesRegex(manager.BlueprintError, "revoked strict credit"):
                manager.strict_inventory()

    def test_open_problem_cannot_leak_into_strict_workset(self) -> None:
        leaked = next(
            row["stage_claim_id"]
            for row in self.open_document["records"]
            if row.get("current_claim_kind") == "open_problem"
        )
        strict, open_doc, aliases = self._strict_leak_fixture(leaked)
        mutated_digest = manager.set_digest(
            row["stage_claim_id"] for row in strict["strict_credits"]
        )

        def bound(path, _expected_sha):
            return strict if path == manager.STRICT_SOURCE else open_doc

        with (
            mock.patch.object(manager, "validate_stage5_release_chain"),
            mock.patch.object(manager, "read_bound_json", side_effect=bound),
            mock.patch.object(manager, "stage6_aliases", return_value=aliases),
            mock.patch.object(manager, "STRICT_ID_SET_SHA256", mutated_digest),
        ):
            with self.assertRaisesRegex(manager.BlueprintError, "unexpected status"):
                manager.strict_inventory()

    def test_prose_header_and_post_checklist_suffix_mutations_are_rejected(self) -> None:
        text = self.blueprint_raw.decode("utf-8")
        mutations = {
            "prose": text.replace(
                "It is an execution authority", "It is only a speculative plan", 1
            ),
            "header": text.replace(
                "> Blueprint version: `fixture-theorem/1.0`",
                "> Blueprint version: `fixture-theorem/9.9`",
                1,
            ),
            "suffix": text + "unsealed trailing authority\n",
        }
        for label, mutation in mutations.items():
            with self.subTest(label=label):
                self._assert_blueprint_rejected(mutation.encode("utf-8"))

    def test_marker_order_and_duplicate_id_mutations_are_rejected(self) -> None:
        text = self.blueprint_raw.decode("utf-8")
        begin_duplicate = text.replace(
            manager.CHECKLIST_BEGIN,
            manager.CHECKLIST_BEGIN + "\n" + manager.CHECKLIST_BEGIN,
            1,
        )
        self._assert_blueprint_rejected(begin_duplicate.encode("utf-8"))

        lines = text.splitlines()
        row_indices = [index for index, line in enumerate(lines) if line.startswith("- [")]
        lines[row_indices[0]], lines[row_indices[1]] = lines[row_indices[1]], lines[row_indices[0]]
        self._assert_blueprint_rejected(("\n".join(lines) + "\n").encode("utf-8"))

        duplicate = list(self.tasks)
        duplicate[1] = replace(duplicate[1], item_id=duplicate[0].item_id)
        with self.assertRaisesRegex(manager.BlueprintError, "duplicate task IDs"):
            manager.validate_task_set(self.program, duplicate)

    def test_nonadjacent_owned_path_prefix_overlap_is_rejected(self) -> None:
        p = self.program.task_prefix
        tasks = [
            manager.Task(f"{p}-BOOT-001", "root owner", (), ("shared/tree",), LONG_GATE),
            manager.Task(
                f"{p}-MIDDLE", "unrelated middle owner", (f"{p}-BOOT-001",),
                ("separate/file.json",), LONG_GATE,
            ),
            manager.Task(
                f"{p}-CHILD", "nonadjacent child owner", (f"{p}-MIDDLE",),
                ("shared/tree/child.json",), LONG_GATE,
            ),
            manager.Task(
                f"{p}-PROGRAM-RELEASE", "terminal", (f"{p}-CHILD",),
                ("release/final.json",), LONG_GATE,
            ),
        ]
        with self.assertRaisesRegex(manager.BlueprintError, "prefix overlap"):
            manager.validate_task_set(self.program, tasks)

    def test_terminal_release_must_cover_every_task(self) -> None:
        p = self.program.task_prefix
        tasks = [
            manager.Task(f"{p}-BOOT-001", "bootstrap", (), ("a/boot.json",), LONG_GATE),
            manager.Task(f"{p}-ORPHAN", "orphan", (), ("a/orphan.json",), LONG_GATE),
            manager.Task(
                f"{p}-PROGRAM-RELEASE", "terminal", (f"{p}-BOOT-001",),
                ("a/release.json",), LONG_GATE,
            ),
        ]
        with self.assertRaisesRegex(manager.BlueprintError, "does not cover all tasks"):
            manager.validate_task_set(self.program, tasks)

    def test_runtime_snapshot_refuses_bootstrap_projection(self) -> None:
        self._write_baseline()
        runtime = ROOT / self.program.runtime_root / "status" / "runtime-snapshot.json"
        runtime.parent.mkdir(parents=True)
        runtime.write_text("{}\n", encoding="utf-8")
        with (
            mock.patch.object(manager, "expected_tasks", return_value=self.tasks),
            mock.patch.object(manager, "validate_bootstrap_cron_absence"),
        ):
            with self.assertRaisesRegex(
                manager.BlueprintError,
                "refuses all runtime input|refuses v2 runtime",
            ):
                manager.render_projections((self.program,))

    def test_force_refuses_progressed_cursor_without_writing(self) -> None:
        raw, _ = self._write_baseline()
        progressed = re.sub(
            rb"^- \[ \] (`[^`]+`)", rb"- [_] \1", raw, count=1, flags=re.MULTILINE
        )
        self.assertNotEqual(progressed, raw)
        self.program.blueprint.write_bytes(progressed)
        before = self.program.blueprint.read_bytes()
        with self.assertRaisesRegex(manager.BlueprintError, "(?i)(wholly blank|pristine)"):
            manager.validate_force_pair(self.program, self.tasks, force=True)
        self.assertEqual(self.program.blueprint.read_bytes(), before)

    def test_missing_stale_duplicate_and_incomplete_gantt_are_rejected(self) -> None:
        blueprint_raw, gantt_raw = self._write_baseline()
        # The canonical theorem evidence root may legitimately exist after BOOT
        # preparation.  This fixture validates only Blueprint/Gantt byte
        # consistency, so isolate it from the canonical one-time execution-history
        # boundary just as the other fixture-only projection tests do.
        with (
            mock.patch.object(manager, "expected_tasks", return_value=self.tasks),
            mock.patch.object(manager, "validate_no_execution_history"),
            mock.patch.object(manager, "validate_bootstrap_cron_absence"),
            mock.patch.object(manager, "validate_shared_execution_history_absence"),
        ):
            manager.check(self.program)
            baseline = self.program.gantt.read_bytes()
            index_lines = [
                line
                for line in baseline.decode("utf-8").splitlines()
                if line.startswith('| "S5THM-')
            ]
            self.assertEqual(len(index_lines), len(self.tasks))

            cases = {
                "stale": baseline.replace(b'"blueprint_sha256": "', b'"blueprint_sha256": "0', 1),
                "duplicate": baseline.replace(
                    index_lines[0].encode("utf-8"),
                    (index_lines[0] + "\n" + index_lines[0]).encode("utf-8"),
                    1,
                ),
                "incomplete": baseline.replace((index_lines[0] + "\n").encode("utf-8"), b"", 1),
            }
            for label, mutation in cases.items():
                with self.subTest(label=label):
                    self.program.gantt.write_bytes(mutation)
                    with self.assertRaises(manager.BlueprintError):
                        manager.check(self.program)

            self.program.gantt.unlink()
            with self.assertRaises(OSError):
                manager.check(self.program)

    def test_atomic_write_failure_preserves_old_bytes_and_removes_temp(self) -> None:
        target = self.root / "atomic.txt"
        target.write_bytes(b"old\n")
        with mock.patch.object(manager.os, "replace", side_effect=OSError("fixture replace failure")):
            with self.assertRaisesRegex(OSError, "fixture replace failure"):
                manager.atomic_write(target, b"new\n")
        self.assertEqual(target.read_bytes(), b"old\n")
        self.assertEqual(list(target.parent.glob(f".{target.name}.*.tmp")), [])

    def _second_program(self, *, common_owned_path: str | None = None):
        docs = self.root
        runtime = (self.root / "runtime-conjecture").relative_to(ROOT).as_posix()
        program = manager.Program(
            kind="conjecture",
            blueprint=docs / "Fixture_Conjectures_Blueprint.md",
            gantt=docs / "Fixture_Conjectures_Gantt.md",
            version="fixture-conjecture/1.0",
            schema="fixture/conjecture-blueprint/1.0",
            task_prefix="S5CON",
            target_count=1,
            phase_count=1,
            runtime_root=runtime,
            cron_marker_begin="# BEGIN FIXTURE_CONJECTURE",
            cron_marker_end="# END FIXTURE_CONJECTURE",
        )
        tasks = self._tasks(program, "fixture/conjecture")
        if common_owned_path is not None:
            tasks[1] = replace(tasks[1], owned_paths=(common_owned_path,))
        manager.validate_task_set(program, tasks, expected_initial=True)
        return program, tasks

    def _run_main(self, argv: list[str], programs, task_sets) -> tuple[int, str]:
        output = io.StringIO()

        def expected(program):
            return task_sets[program.kind]

        with (
            mock.patch.object(manager, "THEOREM", programs["theorem"]),
            mock.patch.object(manager, "CONJECTURE", programs["conjecture"]),
            mock.patch.object(manager, "expected_tasks", side_effect=expected),
            mock.patch.object(sys, "argv", [str(MANAGER_PATH), *argv]),
            redirect_stdout(output),
            redirect_stderr(output),
        ):
            result = manager.main()
        return result, output.getvalue()

    def test_kind_all_rejects_cross_program_owned_path_collision(self) -> None:
        common = "shared/canonical-integration.json"
        theorem_tasks = list(self.tasks)
        theorem_tasks[1] = replace(theorem_tasks[1], owned_paths=(common,))
        manager.validate_task_set(self.program, theorem_tasks, expected_initial=True)
        conjecture, conjecture_tasks = self._second_program(common_owned_path=common)
        with (
            mock.patch.object(manager, "THEOREM", self.program),
            mock.patch.object(manager, "CONJECTURE", conjecture),
        ):
            self._write_baseline(self.program, theorem_tasks)
            self._write_baseline(conjecture, conjecture_tasks)

        result, output = self._run_main(
            ["--check", "--kind", "all"],
            {"theorem": self.program, "conjecture": conjecture},
            {"theorem": theorem_tasks, "conjecture": conjecture_tasks},
        )
        self.assertEqual(result, 1, output)
        self.assertRegex(output, r"(?i)(cross-program|cross program|owned path|ownership)")

    def test_kind_all_bootstrap_rolls_back_every_output_on_replace_failure(self) -> None:
        conjecture, conjecture_tasks = self._second_program()
        paths = (
            self.program.blueprint,
            self.program.gantt,
            conjecture.blueprint,
            conjecture.gantt,
        )
        with (
            mock.patch.object(manager, "THEOREM", self.program),
            mock.patch.object(manager, "CONJECTURE", conjecture),
        ):
            self._write_baseline(self.program, self.tasks)
            self._write_baseline(conjecture, conjecture_tasks)
        before = {path: path.read_bytes() for path in paths}
        real_rename_noreplace = manager.rename_noreplace_at
        failed = False

        def fail_one_replace(source_directory_fd, source_name, destination_directory_fd, destination_name):
            nonlocal failed
            if destination_name == conjecture.blueprint.name and not failed:
                failed = True
                raise OSError("fixture third-output failure")
            return real_rename_noreplace(
                source_directory_fd,
                source_name,
                destination_directory_fd,
                destination_name,
            )

        output = io.StringIO()

        def expected(program):
            return {"theorem": self.tasks, "conjecture": conjecture_tasks}[program.kind]

        with (
            mock.patch.object(manager, "THEOREM", self.program),
            mock.patch.object(manager, "CONJECTURE", conjecture),
            mock.patch.object(manager, "expected_tasks", side_effect=expected),
            mock.patch.object(manager, "validate_bootstrap_cron_absence"),
            mock.patch.object(manager, "validate_no_execution_history"),
            mock.patch.object(manager, "rename_noreplace_at", side_effect=fail_one_replace),
            mock.patch.object(
                sys,
                "argv",
                [str(MANAGER_PATH), "--bootstrap", "--force", "--kind", "all"],
            ),
            redirect_stdout(output),
            redirect_stderr(output),
        ):
            result = manager.main()

        self.assertEqual(result, 1, output.getvalue())
        self.assertTrue(
            failed,
            "the injected cross-program replace failure was not reached: " + output.getvalue(),
        )
        self.assertEqual(
            {path: path.read_bytes() if path.exists() else None for path in paths},
            before,
            "--kind all must publish all four outputs or restore every prior byte",
        )

    def test_atomic_batch_present_racer_is_quarantined_not_overwritten(self) -> None:
        destination = self.root / "Present_Race.md"
        destination.write_bytes(b"old")
        expected = manager.regular_file_expectation(destination)
        assert expected is not None
        transactions_before = set(
            manager.DOCS.glob(f"{manager.BOOTSTRAP_TRANSACTION_PREFIX}*")
        )
        real_rename_noreplace = manager.rename_noreplace_at
        injected = False

        def replace_after_final_cas(
            source_directory_fd, source_name, destination_directory_fd, destination_name
        ):
            nonlocal injected
            if (
                source_name == destination.name
                and destination_name == "old-00.bin"
                and not injected
            ):
                injected = True
                destination.write_bytes(b"same-uid-racer")
            return real_rename_noreplace(
                source_directory_fd,
                source_name,
                destination_directory_fd,
                destination_name,
            )

        with (
            mock.patch.object(
                manager, "rename_noreplace_at", side_effect=replace_after_final_cas
            ),
            mock.patch.object(
                manager,
                "transaction_allowed_destinations",
                return_value={destination.relative_to(ROOT).as_posix()},
            ),
            self.assertRaisesRegex(manager.BlueprintError, "safe automatic rollback|captured"),
        ):
            manager.atomic_batch_write(
                [(destination, b"manager-new")],
                expected_old={destination: expected},
            )
        self.assertTrue(injected)
        self.assertFalse(destination.exists(), "unknown racer bytes must not be overwritten")
        transaction = self._single_new_transaction(transactions_before)
        self.assertEqual((transaction / "old-00.bin").read_bytes(), b"same-uid-racer")
        self.assertEqual((transaction / "new-00.bin").read_bytes(), b"manager-new")

    def test_atomic_batch_expected_absent_racer_is_never_overwritten(self) -> None:
        destination = self.root / "Absent_Race.json"
        self.assertFalse(destination.exists())
        transactions_before = set(
            manager.DOCS.glob(f"{manager.BOOTSTRAP_TRANSACTION_PREFIX}*")
        )
        real_rename_noreplace = manager.rename_noreplace_at
        injected = False

        def create_before_publish(
            source_directory_fd, source_name, destination_directory_fd, destination_name
        ):
            nonlocal injected
            if destination_name == destination.name and not injected:
                injected = True
                destination.write_bytes(b"same-uid-absent-racer")
            return real_rename_noreplace(
                source_directory_fd,
                source_name,
                destination_directory_fd,
                destination_name,
            )

        with (
            mock.patch.object(
                manager, "rename_noreplace_at", side_effect=create_before_publish
            ),
            mock.patch.object(
                manager,
                "transaction_allowed_destinations",
                return_value={destination.relative_to(ROOT).as_posix()},
            ),
            self.assertRaisesRegex(manager.BlueprintError, "safe automatic rollback|File exists"),
        ):
            manager.atomic_batch_write(
                [(destination, b"manager-new")],
                expected_old={destination: None},
            )
        self.assertTrue(injected)
        self.assertEqual(destination.read_bytes(), b"same-uid-absent-racer")
        transaction = self._single_new_transaction(transactions_before)
        self.assertEqual((transaction / "new-00.bin").read_bytes(), b"manager-new")
        self.assertFalse((transaction / "old-00.bin").exists())

    def test_atomic_batch_rollback_never_overwrites_concurrent_destination(self) -> None:
        first = self.root / "Rollback_First.md"
        second = self.root / "Rollback_Second.md"
        first.write_bytes(b"old-first")
        second.write_bytes(b"old-second")
        first_expected = manager.regular_file_expectation(first)
        second_expected = manager.regular_file_expectation(second)
        assert first_expected is not None and second_expected is not None
        transactions_before = set(
            manager.DOCS.glob(f"{manager.BOOTSTRAP_TRANSACTION_PREFIX}*")
        )
        real_rename_noreplace = manager.rename_noreplace_at
        injected = False

        def fail_after_first_publish(
            source_directory_fd, source_name, destination_directory_fd, destination_name
        ):
            nonlocal injected
            if source_name == "new-01.bin" and destination_name == second.name and not injected:
                injected = True
                first.write_bytes(b"same-uid-rollback-racer")
                raise OSError("fixture publish failure after concurrent replacement")
            return real_rename_noreplace(
                source_directory_fd,
                source_name,
                destination_directory_fd,
                destination_name,
            )

        with (
            mock.patch.object(
                manager, "rename_noreplace_at", side_effect=fail_after_first_publish
            ),
            mock.patch.object(
                manager,
                "transaction_allowed_destinations",
                return_value={
                    first.relative_to(ROOT).as_posix(),
                    second.relative_to(ROOT).as_posix(),
                },
            ),
            self.assertRaisesRegex(manager.BlueprintError, "unknown concurrent bytes"),
        ):
            manager.atomic_batch_write(
                [(first, b"new-first"), (second, b"new-second")],
                expected_old={first: first_expected, second: second_expected},
            )
        self.assertTrue(injected)
        self.assertEqual(first.read_bytes(), b"old-first")
        self.assertEqual(second.read_bytes(), b"old-second")
        transaction = self._single_new_transaction(transactions_before)
        self.assertFalse((transaction / "old-00.bin").exists())
        self.assertEqual(
            (transaction / "new-00.bin").read_bytes(), b"same-uid-rollback-racer"
        )
        self.assertEqual((transaction / "new-01.bin").read_bytes(), b"new-second")

    def test_conjecture_resolution_identity_and_event_contract(self) -> None:
        program, _ = self._second_program()
        spec = manager.spec_object(program)
        identity = spec["conjecture_resolution_identity_contract"]
        self.assertEqual(identity["claim_orientation"], "Claim")
        self.assertEqual(identity["baseline_material_status"], "open")
        self.assertEqual(identity["resolution_polarity_enum"], ["Claim", "Not Claim"])
        self.assertEqual(
            identity["resolution_dag"]["cut_sets"],
            ["mapping_cut_set", "candidate_human_cut_set", "candidate_machine_cut_set"],
        )
        self.assertIn("remaining_readability_cut_set=[]", identity["readability_receipt"])
        events = identity["status_event_chain"]
        self.assertEqual(events["event_kind_enum"], ["resolve", "invalidate", "supersede"])
        self.assertIn("RELEASE=x", events["effective_status"])
        self.assertIn("old resolution history grants no current credit", events["effective_status"])
        extensions = spec["append_only_extensions"]
        self.assertIn("existing TARGET claim and exact owned paths", json.dumps(extensions))
        supersession = extensions["resolution_supersession_contract"]
        self.assertIn("candidate_human_cut_set=[]", supersession["acceptance_precondition"])
        self.assertIn("candidate_machine_cut_set=[]", supersession["acceptance_precondition"])
        self.assertIn("content-addressed immutable_acceptance_archive", supersession["immutable_history"])
        self.assertIn("grants no checkbox or math credit", spec["nonacceptance_discovery_rule"])

    def test_m0387_axis_and_cold_cache_contracts_are_bound(self) -> None:
        bundle = manager.source_bundle_object(manager.THEOREM)
        self.assertEqual(
            bundle["m0387_negative_fixture_meta_sha256"], manager.M0387_META_SHA256
        )
        text = manager.controller_validation_section()
        self.assertIn("exact M0 machine root paired with self-labeled R0", text)
        self.assertIn("node-to-anchor collisions", text)
        self.assertIn("claim-specific axiom", text)
        theorem_tasks, _ = manager.theorem_target_tasks(
            [{"stage_claim_id": "S5-CLM-00003485", "proof_evidence": {
                "formal_proof_state": "kernel_checked_sorry_free", "uses_sorry": False
            }}]
        )
        target = theorem_tasks[0]
        self.assertTrue(target.item_id.endswith("-TARGET"))
        self.assertIn("injective node-to-fragment readable reconstruction", target.gate)
        self.assertIn("clean cold from-source offline replay", target.gate)
        self.assertIn("exactly one submitted /goal", target.gate)

    def test_theorem_strictly_dominates_m0387_without_semantic_shadowing(self) -> None:
        section = manager.m0387_section(manager.THEOREM)
        self.assertIn("strict-dominance certificate", section)
        self.assertIn("semantic-environment", section)
        self.assertIn("negative fixture", section)
        target = manager.theorem_target_tasks(
            [{"stage_claim_id": "S5-CLM-00003485", "proof_evidence": {
                "formal_proof_state": "kernel_checked_sorry_free", "uses_sorry": False
            }}]
        )[0][0]
        for clause in (
            "transitive non-foundation constant environment",
            "may not shadow or reinterpret source symbols",
            "semantic-substitution mutations",
            "strict-dominance certificate",
            "Distilled output removes duplication",
        ):
            self.assertIn(clause, target.gate)
        contract = manager.spec_object(manager.THEOREM)["theorem_acceptance_contract"]
        self.assertIn("THM-M-0387", contract["fixture_role"])
        self.assertIn("elaborated root expression", contract["semantic_identity"])
        self.assertIn("retaining every hypothesis", contract["distilled"])

    def test_boot_acceptor_contract_and_direct_blank_to_x_rejection(self) -> None:
        spec = manager.spec_object(manager.THEOREM)
        acceptor = spec["bootstrap_acceptor"]
        self.assertEqual(
            acceptor["actions"], ["--accept-boot-handoff", "--accept-boot-review"]
        )
        self.assertEqual(acceptor["authority_sha256"], manager.manager_code_sha256())
        with self.assertRaises(manager.BlueprintError):
            manager.tasks_with_boot_state(self.program, self.tasks, "x-invalid")
        underscored = manager.tasks_with_boot_state(self.program, self.tasks, "_")
        accepted = manager.tasks_with_boot_state(self.program, underscored, "x")
        self.assertEqual([task.state for task in accepted], ["x", " ", " "])

    def test_boot_signed_external_chain_reaches_underscore_then_x_without_commands_under_lock(self) -> None:
        canonical_program_patch = mock.patch.object(manager, "THEOREM", self.program)
        canonical_program_patch.start()
        self.addCleanup(canonical_program_patch.stop)
        blueprint_raw, gantt_raw = self._write_baseline()
        evidence = ROOT / "Docs" / f"stage5-boot-e2e-{self.root.name.removeprefix('.')}"
        evidence.mkdir()
        self.addCleanup(lambda: __import__("shutil").rmtree(evidence) if evidence.exists() else None)
        trust_path = evidence / manager.BOOT_ROLE_TRUST_ROOT_NAME
        trust_path.write_bytes(b"fixture-pinned-trust-root")
        trust_guard = manager.regular_file_expectation(trust_path)
        assert trust_guard is not None
        handoff_path = evidence / "controller-bootstrap-handoff.json"
        handoff_acceptance_path = evidence / "controller-bootstrap-handoff-acceptance.json"
        review_path = evidence / "controller-bootstrap-review.json"
        acceptance_path = evidence / "controller-bootstrap-acceptance.json"

        role_specs = (
            ("producer", "producer-a", "producer-key"),
            ("reviewer", "reviewer-a", "reviewer-a-key"),
            ("reviewer", "reviewer-b", "reviewer-b-key"),
            ("master", "master-a", "master-key"),
        )
        private_keys = {key_id: Ed25519PrivateKey.generate() for _, _, key_id in role_specs}
        trust = {
            key_id: {
                "key_id": key_id,
                "principal_id": principal,
                "allowed_role": role,
                "public_key_hex": private_keys[key_id].public_key().public_bytes_raw().hex(),
                "status": "active",
            }
            for role, principal, key_id in role_specs
        }
        artifact_bindings = {"fixture/theorem/bootstrap.json": "a" * 64}
        command_results = [{"command": "fixture-self-test", "exit_code": 0}]
        command_spec_sha = manager.sha256_bytes(
            manager.canonical(manager.boot_command_spec(self.program))
        )
        producer_attestation = self._boot_attestation(
            self.program,
            role="producer",
            principal="producer-a",
            key_id="producer-key",
            claim_id="boot-producer",
            run_id="run-producer",
            key=private_keys["producer-key"],
        )
        common = manager.validate_boot_common(
            self.program, self.tasks, blueprint_raw, self.tasks, artifact_bindings
        )
        handoff_unsigned = {
            "schema_version": manager.BOOT_HANDOFF_SCHEMA,
            "role": "producer",
            "principal_id": "producer-a",
            "key_id": "producer-key",
            "signature_algorithm": "Ed25519",
            "status": "self_tested",
            **common,
            "gantt_sha256": manager.sha256_bytes(gantt_raw),
            "command_spec_sha256": command_spec_sha,
            "expected_command_results_sha256": manager.sha256_bytes(
                manager.canonical(command_results)
            ),
            "producer_attestation": producer_attestation,
        }
        handoff = self._signed_document(handoff_unsigned, private_keys["producer-key"])
        handoff_path.write_bytes(self._json_bytes(handoff))

        lock_state = {"depth": 0}

        @contextmanager
        def short_lock():
            lock_state["depth"] += 1
            try:
                yield
            finally:
                lock_state["depth"] -= 1

        def run_commands(_program):
            self.assertEqual(lock_state["depth"], 0, "BOOT commands ran under manager flock")
            return copy.deepcopy(command_results)

        def atomic_write_fixture(outputs, *, expected_old=None, guards=None, precommit_validator=None):
            if precommit_validator is not None:
                precommit_validator()
            for path, expectation in (expected_old or {}).items():
                manager.validate_file_expectation(path, expectation)
            for path, expectation in (guards or {}).items():
                manager.validate_file_expectation(path, expectation)
            for path, content in outputs:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(content)

        patches = (
            mock.patch.object(manager, "THEOREM", self.program),
            mock.patch.object(manager, "expected_tasks", return_value=self.tasks),
            mock.patch.object(manager, "manager_mutation_lock", side_effect=short_lock),
            mock.patch.object(manager, "recover_batch_transactions"),
            mock.patch.object(manager, "validate_bootstrap_cron_absence"),
            mock.patch.object(manager, "validate_boot_runtime_absence"),
            mock.patch.object(manager, "validate_source_authorities_fresh"),
            mock.patch.object(
                manager, "boot_artifact_snapshot", return_value=(artifact_bindings, {})
            ),
            mock.patch.object(manager, "source_input_expectations", return_value={}),
            mock.patch.object(manager, "boot_trust_keys", return_value=(trust, trust_guard)),
            mock.patch.object(manager, "boot_trust_root_path", return_value=trust_path),
            mock.patch.object(
                manager,
                "boot_receipt_paths",
                return_value=(
                    handoff_path,
                    handoff_acceptance_path,
                    review_path,
                    acceptance_path,
                ),
            ),
            mock.patch.object(manager, "boot_evidence_root", return_value=evidence),
            mock.patch.object(manager, "run_boot_commands", side_effect=run_commands),
            mock.patch.object(manager, "executable_python_ast_audit"),
            mock.patch.object(manager, "atomic_batch_write", side_effect=atomic_write_fixture),
        )
        with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], \
             patches[6], patches[7], patches[8], patches[9], patches[10], patches[11], \
             patches[12], patches[13], patches[14]:
            manager.accept_boot(self.program, review=False)
            underscored_raw = self.program.blueprint.read_bytes()
            underscored = manager.parse_blueprint(
                self.program, underscored_raw, self.tasks, allow_boot_transition=True
            )
            self.assertEqual(underscored[0].state, "_")
            handoff_acceptance = json.loads(handoff_acceptance_path.read_text(encoding="utf-8"))
            self.assertEqual(handoff_acceptance["status"], "self_tested")
            self.assertEqual(
                handoff_acceptance["pre_blueprint_sha256"],
                manager.sha256_bytes(blueprint_raw),
            )
            self.assertEqual(
                handoff_acceptance["post_blueprint_sha256"],
                manager.sha256_bytes(underscored_raw),
            )

            reviewer_locators = []
            reviewer_attestations = []
            for index, principal in enumerate(("reviewer-a", "reviewer-b"), start=1):
                key_id = f"{principal}-key"
                attestation = self._boot_attestation(
                    self.program,
                    role="reviewer",
                    principal=principal,
                    key_id=key_id,
                    claim_id=f"boot-reviewer-{index}",
                    run_id=f"run-reviewer-{index}",
                    key=private_keys[key_id],
                )
                reviewer_attestations.append(attestation)
                decision_unsigned = {
                    "schema_version": manager.BOOT_DECISION_SCHEMA,
                    "role": "reviewer",
                    "principal_id": principal,
                    "key_id": key_id,
                    "signature_algorithm": "Ed25519",
                    "program": self.program.version,
                    "boot_item_id": self.tasks[0].item_id,
                    "handoff_acceptance_authority_sha256": handoff_acceptance["authority_sha256"],
                    "artifact_bindings": artifact_bindings,
                    "reviewer_attestation": attestation,
                    "decision": "pass",
                    "conflicts": [],
                    "passed_gates": list(manager.BOOT_REVIEW_GATES),
                    "command_spec_sha256": command_spec_sha,
                }
                decision = self._signed_document(decision_unsigned, private_keys[key_id])
                decision_bytes = self._json_bytes(decision)
                receipt_sha = manager.sha256_bytes(decision_bytes)
                decision_path = evidence / "bootstrap" / "reviews" / principal / f"{receipt_sha}.json"
                decision_path.parent.mkdir(parents=True, exist_ok=True)
                decision_path.write_bytes(decision_bytes)
                reviewer_locators.append({
                    "principal_id": principal,
                    "path": decision_path.relative_to(ROOT).as_posix(),
                    "sha256": receipt_sha,
                })
            master_attestation = self._boot_attestation(
                self.program,
                role="master",
                principal="master-a",
                key_id="master-key",
                claim_id="boot-master",
                run_id="run-master",
                key=private_keys["master-key"],
            )
            review_unsigned = {
                "schema_version": manager.BOOT_REVIEW_SCHEMA,
                "program": self.program.version,
                "boot_item_id": self.tasks[0].item_id,
                "handoff_acceptance_authority_sha256": handoff_acceptance["authority_sha256"],
                "producer_principal_id": "producer-a",
                "master_attestation": master_attestation,
                "reviewer_decisions": reviewer_locators,
                "passed_gates": list(manager.BOOT_REVIEW_GATES),
                "command_spec_sha256": command_spec_sha,
                "expected_command_results_sha256": manager.sha256_bytes(
                    manager.canonical(command_results)
                ),
                "artifact_bindings": artifact_bindings,
                "role": "master",
                "principal_id": "master-a",
                "key_id": "master-key",
                "signature_algorithm": "Ed25519",
            }
            review_doc = self._signed_document(review_unsigned, private_keys["master-key"])
            review_path.write_bytes(self._json_bytes(review_doc))
            manager.accept_boot(self.program, review=True)

        accepted = manager.parse_blueprint(
            self.program,
            self.program.blueprint.read_bytes(),
            self.tasks,
            allow_boot_transition=True,
        )
        self.assertEqual(accepted[0].state, "x")
        final_acceptance = json.loads(acceptance_path.read_text(encoding="utf-8"))
        self.assertEqual(
            final_acceptance["handoff_acceptance_authority_sha256"],
            handoff_acceptance["authority_sha256"],
        )

    def test_boot_canonical_tools_ignore_fake_path(self) -> None:
        fake = self.root / "fake-bin"
        fake.mkdir()
        for name in ("python3", "crontab", "tmux"):
            path = fake / name
            path.write_text("#!/bin/sh\nexit 99\n", encoding="utf-8")
            path.chmod(0o755)
        with mock.patch.dict(manager.os.environ, {"PATH": str(fake)}, clear=False):
            spec = manager.boot_command_spec(manager.THEOREM)
            self.assertTrue(spec)
            self.assertTrue(all(row["argv"][0] == "/usr/bin/python3.12" for row in spec))
            with mock.patch.object(manager.subprocess, "run") as run:
                run.return_value = mock.Mock(returncode=1, stdout="", stderr="no crontab for fixture")
                self.assertEqual(manager.read_user_crontab(), "")
                self.assertEqual(run.call_args.args[0][0], "/usr/bin/crontab")
                self.assertEqual(run.call_args.kwargs["env"]["PATH"], "/usr/bin:/bin")

    def test_boot_trust_root_absence_and_self_sealed_identity_fail_closed(self) -> None:
        missing = self.root / "missing" / manager.BOOT_ROLE_TRUST_ROOT_NAME
        with (
            mock.patch.object(manager, "boot_trust_root_path", return_value=missing),
            self.assertRaisesRegex(manager.BlueprintError, "trust root.*missing|missing regular file"),
        ):
            manager.boot_trust_keys(self.program)
        key = Ed25519PrivateKey.generate()
        unsigned = {
            field: "fixture" for field in manager.BOOT_ROLE_FIELDS
            if field not in {"signed_payload_sha256", "signature", "authority_sha256"}
        }
        unsigned.update(
            schema_version=manager.BOOT_ROLE_SCHEMA,
            role="producer", principal_id="untrusted-producer", key_id="unknown-key",
            signature_algorithm="Ed25519",
        )
        forged = self._signed_document(unsigned, key)
        with self.assertRaisesRegex(manager.BlueprintError, "unauthenticated"):
            manager.validate_signed_boot_document(
                forged, manager.BOOT_ROLE_FIELDS, manager.BOOT_ROLE_SCHEMA,
                "forged BOOT role", {}, "producer",
            )

    def test_boot_unpinned_trust_root_fails_closed(self) -> None:
        root = self.root / manager.BOOT_ROLE_TRUST_ROOT_NAME
        root.write_text("{}", encoding="utf-8")
        with (
            mock.patch.object(manager, "boot_trust_root_path", return_value=root),
            mock.patch.object(
                manager,
                "BOOT_ROLE_TRUST_ROOT_SHA256",
                {"theorem": None, "conjecture": "0" * 64},
            ),
            self.assertRaisesRegex(manager.BlueprintError, "not pinned"),
        ):
            manager.boot_trust_keys(self.program)

    def test_boot_signed_document_rejects_forgery_schema_and_role_alias(self) -> None:
        producer_key = Ed25519PrivateKey.generate()
        reviewer_key = Ed25519PrivateKey.generate()
        trust = {
            "producer-key": {
                "key_id": "producer-key", "principal_id": "producer-a",
                "allowed_role": "producer", "public_key_hex": producer_key.public_key().public_bytes_raw().hex(),
                "status": "active",
            },
            "review-key": {
                "key_id": "review-key", "principal_id": "reviewer-a",
                "allowed_role": "reviewer", "public_key_hex": reviewer_key.public_key().public_bytes_raw().hex(),
                "status": "active",
            },
        }
        base = {
            field: "fixture" for field in manager.BOOT_ROLE_FIELDS
            if field not in {"signed_payload_sha256", "signature", "authority_sha256"}
        }
        base.update(
            schema_version=manager.BOOT_ROLE_SCHEMA, role="producer",
            principal_id="producer-a", key_id="producer-key", signature_algorithm="Ed25519",
        )
        valid = self._signed_document(base, producer_key)
        self.assertEqual(
            manager.validate_signed_boot_document(
                valid, manager.BOOT_ROLE_FIELDS, manager.BOOT_ROLE_SCHEMA,
                "valid role", trust, "producer",
            ),
            "producer-a",
        )
        wrong_schema = dict(valid)
        wrong_schema["schema_version"] = "wrong"
        with self.assertRaisesRegex(manager.BlueprintError, "schema"):
            manager.validate_signed_boot_document(
                wrong_schema, manager.BOOT_ROLE_FIELDS, manager.BOOT_ROLE_SCHEMA,
                "wrong schema", trust, "producer",
            )
        alias = self._signed_document({**base, "principal_id": "alias"}, producer_key)
        with self.assertRaisesRegex(manager.BlueprintError, "unauthenticated"):
            manager.validate_signed_boot_document(
                alias, manager.BOOT_ROLE_FIELDS, manager.BOOT_ROLE_SCHEMA,
                "identity alias", trust, "producer",
            )
        tampered = dict(valid)
        tampered["observed_at"] = "2026-08-11T00:00:00Z"
        with self.assertRaisesRegex(manager.BlueprintError, "payload|authority"):
            manager.validate_signed_boot_document(
                tampered, manager.BOOT_ROLE_FIELDS, manager.BOOT_ROLE_SCHEMA,
                "tampered role", trust, "producer",
            )

    def test_boot_paths_and_reused_decisions_are_rejected(self) -> None:
        for value in ("../escape.json", "/tmp/escape.json", "Docs/../escape.json", "Docs//escape.json"):
            with self.subTest(value=value), self.assertRaises(manager.BlueprintError):
                manager.canonical_repo_relative_path(value, "fixture")
        attestations = []
        for index in range(2):
            attestations.append({
                "claim_id": f"claim-{index}", "run_id": f"run-{index}",
            })
        manager.validate_role_uniqueness(attestations, ["p0", "p1"])
        with self.assertRaisesRegex(manager.BlueprintError, "principals"):
            manager.validate_role_uniqueness(attestations, ["same", "same"])
        reused = [dict(attestations[0]), dict(attestations[1])]
        reused[1]["run_id"] = reused[0]["run_id"]
        with self.assertRaisesRegex(manager.BlueprintError, "run_id"):
            manager.validate_role_uniqueness(reused, ["p0", "p1"])

    def test_boot_command_tamper_and_artifact_mutation_fail_precommit(self) -> None:
        original = manager.BOOT_COMMANDS["theorem"]
        with mock.patch.dict(manager.BOOT_COMMANDS, {"theorem": original + (("evil.py",),)}):
            self.assertNotEqual(
                manager.sha256_bytes(manager.canonical(manager.boot_command_spec(manager.THEOREM))),
                manager.sha256_bytes(manager.canonical(manager.boot_command_spec(manager.CONJECTURE))),
            )
        guard_path = self.root / "guard.json"
        guard_path.write_text("before", encoding="utf-8")
        guard = manager.regular_file_expectation(guard_path)
        assert guard is not None
        destination = self.root / "Output.md"
        destination.write_text("old", encoding="utf-8")
        destination_guard = manager.regular_file_expectation(destination)
        assert destination_guard is not None
        def mutate_final_command_artifact():
            guard_path.write_text("after", encoding="utf-8")
        fixture_program = replace(
            self.program, blueprint=destination, gantt=self.program.gantt
        )
        with (
            mock.patch.object(manager, "THEOREM", fixture_program),
            self.assertRaisesRegex(manager.BlueprintError, "compare-and-swap"),
        ):
            manager.atomic_batch_write(
                [(destination, b"new")],
                expected_old={destination: destination_guard},
                guards={guard_path: guard},
                precommit_validator=mutate_final_command_artifact,
            )
        self.assertEqual(destination.read_text(encoding="utf-8"), "old")

    def test_untrusted_recovery_journal_blocks_without_mutating_destination(self) -> None:
        transaction = Path(tempfile.mkdtemp(
            prefix=manager.BOOTSTRAP_TRANSACTION_PREFIX, dir=manager.DOCS
        ))
        marker = transaction / "attacker"
        marker.write_text("untrusted", encoding="utf-8")
        self.addCleanup(lambda: transaction.rmdir() if transaction.exists() else None)
        self.addCleanup(lambda: marker.unlink() if marker.exists() else None)
        before = manager.THEOREM.blueprint.read_bytes()
        with self.assertRaisesRegex(manager.BlueprintError, "automatic replay is forbidden"):
            manager.recover_batch_transactions()
        self.assertEqual(manager.THEOREM.blueprint.read_bytes(), before)

    def test_schema_valid_fake_journal_is_never_path_recovered(self) -> None:
        victim = self.root / "Fake_Journal_Victim.md"
        victim.write_bytes(b"trusted-victim")
        victim_expectation = manager.regular_file_expectation(victim)
        assert victim_expectation is not None
        fixture_program = replace(self.program, blueprint=victim)
        transaction = Path(
            tempfile.mkdtemp(prefix=manager.BOOTSTRAP_TRANSACTION_PREFIX, dir=manager.DOCS)
        )
        self.addCleanup(
            lambda: manager.cleanup_transaction(transaction) if transaction.exists() else None
        )
        attacker_backup = transaction / "old-00.bin"
        attacker_backup.write_bytes(b"attacker-controlled-restore")
        attacker_expectation = manager.regular_file_expectation(attacker_backup)
        assert attacker_expectation is not None
        manifest = {
            "schema_version": "awesome-theorems/stage5-output-transaction/1.1",
            "phase": "prepared",
            "outputs": [{
                "destination": victim.relative_to(ROOT).as_posix(),
                "staged_name": "new-00.bin",
                "backup_name": "old-00.bin",
                "old_sha256": attacker_expectation.sha256,
                "old_stat": attacker_expectation.stat_identity,
                "new_sha256": victim_expectation.sha256,
                "new_stat": victim_expectation.stat_identity,
            }],
        }
        manager.write_transaction_manifest(transaction, manifest)
        with mock.patch.object(manager, "THEOREM", fixture_program):
            manager.validate_transaction_manifest(transaction)
            with self.assertRaisesRegex(manager.BlueprintError, "path-based.*forbidden"):
                manager.recover_one_transaction(transaction)
        self.assertEqual(victim.read_bytes(), b"trusted-victim")
        self.assertEqual(attacker_backup.read_bytes(), b"attacker-controlled-restore")

    def test_transaction_manifest_rejects_filename_and_digest_drift(self) -> None:
        transaction = Path(
            tempfile.mkdtemp(prefix=manager.BOOTSTRAP_TRANSACTION_PREFIX, dir=manager.DOCS)
        )
        self.addCleanup(lambda: manager.cleanup_transaction(transaction) if transaction.exists() else None)
        destination = manager.THEOREM.blueprint.relative_to(ROOT).as_posix()
        manifest = {
            "schema_version": "awesome-theorems/stage5-output-transaction/1.1",
            "phase": "staging",
            "outputs": [{
                "destination": destination,
                "staged_name": "manifest.json",
                "backup_name": "old-00.bin",
                "old_sha256": None,
                "old_stat": None,
                "new_sha256": "0" * 64,
                "new_stat": None,
            }],
        }
        manager.write_transaction_manifest(transaction, manifest)
        with self.assertRaisesRegex(manager.BlueprintError, "unsafe batch transaction row"):
            manager.validate_transaction_manifest(transaction)


if __name__ == "__main__":
    unittest.main(verbosity=2)
