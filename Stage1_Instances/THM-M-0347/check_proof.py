#!/usr/bin/env python3
"""Fail-closed structural checks for the THM-M-0347 proof packet."""

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
BASE_REVISION = "9e1db93a3c4b869cc7c1f8ac99b6c1b12cb4c82c"
BASE_TREE = "0499e20448fdcec5b57b47cc034570b35aab32a1"
UPSTREAM_SOURCE_SHA256 = "f205a16c5146232c7c23e66a018ebd2dd954d70c5c481de5491d3b0cc8752f4f"
ATLAS_LICENSE_SHA256 = "289dc0e96c537ecc7883cd94c3f65e2b691ac0fd6f4372fc01604531cbbf1abc"

if not __debug__:
    raise SystemExit("FAIL: Python assertions are disabled")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


atlas_source = (ROOT / "AtlasFourierSeries.lean").read_text(encoding="utf-8")
probe_source = (ROOT / "AtlasAxiomProbe.lean").read_text(encoding="utf-8")
proof_source = (ROOT / "Proof.lean").read_text(encoding="utf-8")
receipt = json.loads((ROOT / "proof-receipt.json").read_text(encoding="utf-8"))
registry = json.loads((ROOT / "obligation-registry.json").read_text(encoding="utf-8"))
statement_record = json.loads((ROOT / "statement.json").read_text(encoding="utf-8"))

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

prohibited = re.compile(
    r"\b(sorry|admit|sorryAx|native_decide|implemented_by|proof_wanted)\b|"
    r"^\s*(axiom|constant|opaque|unsafe|extern)\b",
    re.MULTILINE,
)
assert not prohibited.search(atlas_source), "prohibited construct in AtlasFourierSeries.lean"
assert not prohibited.search(probe_source), "prohibited construct in AtlasAxiomProbe.lean"
assert not prohibited.search(proof_source), "prohibited construct in Proof.lean"
assert sha256(ROOT / "AtlasFourierSeries.lean") == UPSTREAM_SOURCE_SHA256
assert sha256(ROOT / "ATLAS-LICENSE") == ATLAS_LICENSE_SHA256

required_atlas = {
    "fourier_integrable",
    "integral_fourier",
    "integral_dirichlet_sum",
    "fejerKernel_symmetric",
    "integral_fejerKernel",
    "norm_fejerKernel_le",
    "fejerKernel_continuous",
    "fejerKernel_integrable",
    "fourier_neg_mul_fourier_eq",
    "sum_range_fourier_shift_neg",
    "sum_range_fourier_shift_pos",
    "fejer_dirichlet_sum_eq_sq",
    "fejerKernel_nonneg",
    "fejer_kernel_properties",
    "fourier_sub_eq",
    "fourier_smul_integrable",
    "fourier_integral_convolution",
    "cesaroMean_eq_fejer_convolution",
    "fejerKernel_eq_ofReal",
    "integral_norm_fejerKernel",
    "cesaroMean_uniform_bound",
    "fejer_uniform_convergence",
}
declared_atlas = set(re.findall(
    r"^(?:noncomputable\s+)?(?:theorem|lemma)\s+([A-Za-z0-9_]+)",
    atlas_source,
    re.MULTILINE,
))
assert required_atlas <= declared_atlas, (
    f"missing ATLAS declarations: {sorted(required_atlas - declared_atlas)}"
)
required_proof = {
    "symmetricFourierPartialSum_apply",
    "fejerMean_apply",
    "fejerTheorem",
}
declared_proof = set(re.findall(
    r"^theorem\s+([A-Za-z0-9_]+)", proof_source, re.MULTILINE
))
assert required_proof <= declared_proof
assert "import Statement" in proof_source
assert "import AtlasFourierSeries" in proof_source
assert "theorem fejerTheorem : FejerTheoremTarget" in proof_source
assert "using fejer_uniform_convergence f" in proof_source

assert receipt["schema_version"] == "stage1-node-receipt/1.0"
assert receipt["item_id"] == "S56-M-0347-PROOF"
assert receipt["theorem_id"] == "THM-M-0347"
assert receipt["phase"] == "proof"
assert receipt["intent"] == "prove"
assert receipt["base_revision"] == BASE_REVISION
assert receipt["base_tree"] == BASE_TREE
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["proposed_state"] == "[_]"
assert receipt["accepted"] is False
assert receipt["acceptance_authority"] == "Stage1 integration lane"
assert receipt["content_addressed"] is False
assert receipt["canonical_target"] == (
    "Stage1Instances.THM_M_0347.FejerTheoremTarget"
)
assert receipt["canonical_target_expression_sha256"] == statement_record[
    "canonical_formal_target"
]["elaborated_expression_sha256"]
assert receipt["registry_denominator_sha256"] == registry["denominator_sha256"]
assert receipt["obligation_statement_fingerprints"] == {
    entry["obligation_id"]: entry["statement_fingerprint"]
    for entry in registry["obligations"]
}
obligation_ids = [entry["obligation_id"] for entry in registry["obligations"]]
assert receipt["related_obligation_ids"] == obligation_ids
assert receipt["closed_obligation_ids"] == []
assert receipt["accepted_closed_obligation_ids"] == []
root = receipt["root_evidence"]
assert root["root_declaration"] == "Stage1Instances.THM_M_0347.fejerTheorem"
assert root["root_kernel_declaration_closed"] is True
assert root["accepted_root_closed"] is False
assert root["internal_per_node_composition_credit"] is False
assert root["mapped_proof_graph_ids"] == obligation_ids
assert root["mapped_proof_graph_id_count"] == len(obligation_ids)
assert receipt["recipe"]["covered_ids"] == ["M0347-ROOT"]
assert receipt["recipe"]["covered_declarations"] == "exact_declarations"
assert receipt["result"]["root_kernel_closed"] is True
assert receipt["result"]["accepted_root_closed"] is False
assert receipt["result"]["theorem_complete"] is False
assert receipt["result"]["placeholder_scan"] == "pass"
assert set(receipt["result"]["axioms"]) == {
    "propext", "Classical.choice", "Quot.sound"
}
assert receipt["debt_vector"]["accepted_before"] == {
    "H": "H1", "M": "M3", "R": "R4"
}
assert receipt["debt_vector"]["accepted_after_worker_selftest"] == {
    "H": "H1", "M": "M3", "R": "R4"
}

proof_body = receipt["proof_bodies"][0]
assert proof_body["source_sha256"] == sha256(ROOT / "AtlasFourierSeries.lean")
assert proof_body["upstream_revision"] == "34ffed396f376454c1a9b297f3fd74c5c801fb50"
assert proof_body["upstream_tree"] == "c12fe2315fe475d70a4fcee81d6b731f853373ab"
assert proof_body["upstream_blob"] == "5d399cda446f9bd901902b281bb796123c5ec856"
assert proof_body["upstream_source_sha256"] == UPSTREAM_SOURCE_SHA256
assert proof_body["upstream_license_sha256"] == ATLAS_LICENSE_SHA256
assert proof_body["license_compatibility"] == "unreviewed_blocker"
assert receipt["proof_bodies"][1]["source_sha256"] == sha256(ROOT / "Proof.lean")

expected_hashes = {
    "statement_sha256": "Statement.lean",
    "statement_json_sha256": "statement.json",
    "obligation_tree_sha256": "ObligationTree.lean",
    "obligation_registry_sha256": "obligation-registry.json",
    "typed_graphs_sha256": "typed-graphs.json",
    "task_dag_sha256": "task-dag.json",
    "atlas_source_sha256": "AtlasFourierSeries.lean",
    "atlas_axiom_probe_sha256": "AtlasAxiomProbe.lean",
    "proof_sha256": "Proof.lean",
    "check_proof_sh_sha256": "check_proof.sh",
    "proof_validation_sha256": "proof-validation.md",
    "atlas_license_sha256": "ATLAS-LICENSE",
}
for field, filename in expected_hashes.items():
    assert receipt["inputs"][field] == sha256(ROOT / filename), field
assert receipt["inputs"]["execution_skill_sha256"] == sha256(
    REPO / "skills/execute-stage1-rev56/SKILL.md"
)
assert receipt["inputs"]["standard_sha256"] == sha256(
    REPO / "Docs/Stage1_Blueprint_rev-5.6.md"
)
assert receipt["inputs"]["lake_manifest_sha256"] == sha256(
    REPO / "Formalizations/Lean/lake-manifest.json"
)

manifest = json.loads(
    (REPO / "Formalizations/Lean/lake-manifest.json").read_text(encoding="utf-8")
)
mathlib = next(p for p in manifest["packages"] if p["name"] == "mathlib")
assert mathlib["rev"] == receipt["environment"]["mathlib_revision"]
mathlib_root = REPO / "Formalizations/Lean/.lake/packages/mathlib"
mathlib_head = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True,
).stdout.strip()
mathlib_tree = subprocess.run(
    ["git", "-C", str(mathlib_root), "rev-parse", "HEAD^{tree}"],
    check=True, capture_output=True, text=True,
).stdout.strip()
assert mathlib_head == mathlib["rev"]
assert receipt["environment"]["mathlib_tree"] == mathlib_tree

lean_bin = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
assert receipt["environment"]["lean_executable_sha256"] == sha256(lean_bin)
lean_version = subprocess.run(
    [str(lean_bin), "--version"], check=True, capture_output=True, text=True
).stdout.strip()
assert receipt["environment"]["lean_version_output"] == lean_version
assert receipt["environment"]["lake_version"] == "not_invoked_by_final_validation"

status = subprocess.run(
    ["git", "status", "--porcelain=v1", "--untracked-files=all"],
    cwd=REPO, check=True, capture_output=True, text=True,
).stdout.splitlines()
allowed_paths = {".stage1-worker-selftest.json"}
for line in status:
    path = line[3:]
    if path == "Formalizations/Lean/.lake":
        continue
    assert path in allowed_paths or path.startswith("Stage1_Instances/THM-M-0347/"), (
        f"change outside owned target path: {path}"
    )

assert sha256(ROOT / "check_proof.py") == receipt["inputs"]["check_proof_py_sha256"]
print("PASS THM-M-0347 proof packet: exact root kernel declaration bound; acceptance remains open")
