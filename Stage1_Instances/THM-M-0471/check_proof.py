#!/usr/bin/env python3
"""Fail-closed source, pin, graph, and receipt checks for S56-M-0471-PROOF."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0471-PROOF"
THEOREM = "THM-M-0471"
BASE_REVISION = "48abbb2d2eeb89816c5ffc0ad8faafa4b9d24dd0"
BASE_TREE = "0f26e2c78fb5fff9277cbbdfef5e145fd4ef06f1"
EXPRESSION_SHA256 = "07ae92b7b398b89a1bbe8413563f1c30da5b8bbd0522f6d070fd62dcea0ac4e4"
DENOMINATOR_SHA256 = "d3f11762e2a0f4c384d094d53e44100f20a21f81eb6ce527cd5f9897a9bc445c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
FACTORS_SOURCE = Path("Mathlib/Data/Nat/Factors.lean")
FACTORS_BLOB = "292355d305be37499c8415d15b430aa241132c9b"
FACTORS_SHA256 = "3e64e2c8ba907c05209966a7bba8754cf2ab33f328a3010667ffe58c95e0bca3"
FACTORS_OLEAN_SHA256 = "ca04f32795ce6aba7a89b812e7b57cf1a11ebebb4a2428469252dad6fa132b70"
LIST_PRIME_SOURCE = Path("Mathlib/Data/List/Prime.lean")
LIST_PRIME_BLOB = "17337ba91fd2f4b2b947301cca165a253662e377"
LIST_PRIME_SHA256 = "148cf3e70ddc39591270dd3c4d9da733a91ff574e8f5c1bd6fd8fd2f42e33591"
LIST_PRIME_OLEAN_SHA256 = "0070fd6c21af18e3bc139e406be76fc7f7d6d2b62165eee6910aee740126c328"
PROOF_IDS = [
    "M0471-ROOT",
    "M0471-T-ROOT-COMPOSE",
    "M0471-T-ASSEMBLE",
    "M0471-C-WITNESS",
    "M0471-L-NONEMPTY",
    "M0471-S-BOUNDARY",
    "M0471-L-PRIMALITY",
    "M0471-L-PRODUCT",
    "M0471-N-NONZERO",
    "M0471-L-UNIQUENESS",
    "M0471-L-PERM-PRODUCT",
    "M0471-L-PRIME-DVD-PRODUCT",
    "M0471-L-MEM-PRIME-DIVISOR",
    "M0471-C-ERASE-PERM",
    "M0471-N-CANCEL-HEAD",
]
OPEN_MACHINE_IDS = [
    "M0471-S-INTERFACE",
    "M0471-S-TRANSPORT",
    "M0471-S-FOUNDATION",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/check_proof.sh",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{path} must contain an object"
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*", "", source)


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    receipt = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    task_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git_output("rev-parse", "HEAD") == BASE_REVISION
    assert git_output("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1353,
        "phase": "proof",
        "layer": 4,
        "state": "[ ]",
        "depends_on": ["S56-M-0471-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide|extern|opaque)\b|"
        r"^[ \t]*(axiom|constant|unsafe)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(without_comments(proof)) is None
    for marker in (
        "import ObligationTree",
        "def NonzeroNormalization : Prop :=",
        "def PrimeDvdProduct : Prop :=",
        "def PrimeDivisorMembership : Prop :=",
        "def ErasePermutation : Prop :=",
        "def CancelCommonHead : Prop :=",
        "def PrimeProductPermutation : Prop :=",
        "theorem nonzeroNormalization : NonzeroNormalization := by",
        "theorem primeDvdProduct : PrimeDvdProduct := by",
        "theorem primeDivisorMembership : PrimeDivisorMembership := by",
        "theorem erasePermutation : ErasePermutation := by",
        "theorem cancelCommonHead : CancelCommonHead := by",
        "theorem primeProductPermutation : PrimeProductPermutation := by",
        "abbrev primeFactorWitness : PrimeFactorWitness := Nat.primeFactorsList",
        "theorem witnessNonempty : WitnessNonempty primeFactorWitness := by",
        "theorem witnessPrimality : WitnessPrimality primeFactorWitness := by",
        "theorem witnessProduct : WitnessProduct primeFactorWitness := by",
        "theorem primeFactorUniqueness : PrimeFactorUniqueness primeFactorWitness := by",
        "theorem primeFactorUniqueness_via_components : PrimeFactorUniqueness primeFactorWitness := by",
        "exactPrimeListAnchor_of_packages primeFactorWitness witnessNonempty witnessPrimality",
        "root_of_exactPrimeListAnchor exactPrimeListAnchor",
        "theorem fundamentalTheoremOfArithmetic : FundamentalTheoremOfArithmeticTarget := by",
        "assert_no_sorry fundamentalTheoremOfArithmetic",
        "#print axioms fundamentalTheoremOfArithmetic",
    ):
        assert marker in proof, marker

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0471-ROOT"
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    required_machine = registry["frozen_denominators"]["required_machine"]
    assert set(required_machine) == set(PROOF_IDS + OPEN_MACHINE_IDS)

    proof_edges = graphs["graphs"]["proof"]["edges"]
    children: dict[str, list[str]] = {}
    for edge in proof_edges:
        if edge["type"] == "proof_requires":
            children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()
    pending = ["M0471-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(children.get(obligation, []))
    assert reachable == set(PROOF_IDS)

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["proof_source_patch_id"] == "bdd85f82704267c6689a406ebd06cd1e682e8d30"
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["provisionally_closed_proof_obligation_ids"] == PROOF_IDS
    assert receipt["required_machine_open_ids"] == OPEN_MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    fingerprints = {
        row["obligation_id"]: row["statement_fingerprint"]
        for row in registry["obligations"]
        if row["obligation_id"] in PROOF_IDS
    }
    assert receipt["statement_fingerprints"] == fingerprints
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["proof_body"]["source_sha256"] == sha256(proof_path)
    for key, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("check_proof_sh_sha256", "check_proof.sh"),
    ):
        assert receipt["inputs"][key] == sha256(HERE / filename)
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert git_output("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git_output("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git_output("status", "--porcelain=v1", cwd=mathlib) == ""
    for source_rel, blob, source_hash, olean_hash in (
        (FACTORS_SOURCE, FACTORS_BLOB, FACTORS_SHA256, FACTORS_OLEAN_SHA256),
        (LIST_PRIME_SOURCE, LIST_PRIME_BLOB, LIST_PRIME_SHA256, LIST_PRIME_OLEAN_SHA256),
    ):
        source = mathlib / source_rel
        olean = mathlib / ".lake/build/lib/lean" / source_rel.with_suffix(".olean")
        assert git_output("rev-parse", f"HEAD:{source_rel}", cwd=mathlib) == blob
        assert sha256(source) == source_hash
        assert sha256(olean) == olean_hash
    factors_text = (mathlib / FACTORS_SOURCE).read_text(encoding="utf-8")
    list_text = (mathlib / LIST_PRIME_SOURCE).read_text(encoding="utf-8")
    for marker in (
        "def primeFactorsList", "theorem prime_of_mem_primeFactorsList",
        "theorem prod_primeFactorsList", "theorem primeFactorsList_ne_nil",
        "theorem primeFactorsList_unique", "refine perm_of_prod_eq_prod",
    ):
        assert marker in factors_text
    for marker in (
        "theorem Prime.dvd_prod_iff", "theorem mem_list_primes_of_dvd_prod",
        "theorem perm_of_prod_eq_prod", "perm_cons_erase", "mul_right_inj'",
    ):
        assert marker in list_text
    assert prohibited.search(without_comments(factors_text)) is None
    assert prohibited.search(without_comments(list_text)) is None

    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git_output("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS

    validation = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "does not claim theorem completion" in validation
    assert "M0-W" in validation and "M0471-S-FOUNDATION" in validation
    for path in (
        proof_path,
        HERE / "check_proof.py",
        HERE / "check_proof.sh",
        HERE / "proof-receipt.json",
        HERE / "proof-validation.md",
        ROOT / ".stage1-worker-selftest.json",
    ):
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0471 proof phase: exact frozen root and every proof-graph child close")


if __name__ == "__main__":
    main()
