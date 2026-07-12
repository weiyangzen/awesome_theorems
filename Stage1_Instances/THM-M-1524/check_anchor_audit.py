#!/usr/bin/env python3
"""Verify the immutable local and Spectra evidence in the THM-M-1524 audit."""

from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
LEAN = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN / ".lake" / "packages" / "mathlib"
AUDIT = Path(__file__).with_name("anchor-audit.json")


def output(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def remote(base: str, path: str) -> bytes:
    with urlopen(f"{base}/{path}", timeout=30) as response:
        return response.read()


audit = json.loads(AUDIT.read_text())
env = audit["immutable_environment"]
assert output("git", "rev-parse", "HEAD", cwd=MATHLIB) == env["mathlib_revision"]
assert output("git", "status", "--short", cwd=MATHLIB) == ""

candidates = {candidate["id"]: candidate for candidate in audit["candidates"]}
basic = MATHLIB / "Mathlib/Analysis/InnerProductSpace/Basic.lean"
partial = MATHLIB / "Mathlib/LinearAlgebra/LinearPMap.lean"
legacy = ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_192.lean"
assert digest(basic.read_bytes()) == candidates["M1524-A-MATHLIB-CS"]["source_sha256"]
assert digest(partial.read_bytes()) == candidates["M1524-A-MATHLIB-PARTIAL-MAP"]["source_sha256"]
assert digest(legacy.read_bytes()) == candidates["M1524-A-LEGACY-BOUNDED"]["source_sha256"]
assert "theorem norm_inner_le_norm" in basic.read_text()
assert "structure LinearPMap" in partial.read_text()

# The bounded legacy theorem is deliberately not an encoding match.
legacy_text = legacy.read_text()
assert "abbrev Observable" in legacy_text and "H →ₗ[ℂ] H" in legacy_text
assert "theorem robertson_inequality" in legacy_text
assert "theorem heisenberg_ccr_inequality" in legacy_text

spectra = candidates["M1524-A-SPECTRA"]
base = f"https://raw.githubusercontent.com/adambornemann-glitch/Spectra/{spectra['revision']}"
paths = [
    "Spectra/QuantumMechanics/Uncertainty/SchrodingerRobertson.lean",
    "Spectra/QuantumMechanics/Uncertainty/Heisenberg.lean",
]
sources = [remote(base, path) for path in paths]
assert [digest(source) for source in sources] == spectra["source_sha256"]
schrodinger, heisenberg = (source.decode() for source in sources)
assert "lemma observable_robertson_stddev" in schrodinger
assert "theorem heisenberg_uncertainty" in heisenberg
assert "have hrob := observable_robertson_stddev A B ψ h" in heisenberg

toolchain = remote(base, "lean-toolchain").decode().strip()
manifest = json.loads(remote(base, "lake-manifest.json"))
license_bytes = remote(base, "LICENSE")
assert toolchain == spectra["toolchain"]
assert next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib") == spectra["mathlib_revision"]
assert digest(license_bytes) == spectra["license_sha256"]

# Follow the local Spectra import closure of the terminal Heisenberg module.
archive = f"https://codeload.github.com/adambornemann-glitch/Spectra/tar.gz/{spectra['revision']}"
archive_bytes = urlopen(archive, timeout=60).read()
listing = subprocess.check_output(["tar", "-tzf", "-"], input=archive_bytes).decode().splitlines()
prefix = listing[0].split("/", 1)[0] + "/"
members = {line[len(prefix):] for line in listing if line.startswith(prefix)}
closure = {"Spectra/QuantumMechanics/Uncertainty/Heisenberg.lean"}
stack = list(closure)
source_by_path = {paths[0]: schrodinger, paths[1]: heisenberg}
while stack:
    path = stack.pop()
    text = source_by_path.get(path)
    if text is None:
        proc = subprocess.run(
            ["tar", "-xOzf", "-", prefix + path], input=archive_bytes,
            stdout=subprocess.PIPE, check=True,
        )
        text = proc.stdout.decode()
        source_by_path[path] = text
    for module in re.findall(r"^import\s+([A-Za-z0-9_.]+)", text, re.MULTILINE):
        dependency = module.replace(".", "/") + ".lean"
        if dependency in members and dependency not in closure:
            closure.add(dependency)
            stack.append(dependency)
assert len(closure) == 4
code_gap = re.compile(r"^\s*(?:axiom|unsafe|implemented_by)\b|\b(?:sorry|admit)\b", re.MULTILINE)
assert not any(code_gap.search(source_by_path[path]) for path in closure)

assert audit["root_decision"]["classification"] == "M2"
assert audit["root_decision"]["kernel_closed"] is False
assert audit["theorem_complete"] is False
print(
    "anchor audit verified: pinned mathlib leaves, bounded legacy mismatch, "
    f"and Spectra {spectra['revision']} root source; integration remains blocked (root=M2)"
)
