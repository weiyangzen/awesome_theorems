#!/usr/bin/env python3
"""Focused precommit mutation tests for Stage5 conjecture Master acceptance."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/stage5_conjecture_handoff_transition.py"


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


handoff = load(SCRIPT, "stage5_conjecture_handoff_precommit_test")


class _Expectation:
    def __init__(self, sha256: str):
        self.sha256 = sha256

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _Expectation) and self.sha256 == other.sha256


class _Manager:
    @staticmethod
    def regular_file_expectation(path: Path):
        if path.is_symlink() or not path.is_file():
            return None
        return _Expectation(handoff.digest(path.read_bytes()))

    @staticmethod
    def validate_file_expectation(path: Path, expected: object) -> None:
        observed = _Manager.regular_file_expectation(path)
        if observed != expected:
            raise RuntimeError(f"guard changed: {path}")

    @staticmethod
    def atomic_batch_write(
        outputs: list[tuple[Path, bytes]],
        *,
        precommit_validator,
        **_kwargs: object,
    ) -> None:
        # Model the manager's relevant ordering: staged bytes exist outside the
        # destinations, candidate boundary runs, then and only then are targets
        # replaced.  Mutation tests assert the final loop is never reached.
        precommit_validator()
        for path, raw in outputs:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)


class _ClaimValidator:
    @staticmethod
    def reviewed_schema(_filename: str) -> dict:
        return {"type": "object"}

    @staticmethod
    def validate_schema(value: object, _schema: dict) -> None:
        if not isinstance(value, dict):
            raise RuntimeError("candidate acceptance is not an object")


class _Controller:
    @staticmethod
    def claim_checker_module():
        return _ClaimValidator


class _Checker:
    @staticmethod
    def strict_json(raw: bytes, _label: str):
        return json.loads(raw)

    @staticmethod
    def parse_blueprint(path: Path):
        raw = path.read_bytes()
        if raw.count(b"<!-- valid-blueprint -->") != 1:
            raise RuntimeError("invalid Blueprint fixture")
        return {}, [], raw


class Stage5ConjectureAcceptancePrecommitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(
            prefix="stage5-conjecture-acceptance-precommit-"
        )
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.blueprint = self.root / "Docs/Stage5_Conjectures_Blueprint.md"
        self.gantt = self.root / "Docs/Stage5_Conjectures_Gantt.md"
        self.evidence = (
            self.root
            / "Docs/evidence/stage5_conjectures/execution/transitions"
        )
        self.acceptances = (
            self.root
            / "Docs/evidence/stage5_conjectures/execution/acceptances"
        )
        for name, value in (
            ("ROOT", self.root),
            ("BLUEPRINT", self.blueprint),
            ("GANTT", self.gantt),
            ("EVIDENCE", self.evidence),
            ("ACCEPTANCES", self.acceptances),
        ):
            original = getattr(handoff, name)
            setattr(handoff, name, value)
            self.addCleanup(setattr, handoff, name, original)

        self.item_id = "S5CON-FIXTURE-TARGET"
        self.pre_blueprint = (
            b"<!-- valid-blueprint -->\n"
            + f"- [_] `{self.item_id}` fixture\n".encode()
        )
        self.post_blueprint = self.pre_blueprint.replace(b"- [_]", b"- [x]", 1)
        self.blueprint.parent.mkdir(parents=True)
        self.blueprint.write_bytes(self.pre_blueprint)
        self.gantt.write_bytes(b"pre-Gantt\n")
        self.post_gantt = self.render_gantt(self.post_blueprint, "2026-08-17T00:00:00Z")

        self.archive = self.root / "archive"
        self.archive.mkdir()
        self.artifact_relative = "Stage5_Conjecture_Instances/FIXTURE/Proof.lean"
        self.artifact_raw = b"theorem fixture : True := by trivial\n"
        archived_artifact = self.archive / "artifacts" / self.artifact_relative
        archived_artifact.parent.mkdir(parents=True)
        archived_artifact.write_bytes(self.artifact_raw)
        self.claim = {
            "program": handoff.PROGRAM,
            "claim_id": "S5CON-FIXTURE-TARGET--producer",
            "run_id": "run-fixture",
            "item_id": self.item_id,
            "mode": "TARGET",
            "writable_paths": [self.artifact_relative],
            "baseline": {
                "owned_paths_baseline_sha256": handoff.digest(
                    handoff.canonical([[self.artifact_relative, None]])
                ),
            },
            "workset_member": {
                "member_id": "fixture-member",
                "member_kind": "strict_resolution",
                "target_item_id": self.item_id,
                "workset_record_sha256": "1" * 64,
                "source_record_sha256": "2" * 64,
            },
        }
        self.typed_outcome = {
            "kind": "strict_resolution",
            "polarity": "Claim",
            "human_resolution_sha256": "3" * 64,
            "lean_root_sha256": handoff.digest(self.artifact_raw),
            "machine_cut_set_empty": True,
            "readability_cut_set_empty": True,
        }
        self.result = {
            "claim_id": self.claim["claim_id"],
            "run_id": self.claim["run_id"],
            "item_id": self.item_id,
            "baseline_sha256": "4" * 64,
            "patch": {"sha256": "5" * 64},
            "typed_outcome": self.typed_outcome,
        }
        self.integrated_files = [{
            "path": self.artifact_relative,
            "sha256": handoff.digest(self.artifact_raw),
            "size_bytes": len(self.artifact_raw),
        }]
        self.manifest_body = {
            "schema_version": "awesome-theorems/stage5-harvest-manifest/1.1",
            "artifacts": [{
                **self.integrated_files[0],
                "source_path": f"/fixture/work/{self.artifact_relative}",
                "archive_path": f"artifacts/{self.artifact_relative}",
                "media_type": "text/plain",
            }],
        }
        self.manifest = handoff.seal(self.manifest_body)
        self.write_json(self.archive / "claim.json", self.claim)
        self.write_json(self.archive / "result.json", self.result)
        (self.archive / "changes.patch").write_bytes(b"fixture patch\n")
        self.write_json(self.archive / "harvest-manifest.json", self.manifest)

        self.record = {
            "claim_id": self.claim["claim_id"],
            "run_id": self.claim["run_id"],
            "runtime_authority_epoch": "fixture-epoch",
            "handoff": {"archive": str(self.archive)},
        }
        receipt_body = {
            "program": handoff.PROGRAM,
            "runtime_authority_epoch": "fixture-epoch",
            "item_id": self.item_id,
            "state_transition": {
                "from": "not_done",
                "to": "handoff_waiting_master",
                "post_blueprint_sha256": handoff.digest(self.pre_blueprint),
            },
            "handoff": {
                "claim_id": self.claim["claim_id"],
                "run_id": self.claim["run_id"],
                "immutable_archive": self.archive.relative_to(self.root).as_posix(),
                "harvest_manifest_sha256": handoff.digest(
                    (self.archive / "harvest-manifest.json").read_bytes()
                ),
            },
            "canonical_integration": {
                "integrated": False,
                "canonical_write": "forbidden_until_master_acceptance",
            },
        }
        self.review_receipt = handoff.seal(receipt_body)
        self.receipt_path = self.evidence / self.item_id / "receipt.json"
        self.write_json(self.receipt_path, self.review_receipt)
        (
            self.acceptance_path,
            self.acceptance,
            self.acceptance_raw,
        ) = handoff.build_acceptance_candidate(
            item_id=self.item_id,
            claim=self.claim,
            result=self.result,
            archive=self.archive,
            record=self.record,
            receipt_path=self.receipt_path,
            workset_member=self.claim["workset_member"],
            integrated_files=self.integrated_files,
            pre_blueprint=self.pre_blueprint,
            post_blueprint=self.post_blueprint,
            post_gantt=self.post_gantt,
            accepted_at="2026-08-17T00:00:00Z",
            master_thread_id="fixture-thread",
            master_objective_sha256="6" * 64,
        )
        self.artifact_destination = self.root / self.artifact_relative
        self.artifact_outputs = [(self.artifact_destination, self.artifact_raw)]
        self.outputs = [
            *self.artifact_outputs,
            (self.blueprint, self.post_blueprint),
            (self.gantt, self.post_gantt),
            (self.acceptance_path, self.acceptance_raw),
        ]
        guard_paths = (
            self.archive / "claim.json",
            self.archive / "result.json",
            self.archive / "changes.patch",
            self.archive / "harvest-manifest.json",
            self.receipt_path,
        )
        self.guards = {
            path: _Manager.regular_file_expectation(path) for path in guard_paths
        }

    @staticmethod
    def write_json(path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        )

    @staticmethod
    def render_gantt(
        blueprint: bytes,
        generated_at: str,
    ) -> bytes:
        return b"Gantt:" + generated_at.encode() + b":" + handoff.digest(blueprint).encode() + b"\n"

    def prepare_gantt_fixture(
        self,
        blueprint: bytes,
        _checker: object,
        generated_at: str,
    ) -> bytes:
        return self.render_gantt(blueprint, generated_at)

    def archived_bundle(self, _controller, _item_id: str):
        return self.claim, self.result, self.manifest, self.archive, self.record

    def archive_replay(self, _archive: Path, _item_id: str):
        return (
            self.claim,
            self.result,
            self.manifest,
            self.integrated_files,
            (self.archive / "harvest-manifest.json").read_bytes(),
        )

    def transition_receipt(self, _item_id: str, _record: dict):
        return self.receipt_path, self.review_receipt

    def arguments(self, outputs: list[tuple[Path, bytes]]) -> dict:
        return {
            "controller": _Controller(),
            "checker": _Checker(),
            "manager": _Manager(),
            "item_id": self.item_id,
            "claim": self.claim,
            "result": self.result,
            "manifest": self.manifest,
            "archive": self.archive,
            "record": self.record,
            "receipt_path": self.receipt_path,
            "review_receipt": self.review_receipt,
            "workset_member": self.claim["workset_member"],
            "integrated_files": self.integrated_files,
            "pre_blueprint": self.pre_blueprint,
            "post_blueprint": self.post_blueprint,
            "post_gantt": self.post_gantt,
            "gantt_generated_at": "2026-08-17T00:00:00Z",
            "acceptance_path": self.acceptance_path,
            "expected_acceptance": self.acceptance,
            "expected_acceptance_raw": self.acceptance_raw,
            "artifact_outputs": self.artifact_outputs,
            "outputs": outputs,
            "guards": self.guards,
            "archive_replay": self.archive_replay,
        }

    def validate(self, outputs: list[tuple[Path, bytes]]) -> None:
        with (
            mock.patch.object(
                handoff, "prepare_gantt", side_effect=self.prepare_gantt_fixture
            ),
            mock.patch.object(handoff, "archived_bundle", side_effect=self.archived_bundle),
            mock.patch.object(
                handoff, "transition_receipt", side_effect=self.transition_receipt
            ),
            mock.patch.object(handoff, "verify_seal", wraps=handoff.verify_seal),
        ):
            handoff.validate_acceptance_candidate(**self.arguments(outputs))

    def transaction_validate(self, outputs: list[tuple[Path, bytes]]) -> None:
        arguments = self.arguments(outputs)
        with (
            mock.patch.object(
                handoff, "prepare_gantt", side_effect=self.prepare_gantt_fixture
            ),
            mock.patch.object(
                handoff, "archived_bundle", side_effect=self.archived_bundle
            ),
            mock.patch.object(
                handoff, "transition_receipt", side_effect=self.transition_receipt
            ),
        ):
            _Manager.atomic_batch_write(
                outputs,
                precommit_validator=lambda: handoff.validate_acceptance_candidate(
                    **arguments
                ),
            )

    def assert_no_target_writes(self) -> None:
        self.assertFalse(self.artifact_destination.exists())
        self.assertFalse(self.acceptance_path.exists())
        self.assertEqual(self.blueprint.read_bytes(), self.pre_blueprint)
        self.assertEqual(self.gantt.read_bytes(), b"pre-Gantt\n")

    def test_exact_candidate_passes_without_writing_targets(self) -> None:
        self.validate(self.outputs)
        self.assert_no_target_writes()

    def test_mutated_acceptance_aborts_with_no_target_writes(self) -> None:
        outputs = list(self.outputs)
        outputs[-1] = (self.acceptance_path, self.acceptance_raw.replace(
            b'"accepted_at": "2026-08-17T00:00:00Z"',
            b'"accepted_at": "2026-08-17T00:00:01Z"',
        ))
        with self.assertRaises(RuntimeError):
            self.transaction_validate(outputs)
        self.assert_no_target_writes()

    def test_mutated_post_blueprint_aborts_with_no_target_writes(self) -> None:
        outputs = list(self.outputs)
        outputs[-3] = (self.blueprint, self.post_blueprint + b"mutation\n")
        with self.assertRaises(RuntimeError):
            self.transaction_validate(outputs)
        self.assert_no_target_writes()

    def test_mutated_post_gantt_aborts_with_no_target_writes(self) -> None:
        outputs = list(self.outputs)
        outputs[-2] = (self.gantt, self.post_gantt + b"mutation\n")
        with self.assertRaises(RuntimeError):
            self.transaction_validate(outputs)
        self.assert_no_target_writes()

    def test_mutated_artifact_aborts_with_no_target_writes(self) -> None:
        outputs = list(self.outputs)
        outputs[0] = (self.artifact_destination, self.artifact_raw + b"mutation\n")
        with self.assertRaises(RuntimeError):
            self.transaction_validate(outputs)
        self.assert_no_target_writes()

    def test_transaction_boundary_mutation_aborts_before_target_writes(self) -> None:
        outputs = list(self.outputs)
        outputs[-2] = (self.gantt, self.post_gantt + b"mutation\n")
        with self.assertRaises(RuntimeError):
            self.transaction_validate(outputs)
        self.assert_no_target_writes()

    def test_archive_artifact_changes_after_preflight_abort_before_writes(self) -> None:
        archived = self.archive / "artifacts" / self.artifact_relative
        archived.write_bytes(self.artifact_raw + b"race mutation\n")
        with self.assertRaises(RuntimeError):
            self.transaction_validate(self.outputs)
        self.assert_no_target_writes()


class Stage5ConjectureRecoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(
            prefix="stage5-conjecture-recovery-"
        )
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.acceptances = self.root / "acceptances"
        self.integration = self.root / "integration"
        for name, value in (("ROOT", self.root), ("ACCEPTANCES", self.acceptances)):
            original = getattr(handoff, name)
            setattr(handoff, name, value)
            self.addCleanup(setattr, handoff, name, original)
        self.item_id = "ITEM"
        self.record = {
            "item_id": self.item_id,
            "claim_id": "CLAIM",
            "run_id": "RUN",
            "runtime_authority_epoch": "epoch",
            "status": "handoff_ready",
            "handoff": {
                "queue": str(self.root / "queue"),
                "archive": str(self.root / "archive"),
            },
        }
        self.state = {
            "runtime_authority_epoch": "epoch",
            "claims": {self.item_id: self.record},
        }
        self.acceptance_path = (
            self.acceptances / self.item_id / ("a" * 64) / ("b" * 64)
            / "acceptance.json"
        )
        self.acceptance_path.parent.mkdir(parents=True)
        self.acceptance_path.write_text("acceptance\n")
        self.acceptance = {
            "handoff": {"claim_id": "CLAIM", "run_id": "RUN"},
            "accepted_at": "2026-08-17T00:00:00Z",
        }

    @staticmethod
    def _guard():
        class Guard:
            def __enter__(self): return self
            def __exit__(self, *_): return False
        return Guard()

    def controller(self):
        validator = mock.Mock()
        validator.validate_acceptance.return_value = self.acceptance
        controller = mock.Mock()
        controller.RUNTIME_AUTHORITY_EPOCH = "epoch"
        controller.INTEGRATION_QUEUE = self.integration
        controller.load_state.return_value = self.state
        controller.claim_checker_module.return_value = validator
        return controller

    def checker(self):
        checker = mock.Mock()
        checker.parse_blueprint.return_value = (
            {},
            [
                {"item_id": "S5CON-BOOT-001", "state": "x"},
                {"item_id": self.item_id, "state": "x"},
            ],
            b"",
        )
        class Manager:
            @staticmethod
            def conjecture_scheduler_transition_guard():
                return Stage5ConjectureRecoveryTests._guard()

            @staticmethod
            def manager_mutation_lock():
                return Stage5ConjectureRecoveryTests._guard()

        manager = Manager()
        checker.manager = lambda: manager
        return checker

    def test_reconcile_repairs_state_then_cleans_queue_idempotently(self) -> None:
        controller = self.controller()
        checker = self.checker()
        entry = self.integration / "ITEM--CLAIM--RUN.json"
        entry.parent.mkdir(parents=True)
        entry.write_text("entry\n")
        with (
            mock.patch.object(handoff, "load_controller", return_value=controller),
            mock.patch.object(controller, "checker_module", return_value=checker),
            mock.patch.object(handoff, "_acceptance_candidates", return_value=[self.acceptance_path]),
            mock.patch.object(handoff, "_validated_integration_entry", return_value=entry),
            mock.patch.object(handoff, "require_boot_authority"),
        ):
            first = handoff.reconcile_acceptance(self.item_id)
            second = handoff.reconcile_acceptance(self.item_id)
        self.assertEqual(self.record["status"], "master_accepted")
        self.assertFalse(entry.exists())
        self.assertTrue(first["reconciled"])
        self.assertTrue(first["queue_removed"])
        self.assertFalse(second["reconciled"])
        self.assertFalse(second["queue_removed"])
        controller.save_state.assert_called_once_with(self.state)

    def test_reconcile_rejects_non_x_cursor_before_state_or_queue_change(self) -> None:
        controller = self.controller()
        checker = self.checker()
        checker.parse_blueprint.return_value[1][1]["state"] = "_"
        entry = self.integration / "ITEM--CLAIM--RUN.json"
        entry.parent.mkdir(parents=True)
        entry.write_text("entry\n")
        with (
            mock.patch.object(handoff, "load_controller", return_value=controller),
            mock.patch.object(controller, "checker_module", return_value=checker),
            mock.patch.object(handoff, "require_boot_authority"),
        ):
            with self.assertRaisesRegex(RuntimeError, "accepted cursor"):
                handoff.reconcile_acceptance(self.item_id)
        self.assertEqual(self.record["status"], "handoff_ready")
        self.assertTrue(entry.exists())
        controller.save_state.assert_not_called()

    def test_reconcile_does_not_delete_unvalidated_queue_entry(self) -> None:
        controller = self.controller()
        checker = self.checker()
        entry = self.integration / "ITEM--CLAIM--RUN.json"
        entry.parent.mkdir(parents=True)
        entry.write_text("tampered\n")
        with (
            mock.patch.object(handoff, "load_controller", return_value=controller),
            mock.patch.object(controller, "checker_module", return_value=checker),
            mock.patch.object(handoff, "_acceptance_candidates", return_value=[self.acceptance_path]),
            mock.patch.object(
                handoff, "_validated_integration_entry",
                side_effect=RuntimeError("integration entry binding differs"),
            ),
            mock.patch.object(handoff, "require_boot_authority"),
        ):
            with self.assertRaisesRegex(RuntimeError, "binding differs"):
                handoff.reconcile_acceptance(self.item_id)
        self.assertEqual(self.record["status"], "handoff_ready")
        self.assertTrue(entry.exists())
        controller.save_state.assert_not_called()

    def test_master_accept_x_cursor_replays_reconciliation_not_candidate(self) -> None:
        controller = self.controller()
        checker = self.checker()
        manager = checker.manager()
        manager.CONJECTURE = object()
        manager.operator_goal_binding = lambda _program: (
            "thread", "a" * 64, None,
        )
        selected = (self.acceptance_path, self.acceptance)
        expected = {
            "valid": True, "item_id": self.item_id,
            "state": "master_accepted",
        }
        with (
            mock.patch.object(handoff, "load_controller", return_value=controller),
            mock.patch.object(controller, "checker_module", return_value=checker),
            mock.patch.object(handoff, "require_boot_authority"),
            mock.patch.object(
                handoff, "_acceptance_candidates", return_value=[self.acceptance_path],
            ),
            mock.patch.object(
                handoff, "_valid_acceptance_candidates", return_value=[selected],
            ),
            mock.patch.object(
                handoff, "_reconcile_acceptance_locked", return_value=expected,
            ) as reconcile,
            mock.patch.object(handoff, "archived_bundle") as archived,
        ):
            observed = handoff.master_accept(self.item_id)
        self.assertEqual(observed, expected)
        reconcile.assert_called_once_with(
            controller, self.item_id, self.record, selected,
        )
        archived.assert_not_called()

    def test_reconcile_rejects_invalid_extra_acceptance_candidate(self) -> None:
        controller = self.controller()
        checker = self.checker()
        invalid = (
            self.acceptances / self.item_id / ("c" * 64) / ("d" * 64)
            / "invalid.json"
        )
        invalid.parent.mkdir(parents=True)
        invalid.write_text("invalid\n")
        validator = controller.claim_checker_module.return_value
        validator.validate_acceptance.side_effect = lambda path: (
            self.acceptance
            if path == self.acceptance_path
            else (_ for _ in ()).throw(RuntimeError("invalid acceptance"))
        )
        with (
            mock.patch.object(handoff, "load_controller", return_value=controller),
            mock.patch.object(controller, "checker_module", return_value=checker),
            mock.patch.object(handoff, "require_boot_authority"),
        ):
            with self.assertRaisesRegex(RuntimeError, "invalid or foreign"):
                handoff.reconcile_acceptance(self.item_id)
        self.assertEqual(self.record["status"], "handoff_ready")
        controller.save_state.assert_not_called()

    def test_transition_underscore_retry_returns_existing_receipt(self) -> None:
        controller = self.controller()
        checker = self.checker()
        checker.parse_blueprint.return_value[1][1]["state"] = "_"
        receipt = self.root / "transition.json"
        receipt.write_text("reviewed\n")
        with (
            mock.patch.object(handoff, "load_controller", return_value=controller),
            mock.patch.object(controller, "checker_module", return_value=checker),
            mock.patch.object(handoff, "require_boot_authority"),
            mock.patch.object(
                handoff, "transition_receipt",
                return_value=(receipt, {"valid": True}),
            ),
            mock.patch.object(handoff, "result_and_claim") as result_and_claim,
        ):
            observed = handoff.transition(self.item_id)
        self.assertEqual(observed["state"], "handoff_waiting_master")
        self.assertTrue(observed["reconciled"])
        result_and_claim.assert_not_called()


if __name__ == "__main__":
    unittest.main()
