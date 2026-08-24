#!/usr/bin/env python3
"""Negative conformance tests for the Stage5.1 organization release gate."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "Docs/tools/check_stage5_1_organization_release.py"
COMMON_PATH = ROOT / "Docs/tools/stage5_1_common.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("stage5_1_release_mutation_checker", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = load_checker()


def load_common():
    spec = importlib.util.spec_from_file_location("stage5_1_registry_common", COMMON_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {COMMON_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


common = load_common()


class Stage51SubjectIDRegistryTests(unittest.TestCase):
    @staticmethod
    def node(notation: str, subject_id: str) -> dict:
        return {
            "subject_id": subject_id, "subject_key": "fixture." + notation.lower(),
            "scheme": "MSC", "edition": "2020", "notation": notation,
        }

    def test_reorder_and_insert_preserve_ids_and_append_after_max(self) -> None:
        initial_nodes = [self.node("00-XX", "S51-SUB-00000007"),
                         self.node("01-XX", "S51-SUB-00000011")]
        _, registry = common.assign_subject_node_ids(initial_nodes)
        reordered = [initial_nodes[1], self.node("02-XX", "ignored"), initial_nodes[0]]
        assigned, successor = common.assign_subject_node_ids(reordered, registry)
        by_notation = {row["notation"]: row["subject_id"] for row in assigned}
        self.assertEqual(by_notation["00-XX"], "S51-SUB-00000007")
        self.assertEqual(by_notation["01-XX"], "S51-SUB-00000011")
        self.assertEqual(by_notation["02-XX"], "S51-SUB-00000012")
        self.assertEqual(len(successor), 3)

    def test_duplicate_registry_is_rejected(self) -> None:
        nodes = [self.node("00-XX", "S51-SUB-00000001")]
        _, registry = common.assign_subject_node_ids(nodes)
        duplicate = registry + [dict(registry[0])]
        with self.assertRaisesRegex(common.Stage51Error, "duplicate stable key or subject ID"):
            common.assign_subject_node_ids(nodes, duplicate)

    def test_stale_registry_is_rejected(self) -> None:
        nodes = [self.node("00-XX", "S51-SUB-00000001"),
                 self.node("01-XX", "S51-SUB-00000002")]
        _, registry = common.assign_subject_node_ids(nodes)
        with self.assertRaisesRegex(common.Stage51Error, "stale predecessor"):
            common.assign_subject_node_ids(nodes[:1], registry)


class Stage51OrganizationCursorContractTests(unittest.TestCase):
    @staticmethod
    def seal(body: dict) -> dict:
        value = dict(body)
        value["authority_sha256"] = checker.sha256_bytes(checker.canonical_json(value))
        return value

    def test_activation_receipt_object_is_schema_and_seal_checked(self) -> None:
        digest = "1" * 64
        receipt = self.seal({
            "schema_version": "awesome-theorems/stage5-1-activation-fence/1.0",
            "organization_release": "1.0",
            "status": "accepted",
            "predecessor_fence": {
                "path": "Docs/evidence/stage5_1_shared_execution/predecessor-fence.json",
                "sha256": "2" * 64,
                "authority_sha256": "3" * 64,
            },
            "boot_acceptance": {
                "theorems": {
                    "item_id": "S51THM-BOOT-001",
                    "pre_blueprint_sha256": digest,
                    "post_blueprint_sha256": digest,
                    "post_gantt_sha256": digest,
                    "review_receipt_sha256": digest,
                },
                "conjectures": {
                    "item_id": "S51CON-BOOT-001",
                    "pre_blueprint_sha256": digest,
                    "post_blueprint_sha256": digest,
                    "post_gantt_sha256": digest,
                    "review_receipt_sha256": digest,
                },
            },
        })
        self.assertEqual(
            checker._activation_receipt_value(ROOT, receipt, "1.0"), receipt,
        )
        broken = dict(receipt, authority_sha256="0" * 64)
        with self.assertRaisesRegex(checker.ReleaseCheckError, "authority_sha256 mismatch"):
            checker._activation_receipt_value(ROOT, broken, "1.0")

    def test_boot_cursor_and_independent_gantt_projection_are_exact(self) -> None:
        boot = "S51THM-BOOT-001"
        initial_blueprint = (
            f"- [ ] `{boot}` BOOT | depends_on=- | owned_paths=- | gate=review\n"
            "- [ ] `S51THM-00000001-TARGET` member | "
            f"depends_on={boot} | owned_paths=x | gate=member\n"
        ).encode()
        current_blueprint = initial_blueprint.replace(
            f"- [ ] `{boot}`".encode(), f"- [x] `{boot}`".encode(),
        )
        checker._accepted_blueprint(
            initial_blueprint, current_blueprint, boot, "fixture Blueprint",
        )
        with self.assertRaisesRegex(checker.ReleaseCheckError, "exactly BOOT"):
            checker._accepted_blueprint(
                initial_blueprint, current_blueprint + b"drift\n", boot,
                "fixture Blueprint",
            )

        initial_gantt = (
            "| Item | Mapping | State | Timing |\n"
            "|---|---|---|---|\n"
            f"| `{boot}` | control successor | not_done | unscheduled |\n\n"
            "```json\n"
            + json.dumps({
                "blueprint_path": "Docs/Stage5_1_Theorems_Blueprint.md",
                "blueprint_sha256": checker.sha256_bytes(initial_blueprint),
                "activation_status": "blocked",
            }, sort_keys=True, indent=2)
            + "\n```\n"
        ).encode()
        post_digest = checker.sha256_bytes(current_blueprint)
        rendered = checker._rerender_accepted_gantt(
            initial_gantt, boot, post_digest, "fixture Gantt",
        ).decode()
        self.assertIn(f"| `{boot}` | control successor | master_accepted |", rendered)
        metadata = checker.strict_json(
            checker.JSON_FENCE_RE.search(rendered).group("body").encode(),
            "fixture metadata",
        )
        self.assertEqual(metadata["blueprint_sha256"], post_digest)
        self.assertEqual(metadata["activation_status"], "blocked")

    def test_hard_edge_typed_receipt_schemas_require_authority_and_replay(self) -> None:
        schema_root = ROOT / "Docs/catalog/stage5_1_organization/schemas"
        schemas = {
            path.name: checker.strict_json(path.read_bytes(), path.name)
            for path in schema_root.glob("*.schema.json")
        }
        common = schemas["common.schema.json"]
        store = {candidate["$id"]: candidate for candidate in schemas.values()}
        artifact = {
            "path": "provider/artifact.bin", "sha256": "1" * 64,
            "evidence_kind": "provider_accepted_artifact",
        }
        base = {
            "schema_version": checker.DEPENDENCY_RECEIPT_SCHEMA,
            "edge_id": "S51-REL-1111111111111111",
            "consumer_member_id": "S51-THM-00000002",
            "provider_member_id": "S51-THM-00000001",
            "direction_semantics": "consumer_requires_provider",
            "provider_artifact": artifact,
        }
        fixtures = {
            "provider_acceptance_receipt": {
                **base, "receipt_kind": "provider_acceptance",
                "producer_actor_id": "producer", "acceptance_issuer_id": "provider-master",
                "decision": "accepted",
            },
            "independent_review_receipt": {
                **base, "receipt_kind": "independent_review",
                "reviewer_id": "reviewer", "issuer_authority_id": "review-board",
                "decision": "accepted",
            },
            "consumer_replay_receipt": {
                **base, "receipt_kind": "consumer_replay",
                "consumer_owner_id": "consumer-worker",
                "acceptance_issuer_id": "consumer-master", "outcome": "accepted",
                "consumption_verified": True, "replay_command_digest": "2" * 64,
                "observed_output_digest": "3" * 64,
                "consumed_provider_artifact_sha256": "1" * 64,
                "consumer_owned_result_path": "consumer/replay.out",
                "consumer_owned_result_sha256": "4" * 64,
            },
        }
        authority_fields = {
            "provider_acceptance_receipt": "producer_actor_id",
            "independent_review_receipt": "reviewer_id",
            "consumer_replay_receipt": "consumer_owner_id",
        }
        for definition, body in fixtures.items():
            with self.subTest(definition=definition):
                receipt = self.seal(body)
                validator = checker.Draft202012Validator(
                    common["$defs"][definition],
                    resolver=checker.RefResolver.from_schema(common, store=store),
                )
                self.assertEqual(list(validator.iter_errors(receipt)), [])
                missing = dict(receipt)
                missing.pop(authority_fields[definition])
                self.assertTrue(list(validator.iter_errors(missing)))

    def test_audit_release_cursor_mode_requires_receipt_and_rejects_unknown_mode(self) -> None:
        with self.assertRaisesRegex(checker.ReleaseCheckError, "cursor_mode"):
            checker.audit_release(ROOT, "1.0", cursor_mode="implicit_runtime")
        with self.assertRaisesRegex(checker.ReleaseCheckError, "requires an activation_receipt"):
            checker.audit_release(ROOT, "1.0", cursor_mode="boot_accepted_overlay")


class Stage51OrganizationReleaseMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        release_dir = (
            ROOT / "Docs/catalog/stage5_1_organization/releases" / checker.DEFAULT_RELEASE
        )
        if not release_dir.is_dir():
            raise unittest.SkipTest("Stage5.1 release has not been materialized yet")
        cls.snapshot = checker.load_snapshot(ROOT, checker.DEFAULT_RELEASE)
        cls.state = checker.validate_member_bijections(cls.snapshot)
        cls.taxonomy = checker.validate_taxonomy(cls.snapshot, cls.state)

    def mutated_snapshot(self, path: str, value) -> object:
        documents = dict(self.snapshot.documents)
        documents[path] = value
        return checker.ReleaseSnapshot(
            self.snapshot.root,
            self.snapshot.release,
            self.snapshot.release_prefix,
            dict(self.snapshot.raw),
            documents,
        )

    @staticmethod
    def seal_record(body: dict) -> dict:
        value = dict(body)
        value["record_sha256"] = checker.sha256_bytes(checker.canonical_json(value))
        return value

    @staticmethod
    def seal_object(body: dict) -> dict:
        value = dict(body)
        value["authority_sha256"] = checker.sha256_bytes(checker.canonical_json(value))
        return value

    def cloned_state(self) -> dict:
        return {
            key: copy.deepcopy(value) if key != "worksets" else value
            for key, value in self.state.items()
        }

    @staticmethod
    def evidence_ref() -> dict:
        relative = "Docs/Stage5_1_Organization_Design.md"
        raw = (ROOT / relative).read_bytes()
        return {
            "path": relative,
            "sha256": checker.sha256_bytes(raw),
            "evidence_kind": "mutation_test_content_bound_fixture",
        }

    def assert_schema_valid(self, schema_name: str, value) -> None:
        schema_root = ROOT / "Docs/catalog/stage5_1_organization/schemas"
        schemas = {
            path.name: checker.strict_json(path.read_bytes(), path.name)
            for path in schema_root.glob("*.schema.json")
        }
        schema = schemas[schema_name]
        store = {candidate["$id"]: candidate for candidate in schemas.values()}
        validator = checker.Draft202012Validator(
            schema,
            resolver=checker.RefResolver.from_schema(schema, store=store),
        )
        errors = list(validator.iter_errors(value))
        self.assertEqual(errors, [], errors[0].message if errors else "")

    def test_pristine_semantic_release_passes(self) -> None:
        checker.audit_release(ROOT, checker.DEFAULT_RELEASE, rebuild=False)

    def test_fake_hard_edge_is_rejected(self) -> None:
        relation_path = checker._doc_name(self.snapshot, "Relation_Edges.jsonl")
        rows = copy.deepcopy(self.snapshot.rows(relation_path))
        members = sorted(self.state["objects"])
        source = ("item", members[0])
        target = ("item", members[1])
        consumer_roots = checker._endpoint_branches(
            source, self.taxonomy, self.state["assignments"],
        )
        provider_roots = checker._endpoint_branches(
            target, self.taxonomy, self.state["assignments"],
        )
        cross_domain = bool(
            consumer_roots and provider_roots and consumer_roots != provider_roots
        )
        rows.append({
            "edge_id": "S51-REL-ffffffffffffffff",
            "consumer_member_id": source[1],
            "provider_member_id": target[1],
            "consumer_identity_sha256": self.state["objects"][source[1]]["identity_sha256"],
            "provider_identity_sha256": self.state["objects"][target[1]]["identity_sha256"],
            "consumer_object_record_sha256": self.state["objects"][source[1]]["record_sha256"],
            "provider_object_record_sha256": self.state["objects"][target[1]]["record_sha256"],
            "plane": "mathematical_prerequisite",
            "relation_type": "proof_prerequisite",
            "evidence_tier": "D_source_reported",
            "review_state": "candidate",
            "blocking": True,
            "scheduler_effect": "block_until_accepted",
            "cross_domain": cross_domain,
            "provider_binding": {"binding_kind": "none"},
            "direction_semantics": "consumer_requires_provider",
            "evidence": [self.evidence_ref()],
            "status_inheritance": False,
            "credit_inheritance": False,
        })
        mutated = self.mutated_snapshot(relation_path, rows)
        with self.assertRaisesRegex(
            checker.ReleaseCheckError, "not verified|not target-owned|lacks A/B",
        ):
            checker.validate_relations_and_hard_dag(mutated, self.state, self.taxonomy)

    def test_relation_plane_collapse_and_self_edge_are_rejected(self) -> None:
        relation_path = checker._doc_name(self.snapshot, "Relation_Edges.jsonl")
        members = sorted(self.state["objects"])
        for label, plane, provider in (
            ("plane collapse", "execution", members[1]),
            ("self edge", "relation", members[0]),
        ):
            with self.subTest(label=label):
                rows = copy.deepcopy(self.snapshot.rows(relation_path))
                rows.append({
                    "edge_id": "S51-REL-eeeeeeeeeeeeeeee",
                    "consumer_member_id": members[0],
                    "provider_member_id": provider,
                    "consumer_identity_sha256": self.state["objects"][members[0]]["identity_sha256"],
                    "provider_identity_sha256": self.state["objects"][provider]["identity_sha256"],
                    "consumer_object_record_sha256": self.state["objects"][members[0]]["record_sha256"],
                    "provider_object_record_sha256": self.state["objects"][provider]["record_sha256"],
                    "plane": plane,
                    "relation_type": "related_source",
                    "evidence_tier": "D_source_reported",
                    "review_state": "candidate",
                    "blocking": False,
                    "scheduler_effect": "none",
                    "cross_domain": False,
                    "provider_binding": {"binding_kind": "none"},
                    "direction_semantics": "consumer_requires_provider",
                    "evidence": [],
                    "status_inheritance": False,
                    "credit_inheritance": False,
                })
                mutated = self.mutated_snapshot(relation_path, rows)
                with self.assertRaisesRegex(
                    checker.ReleaseCheckError, "relation_type/plane|self edge",
                ):
                    checker.validate_relations_and_hard_dag(
                        mutated, self.state, self.taxonomy,
                    )

    def test_valid_nonblocking_cross_domain_projection_is_accepted(self) -> None:
        branches = sorted(
            identity for identity, parent in self.taxonomy["parents"].items()
            if parent == self.taxonomy["root"] and identity.startswith("S51-SUB-0")
        )
        self.assertGreaterEqual(len(branches), 2)
        members = sorted(self.state["objects"])[:2]
        consumer, provider = members
        state = self.cloned_state()
        for identity, branch in zip((consumer, provider), branches[:2]):
            assignment = dict(state["assignments"][identity])
            assignment.pop("record_sha256", None)
            assignment["classification_status"] = "accepted"
            assignment["primary"] = {
                "subject_id": branch,
                "granularity": "broad",
                "assertion_state": "accepted",
                "evidence_tier": "independent_review",
                "evidence": [],
            }
            assignment["secondary_subject_ids"] = []
            state["assignments"][identity] = self.seal_record(assignment)

        edge_id = "S51-REL-dddddddddddddddd"
        relation = self.seal_record({
            "schema_version": "awesome-theorems/stage5-1-organization/relation-edge/1.0",
            "edge_id": edge_id,
            "consumer_member_id": consumer,
            "provider_member_id": provider,
            "consumer_identity_sha256": state["objects"][consumer]["identity_sha256"],
            "provider_identity_sha256": state["objects"][provider]["identity_sha256"],
            "consumer_object_record_sha256": state["objects"][consumer]["record_sha256"],
            "provider_object_record_sha256": state["objects"][provider]["record_sha256"],
            "relation_type": "implies",
            "plane": "mathematical_semantic",
            "provider_binding": {"binding_kind": "none"},
            "blocking": False,
            "scheduler_effect": "none",
            "evidence_tier": "C_reviewed_semantic",
            "review_state": "verified",
            "direction_semantics": "consumer_requires_provider",
            "evidence": [self.evidence_ref()],
            "credit_inheritance": False,
            "status_inheritance": False,
            "cross_domain": True,
        })
        relation_path = checker._doc_name(self.snapshot, "Relation_Edges.jsonl")
        relation_rows = copy.deepcopy(self.snapshot.rows(relation_path)) + [relation]
        cross_path = checker._doc_name(self.snapshot, "Cross_Domain_Edges.jsonl")
        cross_rows = copy.deepcopy(self.snapshot.rows(cross_path))
        cross_rows.append(self.seal_record({
            "schema_version": "awesome-theorems/stage5-1-organization/cross-domain-edge/1.0",
            "edge_id": edge_id,
            "relation_record_sha256": relation["record_sha256"],
            "provider_member_id": provider,
            "consumer_member_id": consumer,
            "provider_root_subject_ids": [branches[1]],
            "consumer_root_subject_ids": [branches[0]],
            "provider_assignment_sha256": state["assignments"][provider]["record_sha256"],
            "consumer_assignment_sha256": state["assignments"][consumer]["record_sha256"],
            "derived": "accepted_non_sentinel_root_sets_differ",
        }))
        for identity, direction in ((consumer, "outgoing_edge_ids"), (provider, "incoming_edge_ids")):
            assessment = dict(state["assessments"][identity])
            assessment.pop("record_sha256", None)
            assessment[direction] = sorted(set(assessment.get(direction, [])) | {edge_id})
            assessment["audit_status"] = "audited_edges_present"
            state["assessments"][identity] = self.seal_record(assessment)
        documents = dict(self.snapshot.documents)
        documents[relation_path] = relation_rows
        documents[cross_path] = cross_rows
        mutated = checker.ReleaseSnapshot(
            self.snapshot.root, self.snapshot.release, self.snapshot.release_prefix,
            dict(self.snapshot.raw), documents,
        )
        result = checker.validate_relations_and_hard_dag(mutated, state, self.taxonomy)
        self.assertIn(edge_id, result["relations"])
        self.assertNotIn(edge_id, result["hard_relation_ids"])

    def test_valid_target_owned_hard_projection_is_accepted(self) -> None:
        state = self.cloned_state()
        dag_path = checker._doc_name(self.snapshot, "Execution_Hard_DAG.json")
        dag = copy.deepcopy(self.snapshot.obj(dag_path))
        item_to_object = {
            row["stage51_item_id"]: identity
            for identity, row in self.state["objects"].items()
        }
        theorem_items = sorted(
            row["stage51_item_id"] for row in self.state["objects"].values()
            if row["program"] == "theorems"
        )
        provider_item, consumer_item = theorem_items[0], theorem_items[-1]
        provider, consumer = item_to_object[provider_item], item_to_object[consumer_item]
        self.assertNotEqual(provider, consumer)
        for identity in (provider, consumer):
            assignment = dict(state["assignments"][identity])
            assignment.pop("record_sha256", None)
            assignment["classification_status"] = "review_pending"
            assignment["primary"] = {
                "subject_id": "S51-SUB-REVIEW-PENDING",
                "granularity": "sentinel",
                "assertion_state": "review_pending",
                "evidence_tier": "none",
                "evidence": [],
            }
            assignment["secondary_subject_ids"] = []
            state["assignments"][identity] = self.seal_record(assignment)
        edge_id = "S51-REL-cccccccccccccccc"
        for identity, direction in ((consumer, "outgoing_edge_ids"), (provider, "incoming_edge_ids")):
            assessment = dict(state["assessments"][identity])
            assessment.pop("record_sha256", None)
            assessment[direction] = sorted(set(assessment.get(direction, [])) | {edge_id})
            assessment["audit_status"] = "audited_edges_present"
            if identity == consumer:
                assessment["hard_prerequisite_item_ids"] = sorted(
                    set(assessment.get("hard_prerequisite_item_ids", [])) | {provider_item}
                )
            state["assessments"][identity] = self.seal_record(assessment)

        with tempfile.TemporaryDirectory(prefix="stage51-hard-binding-") as temporary:
            temp_root = Path(temporary)
            artifact_path = "Docs/evidence/stage5_1_test/provider/artifact.bin"
            acceptance_path = "Docs/evidence/stage5_1_test/provider/acceptance.json"
            review_path = "Docs/evidence/stage5_1_test/review/independent.json"
            replay_path = "Docs/evidence/stage5_1_test/consumer/replay.json"
            replay_result_path = "Docs/evidence/stage5_1_test/consumer/replay.out"

            def write(relative: str, raw: bytes) -> dict:
                path = temp_root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
                return {
                    "path": relative,
                    "sha256": checker.sha256_bytes(raw),
                    "evidence_kind": checker.DEPENDENCY_EVIDENCE_KINDS[
                        next(name for name, candidate in {
                            "provider_artifact": artifact_path,
                            "provider_acceptance_receipt": acceptance_path,
                            "independent_review_receipt": review_path,
                            "consumer_replay_receipt": replay_path,
                        }.items() if candidate == relative)
                    ],
                }

            artifact_ref = write(artifact_path, b"provider accepted artifact\n")

            replay_result_raw = b"consumer replay accepted\n"
            replay_result = temp_root / replay_result_path
            replay_result.parent.mkdir(parents=True, exist_ok=True)
            replay_result.write_bytes(replay_result_raw)

            def receipt(kind: str, *, replay: bool = False) -> bytes:
                body = {
                    "schema_version": checker.DEPENDENCY_RECEIPT_SCHEMA,
                    "receipt_kind": checker.DEPENDENCY_RECEIPT_KINDS[kind],
                    "edge_id": edge_id,
                    "consumer_member_id": consumer,
                    "provider_member_id": provider,
                    "direction_semantics": "consumer_requires_provider",
                    "provider_artifact": artifact_ref,
                }
                if kind == "provider_acceptance_receipt":
                    body.update({
                        "producer_actor_id": "provider-worker",
                        "acceptance_issuer_id": "provider-master",
                        "decision": "accepted",
                    })
                elif kind == "independent_review_receipt":
                    body.update({
                        "reviewer_id": "independent-edge-reviewer",
                        "issuer_authority_id": "independent-review-board",
                        "decision": "accepted",
                    })
                elif replay:
                    body.update({
                        "consumer_owner_id": "consumer-worker",
                        "acceptance_issuer_id": "consumer-master",
                        "outcome": "accepted",
                        "consumption_verified": True,
                        "replay_command_digest": "2" * 64,
                        "observed_output_digest": "3" * 64,
                        "consumed_provider_artifact_sha256": artifact_ref["sha256"],
                        "consumer_owned_result_path": replay_result_path,
                        "consumer_owned_result_sha256": checker.sha256_bytes(
                            replay_result_raw
                        ),
                    })
                else:
                    raise AssertionError(f"unknown receipt fixture kind: {kind}")
                return (json.dumps(self.seal_object(body), sort_keys=True,
                                   separators=(",", ":")) + "\n").encode()

            acceptance_ref = write(
                acceptance_path, receipt("provider_acceptance_receipt"),
            )
            review_ref = write(
                review_path, receipt("independent_review_receipt"),
            )
            replay_ref = write(
                replay_path, receipt("consumer_replay_receipt", replay=True),
            )
            binding_refs = {
                "provider_artifact": artifact_ref,
                "provider_acceptance_receipt": acceptance_ref,
                "independent_review_receipt": review_ref,
                "consumer_replay_receipt": replay_ref,
            }
            relation = self.seal_record({
                "schema_version": "awesome-theorems/stage5-1-organization/relation-edge/1.0",
                "edge_id": edge_id,
                "consumer_member_id": consumer,
                "provider_member_id": provider,
                "consumer_identity_sha256": state["objects"][consumer]["identity_sha256"],
                "provider_identity_sha256": state["objects"][provider]["identity_sha256"],
                "consumer_object_record_sha256": state["objects"][consumer]["record_sha256"],
                "provider_object_record_sha256": state["objects"][provider]["record_sha256"],
                "relation_type": "proof_prerequisite",
                "plane": "mathematical_prerequisite",
                "provider_binding": {
                    "binding_kind": "target_owned_exact_replay", **binding_refs,
                },
                "blocking": True,
                "scheduler_effect": "block_until_accepted",
                "evidence_tier": "A2_target_owned_replay",
                "review_state": "verified",
                "direction_semantics": "consumer_requires_provider",
                "evidence": list(binding_refs.values()),
                "credit_inheritance": False,
                "status_inheritance": False,
                "cross_domain": False,
            })
            relation_path = checker._doc_name(self.snapshot, "Relation_Edges.jsonl")
            relation_rows = copy.deepcopy(self.snapshot.rows(relation_path)) + [relation]

            dag.pop("authority_sha256", None)
            dag["edges"] = list(dag["edges"]) + [{
                "edge_id": edge_id,
                "provider_member_id": provider,
                "consumer_member_id": consumer,
                "scheduler_effect": "block_until_accepted",
                "relation_record_sha256": relation["record_sha256"],
                "evidence_tier": "A2_target_owned_replay",
                "blocking": True,
            }]
            consumers_with_edges = {edge["consumer_member_id"] for edge in dag["edges"]}
            dag["counts"] = dict(dag["counts"], edge_count=len(dag["edges"]),
                                 root_count=len(dag["nodes"]) - len(consumers_with_edges))
            dag = self.seal_object(dag)
            self.assert_schema_valid("relation-edge.schema.json", relation)
            self.assert_schema_valid("execution-hard-dag.schema.json", dag)

            # Copy production nonblocking evidence because the direct semantic
            # pass resolves every relation reference against snapshot.root.
            for existing in self.snapshot.rows(relation_path):
                for ref in existing["evidence"]:
                    destination = temp_root / ref["path"]
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    if not destination.exists():
                        destination.write_bytes((ROOT / ref["path"]).read_bytes())

            documents = dict(self.snapshot.documents)
            theorem_bp = documents["Docs/Stage5_1_Theorems_Blueprint.md"]
            self.assertIsInstance(theorem_bp, str)
            for item, owned in (
                (provider_item, artifact_path),
                (consumer_item, replay_path),
                (consumer_item, replay_result_path),
            ):
                lines = theorem_bp.splitlines(keepends=True)
                matches = [index for index, line in enumerate(lines)
                           if line.startswith("- [") and f"`{item}`" in line]
                self.assertEqual(len(matches), 1)
                index = matches[0]
                lines[index], count = re.subn(
                    r"(?<=\| owned_paths=)([^|]+?)(?=\s+\| gate=)",
                    lambda match: match.group(1).rstrip() + "," + owned,
                    lines[index], count=1,
                )
                self.assertEqual(count, 1)
                theorem_bp = "".join(lines)
            documents["Docs/Stage5_1_Theorems_Blueprint.md"] = theorem_bp
            documents[relation_path] = relation_rows
            documents[dag_path] = dag
            mutated = checker.ReleaseSnapshot(
                temp_root, self.snapshot.release, self.snapshot.release_prefix,
                dict(self.snapshot.raw), documents,
            )
            result = checker.validate_relations_and_hard_dag(mutated, state, self.taxonomy)
            self.assertIn(edge_id, result["hard_relation_ids"])

            for name in binding_refs:
                with self.subTest(stale_binding=name):
                    bad_relation = copy.deepcopy(relation)
                    bad_relation.pop("record_sha256")
                    bad_relation["provider_binding"][name]["sha256"] = "0" * 64
                    for ref in bad_relation["evidence"]:
                        if ref["path"] == binding_refs[name]["path"]:
                            ref["sha256"] = "0" * 64
                    bad_relation = self.seal_record(bad_relation)
                    bad_documents = dict(documents)
                    bad_documents[relation_path] = (
                        copy.deepcopy(self.snapshot.rows(relation_path)) + [bad_relation]
                    )
                    bad_snapshot = checker.ReleaseSnapshot(
                        temp_root, self.snapshot.release, self.snapshot.release_prefix,
                        dict(self.snapshot.raw), bad_documents,
                    )
                    with self.assertRaisesRegex(checker.ReleaseCheckError, "hash drift"):
                        checker.validate_relations_and_hard_dag(
                            bad_snapshot, state, self.taxonomy,
                        )

    def test_missing_classification_is_rejected(self) -> None:
        assignment_path = checker._doc_name(self.snapshot, "Subject_Assignments.jsonl")
        rows = copy.deepcopy(self.snapshot.rows(assignment_path))
        del rows[0]
        mutated = self.mutated_snapshot(assignment_path, rows)
        with self.assertRaisesRegex(
            checker.ReleaseCheckError,
            "Subject_Assignments is not a bijection|exactly cover",
        ):
            checker.validate_member_bijections(mutated)

    def test_legacy_state_cannot_be_inherited(self) -> None:
        blueprint_path = "Docs/Stage5_1_Theorems_Blueprint.md"
        text = self.snapshot.documents[blueprint_path]
        self.assertIsInstance(text, str)
        mutated_text, count = re.subn(r"(?m)^- \[ \]", "- [x]", text, count=1)
        self.assertEqual(count, 1)
        mutated = self.mutated_snapshot(blueprint_path, mutated_text)
        with self.assertRaisesRegex(
            checker.ReleaseCheckError, "all blank|state inheritance",
        ):
            checker.validate_blueprints_and_gantts(mutated, self.state, self.taxonomy)

    def test_gantt_missing_member_row_is_rejected(self) -> None:
        blueprint_path = "Docs/Stage5_1_Theorems_Blueprint.md"
        gantt_path = "Docs/Stage5_1_Theorems_Gantt.md"
        rows = checker.parse_blueprint_rows(
            self.snapshot.documents[blueprint_path], blueprint_path,
        )
        missing_id = rows[0]["item_id"]
        lines = self.snapshot.documents[gantt_path].splitlines(keepends=True)
        filtered = [
            line for line in lines
            if not (line.lstrip().startswith("|") and f"`{missing_id}`" in line)
        ]
        self.assertLess(len(filtered), len(lines))
        mutated = self.mutated_snapshot(gantt_path, "".join(filtered))
        with self.assertRaisesRegex(checker.ReleaseCheckError, "monitoring rows|omits checklist"):
            checker.validate_blueprints_and_gantts(mutated, self.state, self.taxonomy)

    def test_concurrency_numeric_value_and_default_are_rejected(self) -> None:
        blueprint_path = "Docs/Stage5_1_Theorems_Blueprint.md"
        text = self.snapshot.documents[blueprint_path]
        for label, mutated in (
            ("numeric prose", text + "\nConcurrency hard cap: 12\n"),
            (
                "JSON default",
                text.replace(
                    '"concurrency_prompt_contract": {',
                    '"concurrency_prompt_contract": {\n    "worker_count_default": 12,',
                    1,
                ),
            ),
        ):
            with self.subTest(label=label):
                self.assertNotEqual(mutated, text)
                with self.assertRaisesRegex(
                    checker.ReleaseCheckError,
                    "hard-coded numeric concurrency|defaults are forbidden|"
                    "concurrency prompt contract fields differ",
                ):
                    checker.validate_concurrency_prompt(mutated, blueprint_path)


if __name__ == "__main__":
    unittest.main()
