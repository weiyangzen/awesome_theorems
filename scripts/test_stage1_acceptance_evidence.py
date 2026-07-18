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
from unittest import mock


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


def contract(*, authorities: int = 1, receipt_bound: bool = False) -> dict[str, object]:
    validator_authorities = [
        {
            "path_pattern": f"scripts/stage1_phase_validators/check_{index}.py",
            "language": "python",
            "argv_template": ["/usr/bin/python3", "-I", "-B", "{validator_path}"],
            "authority_generation": "stage1-v2",
            "requirements_authority": "Docs/Stage1_Blueprint_v2.md",
            "positive_acceptance_capable": True,
        }
        for index in range(authorities)
    ]
    superseded_validator_sources = [{
        "path_pattern": "Stage1_Instances/{theorem_id}/check_intake.py",
        "language": "python",
        "argv_template": ["/usr/bin/python3", "-I", "-B", "{validator_path}"],
        "authority_generation": "pre-v2",
        "status": "superseded",
        "allowed_use": "historical_negative_observation_only",
        "positive_acceptance_capable": False,
        "superseded_by": "Docs/Stage1_Blueprint_v2.md",
    }]
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
        "requirements_authority": "Docs/Stage1_Blueprint_v2.md",
        "task_state_authority": "Docs/Stage1_Blueprint_v2.md",
        "phase_order": ["intake"],
        "artifact_resolution": {
            "owner_root_pattern": "Stage1_Instances/{theorem_id}",
            "per_item_role_map_owner": "scheduler_master_lane",
            "selected_files_must_be_head_tracked": True,
            "selected_files_must_not_be_symlinks": True,
        },
        "validator_selection": {
            "owner": "scheduler_master_lane",
            "selection_source": "validator_authorities_at_authoritative_head",
            "required_authority_generation": "stage1-v2",
            "required_requirements_authority": "Docs/Stage1_Blueprint_v2.md",
            "worker_or_reviewer_may_select_argv": False,
            "require_exactly_one_current_authority": True,
            "current_authority_must_exist_at_worker_base": True,
            "current_authority_head_blob_must_equal_worker_base_blob": True,
            "superseded_sources_are_history_only": True,
            "superseded_sources_can_accept": False,
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
                "validator_authorities": validator_authorities,
                "superseded_validator_sources": superseded_validator_sources,
            }
        ],
    }


class GitFixture:
    def __init__(
        self,
        *,
        authorities: int = 1,
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
        self.validators = self.root / "scripts" / "stage1_phase_validators"
        self.docs.mkdir()
        self.instance.mkdir(parents=True)
        self.validators.mkdir(parents=True)
        self.lean_project = self.root / "Formalizations" / "Lean"
        self.lean_cache = self.lean_project / ".lake"
        self.lean_packages = self.lean_cache / "packages"
        self.lean_packages.mkdir(parents=True)
        (self.lean_cache / "build").mkdir()
        (self.lean_cache / "config").mkdir()
        self.toolchain_root = self.root / "fixture-toolchain"
        (self.toolchain_root / "bin").mkdir(parents=True)
        (self.toolchain_root / "bin" / "lean").write_bytes(b"fixture-lean")
        (self.toolchain_root / "bin" / "lake").write_bytes(b"fixture-lake")
        (self.toolchain_root / "bin" / "lean").chmod(0o700)
        (self.toolchain_root / "bin" / "lake").chmod(0o700)
        (self.lean_project / "lean-toolchain").write_text(
            "leanprover/lean4:v4.29.0\n", encoding="utf-8"
        )
        (self.lean_project / "lake-manifest.json").write_text(
            json.dumps(
                {
                    "version": "1.1.0",
                    "packagesDir": ".lake/packages",
                    "packages": [],
                    "name": "fixture",
                    "lakeDir": ".lake",
                }
            ),
            encoding="utf-8",
        )
        self.contract_path = self.docs / "Stage1_Phase_Acceptance_Contracts.json"
        self.blueprint_path = self.docs / "Stage1_Blueprint_v2.md"
        self.contract_path.write_text(json.dumps(contract(authorities=authorities, receipt_bound=receipt_bound)), encoding="utf-8")
        self.blueprint_path.write_text("# Test Stage1 v2 SSOT\n", encoding="utf-8")
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
        (self.instance / "check_intake.py").write_text(
            "print('historical only')\n", encoding="utf-8"
        )
        for index in range(authorities):
            (self.validators / f"check_{index}.py").write_text(
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

    def lean_authority(self, checkout: Path | None = None) -> tuple[dict[str, object], Path, Path]:
        return evidence.build_lean_authority(
            checkout or self.root,
            toolchain_root=self.toolchain_root,
            lake_cache_root=self.lean_cache,
        )

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
            blueprint_sha256=digest(self.blueprint_path),
            blueprint_git_blob=run(
                self.root, "git", "rev-parse", "HEAD:Docs/Stage1_Blueprint_v2.md"
            ),
            theorem_dag_sha256="2" * 64,
            worker_claim_sha256="3" * 64,
            worker_status_sha256="4" * 64,
            worker_prompt_sha256="5" * 64,
            worker_goal_sha256="6" * 64,
            worker_handoff_sha256="7" * 64,
        )
        return loaded, role_map, recipe | {"_review_manifest": manifest}


class StagedGitFixture:
    """Authority checkout plus a worker clone whose first receipt is unmerged."""

    def __init__(self, *, receipt_bound: bool = False) -> None:
        self.temp = tempfile.TemporaryDirectory()
        parent = Path(self.temp.name)
        self.root = parent / "authority"
        self.worker = parent / "worker"
        self.root.mkdir()
        run(self.root, "git", "init", "-b", "main")
        run(self.root, "git", "config", "user.email", "tests@example.invalid")
        run(self.root, "git", "config", "user.name", "Stage1 Tests")
        docs = self.root / "Docs"
        validators = self.root / "scripts" / "stage1_phase_validators"
        docs.mkdir()
        validators.mkdir(parents=True)
        self.contract_path = docs / "Stage1_Phase_Acceptance_Contracts.json"
        self.contract_path.write_text(
            json.dumps(contract(receipt_bound=receipt_bound)), encoding="utf-8"
        )
        (docs / "Stage1_Blueprint_v2.md").write_text(
            "# Test Stage1 v2 SSOT\n", encoding="utf-8"
        )
        self.validator = validators / "check_0.py"
        self.validator.write_text("print('authority validator')\n", encoding="utf-8")
        run(self.root, "git", "add", ".")
        run(self.root, "git", "commit", "-m", "authority-only base")
        self.base = run(self.root, "git", "rev-parse", "HEAD")
        run(parent, "git", "clone", str(self.root), str(self.worker))
        self.instance = self.worker / "Stage1_Instances" / "THM-M-0001"
        self.instance.mkdir(parents=True)
        self.receipt_bound = receipt_bound

    def close(self) -> None:
        self.temp.cleanup()

    def write_evidence(self, *, binding_role: str | None = None) -> list[str]:
        instance = self.instance / "instance.json"
        instance.write_text('{"theorem_id":"THM-M-0001"}\n', encoding="utf-8")
        inputs: dict[str, object] = {}
        changed = ["Stage1_Instances/THM-M-0001/instance.json"]
        if self.receipt_bound:
            query = self.instance / "query.json"
            query.write_text('{"query":"exact"}\n', encoding="utf-8")
            binding: dict[str, object] = {
                "path": "Stage1_Instances/THM-M-0001/query.json",
                "sha256": digest(query),
            }
            if binding_role is not None:
                binding["role"] = binding_role
            inputs["discovery_evidence"] = [binding]
            changed.append("Stage1_Instances/THM-M-0001/query.json")
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
        (self.instance / "intake-receipt.json").write_text(
            json.dumps(receipt), encoding="utf-8"
        )
        changed.append("Stage1_Instances/THM-M-0001/intake-receipt.json")
        return changed

    def role_map(self, changed: list[str]) -> dict[str, object]:
        loaded = evidence.load_head_contract(self.root, digest(self.contract_path))
        return evidence.resolve_staged_role_map(
            self.root,
            loaded,
            workspace=self.worker,
            declared_delta_paths=changed,
            item_id="S56-M-0001-INTAKE",
            theorem_id="THM-M-0001",
            phase="intake",
            base_revision=self.base,
        )


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

    def test_zero_and_two_current_validator_authorities_fail_closed(self) -> None:
        for count in (0, 2):
            with self.subTest(count=count):
                fixture = GitFixture(authorities=count)
                try:
                    message = (
                        "no current stage1-v2 validator authority"
                        if count == 0
                        else "exactly one current stage1-v2 authority"
                    )
                    with self.assertRaisesRegex(evidence.EvidenceError, message):
                        fixture.recipe()
                finally:
                    fixture.close()

    def test_superseded_legacy_source_is_never_selected(self) -> None:
        fixture = GitFixture(authorities=0)
        self.addCleanup(fixture.close)
        self.assertTrue((fixture.instance / "check_intake.py").is_file())
        with self.assertRaisesRegex(
            evidence.EvidenceError, "legacy validator sources are superseded"
        ):
            fixture.recipe()

    def test_current_authority_requires_v2_generation_and_ssot_binding(self) -> None:
        for field, replacement in (
            ("authority_generation", "pre-v2"),
            ("requirements_authority", "Docs/Stage1_Blueprint_rev-5.6.md"),
            ("positive_acceptance_capable", False),
        ):
            with self.subTest(field=field):
                fixture = GitFixture()
                try:
                    value = json.loads(fixture.contract_path.read_text())
                    value["phases"][0]["validator_authorities"][0][field] = replacement
                    fixture.contract_path.write_text(json.dumps(value), encoding="utf-8")
                    run(fixture.root, "git", "add", ".")
                    run(fixture.root, "git", "commit", "-m", f"bad-{field}")
                    loaded = fixture.loaded()
                    with self.assertRaisesRegex(
                        evidence.EvidenceError, "not bound to the stage1-v2 SSOT"
                    ):
                        fixture.recipe(loaded)
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
        (fixture.validators / "check_0.py").write_text("print('changed')\n", encoding="utf-8")
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

    def test_current_head_compatibility_selection_ignores_only_old_base_blob(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        worker_base = fixture.head
        validator = fixture.validators / "check_0.py"
        validator.write_text("print('current validator')\n", encoding="utf-8")
        run(fixture.root, "git", "add", ".")
        run(fixture.root, "git", "commit", "-m", "change validator")
        loaded = fixture.loaded()
        recipe = evidence.select_validator_recipe(
            fixture.root,
            loaded,
            item_id="S56-M-0001-INTAKE",
            theorem_id="THM-M-0001",
            phase="intake",
            base_revision=worker_base,
            require_base_blob_match=False,
        )
        self.assertEqual(recipe["validator_sha256"], digest(validator))
        self.assertEqual(recipe["authority_revision"], run(fixture.root, "git", "rev-parse", "HEAD"))

        validator.write_text("print('dirty replacement')\n", encoding="utf-8")
        with self.assertRaisesRegex(evidence.EvidenceError, "differs from authoritative HEAD"):
            evidence.select_validator_recipe(
                fixture.root,
                loaded,
                item_id="S56-M-0001-INTAKE",
                theorem_id="THM-M-0001",
                phase="intake",
                base_revision=worker_base,
                require_base_blob_match=False,
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

    def test_staged_overlay_resolves_first_unmerged_receipt_from_head_contract(self) -> None:
        fixture = StagedGitFixture(receipt_bound=True)
        self.addCleanup(fixture.close)
        changed = fixture.write_evidence()
        role_map = fixture.role_map(changed)
        self.assertEqual(role_map["schema_version"], evidence.STAGED_ROLE_MAP_SCHEMA)
        self.assertEqual(set(role_map["staged_delta_paths"]), set(changed))
        self.assertEqual(
            {row["role"] for row in role_map["artifacts"]},
            {"instance_manifest", "discovery_evidence", "phase_receipt"},
        )
        self.assertEqual(
            next(
                row["sha256"]
                for row in role_map["artifacts"]
                if row["role"] == "phase_receipt"
            ),
            digest(fixture.instance / "intake-receipt.json"),
        )
        recipe = evidence.select_validator_recipe(
            fixture.root,
            evidence.load_head_contract(fixture.root, digest(fixture.contract_path)),
            item_id="S56-M-0001-INTAKE",
            theorem_id="THM-M-0001",
            phase="intake",
            base_revision=fixture.base,
        )
        self.assertEqual(recipe["validator_path"], "scripts/stage1_phase_validators/check_0.py")
        self.assertEqual(recipe["validator_sha256"], digest(fixture.validator))

    def test_staged_overlay_rejects_worker_role_and_validator_selection(self) -> None:
        role_fixture = StagedGitFixture(receipt_bound=True)
        self.addCleanup(role_fixture.close)
        role_changed = role_fixture.write_evidence(binding_role="phase_receipt")
        with self.assertRaisesRegex(evidence.EvidenceError, "role disagrees"):
            role_fixture.role_map(role_changed)

        validator_fixture = StagedGitFixture()
        self.addCleanup(validator_fixture.close)
        validator_changed = validator_fixture.write_evidence()
        worker_validator = validator_fixture.instance / "check_intake.py"
        worker_validator.write_text("raise SystemExit(0)\n", encoding="utf-8")
        validator_changed.append(
            "Stage1_Instances/THM-M-0001/check_intake.py"
        )
        with self.assertRaisesRegex(
            evidence.EvidenceError, "scheduler-owned validator"
        ):
            validator_fixture.role_map(validator_changed)

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
            blueprint_git_blob="a" * 40,
            theorem_dag_sha256="2" * 64,
            worker_claim_sha256="3" * 64,
            worker_status_sha256="4" * 64,
            worker_prompt_sha256="5" * 64,
            worker_goal_sha256="6" * 64,
            worker_handoff_sha256="7" * 64,
        )
        self.assertEqual(manifest["authority_revision"], fixture.head)
        self.assertEqual(
            manifest["blueprint"],
            {
                "path": "Docs/Stage1_Blueprint_v2.md",
                "sha256": "1" * 64,
                "git_blob": "a" * 40,
            },
        )
        self.assertEqual(manifest["role_map_sha256"], role_map["manifest_sha256"])
        self.assertEqual(manifest["validator_recipe_sha256"], recipe["recipe_sha256"])
        self.assertEqual(len(manifest["manifest_sha256"]), 64)

    def test_review_manifest_rejects_malformed_blueprint_blob(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        loaded = fixture.loaded()
        role_map = fixture.role_map(loaded)
        recipe = fixture.recipe(loaded)
        with self.assertRaisesRegex(evidence.EvidenceError, "blueprint Git blob"):
            evidence.build_review_manifest(
                loaded,
                role_map,
                recipe,
                blueprint_sha256="1" * 64,
                blueprint_git_blob="not-a-git-oid",
                theorem_dag_sha256="2" * 64,
                worker_claim_sha256="3" * 64,
                worker_status_sha256="4" * 64,
                worker_prompt_sha256="5" * 64,
                worker_goal_sha256="6" * 64,
                worker_handoff_sha256="7" * 64,
            )

    def test_blueprint_authority_binding_rejects_wrong_path_sha_blob_and_revision(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        _loaded, role_map, recipe_with_manifest = fixture.review_inputs()
        manifest = recipe_with_manifest.pop("_review_manifest")
        recipe = recipe_with_manifest
        mutations = {
            "path": lambda value: value["blueprint"].update(path="Docs/other.md"),
            "sha": lambda value: (
                value["blueprint"].update(sha256="0" * 64),
                value.update(blueprint_sha256="0" * 64),
            ),
            "blob": lambda value: value["blueprint"].update(git_blob="0" * 40),
            "revision": lambda value: value.update(authority_revision="0" * 40),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                forged = json.loads(json.dumps(manifest))
                mutate(forged)
                forged.pop("manifest_sha256")
                forged["manifest_sha256"] = evidence.sha256_bytes(
                    evidence.canonical_json(forged)
                )
                with self.assertRaises(evidence.EvidenceError):
                    evidence._require_blueprint_authority_binding(
                        fixture.root, forged
                    )


class ReplayAndSemanticTests(unittest.TestCase):
    def inputs(self, fixture: GitFixture) -> tuple[dict[str, object], dict[str, object], dict[str, object], dict[str, object]]:
        loaded = fixture.loaded()
        role_map = fixture.role_map(loaded)
        recipe = fixture.recipe(loaded)
        manifest = evidence.build_review_manifest(
            loaded, role_map, recipe,
            blueprint_sha256=digest(fixture.blueprint_path),
            blueprint_git_blob=run(
                fixture.root, "git", "rev-parse", "HEAD:Docs/Stage1_Blueprint_v2.md"
            ),
            theorem_dag_sha256="2" * 64,
            worker_claim_sha256="3" * 64, worker_status_sha256="4" * 64,
            worker_prompt_sha256="5" * 64, worker_goal_sha256="6" * 64,
            worker_handoff_sha256="7" * 64,
        )
        manifest["focus_execution"] = {
            "focus_contract_sha256": "8" * 64,
            "execution_disposition": "research_required",
            "receipt_sha256": "9" * 64,
        }
        manifest["focus_contract_sha256"] = evidence.sha256_bytes(
            evidence.canonical_json(manifest["focus_execution"])
        )
        manifest["manifest_sha256"] = evidence.sha256_bytes(
            evidence.canonical_json({
                key: value for key, value in manifest.items()
                if key != "manifest_sha256"
            })
        )
        self._lean_authority = fixture.lean_authority()[0]
        self._fixture = fixture
        return loaded, role_map, recipe, manifest

    def evaluate(
        self,
        replay: dict[str, object],
        fixture: GitFixture,
        **kwargs: object,
    ) -> dict[str, object]:
        real_builder = evidence.build_lean_authority

        def fixture_builder(checkout: Path, **_ignored: object):
            return real_builder(
                checkout,
                toolchain_root=fixture.toolchain_root,
                lake_cache_root=fixture.lean_cache,
            )

        with mock.patch.object(
            evidence, "build_lean_authority", side_effect=fixture_builder
        ):
            return evidence.evaluate_replay_semantics(
                replay, fixture.root, **kwargs
            )

    def test_real_bwrap_replay_is_detached_readonly_and_captures_output(self) -> None:
        if not Path("/usr/bin/bwrap").is_file():
            self.skipTest("bubblewrap unavailable")
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        _loaded, role_map, recipe, manifest = self.inputs(fixture)
        real_builder = evidence.build_lean_authority

        def fixture_builder(checkout: Path, **_kwargs: object):
            return real_builder(
                checkout,
                toolchain_root=fixture.toolchain_root,
                lake_cache_root=fixture.lean_cache,
            )

        with mock.patch.object(
            evidence, "build_lean_authority", side_effect=fixture_builder
        ):
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
        self.assertIn(evidence.LANDLOCK_EXECUTABLE, result["bwrap_argv"])
        self.assertIn("fs", result["bwrap_argv"])
        self.assertNotIn("--ro-bind\x00/\x00/", "\x00".join(result["bwrap_argv"]))
        self.assertEqual(run(fixture.root, "git", "worktree", "list", "--porcelain").count("worktree "), 1)

    def test_lean_authority_binds_exact_package_revision_and_rejects_cache_poisoning(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        package = fixture.lean_packages / "dep"
        package.mkdir()
        run(package, "git", "init", "-b", "main")
        run(package, "git", "config", "user.email", "tests@example.invalid")
        run(package, "git", "config", "user.name", "Stage1 Tests")
        (package / "Dep.lean").write_text("theorem dep : True := True.intro\n")
        run(package, "git", "add", ".")
        run(package, "git", "commit", "-m", "dep")
        revision = run(package, "git", "rev-parse", "HEAD")
        manifest_path = fixture.lean_project / "lake-manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["packages"] = [{
            "url": "https://github.com/example/dep.git",
            "type": "git",
            "subDir": None,
            "scope": "",
            "rev": revision,
            "name": "dep",
            "manifestFile": "lake-manifest.json",
            "inputRev": revision,
            "inherited": False,
            "configFile": "lakefile.toml",
        }]
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        run(fixture.root, "git", "add", "Formalizations/Lean/lake-manifest.json")
        run(fixture.root, "git", "commit", "-m", "pin dependency")

        authority, _toolchain, _cache = fixture.lean_authority()
        self.assertEqual(authority["schema_version"], evidence.LEAN_AUTHORITY_SCHEMA)
        self.assertEqual(len(authority["dependency_packages_sha256"]), 64)

        (package / "Dep.lean").write_text("theorem dep : False := by sorry\n")
        with self.assertRaisesRegex(evidence.EvidenceError, "clean exact checkout"):
            fixture.lean_authority()

    def test_lean_authority_binds_every_mounted_cache_surface(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        baseline = fixture.lean_authority()[0]
        surfaces = [
            fixture.lean_cache / "build" / "Injected.olean",
            fixture.lean_cache / "config" / "lakefile.olean",
        ]
        for index, surface in enumerate(surfaces):
            with self.subTest(surface=surface.relative_to(fixture.lean_cache)):
                surface.write_bytes(f"poison-{index}".encode())
                changed = fixture.lean_authority()[0]
                self.assertNotEqual(
                    changed["compiled_cache_sha256"],
                    baseline["compiled_cache_sha256"],
                )
                self.assertEqual(
                    changed["compiled_cache_file_count"],
                    baseline["compiled_cache_file_count"] + 1,
                )
                surface.unlink()

    def test_lean_authority_binds_full_toolchain_closure(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        library = fixture.toolchain_root / "lib" / "lean"
        library.mkdir(parents=True)
        runtime = library / "libleanshared.so"
        runtime.write_bytes(b"runtime-a")
        baseline = fixture.lean_authority()[0]
        runtime.write_bytes(b"runtime-b")
        changed = fixture.lean_authority()[0]
        self.assertNotEqual(
            changed["toolchain_closure_sha256"],
            baseline["toolchain_closure_sha256"],
        )
        self.assertEqual(
            changed["toolchain_closure_file_count"],
            baseline["toolchain_closure_file_count"],
        )

    def test_lean_authority_binds_cache_mode_and_symlink_semantics(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        artifact = fixture.lean_cache / "build" / "Mode.olean"
        artifact.write_bytes(b"same bytes")
        artifact.chmod(0o600)
        baseline = fixture.lean_authority()[0]
        artifact.chmod(0o640)
        mode_changed = fixture.lean_authority()[0]
        self.assertNotEqual(
            mode_changed["compiled_cache_sha256"],
            baseline["compiled_cache_sha256"],
        )

        first = fixture.lean_cache / "build" / "First.olean"
        second = fixture.lean_cache / "build" / "Second.olean"
        link = fixture.lean_cache / "build" / "Selected.olean"
        first.write_bytes(b"identical")
        second.write_bytes(b"identical")
        link.symlink_to("First.olean")
        first_link = fixture.lean_authority()[0]
        link.unlink()
        link.symlink_to("Second.olean")
        second_link = fixture.lean_authority()[0]
        self.assertNotEqual(
            second_link["compiled_cache_sha256"],
            first_link["compiled_cache_sha256"],
        )

    def test_lean_authority_binds_package_order_and_full_manifest_identity(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        records: list[dict[str, object]] = []
        for name in ("alpha", "beta"):
            package = fixture.lean_packages / name
            package.mkdir()
            run(package, "git", "init", "-b", "main")
            run(package, "git", "config", "user.email", "tests@example.invalid")
            run(package, "git", "config", "user.name", "Stage1 Tests")
            (package / f"{name}.lean").write_text("theorem t : True := True.intro\n")
            run(package, "git", "add", ".")
            run(package, "git", "commit", "-m", name)
            revision = run(package, "git", "rev-parse", "HEAD")
            records.append({
                "url": f"https://github.com/example/{name}.git",
                "type": "git",
                "subDir": None,
                "scope": "example",
                "rev": revision,
                "name": name,
                "manifestFile": "lake-manifest.json",
                "inputRev": revision,
                "inherited": False,
                "configFile": "lakefile.toml",
            })
        manifest_path = fixture.lean_project / "lake-manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["packages"] = records
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        run(fixture.root, "git", "add", "Formalizations/Lean/lake-manifest.json")
        run(fixture.root, "git", "commit", "-m", "pin ordered dependencies")
        baseline = fixture.lean_authority()[0]

        manifest["packages"] = list(reversed(records))
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        reordered = fixture.lean_authority()[0]
        self.assertNotEqual(
            reordered["dependency_packages_sha256"],
            baseline["dependency_packages_sha256"],
        )

    def test_lean_authority_rejects_extra_cache_package_and_boundary_symlink(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        extra = fixture.lean_packages / "unmanifested"
        extra.mkdir()
        with self.assertRaisesRegex(evidence.EvidenceError, "package set"):
            fixture.lean_authority()
        extra.rmdir()
        (fixture.lean_cache / ".lake").symlink_to(fixture.lean_cache)
        with self.assertRaisesRegex(evidence.EvidenceError, "trust boundary"):
            fixture.lean_authority()

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
        real_builder = evidence.build_lean_authority

        def fixture_builder(checkout: Path, **_kwargs: object):
            return real_builder(
                checkout,
                toolchain_root=fixture.toolchain_root,
                lake_cache_root=fixture.lean_cache,
            )

        with mock.patch.object(
            evidence, "build_lean_authority", side_effect=fixture_builder
        ):
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

    def test_landlock_denies_repo_writes_even_if_outer_mount_were_writable(self) -> None:
        if not Path(evidence.LANDLOCK_EXECUTABLE).is_file():
            self.skipTest("Landlock launcher unavailable")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readonly = root / "repo"
            scratch = root / "scratch"
            readonly.mkdir()
            scratch.mkdir()
            result = subprocess.run(
                [
                    evidence.LANDLOCK_EXECUTABLE,
                    "--no-new-privs",
                    "--landlock-access", "fs",
                    "--landlock-rule", f"path-beneath:read-file,read-dir:{readonly}",
                    "--landlock-rule",
                    "path-beneath:execute,read-file,read-dir:/usr",
                    "--landlock-rule",
                    f"path-beneath:execute,write-file,read-file,read-dir,remove-dir,remove-file,make-dir,make-reg,make-sym,refer,truncate:{scratch}",
                    "--",
                    "/usr/bin/python3",
                    "-c",
                    (
                        "import pathlib; "
                        f"pathlib.Path({str(scratch / 'ok')!r}).write_text('ok'); "
                        f"pathlib.Path({str(readonly / 'forbidden')!r}).write_text('no')"
                    ),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue((scratch / "ok").is_file())
            self.assertFalse((readonly / "forbidden").exists())

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
                    real_builder = evidence.build_lean_authority

                    def fixture_builder(checkout: Path, **_kwargs: object):
                        return real_builder(
                            checkout,
                            toolchain_root=fixture.toolchain_root,
                            lake_cache_root=fixture.lean_cache,
                        )

                    with mock.patch.object(
                        evidence, "build_lean_authority", side_effect=fixture_builder
                    ), self.assertRaises(evidence.EvidenceError):
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
            self.evaluate(
                replay, fixture, contract_record=loaded, review_manifest=manifest,
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
        decision = self.evaluate(
            replay, fixture, contract_record=loaded, review_manifest=manifest,
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
        decision = self.evaluate(
            replay, fixture, contract_record=loaded, review_manifest=manifest,
            role_map=role_map, validator_recipe=recipe,
            worker_verdict="accepted", review_verdict="phase_accepted",
            audit_complete=True, theorem_complete=False,
        )
        self.assertFalse(decision["phase_evidence_accepted"])
        self.assertIn(
            "audit_complete_outside_phase_contract", decision["negative_reasons"]
        )

    def test_accepted_audit_only_records_audit_but_cannot_accept_release(self) -> None:
        fixture = GitFixture()
        self.addCleanup(fixture.close)
        loaded, role_map, recipe, manifest = self.inputs(fixture)
        phase_row = loaded["contract"]["phases"][0]
        phase_row["worker_verdicts_eligible_for_review"] = ["accepted", "no_state_change"]
        phase_row["audit_boundary"]["allowed_audit_complete_values"] = [True]
        phase_row["theorem_boundary"]["allowed_theorem_complete_values"] = [True]
        replay = self.replay_result(
            fixture,
            loaded,
            role_map,
            recipe,
            manifest,
            self.semantic(audit_complete=True, theorem_complete=False),
        )
        replay["result_sha256"] = evidence.sha256_bytes(
            evidence.canonical_json({
                key: value for key, value in replay.items()
                if key != "result_sha256"
            })
        )
        decision = self.evaluate(
            replay,
            fixture,
            contract_record=loaded,
            review_manifest=manifest,
            role_map=role_map,
            validator_recipe=recipe,
            worker_verdict="accepted_audit_only",
            review_verdict="phase_accepted",
            audit_complete=True,
            theorem_complete=False,
        )
        self.assertFalse(decision["phase_evidence_accepted"])
        self.assertEqual(decision["decision"], "remain_[_]")
        self.assertIn(
            "accepted_audit_only_cannot_close_release",
            decision["negative_reasons"],
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
            self.evaluate(
                replay, fixture, contract_record=loaded, review_manifest=manifest,
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
            "validator_input_sha256": evidence._validator_input(
                manifest, role_map, recipe, self._lean_authority
            )["input_sha256"],
            "lean_authority": self._lean_authority,
            "lean_authority_sha256": evidence.sha256_bytes(
                evidence.canonical_json(self._lean_authority)
            ),
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
                decision = self.evaluate(
                    self.replay_result(
                        fixture, loaded, role_map, recipe, manifest,
                        self.semantic(**mutation),
                    ),
                    fixture,
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
        blocked = self.evaluate(
            replay, fixture,
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
        positive = self.evaluate(
            replay, fixture,
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

    def test_replayed_integration_semantics_are_proof_phase_only(self) -> None:
        source = {"file_sha256": "a" * 64, "match_kind": "exact"}
        focus = {
            "execution_disposition": "organize_or_integrate",
            "exact_machine_source": source,
        }
        valid = {
            "exact_machine_source_consumed": True,
            "exact_machine_source_sha256": evidence.sha256_bytes(
                evidence.canonical_json(source)
            ),
            "introduced_root_critical_proof": False,
            "validated_artifact_sha256": "b" * 64,
            "match_kind": "exact",
            "source_consumption": "exact_vendored_provider_dependency",
            "provider_declaration": "Provider.proof",
            "consumer_declaration": "Consumer.proof",
            "provider_dependency_proven": True,
            "exact_vendoring_proven": True,
        }
        statement_replay = {
            "phase": "statement",
            "semantic_result": {},
        }
        self.assertEqual(
            evidence.require_replayed_integration_source_semantics(
                statement_replay,
                focus,
                {"artifacts": [{"role": "phase_receipt"}]},
            ),
            {},
        )
        with self.assertRaisesRegex(
            evidence.EvidenceError, "non-source-consuming phase"
        ):
            evidence.require_replayed_integration_source_semantics(
                {
                    "phase": "statement",
                    "semantic_result": {"integration_source_semantics": valid},
                },
                focus,
                {"artifacts": [{"role": "phase_receipt"}]},
            )
        proof_roles = {"artifacts": [{"role": "proof_sources"}]}
        self.assertEqual(
            evidence.require_replayed_integration_source_semantics(
                {
                    "phase": "proof",
                    "semantic_result": {"integration_source_semantics": valid},
                },
                focus,
                proof_roles,
            ),
            valid,
        )
        forged = dict(valid, introduced_root_critical_proof=True)
        with self.assertRaisesRegex(
            evidence.EvidenceError, "did not independently certify"
        ):
            evidence.require_replayed_integration_source_semantics(
                {
                    "phase": "proof",
                    "semantic_result": {"integration_source_semantics": forged},
                },
                focus,
                proof_roles,
            )

    def test_semantic_stdout_accepts_typed_integration_source_extension(self) -> None:
        semantic = self.semantic()
        semantic["integration_source_semantics"] = {
            "exact_machine_source_consumed": True,
            "exact_machine_source_sha256": "a" * 64,
            "introduced_root_critical_proof": False,
            "validated_artifact_sha256": "b" * 64,
            "match_kind": "exact",
            "source_consumption": "exact_vendored_provider_dependency",
            "provider_declaration": "Provider.proof",
            "consumer_declaration": "Consumer.proof",
            "provider_dependency_proven": True,
            "exact_vendoring_proven": True,
        }
        self.assertEqual(
            evidence._parse_validator_semantic_stdout(
                evidence.canonical_json(semantic) + b"\n"
            ),
            semantic,
        )
        forged = json.loads(json.dumps(semantic))
        forged["integration_source_semantics"]["provider_dependency_proven"] = False
        with self.assertRaisesRegex(
            evidence.EvidenceError, "integration source semantics are malformed"
        ):
            evidence._parse_validator_semantic_stdout(
                evidence.canonical_json(forged) + b"\n"
            )


if __name__ == "__main__":
    unittest.main()
