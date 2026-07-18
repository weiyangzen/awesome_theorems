#!/usr/bin/env python3
"""Focused tests for the central Stage1 v2 phase authority."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock


PATH = Path(__file__).with_name("stage1_phase_validators") / "current.py"
SPEC = importlib.util.spec_from_file_location("stage1_phase_validator_current_test", PATH)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()


class CurrentValidatorTests(unittest.TestCase):
    def test_release_contract_excludes_audit_only_from_positive_review(self) -> None:
        contract = json.loads(
            (Path(__file__).resolve().parents[1] / validator.CONTRACT_PATH).read_text(
                encoding="utf-8"
            )
        )
        release = next(row for row in contract["phases"] if row["phase"] == "release")
        self.assertEqual(release["worker_verdicts_eligible_for_review"], [
            "accepted", "no_state_change"
        ])
        self.assertEqual(
            release["theorem_boundary"]["allowed_theorem_complete_values"],
            [True],
        )
        self.assertTrue(
            release["theorem_boundary"][
                "phase_acceptance_implies_theorem_complete"
            ]
        )

    def validate_fixture_packet(self, root: Path, packet: dict[str, object]):
        binary_bytes = {
            Path("/stage1-toolchain/bin/lean"): b"lean-binary",
            Path("/stage1-toolchain/bin/lake"): b"lake-binary",
        }
        authority = packet["lean_authority"]
        assert isinstance(authority, dict)
        authority["lean_binary_sha256"] = hashlib.sha256(
            binary_bytes[Path("/stage1-toolchain/bin/lean")]
        ).hexdigest()
        authority["lake_binary_sha256"] = hashlib.sha256(
            binary_bytes[Path("/stage1-toolchain/bin/lake")]
        ).hexdigest()
        packet.pop("input_sha256", None)
        packet["input_sha256"] = hashlib.sha256(canonical(packet)).hexdigest()
        real_exact_file = validator.exact_file

        def exact_file(path: Path, label: str) -> bytes:
            return binary_bytes[path] if path in binary_bytes else real_exact_file(path, label)

        with mock.patch.object(validator, "exact_file", side_effect=exact_file):
            return validator.validate(canonical(packet))

    def fixture(self, root: Path) -> tuple[bytes, Path]:
        docs = root / "Docs"
        owner = root / "Stage1_Instances" / "THM-M-0001"
        docs.mkdir()
        owner.mkdir(parents=True)
        lean_project = root / validator.LEAN_PROJECT
        lean_project.mkdir(parents=True)
        (lean_project / "lean-toolchain").write_text("leanprover/lean4:v4.29.0\n")
        (lean_project / "lake-manifest.json").write_text('{"packages":[]}\n')
        (lean_project / "lakefile.lean").write_text(
            "import Lake\nopen Lake DSL\npackage fixture where\n"
        )
        artifact = owner / "instance.json"
        artifact_value = {
            "schema_version": "stage1-instance-intake/1.0",
            "item_id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "lifecycle_mode": "planned",
            "lifecycle": "planned",
            "audit_complete": False,
            "theorem_complete": False,
            "canonical_name": "Fixture theorem",
            "canonical_statement": "True",
            "canonical_formal_target": None,
            "domain_and_universes": [],
            "quantifiers": [],
            "hypotheses": [],
            "conclusion": "True",
            "alternate_encodings": [],
            "excluded_degenerate_cases": [],
            "foundation_profile": "fixture",
            "tcb_profile": "fixture",
            "computation_profile": "none",
            "formal_system": "Lean 4",
            "source_revisions": {},
            "obligation_registry_hash": None,
            "discovery_protocol_hash": None,
            "public_merge_targets": [],
            "owners_and_reviewers": {},
            "freshness_and_revocation_policy": {},
            "status_boundary": "Formal target remains open.",
        }
        artifact.write_text(json.dumps(artifact_value))
        scope = owner / "scope-map.md"
        scope.write_text("# THM-M-0001 scope\nExact fixture boundary.\n")
        crosswalk = owner / "source-statement-crosswalk.md"
        crosswalk.write_text("# THM-M-0001 source crosswalk\nExact fixture source.\n")
        dag = owner / "task-dag.json"
        dag.write_text(json.dumps({
            "schema_version": "stage1-open-task-dag/1.0",
            "item_id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "lifecycle_mode": "planned",
            "lifecycle": "planned",
            "theorem_complete": False,
            "tasks": [{
                "id": "S56-M-0001-STATEMENT", "phase": "statement",
                "state": "open", "depends_on": ["S56-M-0001-INTAKE"],
            }],
        }))
        receipt = owner / "intake-receipt.json"
        receipt_value = {
            "schema_version": "stage1-node-receipt/1.0",
            "receipt_id": "r1",
            "item_id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "phase": "intake",
            "intent": "intake",
            "base_revision": "b" * 40,
            "base_tree": "c" * 40,
            "inputs": {},
            "support_state": "self_tested",
            "proposed_state": "[_]",
            "accepted": False,
            "verdict": "accepted",
            "selftest_status": "passed",
            "selftest_result": {"exit_code": 0, "commands": ["check"]},
            "known_failures": [],
            "first_failed_gate": None,
            "retry_condition": None,
            "status_boundary": "phase only",
            "audit_complete": False,
            "theorem_complete": False,
            "invalidation_inputs": [],
            "focus_execution": None,
            "lifecycle_after": "planned",
        }
        receipt.write_text(json.dumps(receipt_value))
        contract = {
            "phases": [{
                "phase": "intake",
                "intent": "intake",
                "worker_verdicts_eligible_for_review": ["accepted", "no_state_change"],
                "audit_boundary": {"allowed_audit_complete_values": [False]},
                "theorem_boundary": {"allowed_theorem_complete_values": [False]},
                "phase_receipt_required_fields": ["/schema_version"],
                "required_artifact_roles": [
                    {"role": "instance_manifest", "requirement": "required", "cardinality": "exactly_one"},
                    {"role": "scope_map", "requirement": "required", "cardinality": "exactly_one"},
                    {"role": "source_crosswalk", "requirement": "required", "cardinality": "exactly_one"},
                    {"role": "open_task_dag", "requirement": "required", "cardinality": "exactly_one"},
                    {"role": "phase_receipt", "requirement": "required", "cardinality": "exactly_one"},
                ],
                "semantic_gates": [
                    {"gate_id": "I01-ARTIFACTS"},
                    {"gate_id": "I02-PLANNED-STATE"},
                    {"gate_id": "I03-CONTENT"},
                ],
            }]
        }
        contract_path = docs / "Stage1_Phase_Acceptance_Contracts.json"
        contract_path.write_text(json.dumps(contract))
        artifacts = []
        for role, path in (
            ("instance_manifest", artifact), ("scope_map", scope),
            ("source_crosswalk", crosswalk), ("open_task_dag", dag),
            ("phase_receipt", receipt),
        ):
            data = path.read_bytes()
            artifacts.append({
                "role": role,
                "path": path.relative_to(root).as_posix(),
                "sha256": hashlib.sha256(data).hexdigest(),
                "git_blob": "d" * 40,
            })
        role_map = {
            "schema_version": "stage1-phase-artifact-role-map/1.0",
            "item_id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "phase": "intake",
            "base_revision": "b" * 40,
            "authority_revision": "a" * 40,
            "staged_delta_paths": [
                path.relative_to(root).as_posix()
                for path in (artifact, scope, crosswalk, dag, receipt)
            ],
            "artifacts": artifacts,
        }
        role_map["manifest_sha256"] = hashlib.sha256(canonical(role_map)).hexdigest()
        focus = {
            "focus_contract_sha256": "e" * 64,
            "execution_disposition": "research_required",
            "receipt_sha256": "f" * 64,
        }
        receipt_value["focus_execution"] = focus
        receipt.write_text(json.dumps(receipt_value))
        receipt_binding = next(
            row for row in artifacts if row["role"] == "phase_receipt"
        )
        receipt_binding["sha256"] = hashlib.sha256(receipt.read_bytes()).hexdigest()
        role_map["manifest_sha256"] = hashlib.sha256(
            canonical({
                key: value for key, value in role_map.items()
                if key != "manifest_sha256"
            })
        ).hexdigest()
        toolchain_data = (lean_project / "lean-toolchain").read_bytes()
        lock_data = (lean_project / "lake-manifest.json").read_bytes()
        lean_authority = {
            "schema_version": validator.LEAN_AUTHORITY_SCHEMA,
            "toolchain": "leanprover/lean4:v4.29.0",
            "toolchain_file_sha256": hashlib.sha256(toolchain_data).hexdigest(),
            "dependency_lock_sha256": hashlib.sha256(lock_data).hexdigest(),
            "dependency_packages_sha256": "3" * 64,
            "toolchain_closure_sha256": "5" * 64,
            "toolchain_closure_file_count": 1,
            "toolchain_closure_bytes": 1,
            "compiled_cache_sha256": "4" * 64,
            "compiled_cache_file_count": 1,
            "compiled_cache_bytes": 1,
            "lean_binary_sha256": "1" * 64,
            "lake_binary_sha256": "2" * 64,
            "toolchain_mount": "/stage1-toolchain",
            "lake_cache_mount": "/stage1-lake-cache",
            "network_policy": "denied",
            "repo_access": "read_only",
        }
        packet = {
            "schema_version": validator.INPUT_SCHEMA,
            "item_id": "S56-M-0001-INTAKE",
            "theorem_id": "THM-M-0001",
            "phase": "intake",
            "authority_revision": "a" * 40,
            "base_revision": "b" * 40,
            "contract": {
                "path": validator.CONTRACT_PATH,
                "sha256": hashlib.sha256(contract_path.read_bytes()).hexdigest(),
                "git_blob": "1" * 40,
            },
            "role_map": role_map,
            "focus_execution": focus,
            "focus_contract_sha256": hashlib.sha256(canonical(focus)).hexdigest(),
            "lean_authority": lean_authority,
        }
        packet["input_sha256"] = hashlib.sha256(canonical(packet)).hexdigest()
        return canonical(packet), artifact

    def test_all_phase_focus_contract_rules_are_fail_closed(self) -> None:
        research_focus = {
            "focus_contract_sha256": "e" * 64,
            "execution_disposition": "research_required",
            "receipt_sha256": "f" * 64,
        }
        integration_source = {
            "formal_system": "Lean 4",
            "repository": "https://example.invalid/proofs",
            "revision": "a" * 40,
            "tree_or_archive_sha256": "1" * 64,
            "file_path": "Proof.lean",
            "file_sha256": "2" * 64,
            "module": "External.Proof",
            "declaration": "External.proof",
            "declaration_type_sha256": "3" * 64,
            "match_kind": "exact",
            "transport_evidence": [],
            "terminal_proof_body": {
                "locator": "External.proof", "kind": "theorem", "sha256": "4" * 64,
            },
        }
        integration_focus = {
            **research_focus,
            "execution_disposition": "organize_or_integrate",
            "machine_evidence_class": "exact_external_unintegrated",
            "exact_machine_source": integration_source,
            "exact_machine_source_used": True,
            "introduced_root_critical_proof": False,
        }
        frontier_focus = {
            **research_focus,
            "execution_disposition": "frontier_exception",
        }
        intents = {
            "intake": "intake", "statement": "audit", "anchor_audit": "audit",
            "obligation_tree": "audit", "proof": {
                "organize_or_integrate": "integrate",
                "frontier_exception": "frontier_prove",
            }, "validation": "validate", "release": "release",
        }
        for phase, intent_contract in intents.items():
            for focus in (integration_focus, frontier_focus):
                expected_intent = (
                    intent_contract[focus["execution_disposition"]]
                    if isinstance(intent_contract, dict) else intent_contract
                )
                receipt = {"intent": expected_intent, "focus_execution": focus}
                validator.require_focus_semantic_bindings(
                    phase, receipt, focus, {"intent": intent_contract}
                )
                mutations = (
                    ({**focus, "unexpected": True}, "exactly bound"),
                    ({**focus, "receipt_sha256": "not-a-digest"}, "exactly bound"),
                )
                for mutated, message in mutations:
                    with self.assertRaisesRegex(validator.ValidationError, message):
                        validator.require_focus_semantic_bindings(
                            phase,
                            {"intent": expected_intent, "focus_execution": mutated},
                            mutated,
                            {"intent": intent_contract},
                        )
                if focus["execution_disposition"] == "organize_or_integrate":
                    for mutated in (
                        {**focus, "exact_machine_source_used": False},
                        {**focus, "introduced_root_critical_proof": True},
                        {
                            **focus,
                            "exact_machine_source": {
                                **integration_source, "unexpected": True,
                            },
                        },
                    ):
                        with self.assertRaisesRegex(
                            validator.ValidationError, "exactly bound"
                        ):
                            validator.require_focus_semantic_bindings(
                                phase,
                                {"intent": expected_intent, "focus_execution": mutated},
                                mutated,
                                {"intent": intent_contract},
                            )
                with self.assertRaisesRegex(validator.ValidationError, "exactly bound"):
                    validator.require_focus_semantic_bindings(
                        phase,
                        {"intent": "wrong", "focus_execution": focus},
                        focus,
                        {"intent": intent_contract},
                    )

        for phase in validator.PHASES - validator.RESEARCH_PHASES:
            with self.assertRaisesRegex(validator.ValidationError, "permitted focus"):
                validator.require_focus_semantic_bindings(
                    phase,
                    {"intent": intents[phase], "focus_execution": research_focus},
                    research_focus,
                    {"intent": intents[phase]},
                )

        research_receipt = {"focus_execution": research_focus}
        for phase in validator.RESEARCH_PHASES:
            research_receipt["intent"] = intents[phase]
            validator.require_focus_semantic_bindings(
                phase, research_receipt, research_focus, {"intent": intents[phase]}
            )

    def test_exact_vendoring_hash_is_not_type_only_reproof_evidence(self) -> None:
        external = (
            b"namespace Provider\n"
            b"theorem proof : True := by trivial\n"
            b"end Provider\n"
        )
        independent = (
            b"namespace Provider\n"
            b"theorem proof : True := by exact True.intro\n"
            b"end Provider\n"
        )
        expected = validator.declaration_region_sha256(external, "Provider.proof")
        self.assertIsNotNone(expected)
        self.assertNotEqual(
            expected,
            validator.declaration_region_sha256(independent, "Provider.proof"),
        )
        source = {
            "path": "Stage1_Instances/THM-M-0001/Provider.lean",
            "sha256": hashlib.sha256(independent).hexdigest(),
        }
        self.assertIsNone(
            validator.exact_vendored_provider(
                [source],
                {source["path"]: independent},
                theorem_id="THM-M-0001",
                declaration="Provider.proof",
                terminal_body_sha256=str(expected),
            )
        )

    def test_same_file_vendoring_always_requires_kernel_provider_consumption(self) -> None:
        source_path = "Stage1_Instances/THM-M-0001/Proof.lean"
        source = (
            b"namespace Provider\n"
            b"theorem proof : True := by trivial\n"
            b"theorem target : True := by trivial\n"
            b"end Provider\n"
        )
        binding = {
            "path": source_path,
            "sha256": hashlib.sha256(source).hexdigest(),
        }
        terminal = validator.declaration_region_sha256(source, "Provider.proof")
        vendored = validator.exact_vendored_provider(
            [binding], {source_path: source}, theorem_id="THM-M-0001",
            declaration="Provider.proof", terminal_body_sha256=str(terminal),
        )
        self.assertIsNotNone(vendored)
        replay = {
            "provider_dependency": {
                "schema": validator.DEPENDENCY_PROBE_SCHEMA,
                "consumer": "Provider.target",
                "provider": "Provider.proof",
                "provider_module": "Proof",
                "relation": "direct_proof_body_constant_dependency",
            }
        }
        self.assertEqual(replay["provider_dependency"]["provider"], "Provider.proof")
        attacked = dict(replay)
        attacked.pop("provider_dependency")
        self.assertNotIn("provider_dependency", attacked)

    def test_research_only_changed_lean_paths_are_checked_fail_closed(self) -> None:
        focus = {"execution_disposition": "research_required"}
        statement_path = "Stage1_Instances/THM-M-0001/Statement.lean"
        anchor_path = "Stage1_Instances/THM-M-0001/AnchorAudit.lean"
        validator.reject_research_proof_construction(
            "statement", focus, {"staged_delta_paths": [statement_path]},
            {statement_path: b"variable (Target : Prop)\n#check Target\n"},
        )
        for declaration in (
            b"theorem Target : True := by trivial\n",
            b"def Target : True := by trivial\n",
            b"private noncomputable def Target : True := by trivial\n",
            b"abbrev Target : True := by trivial\n",
            b"opaque Target : True\n",
            b"example : True := by trivial\n",
            b"instance : Nonempty True := inferInstance\n",
            b"structure Carrier where proof : True\n",
            b"inductive Hidden : Prop where | proof : Hidden\n",
            b"elab \"makeProof\" : command => pure ()\n",
            b"run_cmd Lean.Elab.Command.elabCommand (`(theorem X : True := by trivial))\n",
        ):
            with (
                self.subTest(declaration=declaration),
                self.assertRaisesRegex(validator.ValidationError, "persistent Lean"),
            ):
                validator.reject_research_proof_construction(
                    "statement", focus, {"staged_delta_paths": [statement_path]},
                    {statement_path: declaration},
                )
        with self.assertRaisesRegex(validator.ValidationError, "anchor audit"):
            validator.reject_research_proof_construction(
                "anchor_audit", focus, {"staged_delta_paths": [anchor_path]},
                {anchor_path: b"theorem hiddenProof : True := by trivial\n"},
            )
        with self.assertRaisesRegex(validator.ValidationError, "not a bound phase artifact"):
            validator.reject_research_proof_construction(
                "anchor_audit", focus, {"staged_delta_paths": [anchor_path]}, {},
            )
        with self.assertRaisesRegex(validator.ValidationError, "intake"):
            validator.reject_research_proof_construction(
                "intake", focus, {"staged_delta_paths": [statement_path]},
                {statement_path: b"variable (Target : Prop)\n"},
            )

    def test_checked_transport_focus_binds_one_exact_target_identity(self) -> None:
        transport = {
            "path": "Stage1_Instances/THM-M-0001/machine-transport-replay.json",
            "sha256": "1" * 64,
            "role": "statement_match",
            "evidence_kind": "machine_checked_statement_transport",
            "source_formal_system": "Lean 4",
            "source_declaration": "Provider.proof",
            "source_declaration_type_sha256": "2" * 64,
            "target_formal_system": "Lean 4",
            "target_declaration": "Consumer.wrapper",
            "target_declaration_type_sha256": "3" * 64,
            "replay_receipt_sha256": "1" * 64,
        }
        source = {
            "formal_system": "Lean 4",
            "repository": "https://example.invalid/provider",
            "revision": "a" * 40,
            "tree_or_archive_sha256": "4" * 64,
            "file_path": "Provider.lean",
            "file_sha256": "5" * 64,
            "module": "Provider",
            "declaration": "Provider.proof",
            "declaration_type_sha256": "2" * 64,
            "match_kind": "checked_transport",
            "transport_evidence": [transport],
            "terminal_proof_body": {
                "locator": "Provider.proof", "kind": "theorem", "sha256": "6" * 64,
            },
        }
        focus = {
            "focus_contract_sha256": "7" * 64,
            "execution_disposition": "organize_or_integrate",
            "receipt_sha256": "8" * 64,
            "machine_evidence_class": "exact_pinned_closure",
            "exact_machine_source": source,
            "exact_machine_source_used": True,
            "introduced_root_critical_proof": False,
        }
        receipt = {"intent": "integrate", "focus_execution": focus}
        validator.require_focus_semantic_bindings(
            "proof", receipt, focus,
            {"intent": {"organize_or_integrate": "integrate"}},
        )
        for mutate in (
            lambda row: row["exact_machine_source"].update(transport_evidence=[]),
            lambda row: row["exact_machine_source"]["transport_evidence"][0].update(
                target_declaration_type_sha256="not-a-digest"
            ),
        ):
            attacked = copy.deepcopy(focus)
            mutate(attacked)
            with self.assertRaisesRegex(validator.ValidationError, "exactly bound"):
                validator.require_focus_semantic_bindings(
                    "proof",
                    {"intent": "integrate", "focus_execution": attacked},
                    attacked,
                    {"intent": {"organize_or_integrate": "integrate"}},
                )

    def test_positive_and_tampered_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw, artifact = self.fixture(root)
            # Validator paths are relative to process cwd; switch only for this fixture.
            old = os.getcwd()
            os.chdir(root)
            try:
                binary_bytes = {
                    Path("/stage1-toolchain/bin/lean"): b"lean-binary",
                    Path("/stage1-toolchain/bin/lake"): b"lake-binary",
                }
                packet = json.loads(raw)
                packet["lean_authority"]["lean_binary_sha256"] = hashlib.sha256(
                    binary_bytes[Path("/stage1-toolchain/bin/lean")]
                ).hexdigest()
                packet["lean_authority"]["lake_binary_sha256"] = hashlib.sha256(
                    binary_bytes[Path("/stage1-toolchain/bin/lake")]
                ).hexdigest()
                packet.pop("input_sha256")
                packet["input_sha256"] = hashlib.sha256(canonical(packet)).hexdigest()
                raw = canonical(packet)
                real_exact_file = validator.exact_file

                def exact_file(path: Path, label: str) -> bytes:
                    return binary_bytes[path] if path in binary_bytes else real_exact_file(path, label)

                with mock.patch.object(validator, "exact_file", side_effect=exact_file):
                    result = validator.validate(raw)
                self.assertTrue(result["phase_accepted"])
                artifact.write_text("tampered\n")
                with mock.patch.object(validator, "exact_file", side_effect=exact_file):
                    with self.assertRaisesRegex(validator.ValidationError, "digest is stale"):
                        validator.validate(raw)
            finally:
                os.chdir(old)

    def test_intake_surface_fields_cannot_replace_semantic_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw, _ = self.fixture(root)
            packet = json.loads(raw)
            packet["role_map"]["artifacts"] = [
                row for row in packet["role_map"]["artifacts"]
                if row["role"] not in {"scope_map", "source_crosswalk", "open_task_dag"}
            ]
            packet["role_map"].pop("manifest_sha256")
            packet["role_map"]["manifest_sha256"] = hashlib.sha256(
                canonical(packet["role_map"])
            ).hexdigest()
            packet.pop("input_sha256")
            packet["input_sha256"] = hashlib.sha256(canonical(packet)).hexdigest()
            old = os.getcwd()
            os.chdir(root)
            try:
                with self.assertRaisesRegex(validator.ValidationError, "required artifact role"):
                    self.validate_fixture_packet(root, packet)
            finally:
                os.chdir(old)

    def test_intake_spoofed_lifecycle_and_cyclic_dag_are_rejected(self) -> None:
        for mutation, message in (
            (lambda root: json.loads((root / "Stage1_Instances/THM-M-0001/instance.json").read_text()) | {"lifecycle": "accepted"}, "planned-state"),
            (lambda root: json.loads((root / "Stage1_Instances/THM-M-0001/task-dag.json").read_text()) | {"tasks": [
                {"id": "S56-M-0001-STATEMENT", "phase": "statement", "state": "open", "depends_on": ["S56-M-0001-PROOF"]},
                {"id": "S56-M-0001-PROOF", "phase": "proof", "state": "open", "depends_on": ["S56-M-0001-STATEMENT"]},
            ]}, "cycle"),
        ):
            with self.subTest(message=message), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                raw, _ = self.fixture(root)
                packet = json.loads(raw)
                role = "instance_manifest" if message == "planned-state" else "open_task_dag"
                binding = next(row for row in packet["role_map"]["artifacts"] if row["role"] == role)
                path = root / binding["path"]
                path.write_text(json.dumps(mutation(root)))
                binding["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                packet["role_map"].pop("manifest_sha256")
                packet["role_map"]["manifest_sha256"] = hashlib.sha256(canonical(packet["role_map"])).hexdigest()
                packet.pop("input_sha256")
                packet["input_sha256"] = hashlib.sha256(canonical(packet)).hexdigest()
                old = os.getcwd()
                os.chdir(root)
                try:
                    with self.assertRaisesRegex(validator.ValidationError, message):
                        self.validate_fixture_packet(root, packet)
                finally:
                    os.chdir(old)

    def test_structured_phase_replay_requires_typed_gate_results(self) -> None:
        recipe = {
            "argv": ["/usr/bin/python3", "-I", "-B", "scripts/stage1_phase_replays/validation.py"],
            "cwd": ".", "env_allowlist": {}, "timeout_seconds": 30,
            "network_policy": "denied", "expected_exit": 0,
        }
        gates = ["V01-ARTIFACTS", "V02-RECIPES", "V03-TRUST-PROVENANCE", "V04-CONSUMER-REUSE"]
        positive = {
            "schema_version": "stage1-phase-semantic-replay/1.0",
            "phase": "validation", "semantic_verdict": "passed",
            "gate_results": {gate: "passed" for gate in gates},
            "open_obligations": 0, "stale_inputs": [], "blocked": False,
        }
        stdout = validator.PHASE_RESULT_BEGIN.encode() + canonical(positive) + validator.PHASE_RESULT_END.encode() + b"\n"
        runner = mock.Mock(return_value=subprocess.CompletedProcess([], 0, stdout=stdout, stderr=b""))
        with mock.patch.object(validator, "safe_path", return_value=Path("scripts/stage1_phase_replays/validation.py")):
            result = validator.run_structured_phase_recipe(recipe, "validation", gates, command_runner=runner)
        self.assertEqual(result["semantic_verdict"], "passed")
        forged = dict(positive)
        forged["gate_results"] = {gate: "passed" for gate in gates}
        forged["gate_results"]["V03-TRUST-PROVENANCE"] = "fail_closed"
        bad_stdout = validator.PHASE_RESULT_BEGIN.encode() + canonical(forged) + validator.PHASE_RESULT_END.encode() + b"\n"
        runner.return_value = subprocess.CompletedProcess([], 0, stdout=bad_stdout, stderr=b"")
        with (
            mock.patch.object(validator, "safe_path", return_value=Path("scripts/stage1_phase_replays/validation.py")),
            self.assertRaisesRegex(validator.ValidationError, "nonpositive"),
        ):
            validator.run_structured_phase_recipe(recipe, "validation", gates, command_runner=runner)

    def test_statement_semantics_replay_type_and_mutations(self) -> None:
        target_hash = hashlib.sha256(b"True").hexdigest()
        mutations = [
            {"kind": kind, "expression_sha256": hashlib.sha256(kind.encode()).hexdigest()}
            for kind in ("removed_hypothesis", "changed_domain", "changed_binder_scope", "boundary_case")
        ]
        record = {
            "schema_version": "stage1-statement/1.0", "item_id": "S56-M-0001-STATEMENT",
            "theorem_id": "THM-M-0001", "statement_elaborated": True,
            "audit_complete": False, "theorem_complete": False,
            "canonical_formal_target": {
                "backend": "lean4", "module": "Stage1_Instances/THM-M-0001/Statement.lean",
                "declaration_or_expression": "Fixture.Target",
                "elaborated_expression_sha256": target_hash, "statement_file_sha256": "a" * 64,
            },
            "mutation_tests": {"killed": mutations},
        }
        receipt = {
            "intent": "audit", "statement_fingerprints": [f"sha256:{target_hash}"],
            "mutation_tests": {"executed": mutations},
        }
        roles = {
            "statement_record": [{"path": "record.json"}],
            "statement_source": [{"path": "Stage1_Instances/THM-M-0001/Statement.lean", "sha256": "a" * 64}],
        }
        phase = {"semantic_gates": [
            {"gate_id": "S01-ARTIFACTS"}, {"gate_id": "S02-EXACT-TARGET"},
            {"gate_id": "S03-MUTATIONS"},
        ]}
        replay = {"declaration_type_sha256s": {"Fixture.Target": target_hash}}
        with mock.patch.object(validator, "replay_declarations", return_value=replay):
            result = validator.validate_statement_semantics(
                receipt, phase, roles, {"record.json": canonical(record)},
                "S56-M-0001-STATEMENT", "THM-M-0001", {}, {},
            )
        self.assertEqual(result["statement_type_sha256"], target_hash)
        receipt["mutation_tests"]["executed"][0]["expression_sha256"] = target_hash
        with (
            mock.patch.object(validator, "replay_declarations", return_value=replay),
            self.assertRaisesRegex(validator.ValidationError, "did not distinguish"),
        ):
            validator.validate_statement_semantics(
                receipt, phase, roles, {"record.json": canonical(record)},
                "S56-M-0001-STATEMENT", "THM-M-0001", {}, {},
            )

    def test_tampered_input_digest_is_typed_negative(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            raw, _ = self.fixture(Path(directory))
            packet = json.loads(raw)
            packet["phase"] = "proof"
            with self.assertRaisesRegex(validator.ValidationError, "input digest"):
                validator.validate(canonical(packet))

    def test_lean_replay_executes_read_only_probe_and_parses_kernel_facts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / validator.LEAN_PROJECT
            source = root / "Stage1_Instances" / "THM-M-0001" / "Proof.lean"
            source.parent.mkdir(parents=True)
            project.mkdir(parents=True)
            source.write_text("theorem localProof : True := by trivial\n")
            (project / "lean-toolchain").write_text("leanprover/lean4:v4.29.0\n")
            (project / "lake-manifest.json").write_text('{"packages":[]}\n')
            (project / "lakefile.lean").write_text(
                "import Lake\nopen Lake DSL\npackage fixture where\n"
            )
            tool_root = root / "toolchain"
            cache = root / "cache"
            (tool_root / "bin").mkdir(parents=True)
            (cache / "packages").mkdir(parents=True)
            (cache / "build").mkdir()
            for name in ("lean", "lake"):
                executable = tool_root / "bin" / name
                executable.write_bytes(name.encode())
                executable.chmod(0o700)
            stdout = (
                b"localProof : misleading worker #check output\n"
                b"STAGE1_PROBE_BEGIN {\"axioms\":[],\"declaration\":\"localProof\","
                b"\"index\":0,\"schema\":\"stage1-lean-probe-row/1.0\","
                b"\"type\":\"True\"} STAGE1_PROBE_END\n"
            )
            captured: dict[str, object] = {}

            def runner(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[bytes]:
                captured["argv"] = argv
                probe = Path(argv[-1])
                if probe.name == "AuthorityProbe.lean":
                    text = probe.read_text()
                    self.assertIn("import Proof", text)
                    self.assertNotIn("#check", text)
                    self.assertNotIn(source.read_text(), text)
                self.assertFalse(kwargs.get("shell"))
                return subprocess.CompletedProcess(argv, 0, stdout=stdout, stderr=b"")

            old = os.getcwd()
            os.chdir(root)
            try:
                result = validator.readonly_lean_replay(
                    Path("Stage1_Instances/THM-M-0001/Proof.lean"),
                    ["localProof"],
                    command_runner=runner,
                    tool_root=tool_root,
                    cache=cache,
                    scratch_root=root,
                    dependency_packages_sha256="3" * 64,
                    compiled_cache_sha256="4" * 64,
                    compiled_cache_file_count=1,
                    compiled_cache_bytes=1,
                )
            finally:
                os.chdir(old)
            argv = captured["argv"]
            self.assertRegex(argv[0], r"^/proc/self/fd/[0-9]+$")
            self.assertEqual(argv[1], "env")
            self.assertRegex(argv[2], r"^/proc/self/fd/[0-9]+$")
            self.assertEqual(argv[3], "--trust=0")
            self.assertEqual(result["declaration_axioms"], {"localProof": []})
            self.assertEqual(
                result["declaration_type_sha256s"]["localProof"],
                hashlib.sha256(b"True").hexdigest(),
            )
            self.assertEqual(result["network_policy"], "denied")
            self.assertEqual(result["repository_access"], "read_only")

    def test_lean_replay_executes_open_bound_inodes_and_rejects_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tool_root = root / "toolchain"
            (tool_root / "bin").mkdir(parents=True)
            lean = tool_root / "bin" / "lean"
            lake = tool_root / "bin" / "lake"
            for executable, payload in ((lean, b"lean-v1"), (lake, b"lake-v1")):
                executable.write_bytes(payload)
                executable.chmod(0o700)

            captured: dict[str, object] = {}

            def runner(argv: list[str], **kwargs: object) -> subprocess.CompletedProcess[bytes]:
                captured["argv"] = argv
                captured["pass_fds"] = kwargs.get("pass_fds")
                # Replace the pathname after admission. The open descriptor must
                # continue to name the original inode, while the postcondition
                # rejects the path substitution as an authority change.
                replacement = tool_root / "bin" / "lean.new"
                replacement.write_bytes(b"lean-v2")
                replacement.chmod(0o700)
                replacement.replace(lean)
                return subprocess.CompletedProcess(argv, 0, stdout=b"", stderr=b"")

            with self.assertRaisesRegex(
                validator.ValidationError, "Lean executable changed during replay"
            ):
                validator._run_bound_toolchain_command(
                    runner,
                    tool_root,
                    ["--version"],
                    expected_lean_sha256=hashlib.sha256(b"lean-v1").hexdigest(),
                    expected_lake_sha256=hashlib.sha256(b"lake-v1").hexdigest(),
                )
            argv = captured["argv"]
            pass_fds = captured["pass_fds"]
            self.assertRegex(argv[0], r"^/proc/self/fd/[0-9]+$")
            self.assertRegex(argv[2], r"^/proc/self/fd/[0-9]+$")
            self.assertEqual(len(pass_fds), 2)

    def test_lean_replay_rejects_compile_failure_or_unpermitted_axiom(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / validator.LEAN_PROJECT
            source = root / "Stage1_Instances" / "THM-M-0001" / "Proof.lean"
            source.parent.mkdir(parents=True)
            project.mkdir(parents=True)
            source.write_text("theorem localProof : True := by trivial\n")
            (project / "lean-toolchain").write_text("leanprover/lean4:v4.29.0\n")
            (project / "lake-manifest.json").write_text('{"packages":[]}\n')
            (project / "lakefile.lean").write_text(
                "import Lake\nopen Lake DSL\npackage fixture where\n"
            )
            tool_root = root / "toolchain"
            cache = root / "cache"
            (tool_root / "bin").mkdir(parents=True)
            (cache / "packages").mkdir(parents=True)
            (cache / "build").mkdir()
            for name in ("lean", "lake"):
                executable = tool_root / "bin" / name
                executable.write_bytes(name.encode())
                executable.chmod(0o700)

            def completed(code: int, stdout: bytes, stderr: bytes = b""):
                return lambda argv, **kwargs: subprocess.CompletedProcess(
                    argv, code, stdout=stdout, stderr=stderr
                )

            old = os.getcwd()
            os.chdir(root)
            try:
                with self.assertRaisesRegex(validator.ValidationError, "failed to compile"):
                    validator.readonly_lean_replay(
                        Path("Stage1_Instances/THM-M-0001/Proof.lean"),
                        ["localProof"],
                        command_runner=completed(1, b"", b"type mismatch"),
                        tool_root=tool_root,
                        cache=cache,
                        scratch_root=root,
                        dependency_packages_sha256="3" * 64,
                        compiled_cache_sha256="4" * 64,
                        compiled_cache_file_count=1,
                        compiled_cache_bytes=1,
                    )
                with self.assertRaisesRegex(validator.ValidationError, "unpermitted axioms"):
                    validator.readonly_lean_replay(
                        Path("Stage1_Instances/THM-M-0001/Proof.lean"),
                        ["localProof"],
                        command_runner=completed(
                            0,
                            b"STAGE1_PROBE_BEGIN {\"axioms\":[\"workerAxiom\"],\"declaration\":\"localProof\",\"index\":0,\"schema\":\"stage1-lean-probe-row/1.0\",\"type\":\"True\"} STAGE1_PROBE_END\n",
                        ),
                        tool_root=tool_root,
                        cache=cache,
                        scratch_root=root,
                        dependency_packages_sha256="3" * 64,
                        compiled_cache_sha256="4" * 64,
                        compiled_cache_file_count=1,
                        compiled_cache_bytes=1,
                    )
            finally:
                os.chdir(old)

    def test_external_exact_source_cannot_be_reproved_independently(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw, _ = self.fixture(root)
            packet = json.loads(raw)
            owner = root / "Stage1_Instances" / "THM-M-0001"
            source_path = owner / "Proof.lean"
            source_path.write_text("theorem localProof : True := by trivial\n")
            receipt_path = owner / "intake-receipt.json"
            receipt = json.loads(receipt_path.read_text())
            receipt.update(
                item_id="S56-M-0001-PROOF",
                phase="proof",
                intent="integrate",
                canonical_target="localProof",
                exact_declarations=["localProof"],
                closed_obligation_ids=["root"],
                proof_body={"source": source_path.relative_to(root).as_posix()},
                result={"exit_code": 0, "axioms": []},
            )
            focus_source = {
                "formal_system": "Lean 4",
                "repository": "https://example.invalid/proofs",
                "revision": "a" * 40,
                "tree_or_archive_sha256": "1" * 64,
                "file_path": "Proof.lean",
                "file_sha256": "2" * 64,
                "module": "External.Proof",
                "declaration": "External.Proof.externalProof",
                "declaration_type_sha256": hashlib.sha256(b"True").hexdigest(),
                "match_kind": "exact",
                "transport_evidence": [],
                "terminal_proof_body": {
                    "locator": "External.Proof.externalProof",
                    "kind": "theorem",
                    "sha256": "3" * 64,
                },
            }
            packet["focus_execution"] = {
                "focus_contract_sha256": "e" * 64,
                "execution_disposition": "organize_or_integrate",
                "machine_evidence_class": "exact_external_unintegrated",
                "receipt_sha256": "f" * 64,
                "exact_machine_source": focus_source,
                "exact_machine_source_used": True,
                "introduced_root_critical_proof": False,
            }
            packet["focus_contract_sha256"] = hashlib.sha256(
                canonical(packet["focus_execution"])
            ).hexdigest()
            receipt["focus_execution"] = packet["focus_execution"]
            receipt["obligation_bindings"] = {"root": "localProof"}
            receipt["proof_body"]["source_sha256"] = hashlib.sha256(
                source_path.read_bytes()
            ).hexdigest()
            source_sha = hashlib.sha256(source_path.read_bytes()).hexdigest()
            receipt["integration_source_evidence"] = {
                "exact_machine_source": focus_source,
                "exact_machine_source_used": True,
                "introduced_root_critical_proof": False,
                "local_proof_source": {
                    "path": source_path.relative_to(root).as_posix(),
                    "sha256": source_sha,
                },
            }
            receipt_path.write_text(json.dumps(receipt))
            contract_path = root / validator.CONTRACT_PATH
            contract = json.loads(contract_path.read_text())
            contract["phases"][0].update(
                phase="proof",
                intent={
                    "organize_or_integrate": "integrate",
                    "frontier_exception": "frontier_prove",
                },
                worker_verdicts_eligible_for_review=["accepted"],
                phase_receipt_required_fields=[
                    "/schema_version", "/canonical_target", "/exact_declarations",
                    "/closed_obligation_ids", "/proof_body", "/result/exit_code",
                ],
                required_artifact_roles=[
                    {"role": "proof_sources", "requirement": "required", "cardinality": "one_or_more"},
                    {"role": "phase_receipt", "requirement": "required", "cardinality": "exactly_one"},
                ],
            )
            contract_path.write_text(json.dumps(contract))
            artifacts = [
                {
                    "role": "proof_sources",
                    "path": source_path.relative_to(root).as_posix(),
                    "sha256": source_sha,
                    "git_blob": "d" * 40,
                },
                {
                    "role": "phase_receipt",
                    "path": receipt_path.relative_to(root).as_posix(),
                    "sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
                    "git_blob": "d" * 40,
                },
            ]
            packet.update(
                item_id="S56-M-0001-PROOF",
                phase="proof",
                contract={
                    "path": validator.CONTRACT_PATH,
                    "sha256": hashlib.sha256(contract_path.read_bytes()).hexdigest(),
                    "git_blob": "1" * 40,
                },
            )
            packet["role_map"].update(
                item_id="S56-M-0001-PROOF", phase="proof", artifacts=artifacts
            )
            packet["role_map"].pop("manifest_sha256")
            packet["role_map"]["manifest_sha256"] = hashlib.sha256(
                canonical(packet["role_map"])
            ).hexdigest()
            packet.pop("input_sha256")
            packet["input_sha256"] = hashlib.sha256(canonical(packet)).hexdigest()
            binary_bytes = {
                Path("/stage1-toolchain/bin/lean"): b"lean-binary",
                Path("/stage1-toolchain/bin/lake"): b"lake-binary",
            }
            packet["lean_authority"]["lean_binary_sha256"] = hashlib.sha256(
                binary_bytes[Path("/stage1-toolchain/bin/lean")]
            ).hexdigest()
            packet["lean_authority"]["lake_binary_sha256"] = hashlib.sha256(
                binary_bytes[Path("/stage1-toolchain/bin/lake")]
            ).hexdigest()
            packet["input_sha256"] = hashlib.sha256(
                canonical({key: value for key, value in packet.items() if key != "input_sha256"})
            ).hexdigest()
            real_exact_file = validator.exact_file

            def exact_file(path: Path, label: str) -> bytes:
                return binary_bytes[path] if path in binary_bytes else real_exact_file(path, label)

            old = os.getcwd()
            os.chdir(root)
            try:
                with (
                    mock.patch.object(validator, "exact_file", side_effect=exact_file),
                    mock.patch.object(
                        validator,
                        "readonly_lean_replay",
                        side_effect=validator.ValidationError("Lean authority replay failed"),
                    ) as replay,
                    self.assertRaisesRegex(
                        validator.ValidationError,
                        "must vendor the admitted terminal body",
                    ),
                ):
                    validator.validate(canonical(packet))
                replay.assert_not_called()
            finally:
                os.chdir(old)

    def checked_transport_fixture(
        self, root: Path, *, include_validation_receipt: bool = True
    ) -> tuple[
        dict[str, object], list[dict[str, str]], dict[str, bytes],
        dict[str, object], dict[str, object], Path,
    ]:
        provider_id = "THM-M-0002"
        consumer_id = "THM-M-0001"
        provider_path = root / "Stage1_Instances/THM-M-0002/Provider.lean"
        consumer_path = root / "Stage1_Instances/THM-M-0001/Transport.lean"
        provider_path.parent.mkdir(parents=True)
        consumer_path.parent.mkdir(parents=True)
        provider_path.write_text(
            "namespace Provider\n"
            "theorem proof : True ∧ True := by exact ⟨trivial, trivial⟩\n"
            "end Provider\n"
        )
        consumer_path.write_text(
            "import Provider\n"
            "namespace Consumer\n"
            "theorem wrapper : True := Provider.proof.1\n"
            "end Consumer\n"
        )
        provider_fingerprint = hashlib.sha256("True ∧ True".encode()).hexdigest()
        consumer_fingerprint = hashlib.sha256(b"True").hexdigest()
        provider_relative = provider_path.relative_to(root).as_posix()
        consumer_relative = consumer_path.relative_to(root).as_posix()
        provider_sha = hashlib.sha256(provider_path.read_bytes()).hexdigest()
        consumer_sha = hashlib.sha256(consumer_path.read_bytes()).hexdigest()

        def receipt(
            theorem_id: str, phase: str, receipt_id: str, result: dict[str, object]
        ) -> dict[str, object]:
            return {
                "schema_version": "stage1-node-receipt/1.0",
                "receipt_id": receipt_id,
                "item_id": f"S56-{theorem_id.removeprefix('THM-')}-{phase.upper()}",
                "theorem_id": theorem_id,
                "phase": phase,
                "intent": "integrate" if phase == "proof" else "validate",
                "base_revision": "a" * 40,
                "base_tree": "b" * 40,
                "inputs": {"fixture_sha256": "c" * 64},
                "support_state": "provisional_worker_selftest",
                "proposed_state": "[_]",
                "accepted": False,
                "verdict": "accepted",
                "selftest_status": "passed",
                "selftest_result": {
                    "exit_code": 0,
                    "commands": [{"argv": ["/usr/bin/true"], "exit_code": 0}],
                },
                "known_failures": [],
                "first_failed_gate": None,
                "retry_condition": None,
                "status_boundary": "Positive fixture phase evidence only.",
                "audit_complete": False,
                "theorem_complete": False,
                "invalidation_inputs": [],
                "result": result,
            }

        provider_receipt_path = provider_path.with_name("proof-receipt.json")
        provider_receipt = receipt(
            provider_id,
            "proof",
            "provider-proof-receipt",
            {
                "exit_code": 0,
                "axioms": [],
                "declaration_type_sha256s": {
                    "Provider.proof": provider_fingerprint,
                },
            },
        )
        provider_receipt.update(
            exact_declarations=["Provider.proof"],
            proof_body={"source": provider_relative, "source_sha256": provider_sha},
        )
        provider_receipt_path.write_text(json.dumps(provider_receipt))

        validation_receipt_path = consumer_path.with_name("validation-receipt.json")
        validation_receipt = receipt(
            consumer_id,
            "validation",
            "consumer-validation-receipt",
            {
                "exit_code": 0,
                "semantic_verdict": "passed",
                "kernel_replay": {
                    "source": consumer_relative,
                    "declarations": ["Consumer.wrapper"],
                    "declaration_type_sha256s": {
                        "Consumer.wrapper": consumer_fingerprint,
                    },
                },
            },
        )
        validation_receipt_path.write_text(json.dumps(validation_receipt))

        replay = {
            "toolchain": "leanprover/lean4:v4.29.0",
            "toolchain_file_sha256": "1" * 64,
            "dependency_lock_sha256": "2" * 64,
            "dependency_packages_sha256": "7" * 64,
            "toolchain_closure_sha256": "9" * 64,
            "toolchain_closure_file_count": 1,
            "toolchain_closure_bytes": 1,
            "compiled_cache_sha256": "8" * 64,
            "compiled_cache_file_count": 1,
            "compiled_cache_bytes": 1,
            "lean_binary_sha256": "3" * 64,
            "lake_binary_sha256": "4" * 64,
            "source_path": consumer_relative,
            "source_sha256": consumer_sha,
            "declaration_type_sha256s": {
                "Consumer.wrapper": consumer_fingerprint,
            },
            "declaration_axioms": {"Consumer.wrapper": []},
            "provider_dependency": {
                "schema": validator.DEPENDENCY_PROBE_SCHEMA,
                "consumer": "Consumer.wrapper",
                "provider": "Provider.proof",
                "provider_module": "Provider",
                "relation": "direct_proof_body_constant_dependency",
            },
            "network_policy": "denied",
            "repository_access": "read_only",
            "trust_level": 0,
        }
        authority = {
            key: replay[key]
            for key in (
                "toolchain", "toolchain_file_sha256", "dependency_lock_sha256",
                "dependency_packages_sha256", "lean_binary_sha256",
                "lake_binary_sha256", "toolchain_closure_sha256",
                "toolchain_closure_file_count", "toolchain_closure_bytes",
                "compiled_cache_sha256",
                "compiled_cache_file_count", "compiled_cache_bytes",
            )
        }
        context_digest = "d" * 64
        provider_reference = {
            "path": provider_receipt_path.relative_to(root).as_posix(),
            "receipt_id": "provider-proof-receipt",
            "sha256": hashlib.sha256(provider_receipt_path.read_bytes()).hexdigest(),
        }
        validation_reference = {
            "path": validation_receipt_path.relative_to(root).as_posix(),
            "receipt_id": "consumer-validation-receipt",
            "sha256": hashlib.sha256(validation_receipt_path.read_bytes()).hexdigest(),
        }
        decision: dict[str, object] = {
            "source_id": "EDGE-1",
            "consumer_obligation_id": "CONSUMER-ROOT",
            "provider_theorem_id": provider_id,
            "provider_obligation_id": "PROVIDER-ROOT",
            "terminal_proof_body_id": "Provider.proof",
            "provider_body_source": {
                "path": provider_relative,
                "sha256": provider_sha,
            },
            "provider_statement_fingerprint": provider_fingerprint,
            "consumer_required_fingerprint": consumer_fingerprint,
            "provider_proof_state": "[_]",
            "provider_receipts": [provider_reference],
            "decision": "reused_with_transport",
            "relationship": "checked_transport",
            "consumer_import_source": {
                "path": consumer_relative,
                "sha256": consumer_sha,
            },
            "consumer_import_or_wrapper": "Consumer.wrapper",
            "provider_import_module": "Provider",
            "context_digest": context_digest,
        }
        if include_validation_receipt:
            decision["consumer_validation_receipts"] = [validation_reference]
        ledger = {
            "schema_version": "stage1-dependency-reuse-ledger/1.1",
            "consumer_theorem_id": consumer_id,
            "dependency_context_sha256": context_digest,
            "inspections": [{
                "theorem_id": provider_id,
                "phase_states": {
                    phase: ("[_]" if phase == "proof" else "[ ]")
                    for phase in validator.PHASES
                },
                "artifact_digests": {provider_relative: provider_sha},
                "compatibility": "checked_transport",
            }],
            "reuse_decisions": [decision],
            "unresolved_compatibility_obligations": [],
        }
        artifacts = [
            {"role": "provider_material", "path": provider_relative, "sha256": provider_sha},
            {
                "role": "provider_material",
                "path": provider_receipt_path.relative_to(root).as_posix(),
                "sha256": provider_reference["sha256"],
            },
            {"role": "proof_sources", "path": consumer_relative, "sha256": consumer_sha},
        ]
        bound_sources = {consumer_relative: consumer_path.read_bytes()}
        return (
            ledger, artifacts, bound_sources, authority, replay,
            validation_receipt_path,
        )

    def test_checked_transport_replays_complete_positive_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger, artifacts, bound_sources, authority, replay, _ = (
                self.checked_transport_fixture(root)
            )
            old = os.getcwd()
            os.chdir(root)
            try:
                with mock.patch.object(
                    validator, "readonly_lean_replay", return_value=replay
                ) as kernel:
                    result = validator.replay_checked_transports(
                        ledger,
                        theorem_id="THM-M-0001",
                        artifacts=artifacts,
                        lean_authority=authority,
                        bound_sources=bound_sources,
                    )
                self.assertEqual(result[0]["consumer_wrapper"], "Consumer.wrapper")
                self.assertEqual(result[0]["consumer_validation_receipt_count"], 1)
                kernel.assert_called_once_with(
                    Path("Stage1_Instances/THM-M-0001/Transport.lean"),
                    ["Consumer.wrapper"],
                    dependency_packages_sha256="7" * 64,
                    toolchain_closure_sha256="9" * 64,
                    toolchain_closure_file_count=1,
                    toolchain_closure_bytes=1,
                    compiled_cache_sha256="8" * 64,
                    compiled_cache_file_count=1,
                    compiled_cache_bytes=1,
                    bound_sources=bound_sources,
                    dependency_probe=(
                        "Consumer.wrapper", "Provider.proof", "Provider"
                    ),
                    imported_provider=(
                        "Provider",
                        "Provider.proof",
                        "stage1-local://THM-M-0002",
                        "0" * 40,
                    ),
                    bound_provider_source=(
                        "Stage1_Instances/THM-M-0002/Provider.lean",
                        (
                            root
                            / "Stage1_Instances/THM-M-0002/Provider.lean"
                        ).read_bytes(),
                    ),
                )
            finally:
                os.chdir(old)

    def test_checked_transport_proof_does_not_invent_future_validation_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger, artifacts, bound_sources, authority, replay, _ = (
                self.checked_transport_fixture(root, include_validation_receipt=False)
            )
            old = os.getcwd()
            os.chdir(root)
            try:
                with mock.patch.object(
                    validator, "readonly_lean_replay", return_value=replay
                ):
                    result = validator.replay_checked_transports(
                        ledger,
                        theorem_id="THM-M-0001",
                        artifacts=artifacts,
                        lean_authority=authority,
                        bound_sources=bound_sources,
                    )
                self.assertEqual(result[0]["consumer_validation_receipt_count"], 0)
            finally:
                os.chdir(old)

    def test_checked_transport_attacks_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger, artifacts, bound_sources, authority, replay, validation_path = (
                self.checked_transport_fixture(root)
            )

            def decision(value: dict[str, object]) -> dict[str, object]:
                rows = value["reuse_decisions"]
                assert isinstance(rows, list) and isinstance(rows[0], dict)
                return rows[0]

            mutations = {
                "decision schema": lambda value, rows: decision(value).update(extra="forged"),
                "consumer owner": lambda value, rows: decision(value)["consumer_import_source"].update(  # type: ignore[union-attr]
                    path="Stage1_Instances/THM-M-0002/Transport.lean"
                ),
                "consumer digest": lambda value, rows: decision(value)["consumer_import_source"].update(  # type: ignore[union-attr]
                    sha256="0" * 64
                ),
                "fingerprint": lambda value, rows: decision(value).update(
                    consumer_required_fingerprint=decision(value)["provider_statement_fingerprint"]
                ),
                "relationship": lambda value, rows: decision(value).update(relationship="exact"),
                "compatibility": lambda value, rows: value["inspections"][0].update(  # type: ignore[index,union-attr]
                    compatibility="exact"
                ),
                "wrapper declaration": lambda value, rows: decision(value).update(
                    consumer_import_or_wrapper="Consumer.fabricated"
                ),
                "provider import module": lambda value, rows: decision(value).update(
                    provider_import_module="Provider.Fabricated"
                ),
                "provider artifact": lambda value, rows: rows.__setitem__(
                    0, {**rows[0], "role": "proof_sources"}
                ),
                "provider receipt": lambda value, rows: decision(value).update(
                    provider_receipts=[]
                ),
                "unresolved transport": lambda value, rows: value.update(
                    unresolved_compatibility_obligations=["EDGE-1"]
                ),
            }
            old = os.getcwd()
            os.chdir(root)
            try:
                for label, mutate in mutations.items():
                    with self.subTest(label=label):
                        attacked = copy.deepcopy(ledger)
                        attacked_artifacts = copy.deepcopy(artifacts)
                        mutate(attacked, attacked_artifacts)
                        with (
                            mock.patch.object(
                                validator, "readonly_lean_replay", return_value=replay
                            ),
                            self.assertRaises(validator.ValidationError),
                        ):
                            validator.replay_checked_transports(
                                attacked,
                                theorem_id="THM-M-0001",
                                artifacts=attacked_artifacts,
                                lean_authority=authority,
                                bound_sources=bound_sources,
                            )

                original_validation = validation_path.read_bytes()
                malformed = json.loads(original_validation)
                malformed["result"].pop("kernel_replay")
                validation_path.write_text(json.dumps(malformed))
                attacked = copy.deepcopy(ledger)
                reference = decision(attacked)["consumer_validation_receipts"][0]  # type: ignore[index]
                reference["sha256"] = hashlib.sha256(validation_path.read_bytes()).hexdigest()
                with (
                    mock.patch.object(
                        validator, "readonly_lean_replay", return_value=replay
                    ),
                    self.assertRaisesRegex(validator.ValidationError, "validation receipt"),
                ):
                    validator.replay_checked_transports(
                        attacked,
                        theorem_id="THM-M-0001",
                        artifacts=artifacts,
                        lean_authority=authority,
                        bound_sources=bound_sources,
                    )
                validation_path.write_bytes(original_validation)

                attacked_replay = copy.deepcopy(replay)
                attacked_replay["declaration_type_sha256s"] = {
                    "Consumer.wrapper": "0" * 64
                }
                with (
                    mock.patch.object(
                        validator, "readonly_lean_replay", return_value=attacked_replay
                    ),
                    self.assertRaisesRegex(validator.ValidationError, "Lean replay"),
                ):
                    validator.replay_checked_transports(
                        ledger,
                        theorem_id="THM-M-0001",
                        artifacts=artifacts,
                        lean_authority=authority,
                        bound_sources=bound_sources,
                    )

                independent_replay = copy.deepcopy(replay)
                independent_replay.pop("provider_dependency")
                with (
                    mock.patch.object(
                        validator,
                        "readonly_lean_replay",
                        return_value=independent_replay,
                    ),
                    self.assertRaisesRegex(
                        validator.ValidationError, "Lean replay"
                    ),
                ):
                    validator.replay_checked_transports(
                        ledger,
                        theorem_id="THM-M-0001",
                        artifacts=artifacts,
                        lean_authority=authority,
                        bound_sources=bound_sources,
                    )
            finally:
                os.chdir(old)

    def test_checked_transport_propagates_kernel_replay_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger, artifacts, bound_sources, authority, _, _ = (
                self.checked_transport_fixture(root)
            )
            old = os.getcwd()
            os.chdir(root)
            try:
                with (
                    mock.patch.object(
                        validator,
                        "readonly_lean_replay",
                        side_effect=validator.ValidationError("Lean authority replay failed"),
                    ) as kernel,
                    self.assertRaisesRegex(validator.ValidationError, "replay failed"),
                ):
                    validator.replay_checked_transports(
                        ledger,
                        theorem_id="THM-M-0001",
                        artifacts=artifacts,
                        lean_authority=authority,
                        bound_sources=bound_sources,
                    )
                kernel.assert_called_once()
            finally:
                os.chdir(old)

    def test_bound_provider_source_identity_is_owner_scoped_and_exact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / validator.LEAN_PROJECT
            source = root / "Stage1_Instances/THM-M-0001/Transport.lean"
            source.parent.mkdir(parents=True)
            project.mkdir(parents=True)
            source.write_text(
                "import Provider\nnamespace Consumer\n"
                "theorem wrapper : True := Provider.proof\nend Consumer\n"
            )
            (project / "lean-toolchain").write_text(
                "leanprover/lean4:v4.29.0\n"
            )
            (project / "lake-manifest.json").write_text('{"packages":[]}\n')
            (project / "lakefile.lean").write_text(
                "import Lake\nopen Lake DSL\npackage fixture where\n"
            )
            tool_root = root / "toolchain"
            cache = root / "cache"
            (tool_root / "bin").mkdir(parents=True)
            (cache / "packages").mkdir(parents=True)
            (cache / "build").mkdir()
            for name in ("lean", "lake"):
                executable = tool_root / "bin" / name
                executable.write_bytes(name.encode())
                executable.chmod(0o700)
            old = os.getcwd()
            os.chdir(root)
            try:
                for label, provider_source in (
                    (
                        "same owner",
                        (
                            "Stage1_Instances/THM-M-0001/Provider.lean",
                            b"theorem proof : True := by trivial\n",
                        ),
                    ),
                    (
                        "escape",
                        (
                            "Stage1_Instances/THM-M-0002/../Provider.lean",
                            b"theorem proof : True := by trivial\n",
                        ),
                    ),
                    (
                        "module mismatch",
                        (
                            "Stage1_Instances/THM-M-0002/Nested/Provider.lean",
                            b"namespace Provider\ntheorem proof : True := by trivial\nend Provider\n",
                        ),
                    ),
                ):
                    with (
                        self.subTest(label=label),
                        self.assertRaises(validator.ValidationError),
                    ):
                        validator.readonly_lean_replay(
                            Path("Stage1_Instances/THM-M-0001/Transport.lean"),
                            ["Consumer.wrapper"],
                            tool_root=tool_root,
                            cache=cache,
                            scratch_root=root,
                            dependency_packages_sha256="3" * 64,
                            compiled_cache_sha256="4" * 64,
                            compiled_cache_file_count=1,
                            compiled_cache_bytes=1,
                            dependency_probe=(
                                "Consumer.wrapper", "Provider.proof", "Provider"
                            ),
                            imported_provider=(
                                "Provider", "Provider.proof",
                                "stage1-local://THM-M-0002", "0" * 40,
                            ),
                            bound_provider_source=provider_source,
                        )
            finally:
                os.chdir(old)

    @unittest.skipUnless(
        (Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean").is_file()
        and (PATH.parents[2] / "Formalizations/Lean/.lake").is_dir()
        and Path("/usr/bin/bwrap").is_file(),
        "pinned Stage1 Lean authority is not installed",
    )
    def test_real_pinned_toolchain_and_cache_compile_local_wrapper(self) -> None:
        root = PATH.parents[2]
        tool_root = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0"
        cache = root / "Formalizations/Lean/.lake"
        owner = root / "Stage1_Instances/THM-M-0001"
        owner.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=owner, prefix="ValidatorReplay") as raw:
            source = Path(raw) / "Proof.lean"
            source.write_text(
                "import AwesomeTheorems.Stage1.S1_M_001\n"
                "namespace Stage1ValidatorFixture\n"
                "theorem localWrapper : True := by trivial\n"
                "end Stage1ValidatorFixture\n"
            )
            relative = source.relative_to(root)
            old = os.getcwd()
            os.chdir(root)
            try:
                result = validator.readonly_lean_replay(
                    relative,
                    ["Stage1ValidatorFixture.localWrapper"],
                    tool_root=tool_root,
                    cache=cache,
                    scratch_root=owner,
                    dependency_packages_sha256="3" * 64,
                    compiled_cache_sha256="4" * 64,
                    compiled_cache_file_count=1,
                    compiled_cache_bytes=1,
                )
            finally:
                os.chdir(old)
        self.assertEqual(
            result["declaration_axioms"],
            {"Stage1ValidatorFixture.localWrapper": []},
        )
        self.assertEqual(result["toolchain"], "leanprover/lean4:v4.29.0")
        self.assertEqual(result["network_policy"], "denied")
        self.assertEqual(result["repository_access"], "read_only")
        self.assertEqual(result["trust_level"], 0)

    @unittest.skipUnless(
        (Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean").is_file()
        and (PATH.parents[2] / "Formalizations/Lean/.lake").is_dir(),
        "pinned Stage1 Lean authority is not installed",
    )
    def test_real_replay_compiles_only_bound_sibling_import_closure(self) -> None:
        root = PATH.parents[2]
        tool_root = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0"
        cache = root / "Formalizations/Lean/.lake"
        owner = root / "Stage1_Instances/THM-M-0001"
        with tempfile.TemporaryDirectory(dir=owner, prefix="ValidatorSiblings") as raw:
            directory = Path(raw)
            statement = directory / "Statement.lean"
            proof = directory / "Proof.lean"
            statement.write_text(
                "namespace SiblingFixture\ndef Target : Prop := True\nend SiblingFixture\n"
            )
            proof.write_text(
                "import Statement\nnamespace SiblingFixture\n"
                "theorem wrapper : Target := by trivial\nend SiblingFixture\n"
            )
            relative_statement = statement.relative_to(root).as_posix()
            relative_proof = proof.relative_to(root).as_posix()
            bound = {
                relative_statement: statement.read_bytes(),
                relative_proof: proof.read_bytes(),
            }
            old = os.getcwd()
            os.chdir(root)
            try:
                result = validator.readonly_lean_replay(
                    Path(relative_proof),
                    ["SiblingFixture.wrapper"],
                    tool_root=tool_root,
                    cache=cache,
                    scratch_root=owner,
                    dependency_packages_sha256="3" * 64,
                    compiled_cache_sha256="4" * 64,
                    compiled_cache_file_count=1,
                    compiled_cache_bytes=1,
                    bound_sources=bound,
                )
                with self.assertRaisesRegex(validator.ValidationError, "unbound or unavailable"):
                    validator.readonly_lean_replay(
                        Path(relative_proof),
                        ["SiblingFixture.wrapper"],
                        tool_root=tool_root,
                        cache=cache,
                        scratch_root=owner,
                        dependency_packages_sha256="3" * 64,
                        compiled_cache_sha256="4" * 64,
                        compiled_cache_file_count=1,
                        compiled_cache_bytes=1,
                        bound_sources={relative_proof: proof.read_bytes()},
                    )
            finally:
                os.chdir(old)
        self.assertEqual(result["declaration_axioms"], {"SiblingFixture.wrapper": []})

    @unittest.skipUnless(
        (Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean").is_file()
        and (PATH.parents[2] / "Formalizations/Lean/.lake").is_dir(),
        "pinned Stage1 Lean authority is not installed",
    )
    def test_real_bound_provider_dependency_rejects_independent_reproof(self) -> None:
        root = PATH.parents[2]
        tool_root = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0"
        cache = root / "Formalizations/Lean/.lake"
        provider_owner = root / "Stage1_Instances/THM-M-0002"
        consumer_owner = root / "Stage1_Instances/THM-M-0001"
        provider_owner.mkdir(parents=True, exist_ok=True)
        consumer_owner.mkdir(parents=True, exist_ok=True)
        with (
            tempfile.TemporaryDirectory(dir=provider_owner, prefix="ProviderProbe") as provider_raw,
            tempfile.TemporaryDirectory(dir=consumer_owner, prefix="ConsumerProbe") as consumer_raw,
        ):
            provider = Path(provider_raw) / "Provider.lean"
            consumer = Path(consumer_raw) / "Transport.lean"
            provider.write_text(
                "namespace KernelProvider\n"
                "theorem proof : True := by trivial\n"
                "end KernelProvider\n"
            )
            provider_relative = provider.relative_to(root).as_posix()
            consumer_relative = consumer.relative_to(root)
            provider_module = f"{Path(provider_raw).name}.Provider"
            consumer.write_text(
                f"import {provider_module}\nnamespace KernelConsumer\n"
                "theorem wrapper : True := KernelProvider.proof\n"
                "end KernelConsumer\n"
            )
            kwargs = {
                "tool_root": tool_root,
                "cache": cache,
                "scratch_root": consumer_owner,
                "dependency_packages_sha256": "3" * 64,
                "compiled_cache_sha256": "4" * 64,
                "compiled_cache_file_count": 1,
                "compiled_cache_bytes": 1,
                "dependency_probe": (
                    "KernelConsumer.wrapper", "KernelProvider.proof", provider_module
                ),
                "imported_provider": (
                    provider_module,
                    "KernelProvider.proof",
                    "stage1-local://THM-M-0002",
                    "0" * 40,
                ),
                "bound_provider_source": (
                    provider_relative, provider.read_bytes()
                ),
            }
            old = os.getcwd()
            os.chdir(root)
            try:
                result = validator.readonly_lean_replay(
                    consumer_relative,
                    ["KernelConsumer.wrapper"],
                    **kwargs,
                )
                consumer.write_text(
                    f"import {provider_module}\nnamespace KernelConsumer\n"
                    "theorem wrapper : True := by trivial\n"
                    "end KernelConsumer\n"
                )
                with self.assertRaisesRegex(
                    validator.ValidationError,
                    "does not depend on the admitted provider",
                ):
                    validator.readonly_lean_replay(
                        consumer_relative,
                        ["KernelConsumer.wrapper"],
                        **kwargs,
                    )
            finally:
                os.chdir(old)
        self.assertEqual(
            result["provider_dependency"]["provider"], "KernelProvider.proof"
        )


if __name__ == "__main__":
    unittest.main()
