#!/usr/bin/env python3
"""Focused regressions for the Stage1 historical revalidation boundary."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock


CRON_PATH = Path(__file__).with_name("stage1_execution_cron.py")
SPEC = importlib.util.spec_from_file_location(
    "stage1_execution_revalidation_under_test", CRON_PATH
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {CRON_PATH}")
cron = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cron)


def canonical_digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


class HistoricalRevalidationBoundaryTests(unittest.TestCase):
    HEAD = "b" * 40
    TREE = "c" * 40

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.runtime = self.root / ".cron" / "stage1-v2-app-server"
        self.runtime.mkdir(parents=True)
        self.plan_path = self.runtime / "legacy-revalidation-plan.json"
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
        self.open_item = {
            **self.item,
            "id": "S56-M-0002-INTAKE",
            "theorem_id": "THM-M-0002",
            "state": "[ ]",
            "attempts": 0,
            "owned_paths": ["Stage1_Instances/THM-M-0002"],
        }
        self.nodes = {
            self.item["theorem_id"]: {"v2_execution_rank": 1},
            self.open_item["theorem_id"]: {"v2_execution_rank": 2},
        }

    def lane(self) -> dict[str, object]:
        lane: dict[str, object] = {
            "schema_version": "stage1-legacy-revalidation-lane/1.0",
            "item_id": self.item["id"],
            "theorem_id": self.item["theorem_id"],
            "phase": self.item["phase"],
            "phase_layer": 0,
            "v2_execution_rank": 1,
            "attempts_at_plan_base": self.item["attempts"],
            "authoritative_state": "[_]",
            "required_steps": [
                "fresh_self_test",
                "new_contract_receipt",
                "new_provenance",
                "independent_review",
                "master_replay",
            ],
            "step_outcomes": {
                "fresh_self_test": "unknown",
                "new_contract_receipt": "unknown",
                "new_provenance": "unknown",
                "independent_review": "unknown",
                "master_replay": "unknown",
            },
            "state_transition": "none",
            "acceptance_claimed": False,
            "promotes_to_master_accepted": False,
            "executes_validators": False,
            "launches_workers": False,
            "mutates_repository": False,
            "legacy_migration_ready_observation": False,
            "legacy_classification_statuses": {
                "missing_receipt": "unknown",
                "legacy_receipt": "unknown",
                "phase_mismatch": "unknown",
                "missing_or_ambiguous_role": "unknown",
                "validator_base_mismatch": "unknown",
                "validator_stdout_mismatch": "unknown",
                "sandbox_incompatible": "unknown",
            },
            "authority_revision": self.HEAD,
            "authority_tree": self.TREE,
            "bindings": {
                "blueprint_sha256": "1" * 64,
                "theorem_dag_sha256": "2" * 64,
                "contract_sha256": "3" * 64,
                "inventory_sha256": "4" * 64,
                "inventory_item_sha256": "5" * 64,
                "dependency_context_sha256": "6" * 64,
            },
        }
        lane["lane_sha256"] = canonical_digest(lane)
        return lane

    def plan(self, *, revision: str | None = None) -> dict[str, object]:
        lane = self.lane()
        plan: dict[str, object] = {
            "schema_version": cron.LEGACY_REVALIDATION_PLAN_SCHEMA,
            "generated_from_revision": revision or self.HEAD,
            "generated_from_tree": self.TREE,
            "authority_mode": "authoritative_head",
            "head_owned_contract": True,
            "planning_only": True,
            "authoritative_for_acceptance": False,
            "mutates_repository": False,
            "executes_validators": False,
            "launches_workers": False,
            "writes_ssot": False,
            "writes_todo": False,
            "writes_claims": False,
            "writes_paused_state": False,
            "state_transition": "none",
            "acceptance_claimed": False,
            "source_bindings": {
                "blueprint": {
                    "path": "Docs/Stage1_Blueprint_v2.md",
                    "git_blob": "7" * 40,
                    "sha256": "1" * 64,
                    "size": 100,
                    "git_mode": "100644",
                },
                "theorem_dag": {
                    "path": "Docs/Stage1_Theorem_DAG_v2.json",
                    "git_blob": "8" * 40,
                    "sha256": "2" * 64,
                    "size": 200,
                    "git_mode": "100644",
                },
                "contract": {
                    "path": "Docs/Stage1_Phase_Acceptance_Contracts.json",
                    "git_blob": "9" * 40,
                    "sha256": "3" * 64,
                    "size": 300,
                    "git_mode": "100644",
                },
                "inventory": {
                    "schema_version": "stage1-legacy-migration-inventory/1.0",
                    "inventory_sha256": "4" * 64,
                    "json_bytes_sha256": "a" * 64,
                    "size": 400,
                },
            },
            "selection_policy": {
                "hard_max_samples": 50,
                "requested_limit": 1,
                "authoritative_state_filter": "[_]",
                "phase_order": [
                    "intake",
                    "statement",
                    "anchor_audit",
                    "obligation_tree",
                    "proof",
                    "validation",
                    "release",
                ],
                "phase_layers": {
                    "intake": 0,
                    "statement": 1,
                    "anchor_audit": 2,
                    "obligation_tree": 3,
                    "proof": 4,
                    "validation": 5,
                    "release": 6,
                },
                "allocation": "stable_round_robin_across_nonempty_phase_strata",
                "within_phase_order": ["v2_execution_rank", "item_id"],
                "output_order": ["phase_layer", "v2_execution_rank", "item_id"],
                "classification_counts_do_not_imply_acceptance": True,
            },
            "required_item_ids": [],
            "eligible_item_count": 1,
            "selected_item_count": 1,
            "eligible_phase_counts": {
                "intake": 1,
                "statement": 0,
                "anchor_audit": 0,
                "obligation_tree": 0,
                "proof": 0,
                "validation": 0,
                "release": 0,
            },
            "selected_phase_counts": {
                "intake": 1,
                "statement": 0,
                "anchor_audit": 0,
                "obligation_tree": 0,
                "proof": 0,
                "validation": 0,
                "release": 0,
            },
            "required_steps": lane["required_steps"],
            "lanes": [lane],
        }
        plan["plan_sha256"] = canonical_digest(plan)
        return plan

    def write_plan(self, plan: dict[str, object] | None = None) -> dict[str, object]:
        value = plan or self.plan()
        inventory: dict[str, object] = {
            "schema_version": "stage1-legacy-migration-inventory/1.0",
            "generated_from_revision": value["generated_from_revision"],
            "generated_from_tree": value["generated_from_tree"],
            "authority_mode": "authoritative_head",
            "authoritative_for_acceptance": False,
            "mutates_repository": False,
            "executes_validators": False,
            "blueprint": value["source_bindings"]["blueprint"],
            "contract": value["source_bindings"]["contract"],
        }
        inventory["inventory_sha256"] = canonical_digest(inventory)
        inventory_payload = (
            json.dumps(inventory, ensure_ascii=False, sort_keys=True) + "\n"
        ).encode()
        inventory_binding = value["source_bindings"]["inventory"]
        inventory_binding.update(
            inventory_sha256=inventory["inventory_sha256"],
            json_bytes_sha256=hashlib.sha256(inventory_payload).hexdigest(),
            size=len(inventory_payload),
        )
        lanes = value.get("lanes", [])
        for lane in lanes:
            lane["bindings"]["inventory_sha256"] = inventory["inventory_sha256"]
            lane["lane_sha256"] = canonical_digest(
                {key: field for key, field in lane.items() if key != "lane_sha256"}
            )
        value["plan_sha256"] = canonical_digest(
            {key: field for key, field in value.items() if key != "plan_sha256"}
        )
        (self.runtime / "legacy-migration-inventory.json").write_bytes(
            inventory_payload
        )
        self.plan_path.write_text(
            json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return value

    def stored_lane(self) -> dict[str, object]:
        return json.loads(self.plan_path.read_text(encoding="utf-8"))["lanes"][0]

    def plan_digest(self) -> str:
        return str(json.loads(self.plan_path.read_text(encoding="utf-8"))["plan_sha256"])

    def plan_file_digest(self) -> str:
        return hashlib.sha256(self.plan_path.read_bytes()).hexdigest()

    def claim(
        self, *, fresh: bool | None, include_bindings: bool = True
    ) -> dict[str, object]:
        claim: dict[str, object] = {
            "lane": cron.IMPLEMENTATION_LANE,
            "item_id": self.item["id"],
            "theorem_id": self.item["theorem_id"],
            "status": "finished_integrated",
            "runtime_protocol": cron.RUNTIME_PROTOCOL,
            "base_revision": self.HEAD,
            "claim_id": "20260716T120000Z-0123456789ab",
            "goal_objective": "implement exact item",
            "goal_objective_path": str(self.runtime / "goals" / "impl.txt"),
            "app_server_status": str(self.runtime / "app-server" / "impl.json"),
            "output_log": str(self.runtime / "logs" / "impl.out"),
            "workspace": str(self.runtime / "workers" / "slot1"),
            "selftest_manifest": str(
                self.runtime / "workers" / "slot1" / ".stage1-worker-selftest.json"
            ),
        }
        if fresh is not None:
            claim["fresh_revalidation"] = fresh
        if include_bindings:
            plan = json.loads(self.plan_path.read_text(encoding="utf-8"))
            lane = copy.deepcopy(plan["lanes"][0])
            claim.update(
                {
                    "legacy_revalidation_lane": lane,
                    "legacy_revalidation_lane_sha256": lane["lane_sha256"],
                    "legacy_revalidation_plan_sha256": self.plan_digest(),
                    "legacy_revalidation_plan_file_sha256": self.plan_file_digest(),
                    "legacy_revalidation_plan_binding": {
                        "schema_version": cron.LEGACY_REVALIDATION_PLAN_BINDING_SCHEMA,
                        "plan_sha256": plan["plan_sha256"],
                        "plan_file_sha256": self.plan_file_digest(),
                        "generated_from_revision": plan["generated_from_revision"],
                        "generated_from_tree": plan["generated_from_tree"],
                        "source_bindings": plan["source_bindings"],
                        "lane_sha256s": [
                            candidate["lane_sha256"] for candidate in plan["lanes"]
                        ],
                    },
                }
            )
            binding = claim["legacy_revalidation_plan_binding"]
            claim["legacy_revalidation_plan_binding_sha256"] = canonical_digest(binding)
        return claim

    def integrated_historical_claim(self) -> dict[str, object]:
        claim = self.claim(fresh=True)
        claim["integrated_at"] = "2026-07-16T12:00:00+00:00"
        closure = {
            "schema_version": cron.LEGACY_REVALIDATION_INTEGRATION_SCHEMA,
            "item_id": self.item["id"],
            "theorem_id": self.item["theorem_id"],
            "phase": self.item["phase"],
            "plan_sha256": claim["legacy_revalidation_plan_sha256"],
            "plan_file_sha256": claim["legacy_revalidation_plan_file_sha256"],
            "plan_binding_sha256": claim[
                "legacy_revalidation_plan_binding_sha256"
            ],
            "lane_sha256": claim["legacy_revalidation_lane_sha256"],
            "base_revision": claim["base_revision"],
            "pre_attempts": self.item["attempts"],
            "post_attempts": self.item["attempts"] + 1,
            "integrated_at": claim["integrated_at"],
        }
        claim["legacy_revalidation_integration"] = closure
        claim["legacy_revalidation_integration_sha256"] = canonical_digest(closure)
        return claim

    def runtime_patches(self):
        return (
            mock.patch.object(cron, "ROOT", self.root),
            mock.patch.object(cron, "RUNTIME", self.runtime),
            mock.patch.object(
                cron,
                "run",
                side_effect=lambda argv, **_kwargs: subprocess.CompletedProcess(
                    argv,
                    0,
                    (self.HEAD if "HEAD^{commit}" in argv else self.TREE) + "\n",
                    "",
                ),
            ),
        )

    def test_normal_fresh_source_without_legacy_lane_enters_review_frontier(self) -> None:
        claim = self.claim(fresh=False, include_bindings=False)
        with (
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, self.nodes)),
            mock.patch.object(
                cron, "read_persisted_worker_handoff", return_value=(b"{}", "a" * 64, Path("archive"))
            ),
        ):
            claim.update({
                "worker_handoff_archive_schema": cron.WORKER_HANDOFF_ARCHIVE_SCHEMA,
                "worker_handoff_path": str(
                    self.runtime / "worker-handoffs" / f"{claim['claim_id']}.json"
                ),
                "worker_handoff_sha256": "a" * 64,
                "worker_handoff_size": 2,
            })
            self.assertEqual(cron.review_candidates([self.item], [claim]), [self.item])
            self.assertIs(cron.review_source_claim(self.item, [claim]), claim)
        self.assertIsNone(cron.claim_legacy_revalidation_lane(claim, self.item))

    def test_historical_fresh_source_requires_exact_lane_and_plan_binding(self) -> None:
        self.write_plan()
        claim = self.claim(fresh=True)
        expected_lane = copy.deepcopy(claim["legacy_revalidation_lane"])
        # A claim's immutable bindings remain verifiable after the optional
        # planning file rotates; current runtime plan bytes are not authority.
        self.plan_path.unlink()
        with self.runtime_patches()[0], self.runtime_patches()[1], self.runtime_patches()[2]:
            self.assertEqual(
                cron.claim_legacy_revalidation_lane(claim, self.item), expected_lane
            )

    def test_current_exact_plan_admits_only_its_historical_lane(self) -> None:
        self.write_plan()
        patches = self.runtime_patches()
        source_bindings = self.plan()["source_bindings"]
        with (
            patches[0], patches[1], patches[2],
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, self.nodes)),
            mock.patch.object(
                cron, "_head_blob_binding",
                side_effect=lambda relative: source_bindings[{
                    "Docs/Stage1_Blueprint_v2.md": "blueprint",
                    "Docs/Stage1_Theorem_DAG_v2.json": "theorem_dag",
                    "Docs/Stage1_Phase_Acceptance_Contracts.json": "contract",
                }[relative]],
            ),
            mock.patch.object(cron, "load_blueprint_items", return_value=[self.item]),
        ):
            self.assertEqual(
                cron.legacy_revalidation_lanes(),
                {self.item["id"]: self.stored_lane()},
            )
            self.assertEqual(
                cron.implementation_candidates([self.open_item, self.item], []),
                [self.item, self.open_item],
            )

    def test_true_without_or_with_tampered_lane_is_rejected(self) -> None:
        self.write_plan()
        missing = self.claim(fresh=True, include_bindings=False)
        with self.assertRaisesRegex(ValueError, "revalidation|content-bound|binding"):
            cron.claim_legacy_revalidation_lane(missing, self.item)

        tampered = self.claim(fresh=True)
        tampered_lane = copy.deepcopy(tampered["legacy_revalidation_lane"])
        tampered_lane["attempts_at_plan_base"] = 99
        tampered["legacy_revalidation_lane"] = tampered_lane
        with self.assertRaisesRegex(ValueError, "revalidation|content-bound|binding"):
            cron.claim_legacy_revalidation_lane(tampered, self.item)

    def test_false_with_any_legacy_binding_is_rejected(self) -> None:
        self.write_plan()
        for field in (
            "legacy_revalidation_lane",
            "legacy_revalidation_lane_sha256",
            "legacy_revalidation_plan_sha256",
            "legacy_revalidation_plan_file_sha256",
            "legacy_revalidation_plan_binding",
            "legacy_revalidation_plan_binding_sha256",
        ):
            with self.subTest(field=field):
                claim = self.claim(fresh=False, include_bindings=False)
                claim[field] = self.claim(fresh=True)[field]
                with self.assertRaisesRegex(ValueError, "revalidation|legacy|binding"):
                    cron.claim_legacy_revalidation_lane(claim, self.item)

    def test_missing_fresh_provenance_is_fail_closed(self) -> None:
        claim = self.claim(fresh=None, include_bindings=False)
        with self.assertRaisesRegex(ValueError, "fresh_revalidation|revalidation"):
            cron.claim_legacy_revalidation_lane(claim, self.item)
        self.assertIsNone(cron.review_source_claim(self.item, [claim]))

    def test_stale_plan_isolated_without_blocking_open_candidates(self) -> None:
        self.write_plan(self.plan(revision="d" * 40))
        patches = self.runtime_patches()
        with patches[0], patches[1], patches[2], mock.patch.object(
            cron, "theorem_dag_v2", return_value=({}, self.nodes)
        ):
            self.assertEqual(cron.legacy_revalidation_lanes(), {})
            self.assertEqual(
                cron.implementation_candidates([self.item, self.open_item], []),
                [self.open_item],
            )

    def test_malformed_current_plan_cannot_starve_open_candidates(self) -> None:
        self.plan_path.write_text('{"broken":true}\n', encoding="utf-8")
        patches = self.runtime_patches()
        with (
            patches[0], patches[1], patches[2],
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, self.nodes)),
            mock.patch.object(
                cron, "load_blueprint_items", return_value=[self.item, self.open_item]
            ),
        ):
            self.assertEqual(
                cron.implementation_candidates([self.item, self.open_item], []),
                [self.open_item],
            )

    def test_historical_claim_rejects_cross_head_integration(self) -> None:
        self.write_plan()
        claim = self.claim(fresh=True)
        advanced = "d" * 40
        with (
            mock.patch.object(
                cron,
                "run",
                side_effect=lambda argv, **_kwargs: subprocess.CompletedProcess(
                    argv,
                    0,
                    (advanced if "HEAD^{commit}" in argv else self.TREE) + "\n",
                    "",
                ),
            ),
            self.assertRaisesRegex(
                ValueError, "current HEAD|authority|binding is not exact"
            ),
        ):
            cron.current_claim_legacy_revalidation_lane(claim, self.item)

    def test_post_integration_attempt_increment_requires_current_head_rerun(self) -> None:
        self.write_plan()
        claim = self.integrated_historical_claim()
        pre_attempts = self.item["attempts"]
        post_item = {**self.item, "attempts": pre_attempts + 1}
        self.plan_path.unlink()
        self.assertEqual(
            cron.post_integration_legacy_revalidation_lane(claim, post_item),
            claim["legacy_revalidation_lane"],
        )
        tampered = copy.deepcopy(claim)
        tampered["legacy_revalidation_integration"]["post_attempts"] += 1
        tampered["legacy_revalidation_integration_sha256"] = canonical_digest(
            tampered["legacy_revalidation_integration"]
        )
        with self.assertRaisesRegex(ValueError, "integration closure"):
            cron.post_integration_legacy_revalidation_lane(tampered, post_item)

    def test_historical_source_missing_validator_at_base_requires_rerun_not_review(self) -> None:
        self.write_plan()
        claim = self.integrated_historical_claim()
        post_item = {**self.item, "attempts": self.item["attempts"] + 1}
        old_review = {
            "lane": cron.REVIEW_LANE,
            "item_id": self.item["id"],
            "status": "review_failed",
        }
        claims = [claim, old_review]
        with mock.patch.object(
            cron,
            "select_review_validator",
            side_effect=SystemExit("selected validator did not exist at the worker base"),
        ):
            self.assertTrue(
                cron.reconcile_historical_revalidation_sources([post_item], claims)
            )
        self.assertEqual(claim["status"], "revalidation_required")
        self.assertEqual(old_review["status"], "superseded")
        self.assertEqual(old_review["superseded_by_claim_id"], claim["claim_id"])
        with (
            mock.patch.object(
                cron,
                "optional_legacy_revalidation_lanes",
                return_value={self.item["id"]: self.lane()},
            ),
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, self.nodes)),
        ):
            self.assertEqual(
                cron.implementation_candidates([post_item], claims), [post_item]
            )
            self.assertEqual(cron.review_candidates([post_item], claims), [])

    def test_historical_successor_validator_mismatch_is_quarantined_not_requeued(self) -> None:
        self.write_plan()
        claim = self.integrated_historical_claim()
        claim["revalidation_predecessor_claim_id"] = (
            "20260716T120000Z-0123456789ab"
        )
        post_item = {**self.item, "attempts": self.item["attempts"] + 1}
        with mock.patch.object(
            cron,
            "select_review_validator",
            side_effect=SystemExit(
                "selected validator HEAD blob differs from worker-base blob"
            ),
        ):
            self.assertTrue(
                cron.reconcile_historical_revalidation_sources([post_item], [claim])
            )
        self.assertEqual(claim["status"], "quarantined")
        self.assertIn("successor", claim["quarantine_reason"])
        self.assertNotIn("revalidation_required_at", claim)

    def test_malformed_historical_integration_is_quarantined_not_requeued(self) -> None:
        self.write_plan()
        claim = self.integrated_historical_claim()
        claim["legacy_revalidation_integration"]["post_attempts"] += 1
        claim["legacy_revalidation_integration_sha256"] = canonical_digest(
            claim["legacy_revalidation_integration"]
        )
        post_item = {**self.item, "attempts": self.item["attempts"] + 1}
        self.assertTrue(
            cron.reconcile_historical_revalidation_sources([post_item], [claim])
        )
        self.assertEqual(claim["status"], "quarantined")
        self.assertIn("integration closure", claim["quarantine_reason"])

    def test_required_source_rebuild_passes_exact_required_item_ids(self) -> None:
        self.write_plan()
        required_claim = self.integrated_historical_claim()
        required_claim["status"] = "revalidation_required"
        post_item = {**self.item, "attempts": self.item["attempts"] + 1}
        with (
            mock.patch.object(cron, "optional_legacy_revalidation_lanes", return_value={}),
            mock.patch.object(cron, "rebuild_legacy_revalidation_plan") as rebuild,
            mock.patch.object(
                cron,
                "legacy_revalidation_lanes",
                return_value={self.item["id"]: self.lane()},
            ),
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, self.nodes)),
        ):
            self.assertTrue(
                cron.ensure_revalidation_plan_for_required_sources(
                    [post_item], [required_claim]
                )
            )
        rebuild.assert_called_once_with([self.item["id"]])

    def test_second_historical_pass_supersedes_old_source_and_becomes_review_source(self) -> None:
        self.write_plan()
        old_source = self.integrated_historical_claim()
        old_source["status"] = "revalidation_required"
        new_source = self.claim(fresh=True)
        new_source["claim_id"] = "20260717T120000Z-fedcba987654"
        new_source["base_revision"] = "d" * 40
        new_source["legacy_revalidation_lane"]["authority_revision"] = "d" * 40
        new_source["legacy_revalidation_plan_binding"]["generated_from_revision"] = "d" * 40
        new_source["legacy_revalidation_plan_binding_sha256"] = canonical_digest(
            new_source["legacy_revalidation_plan_binding"]
        )
        new_source["integrated_at"] = "2026-07-17T12:00:00+00:00"
        new_source["revalidation_predecessor_claim_id"] = old_source["claim_id"]
        claims = [old_source, new_source]
        self.assertTrue(cron.supersede_revalidation_predecessors(new_source, claims))
        self.assertEqual(old_source["status"], "superseded")
        self.assertEqual(
            old_source["superseded_by_claim_id"], new_source["claim_id"]
        )
        new_source.update({
            "worker_handoff_archive_schema": cron.WORKER_HANDOFF_ARCHIVE_SCHEMA,
            "worker_handoff_path": str(
                self.runtime / "worker-handoffs" / f"{new_source['claim_id']}.json"
            ),
            "worker_handoff_sha256": "a" * 64,
            "worker_handoff_size": 2,
        })
        with mock.patch.object(
            cron, "read_persisted_worker_handoff", return_value=(b"{}", "a" * 64, Path("archive"))
        ):
            self.assertIs(cron.review_source_claim(self.item, claims), new_source)

    def test_resigned_claim_cannot_replace_head_owned_plan(self) -> None:
        plan = self.write_plan()
        claim = self.claim(fresh=True)
        forged_lane = copy.deepcopy(claim["legacy_revalidation_lane"])
        forged_lane["legacy_migration_ready_observation"] = True
        forged_lane["lane_sha256"] = canonical_digest(
            {
                key: value
                for key, value in forged_lane.items()
                if key != "lane_sha256"
            }
        )
        claim["legacy_revalidation_lane"] = forged_lane
        claim["legacy_revalidation_lane_sha256"] = forged_lane["lane_sha256"]
        binding = copy.deepcopy(claim["legacy_revalidation_plan_binding"])
        binding["lane_sha256s"] = [forged_lane["lane_sha256"]]
        claim["legacy_revalidation_plan_binding"] = binding
        claim["legacy_revalidation_plan_binding_sha256"] = canonical_digest(binding)
        source_bindings = plan["source_bindings"]
        patches = self.runtime_patches()
        with (
            patches[0], patches[1], patches[2],
            mock.patch.object(cron, "theorem_dag_v2", return_value=({}, self.nodes)),
            mock.patch.object(
                cron, "_head_blob_binding",
                side_effect=lambda relative: source_bindings[{
                    "Docs/Stage1_Blueprint_v2.md": "blueprint",
                    "Docs/Stage1_Theorem_DAG_v2.json": "theorem_dag",
                    "Docs/Stage1_Phase_Acceptance_Contracts.json": "contract",
                }[relative]],
            ),
            mock.patch.object(cron, "load_blueprint_items", return_value=[self.item]),
            self.assertRaisesRegex(
                (ValueError, SystemExit),
                "HEAD-owned plan|no longer matches|inventory|source binding",
            ),
        ):
            cron.current_claim_legacy_revalidation_lane(claim, self.item)

    def test_plan_source_binding_tamper_fails_closed(self) -> None:
        plan = self.plan()
        plan["source_bindings"]["blueprint"]["sha256"] = "f" * 64
        plan["plan_sha256"] = canonical_digest(
            {key: value for key, value in plan.items() if key != "plan_sha256"}
        )
        self.write_plan(plan)
        patches = self.runtime_patches()
        with patches[0], patches[1], patches[2], self.assertRaisesRegex(
            (SystemExit, ValueError), "binding|content-bound|malformed|authority"
        ):
            cron.legacy_revalidation_lanes()

    def test_plan_required_ids_must_be_selected_and_digest_bound(self) -> None:
        plan = self.plan()
        plan["required_item_ids"] = ["S56-M-9999-INTAKE"]
        plan["plan_sha256"] = canonical_digest(
            {key: value for key, value in plan.items() if key != "plan_sha256"}
        )
        self.write_plan(plan)
        patches = self.runtime_patches()
        with patches[0], patches[1], patches[2], self.assertRaisesRegex(
            SystemExit, "malformed"
        ):
            cron.legacy_revalidation_lanes()

    def test_lane_binding_tamper_fails_closed_even_with_resigned_digests(self) -> None:
        plan = self.plan()
        lane = plan["lanes"][0]
        lane["bindings"]["contract_sha256"] = "f" * 64
        lane["lane_sha256"] = canonical_digest(
            {key: value for key, value in lane.items() if key != "lane_sha256"}
        )
        plan["plan_sha256"] = canonical_digest(
            {key: value for key, value in plan.items() if key != "plan_sha256"}
        )
        self.write_plan(plan)
        patches = self.runtime_patches()
        with patches[0], patches[1], patches[2], self.assertRaisesRegex(
            (SystemExit, ValueError), "binding|content-bound|malformed|authority"
        ):
            cron.legacy_revalidation_lanes()

    def test_claim_plan_digest_is_exact_not_just_hex_shaped(self) -> None:
        self.write_plan()
        claim = self.claim(fresh=True)
        self.assertNotEqual(claim["legacy_revalidation_plan_sha256"], "e" * 64)
        claim["legacy_revalidation_plan_sha256"] = "e" * 64
        patches = self.runtime_patches()
        with patches[0], patches[1], patches[2], self.assertRaisesRegex(
            ValueError, "plan|content-bound|binding"
        ):
            cron.claim_legacy_revalidation_lane(claim, self.item)

    def test_claim_plan_binding_requires_exact_lane_membership_and_sources(self) -> None:
        self.write_plan()
        claim = self.claim(fresh=True)
        for field, replacement in (
            ("lane_sha256s", ["e" * 64]),
            (
                "source_bindings",
                {
                    **claim["legacy_revalidation_plan_binding"]["source_bindings"],
                    "blueprint": {
                        **claim["legacy_revalidation_plan_binding"]["source_bindings"]["blueprint"],
                        "sha256": "e" * 64,
                    },
                },
            ),
        ):
            with self.subTest(field=field):
                tampered = copy.deepcopy(claim)
                tampered["legacy_revalidation_plan_binding"][field] = replacement
                tampered["legacy_revalidation_plan_binding_sha256"] = canonical_digest(
                    tampered["legacy_revalidation_plan_binding"]
                )
                patches = self.runtime_patches()
                with patches[0], patches[1], patches[2], self.assertRaisesRegex(
                    ValueError, "plan|content-bound|binding"
                ):
                    cron.claim_legacy_revalidation_lane(tampered, self.item)


if __name__ == "__main__":
    unittest.main()
