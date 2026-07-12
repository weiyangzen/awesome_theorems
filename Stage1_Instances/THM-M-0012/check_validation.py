#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0012-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0012"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0012-VALIDATION"
THEOREM = "THM-M-0012"
EXPECTED_MATHLIB = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
EXPECTED_MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_MATHLIB_SOURCE = "f6159d7625ca323846088b04ae89fca501bb040fcdce982f8f24c453e587d491"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PROVISIONAL_CLOSED = {
    "M0012-ROOT",
    "M0012-N-DEGREE",
    "M0012-A-POSITIVE-ROOT",
    "M0012-B-NO-ROOT",
    "M0012-L-RECIPROCAL-DIFF",
    "M0012-L-RECIPROCAL-DECAY",
    "M0012-L-LIOUVILLE",
    "M0012-L-POLYNOMIAL-CONSTANT",
    "M0012-T-ANALYTIC-COMPOSE",
    "M0012-T-ROOT-COMPOSE",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if result.returncode:
        raise SystemExit(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    if not match:
        raise SystemExit(f"validation failed: missing axiom report for {declaration}")
    return {item.strip() for item in match.group(1).split(",") if item.strip()}


spec = load(HERE / "validation-spec.json")
receipt = load(HERE / "validation-receipt.json")
statement = load(HERE / "statement.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
anchor = load(HERE / "anchor-audit.json")
proof_receipt = load(HERE / "proof-receipt.json")
execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

assert spec["item_id"] == receipt["item_id"] == ITEM
assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
recipe = spec["recipes"][0]
assert recipe["cwd"] == "." and isinstance(recipe["argv"], list)
assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
assert receipt["recipe"] == recipe

validation_item = next(row for row in execution["items"] if row["id"] == ITEM)
proof_item = next(
    row for row in execution["items"] if row["id"] == "S56-M-0012-PROOF"
)
assert validation_item["phase"] == "validation" and validation_item["state"] in {
    "[ ]",
    "[_]",
}
assert validation_item["depends_on"] == [proof_item["id"]]
assert proof_item["state"] == "[_]", "proof prerequisite is not provisionally self-tested"
assert validation_item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

assert statement["canonical_formal_target"]["statement_file_sha256"] == digest(
    HERE / "Statement.lean"
)
assert registry["root_obligation_id"] == "M0012-ROOT"
assert registry["frozen_against_statement_sha256"] == digest(HERE / "Statement.lean")
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
assert proof_receipt["item_id"] == "S56-M-0012-PROOF"
assert proof_receipt["accepted"] is False
assert proof_receipt["proof_body"]["source_sha256"] == digest(HERE / "Proof.lean")
assert proof_receipt["inputs"]["statement_sha256"] == digest(HERE / "Statement.lean")
assert proof_receipt["inputs"]["obligation_tree_sha256"] == digest(
    HERE / "ObligationTree.lean"
)
assert proof_receipt["inputs"]["obligation_registry_sha256"] == digest(
    HERE / "obligation-registry.json"
)
assert proof_receipt["result"]["root_kernel_closed"] is True
assert set(proof_receipt["provisionally_closed_obligation_ids"]) == PROVISIONAL_CLOSED
assert proof_receipt["accepted_closed_obligation_ids"] == []
assert set(recipe["covered_obligation_ids"]) >= PROVISIONAL_CLOSED

for name, expected in receipt["inputs"].items():
    path = (ROOT / name) if name.startswith("Formalizations/Lean/") else (HERE / name)
    assert digest(path) == expected, f"stale validation input: {name}"

prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b"
    r"|^[ \t]*(?:axiom|unsafe|constant)\b",
    re.MULTILINE,
)
for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
    assert prohibited.search(without_comments((HERE / name).read_text(encoding="utf-8"))) is None

manifest = load(LEAN_ROOT / "lake-manifest.json")
mathlib_record = next(p for p in manifest["packages"] if p["name"] == "mathlib")
assert mathlib_record["rev"] == EXPECTED_MATHLIB
mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
assert mathlib.is_dir(), "pinned mathlib artifact is unavailable"
assert run(["git", "rev-parse", "HEAD"], cwd=mathlib).strip() == EXPECTED_MATHLIB
assert run(["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib).strip() == EXPECTED_MATHLIB_TREE
assert run(["git", "status", "--short"], cwd=mathlib) == ""
mathlib_source = mathlib / "Mathlib/Analysis/Complex/Polynomial/Basic.lean"
assert digest(mathlib_source) == EXPECTED_MATHLIB_SOURCE
candidate = next(c for c in anchor["candidates"] if c["candidate_id"] == "M0012-C01-MATHLIB-DIRECT")
assert candidate["revision"] == EXPECTED_MATHLIB
assert candidate["tree"] == EXPECTED_MATHLIB_TREE
assert candidate["file_sha256"] == EXPECTED_MATHLIB_SOURCE
assert candidate["terminal_declaration"] == "Complex.exists_root"
assert candidate["license"] == "Apache-2.0"
terminal_body = mathlib_source.read_text(encoding="utf-8").split(
    "theorem exists_root {f : ℂ[X]}", 1
)[1].split("instance isAlgClosed", 1)[0]
assert prohibited.search(without_comments(terminal_body)) is None

with tempfile.TemporaryDirectory(prefix="m0012-validation-", dir=LEAN_ROOT) as tmp_name:
    tmp = Path(tmp_name)
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        (tmp / name).write_bytes((HERE / name).read_bytes())
    run(
        [
            "lake",
            "env",
            "lean",
            "-o",
            str(tmp / "Statement.olean"),
            str(tmp / "Statement.lean"),
        ],
        cwd=LEAN_ROOT,
    )
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    env = os.environ.copy()
    env["LEAN_PATH"] = f"{tmp}:{lean_path}"
    run(
        [
            "lake",
            "env",
            "lean",
            "-o",
            str(tmp / "ObligationTree.olean"),
            str(tmp / "ObligationTree.lean"),
        ],
        cwd=LEAN_ROOT,
        env=env,
    )
    proof_output = run(
        ["lake", "env", "lean", str(tmp / "Proof.lean")],
        cwd=LEAN_ROOT,
        env=env,
    )

for declaration in receipt["trust_observation"]["checked_declarations"]:
    actual = reported_axioms(proof_output, declaration)
    assert actual == EXPECTED_AXIOMS, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in proof_output

# Validation must preserve stale/unaccepted structured authority rather than promote it.
closure = graphs["closure_boundary"]
assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
assert closure["accepted_closed_obligations"] == []
assert closure["audit_complete"] is False and closure["theorem_complete"] is False
assert receipt["result"]["structured_state_freshness"] == "fail_closed"
assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
assert receipt["result"]["independent_verification_gate"] == "fail_closed"
assert receipt["result"]["audit_complete"] is False
assert receipt["result"]["theorem_complete"] is False
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["release_grade"] is False

selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    selftest = load(selftest_path)
    if selftest.get("item_id") == ITEM:
        assert set(selftest) == {
            "item_id",
            "changed_paths",
            "commands",
            "output_summary",
            "base_revision",
            "known_failures",
            "state",
        }
        assert selftest["state"] == "[_]"
        assert selftest["base_revision"] == receipt["base_revision"]
        assert selftest["changed_paths"] == receipt["changed_paths"]
        assert selftest["known_failures"] == receipt["known_failures"]

print("PASS THM-M-0012 narrow validation")
print("kernel: exact root and frozen analytic composition re-elaborated from copied sources")
print("trust: checked proof declarations report only propext, Classical.choice, Quot.sound")
print("provenance: proof hashes and clean pinned mathlib terminal source agree")
print("blocked: proof acceptance and structured state freshness remain open")
print("blocked: cold hermetic replay, complete transitive TCB closure, and distinct-runner verification")
