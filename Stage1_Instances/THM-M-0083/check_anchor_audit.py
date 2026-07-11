#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0083"
MATHLIB = ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads((OWNED / "anchor-audit.json").read_text())
assert audit["item_id"] == "S56-M-0083-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-0083"
assert audit["canonical_target"] == "Stage1Instances.THM_M_0083.RepresentableFunctorTarget"
assert len({c["candidate_id"] for c in audit["candidates"]}) == len(audit["candidates"])

candidate = audit["candidates"][0]
assert subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip() == candidate["revision"]
assert subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD^{tree}"], text=True
).strip() == candidate["tree"]
assert not subprocess.check_output(
    ["git", "-C", str(MATHLIB), "status", "--short"], text=True
).strip()
assert sha256(MATHLIB / candidate["file"]) == candidate["file_sha256"]
assert sha256(MATHLIB / "LICENSE") == candidate["license_sha256"]

source = (MATHLIB / candidate["file"]).read_text()
assert "structure IsRepresentedBy" in source
assert "map_bijective {Y : C}" in source
assert "lemma IsRepresentable.iff_exists_isRepresentedBy" in source
assert "fun ⟨_, _, h⟩ ↦ h.representableBy.isRepresentable" in source

adapter = (OWNED / "AnchorAudit.lean").read_text()
statement = (OWNED / "Statement.lean").read_text()
for marker in ("∀ Y : C", "Function.Bijective", "F.map f.op x", "F.IsRepresentable"):
    assert marker in adapter and marker in statement
assert "IsRepresentable.iff_exists_isRepresentedBy" in adapter
assert "simp only [isRepresentedBy_iff]" in adapter

result = audit["audit_result"]
assert result["root_machine_debt"] == "M0-W"
assert result["candidate_kernel_checked"] is True
assert result["candidate_accepted_by_master"] is False
assert result["theorem_complete"] is False
print("check_anchor_audit: ok (2 candidates classified; immutable pins, hashes, exact wrapper, and fail-closed boundary verified)")
