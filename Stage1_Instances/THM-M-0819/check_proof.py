#!/usr/bin/env python3
"""Fail-closed source and receipt checks for S56-M-0819-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0819-PROOF"
THEOREM = "THM-M-0819"
BASE = "7505614b75de56cf10bbd196a4aaa0ca2a117064"
BASE_TREE = "730e162a2133e4a077d764043b5e722c1f7feb39"
MATHLIB_REV = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
UPSTREAM_SOURCE_SHA = "4bc86897588087f472b358830bba157b92994e2b0dd44c66805f57c29211c985"
UPSTREAM_LICENSE_SHA = "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_without_comments(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    out: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            index += 1
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        else:
            out.append(source[index])
            index += 1
    assert depth == 0, f"unterminated block comment in {path}"
    return "".join(out)


proof_path = HERE / "Proof.lean"
finite_path = HERE / "FiniteDilworth.lean"
license_path = HERE / "LICENSE"
for path in (proof_path, finite_path):
    forbidden = re.compile(
        r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe|implemented_by|"
        r"native_decide|extern)\b"
    )
    assert forbidden.search(source_without_comments(path)) is None, path

proof = proof_path.read_text(encoding="utf-8")
for required in (
    "import Statement",
    "import FiniteDilworth",
    "import Mathlib.Combinatorics.Compactness",
    "Set.Finite.rado_selection_subtype",
    "private theorem finite_width_le",
    "private theorem finite_chain_partition",
    "private theorem positiveWidth",
    "theorem dilworthPrimary : DilworthPrimaryTarget.{u}",
    "assert_no_sorry dilworthPrimary",
    "#print axioms dilworthPrimary",
):
    assert required in proof, required

finite = finite_path.read_text(encoding="utf-8")
for required in (
    "Copyright (c) 2025 Vlad Tsyrklevich",
    "Released under Apache 2.0 license",
    "theorem minChainPartition_eq_antichainWidth",
    "hc₂.image_of_map_rel",
    "#print axioms minChainPartition_eq_antichainWidth",
):
    assert required in finite, required

statement = load(HERE / "statement.json")
registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
receipt = load(HERE / "proof-receipt.json")

assert statement["canonical_formal_target"]["declaration_or_expression"] == (
    "Stage1Instances.THM_M_0819.DilworthPrimaryTarget"
)
assert registry["root_obligation_id"] == "M0819-ROOT"
assert registry["denominator_sha256"] == (
    "3e19428b16575891198438f798957373f440bf15623c22c44df4c1f69239742c"
)
assert registry["frozen_against_statement_sha256"] == sha(HERE / "Statement.lean")
assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
assert graphs["closure_boundary"]["accepted_closed_obligations"] == []

item = next(row for row in execution["items"] if row["id"] == ITEM)
assert item["theorem_id"] == THEOREM
assert item["phase"] == "proof" and item["layer"] == 4
assert item["state"] in {"[ ]", "[_]"}
assert item["depends_on"] == ["S56-M-0819-OBLIGATION_TREE"]
assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
assert receipt["base_revision"] == BASE and receipt["base_tree"] == BASE_TREE
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
assert receipt["canonical_target"] == (
    "Stage1Instances.THM_M_0819.DilworthPrimaryTarget"
)
assert receipt["proof_body"]["root_source_sha256"] == sha(proof_path)
assert receipt["proof_body"]["finite_source_sha256"] == sha(finite_path)
assert receipt["proof_body"]["upstream_source_sha256"] == UPSTREAM_SOURCE_SHA
assert sha(license_path) == UPSTREAM_LICENSE_SHA
assert receipt["proof_body"]["license_sha256"] == sha(license_path)
assert receipt["inputs"]["check_proof_sh_sha256"] == sha(HERE / "check_proof.sh")
assert receipt["inputs"]["check_proof_py_sha256"] == sha(Path(__file__))
assert receipt["inputs"]["statement_sha256"] == sha(HERE / "Statement.lean")
assert receipt["inputs"]["obligation_registry_sha256"] == sha(
    HERE / "obligation-registry.json"
)
assert receipt["inputs"]["typed_graphs_sha256"] == sha(HERE / "typed-graphs.json")
assert receipt["result"]["root_kernel_closed"] is True
assert receipt["result"]["accepted_root_closed"] is False
assert receipt["result"]["theorem_complete"] is False

mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
assert subprocess.check_output(
    ["git", "-C", str(mathlib), "rev-parse", "HEAD"], text=True
).strip() == MATHLIB_REV
assert subprocess.check_output(
    ["git", "-C", str(mathlib), "rev-parse", "HEAD^{tree}"], text=True
).strip() == MATHLIB_TREE
assert subprocess.check_output(
    ["git", "-C", str(mathlib), "status", "--short"], text=True
) == ""

selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    selftest = load(selftest_path)
    assert set(selftest) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
    assert selftest["base_revision"] == BASE
    assert selftest["changed_paths"] == receipt["changed_paths"]
    assert selftest["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changes = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
        and not line[3:].startswith(".m0819-proof.")
    }
    assert actual_changes == set(selftest["changed_paths"]), (
        actual_changes,
        set(selftest["changed_paths"]),
    )

print("PASS THM-M-0819 proof phase: exact arbitrary-poset Dilworth root checked")
print(f"root proof sha256: {sha(proof_path)}")
print(f"finite proof sha256: {sha(finite_path)}")
print("accepted state unchanged; proof proposal is provisional pending master acceptance")
