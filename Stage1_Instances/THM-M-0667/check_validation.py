#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0667-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0667"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "b08602621218293de230722de60ce7a0b5dd2131f8d9203e4d61acec54d33652",
    "CandidateAudit.lean": "5f0a2ec57e98c5143803863bf662b01270a62812dbbf3269461ccd2b9af7de77",
    "ObligationTree.lean": "65e9a2702a1d46c3a045986ef695de3dee89a0f9e9df8ef8f94e08321d65b113",
    "Proof.lean": "9cb852103e70aa57874e0286e18c035088e1e8017d69f26576db0d99089f27e1",
    "anchor-audit.json": "f7144106bc01baec192e8073d89261136e266c1f40b0883f64c8ccdfc6eabca6",
    "obligation-registry.json": "01e69d1a1dfba30d342225fb2fad1fd5bf460ed373b19cd766a74697364f4367",
    "typed-graphs.json": "53a32b0eb7241331113dfd40a133fa225992453412fb718f7df881154f12e676",
    "proof-receipt.json": "8affa67ef39cd2fdebf2d532675d38bd6001a824f2716ecf6daa58626ee4572e",
}
EXPECTED_VALIDATION_INPUTS = {
    "Validation.lean": "549a8bdd5e8ca1cc2ead96f6d368163db530f45bb7108f2f1d2b70d7cf28f54f",
    "validation-spec.json": "629e4af69159561ef5d841d6092a421db513837917d098e69ec0c467eaecd580",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if completed.returncode:
        raise RuntimeError(
            f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}"
        )
    return completed.stdout


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def reported_axioms(output: str, declaration: str) -> set[str]:
    marker = f"'{declaration}' depends on axioms:"
    lines = output.splitlines()
    start = next(
        (
            index
            for index, line in enumerate(lines)
            if marker in line or (line.startswith("'") and f".{declaration}' depends on axioms:" in line)
        ),
        None,
    )
    assert start is not None, f"missing axiom report for {declaration}\n{output}"
    report = lines[start].partition("depends on axioms:")[2].strip()
    index = start + 1
    while "]" not in report and index < len(lines):
        report += " " + lines[index].strip()
        index += 1
    assert report.startswith("[") and report.endswith("]"), report
    return {name.strip() for name in report[1:-1].split(",") if name.strip()}


spec = load("validation-spec.json")
statement = load("statement.json")
anchor = load("anchor-audit.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof_receipt = load("proof-receipt.json")

assert spec["item_id"] == "S56-M-0667-VALIDATION"
assert spec["theorem_id"] == statement["theorem_id"] == "THM-M-0667"
assert spec["depends_on"] == ["S56-M-0667-PROOF"]
assert len(spec["recipes"]) == 1
recipe = spec["recipes"][0]
assert recipe["argv"] == [
    "python3",
    "-B",
    "Stage1_Instances/THM-M-0667/check_validation.py",
]
assert recipe["network_policy"] == "denied"
assert recipe["expected_exit"] == 0

for name, expected in EXPECTED_INPUTS.items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"
for name, expected in EXPECTED_VALIDATION_INPUTS.items():
    assert digest(HERE / name) == expected, f"stale validation input: {name}"
assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["frozen_against_anchor_audit_sha256"] == digest(
    HERE / "anchor-audit.json"
)
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_registry_sha256"] == digest(
    HERE / "obligation-registry.json"
)
assert proof_receipt["proof_body"]["local_wrapper_sha256"] == digest(
    HERE / "Proof.lean"
)
assert proof_receipt["result"]["root_closed"] is True
assert proof_receipt["result"]["theorem_complete"] is False

required_machine = set(registry["frozen_denominators"]["required_machine"])
closed = set(proof_receipt["closed_obligation_ids"])
assert required_machine - closed == {"M0667-X-FOUNDATION"}
assert closed <= required_machine
node_ids = {node["obligation_id"] for node in graphs["nodes"]}
assert node_ids == {row["obligation_id"] for row in registry["obligations"]}
closure = graphs["closure_boundary"]
assert closure["root_machine_debt"] == "M3"
assert closure["theorem_complete"] is False
assert closure["remaining_root_cut_set"] == [
    "M0667-N-DOMINATION",
    "M0667-X-FOUNDATION",
    "M0667-X-SOURCE",
]

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|unsafe|opaque|extern)\b|"
    r"\b(?:implemented_by|native_decide)\b",
    re.MULTILINE,
)
for name in (
    "Statement.lean",
    "CandidateAudit.lean",
    "ObligationTree.lean",
    "Proof.lean",
    "Validation.lean",
):
    assert prohibited.search(without_comments((HERE / name).read_text())) is None, name

validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
assert "import Proof" not in validation_source
assert "import ObligationTree" not in validation_source
assert "ackermannNondefinability" not in without_comments(validation_source)
assert "not_primrec₂_ack" not in without_comments(validation_source)
assert "exists_lt_ack_of_nat_primrec" in validation_source

assert digest(LEAN_ROOT / "lean-toolchain") == (
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
)
assert digest(LEAN_ROOT / "lake-manifest.json") == (
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
)
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "canonical pinned mathlib artifact missing"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == MATHLIB_REVISION
assert run(["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib).strip() == MATHLIB_TREE
assert run(["git", "status", "--short"], cwd=mathlib) == ""
assert run(["git", "remote", "get-url", "origin"], cwd=mathlib).strip() == MATHLIB_REMOTE

terminal_source = mathlib / "Mathlib" / "Computability" / "Ackermann.lean"
assert digest(terminal_source) == (
    "02135d74dcfe97d8ad95402d224be3979babc6e69c2a2b6f2ad06c9fc2f17578"
)
assert proof_receipt["proof_body"]["terminal_source_sha256"] == digest(terminal_source)
assert anchor["candidates"][1]["terminal_declaration"] == "not_primrec₂_ack"
assert prohibited.search(without_comments(terminal_source.read_text())) is None
for declaration in (
    "exists_lt_ack_of_nat_primrec",
    "not_nat_primrec_ack_self",
    "not_primrec_ack_self",
    "not_primrec₂_ack",
):
    assert re.search(rf"^theorem {re.escape(declaration)}\b", terminal_source.read_text(), re.MULTILINE)

env = os.environ.copy()
env["ELAN_TOOLCHAIN"] = TOOLCHAIN
version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT, env=env)
assert "4.29.0" in version and LEAN_COMMIT in version
lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=env).strip()
lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=env).strip())
assert digest(lean) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"

outputs: dict[str, str] = {}
with tempfile.TemporaryDirectory(prefix="m0667-validation-", dir=HERE) as tmp_name:
    tmp = Path(tmp_name)
    for name in (
        "Statement.lean",
        "CandidateAudit.lean",
        "ObligationTree.lean",
        "Proof.lean",
        "Validation.lean",
    ):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    base_env = env.copy()
    base_env["LEAN_PATH"] = lean_path
    outputs["Statement.lean"] = run(
        [str(lean), "-o", str(tmp / "Statement.olean"), str(tmp / "Statement.lean")],
        cwd=ROOT,
        env=base_env,
    )
    module_env = base_env.copy()
    module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    outputs["CandidateAudit.lean"] = run(
        [str(lean), str(tmp / "CandidateAudit.lean")], cwd=ROOT, env=module_env
    )
    outputs["ObligationTree.lean"] = run(
        [str(lean), "-o", str(tmp / "ObligationTree.olean"), str(tmp / "ObligationTree.lean")],
        cwd=ROOT,
        env=module_env,
    )
    outputs["Proof.lean"] = run(
        [str(lean), str(tmp / "Proof.lean")], cwd=ROOT, env=module_env
    )
    outputs["Validation.lean"] = run(
        [str(lean), str(tmp / "Validation.lean")], cwd=ROOT, env=module_env
    )

assert "ackermannNondefinability : AckermannNondefinabilityTarget" in outputs["Proof.lean"]
assert "independentlyReconstructedRoot : AckermannNondefinabilityTarget" in outputs["Validation.lean"]
assert "root_of_domination" in outputs["ObligationTree.lean"]
for output in outputs.values():
    assert "sorryAx" not in output
assert reported_axioms(outputs["Proof.lean"], "ackermannNondefinability") == EXPECTED_AXIOMS
validation_axioms = reported_axioms(
    outputs["Validation.lean"], "independentlyReconstructedRoot"
)
assert validation_axioms == EXPECTED_AXIOMS, validation_axioms
assert reported_axioms(
    outputs["CandidateAudit.lean"], "not_primrec₂_ack"
) == EXPECTED_AXIOMS

print("PASS THM-M-0667 narrow kernel replay: exact proof root and differential root elaborated")
print("PASS THM-M-0667 trust observation: roots report propext, Classical.choice, Quot.sound")
print("PASS THM-M-0667 local provenance: frozen hashes and clean pinned mathlib source agree")
print("STALE structured state: pre-proof graph remains M3 pending master reconciliation")
print("BLOCKED hermetic gate: shared warm .lake; no cold empty-cache offline replay or full TCB archive")
print("BLOCKED independent gate: differential probe shared this worker checkout and cache")
