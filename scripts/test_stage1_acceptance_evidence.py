#!/usr/bin/env python3
"""Real-Git focused tests for Stage1 acceptance evidence and replay."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


MODULE_PATH = Path(__file__).with_name("stage1_acceptance_evidence.py")
SPEC = importlib.util.spec_from_file_location("stage1_acceptance_evidence_under_test", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
evidence = importlib.util.module_from_spec(SPEC)
import sys
sys.modules[SPEC.name] = evidence
SPEC.loader.exec_module(evidence)


def run(repo: Path, *argv: str) -> str:
    result = subprocess.run(argv, cwd=repo, text=True, capture_output=True, check=False)
    if result.returncode:
        raise AssertionError(f"{argv!r} failed:\n{result.stdout}\n{result.stderr}")
    return result.stdout.strip()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contract(*, candidates: int = 1, receipt_bound: bool = False) -> dict[str, object]:
    validator_candidates = [
        {
            "path_pattern": f"Stage1_Instances/{{theorem_id}}/check_{index}.py",
            "language": "python",
            "argv_template": ["/usr/bin/python3", "-I", "-B", "{validator_path}"],
            "candidate_only": True,
        }
        for index in range(candidates)
    ]
    roles: list[dict[str, object]] = [
        {
            "role": "instance_manifest",
            "requirement": "required",
            "cardinality": "exactly_one",
            "resolution": "path_candidates",
            "path_candidates": ["Stage1_Instances/{theorem_id}/instance.json"],
            "binding_pointer": None,
        },
        {
            "role": "phase_receipt",
            "requirement": "required",
            "cardinality": "exactly_one",
            "resolution": "path_candidates",
            "path_candidates": ["Stage1_Instances/{theorem_id}/intake-receipt.json"],
            "binding_pointer": None,
        },
    ]
    if receipt_bound:
        roles.insert(
            1,
            {
                "role": "discovery_evidence",
                "requirement": "required",
                "cardinality": "one_or_more",
                "resolution": "receipt_bound_paths",
                "path_candidates": [],
                "binding_pointer": "/inputs/discovery_evidence",
            },
        )
    return {
        "schema_version": evidence.CONTRACT_SCHEMA,
        "authority_id": "test",
        "phase_order": ["intake"],
        "artifact_resolution": {
            "per_item_role_map_owner": "scheduler_master_lane",
            "selected_files_must_be_head_tracked": True,
            "selected_files_must_not_be_symlinks": True,
        },
        "validator_selection": {
            "owner": "scheduler_master_lane",
            "worker_or_reviewer_may_select_argv": False,
            "require_exactly_one_candidate": True,
            "candidate_must_exist_at_worker_base": True,
            "candidate_head_blob_must_equal_worker_base_blob": True,
            "argv_templates": {
                "python": ["/usr/bin/python3", "-I", "-B", "{validator_path}"],
                "bash": ["/usr/bin/bash", "{validator_path}"],
            },
            "cwd": ".",
            "shell_interpolation": False,
            "repo_write_access": False,
            "isolated_scratch_write_access": True,
            "network_policy": "denied",
            "exit_zero_is_sufficient": False,
            "semantic_result_required": True,
        },
        "verdict_protocol": {
            "no_state_change_policy": {
                "phase_closure_condition": "master_independently_proves_the_phase_completion_predicate"
            }
        },
        "phases": [
            {
                "phase": "intake",
                "item_suffix": "INTAKE",
                "worker_verdicts_eligible_for_review": ["accepted", "no_state_change"],
                "raw_blocked_can_close_phase": False,
                "audit_boundary": {"allowed_audit_complete_values": [False]},
                "theorem_boundary": {"allowed_theorem_complete_values": [False]},
                "required_artifact_roles": roles,
                "validator_candidates": validator_candidates,
            }
        ],
    }


class GitFixture:
    def __init__(
        self,
        *,
        candidates: int = 1,
        receipt_bound: bool = False,
        validator_body: str | None = None,
    ) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        run(self.root, "git", "init", "-b", "main")
        run(self.root, "git", "config", "user.email", "tests@example.invalid")
        run(self.root, "git", "config", "user.name", "Stage1 Tests")
        self.docs = self.root / "Docs"
        self.instance = self.root / "Stage1_Instances" / "THM-M-0001"
        self.docs.mkdir()
        self.instance.mkdir(parents=True)
        self.contract_path = self.docs / "Stage1_Phase_Acceptance_Contracts.json"
        self.contract_path.write_text(json.dumps(contract(candidates=candidates, receipt_bound=receipt_bound)), encoding="utf-8")
        instance_bytes = b'{"theorem_id":"THM-M-0001"}\n'
        (self.instance / "instance.json").write_bytes(instance_bytes)
        inputs: dict[str, object] = {}
        if receipt_bound:
            discovery = self.instance / "query.json"
            discovery.write_text('{"query":"exact"}\n', encoding="utf-8")
            inputs["discovery_evidence"] = [
                {
                    "path": "Stage1_Instances/THM-M-0001/query.json",
                    "sha256": digest(discovery),
                }
            ]
        receipt = {
            "schema_version": "stage1-node-receipt/1.0",
            "item_id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "phase": "intake",
            "inputs": inputs,
            "verdict": "no_state_change",
            "audit_complete": False,
            "theorem_complete": False,
        }
        (self.instance / "intake-receipt.json").write_text(json.dumps(receipt), encoding="utf-8")
        for index in range(candidates):
            (self.instance / f"check_{index}.py").write_text(
                validator_body
                or "import json, pathlib\n"
                "assert not pathlib.Path('forbidden-write').exists()\n"
                "print(json.dumps({"
                "'schema_version':'stage1-validator-semantic-result/1.0',"
                "'item_id':'S56-M-0001-INTAKE','theorem_id':'THM-M-0001',"
                "'phase':'intake','status':'passed','verdict':'phase_accepted',"
                "'phase_accepted':True,'audit_complete':False,"
                "'theorem_complete':False,'phase_predicate_proven':True,"
                "'first_failed_gate':None,'open_obligations':0,"
                "'stale_inputs':[],'blocked':False}, sort_keys=True))\n",
                encoding="utf-8",
            )
        run(self.root, "git", "add", ".")
        run(self.root, "git", "commit", "-m", "fixture")
        self.head = run(self.root, "git", "rev-parse", "HEAD")

    def close(self) -> None:
        self.temp.cleanup()

    def loaded(self) -> dict[str, object]:
        return evidence.load_head_contract(self.root, digest(self.contract_path))

    def role_map(self, loaded: dict[str, object] | None = None) -> dict[str, object]:
        return evidence.resolve_role_map(
            self.root,
            loaded or self.loaded(),
            item_id="S56-M-0001-INTAKE",
            theorem_id="THM-M-0001",
            phase="intake",
            base_revision=self.head,
        )

    def recipe(self, loaded: dict[str, object] | None = None) -> dict[str, object]:
        return evidence.select_validator_recipe(
            self.root,
            loaded or self.loaded(),
            item_id="S56-M-0001-INTAKE",
            theorem_id="THM-M-0001",
            phase="intake",
            base_revision=self.head,
        )

    def review_inputs(self) -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
        loaded = self.loaded()
        role_map = self.role_map(loaded)
        recipe = self.recipe(loaded)
        manifest = evidence.build_review_manifest(
            loaded,
            role_map,
            recipe,
            blueprint_sha256="1" * 64,
            theorem_dag_sha256="2" * 64,
            worker_claim_sha256="3" * 64,
            worker_status_sha256="4" * 64,
            worker_prompt_sha256="5" * 64,
            worker_goal_sha256="6" * 64,
            worker_handoff_sha256="7" * 64,
        )
        return loaded, role_map, recipe | {"_review_manifest": manifest}


class ContractAndBindingTests(unittest.TestCase):
    def test_contract_must_be_head_owned_and_digest_pinned(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        loaded = fixture.loaded()
        self.assertEqual(loaded["revision"], fixture.head)
        with self.assertRaisesRegex(evidence.EvidenceError, "digest mismatch"):
            evidence.load_head_contract(fixture.root, "0" * 64)
        fixture.contract_path.write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(evidence.EvidenceError, "differs from authoritative HEAD"):
            evidence.load_head_contract(fixture.root, loaded["sha256"])

    def test_zero_and_two_validator_candidates_fail_closed(self) -> None:
        for count in (0, 2):
            with self.subTest(count=count):
                fixture = GitFixture(candidates=count)
                try:
                    with self.assertRaisesRegex(evidence.EvidenceError, "exactly one HEAD candidate"):
                        fixture.recipe()
                finally:
                    fixture.close()

    def test_missing_and_ambiguous_artifact_candidates_fail_closed(self) -> None:
        for name, add_alternate in (("missing", False), ("ambiguous", True)):
            with self.subTest(name=name):
                fixture = GitFixture()
                try:
                    value = json.loads(fixture.contract_path.read_text())
                    role = value["phases"][0]["required_artifact_roles"][0]
                    if add_alternate:
                        role["path_candidates"].append(
                            "Stage1_Instances/{theorem_id}/intake.json"
                        )
                        (fixture.instance / "intake.json").write_text("{}\n", encoding="utf-8")
                    else:
                        (fixture.instance / "instance.json").unlink()
                    fixture.contract_path.write_text(json.dumps(value), encoding="utf-8")
                    run(fixture.root, "git", "add", "-A")
                    run(fixture.root, "git", "commit", "-m", name)
                    loaded = evidence.load_head_contract(
                        fixture.root, digest(fixture.contract_path)
                    )
                    with self.assertRaisesRegex(
                        evidence.EvidenceError, "requires exactly one artifact"
                    ):
                        fixture.role_map(loaded)
                finally:
                    fixture.close()

    def test_validator_must_have_the_same_blob_at_worker_base_and_head(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        worker_base = fixture.head
        (fixture.instance / "check_0.py").write_text("print('changed')\n", encoding="utf-8")
        run(fixture.root, "git", "add", ".")
        run(fixture.root, "git", "commit", "-m", "change validator")
        loaded = fixture.loaded()
        with self.assertRaisesRegex(evidence.EvidenceError, "differs from worker-base blob"):
            evidence.select_validator_recipe(
                fixture.root,
                loaded,
                item_id="S56-M-0001-INTAKE",
                theorem_id="THM-M-0001",
                phase="intake",
                base_revision=worker_base,
            )

    def test_role_map_binds_every_selected_head_blob(self) -> None:
        fixture = GitFixture(receipt_bound=True)
        self.addCleanup(fixture.close)
        role_map = fixture.role_map()
        self.assertEqual(
            {row["role"] for row in role_map["artifacts"]},
            {"instance_manifest", "discovery_evidence", "phase_receipt"},
        )
        self.assertTrue(all(len(row["sha256"]) == 64 for row in role_map["artifacts"]))
        self.assertTrue(all(len(row["git_blob"]) == 40 for row in role_map["artifacts"]))

    def test_receipt_pointer_requires_structured_complete_binding(self) -> None:
        fixture = GitFixture(receipt_bound=True)
        self.addCleanup(fixture.close)
        receipt_path = fixture.instance / "intake-receipt.json"
        receipt = json.loads(receipt_path.read_text())
        receipt["inputs"]["discovery_evidence"] = "Stage1_Instances/THM-M-0001/query.json"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        run(fixture.root, "git", "add", ".")
        run(fixture.root, "git", "commit", "-m", "bad pointer")
        loaded = evidence.load_head_contract(fixture.root, digest(fixture.contract_path))
        with self.assertRaisesRegex(evidence.EvidenceError, "must be an object binding"):
            fixture.role_map(loaded)

    def test_symlink_artifact_is_rejected_even_when_git_tracked(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        target = fixture.instance / "instance.json"
        target.unlink()
        target.symlink_to("intake-receipt.json")
        run(fixture.root, "git", "add", ".")
        run(fixture.root, "git", "commit", "-m", "symlink")
        loaded = evidence.load_head_contract(fixture.root, digest(fixture.contract_path))
        with self.assertRaisesRegex(evidence.EvidenceError, "symlink"):
            fixture.role_map(loaded)

    def test_dirty_artifact_and_receipt_hash_mismatch_are_rejected(self) -> None:
        fixture = GitFixture(receipt_bound=True)
        self.addCleanup(fixture.close)
        loaded = fixture.loaded()
        (fixture.instance / "instance.json").write_text("dirty", encoding="utf-8")
        with self.assertRaisesRegex(evidence.EvidenceError, "differs from authoritative HEAD"):
            fixture.role_map(loaded)
        run(fixture.root, "git", "checkout", "--", "Stage1_Instances/THM-M-0001/instance.json")
        receipt_path = fixture.instance / "intake-receipt.json"
        receipt = json.loads(receipt_path.read_text())
        receipt["inputs"]["discovery_evidence"][0]["sha256"] = "0" * 64
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        run(fixture.root, "git", "add", ".")
        run(fixture.root, "git", "commit", "-m", "bad hash")
        loaded = evidence.load_head_contract(fixture.root, digest(fixture.contract_path))
        with self.assertRaisesRegex(evidence.EvidenceError, "sha256 disagrees"):
            fixture.role_map(loaded)

    def test_worker_argv_cannot_bypass_scheduler_recipe(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        recipe = fixture.recipe()
        supplied = dict(recipe)
        supplied["argv"] = ["/bin/sh", "-c", "touch owned"]
        with self.assertRaisesRegex(evidence.EvidenceError, "not scheduler-authorized"):
            evidence.replay_validator(
                fixture.root,
                supplied,
                review_manifest={},
                role_map={},
                timeout_seconds=2,
            )

    def test_review_manifest_binds_all_worker_and_authority_inputs(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        loaded = fixture.loaded()
        role_map = fixture.role_map(loaded)
        recipe = fixture.recipe(loaded)
        manifest = evidence.build_review_manifest(
            loaded,
            role_map,
            recipe,
            blueprint_sha256="1" * 64,
            theorem_dag_sha256="2" * 64,
            worker_claim_sha256="3" * 64,
            worker_status_sha256="4" * 64,
            worker_prompt_sha256="5" * 64,
            worker_goal_sha256="6" * 64,
            worker_handoff_sha256="7" * 64,
        )
        self.assertEqual(manifest["authority_revision"], fixture.head)
        self.assertEqual(manifest["role_map_sha256"], role_map["manifest_sha256"])
        self.assertEqual(manifest["validator_recipe_sha256"], recipe["recipe_sha256"])
        self.assertEqual(len(manifest["manifest_sha256"]), 64)


class ReplayAndSemanticTests(unittest.TestCase):
    def inputs(self, fixture: GitFixture) -> tuple[dict[str, object], dict[str, object], dict[str, object], dict[str, object]]:
        loaded = fixture.loaded()
        role_map = fixture.role_map(loaded)
        recipe = fixture.recipe(loaded)
        manifest = evidence.build_review_manifest(
            loaded, role_map, recipe,
            blueprint_sha256="1" * 64, theorem_dag_sha256="2" * 64,
            worker_claim_sha256="3" * 64, worker_status_sha256="4" * 64,
            worker_prompt_sha256="5" * 64, worker_goal_sha256="6" * 64,
            worker_handoff_sha256="7" * 64,
        )
        return loaded, role_map, recipe, manifest

    def test_real_bwrap_replay_is_detached_readonly_and_captures_output(self) -> None:
        if not Path("/usr/bin/bwrap").is_file():
            self.skipTest("bubblewrap unavailable")
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        _loaded, role_map, recipe, manifest = self.inputs(fixture)
        result = evidence.replay_validator(
            fixture.root,
            recipe,
            review_manifest=manifest,
            role_map=role_map,
            timeout_seconds=10,
        )
        self.assertEqual(result["exit_code"], 0)
        self.assertFalse(result["timed_out"])
        self.assertFalse(result["shell"])
        self.assertEqual(result["repo_access"], "read_only")
        self.assertEqual(result["network_policy"], "denied")
        self.assertTrue(result["semantic_result"]["phase_accepted"])
        self.assertEqual(result["cwd"], "/repo")
        self.assertNotIn("--ro-bind\x00/\x00/", "\x00".join(result["bwrap_argv"]))
        self.assertEqual(run(fixture.root, "git", "worktree", "list", "--porcelain").count("worktree "), 1)

    def test_real_bwrap_cannot_read_host_home_or_secret_and_has_private_tmp(self) -> None:
        if not Path("/usr/bin/bwrap").is_file():
            self.skipTest("bubblewrap unavailable")
        secret = Path.home() / f"stage1-evidence-secret-{os.getpid()}"
        secret.write_text("must-not-be-mounted", encoding="utf-8")
        self.addCleanup(secret.unlink, missing_ok=True)
        probe = (
            "import json, pathlib\n"
            f"assert not pathlib.Path({str(secret)!r}).exists()\n"
            "assert not pathlib.Path('/root').exists()\n"
            "assert not pathlib.Path('/home').exists()\n"
            "pathlib.Path('/scratch/ok').write_text('ok')\n"
            "pathlib.Path('/tmp/ok').write_text('ok')\n"
            "print(json.dumps({"
            "'schema_version':'stage1-validator-semantic-result/1.0',"
            "'item_id':'S56-M-0001-INTAKE','theorem_id':'THM-M-0001',"
            "'phase':'intake','status':'passed','verdict':'phase_accepted',"
            "'phase_accepted':True,'audit_complete':False,"
            "'theorem_complete':False,'phase_predicate_proven':True,"
            "'first_failed_gate':None,'open_obligations':0,"
            "'stale_inputs':[],'blocked':False}))\n"
        )
        fixture = GitFixture(validator_body=probe)
        self.addCleanup(fixture.close)
        _loaded, role_map, recipe, manifest = self.inputs(fixture)
        result = evidence.replay_validator(
            fixture.root, recipe, review_manifest=manifest, role_map=role_map,
            timeout_seconds=10,
        )
        self.assertEqual(result["exit_code"], 0)
        argv = result["bwrap_argv"]
        mounts = list(zip(argv, argv[1:], argv[2:]))
        self.assertNotIn(("--ro-bind", "/", "/"), mounts)
        self.assertIn(("--tmpfs", "/", "--dir"), mounts)
        self.assertIn(("--tmpfs", "/tmp", "--chdir"), mounts)

    def test_stdout_must_be_one_exact_json_object(self) -> None:
        for name, tail in (
            ("trailing", "\\nextra"),
            ("duplicate", ""),
        ):
            with self.subTest(name=name):
                semantic = self.semantic()
                if name == "duplicate":
                    output = '{"schema_version":"stage1-validator-semantic-result/1.0","schema_version":"stage1-validator-semantic-result/1.0"}'
                else:
                    output = evidence.canonical_json(semantic).decode() + tail
                probe = f"print({output!r})\n"
                fixture = GitFixture(validator_body=probe)
                try:
                    _loaded, role_map, recipe, manifest = self.inputs(fixture)
                    with self.assertRaises(evidence.EvidenceError):
                        evidence.replay_validator(
                            fixture.root, recipe, review_manifest=manifest,
                            role_map=role_map, timeout_seconds=10,
                        )
                finally:
                    fixture.close()

    def test_evaluator_rejects_forged_semantics_and_manifest_binding(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        loaded, role_map, recipe, manifest = self.inputs(fixture)
        replay = self.replay_result(fixture, loaded, role_map, recipe, manifest)
        replay["semantic_result"] = self.semantic(blocked=True)
        unhashed = dict(replay)
        unhashed.pop("result_sha256")
        replay["result_sha256"] = evidence.sha256_bytes(evidence.canonical_json(unhashed))
        with self.assertRaisesRegex(evidence.EvidenceError, "semantic digest"):
            evidence.evaluate_replay_semantics(
                replay, contract_record=loaded, review_manifest=manifest,
                role_map=role_map, validator_recipe=recipe,
                worker_verdict="accepted", review_verdict="phase_accepted",
                audit_complete=False, theorem_complete=False,
            )

    def test_no_state_change_requires_independent_phase_predicate(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        loaded, role_map, recipe, manifest = self.inputs(fixture)
        semantic = self.semantic(phase_predicate_proven=False)
        replay = self.replay_result(
            fixture, loaded, role_map, recipe, manifest, semantic
        )
        decision = evidence.evaluate_replay_semantics(
            replay, contract_record=loaded, review_manifest=manifest,
            role_map=role_map, validator_recipe=recipe,
            worker_verdict="no_state_change", review_verdict="phase_accepted",
            audit_complete=False, theorem_complete=False,
        )
        self.assertFalse(decision["phase_evidence_accepted"])
        self.assertIn(
            "no_state_change_predicate_not_independently_proven",
            decision["negative_reasons"],
        )

    def test_terminal_flags_are_checked_against_head_phase_row(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        loaded, role_map, recipe, manifest = self.inputs(fixture)
        semantic = self.semantic(audit_complete=True)
        replay = self.replay_result(
            fixture, loaded, role_map, recipe, manifest, semantic
        )
        decision = evidence.evaluate_replay_semantics(
            replay, contract_record=loaded, review_manifest=manifest,
            role_map=role_map, validator_recipe=recipe,
            worker_verdict="accepted", review_verdict="phase_accepted",
            audit_complete=True, theorem_complete=False,
        )
        self.assertFalse(decision["phase_evidence_accepted"])
        self.assertIn(
            "audit_complete_outside_phase_contract", decision["negative_reasons"]
        )

    def test_evaluator_rejects_digest_bound_extra_semantic_member(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        loaded, role_map, recipe, manifest = self.inputs(fixture)
        semantic = self.semantic()
        semantic["unreviewed_override"] = True
        replay = self.replay_result(
            fixture, loaded, role_map, recipe, manifest, semantic
        )
        with self.assertRaisesRegex(evidence.EvidenceError, "semantic schema is not exact"):
            evidence.evaluate_replay_semantics(
                replay, contract_record=loaded, review_manifest=manifest,
                role_map=role_map, validator_recipe=recipe,
                worker_verdict="accepted", review_verdict="phase_accepted",
                audit_complete=False, theorem_complete=False,
            )

    def replay_result(
        self,
        fixture: GitFixture,
        loaded: dict[str, object],
        role_map: dict[str, object],
        recipe: dict[str, object],
        manifest: dict[str, object],
        semantic: dict[str, object] | None = None,
    ) -> dict[str, object]:
        semantic = semantic or self.semantic()
        stdout_bytes = evidence.canonical_json(semantic)
        result = {
            "schema_version": evidence.REPLAY_RESULT_SCHEMA,
            "item_id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "phase": "intake",
            "authority_revision": fixture.head,
            "authority_tree": loaded["git_tree"],
            "recipe_sha256": recipe["recipe_sha256"],
            "review_manifest_sha256": manifest["manifest_sha256"],
            "role_map_sha256": role_map["manifest_sha256"],
            "artifact_bindings_sha256": evidence.sha256_bytes(evidence.canonical_json(role_map["artifacts"])),
            "timed_out": False,
            "exit_code": 0,
            "shell": False,
            "network_policy": "denied",
            "repo_access": "read_only",
            "scratch_access": "isolated_writable",
            "stdout_complete": True,
            "stderr_complete": True,
            "stdout": stdout_bytes.decode(),
            "stdout_base64": __import__("base64").b64encode(stdout_bytes).decode(),
            "stdout_sha256": evidence.sha256_bytes(stdout_bytes),
            "stderr": "",
            "semantic_result": semantic,
            "semantic_result_sha256": evidence.sha256_bytes(evidence.canonical_json(semantic)),
        }
        result["result_sha256"] = evidence.sha256_bytes(evidence.canonical_json(result))
        return result

    def semantic(self, **updates: object) -> dict[str, object]:
        value: dict[str, object] = {
            "status": "passed",
            "schema_version": evidence.VALIDATOR_SEMANTIC_SCHEMA,
            "item_id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "phase": "intake",
            "verdict": "phase_accepted",
            "phase_accepted": True,
            "audit_complete": False,
            "theorem_complete": False,
            "first_failed_gate": None,
            "open_obligations": 0,
            "stale_inputs": [],
            "blocked": False,
            "phase_predicate_proven": True,
        }
        value.update(updates)
        return value

    def test_exit_zero_plus_blocked_open_or_stale_is_negative(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        loaded, role_map, recipe, manifest = self.inputs(fixture)
        for name, mutation in (
            ("blocked", {"status": "blocked", "blocked": True}),
            ("open", {"open_obligations": 1}),
            ("stale", {"stale_inputs": ["artifact"]}),
        ):
            with self.subTest(name=name):
                decision = evidence.evaluate_replay_semantics(
                    self.replay_result(
                        fixture, loaded, role_map, recipe, manifest,
                        self.semantic(**mutation),
                    ),
                    contract_record=loaded,
                    review_manifest=manifest,
                    role_map=role_map,
                    validator_recipe=recipe,
                    worker_verdict="accepted",
                    review_verdict="phase_accepted",
                    audit_complete=False,
                    theorem_complete=False,
                )
                self.assertFalse(decision["phase_evidence_accepted"])
                self.assertEqual(decision["decision"], "remain_[_]")

    def test_raw_worker_blocked_never_promotes_and_positive_can_pass(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        loaded, role_map, recipe, manifest = self.inputs(fixture)
        replay = self.replay_result(fixture, loaded, role_map, recipe, manifest)
        blocked = evidence.evaluate_replay_semantics(
            replay,
            contract_record=loaded,
            review_manifest=manifest,
            role_map=role_map,
            validator_recipe=recipe,
            worker_verdict="blocked",
            review_verdict="phase_accepted",
            audit_complete=False,
            theorem_complete=False,
        )
        self.assertFalse(blocked["phase_evidence_accepted"])
        positive = evidence.evaluate_replay_semantics(
            replay,
            contract_record=loaded,
            review_manifest=manifest,
            role_map=role_map,
            validator_recipe=recipe,
            worker_verdict="no_state_change",
            review_verdict="phase_accepted",
            audit_complete=False,
            theorem_complete=False,
        )
        self.assertTrue(positive["phase_evidence_accepted"])


if __name__ == "__main__":
    unittest.main()
