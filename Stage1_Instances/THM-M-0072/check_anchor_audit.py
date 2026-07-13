#!/usr/bin/env python3
"""Validate the immutable, bounded THM-M-0072 formal-anchor audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0072-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0072"
BASE_REVISION = "56cce0660d633175f8e66c4a538e5c7dce64652e"
BASE_TREE = "94920deccabd41cd711821885fe08d62eed67a4e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "c8a89538bd8b492ba31ce5d516a0f8fefef70a550e1d2fe74e39a4cba7849051"
STATEMENT_SHA256 = "0e9a35c7d2a9eaafb2aa6f8357277e9bf1e79e9a5e88500bda6cd8300a6757aa"
PROTOCOL_SHA256 = "7a28cfb7068c8a3b6473c909cfafc4a055a96f82fea28a467b8cb206cc474137"
ANCHOR_LEAN_SHA256 = "5ef2cdf8984a7f728a9995e6c1afa7872a4cf579f9cf80f71486e08c56129731"
LEAN_OUTPUT_SHA256 = "8b19682c9ebb13800e93a34859f4701dc061ecf0faa4bd45721cfa2925614d86"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM_ID}/AnchorAudit.lean",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-receipt.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit-validation.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.json",
    f"Stage1_Instances/{THEOREM_ID}/anchor-audit.md",
    f"Stage1_Instances/{THEOREM_ID}/anchor-discovery-protocol.json",
    f"Stage1_Instances/{THEOREM_ID}/check_anchor_audit.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_lines(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    audit = load(HERE / "anchor-audit.json")
    protocol = load(HERE / "anchor-discovery-protocol.json")
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1102
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1102
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0072-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256

    assert protocol["schema_version"] == "stage1-anchor-discovery-protocol/1.0"
    assert protocol["item_id"] == ITEM_ID and protocol["theorem_id"] == THEOREM_ID
    assert protocol["inventory_version"] == audit["discovery_protocol"]["inventory_version"]
    assert protocol["saturation_claim"] is False
    assert sha256(HERE / "anchor-discovery-protocol.json") == PROTOCOL_SHA256
    assert audit["discovery_protocol"]["sha256"] == PROTOCOL_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["mathlib_license_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]

    candidates = audit["candidates"]
    assert len(candidates) == 6
    assert {candidate["candidate_id"] for candidate in candidates} == {
        "M0072-C01-REPO-LOCAL-STATEMENT",
        "M0072-C02-MATHLIB-TRANSFER-SUBSTRATE",
        "M0072-C03-MATHLIB-BURNSIDE-NONSUBSTITUTE",
        "M0072-C04-MATHLIB-FOCAL-SUBSTRATE",
        "M0072-C05-MANIFEST-EXTERNAL-CORPUS",
        "M0072-C06-FORMAL-CONJECTURES",
    }
    transfer = next(c for c in candidates if c["candidate_id"] == "M0072-C02-MATHLIB-TRANSFER-SUBSTRATE")
    burnside = next(c for c in candidates if c["candidate_id"] == "M0072-C03-MATHLIB-BURNSIDE-NONSUBSTITUTE")
    focal = next(c for c in candidates if c["candidate_id"] == "M0072-C04-MATHLIB-FOCAL-SUBSTRATE")
    for candidate in (transfer, burnside, focal):
        source = MATHLIB / candidate["file"]
        assert candidate["revision"] == MATHLIB_REVISION
        assert candidate["tree"] == MATHLIB_TREE
        assert candidate["file_blob"] == output("git", "rev-parse", f"HEAD:{candidate['file']}", cwd=MATHLIB)
        assert candidate["file_sha256"] == sha256(source)
    assert transfer["candidate_classification"] == "M3_substrate_only"
    assert burnside["candidate_classification"] == "M5_statement_mismatch"
    assert focal["candidate_classification"] == "M3_substrate_only"
    assert sha256_lines(MATHLIB / transfer["file"], 148, 269) == transfer["source_region_sha256"]
    assert sha256_lines(MATHLIB / burnside["file"], 275, 283) == burnside["source_region_sha256"]
    assert sha256_lines(MATHLIB / focal["file"], 116, 212) == focal["source_region_sha256"]

    transfer_source = (MATHLIB / transfer["file"]).read_text(encoding="utf-8")
    focal_source = (MATHLIB / focal["file"]).read_text(encoding="utf-8")
    for marker in (
        "noncomputable def transfer [FiniteIndex H]",
        "theorem transfer_eq_prod_quotient_orbitRel_zpowers_quot",
        "theorem transfer_eq_pow [FiniteIndex H]",
        "noncomputable def transferSylow",
        "theorem transferSylow_eq_pow",
        "theorem ker_transferSylow_isComplement'",
        "**Burnside's normal p-complement theorem**",
    ):
        assert marker in transfer_source, marker
    for marker in (
        "lemma focalSubgroupOf.mk'_conj_eq",
        "noncomputable def transferFocal",
        "theorem transferFocal_eq_pow",
        "lemma transferFocal_surjective",
        "lemma ker_restrict_transferFocal_eq_focalSubgroupOf",
        "theorem commutator_inf_eq_focalSubgroup",
        "**The Focal Subgroup Theorem**",
    ):
        assert marker in focal_source, marker

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["source_boundary_coverage"].startswith("6/6 frozen candidate groups classified")
    assert result["exact_candidate_located"] is False
    assert result["substrate_candidates_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["independent_external_exact_terminal_body_found"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == "M3"
    assert result["accepted_root_machine_debt_after"] == "M3"
    assert result["root_evidence_level"] == "E3"
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is False and result["theorem_complete"] is False
    assert audit["theorem_complete"] is False

    receipt_paths = set(receipt["changed_paths"])
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == "anchor_audit" and receipt["intent"] == "audit"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["content_addressed"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt_paths == CHANGED_PATHS
    assert receipt["lean_output_sha256"] == LEAN_OUTPUT_SHA256
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []

    assert packet["item_id"] == ITEM_ID and packet["theorem_id"] == THEOREM_ID
    assert packet["state"] == "[_]" and packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]

    adapter_path = HERE / "AnchorAudit.lean"
    adapter = adapter_path.read_text(encoding="utf-8")
    assert sha256(adapter_path) == ANCHOR_LEAN_SHA256
    for marker in (
        "def ExactTarget : Prop",
        "forall H : Subgroup G, H.index != 2",
        "exists m : M, IsConj (x : G) ((m : S) : G)",
        "#check_failure (MonoidHom.ker_transferSylow_isComplement' : ExactTarget.{u})",
        "#check_failure (Subgroup.commutator_inf_eq_focalSubgroup : ExactTarget.{u})",
        "#print sorries Subgroup.commutator_inf_eq_focalSubgroup",
    ):
        assert marker in adapter, marker
    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    assert not forbidden.search(without_comments(adapter))

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0072/AnchorAudit.lean"],
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
    if lean.stdout.count("depends on axioms: [propext, Classical.choice, Quot.sound]") != 5:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected candidate axiom report")
    if lean.stdout.count("Declarations are sorry-free!") != 5:
        sys.stdout.write(lean.stdout)
        raise SystemExit("unexpected candidate placeholder report")
    if lean.stdout.count("Type mismatch") != 2:
        sys.stdout.write(lean.stdout)
        raise SystemExit("expected two explicit non-substitute type rejections")
    if "def Stage1Instances.THM_M_0072_AnchorAudit.ExactTarget.{u} : Prop" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("exact audit target was not printed")
    if hashlib.sha256(lean.stdout.encode()).hexdigest() != LEAN_OUTPUT_SHA256:
        sys.stdout.write(lean.stdout)
        raise SystemExit("candidate Lean output changed")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0072; 6 candidate groups; no exact Lean body; pinned transfer/focal M3/E3; "
        "accepted root remains M3; audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
