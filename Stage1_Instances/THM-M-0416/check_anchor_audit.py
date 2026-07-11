#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNED = ROOT / "Stage1_Instances" / "THM-M-0416"
MATHLIB = ROOT / "Formalizations" / "Lean" / ".lake" / "packages" / "mathlib"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads((OWNED / "anchor-audit.json").read_text())
assert audit["item_id"] == "S56-M-0416-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-0416"
assert audit["canonical_target"] == "Stage1Instances.THM_M_0416.DirichletUnitTheoremTarget"
assert len({candidate["candidate_id"] for candidate in audit["candidates"]}) == len(audit["candidates"])

candidate = audit["candidates"][0]
manifest = json.loads((ROOT / "Formalizations" / "Lean" / "lake-manifest.json").read_text())
mathlib_pin = next(package for package in manifest["packages"] if package["name"] == "mathlib")["rev"]
assert candidate["revision"] == mathlib_pin
assert subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True
).strip() == candidate["revision"]
assert subprocess.check_output(
    ["git", "-C", str(MATHLIB), "rev-parse", "HEAD^{tree}"], text=True
).strip() == candidate["tree"]
assert sha256(MATHLIB / candidate["file"]) == candidate["file_sha256"]
assert sha256(MATHLIB / "LICENSE") == candidate["license_sha256"]

source = (MATHLIB / candidate["file"]).read_text()
for declaration in candidate["declarations"]:
    short_name = declaration.rsplit(".", 1)[-1]
    assert f"theorem {short_name}" in source
adapter = (OWNED / "AnchorAudit.lean").read_text()
for declaration in candidate["declarations"]:
    assert declaration in adapter
assert "theorem dirichletUnitTheorem_mathlib_candidate" in adapter
assert "#print axioms dirichletUnitTheorem_mathlib_candidate" in adapter

for forbidden in ("sorry", "native_decide", "unsafe", "external "):
    assert forbidden not in adapter
assert audit["audit_result"]["root_machine_debt_after_this_node"] == "M3"
assert audit["audit_result"]["candidate_kernel_checked"] is True
assert audit["audit_result"]["theorem_complete"] is False
print("check_anchor_audit: ok (exact pinned mathlib route, immutable hashes, adapter probes, and status boundary verified)")
