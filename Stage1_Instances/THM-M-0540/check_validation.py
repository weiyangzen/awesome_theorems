#!/usr/bin/env python3
"""Fail-closed worker validator for S56-M-0540-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0540"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
SOURCE_SHA256 = "655867a11ed5ec706a554ac32f8f273c5227cafd4b47f0de42d84e24b0d33c7c"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 120) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, f"missing axiom report for {declaration}"
    return {item.strip() for item in match.group(1).split(",")}


spec = json.loads((HERE / "validation-spec.json").read_text(encoding="utf-8"))
statement = json.loads((HERE / "statement.json").read_text(encoding="utf-8"))
registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
graphs = json.loads((HERE / "typed-graphs.json").read_text(encoding="utf-8"))
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))

assert spec["item_id"] == "S56-M-0540-VALIDATION"
assert spec["theorem_id"] == "THM-M-0540"
assert spec["network_policy"] == "denied"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == digest(HERE / "statement.json")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["proof_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["statement_file_sha256"] == digest(HERE / "Statement.lean")
assert proof_receipt["obligation_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["theorem_complete"] is False

lean_sources = "\n".join(
    (HERE / name).read_text(encoding="utf-8")
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean")
)
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe)\b", re.MULTILINE
)
assert prohibited.search(lean_sources) is None

assert MATHLIB.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=MATHLIB).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=MATHLIB) == ""
assert digest(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
assert digest(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
source = MATHLIB / "Mathlib" / "AlgebraicTopology" / "SingularHomology" / "Basic.lean"
assert digest(source) == SOURCE_SHA256
source_text = source.read_text(encoding="utf-8")
assert re.search(
    r"def singularHomologyFunctor\s*:.*?\:=\s*singularChainComplexFunctor C\s*⋙\s*"
    r"\(Functor\.whiskeringRight .*?homologyFunctor _ _ n\)",
    source_text,
    re.DOTALL,
)

outputs: dict[str, str] = {}
with tempfile.TemporaryDirectory(prefix="m0540-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        temporary_source = tmp / name
        temporary_source.write_bytes((HERE / name).read_bytes())
        output = tmp / name.replace(".lean", ".olean")
        outputs[name] = run(
            ["lake", "env", "lean", "-o", str(output), str(temporary_source)],
            cwd=LEAN_ROOT,
        )

for output_name, declaration in (
    ("ObligationTree.lean", "Stage1.THM_M_0540.root_of_unfolding"),
    ("Proof.lean", "Stage1.THM_M_0540.Proof.unfoldingEquation"),
    ("Proof.lean", "Stage1.THM_M_0540.Proof.integralSingularHomology_eq_homology"),
):
    assert reported_axioms(outputs[output_name], declaration) == EXPECTED_AXIOMS

assert set(proof_receipt["closed_machine_obligations"]) == set(
    registry["frozen_denominators"]["required_machine"]
)
assert proof_receipt["composition"]["parent"] == registry["root_obligation_id"]
assert "child-to-root composition certificate" in lean_sources

print("ok: exact statement, conditional composition, terminal equation, and root replayed with fresh temporary outputs")
print("ok: checked proof and composition declarations report exactly propext, Classical.choice, and Quot.sound")
print("ok: placeholder scan, receipt/hash linkage, frozen denominator, pinned clean mathlib, and terminal source provenance passed")
print("blocked: shared warm .lake artifacts are not a cold empty-cache hermetic release replay")
print("blocked: this single mutable worker is not a distinct independently provisioned verifier")
print("open: H0, R0, AUDIT-Z, THEOREM-Z, release, and master acceptance")
