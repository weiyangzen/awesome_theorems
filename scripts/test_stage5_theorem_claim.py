#!/usr/bin/env python3
"""Mutation tests for the Stage5 theorem claim validator."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts/check_stage5_theorem_claim.py"
CONTROLLER_PATH = ROOT / "scripts/stage5_theorems_execution_cron_v2.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


validator = load(VALIDATOR_PATH, "stage5_theorem_claim_test_validator")
controller = load(CONTROLLER_PATH, "stage5_theorem_claim_test_controller")


class Stage5TheoremClaimTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.specification, rows, cls.blueprint_raw = validator.blueprint_context()
        # v2 has one TARGET row per mathematical object; legacy phase rows
        # such as -INTAKE are intentionally absent from the authoritative DAG.
        cls.item = next(row for row in rows.values() if row["item_id"].endswith("-TARGET"))

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="stage5-theorem-claim-test-")
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
        item_validator = ROOT / "scripts/check_stage5_theorem_item.py"
        item_validator_target = self.work / "_baseline/check_stage5_theorem_item.py"
        item_validator_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(item_validator, item_validator_target)
        self.read_only.append({
            "path": "_baseline/check_stage5_theorem_item.py",
            "sha256": validator.file_digest(item_validator_target),
            "size_bytes": item_validator_target.stat().st_size,
        })
        provider_source = self.work / "_baseline/provider-sources/fixture/revision/Source.lean"
        provider_source.parent.mkdir(parents=True)
        provider_source.write_text("def fixture : True := True.intro\n")
        self.read_only.append({
            "path": provider_source.relative_to(self.work).as_posix(),
            "sha256": validator.file_digest(provider_source),
            "size_bytes": provider_source.stat().st_size,
        })
        baseline = self.work / "_baseline/Stage5_Theorems_Blueprint.md"
        baseline.parent.mkdir(parents=True, exist_ok=True)
        baseline.write_bytes(cls_blueprint := self.blueprint_raw)
        self.read_only.append({
            "path": "_baseline/Stage5_Theorems_Blueprint.md",
            "sha256": validator.digest(cls_blueprint),
            "size_bytes": len(cls_blueprint),
        })
        self.concurrency = {
            "logical_claims": 120,
            "service_records": "not_applicable",
            "agent_executions": 120,
            "startup_reservations": 120,
            "launch_fanout_per_wave": 4,
            "live_transports": 120,
            "authenticated_goals": 120,
            "running_turns": 120,
            "outbound_request_starts_per_window": 120,
            "in_flight_requests": 120,
            "integration": 1,
            "validators": 4,
            "exact_path_conflicts": 0,
        }
        prompt_body = {
            "schema_version": "awesome-theorems/stage5-concurrency-prompt/2.0",
            "program": validator.PROGRAM,
            "policy_epoch": "stage5-concurrency-prompt-2026-08-14-fixture",
            "execution_spec_sha256": validator.digest(validator.canonical(self.specification)),
            "operator_identity": "codex-user-goal:fixture",
            "operator_goal_thread_id": "fixture",
            "operator_goal_objective_sha256": "f" * 64,
            "request_window_seconds": 120,
            "concurrency": self.concurrency,
            "source": "test fixture",
            "execution_limits": {"generation_lifetime_seconds":1209600,"model_input_tokens":2000000,"model_output_tokens":500000,"model_turns":"unbounded","cpu_seconds":1209600,"external_launches":4},
            "recovery": {"startup_attempts_per_generation":1,"provider_attempts_per_request":60,"repair_attempts_per_failure_identity":3,"generation_replacements_per_work_item":60,"backoff_initial_seconds":60,"backoff_max_seconds":3600,"backoff_multiplier":2,"backoff_jitter_ratio":0.2,"retry_after_precedence":"provider_retry_after_then_exponential","breaker_failure_classes":["http_429","http_503","provider_unavailable"],"breaker_scope":"provider","breaker_failure_threshold":3,"breaker_cooldown_seconds":1800},
        }
        self.prompt = {
            **prompt_body,
            "authority_sha256": validator.digest(validator.canonical(prompt_body)),
        }
        self.prompt_source = root / "concurrency-prompt-source.json"
        self.write_json(self.prompt_source, self.prompt)
        prompt_path = self.work / "_baseline/concurrency-prompt.json"
        shutil.copyfile(self.prompt_source, prompt_path)
        self.prompt_digest = validator.file_digest(prompt_path)
        self.read_only.append({
            "path": "_baseline/concurrency-prompt.json",
            "sha256": self.prompt_digest,
            "size_bytes": prompt_path.stat().st_size,
        })
        maxima = self.specification["operator_budget_policy"]["finite_initial_allowances"]["per_claim_maxima"]
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
            "validation_commands": [{
                "command_id": "complete-target-semantic-proof-debt", "cwd": ".",
                "argv": [],
                "environment": [], "timeout_seconds": 900, "network": "denied",
            }],
            "artifact_policy": {
                "allowed_paths": owned, "required_paths": owned,
                "forbidden_paths": [
                    "Docs/Stage5_Theorems_Blueprint.md", "Docs/Stage5_Theorems_Gantt.md",
                    "Docs/catalog", ".git", ".ops",
                ],
            },
            "result_schema": {
                "path": "Docs/evidence/stage5_theorems/worker-result.schema.json",
                "schema_id": validator.load_schema("worker-result.schema.json")["$id"],
                "sha256": validator.file_digest(validator.EVIDENCE / "worker-result.schema.json"),
            },
            "resource_budget": {key: ("unbounded" if key == "model_turns" else min(value, 10)) for key, value in maxima.items() if key in {"model_input_tokens","model_output_tokens","model_turns","external_launches","wall_seconds","cpu_seconds"}},
            "retry_budget": {"attempt": 1, "max_attempts": 61},
            "execution_identity": {
                "lane_id": self.item["item_id"],
                "generation_id": self.run_id,
                "prompt_epoch": self.prompt["policy_epoch"],
                "prompt_digest": self.prompt_digest,
                "execution_spec_sha256": validator.digest(validator.canonical(self.specification)),
                "requested_concurrency": self.concurrency,
                "resolved_concurrency": self.concurrency,
            },
            "execution_policy": {"execution_limits": {"generation_lifetime_seconds":1209600,"model_input_tokens":2000000,"model_output_tokens":500000,"model_turns":"unbounded","cpu_seconds":1209600,"external_launches":4}, "recovery": {"startup_attempts_per_generation":1,"provider_attempts_per_request":60,"repair_attempts_per_failure_identity":3,"generation_replacements_per_work_item":60,"backoff_initial_seconds":60,"backoff_max_seconds":3600,"backoff_multiplier":2,"backoff_jitter_ratio":0.2,"retry_after_precedence":"provider_retry_after_then_exponential","breaker_failure_classes":["http_429","http_503","provider_unavailable"],"breaker_scope":"provider","breaker_failure_threshold":3,"breaker_cooldown_seconds":1800}},
            "generation_lineage": {"replacement_ordinal":0,"replacement_cap":60,"previous_generation_id":None},
        }
        self.claim["validation_commands"][0]["cwd"] = str(self.work)
        self.claim["validation_commands"][0]["argv"] = [
            "/usr/bin/python3", str(self.work / "_baseline/check_stage5_theorem_item.py"),
            "--claim-card", str(self.task / "claim.json"),
            "--work-root", str(self.work),
            "--no-lean",
        ]
        self.claim_path = self.task / "claim.json"
        self.write_json(self.claim_path, self.claim)

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
        artifact_path = self.work / owned[0]
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        artifact_path.write_text("{}\n")
        patch = self.task / "changes.patch"
        patch.write_text("diff --git a/x b/x\n")
        body = {
            "schema_version": "awesome-theorems/stage5-proof-debt-worker-result/1.0",
            "program": self.claim["program"], "claim_id": self.claim_id,
            "run_id": self.run_id, "item_id": self.item["item_id"], "mode": self.claim["mode"],
            "claim_card_sha256": validator.file_digest(self.claim_path),
            "baseline_sha256": validator.digest(validator.canonical(self.claim["baseline"])),
            "status": "self_tested", "changed_paths": owned,
            "patch": {"path": str(patch), "sha256": validator.file_digest(patch), "size_bytes": patch.stat().st_size},
            "command_outcomes": [{
                "command_id": "complete-target-semantic-proof-debt", "argv_sha256": validator.digest(
                    validator.canonical(self.claim["validation_commands"][0]["argv"])
                ), "exit_code": 0,
                "passed": True, "stdout_sha256": "4" * 64, "stderr_sha256": "5" * 64,
                "started_at": "2026-08-11T00:00:00Z", "finished_at": "2026-08-11T00:00:01Z",
            }],
            "artifacts": [{
                "path": str(artifact_path), "sha256": validator.file_digest(artifact_path),
                "size_bytes": artifact_path.stat().st_size, "media_type": "application/json",
            }],
            "completed_at": "2026-08-11T00:00:01Z",
        }
        result = dict(body)
        result["authority_sha256"] = validator.digest(validator.canonical(body))
        result_path = self.task / "result.json"
        self.write_json(result_path, result)
        self.assertEqual(validator.validate_result(result_path, self.claim_path)["status"], "self_tested")
        result["changed_paths"] = ["outside.json"]
        body = dict(result); body.pop("authority_sha256", None)
        result["authority_sha256"] = validator.digest(validator.canonical(body))
        self.write_json(result_path, result)
        with self.assertRaises(validator.ClaimError):
            validator.validate_result(result_path, self.claim_path)

    def test_controller_materialized_claim_passes_validator(self) -> None:
        original_runtime = controller.RUNTIME
        controller.RUNTIME = validator.RUNTIME
        self.addCleanup(setattr, controller, "RUNTIME", original_runtime)
        original_bootstrap = controller.bootstrap_home
        controller.bootstrap_home = lambda home: home.mkdir(parents=True, exist_ok=True)
        self.addCleanup(setattr, controller, "bootstrap_home", original_bootstrap)
        original_provider_sources = controller.copy_provider_sources
        def fixture_provider_sources(work: Path, item: dict) -> None:
            target = work / "_baseline/provider-sources/fixture/revision/Source.lean"
            target.parent.mkdir(parents=True)
            target.write_text("def fixture : True := True.intro\n")
        controller.copy_provider_sources = fixture_provider_sources
        self.addCleanup(setattr, controller, "copy_provider_sources", original_provider_sources)
        # Existing accepted/bootstrap artifacts occupy the first TARGET's
        # canonical path.  Exercise the real materializer with an untouched
        # TARGET so the ownership-conflict guard is not mistaken for a schema
        # failure.
        item = next(
            candidate for candidate in validator.blueprint_context()[1].values()
            if candidate["item_id"].endswith("-TARGET")
            and all(not (ROOT / path).exists() for path in candidate["owned_paths"])
        )
        # Remove the fixture task root so the real materializer can choose its own run.
        shutil.rmtree(self.task)
        record = controller.materialize_claim(
            item, self.specification, self.blueprint_raw, 1,
            prompt=self.prompt, prompt_digest=self.prompt_digest,
            resolved_concurrency=self.concurrency,
            concurrency_prompt_path=self.prompt_source,
        )
        claim_path = Path(record["task_root"]) / "claim.json"
        self.assertEqual(validator.validate_claim(claim_path)["claim_id"], record["claim_id"])


if __name__ == "__main__":
    unittest.main()
