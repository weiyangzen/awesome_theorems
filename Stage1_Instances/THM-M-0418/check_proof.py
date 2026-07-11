#!/usr/bin/env python3
"""Fail-closed source checks for the THM-M-0418 proof phase."""

from pathlib import Path
import hashlib
import re

root = Path(__file__).resolve().parent
proof = root / "Proof.lean"
source = proof.read_text(encoding="utf-8")

assert "theorem minkowskiIdealClassBound_proof : MinkowskiIdealClassBound.{u}" in source
assert "exact NumberField.exists_ideal_in_class_of_norm_le C" in source
assert "theorem pinnedMathlibSourceShape_proof : PinnedMathlibSourceShape.{u}" in source
assert "minkowskiIdealClassBound_iff_pinnedMathlibSourceShape.mp" in source

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)[ \t]",
    re.MULTILINE,
)
assert prohibited.search(source) is None, "placeholder, axiom, or unsafe declaration found"

digest = hashlib.sha256(proof.read_bytes()).hexdigest()
assert digest == "84857a936c29627de8a6c3c79b1a4076b8595a610bbac2f4f244235f455e2b1d"
print("PASS THM-M-0418 proof: exact pinned-mathlib adapter and statement transport present")
