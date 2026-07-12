#!/usr/bin/env python3
"""Validate the THM-M-0645 anchor-audit receipt and its pinned local anchors."""

from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OWNED = Path(__file__).resolve().parent
LEAN = ROOT / "Formalizations" / "Lean"


def git(*args: str, cwd: Path) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout.strip()


def main() -> None:
    audit = json.loads((OWNED / "anchor-audit.json").read_text())
    assert audit["item_id"] == "S56-M-0645-ANCHOR_AUDIT"
    assert audit["theorem_id"] == "THM-M-0645"
    assert audit["canonical_target"] == "Stage1Instances.THM_M_0645.CompletenessTarget"
    assert audit["decision"]["audit_complete"] is True
    assert audit["decision"]["theorem_complete"] is False
    assert audit["decision"]["selected_proof_anchor"] is None
    assert audit["decision"]["machine_status"] == "not_repo_local_closed"
    assert audit["decision"]["gate_state"] == "self_tested_pending_master_acceptance"

    candidates = {row["id"]: row for row in audit["candidates"]}
    assert set(candidates) == {
        "A-MATHLIB-SEMANTICS", "A-LOCAL-CRAIG-KERNEL", "A-FOUNDATION-FOL"
    }
    assert candidates["A-FOUNDATION-FOL"]["classification"] == "external_upstream_anchor_only"
    assert all(not row["exact_target"] for row in candidates.values())

    manifest = json.loads((LEAN / "lake-manifest.json").read_text())
    mathlib_rev = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
    assert mathlib_rev == candidates["A-MATHLIB-SEMANTICS"]["revision"]
    assert git("rev-parse", "HEAD", cwd=LEAN / ".lake" / "packages" / "mathlib") == mathlib_rev

    statement = json.loads((OWNED / "statement.json").read_text())
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == audit[
        "canonical_target_expression_sha256"
    ]
    local_source = ROOT / candidates["A-LOCAL-CRAIG-KERNEL"]["modules"][0]
    local_text = local_source.read_text()
    assert "structure SemanticToDerivabilityBridge" in local_text
    assert "no inhabitant of `SemanticToDerivabilityBridge`" in local_text

    source_hash = candidates["A-FOUNDATION-FOL"]["source_sha256"]
    assert len(source_hash) == 64 and all(c in "0123456789abcdef" for c in source_hash)
    digest = hashlib.sha256((OWNED / "anchor-audit.json").read_bytes()).hexdigest()
    print(f"anchor audit check: ok; receipt_sha256={digest}; mathlib={mathlib_rev}")


if __name__ == "__main__":
    main()
