#!/usr/bin/env python3
"""Focused conformance tests for the conjecture v2 tmux-only controller."""
from __future__ import annotations
import ast
import json
from pathlib import Path
import importlib.util
from unittest import mock
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "scripts/stage5_conjectures_execution_cron_v2.py"
_spec = importlib.util.spec_from_file_location("stage5_conjecture_v2_test_controller", PATH)
assert _spec is not None and _spec.loader is not None
controller = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = controller
_spec.loader.exec_module(controller)


class ConjectureV2Tests(unittest.TestCase):
    def _harvest_fixture(self, temporary: str, *, artifact_rows=None):
        """Build the smallest sealed handoff needed to exercise harvest IO."""
        root = Path(temporary)
        task = root / "tasks/CLAIM/run"
        work = task / "work"
        work.mkdir(parents=True)
        owned = ["owned/proof.md", "owned/data.json"]
        payloads = {owned[0]: b"proof bytes\n", owned[1]: b'{"valid":true}\n'}
        for relative, raw in payloads.items():
            path = work / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        claim = {"writable_paths": owned}
        claim_path = task / "claim.json"
        claim_path.write_text(json.dumps(claim), encoding="utf-8")
        patch_raw = b"".join(
            f"diff --git a/{relative} b/{relative}\n".encode() for relative in owned
        )
        patch_path = task / "changes.patch"
        patch_path.write_bytes(patch_raw)
        result = {
            "program": controller.PROGRAM,
            "item_id": "ITEM", "claim_id": "CLAIM", "run_id": "run",
            "baseline_sha256": "a" * 64,
            "changed_paths": owned,
            "patch": {
                "path": str(patch_path), "sha256": controller.digest(patch_raw),
                "size_bytes": len(patch_raw),
            },
            "artifacts": artifact_rows if artifact_rows is not None else [
                {
                    "path": str(work / relative),
                    "sha256": controller.digest(payloads[relative]),
                    "size_bytes": len(payloads[relative]),
                    "media_type": "application/json" if relative.endswith(".json") else "text/markdown",
                }
                for relative in owned
            ],
        }
        result_path = task / "result.json"
        result_path.write_text(json.dumps(result), encoding="utf-8")
        record = {
            "status": "live", "item_id": "ITEM", "claim_id": "CLAIM",
            "run_id": "run", "task_root": str(task), "work_root": str(work),
            "codex_home": str(task / "codex-home"),
        }

        class Validator:
            @staticmethod
            def validate_result(*_): return result

        patches = (
            mock.patch.object(controller, "ROOT", root),
            mock.patch.object(controller, "HANDOFF_ARCHIVE", root / "archive"),
            mock.patch.object(controller, "HANDOFF_QUEUE", root / "queue"),
            mock.patch.object(controller, "INTEGRATION_QUEUE", root / "integration"),
            mock.patch.object(controller, "HARVEST_LEDGER", root / "harvest.jsonl"),
            mock.patch.object(controller, "claim_checker_module", return_value=Validator),
            mock.patch.object(controller, "stop_record"),
            mock.patch.object(controller, "append_event"),
        )
        return record, claim, result, payloads, patches

    def test_harvest_archives_each_result_artifact_and_closes_manifest(self):
        with tempfile.TemporaryDirectory(prefix="stage5-con-harvest-") as temporary:
            record, claim, result, payloads, patches = self._harvest_fixture(temporary)
            result["artifacts"].reverse()
            (Path(record["task_root"]) / "result.json").write_text(
                json.dumps(result), encoding="utf-8"
            )
            with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7]:
                self.assertTrue(controller.harvest_record(record, {}), record.get("harvest_error"))
            archive = Path(record["handoff"]["archive"])
            queue = Path(record["handoff"]["queue"])
            manifest_raw = (archive / "harvest-manifest.json").read_bytes()
            manifest = controller.verify(json.loads(manifest_raw), "fixture manifest")
            self.assertEqual(set(manifest), {
                "schema_version", "program", "item_id", "claim_id", "run_id",
                "task_root", "baseline_sha256", "patch_sha256", "changed_paths",
                "artifacts", "file_set", "file_set_sha256", "archive", "queue",
                "authority_sha256",
            })
            self.assertEqual(manifest["schema_version"], "awesome-theorems/stage5-harvest-manifest/1.1")
            self.assertEqual(manifest["changed_paths"], claim["writable_paths"])
            self.assertEqual([row["path"] for row in manifest["artifacts"]], claim["writable_paths"])
            source_by_relative = {
                Path(source_row["path"]).relative_to(record["work_root"]).as_posix(): source_row
                for source_row in result["artifacts"]
            }
            for row in manifest["artifacts"]:
                source_row = source_by_relative[row["path"]]
                self.assertEqual(set(row), {"path", "source_path", "archive_path", "sha256", "size_bytes", "media_type"})
                self.assertEqual(row["source_path"], source_row["path"])
                self.assertEqual(row["archive_path"], f"artifacts/{row['path']}")
                self.assertEqual(row["sha256"], source_row["sha256"])
                self.assertEqual(row["size_bytes"], source_row["size_bytes"])
                for root in (archive, queue):
                    raw = (root / row["archive_path"]).read_bytes()
                    self.assertEqual(raw, payloads[row["path"]])
                    self.assertEqual(controller.digest(raw), row["sha256"])
                    self.assertEqual(len(raw), row["size_bytes"])
            expected_file_set = sorted([
                ["claim.json", controller.file_digest(archive / "claim.json"), (archive / "claim.json").stat().st_size],
                ["result.json", controller.file_digest(archive / "result.json"), (archive / "result.json").stat().st_size],
                ["changes.patch", controller.file_digest(archive / "changes.patch"), (archive / "changes.patch").stat().st_size],
                *[[row["archive_path"], row["sha256"], row["size_bytes"]] for row in manifest["artifacts"]],
            ])
            self.assertEqual(manifest["file_set"], expected_file_set)
            self.assertEqual(manifest["file_set_sha256"], controller.digest(controller.canonical(expected_file_set)))
            self.assertEqual(record["handoff"]["manifest_sha256"], controller.digest(manifest_raw))

    def test_harvest_rejects_duplicate_missing_extra_escape_and_byte_drift(self):
        mutations = {
            "duplicate": lambda rows, work: [rows[0], dict(rows[0])],
            "missing": lambda rows, work: rows[:-1],
            "extra": lambda rows, work: rows + [{
                "path": str(work / "extra.txt"), "sha256": "0" * 64,
                "size_bytes": 1, "media_type": "text/plain",
            }],
            "escape": lambda rows, work: [{**rows[0], "path": str(work.parent / "escape.txt")}, rows[1]],
            "path_escape": lambda rows, work: [{**rows[0], "path": str(work / "owned/../proof.md")}, rows[1]],
            "byte_drift": lambda rows, work: [{**rows[0], "sha256": "f" * 64}, rows[1]],
            "size_drift": lambda rows, work: [{**rows[0], "size_bytes": rows[0]["size_bytes"] + 1}, rows[1]],
        }
        for label, mutation in mutations.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory(prefix=f"stage5-con-{label}-") as temporary:
                record, _, result, _, patches = self._harvest_fixture(temporary)
                result["artifacts"] = mutation(result["artifacts"], Path(record["work_root"]))
                with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7]:
                    self.assertFalse(controller.harvest_record(record, {}))
                self.assertIn("artifact", record.get("harvest_error", ""))
                self.assertFalse((Path(temporary) / "integration").exists())

    def test_harvest_rejects_tampered_or_missing_immutable_archive_artifact(self):
        for destination_name, label in (
            ("archive", "tampered"), ("archive", "missing"),
            ("queue", "tampered"), ("queue", "missing"),
        ):
            with self.subTest(label=label), tempfile.TemporaryDirectory(prefix=f"stage5-con-{label}-") as temporary:
                record, _, _, _, patches = self._harvest_fixture(temporary)
                with patches[0], patches[1], patches[2], patches[3], patches[4], patches[5], patches[6], patches[7]:
                    self.assertTrue(controller.harvest_record(record, {}), record.get("harvest_error"))
                    archive_artifact = Path(record["handoff"][destination_name]) / "artifacts/owned/proof.md"
                    if label == "tampered":
                        archive_artifact.chmod(0o644)
                        archive_artifact.write_bytes(b"tampered\n")
                    else:
                        archive_artifact.unlink()
                    record["status"] = "handoff_ready"
                    self.assertFalse(controller.harvest_record(record, {}))
                self.assertRegex(record.get("harvest_error", ""), "conflict|missing")

    def test_handoff_tree_publish_recovers_from_stale_staging_directory(self):
        with tempfile.TemporaryDirectory(prefix="stage5-con-staging-") as temporary:
            root = Path(temporary)
            source = root / "source.txt"
            source.write_bytes(b"complete bytes\n")
            destination = root / "archive" / "claim" / "baseline" / "patch"
            staging = destination.parent / f".{destination.name}.staging"
            staging.mkdir(parents=True)
            (staging / "partial.txt").write_bytes(b"crash residue")
            manifest = b'{"complete":true}\n'
            controller._publish_handoff_tree(
                destination,
                [(source, Path("artifact.txt"), "fixture artifact")],
                manifest,
            )
            self.assertFalse(staging.exists())
            self.assertEqual((destination / "artifact.txt").read_bytes(), source.read_bytes())
            self.assertEqual((destination / "harvest-manifest.json").read_bytes(), manifest)

    def test_current_session_rejects_theorem_or_conjecture_sibling_task_roots(self):
        with tempfile.TemporaryDirectory(prefix="stage5-con-session-boundary-") as temporary:
            task = Path(temporary) / "runtime/tasks/S5CON-00000001-TARGET--worker/r-1-aaaa"
            work = task / "work"; home = task / "codex-home"; sessions = home / "sessions"
            work.mkdir(parents=True); sessions.mkdir(parents=True)
            foreign = controller.ROOT / ".ops/stage5-theorems-execution-v2/tasks/S5THM-00000002-TARGET--worker/r-2-bbbb/work"
            event = {"payload": {"type": "custom_tool_call", "input": f'const r = await tools.exec_command({{"cmd":"sha256sum {foreign}/Proof.lean"}});'}}
            (sessions / "rollout.jsonl").write_text(json.dumps(event) + "\n")
            record = {"task_root":str(task), "work_root":str(work), "codex_home":str(home)}
            self.assertIn("foreign_task_root_reference", controller.session_access_violation(record) or "")

    def test_current_session_allows_only_own_task_subpaths(self):
        with tempfile.TemporaryDirectory(prefix="stage5-con-session-own-") as temporary:
            task = Path(temporary) / "runtime/tasks/S5CON-00000001-TARGET--worker/r-1-aaaa"
            work = task / "work"; home = task / "codex-home"; sessions = home / "sessions"
            work.mkdir(parents=True); sessions.mkdir(parents=True)
            event = {"payload": {"type": "CommandExecution", "command": ["/bin/bash", "-lc", f"find {work} -type f"]}}
            (sessions / "rollout.jsonl").write_text(json.dumps(event) + "\n")
            record = {"task_root":str(task), "work_root":str(work), "codex_home":str(home)}
            self.assertIsNone(controller.session_access_violation(record))

    def test_validate_only_is_read_only_and_route_is_frozen(self):
        before = controller.RUNTIME.exists(); result = controller.validate_only(controller.CONCURRENCY_PROMPT)
        self.assertTrue(result["valid"], result)
        self.assertEqual(result["transport"], "tmux_codex_tui")
        self.assertEqual(result["goal_command"], "/goal")
        self.assertEqual(result["route"], {"provider": "sub2api", "model": "gpt-5.6-sol", "reasoning_effort": "ultra", "service_tier": "default"})
        self.assertEqual(controller.RUNTIME.exists(), before)

    def test_no_container_or_shared_transport(self):
        source = PATH.read_text(encoding="utf-8").lower(); ast.parse(source)
        self.assertNotIn("docker run", source); self.assertNotIn("codex exec", source); self.assertNotIn("app-server", source)
        self.assertIn("tmux", source); self.assertIn("/goal", source)
        self.assertEqual(controller.PROGRAM, "stage5-conjecture-proof-debt/2.0")
        self.assertEqual(controller.RUNTIME.name, controller.RUNTIME_AUTHORITY_EPOCH)
        self.assertEqual(controller.RUNTIME.parent.name, "epochs")
        self.assertTrue(controller.validate_only(controller.CONCURRENCY_PROMPT)["valid"])

    def test_status_and_stop_do_not_create_absent_runtime(self):
        with tempfile.TemporaryDirectory(prefix="stage5-con-observe-") as temporary:
            original_runtime, original_state = controller.RUNTIME, controller.STATE
            controller.RUNTIME = Path(temporary) / "absent-runtime"
            controller.STATE = controller.RUNTIME / "state/controller-state.json"
            try:
                self.assertEqual(controller.status()["claims"], [])
                self.assertEqual(controller.stop()["stopped"], 0)
                self.assertFalse(controller.RUNTIME.exists())
            finally:
                controller.RUNTIME, controller.STATE = original_runtime, original_state

    def test_scheduler_guard_is_shared_and_non_reentrant(self):
        self.assertEqual(
            controller.SCHEDULER_LOCK,
            controller.ROOT / ".ops/stage5-conjectures-execution-v2.scheduler.lock",
        )
        with controller.scheduler_guard():
            with self.assertRaises(controller.ControllerError):
                with controller.scheduler_guard():
                    self.fail("nested scheduler transition should not enter")

    def test_stop_record_only_removes_its_task_local_socket(self):
        with tempfile.TemporaryDirectory(prefix="stage5-con-socket-") as temporary:
            task = Path(temporary)
            socket_path = task / "tmux.sock"
            socket_path.write_text("sentinel")
            controller.stop_record({"task_root": str(task), "socket_argument": "tmux.sock"})
            self.assertTrue(socket_path.exists())

    def test_orphan_fencing_is_registry_and_socket_local(self):
        with tempfile.TemporaryDirectory(prefix="stage5-con-fence-") as temporary:
            original_runtime = controller.RUNTIME
            controller.RUNTIME = Path(temporary) / "runtime"
            orphan = controller.RUNTIME / "tasks" / "S5CON-99999999-TARGET--worker" / "r-old"
            orphan.mkdir(parents=True)
            (orphan / "claim.json").write_text('{"claim_id":"S5CON-99999999-TARGET--worker","item_id":"S5CON-99999999-TARGET","run_id":"r-old"}')
            (orphan / "tmux.sock").write_text("sentinel")
            try:
                self.assertEqual(controller.fence_orphaned_generations({"claims": {}}), 0)
                self.assertTrue((orphan / "tmux.sock").exists())
            finally:
                controller.RUNTIME = original_runtime

    def test_materialized_target_claim_is_schema_complete_and_isolated(self):
        """A future BOOT release must not admit the old minimal claim card."""
        specification, rows, raw = controller.load_program()
        target = next(row for row in rows if row["item_id"].endswith("-TARGET"))
        with tempfile.TemporaryDirectory(prefix="stage5-con-materialize-") as temporary:
            original_runtime = controller.RUNTIME
            controller.RUNTIME = Path(temporary) / "runtime"
            try:
                record = controller.materialize(target, specification, raw)
                claim_path = Path(record["task_root"]) / "claim.json"
                self.assertGreaterEqual(len(json.loads(claim_path.read_text())["read_only_bootstrap_files"]), 1)
                checker_path = ROOT / "scripts/check_stage5_conjecture_claim.py"
                spec = importlib.util.spec_from_file_location("stage5_conjecture_claim_materialize_test", checker_path)
                assert spec is not None and spec.loader is not None
                module = importlib.util.module_from_spec(spec)
                sys.modules[spec.name] = module
                spec.loader.exec_module(module)
                original_checker_runtime = module.RUNTIME
                module.RUNTIME = controller.RUNTIME
                try:
                    value = module.validate_claim(claim_path)
                    self.assertEqual(value["item_id"], target["item_id"])
                    self.assertEqual(value["writable_paths"], target["owned_paths"])
                    prompt_raw = controller.CONCURRENCY_PROMPT.read_bytes()
                    prompt = json.loads(prompt_raw)
                    self.assertEqual(value["execution_identity"]["prompt_digest"], controller.digest(prompt_raw))
                    self.assertEqual(value["execution_identity"]["requested_concurrency"], prompt["concurrency"])
                    self.assertEqual(
                        value["work_contract"]["strict_resolution_proof_search"],
                        specification["conjecture_proof_search_prompt"],
                    )
                    token = "GOAL_READY_" + "A" * 24
                    objective = controller.build_goal_objective(record, token)
                    self.assertTrue(objective.startswith("/goal "))
                    self.assertLessEqual(len(objective.encode("utf-8")), 768)
                    self.assertIn(target["item_id"], objective)
                    self.assertIn("approach-family registry", objective)
                    self.assertIn("theorem-equivalent gaps", objective)
                    self.assertIn("adversarially audit", objective)
                    self.assertIn("child agents", objective)
                    self.assertTrue(objective.endswith(token))
                finally:
                    module.RUNTIME = original_checker_runtime
            finally:
                controller.RUNTIME = original_runtime

    def test_occurrence_intake_goal_uses_intake_not_proof_protocol(self):
        specification, rows, raw = controller.load_program()
        target = next(row for row in rows if row["item_id"].startswith("S5CON-POOL-"))
        with tempfile.TemporaryDirectory(prefix="stage5-con-intake-") as temporary:
            original_runtime = controller.RUNTIME
            controller.RUNTIME = Path(temporary) / "runtime"
            try:
                record = controller.materialize(target, specification, raw)
                objective = controller.build_goal_objective(
                    record, "GOAL_READY_" + "B" * 24,
                )
                claim = json.loads((Path(record["task_root"]) / "claim.json").read_text())
                self.assertEqual(claim["work_contract"]["kind"], "source_occurrence_intake")
                source_record = Path(record["task_root"]) / "work/_baseline/source-record.json"
                self.assertTrue(source_record.is_file())
                self.assertIn(
                    "_baseline/source-record.json",
                    {entry["path"] for entry in claim["read_only_bootstrap_files"]},
                )
                self.assertNotIn("strict_resolution_proof_search", claim["work_contract"])
                self.assertNotIn("CrouzeixConjecture", json.dumps(claim["work_contract"]))
                self.assertIn("do not attempt a proof", objective)
                self.assertIn("source-occurrence intake adjudication", objective)
                self.assertNotIn("approach-family registry", objective)
                self.assertLessEqual(len(objective.encode("utf-8")), 768)
            finally:
                controller.RUNTIME = original_runtime

    def test_concurrency_prompt_must_bind_current_specification(self):
        specification, _, _ = controller.load_program()
        with tempfile.TemporaryDirectory(prefix="stage5-con-prompt-") as temporary:
            path = Path(temporary) / "prompt.json"
            value = json.loads(controller.CONCURRENCY_PROMPT.read_text())
            body = dict(value)
            body.pop("authority_sha256")
            body["execution_spec_sha256"] = "0" * 64
            value = {**body, "authority_sha256": controller.digest(controller.canonical(body))}
            path.write_text(json.dumps(value))
            with self.assertRaises(controller.ControllerError):
                controller.load_concurrency_prompt(path, specification)

    @staticmethod
    def _master_prompt(cap: int) -> dict:
        return {"concurrency": {"integration": cap}}

    @staticmethod
    def _master_rows(item_state: str = " ") -> list[dict]:
        return [
            {"item_id": "S5CON-BOOT-001", "state": "x"},
            {"item_id": "ITEM", "state": item_state},
        ]

    def test_master_pipeline_requires_boot_before_loading_transitioner(self):
        rows = [
            {"item_id": "S5CON-BOOT-001", "state": " "},
            {"item_id": "ITEM", "state": " "},
        ]
        with (
            mock.patch.object(controller, "load_program", return_value=({}, rows, b"")),
            mock.patch.object(
                controller, "load_concurrency_prompt",
                return_value=(self._master_prompt(1), "d" * 64),
            ),
            mock.patch.object(controller, "handoff_transition_module") as transitioner,
            mock.patch.object(controller, "load_state") as state,
        ):
            with self.assertRaisesRegex(controller.ControllerError, "BOOT"):
                controller.run_master_pipeline(Path("prompt.json"))
        transitioner.assert_not_called()
        state.assert_not_called()

    def test_master_pipeline_zero_cap_has_no_transition_side_effect(self):
        with (
            mock.patch.object(
                controller, "load_program",
                return_value=({}, self._master_rows(), b""),
            ),
            mock.patch.object(
                controller, "load_concurrency_prompt",
                return_value=(self._master_prompt(0), "d" * 64),
            ),
            mock.patch.object(controller, "load_state", return_value={
                "runtime_authority_epoch": controller.RUNTIME_AUTHORITY_EPOCH,
                "claims": {"ITEM": {
                    "item_id": "ITEM", "claim_id": "CLAIM", "run_id": "RUN",
                    "runtime_authority_epoch": controller.RUNTIME_AUTHORITY_EPOCH,
                    "status": "handoff_ready",
                }},
            }),
            mock.patch.object(controller, "handoff_transition_module") as transitioner,
        ):
            result = controller.run_master_pipeline(Path("prompt.json"))
        self.assertEqual(result["cap"], 0)
        self.assertEqual(result["eligible"], 1)
        self.assertEqual(result["integrated"], [])
        transitioner.assert_not_called()

    def test_master_pipeline_performs_blank_underscore_x_and_is_idempotent(self):
        class Transitioner:
            def __init__(self):
                self.calls: list[tuple[str, str]] = []

            def transition(self, item_id: str):
                self.calls.append(("transition", item_id))

            def master_accept(self, item_id: str):
                self.calls.append(("accept", item_id))
                return {"item_id": item_id, "state": "master_accepted"}

            def reconcile_acceptance(self, item_id: str):
                self.calls.append(("reconcile", item_id))
                return {"item_id": item_id, "state": "master_accepted"}

        transitioner = Transitioner()
        state = {
            "runtime_authority_epoch": controller.RUNTIME_AUTHORITY_EPOCH,
            "claims": {"ITEM": {
                "item_id": "ITEM", "claim_id": "CLAIM", "run_id": "RUN",
                "runtime_authority_epoch": controller.RUNTIME_AUTHORITY_EPOCH,
                "status": "handoff_ready",
            }},
        }
        with (
            mock.patch.object(
                controller, "load_program",
                return_value=({}, self._master_rows(" "), b""),
            ),
            mock.patch.object(
                controller, "load_concurrency_prompt",
                return_value=(self._master_prompt(1), "d" * 64),
            ),
            mock.patch.object(controller, "load_state", return_value=state),
            mock.patch.object(
                controller, "handoff_transition_module", return_value=transitioner,
            ),
        ):
            result = controller.run_master_pipeline(Path("prompt.json"))
        self.assertEqual(
            transitioner.calls, [("transition", "ITEM"), ("accept", "ITEM")]
        )
        self.assertEqual(len(result["integrated"]), 1)

        state["claims"]["ITEM"].update({
            "status": "master_accepted",
            "integration": {
                "acceptance_path": "placeholder",
                "acceptance_sha256": "a" * 64,
                "accepted_at": "2026-08-17T00:00:00Z",
            },
        })
        transitioner.calls.clear()
        with tempfile.TemporaryDirectory(prefix="stage5-master-acceptance-") as temporary:
            acceptance_body = {
                "program": controller.PROGRAM,
                "item_id": "ITEM",
                "handoff": {
                    "claim_id": "CLAIM", "run_id": "RUN",
                    "baseline_sha256": "a" * 64,
                },
                "integration": {"post_tree_sha256": "b" * 64},
                "accepted_at": "2026-08-17T00:00:00Z",
            }
            acceptance_value = controller.seal(acceptance_body)
            acceptance = (
                Path(temporary) / "ITEM" / ("a" * 64) / ("b" * 64)
                / f"{acceptance_value['authority_sha256']}.json"
            )
            acceptance.parent.mkdir(parents=True)
            acceptance.write_text(json.dumps(acceptance_value))
            state["claims"]["ITEM"]["integration"].update({
                "acceptance_path": str(acceptance),
                "acceptance_sha256": controller.file_digest(acceptance),
            })
            with (
                mock.patch.object(
                    controller, "MASTER_ACCEPTANCES", Path(temporary),
                ),
                mock.patch.object(
                    controller, "load_program",
                    return_value=({}, self._master_rows("x"), b""),
                ),
                mock.patch.object(
                    controller, "load_concurrency_prompt",
                    return_value=(self._master_prompt(1), "d" * 64),
                ),
                mock.patch.object(controller, "load_state", return_value=state),
                mock.patch.object(
                    controller, "handoff_transition_module", return_value=transitioner,
                ) as loader,
            ):
                result = controller.run_master_pipeline(Path("prompt.json"))
        self.assertEqual(result["eligible"], 0)
        self.assertEqual(transitioner.calls, [])
        loader.assert_not_called()

    def test_master_pipeline_reconciles_x_cursor_crash_state(self):
        transitioner = mock.Mock()
        transitioner.reconcile_acceptance.return_value = {
            "item_id": "ITEM", "state": "master_accepted",
        }
        state = {
            "runtime_authority_epoch": controller.RUNTIME_AUTHORITY_EPOCH,
            "claims": {"ITEM": {
                "item_id": "ITEM", "claim_id": "CLAIM", "run_id": "RUN",
                "runtime_authority_epoch": controller.RUNTIME_AUTHORITY_EPOCH,
                "status": "handoff_ready",
            }},
        }
        with (
            mock.patch.object(
                controller, "load_program",
                return_value=({}, self._master_rows("x"), b""),
            ),
            mock.patch.object(
                controller, "load_concurrency_prompt",
                return_value=(self._master_prompt(1), "d" * 64),
            ),
            mock.patch.object(controller, "load_state", return_value=state),
            mock.patch.object(
                controller, "handoff_transition_module", return_value=transitioner,
            ),
        ):
            result = controller.run_master_pipeline(Path("prompt.json"))
        transitioner.reconcile_acceptance.assert_called_once_with("ITEM")
        transitioner.transition.assert_not_called()
        transitioner.master_accept.assert_not_called()
        self.assertEqual(len(result["integrated"]), 1)

    def test_master_pipeline_cap_bounds_attempts_and_keeps_later_work(self):
        transitioner = mock.Mock()
        transitioner.master_accept.side_effect = [
            RuntimeError("first fails"),
            {"item_id": "B", "state": "master_accepted"},
        ]
        rows = [
            {"item_id": "S5CON-BOOT-001", "state": "x"},
            {"item_id": "A", "state": "_"},
            {"item_id": "B", "state": "_"},
            {"item_id": "C", "state": "_"},
        ]
        claims = {
            item_id: {
                "item_id": item_id, "claim_id": f"CLAIM-{item_id}",
                "run_id": f"RUN-{item_id}",
                "runtime_authority_epoch": controller.RUNTIME_AUTHORITY_EPOCH,
                "status": "handoff_ready",
            }
            for item_id in ("A", "B", "C")
        }
        with (
            mock.patch.object(
                controller, "load_program", return_value=({}, rows, b""),
            ),
            mock.patch.object(
                controller, "load_concurrency_prompt",
                return_value=(self._master_prompt(2), "d" * 64),
            ),
            mock.patch.object(controller, "load_state", return_value={
                "runtime_authority_epoch": controller.RUNTIME_AUTHORITY_EPOCH,
                "claims": claims,
            }),
            mock.patch.object(
                controller, "handoff_transition_module", return_value=transitioner,
            ),
        ):
            result = controller.run_master_pipeline(Path("prompt.json"))
        self.assertEqual(
            [call.args[0] for call in transitioner.master_accept.call_args_list],
            ["A", "B"],
        )
        self.assertEqual([row["item_id"] for row in result["errors"]], ["A"])
        self.assertEqual([row["item_id"] for row in result["integrated"]], ["B"])
        self.assertEqual(result["eligible"], 3)

    def test_master_pipeline_revalidates_boot_before_each_candidate(self):
        initial = [
            {"item_id": "S5CON-BOOT-001", "state": "x"},
            {"item_id": "A", "state": "_"},
        ]
        changed = [
            {"item_id": "S5CON-BOOT-001", "state": " "},
            {"item_id": "A", "state": "_"},
        ]
        transitioner = mock.Mock()
        state = {
            "runtime_authority_epoch": controller.RUNTIME_AUTHORITY_EPOCH,
            "claims": {"A": {
                "item_id": "A", "claim_id": "CLAIM-A", "run_id": "RUN-A",
                "runtime_authority_epoch": controller.RUNTIME_AUTHORITY_EPOCH,
                "status": "handoff_ready",
            }},
        }
        with (
            mock.patch.object(
                controller, "load_program",
                side_effect=[({}, initial, b""), ({}, changed, b"")],
            ),
            mock.patch.object(
                controller, "load_concurrency_prompt",
                return_value=(self._master_prompt(1), "d" * 64),
            ),
            mock.patch.object(controller, "load_state", return_value=state),
            mock.patch.object(
                controller, "handoff_transition_module", return_value=transitioner,
            ),
        ):
            result = controller.run_master_pipeline(Path("prompt.json"))
        self.assertEqual([row["item_id"] for row in result["errors"]], ["A"])
        self.assertIn("BOOT changed", result["errors"][0]["error"])
        transitioner.transition.assert_not_called()
        transitioner.master_accept.assert_not_called()
        transitioner.reconcile_acceptance.assert_not_called()


if __name__ == "__main__": unittest.main()
