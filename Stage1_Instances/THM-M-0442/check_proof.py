#!/usr/bin/env python3
"""Fail-closed replay of the partial THM-M-0442 proof execution."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


if sys.flags.optimize:
    raise SystemExit("check_proof.py requires assertions; do not run Python with -O")


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0442-PROOF"
THEOREM = "THM-M-0442"
BASE_REVISION = "4990a9d6fa09beb7747e6822c6543c6123ca7504"
BASE_TREE = "b74497bc09c004757aa3974f3bb0622d77e20106"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
CANONICAL_EXPRESSION_SHA256 = (
    "b65a3a73cac19c57286b3cba584fc84ebda329b70006b409f12ec6e761721658"
)
EXPECTED_INPUT_HASHES = {
    "Statement.lean": "8779e87e3bc1c18654f30bb6380798da00baeaf18e8df6a588c6519ae8655ce4",
    "ObligationTree.lean": "6bf3713e057593c9690ea877901e3418d1c1b3f4e41c8f8acd43d01198e7b38e",
    "Proof.lean": "6c0c7737f36b2e0d692828ed596c4d6286d258efcd122835a84eaf8cf9b9630b",
    "obligation-registry.json": (
        "1df31d91ca04657c2c90d2effbd80daad2988a1d0b3d64f4a6e1ed8ebd2a15c9"
    ),
    "typed-graphs.json": "6248c8a590c5bc358ea0cf0de179d3e3c9db725fa30fb37d05c4be3b9c6f594d",
    "anchor-audit.json": "cf6d14efe101761821962b52d54e69c01a5c32557c3502ed1f1112217370ecf0",
}
PROOF_DECLARATIONS = (
    "cyclic_order_le_sixteen",
    "bicyclic_index_four_mul_le_sixteen",
    "torsion_ncard_eq_of_hasCyclicTorsionOrder",
    "torsion_ncard_eq_of_hasBicyclicTorsionIndex",
    "mazurRationalTorsionTarget_implies_torsionBoundAtMostSixteen",
)
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
REMAINING_ROOT_CUT = [
    "M0442-G-FIN",
    "M0442-G-RANK",
    "M0442-C-PRIME",
    "M0442-C-POWER",
    "M0442-B-TWO",
    "M0442-B-INDEX",
    "M0442-M-MODULI",
    "M0442-M-CUSPS",
    "M0442-M-RATIONAL",
    "M0442-A-REDUCTION",
    "M0442-A-DESCENT",
    "M0442-SOURCE",
    "M0442-TRUST",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            if key in value:
                raise AssertionError(f"duplicate JSON key in {path}: {key}")
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def command(*argv: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(argv, cwd=cwd, text=True).strip()


def run_lean(lean: str, source: str, output: str, *, cwd: Path, lean_path: str) -> str:
    env = os.environ.copy()
    env["LEAN_NUM_THREADS"] = "1"
    env["LEAN_PATH"] = lean_path
    result = subprocess.run(
        [lean, "--trust=0", "-t0", "-R", str(cwd), "-o", output, source],
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=300,
        check=False,
    )
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout


def main() -> None:
    assert command("git", "rev-parse", "HEAD") == BASE_REVISION
    assert command("git", "rev-parse", "HEAD^{tree}") == BASE_TREE
    assert command("git", "rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION

    for name, expected in EXPECTED_INPUT_HASHES.items():
        assert sha256(HERE / name) == expected, f"bound input changed: {name}"

    execution = load_json(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["execution_rank"] == 88
    assert item["phase"] == "proof" and item["layer"] == 4 and item["state"] == "[ ]"
    assert item["depends_on"] == ["S56-M-0442-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]

    local_dag = load_json(HERE / "task-dag.json")
    local_item = next(row for row in local_dag["nodes"] if row["id"] == ITEM)
    assert local_item["state"] == "open"

    statement = load_json(HERE / "statement.json")
    assert (
        statement["canonical_formal_target"]["elaborated_expression_sha256"]
        == CANONICAL_EXPRESSION_SHA256
    )
    registry = load_json(HERE / "obligation-registry.json")
    graphs = load_json(HERE / "typed-graphs.json")
    assert registry["root_obligation_id"] == graphs["root_obligation_id"] == "M0442-ROOT"
    boundary = graphs["closure_boundary"]
    assert boundary["closed_obligations"] == []
    assert boundary["remaining_root_cut_set"] == REMAINING_ROOT_CUT
    assert boundary["root_closed"] is False
    assert boundary["audit_complete"] is False
    assert boundary["theorem_complete"] is False

    proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
    prohibited = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(axiom|constant|opaque|unsafe|extern)[ \t]+",
        re.MULTILINE,
    )
    assert prohibited.search(proof) is None, "prohibited proof device in Proof.lean"
    for declaration in PROOF_DECLARATIONS:
        assert re.search(rf"^theorem {re.escape(declaration)}\b", proof, re.MULTILINE)
        assert f"#print axioms {declaration}" in proof
    assert "#print axioms Stage1Instances.THMM0442.ObligationTree.engine_compose" in proof

    blocker = load_json(HERE / "proof-blocker.json")
    assert blocker["item_id"] == ITEM and blocker["theorem_id"] == THEOREM
    assert blocker["base_revision"] == BASE_REVISION and blocker["base_tree"] == BASE_TREE
    assert blocker["outcome"] == "partial_proof_self_tested_root_blocked"
    assert blocker["verdict"] == "blocked" and blocker["state"] == "[_]"
    assert blocker["proof_body_present"] is True
    assert blocker["proof_body_added_this_attempt"] is False
    assert blocker["closed_obligations"] == []
    assert blocker["remaining_root_cut_set"] == REMAINING_ROOT_CUT
    assert blocker["root_closed"] is False
    assert blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False
    for name, expected in EXPECTED_INPUT_HASHES.items():
        assert blocker["source_hashes"][name] == expected
    assert blocker["source_hashes"]["check_proof.py"] == sha256(Path(__file__))
    assert blocker["selftest_manifest_written"] is True

    packet = load_json(ROOT / ".stage1-worker-selftest.json")
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    expected_changed = {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/check_proof.py",
        f"Stage1_Instances/{THEOREM}/proof-blocker.json",
        f"Stage1_Instances/{THEOREM}/proof-validation.md",
    }
    assert set(packet["changed_paths"]) == expected_changed

    status = command(
        "git",
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
        "--",
        str(HERE),
        str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == expected_changed

    manifest = load_json(LEAN_ROOT / "lake-manifest.json")
    mathlib_pin = next(package["rev"] for package in manifest["packages"] if package["name"] == "mathlib")
    assert mathlib_pin == MATHLIB_REVISION
    lean = command("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    base_lean_path = command("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)

    with tempfile.TemporaryDirectory(prefix="thm-m-0442-proof-") as temporary:
        temp = Path(temporary)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
            shutil.copyfile(HERE / name, temp / name)
        statement_output = run_lean(
            lean, "Statement.lean", "Statement.olean", cwd=temp, lean_path=base_lean_path
        )
        local_lean_path = f"{temp}:{base_lean_path}"
        tree_output = run_lean(
            lean,
            "ObligationTree.lean",
            "ObligationTree.olean",
            cwd=temp,
            lean_path=local_lean_path,
        )
        proof_output = run_lean(
            lean, "Proof.lean", "Proof.olean", cwd=temp, lean_path=local_lean_path
        )

    combined = tree_output + proof_output
    assert "MazurRationalTorsionTarget : Prop" in statement_output
    assert combined.count("depends on axioms:") == 7
    for declaration in PROOF_DECLARATIONS:
        qualified = f"Stage1Instances.THMM0442.Proof.{declaration}"
        assert f"'{qualified}' depends on axioms:" in proof_output
    engine = "'Stage1Instances.THMM0442.ObligationTree.engine_compose' depends on axioms:"
    assert engine in tree_output and engine in proof_output
    assert "sorryAx" not in combined and "error:" not in combined
    reported = set(re.findall(r"propext|Classical\.choice|Quot\.sound|sorryAx", combined))
    assert reported == ALLOWED_AXIOMS

    print("--- Statement.lean ---")
    print(statement_output, end="")
    print("--- ObligationTree.lean ---")
    print(tree_output, end="")
    print("--- Proof.lean ---")
    print(proof_output, end="")
    print("PASS THM-M-0442 partial proof replay: five consequence bodies; zero frozen obligations closed")
    print("ROOT BLOCKED: no placeholder-free MazurEngine or exact-root body is in the pinned closure")


if __name__ == "__main__":
    main()
