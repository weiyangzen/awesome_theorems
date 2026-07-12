#!/usr/bin/env python3
"""Fail-closed worker validator for S56-M-0529-VALIDATION."""

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0529"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, cwd=ROOT) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


expected = {
    "Statement.lean": "3e40221253a26e8c00fe59a84cf516f01fdcce7fbeb6e8d1b4aaba3b11590ff9",
    "Proof.lean": "e4a6e1b92400be30200d8d5f7e123e2418786f6a54a268fb78dcd2b96d21c275",
    "obligation-registry.json": "5deb94546a10e344c81ca82dde8624c23aad2e337b89084139ea6c07b105bfb7",
    "typed-graphs.json": "b923f8125084c535b609980af687daabf8e014a82b1728438dd68dff7bf10ee8",
    "proof-receipt.json": "e6f462f778614a0b93041b334173edac187d388ffed71f798f900024c8ea4c29",
}
for name, wanted in expected.items():
    actual = digest(HERE / name)
    if actual != wanted:
        raise SystemExit(f"validation failed: stale {name}: expected {wanted}, got {actual}")

if digest(LEAN_ROOT / "lean-toolchain") != "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2":
    raise SystemExit("validation failed: Lean toolchain pin changed")
if digest(LEAN_ROOT / "lake-manifest.json") != "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81":
    raise SystemExit("validation failed: Lake manifest pin changed")

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
if run(["git", "rev-parse", "HEAD"], mathlib).strip() != "8a178386ffc0f5fef0b77738bb5449d50efeea95":
    raise SystemExit("validation failed: mathlib revision changed")
if run(["git", "status", "--short"], mathlib):
    raise SystemExit("validation failed: pinned mathlib worktree is dirty")

instance = json.loads((HERE / "instance.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
receipt = json.loads((HERE / "proof-receipt.json").read_text())
ids = {row["obligation_id"] for row in registry["obligations"]}
if instance["theorem_id"] != "THM-M-0529" or registry["root_obligation_id"] != "M0529-ROOT":
    raise SystemExit("validation failed: theorem or root identity mismatch")
if ids != {row["obligation_id"] for row in graphs["nodes"]} or len(ids) != 7:
    raise SystemExit("validation failed: frozen registry/graph denominator mismatch")
closed = set(receipt["closed_machine_obligations"])
required = {"M0529-ROOT", "M0529-C-MAP", "M0529-B-HOMEO", "M0529-B-FUNCTOR", "M0529-S-STATEMENT"}
if closed != required or receipt["theorem_complete"] is not False:
    raise SystemExit("validation failed: proof closure boundary mismatch")

prohibited = re.compile(r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE)
for name in ("Statement.lean", "Proof.lean", "Validation.lean"):
    source = (HERE / name).read_text()
    code = "\n".join(line for line in source.splitlines() if not line.lstrip().startswith(("--", "/-", "*")))
    if prohibited.search(code):
        raise SystemExit(f"validation failed: prohibited trust token in {name}")

proof_output = run(["lake", "env", "lean", "../../Stage1_Instances/THM-M-0529/Proof.lean"], LEAN_ROOT)
probe_output = run(["lake", "env", "lean", "../../Stage1_Instances/THM-M-0529/Validation.lean"], LEAN_ROOT)
for label, output in (("proof", proof_output), ("independent probe", probe_output)):
    if "sorryAx" in output:
        raise SystemExit(f"validation failed: {label} axiom report contains sorryAx")
    for axiom in ("propext", "Classical.choice", "Quot.sound"):
        if axiom not in output:
            raise SystemExit(f"validation failed: {label} omitted expected axiom {axiom}")

topcat_source = mathlib / "Mathlib" / "Topology" / "Category" / "TopCat" / "Basic.lean"
iso_source = mathlib / "Mathlib" / "CategoryTheory" / "Iso.lean"
if digest(topcat_source) != "f3a4abd6a77e9ddc999306c2ed62535075a137474553fbdc837f3f05f15252d4":
    raise SystemExit("validation failed: TopCat.isoOfHomeo provenance source changed")
if digest(iso_source) != "12b67503207b201a82e66ff59ea597aa06d4ad9f50913266535d9cc924101bf4":
    raise SystemExit("validation failed: Functor.map_isIso provenance source changed")

print("validation ok: exact proof and independent target reconstruction kernel-elaborated")
print("validation ok: frozen hashes, 7-node denominator, dependency pins, provenance, and placeholder/trust scans passed")
print("axioms: propext, Classical.choice, Quot.sound; no sorryAx")
print("boundary: warm shared dependency cache and same checkout are not release-hermetic or distinct-runner independent evidence")
