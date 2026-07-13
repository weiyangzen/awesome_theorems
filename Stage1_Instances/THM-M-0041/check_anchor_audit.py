#!/usr/bin/env python3
"""Validate the bounded immutable THM-M-0041 anchor inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0041-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0041"
BASE_REVISION = "540472523b6c0717ed925193071191f81f62d6eb"
BASE_TREE = "64b0c81418ef2c97b0250188444c672b9ae885d0"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "5aad8415af4578ca43d0ec58eee038ed4470dce17896766215d3bf9f49d8e711"
STATEMENT_SHA256 = "3b218c1a96922399bb8ed2d852d556422a92901dca10efdd431a677eaefd2b0b"
LEAN_OUTPUT_SHA256 = "4d6423e2e5e4b1f9d6c8e410782108da66670ca1d598e80ab75567ac4acd89f7"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.md",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def check_actual_canonical_declaration(probe: str) -> None:
    statement_source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    imports = (
        "import Mathlib.Algebra.Polynomial.AlgebraMap\n"
        "import Mathlib.LinearAlgebra.Charpoly.Basic\n"
    )
    statement_body = re.sub(r"^import .*\n", "", statement_source, flags=re.MULTILINE)
    statement_body = re.sub(
        r"^#check_failure Matrix\.(?:charpoly|aeval_self_charpoly)\n",
        "",
        statement_body,
        flags=re.MULTILINE,
    )
    probe_body = re.sub(r"^import .*\n", "", probe, flags=re.MULTILINE)
    comparison = """

namespace Stage1Instances.THM_M_0041_AnchorAudit

/-- Validator-only checked identity between the actual statement declaration and audit copy. -/
theorem actualCanonicalTarget_eq_auditTarget :
    Stage1Instances.THM_M_0041.CayleyHamiltonTarget.{u, v} = CanonicalTarget.{u, v} :=
  rfl

/-- Validator-only exact wrapper whose type is the actual statement-gate declaration. -/
theorem exactActualCanonicalAnchor :
    Stage1Instances.THM_M_0041.CayleyHamiltonTarget.{u, v} := by
  intro R _ n _ _ A
  exact Matrix.aeval_self_charpoly A

end Stage1Instances.THM_M_0041_AnchorAudit
"""
    with tempfile.NamedTemporaryFile("w", suffix=".lean", encoding="utf-8") as handle:
        handle.write(imports + statement_body + probe_body + comparison)
        handle.flush()
        result = subprocess.run(
            ["lake", "env", "lean", handle.name],
            cwd=LEAN_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            check=False,
        )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit("actual canonical declaration comparison failed")


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    target_manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1081 and audit["phase"] == "anchor_audit"
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert audit["discovery_protocol_sha256"] == canonical_json_sha256(audit["discovery_protocol"])
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in target_manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1081
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0041-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256
    assert audit["canonical_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]

    candidates = {candidate["candidate_id"]: candidate for candidate in audit["candidates"]}
    assert set(candidates) == {
        "M0041-C01-MATHLIB-EXACT",
        "M0041-C02-MATHLIB-LINEAR-MAP-DUPLICATE",
        "M0041-C03-MATHLIB-FG-MODULE-SUPPORT",
        "M0041-C04-ATLAS-FIN-TWO-SPECIAL-CASE",
        "M0041-C05-AUTOMATH-DOWNSTREAM-CONSUMER",
    }
    exact = candidates["M0041-C01-MATHLIB-EXACT"]
    assert exact["candidate_classification"] == "M3"
    assert exact["candidate_route_if_e1_accepted"] == "M0-W"
    assert exact["declaration"] == exact["terminal_declaration"] == "Matrix.aeval_self_charpoly"
    assert exact["local_wrapper"].endswith("exactMathlibAnchor")
    assert exact["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert sha256(MATHLIB / exact["file"]) == exact["file_sha256"]
    assert output("git", "rev-parse", f"HEAD:{exact['file']}", cwd=MATHLIB) == exact["file_blob"]
    for file, blob in exact["direct_dependency_source_blobs"].items():
        assert output("git", "rev-parse", f"HEAD:{file}", cwd=MATHLIB) == blob

    matrix_text = (MATHLIB / exact["file"]).read_text(encoding="utf-8")
    for marker in (
        "def charmatrix",
        "def charpoly",
        "theorem aeval_self_charpoly",
        "have h : M.charpoly",
        "rw [eval_mul_X_sub_C] at h",
        "rw [matPolyEquiv_smul_one, eval_map] at h",
    ):
        assert marker in matrix_text, marker

    duplicate = candidates["M0041-C02-MATHLIB-LINEAR-MAP-DUPLICATE"]
    assert duplicate["candidate_classification"] == "M3"
    assert duplicate["candidate_role"] == "support_duplicate"
    assert duplicate["terminal_declaration"] == "Matrix.aeval_self_charpoly"
    assert sha256(MATHLIB / duplicate["file"]) == duplicate["file_sha256"]
    linear_text = (MATHLIB / duplicate["file"]).read_text(encoding="utf-8")
    assert "theorem aeval_self_charpoly" in linear_text
    assert "exact Matrix.aeval_self_charpoly _" in linear_text

    fg_module = candidates["M0041-C03-MATHLIB-FG-MODULE-SUPPORT"]
    assert fg_module["candidate_classification"] == "M3"
    assert fg_module["candidate_role"] == "support_duplicate"
    assert sha256(MATHLIB / fg_module["file"]) == fg_module["file_sha256"]
    assert output("git", "rev-parse", f"HEAD:{fg_module['file']}", cwd=MATHLIB) == fg_module["file_blob"]
    fg_text = (MATHLIB / fg_module["file"]).read_text(encoding="utf-8")
    assert "theorem LinearMap.exists_monic_and_aeval_eq_zero" in fg_text
    assert "Matrix.aeval_self_charpoly" in fg_text

    atlas = candidates["M0041-C04-ATLAS-FIN-TWO-SPECIAL-CASE"]
    assert atlas["revision"] == "34ffed396f376454c1a9b297f3fd74c5c801fb50"
    assert atlas["tree"] == "c12fe2315fe475d70a4fcee81d6b731f853373ab"
    assert atlas["candidate_classification"] == "M3"
    assert atlas["candidate_role"] == "external_special_case_source_only"
    assert "Fin 2" in atlas["type"] and "ZMod n" in atlas["type"]
    assert atlas["file_sha256"] == "885d85b3b3e121d0d30c9903e04b61d93feb1b317ad0f45aa55537d338c8110e"

    automath = candidates["M0041-C05-AUTOMATH-DOWNSTREAM-CONSUMER"]
    assert automath["revision"] == "f76f46f07a1a48d5c12a20c2f8d366bb9df9330d"
    assert automath["tree"] == "971613ac246ba81191b7654cc84fff1169ec5188"
    assert automath["candidate_classification"] == "M3"
    assert automath["candidate_role"] == "downstream_consumer_duplicate"
    assert automath["terminal_declaration_for_cayley_hamilton_step"] == "Matrix.aeval_self_charpoly"
    assert automath["file_sha256"] == "f173ee684b46c16013de0e932fec4f56dc2229ff6fe72dfed6db42cd3b956b46"

    searches = audit["external_searches"]
    assert len(searches) == 7
    assert all(row["response_sha256"] for row in searches)
    assert any("HTTP 401" in row["result"] for row in searches)
    assert audit["discovery_protocol"]["frozen_before_candidate_classification"] is True
    assert audit["discovery_protocol"]["saturation_claim"] is False

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("5/5 candidate records classified")
    assert result["exact_candidate_located"] is result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["independent_external_exact_terminal_body_found"] is False
    assert result["eligible_external_integration_debt"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_route"] == "M0-W"
    assert result["root_machine_candidate_after"] == "M3"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert audit["theorem_complete"] is False

    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["classified_records"] == 5
    assert receipt["candidate_result"]["exact_mathlib_candidate_found"] is True
    assert receipt["candidate_result"]["candidate_classification"] == "M3"
    assert receipt["candidate_result"]["candidate_route_if_e1_accepted"] == "M0-W"
    assert receipt["candidate_result"]["accepted_root_classification"] == "M3"
    assert receipt["candidate_result"]["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False

    required_packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet) == required_packet_fields
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]

    probe = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    for marker in (
        "def characteristicPolynomial",
        "def CanonicalTarget : Prop",
        "theorem characteristicPolynomial_eq_charpoly",
        "theorem exactMathlibAnchor",
        "exact Matrix.aeval_self_charpoly A",
        "#print axioms Matrix.aeval_self_charpoly",
        "#print axioms LinearMap.aeval_self_charpoly",
    ):
        assert marker in probe, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    assert not forbidden.search(without_comments(probe))
    check_actual_canonical_declaration(probe)

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0041/AnchorAudit.lean"],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    for marker in (
        "@Matrix.aeval_self_charpoly",
        "'Stage1Instances.THM_M_0041_AnchorAudit.exactMathlibAnchor' depends on axioms: [propext, Classical.choice, Quot.sound]",
        "'Matrix.aeval_self_charpoly' depends on axioms: [propext, Classical.choice, Quot.sound]",
        "'LinearMap.aeval_self_charpoly' depends on axioms: [propext, Classical.choice, Quot.sound]",
    ):
        if marker not in lean.stdout:
            sys.stdout.write(lean.stdout)
            raise SystemExit(f"expected Lean evidence missing: {marker}")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("anchor probe output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0041; 5 classified records; exact pinned route toward M0-W; "
        "accepted root remains M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
