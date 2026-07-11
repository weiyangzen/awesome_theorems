#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0388"
MATHLIB = ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads((OWNED / "anchor-audit.json").read_text())
assert audit["theorem_id"] == "THM-M-0388"
assert audit["item_id"] == "S56-M-0388-ANCHOR_AUDIT"
assert audit["canonical_target"] == "Stage1Instances.THMM0388.PellEquationStatement"
assert len({c["candidate_id"] for c in audit["candidates"]}) == len(audit["candidates"])

candidate = audit["candidates"][0]
assert subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip() == candidate["revision"]
assert subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD^{tree}"], text=True
).strip() == candidate["tree"]
assert sha256(MATHLIB / candidate["file"]) == candidate["file_sha256"]
assert sha256(MATHLIB / "LICENSE") == candidate["license_sha256"]

source = (MATHLIB / candidate["file"]).read_text()
assert "theorem exists_of_not_isSquare" in source
assert "∃ x y : ℤ, x ^ 2 - d * y ^ 2 = 1 ∧ y ≠ 0" in source
assert "theorem exists_iff_not_isSquare" in source
assert "theorem existsUnique_pos_generator" in source

adapter = (OWNED / "AnchorAudit.lean").read_text()
statement = (OWNED / "Statement.lean").read_text()
assert "¬ ∃ k : Int, k * k = D" in statement
assert "¬ ∃ k : Int, k * k = D" in adapter
assert "theorem isNonsquareInteger_iff_not_isSquare" in adapter
assert "theorem pellEquationStatement_mathlib_candidate" in adapter
assert "Pell.exists_of_not_isSquare" in adapter

assert audit["audit_result"]["root_machine_debt"] == "M3"
assert audit["audit_result"]["candidate_kernel_checked"] is False
assert audit["audit_result"]["theorem_complete"] is False
print("check_anchor_audit: ok (3 candidates classified; exact mathlib source anchor and hashes verified; kernel closure blocked)")
