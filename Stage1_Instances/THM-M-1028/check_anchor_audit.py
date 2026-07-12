#!/usr/bin/env python3
"""Verify immutable local and external evidence for the THM-M-1028 audit."""

import hashlib
import json
import pathlib
import re
import subprocess
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
AUDIT = pathlib.Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: pathlib.Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"missing {label}: {needle}")


audit = json.loads(AUDIT.read_text(encoding="utf-8"))
env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""

gaussian = (MATHLIB / "Mathlib/Probability/Distributions/Gaussian/IsGaussianProcess/Basic.lean").read_text()
kolmogorov = (MATHLIB / "Mathlib/Probability/Process/Kolmogorov.lean").read_text()
require(gaussian, "lemma congr (hX : IsGaussianProcess", "Gaussian modification lemma")
require(gaussian, "lemma hasGaussianLaw_increments", "Gaussian increment lemma")
require(kolmogorov, "structure IsKolmogorovProcess", "Kolmogorov predicate")
require(kolmogorov, "def IsAEKolmogorovProcess", "AE Kolmogorov predicate")
assert "continuous modification" in kolmogorov
assert "Continuous" not in kolmogorov

external = next(c for c in audit["candidates"] if c["id"] == "M1028-A-BROWNIAN-MOTION")
base = f"https://raw.githubusercontent.com/RemyDegenne/brownian-motion/{external['revision']}"


def remote(path: str) -> bytes:
    request = urllib.request.Request(f"{base}/{path}", headers={"User-Agent": "stage1-anchor-audit"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


brownian_bytes = remote("BrownianMotion/Gaussian/BrownianMotion.lean")
brownian = brownian_bytes.decode()
require(brownian, "lemma IsPreBrownianReal.exists_continuous_modification", "continuous modification")
require(brownian, "lemma IsPreBrownianReal.continuous_mk", "continuous path endpoint")
require(brownian, "lemma isBrownianReal_brownian", "constructed Brownian process")
assert "nowhere" not in brownian.lower()
assert "differentiable" not in brownian.lower()
assert hashlib.sha256(brownian_bytes).hexdigest() == external["source_sha256"]
assert remote("lean-toolchain").decode().strip() == external["toolchain"]
manifest = json.loads(remote("lake-manifest.json"))
mathlib_pin = next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib")
assert mathlib_pin == external["mathlib_revision"]

tree_request = urllib.request.Request(
    f"https://api.github.com/repos/RemyDegenne/brownian-motion/git/trees/{external['revision']}?recursive=1",
    headers={"Accept": "application/vnd.github+json", "User-Agent": "stage1-anchor-audit"},
)
with urllib.request.urlopen(tree_request, timeout=30) as response:
    tree = json.load(response)["tree"]
sources: dict[str, str] = {}
for blob in tree:
    if blob["type"] == "blob" and blob["path"].endswith(".lean"):
        module = blob["path"][:-5].replace("/", ".")
        sources[module] = remote(blob["path"]).decode()

# Audit the local transitive import closure of the candidate module. Other,
# unrelated areas of this work-in-progress repository contain proof gaps.
seen: set[str] = set()
stack = ["BrownianMotion.Gaussian.BrownianMotion"]
while stack:
    module = stack.pop()
    if module in seen or module not in sources:
        continue
    seen.add(module)
    source = sources[module]
    assert re.search(r"\bsorry\b", source) is None
    assert re.search(r"^\s*axiom\s", source, re.MULTILINE) is None
    for dependency in re.findall(r"^(?:public )?import\s+([^\s]+)", source, re.MULTILINE):
        if dependency in sources:
            stack.append(dependency)
assert len(seen) == 25

assert audit["root_decision"]["classification"] == "M2"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["theorem_complete"] is False
print("anchor audit verified: pinned mathlib infrastructure and immutable external continuity candidate match; nowhere-differentiability root remains open (M2)")
