#!/usr/bin/env python3
"""Focused regression tests for the Stage1 v2 dependency/reuse gate."""

from __future__ import annotations

import copy
import contextlib
import datetime as dt
import hashlib
import inspect
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from unittest import mock

CRON_PATH = Path(__file__).with_name("stage1_execution_cron.py")
CRON_SPEC = importlib.util.spec_from_file_location("stage1_execution_cron_under_test", CRON_PATH)
if CRON_SPEC is None or CRON_SPEC.loader is None:
    raise RuntimeError(f"cannot load {CRON_PATH}")
cron = importlib.util.module_from_spec(CRON_SPEC)
CRON_SPEC.loader.exec_module(cron)

INTAKE_VALIDATOR_PATH = (
    Path(__file__).resolve().parents[1]
    / "Stage1_Instances"
    / "THM-M-0387"
    / "check_intake.py"
)
INTAKE_VALIDATOR_SPEC = importlib.util.spec_from_file_location(
    "stage1_m0387_intake_validator_under_test", INTAKE_VALIDATOR_PATH
)
if INTAKE_VALIDATOR_SPEC is None or INTAKE_VALIDATOR_SPEC.loader is None:
    raise RuntimeError(f"cannot load {INTAKE_VALIDATOR_PATH}")
intake_validator = importlib.util.module_from_spec(INTAKE_VALIDATOR_SPEC)
INTAKE_VALIDATOR_SPEC.loader.exec_module(intake_validator)


CHILD = "THM-M-0990"
PARENT = "THM-M-0989"
EDGE = "HARD-THM-M-0989-THM-M-0990-PROOF"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refresh_blueprint_progress_summary(text: str) -> str:
    """Render the summary from the fixture rows instead of a live SSOT snapshot."""
    body = cron.checklist_body(text)
    counts = Counter(match["state"] for match in cron.CHECKLIST_ROW_RE.finditer(body))
    total = sum(counts.values())
    if total != 1546 * len(cron.PHASES):
        raise AssertionError(f"fixture blueprint has {total} checklist rows")
    summary = (
        "Authoritative progress summary (derived and validated from the rows below):\n"
        f"- `[_]` {counts['[_]']} ({100 * counts['[_]'] / total:.2f}% worker self-tested)\n"
        f"- `[ ]` {counts['[ ]']}\n"
        f"- `[x]` {counts['[x]']}"
    )
    pattern = (
        r"Authoritative progress summary \(derived and validated from the rows below\):\n"
        r"- `\[_\]` \d+ \([0-9.]+% worker self-tested\)\n"
        r"- `\[ \]` \d+\n"
        r"- `\[x\]` \d+"
    )
    updated, count = re.subn(pattern, summary, text, count=1)
    if count != 1:
        raise AssertionError("fixture blueprint progress summary is missing or ambiguous")
    return updated


def lean_declaration_signature(path: Path, declaration: str) -> str:
    """Extract the normalized signature used by the production gate."""
    text = path.read_text(encoding="utf-8", errors="replace")
    stripped = re.sub(r'(?s)/-.*?-/|--[^\n]*|"(?:\\.|[^"\\])*"', "", text)
    declaration_tail = declaration.rsplit(".", 1)[-1]
    match = re.search(
        rf"(?ms)^\s*(?:theorem|lemma|def|abbrev)\s+{re.escape(declaration_tail)}\b(.*?)\s*:=",
        stripped,
    )
    if match is None:
        raise AssertionError(f"fixture declaration {declaration} is missing from {path}")
    signature = " ".join(match.group(1).split())
    signature = signature.split(":", 1)[-1].strip() if ":" in signature else signature
    return signature


def lean_declaration_fingerprint(path: Path, declaration: str) -> str:
    signature = lean_declaration_signature(path, declaration)
    return hashlib.sha256(signature.encode("utf-8")).hexdigest()


class SchedulerOwnedIntakeValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        root = Path(__file__).resolve().parents[1]
        owner = root / "Stage1_Instances" / "THM-M-0387"
        self.instance = json.loads((owner / "intake.json").read_text(encoding="utf-8"))
        self.receipt = json.loads(
            (owner / "intake-receipt.json").read_text(encoding="utf-8")
        )
        self.ledger = json.loads(
            (owner / "dependency-reuse-ledger.json").read_text(encoding="utf-8")
        )

    def test_stable_provenance_must_agree_across_intake_evidence(self) -> None:
        intake_validator.require_stable_provenance_consistency(
            self.instance, self.receipt, self.ledger
        )
        mutations = (
            (self.receipt, "base_revision", "f" * 40),
            (self.receipt["inputs"], "theorem_dag_sha256", "f" * 64),
            (self.ledger, "repository_revision", "e" * 40),
        )
        for record, field, replacement in mutations:
            original = record[field]
            record[field] = replacement
            with self.subTest(field=field), self.assertRaisesRegex(
                ValueError, "disagrees across intake evidence"
            ):
                intake_validator.require_stable_provenance_consistency(
                    self.instance, self.receipt, self.ledger
                )
            record[field] = original

    def test_required_narrative_evidence_rejects_empty_values(self) -> None:
        for value in ([], [""], ["valid", "  "]):
            with self.subTest(value=value), self.assertRaisesRegex(
                ValueError, "empty"
            ):
                intake_validator.require_nonempty_strings(value, "evidence is empty")

    def test_phase_contract_record_cache_tracks_checkpointed_head(self) -> None:
        first = "1" * 40
        second = "2" * 40
        loaded: list[str] = []

        records = iter((first, second))
        revisions_seen: list[object] = []

        def load_contract(
            root: Path, expected_sha256: str, **kwargs: object
        ) -> dict[str, object]:
            self.assertEqual(root, cron.ROOT)
            self.assertEqual(expected_sha256, cron.PHASE_ACCEPTANCE_CONTRACT_SHA256)
            revisions_seen.append(kwargs.get("revision"))
            revision = next(records)
            loaded.append(revision)
            return {"revision": revision, "contract": {"phase_order": []}}

        cron._phase_acceptance_contract_record_at.cache_clear()
        self.addCleanup(cron._phase_acceptance_contract_record_at.cache_clear)
        with (
            mock.patch.object(
                cron,
                "authoritative_head_revision",
                side_effect=[first, first, first, second, second],
            ),
            mock.patch.object(
                cron.acceptance_evidence, "load_head_contract", side_effect=load_contract
            ),
        ):
            self.assertEqual(cron.phase_acceptance_contract_record()["revision"], first)
            self.assertEqual(cron.phase_acceptance_contract()["phase_order"], [])
            self.assertEqual(cron.phase_acceptance_contract_record()["revision"], second)

        self.assertEqual(loaded, [first, second])
        self.assertEqual(revisions_seen, [None, None])


class DurableWorkerHandoffTests(unittest.TestCase):
    CLAIM_ID = "20260716T120000Z-0123456789ab"

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.runtime = self.root / ".cron" / "stage1-v2-app-server"
        self.runtime.mkdir(parents=True)
        self.item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "phase": "intake",
            "layer": 0,
            "state": "[_]",
            "attempts": 1,
            "depends_on": [],
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
        }
        self.claim = {
            "lane": cron.IMPLEMENTATION_LANE,
            "claim_id": self.CLAIM_ID,
            "item_id": self.item["id"],
            "theorem_id": self.item["theorem_id"],
            "base_revision": "b" * 40,
            "status": "finished_integrated",
            "runtime_protocol": cron.RUNTIME_PROTOCOL,
            "fresh_revalidation": False,
            "goal_objective": "implement",
            "goal_objective_path": str(self.runtime / "goals" / "impl.txt"),
            "app_server_status": str(self.runtime / "app-server" / "impl.json"),
            "output_log": str(self.runtime / "logs" / "impl.out"),
            "workspace": str(self.runtime / "workers" / "slot1"),
            "selftest_manifest": str(
                self.runtime / "workers" / "slot1" / ".stage1-worker-selftest.json"
            ),
        }
        self.payload = (
            json.dumps({
                "item_id": self.item["id"],
                "state": "[_]",
                "base_revision": self.claim["base_revision"],
                "changed_paths": ["Stage1_Instances/THM-M-0001/intake.json"],
                "commands": ["python3 check_intake.py"],
            }, sort_keys=True) + "\n"
        ).encode()

    def archive(self) -> Path:
        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
        ):
            path, digest, size = cron.persist_worker_handoff(
                self.claim, self.payload
            )
        self.claim.update({
            "worker_handoff_archive_schema": cron.WORKER_HANDOFF_ARCHIVE_SCHEMA,
            "worker_handoff_path": str(path),
            "worker_handoff_sha256": digest,
            "worker_handoff_size": size,
        })
        return path

    def test_archive_survives_slot_reuse_and_is_exactly_bound(self) -> None:
        path = self.archive()
        shutil.rmtree(Path(str(self.claim["workspace"])), ignore_errors=True)
        Path(str(self.claim["workspace"])).mkdir(parents=True)
        (Path(str(self.claim["workspace"])) / ".stage1-worker-selftest.json").write_text(
            '{"item_id":"S56-M-9999-INTAKE"}\n', encoding="utf-8"
        )
        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
        ):
            data, digest, loaded = cron.read_persisted_worker_handoff(self.claim)
            self.assertIs(cron.review_source_claim(self.item, [self.claim]), self.claim)
        self.assertEqual((data, loaded), (self.payload, path))
        self.assertEqual(digest, hashlib.sha256(self.payload).hexdigest())

    def test_review_provenance_binds_original_archived_bytes(self) -> None:
        path = self.archive()
        handoff_sha256 = hashlib.sha256(self.payload).hexdigest()
        provenance = {
            "schema_version": cron.WORKER_PROVENANCE_SCHEMA,
            "claim": copy.deepcopy(self.claim),
            "files": {
                "selftest_manifest": {
                    "path": str(path),
                    "sha256": handoff_sha256,
                    "size": len(self.payload),
                    "content_base64": __import__("base64").b64encode(
                        self.payload
                    ).decode(),
                }
            },
        }
        provenance["snapshot_sha256"] = cron.canonical_json_sha256(provenance)
        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
        ):
            source, record = cron.validate_review_provenance_handoff(
                self.item, provenance
            )
        self.assertEqual(source["claim_id"], self.CLAIM_ID)
        self.assertEqual(record["sha256"], handoff_sha256)
        tampered = copy.deepcopy(provenance)
        tampered["files"]["selftest_manifest"]["size"] += 1
        tampered["snapshot_sha256"] = cron.canonical_json_sha256(
            {key: value for key, value in tampered.items() if key != "snapshot_sha256"}
        )
        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            self.assertRaisesRegex(ValueError, "durable worker handoff"),
        ):
            cron.validate_review_provenance_handoff(self.item, tampered)

    def test_archive_is_idempotent_and_rejects_conflict_tamper_and_symlink(self) -> None:
        path = self.archive()
        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
        ):
            self.assertEqual(
                cron.persist_worker_handoff(self.claim, self.payload)[0], path
            )
            conflicting = self.payload.replace(b"check_intake", b"check_other_")
            with self.assertRaisesRegex(ValueError, "conflicts"):
                cron.persist_worker_handoff(self.claim, conflicting)
            self.claim["worker_handoff_sha256"] = "0" * 64
            with self.assertRaisesRegex(ValueError, "binding"):
                cron.read_persisted_worker_handoff(self.claim)
            self.claim["worker_handoff_sha256"] = hashlib.sha256(self.payload).hexdigest()
            path.unlink()
            outside = self.root / "outside.json"
            outside.write_bytes(self.payload)
            path.symlink_to(outside)
            with self.assertRaisesRegex(ValueError, "missing or unsafe"):
                cron.read_persisted_worker_handoff(self.claim)

    def test_duplicate_key_handoff_is_rejected(self) -> None:
        duplicate = (
            '{"item_id":"S56-M-0001-INTAKE","item_id":"S56-M-0001-INTAKE",'
            '"state":"[_]","base_revision":"' + "b" * 40 + '"}\n'
        ).encode()
        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            self.assertRaisesRegex(ValueError, "duplicate key"),
        ):
            cron.persist_worker_handoff(self.claim, duplicate)

    def test_failed_archive_create_removes_partial_leaf(self) -> None:
        real_write = os.write
        writes = 0

        def fail_after_partial(descriptor: int, value: object) -> int:
            nonlocal writes
            writes += 1
            if writes == 1:
                data = bytes(value)
                return real_write(descriptor, data[: max(1, len(data) // 2)])
            raise OSError("injected archive write failure")

        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(cron.os, "write", side_effect=fail_after_partial),
            self.assertRaisesRegex(OSError, "injected"),
        ):
            cron.persist_worker_handoff(self.claim, self.payload)
        self.assertFalse(
            (self.runtime / "worker-handoffs" / f"{self.CLAIM_ID}.json").exists()
        )

    def test_reconcile_is_bounded_and_excludes_unmigrated_sources_from_review(self) -> None:
        items: list[dict[str, object]] = []
        claims: list[dict[str, object]] = []
        nodes: dict[str, dict[str, int]] = {}
        for index in range(1, 82):
            item = {
                **self.item,
                "id": f"S56-M-{index:04d}-INTAKE",
                "theorem_id": f"THM-M-{index:04d}",
                "owned_paths": [f"Stage1_Instances/THM-M-{index:04d}"],
            }
            claim = {
                **self.claim,
                "claim_id": f"20260716T12{index // 60:02d}{index % 60:02d}Z-{index:012x}",
                "item_id": item["id"],
                "theorem_id": item["theorem_id"],
            }
            items.append(item)
            claims.append(claim)
            nodes[item["theorem_id"]] = {"v2_execution_rank": index}
        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, nodes)),
        ):
            self.assertTrue(
                cron.reconcile_finished_implementation_handoffs(items, claims)
            )
            self.assertEqual(
                sum(row["status"] == "revalidation_required" for row in claims), 50
            )
            self.assertEqual(cron.review_candidates(items, claims), [])


class DependencyReuseLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        cron.theorem_dag_v2.cache_clear()
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)
        self.parent_artifact = self.root / "Stage1_Instances" / PARENT / "Proof.lean"
        self.parent_artifact.parent.mkdir(parents=True)
        self.parent_artifact.write_text("theorem provider : True := by trivial\n", encoding="utf-8")
        self.consumer_import = self.root / "Stage1_Instances" / CHILD / "GeneralizedLindeberg.lean"
        self.consumer_import.parent.mkdir(parents=True, exist_ok=True)
        self.consumer_import.write_text("theorem consumeProvider : True := by trivial\n", encoding="utf-8")
        self.parent_receipt = self.write_receipt(PARENT, "proof", accepted=True)
        self.consumer_receipt = self.write_receipt(CHILD, "validation", accepted=True)
        self.dag_path = self.root / "Docs" / "Stage1_Execution_DAG_rev-5.6.json"
        self.dag_path.parent.mkdir(parents=True, exist_ok=True)
        dag = copy.deepcopy(cron.read_json(cron.DAG))
        for item in dag["items"]:
            if item["theorem_id"] in {PARENT, CHILD}:
                item["state"] = "[x]"
        self.dag_path.write_text(json.dumps(dag) + "\n", encoding="utf-8")
        self.blueprint_path = self.root / "Docs" / "Stage1_Blueprint_v2.md"
        blueprint = cron.BLUEPRINT.read_text(encoding="utf-8")
        for theorem_id in (PARENT, CHILD):
            for phase in cron.PHASE_NAMES:
                item_id = cron.task_id(theorem_id, phase)
                pattern = rf"^- (\[[_x ]\]) (`{re.escape(item_id)}`)"
                match = re.search(pattern, blueprint, re.MULTILINE)
                if match is None:
                    self.fail(f"missing SSOT fixture row: {item_id}")
                blueprint = re.sub(pattern, r"- [x] \2", blueprint, count=1, flags=re.MULTILINE)
        blueprint = refresh_blueprint_progress_summary(blueprint)
        self.blueprint_path.write_text(blueprint, encoding="utf-8")
        self.dag_patch = mock.patch.object(cron, "DAG", self.dag_path)
        self.dag_patch.start()
        self.addCleanup(self.dag_patch.stop)
        self.blueprint_patch = mock.patch.object(cron, "BLUEPRINT", self.blueprint_path)
        self.blueprint_patch.start()
        self.addCleanup(self.blueprint_patch.stop)
        graph, nodes = cron.theorem_dag_v2()
        self.fixture_graph = copy.deepcopy(graph)
        self.fixture_nodes = copy.deepcopy(nodes)
        fixture_edge = next(edge for edge in self.fixture_graph["hard_edges"] if edge["edge_id"] == EDGE)
        fixture_edge["material_contract"] = {
            "contract_kind": "cross_target_import_and_proof_receipt_input",
            "provider_sources": [{
                "path": self.parent_artifact.relative_to(self.root).as_posix(),
                "sha256": sha256(self.parent_artifact),
                "declarations": ["provider"],
            }],
            "consumer_sources": [{
                "path": self.consumer_import.relative_to(self.root).as_posix(),
                "sha256": sha256(self.consumer_import),
                "declarations": ["consumeProvider"],
            }],
            "receipt_input_binding": {
                "path": f"Stage1_Instances/{CHILD}/proof-receipt.json",
                "sha256": "0" * 64,
                "json_pointer": "/inputs/test_dependency",
            },
        }
        self.theorem_dag_patch = mock.patch.object(
            cron, "theorem_dag_v2", return_value=(self.fixture_graph, self.fixture_nodes)
        )
        self.theorem_dag_patch.start()
        self.addCleanup(self.theorem_dag_patch.stop)
        self.ledger_path = self.root / "Stage1_Instances" / CHILD / "dependency-reuse-ledger.json"
        self.ledger = self.make_ledger()
        self.write_ledger()

    def write_receipt(self, theorem_id: str, phase: str, *, accepted: bool) -> Path:
        path = self.root / "Stage1_Instances" / theorem_id / f"{phase}-receipt.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        receipt = {
            "schema_version": "stage1-node-receipt/1.0",
            "receipt_id": f"{theorem_id}-{phase}-accepted",
            "item_id": f"S56-{theorem_id.removeprefix('THM-')}-{phase.upper()}",
            "theorem_id": theorem_id,
            "phase": phase,
            "intent": "validate" if phase == "validation" else "prove",
            "base_revision": "test-revision",
            "inputs": {"fixture_sha256": "f" * 64},
            "accepted": accepted,
            "support_state": "master_accepted" if accepted else "provisional_worker_selftest",
            "proposed_state": "[x]" if accepted else "[_]",
            "verdict": "accepted" if accepted else "blocked",
            "selftest_status": "passed" if accepted else "blocked",
            "selftest_result": {"exit_code": 0 if accepted else 1, "commands": ["test-command"]},
        }
        path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def refresh_fixture_material_contract(self) -> None:
        edge = next(row for row in self.fixture_graph["hard_edges"] if row["edge_id"] == EDGE)
        edge["material_contract"]["provider_sources"][0]["sha256"] = sha256(self.parent_artifact)
        edge["material_contract"]["consumer_sources"][0]["sha256"] = sha256(self.consumer_import)

    def reference(self, path: Path) -> dict[str, str]:
        receipt = json.loads(path.read_text(encoding="utf-8"))
        return {
            "path": path.relative_to(self.root).as_posix(),
            "receipt_id": receipt["receipt_id"],
            "sha256": sha256(path),
        }

    def make_ledger(self) -> dict[str, object]:
        expected = cron.expected_dependency_context(CHILD)
        _, nodes = cron.theorem_dag_v2()
        phase_states = {
            item["phase"]: item["state"]
            for item in cron.read_json(cron.DAG)["items"]
            if item["theorem_id"] == PARENT
        }
        decision = {
            "source_id": EDGE,
            "consumer_obligation_id": "M0990-ROOT",
            "provider_theorem_id": PARENT,
            "provider_obligation_id": "M0989-ROOT",
            "terminal_proof_body_id": "provider",
            "provider_body_source": {
                "path": self.parent_artifact.relative_to(self.root).as_posix(),
                "sha256": sha256(self.parent_artifact),
            },
            "provider_statement_fingerprint": hashlib.sha256(b"True").hexdigest(),
            "consumer_required_fingerprint": hashlib.sha256(b"True").hexdigest(),
            "relationship": "exact",
            "provider_proof_state": phase_states["proof"],
            "provider_receipts": [self.reference(self.parent_receipt)],
            "decision": "reused_exact",
            "consumer_import_or_wrapper": "consumeProvider",
            "consumer_import_source": {
                "path": self.consumer_import.relative_to(self.root).as_posix(),
                "sha256": sha256(self.consumer_import),
            },
            "consumer_validation_receipts": [self.reference(self.consumer_receipt)],
            "context_digest": nodes[CHILD]["dependency_context_sha256"],
        }
        decisions = [decision]
        for source_id in expected["shared_group_ids"]:
            graph, _ = cron.theorem_dag_v2()
            group = next(row for row in graph["shared_lemma_groups"] if row["group_id"] == source_id)
            provider = next(theorem_id for theorem_id in group["member_theorem_ids"] if theorem_id != CHILD)
            decisions.append(
                {
                    "source_id": source_id,
                    "provider_theorem_id": provider,
                    "decision": "not_applicable",
                    "non_reuse_reason": "weak shared-module hint has no checked exact transport",
                    "context_digest": nodes[CHILD]["dependency_context_sha256"],
                }
            )
        return {
            "schema_version": cron.DEPENDENCY_LEDGER_SCHEMA,
            "consumer_theorem_id": CHILD,
            "observed_theorem_dag_sha256": cron.graph_sha256(),
            "dependency_context_sha256": nodes[CHILD]["dependency_context_sha256"],
            "repository_revision": "test-revision",
            **expected,
            "inspections": [
                {
                    "theorem_id": PARENT,
                    "phase_states": phase_states,
                    "artifact_digests": {
                        self.parent_artifact.relative_to(self.root).as_posix(): sha256(self.parent_artifact)
                    },
                    "compatibility": "exact",
                }
            ],
            "reuse_decisions": decisions,
            "unresolved_compatibility_obligations": [],
        }

    def write_ledger(self) -> None:
        self.refresh_fixture_material_contract()
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
        self.ledger_path.write_text(json.dumps(self.ledger, indent=2) + "\n", encoding="utf-8")

    def validate(self) -> dict[str, object]:
        return cron.validate_dependency_reuse_ledger(
            self.ledger_path,
            CHILD,
            expected_observed_graph_sha256=cron.graph_sha256(),
            evidence_root=self.root,
            authoritative_root=self.root,
        )

    def copy_authoritative_state(self, root: Path) -> None:
        docs = root / "Docs"
        docs.mkdir(parents=True, exist_ok=True)
        (docs / "Stage1_Blueprint_v2.md").write_bytes(self.blueprint_path.read_bytes())
        (docs / "Stage1_Execution_DAG_rev-5.6.json").write_bytes(self.dag_path.read_bytes())

    def decision(self) -> dict[str, object]:
        return next(row for row in self.ledger["reuse_decisions"] if row["source_id"] == EDGE)

    def test_valid_hard_parent_ledger_and_phase_names_are_accepted(self) -> None:
        self.assertEqual(set(self.ledger["inspections"][0]["phase_states"]), cron.PHASE_NAMES)
        self.assertEqual(self.validate()["consumer_theorem_id"], CHILD)

    def test_ledger_repository_revision_binds_worker_claim(self) -> None:
        with self.assertRaisesRegex(ValueError, "worker claim"):
            cron.validate_dependency_reuse_ledger(
                self.ledger_path,
                CHILD,
                expected_repository_revision="different-revision",
                evidence_root=self.root,
                authoritative_root=self.root,
            )

    def test_shared_group_decision_names_an_actual_member_provider(self) -> None:
        group_decision = next(
            row for row in self.ledger["reuse_decisions"] if row["source_id"].startswith("SHARED-")
        )
        graph, _ = cron.theorem_dag_v2()
        group = next(row for row in graph["shared_lemma_groups"] if row["group_id"] == group_decision["source_id"])
        provider = next(theorem_id for theorem_id in group["member_theorem_ids"] if theorem_id != CHILD)
        group_decision["provider_theorem_id"] = provider
        self.write_ledger()
        self.validate()

        group_decision["provider_theorem_id"] = "THM-M-0001"
        self.write_ledger()
        with self.assertRaisesRegex(ValueError, "not a member"):
            self.validate()

    def test_incomplete_or_stale_context_is_rejected(self) -> None:
        for field in (
            "direct_parent_ids",
            "transitive_ancestor_ids",
            "hard_edge_ids",
            "reuse_hint_ids",
            "shared_group_ids",
        ):
            with self.subTest(field=field):
                original = copy.deepcopy(self.ledger)
                del self.ledger[field]
                self.write_ledger()
                with self.assertRaisesRegex(ValueError, "incomplete"):
                    self.validate()
                self.ledger = original
        self.ledger["inspections"][0]["phase_states"].pop("release")
        self.write_ledger()
        with self.assertRaisesRegex(ValueError, "phase states"):
            self.validate()

    def test_artifact_path_and_digest_fail_closed(self) -> None:
        digests = self.ledger["inspections"][0]["artifact_digests"]
        relative = next(iter(digests))
        digests[relative] = "0" * 64
        self.write_ledger()
        with self.assertRaisesRegex(ValueError, "artifact digest"):
            self.validate()

    def test_inspection_artifact_must_belong_to_inspected_parent(self) -> None:
        foreign = self.root / "Stage1_Instances" / CHILD / "validation-receipt.json"
        self.ledger["inspections"][0]["artifact_digests"] = {
            foreign.relative_to(self.root).as_posix(): sha256(foreign)
        }
        self.write_ledger()
        with self.assertRaisesRegex(ValueError, "artifact digest"):
            self.validate()

    def test_artifact_symlink_cannot_escape_evidence_root(self) -> None:
        outside = Path(self.temporary.name).parent / f"{Path(self.temporary.name).name}-outside"
        outside.write_text("outside\n", encoding="utf-8")
        self.addCleanup(outside.unlink)
        link = self.root / "Stage1_Instances" / PARENT / "escape"
        link.symlink_to(outside)
        self.ledger["inspections"][0]["artifact_digests"] = {
            link.relative_to(self.root).as_posix(): sha256(outside)
        }
        self.write_ledger()
        with self.assertRaisesRegex(ValueError, "artifact digest"):
            self.validate()

    def test_receipt_symlink_cannot_cross_theorem_owner(self) -> None:
        foreign = self.root / "Stage1_Instances" / "THM-M-0001" / "validation-receipt.json"
        foreign.parent.mkdir(parents=True, exist_ok=True)
        foreign.write_text(self.consumer_receipt.read_text(encoding="utf-8"), encoding="utf-8")
        link = self.root / "Stage1_Instances" / CHILD / "linked-validation-receipt.json"
        link.symlink_to(foreign)
        decision = self.decision()
        decision["consumer_validation_receipts"] = [{
            "path": link.relative_to(self.root).as_posix(),
            "receipt_id": json.loads(foreign.read_text(encoding="utf-8"))["receipt_id"],
            "sha256": sha256(foreign),
        }]
        self.write_ledger()
        ledger = self.validate()
        item = {"phase": "validation", "theorem_id": CHILD, "owned_paths": [f"Stage1_Instances/{CHILD}"]}
        with self.assertRaisesRegex(ValueError, "hard-edge master gate failed"):
            cron.enforce_master_hard_edge_gate(
                item,
                ledger,
                evidence_root=self.root,
                authoritative_root=self.root,
            )

    def test_worker_cannot_rewrite_authoritative_parent_evidence(self) -> None:
        authoritative = self.root / "authoritative"
        worker = self.root / "worker"
        relative = Path("Stage1_Instances") / PARENT / "Proof.lean"
        authoritative_artifact = authoritative / relative
        worker_artifact = worker / relative
        authoritative_artifact.parent.mkdir(parents=True)
        self.copy_authoritative_state(authoritative)
        worker_artifact.parent.mkdir(parents=True)
        authoritative_artifact.write_text("theorem provider : True := by trivial\n", encoding="utf-8")
        worker_artifact.write_text("theorem provider : False := by trivial\n", encoding="utf-8")
        self.ledger["inspections"][0]["artifact_digests"] = {
            relative.as_posix(): sha256(worker_artifact)
        }
        ledger_path = worker / "Stage1_Instances" / CHILD / "dependency-reuse-ledger.json"
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        ledger_path.write_text(json.dumps(self.ledger, indent=2) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "artifact digest"):
            cron.validate_dependency_reuse_ledger(
                ledger_path,
                CHILD,
                evidence_root=worker,
                authoritative_root=authoritative,
            )
        self.ledger = self.make_ledger()
        self.ledger["inspections"][0]["artifact_digests"] = {"../escape": "0" * 64}
        self.write_ledger()
        with self.assertRaisesRegex(ValueError, "artifact digest"):
            self.validate()

    def test_decision_material_fields_are_required(self) -> None:
        for field in (
            "consumer_obligation_id",
            "provider_theorem_id",
            "provider_obligation_id",
            "terminal_proof_body_id",
            "provider_body_source",
            "provider_statement_fingerprint",
            "consumer_required_fingerprint",
            "relationship",
            "provider_proof_state",
            "provider_receipts",
            "consumer_import_or_wrapper",
            "consumer_import_source",
            "context_digest",
        ):
            with self.subTest(field=field):
                original = copy.deepcopy(self.ledger)
                self.decision().pop(field)
                self.write_ledger()
                with self.assertRaises(ValueError):
                    self.validate()
                self.ledger = original

    def test_nonaccepted_decision_requires_a_reason(self) -> None:
        decision = self.decision()
        decision["decision"] = "blocked_missing_acceptance"
        decision.pop("provider_receipts")
        decision.pop("consumer_import_or_wrapper")
        self.write_ledger()
        with self.assertRaisesRegex(ValueError, "non_reuse_reason"):
            self.validate()

    def test_provider_receipt_is_content_and_authority_bound(self) -> None:
        reference = self.decision()["provider_receipts"][0]
        mutations = {
            "missing": lambda: reference.update(path=f"Stage1_Instances/{PARENT}/missing.json"),
            "escape": lambda: reference.update(path="../receipt.json"),
            "wrong id": lambda: reference.update(receipt_id="made-up"),
            "wrong digest": lambda: reference.update(sha256="0" * 64),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                original = copy.deepcopy(self.ledger)
                mutate()
                self.write_ledger()
                with self.assertRaises(ValueError):
                    self.validate()
                self.ledger = original
                reference = self.decision()["provider_receipts"][0]
        self.parent_receipt = self.write_receipt(PARENT, "proof", accepted=False)
        receipt = json.loads(self.parent_receipt.read_text(encoding="utf-8"))
        receipt["verdict"] = "no_state_change"
        receipt["selftest_status"] = "passed"
        receipt["selftest_result"] = {"exit_code": 0, "commands": ["provider-proof-command"]}
        self.parent_receipt.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
        self.decision()["provider_receipts"] = [self.reference(self.parent_receipt)]
        self.write_ledger()
        self.validate()

    def test_provider_proof_state_must_match_the_inspection(self) -> None:
        self.decision()["provider_proof_state"] = "[ ]"
        self.write_ledger()
        with self.assertRaisesRegex(ValueError, "provider proof state is stale"):
            self.validate()

    def test_checked_transport_still_requires_consumer_owned_material_and_receipt(self) -> None:
        decision = self.decision()
        decision["decision"] = "reused_with_transport"
        decision["relationship"] = "checked_transport"
        self.ledger["inspections"][0]["compatibility"] = "checked_transport"
        decision["consumer_required_fingerprint"] = hashlib.sha256(b"True").hexdigest()
        self.write_ledger()
        self.validate()

        for field in ("consumer_import_source", "consumer_validation_receipts"):
            with self.subTest(field=field):
                original = copy.deepcopy(self.ledger)
                self.decision().pop(field)
                self.write_ledger()
                if field == "consumer_import_source":
                    with self.assertRaises(ValueError):
                        self.validate()
                else:
                    ledger = self.validate()
                    item = {
                        "phase": "validation",
                        "theorem_id": CHILD,
                        "owned_paths": [f"Stage1_Instances/{CHILD}"],
                    }
                    with self.assertRaisesRegex(ValueError, "hard-edge master gate failed"):
                        cron.enforce_master_hard_edge_gate(item, ledger, evidence_root=self.root)
                self.ledger = original

    def test_accepted_reuse_cannot_hide_mismatch_or_unresolved_work(self) -> None:
        mutations = (
            lambda: self.decision().update(relationship="mismatch"),
            lambda: self.ledger["inspections"][0].update(compatibility="mismatch"),
            lambda: self.decision().update(consumer_required_fingerprint="b" * 64),
            lambda: self.ledger.update(unresolved_compatibility_obligations=[EDGE]),
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                original = copy.deepcopy(self.ledger)
                mutation()
                self.write_ledger()
                with self.assertRaises(ValueError):
                    self.validate()
                self.ledger = original

    def test_accepted_reuse_material_must_bind_real_declarations(self) -> None:
        for field in ("terminal_proof_body_id", "consumer_import_or_wrapper"):
            with self.subTest(field=field):
                original = copy.deepcopy(self.ledger)
                self.decision()[field] = "fabricatedDeclaration"
                self.write_ledger()
                with self.assertRaisesRegex(ValueError, "not present"):
                    self.validate()
                self.ledger = original

    def test_same_owner_material_outside_hard_edge_allowlist_is_rejected(self) -> None:
        unlisted = self.root / "Stage1_Instances" / PARENT / "Unlisted.lean"
        unlisted.write_text("theorem unlistedProvider : True := by trivial\n", encoding="utf-8")
        decision = self.decision()
        decision["terminal_proof_body_id"] = "unlistedProvider"
        decision["provider_body_source"] = {
            "path": unlisted.relative_to(self.root).as_posix(),
            "sha256": sha256(unlisted),
        }
        self.write_ledger()
        with self.assertRaisesRegex(ValueError, "content-bound allowlist"):
            self.validate()

    def test_artifact_edge_release_does_not_inherit_provider_acceptance(self) -> None:
        child = "THM-M-0320"
        parent = "THM-M-0318"
        edge = "HARD-THM-M-0318-THM-M-0320-ARTIFACT"
        provider_artifact = self.root / "Stage1_Instances" / parent / "Vendor" / "Brouwer.lean"
        provider_artifact.parent.mkdir(parents=True, exist_ok=True)
        provider_artifact.write_text("theorem brouwer_source : True := by trivial\n", encoding="utf-8")
        consumer_import = self.root / "Stage1_Instances" / child / "BrouwerSource.lean"
        consumer_import.parent.mkdir(parents=True, exist_ok=True)
        consumer_import.write_text("theorem consumeBrouwer : True := by trivial\n", encoding="utf-8")
        provider_receipt = self.write_receipt(parent, "proof", accepted=False)
        provider_receipt_data = json.loads(provider_receipt.read_text(encoding="utf-8"))
        provider_receipt_data["verdict"] = "no_state_change"
        provider_receipt_data["selftest_status"] = "passed"
        provider_receipt_data["selftest_result"] = {"exit_code": 0, "commands": ["provider-proof-command"]}
        provider_receipt.write_text(json.dumps(provider_receipt_data, sort_keys=True) + "\n", encoding="utf-8")
        consumer_receipt = self.write_receipt(child, "validation", accepted=True)

        dag = json.loads(self.dag_path.read_text(encoding="utf-8"))
        for item in dag["items"]:
            if item["theorem_id"] == parent and item["phase"] == "proof":
                item["state"] = "[_]"
            if item["theorem_id"] == child and item["phase"] == "validation":
                item["state"] = "[x]"
        self.dag_path.write_text(json.dumps(dag) + "\n", encoding="utf-8")
        blueprint = self.blueprint_path.read_text(encoding="utf-8")
        for item_id, state in (
            (cron.task_id(parent, "proof"), "[_]"),
            (cron.task_id(child, "validation"), "[x]"),
        ):
            blueprint = re.sub(
                rf"^- \[[_x ]\] (`{re.escape(item_id)}`)",
                f"- {state} \\1",
                blueprint,
                count=1,
                flags=re.MULTILINE,
            )
        blueprint = refresh_blueprint_progress_summary(blueprint)
        self.blueprint_path.write_text(blueprint, encoding="utf-8")
        parent_states = {
            item["phase"]: item["state"] for item in dag["items"] if item["theorem_id"] == parent
        }
        expected = cron.expected_dependency_context(child)
        _, nodes = cron.theorem_dag_v2()
        ledger = {
            "schema_version": cron.DEPENDENCY_LEDGER_SCHEMA,
            "consumer_theorem_id": child,
            "observed_theorem_dag_sha256": cron.graph_sha256(),
            "dependency_context_sha256": nodes[child]["dependency_context_sha256"],
            "repository_revision": "test-revision",
            **expected,
            "inspections": [{
                "theorem_id": parent,
                "phase_states": parent_states,
                "artifact_digests": {
                    provider_artifact.relative_to(self.root).as_posix(): sha256(provider_artifact)
                },
                "compatibility": "exact",
            }],
            "reuse_decisions": [{
                "source_id": edge,
                "consumer_obligation_id": "M0320-ROOT",
                "provider_theorem_id": parent,
                "provider_obligation_id": "M0318-B-BROUWER",
                "terminal_proof_body_id": "brouwer_source",
                "provider_body_source": {
                    "path": provider_artifact.relative_to(self.root).as_posix(),
                    "sha256": sha256(provider_artifact),
                },
                "provider_statement_fingerprint": hashlib.sha256(b"True").hexdigest(),
                "consumer_required_fingerprint": hashlib.sha256(b"True").hexdigest(),
                "relationship": "exact",
                "provider_proof_state": "[_]",
                "provider_receipts": [self.reference(provider_receipt)],
                "decision": "reused_exact",
                "consumer_import_or_wrapper": "consumeBrouwer",
                "consumer_import_source": {
                    "path": consumer_import.relative_to(self.root).as_posix(),
                    "sha256": sha256(consumer_import),
                },
                "consumer_validation_receipts": [self.reference(consumer_receipt)],
                "context_digest": nodes[child]["dependency_context_sha256"],
            }],
            "unresolved_compatibility_obligations": [],
        }
        ledger_path = self.root / "Stage1_Instances" / child / "dependency-reuse-ledger.json"
        ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
        artifact_graph = copy.deepcopy(self.fixture_graph)
        artifact_edge = next(row for row in artifact_graph["hard_edges"] if row["edge_id"] == edge)
        artifact_edge["material_contract"] = {
            "contract_kind": "source_manifest_and_consumer_adapter",
            "provider_sources": [{
                "path": provider_artifact.relative_to(self.root).as_posix(),
                "sha256": sha256(provider_artifact),
                "declarations": ["brouwer_source"],
            }],
            "consumer_sources": [{
                "path": consumer_import.relative_to(self.root).as_posix(),
                "sha256": sha256(consumer_import),
                "declarations": ["consumeBrouwer"],
            }],
            "source_manifest_binding": {
                "path": f"Stage1_Instances/{child}/brouwer-source.json",
                "sha256": "0" * 64,
            },
        }
        with mock.patch.object(cron, "theorem_dag_v2", return_value=(artifact_graph, self.fixture_nodes)):
            validated = cron.validate_dependency_reuse_ledger(
                ledger_path,
                child,
                expected_observed_graph_sha256=cron.graph_sha256(),
                evidence_root=self.root,
                authoritative_root=self.root,
            )
        item = {"phase": "release", "theorem_id": child, "owned_paths": [f"Stage1_Instances/{child}"]}
        cron.enforce_master_hard_edge_gate(
            item,
            validated,
            evidence_root=self.root,
            authoritative_root=self.root,
        )

    def test_proof_gate_does_not_require_a_future_consumer_receipt(self) -> None:
        self.decision().pop("consumer_validation_receipts")
        self.write_ledger()
        ledger = self.validate()
        item = {"phase": "proof", "theorem_id": CHILD, "owned_paths": [f"Stage1_Instances/{CHILD}"]}
        cron.enforce_master_hard_edge_gate(item, ledger, evidence_root=self.root)

    def test_validation_and_release_require_bound_consumer_receipt(self) -> None:
        ledger = self.validate()
        decision = next(row for row in ledger["reuse_decisions"] if row["source_id"] == EDGE)
        decision["consumer_validation_receipts"] = [
            {"path": f"Stage1_Instances/{CHILD}/missing.json", "receipt_id": "made-up", "sha256": "0" * 64}
        ]
        for phase in ("validation", "release"):
            with self.subTest(phase=phase):
                item = {"phase": phase, "theorem_id": CHILD, "owned_paths": [f"Stage1_Instances/{CHILD}"]}
                with self.assertRaisesRegex(ValueError, "hard-edge master gate failed"):
                    cron.enforce_master_hard_edge_gate(item, ledger, evidence_root=self.root)

    def test_todo_gate_status_matches_proof_validation_release_timing(self) -> None:
        source_root = cron.ROOT
        real_graph = cron.read_json(cron.THEOREM_DAG_V2)
        real_nodes = {row["theorem_id"]: row for row in real_graph["theorems"]}
        status_root = self.root / "todo-status"
        status_dag = status_root / "Docs" / "Stage1_Execution_DAG_rev-5.6.json"
        status_graph = status_root / "Docs" / "Stage1_Theorem_DAG_v2.json"
        status_blueprint = status_root / "Docs" / "Stage1_Blueprint_v2.md"
        status_dag.parent.mkdir(parents=True)
        status_dag.write_bytes(self.dag_path.read_bytes())
        status_graph.write_bytes(cron.THEOREM_DAG_V2.read_bytes())
        blueprint_text = cron.BLUEPRINT.read_text(encoding="utf-8")
        for theorem_id in (PARENT, CHILD):
            for phase in cron.PHASE_NAMES:
                item_id = cron.task_id(theorem_id, phase)
                blueprint_text = re.sub(
                    rf"^- \[[_x ]\] (`{re.escape(item_id)}`)",
                    r"- [x] \1",
                    blueprint_text,
                    count=1,
                    flags=re.MULTILINE,
                )
        blueprint_text = refresh_blueprint_progress_summary(blueprint_text)
        status_blueprint.write_text(blueprint_text, encoding="utf-8")
        provider_source = status_root / "Stage1_Instances" / PARENT / "Proof.lean"
        consumer_source = status_root / "Stage1_Instances" / CHILD / "GeneralizedLindeberg.lean"
        provider_source.parent.mkdir(parents=True)
        consumer_source.parent.mkdir(parents=True)
        provider_source.write_bytes((source_root / provider_source.relative_to(status_root)).read_bytes())
        consumer_source.write_bytes((source_root / consumer_source.relative_to(status_root)).read_bytes())
        provider_receipt = status_root / "Stage1_Instances" / PARENT / "v2-fixture-proof-receipt.json"
        provider_receipt.write_bytes(self.parent_receipt.read_bytes())
        ledger_path = status_root / "Stage1_Instances" / CHILD / "dependency-reuse-ledger.json"

        status_ledger = copy.deepcopy(self.ledger)
        status_ledger["inspections"][0]["artifact_digests"] = {
            provider_source.relative_to(status_root).as_posix(): sha256(provider_source)
        }
        decision = status_ledger["reuse_decisions"][0]
        decision["provider_receipts"] = [{
            "path": provider_receipt.relative_to(status_root).as_posix(),
            "receipt_id": json.loads(provider_receipt.read_text(encoding="utf-8"))["receipt_id"],
            "sha256": sha256(provider_receipt),
        }]
        decision["provider_body_source"] = {
            "path": provider_source.relative_to(status_root).as_posix(),
            "sha256": sha256(provider_source),
        }
        decision["terminal_proof_body_id"] = (
            "Stage1Instances.THM_M_0989.integrable_truncatedSecondMoment_integrand"
        )
        decision["provider_statement_fingerprint"] = lean_declaration_fingerprint(
            provider_source, "integrable_truncatedSecondMoment_integrand"
        )
        decision["consumer_import_or_wrapper"] = (
            "Stage1Instances.THM_M_0990.secondMoment_le_sq_add_truncated"
        )
        decision["consumer_import_source"] = {
            "path": consumer_source.relative_to(status_root).as_posix(),
            "sha256": sha256(consumer_source),
        }
        decision["consumer_required_fingerprint"] = lean_declaration_fingerprint(
            consumer_source, "secondMoment_le_sq_add_truncated"
        )
        decision["decision"] = "reused_with_transport"
        decision["relationship"] = "checked_transport"
        status_ledger["inspections"][0]["compatibility"] = "checked_transport"
        decision.pop("consumer_validation_receipts", None)
        ledger_path.write_text(json.dumps(status_ledger, indent=2) + "\n", encoding="utf-8")

        with (
            mock.patch.object(cron, "ROOT", status_root),
            mock.patch.object(cron, "DAG", status_dag),
            mock.patch.object(cron, "BLUEPRINT", status_blueprint),
            mock.patch.object(cron, "THEOREM_DAG_V2", status_graph),
            mock.patch.object(cron, "audited_legacy_hard_edge_status", return_value=None),
            mock.patch.object(cron, "theorem_dag_v2", return_value=(real_graph, real_nodes)),
        ):
            self.assertEqual(cron.hard_edge_gate_status(CHILD, "proof"), ("satisfied", []))
            validation_status, validation_blockers = cron.hard_edge_gate_status(CHILD, "validation")
            self.assertEqual(validation_status, "blocked")
            self.assertTrue(validation_blockers)
            release_status, release_blockers = cron.hard_edge_gate_status(CHILD, "release")
            self.assertEqual(release_status, "blocked")
            self.assertTrue(release_blockers)

    def test_self_tested_consumer_receipt_satisfies_validation_handoff_gate(self) -> None:
        ledger = self.validate()
        self.consumer_receipt = self.write_receipt(CHILD, "validation", accepted=False)
        receipt = json.loads(self.consumer_receipt.read_text(encoding="utf-8"))
        receipt["verdict"] = "no_state_change"
        receipt["selftest_status"] = "passed"
        validator_argv = ["python3", f"Stage1_Instances/{CHILD}/check_validation.py"]
        receipt["selftest_result"] = {"exit_code": 0, "commands": [" ".join(validator_argv)]}
        validator = self.root / "Stage1_Instances" / CHILD / "check_validation.py"
        validator.write_text("raise SystemExit(0)\n", encoding="utf-8")
        recipe = self.root / "Stage1_Instances" / CHILD / "validation-phase-spec.json"
        recipe.write_text(
            json.dumps(
                {
                    "schema_version": "stage1-validation-recipe/1.0",
                    "item_id": cron.task_id(CHILD, "validation"),
                    "theorem_id": CHILD,
                    "cwd": ".",
                    "argv": validator_argv,
                    "expected_exit": 0,
                    "network_policy": "denied",
                    "timeout_seconds": 30,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        self.consumer_receipt.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
        self.decision()["consumer_validation_receipts"] = [self.reference(self.consumer_receipt)]
        self.write_ledger()
        ledger = self.validate()
        item = {"phase": "validation", "theorem_id": CHILD, "owned_paths": [f"Stage1_Instances/{CHILD}"]}
        with (
            mock.patch.object(
                cron,
                "require_head_tracked_file",
                side_effect=lambda root, relative: cron.safe_evidence_path(root, relative),
            ),
            mock.patch.object(cron, "require_authoritative_match"),
        ):
            self.assertEqual(
                cron.authoritative_validation_recipe(
                    theorem_id=CHILD,
                    evidence_root=self.root,
                    authoritative_root=self.root,
                    receipt_commands=receipt["selftest_result"]["commands"],
                )[0],
                validator_argv,
            )
            cron.enforce_master_hard_edge_gate(
                item,
                ledger,
                evidence_root=self.root,
                authoritative_root=self.root,
            )

    def test_consumer_receipt_commands_must_match_worker_packet(self) -> None:
        self.consumer_receipt = self.write_receipt(CHILD, "validation", accepted=False)
        receipt = json.loads(self.consumer_receipt.read_text(encoding="utf-8"))
        command = f"python3 Stage1_Instances/{CHILD}/check_validation.py"
        receipt["verdict"] = "no_state_change"
        receipt["selftest_status"] = "passed"
        receipt["selftest_result"] = {"exit_code": 0, "commands": [command]}
        self.consumer_receipt.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
        self.decision()["consumer_validation_receipts"] = [self.reference(self.consumer_receipt)]
        validator = self.root / "Stage1_Instances" / CHILD / "check_validation.py"
        validator.write_text("raise SystemExit(0)\n", encoding="utf-8")
        recipe = self.root / "Stage1_Instances" / CHILD / "validation-phase-spec.json"
        recipe.write_text(
            json.dumps(
                {
                    "schema_version": "stage1-validation-recipe/1.0",
                    "item_id": cron.task_id(CHILD, "validation"),
                    "theorem_id": CHILD,
                    "cwd": ".",
                    "argv": ["python3", f"Stage1_Instances/{CHILD}/check_validation.py"],
                    "expected_exit": 0,
                    "network_policy": "denied",
                    "timeout_seconds": 30,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        self.decision()["consumer_validation_receipts"] = [self.reference(self.consumer_receipt)]
        self.write_ledger()
        ledger = self.validate()
        item = {"phase": "validation", "theorem_id": CHILD, "owned_paths": [f"Stage1_Instances/{CHILD}"]}
        with (
            mock.patch.object(
                cron,
                "require_head_tracked_file",
                side_effect=lambda root, relative: cron.safe_evidence_path(root, relative),
            ),
            mock.patch.object(cron, "require_authoritative_match"),
        ):
            with self.assertRaisesRegex(ValueError, "worker packet"):
                cron.enforce_master_hard_edge_gate(
                    item,
                    ledger,
                    evidence_root=self.root,
                    authoritative_root=self.root,
                    expected_commands=[f"python3 Stage1_Instances/{CHILD}/other.py"],
                )

    def test_authoritative_validation_timeout_fails_closed(self) -> None:
        reference = self.reference(self.consumer_receipt)
        with (
            mock.patch.object(
                cron,
                "authoritative_validation_recipe",
                return_value=(["python3", f"Stage1_Instances/{CHILD}/check_validation.py"], 7),
            ),
            mock.patch.object(
                cron,
                "run",
                side_effect=subprocess.TimeoutExpired(["python3", "check_validation.py"], 7),
            ) as replay,
        ):
            with self.assertRaisesRegex(ValueError, "timed out after 7s"):
                cron.validate_consumer_validation_commands(
                    [reference],
                    evidence_root=self.root,
                    authoritative_root=self.root,
                    theorem_id=CHILD,
                )
        self.assertEqual(replay.call_args.kwargs["timeout"], 7)

    def test_worker_noop_validator_cannot_satisfy_authority_bound_gate(self) -> None:
        authoritative = self.root / "authoritative"
        worker = self.root / "worker"
        self.copy_authoritative_state(authoritative)
        shutil.copytree(self.root / "Stage1_Instances", authoritative / "Stage1_Instances")

        validator_relative = Path("Stage1_Instances") / CHILD / "check_validation.py"
        spec_relative = Path("Stage1_Instances") / CHILD / "validation-phase-spec.json"
        validator_argv = ["python3", validator_relative.as_posix()]
        authoritative_validator = authoritative / validator_relative
        authoritative_validator.write_text("raise SystemExit(23)\n", encoding="utf-8")
        (authoritative / spec_relative).write_text(
            json.dumps(
                {
                    "schema_version": "stage1-validation-recipe/1.0",
                    "recipe_id": "authority-bound-fixture",
                    "item_id": cron.task_id(CHILD, "validation"),
                    "theorem_id": CHILD,
                    "cwd": ".",
                    "argv": validator_argv,
                    "expected_exit": 0,
                    "network_policy": "denied",
                    "timeout_seconds": 30,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "init", "-q"], cwd=authoritative, check=True)
        subprocess.run(
            ["git", "add", validator_relative.as_posix(), spec_relative.as_posix()],
            cwd=authoritative,
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Stage1 Test",
                "-c",
                "user.email=stage1-test@example.invalid",
                "commit",
                "-q",
                "-m",
                "Bind authoritative validator fixture",
            ],
            cwd=authoritative,
            check=True,
        )
        shutil.copytree(authoritative / "Stage1_Instances", worker / "Stage1_Instances")

        # The worker keeps the committed recipe shape but replaces its checker
        # with a vacuous success.  A replay of worker-controlled bytes alone is
        # not validation authority.
        (worker / validator_relative).write_text("raise SystemExit(0)\n", encoding="utf-8")
        receipt_path = worker / "Stage1_Instances" / CHILD / "validation-receipt.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        command = " ".join(validator_argv)
        receipt.update(
            {
                "accepted": False,
                "support_state": "provisional_worker_selftest",
                "proposed_state": "[_]",
                "verdict": "no_state_change",
                "selftest_status": "passed",
                "selftest_result": {"exit_code": 0, "commands": [command]},
                "recipe": {"cwd": ".", "argv": validator_argv},
                "result": {"exit_code": 0},
            }
        )
        receipt_path.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")

        ledger = copy.deepcopy(self.ledger)
        hard_decision = next(row for row in ledger["reuse_decisions"] if row["source_id"] == EDGE)
        hard_decision["consumer_validation_receipts"] = [{
            "path": receipt_path.relative_to(worker).as_posix(),
            "receipt_id": receipt["receipt_id"],
            "sha256": sha256(receipt_path),
        }]
        ledger_path = worker / "Stage1_Instances" / CHILD / "dependency-reuse-ledger.json"
        ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
        validated = cron.validate_dependency_reuse_ledger(
            ledger_path,
            CHILD,
            evidence_root=worker,
            authoritative_root=authoritative,
        )
        item = {"phase": "validation", "theorem_id": CHILD, "owned_paths": [f"Stage1_Instances/{CHILD}"]}
        packet_commands = [
            f"python3 Stage1_Instances/{CHILD}/precheck.py",
            {"argv": validator_argv, "exit_code": 0},
        ]
        with self.assertRaisesRegex(
            ValueError,
            "dependency reuse provider evidence differs from the authoritative checkout",
        ):
            cron.enforce_master_hard_edge_gate(
                item,
                validated,
                evidence_root=worker,
                authoritative_root=authoritative,
                expected_commands=packet_commands,
            )

    def test_blocked_consumer_receipt_fails_validation_handoff_gate(self) -> None:
        self.consumer_receipt = self.write_receipt(CHILD, "validation", accepted=False)
        self.decision()["consumer_validation_receipts"] = [self.reference(self.consumer_receipt)]
        self.write_ledger()
        ledger = self.validate()
        item = {"phase": "validation", "theorem_id": CHILD, "owned_paths": [f"Stage1_Instances/{CHILD}"]}
        with self.assertRaisesRegex(ValueError, "hard-edge master gate failed"):
            cron.enforce_master_hard_edge_gate(item, ledger, evidence_root=self.root)

    def test_provisional_consumer_receipt_requires_normalized_pass_evidence(self) -> None:
        for mutation in (
            lambda receipt: receipt.pop("selftest_status"),
            lambda receipt: receipt["selftest_result"].update(exit_code=2),
            lambda receipt: receipt["selftest_result"].update(commands=[]),
        ):
            with self.subTest(mutation=mutation):
                self.consumer_receipt = self.write_receipt(CHILD, "validation", accepted=False)
                receipt = json.loads(self.consumer_receipt.read_text(encoding="utf-8"))
                receipt["selftest_status"] = "passed"
                receipt["selftest_result"] = {"exit_code": 0, "commands": ["validate-command"]}
                mutation(receipt)
                self.consumer_receipt.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
                self.decision()["consumer_validation_receipts"] = [self.reference(self.consumer_receipt)]
                self.write_ledger()
                ledger = self.validate()
                item = {"phase": "validation", "theorem_id": CHILD, "owned_paths": [f"Stage1_Instances/{CHILD}"]}
                with self.assertRaisesRegex(ValueError, "hard-edge master gate failed"):
                    cron.enforce_master_hard_edge_gate(item, ledger, evidence_root=self.root)
                self.ledger = self.make_ledger()

    def test_consumer_receipt_cannot_override_nonaccepted_phase_state(self) -> None:
        ledger = self.validate()
        dag = json.loads(self.dag_path.read_text(encoding="utf-8"))
        next(
            item for item in dag["items"]
            if item["theorem_id"] == CHILD and item["phase"] == "validation"
        )["state"] = "[_]"
        self.dag_path.write_text(json.dumps(dag) + "\n", encoding="utf-8")
        item = {"phase": "release", "theorem_id": CHILD, "owned_paths": [f"Stage1_Instances/{CHILD}"]}
        with self.assertRaisesRegex(ValueError, "hard-edge master gate failed"):
            cron.enforce_master_hard_edge_gate(item, ledger, evidence_root=self.root)


class IntegrationTransactionTests(unittest.TestCase):
    def setUp(self) -> None:
        cron.theorem_dag_v2.cache_clear()
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.sandbox = Path(self.temporary.name)
        self.master = self.sandbox / "master"
        self.workspace = self.sandbox / "worker"
        self.runtime = self.master / ".cron" / "stage1-v2-app-server"
        self.docs = self.master / "Docs"
        self.owner = "Stage1_Instances/THM-M-0001"
        self.existing_relative = f"{self.owner}/intake-record.json"
        self.new_relative = f"{self.owner}/worker-note.txt"
        (self.master / self.owner).mkdir(parents=True)
        (self.workspace / self.owner).mkdir(parents=True)
        self.master_existing = b'{"theorem_id":"THM-M-0001","value":"master"}\n'
        (self.master / self.existing_relative).write_bytes(self.master_existing)
        (self.workspace / self.existing_relative).write_text(
            '{"theorem_id":"THM-M-0001","value":"worker"}\n', encoding="utf-8"
        )
        (self.workspace / self.new_relative).write_text("THM-M-0001 worker evidence\n", encoding="utf-8")
        self.item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "phase": "intake",
            "state": "[ ]",
            "attempts": 0,
            "depends_on": [],
            "layer": 0,
            "execution_rank": 1,
            "owned_paths": [self.owner],
        }
        self.data = {"items": [self.item]}
        self.claim = {
            "item_id": self.item["id"],
            "theorem_id": self.item["theorem_id"],
            "owned_paths": self.item["owned_paths"],
            "workspace": str(self.workspace),
            "status": "finished",
            "base_revision": "test-revision",
            "slot": 1,
            "runtime_protocol": cron.RUNTIME_PROTOCOL,
            "output_log": str(self.runtime / "logs" / "test.out"),
            "fresh_revalidation": False,
        }
        (self.workspace / ".stage1-worker-selftest.json").write_text(
            json.dumps(
                {
                    "item_id": self.item["id"],
                    "state": "[_]",
                    "base_revision": "test-revision",
                    "changed_paths": [self.existing_relative, self.new_relative],
                    "commands": ["python3 target-selftest.py"],
                    "known_failures": [],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        self.docs.mkdir(parents=True)
        self.dag = self.docs / "Stage1_Execution_DAG_rev-5.6.json"
        self.theorem_dag = self.docs / "Stage1_Theorem_DAG_v2.json"
        self.blueprint = self.docs / "Stage1_Blueprint_v2.md"
        self.dag.write_text(json.dumps(self.data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.theorem_dag.write_text('{"projection":"original"}\n', encoding="utf-8")
        self.blueprint.write_text("original blueprint\n", encoding="utf-8")
        self.runtime.mkdir(parents=True)
        self.claims_path = self.runtime / "claims.json"
        self.queue_path = self.runtime / "integration_queue.json"
        self.claims_path.write_text(json.dumps({"claims": [self.claim]}, indent=2) + "\n", encoding="utf-8")
        self.queue_path.write_text('{"queued":["previous"]}\n', encoding="utf-8")
        self.original_surfaces = {
            path: path.read_bytes()
            for path in (
                self.dag,
                self.theorem_dag,
                self.blueprint,
                self.claims_path,
                self.queue_path,
                self.master / self.existing_relative,
            )
        }

    @staticmethod
    def _file_identity(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _assert_transaction_restored(self) -> None:
        for path, expected in self.original_surfaces.items():
            with self.subTest(path=path):
                self.assertEqual(path.read_bytes(), expected)
        self.assertFalse((self.master / self.new_relative).exists())
        self.assertFalse(any(self.master.rglob("*.tmp")))

    def _exercise_post_merge_failure(self, failure_point: str) -> None:
        original_existing_oid = self._file_identity(self.master / self.existing_relative)

        def fake_run(
            command: list[str],
            *,
            cwd: Path = self.master,
            check: bool = True,
            timeout: int | None = None,
        ):
            if command[:3] == ["git", "rev-parse", "HEAD"]:
                return subprocess.CompletedProcess(command, 0, "test-revision\n", "")
            if len(command) > 1 and command[1].endswith("generate_stage1_theorem_dag_v2.py"):
                self.theorem_dag.write_text('{"projection":"regenerated"}\n', encoding="utf-8")
            if (
                failure_point == "validator"
                and len(command) > 1
                and command[1].endswith("check_stage1_theorem_dag_v2.py")
            ):
                raise SystemExit("injected theorem DAG validator failure")
            return subprocess.CompletedProcess(command, 0, "", "")

        def write_projection_then_fail(data: dict[str, object]) -> None:
            self.blueprint.write_text("partially regenerated blueprint\n", encoding="utf-8")
            raise RuntimeError("injected projection failure")

        projection = write_projection_then_fail if failure_point == "projection" else mock.Mock()
        expected_exception = RuntimeError if failure_point == "projection" else SystemExit
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.object(cron, "ROOT", self.master))
            stack.enter_context(mock.patch.object(cron, "DOCS", self.docs))
            stack.enter_context(mock.patch.object(cron, "DAG", self.dag))
            stack.enter_context(mock.patch.object(cron, "THEOREM_DAG_V2", self.theorem_dag))
            stack.enter_context(mock.patch.object(cron, "BLUEPRINT", self.blueprint))
            stack.enter_context(mock.patch.object(cron, "RUNTIME", self.runtime))
            stack.enter_context(mock.patch.object(cron, "PAUSE_FILE", self.runtime / "test-PAUSED"))
            stack.enter_context(mock.patch.object(cron, "load_dag", return_value=(self.data, [self.item])))
            stack.enter_context(mock.patch.object(cron, "order_by_v2", side_effect=lambda items: items))
            stack.enter_context(mock.patch.object(cron, "validate_dag", side_effect=lambda data: data["items"]))
            stack.enter_context(
                mock.patch.object(
                    cron,
                    "worker_changed_paths",
                    return_value=[self.existing_relative, self.new_relative],
                )
            )
            stack.enter_context(mock.patch.object(cron, "reject_mutable_dependency_operations"))
            stack.enter_context(
                mock.patch.object(
                    cron,
                    "git_blob_oid",
                    side_effect=lambda workspace, relative: (
                        original_existing_oid if relative == self.existing_relative else None
                    ),
                )
            )
            stack.enter_context(mock.patch.object(cron, "file_oid", side_effect=self._file_identity))
            stack.enter_context(mock.patch.object(cron, "run", side_effect=fake_run))
            stack.enter_context(mock.patch.object(cron, "theorem_dag_v2", return_value=({}, {self.item["theorem_id"]: {"v2_execution_rank": 1}})))
            stack.enter_context(mock.patch.object(cron, "refresh_claims", return_value=[self.claim]))
            stack.enter_context(mock.patch.object(cron, "goal_runtime_is_verified", return_value=True))
            stack.enter_context(
                mock.patch.object(
                    cron,
                    "persist_worker_handoff",
                    return_value=(
                        self.runtime / "worker-handoffs" / "fixture.json",
                        "a" * 64,
                        123,
                    ),
                )
            )
            stack.enter_context(mock.patch.object(
                cron, "phase_validator_candidate_paths", return_value=set()
            ))
            stack.enter_context(mock.patch.object(cron, "write_projection", side_effect=projection))
            stack.enter_context(mock.patch.object(cron, "load_blueprint_items", return_value=[self.item]))
            stack.enter_context(mock.patch.object(cron, "write_todo", return_value=self.docs / "todos_test.md"))
            with self.assertRaises(expected_exception):
                cron.integrate(1)
        self._assert_transaction_restored()

    def test_post_merge_validator_failure_restores_all_integration_surfaces(self) -> None:
        self._exercise_post_merge_failure("validator")

    def test_projection_failure_restores_existing_new_and_generated_surfaces(self) -> None:
        self._exercise_post_merge_failure("projection")

    def test_second_path_conflict_does_not_leave_first_path_merged(self) -> None:
        first = f"{self.owner}/first.txt"
        second = f"{self.owner}/second.txt"
        first_original = b"first base\n"
        second_base = b"second base\n"
        (self.master / first).write_bytes(first_original)
        (self.master / second).write_bytes(b"second independently changed\n")
        (self.workspace / first).write_text("first worker\n", encoding="utf-8")
        (self.workspace / second).write_text("second worker\n", encoding="utf-8")
        base_oids = {
            first: hashlib.sha256(first_original).hexdigest(),
            second: hashlib.sha256(second_base).hexdigest(),
        }
        with (
            mock.patch.object(cron, "ROOT", self.master),
            mock.patch.object(cron, "git_blob_oid", side_effect=lambda workspace, relative: base_oids[relative]),
            mock.patch.object(cron, "file_oid", side_effect=self._file_identity),
        ):
            transaction = cron.FileTransaction()
            with self.assertRaisesRegex(ValueError, "master file changed"):
                try:
                    cron.merge_worker_changes(self.workspace, [first, second], transaction=transaction)
                except ValueError:
                    transaction.rollback()
                    raise
        self.assertEqual((self.master / first).read_bytes(), first_original)
        self.assertEqual((self.master / second).read_bytes(), b"second independently changed\n")

    def test_blocked_snapshot_rejects_traversal_and_symlink_sources(self) -> None:
        snapshot = self.runtime / "blocked-reports" / self.item["id"]
        owned_snapshot = snapshot / self.owner
        owned_snapshot.mkdir(parents=True)
        report = owned_snapshot / "blocked.md"
        report.write_text("THM-M-0001 blocked\n", encoding="utf-8")
        with (
            mock.patch.object(cron, "ROOT", self.master),
            mock.patch.object(cron, "RUNTIME", self.runtime),
        ):
            self.assertEqual(
                cron.validated_blocked_snapshot(self.item["id"], str(snapshot)),
                snapshot,
            )
            with self.assertRaisesRegex(ValueError, "ownership scope"):
                cron.validate_owned_relative_paths([f"{self.owner}/../../escape.md"], self.owner)
            receipt_path = cron.master_acceptance_receipt_path(
                "THM-M-0001", "intake", "a" * 64
            )
            with self.assertRaisesRegex(ValueError, "scheduler-reserved"):
                cron.validate_owned_relative_paths([receipt_path], self.owner)
            reserved_source = self.workspace / receipt_path
            reserved_source.parent.mkdir(parents=True, exist_ok=True)
            reserved_source.write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "scheduler-reserved"):
                cron.merge_worker_changes(
                    self.workspace, [receipt_path], owner=self.owner
                )
            outside = self.sandbox / "outside.md"
            outside.write_text("THM-M-0001 blocked\n", encoding="utf-8")
            link = owned_snapshot / "linked.md"
            link.symlink_to(outside)
            with self.assertRaisesRegex(ValueError, "regular file"):
                cron.contained_regular_file(snapshot, f"{self.owner}/linked.md", self.owner)
            with self.assertRaisesRegex(ValueError, "scheduler-owned"):
                cron.validated_blocked_snapshot(self.item["id"], str(self.sandbox))

    def test_blocked_only_batch_regenerates_v2_before_validation(self) -> None:
        source = inspect.getsource(cron._integrate)
        regeneration = source.index('run(["python3", "Docs/tools/generate_stage1_theorem_dag_v2.py"])')
        validation = source.index('run(["python3", "Docs/tools/check_stage1_theorem_dag_v2.py"])')
        self.assertLess(regeneration, validation)
        between = source[
            source.index("if accepted or preserved_blockers or master_accepted:"):validation
        ]
        self.assertNotIn('if accepted:\n            run(["python3", "Docs/tools/generate_stage1_theorem_dag_v2.py"])', between)

    def test_checkpoint_manifest_filters_paths_identical_to_head(self) -> None:
        source = inspect.getsource(cron._integrate)
        self.assertIn(
            "checkpoint_files = [path for path in checkpoint_files if path_differs_from_head(path)]",
            source,
        )

    def test_invalid_attempts_fail_before_worker_files_are_copied(self) -> None:
        data = copy.deepcopy(cron.read_json(cron.DAG))
        data["items"][0]["attempts"] = None
        with self.assertRaisesRegex(SystemExit, "invalid attempts"):
            cron.validate_dag(data)
        self.assertEqual((self.master / self.existing_relative).read_bytes(), self.master_existing)

    def test_phase_validator_guard_rejects_every_contract_candidate(self) -> None:
        candidates = [
            f"{self.owner}/check_intake.py",
            f"{self.owner}/validate_intake.py",
        ]
        contract = {
            "validator_candidates": [
                {
                    "path_pattern": candidate.replace(
                        self.item["theorem_id"], "{theorem_id}"
                    )
                }
                for candidate in candidates
            ]
        }
        with mock.patch.object(cron, "phase_contract", return_value=contract):
            self.assertEqual(
                cron.phase_validator_candidate_paths(self.item), set(candidates)
            )
            for candidate in candidates:
                with self.subTest(candidate=candidate), self.assertRaisesRegex(
                    ValueError, "scheduler-owned validator candidate"
                ):
                    cron.reject_worker_validator_changes(self.item, [candidate])

    def test_worker_changed_paths_rejects_deleted_protected_candidate(self) -> None:
        candidate = f"{self.owner}/check_intake.py"
        responses = iter(
            [
                subprocess.CompletedProcess([], 0, f"D\t{candidate}\n", ""),
                subprocess.CompletedProcess([], 0, "", ""),
                subprocess.CompletedProcess([], 0, "", ""),
            ]
        )
        with (
            mock.patch.object(cron, "run", side_effect=lambda *_args, **_kwargs: next(responses)),
            self.assertRaisesRegex(ValueError, "scheduler-owned validator candidate"),
        ):
            cron.worker_changed_paths(
                self.workspace, self.owner + "/", protected_paths={candidate}
            )

    def test_interrupted_integration_wal_restores_original_bytes(self) -> None:
        original = self.master / self.existing_relative
        created = self.master / self.new_relative
        with (
            mock.patch.object(cron, "ROOT", self.master),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(
                cron,
                "run",
                return_value=subprocess.CompletedProcess([], 0, "test-revision\n", ""),
            ),
        ):
            transaction = cron.FileTransaction(self.runtime / "integration_wal.json")
            transaction.snapshot(original)
            transaction.snapshot(created)
            original.write_text("interrupted mutation\n", encoding="utf-8")
            created.write_text("interrupted new file\n", encoding="utf-8")
            cron.recover_integration_wal()
        self.assertEqual(original.read_bytes(), self.master_existing)
        self.assertFalse(created.exists())
        self.assertFalse((self.runtime / "integration_wal.json").exists())

    def test_integration_wal_exists_before_first_authoritative_copy(self) -> None:
        observed = False
        destination = self.master / self.new_relative
        with (
            mock.patch.object(cron, "ROOT", self.master),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(
                cron,
                "run",
                return_value=subprocess.CompletedProcess([], 0, "test-revision\n", ""),
            ),
        ):
            transaction = cron.FileTransaction(self.runtime / "integration_wal.json")
            transaction.snapshot(destination)
            observed = (self.runtime / "integration_wal.json").is_file()
            destination.write_text("first mutation\n", encoding="utf-8")
            transaction.rollback()
        self.assertTrue(observed)
        self.assertFalse(destination.exists())

    def test_integration_wal_rejects_git_metadata_path(self) -> None:
        wal = self.runtime / "integration_wal.json"
        wal.write_text(
            json.dumps({
                "schema_version": "stage1-integration-wal/1.0",
                "state": "prepared",
                "base_revision": "test-revision",
                "files": [{"path": ".git/config", "kind": "missing", "mode": None}],
                "created_dirs": [],
            }) + "\n"
        )
        with (
            mock.patch.object(cron, "ROOT", self.master),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(
                cron,
                "run",
                return_value=subprocess.CompletedProcess([], 0, "test-revision\n", ""),
            ),
        ):
            with self.assertRaisesRegex(SystemExit, "unsafe path"):
                cron.recover_integration_wal()

    def test_integration_wal_removes_canonical_master_receipt_directories(self) -> None:
        root = self.sandbox / "receipt-recovery-master"
        runtime = root / ".cron" / "stage1-v2-app-server"
        runtime.mkdir(parents=True)
        instances_root = root / "Stage1_Instances"
        theorem_root = instances_root / "THM-M-0001"
        receipt_root = theorem_root / "master-acceptance"
        phase_directory = receipt_root / "intake"
        receipt = phase_directory / f"{'a' * 64}.json"
        phase_directory.mkdir(parents=True)
        receipt.write_text("interrupted receipt\n", encoding="utf-8")
        wal = runtime / "integration_wal.json"
        wal.write_text(
            json.dumps({
                "schema_version": "stage1-integration-wal/1.0",
                "state": "prepared",
                "base_revision": "test-revision",
                "files": [{
                    "path": receipt.relative_to(root).as_posix(),
                    "kind": "missing",
                    "mode": None,
                }],
                "created_dirs": [
                    "Stage1_Instances",
                    "Stage1_Instances/THM-M-0001",
                    "Stage1_Instances/THM-M-0001/master-acceptance",
                    "Stage1_Instances/THM-M-0001/master-acceptance/intake",
                ],
            }) + "\n",
            encoding="utf-8",
        )
        with (
            mock.patch.object(cron, "ROOT", root),
            mock.patch.object(cron, "RUNTIME", runtime),
            mock.patch.object(
                cron,
                "run",
                return_value=subprocess.CompletedProcess([], 0, "test-revision\n", ""),
            ),
        ):
            cron.recover_integration_wal()
        self.assertFalse(receipt.exists())
        self.assertFalse(phase_directory.exists())
        self.assertFalse(receipt_root.exists())
        self.assertFalse(theorem_root.exists())
        self.assertFalse(instances_root.exists())
        self.assertFalse(wal.exists())

    def test_integration_wal_rejects_noncanonical_master_receipt_directory(self) -> None:
        wal = self.runtime / "integration_wal.json"
        wal.write_text(
            json.dumps({
                "schema_version": "stage1-integration-wal/1.0",
                "state": "prepared",
                "base_revision": "test-revision",
                "files": [],
                "created_dirs": [
                    "Stage1_Instances/THM-M-0001/master-acceptance/not-a-phase",
                ],
            }) + "\n",
            encoding="utf-8",
        )
        with (
            mock.patch.object(cron, "ROOT", self.master),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(
                cron,
                "run",
                return_value=subprocess.CompletedProcess([], 0, "test-revision\n", ""),
            ),
            self.assertRaisesRegex(SystemExit, "unsafe path"),
        ):
            cron.recover_integration_wal()
        self.assertTrue(wal.exists())

    def test_integration_wal_rejects_noncanonical_instance_and_receipt_files(self) -> None:
        unsafe_paths = (
            "Stage1_Instances/THM-M-evil/note.json",
            "Stage1_Instances/THM-M-0001/master-acceptance/intake/not-a-digest.json",
            f"Stage1_Instances/THM-M-0001/master-acceptance/not-a-phase/{'a' * 64}.json",
        )
        for relative in unsafe_paths:
            with self.subTest(relative=relative):
                wal = self.runtime / "integration_wal.json"
                wal.write_text(
                    json.dumps({
                        "schema_version": "stage1-integration-wal/1.0",
                        "state": "prepared",
                        "base_revision": "test-revision",
                        "files": [{"path": relative, "kind": "missing", "mode": None}],
                        "created_dirs": [],
                    }) + "\n",
                    encoding="utf-8",
                )
                with (
                    mock.patch.object(cron, "ROOT", self.master),
                    mock.patch.object(cron, "RUNTIME", self.runtime),
                    mock.patch.object(
                        cron,
                        "run",
                        return_value=subprocess.CompletedProcess([], 0, "test-revision\n", ""),
                    ),
                    self.assertRaisesRegex(SystemExit, "unsafe path"),
                ):
                    cron.recover_integration_wal()
                self.assertTrue(wal.exists())
                wal.unlink()

    def test_integration_wal_restores_pending_and_prior_day_todo(self) -> None:
        pending = self.runtime / "pending_checkpoint.json"
        prior_todo = self.docs / "todos_20260715.md"
        pending.write_text("pending before interruption\n")
        prior_todo.write_text("prior todo before interruption\n")
        with (
            mock.patch.object(cron, "ROOT", self.master),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(
                cron,
                "run",
                return_value=subprocess.CompletedProcess([], 0, "test-revision\n", ""),
            ),
        ):
            transaction = cron.FileTransaction(self.runtime / "integration_wal.json")
            transaction.snapshot(pending)
            transaction.snapshot(prior_todo)
            pending.write_text("interrupted pending\n")
            prior_todo.write_text("interrupted todo\n")
            cron.recover_integration_wal()
        self.assertEqual(pending.read_text(), "pending before interruption\n")
        self.assertEqual(prior_todo.read_text(), "prior todo before interruption\n")

    def test_transaction_commit_durably_removes_wal(self) -> None:
        wal = self.runtime / "integration_wal.json"
        with (
            mock.patch.object(cron, "ROOT", self.master),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(
                cron,
                "run",
                return_value=subprocess.CompletedProcess([], 0, "test-revision\n", ""),
            ),
            mock.patch("os.fsync", wraps=os.fsync) as fsync,
        ):
            transaction = cron.FileTransaction(wal)
            transaction.snapshot(self.master / self.existing_relative)
            calls_before_commit = fsync.call_count
            transaction.commit()
        self.assertFalse(wal.exists())
        self.assertGreater(fsync.call_count, calls_before_commit)

    def test_rollback_does_not_follow_predictable_temp_symlink(self) -> None:
        target = self.master / self.existing_relative
        outside = self.sandbox / "outside.txt"
        outside.write_text("outside stays intact\n")
        predictable = target.with_name(target.name + ".stage1-rollback.tmp")
        predictable.symlink_to(outside)
        with (
            mock.patch.object(cron, "ROOT", self.master),
            mock.patch.object(
                cron,
                "run",
                return_value=subprocess.CompletedProcess([], 0, "test-revision\n", ""),
            ),
        ):
            transaction = cron.FileTransaction()
            transaction.snapshot(target)
            target.write_text("mutated\n")
            transaction.rollback()
        self.assertEqual(target.read_bytes(), self.master_existing)
        self.assertEqual(outside.read_text(), "outside stays intact\n")
        self.assertTrue(predictable.is_symlink())

    def test_child_transaction_persists_parent_wal_before_copy(self) -> None:
        destination = self.master / self.new_relative
        with (
            mock.patch.object(cron, "ROOT", self.master),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(
                cron,
                "run",
                return_value=subprocess.CompletedProcess([], 0, "test-revision\n", ""),
            ),
        ):
            parent = cron.FileTransaction(self.runtime / "integration_wal.json")
            child = cron.FileTransaction(wal_parent=parent)
            child.snapshot(destination)
            wal = json.loads((self.runtime / "integration_wal.json").read_text())
            self.assertEqual(wal["files"][0]["path"], self.new_relative)
            destination.write_text("interrupted child copy\n")
            cron.recover_integration_wal()
        self.assertFalse(destination.exists())


class SchedulerCapacityTests(unittest.TestCase):
    def setUp(self) -> None:
        # Focused refresh tests commonly replace only the claim ledger. Give
        # them an empty synthetic /proc tree so a live scheduler cohort on the
        # host cannot be mistaken for unledgered fixture processes. Tests of
        # process reconciliation below replace this root with their own fully
        # described synthetic inventory.
        self.process_inventory = tempfile.TemporaryDirectory()
        self.addCleanup(self.process_inventory.cleanup)
        proc_root = Path(self.process_inventory.name) / "proc"
        proc_root.mkdir()
        proc_patch = mock.patch.object(cron, "PROC_ROOT", proc_root)
        proc_patch.start()
        self.addCleanup(proc_patch.stop)

    @staticmethod
    def canonical_claim(item: dict[str, object], status: str) -> dict[str, object]:
        _, theorem_nodes = cron.theorem_dag_v2()
        slot = 1
        claim_id = "20260716T120000Z-0123456789ab"
        worker_id = f"stage1app-{slot}-{theorem_nodes[str(item['theorem_id'])]['v2_execution_rank']:04d}-{claim_id[-12:]}"
        objective = cron.worker_goal_objective(item)
        return {
            "item_id": item["id"],
            "theorem_id": item["theorem_id"],
            "owned_paths": item["owned_paths"],
            "status": status,
            "slot": slot,
            "claim_id": claim_id,
            "worker_id": worker_id,
            "workspace": str(cron.RUNTIME / "workers" / f"slot{slot}"),
            "output_log": str(cron.RUNTIME / "logs" / f"{claim_id}.out"),
            "app_server_status": str(cron.RUNTIME / "app-server" / f"{claim_id}.json"),
            "goal_objective_path": str(cron.RUNTIME / "goals" / f"{claim_id}.txt"),
            "goal_objective": objective,
            "runtime_protocol": cron.RUNTIME_PROTOCOL,
            "runtime_config": {
                "model": cron.CODEX_MODEL,
                "reasoning_effort": cron.CODEX_REASONING_EFFORT,
                "service_tier": cron.CODEX_SERVICE_TIER,
            },
            "pid": 4242,
            "pid_start_ticks": 12345,
        }

    def run_refill_fixture(
        self,
        live_count: int,
        *,
        launch_failure_at: int | None = None,
        pause_before_launch_at: int | None = None,
    ) -> tuple[list[dict[str, object]], list[str], list[dict[str, object]]]:
        items: list[dict[str, object]] = []
        nodes: dict[str, dict[str, object]] = {}
        for index in range(1, 51):
            theorem_id = f"THM-M-{index:04d}"
            items.append({
                "id": f"S56-M-{index:04d}-INTAKE",
                "theorem_id": theorem_id,
                "phase": "intake",
                "layer": 0,
                "state": "[ ]",
                "attempts": 0,
                "depends_on": [],
                "owned_paths": [f"Stage1_Instances/{theorem_id}"],
            })
            nodes[theorem_id] = {
                "v2_execution_rank": index,
                "dependency_context_sha256": f"{index:064x}"[-64:],
            }
        existing: list[dict[str, object]] = []
        for index in range(live_count):
            item = items[index]
            claim_id = f"20260716T12{index:04d}Z-{index:012x}"
            objective = cron.worker_goal_objective(item)
            claim = {
                "item_id": item["id"],
                "theorem_id": item["theorem_id"],
                "owned_paths": item["owned_paths"],
                "status": "live",
                "claim_id": claim_id,
                "goal_objective": objective,
                "runtime_protocol": cron.RUNTIME_PROTOCOL,
            }
            claim["slot"] = index + 1
            claim["workspace"] = str(cron.RUNTIME / "workers" / f"slot{index + 1}")
            claim["worker_id"] = (
                f"stage1app-{index + 1}-{index + 1:04d}-{str(claim['claim_id'])[-12:]}"
            )
            existing.append(claim)
        events: list[str] = []
        saved: list[list[dict[str, object]]] = []
        launch_calls = 0
        pause = Path(tempfile.gettempdir()) / f"stage1-test-pause-{os.getpid()}"
        pause.unlink(missing_ok=True)

        def save(claims: list[dict[str, object]]) -> None:
            events.append("save")
            saved.append(copy.deepcopy(claims))

        def prepare(_slot: int) -> Path:
            nonlocal launch_calls
            events.append("prepare")
            if pause_before_launch_at is not None and launch_calls == pause_before_launch_at:
                pause.write_text("paused\n", encoding="utf-8")
            return Path("/unused")

        def launch_worker(
            _argv: list[str], *, delay_seconds: float = 0.0
        ) -> int:
            nonlocal launch_calls
            launch_calls += 1
            events.append(f"delay:{delay_seconds}")
            events.append("popen")
            if launch_failure_at == launch_calls:
                raise OSError("injected launch failure")
            return 10_000 + launch_calls

        def confirm(_claims: list[dict[str, object]], cohort: list[dict[str, object]]) -> int:
            events.append("handshake")
            for claim in cohort:
                claim["status"] = "live"
            save(_claims)
            return len(cohort)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / ".cron" / "stage1-v2-app-server"
            pause = root / "PAUSED"
            todo = root / "Docs" / "todo.md"
            todo.parent.mkdir(parents=True)
            with contextlib.ExitStack() as stack:
                for name, value in {
                    "ROOT": root,
                    "RUNTIME": runtime,
                    "PAUSE_FILE": pause,
                }.items():
                    stack.enter_context(mock.patch.object(cron, name, value))
                for name, kwargs in (
                    ("load_dag", {"return_value": ({"items": items}, items)}),
                    ("refresh_claims", {"return_value": existing}),
                    ("space_guard", {}),
                    ("reconcile_process_inventory", {"return_value": False}),
                    ("app_server_worker_is_live", {"side_effect": lambda claim: claim in existing}),
                    ("app_server_child_is_live", {"return_value": False}),
                    ("refill_reviews", {"return_value": 0}),
                    ("theorem_dag_v2", {"return_value": ({}, nodes)}),
                    ("graph_sha256", {"return_value": "a" * 64}),
                    ("run", {"return_value": subprocess.CompletedProcess([], 0, "b" * 40 + "\n", "")}),
                    ("save_claims", {"side_effect": save}),
                    ("prepare_workspace", {"side_effect": prepare}),
                    ("task_prompt", {"return_value": "prompt\n"}),
                    ("launch_app_server_worker", {"side_effect": launch_worker}),
                    ("process_start_ticks", {"return_value": 77}),
                    ("confirm_goal_handshakes", {"side_effect": confirm}),
                    ("write_todo", {"return_value": todo}),
                ):
                    stack.enter_context(mock.patch.object(cron, name, **kwargs))
                stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
                cron.refill_workers(cron.MAX_WORKERS)
        return (saved[-1] if saved else existing), events, saved

    def test_finished_handoffs_do_not_consume_live_capacity(self) -> None:
        live = [{"status": "live", "slot": slot} for slot in range(1, 11)]
        finished = [{"status": "finished", "slot": slot} for slot in range(11, 21)]
        claims = live + finished
        reservations = [claim for claim in claims if claim["status"] in {"live", "finished"}]
        occupied = {claim["slot"] for claim in reservations}
        capacity = max(0, cron.MAX_WORKERS - len(live))
        available = [
            slot
            for slot in range(1, cron.MAX_SLOT_ID + 1)
            if slot not in occupied
        ][:capacity]
        self.assertEqual(capacity, 40)
        self.assertEqual(available, list(range(21, 61)))

    def test_zero_live_refill_persists_fifty_reservations_before_any_launch(self) -> None:
        claims, events, saved = self.run_refill_fixture(0)
        new_claims = [claim for claim in claims if claim.get("status") == "live"]
        self.assertEqual(len(new_claims), 50)
        self.assertEqual(len({claim["claim_id"] for claim in new_claims}), 50)
        self.assertEqual(len({claim["slot"] for claim in new_claims}), 50)
        self.assertLess(events.index("save"), events.index("prepare"))
        self.assertLess(events.index("save"), events.index("popen"))
        first_save = saved[0]
        self.assertEqual(len(first_save), 50)
        self.assertTrue(all(claim["status"] == "preparing" for claim in first_save))
        self.assertEqual(events.count("delay:0.0"), 1)
        self.assertEqual(
            events.count(f"delay:{cron.APP_SERVER_LAUNCH_STAGGER_SECONDS}"), 49
        )

    def test_forty_eight_live_refill_launches_exactly_two(self) -> None:
        claims, events, saved = self.run_refill_fixture(48)
        self.assertEqual(events.count("popen"), 2)
        self.assertEqual(sum(claim.get("status") == "live" for claim in claims), 50)
        first_save = saved[0]
        self.assertEqual(sum(claim.get("status") == "preparing" for claim in first_save), 2)

    def test_live_preparing_processes_consume_the_fifty_lease_cap(self) -> None:
        items: list[dict[str, object]] = []
        nodes: dict[str, dict[str, object]] = {}
        claims: list[dict[str, object]] = []
        for index in range(1, 53):
            theorem_id = f"THM-M-{index:04d}"
            item = {
                "id": f"S56-M-{index:04d}-INTAKE",
                "theorem_id": theorem_id,
                "phase": "intake",
                "layer": 0,
                "state": "[ ]",
                "attempts": 0,
                "depends_on": [],
                "owned_paths": [f"Stage1_Instances/{theorem_id}"],
            }
            items.append(item)
            nodes[theorem_id] = {"v2_execution_rank": index}
            if index <= 50:
                claim_id = f"20260716T120000Z-{index:012x}"
                claim = {
                    "item_id": item["id"],
                    "theorem_id": theorem_id,
                    "owned_paths": item["owned_paths"],
                    "status": "live" if index <= 48 else "preparing",
                    "slot": index,
                    "claim_id": claim_id,
                    "worker_id": f"stage1app-{index}-{index:04d}-{claim_id[-12:]}",
                    "workspace": str(cron.RUNTIME / "workers" / f"slot{index}"),
                    "runtime_protocol": cron.RUNTIME_PROTOCOL,
                }
                claims.append(claim)
        with tempfile.TemporaryDirectory() as directory:
            todo = Path(directory) / "todo.md"
            with (
                mock.patch.object(cron, "PAUSE_FILE", Path(directory) / "PAUSED"),
                mock.patch.object(cron, "load_dag", return_value=({"items": items}, items)),
                mock.patch.object(cron, "refresh_claims", return_value=claims),
                mock.patch.object(cron, "space_guard"),
                mock.patch.object(cron, "reconcile_process_inventory", return_value=False),
                mock.patch.object(
                    cron,
                    "app_server_worker_is_live",
                    side_effect=lambda claim: claim.get("status") in {"live", "preparing"},
                ),
                mock.patch.object(cron, "app_server_child_is_live", return_value=False),
                mock.patch.object(cron, "write_todo", return_value=todo),
                mock.patch.object(cron, "prepare_workspace") as prepare,
                mock.patch.object(cron, "launch_app_server_worker") as launch_worker,
                contextlib.redirect_stdout(io.StringIO()),
            ):
                launched = cron.refill_workers(cron.MAX_WORKERS)
        self.assertEqual(launched, 0)
        prepare.assert_not_called()
        launch_worker.assert_not_called()

    def test_launch_failure_does_not_block_remaining_cohort_or_exceed_cap(self) -> None:
        claims, events, _ = self.run_refill_fixture(48, launch_failure_at=1)
        self.assertEqual(events.count("popen"), 2)
        self.assertEqual(sum(claim.get("status") == "live" for claim in claims), 49)
        self.assertEqual(sum(claim.get("status") == "launch_failed" for claim in claims), 1)
        self.assertLessEqual(sum(claim.get("status") in {"live", "preparing"} for claim in claims), 50)

    def test_pause_between_prepare_and_popen_cancels_all_unstarted_reservations(self) -> None:
        claims, events, _ = self.run_refill_fixture(0, pause_before_launch_at=0)
        self.assertEqual(events.count("popen"), 0)
        self.assertEqual(sum(claim.get("status") == "cancelled" for claim in claims), 50)
        self.assertEqual(sum(claim.get("status") in {"live", "preparing"} for claim in claims), 0)

    def test_worker_cap_above_fifty_fails_before_refill_side_effects(self) -> None:
        with (
            mock.patch.object(cron, "recover_integration_wal") as recover,
            mock.patch.object(cron, "refill_workers") as refill,
            self.assertRaisesRegex(SystemExit, "0..50"),
        ):
            cron.launch(51)
        recover.assert_not_called()
        refill.assert_not_called()

    def test_tick_integration_limit_is_validated_before_side_effects(self) -> None:
        with (
            mock.patch.object(cron, "recover_integration_wal") as recover,
            mock.patch.object(cron, "refill_workers") as refill,
            self.assertRaisesRegex(SystemExit, "--limit must be"),
        ):
            cron.launch(50, cron.MAX_INTEGRATION_LIMIT + 1)
        recover.assert_not_called()
        refill.assert_not_called()

    def test_tick_refills_before_heavy_integration(self) -> None:
        events: list[str] = []
        with tempfile.TemporaryDirectory() as directory:
            runtime = Path(directory) / "runtime"
            with (
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(cron, "PAUSE_FILE", Path(directory) / "PAUSED"),
                mock.patch.object(cron, "recover_integration_wal", side_effect=lambda: events.append("recover")),
                mock.patch.object(cron, "sync_guard", side_effect=lambda: events.append("sync")),
                mock.patch.object(
                    cron, "stable_refill",
                    side_effect=lambda _count, **kwargs: events.append(
                        f"refill:{kwargs['phase']}"
                    ) or 0,
                ),
                mock.patch.object(cron, "integrate", side_effect=lambda _count: events.append("integrate") or 0) as integrate,
            ):
                cron.launch(20, 73)
        self.assertEqual(
            events,
            ["recover", "sync", "refill:pre-integration", "integrate", "refill:tail"],
        )
        integrate.assert_called_once_with(73)

    def test_pending_checkpoint_is_committed_before_worker_refill(self) -> None:
        events: list[str] = []
        with tempfile.TemporaryDirectory() as directory:
            runtime = Path(directory) / "runtime"
            runtime.mkdir()
            (runtime / "pending_checkpoint.json").write_text("{}\n", encoding="utf-8")
            with (
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(cron, "PAUSE_FILE", Path(directory) / "PAUSED"),
                mock.patch.object(cron, "recover_integration_wal", side_effect=lambda: events.append("recover")),
                mock.patch.object(cron, "checkpoint_sync_guard", side_effect=lambda: events.append("checkpoint_sync")),
                mock.patch.object(cron, "checkpoint_integration", side_effect=lambda: (events.append("checkpoint"), (runtime / "pending_checkpoint.json").unlink())),
                mock.patch.object(
                    cron, "stable_refill",
                    side_effect=lambda _count, **kwargs: events.append(
                        f"refill:{kwargs['phase']}"
                    ) or 0,
                ),
                mock.patch.object(cron, "integrate", side_effect=lambda _count: events.append("integrate") or 0) as integrate,
            ):
                cron.launch(20, 47)
        self.assertEqual(
            events,
            [
                "recover", "checkpoint_sync", "checkpoint",
                "refill:pre-integration", "integrate", "refill:tail",
            ],
        )
        integrate.assert_called_once_with(47)

    def test_stable_refill_reaudits_and_retries_only_to_cap(self) -> None:
        # Each tuple is (pre-refill audit, post-refill audit).  A launch that
        # exits immediately leaves a real vacancy for the next bounded round.
        audits = iter([47, 49, 48, 50])
        with (
            mock.patch.object(cron, "audited_active_worker_count", side_effect=audits) as audit,
            mock.patch.object(cron, "refill_workers", side_effect=[2, 2]) as refill,
            mock.patch.object(cron, "execution_is_paused", return_value=False),
            mock.patch.object(cron.time, "sleep") as sleep,
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            active = cron.stable_refill(
                50, phase="pre-integration", max_rounds=3, deadline_seconds=180,
            )
        self.assertEqual(active, 50)
        self.assertEqual(audit.call_count, 4)
        self.assertEqual(refill.call_count, 2)
        sleep.assert_called_once_with(cron.REFILL_RETRY_SETTLE_SECONDS)
        self.assertIn("active=50/50, stop=cap_reached", output.getvalue())

    def test_stable_refill_downscale_does_not_refill_or_stop_workers(self) -> None:
        with (
            mock.patch.object(cron, "audited_active_worker_count", return_value=20),
            mock.patch.object(cron, "refill_workers") as refill,
            mock.patch.object(cron, "execution_is_paused", return_value=False),
            mock.patch.object(cron, "terminate_app_server_worker") as terminate,
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            active = cron.stable_refill(
                1, phase="tail", max_rounds=1, deadline_seconds=60,
            )
        self.assertEqual(active, 20)
        refill.assert_not_called()
        terminate.assert_not_called()
        self.assertIn("active=20/1, stop=downscale_draining", output.getvalue())

    def test_stable_refill_deadline_prevents_busy_loop(self) -> None:
        monotonic = iter([0.0, 0.0, 181.0])
        with (
            mock.patch.object(cron.time, "monotonic", side_effect=monotonic),
            mock.patch.object(cron, "audited_active_worker_count", side_effect=[10, 11]),
            mock.patch.object(cron, "refill_workers", return_value=1) as refill,
            mock.patch.object(cron, "execution_is_paused", return_value=False),
            mock.patch.object(cron.time, "sleep") as sleep,
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            active = cron.stable_refill(
                50, phase="pre-integration", max_rounds=3, deadline_seconds=180,
            )
        self.assertEqual(active, 11)
        refill.assert_called_once_with(50)
        sleep.assert_not_called()
        self.assertIn("stop=deadline", output.getvalue())

    def test_paused_after_integration_skips_tail_refill(self) -> None:
        events: list[str] = []
        pause_states = iter([False, False, True])
        with tempfile.TemporaryDirectory() as directory:
            with (
                mock.patch.object(cron, "RUNTIME", Path(directory) / "runtime"),
                mock.patch.object(cron, "execution_is_paused", side_effect=pause_states),
                mock.patch.object(cron, "recover_integration_wal"),
                mock.patch.object(cron, "sync_guard"),
                mock.patch.object(
                    cron, "stable_refill",
                    side_effect=lambda _count, **kwargs: events.append(kwargs["phase"]) or 0,
                ),
                mock.patch.object(cron, "integrate", return_value=0),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                cron.launch(20, 20)
        self.assertEqual(events, ["pre-integration"])

    def test_claim_order_key_is_rank_then_phase_layer_then_item_id(self) -> None:
        nodes = {
            "THM-M-0001": {"v2_execution_rank": 2},
            "THM-M-0002": {"v2_execution_rank": 1},
        }
        items = [
            {"theorem_id": "THM-M-0001", "layer": 0, "id": "S56-M-0001-INTAKE"},
            {"theorem_id": "THM-M-0002", "layer": 2, "id": "S56-M-0002-Z"},
            {"theorem_id": "THM-M-0002", "layer": 1, "id": "S56-M-0002-B"},
            {"theorem_id": "THM-M-0002", "layer": 1, "id": "S56-M-0002-A"},
        ]
        ordered = sorted(items, key=lambda item: cron.claim_order_key(item, nodes))
        self.assertEqual(
            [item["id"] for item in ordered],
            ["S56-M-0002-A", "S56-M-0002-B", "S56-M-0002-Z", "S56-M-0001-INTAKE"],
        )

    def test_unified_queue_capacity_one_never_prefers_later_review(self) -> None:
        implementation = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "layer": 0,
        }
        review = {
            "id": "S56-M-0100-INTAKE", "theorem_id": "THM-M-0100",
            "phase": "intake", "layer": 0,
        }
        nodes = {
            implementation["theorem_id"]: {"v2_execution_rank": 1},
            review["theorem_id"]: {"v2_execution_rank": 100},
        }
        with (
            mock.patch.object(cron, "implementation_candidates", return_value=[implementation]),
            mock.patch.object(cron, "review_candidates", return_value=[review]),
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, nodes)),
        ):
            selected = cron.unified_lane_candidates([], [])[:1]
        self.assertEqual(
            [(row["lane"], row["item"]["id"]) for row in selected],
            [(cron.IMPLEMENTATION_LANE, implementation["id"])],
        )

    def test_unified_queue_capacity_two_interleaves_lanes_by_exact_key(self) -> None:
        review = {
            "id": "S56-M-0001-STATEMENT", "theorem_id": "THM-M-0001",
            "phase": "statement", "layer": 1,
        }
        early_implementation = {
            "id": "S56-M-0002-INTAKE", "theorem_id": "THM-M-0002",
            "phase": "intake", "layer": 0,
        }
        late_implementation = {
            "id": "S56-M-0003-INTAKE", "theorem_id": "THM-M-0003",
            "phase": "intake", "layer": 0,
        }
        nodes = {
            review["theorem_id"]: {"v2_execution_rank": 1},
            early_implementation["theorem_id"]: {"v2_execution_rank": 2},
            late_implementation["theorem_id"]: {"v2_execution_rank": 3},
        }
        with (
            mock.patch.object(
                cron, "implementation_candidates",
                return_value=[late_implementation, early_implementation],
            ),
            mock.patch.object(cron, "review_candidates", return_value=[review]),
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, nodes)),
        ):
            selected = cron.unified_lane_candidates([], [])[:2]
        self.assertEqual(
            [(row["lane"], row["item"]["id"]) for row in selected],
            [
                (cron.REVIEW_LANE, review["id"]),
                (cron.IMPLEMENTATION_LANE, early_implementation["id"]),
            ],
        )

    def test_unified_queue_does_not_prioritize_revalidation_over_exact_key(self) -> None:
        review = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "layer": 0,
        }
        ordinary = {
            "id": "S56-M-0002-INTAKE", "theorem_id": "THM-M-0002",
            "phase": "intake", "layer": 0,
        }
        required = {
            "id": "S56-M-0300-INTAKE", "theorem_id": "THM-M-0300",
            "phase": "intake", "layer": 0,
        }
        nodes = {
            review["theorem_id"]: {"v2_execution_rank": 1},
            ordinary["theorem_id"]: {"v2_execution_rank": 2},
            required["theorem_id"]: {"v2_execution_rank": 300},
        }
        required_claim = {
            "item_id": required["id"],
            "lane": cron.IMPLEMENTATION_LANE,
            "status": "revalidation_required",
            "runtime_protocol": cron.RUNTIME_PROTOCOL,
        }
        with (
            mock.patch.object(
                cron, "implementation_candidates",
                return_value=[required, ordinary],
            ),
            mock.patch.object(cron, "review_candidates", return_value=[review]),
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, nodes)),
        ):
            selected = cron.unified_lane_candidates([], [required_claim])
        self.assertEqual(
            [row["item"]["id"] for row in selected],
            [review["id"], ordinary["id"], required["id"]],
        )

    def test_unified_queue_rejects_same_item_on_both_lanes(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "layer": 0,
        }
        with (
            mock.patch.object(cron, "implementation_candidates", return_value=[item]),
            mock.patch.object(cron, "review_candidates", return_value=[item]),
            self.assertRaisesRegex(SystemExit, "simultaneously eligible"),
        ):
            cron.unified_lane_candidates([], [])

    def test_refill_uses_contract_claim_order_for_actual_reservations(self) -> None:
        items = [
            {
                "id": "S56-M-0001-INTAKE",
                "theorem_id": "THM-M-0001",
                "phase": "intake",
                "layer": 0,
                "state": "[ ]",
                "attempts": 0,
                "depends_on": [],
                "owned_paths": ["Stage1_Instances/THM-M-0001"],
            },
            {
                "id": "S56-M-0002-STATEMENT",
                "theorem_id": "THM-M-0002",
                "phase": "statement",
                "layer": 1,
                "state": "[ ]",
                "attempts": 0,
                "depends_on": ["S56-M-0002-INTAKE"],
                "owned_paths": ["Stage1_Instances/THM-M-0002"],
            },
            {
                "id": "S56-M-0002-INTAKE",
                "theorem_id": "THM-M-0002",
                "phase": "intake",
                "layer": 0,
                "state": "[_]",
                "attempts": 1,
                "depends_on": [],
                "owned_paths": ["Stage1_Instances/THM-M-0002"],
            },
        ]
        nodes = {
            "THM-M-0001": {"v2_execution_rank": 2, "dependency_context_sha256": "1" * 64},
            "THM-M-0002": {"v2_execution_rank": 1, "dependency_context_sha256": "2" * 64},
        }
        saved: list[list[dict[str, object]]] = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / ".cron" / "stage1-v2-app-server"
            todo = root / "Docs" / "todo.md"
            todo.parent.mkdir(parents=True)
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(cron, "PAUSE_FILE", root / "PAUSED"),
                mock.patch.object(cron, "load_dag", return_value=({"items": items}, items)),
                mock.patch.object(cron, "refresh_claims", return_value=[]),
                mock.patch.object(cron, "space_guard"),
                mock.patch.object(cron, "reconcile_process_inventory", return_value=False),
                mock.patch.object(cron, "review_candidates", return_value=[]),
                mock.patch.object(cron, "refill_reviews", return_value=0),
                mock.patch.object(cron, "theorem_dag_v2", return_value=({}, nodes)),
                mock.patch.object(cron, "graph_sha256", return_value="a" * 64),
                mock.patch.object(
                    cron,
                    "run",
                    return_value=subprocess.CompletedProcess([], 0, "b" * 40 + "\n", ""),
                ),
                mock.patch.object(
                    cron,
                    "save_claims",
                    side_effect=lambda claims: saved.append(copy.deepcopy(claims)),
                ),
                mock.patch.object(cron, "prepare_workspace", side_effect=RuntimeError("stop after reservations")),
                mock.patch.object(cron, "confirm_goal_handshakes", return_value=0),
                mock.patch.object(cron, "write_todo", return_value=todo),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                cron.refill_workers(2)
        reservations = next(rows for rows in saved if len(rows) == 2)
        self.assertEqual(
            [claim["item_id"] for claim in reservations],
            ["S56-M-0002-STATEMENT", "S56-M-0001-INTAKE"],
        )

    def test_task_prompt_exposes_complete_ranked_parent_closure_and_reuse_boundary(self) -> None:
        theorem_id = "THM-M-0004"
        item = {
            "id": "S56-M-0004-PROOF",
            "theorem_id": theorem_id,
            "phase": "proof",
            "layer": 4,
            "state": "[ ]",
            "depends_on": ["S56-M-0004-OBLIGATION_TREE"],
            "owned_paths": [f"Stage1_Instances/{theorem_id}"],
        }
        nodes = {
            "THM-M-0001": {"theorem_id": "THM-M-0001", "v2_execution_rank": 1},
            "THM-M-0002": {"theorem_id": "THM-M-0002", "v2_execution_rank": 2},
            "THM-M-0003": {"theorem_id": "THM-M-0003", "v2_execution_rank": 3},
            theorem_id: {
                "theorem_id": theorem_id,
                "v2_execution_rank": 4,
                "direct_hard_parents": ["THM-M-0003"],
                "transitive_hard_ancestors": ["THM-M-0001", "THM-M-0002", "THM-M-0003"],
                "direct_reuse_hint_ids": [],
                "shared_lemma_group_ids": [],
                "dependency_context_sha256": "a" * 64,
            },
        }
        graph = {
            "execution_contract": cron.EXECUTION_CONTRACT,
            "hard_edges": [
                {
                    "edge_id": "HARD-1-3",
                    "parent_theorem_id": "THM-M-0001",
                    "child_theorem_id": "THM-M-0003",
                },
                {
                    "edge_id": "HARD-3-4",
                    "parent_theorem_id": "THM-M-0003",
                    "child_theorem_id": theorem_id,
                },
            ],
        }
        with (
            mock.patch.object(cron, "theorem_dag_v2", return_value=(graph, nodes)),
            mock.patch.object(cron, "graph_sha256", return_value="b" * 64),
        ):
            prompt = cron.task_prompt(item, Path("/repo/worker"))
        context_text = prompt.split(
            "The authoritative v2 dependency/reuse context for this theorem is:\n", 1
        )[1].split("\n\nRequired work:", 1)[0]
        context = json.loads(context_text)
        self.assertEqual(
            context["parent_inspection_order"],
            ["THM-M-0001", "THM-M-0002", "THM-M-0003"],
        )
        self.assertEqual(
            context["required_ledger_context"]["transitive_ancestor_ids"],
            ["THM-M-0001", "THM-M-0002", "THM-M-0003"],
        )
        for text in (
            "reused_exact",
            "reused_with_transport",
            "consumer's own validation receipt",
            "never transfers parent acceptance",
            "scheduler owns every declared validator candidate",
            "never create, refresh, rename, replace, or delete any\n   validator candidate",
        ):
            self.assertIn(text, prompt)

        self.assertNotIn("Produce exactly one HEAD-tracked validator", prompt)

    def test_parent_inspection_order_rejects_parent_after_consumer(self) -> None:
        nodes = {
            "THM-M-0001": {"v2_execution_rank": 2},
            "THM-M-0002": {
                "v2_execution_rank": 1,
                "direct_hard_parents": ["THM-M-0001"],
                "transitive_hard_ancestors": ["THM-M-0001"],
            },
        }
        with self.assertRaisesRegex(SystemExit, "not ranked before"):
            cron.parent_inspection_order("THM-M-0002", nodes)

    def test_dependency_ledger_requires_ranked_parent_and_ancestor_order(self) -> None:
        child = "THM-M-0003"
        nodes = {
            "THM-M-0001": {"v2_execution_rank": 2},
            "THM-M-0002": {"v2_execution_rank": 1},
            child: {
                "v2_execution_rank": 3,
                "direct_hard_parents": ["THM-M-0001"],
                "transitive_hard_ancestors": ["THM-M-0001", "THM-M-0002"],
                "direct_reuse_hint_ids": [],
                "shared_lemma_group_ids": [],
                "dependency_context_sha256": "a" * 64,
            },
        }
        graph = {"hard_edges": []}
        ledger = {
            "schema_version": cron.DEPENDENCY_LEDGER_SCHEMA,
            "consumer_theorem_id": child,
            "observed_theorem_dag_sha256": "b" * 64,
            "dependency_context_sha256": "a" * 64,
            "repository_revision": "base",
            "direct_parent_ids": ["THM-M-0001"],
            "transitive_ancestor_ids": ["THM-M-0001", "THM-M-0002"],
            "hard_edge_ids": [],
            "reuse_hint_ids": [],
            "shared_group_ids": [],
            "inspections": [],
            "reuse_decisions": [],
            "unresolved_compatibility_obligations": [],
        }
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "ledger.json"
            path.write_text(json.dumps(ledger), encoding="utf-8")
            with mock.patch.object(cron, "theorem_dag_v2", return_value=(graph, nodes)):
                self.assertEqual(
                    cron.expected_dependency_context(child)["transitive_ancestor_ids"],
                    ["THM-M-0002", "THM-M-0001"],
                )
                with self.assertRaisesRegex(ValueError, "incomplete transitive_ancestor_ids"):
                    cron.validate_dependency_reuse_ledger(path, child)

    def test_scheduler_loader_rejects_incomplete_transitive_parent_closure(self) -> None:
        graph = copy.deepcopy(cron.read_json(cron.THEOREM_DAG_V2))
        target = next(row for row in graph["theorems"] if row["direct_hard_parents"])
        parent = target["direct_hard_parents"][0]
        target["transitive_hard_ancestors"].remove(parent)
        with tempfile.TemporaryDirectory() as directory:
            dag = Path(directory) / "Stage1_Theorem_DAG_v2.json"
            dag.write_text(json.dumps(graph), encoding="utf-8")
            cron.theorem_dag_v2.cache_clear()
            try:
                with (
                    mock.patch.object(cron, "THEOREM_DAG_V2", dag),
                    self.assertRaisesRegex(SystemExit, "parent closure is incomplete or stale"),
                ):
                    cron.theorem_dag_v2()
            finally:
                cron.theorem_dag_v2.cache_clear()

    def test_invalid_integration_limit_has_no_refresh_side_effects(self) -> None:
        with mock.patch.object(cron, "refresh_claims") as refresh:
            with self.assertRaisesRegex(SystemExit, "--limit must be"):
                cron.integrate(cron.MAX_INTEGRATION_LIMIT + 1)
        refresh.assert_not_called()

    def test_app_server_runtime_is_isolated_from_legacy_claim_ledger(self) -> None:
        self.assertNotEqual(cron.RUNTIME, cron.LEGACY_RUNTIME)
        self.assertEqual(cron.RUNTIME.name, "stage1-v2-app-server")
        self.assertEqual(cron.PAUSE_FILE, cron.RUNTIME / "PAUSED")
        self.assertEqual(cron.LEGACY_PAUSE_FILE, cron.LEGACY_RUNTIME / "PAUSED")

    def test_current_and_legacy_pause_markers_both_freeze_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            current = root / "current" / "PAUSED"
            legacy = root / "legacy" / "PAUSED"
            with (
                mock.patch.object(cron, "RUNTIME", current.parent),
                mock.patch.object(cron, "LEGACY_RUNTIME", legacy.parent),
                mock.patch.object(cron, "PAUSE_FILE", current),
                mock.patch.object(cron, "LEGACY_PAUSE_FILE", legacy),
            ):
                self.assertFalse(cron.execution_is_paused())
                legacy.parent.mkdir(parents=True)
                legacy.write_text("paused\n", encoding="utf-8")
                self.assertTrue(cron.execution_is_paused())
                legacy.unlink()
                current.parent.mkdir(parents=True)
                current.write_text("paused\n", encoding="utf-8")
                self.assertTrue(cron.execution_is_paused())

    def test_legacy_pause_is_migrated_without_clearing_the_freeze(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / ".cron" / "current"
            legacy_runtime = root / ".cron" / "legacy"
            current = runtime / "PAUSED"
            legacy = legacy_runtime / "PAUSED"
            legacy.parent.mkdir(parents=True)
            legacy.write_text("frozen-boundary\n", encoding="utf-8")
            with (
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(cron, "LEGACY_RUNTIME", legacy_runtime),
                mock.patch.object(cron, "PAUSE_FILE", current),
                mock.patch.object(cron, "LEGACY_PAUSE_FILE", legacy),
            ):
                self.assertTrue(cron.migrate_pause_marker())
                self.assertEqual(current.read_text(encoding="utf-8"), "frozen-boundary\n")
                self.assertTrue(legacy.exists())
                self.assertTrue(cron.execution_is_paused())

    def test_worker_argv_binds_exact_ultra_default_runtime_contract(self) -> None:
        argv = cron.worker_argv(
            Path("/repo/worker"), Path("/repo/prompt"), Path("/repo/log"),
            Path("/repo/status"), Path("/repo/objective"),
        )
        self.assertEqual(argv[1], str(cron.APP_SERVER_CLIENT))
        self.assertEqual(argv[argv.index("--model") + 1], "gpt-5.6-sol")
        self.assertEqual(argv[argv.index("--effort") + 1], "ultra")
        self.assertEqual(argv[argv.index("--service-tier") + 1], "default")
        self.assertNotIn("tmux", argv)

    def test_worker_argv_rejects_scheduler_runtime_fallback(self) -> None:
        with (
            mock.patch.object(cron, "CODEX_REASONING_EFFORT", "max"),
            self.assertRaisesRegex(SystemExit, "fallback is forbidden"),
        ):
            cron.worker_argv(
                Path("/repo/worker"), Path("/repo/prompt"), Path("/repo/log"),
                Path("/repo/status"), Path("/repo/objective"),
            )

    def test_worker_argv_requires_explicit_client_lane_and_review_binding(self) -> None:
        implementation = cron.worker_argv(
            Path("/repo/worker"), Path("/repo/prompt"), Path("/repo/log"),
            Path("/repo/status"), Path("/repo/objective"),
        )
        self.assertEqual(
            implementation[implementation.index("--lane") + 1], cron.IMPLEMENTATION_LANE
        )
        self.assertNotIn("--binding", implementation)
        binding = Path("/repo/review-binding.json")
        review = cron.worker_argv(
            Path("/repo"), Path("/repo/prompt"), Path("/repo/log"),
            Path("/repo/status"), Path("/repo/objective"),
            lane=cron.REVIEW_LANE, binding_path=binding,
        )
        self.assertEqual(review[review.index("--lane") + 1], cron.REVIEW_LANE)
        self.assertEqual(review[review.index("--binding") + 1], str(binding))
        with self.assertRaisesRegex(SystemExit, "requires a scheduler-owned binding"):
            cron.worker_argv(
                Path("/repo"), Path("/repo/prompt"), Path("/repo/log"),
                Path("/repo/status"), Path("/repo/objective"), lane=cron.REVIEW_LANE,
            )
        resumed = cron.worker_argv(
            Path("/repo/worker"), Path("/repo/prompt"), Path("/repo/log"),
            Path("/repo/status"), Path("/repo/objective"), thread_id="thread-123",
        )
        self.assertEqual(resumed[resumed.index("--thread-id") + 1], "thread-123")
        with self.assertRaisesRegex(SystemExit, "thread id is malformed"):
            cron.worker_argv(
                Path("/repo/worker"), Path("/repo/prompt"), Path("/repo/log"),
                Path("/repo/status"), Path("/repo/objective"), thread_id="bad thread",
            )

    def test_active_lease_budget_is_shared_by_implementation_and_review(self) -> None:
        claims = [
            {
                "lane": cron.IMPLEMENTATION_LANE,
                "runtime_protocol": cron.RUNTIME_PROTOCOL,
                "status": "live",
            }
            for _ in range(30)
        ] + [
            {
                "lane": cron.REVIEW_LANE,
                "runtime_protocol": cron.RUNTIME_PROTOCOL,
                "status": "preparing",
            }
            for _ in range(20)
        ]
        with (
            mock.patch.object(
                cron, "app_server_worker_is_live",
                return_value=True,
            ),
            mock.patch.object(cron, "app_server_child_is_live", return_value=False),
        ):
            self.assertEqual(len(cron.active_lane_leases(claims)), cron.MAX_WORKERS)

    def test_quarantined_live_identity_blocks_lane_allocation(self) -> None:
        claims = [{"runtime_protocol": cron.RUNTIME_PROTOCOL, "status": "quarantined"}]
        with (
            mock.patch.object(cron, "app_server_worker_is_live", return_value=True),
            mock.patch.object(cron, "app_server_child_is_live", return_value=False),
            self.assertRaisesRegex(SystemExit, "quarantined live app-server identity"),
        ):
            cron.refuse_unsafe_live_identities(claims)

    @staticmethod
    def write_proc_entry(
        proc_root: Path,
        pid: int,
        command: list[str],
        *,
        parent: int = 1,
        start_ticks: int = 12345,
    ) -> None:
        entry = proc_root / str(pid)
        entry.mkdir(parents=True)
        entry.joinpath("cmdline").write_bytes(
            b"\0".join(part.encode() for part in command) + b"\0"
        )
        # process_start_ticks consumes field 22 and proc_parent_pid consumes
        # field 4. The values after comm begin at field 3.
        fields = ["S", str(parent)] + ["0"] * 17 + [str(start_ticks)]
        entry.joinpath("stat").write_text(
            f"{pid} (stage1-fixture) " + " ".join(fields) + "\n",
            encoding="utf-8",
        )

    def process_inventory_fixture(
        self, root: Path, claim: dict[str, object]
    ) -> tuple[Path, list[str]]:
        runtime = root / ".cron" / "stage1-v2-app-server"
        claim_id = str(claim["claim_id"])
        workspace = runtime / "workers" / "slot1"
        prompt = runtime / "prompts" / f"{claim_id}.txt"
        objective = runtime / "goals" / f"{claim_id}.txt"
        status = runtime / "app-server" / f"{claim_id}.json"
        output = runtime / "logs" / f"{claim_id}.out"
        command = [
            "/usr/bin/python3", str(root / "scripts" / "stage1_app_server_client.py"),
            "--workspace", str(workspace), "--prompt", str(prompt),
            "--objective", str(objective), "--status", str(status),
            "--log", str(output), "--lane", cron.IMPLEMENTATION_LANE,
            "--model", cron.CODEX_MODEL, "--effort", cron.CODEX_REASONING_EFFORT,
            "--service-tier", cron.CODEX_SERVICE_TIER,
        ]
        claim.update(
            lane=cron.IMPLEMENTATION_LANE,
            slot=1,
            workspace=str(workspace),
            app_server_status=str(status),
            goal_objective_path=str(objective),
            output_log=str(output),
            runtime_protocol=cron.RUNTIME_PROTOCOL,
            status="preparing",
            pid=None,
        )
        return runtime, command

    def test_proc_inventory_recovers_unique_preparing_claim_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            proc_root = Path(directory) / "proc"
            proc_root.mkdir()
            claim: dict[str, object] = {
                "claim_id": "20260716T120000Z-0123456789ab",
            }
            runtime, command = self.process_inventory_fixture(root, claim)
            self.write_proc_entry(proc_root, 4242, command, start_ticks=98765)
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(
                    cron, "APP_SERVER_CLIENT",
                    root / "scripts" / "stage1_app_server_client.py",
                ),
                mock.patch.object(cron, "PROC_ROOT", proc_root),
            ):
                changed = cron.reconcile_process_inventory([claim])
            self.assertTrue(changed)
            self.assertEqual((claim["pid"], claim["pid_start_ticks"]), (4242, 98765))

    def test_refresh_reconciles_process_identity_before_claim_mutation(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "preparing")
        events: list[str] = []
        with tempfile.TemporaryDirectory() as directory:
            with (
                mock.patch.object(cron, "PROC_ROOT", Path(directory) / "proc"),
                mock.patch.object(cron, "load_claims", side_effect=lambda: events.append("load") or [claim]),
                mock.patch.object(
                    cron, "reconcile_process_inventory",
                    side_effect=lambda _claims: events.append("inventory") or False,
                ),
                mock.patch.object(
                    cron, "run",
                    side_effect=lambda *_args, **_kwargs: events.append("git")
                    or subprocess.CompletedProcess([], 0, "base\n", ""),
                ),
                mock.patch.object(cron, "theorem_dag_v2", return_value=({}, {
                    item["theorem_id"]: {"v2_execution_rank": 1},
                })),
                mock.patch.object(cron, "app_server_worker_is_live", return_value=False),
                mock.patch.object(cron, "app_server_child_is_live", return_value=False),
                mock.patch.object(cron, "recover_claim_process_identity", return_value=False),
                mock.patch.object(cron, "save_claims"),
            ):
                cron.refresh_claims([item])
        self.assertLess(events.index("inventory"), events.index("git"))

    def test_proc_inventory_rejects_unledgered_client_without_disclosing_argv(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            proc_root = Path(directory) / "proc"
            proc_root.mkdir()
            claim: dict[str, object] = {
                "claim_id": "20260716T120000Z-0123456789ab",
            }
            runtime, command = self.process_inventory_fixture(root, claim)
            self.write_proc_entry(proc_root, 4242, command)
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(
                    cron, "APP_SERVER_CLIENT",
                    root / "scripts" / "stage1_app_server_client.py",
                ),
                mock.patch.object(cron, "PROC_ROOT", proc_root),
                self.assertRaisesRegex(SystemExit, "unledgered or ambiguous"),
            ):
                cron.reconcile_process_inventory([])

    def test_proc_inventory_rejects_unbound_child_and_ignores_unrelated_process(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            proc_root = Path(directory) / "proc"
            proc_root.mkdir()
            claim: dict[str, object] = {
                "claim_id": "20260716T120000Z-0123456789ab",
            }
            runtime, command = self.process_inventory_fixture(root, claim)
            self.write_proc_entry(proc_root, 4242, command)
            self.write_proc_entry(
                proc_root,
                4243,
                ["/usr/bin/codex", *cron.REQUIRED_APP_SERVER_ARGV],
                parent=4242,
                start_ticks=777,
            )
            self.write_proc_entry(
                proc_root, 5000, ["/usr/bin/codex", "app-server", "proxy"]
            )
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(
                    cron, "APP_SERVER_CLIENT",
                    root / "scripts" / "stage1_app_server_client.py",
                ),
                mock.patch.object(cron, "PROC_ROOT", proc_root),
                self.assertRaisesRegex(SystemExit, "unledgered Stage1 app-server child"),
            ):
                cron.reconcile_process_inventory([claim])

    def test_proc_inventory_accepts_child_only_with_claim_bound_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            proc_root = Path(directory) / "proc"
            proc_root.mkdir()
            claim: dict[str, object] = {
                "claim_id": "20260716T120000Z-0123456789ab",
            }
            runtime, command = self.process_inventory_fixture(root, claim)
            self.write_proc_entry(proc_root, 4242, command)
            self.write_proc_entry(
                proc_root,
                4243,
                ["/usr/bin/codex", *cron.REQUIRED_APP_SERVER_ARGV],
                parent=4242,
                start_ticks=777,
            )
            status = Path(str(claim["app_server_status"]))
            status.parent.mkdir(parents=True)
            status.write_text(json.dumps({
                "app_server_pid": 4243,
                "app_server_start_ticks": 777,
            }) + "\n", encoding="utf-8")
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(
                    cron, "APP_SERVER_CLIENT",
                    root / "scripts" / "stage1_app_server_client.py",
                ),
                mock.patch.object(cron, "PROC_ROOT", proc_root),
            ):
                self.assertTrue(cron.reconcile_process_inventory([claim]))

    def test_proc_inventory_rejects_orphan_child_after_canonical_parent_exits(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            proc_root = Path(directory) / "proc"
            proc_root.mkdir()
            claim: dict[str, object] = {
                "claim_id": "20260716T120000Z-0123456789ab",
            }
            runtime, _command = self.process_inventory_fixture(root, claim)
            self.write_proc_entry(
                proc_root,
                4243,
                ["/usr/bin/codex", *cron.REQUIRED_APP_SERVER_ARGV],
                parent=1,
                start_ticks=777,
            )
            status = Path(str(claim["app_server_status"]))
            status.parent.mkdir(parents=True)
            status.write_text(json.dumps({
                "app_server_pid": 4243,
                "app_server_start_ticks": 777,
            }) + "\n", encoding="utf-8")
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(
                    cron, "APP_SERVER_CLIENT",
                    root / "scripts" / "stage1_app_server_client.py",
                ),
                mock.patch.object(cron, "PROC_ROOT", proc_root),
                self.assertRaisesRegex(SystemExit, "unledgered Stage1 app-server child"),
            ):
                cron.reconcile_process_inventory([])

    def test_proc_inventory_rejects_duplicate_or_noncanonical_client_argv(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            proc_root = Path(directory) / "proc"
            proc_root.mkdir()
            claim: dict[str, object] = {
                "claim_id": "20260716T120000Z-0123456789ab",
            }
            runtime, command = self.process_inventory_fixture(root, claim)
            command.extend(["--workspace", str(runtime / "workers" / "slot2")])
            self.write_proc_entry(proc_root, 4242, command)
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(
                    cron, "APP_SERVER_CLIENT",
                    root / "scripts" / "stage1_app_server_client.py",
                ),
                mock.patch.object(cron, "PROC_ROOT", proc_root),
                self.assertRaisesRegex(SystemExit, "noncanonical Stage1 app-server client"),
            ):
                cron.stage1_process_inventory()

    def test_review_candidates_use_stable_order_but_source_requires_provenance(self) -> None:
        first = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "layer": 0, "state": "[_]",
        }
        second = {
            "id": "S56-M-0002-INTAKE", "theorem_id": "THM-M-0002",
            "phase": "intake", "layer": 0, "state": "[_]",
        }
        claims: list[dict[str, object]] = [
            {
                "item_id": item["id"],
                "lane": cron.IMPLEMENTATION_LANE,
                "status": "finished_integrated",
                "runtime_protocol": cron.RUNTIME_PROTOCOL,
                "fresh_revalidation": False,
            }
            for item in (first, second)
        ]
        nodes = {
            first["theorem_id"]: {"v2_execution_rank": 2},
            second["theorem_id"]: {"v2_execution_rank": 1},
        }
        with (
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, nodes)),
            mock.patch.object(
                cron, "review_source_claim", side_effect=lambda _item, rows: rows[0]
            ),
        ):
            selected = cron.review_candidates([first, second], claims)
        self.assertEqual([item["id"] for item in selected], [second["id"], first["id"]])
        self.assertIsNone(cron.review_source_claim(first, claims))
        claims.append({
            "item_id": second["id"], "lane": cron.REVIEW_LANE, "status": "review_finished",
        })
        with (
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, nodes)),
            mock.patch.object(
                cron, "review_source_claim", side_effect=lambda _item, rows: rows[0]
            ),
        ):
            selected = cron.review_candidates([first, second], claims)
        self.assertEqual([item["id"] for item in selected], [first["id"]])

    def test_review_failed_retries_after_backoff_but_live_implementation_excludes(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "layer": 0, "state": "[_]", "depends_on": [],
        }
        nodes = {item["theorem_id"]: {"v2_execution_rank": 1}}
        expired = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=1)).isoformat()
        with (
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, nodes)),
            mock.patch.object(
                cron, "review_source_claim", side_effect=lambda _item, rows: rows[0]
            ),
        ):
            source = {
                "item_id": item["id"], "lane": cron.IMPLEMENTATION_LANE,
                "status": "finished_integrated", "runtime_protocol": cron.RUNTIME_PROTOCOL,
                "fresh_revalidation": False,
            }
            self.assertEqual(
                cron.review_candidates([item], [source, {
                    "item_id": item["id"], "lane": cron.REVIEW_LANE,
                    "status": "review_failed", "review_retry_after": expired,
                }]),
                [item],
            )
            self.assertEqual(
                cron.review_candidates([item], [{
                    "item_id": item["id"], "lane": cron.IMPLEMENTATION_LANE,
                    "status": "live",
                }]),
                [],
            )

    def test_review_candidates_require_master_accepted_phase_dependencies(self) -> None:
        intake = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "layer": 0, "state": "[_]", "depends_on": [],
        }
        statement = {
            "id": "S56-M-0001-STATEMENT", "theorem_id": "THM-M-0001",
            "phase": "statement", "layer": 1, "state": "[_]",
            "depends_on": [intake["id"]],
        }
        nodes = {intake["theorem_id"]: {"v2_execution_rank": 1}}
        with (
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, nodes)),
            mock.patch.object(
                cron, "review_source_claim", side_effect=lambda _item, rows: rows[0]
            ),
        ):
            intake_source = {
                "item_id": intake["id"], "lane": cron.IMPLEMENTATION_LANE,
                "status": "finished_integrated", "runtime_protocol": cron.RUNTIME_PROTOCOL,
                "fresh_revalidation": False,
            }
            statement_source = {
                "item_id": statement["id"], "lane": cron.IMPLEMENTATION_LANE,
                "status": "finished_integrated", "runtime_protocol": cron.RUNTIME_PROTOCOL,
                "fresh_revalidation": False,
            }
            self.assertEqual(
                cron.review_candidates([intake, statement], [intake_source, statement_source]),
                [intake],
            )
            intake["state"] = "[x]"
            self.assertEqual(
                cron.review_candidates([intake, statement], [intake_source, statement_source]),
                [statement],
            )

    def test_historical_self_tested_item_requires_content_bound_revalidation_plan(self) -> None:
        historical = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "layer": 0, "state": "[_]", "attempts": 1,
            "depends_on": [], "owned_paths": ["Stage1_Instances/THM-M-0001"],
        }
        open_item = {
            **historical,
            "id": "S56-M-0002-INTAKE", "theorem_id": "THM-M-0002",
            "state": "[ ]", "attempts": 0,
            "owned_paths": ["Stage1_Instances/THM-M-0002"],
        }
        nodes = {
            historical["theorem_id"]: {"v2_execution_rank": 1},
            open_item["theorem_id"]: {"v2_execution_rank": 2},
        }
        with (
            mock.patch.object(cron, "legacy_revalidation_lanes", return_value={}),
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, nodes)),
        ):
            self.assertEqual(cron.implementation_candidates([historical, open_item], []), [open_item])
        lane = {
            "schema_version": "stage1-legacy-revalidation-lane/1.0",
            "item_id": historical["id"], "theorem_id": historical["theorem_id"],
            "phase": historical["phase"], "authoritative_state": "[_]",
        }
        with (
            mock.patch.object(
                cron, "legacy_revalidation_lanes", return_value={historical["id"]: lane}
            ),
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, nodes)),
        ):
            self.assertEqual(
                cron.implementation_candidates([open_item, historical], []),
                [historical, open_item],
            )

    def test_review_frontier_excludes_historical_marker_without_fresh_source(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "layer": 0, "state": "[_]", "depends_on": [],
        }
        nodes = {item["theorem_id"]: {"v2_execution_rank": 1}}
        with (
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, nodes)),
            mock.patch.object(
                cron, "review_source_claim", side_effect=lambda _item, rows: rows[0]
            ),
        ):
            self.assertEqual(cron.review_candidates([item], []), [])
            self.assertEqual(
                cron.review_candidates([item], [{
                    "item_id": item["id"], "lane": cron.IMPLEMENTATION_LANE,
                    "status": "finished_integrated", "runtime_protocol": cron.RUNTIME_PROTOCOL,
                    "fresh_revalidation": False,
                }]),
                [item],
            )

    def test_scheduler_head_path_rejects_dirty_worktree_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifact = root / "evidence.json"
            artifact.write_text("dirty\n", encoding="utf-8")
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(
                    cron, "run",
                    return_value=subprocess.CompletedProcess([], 0, "evidence.json\n", ""),
                ),
                mock.patch.object(cron, "git_object_bytes", return_value=b"head\n"),
                self.assertRaisesRegex(SystemExit, "worktree bytes disagree with HEAD"),
            ):
                cron.scheduler_head_path("evidence.json")

    def test_refill_reviews_launches_read_only_lane_from_detached_checkout(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "layer": 0, "state": "[_]", "attempts": 1,
            "depends_on": [], "owned_paths": ["Stage1_Instances/THM-M-0001"],
        }
        role_map = {
            "schema_version": cron.ROLE_MAP_SCHEMA, "item_id": item["id"],
            "theorem_id": item["theorem_id"], "phase": item["phase"],
            "base_revision": "b" * 40, "contract_sha256": "c" * 64,
            "artifacts": [{
                "role": "phase_receipt", "path": "Stage1_Instances/THM-M-0001/intake-receipt.json",
                "sha256": "d" * 64, "git_blob": "e" * 40,
            }],
        }
        validator = {
            "path": "Stage1_Instances/THM-M-0001/check_intake.py", "sha256": "f" * 64,
            "git_blob": "1" * 40, "argv": ["/usr/bin/python3", "-I", "-B", "check_intake.py"],
            "recipe_sha256": "2" * 64,
        }
        saved: list[list[dict[str, object]]] = []
        launched_argv: list[str] = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / ".cron" / "stage1-v2-app-server"
            blueprint = root / "Docs" / "Stage1_Blueprint_v2.md"
            theorem_dag = root / "Docs" / "Stage1_Theorem_DAG_v2.json"
            blueprint.parent.mkdir(parents=True)
            blueprint.write_text("blueprint\n", encoding="utf-8")
            theorem_dag.write_text("{}\n", encoding="utf-8")
            review_workspace = runtime / "review-workspaces" / "slot1"
            review_workspace.mkdir(parents=True)

            def launch(
                argv: list[str], *, delay_seconds: float = 0.0
            ) -> int:
                self.assertEqual(delay_seconds, 0.0)
                launched_argv.extend(argv)
                return 7654

            def confirm(claims: list[dict[str, object]], cohort: list[dict[str, object]]) -> int:
                cohort[0]["status"] = "live"
                return 1

            source_claim = {
                "lane": cron.IMPLEMENTATION_LANE,
                "item_id": item["id"],
                "theorem_id": item["theorem_id"],
                "owned_paths": item["owned_paths"],
                "status": "finished_integrated",
                "runtime_protocol": cron.RUNTIME_PROTOCOL,
                "fresh_revalidation": False,
                "claim_id": "20260716T120000Z-0123456789ab",
                "base_revision": "b" * 40,
                "goal_objective": "implement",
                "goal_objective_path": str(runtime / "goals" / "impl.txt"),
                "app_server_status": str(runtime / "app-server" / "impl.json"),
                "output_log": str(runtime / "logs" / "impl.out"),
                "workspace": str(runtime / "workers" / "slot2"),
                "selftest_manifest": str(runtime / "workers" / "slot2" / ".stage1-worker-selftest.json"),
            }

            patches = [
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(cron, "BLUEPRINT", blueprint),
                mock.patch.object(cron, "THEOREM_DAG_V2", theorem_dag),
                mock.patch.object(cron, "PAUSE_FILE", root / "PAUSED"),
                mock.patch.object(cron, "active_lane_leases", return_value=[]),
                mock.patch.object(cron, "review_candidates", return_value=[item]),
                mock.patch.object(
                    cron, "review_source_claim", return_value=source_claim
                ),
                mock.patch.object(cron, "build_review_role_map", return_value=role_map),
                mock.patch.object(cron, "select_review_validator", return_value=validator),
                mock.patch.object(cron, "snapshot_review_provenance", return_value={
                    "schema_version": cron.WORKER_PROVENANCE_SCHEMA,
                    "claim_sha256": "3" * 64,
                    "status_sha256": "4" * 64,
                    "files": {},
                    "snapshot_sha256": "5" * 64,
                }),
                mock.patch.object(
                    cron, "persist_review_provenance",
                    return_value=(runtime / "worker-provenance" / "impl.json", "6" * 64),
                ),
                mock.patch.object(cron, "build_scheduler_review_manifest", return_value={
                    "schema_version": "stage1-master-review-input/1.0",
                    "manifest_sha256": "7" * 64,
                }),
                mock.patch.object(
                    cron, "persist_review_manifest",
                    return_value=(runtime / "review-manifests" / "review.json", "8" * 64),
                ),
                mock.patch.object(cron, "phase_contract", return_value={"phase": "intake"}),
                mock.patch.object(cron, "theorem_dag_v2", return_value=({}, {
                    item["theorem_id"]: {"v2_execution_rank": 1},
                })),
                mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "b" * 40 + "\n", "")),
                mock.patch.object(cron, "save_claims", side_effect=lambda rows: saved.append(copy.deepcopy(rows))),
                mock.patch.object(cron, "prepare_review_workspace", return_value=review_workspace),
                mock.patch.object(cron, "launch_app_server_worker", side_effect=launch),
                mock.patch.object(cron, "process_start_ticks", return_value=99),
                mock.patch.object(cron, "confirm_goal_handshakes", side_effect=confirm),
            ]
            with contextlib.ExitStack() as stack:
                for patcher in patches:
                    stack.enter_context(patcher)
                count = cron.refill_reviews(
                    20, data={"items": [item]}, ordered=[item], claims=[source_claim]
                )
                launched_claim = saved[-1][-1]
                review_input = json.loads(Path(launched_claim["review_input_path"]).read_text())
                prompt = Path(
                    runtime / "prompts" / f"{launched_claim['claim_id']}.txt"
                ).read_text()
        self.assertEqual(count, 1)
        claim = saved[-1][-1]
        self.assertEqual(claim["lane"], cron.REVIEW_LANE)
        self.assertEqual(claim["workspace"], str(review_workspace))
        self.assertEqual(claim["review_manifest_sha256"], "7" * 64)
        self.assertEqual(claim["review_provenance_sha256"], "6" * 64)
        self.assertEqual(review_input["review_manifest"]["manifest_sha256"], "7" * 64)
        self.assertEqual(
            review_input["implementation_provenance"]["snapshot_sha256"], "5" * 64
        )
        self.assertIn("\"snapshot_sha256\": \"" + "5" * 64 + "\"", prompt)
        self.assertIn("\"manifest_sha256\": \"" + "7" * 64 + "\"", prompt)
        self.assertEqual(launched_argv[launched_argv.index("--lane") + 1], cron.REVIEW_LANE)
        self.assertIn("--binding", launched_argv)

    def test_review_pause_after_prepare_persists_all_unstarted_cancellations(self) -> None:
        items = [
            {
                "id": f"S56-M-{index:04d}-INTAKE",
                "theorem_id": f"THM-M-{index:04d}",
                "phase": "intake", "layer": 0, "state": "[_]", "attempts": 1,
                "depends_on": [],
                "owned_paths": [f"Stage1_Instances/THM-M-{index:04d}"],
            }
            for index in (1, 2)
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / ".cron/runtime"
            pause = root / "PAUSED"
            saved: list[list[dict[str, object]]] = []

            def prepare(_slot: int, _base: str) -> Path:
                pause.write_text("paused\n", encoding="utf-8")
                return runtime / "review-workspaces/slot1"

            def add_reservations(*args: object, **kwargs: object) -> int:
                return 0

            source_claims = [{
                "lane": cron.IMPLEMENTATION_LANE, "item_id": item["id"],
                "theorem_id": item["theorem_id"], "owned_paths": item["owned_paths"],
                "status": "finished_integrated", "runtime_protocol": cron.RUNTIME_PROTOCOL,
                "fresh_revalidation": False,
            } for item in items]
            # Exercise only the post-reservation launch gate by replacing the
            # expensive evidence builders with canonical fixture values.
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(cron, "PAUSE_FILE", pause),
                mock.patch.object(cron, "active_lane_leases", return_value=[]),
                mock.patch.object(cron, "review_candidates", return_value=items),
                mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "b" * 40 + "\n", "")),
                mock.patch.object(cron, "theorem_dag_v2", return_value=({}, {
                    item["theorem_id"]: {"v2_execution_rank": index}
                    for index, item in enumerate(items, 1)
                })),
                mock.patch.object(cron, "review_source_claim", side_effect=lambda item, claims: next(c for c in source_claims if c["item_id"] == item["id"])),
                mock.patch.object(cron, "build_review_role_map", return_value={"artifacts": []}),
                mock.patch.object(cron, "select_review_validator", return_value={"recipe_sha256": "1" * 64}),
                mock.patch.object(cron, "snapshot_review_provenance", return_value={}),
                mock.patch.object(cron, "persist_review_provenance", return_value=(runtime / "p.json", "2" * 64)),
                mock.patch.object(cron, "build_scheduler_review_manifest", return_value={"manifest_sha256": "3" * 64}),
                mock.patch.object(cron, "persist_review_manifest", return_value=(runtime / "m.json", "4" * 64)),
                mock.patch.object(cron, "phase_contract", return_value={}),
                mock.patch.object(cron, "build_review_binding", return_value={}),
                mock.patch.object(cron, "prepare_review_workspace", side_effect=prepare),
                mock.patch.object(cron, "launch_app_server_worker") as launch,
                mock.patch.object(cron, "confirm_goal_handshakes", side_effect=add_reservations),
                mock.patch.object(cron, "save_claims", side_effect=lambda rows: saved.append(copy.deepcopy(rows))),
            ):
                cron.refill_reviews(
                    2, data={"items": items}, ordered=items, claims=source_claims,
                    selected_items=items, selected_slots=[1, 2],
                )
        review_rows = [row for row in saved[-1] if row.get("lane") == cron.REVIEW_LANE]
        self.assertEqual([row["status"] for row in review_rows], ["cancelled", "cancelled"])
        self.assertTrue(all("cancelled_at" in row for row in review_rows))
        launch.assert_not_called()

    def test_master_acceptance_replays_receipts_and_cas_closes_phase(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "layer": 0, "state": "[_]", "attempts": 1,
            "depends_on": [], "owned_paths": ["Stage1_Instances/THM-M-0001"],
        }
        review_output = {
            "worker_verdict": "no_state_change", "review_verdict": "phase_accepted",
            "audit_complete": False, "theorem_complete": False,
            "status_boundary": "phase only",
        }
        manifest = {
            "authority_revision": "a" * 40, "authority_tree": "b" * 40,
            "blueprint_sha256": "", "manifest_sha256": "c" * 64,
        }
        role_map = {"manifest_sha256": "d" * 64, "artifacts": []}
        validator = {"recipe_sha256": "e" * 64}
        replay = {"result_sha256": "f" * 64}
        decision = {
            "decision": "phase_accepted", "phase_evidence_accepted": True,
            "decision_sha256": "1" * 64,
        }
        claim = {
            "lane": cron.REVIEW_LANE, "status": "review_finished",
            "item_id": item["id"], "claim_id": "20260716T120000Z-abcdef123456",
            "review_binding_sha256": "2" * 64,
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            blueprint = root / "Docs" / "Stage1_Blueprint_v2.md"
            blueprint.parent.mkdir(parents=True)
            blueprint.write_text("frozen [_] authority\n", encoding="utf-8")
            manifest["blueprint_sha256"] = sha256(blueprint)
            transaction = cron.FileTransaction()
            original = copy.deepcopy(item)
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "BLUEPRINT", blueprint),
                mock.patch.object(cron, "PAUSE_FILE", root / "PAUSED"),
                mock.patch.object(cron, "theorem_dag_v2", return_value=({}, {
                    item["theorem_id"]: {"v2_execution_rank": 1},
                })),
                mock.patch.object(cron, "hard_edge_gate_status", return_value=("not_applicable", [])),
                mock.patch.object(
                    cron, "verify_review_evidence_bundle",
                    return_value=(review_output, manifest, role_map, validator, {}),
                ),
                mock.patch.object(
                    cron, "require_review_compatible_with_current_head",
                    return_value="a" * 40,
                ),
                mock.patch.object(
                    cron, "authoritative_head_revision", return_value="a" * 40
                ),
                mock.patch.object(cron, "review_authority_contract_record", return_value={}),
                mock.patch.object(cron.acceptance_evidence, "replay_validator", return_value=replay),
                mock.patch.object(
                    cron.acceptance_evidence, "evaluate_replay_semantics", return_value=decision
                ),
                mock.patch.object(cron, "phase_acceptance_contract_record", return_value={}),
                mock.patch.object(cron, "load_blueprint_items", return_value=[original]),
                mock.patch.object(cron, "write_projection") as write_projection,
                mock.patch.object(cron, "write_derived_surfaces") as write_derived,
            ):
                accepted, rejected = cron.consume_review_finished(
                    {"items": [item]}, [item], [claim], transaction, limit=1
                )
            self.assertEqual(accepted, [item["id"]])
            self.assertEqual(rejected, [])
            self.assertEqual(item["state"], "[x]")
            self.assertEqual(claim["status"], "master_accepted")
            receipt = root / str(claim["master_receipt_path"])
            self.assertTrue(receipt.is_file())
            self.assertEqual(sha256(receipt), claim["master_receipt_sha256"])
            write_projection.assert_called_once()
            write_derived.assert_called_once()

    def test_review_compatibility_allows_unrelated_head_drift(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "state": "[_]", "attempts": 1,
        }
        role_map = {
            "schema_version": "role-map", "item_id": item["id"],
            "theorem_id": item["theorem_id"], "phase": item["phase"],
            "base_revision": "a" * 40, "contract_sha256": "c" * 64,
            "contract_git_blob": "d" * 40, "phase_receipt_path": "receipt.json",
            "phase_receipt_sha256": "e" * 64, "artifacts": [{"path": "artifact"}],
        }
        validator = {
            "item_id": item["id"], "theorem_id": item["theorem_id"],
            "phase": item["phase"], "base_revision": "a" * 40,
            "contract_sha256": "c" * 64, "validator_path": "check.py",
            "validator_sha256": "f" * 64, "validator_git_blob": "1" * 40,
            "validator_git_mode": "100644", "argv": ["/usr/bin/python3", "check.py"],
            "cwd": ".", "network_policy": "denied", "repo_write_access": False,
            "isolated_scratch_write_access": True, "shell_interpolation": False,
        }
        node = {"theorem_id": item["theorem_id"], "v2_execution_rank": 1}
        manifest = {
            "authority_revision": "b" * 40, "base_revision": "a" * 40,
            "blueprint_sha256": "2" * 64,
            "contract": {
                "path": "Docs/Stage1_Phase_Acceptance_Contracts.json",
                "sha256": "c" * 64, "git_blob": "d" * 40,
            },
        }
        select_validator = mock.Mock(return_value={
            **validator, "authority_revision": "9" * 40,
        })
        with (
            mock.patch.object(cron, "PHASE_ACCEPTANCE_CONTRACT_SHA256", "c" * 64),
            mock.patch.object(cron, "phase_acceptance_contract_record", return_value={
                "revision": "9" * 40,
                "path": manifest["contract"]["path"],
                "sha256": "c" * 64, "git_blob": "d" * 40,
            }),
            mock.patch.object(cron, "sha256_file", return_value="2" * 64),
            mock.patch.object(cron, "build_review_role_map", return_value={
                **role_map, "authority_revision": "9" * 40,
            }),
            mock.patch.object(cron, "select_review_validator", select_validator),
            mock.patch.object(cron, "git_object_bytes", side_effect=[
                json.dumps({
                    "theorems": [node], "hard_edges": [], "reuse_hints": [],
                    "shared_lemma_groups": [],
                }).encode(),
                json.dumps({
                    "theorems": [node], "hard_edges": [], "reuse_hints": [],
                    "shared_lemma_groups": [],
                }).encode(),
            ]),
            mock.patch.object(
                cron, "authoritative_head_revision", return_value="9" * 40
            ),
        ):
            compatible_head = cron.require_review_compatible_with_current_head(
                item, manifest, role_map, validator
            )
        self.assertEqual(compatible_head, "9" * 40)
        select_validator.assert_called_once_with(
            item, "a" * 40, require_base_blob_match=False
        )

    def test_review_compatibility_rejects_target_artifact_or_dag_drift(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "state": "[_]",
        }
        role_map = {
            "schema_version": "role-map", "item_id": item["id"],
            "theorem_id": item["theorem_id"], "phase": item["phase"],
            "base_revision": "a" * 40, "contract_sha256": "c" * 64,
            "contract_git_blob": "d" * 40, "phase_receipt_path": "receipt.json",
            "phase_receipt_sha256": "e" * 64, "artifacts": [{"path": "artifact"}],
        }
        validator = {
            "item_id": item["id"], "theorem_id": item["theorem_id"],
            "phase": item["phase"], "base_revision": "a" * 40,
            "contract_sha256": "c" * 64, "validator_path": "check.py",
            "validator_sha256": "f" * 64, "validator_git_blob": "1" * 40,
            "validator_git_mode": "100644", "argv": ["/usr/bin/python3", "check.py"],
            "cwd": ".", "network_policy": "denied", "repo_write_access": False,
            "isolated_scratch_write_access": True, "shell_interpolation": False,
        }
        manifest = {
            "authority_revision": "b" * 40, "base_revision": "a" * 40,
            "blueprint_sha256": "2" * 64,
            "contract": {
                "path": "Docs/Stage1_Phase_Acceptance_Contracts.json",
                "sha256": "c" * 64, "git_blob": "d" * 40,
            },
        }
        with (
            self.assertRaisesRegex(ValueError, "artifacts or validator"),
            mock.patch.object(cron, "PHASE_ACCEPTANCE_CONTRACT_SHA256", "c" * 64),
            mock.patch.object(cron, "phase_acceptance_contract_record", return_value={
                "revision": "9" * 40,
                "path": manifest["contract"]["path"],
                "sha256": "c" * 64, "git_blob": "d" * 40,
            }),
            mock.patch.object(cron, "sha256_file", return_value="2" * 64),
            mock.patch.object(cron, "select_review_validator", return_value=validator),
            mock.patch.object(cron, "build_review_role_map", return_value={
                **role_map, "artifacts": [{"path": "changed"}],
            }),
            mock.patch.object(
                cron, "authoritative_head_revision", return_value="9" * 40
            ),
        ):
            cron.require_review_compatible_with_current_head(
                item, manifest, role_map, validator
            )

    def test_review_compatibility_rejects_related_dag_row_drift(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "state": "[_]",
        }
        role_map = {
            "schema_version": "role-map", "item_id": item["id"],
            "theorem_id": item["theorem_id"], "phase": item["phase"],
            "base_revision": "a" * 40, "contract_sha256": "c" * 64,
            "contract_git_blob": "d" * 40, "phase_receipt_path": "receipt.json",
            "phase_receipt_sha256": "e" * 64, "artifacts": [{"path": "artifact"}],
        }
        validator = {
            "item_id": item["id"], "theorem_id": item["theorem_id"],
            "phase": item["phase"], "base_revision": "a" * 40,
            "contract_sha256": "c" * 64, "validator_path": "check.py",
            "validator_sha256": "f" * 64, "validator_git_blob": "1" * 40,
            "validator_git_mode": "100644", "argv": ["/usr/bin/python3", "check.py"],
            "cwd": ".", "network_policy": "denied", "repo_write_access": False,
            "isolated_scratch_write_access": True, "shell_interpolation": False,
        }
        node = {
            "theorem_id": item["theorem_id"], "v2_execution_rank": 1,
            "topological_layer": 0, "direct_hard_parents": [],
            "transitive_hard_ancestors": [], "direct_reuse_hint_ids": [],
            "shared_lemma_group_ids": ["G1"], "dependency_context_sha256": "2" * 64,
        }
        authority_group = {
            "group_id": "G1", "member_theorem_ids": [item["theorem_id"], "THM-M-0002"],
            "blocking": False, "reuse_boundary": "frozen",
        }
        current_group = {**authority_group, "reuse_boundary": "changed"}
        manifest = {
            "authority_revision": "b" * 40, "base_revision": "a" * 40,
            "contract": {
                "path": "Docs/Stage1_Phase_Acceptance_Contracts.json",
                "sha256": "c" * 64, "git_blob": "d" * 40,
            },
        }
        with (
            self.assertRaisesRegex(ValueError, "shared_lemma_groups changed"),
            mock.patch.object(cron, "PHASE_ACCEPTANCE_CONTRACT_SHA256", "c" * 64),
            mock.patch.object(cron, "phase_acceptance_contract_record", return_value={
                "revision": "9" * 40,
                "path": manifest["contract"]["path"], "sha256": "c" * 64,
                "git_blob": "d" * 40,
            }),
            mock.patch.object(cron, "build_review_role_map", return_value=role_map),
            mock.patch.object(cron, "select_review_validator", return_value=validator),
            mock.patch.object(cron, "git_object_bytes", side_effect=[
                json.dumps({
                    "theorems": [node], "hard_edges": [], "reuse_hints": [],
                    "shared_lemma_groups": [current_group],
                }).encode(),
                json.dumps({
                    "theorems": [node], "hard_edges": [], "reuse_hints": [],
                    "shared_lemma_groups": [authority_group],
                }).encode(),
            ]),
            mock.patch.object(
                cron, "authoritative_head_revision", return_value="9" * 40
            ),
        ):
            cron.require_review_compatible_with_current_head(
                item, manifest, role_map, validator
            )

    def test_review_compatibility_rejects_head_change_during_check(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "state": "[_]",
        }
        role_map = {
            "schema_version": "role-map", "item_id": item["id"],
            "theorem_id": item["theorem_id"], "phase": item["phase"],
            "base_revision": "a" * 40, "contract_sha256": "c" * 64,
            "contract_git_blob": "d" * 40, "phase_receipt_path": "receipt.json",
            "phase_receipt_sha256": "e" * 64, "artifacts": [],
        }
        validator = {
            "item_id": item["id"], "theorem_id": item["theorem_id"],
            "phase": item["phase"], "base_revision": "a" * 40,
            "contract_sha256": "c" * 64, "validator_path": "check.py",
            "validator_sha256": "f" * 64, "validator_git_blob": "1" * 40,
            "validator_git_mode": "100644", "argv": ["python3", "check.py"],
            "cwd": ".", "network_policy": "denied", "repo_write_access": False,
            "isolated_scratch_write_access": True, "shell_interpolation": False,
        }
        node = {"theorem_id": item["theorem_id"], "v2_execution_rank": 1}
        manifest = {
            "authority_revision": "b" * 40, "base_revision": "a" * 40,
            "contract": {
                "path": "Docs/Stage1_Phase_Acceptance_Contracts.json",
                "sha256": "c" * 64, "git_blob": "d" * 40,
            },
        }
        with (
            self.assertRaisesRegex(ValueError, "HEAD changed"),
            mock.patch.object(cron, "PHASE_ACCEPTANCE_CONTRACT_SHA256", "c" * 64),
            mock.patch.object(cron, "phase_acceptance_contract_record", return_value={
                "revision": "9" * 40,
                "path": manifest["contract"]["path"], "sha256": "c" * 64,
                "git_blob": "d" * 40,
            }),
            mock.patch.object(cron, "build_review_role_map", return_value=role_map),
            mock.patch.object(cron, "select_review_validator", return_value=validator),
            mock.patch.object(cron, "git_object_bytes", side_effect=[
                json.dumps({
                    "theorems": [node], "hard_edges": [], "reuse_hints": [],
                    "shared_lemma_groups": [],
                }).encode(),
                json.dumps({
                    "theorems": [node], "hard_edges": [], "reuse_hints": [],
                    "shared_lemma_groups": [],
                }).encode(),
            ]),
            mock.patch.object(
                cron, "authoritative_head_revision",
                side_effect=["9" * 40, "8" * 40],
            ),
        ):
            cron.require_review_compatible_with_current_head(
                item, manifest, role_map, validator
            )

    def test_review_authority_contract_reloads_manifest_revision(self) -> None:
        authority = "a" * 40
        manifest = {
            "authority_revision": authority,
            "authority_tree": "b" * 40,
            "contract": {
                "path": "Docs/Stage1_Phase_Acceptance_Contracts.json",
                "sha256": "c" * 64,
                "git_blob": "d" * 40,
            },
        }
        record = {
            "revision": authority,
            "git_tree": manifest["authority_tree"],
            **manifest["contract"],
            "contract": {"phase_order": []},
        }
        with (
            mock.patch.object(cron, "PHASE_ACCEPTANCE_CONTRACT_SHA256", "c" * 64),
            mock.patch.object(
                cron.acceptance_evidence, "load_head_contract", return_value=record
            ) as load_contract,
        ):
            self.assertEqual(
                cron.review_authority_contract_record(manifest), record
            )
        load_contract.assert_called_once_with(
            cron.ROOT, "c" * 64, revision=authority
        )

        with (
            self.assertRaisesRegex(ValueError, "snapshot is stale"),
            mock.patch.object(cron, "PHASE_ACCEPTANCE_CONTRACT_SHA256", "c" * 64),
            mock.patch.object(
                cron.acceptance_evidence, "load_head_contract",
                return_value={**record, "git_tree": "e" * 40},
            ),
        ):
            cron.review_authority_contract_record(manifest)

    def test_master_acceptance_rejects_legacy_hard_edge_evidence(self) -> None:
        item = {
            "id": "S56-M-0001-PROOF", "theorem_id": "THM-M-0001",
            "phase": "proof", "layer": 4, "state": "[_]", "attempts": 1,
            "depends_on": [], "owned_paths": ["Stage1_Instances/THM-M-0001"],
        }
        claim = {
            "lane": cron.REVIEW_LANE, "status": "review_finished",
            "item_id": item["id"], "claim_id": "20260716T120000Z-abcdef123456",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            blueprint = root / "blueprint.md"
            blueprint.write_text("[_]\n", encoding="utf-8")
            verify = mock.Mock()
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "BLUEPRINT", blueprint),
                mock.patch.object(cron, "PAUSE_FILE", root / "PAUSED"),
                mock.patch.object(cron, "theorem_dag_v2", return_value=({}, {
                    item["theorem_id"]: {"v2_execution_rank": 1},
                })),
                mock.patch.object(
                    cron, "hard_edge_gate_status",
                    return_value=("legacy_evidence_present", []),
                ),
                mock.patch.object(cron, "verify_review_evidence_bundle", verify),
            ):
                accepted, rejected = cron.consume_review_finished(
                    {"items": [item]}, [item], [claim], cron.FileTransaction(), limit=1
                )
        self.assertEqual(accepted, [])
        self.assertEqual(rejected, [item["id"]])
        self.assertEqual(item["state"], "[_]")
        self.assertEqual(claim["status"], "review_failed")
        self.assertIn("G08", claim["review_rejection_reason"])
        verify.assert_not_called()

    def test_master_acceptance_requires_every_phase_predecessor_x(self) -> None:
        predecessor = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "layer": 0, "state": "[_]", "attempts": 1,
            "depends_on": [], "owned_paths": ["Stage1_Instances/THM-M-0001"],
        }
        item = {
            "id": "S56-M-0001-STATEMENT", "theorem_id": "THM-M-0001",
            "phase": "statement", "layer": 1, "state": "[_]", "attempts": 1,
            "depends_on": [predecessor["id"]],
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
        }
        claim = {
            "lane": cron.REVIEW_LANE, "status": "review_finished",
            "item_id": item["id"], "claim_id": "20260716T120000Z-abcdef123456",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            blueprint = root / "blueprint.md"
            blueprint.write_text("[_]\n", encoding="utf-8")
            verify = mock.Mock()
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "BLUEPRINT", blueprint),
                mock.patch.object(cron, "PAUSE_FILE", root / "PAUSED"),
                mock.patch.object(cron, "theorem_dag_v2", return_value=({}, {
                    item["theorem_id"]: {"v2_execution_rank": 1},
                })),
                mock.patch.object(cron, "verify_review_evidence_bundle", verify),
            ):
                accepted, rejected = cron.consume_review_finished(
                    {"items": [predecessor, item]}, [predecessor, item], [claim],
                    cron.FileTransaction(), limit=1,
                )
        self.assertEqual(accepted, [])
        self.assertEqual(rejected, [item["id"]])
        self.assertEqual(item["state"], "[_]")
        self.assertIn("predecessor", claim["review_rejection_reason"])
        verify.assert_not_called()

    def test_review_output_worker_verdict_must_match_frozen_receipt_and_handoff(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "layer": 0, "state": "[_]", "attempts": 1,
            "depends_on": [], "owned_paths": ["Stage1_Instances/THM-M-0001"],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / ".cron" / "runtime"
            claim_id = "20260716T120000Z-abcdef123456"
            paths = {
                "review_input": runtime / "review-inputs" / f"{claim_id}.json",
                "manifest": runtime / "review-manifests" / f"{claim_id}.json",
                "binding": runtime / "review-bindings" / f"{claim_id}.json",
                "provenance": runtime / "worker-provenance" / "impl.json",
                "prompt": runtime / "prompts" / f"{claim_id}.txt",
                "status": runtime / "app-server" / f"{claim_id}.json",
                "receipt": root / "Stage1_Instances" / "THM-M-0001" / "intake-receipt.json",
            }
            for path in paths.values():
                path.parent.mkdir(parents=True, exist_ok=True)
            receipt = {"worker_verdict": "no_state_change"}
            paths["receipt"].write_text(json.dumps(receipt), encoding="utf-8")
            handoff_bytes = json.dumps({"worker_verdict": "no_state_change"}).encode()
            handoff_sha256 = hashlib.sha256(handoff_bytes).hexdigest()
            implementation_claim = {
                "claim_id": "20260716T110000Z-0123456789ab",
                "item_id": item["id"],
                "theorem_id": item["theorem_id"],
                "worker_handoff_path": str(runtime / "worker-handoffs" / "impl.json"),
                "worker_handoff_sha256": handoff_sha256,
                "worker_handoff_size": len(handoff_bytes),
            }
            provenance = {
                "schema_version": cron.WORKER_PROVENANCE_SCHEMA,
                "claim": implementation_claim,
                "files": {"selftest_manifest": {
                    "path": implementation_claim["worker_handoff_path"],
                    "sha256": handoff_sha256,
                    "size": len(handoff_bytes),
                    "content_base64": __import__("base64").b64encode(handoff_bytes).decode(),
                }},
            }
            provenance["snapshot_sha256"] = cron.canonical_json_sha256(provenance)
            manifest = {
                "manifest_sha256": "a" * 64, "base_revision": "r",
                "blueprint_sha256": "s", "theorem_dag_sha256": "t",
            }
            role_map = {"artifacts": [{
                "role": "phase_receipt",
                "path": paths["receipt"].relative_to(root).as_posix(),
                "sha256": sha256(paths["receipt"]),
            }]}
            validator = {"recipe_sha256": "b" * 64}
            review_input = {
                "schema_version": cron.REVIEW_INPUT_SCHEMA,
                "review_claim_id": claim_id,
                "item": item,
                "implementation_provenance": provenance,
                "implementation_provenance_path": str(paths["provenance"]),
                "implementation_provenance_file_sha256": "p",
                "review_manifest": manifest,
                "review_manifest_path": str(paths["manifest"]),
                "review_manifest_file_sha256": "m",
                "role_map": role_map,
                "validator_recipe": validator,
            }
            objective = cron.review_goal_objective(item)
            prompt = cron.review_prompt(item, review_input, claim_id, runtime / "review-workspaces/slot1")
            binding = {
                "schema_version": cron.REVIEW_BINDING_SCHEMA,
                "claim_id": claim_id, "item_id": item["id"],
                "theorem_id": item["theorem_id"], "phase": item["phase"],
                "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                "objective_sha256": hashlib.sha256(objective.encode()).hexdigest(),
                "artifact_digests": {
                    role_map["artifacts"][0]["path"]: role_map["artifacts"][0]["sha256"]
                },
                "validator_recipe_sha256s": [validator["recipe_sha256"]],
                "base_revision": "r", "blueprint_sha256": "s",
                "theorem_dag_sha256": "t",
            }
            output = {
                "schema_version": cron.REVIEW_OUTPUT_SCHEMA, "claim_id": claim_id,
                "item_id": item["id"], "theorem_id": item["theorem_id"],
                "phase": item["phase"], "worker_verdict": "accepted",
                "review_verdict": "phase_accepted", "audit_complete": False,
                "theorem_complete": False, "root_state": None,
                "first_failed_gate": None, "retry_condition": None,
                "status_boundary": "phase", "artifact_findings": [],
                "reviewed_artifact_sha256s": binding["artifact_digests"],
                "validator_recipe_sha256s": binding["validator_recipe_sha256s"],
            }
            status = {
                "state": "finished", "review_output": output,
                "review_output_text": json.dumps(output),
            }
            status["review_output_sha256"] = hashlib.sha256(
                status["review_output_text"].encode()
            ).hexdigest()
            status["review_output_canonical_sha256"] = cron.canonical_json_sha256(output)
            claim = {
                "claim_id": claim_id, "item_id": item["id"],
                "theorem_id": item["theorem_id"], "workspace": str(runtime / "review-workspaces/slot1"),
                "review_input_path": str(paths["review_input"]),
                "review_manifest_path": str(paths["manifest"]),
                "review_binding_path": str(paths["binding"]),
                "review_provenance_path": str(paths["provenance"]),
                "review_manifest_sha256": manifest["manifest_sha256"],
            }
            claim["review_provenance_sha256"] = "p"
            claim["review_manifest_file_sha256"] = "m"
            paths["prompt"].write_text(prompt, encoding="utf-8")
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(
                    cron, "claimed_runtime_json",
                    side_effect=[review_input, manifest, binding],
                ),
                mock.patch.object(
                    cron, "read_exact_json_file", return_value=(provenance, b"{}")
                ),
                mock.patch.object(
                    cron, "review_source_claim", return_value=implementation_claim
                ),
                mock.patch.object(cron, "worker_status", return_value=status),
            ):
                with self.assertRaisesRegex(ValueError, "differs from immutable"):
                    cron.verify_review_evidence_bundle(item, claim)

    def test_pause_after_replay_rolls_back_without_receipt_or_x(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "layer": 0, "state": "[_]", "attempts": 1,
            "depends_on": [], "owned_paths": ["Stage1_Instances/THM-M-0001"],
        }
        claim = {
            "lane": cron.REVIEW_LANE, "status": "review_finished",
            "item_id": item["id"], "claim_id": "20260716T120000Z-abcdef123456",
        }
        output = {
            "worker_verdict": "no_state_change", "review_verdict": "phase_accepted",
            "audit_complete": False, "theorem_complete": False,
        }
        manifest = {"manifest_sha256": "a" * 64}
        role_map = {"manifest_sha256": "b" * 64, "artifacts": []}
        validator = {"recipe_sha256": "c" * 64}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            blueprint = root / "blueprint.md"
            blueprint.write_text("[_]\n", encoding="utf-8")
            pause = root / "PAUSED"

            def replay(*args: object, **kwargs: object) -> dict[str, object]:
                pause.write_text("paused\n", encoding="utf-8")
                return {"result_sha256": "d" * 64}

            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", root / ".cron/runtime"),
                mock.patch.object(cron, "BLUEPRINT", blueprint),
                mock.patch.object(cron, "PAUSE_FILE", pause),
                mock.patch.object(cron, "theorem_dag_v2", return_value=({}, {
                    item["theorem_id"]: {"v2_execution_rank": 1},
                })),
                mock.patch.object(cron, "hard_edge_gate_status", return_value=("not_applicable", [])),
                mock.patch.object(
                    cron, "verify_review_evidence_bundle",
                    return_value=(output, manifest, role_map, validator, {}),
                ),
                mock.patch.object(
                    cron, "require_review_compatible_with_current_head",
                    return_value="a" * 40,
                ),
                mock.patch.object(cron, "review_authority_contract_record", return_value={}),
                mock.patch.object(cron.acceptance_evidence, "replay_validator", side_effect=replay),
                mock.patch.object(cron, "write_projection") as write_projection,
            ):
                with self.assertRaisesRegex(SystemExit, "pause after authority replay"):
                    cron.consume_review_finished(
                        {"items": [item]}, [item], [claim], cron.FileTransaction(), limit=1
                    )
            self.assertEqual(item["state"], "[_]")
            self.assertFalse((root / "Stage1_Instances").exists())
            write_projection.assert_not_called()

    def test_review_finished_with_invalid_exact_output_is_failed_closed_on_refresh(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "phase": "intake", "state": "[_]", "owned_paths": ["owner"],
        }
        claim = {
            "lane": cron.REVIEW_LANE, "status": "review_finished",
            "item_id": item["id"], "theorem_id": item["theorem_id"],
            "owned_paths": item["owned_paths"],
            "runtime_protocol": cron.RUNTIME_PROTOCOL,
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / ".cron/runtime"
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(cron, "load_claims", return_value=[claim]),
                mock.patch.object(cron, "save_claims"),
                mock.patch.object(cron, "theorem_dag_v2", return_value=({}, {
                    item["theorem_id"]: {"v2_execution_rank": 1},
                })),
                mock.patch.object(cron, "app_server_worker_is_live", return_value=False),
                mock.patch.object(cron, "app_server_child_is_live", return_value=False),
                mock.patch.object(cron, "CLAIM_ID_RE", mock.Mock(fullmatch=mock.Mock(return_value=True))),
                mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "a" * 40 + "\n", "")),
                mock.patch.object(cron, "worker_status", return_value={"state": "finished"}),
                mock.patch.object(cron, "claimed_runtime_json", return_value={}),
            ):
                kept = cron.refresh_claims([item])
        self.assertEqual(kept[0]["status"], "review_failed")
        self.assertIn("review output", kept[0]["review_failure_reason"])

    def test_pid_reuse_fails_closed_on_start_tick_mismatch(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "live")
        command = cron.worker_argv(
            Path(str(claim["workspace"])),
            Path("/prompt"),
            Path(str(claim["output_log"])),
            Path(str(claim["app_server_status"])),
            Path(str(claim["goal_objective_path"])),
        )
        with (
            mock.patch.object(cron, "process_command", return_value=command),
            mock.patch.object(cron, "process_start_ticks", return_value=int(claim["pid_start_ticks"]) + 1),
        ):
            self.assertFalse(cron.app_server_worker_is_live(claim))

    def test_app_server_child_identity_requires_all_three_disable_flags(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "preparing")
        with (
            mock.patch.object(
                cron,
                "worker_status",
                return_value={"app_server_pid": 7654, "app_server_start_ticks": 99},
            ),
            mock.patch.object(cron, "process_start_ticks", return_value=99),
            mock.patch.object(
                cron,
                "process_command",
                return_value=["/usr/bin/codex", *cron.REQUIRED_APP_SERVER_ARGV],
            ),
        ):
            self.assertTrue(cron.app_server_child_is_live(claim))
        missing_code_mode_only = cron.REQUIRED_APP_SERVER_ARGV[:-2]
        with (
            mock.patch.object(
                cron,
                "worker_status",
                return_value={"app_server_pid": 7654, "app_server_start_ticks": 99},
            ),
            mock.patch.object(cron, "process_start_ticks", return_value=99),
            mock.patch.object(
                cron,
                "process_command",
                return_value=["/usr/bin/codex", *missing_code_mode_only],
            ),
        ):
            self.assertFalse(cron.app_server_child_is_live(claim))

    def test_goal_runtime_verification_binds_thread_goal_pid_and_contract(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "finished")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / "stage1-v2-app-server"
            claim_id = str(claim["claim_id"])
            objective = runtime / "goals" / f"{claim_id}.txt"
            status = runtime / "app-server" / f"{claim_id}.json"
            objective.parent.mkdir(parents=True)
            status.parent.mkdir(parents=True)
            objective.write_text(str(claim["goal_objective"]) + "\n", encoding="utf-8")
            claim["goal_objective_path"] = str(objective)
            claim["app_server_status"] = str(status)
            status.write_text(json.dumps({
                "state": "finished",
                "protocol": cron.RUNTIME_PROTOCOL,
                "client_pid": claim["pid"],
                "client_start_ticks": claim["pid_start_ticks"],
                "app_server_pid": 9999,
                "app_server_start_ticks": 777,
                "thread_id": "thread-1",
                "goal": {
                    "threadId": "thread-1",
                    "objective": claim["goal_objective"],
                    "status": "complete",
                },
                "runtime_contract": {
                    "model": cron.CODEX_MODEL,
                    "reasoning_effort": cron.CODEX_REASONING_EFFORT,
                    "service_tier": cron.CODEX_SERVICE_TIER,
                    "cwd": claim["workspace"],
                    "sandbox": cron.REQUIRED_SANDBOX_CONTRACT,
                    "network_access": False,
                    "app_server_argv": cron.REQUIRED_APP_SERVER_ARGV,
                },
            }), encoding="utf-8")
            with mock.patch.object(cron, "RUNTIME", runtime):
                self.assertTrue(cron.goal_runtime_is_verified(claim))
                payload = json.loads(status.read_text(encoding="utf-8"))
                payload["runtime_contract"]["sandbox"]["networkAccess"] = True
                status.write_text(json.dumps(payload), encoding="utf-8")
                self.assertFalse(cron.goal_runtime_is_verified(claim))
                payload["runtime_contract"]["sandbox"]["networkAccess"] = False
                payload["runtime_contract"]["app_server_argv"].pop()
                status.write_text(json.dumps(payload), encoding="utf-8")
                self.assertFalse(cron.goal_runtime_is_verified(claim))
                payload["runtime_contract"]["app_server_argv"] = cron.REQUIRED_APP_SERVER_ARGV
                payload["goal"]["objective"] = "wrong goal"
                status.write_text(json.dumps(payload), encoding="utf-8")
                self.assertFalse(cron.goal_runtime_is_verified(claim))

    def test_worker_status_rejects_invalid_json_and_symlinked_parent(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "finished")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / "runtime"
            status_root = runtime / "app-server"
            status_root.mkdir(parents=True)
            status = status_root / f"{claim['claim_id']}.json"
            claim["app_server_status"] = str(status)
            status.write_text("not json\n", encoding="utf-8")
            with mock.patch.object(cron, "RUNTIME", runtime):
                self.assertIsNone(cron.worker_status(claim))

    def test_restart_live_workers_uses_only_app_server_lifecycle(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        data = {"items": [item]}
        claim = self.canonical_claim(item, "live")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / "stage1-v2-app-server"
            workspace = runtime / "workers" / "slot1"
            workspace.mkdir(parents=True)
            claim["workspace"] = str(workspace)
            old_objective = str(claim["goal_objective"])
            old_status = {
                "thread_id": "thread-existing-1",
                "goal": {
                    "threadId": "thread-existing-1",
                    "objective": old_objective,
                    "status": "active",
                },
            }
            launched: list[list[str]] = []

            def fake_launch(
                argv: list[str], *, delay_seconds: float = 0.0
            ) -> int:
                self.assertEqual(delay_seconds, 0.0)
                launched.append(argv)
                return 777

            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(cron, "PAUSE_FILE", root / "PAUSED"),
                mock.patch.object(cron, "sync_guard"),
                mock.patch.object(cron, "load_dag", return_value=(data, [item])),
                mock.patch.object(cron, "refresh_claims", return_value=[claim]),
                mock.patch.object(cron, "worker_status", return_value=old_status),
                mock.patch.object(cron, "app_server_worker_is_live", return_value=True),
                mock.patch.object(cron, "terminate_app_server_worker", return_value=True) as terminate,
                mock.patch.object(cron, "launch_app_server_worker", side_effect=fake_launch),
                mock.patch.object(cron, "process_start_ticks", return_value=999),
                mock.patch.object(cron, "confirm_goal_handshakes", side_effect=lambda _claims, cohort: (cohort[0].update(status="live") or 1)),
                mock.patch.object(cron, "save_claims"),
                mock.patch.object(cron, "write_todo"),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                cron.restart_live_workers(1)
            terminate.assert_called_once_with(claim)
            self.assertEqual(len(launched), 1)
            self.assertEqual(launched[0][1], str(cron.APP_SERVER_CLIENT))
            self.assertNotIn("tmux", launched[0])
            self.assertEqual(
                launched[0][launched[0].index("--thread-id") + 1], "thread-existing-1"
            )
            self.assertEqual(claim["status"], "live")
            self.assertEqual(claim["pid_start_ticks"], 999)
            self.assertEqual(claim["goal_objective"], old_objective)
            self.assertEqual(claim["previous_runtime"]["thread_id"], "thread-existing-1")

    def test_restart_live_workers_refuses_missing_resume_thread_before_stop(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE", "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"], "state": "[ ]",
        }
        claim = self.canonical_claim(item, "live")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            workspace = root / "runtime/workers/slot1"
            workspace.mkdir(parents=True)
            claim["workspace"] = str(workspace)
            terminate = mock.Mock(return_value=True)
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", root / "runtime"),
                mock.patch.object(cron, "PAUSE_FILE", root / "PAUSED"),
                mock.patch.object(cron, "sync_guard"),
                mock.patch.object(cron, "load_dag", return_value=({"items": [item]}, [item])),
                mock.patch.object(cron, "refresh_claims", return_value=[claim]),
                mock.patch.object(cron, "worker_status", return_value={"goal": {}}),
                mock.patch.object(cron, "terminate_app_server_worker", terminate),
                mock.patch.object(cron, "theorem_dag_v2", return_value=({}, {
                    item["theorem_id"]: {"v2_execution_rank": 1},
                })),
                self.assertRaisesRegex(SystemExit, "exact active thread/goal"),
            ):
                cron.restart_live_workers(1)
        terminate.assert_not_called()

    def test_paused_tick_is_noop_before_sync_or_integration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            pause_file = Path(directory) / "PAUSED"
            pause_file.write_text("paused\n", encoding="utf-8")
            with (
                mock.patch.object(cron, "PAUSE_FILE", pause_file),
                mock.patch.object(cron, "LEGACY_PAUSE_FILE", pause_file),
                mock.patch.object(cron, "recover_integration_wal") as recover,
                mock.patch.object(cron, "sync_guard") as sync,
                mock.patch.object(cron, "integrate") as integrate,
                contextlib.redirect_stdout(io.StringIO()),
            ):
                cron.launch(cron.MAX_WORKERS)
        recover.assert_not_called()
        sync.assert_not_called()
        integrate.assert_not_called()

    def test_install_refuses_persistent_pause(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            pause_file = Path(directory) / "PAUSED"
            pause_file.write_text("paused\n", encoding="utf-8")
            with (
                mock.patch.object(cron, "PAUSE_FILE", pause_file),
                mock.patch.object(cron, "LEGACY_PAUSE_FILE", pause_file),
                mock.patch.object(cron, "run") as run,
                self.assertRaisesRegex(SystemExit, "paused"),
            ):
                cron.install("*/5 * * * *")
        run.assert_not_called()

    def test_default_install_is_five_minute_fifty_worker_cron(self) -> None:
        captured: dict[str, str] = {}

        def write_crontab(command: list[str], **kwargs):
            captured["input"] = kwargs["input"]
            return subprocess.CompletedProcess(command, 0, "", "")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / ".cron" / "stage1-v2-app-server"
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(cron, "PAUSE_FILE", root / "PAUSED"),
                mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 1, "", "")),
                mock.patch.object(cron.subprocess, "run", side_effect=write_crontab),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                cron.install("*/5 * * * *")
        line = captured["input"].strip()
        self.assertTrue(line.startswith("*/5 * * * * "))
        self.assertIn(f"{sys.executable} {root / 'scripts' / 'stage1_execution_cron.py'}", line)
        self.assertIn("--tick --workers 50 --limit 50", line)
        self.assertIn("stage1-v2-app-server/keepalive.log", line)

    def test_integrate_refuses_persistent_pause_before_recovery(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            pause_file = Path(directory) / "PAUSED"
            pause_file.write_text("paused\n", encoding="utf-8")
            with (
                mock.patch.object(cron, "PAUSE_FILE", pause_file),
                mock.patch.object(cron, "recover_integration_wal") as recover,
                self.assertRaisesRegex(SystemExit, "paused"),
            ):
                cron.integrate(1)
        recover.assert_not_called()

    def test_resume_refuses_when_cron_entry_exists(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            pause_file = Path(directory) / "PAUSED"
            pause_file.write_text("paused\n", encoding="utf-8")
            cron_line = "*/5 * * * * /repo/scripts/stage1_execution_cron.py --tick\n"
            with (
                mock.patch.object(cron, "PAUSE_FILE", pause_file),
                mock.patch.object(
                    cron,
                    "run",
                    return_value=subprocess.CompletedProcess(["crontab", "-l"], 0, cron_line, ""),
                ),
                self.assertRaisesRegex(SystemExit, "cron entry already exists"),
            ):
                cron.resume()
            self.assertTrue(pause_file.exists())

    def test_pause_cli_bypasses_busy_scheduler_lock(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            runtime = Path(directory) / ".cron" / "stage1-rev56"
            pause_file = runtime / "PAUSED"
            argv = ["stage1_execution_cron.py", "--pause"]
            with (
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(cron, "PAUSE_FILE", pause_file),
                mock.patch.object(cron, "LEGACY_PAUSE_FILE", pause_file),
                mock.patch.object(cron.sys, "argv", argv),
                mock.patch.object(cron, "pause") as pause,
            ):
                cron.main()
        pause.assert_called_once_with()

    def test_pause_persists_intent_before_waiting_for_active_tick(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / ".cron" / "stage1-rev56"
            pause_file = runtime / "PAUSED"
            calls: list[bool] = []

            def observe_lock(_fd: int, _mode: int) -> None:
                calls.append(pause_file.is_file())

            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(cron, "PAUSE_FILE", pause_file),
                mock.patch.object(cron, "LEGACY_PAUSE_FILE", pause_file),
                mock.patch.object(cron, "validate_runtime_root"),
                mock.patch.object(
                    cron,
                    "run",
                    return_value=subprocess.CompletedProcess(["crontab", "-l"], 0, "", ""),
                ),
                mock.patch.object(cron.subprocess, "run"),
                mock.patch.object(cron.fcntl, "flock", side_effect=observe_lock),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                cron.pause()
        self.assertEqual(calls, [True])

    def test_v2_blueprint_is_the_only_loaded_state_cursor(self) -> None:
        items = cron.load_blueprint_items()
        data, ordered = cron.load_dag()
        self.assertEqual(data["requirements_source"], "Docs/Stage1_Blueprint_v2.md")
        self.assertEqual(data["items"], items)
        self.assertEqual(len(ordered), 10822)

    def test_derived_dag_divergence_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dag = Path(directory) / "dag.json"
            derived = cron.project_dag(cron.load_blueprint_items())
            derived["items"][0]["state"] = "[x]" if derived["items"][0]["state"] != "[x]" else "[ ]"
            dag.write_text(json.dumps(derived), encoding="utf-8")
            with mock.patch.object(cron, "DAG", dag):
                with self.assertRaisesRegex(SystemExit, "disagrees with the v2 blueprint SSOT"):
                    cron.load_dag()

    def test_todo_rejects_non_ssot_state_before_writing_snapshot(self) -> None:
        authoritative = cron.load_blueprint_items()
        forged = cron.project_dag(copy.deepcopy(authoritative))
        forged["items"][0]["state"] = (
            "[x]" if forged["items"][0]["state"] != "[x]" else "[ ]"
        )
        with tempfile.TemporaryDirectory() as directory:
            docs = Path(directory) / "Docs"
            docs.mkdir()
            with (
                mock.patch.object(cron, "DOCS", docs),
                mock.patch.object(cron, "load_blueprint_items", return_value=authoritative),
                mock.patch.object(cron, "order_by_v2") as order,
                self.assertRaisesRegex(SystemExit, "todo input disagrees with the v2 blueprint SSOT"),
            ):
                cron.write_todo(forged, forged["items"], [])
            order.assert_not_called()
            self.assertEqual(list(docs.iterdir()), [])

    def test_refresh_quarantines_unknown_claim_before_side_effects(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        hostile = {
            "item_id": "../../outside",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "status": "live",
            "worker_id": "hostile",
        }
        with (
            mock.patch.object(cron, "load_claims", return_value=[hostile]),
            mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "base\n", "")),
            mock.patch.object(cron, "app_server_worker_is_live") as is_live,
            mock.patch.object(cron, "snapshot_blocked_worker") as snapshot,
            mock.patch.object(cron, "save_claims") as save,
        ):
            result = cron.refresh_claims([item])
        self.assertEqual(result[0]["status"], "quarantined")
        is_live.assert_not_called()
        snapshot.assert_not_called()
        save.assert_called_once()

    def test_blocked_snapshot_rejects_unsafe_item_id_before_removal(self) -> None:
        claim = {
            "item_id": "../../outside",
            "workspace": "/tmp/does-not-matter",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
        }
        with mock.patch("shutil.rmtree") as remove:
            with self.assertRaisesRegex(ValueError, "unsafe item id"):
                cron.snapshot_blocked_worker(claim)
        remove.assert_not_called()

    def test_live_app_server_worker_survives_when_identity_is_live_and_goal_verified(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "live")
        with (
            mock.patch.object(cron, "load_claims", return_value=[claim]),
            mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "base\n", "")),
            mock.patch.object(cron, "app_server_worker_is_live", return_value=True),
            mock.patch.object(cron, "goal_runtime_is_verified", return_value=True),
            mock.patch.object(cron, "snapshot_blocked_worker") as snapshot,
            mock.patch.object(cron, "save_claims"),
        ):
            result = cron.refresh_claims([item])
        self.assertEqual(result[0]["status"], "live")
        snapshot.assert_not_called()

    def test_accepted_live_claim_is_stopped_before_release(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[x]",
        }
        claim = self.canonical_claim(item, "live")
        with (
            mock.patch.object(cron, "load_claims", return_value=[claim]),
            mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "base\n", "")),
            mock.patch.object(cron, "app_server_worker_is_live", side_effect=[True, False]),
            mock.patch.object(cron, "terminate_app_server_worker", return_value=True) as terminate,
            mock.patch.object(cron, "save_claims") as save,
            mock.patch.object(cron, "runtime_path", return_value=Path(tempfile.gettempdir()) / "stage1-test-released.jsonl"),
        ):
            result = cron.refresh_claims([item])
        self.assertEqual(result, [])
        terminate.assert_called_once_with(claim)
        save.assert_called_once_with([])

    def test_validate_only_renders_complete_todo_validation_without_writing(self) -> None:
        data = {"items": []}
        todo = cron.DOCS / "todo.md"
        projection = "validated projection\n"
        with (
            mock.patch.object(cron, "run") as run,
            mock.patch.object(cron, "validate_runtime_root") as validate_runtime,
            mock.patch.object(cron, "load_dag", return_value=(data, [])),
            mock.patch.object(cron, "theorem_dag_v2", return_value=({"hard_edges": [], "reuse_hints": []}, {})),
            mock.patch.object(cron, "load_claims", return_value=[]),
            mock.patch.object(cron, "refresh_claims") as refresh,
            mock.patch.object(cron, "space_guard") as space,
            mock.patch.object(
                cron, "render_todo", return_value=(todo, projection)
            ) as render,
            mock.patch.object(cron, "write_todo") as write,
            mock.patch.object(cron, "atomic_write") as atomic,
            mock.patch.object(Path, "exists", return_value=False),
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            cron.validate_only()
        validate_runtime.assert_called_once_with()
        run.assert_called_once_with(
            ["python3", "-B", "Docs/tools/check_stage1_theorem_dag_v2.py"]
        )
        render.assert_called_once_with(data, [], [])
        write.assert_not_called()
        atomic.assert_not_called()
        refresh.assert_not_called()
        space.assert_not_called()
        self.assertIn(
            "todo=Docs/todo.md status=absent_projection_validated",
            output.getvalue(),
        )

    def test_validate_only_rejects_stale_existing_todo_without_rewriting(self) -> None:
        data = {"items": []}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "Docs"
            docs.mkdir()
            todo = docs / "todos_20260717.md"
            todo.write_text("stale projection\n", encoding="utf-8")
            before = todo.read_bytes()
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "DOCS", docs),
                mock.patch.object(cron, "validate_runtime_root"),
                mock.patch.object(cron, "run"),
                mock.patch.object(cron, "load_dag", return_value=(data, [])),
                mock.patch.object(
                    cron,
                    "theorem_dag_v2",
                    return_value=({"hard_edges": [], "reuse_hints": []}, {}),
                ),
                mock.patch.object(cron, "load_claims", return_value=[]),
                mock.patch.object(
                    cron,
                    "render_todo",
                    return_value=(todo, "current projection\n"),
                ),
                mock.patch.object(cron, "atomic_write") as write,
                self.assertRaisesRegex(SystemExit, "daily todo projection is stale"),
            ):
                cron.validate_only()
            self.assertEqual(todo.read_bytes(), before)
            write.assert_not_called()

    def test_validate_only_accepts_current_existing_todo_without_rewriting(self) -> None:
        data = {"items": []}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "Docs"
            docs.mkdir()
            todo = docs / "todos_20260717.md"
            projection = "current projection\n"
            todo.write_text(projection, encoding="utf-8")
            before = todo.stat()
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "DOCS", docs),
                mock.patch.object(cron, "validate_runtime_root"),
                mock.patch.object(cron, "run"),
                mock.patch.object(cron, "load_dag", return_value=(data, [])),
                mock.patch.object(
                    cron,
                    "theorem_dag_v2",
                    return_value=({"hard_edges": [], "reuse_hints": []}, {}),
                ),
                mock.patch.object(cron, "load_claims", return_value=[]),
                mock.patch.object(
                    cron,
                    "render_todo",
                    return_value=(todo, projection),
                ),
                mock.patch.object(cron, "atomic_write") as write,
                contextlib.redirect_stdout(io.StringIO()) as output,
            ):
                cron.validate_only()
            after = todo.stat()
            self.assertEqual(todo.read_text(encoding="utf-8"), projection)
            self.assertEqual((after.st_ino, after.st_mtime_ns), (before.st_ino, before.st_mtime_ns))
            write.assert_not_called()
            self.assertIn("status=current", output.getvalue())

    def test_validate_only_main_does_not_create_runtime_or_migrate_pause(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = root / ".cron" / "stage1-v2-app-server"
            argv = ["stage1_execution_cron.py", "--validate-only"]
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch.object(cron.sys, "argv", argv),
                mock.patch.object(cron, "migrate_pause_marker") as migrate,
                mock.patch.object(cron, "validate_only") as validate,
                mock.patch.object(cron, "runtime_path") as runtime_path,
                mock.patch.object(cron.fcntl, "flock") as flock,
            ):
                cron.main()
            validate.assert_called_once_with()
            migrate.assert_not_called()
            runtime_path.assert_not_called()
            flock.assert_not_called()
            self.assertFalse(runtime.exists())

    def test_preparing_claim_recovers_live_app_server_worker(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "preparing")

        with (
            mock.patch.object(cron, "load_claims", return_value=[claim]),
            mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "base\n", "")),
            mock.patch.object(cron, "app_server_worker_is_live", return_value=True),
            mock.patch.object(cron, "goal_runtime_is_verified", return_value=True),
            mock.patch.object(cron, "save_claims"),
        ):
            result = cron.refresh_claims([item])
        self.assertEqual(result[0]["status"], "live")
        self.assertEqual(result[0]["pid"], 4242)

    def test_preparing_starting_handshake_is_not_killed_before_grace(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "preparing")
        claim["client_started_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
        with (
            mock.patch.object(cron, "load_claims", return_value=[claim]),
            mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "base\n", "")),
            mock.patch.object(cron, "app_server_worker_is_live", return_value=True),
            mock.patch.object(cron, "goal_runtime_is_verified", return_value=False),
            mock.patch.object(cron, "worker_status", return_value={"state": "starting"}),
            mock.patch.object(cron, "terminate_app_server_worker") as terminate,
            mock.patch.object(cron, "save_claims"),
        ):
            result = cron.refresh_claims([item])
        self.assertEqual(result[0]["status"], "preparing")
        terminate.assert_not_called()

    def test_preparing_orphan_child_is_retained_during_handshake_grace(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "preparing")
        claim["pid"] = None
        claim["pid_start_ticks"] = None
        claim["client_started_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
        with (
            mock.patch.object(cron, "load_claims", return_value=[claim]),
            mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "base\n", "")),
            mock.patch.object(cron, "app_server_worker_is_live", return_value=False),
            mock.patch.object(cron, "recover_claim_process_identity", return_value=False),
            mock.patch.object(cron, "app_server_child_is_live", return_value=True),
            mock.patch.object(cron, "worker_status", return_value={"state": "starting"}),
            mock.patch.object(cron, "terminate_app_server_worker") as terminate,
            mock.patch.object(cron, "save_claims"),
        ):
            result = cron.refresh_claims([item])
        self.assertEqual(result[0]["status"], "preparing")
        terminate.assert_not_called()

    def test_preparing_claim_recovers_client_identity_from_starting_status(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "preparing")
        claim["pid"] = None
        claim["pid_start_ticks"] = None
        with (
            mock.patch.object(cron, "worker_status", return_value={"client_pid": 7654, "client_start_ticks": 4321}),
            mock.patch.object(cron, "app_server_worker_is_live", side_effect=lambda row: row.get("pid") == 7654 and row.get("pid_start_ticks") == 4321),
        ):
            self.assertTrue(cron.recover_claim_process_identity(claim))
        self.assertEqual(claim["pid"], 7654)
        self.assertEqual(claim["pid_start_ticks"], 4321)

    def test_handshake_timeout_terminates_live_client_fail_closed(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "preparing")
        claims = [claim]
        with (
            mock.patch.object(cron, "goal_runtime_is_verified", return_value=False),
            mock.patch.object(cron, "worker_status", return_value={"state": "starting"}),
            mock.patch.object(cron, "app_server_worker_is_live", return_value=True),
            mock.patch.object(cron, "terminate_app_server_worker", return_value=True) as terminate,
            mock.patch.object(cron, "save_claims") as save,
        ):
            count = cron.confirm_goal_handshakes(claims, [claim], timeout_seconds=0)
        self.assertEqual(count, 0)
        self.assertEqual(claim["status"], "launch_failed")
        self.assertTrue(claim["process_terminated_after_handshake_timeout"])
        terminate.assert_called_once_with(claim)
        save.assert_called()

    def test_handshake_timeout_terminates_verified_orphan_child(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "preparing")
        claim["pid"] = None
        claim["pid_start_ticks"] = None
        claims = [claim]
        with (
            mock.patch.object(cron, "goal_runtime_is_verified", return_value=False),
            mock.patch.object(cron, "worker_status", return_value={"state": "starting"}),
            mock.patch.object(cron, "app_server_worker_is_live", return_value=False),
            mock.patch.object(cron, "app_server_child_is_live", return_value=True),
            mock.patch.object(cron, "terminate_app_server_worker", return_value=True) as terminate,
            mock.patch.object(cron, "save_claims"),
        ):
            count = cron.confirm_goal_handshakes(claims, [claim], timeout_seconds=0)
        self.assertEqual(count, 0)
        self.assertTrue(claim["process_terminated_after_handshake_timeout"])
        terminate.assert_called_once_with(claim)

    def test_terminate_verified_orphan_child_does_not_require_client_pid(self) -> None:
        claim: dict[str, object] = {"pid": None}
        with (
            mock.patch.object(cron, "app_server_worker_is_live", return_value=False),
            mock.patch.object(cron, "app_server_child_is_live", return_value=True),
            mock.patch.object(
                cron,
                "worker_status",
                return_value={"app_server_pid": 9876, "app_server_start_ticks": 55},
            ),
            mock.patch.object(cron.os, "killpg") as killpg,
            mock.patch.object(cron, "pid_alive", return_value=False),
        ):
            self.assertTrue(cron.terminate_app_server_worker(claim))
        killpg.assert_called_once_with(9876, 15)

    def test_failed_preparing_claim_releases_for_retry(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "launch_failed")
        with tempfile.TemporaryDirectory() as directory:
            test_root = Path(directory)
            test_runtime = test_root / ".cron" / "stage1-rev56"
            claim["workspace"] = str(test_runtime / "workers" / "slot1")
            claim_id = str(claim["claim_id"])
            claim["output_log"] = str(test_runtime / "logs" / f"{claim_id}.out")
            claim["app_server_status"] = str(test_runtime / "app-server" / f"{claim_id}.json")
            claim["goal_objective_path"] = str(test_runtime / "goals" / f"{claim_id}.txt")
            with (
                mock.patch.object(cron, "ROOT", test_root),
                mock.patch.object(cron, "RUNTIME", test_runtime),
                mock.patch.object(cron, "load_claims", return_value=[claim]),
                mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "base\n", "")),
                mock.patch.object(cron, "app_server_worker_is_live", return_value=False),
                mock.patch.object(cron, "save_claims") as save,
                mock.patch.object(cron, "runtime_path", return_value=Path(tempfile.gettempdir()) / "stage1-test-launch-released.jsonl"),
            ):
                result = cron.refresh_claims([item])
        self.assertEqual(result, [])
        save.assert_called_once_with([])

    def test_refresh_quarantines_duplicate_runtime_identity(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claims = [self.canonical_claim(item, "live"), self.canonical_claim(item, "live")]
        with (
            mock.patch.object(cron, "load_claims", return_value=claims),
            mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "base\n", "")),
            mock.patch.object(cron, "app_server_worker_is_live") as is_live,
            mock.patch.object(cron, "save_claims"),
        ):
            result = cron.refresh_claims([item])
        self.assertEqual([claim["status"] for claim in result], ["quarantined", "quarantined"])
        is_live.assert_not_called()

    def test_prepare_workspace_rejects_symlink_slot_before_removal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            runtime = root / ".cron" / "stage1-rev56"
            outside = Path(directory) / "outside"
            (runtime / "workers").mkdir(parents=True)
            outside.mkdir()
            (runtime / "workers" / "slot1").symlink_to(outside, target_is_directory=True)
            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "RUNTIME", runtime),
                mock.patch("shutil.rmtree") as remove,
            ):
                with self.assertRaisesRegex(SystemExit, "symlink"):
                    cron.prepare_workspace(1)
            remove.assert_not_called()

    def test_noncanonical_claim_cannot_touch_unrelated_process(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[x]",
        }
        claim = self.canonical_claim(item, "live")
        claim["app_server_status"] = "/tmp/unrelated.json"
        with (
            mock.patch.object(cron, "load_claims", return_value=[claim]),
            mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "base\n", "")),
            mock.patch.object(cron, "app_server_worker_is_live") as is_live,
            mock.patch.object(cron, "terminate_app_server_worker") as terminate,
            mock.patch.object(cron, "save_claims"),
        ):
            result = cron.refresh_claims([item])
        self.assertEqual(result[0]["status"], "quarantined")
        is_live.assert_not_called()
        terminate.assert_not_called()

    def test_draining_claim_retries_without_releasing_live_app_server_worker(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "draining")
        with (
            mock.patch.object(cron, "load_claims", return_value=[claim]),
            mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "base\n", "")),
            mock.patch.object(cron, "app_server_worker_is_live", return_value=True),
            mock.patch.object(cron, "terminate_app_server_worker", return_value=False) as terminate,
            mock.patch.object(cron, "save_claims"),
        ):
            result = cron.refresh_claims([item])
        self.assertEqual(result[0]["status"], "draining")
        self.assertIn("drain_retried_at", result[0])
        terminate.assert_called_once_with(claim)


class CheckpointManifestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.sandbox = Path(self.temporary.name)
        self.root = self.sandbox / "repo"
        self.remote = self.sandbox / "remote.git"
        subprocess.run(["git", "init", "-q", "--bare", str(self.remote)], check=True)
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.root)], check=True)
        subprocess.run(["git", "config", "user.name", "Stage1 Test"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.root, check=True)
        (self.root / "Stage1_Instances" / "THM-M-0001").mkdir(parents=True)
        self.relative = "Stage1_Instances/THM-M-0001/evidence.json"
        self.target = self.root / self.relative
        self.target.write_text('{"theorem_id":"THM-M-0001","value":"base"}\n', encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "base"], cwd=self.root, check=True)
        subprocess.run(["git", "remote", "add", "origin", str(self.remote)], cwd=self.root, check=True)
        subprocess.run(["git", "push", "-qu", "origin", "main"], cwd=self.root, check=True)
        self.runtime = self.root / ".cron" / "stage1-rev56"
        self.runtime.mkdir(parents=True)
        self.pause = self.sandbox / "PAUSED"
        pause_patcher = mock.patch.object(cron, "PAUSE_FILE", self.pause)
        pause_patcher.start()
        self.addCleanup(pause_patcher.stop)

    def write_pending(self) -> dict[str, object]:
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        pending = {
            "schema_version": "stage1-pending-checkpoint/1.0",
            "base_revision": base,
            "state": "integrated_uncommitted",
            "paths": [{"path": self.relative, "sha256": sha256(self.target), "mode": "100644"}],
            "created_at": "2026-07-16T00:00:00+00:00",
        }
        (self.runtime / "pending_checkpoint.json").write_text(
            json.dumps(pending) + "\n", encoding="utf-8"
        )
        return pending

    def checkpoint(self) -> None:
        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
        ):
            cron.checkpoint_integration()

    def upstream(self) -> str:
        return subprocess.check_output(
            ["git", "rev-parse", "@{u}"], cwd=self.root, text=True
        ).strip()

    def test_checkpoint_rejects_bytes_changed_after_validation(self) -> None:
        self.target.write_text('{"theorem_id":"THM-M-0001","value":"validated"}\n', encoding="utf-8")
        self.write_pending()
        self.target.write_text('{"theorem_id":"THM-M-0001","value":"raced"}\n', encoding="utf-8")
        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
        ):
            with self.assertRaisesRegex(SystemExit, "changed after validation"):
                cron.checkpoint_integration()

    def test_checkpoint_refuses_pause_before_staging(self) -> None:
        self.target.write_text('{"theorem_id":"THM-M-0001","value":"validated"}\n', encoding="utf-8")
        self.write_pending()
        pause = self.sandbox / "PAUSED"
        pause.write_text("paused\n", encoding="utf-8")
        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(cron, "PAUSE_FILE", pause),
            self.assertRaisesRegex(SystemExit, "checkpoint refused"),
        ):
            cron.checkpoint_integration()
        self.assertEqual(
            subprocess.check_output(
                ["git", "diff", "--cached", "--name-only"], cwd=self.root, text=True
            ).strip(),
            "",
        )

    def test_checkpoint_rejects_partial_state_surface_manifest(self) -> None:
        relative = "Docs/Stage1_Blueprint_v2.md"
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("authoritative state\n", encoding="utf-8")
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        pending = {
            "schema_version": "stage1-pending-checkpoint/1.0",
            "base_revision": base,
            "state": "integrated_uncommitted",
            "paths": [{"path": relative, "sha256": sha256(target), "mode": "100644"}],
        }
        (self.runtime / "pending_checkpoint.json").write_text(json.dumps(pending) + "\n")
        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            self.assertRaisesRegex(SystemExit, "both state projections"),
        ):
            cron.checkpoint_integration()

    def test_theorem_projection_only_checkpoint_runs_semantic_validator(self) -> None:
        relative = "Docs/Stage1_Theorem_DAG_v2.json"
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text('{"projection":"blocked-only"}\n', encoding="utf-8")
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        pending = {
            "schema_version": "stage1-pending-checkpoint/1.0",
            "base_revision": base,
            "state": "integrated_uncommitted",
            "paths": [{"path": relative, "sha256": sha256(target), "mode": "100644"}],
        }
        (self.runtime / "pending_checkpoint.json").write_text(json.dumps(pending) + "\n")
        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(cron, "load_dag", return_value=({}, [])) as load_dag,
            mock.patch.object(cron, "run", side_effect=SystemExit("semantic validator invoked")) as run,
            self.assertRaisesRegex(SystemExit, "semantic validator invoked"),
        ):
            cron.checkpoint_integration()
        load_dag.assert_called_once_with()
        self.assertEqual(
            run.call_args.args[0],
            ["python3", "Docs/tools/check_stage1_theorem_dag_v2.py"],
        )

    def test_push_failure_leaves_retryable_committed_manifest(self) -> None:
        self.target.write_text('{"theorem_id":"THM-M-0001","value":"validated"}\n', encoding="utf-8")
        self.write_pending()
        real_run = cron.run

        def fail_push(command: list[str], **kwargs):
            if command[:2] == ["git", "push"]:
                raise SystemExit("injected push failure")
            return real_run(command, **kwargs)

        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(cron, "run", side_effect=fail_push),
        ):
            with self.assertRaisesRegex(SystemExit, "push failure"):
                cron.checkpoint_integration()
        pending = json.loads((self.runtime / "pending_checkpoint.json").read_text(encoding="utf-8"))
        self.assertEqual(pending["state"], "committed_unpushed")
        self.assertEqual(
            pending["commit_revision"],
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip(),
        )

        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
        ):
            cron.checkpoint_integration()
        self.assertFalse((self.runtime / "pending_checkpoint.json").exists())
        self.assertEqual(self.upstream(), pending["commit_revision"])

    def test_checkpoint_rejects_staged_substitution_after_manifest_check(self) -> None:
        validated = '{"theorem_id":"THM-M-0001","value":"validated"}\n'
        self.target.write_text(validated, encoding="utf-8")
        self.write_pending()
        real_run = cron.run
        substituted = False

        def replace_before_add(command: list[str], **kwargs):
            nonlocal substituted
            if command[:2] == ["git", "add"] and not substituted:
                substituted = True
                self.target.write_text(
                    '{"theorem_id":"THM-M-0001","value":"substituted"}\n',
                    encoding="utf-8",
                )
            return real_run(command, **kwargs)

        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(cron, "run", side_effect=replace_before_add),
        ):
            with self.assertRaisesRegex(SystemExit, "staged bytes"):
                cron.checkpoint_integration()
        self.assertEqual(
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip(),
            json.loads((self.runtime / "pending_checkpoint.json").read_text())["base_revision"],
        )

    def test_checkpoint_rejects_worktree_change_after_staging(self) -> None:
        self.target.write_text('{"theorem_id":"THM-M-0001","value":"validated"}\n', encoding="utf-8")
        self.write_pending()
        real_git_object_bytes = cron.git_object_bytes
        changed = False

        def race_after_index_read(object_name: str, **kwargs):
            nonlocal changed
            data = real_git_object_bytes(object_name, **kwargs)
            if object_name == f":{self.relative}" and not changed:
                changed = True
                self.target.write_text(
                    '{"theorem_id":"THM-M-0001","value":"after-stage-race"}\n',
                    encoding="utf-8",
                )
            return data

        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(cron, "git_object_bytes", side_effect=race_after_index_read),
        ):
            with self.assertRaisesRegex(SystemExit, "worktree changed after staging"):
                cron.checkpoint_integration()

    def test_commit_success_before_journal_update_recovers_and_pushes(self) -> None:
        self.target.write_text('{"theorem_id":"THM-M-0001","value":"validated"}\n', encoding="utf-8")
        pending = self.write_pending()
        subprocess.run(["git", "add", "--", self.relative], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "Integrate Stage1 worker evidence batch"], cwd=self.root, check=True)
        committed = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        self.checkpoint()
        self.assertFalse((self.runtime / "pending_checkpoint.json").exists())
        self.assertEqual(self.upstream(), committed)
        self.assertNotEqual(pending["base_revision"], committed)

    def test_already_pushed_commit_is_idempotently_finalized(self) -> None:
        self.target.write_text('{"theorem_id":"THM-M-0001","value":"validated"}\n', encoding="utf-8")
        pending = self.write_pending()
        subprocess.run(["git", "add", "--", self.relative], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "Integrate Stage1 worker evidence batch"], cwd=self.root, check=True)
        committed = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        pending["state"] = "committed_unpushed"
        pending["commit_revision"] = committed
        (self.runtime / "pending_checkpoint.json").write_text(json.dumps(pending) + "\n")
        subprocess.run(["git", "push", "-q", "origin", "main"], cwd=self.root, check=True)
        self.checkpoint()
        self.assertFalse((self.runtime / "pending_checkpoint.json").exists())
        self.assertEqual(self.upstream(), committed)

    def test_recovery_rejects_same_bytes_with_changed_file_mode(self) -> None:
        self.target.write_text('{"theorem_id":"THM-M-0001","value":"validated"}\n', encoding="utf-8")
        self.write_pending()
        self.target.chmod(0o755)
        subprocess.run(["git", "add", "--", self.relative], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "mode-only checkpoint attack"], cwd=self.root, check=True)
        self.target.chmod(0o644)
        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
        ):
            with self.assertRaisesRegex(SystemExit, "file mode"):
                cron.checkpoint_integration()

    def test_push_uses_content_bound_oid_not_mutable_main_ref(self) -> None:
        self.target.write_text('{"theorem_id":"THM-M-0001","value":"validated"}\n', encoding="utf-8")
        pending = self.write_pending()
        subprocess.run(["git", "add", "--", self.relative], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "validated checkpoint"], cwd=self.root, check=True)
        validated = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        pending["state"] = "committed_unpushed"
        pending["commit_revision"] = validated
        (self.runtime / "pending_checkpoint.json").write_text(json.dumps(pending) + "\n")
        real_run = cron.run
        attacked = False

        def advance_main_before_push(command: list[str], **kwargs):
            nonlocal attacked
            if command[:2] == ["git", "push"] and not attacked:
                attacked = True
                (self.root / "attacker.txt").write_text("unvalidated\n")
                subprocess.run(["git", "add", "attacker.txt"], cwd=self.root, check=True)
                subprocess.run(["git", "commit", "-qm", "unvalidated descendant"], cwd=self.root, check=True)
            return real_run(command, **kwargs)

        with (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(cron, "run", side_effect=advance_main_before_push),
        ):
            cron.checkpoint_integration()
        self.assertEqual(self.upstream(), validated)
        self.assertFalse((self.runtime / "pending_checkpoint.json").exists())


class TheoremDagRegenerationTests(unittest.TestCase):
    @staticmethod
    def load_generator(module_name: str):
        generator_path = CRON_PATH.parents[1] / "Docs" / "tools" / "generate_stage1_theorem_dag_v2.py"
        spec = importlib.util.spec_from_file_location(module_name, generator_path)
        if spec is None or spec.loader is None:
            raise AssertionError(f"cannot load {generator_path}")
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
        return generator

    def test_generator_reads_state_from_blueprint_not_execution_dag(self) -> None:
        generator = self.load_generator("stage1_theorem_dag_ssot_test")
        source = cron.BLUEPRINT.read_text(encoding="utf-8")
        row = re.search(r"^- (\[[_x ]\]) (`S56-M-0387-INTAKE`)", source, re.MULTILINE)
        self.assertIsNotNone(row)
        assert row is not None
        mutated_state = "[ ]" if row.group(1) != "[ ]" else "[_]"
        mutated = re.sub(
            r"^- \[[_x ]\] (`S56-M-0387-INTAKE`)",
            f"- {mutated_state} \\1",
            source,
            count=1,
            flags=re.MULTILINE,
        )
        mutated = refresh_blueprint_progress_summary(mutated)
        with tempfile.TemporaryDirectory() as directory:
            blueprint = Path(directory) / "Stage1_Blueprint_v2.md"
            blueprint.write_text(mutated, encoding="utf-8")
            with mock.patch.object(generator, "BLUEPRINT", blueprint):
                items = generator.blueprint_state_items()
        self.assertEqual(items[0]["state"], mutated_state)

    def test_regeneration_and_dependency_context_digests_are_stable(self) -> None:
        generator = self.load_generator("stage1_theorem_dag_generator_under_test")
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "Stage1_Theorem_DAG_v2.json"
            with (
                mock.patch.object(generator, "OUTPUT", output),
                mock.patch.object(generator, "inventory", side_effect=lambda theorem_id: ({
                    "instance_directory": f"Stage1_Instances/{theorem_id}",
                    "instance_directory_exists": False,
                    "lean_sources": [],
                    "receipt_files": [],
                    "structured_json_files": [],
                }, [])),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                first_data = generator.build()
                first = json.dumps(first_data, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
                second_data = generator.build()
                second = json.dumps(second_data, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
        self.assertEqual(first, second)
        first_contexts = {
            row["theorem_id"]: row["dependency_context_sha256"] for row in first_data["theorems"]
        }
        second_contexts = {
            row["theorem_id"]: row["dependency_context_sha256"] for row in second_data["theorems"]
        }
        self.assertEqual(first_contexts, second_contexts)
        self.assertEqual(len(first_contexts), 1546)

    def test_v2_order_and_complete_ancestor_closure_are_deterministic(self) -> None:
        generator = self.load_generator("stage1_theorem_dag_topology_contract_test")
        theorem_ids = {"THM-M-0001", "THM-M-0002", "THM-M-0003", "THM-M-0004"}
        edges = [
            {"parent_theorem_id": "THM-M-0001", "child_theorem_id": "THM-M-0003"},
            {"parent_theorem_id": "THM-M-0002", "child_theorem_id": "THM-M-0003"},
            {"parent_theorem_id": "THM-M-0003", "child_theorem_id": "THM-M-0004"},
        ]
        buckets = {theorem_id: "partial" for theorem_id in theorem_ids}
        original_ranks = {
            "THM-M-0001": 2,
            "THM-M-0002": 1,
            "THM-M-0003": 4,
            "THM-M-0004": 3,
        }

        first = generator.topological_metadata(theorem_ids, edges, buckets, original_ranks)
        second = generator.topological_metadata(set(reversed(sorted(theorem_ids))), list(reversed(edges)), buckets, original_ranks)
        self.assertEqual(first, second)
        order, layers, parents, _, ancestors = first
        self.assertEqual(order, ["THM-M-0002", "THM-M-0001", "THM-M-0003", "THM-M-0004"])
        self.assertEqual(parents["THM-M-0004"], ["THM-M-0003"])
        self.assertEqual(ancestors["THM-M-0004"], ["THM-M-0002", "THM-M-0001", "THM-M-0003"])
        self.assertEqual(layers["THM-M-0004"], 2)
        rank = {theorem_id: index for index, theorem_id in enumerate(order)}
        self.assertTrue(all(rank[ancestor] < rank["THM-M-0004"] for ancestor in ancestors["THM-M-0004"]))

    def test_generated_execution_contract_requires_checked_transport_without_inherited_acceptance(self) -> None:
        generator = self.load_generator("stage1_theorem_dag_execution_contract_test")
        contract = generator.EXECUTION_CONTRACT
        self.assertEqual(contract["claim_order"], ["v2_execution_rank", "phase_layer", "phase_item_id"])
        self.assertEqual(
            contract["proof_parent_inspection"]["scope"],
            ["direct_hard_parents", "transitive_hard_ancestors"],
        )
        self.assertTrue(contract["proof_parent_inspection"]["complete_closure_required"])
        self.assertIn("checked_transport", contract["accepted_reuse_relationships"])
        self.assertIn("consumer_owned_import_or_wrapper", contract["checked_transport_requires"])
        self.assertIn("consumer_validation_receipt", contract["checked_transport_requires"])
        self.assertTrue(contract["provider_checkbox_state_is_observation_only"])
        self.assertFalse(contract["provider_acceptance_inherited"])
        self.assertTrue(contract["consumer_acceptance_required"])


if __name__ == "__main__":
    unittest.main()
