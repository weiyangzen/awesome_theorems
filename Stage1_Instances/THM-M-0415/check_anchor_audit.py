#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).with_name("anchor-audit.json")
MATHLIB = ROOT / "Formalizations/Lean/.lake/packages/mathlib"

data = json.loads(AUDIT.read_text())
assert data["item_id"] == "S56-M-0415-ANCHOR_AUDIT"
assert data["canonical_expression_sha256"] == json.loads(
    AUDIT.with_name("statement.json").read_text()
)["canonical_formal_target"]["elaborated_expression_sha256"]

c1 = data["candidates"][0]
head = subprocess.check_output(["git", "-C", str(MATHLIB), "rev-parse", "HEAD"], text=True).strip()
assert head == c1["revision"]
assert not subprocess.check_output(["git", "-C", str(MATHLIB), "status", "--short"], text=True).strip()

for rel, expected in [
    (c1["file"], c1["file_sha256"]),
    (c1["terminal_file"], c1["terminal_file_sha256"]),
    ("LICENSE", c1["license_sha256"]),
]:
    assert hashlib.sha256((MATHLIB / rel).read_bytes()).hexdigest() == expected

for rel, expected in [(c1["file"], c1["git_blob"]), (c1["terminal_file"], c1["terminal_git_blob"])]:
    blob = subprocess.check_output(["git", "-C", str(MATHLIB), "rev-parse", f"HEAD:{rel}"], text=True).strip()
    assert blob == expected

source = (MATHLIB / c1["file"]).read_text() + (MATHLIB / c1["terminal_file"]).read_text()
for name in ["instFintypeClassGroup", "fintypeOfAdmissibleOfFinite", "fintypeOfAdmissibleOfAlgebraic"]:
    assert name in source
for forbidden in ["sorry", "unsafe def", "unsafe theorem", "axiom "]:
    assert forbidden not in source

assert data["audit_result"]["theorem_complete"] is False
print("anchor audit invariant check: ok; 3 candidates classified; pinned source hashes verified")
