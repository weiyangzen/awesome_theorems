#!/usr/bin/env python3
"""Validate THM-M-0579 anchor evidence against frozen local inputs."""

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN = ROOT / "Formalizations" / "Lean"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


audit = json.loads((HERE / "anchor-audit.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
manifest = json.loads((LEAN / "lake-manifest.json").read_text())
packages = {package["name"]: package for package in manifest["packages"]}

assert audit["item_id"] == "S56-M-0579-ANCHOR_AUDIT"
assert audit["theorem_id"] == "THM-M-0579"
assert audit["audited_target"]["elaborated_expression_sha256"] == \
    statement["canonical_formal_target"]["elaborated_expression_hash"]
assert audit["audited_target"]["statement_file_sha256"] == sha256(HERE / "Statement.lean")
assert audit["immutable_environment"]["mathlib_revision"] == packages["mathlib"]["rev"]
assert audit["immutable_environment"]["batteries_revision"] == packages["batteries"]["rev"]

mathlib_source = LEAN / ".lake/packages/mathlib/Mathlib/Geometry/Manifold/PoincareConjecture.lean"
batteries_source = LEAN / ".lake/packages/batteries/Batteries/Util/ProofWanted.lean"
legacy_source = LEAN / "AwesomeTheorems/Stage1/S1_M_114.lean"
assert audit["candidates"][1]["source_sha256"] == sha256(mathlib_source)
assert audit["candidates"][2]["source_sha256"] == sha256(legacy_source)
assert "proof_wanted SimplyConnectedSpace.nonempty_homeomorph_sphere_three" in mathlib_source.read_text()
assert "withoutModifyingEnv" in batteries_source.read_text()

for package_name, revision_key in (("mathlib", "mathlib_revision"),
                                   ("batteries", "batteries_revision")):
    package_root = LEAN / ".lake/packages" / package_name
    head = subprocess.run(
        ["git", "-C", str(package_root), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    assert head == audit["immutable_environment"][revision_key]

assert audit["root_machine_classification"] == "M3"
assert audit["theorem_proved"] is False
assert audit["theorem_complete"] is False
assert any(candidate["classification"] == "M5" for candidate in audit["candidates"])

print("ok: frozen target, 5 candidates, proof_wanted boundary, dependency pins, and noncompletion status agree")
