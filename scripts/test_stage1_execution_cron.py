#!/usr/bin/env python3
"""Focused regression tests for the Stage1 v2 dependency/reuse gate."""

from __future__ import annotations

import copy
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

CRON_PATH = Path(__file__).with_name("stage1_execution_cron.py")
CRON_SPEC = importlib.util.spec_from_file_location("stage1_execution_cron_under_test", CRON_PATH)
if CRON_SPEC is None or CRON_SPEC.loader is None:
    raise RuntimeError(f"cannot load {CRON_PATH}")
cron = importlib.util.module_from_spec(CRON_SPEC)
CRON_SPEC.loader.exec_module(cron)


CHILD = "THM-M-0990"
PARENT = "THM-M-0989"
EDGE = "HARD-THM-M-0989-THM-M-0990-PROOF"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
        self.dag_patch = mock.patch.object(cron, "DAG", self.dag_path)
        self.dag_patch.start()
        self.addCleanup(self.dag_patch.stop)
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
        status_dag.parent.mkdir(parents=True)
        status_dag.write_bytes(self.dag_path.read_bytes())
        status_graph.write_bytes(cron.THEOREM_DAG_V2.read_bytes())
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
        self.runtime = self.master / ".cron" / "stage1-rev56"
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
            "session": "stage1r56-1-0001",
            "output_log": str(self.runtime / "logs" / f"{self.item['id']}.out"),
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
        self.blueprint = self.docs / "Stage1_Blueprint_rev-5.6.md"
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
            stack.enter_context(mock.patch.object(cron, "write_projection", side_effect=projection))
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
            outside = self.sandbox / "outside.md"
            outside.write_text("THM-M-0001 blocked\n", encoding="utf-8")
            link = owned_snapshot / "linked.md"
            link.symlink_to(outside)
            with self.assertRaisesRegex(ValueError, "regular file"):
                cron.contained_regular_file(snapshot, f"{self.owner}/linked.md", self.owner)
            with self.assertRaisesRegex(ValueError, "scheduler-owned"):
                cron.validated_blocked_snapshot(self.item["id"], str(self.sandbox))

    def test_invalid_attempts_fail_before_worker_files_are_copied(self) -> None:
        data = copy.deepcopy(cron.read_json(cron.DAG))
        data["items"][0]["attempts"] = None
        with self.assertRaisesRegex(SystemExit, "invalid attempts"):
            cron.validate_dag(data)
        self.assertEqual((self.master / self.existing_relative).read_bytes(), self.master_existing)

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
    @staticmethod
    def canonical_claim(item: dict[str, object], status: str) -> dict[str, object]:
        _, theorem_nodes = cron.theorem_dag_v2()
        slot = 1
        return {
            "item_id": item["id"],
            "theorem_id": item["theorem_id"],
            "owned_paths": item["owned_paths"],
            "status": status,
            "slot": slot,
            "session": f"stage1r56-{slot}-{theorem_nodes[str(item['theorem_id'])]['v2_execution_rank']:04d}",
            "workspace": str(cron.RUNTIME / "workers" / f"slot{slot}"),
            "output_log": str(cron.RUNTIME / "logs" / f"{item['id']}.out"),
        }

    def test_finished_handoffs_do_not_consume_live_capacity(self) -> None:
        live = [{"status": "live", "slot": slot} for slot in range(1, 41)]
        finished = [{"status": "finished", "slot": slot} for slot in range(41, 81)]
        claims = live + finished
        reservations = [claim for claim in claims if claim["status"] in {"live", "finished"}]
        occupied = {claim["slot"] for claim in reservations}
        capacity = max(0, 80 - len(live))
        available = [
            slot
            for slot in range(1, 80 + len(reservations) + 1)
            if slot not in occupied
        ][:capacity]
        self.assertEqual(capacity, 40)
        self.assertEqual(available, list(range(81, 121)))

    def test_invalid_integration_limit_has_no_refresh_side_effects(self) -> None:
        with mock.patch.object(cron, "refresh_claims") as refresh:
            with self.assertRaisesRegex(SystemExit, "--limit must be"):
                cron.integrate(cron.MAX_WORKERS + 1)
        refresh.assert_not_called()

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
            "session": "hostile",
        }
        with (
            mock.patch.object(cron, "load_claims", return_value=[hostile]),
            mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "base\n", "")),
            mock.patch.object(cron, "pid_alive") as pid_alive,
            mock.patch.object(cron, "session_is_live") as session_is_live,
            mock.patch.object(cron, "snapshot_blocked_worker") as snapshot,
            mock.patch.object(cron, "save_claims") as save,
        ):
            result = cron.refresh_claims([item])
        self.assertEqual(result[0]["status"], "quarantined")
        pid_alive.assert_not_called()
        session_is_live.assert_not_called()
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

    def test_live_tmux_session_survives_missing_pid(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "live")
        claim["pid"] = None
        with (
            mock.patch.object(cron, "load_claims", return_value=[claim]),
            mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "base\n", "")),
            mock.patch.object(cron, "session_is_live", return_value=True),
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
        responses = iter([True, False])

        def fake_run(command: list[str], **kwargs):
            return subprocess.CompletedProcess(command, 0, "base\n", "")

        with (
            mock.patch.object(cron, "load_claims", return_value=[claim]),
            mock.patch.object(cron, "run", side_effect=fake_run) as run,
            mock.patch.object(cron, "session_is_live", side_effect=lambda session: next(responses)),
            mock.patch.object(cron, "save_claims") as save,
            mock.patch.object(cron, "runtime_path", return_value=Path(tempfile.gettempdir()) / "stage1-test-released.jsonl"),
        ):
            result = cron.refresh_claims([item])
        self.assertEqual(result, [])
        self.assertTrue(any(call.args[0][:2] == ["tmux", "kill-session"] for call in run.call_args_list))
        save.assert_called_once_with([])

    def test_validate_only_does_not_refresh_or_apply_space_guard(self) -> None:
        data = {"items": []}
        with (
            mock.patch.object(cron, "run"),
            mock.patch.object(cron, "load_dag", return_value=(data, [])),
            mock.patch.object(cron, "theorem_dag_v2", return_value=({"hard_edges": [], "reuse_hints": []}, {})),
            mock.patch.object(cron, "load_claims", return_value=[]),
            mock.patch.object(cron, "refresh_claims") as refresh,
            mock.patch.object(cron, "space_guard") as space,
            mock.patch.object(cron, "write_todo", return_value=cron.DOCS / "todo.md"),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            cron.validate_only()
        refresh.assert_not_called()
        space.assert_not_called()

    def test_preparing_claim_recovers_live_session(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "preparing")

        def fake_run(command: list[str], **kwargs):
            output = "4242\n" if command[:2] == ["tmux", "list-panes"] else "base\n"
            return subprocess.CompletedProcess(command, 0, output, "")

        with (
            mock.patch.object(cron, "load_claims", return_value=[claim]),
            mock.patch.object(cron, "run", side_effect=fake_run),
            mock.patch.object(cron, "session_is_live", return_value=True),
            mock.patch.object(cron, "save_claims"),
        ):
            result = cron.refresh_claims([item])
        self.assertEqual(result[0]["status"], "live")
        self.assertEqual(result[0]["pid"], 4242)

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
            claim["output_log"] = str(test_runtime / "logs" / f"{item['id']}.out")
            with (
                mock.patch.object(cron, "ROOT", test_root),
                mock.patch.object(cron, "RUNTIME", test_runtime),
                mock.patch.object(cron, "load_claims", return_value=[claim]),
                mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "base\n", "")),
                mock.patch.object(cron, "session_is_live", return_value=False),
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
            mock.patch.object(cron, "session_is_live") as session_is_live,
            mock.patch.object(cron, "save_claims"),
        ):
            result = cron.refresh_claims([item])
        self.assertEqual([claim["status"] for claim in result], ["quarantined", "quarantined"])
        session_is_live.assert_not_called()

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

    def test_noncanonical_claim_cannot_touch_unrelated_session(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[x]",
        }
        claim = self.canonical_claim(item, "live")
        claim["session"] = "unrelated-session"
        with (
            mock.patch.object(cron, "load_claims", return_value=[claim]),
            mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "base\n", "")) as run,
            mock.patch.object(cron, "session_is_live") as session_is_live,
            mock.patch.object(cron, "save_claims"),
        ):
            result = cron.refresh_claims([item])
        self.assertEqual(result[0]["status"], "quarantined")
        session_is_live.assert_not_called()
        self.assertFalse(any(call.args[0][:2] == ["tmux", "kill-session"] for call in run.call_args_list))

    def test_draining_claim_retries_without_releasing_live_session(self) -> None:
        item = {
            "id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
            "state": "[ ]",
        }
        claim = self.canonical_claim(item, "draining")
        with (
            mock.patch.object(cron, "load_claims", return_value=[claim]),
            mock.patch.object(cron, "run", return_value=subprocess.CompletedProcess([], 0, "base\n", "")) as run,
            mock.patch.object(cron, "session_is_live", return_value=True),
            mock.patch.object(cron, "save_claims"),
        ):
            result = cron.refresh_claims([item])
        self.assertEqual(result[0]["status"], "draining")
        self.assertIn("drain_retried_at", result[0])
        self.assertTrue(any(call.args[0][:2] == ["tmux", "kill-session"] for call in run.call_args_list))


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
    def test_regeneration_and_dependency_context_digests_are_stable(self) -> None:
        generator_path = CRON_PATH.parents[1] / "Docs" / "tools" / "generate_stage1_theorem_dag_v2.py"
        spec = importlib.util.spec_from_file_location("stage1_theorem_dag_generator_under_test", generator_path)
        if spec is None or spec.loader is None:
            self.fail(f"cannot load {generator_path}")
        generator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator)
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


if __name__ == "__main__":
    unittest.main()
