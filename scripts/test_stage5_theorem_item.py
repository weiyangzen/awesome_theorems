#!/usr/bin/env python3
"""Semantic-substitution tests for the complete theorem TARGET validator."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts/check_stage5_theorem_item.py"


def load():
    spec = importlib.util.spec_from_file_location("stage5_theorem_target_test_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = load()


class Stage5TheoremItemTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="stage5-theorem-target-test-")
        self.addCleanup(self.temporary.cleanup)
        self.task = Path(self.temporary.name)
        self.work = self.task / "work"
        self.work.mkdir()
        source_workset = ROOT / "Docs/evidence/stage5_theorems/workset-5.6.json"
        baseline = self.work / "_baseline"
        baseline.mkdir()
        shutil.copyfile(source_workset, baseline / source_workset.name)
        shutil.copyfile(
            ROOT / "Docs/evidence/stage5_theorems/provider-registry.json",
            baseline / "provider-registry.json",
        )
        workset = json.loads(source_workset.read_text())
        self.member = next(
            row for row in workset["members"]
            if row["stage_claim_id"] == "S5-CLM-00003514"
        )
        self.item_id = self.member["target_item_id"]
        self.stage_claim_id = self.member["stage_claim_id"]
        dossier = f"Stage5_Theorem_Instances/{self.stage_claim_id}"
        lean = "Formalizations/Lean/AwesomeTheorems/Stage5/Theorems/S5_CLM_00003514"
        self.writable = [
            f"{dossier}/intake.json", f"{lean}/Statement.lean",
            f"{dossier}/statement-crosswalk.json", f"{dossier}/anchor-audit.json",
            f"{dossier}/proof-units.json", f"{dossier}/process-audit.md",
            f"{lean}/Proof.lean", f"{dossier}/machine-closure.json",
            f"{dossier}/machine-checked-audit.md", f"{dossier}/proof-outline.md",
            f"{dossier}/full-study.md", f"{dossier}/readability-review.json",
            f"{lean}/Audit.lean", f"{dossier}/build-validation.md",
            f"{dossier}/receipts/current-validation.json", f"{dossier}/README.md",
            f"{dossier}/meta.json", f"{dossier}/receipts/release-decision.json",
        ]
        for relative in self.writable:
            path = self.work / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("evidence\n")
        self.lean_paths = [self.work / path for path in self.writable if path.endswith(".lean")]
        module = validator.lean_module_spelling(self.member["module"])
        qualified = self.member["formal_statement"]["qualified_declaration"]
        for path in self.lean_paths:
            path.write_text(
                f"import {module}\n"
                f"#check {qualified}\n"
                "namespace Fixture\ntheorem root : True := trivial\nend Fixture\n"
            )
        self.path_named("Audit.lean").write_text(
            f"import {module}\nnamespace Fixture\n"
            f"#check {qualified}\n"
            "theorem root : True := trivial\n"
            f"example : type_of% {qualified} := Fixture.root\n"
            "#print axioms Fixture.root\nend Fixture\n"
        )
        self.claim = {
            "program": validator.PROGRAM, "item_id": self.item_id,
            "task_root": str(self.task), "canonical_repository_root": str(ROOT),
            "writable_paths": self.writable,
        }
        locator = self.member["source_locator"]
        formal = self.member["formal_statement"]
        constants = [
            {
                "name": name, "declaration_kind": "def",
                "provider_id": self.member["provider_id"],
                "provider_revision": locator["revision"],
                "source_path": f"Provider/{name}.lean", "source_sha256": digit * 64,
                "type_sha256": chr(ord(digit) + 1) * 64,
                "body_sha256": chr(ord(digit) + 2) * 64,
            }
            for name, digit in (("Real", "1"), ("Polynomial", "4"), ("FourProp", "7"))
        ]
        for row in constants:
            source = (
                baseline / "provider-sources" / row["provider_id"]
                / row["provider_revision"] / row["source_path"]
            )
            source.parent.mkdir(parents=True, exist_ok=True)
            raw = f"provider declaration {row['name']}\n".encode()
            source.write_bytes(raw)
            row["source_sha256"] = validator.sha(raw)
        self.environment = {
            "provider_id": self.member["provider_id"],
            "provider_revision": locator["revision"],
            "source_module": self.member["module"], "source_path": locator["member_path"],
            "source_file_sha256": locator["file_sha256"],
            "source_declaration_sha256": formal["declaration_sha256"],
            "source_declaration_type_sha256": formal["declaration_type_sha256"],
            "elaborated_source_expr_sha256": "a" * 64,
            "elaborated_target_expr_sha256": "a" * 64,
            "transitive_constants": constants,
            "source_surface_symbols": ["Real", "Polynomial", "FourProp"],
            "local_shadowed_source_symbols": [], "semantic_substitutions": [],
            "bidirectional_transport": {
                "source_to_target_theorem": "source_to_target",
                "target_to_source_theorem": "target_to_source",
                "lean_checked": True, "master_recompute_required": True,
            },
            "recompute_evidence": {
                "audit_declaration": "Fixture.audit", "command_id": "semantic-recompute",
                "trust": 0, "cold_from_source": True, "worker_recomputed": True,
                "master_recompute_required": True,
            },
        }
        route = {
            "schema_version": "awesome-theorems/stage5-provider-kernel-route/1.0",
            "provider_id": self.member["provider_id"],
            "revision": locator["revision"],
            "module": self.member["module"],
            "lean_module": validator.lean_module_spelling(self.member["module"]),
            "qualified_declaration": formal["qualified_declaration"],
            "toolchain": "leanprover/lean4:v4.27.0",
            "master_environment": "Formalizations/Lean/.lake/packages/formal-conjectures",
            "proof_authority": "claim_owned_root_only",
            "provider_body_authority": False,
        }
        self.write_sealed_path(baseline / "provider-kernel-route.json", route)
        self.crosswalk = self.seal({
            "schema_version": "awesome-theorems/stage5-theorem-statement-crosswalk/2.0",
            "program": validator.PROGRAM, "item_id": self.item_id,
            "stage_claim_id": self.stage_claim_id,
            "member_record_sha256": self.member["record_sha256"],
            "source_formal_type_sha256": self.member["formal_type_sha256"],
            "semantic_environment": self.environment,
        })
        self.semantic_sha = validator.sha(validator.canonical(self.environment))
        self.identity = {
            "program": validator.PROGRAM, "item_id": self.item_id,
            "stage_claim_id": self.stage_claim_id,
        }
        self.machine = self.seal({
            "schema_version": "awesome-theorems/stage5-theorem-machine-closure/2.0",
            **self.identity, "semantic_environment_sha256": self.semantic_sha,
            "machine_level": "M0-P", "root_declaration": "Fixture.root",
            "root_expr_sha256": "a" * 64,
            "declaration_census": [{"name": "Fixture.root"}],
            "dependency_edges": [], "observed_axioms": [],
            "remaining_machine_cut_set": [], "trust": 0,
            "cold_from_source_replay": True,
        })
        fragment = {
            "node_id": "root", "path": "full-study.md#root",
            "fragment_sha256": "b" * 64, "hypotheses": ["source hypotheses"],
            "inference": "apply the proved harmonic-mean inequality",
            "output": "the exact frozen root", "formal_anchor": "Fixture.root",
            "downstream_uses": ["release root"], "exceptional_cases": ["none"],
            "trust_boundary": "Lean kernel and pinned providers",
        }
        self.readable = self.seal({
            "schema_version": "awesome-theorems/stage5-theorem-readability/2.0",
            **self.identity, "readability_level": "R0", "required_nodes": ["root"],
            "node_to_anchor": {"root": "root-anchor"},
            "anchor_to_fragment": {"root-anchor": fragment},
            "reviewers": [{"reviewer_id": "r1"}, {"reviewer_id": "r2"}],
            "remaining_readability_cut_set": [],
            "distilled": {
                "duplicate_prose_removed": True,
                "structured_inventory_not_duplicated": True,
                "mathematical_content_preserved": True,
                "deletion_mutations_passed": True,
            },
        })
        self.release = self.seal({
            "schema_version": "awesome-theorems/stage5-theorem-release/2.0",
            **self.identity, "decision": "provisional_release_candidate",
            "semantic_environment_sha256": self.semantic_sha,
            "machine_complete": True, "readable_complete": True,
            "human_cut_set": [], "machine_cut_set": [], "readability_cut_set": [],
            "current_trace_sha256": "c" * 64,
            "strict_dominance": {
                "fixture": "THM-M-0387",
                "fixture_status": "incomplete_H1_M2_R0_negative_fixture",
                "all_applicable_shape_predicates_passed": True, "exact_m0": True,
                "true_r0": True, "empty_hmr_cuts": True,
                "semantic_environment_added": True,
                "semantic_substitution_mutations_passed": True,
                "cold_from_source_replay_passed": True,
                "strict_dimensions": [
                    "semantic_environment", "semantic_substitution_mutations",
                    "cold_from_source_replay",
                ],
            },
            "theorem_complete_candidate": True, "master_accepted": False,
        })
        self.write_json("statement-crosswalk.json", self.crosswalk)
        self.write_json("machine-closure.json", self.machine)
        self.write_json("readability-review.json", self.readable)
        self.write_json("release-decision.json", self.release)

    @staticmethod
    def seal(value: dict) -> dict:
        result = copy.deepcopy(value)
        result["authority_sha256"] = validator.sha(validator.canonical(result))
        return result

    def path_named(self, filename: str) -> Path:
        return next(self.work / path for path in self.writable if Path(path).name == filename)

    def write_json(self, filename: str, value: dict) -> None:
        self.path_named(filename).write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")

    def write_sealed_path(self, path: Path, value: dict) -> None:
        path.write_text(json.dumps(self.seal(value), sort_keys=True, indent=2) + "\n")

    def test_exact_complete_target_contract_is_accepted(self) -> None:
        result = validator.validate_target(self.claim, self.work, ROOT, compile_files=False)
        self.assertEqual(result["semantic_environment_sha256"], self.semantic_sha)

    def test_lean_failure_preserves_stdout_stderr_and_exit_code(self) -> None:
        lean_root = self.task / "canonical/Formalizations/Lean"
        lean_root.mkdir(parents=True)
        (lean_root / "lean-toolchain").write_text("v4.fixture\n")
        elan = self.task / "elan/bin/elan"; elan.parent.mkdir(parents=True)
        elan.write_text("fixture\n"); elan.chmod(0o755)
        artifact = self.path_named("Proof.lean")
        completed = subprocess.CompletedProcess(
            args=[], returncode=7, stdout="stdout elaboration detail\n",
            stderr="stderr elaboration detail\n",
        )
        with (
            mock.patch.dict(validator.os.environ, {"ELAN_HOME": str(self.task / "elan")}),
            mock.patch.object(
                validator.subprocess,
                "Popen",
                return_value=mock.Mock(
                    returncode=completed.returncode,
                    communicate=mock.Mock(return_value=(completed.stdout, completed.stderr)),
                    pid=1234,
                ),
            ),
            self.assertRaisesRegex(
                validator.ItemError,
                r"(?s)exit=7.*stdout elaboration detail.*stderr elaboration detail",
            ),
        ):
            validator.compile_lean(artifact, self.task / "canonical")

    def test_nat_list_true_and_reflexive_semantic_substitutions_are_rejected(self) -> None:
        statement = self.path_named("Statement.lean")
        substitutions = (
            "abbrev ℝ := Nat\n",
            "def Polynomial (R : Type) := List R\n",
            "def FourProp (p q : Nat) (n : Nat) : Prop := True\n",
            "def FourProp (p q : Nat) (n : Nat) : Prop := p = p ∧ q = q ∧ n = n\n",
        )
        for source in substitutions:
            with self.subTest(source=source):
                statement.write_text(
                    f"import {validator.lean_module_spelling(self.member['module'])}\n"
                    f"#check {self.member['formal_statement']['qualified_declaration']}\n"
                    + source
                )
                with self.assertRaisesRegex(validator.ItemError, "semantic shadow/redefinition"):
                    validator.validate_target(self.claim, self.work, ROOT, compile_files=False)

    def test_renamed_local_alias_and_import_substitution_are_rejected(self) -> None:
        statement = self.path_named("Statement.lean")
        statement.write_text(
            f"import {validator.lean_module_spelling(self.member['module'])}\n"
            f"#check {self.member['formal_statement']['qualified_declaration']}\n"
            "def RenamedSourcePredicate : Prop := True\n"
            "theorem renamed_target : RenamedSourcePredicate := trivial\n"
        )
        with self.assertRaisesRegex(validator.ItemError, "local semantic"):
            validator.validate_target(self.claim, self.work, ROOT, compile_files=False)

        statement.write_text("import Mathlib\ntheorem renamed_target : True := trivial\n")
        with self.assertRaisesRegex(validator.ItemError, "exact provider module import"):
            validator.validate_target(self.claim, self.work, ROOT, compile_files=False)

    def test_comment_only_import_reference_and_axiom_query_are_rejected(self) -> None:
        module = validator.lean_module_spelling(self.member["module"])
        qualified = self.member["formal_statement"]["qualified_declaration"]
        audit = self.path_named("Audit.lean")
        audit.write_text(
            f"/- import {module}\n#check {qualified}\n"
            f"example : type_of% {qualified} := {qualified}\n"
            "#print axioms Fixture.root -/\n"
            "import Mathlib\nnamespace Fixture\n"
            "theorem root : True := trivial\nend Fixture\n"
        )
        with self.assertRaisesRegex(validator.ItemError, "exact provider module import"):
            validator.validate_target(self.claim, self.work, ROOT, compile_files=False)

    def test_true_root_without_exact_type_and_axiom_probe_is_rejected(self) -> None:
        module = validator.lean_module_spelling(self.member["module"])
        qualified = self.member["formal_statement"]["qualified_declaration"]
        audit = self.path_named("Audit.lean")
        audit.write_text(
            f"import {module}\n#check {qualified}\n"
            "namespace Fixture\ntheorem root : True := trivial\nend Fixture\n"
        )
        with self.assertRaisesRegex(
            validator.ItemError, "machine root|exact-type transport",
        ):
            validator.validate_target(self.claim, self.work, ROOT, compile_files=False)

    def test_provider_self_check_beside_unrelated_root_is_rejected(self) -> None:
        module = validator.lean_module_spelling(self.member["module"])
        qualified = self.member["formal_statement"]["qualified_declaration"]
        audit = self.path_named("Audit.lean")
        audit.write_text(
            f"import {module}\nnamespace Fixture\n"
            f"example : type_of% {qualified} := {qualified}\n"
            "theorem root : True := trivial\n"
            "#print axioms Fixture.root\nend Fixture\n"
        )
        with self.assertRaisesRegex(validator.ItemError, "exact-type transport"):
            validator.validate_target(self.claim, self.work, ROOT, compile_files=False)

    def test_imported_declaration_cannot_be_claim_owned_machine_root(self) -> None:
        qualified = self.member["formal_statement"]["qualified_declaration"]
        changed = copy.deepcopy(self.machine)
        changed["root_declaration"] = qualified
        changed["declaration_census"] = [{"name": qualified}]
        self.write_json("machine-closure.json", self.seal({
            key: value for key, value in changed.items()
            if key != "authority_sha256"
        }))
        with self.assertRaisesRegex(validator.ItemError, "claim-owned machine root"):
            validator.validate_target(self.claim, self.work, ROOT, compile_files=False)

    def test_custom_or_sorry_axiom_is_rejected(self) -> None:
        for axiom in ("sorryAx", "Fixture.unproved"):
            with self.subTest(axiom=axiom):
                changed = copy.deepcopy(self.machine)
                changed["observed_axioms"] = [axiom]
                self.write_json("machine-closure.json", self.seal({
                    key: value for key, value in changed.items()
                    if key != "authority_sha256"
                }))
                with self.assertRaisesRegex(validator.ItemError, "machine closure"):
                    validator.validate_target(
                        self.claim, self.work, ROOT, compile_files=False,
                    )
        self.write_json("machine-closure.json", self.machine)

    def test_terminal_axiom_report_is_parsed_for_exact_root(self) -> None:
        output = (
            "'Fixture.helper' depends on axioms: [Classical.choice]\n"
            "'Fixture.root' depends on axioms: [propext, Quot.sound]\n"
        )
        self.assertEqual(
            validator.reported_root_axioms(output, "Fixture.root"),
            ["propext", "Quot.sound"],
        )
        with self.assertRaisesRegex(validator.ItemError, "one parseable"):
            validator.reported_root_axioms(output, "Fixture.missing")

    def test_provider_native_kernel_routes_are_revision_and_toolchain_pinned(self) -> None:
        fc_root, fc_toolchain = validator.kernel_route(self.member, ROOT)
        self.assertEqual(
            fc_root,
            ROOT / "Formalizations/Lean/.lake/packages/formal-conjectures",
        )
        self.assertEqual(fc_toolchain, "leanprover/lean4:v4.27.0")
        workset = json.loads(
            (ROOT / "Docs/evidence/stage5_theorems/workset-5.6.json").read_text()
        )
        mathlib = next(
            row for row in workset["members"]
            if row["provider_id"] == "mathlib-8a178386"
        )
        mathlib_root, mathlib_toolchain = validator.kernel_route(mathlib, ROOT)
        self.assertEqual(mathlib_root, ROOT / "Formalizations/Lean")
        self.assertEqual(mathlib_toolchain, "leanprover/lean4:v4.29.0")

        tampered = copy.deepcopy(mathlib)
        tampered["proof_evidence"]["olean_sha256"] = "0" * 64
        with self.assertRaisesRegex(validator.ItemError, "olean digest differs"):
            validator.kernel_route(tampered, ROOT)

    def test_lean_module_spelling_preserves_complete_arxiv_directory_identifier(self) -> None:
        self.assertEqual(
            validator.lean_module_spelling(
                "FormalConjectures.Arxiv.2208.14736.ZariskiCancellation"
            ),
            "FormalConjectures.Arxiv.«2208.14736».ZariskiCancellation",
        )
        self.assertEqual(
            validator.lean_module_spelling(
                "FormalConjectures.Arxiv.math.0110202.BanachMazurRotation"
            ),
            "FormalConjectures.Arxiv.«math.0110202».BanachMazurRotation",
        )

    def test_self_attested_semantics_noninjective_readability_and_nonstrict_release_fail(self) -> None:
        changed = copy.deepcopy(self.crosswalk)
        changed["semantic_environment"]["elaborated_target_expr_sha256"] = "d" * 64
        self.write_json("statement-crosswalk.json", self.seal({
            key: value for key, value in changed.items() if key != "authority_sha256"
        }))
        with self.assertRaisesRegex(validator.ItemError, "elaborated expressions differ"):
            validator.validate_target(self.claim, self.work, ROOT, compile_files=False)
        self.write_json("statement-crosswalk.json", self.crosswalk)

        readable = copy.deepcopy(self.readable)
        readable["required_nodes"] = ["root", "second"]
        readable["node_to_anchor"] = {"root": "root-anchor", "second": "root-anchor"}
        self.write_json("readability-review.json", self.seal({
            key: value for key, value in readable.items() if key != "authority_sha256"
        }))
        with self.assertRaisesRegex(validator.ItemError, "not total, injective R0"):
            validator.validate_target(self.claim, self.work, ROOT, compile_files=False)
        self.write_json("readability-review.json", self.readable)

        release = copy.deepcopy(self.release)
        release["strict_dominance"]["semantic_environment_added"] = False
        self.write_json("release-decision.json", self.seal({
            key: value for key, value in release.items() if key != "authority_sha256"
        }))
        with self.assertRaisesRegex(validator.ItemError, "does not strictly dominate"):
            validator.validate_target(self.claim, self.work, ROOT, compile_files=False)


if __name__ == "__main__":
    unittest.main()
