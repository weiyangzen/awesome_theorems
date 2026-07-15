#!/usr/bin/env python3
"""Fail-closed proof-phase replay for S56-M-0841-PROOF."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0841-PROOF"
THEOREM = "THM-M-0841"
BASE_REVISION = "aef94f39853f9222e48f83b2358a6822aafd3c50"
BASE_TREE = "8c42e198fdbcc36b0f5cc0f865e0961715a35c17"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EVIDENCED = ["M0841-S-COMPLEMENT-TRANSPORT"]
DECLARATIONS = (
    "cast_choose_two",
    "card_edgeFinset_compl",
    "sparseFromDense",
    "denseFamily_of_base_step",
    "erdosStone_of_dense_base_step",
)


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None,
        timeout: int = 180) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )


def output(*argv: str, cwd: Path = ROOT) -> str:
    result = run(list(argv), cwd=cwd)
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout.strip()


def main() -> None:
    proof_path = HERE / "Proof.lean"
    proof = proof_path.read_text(encoding="utf-8")
    uncommented = re.sub(r"/-.*?-/", "", proof, flags=re.DOTALL)
    uncommented = re.sub(r"--.*", "", uncommented)
    prohibited = re.search(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|unsafe|implemented_by|"
        r"native_decide|extern|opaque|run_tac)\b",
        uncommented,
    )
    assert prohibited is None, prohibited.group(0) if prohibited else ""
    for marker in (
        "import ObligationTree",
        "theorem cast_choose_two",
        "theorem card_edgeFinset_compl",
        "theorem sparseFromDense : SparseFromDense",
        "dense r hr (epsilon / 2)",
        "rw [card_edgeFinset_compl, Nat.cast_sub hle, cast_choose_two]",
        "theorem denseFamily_of_base_step",
        "theorem erdosStone_of_dense_base_step",
        "assert_no_sorry sparseFromDense",
        "#print axioms sparseFromDense",
    ):
        assert marker in proof, marker

    assert output("git", "rev-parse", "HEAD") == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item["theorem_id"] == THEOREM and item["phase"] == "proof"
    assert item["layer"] == 4 and item["state"] in {"[ ]", "[_]"}
    assert item["depends_on"] == ["S56-M-0841-OBLIGATION_TREE"]
    assert item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    predecessor = next(
        row for row in execution["items"] if row["id"] == item["depends_on"][0]
    )
    assert predecessor["state"] in {"[_]", "[x]"}

    task_dag = load(HERE / "task-dag.json")
    local_task = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open" and task_dag["accepted_states"] == []

    registry = load(HERE / "obligation-registry.json")
    receipt = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    assert registry["denominator_sha256"] == receipt["registry_denominator_sha256"]
    assert registry["status_observed_after_freeze"]["accepted_closed_obligations"] == []
    obligation = next(
        row for row in registry["obligations"]
        if row["obligation_id"] == EVIDENCED[0]
    )
    assert receipt["obligation_statement_fingerprints"][EVIDENCED[0]] == obligation[
        "statement_fingerprint"
    ]
    assert receipt["item_id"] == blocker["item_id"] == ITEM
    assert receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert receipt["base_revision"] == blocker["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == blocker["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["exact_declaration_evidence_ids"] == EVIDENCED
    assert receipt["provisionally_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["exact_declaration_bindings"] == {
        EVIDENCED[0]: "Stage1Instances.THM_M_0841_Proof.sparseFromDense"
    }
    assert receipt["proof_body"]["source_sha256"] == sha(proof_path)
    for key, name in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("validation_specs_sha256", "validation-specs.json"),
        ("check_proof_py_sha256", "check_proof.py"),
    ):
        assert receipt["inputs"][key] == sha(HERE / name), key
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert blocker["exact_declaration_evidence_ids"] == EVIDENCED
    assert blocker["provisionally_closed_obligation_ids"] == []
    assert blocker["remaining_root_cut_set"] == [
        "M0841-S-COMPLEMENT-TRANSPORT",
        "M0841-B-R-TWO",
        "M0841-B-R-GE-THREE",
    ]
    assert blocker["formal_premise_cut_using_direct_body"] == [
        "M0841-B-R-TWO", "M0841-B-R-GE-THREE"
    ]
    assert blocker["selftest_manifest_written"] is True
    assert receipt["root_vector_proposed"] == {
        "H": "H1", "M": "M3", "R": "R4"
    }
    assert receipt["internal_per_node_composition_credit"] is False
    plans = load(HERE / "typed-graphs.json")["unverified_decomposition_plans"]
    assert receipt["unverified_internal_composition_count"] == len(plans) == 25
    transport_plan = next(
        row for row in plans
        if row["parent_obligation_id"] == EVIDENCED[0]
    )
    assert transport_plan["planned_child_ids"] == [
        "M0841-N-DENSE-FORM", "M0841-N-THRESHOLD-PACKAGE"
    ]
    assert transport_plan["status"] == (
        "source_body_decomposition_unverified_as_child_to_parent_composition"
    )

    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    assert output("git", "rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert output("git", "status", "--short", cwd=mathlib) == ""

    lean_bin = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0841-proof-") as temporary:
        temp = Path(temporary)
        env = {
            **os.environ,
            "LEAN_PATH": lean_path,
            "LEAN_NUM_THREADS": "1",
            "LC_ALL": "C",
            "LANG": "C",
            "NO_COLOR": "1",
        }
        statement = run(
            [lean_bin, "--trust=0", "-o", str(temp / "Statement.olean"),
             str(HERE / "Statement.lean")],
            cwd=ROOT,
            env=env,
        )
        if statement.returncode:
            sys.stdout.write(statement.stdout)
            raise SystemExit(statement.returncode)
        local_env = {**env, "LEAN_PATH": f"{temp}{os.pathsep}{lean_path}"}
        obligations = run(
            [lean_bin, "--trust=0", "-o", str(temp / "ObligationTree.olean"),
             str(HERE / "ObligationTree.lean")],
            cwd=ROOT,
            env=local_env,
        )
        if obligations.returncode:
            sys.stdout.write(obligations.stdout)
            raise SystemExit(obligations.returncode)
        lean = run(
            [lean_bin, "--trust=0", str(proof_path)],
            cwd=ROOT,
            env=local_env,
        )
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)

    normalized = re.sub(r"\s+", " ", lean.stdout)
    allowed = "depends on axioms: [propext, Classical.choice, Quot.sound]"
    assert normalized.count(allowed) == len(DECLARATIONS), lean.stdout
    assert "sorryAx" not in lean.stdout
    assert "Declarations are sorry-free!" in lean.stdout
    for declaration in DECLARATIONS:
        assert f"THM_M_0841_Proof.{declaration}" in lean.stdout

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert packet["known_failures"] == receipt["known_failures"]
    status = output("git", "status", "--short", "--untracked-files=all")
    actual = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == set(packet["changed_paths"]), (actual, packet["changed_paths"])

    print("check_proof: ok")
    print("exact body evidence: M0841-S-COMPLEMENT-TRANSPORT")
    print("canonical closure withheld: open logical-decomposition children")
    print("frozen root cut: M0841-S-COMPLEMENT-TRANSPORT, M0841-B-R-TWO, "
          "M0841-B-R-GE-THREE")
    print(lean.stdout, end="")


if __name__ == "__main__":
    main()
