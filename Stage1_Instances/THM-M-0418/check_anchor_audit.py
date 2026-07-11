#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = Path(__file__).resolve().parent
MATHLIB = ROOT / "Formalizations/Lean/.lake/packages/mathlib"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads((OWNED / "anchor-audit.json").read_text())
statement = json.loads((OWNED / "statement.json").read_text())
manifest = json.loads((ROOT / "Formalizations/Lean/lake-manifest.json").read_text())

assert audit["item_id"] == "S56-M-0418-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-0418"
assert audit["canonical_statement_sha256"] == statement["canonical_formal_target"]["elaborated_expression_sha256"]
assert len({c["candidate_id"] for c in audit["candidates"]}) == len(audit["candidates"])

candidate = audit["candidates"][0]
mathlib_pin = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
assert candidate["revision"] == mathlib_pin
assert subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip() == candidate["revision"]
assert subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD^{tree}"], text=True
).strip() == candidate["tree"]
assert not subprocess.check_output(
    ["git", "-C", str(MATHLIB), "status", "--porcelain"], text=True
).strip()
assert sha256(MATHLIB / candidate["file"]) == candidate["file_sha256"]
assert sha256(MATHLIB / "LICENSE") == candidate["license_sha256"]

source = (MATHLIB / candidate["file"]).read_text()
body = source[source.index("theorem exists_ideal_in_class_of_norm_le"):source.index("end NumberField")]
assert ":= by" in body
for forbidden in ("sorry", "axiom ", "unsafe ", "@[extern", "implemented_by"):
    assert forbidden not in body

adapter = (OWNED / "AnchorAudit.lean").read_text()
assert "theorem minkowskiIdealClassBound_mathlibAnchor" in adapter
assert "exact NumberField.exists_ideal_in_class_of_norm_le C" in adapter
assert "#print axioms NumberField.exists_ideal_in_class_of_norm_le" in adapter
assert "propext, Classical.choice, and Quot.sound" in candidate["placeholder_unsafe_oracle_audit"]
assert audit["audit_result"]["root_machine_debt"] == "M0-W"
assert audit["audit_result"]["candidate_kernel_checked"] is True
assert audit["audit_result"]["theorem_complete"] is False

print("check_anchor_audit: ok (exact M0-W candidate, immutable pin/tree/source, clean dependency, body and wrapper boundary verified)")
