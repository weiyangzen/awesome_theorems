#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0414"
MATHLIB = ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads((OWNED / "anchor-audit.json").read_text())
assert audit["item_id"] == "S56-M-0414-ANCHOR_AUDIT"
assert audit["canonical_target"] == "Stage1Instances.THM_M_0414.IdealUniqueFactorizationTarget"
assert len({c["candidate_id"] for c in audit["candidates"]}) == len(audit["candidates"])

for candidate in audit["candidates"][:2]:
    assert subprocess.check_output(
        ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
    ).strip() == candidate["revision"]
    assert subprocess.check_output(
        ["git", "-C", str(MATHLIB), "rev-parse", "HEAD^{tree}"], text=True
    ).strip() == candidate["tree"]
    assert sha256(MATHLIB / candidate["file"]) == candidate["file_sha256"]
    assert sha256(MATHLIB / "LICENSE") == candidate["license_sha256"]

basic = (MATHLIB / audit["candidates"][0]["file"]).read_text()
factorization = (MATHLIB / audit["candidates"][1]["file"]).read_text()
assert "instance Ideal.uniqueFactorizationMonoid" in basic
assert "theorem finprod_heightOneSpectrum_factorization {I : Ideal R}" in factorization
assert "apply Associates.eq_of_eq_counts" in factorization

adapter = (OWNED / "AnchorAudit.lean").read_text()
statement = (OWNED / "Statement.lean").read_text()
target_body = """def IdealUniqueFactorizationTarget : Prop :=
  ∀ (R : Type u) [CommRing R] [IsDedekindDomain R],
    UniqueFactorizationMonoid (Ideal R) ∧
      ∀ {I : Ideal R}, I ≠ 0 →
        ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R, v.maxPowDividing I = I"""
assert target_body in statement
assert target_body in adapter
assert "theorem idealUniqueFactorization_mathlib_candidate" in adapter
assert "IdealUniqueFactorizationTarget.{u}" in adapter
assert "Ideal.finprod_heightOneSpectrum_factorization hI" in adapter
assert "#print axioms Ideal.uniqueFactorizationMonoid" in adapter
assert "#print axioms Ideal.finprod_heightOneSpectrum_factorization" in adapter

result = audit["audit_result"]
assert result["candidate_kernel_checked"] is True
assert result["root_machine_debt"] == "M2"
assert result["theorem_complete"] is False
print("check_anchor_audit: ok (3 candidates classified; 2 immutable mathlib terminal anchors and exact adapter verified)")
