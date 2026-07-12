#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0769-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0769"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, *, cwd=ROOT, env=None) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=120,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
anchor = json.loads((HERE / "anchor-audit.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())

assert spec["item_id"] == "S56-M-0769-VALIDATION"
assert spec["theorem_id"] == statement["theorem_id"] == "THM-M-0769"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == digest(
    HERE / "anchor-audit.json"
)
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["inputs"]["obligation_registry_sha256"] == digest(
    HERE / "obligation-registry.json"
)
assert proof_receipt["result"]["axioms"] == ["Classical.choice"]

lean_files = (
    "Statement.lean",
    "AnchorAudit.lean",
    "ObligationTree.lean",
    "Proof.lean",
    "Validation.lean",
)
source = "\n".join((HERE / name).read_text() for name in lean_files)
for pattern in (
    r"\b(?:sorry|admit|sorryAx)\b",
    r"^[ \t]*axiom\b",
    r"^[ \t]*unsafe\b",
):
    assert re.search(pattern, source, re.MULTILINE) is None, pattern

independent_source = (HERE / "Validation.lean").read_text()
assert "import Proof" not in independent_source
assert "import ObligationTree" not in independent_source
assert "fiberSelector_proof" not in independent_source
assert "Pi.instNonempty" in independent_source

assert digest(LEAN_ROOT / "lean-toolchain") == (
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
)
assert digest(LEAN_ROOT / "lake-manifest.json") == (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)
env = os.environ.copy()
env["ELAN_TOOLCHAIN"] = TOOLCHAIN
version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT, env=env)
assert "4.29.0" in version and LEAN_COMMIT in version
mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=mathlib) == ""

with tempfile.TemporaryDirectory(prefix="m0769-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in lean_files:
        (tmp / name).write_bytes((HERE / name).read_bytes())
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=env).strip()
    outputs = {}
    statement_output = run(
        ["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    outputs["Statement.lean"] = statement_output
    module_env = env.copy()
    module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    for name in lean_files[1:]:
        outputs[name] = run(
            ["lake", "env", "lean", str(tmp / name)], cwd=LEAN_ROOT, env=module_env
        )

for name, declarations in {
    "AnchorAudit.lean": (
        "viaPiInstNonempty",
        "viaClassicalNonemptyPi",
        "viaClassicalChoice",
    ),
    "ObligationTree.lean": ("root_of_fiberSelector",),
    "Proof.lean": ("fiberSelector_proof", "axiomOfChoice_proof"),
    "Validation.lean": ("independentAxiomOfChoice",),
}.items():
    output = outputs[name]
    for declaration in declarations:
        if declaration == "root_of_fiberSelector":
            assert any(
                declaration in line and "does not depend on any axioms" in line
                for line in output.splitlines()
            ), output
            continue
        axiom_line = next(
            line
            for line in output.splitlines()
            if declaration in line and "depends on axioms" in line
        )
        assert "[Classical.choice]" in axiom_line, axiom_line
        assert "sorryAx" not in axiom_line

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["root_machine_classification"] == "M3"
assert closure["theorem_complete"] is False
assert "M0769-L-FIBER-CHOICE" in closure["first_open_cut"]

print("PASS narrow kernel replay: exact statement, frozen composition, proof root, and differential direct root elaborated")
print("PASS trust observation: proof and differential roots report exactly Classical.choice; conditional composition is axiom-free")
print("PASS local provenance: statement, anchor, registry, graph, proof receipt, toolchain, and clean mathlib pin agree")
print("STALE frozen graph: the pre-proof graph retains an M3 root and open fiber-choice node pending master reconciliation")
print("BLOCKED hermetic gate: shared warm canonical .lake was reused; no cold empty-cache offline replay or complete TCB/SBOM archive")
print("BLOCKED independent gate: differential source ran in this worker and shared cache, not a distinct signed runner")
