#!/usr/bin/env python3
from pathlib import Path

HERE = Path(__file__).resolve().parent
proof = (HERE / "Proof.lean").read_text()

required = (
    "import Statement",
    "theorem normalization_open",
    "infer_instance",
    "theorem normalization_equation",
    "f.toNormalization_fromNormalization",
    "theorem exactTarget_of_normalization_finite",
    "finiteFactor :",
    "ZariskiMainFactorizationTarget",
    "normalization_open f, finiteFactor f, normalization_equation f",
)
for fragment in required:
    assert fragment in proof, f"missing proof fragment: {fragment}"

for forbidden in ("sorry", "admit", "sorryAx", "axiom ", "unsafe "):
    assert forbidden not in proof, f"forbidden proof token: {forbidden!r}"

print("PASS THM-M-0107 proof phase: open factor, equation, and conditional exact-root assembly checked")
print("root remains open: finiteness of the normalization envelope is an explicit premise")
