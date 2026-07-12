#!/usr/bin/env python3
"""Fail-closed narrow validation for THM-M-0707 worker evidence."""

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_DIR = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_DIR / ".lake" / "packages" / "mathlib"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, cwd=ROOT) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=60
    )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
anchor = json.loads((HERE / "anchor-audit.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
manifest = json.loads((LEAN_DIR / "lake-manifest.json").read_text())

assert spec["item_id"] == "S56-M-0707-VALIDATION"
assert spec["theorem_id"] == "THM-M-0707"
for recipe in spec["recipes"]:
    assert isinstance(recipe["argv"], list) and recipe["argv"]
    assert recipe["network_policy"] == "denied"
    assert recipe["expected_exit"] == 0
    assert 0 < recipe["timeout_seconds"] <= 60

assert proof_receipt["item_id"] == "S56-M-0707-PROOF"
assert proof_receipt["result"]["root_closed"] is True
assert proof_receipt["result"]["theorem_complete"] is False
assert proof_receipt["proof_body"]["source_sha256"] == sha(HERE / "Proof.lean")
assert proof_receipt["inputs"]["statement_sha256"] == sha(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_registry_sha256"] == sha(HERE / "obligation-registry.json")
assert statement["canonical_formal_target"]["statement_file_sha256"] == sha(HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == sha(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == sha(HERE / "anchor-audit.json")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

mathlib_pin = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
assert mathlib_pin == anchor["mathlib_revision"] == proof_receipt["environment"]["mathlib_revision"]
assert run(["git", "rev-parse", "HEAD"], MATHLIB).strip() == mathlib_pin
assert run(["git", "status", "--porcelain"], MATHLIB) == ""
halting_source = MATHLIB / "Mathlib" / "Computability" / "Halting.lean"
assert sha(halting_source) == anchor["candidates"][1]["source_sha256"]
source_text = halting_source.read_text()
assert re.search(r"theorem halting_problem \(n\).*\n\s*\| h => rice", source_text)

for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
    text = (HERE / name).read_text()
    forbidden = re.search(
        r"\b(sorry|admit|sorryAx)\b|^\s*(axiom|constant)\s|^\s*unsafe\s",
        text, re.MULTILINE
    )
    assert forbidden is None, f"forbidden declaration/token in {name}: {forbidden.group(0)}"
assert "import Proof" not in (HERE / "Validation.lean").read_text()
assert "import ObligationTree" not in (HERE / "Validation.lean").read_text()

lean_output = run(["bash", str(HERE / "check_validation.sh")], LEAN_DIR)
expected_declarations = (
    "codePairZero_computable",
    "fixedInputDecider_of_pairDecider",
    "haltingProblemUndecidable",
    "independentlyReconstructedHaltingProblemUndecidable",
)
for declaration in expected_declarations:
    assert declaration in lean_output, f"missing axiom output for {declaration}"
observed = set(re.findall(r"\b(?:propext|Classical\.choice|Quot\.sound)\b", lean_output))
assert observed == {"propext", "Classical.choice", "Quot.sound"}
assert "sorryAx" not in lean_output

print("PASS narrow kernel replay: exact proof root and separate Statement-only reconstruction elaborated")
print("PASS trust observation: declarations report only propext, Classical.choice, and Quot.sound")
print("PASS local provenance: frozen hashes, clean pinned mathlib source, manifest, and proof receipt agree")
print("PASS hygiene: no placeholder, local axiom/constant, or unsafe declaration")
print("OPEN hermetic release: shared warm canonical .lake is not an empty-cache cold offline replay")
print("OPEN independent release verification: differential reconstruction used this worker and shared cache")
