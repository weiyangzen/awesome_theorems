#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0403"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, *, cwd=ROOT, env=None):
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=120, check=False
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
proof_receipt = json.loads((HERE / "proof-receipt.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "obligation-graphs.json").read_text())

assert spec["item_id"] == "S56-M-0403-VALIDATION"
assert spec["theorem_id"] == "THM-M-0403"
assert proof_receipt["inputs"]["statement_sha256"] == sha256(HERE / "Statement.lean")
assert proof_receipt["proof_body"]["source_sha256"] == sha256(HERE / "Proof.lean")
assert proof_receipt["inputs"]["obligation_registry_sha256"] == sha256(
    HERE / "obligation-registry.json"
)
assert proof_receipt["inputs"]["obligation_graphs_sha256"] == sha256(
    HERE / "obligation-graphs.json"
)

status = registry["status_observed_after_freeze"]
boundary = graphs["closure_boundary"]
assert status == {"closed_obligations": [], "root_machine_debt": "M4"}
assert boundary["root_machine_debt"] == "M4"
assert boundary["closed_obligations"] == []
assert boundary["minimal_open_root_cut_set"] == ["M0403-L-ESS-FINITE"]
assert boundary["composition_certificates"] == []
assert boundary["theorem_complete"] is False
assert proof_receipt["result"]["root_closed"] is False
assert proof_receipt["closed_obligation_ids"] == []

lean_source = (HERE / "Statement.lean").read_text() + "\n" + (HERE / "Proof.lean").read_text()
for pattern in (
    r"\b(?:sorry|admit)\b", r"^[ \t]*axiom\b", r"^[ \t]*unsafe\b",
):
    assert re.search(pattern, lean_source, re.MULTILINE) is None, pattern

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
mathlib_head = run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip()
assert mathlib_head == "8a178386ffc0f5fef0b77738bb5449d50efeea95"
assert run(["git", "status", "--short"], cwd=mathlib) == ""

with tempfile.TemporaryDirectory(prefix="m0403-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    statement = tmp / "Statement.lean"
    proof = tmp / "Proof.lean"
    statement.write_bytes((HERE / "Statement.lean").read_bytes())
    proof.write_bytes((HERE / "Proof.lean").read_bytes())
    run(["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(statement)], cwd=LEAN_ROOT)
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    proof_output = run(["lake", "env", "lean", str(proof)], cwd=LEAN_ROOT, env=env)

declarations = proof_receipt["exact_declarations"]
for declaration in declarations:
    expected = f"'{declaration}' depends on axioms: [propext, Classical.choice, Quot.sound]"
    assert expected in proof_output, (expected, proof_output)

print("ok: pinned Statement.lean and Proof.lean elaborated in a fresh temporary module directory")
print("ok: six proof declarations report only propext, Classical.choice, and Quot.sound")
print("ok: proof provenance hashes and pinned clean mathlib revision match the proof receipt")
print("open: root M4; no closed obligations or composition certificate; cut set M0403-L-ESS-FINITE")
print("blocked: cold hermetic replay, complete TCB/SBOM, and distinct-runner independent verification")
