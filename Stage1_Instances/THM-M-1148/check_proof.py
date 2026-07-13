#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-1148 proof packet."""

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
BASE_REVISION = "0afbf514f9bd5f339943542106f6b811869fe572"
BASE_TREE = "adbd9c80e360931a3e7c51cae73dda809b5bed65"

if not __debug__:
    raise SystemExit("FAIL: Python assertions are disabled")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


unit_source = (ROOT / "PoissonUnitDisk.lean").read_text(encoding="utf-8")
proof_source = (ROOT / "Proof.lean").read_text(encoding="utf-8")
receipt = json.loads((ROOT / "proof-receipt.json").read_text(encoding="utf-8"))

assert subprocess.run(
    ["git", "rev-parse", "HEAD"], cwd=REPO, check=True, capture_output=True, text=True
).stdout.strip() == BASE_REVISION
assert subprocess.run(
    ["git", "rev-parse", "HEAD^{tree}"],
    cwd=REPO,
    check=True,
    capture_output=True,
    text=True,
).stdout.strip() == BASE_TREE

required_unit = {
    "poissonIntegral_eq_re_herglotzIntegral",
    "herglotzIntegral_differentiableOn",
    "poissonIntegral_harmonic",
    "unitDiskExtension_harmonic",
    "unitDiskExtension_eqOn_sphere",
    "unitDiskExtension_continuousOn",
    "unitKernelMass",
    "unitPoissonKernel_nonneg",
    "boundaryData_uniformContinuousOn",
    "continuous_extension_of_sphere",
    "invMobiusAngle_mobiusTransform_core",
    "poissonIntegral_eq_circleAverage_mobiusTransform",
    "mobiusTransform_tendsto_on_circle",
    "circleAverage_mobiusTransform_tendsto",
    "poissonIntegral_tendsto_boundary",
    "bounded_continuous_extension_of_sphere",
    "unitDiskConstruction",
    "harmonicOnNhd_affine_pullback",
    "continuousOn_affine_pullback",
    "eqOn_affine_pullback",
    "generalDiskConstruction",
}
required_proof = {
    "interiorFormula_of_harmonicContOnCl_of_eqOn",
    "dirichletExtension_to_root",
    "rootTarget_to_frozen",
    "dirichletExtension_to_frozen",
    "dirichletExtension",
    "poissonIntegralFormula",
    "unitDiskConstruction_of_boundaryConvergence",
}

expected_declarations = {
    *(f"Stage1Instances.THM_M_1148.PoissonUnitDisk.{name}" for name in required_unit),
    *(f"Stage1Instances.THM_M_1148.Proof.{name}" for name in required_proof),
}

declared_unit = set(re.findall(r"^(?:set_option[^\n]*\n)?(?:noncomputable\s+)?(?:theorem|lemma)\s+([A-Za-z0-9_]+)", unit_source, re.MULTILINE))
declared_proof = set(re.findall(r"^theorem\s+([A-Za-z0-9_]+)", proof_source, re.MULTILINE))
assert required_unit <= declared_unit, f"missing unit-disk declarations: {sorted(required_unit - declared_unit)}"
assert required_proof <= declared_proof, f"missing proof declarations: {sorted(required_proof - declared_proof)}"

prohibited = re.compile(
    r"\b(sorry|admit|sorryAx|native_decide|implemented_by)\b|"
    r"^\s*(axiom|constant|opaque|unsafe|extern)\b",
    re.MULTILINE,
)
assert not prohibited.search(unit_source), "prohibited construct in PoissonUnitDisk.lean"
assert not prohibited.search(proof_source), "prohibited construct in Proof.lean"
assert "hboundary :" in proof_source, "boundary convergence must remain an explicit premise"
assert "DirichletExtension →" in proof_source, "general extension must remain an explicit premise"
assert "theorem dirichletExtension : DirichletExtension" in proof_source
assert "theorem poissonIntegralFormula : PoissonIntegralFormula" in proof_source
assert "import Statement" in proof_source
assert "import PoissonUnitDisk" in proof_source

assert receipt["schema_version"] == "stage1-node-receipt/1.0"
assert receipt["item_id"] == "S56-M-1148-PROOF"
assert receipt["theorem_id"] == "THM-M-1148"
assert receipt["phase"] == "proof"
assert receipt["intent"] == "prove"
assert receipt["base_revision"] == BASE_REVISION
assert receipt["base_tree"] == BASE_TREE
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["proposed_state"] == "[_]"
assert receipt["accepted"] is False
assert receipt["acceptance_authority"] == "Stage1 integration lane"
assert receipt["content_addressed"] is False
assert receipt["owner"] == "THM-M-1148 proof lane"
assert receipt["review_due"] == "before master acceptance or any dependent validation receipt"
assert receipt["supersession_state"] == (
    "current provisional receipt until master acceptance or invalidation"
)
assert receipt["incident_path"] == (
    "Stage1 integration lane rejects or supersedes this receipt and requeues "
    "S56-M-1148-PROOF"
)
assert set(receipt["exact_declarations"]) == expected_declarations
assert receipt["related_obligation_ids"] == [
    "M1148-ROOT", "M1148-S", "M1148-S1", "M1148-S2", "M1148-S3", "M1148-S4",
    "M1148-N", "M1148-N1", "M1148-N2", "M1148-N3", "M1148-B", "M1148-B1",
    "M1148-B2", "M1148-B3", "M1148-C", "M1148-C1", "M1148-C2", "M1148-C3",
    "M1148-L", "M1148-L1", "M1148-L2", "M1148-L3", "M1148-L4", "M1148-L5",
    "M1148-X", "M1148-T",
]
registry = json.loads((ROOT / "obligation-registry.json").read_text(encoding="utf-8"))
statement_record = json.loads((ROOT / "statement.json").read_text(encoding="utf-8"))
assert receipt["canonical_target_expression_sha256"] == statement_record[
    "elaborated_expression_sha256"
]
assert receipt["registry_denominator_sha256"] == registry["denominator_sha256"]
assert receipt["obligation_statement_fingerprints"] == {
    entry["obligation_id"]: entry["statement_fingerprint"]
    for entry in registry["obligations"]
}
assert receipt["accepted_closed_obligation_ids"] == []
assert receipt["closed_obligation_ids"] == []
assert receipt["root_evidence"]["root_kernel_declaration_closed"] is True
assert receipt["root_evidence"]["accepted_root_closed"] is False
assert receipt["root_evidence"]["internal_per_node_composition_credit"] is False
assert receipt["root_evidence"]["mapped_proof_graph_ids"] == receipt["related_obligation_ids"]
assert receipt["root_evidence"]["mapped_proof_graph_id_count"] == 26
assert receipt["root_evidence"]["composition_boundary"] == (
    "The exact canonical declaration kernel-checks through the implemented analytic route. "
    "The frozen internal obligations have only planned prose fingerprints and the route replaces "
    "the planned near/far-arc boundary proof with an ATLAS Mobius-transform argument, so no "
    "individual frozen obligation or internal composition certificate receives closure credit."
)
assert receipt["recipe"]["covered_ids"] == ["M1148-ROOT"]
assert receipt["recipe"]["covered_declarations"] == "exact_declarations"
assert receipt["result"]["theorem_complete"] is False
assert receipt["result"]["placeholder_scan"] == "pass"
assert set(receipt["result"]["axioms"]) == {"propext", "Classical.choice", "Quot.sound"}
assert receipt["debt_vector"]["accepted_before"] == {"H": "H2", "M": "M4", "R": "R4"}
assert receipt["debt_vector"]["proposed_after_proof_master_acceptance"] == {
    "H": "H2", "M": "M0-L-candidate", "R": "R4"
}
assert receipt["debt_vector"]["accepted_after_worker_selftest"] == {
    "H": "H2", "M": "M4", "R": "R4"
}
assert receipt["proof_bodies"][0]["source_sha256"] == sha256(ROOT / "PoissonUnitDisk.lean")
assert receipt["proof_bodies"][1]["source_sha256"] == sha256(ROOT / "Proof.lean")
assert receipt["inputs"]["statement_sha256"] == sha256(ROOT / "Statement.lean")
assert receipt["inputs"]["statement_json_sha256"] == sha256(ROOT / "statement.json")
assert receipt["inputs"]["obligation_registry_sha256"] == sha256(ROOT / "obligation-registry.json")
assert receipt["inputs"]["obligation_tree_sha256"] == sha256(ROOT / "ObligationTree.lean")
assert receipt["inputs"]["typed_graphs_sha256"] == sha256(ROOT / "typed-graphs.json")
assert receipt["inputs"]["task_dag_sha256"] == sha256(ROOT / "task-dag.json")
assert receipt["inputs"]["check_proof_sh_sha256"] == sha256(ROOT / "check_proof.sh")
assert receipt["inputs"]["check_proof_py_sha256"] == sha256(ROOT / "check_proof.py")
assert receipt["inputs"]["proof_validation_sha256"] == sha256(ROOT / "proof-validation.md")
assert receipt["inputs"]["atlas_license_sha256"] == sha256(ROOT / "ATLAS-LICENSE")
assert receipt["inputs"]["execution_skill_sha256"] == sha256(
    REPO / "skills/execute-stage1-rev56/SKILL.md"
)
assert receipt["inputs"]["standard_sha256"] == sha256(
    REPO / "Docs/Stage1_Blueprint_rev-5.6.md"
)

manifest = json.loads((REPO / "Formalizations/Lean/lake-manifest.json").read_text(encoding="utf-8"))
mathlib = next(package for package in manifest["packages"] if package["name"] == "mathlib")
assert mathlib["rev"] == receipt["environment"]["mathlib_revision"]
mathlib_root = REPO / "Formalizations/Lean/.lake/packages/mathlib"
mathlib_head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert mathlib_head == mathlib["rev"], "installed mathlib HEAD differs from pinned manifest"
assert receipt["environment"]["mathlib_tree"] == subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD^{tree}"],
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
assert receipt["inputs"]["lake_manifest_sha256"] == sha256(
    REPO / "Formalizations/Lean/lake-manifest.json"
)
lean_bin = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
assert lean_bin.is_file()
assert receipt["environment"]["lean_executable_sha256"] == sha256(lean_bin)
lean_version = subprocess.run(
    [str(lean_bin), "--version"], check=True, capture_output=True, text=True
).stdout.strip()
assert lean_version == receipt["environment"]["lean_version_output"]
assert receipt["environment"]["lake_version"] == "not_invoked_by_validation"
assert receipt["environment"]["shared_cache_incident"] == (
    "A superseded Lake-based checker attempted to materialize missing flt-regular through the "
    "shared canonical .lake symlink and left an incomplete Git directory; this final recipe "
    "does not invoke Lake, repair, or delete that shared state."
)

adapted = receipt["proof_bodies"][0]
assert adapted["classification"] == "repo_local_adaptation_with_local_additions"
assert adapted["adapted_declarations"] == [
    "poissonIntegral",
    "herglotzIntegral",
    "poissonIntegral_eq_re_herglotzIntegral",
    "herglotzIntegral_differentiableOn",
    "harmonicOnNhd_re_of_differentiableOn",
    "harmonicOnNhd_congr_eqOn",
    "poissonIntegral_harmonic",
    "mobiusTransform",
    "continuous_poissonKernel_circleMap",
    "invMobiusAngle",
    "mobiusTransform_circleMap_invMobiusAngle_zero",
    "eq_zero_of_hasDerivAt_mul",
    "deriv_inv_mobius_eq_poisson_mul'",
    "one_sub_conj_mul_circleMap_ne_zero",
    "invMobiusAngle_mobiusTransform_core",
    "invMobiusAngle_mobiusTransform",
    "hasDerivAt_invMobiusAngle",
    "invMobiusAngle_add_two_pi",
    "norm_circleMap_zero_one",
    "poissonKernel_nonneg_circleMap",
    "poissonIntegral_eq_circleAverage_mobiusTransform",
    "mobiusTransform_tendsto_on_circle",
    "circleAverage_mobiusTransform_aestronglyMeasurable",
    "circleAverage_mobiusTransform_bound",
    "circleAverage_mobiusTransform_tendsto",
    "poissonIntegral_tendsto_boundary",
]
assert adapted["upstream_source_regions"] == [
    "Lecture16.lean lines 38-194",
    "Lecture16.lean lines 196-768",
    "Lecture16.lean lines 770-789",
]
assert adapted["upstream_revision"] == "34ffed396f376454c1a9b297f3fd74c5c801fb50"
assert adapted["upstream_source_sha256"] == (
    "e6eee1fa36081cf1a83c1394541fdefe5714d8b42d86bcb88210e1dbd94628da"
)
assert adapted["upstream_license_sha256"] == (
    "289dc0e96c537ecc7883cd94c3f65e2b691ac0fd6f4372fc01604531cbbf1abc"
)
assert adapted["license_compatibility"] == "unreviewed_blocker"

print("PASS THM-M-1148 proof packet: exact root kernel declaration bound; acceptance remains open")
