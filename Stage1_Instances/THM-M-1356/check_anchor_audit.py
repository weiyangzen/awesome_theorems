#!/usr/bin/env python3
"""Verify immutable anchors and fail-closed classifications for THM-M-1356."""

import json
from pathlib import Path
import hashlib
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
AUDIT = HERE / "anchor-audit.json"
RECEIPT = HERE / "anchor-audit-receipt.json"


def output(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = json.loads(packet_path.read_text(encoding="utf-8")) if packet_path.exists() else None
    assert audit["item_id"] == "S56-M-1356-ANCHOR_AUDIT"
    assert audit["theorem_id"] == "THM-M-1356"
    assert audit["canonical_target"] == (
        "Stage1Instances.THM_M_1356.RouthHurwitzTarget"
    )
    assert audit["discovery_protocol_frozen_at"] < audit["audit_cutoff"]
    assert audit["external_candidates"] == []
    assert len(audit["candidates"]) == 3
    local_candidate, support_candidate, catalog_candidate = audit["candidates"]
    assert local_candidate["terminal_declaration"] is None
    assert local_candidate["terminal_proof_body"] is None
    assert support_candidate["classification"] == "M3_support_only"
    assert support_candidate["license"] == "Apache-2.0"
    assert catalog_candidate["classification"] == "not_a_formal_candidate"
    assert len(audit["mathematical_source_anchors"]) == 3
    assert all(
        "not_a_Lean" in source["classification"]
        for source in audit["mathematical_source_anchors"]
    )
    assert audit["root_decision"]["classification"] == "M3"
    assert audit["root_decision"]["kernel_closed"] is False
    assert audit["audit_complete"] is False
    assert audit["theorem_complete"] is False
    assert audit["gate_state"] == "self_tested_pending_master_acceptance"
    assert receipt["item_id"] == audit["item_id"]
    assert receipt["theorem_id"] == audit["theorem_id"]
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False
    assert receipt["formal_candidate_summary"]["classification"] == "M3"
    assert receipt["audit_complete"] is False
    assert receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []

    environment = audit["immutable_environment"]
    assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == environment[
        "mathlib_revision"
    ]
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=MATHLIB) == environment[
        "mathlib_tree"
    ]
    assert output("git", "status", "--short", cwd=MATHLIB) == ""
    assert environment["mathlib_license"] == "Apache-2.0"
    assert output("git", "rev-parse", "HEAD:LICENSE", cwd=MATHLIB) == environment[
        "mathlib_license_blob"
    ]

    statement = (HERE / "Statement.lean").read_text(encoding="utf-8")
    assert "noncomputable def RouthHurwitzTarget : Prop" in statement
    assert "theorem routhHurwitzTarget_iff_expandedTarget" in statement

    topic = re.compile(
        r"routh|hurwitz.(?:matrix|determinant|criterion)|"
        r"hermite.biehler|lienard.chipart|stable polynomial",
        re.IGNORECASE,
    )
    mathlib_hits = []
    for path in (MATHLIB / "Mathlib").rglob("*.lean"):
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if topic.search(line):
                mathlib_hits.append(f"{path.relative_to(MATHLIB)}:{line_number}:{line}")
    assert mathlib_hits == [], "unexpected pinned-mathlib candidate:\n" + "\n".join(
        mathlib_hits
    )

    catalog = (MATHLIB / "docs" / "1000.yaml").read_text(encoding="utf-8")
    assert "Q4455015:\n  title: Routh-Hurwitz theorem" in catalog.replace("–", "-")

    local_hits = []
    for path in ROOT.rglob("*.lean"):
        if MATHLIB in path.parents or HERE in path.parents:
            continue
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if topic.search(line):
                local_hits.append(f"{path.relative_to(ROOT)}:{line_number}:{line}")
    assert local_hits == [], "unexpected repo-local candidate:\n" + "\n".join(
        local_hits
    )

    external = {entry["surface"] for entry in audit["external_searches"]}
    assert external == {
        "Sourcegraph public Lean index",
        "GitHub REST repository search",
        "GitHub REST code search",
        "grep.app public index",
    }
    sourcegraph = [
        entry
        for entry in audit["external_searches"]
        if entry["surface"] == "Sourcegraph public Lean index"
    ]
    assert len(sourcegraph) == 2
    assert all("matchCount=0" in entry["result"] for entry in sourcegraph)
    assert all("not global saturation" in entry["boundary"] for entry in sourcegraph)

    expected_changed = {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-1356/AnchorAudit.lean",
        "Stage1_Instances/THM-M-1356/README.md",
        "Stage1_Instances/THM-M-1356/anchor-audit-validation.md",
        "Stage1_Instances/THM-M-1356/anchor-audit-receipt.json",
        "Stage1_Instances/THM-M-1356/anchor-audit.json",
        "Stage1_Instances/THM-M-1356/anchor-audit.md",
        "Stage1_Instances/THM-M-1356/check_anchor_audit.py",
    }
    assert set(receipt["changed_paths"]) == expected_changed
    if packet is not None:
        assert packet["item_id"] == audit["item_id"]
        assert packet["state"] == "[_]"
        assert set(packet["changed_paths"]) == expected_changed
        assert packet["base_revision"] == receipt["base_revision"]
    for relative, expected in receipt["artifact_hashes_before_receipt_and_packet"].items():
        actual = "sha256:" + hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected, f"artifact hash mismatch: {relative}"

    print(
        "anchor audit verified: exact local statement only; pinned mathlib topic "
        "inventory empty; external candidate inventory empty; root=M3"
    )


if __name__ == "__main__":
    main()
