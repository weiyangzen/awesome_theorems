#!/usr/bin/env python3
"""Focused fail-closed tests for cleanup-time release revalidation."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
from pathlib import Path
import tempfile
import unittest
from unittest import mock


MODULE = Path(__file__).with_name("stage1_execution_cron.py")
SPEC = importlib.util.spec_from_file_location("stage1_cleanup_currentness_cron", MODULE)
assert SPEC is not None and SPEC.loader is not None
cron = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cron)


def embedded(value: dict[str, object], field: str) -> dict[str, object]:
    result = copy.deepcopy(value)
    result[field] = cron.canonical_json_sha256(result)
    return result


class CleanupCurrentnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.item = {
            "id": "S56-M-0001-RELEASE",
            "theorem_id": "THM-M-0001",
            "phase": "release",
            "owned_paths": ["Stage1_Instances/THM-M-0001"],
        }
        self.focus = {
            "present": True,
            "valid": True,
            "execution_disposition": "organize_or_integrate",
            "phase_permissions": {"release": True},
            "receipt_sha256": "f" * 64,
        }
        self.focus_contract = {
            "focus_contract_sha256": "0" * 64,
            "execution_disposition": "organize_or_integrate",
        }
        self.head = "9" * 40
        self.base = "8" * 40
        self.contract = {
            "revision": self.head,
            "git_tree": "7" * 40,
            "path": "Docs/Stage1_Phase_Acceptance_Contracts.json",
            "sha256": "b" * 64,
            "git_blob": "c" * 40,
            "contract": {"validator_selection": {}},
        }
        self.role_map = embedded({
            "schema_version": "stage1-artifact-role-map/1.0",
            "item_id": self.item["id"],
            "theorem_id": self.item["theorem_id"],
            "phase": "release",
            "base_revision": self.base,
            "authority_revision": "a" * 40,
            "contract_sha256": self.contract["sha256"],
            "contract_git_blob": self.contract["git_blob"],
            "phase_receipt_path": "Stage1_Instances/THM-M-0001/release-receipt.json",
            "phase_receipt_sha256": "4" * 64,
            "artifacts": [{
                "role": "phase_receipt",
                "path": "Stage1_Instances/THM-M-0001/release-receipt.json",
                "sha256": "4" * 64,
                "git_blob": "5" * 40,
            }],
        }, "manifest_sha256")
        self.validator = embedded({
            "item_id": self.item["id"],
            "theorem_id": self.item["theorem_id"],
            "phase": "release",
            "base_revision": self.base,
            "authority_revision": "a" * 40,
            "contract_sha256": self.contract["sha256"],
            "validator_authority_generation": "stage1-v2",
            "requirements_authority": "Docs/Stage1_Blueprint_v2.md",
            "positive_acceptance_capable": True,
            "validator_path": "scripts/stage1_phase_validators/current.py",
            "validator_sha256": "6" * 64,
            "validator_git_blob": "7" * 40,
            "validator_git_mode": "100644",
            "argv": ["/usr/bin/python3", "-I", "-B", "scripts/stage1_phase_validators/current.py"],
            "cwd": ".",
            "network_policy": "denied",
            "repo_write_access": False,
            "isolated_scratch_write_access": True,
            "shell_interpolation": False,
        }, "recipe_sha256")
        self.manifest = embedded({
            "schema_version": "stage1-review-manifest/1.0",
            "item_id": self.item["id"],
            "theorem_id": self.item["theorem_id"],
            "phase": "release",
            "authority_revision": "a" * 40,
            "authority_tree": "d" * 40,
            "base_revision": self.base,
            "contract": {
                "path": self.contract["path"],
                "sha256": self.contract["sha256"],
                "git_blob": self.contract["git_blob"],
            },
            "blueprint": {
                "path": "Docs/Stage1_Blueprint_v2.md",
                "sha256": "e" * 64,
                "git_blob": "f" * 40,
            },
            "blueprint_sha256": "e" * 64,
            "theorem_dag_sha256": "1" * 64,
            "worker_claim_sha256": "2" * 64,
            "worker_status_sha256": "3" * 64,
            "worker_prompt_sha256": "4" * 64,
            "worker_goal_sha256": "5" * 64,
            "worker_handoff_sha256": "6" * 64,
            "role_map_sha256": self.role_map["manifest_sha256"],
            "validator_recipe_sha256": self.validator["recipe_sha256"],
            "artifact_bindings": self.role_map["artifacts"],
            "focus_execution": self.focus_contract,
            "focus_contract_sha256": cron.canonical_json_sha256(self.focus_contract),
        }, "manifest_sha256")
        self.replay = embedded({
            "schema_version": "stage1-authority-replay/1.0",
            "item_id": self.item["id"],
            "theorem_id": self.item["theorem_id"],
            "phase": "release",
            "authority_revision": "a" * 40,
            "authority_tree": "d" * 40,
            "validator_path": self.validator["validator_path"],
            "validator_sha256": self.validator["validator_sha256"],
            "validator_git_blob": self.validator["validator_git_blob"],
            "recipe_sha256": self.validator["recipe_sha256"],
            "review_manifest_sha256": self.manifest["manifest_sha256"],
            "role_map_sha256": self.role_map["manifest_sha256"],
            "artifact_bindings_sha256": cron.canonical_json_sha256(self.role_map["artifacts"]),
            "validator_input_sha256": "7" * 64,
            "lean_authority": {"toolchain_closure_sha256": "8" * 64},
            "lean_authority_sha256": "9" * 64,
            "argv": self.validator["argv"],
            "bwrap_argv": ["/usr/bin/bwrap", "--", *self.validator["argv"]],
            "cwd": "/repo",
            "network_policy": "denied",
            "repo_access": "read_only",
            "scratch_access": "isolated_writable",
            "scratch_was_isolated": True,
            "shell": False,
            "started_at_unix_ns": 1,
            "duration_ms": 2,
            "exit_code": 0,
            "timed_out": False,
            "stdout": "accepted",
            "stderr": "",
            "stdout_base64": "YWNjZXB0ZWQ=",
            "stderr_base64": "",
            "stdout_sha256": hashlib.sha256(b"accepted").hexdigest(),
            "stderr_sha256": hashlib.sha256(b"").hexdigest(),
            "stdout_complete": True,
            "stderr_complete": True,
            "semantic_result": {
                "status": "passed", "verdict": "phase_accepted",
                "phase_accepted": True, "audit_complete": True,
                "theorem_complete": True,
            },
            "semantic_result_sha256": cron.canonical_json_sha256({
                "status": "passed", "verdict": "phase_accepted",
                "phase_accepted": True, "audit_complete": True,
                "theorem_complete": True,
            }),
        }, "result_sha256")
        self.decision = embedded({
            "schema_version": "stage1-replay-semantic-decision/1.0",
            "phase": "release",
            "item_id": self.item["id"],
            "theorem_id": self.item["theorem_id"],
            "worker_verdict": "accepted",
            "review_verdict": "phase_accepted",
            "audit_complete": True,
            "theorem_complete": True,
            "replay_result_sha256": self.replay["result_sha256"],
            "review_manifest_sha256": self.manifest["manifest_sha256"],
            "role_map_sha256": self.role_map["manifest_sha256"],
            "contract_sha256": self.contract["sha256"],
            "semantic_result_sha256": self.replay["semantic_result_sha256"],
            "phase_evidence_accepted": True,
            "decision": "phase_accepted",
            "negative_reasons": [],
        }, "decision_sha256")
        self.receipt = {
            "focus_eligibility": copy.deepcopy(self.focus),
            "review_manifest": self.manifest,
            "review_manifest_sha256": self.manifest["manifest_sha256"],
            "role_map": self.role_map,
            "role_map_sha256": self.role_map["manifest_sha256"],
            "validator_recipe": self.validator,
            "validator_recipe_sha256": self.validator["recipe_sha256"],
            "worker_verdict": "accepted",
            "review_verdict": "phase_accepted",
            "audit_complete": True,
            "theorem_complete": True,
            "replay_result": self.replay,
            "replay_result_sha256": self.replay["result_sha256"],
            "semantic_decision": self.decision,
            "semantic_decision_sha256": self.decision["decision_sha256"],
        }

    def current_role_map(self) -> dict[str, object]:
        value = copy.deepcopy(self.role_map)
        value["authority_revision"] = self.head
        return embedded(
            {key: row for key, row in value.items() if key != "manifest_sha256"},
            "manifest_sha256",
        )

    def current_validator(self) -> dict[str, object]:
        value = copy.deepcopy(self.validator)
        value["authority_revision"] = self.head
        return embedded(
            {key: row for key, row in value.items() if key != "recipe_sha256"},
            "recipe_sha256",
        )

    def current_replay(self) -> dict[str, object]:
        value = copy.deepcopy(self.replay)
        value.update({
            "authority_revision": self.head,
            "authority_tree": self.contract["git_tree"],
            "recipe_sha256": self.current_validator()["recipe_sha256"],
            "review_manifest_sha256": "0" * 64,
            "role_map_sha256": self.current_role_map()["manifest_sha256"],
            "validator_input_sha256": "0" * 64,
            "bwrap_argv": ["/usr/bin/bwrap", "--current"],
            "started_at_unix_ns": 10,
            "duration_ms": 20,
        })
        return embedded(
            {key: row for key, row in value.items() if key != "result_sha256"},
            "result_sha256",
        )

    def current_decision(self) -> dict[str, object]:
        value = copy.deepcopy(self.decision)
        value.update({
            "replay_result_sha256": self.current_replay()["result_sha256"],
            "review_manifest_sha256": "0" * 64,
            "role_map_sha256": self.current_role_map()["manifest_sha256"],
        })
        return embedded(
            {key: row for key, row in value.items() if key != "decision_sha256"},
            "decision_sha256",
        )

    def patches(self):
        return (
            mock.patch.object(cron, "require_item_focus_phase_allowed", return_value=self.focus),
            mock.patch.object(cron, "_require_frontier_runtime"),
            mock.patch.object(cron, "authoritative_head_revision", return_value=self.head),
            mock.patch.object(cron, "phase_acceptance_contract_record", return_value=self.contract),
            mock.patch.object(
                cron, "_cleanup_blueprint_and_dag_authority",
                return_value=("a" * 64, "b" * 40, "c" * 64),
            ),
            mock.patch.object(cron, "build_review_role_map", return_value=self.current_role_map()),
            mock.patch.object(cron, "select_review_validator", return_value=self.current_validator()),
            mock.patch.object(cron, "focus_execution_contract", return_value=self.focus_contract),
            mock.patch.object(
                cron.acceptance_evidence, "build_review_manifest",
                return_value={"manifest_sha256": "0" * 64},
            ),
            mock.patch.object(
                cron.acceptance_evidence, "replay_validator",
                return_value=self.current_replay(),
            ),
            mock.patch.object(
                cron.acceptance_evidence, "evaluate_replay_semantics",
                return_value=self.current_decision(),
            ),
            mock.patch.object(
                cron.acceptance_evidence,
                "require_replayed_integration_source_semantics",
                return_value={},
            ),
        )

    def call(self):
        patches = self.patches()
        with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], \
             patches[6], patches[7], patches[8], patches[9], patches[10], patches[11]:
            return cron.revalidate_cleanup_release_acceptance(self.item, {}, self.receipt)

    def test_current_release_replay_is_accepted_after_checkpoint_head_advance(self) -> None:
        replay, decision = self.call()
        self.assertEqual(
            cron._cleanup_replay_invariants(replay),
            cron._cleanup_replay_invariants(self.replay),
        )
        self.assertEqual(
            cron._cleanup_decision_invariants(decision),
            cron._cleanup_decision_invariants(self.decision),
        )

    def test_expired_or_revoked_release_focus_is_rejected(self) -> None:
        with mock.patch.object(
            cron, "require_item_focus_phase_allowed",
            side_effect=ValueError("release focus permission expired"),
        ), self.assertRaisesRegex(ValueError, "expired"):
            cron.revalidate_cleanup_release_acceptance(self.item, {}, self.receipt)

    def test_changed_contract_is_rejected(self) -> None:
        changed = {**self.contract, "sha256": "0" * 64}
        patches = self.patches()
        with patches[0], patches[1], patches[2], mock.patch.object(
            cron, "phase_acceptance_contract_record", return_value=changed
        ), self.assertRaisesRegex(ValueError, "contract"):
            cron.revalidate_cleanup_release_acceptance(self.item, {}, self.receipt)

    def test_changed_validator_bytes_are_rejected(self) -> None:
        changed = {**self.current_validator(), "validator_sha256": "0" * 64}
        patches = self.patches()
        with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], \
             mock.patch.object(cron, "select_review_validator", return_value=changed), \
             self.assertRaisesRegex(ValueError, "validator"):
            cron.revalidate_cleanup_release_acceptance(self.item, {}, self.receipt)

    def test_changed_toolchain_closure_is_rejected(self) -> None:
        changed = copy.deepcopy(self.current_replay())
        changed["lean_authority"]["toolchain_closure_sha256"] = "0" * 64
        changed = embedded(
            {key: row for key, row in changed.items() if key != "result_sha256"},
            "result_sha256",
        )
        patches = self.patches()
        with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], \
             patches[6], patches[7], patches[8], mock.patch.object(
                 cron.acceptance_evidence, "replay_validator", return_value=changed
             ), patches[10], patches[11], self.assertRaisesRegex(ValueError, "toolchain"):
            cron.revalidate_cleanup_release_acceptance(self.item, {}, self.receipt)

    def test_changed_target_artifact_bytes_are_rejected(self) -> None:
        changed = copy.deepcopy(self.current_role_map())
        changed["artifacts"][0]["sha256"] = "0" * 64
        changed = embedded(
            {key: row for key, row in changed.items() if key != "manifest_sha256"},
            "manifest_sha256",
        )
        patches = self.patches()
        with patches[0], patches[1], patches[2], patches[3], patches[4], mock.patch.object(
            cron, "build_review_role_map", return_value=changed
        ), patches[6], self.assertRaisesRegex(ValueError, "target"):
            cron.revalidate_cleanup_release_acceptance(self.item, {}, self.receipt)

    def test_material_blueprint_or_dag_drift_is_rejected(self) -> None:
        before = (
            "# Normative release authority\n"
            f"{cron.CHECKLIST_BEGIN}\n"
            "- [_] `S56-M-0001-RELEASE` / `THM-M-0001` / `release`: "
            "release predicate {attempts=1}\n"
            f"{cron.CHECKLIST_END}\n"
        ).encode()
        after = before.replace(b"- [_]", b"- [x]").replace(
            b"{attempts=1}", b"{attempts=2}"
        )
        node = {
            "theorem_id": self.item["theorem_id"],
            "v2_execution_rank": 1,
            "topological_layer": 0,
            "direct_hard_parents": [],
            "transitive_hard_ancestors": [],
            "direct_reuse_hint_ids": [],
            "shared_lemma_group_ids": [],
            "dependency_context_sha256": "3" * 64,
            "focus_eligibility": self.focus,
            "completion_bucket": "partial",
            "phase_states": {"release": "[_]"},
        }
        dag = {
            "schema_version": "stage1-theorem-dag/2.1",
            "requirements_source": "Docs/Stage1_Blueprint_v2.md",
            "target_manifest": "Docs/Stage1_Target_Membership_v2.json",
            "target_id_set_sha256": "4" * 64,
            "execution_contract": {"claim_order": []},
            "focus_policy": {"requirements_source": "Docs/Stage1_Blueprint_v2.md"},
            "edge_policy": {"unknown_policy": "fail_closed"},
            "theorems": [node],
            "hard_edges": [],
            "reuse_hints": [],
            "shared_lemma_groups": [],
        }
        old_dag = json.dumps(dag, sort_keys=True).encode()
        current_dag_value = copy.deepcopy(dag)
        current_dag_value["theorems"][0]["completion_bucket"] = "master_complete"
        current_dag_value["theorems"][0]["phase_states"] = {"release": "[x]"}
        current_dag = json.dumps(current_dag_value, sort_keys=True).encode()
        manifest = {
            "authority_revision": "a" * 40,
            "blueprint_sha256": hashlib.sha256(before).hexdigest(),
            "blueprint": {
                "path": "Docs/Stage1_Blueprint_v2.md",
                "sha256": hashlib.sha256(before).hexdigest(),
                "git_blob": hashlib.sha1(
                    f"blob {len(before)}\0".encode() + before
                ).hexdigest(),
            },
            "theorem_dag_sha256": hashlib.sha256(old_dag).hexdigest(),
        }
        contract = {
            "contract": {
                "source_references": [{
                    "reference_id": "release-authority",
                    "path": "Docs/Stage1_Blueprint_v2.md",
                    "line_start": 1,
                    "line_end": 1,
                    "required_phrases": ["Normative release authority"],
                }],
                "common_master_gates": [{
                    "source_reference_ids": ["release-authority"]
                }],
                "phases": [],
            }
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            blueprint = root / "Docs/Stage1_Blueprint_v2.md"
            theorem_dag = root / "Docs/Stage1_Theorem_DAG_v2.json"
            blueprint.parent.mkdir(parents=True)
            blueprint.write_bytes(after)
            theorem_dag.write_bytes(current_dag)

            def objects(specification: str) -> bytes:
                if specification == f"{'a' * 40}:Docs/Stage1_Blueprint_v2.md":
                    return before
                if specification == f"{self.head}:Docs/Stage1_Blueprint_v2.md":
                    return after
                if specification == f"{'a' * 40}:Docs/Stage1_Theorem_DAG_v2.json":
                    return old_dag
                if specification == f"{self.head}:Docs/Stage1_Theorem_DAG_v2.json":
                    return current_dag
                raise AssertionError(specification)

            with (
                mock.patch.object(cron, "ROOT", root),
                mock.patch.object(cron, "BLUEPRINT", blueprint),
                mock.patch.object(cron, "THEOREM_DAG_V2", theorem_dag),
                mock.patch.object(cron, "git_object_bytes", side_effect=objects),
            ):
                current = cron._cleanup_blueprint_and_dag_authority(
                    self.item, manifest, self.head, contract
                )
                self.assertEqual(current[0], hashlib.sha256(after).hexdigest())

                materially_changed = copy.deepcopy(current_dag_value)
                materially_changed["theorems"][0]["dependency_context_sha256"] = "0" * 64
                current_dag = json.dumps(materially_changed, sort_keys=True).encode()
                theorem_dag.write_bytes(current_dag)
                with self.assertRaisesRegex(ValueError, "target DAG authority"):
                    cron._cleanup_blueprint_and_dag_authority(
                        self.item, manifest, self.head, contract
                    )

                current_dag = json.dumps(current_dag_value, sort_keys=True).encode()
                theorem_dag.write_bytes(current_dag)
                blueprint.write_bytes(after.replace(b"Normative", b"Mutated__"))
                with self.assertRaisesRegex(ValueError, "blueprint authority"):
                    cron._cleanup_blueprint_and_dag_authority(
                        self.item, manifest, self.head, contract
                    )

    def test_cleanup_replay_invariants_match_real_replay_result_schema(self) -> None:
        source = (Path(cron.acceptance_evidence.__file__)).read_text(encoding="utf-8")
        match = re.search(
            r"class ReplayResult:\n(?P<body>.*?)(?:\n    def to_dict)",
            source,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        fields = set(re.findall(r"^    ([a-z][a-z0-9_]*):", match.group("body"), re.MULTILINE))
        self.assertEqual(
            set(cron._cleanup_replay_invariants(self.replay)),
            fields - cron.CLEANUP_REPLAY_VOLATILE_FIELDS,
        )
        decision_fields = {
            "schema_version", "phase", "item_id", "theorem_id", "worker_verdict",
            "review_verdict", "audit_complete", "theorem_complete",
            "replay_result_sha256", "review_manifest_sha256", "role_map_sha256",
            "contract_sha256", "semantic_result_sha256", "phase_evidence_accepted",
            "decision", "negative_reasons", "decision_sha256",
        }
        self.assertEqual(
            set(cron._cleanup_decision_invariants(self.decision)),
            decision_fields - cron.CLEANUP_DECISION_VOLATILE_FIELDS,
        )


if __name__ == "__main__":
    unittest.main()
