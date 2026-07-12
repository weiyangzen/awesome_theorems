#!/usr/bin/env python3
"""Fail-closed worker validation for S56-M-0768-VALIDATION."""

import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0768"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
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
validation_receipt = json.loads((HERE / "validation-receipt.json").read_text())

assert spec["item_id"] == "S56-M-0768-VALIDATION"
assert spec["theorem_id"] == "THM-M-0768"
assert spec["recipe"]["network_policy"] == "not_used"
assert set(spec["recipe"]["covered_obligation_ids"]) == set(
    registry["frozen_denominators"]["required_machine"]
)
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
assert validation_receipt["item_id"] == "S56-M-0768-VALIDATION"
for key, name in (
    ("validation_spec_sha256", "validation-spec.json"),
    ("independent_probe_sha256", "Validation.lean"),
    ("statement_sha256", "Statement.lean"),
    ("obligation_tree_sha256", "ObligationTree.lean"),
    ("proof_sha256", "Proof.lean"),
    ("statement_record_sha256", "statement.json"),
    ("anchor_audit_sha256", "anchor-audit.json"),
    ("obligation_registry_sha256", "obligation-registry.json"),
    ("typed_graphs_sha256", "typed-graphs.json"),
    ("proof_receipt_sha256", "proof-receipt.json"),
):
    assert validation_receipt["inputs"][key] == digest(HERE / name)
assert validation_receipt["result"]["theorem_complete"] is False

sources = "\n".join(
    (HERE / name).read_text()
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
)
for pattern in (r"\b(?:sorry|admit|sorryAx)\b", r"^[ \t]*axiom\b", r"^[ \t]*unsafe\b"):
    assert re.search(pattern, sources, re.MULTILINE) is None, pattern
independent = (HERE / "Validation.lean").read_text()
assert "import Proof" not in independent
assert "import ObligationTree" not in independent
assert "schroeder_bernstein_of_rel" not in independent
assert "Function.Embedding.schroeder_bernstein hf hg" in independent

assert digest(LEAN_ROOT / "lean-toolchain") == (
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
)
assert digest(LEAN_ROOT / "lake-manifest.json") == (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == (
    "8a178386ffc0f5fef0b77738bb5449d50efeea95"
)
assert run(["git", "status", "--short"], cwd=mathlib) == ""
upstream = mathlib / anchor["immutable_environment"]["module_path"]
assert digest(upstream) == anchor["immutable_environment"]["module_sha256"]

with tempfile.TemporaryDirectory(prefix="m0768-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    statement_output = run(
        ["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=LEAN_ROOT,
    )
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    import os
    scoped_env = dict(os.environ, LEAN_PATH=f"{tmp}:{lean_path}")
    tree_output = run(
        ["lake", "env", "lean", "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
        cwd=LEAN_ROOT,
        env=scoped_env,
    )
    proof_output = run(["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=scoped_env)
    independent_output = run(
        ["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=scoped_env
    )

combined = statement_output + tree_output + proof_output + independent_output
for declaration in (
    "root_of_relational_package",
    "cantorBernsteinSchroeder_proof",
    "independentCantorBernsteinSchroeder",
):
    assert declaration in combined
for output in (proof_output, independent_output):
    assert EXPECTED_AXIOMS <= {axiom for axiom in EXPECTED_AXIOMS if axiom in output}
assert "sorryAx" not in combined

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False

print("ok: exact statement, frozen composition, proof root, and separately implemented exact root elaborated")
print("ok: both roots report only the expected classical mathlib axiom profile; prohibited source scans passed")
print("ok: frozen hashes, dependency pin, clean mathlib checkout, and terminal module provenance passed")
print("stale: the pre-proof typed graph remains open and requires master reconciliation")
print("blocked: cold empty-cache hermetic replay and distinct-runner independent verification")
