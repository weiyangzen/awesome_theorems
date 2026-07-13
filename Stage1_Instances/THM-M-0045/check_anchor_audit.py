#!/usr/bin/env python3
"""Fail-closed worker check for the THM-M-0045 anchor-audit packet."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0045-ANCHOR_AUDIT"
THEOREM_ID = "THM-M-0045"
BASE_REVISION = "c76fe0f1a7514b41f191d16840eff25e64ee9d17"
BASE_TREE = "388bc991837bae9741d7e7cb88b43c216eab966a"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
CANDIDATE_REVISION = "0a539f0ce764fd16726509b62ed7b870461070eb"
CANDIDATE_TREE = "5da322f204f788b5eb2649c51fbfd54ffadb7265"
CANDIDATE_PATH = "Mathlib/LinearAlgebra/Matrix/SchurTriangulation.lean"
CANDIDATE_SHA256 = "8fc4d47249d8bcc75c02fedc6d9b0008f7c0127c501f608d4226a7f5872f4bc3"
TARGET_SHA256 = "275e1e43027f442607fc48e78ce4e189de66b328d39c61044e87a4c8f85c001b"


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{name} must contain a JSON object")
    return value


def output(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def run_lean(name: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", str(HERE / name)], cwd=LEAN_ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path, default=ROOT / ".stage1-worker-selftest.json")
    args = parser.parse_args()

    audit = load("anchor-audit.json")
    protocol = load("anchor-discovery-protocol.json")
    snapshot = load("external-anchor-snapshot.json")
    receipt = load("anchor-audit-receipt.json")

    assert audit["item_id"] == receipt["item_id"] == protocol["item_id"] == ITEM_ID
    assert audit["theorem_id"] == receipt["theorem_id"] == protocol["theorem_id"] == THEOREM_ID
    assert audit["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert audit["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert audit["canonical_target_expression_sha256"] == TARGET_SHA256
    assert receipt["canonical_target_expression_sha256"] == TARGET_SHA256
    assert audit["discovery_protocol"]["inventory_version"] == protocol["inventory_version"]
    assert receipt["inventory_version"] == protocol["inventory_version"]
    assert audit["root_decision"]["classification_after"] == "M3"
    assert audit["root_decision"]["kernel_closed"] is False
    assert audit["root_vector_before"] == audit["root_vector_after"]
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == audit["root_vector_after"]
    assert audit["audit_complete"] is receipt["audit_complete"] is False
    assert audit["theorem_complete"] is receipt["theorem_complete"] is False
    assert audit["gate_state"] == "self_tested_pending_master_acceptance"
    assert receipt["receipt_state"] == "provisional_pending_master_acceptance"
    assert receipt["accepted_receipt_ids"] == []

    assert output("git", "rev-parse", "HEAD", cwd=ROOT) == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=ROOT) == BASE_TREE
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=MATHLIB) == ""

    assert output("git", "cat-file", "-t", CANDIDATE_REVISION, cwd=MATHLIB) == "commit"
    assert output("git", "rev-parse", f"{CANDIDATE_REVISION}^{{tree}}", cwd=MATHLIB) == CANDIDATE_TREE
    candidate_source = subprocess.check_output(
        ["git", "show", f"{CANDIDATE_REVISION}:{CANDIDATE_PATH}"], cwd=MATHLIB
    )
    assert sha256(candidate_source) == CANDIDATE_SHA256
    candidate_text = candidate_source.decode("utf-8")
    assert "lemma schur_triangulation" in candidate_text
    assert "A = A.schurTriangulationUnitary * A.schurTriangulation * star" in candidate_text
    assert "noncomputable def schurTriangulationUnitary : unitaryGroup" in candidate_text
    assert "noncomputable def schurTriangulation : UpperTriangular" in candidate_text
    prohibited = re.compile(r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe)\b")
    assert prohibited.search(candidate_text) is None

    external = next(c for c in audit["candidates"] if c["id"] == "M0045-A-MATHLIB-BRANCH-SCHUR")
    spectral = next(c for c in audit["candidates"] if c["id"] == "M0045-A-MATHLIB-HERMITIAN-SPECTRAL")
    assert external["revision"] == snapshot["revision"] == CANDIDATE_REVISION
    assert external["tree_revision"] == snapshot["tree_revision"] == CANDIDATE_TREE
    assert external["source_file_sha256"] == snapshot["file_sha256"] == CANDIDATE_SHA256
    assert external["classification"] == receipt["external_candidate_classification"] == "M5"
    assert external["local_dependency_closure"] is False
    assert spectral["classification"] == "M5"
    assert "strict specialization" in spectral["result"].lower() or "Statement mismatch" in spectral["result"]
    assert snapshot["local_replay_at_current_pin"]["exit"] == 1
    assert snapshot["toolchain"] != audit["immutable_environment"]["lean_toolchain"]

    statement = (HERE / "Statement.lean").read_text(encoding="utf-8")
    assert "def SchurTriangularizationTarget : Prop" in statement
    probe = (HERE / "AnchorAudit.lean").read_text(encoding="utf-8")
    assert "theorem equationCandidate_implies_targetAt" in probe
    assert prohibited.search(probe) is None
    result = run_lean("AnchorAudit.lean")
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    assert "sorryAx" not in result.stdout
    assert result.stdout.count("depends on axioms") == 6

    item = next(
        row for row in json.loads((ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text())["items"]
        if row["id"] == ITEM_ID
    )
    assert (item["theorem_id"], item["phase"], item["layer"]) == (THEOREM_ID, "anchor_audit", 2)
    assert item["depends_on"] == ["S56-M-0045-STATEMENT"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"]

    packet = json.loads(args.worker_packet.read_text(encoding="utf-8"))
    expected_fields = {
        "item_id", "changed_paths", "commands", "output_summary", "base_revision",
        "known_failures", "state",
    }
    assert set(packet) == expected_fields
    assert packet["item_id"] == ITEM_ID and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    required_changes = {
        "Stage1_Instances/THM-M-0045/AnchorAudit.lean",
        "Stage1_Instances/THM-M-0045/anchor-discovery-protocol.json",
        "Stage1_Instances/THM-M-0045/external-anchor-snapshot.json",
        "Stage1_Instances/THM-M-0045/anchor-audit.json",
        "Stage1_Instances/THM-M-0045/anchor-audit-validation.md",
        "Stage1_Instances/THM-M-0045/anchor-audit-receipt.json",
        "Stage1_Instances/THM-M-0045/check_anchor_audit.py",
        ".stage1-worker-selftest.json",
    }
    assert set(packet["changed_paths"]) == required_changes
    assert packet["known_failures"] == receipt["known_failures"]
    print(
        "anchor audit verified: exact target M3; pinned interfaces checked; immutable mathlib "
        f"branch candidate {CANDIDATE_REVISION} classified M5/E3; no proof completion"
    )


if __name__ == "__main__":
    main()
