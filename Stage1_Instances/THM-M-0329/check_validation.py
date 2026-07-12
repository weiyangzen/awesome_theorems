#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0329-VALIDATION."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0329"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def sha256(path: Path) -> str:
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
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


spec = json.loads((HERE / "validation-spec.json").read_text())
statement = json.loads((HERE / "statement.json").read_text())
registry = json.loads((HERE / "obligation-registry.json").read_text())
graphs = json.loads((HERE / "typed-graphs.json").read_text())

assert spec["item_id"] == "S56-M-0329-VALIDATION"
assert spec["theorem_id"] == registry["theorem_id"] == "THM-M-0329"
assert spec["network_policy"] == "denied"
assert isinstance(spec["argv"], list) and spec["expected_exit"] == 0
assert statement["canonical_formal_target"]["statement_file_sha256"] == sha256(HERE / "Statement.lean")
assert registry["frozen_against_statement_sha256"] == sha256(HERE / "Statement.lean")
assert registry["frozen_against_anchor_audit_sha256"] == sha256(HERE / "anchor-audit.json")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

lean_files = ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean")
lean_source = "\n".join((HERE / name).read_text() for name in lean_files)
for pattern in (
    r"\b(?:sorry|admit|sorryAx)\b",
    r"^[ \t]*axiom\b",
    r"^[ \t]*unsafe\b",
    r"\bproof_wanted\b",
):
    assert re.search(pattern, lean_source, re.MULTILINE) is None, pattern
validation_source = (HERE / "Validation.lean").read_text()
assert "import Proof" not in validation_source
assert "import ObligationTree" not in validation_source
assert "theorem laxMilgramDirect : LaxMilgramTarget.{u}" in validation_source

mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
assert mathlib.resolve().is_dir()
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "status", "--short"], cwd=mathlib) == ""

with tempfile.TemporaryDirectory(prefix="m0329-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in lean_files:
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(
        ["lake", "env", "lean", "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=LEAN_ROOT,
    )
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    obligation_output = run(
        ["lake", "env", "lean", "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )
    proof_output = run(["lake", "env", "lean", str(tmp / "Proof.lean")], cwd=LEAN_ROOT, env=env)
    validation_output = run(
        ["lake", "env", "lean", str(tmp / "Validation.lean")], cwd=LEAN_ROOT, env=env
    )

for declaration, output in (
    ("root_of_packages", obligation_output),
    ("rieszPackage", proof_output),
    ("operatorPackage", proof_output),
    ("laxMilgram", proof_output),
    ("laxMilgramDirect", validation_output),
):
    match = re.search(
        rf"[^\n]*{re.escape(declaration)}[^\n]*depends on axioms:\s*\[([^]]+)\]",
        output,
        re.DOTALL,
    )
    assert match is not None, (declaration, output)
    observed = {part.strip() for part in match.group(1).replace("\n", " ").split(",")}
    assert observed == EXPECTED_AXIOMS, (declaration, observed)

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False
assert closure["theorem_complete"] is False
assert set(closure["first_open_cut"]) == {
    "M0329-X-SOURCE",
    "M0329-X-FOUNDATION",
    "M0329-X-PROVENANCE",
    "M0329-X-WORKFLOW",
}

print("PASS narrow kernel replay: exact statement, frozen composition, proof packages, and exact root elaborated")
print("PASS trust observation: five checked declarations report propext, Classical.choice, and Quot.sound")
print("PASS local provenance: statement, anchor, registry, graph, source, and clean pinned mathlib hashes agree")
print("PASS same-worker differential probe: exact root reconstructed without importing Proof or ObligationTree")
print("STALE frozen graph: root remains candidate/open pending master reconciliation with proof evidence")
print("BLOCKED release gates: shared warm .lake, incomplete transitive TCB/SBOM archive, and no distinct independent runner")
