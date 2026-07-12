#!/usr/bin/env python3
"""Verify the immutable local and remote evidence in the anchor-audit ledger."""

import hashlib
import json
from pathlib import Path
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
LEAN = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN / ".lake" / "packages" / "mathlib"
AUDIT_PATH = Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(data: bytes, needle: bytes, label: str) -> None:
    if needle not in data:
        raise SystemExit(f"missing {label}: {needle.decode(errors='replace')}")


def remote(project: str, revision: str, path: str) -> bytes:
    url = f"https://raw.githubusercontent.com/{project}/{revision}/{path}"
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read()


audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]

computable = MATHLIB / "Mathlib/Computability/TuringMachine/Computable.lean"
reduce = MATHLIB / "Mathlib/Computability/Reduce.lean"
assert digest(computable.read_bytes()) == env["computable_source_sha256"]
assert digest(reduce.read_bytes()) == env["reduce_source_sha256"]
require(computable.read_bytes(), b"structure TM2ComputableInPolyTime", "TM2 polynomial-time substrate")
require(computable.read_bytes(), b"proof_wanted TM2ComputableInPolyTime.comp", "open composition endpoint")
require(reduce.read_bytes(), b"def ManyOneReducible", "computable reduction anchor")

candidates = {candidate["candidate_id"]: candidate for candidate in audit["candidates"]}

ae = candidates["S56-M-0721-C03"]
ae_source = remote(ae["project"], ae["revision"], "Cook-Levin-Lean4.lean")
assert digest(ae_source) == ae["source_sha256"]
require(ae_source, b"theorem cook_levin_final_soundness", "AEjon terminal theorem")
assert b"def NPcomplete" not in ae_source and b"IsNPComplete" not in ae_source
assert b"sorry" not in ae_source and b"axiom " not in ae_source
assert remote(ae["project"], ae["revision"], "toolchain-lean").decode().strip() == ae["toolchain"]

dom = candidates["S56-M-0721-C04"]
dom_source = remote(dom["project"], dom["revision"], "CookLevin/Complexity/NP/SAT/CookLevin.lean")
dom_readme = remote(dom["project"], dom["revision"], "README.md")
dom_np = remote(dom["project"], dom["revision"], "CookLevin/Complexity/Complexity/NP.lean")
assert digest(dom_source) == dom["source_sha256"]
require(dom_source, b"theorem CookLevin : NPcomplete SAT", "Dominic headline theorem")
require(dom_readme, b"does depend on `sorryAx`", "Dominic reported axiom dependency")
require(dom_readme, b"NOT yet a faithful proof", "Dominic fidelity warning")
require(dom_np, b"def NPcomplete", "Dominic NP-completeness definition")
require(dom_np, b"sorry", "Dominic built-code gap")

atlas = candidates["S56-M-0721-C05"]
atlas_source = remote(atlas["project"], atlas["revision"], "Atlas/TheoryOfComputation/code/NPCompleteness.lean")
assert digest(atlas_source) == atlas["source_sha256"]
require(atlas_source, b"theorem cook_levin : IsNPComplete SATLang", "Atlas headline theorem")
for declaration in (
    b"theorem tableau_from_accepting_branch",
    b"theorem buildTableauFormula_correct",
    b"theorem cookLevinReductionFn_polyTime",
):
    require(atlas_source, declaration, "Atlas root-relevant declaration")
assert atlas_source.count(b"sorry") >= 5

assert audit["root_decision"]["classification"] == "M2"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["theorem_complete"] is False
print("anchor audit verified: local pins/hashes and three immutable external candidates match; root=M2")
