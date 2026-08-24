#!/usr/bin/env python3
"""Mutation tests for the Stage5 conjecture claim validator."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts/check_stage5_conjecture_claim.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


validator = load(VALIDATOR_PATH, "stage5_conjecture_claim_test_validator")


class Stage5ConjectureClaimTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        try:
            cls.specification, rows, cls.blueprint_raw = validator.blueprint_context()
        except RuntimeError as exc:
            if "embedded conjecture execution specification is stale" not in str(exc):
                raise
            checker = validator.load_checker()
            manager = checker.manager()
            cls.specification = manager.spec_object(manager.CONJECTURE)
            tasks = manager.expected_tasks(manager.CONJECTURE)
            cls.blueprint_raw = manager.render_blueprint(manager.CONJECTURE, tasks)
            rows = {
                task.item_id: {
                    "item_id": task.item_id, "state": task.state,
                    "title": task.title, "dependencies": list(task.dependencies),
                    "owned_paths": list(task.owned_paths), "gate": task.gate,
                }
                for task in tasks
            }
        cls.item = next(row for row in rows.values() if row["item_id"].endswith("-TARGET"))
        cls.intake_item = next(
            row for row in rows.values()
            if row["item_id"].startswith("S5CON-POOL-")
            and row["item_id"].endswith("-INTAKE")
        )

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="stage5-conjecture-claim-test-")
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        self.original_runtime = validator.RUNTIME
        validator.RUNTIME = root / "runtime"
        self.addCleanup(setattr, validator, "RUNTIME", self.original_runtime)
        self.claim_id = self.item["item_id"] + "--producer"
        self.run_id = "r-fixture"
        self.task = validator.RUNTIME / "tasks" / self.claim_id / self.run_id
        self.work = self.task / "work"
        self.work.mkdir(parents=True)
        source = validator.EVIDENCE / "workset-5.6-receipt.json"
        target = self.work / source.relative_to(ROOT)
        target.parent.mkdir(parents=True)
        shutil.copyfile(source, target)
        self.read_only = [{
            "path": source.relative_to(ROOT).as_posix(),
            "sha256": validator.file_digest(target),
            "size_bytes": target.stat().st_size,
        }]
        baseline = self.work / "_baseline/Stage5_Conjectures_Blueprint.md"
        baseline.parent.mkdir(parents=True)
        baseline.write_bytes(cls_blueprint := self.blueprint_raw)
        self.read_only.append({
            "path": "_baseline/Stage5_Conjectures_Blueprint.md",
            "sha256": validator.digest(cls_blueprint),
            "size_bytes": len(cls_blueprint),
        })
        workset = json.loads((validator.EVIDENCE / "workset-5.6.json").read_text())
        member = next(
            row for row in workset["members"]
            if row["target_item_id"] == self.item["item_id"]
        )
        member_path = self.work / "_baseline/workset-member.json"
        member_path.write_text(
            json.dumps(member, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        )
        self.read_only.append({
            "path": "_baseline/workset-member.json",
            "sha256": validator.file_digest(member_path),
            "size_bytes": member_path.stat().st_size,
        })
        prompt_source = validator.EVIDENCE / "execution/concurrency-prompt.json"
        prompt_target = self.work / "_baseline/concurrency-prompt.json"
        shutil.copyfile(prompt_source, prompt_target)
        self.read_only.append({
            "path": "_baseline/concurrency-prompt.json",
            "sha256": validator.file_digest(prompt_target),
            "size_bytes": prompt_target.stat().st_size,
        })
        maxima = self.specification["operator_budget_policy"]["finite_initial_allowances"]["per_claim_maxima"]
        prompt_raw = (validator.EVIDENCE / "execution/concurrency-prompt.json").read_bytes()
        prompt = json.loads(prompt_raw)
        owned = list(self.item["owned_paths"])
        self.claim = {
            "schema_version": "awesome-theorems/stage5-proof-debt-claim-card/1.1",
            "program": validator.PROGRAM,
            "claim_id": self.claim_id,
            "run_id": self.run_id,
            "item_id": self.item["item_id"],
            "mode": validator.mode_for(self.item["item_id"]),
            "dependencies": list(self.item["dependencies"]),
            "baseline": {
                "execution_spec_sha256": validator.digest(validator.canonical(self.specification)),
                "blueprint_sha256": validator.digest(self.blueprint_raw),
                "source_bundle_sha256": self.specification["source_bundle"]["sha256"],
                "dependency_state_sha256": "1" * 64,
                "owned_paths_baseline_sha256": "2" * 64,
            },
            "deadline": "2027-01-01T00:00:00Z",
            "task_root": str(self.task),
            "canonical_repository_root": str(ROOT),
            "canonical_write_policy": "forbidden",
            "writable_paths": owned,
            "read_only_bootstrap_files": self.read_only,
            "deliverable": "fixture exact item deliverable",
            "execution_identity": {
                "lane_id": self.item["item_id"], "generation_id": self.run_id,
                "prompt_epoch": prompt["policy_epoch"],
                "prompt_digest": validator.digest(prompt_raw),
                "execution_spec_sha256": validator.digest(validator.canonical(self.specification)),
                "requested_concurrency": prompt["concurrency"],
                "resolved_concurrency": prompt["concurrency"],
            },
            "workset_member": {
                "member_id": member["member_id"],
                "member_kind": member["member_kind"],
                "target_item_id": member["target_item_id"],
                "workset_record_sha256": member["workset_record_sha256"],
                "source_record_sha256": member["record_sha256"],
            },
            "work_contract": {
                "kind": "strict_resolution_proof_search",
                "strict_resolution_proof_search": self.specification["conjecture_proof_search_prompt"],
            },
            "validation_commands": [{
                "command_id": "fixture", "cwd": ".", "argv": ["/usr/bin/true"],
                "environment": [], "timeout_seconds": 10, "network": "denied",
            }],
            "artifact_policy": {
                "allowed_paths": owned, "required_paths": owned,
                "forbidden_paths": [
                    "Docs/Stage5_Conjectures_Blueprint.md", "Docs/Stage5_Conjectures_Gantt.md",
                    "Docs/catalog", ".git", ".ops",
                ],
            },
            "result_schema": {
                "path": "Docs/evidence/stage5_conjectures/worker-result.schema.json",
                "schema_id": validator.load_schema("worker-result.schema.json")["$id"],
                "sha256": validator.file_digest(validator.EVIDENCE / "worker-result.schema.json"),
            },
            "resource_budget": {
                key: ("unbounded" if key == "model_turns" else min(maxima[key], 10))
                for key in (
                    "model_input_tokens", "model_output_tokens", "model_turns",
                    "external_launches", "wall_seconds", "cpu_seconds",
                )
            },
            "retry_budget": {"attempt": 1, "max_attempts": 3},
        }
        self.claim_path = self.task / "claim.json"
        self.write_json(self.claim_path, self.claim)

    def validate_result(self, result_path: Path) -> dict[str, object]:
        # Result-focused mutation tests keep the already validated immutable
        # claim in memory; claim mutations are exercised separately above.
        original = validator.validate_claim
        validator.validate_claim = lambda _path: self.claim
        try:
            return validator.validate_result(result_path, self.claim_path)
        finally:
            validator.validate_claim = original

    @staticmethod
    def write_json(path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")

    def test_valid_claim_and_closed_schema(self) -> None:
        observed = validator.validate_claim(self.claim_path)
        self.assertEqual(observed["item_id"], self.item["item_id"])
        for filename in ("claim-card.schema.json", "worker-result.schema.json", "master-acceptance.schema.json"):
            self.assertFalse(validator.load_schema(filename)["additionalProperties"])

    def test_claim_rejects_extra_field_path_escape_and_budget_overrun(self) -> None:
        mutations = (
            lambda value: value.update(extra=True),
            lambda value: value.__setitem__("writable_paths", ["../escape"]),
            lambda value: value["resource_budget"].__setitem__("model_turns", 1001),
            lambda value: value["artifact_policy"].__setitem__("allowed_paths", ["other.json"]),
            lambda value: value["work_contract"]["strict_resolution_proof_search"].__setitem__(
                "completion_rule", "a polished summary is enough"
            ),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                value = json.loads(json.dumps(self.claim))
                mutation(value)
                self.write_json(self.claim_path, value)
                with self.assertRaises((validator.ClaimError, RuntimeError)):
                    validator.validate_claim(self.claim_path)
                self.write_json(self.claim_path, self.claim)

    def test_result_binds_exact_paths_patch_artifacts_and_seal(self) -> None:
        owned = self.claim["writable_paths"]
        artifacts = []
        for relative in owned:
            artifact_path = self.work / relative
            artifact_path.parent.mkdir(parents=True, exist_ok=True)
            artifact_path.write_text("fixture\n")
            artifacts.append({
                "path": str(artifact_path), "sha256": validator.file_digest(artifact_path),
                "size_bytes": artifact_path.stat().st_size, "media_type": "text/plain",
            })
        patch = self.task / "changes.patch"
        patch.write_text("diff --git a/x b/x\n")
        by_relative = {
            Path(artifact["path"]).relative_to(self.work).as_posix(): artifact
            for artifact in artifacts
        }
        body = {
            "schema_version": "awesome-theorems/stage5-proof-debt-worker-result/1.0",
            "program": self.claim["program"], "claim_id": self.claim_id,
            "run_id": self.run_id, "item_id": self.item["item_id"], "mode": self.claim["mode"],
            "claim_card_sha256": validator.file_digest(self.claim_path),
            "baseline_sha256": validator.digest(validator.canonical(self.claim["baseline"])),
            "status": "self_tested", "changed_paths": owned,
            "patch": {"path": str(patch), "sha256": validator.file_digest(patch), "size_bytes": patch.stat().st_size},
            "command_outcomes": [{
                "command_id": "fixture", "argv_sha256": validator.digest(
                    validator.canonical(self.claim["validation_commands"][0]["argv"])
                ), "exit_code": 0,
                "passed": True, "stdout_sha256": "4" * 64, "stderr_sha256": "5" * 64,
                "started_at": "2026-08-11T00:00:00Z", "finished_at": "2026-08-11T00:00:01Z",
            }],
            "artifacts": artifacts,
            "completed_at": "2026-08-11T00:00:01Z",
            "typed_outcome": {
                "kind": "strict_resolution", "polarity": "Claim",
                "human_resolution_sha256": by_relative[next(
                    item for item in owned if item.endswith("/human-resolution.md")
                )]["sha256"],
                "lean_root_sha256": by_relative[next(
                    item for item in owned if item.endswith("/Proof.lean")
                )]["sha256"],
                "machine_cut_set_empty": True, "readability_cut_set_empty": True,
            },
        }
        result = dict(body)
        result["authority_sha256"] = validator.digest(validator.canonical(body))
        result_path = self.task / "result.json"
        self.write_json(result_path, result)
        self.assertEqual(self.validate_result(result_path)["status"], "self_tested")
        result["changed_paths"] = ["outside.json"]
        body = dict(result); body.pop("authority_sha256", None)
        result["authority_sha256"] = validator.digest(validator.canonical(body))
        self.write_json(result_path, result)
        with self.assertRaises(validator.ClaimError):
            self.validate_result(result_path)

        valid_body = json.loads(json.dumps(body))
        valid_body["changed_paths"] = owned
        for mutation in (
            lambda value: value.pop("typed_outcome"),
            lambda value: value["artifacts"].pop(),
            lambda value: value["typed_outcome"].__setitem__("human_resolution_sha256", "9" * 64),
            lambda value: value["typed_outcome"].__setitem__("lean_root_sha256", "8" * 64),
            lambda value: value.__setitem__("typed_outcome", {
                "kind": "source_occurrence_intake",
                "status_review_sha256": "1" * 64, "rights_review_sha256": "2" * 64,
                "importance_review_sha256": "3" * 64,
                "identity_relation": "new_identity", "identity_crosswalk_sha256": "4" * 64,
                "strict_credit_granted": False, "stage5_claim_id_allocated": False,
                "stage6_alias_allocated": False,
            }),
        ):
            with self.subTest(mutation=mutation):
                mutated = json.loads(json.dumps(valid_body))
                mutation(mutated)
                unsigned = dict(mutated); unsigned.pop("authority_sha256", None)
                mutated["authority_sha256"] = validator.digest(validator.canonical(unsigned))
                self.write_json(result_path, mutated)
                with self.assertRaises(validator.ClaimError):
                    self.validate_result(result_path)

    def test_intake_result_binds_reviews_and_grants_zero_credit(self) -> None:
        self.item = self.intake_item
        self.claim_id = self.item["item_id"] + "--producer"
        self.task = validator.RUNTIME / "tasks" / self.claim_id / self.run_id
        self.work = self.task / "work"
        self.work.mkdir(parents=True)
        baseline = self.work / "_baseline/Stage5_Conjectures_Blueprint.md"
        baseline.parent.mkdir(parents=True)
        baseline.write_bytes(self.blueprint_raw)
        prompt_target = self.work / "_baseline/concurrency-prompt.json"
        shutil.copyfile(
            validator.EVIDENCE / "execution/concurrency-prompt.json", prompt_target
        )
        workset = json.loads((validator.EVIDENCE / "workset-5.6.json").read_text())
        member = next(row for row in workset["members"] if row["target_item_id"] == self.item["item_id"])
        member_path = self.work / "_baseline/workset-member.json"
        self.write_json(member_path, member)
        prompt_target = self.work / "_baseline/concurrency-prompt.json"
        shutil.copyfile(validator.EVIDENCE / "execution/concurrency-prompt.json", prompt_target)
        source_record_path = self.work / "_baseline/source-record.json"
        # The semantic validator binds canonical JSON to the workset hash.  Use
        # the pinned first occurrence through the same controller materializer
        # rather than fabricating source bytes in this mutation fixture.
        controller_path = ROOT / "scripts/stage5_conjectures_execution_cron_v2.py"
        controller = load(controller_path, "stage5_conjecture_claim_intake_source_fixture")
        original_controller_runtime = controller.RUNTIME
        controller.RUNTIME = Path(self.temporary.name) / "source-runtime"
        prompt_raw = (validator.EVIDENCE / "execution/concurrency-prompt.json").read_bytes()
        prompt = json.loads(prompt_raw)
        try:
            materialized = controller.materialize(
                self.item, self.specification, self.blueprint_raw,
                generation_id="r-source-fixture", lane_id=self.item["item_id"],
                prompt=prompt, prompt_digest=validator.digest(prompt_raw),
            )
            source_record_path.write_bytes(
                (Path(materialized["task_root"]) / "work/_baseline/source-record.json").read_bytes()
            )
        finally:
            controller.RUNTIME = original_controller_runtime
        self.claim.update({
            "claim_id": self.claim_id, "item_id": self.item["item_id"],
            "mode": validator.mode_for(self.item["item_id"]),
            "dependencies": list(self.item["dependencies"]), "task_root": str(self.task),
            "writable_paths": list(self.item["owned_paths"]),
            "workset_member": {
                "member_id": member["member_id"], "member_kind": member["member_kind"],
                "target_item_id": member["target_item_id"],
                "workset_record_sha256": member["workset_record_sha256"],
                "source_record_sha256": member["record_sha256"],
            },
            "work_contract": {
                "kind": "source_occurrence_intake",
                "source_occurrence_intake": self.specification["conjecture_occurrence_intake_contract"],
            },
        })
        self.claim["execution_identity"]["lane_id"] = self.item["item_id"]
        self.claim["execution_identity"]["generation_id"] = self.run_id
        owned = self.claim["writable_paths"]
        self.claim["artifact_policy"]["allowed_paths"] = owned
        self.claim["artifact_policy"]["required_paths"] = owned
        self.claim["read_only_bootstrap_files"] = [
            {"path": "_baseline/Stage5_Conjectures_Blueprint.md", "sha256": validator.file_digest(baseline), "size_bytes": baseline.stat().st_size},
            {"path": "_baseline/workset-member.json", "sha256": validator.file_digest(member_path), "size_bytes": member_path.stat().st_size},
            {"path": "_baseline/source-record.json", "sha256": validator.file_digest(source_record_path), "size_bytes": source_record_path.stat().st_size},
            {"path": "_baseline/concurrency-prompt.json", "sha256": validator.file_digest(self.work / "_baseline/concurrency-prompt.json"), "size_bytes": (self.work / "_baseline/concurrency-prompt.json").stat().st_size},
        ]
        self.claim_path = self.task / "claim.json"
        self.write_json(self.claim_path, self.claim)

        artifacts = []
        digests = {}
        for relative in owned:
            artifact_path = self.work / relative
            artifact_path.parent.mkdir(parents=True, exist_ok=True)
            artifact_path.write_text("fixture\n")
            digests[relative] = validator.file_digest(artifact_path)
            artifacts.append({"path": str(artifact_path), "sha256": digests[relative], "size_bytes": artifact_path.stat().st_size, "media_type": "text/plain"})
        patch = self.task / "changes.patch"
        patch.write_text("diff --git a/x b/x\n")
        outcome = {
            "kind": "source_occurrence_intake",
            "status_review_sha256": digests[next(item for item in owned if item.endswith("/status-review.json"))],
            "rights_review_sha256": digests[next(item for item in owned if item.endswith("/rights-review.json"))],
            "importance_review_sha256": digests[next(item for item in owned if item.endswith("/importance-review.json"))],
            "identity_relation": "new_identity",
            "identity_crosswalk_sha256": digests[next(item for item in owned if item.endswith("/identity-crosswalk.json"))],
            "strict_credit_granted": False, "stage5_claim_id_allocated": False,
            "stage6_alias_allocated": False,
        }
        body = {
            "schema_version": "awesome-theorems/stage5-proof-debt-worker-result/1.0",
            "program": self.claim["program"], "claim_id": self.claim_id, "run_id": self.run_id,
            "item_id": self.item["item_id"], "mode": self.claim["mode"],
            "claim_card_sha256": validator.file_digest(self.claim_path),
            "baseline_sha256": validator.digest(validator.canonical(self.claim["baseline"])),
            "status": "self_tested", "changed_paths": owned,
            "patch": {"path": str(patch), "sha256": validator.file_digest(patch), "size_bytes": patch.stat().st_size},
            "command_outcomes": [{"command_id": "fixture", "argv_sha256": validator.digest(validator.canonical(["/usr/bin/true"])), "exit_code": 0, "passed": True, "stdout_sha256": "4" * 64, "stderr_sha256": "5" * 64, "started_at": "2026-08-11T00:00:00Z", "finished_at": "2026-08-11T00:00:01Z"}],
            "artifacts": artifacts, "completed_at": "2026-08-11T00:00:01Z",
            "typed_outcome": outcome,
        }
        result_path = self.task / "result.json"
        body["authority_sha256"] = validator.digest(validator.canonical(body))
        self.write_json(result_path, body)
        self.assertEqual(self.validate_result(result_path)["typed_outcome"], outcome)

        for field in ("strict_credit_granted", "stage5_claim_id_allocated", "stage6_alias_allocated"):
            with self.subTest(field=field):
                mutated = json.loads(json.dumps(body))
                mutated["typed_outcome"][field] = True
                unsigned = dict(mutated); unsigned.pop("authority_sha256")
                mutated["authority_sha256"] = validator.digest(validator.canonical(unsigned))
                self.write_json(result_path, mutated)
                with self.assertRaises(validator.ClaimError):
                    self.validate_result(result_path)

        for mutation in (
            lambda value: value["typed_outcome"].__setitem__("status_review_sha256", "9" * 64),
            lambda value: value["typed_outcome"].__setitem__("rights_review_sha256", "9" * 64),
            lambda value: value["typed_outcome"].__setitem__("importance_review_sha256", "9" * 64),
            lambda value: value["typed_outcome"].__setitem__("identity_crosswalk_sha256", "9" * 64),
            lambda value: value.__setitem__("typed_outcome", {
                "kind": "strict_resolution", "polarity": "Claim",
                "human_resolution_sha256": "1" * 64, "lean_root_sha256": "2" * 64,
                "machine_cut_set_empty": True, "readability_cut_set_empty": True,
            }),
        ):
            with self.subTest(mutation=mutation):
                mutated = json.loads(json.dumps(body))
                mutation(mutated)
                unsigned = dict(mutated); unsigned.pop("authority_sha256", None)
                mutated["authority_sha256"] = validator.digest(validator.canonical(unsigned))
                self.write_json(result_path, mutated)
                with self.assertRaises(validator.ClaimError):
                    self.validate_result(result_path)

    def test_self_sealed_acceptance_cannot_name_a_missing_archive(self) -> None:
        """Regression: a schema-valid/self-sealed receipt is not authority."""
        item_id = self.item["item_id"]
        manager = validator.load_checker().manager()
        thread_id, objective_sha, _ = manager.operator_goal_binding(manager.CONJECTURE)
        typed = {
            "kind": "strict_resolution", "polarity": "Claim",
            "human_resolution_sha256": "1" * 64,
            "lean_root_sha256": "2" * 64,
            "machine_cut_set_empty": True, "readability_cut_set_empty": True,
        }
        body = {
            "schema_version": "awesome-theorems/stage5-proof-debt-master-acceptance/1.0",
            "program": validator.PROGRAM, "item_id": item_id,
            "mode": validator.mode_for(item_id),
            "master": {
                "principal_id": f"codex-user-goal:{thread_id}",
                "decision_id": "fixture-decision",
                "authentication_sha256": validator.digest(validator.canonical({
                    "thread_id": thread_id, "objective_sha256": objective_sha,
                })),
            },
            "handoff": {
                "claim_id": self.claim_id, "run_id": self.run_id,
                "claim_card_sha256": "3" * 64, "worker_result_sha256": "4" * 64,
                "baseline_sha256": "5" * 64, "patch_sha256": "6" * 64,
                "immutable_archive_path": (
                    "Docs/evidence/stage5_conjectures/execution/handoffs/"
                    f"{self.claim_id}/{'5' * 64}/{'6' * 64}"
                ),
                "immutable_archive_sha256": "7" * 64,
            },
            "review_decisions": [{
                "reviewer_id": "fixture-reviewer", "decision": "accepted",
                "decision_receipt_path": "Docs/nonexistent-review.json",
                "decision_receipt_sha256": "8" * 64,
            }],
            "integration": {
                "pre_tree_sha256": "9" * 64, "post_tree_sha256": "a" * 64,
                "integrated_bytes_sha256": "b" * 64,
                "integrated_files": [{
                    "path": self.item["owned_paths"][0], "sha256": "c" * 64,
                    "size_bytes": 1,
                }],
            },
            "validation_gates": [{
                "gate_id": "fixture", "command_sha256": "d" * 64,
                "exit_code": 0, "passed": True,
                "stdout_sha256": "e" * 64, "stderr_sha256": "f" * 64,
            }],
            "state_transition": {
                "from": "handoff_waiting_master", "to": "master_accepted",
                "pre_blueprint_sha256": "1" * 64,
                "post_blueprint_sha256": "2" * 64,
                "post_gantt_sha256": "3" * 64,
            },
            "workset_member": self.claim["workset_member"],
            "accepted_outcome": typed,
            "accepted_at": "2026-08-17T00:00:00Z",
        }
        value = dict(body)
        value["authority_sha256"] = validator.digest(validator.canonical(body))
        acceptance = Path(self.temporary.name) / "acceptance.json"
        self.write_json(acceptance, value)
        rows = {item_id: {**self.item, "state": "x"}}
        with mock.patch.object(
            validator, "blueprint_context",
            return_value=(self.specification, rows, self.blueprint_raw),
        ):
            with self.assertRaisesRegex(validator.ClaimError, "archive"):
                validator.validate_acceptance(acceptance)

    def _archived_handoff_fixture(self) -> tuple[Path, str, dict[str, object], list[str]]:
        """Build one current-authority archive after deleting its task root."""
        self.claim["claim_id"] = f"{self.item['item_id']}--worker"
        self.claim_id = self.claim["claim_id"]
        production_task = (
            ROOT / self.specification["runtime_root"] / "epochs"
            / self.specification["runtime_authority_epoch"] / "tasks"
            / self.claim_id / self.run_id
        )
        self.claim.update({
            "task_root": str(production_task),
            "deadline": "2027-08-12T00:00:00Z",
            "deliverable": f"{self.item['title']}. {self.item['gate']}",
            "validation_commands": [{
                "command_id": "claim-self-check", "cwd": ".",
                "argv": ["/usr/bin/python3", "-I", "-B", "-c", "pass"],
                "environment": [], "timeout_seconds": 30,
                "network": "denied",
            }],
            "resource_budget": {
                key: self.specification["operator_budget_policy"]
                ["finite_initial_allowances"]["per_claim_maxima"][key]
                for key in (
                    "model_input_tokens", "model_output_tokens", "model_turns",
                    "external_launches", "wall_seconds", "cpu_seconds",
                )
            },
        })
        self.claim["execution_identity"]["lane_id"] = self.item["item_id"]
        self.claim["execution_identity"]["generation_id"] = self.run_id
        authority_manager = validator.load_checker().manager()
        authority_spec = authority_manager.spec_object(authority_manager.CONJECTURE)
        authority_spec_sha = validator.digest(validator.canonical(authority_spec))
        self.claim["execution_identity"]["execution_spec_sha256"] = authority_spec_sha
        self.claim["baseline"]["execution_spec_sha256"] = authority_spec_sha
        self.claim["baseline"]["source_bundle_sha256"] = authority_spec[
            "source_bundle"
        ]["sha256"]
        reviewed_worker_schema = validator.reviewed_schema(
            "worker-result.schema.json"
        )
        reviewed_worker_raw = validator.reviewed_schema_bytes(
            "worker-result.schema.json"
        )
        self.claim["result_schema"] = {
            "path": "Docs/evidence/stage5_conjectures/worker-result.schema.json",
            "schema_id": reviewed_worker_schema["$id"],
            "sha256": validator.digest(reviewed_worker_raw),
        }
        self.claim["baseline"]["dependency_state_sha256"] = validator.digest(
            validator.canonical([
                [dependency, "master_accepted"]
                for dependency in self.item["dependencies"]
            ])
        )
        self.claim["baseline"]["owned_paths_baseline_sha256"] = validator.digest(
            validator.canonical([[path, None] for path in self.item["owned_paths"]])
        )
        bootstrap_sources = {
            "_baseline/Stage5_Conjectures_Blueprint.md": self.work / "_baseline/Stage5_Conjectures_Blueprint.md",
            "_baseline/workset-member.json": self.work / "_baseline/workset-member.json",
            "_baseline/workset-5.6-receipt.json": validator.EVIDENCE / "workset-5.6-receipt.json",
            "_baseline/execution-spec.json": validator.EVIDENCE / "execution-spec.json",
            "_baseline/foundation-profiles.json": validator.EVIDENCE / "foundation-profiles.json",
            "_baseline/provider-registry.json": validator.EVIDENCE / "provider-registry.json",
            "_baseline/claim-card.schema.json": validator.EVIDENCE / "claim-card.schema.json",
            "_baseline/worker-result.schema.json": validator.EVIDENCE / "worker-result.schema.json",
            "_baseline/master-acceptance.schema.json": validator.EVIDENCE / "master-acceptance.schema.json",
            "_baseline/concurrency-prompt.json": validator.EVIDENCE / "execution/concurrency-prompt.json",
            "_baseline/Current_Pool_Release.json": ROOT / "Docs/catalog/v5/pools/Current_Pool_Release.json",
            "_baseline/Pool_Manifest.json": ROOT / "Docs/catalog/v5/pools/conjecturebench-357bcb1a/Pool_Manifest.json",
        }
        self.claim["read_only_bootstrap_files"] = [{
            "path": relative, "sha256": validator.file_digest(source),
            "size_bytes": source.stat().st_size,
        } for relative, source in bootstrap_sources.items()]
        self.claim_path = self.task / "claim.json"
        self.write_json(self.claim_path, self.claim)
        owned = self.claim["writable_paths"]
        artifacts = []
        for relative in owned:
            artifact_path = self.work / relative
            artifact_path.parent.mkdir(parents=True, exist_ok=True)
            artifact_path.write_text(f"archived fixture for {relative}\n")
            artifacts.append({
                "path": str(production_task / "work" / relative),
                "sha256": validator.file_digest(artifact_path),
                "size_bytes": artifact_path.stat().st_size,
                "media_type": "text/plain",
            })
        by_relative = {
            Path(row["path"]).relative_to(production_task / "work").as_posix(): row
            for row in artifacts
        }
        patch = self.task / "changes.patch"
        patch.write_text("".join(
            f"diff --git a/{relative} b/{relative}\n" for relative in owned
        ))
        result_body = {
            "schema_version": "awesome-theorems/stage5-proof-debt-worker-result/1.0",
            "program": self.claim["program"], "claim_id": self.claim_id,
            "run_id": self.run_id, "item_id": self.item["item_id"],
            "mode": self.claim["mode"],
            "claim_card_sha256": validator.file_digest(self.claim_path),
            "baseline_sha256": validator.digest(validator.canonical(self.claim["baseline"])),
            "status": "self_tested", "changed_paths": owned,
            "patch": {
                "path": str(production_task / "changes.patch"),
                "sha256": validator.file_digest(patch),
                "size_bytes": patch.stat().st_size,
            },
            "command_outcomes": [{
                "command_id": "claim-self-check",
                "argv_sha256": validator.digest(validator.canonical(
                    ["/usr/bin/python3", "-I", "-B", "-c", "pass"]
                )),
                "exit_code": 0, "passed": True,
                "stdout_sha256": "4" * 64, "stderr_sha256": "5" * 64,
                "started_at": "2026-08-17T00:00:00Z",
                "finished_at": "2026-08-17T00:00:01Z",
            }],
            "artifacts": artifacts,
            "completed_at": "2026-08-17T00:00:01Z",
            "typed_outcome": {
                "kind": "strict_resolution", "polarity": "Claim",
                "human_resolution_sha256": by_relative[next(
                    path for path in owned if path.endswith("/human-resolution.md")
                )]["sha256"],
                "lean_root_sha256": by_relative[next(
                    path for path in owned if path.endswith("/Proof.lean")
                )]["sha256"],
                "machine_cut_set_empty": True,
                "readability_cut_set_empty": True,
            },
        }
        result = dict(result_body)
        result["authority_sha256"] = validator.digest(validator.canonical(result_body))
        result_path = self.task / "result.json"
        self.write_json(result_path, result)
        new_root = Path(self.temporary.name)
        evidence = new_root / "Docs/evidence/stage5_conjectures"
        for filename in (
            "claim-card.schema.json", "worker-result.schema.json",
            "master-acceptance.schema.json", "workset-5.6.json",
            "workset-5.6-receipt.json", "execution-spec.json",
            "foundation-profiles.json", "provider-registry.json",
        ):
            target = evidence / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(validator.EVIDENCE / filename, target)
        prompt_target = evidence / "execution/concurrency-prompt.json"
        prompt_target.parent.mkdir(parents=True, exist_ok=True)
        prompt = json.loads(
            (validator.EVIDENCE / "execution/concurrency-prompt.json").read_text()
        )
        prompt["execution_spec_sha256"] = authority_spec_sha
        prompt_body = dict(prompt); prompt_body.pop("authority_sha256", None)
        prompt["authority_sha256"] = validator.digest(
            validator.canonical(prompt_body)
        )
        self.write_json(prompt_target, prompt)
        prompt_raw = prompt_target.read_bytes()
        self.claim["execution_identity"].update({
            "prompt_epoch": prompt["policy_epoch"],
            "prompt_digest": validator.digest(prompt_raw),
            "requested_concurrency": prompt["concurrency"],
            "resolved_concurrency": prompt["concurrency"],
        })
        next(
            entry for entry in self.claim["read_only_bootstrap_files"]
            if entry["path"] == "_baseline/concurrency-prompt.json"
        ).update({
            "sha256": validator.digest(prompt_raw),
            "size_bytes": len(prompt_raw),
        })
        self.write_json(self.claim_path, self.claim)
        result_body["claim_card_sha256"] = validator.file_digest(self.claim_path)
        result_body["baseline_sha256"] = validator.digest(
            validator.canonical(self.claim["baseline"])
        )
        result = dict(result_body)
        result["authority_sha256"] = validator.digest(
            validator.canonical(result_body)
        )
        self.write_json(result_path, result)
        contract_target = new_root / "scripts/stage5_boot_schema_contract.py"
        contract_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / "scripts/stage5_boot_schema_contract.py", contract_target)
        for relative in (
            "Docs/catalog/v5/pools/Current_Pool_Release.json",
            "Docs/catalog/v5/pools/conjecturebench-357bcb1a/Pool_Manifest.json",
            "Docs/catalog/v5/sources/conjecturebench-357bcb1a-full-source.tar.gz",
        ):
            target = new_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        baseline = result["baseline_sha256"]
        patch_sha = result["patch"]["sha256"]
        archive = (
            evidence / "execution/handoffs" / self.claim_id / baseline / patch_sha
        )
        archive.mkdir(parents=True)
        shutil.copyfile(self.claim_path, archive / "claim.json")
        shutil.copyfile(result_path, archive / "result.json")
        shutil.copyfile(patch, archive / "changes.patch")
        manifest_artifacts = []
        for relative, source in zip(owned, artifacts):
            archive_relative = f"artifacts/{relative}"
            target = archive / archive_relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(self.work / relative, target)
            manifest_artifacts.append({
                "path": relative, "source_path": source["path"],
                "archive_path": archive_relative,
                "sha256": source["sha256"], "size_bytes": source["size_bytes"],
                "media_type": source["media_type"],
            })
        file_set = sorted([
            ["claim.json", validator.file_digest(archive / "claim.json"), (archive / "claim.json").stat().st_size],
            ["result.json", validator.file_digest(archive / "result.json"), (archive / "result.json").stat().st_size],
            ["changes.patch", validator.file_digest(archive / "changes.patch"), (archive / "changes.patch").stat().st_size],
            *[[row["archive_path"], row["sha256"], row["size_bytes"]] for row in manifest_artifacts],
        ])
        manifest_body = {
            "schema_version": "awesome-theorems/stage5-harvest-manifest/1.1",
            "program": validator.PROGRAM, "item_id": self.item["item_id"],
            "claim_id": self.claim_id, "run_id": self.run_id,
            "task_root": str(production_task), "baseline_sha256": baseline,
            "patch_sha256": patch_sha, "changed_paths": owned,
            "artifacts": manifest_artifacts, "file_set": file_set,
            "file_set_sha256": validator.digest(validator.canonical(file_set)),
            "archive": archive.relative_to(new_root).as_posix(),
            "queue": "runtime/handoffs/fixture",
        }
        manifest = dict(manifest_body)
        manifest["authority_sha256"] = validator.digest(validator.canonical(manifest_body))
        self.write_json(archive / "harvest-manifest.json", manifest)
        shutil.rmtree(self.task)
        return archive, self.item["item_id"], result, owned

    def test_archived_handoff_replays_after_task_root_cleanup(self) -> None:
        """Master replay must not depend on a retained worker lifecycle root."""
        archive, item_id, result, owned = self._archived_handoff_fixture()
        new_root = archive.parents[7]
        evidence = new_root / "Docs/evidence/stage5_conjectures"
        authority_manager = validator.load_checker().manager()
        authority_spec = authority_manager.spec_object(authority_manager.CONJECTURE)
        original_root, original_evidence = validator.ROOT, validator.EVIDENCE
        validator.ROOT, validator.EVIDENCE = new_root, evidence
        try:
            original_spec = (evidence / "execution-spec.json").read_bytes()
            (evidence / "execution-spec.json").write_text(
                json.dumps(
                    authority_spec, ensure_ascii=False, sort_keys=True, indent=2
                ) + "\n"
            )
            authority_spec_raw = (evidence / "execution-spec.json").read_bytes()
            execution_entry = next(
                entry for entry in self.claim["read_only_bootstrap_files"]
                if entry["path"] == "_baseline/execution-spec.json"
            )
            execution_entry.update({
                "sha256": validator.digest(authority_spec_raw),
                "size_bytes": len(authority_spec_raw),
            })
            self.write_json(archive / "claim.json", self.claim)
            archived_result = json.loads((archive / "result.json").read_text())
            archived_result["claim_card_sha256"] = validator.file_digest(
                archive / "claim.json"
            )
            result_unsigned = dict(archived_result)
            result_unsigned.pop("authority_sha256", None)
            archived_result["authority_sha256"] = validator.digest(
                validator.canonical(result_unsigned)
            )
            self.write_json(archive / "result.json", archived_result)
            archived_manifest = json.loads(
                (archive / "harvest-manifest.json").read_text()
            )
            file_set = archived_manifest["file_set"]
            for row in file_set:
                if row[0] == "claim.json":
                    row[1:] = [
                        validator.file_digest(archive / "claim.json"),
                        (archive / "claim.json").stat().st_size,
                    ]
                elif row[0] == "result.json":
                    row[1:] = [
                        validator.file_digest(archive / "result.json"),
                        (archive / "result.json").stat().st_size,
                    ]
            archived_manifest["file_set_sha256"] = validator.digest(
                validator.canonical(file_set)
            )
            manifest_unsigned = dict(archived_manifest)
            manifest_unsigned.pop("authority_sha256", None)
            archived_manifest["authority_sha256"] = validator.digest(
                validator.canonical(manifest_unsigned)
            )
            self.write_json(archive / "harvest-manifest.json", archived_manifest)
            try:
                claim, replayed, _, integrated, _ = validator.validate_archived_claim_result(
                    archive, item_id
                )
            finally:
                (evidence / "execution-spec.json").write_bytes(original_spec)
        finally:
            validator.ROOT, validator.EVIDENCE = original_root, original_evidence
        self.assertEqual(claim["claim_id"], self.claim_id)
        self.assertEqual(replayed["typed_outcome"], result["typed_outcome"])
        self.assertEqual([row["path"] for row in integrated], owned)

    def test_archived_handoff_rejects_extra_file_and_symlink(self) -> None:
        archive, item_id, _, _ = self._archived_handoff_fixture()
        new_root = archive.parents[7]
        evidence = new_root / "Docs/evidence/stage5_conjectures"
        authority_manager = validator.load_checker().manager()
        authority_spec = authority_manager.spec_object(authority_manager.CONJECTURE)
        original_root, original_evidence = validator.ROOT, validator.EVIDENCE
        validator.ROOT, validator.EVIDENCE = new_root, evidence
        try:
            for name, create in (
                ("extra.txt", lambda path: path.write_text("not manifested\n")),
                (
                    "linked-dir",
                    lambda path: path.symlink_to(
                        archive / "artifacts", target_is_directory=True
                    ),
                ),
            ):
                with self.subTest(name=name):
                    path = archive / name
                    create(path)
                    try:
                        with self.assertRaisesRegex(
                            validator.ClaimError, "archive"
                        ):
                            validator.validate_archived_claim_result(
                                archive, item_id
                            )
                    finally:
                        path.unlink()
        finally:
            validator.ROOT, validator.EVIDENCE = original_root, original_evidence



if __name__ == "__main__":
    unittest.main()
