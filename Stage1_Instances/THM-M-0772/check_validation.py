#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0772-VALIDATION."""

import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0772"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, *, cwd=ROOT) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            f"validation failed: command exited {result.returncode}: {argv!r}\n{result.stdout}"
        )
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
anchor = json.loads((HERE / "anchor-audit.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert spec["item_id"] == "S56-M-0772-VALIDATION"
assert spec["theorem_id"] == "THM-M-0772"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == digest(HERE / "anchor-audit.json")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["inputs"]["obligation_registry_sha256"] == digest(
    HERE / "obligation-registry.json"
)

source = "\n".join(
    (HERE / name).read_text()
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
)
for pattern in (r"\b(?:sorry|admit|sorryAx)\b", r"^[ \t]*axiom\b", r"^[ \t]*unsafe\b"):
    assert re.search(pattern, source, re.MULTILINE) is None, pattern
independent_source = (HERE / "Validation.lean").read_text()
assert "Proof" not in independent_source
assert "ObligationTree" not in independent_source
assert "maxChain_spec" not in independent_source
assert "IsChain.exists_maxChain" in independent_source

assert digest(LEAN_ROOT / "lean-toolchain") == (
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
)
assert digest(LEAN_ROOT / "lake-manifest.json") == (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)
mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert run(["git", "status", "--short"], cwd=mathlib) == ""
candidate = anchor["candidates"][1]
upstream = mathlib / candidate["file"]
assert digest(upstream) == candidate["file_sha256"]

with tempfile.TemporaryDirectory(prefix="m0772-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    outputs = {}
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        temporary = tmp / name
        temporary.write_bytes((HERE / name).read_bytes())
        outputs[name] = run(["lake", "env", "lean", str(temporary)], cwd=LEAN_ROOT)

for name, declaration in (
    ("ObligationTree.lean", "root_of_relationGenericMaxChain"),
    ("Proof.lean", "hausdorffMaximalPrinciple"),
    ("Proof.lean", "expandedHausdorffMaximalPrinciple"),
    ("Validation.lean", "independentHausdorffMaximalPrinciple"),
):
    output = outputs[name]
    assert declaration in output
    assert {axiom for axiom in EXPECTED_AXIOMS if axiom in output} == EXPECTED_AXIOMS
assert "sorryAx" not in "".join(outputs.values())

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == ["M0772-X-MATHLIB-BODY"]

print("ok: exact statement, frozen composition, proof root, expanded root, and independent direct root elaborated in a fresh temporary directory")
print("ok: checked declarations report only propext, Classical.choice, and Quot.sound; placeholder and unsafe scans passed")
print("ok: statement, registry, graph, proof receipt, toolchain, dependency pin, and upstream source provenance hashes passed")
print("stale: the pre-proof frozen graph retains an open M3 root and X-MATHLIB-BODY cut; only the master may reconcile authoritative state")
print("blocked: cold empty-cache hermetic replay, complete TCB/SBOM closure, and distinct-runner independent verification")
