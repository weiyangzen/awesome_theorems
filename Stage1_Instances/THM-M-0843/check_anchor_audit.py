#!/usr/bin/env python3
"""Validate the immutable, locally checkable THM-M-0843 anchor ledger."""

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
AUDIT_PATH = HERE / "anchor-audit.json"
ITEM_ID = "S56-M-0843-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0843"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0843/AnchorAudit.lean",
    "Stage1_Instances/THM-M-0843/README.md",
    "Stage1_Instances/THM-M-0843/anchor-audit-receipt.json",
    "Stage1_Instances/THM-M-0843/anchor-audit-validation.md",
    "Stage1_Instances/THM-M-0843/anchor-audit.json",
    "Stage1_Instances/THM-M-0843/check_anchor_audit.py",
    "Stage1_Instances/THM-M-0843/source-statement-crosswalk.md",
}
BASE_REVISION = "5ae439adae290d44dcf08cc6439c5fb64154fe47"
BASE_TREE = "51717feef6efc7076e60ee31e7a1ca0a246fec42"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "3fe13f3562cb642e45e467687508ac44f945e9848ff53d22b9cf068d7ec11219"
STATEMENT_SHA256 = "6afd11f23d5245eaa4c487ad4484249b517f6fcf4f99373a2f437d5307aee9ec"
REGULARITY_FILES = {
    "Bound.lean": "4b8f892d4cede7359c792bbcff09d4f9a86136edc405f1e287b767d3b362b99a",
    "Chunk.lean": "238f19d5547c346f7eeaff02e84b4ab78279594d38dacfa990e51bc666d82008",
    "Energy.lean": "e2ead2d6b414091f83a91e8561b014394407eaedab6a9801bc467d9fa54fc95c",
    "Equitabilise.lean": "546ad28d80d0b064fa928bb791cf8204bc2f10ab734f250101408cdee8ee868f",
    "Increment.lean": "74f073e00ff00483af32a7a32168bd157ffb3d54c6952216399d60371045eb4c",
    "Lemma.lean": "eee7f2c505130c4a09fa8e62dca7bc1bbfaff90c18e86e9ad43f44f7f0ea8fd6",
    "Uniform.lean": "05197020a8ccd5a34989502d2e0ef1f271f9b6cd1436970406f4d72be4e5d77c",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    audit = load(AUDIT_PATH)
    receipt = load(HERE / "anchor-audit-receipt.json")
    statement = load(HERE / "statement.json")
    manifest = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = load(packet_path) if packet_path.exists() else None

    assert audit["schema_version"] == "stage1-anchor-audit/1.0"
    assert audit["item_id"] == ITEM_ID and audit["theorem_id"] == THEOREM_ID
    assert audit["execution_rank"] == 1032
    assert audit["base_revision"] == BASE_REVISION and audit["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["candidate_result"]["classification"] == "M0-W"
    assert receipt["candidate_result"]["evidence_level"] == "E2"
    assert receipt["candidate_result"]["master_accepted"] is False
    assert receipt["audit_complete"] is False and receipt["theorem_complete"] is False
    if packet is not None:
        assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == receipt["known_failures"]

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 1032
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item["phase"] == "anchor_audit" and item["layer"] == 2
    assert item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0843-STATEMENT"]
    assert item["owned_paths"] == ["Stage1_Instances/THM-M-0843"]

    assert audit["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert audit["canonical_statement_file_sha256"] == STATEMENT_SHA256
    assert sha256(HERE / "Statement.lean") == STATEMENT_SHA256
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == STATEMENT_SHA256

    env = audit["immutable_environment"]
    assert env["mathlib_revision"] == MATHLIB_REVISION
    assert env["mathlib_tree"] == MATHLIB_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == env["license_sha256"]
    assert sha256(LEAN_ROOT / "lake-manifest.json") == env["manifest_sha256"]

    regularity = MATHLIB / "Mathlib/Combinatorics/SimpleGraph/Regularity"
    for name, expected in REGULARITY_FILES.items():
        assert sha256(regularity / name) == expected, name

    candidate_ids = [candidate["candidate_id"] for candidate in audit["candidates"]]
    assert len(candidate_ids) == len(set(candidate_ids)) == 2
    candidate = next(candidate for candidate in audit["candidates"] if candidate["candidate_id"] == "M0843-C01")
    assert candidate["revision"] == MATHLIB_REVISION and candidate["tree"] == MATHLIB_TREE
    assert candidate["file_sha256"] == REGULARITY_FILES["Lemma.lean"]
    assert candidate["file_blob"] == output(
        "git", "rev-parse", f"HEAD:{candidate['file']}", cwd=MATHLIB
    )
    assert candidate["declaration"] == "szemeredi_regularity"
    assert candidate["classification"] == "M0-W"
    assert candidate["evidence_level"] == "E2"
    history = candidate["historical_provenance"]
    assert history["mathlib3_introduction_commit"] == "1d4d3ca5ec44693640c4f5e407a6b611f77accc8"
    assert history["mathlib4_port_commit"] == "4ab276de9cf469a250730f765fc08d2b7b613870"
    assert history["mathlib4_port_tree"] == output(
        "git", "rev-parse", "4ab276de9cf469a250730f765fc08d2b7b613870^{tree}", cwd=MATHLIB
    )
    assert output(
        "git", "merge-base", "--is-ancestor",
        history["mathlib4_port_commit"], MATHLIB_REVISION, cwd=MATHLIB
    ) == ""

    lemma_source = (MATHLIB / candidate["file"]).read_text(encoding="utf-8")
    for marker in (
        "theorem szemeredi_regularity",
        "obtain hα | hα := le_total (card α) (bound ε l)",
        "obtain hε₁ | hε₁ := le_total 1 ε",
        "induction i with",
        "energy_increment hP₁",
    ):
        assert marker in lemma_source, marker

    forbidden = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|unsafe|opaque)\b")
    for name in REGULARITY_FILES:
        source = without_comments((regularity / name).read_text(encoding="utf-8"))
        assert not forbidden.search(source), f"forbidden construct in {name}"

    adapter = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    statement_source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    for marker in (
        "0 < epsilon ->",
        "l <= Fintype.card alpha ->",
        "P.IsEquipartition",
        "P.parts.card <= SzemerediRegularity.bound epsilon l",
        "P.IsUniform G epsilon",
    ):
        assert marker in adapter and marker in statement_source, marker
    assert "exact szemeredi_regularity G hEpsilon hCard" in adapter
    assert not forbidden.search(without_comments(adapter))

    result = audit["audit_result"]
    assert result["inventory_classified"] is True
    assert result["exact_candidate_located"] is True
    assert result["candidate_kernel_checked"] is True
    assert result["candidate_accepted_by_master"] is False
    assert result["root_machine_debt_before"] == "M3"
    assert result["root_machine_candidate_after"] == "M0-W"
    assert result["root_evidence_level"] == "E2"
    assert result["node_self_tested"] is True
    assert result["audit_complete"] is False
    assert result["theorem_complete"] is False
    assert audit["discovery_protocol"]["saturation_claim"] is False

    lean = subprocess.run(
        ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0843/AnchorAudit.lean"],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
    )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)
    if "Declarations are sorry-free!" not in lean.stdout:
        sys.stdout.write(lean.stdout)
        raise SystemExit("terminal declaration is not machine-reported sorry-free")
    expected_axioms = "propext, Classical.choice, Quot.sound"
    if lean.stdout.count(expected_axioms) != 1:
        # The wrapper's pretty printer inserts newlines, so also compare normalized output.
        normalized = re.sub(r"\s+", " ", lean.stdout)
        if normalized.count(expected_axioms) != 2:
            sys.stdout.write(lean.stdout)
            raise SystemExit("unexpected axiom report")

    print(
        "check_anchor_audit: ok "
        "(THM-M-0843; 2 candidates; exact pinned mathlib wrapper M0-W/E2; "
        "audit_complete=false; theorem_complete=false)"
    )


if __name__ == "__main__":
    main()
