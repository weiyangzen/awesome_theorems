#!/usr/bin/env python3
"""Narrow proof-phase replay for THM-M-0861."""

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
THEOREM = "THM-M-0861"
ITEM = "S56-M-0861-PROOF"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
BASE_REVISION = "51c2828e82ffb19860830f78b771f80e13ad7dff"
BASE_TREE = "4655b8b40829513de6fb5661344b33fc7cd17cd1"


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


def output(*argv: str, cwd: Path) -> str:
    result = run(list(argv), cwd=cwd)
    if result.returncode:
        sys.stdout.write(result.stdout)
        raise SystemExit(result.returncode)
    return result.stdout.strip()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    proof = HERE / "Proof.lean"
    registry = json.loads((HERE / "obligation-registry.json").read_text(encoding="utf-8"))
    receipt = json.loads((HERE / "proof-receipt.json").read_text(encoding="utf-8"))
    blocker = json.loads((HERE / "proof-blocker.json").read_text(encoding="utf-8"))

    assert receipt["item_id"] == blocker["item_id"] == ITEM
    assert receipt["theorem_id"] == blocker["theorem_id"] == THEOREM
    assert receipt["inputs"]["obligation_registry_sha256"] == sha(
        HERE / "obligation-registry.json"
    )
    for key, name in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
    ):
        assert receipt["inputs"][key] == sha(HERE / name)
    assert receipt["inputs"]["lean_toolchain_sha256"] == sha(LEAN_ROOT / "lean-toolchain")
    assert receipt["inputs"]["lake_manifest_sha256"] == sha(LEAN_ROOT / "lake-manifest.json")
    assert receipt["proof_body"]["source_sha256"] == sha(proof)
    assert receipt["inputs"]["check_proof_py_sha256"] == sha(HERE / "check_proof.py")
    assert receipt["base_revision"] == blocker["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == blocker["base_tree"] == BASE_TREE
    assert output("git", "rev-parse", "HEAD", cwd=ROOT) == BASE_REVISION
    assert output("git", "rev-parse", "HEAD^{tree}", cwd=ROOT) == BASE_TREE
    assert receipt["canonical_target_expression_sha256"] == (
        "4e7919ed3b44379a42d69ef88cfb5e512248eccfe755392723cb6769c4f8e197"
    )
    assert registry["denominator_sha256"] == receipt["registry_denominator_sha256"]
    assert receipt["provisionally_closed_obligation_ids"] == [
        "M0861-L-DEGREE-LE-MAX",
        "M0861-L-INCIDENCE-FIN",
        "M0861-L-COLOR-INJECTIVE",
        "M0861-L-SUP-LOWER",
        "M0861-T-LOWER",
        "M0861-B-SMALL-EDGE-COUNT",
        "M0861-L-SMALL-PALETTE-EMBED",
    ]
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["recipe"]["covered_obligation_ids"] == receipt[
        "provisionally_closed_obligation_ids"
    ]
    assert "nine exact allowed axiom sets" in receipt["recipe"]["expected_outputs"][0][
        "semantic_hash_policy"
    ]
    assert blocker["remaining_root_cut_set"] == ["M0861-T-UPPER"]
    assert blocker["selftest_manifest_written"] is True
    packet = json.loads((ROOT / ".stage1-worker-selftest.json").read_text(encoding="utf-8"))
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"]
    assert packet["changed_paths"] == receipt["changed_paths"]
    assert set(receipt["obligation_bindings"]) == set(
        receipt["provisionally_closed_obligation_ids"]
    )
    proof_bindings = receipt["obligation_bindings"]
    for declaration in proof_bindings.values():
        assert declaration.rsplit(".", 1)[-1] in (HERE / "Proof.lean").read_text(encoding="utf-8")

    source = proof.read_text(encoding="utf-8")
    without_comments = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    without_comments = re.sub(r"--.*", "", without_comments)
    prohibited = re.search(
        r"\b(?:sorry|admit|sorryAx|axiom|constant|unsafe|implemented_by|native_decide|extern|opaque|run_tac)\b",
        without_comments,
    )
    assert prohibited is None, prohibited.group(0) if prohibited else ""
    for marker in (
        "theorem degree_le_maxDegree",
        "theorem incidenceSet_finite",
        "theorem incidentColor_injective",
        "theorem maxDegree_le_of_degree_le",
        "theorem lowerBound : LowerBoundTarget",
        "noncomputable def edgePaletteEmbedding",
        "theorem edgeColorable_of_edge_ncard_le",
        "theorem upperBound_of_boundedSatzC",
        "theorem konigEdgeColoring_of_boundedSatzC",
        "#print axioms lowerBound",
    ):
        assert marker in source, marker

    assert output("git", "rev-parse", "HEAD", cwd=LEAN_ROOT / ".lake" / "packages" / "mathlib") == MATHLIB_REVISION
    lean_exe = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    base_lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0861-proof-") as temp_dir:
        env = os.environ | {"LEAN_PATH": base_lean_path, "LEAN_NUM_THREADS": "1"}
        statement = run(
            [lean_exe, "--trust=0", "Statement.lean", "-o", str(Path(temp_dir) / "Statement.olean")],
            cwd=HERE,
            env=env,
        )
        if statement.returncode:
            sys.stdout.write(statement.stdout)
            raise SystemExit(statement.returncode)
        env["LEAN_PATH"] = temp_dir + ":" + base_lean_path
        obligations = run(
            [lean_exe, "--trust=0", "ObligationTree.lean", "-o", str(Path(temp_dir) / "ObligationTree.olean")],
            cwd=HERE,
            env=env,
        )
        if obligations.returncode:
            sys.stdout.write(obligations.stdout)
            raise SystemExit(obligations.returncode)
        lean = run([lean_exe, "--trust=0", "Proof.lean"], cwd=HERE, env=env)
    if lean.returncode:
        sys.stdout.write(lean.stdout)
        raise SystemExit(lean.returncode)

    normalized = re.sub(r"\s+", " ", lean.stdout)
    allowed = "depends on axioms: [propext, Classical.choice, Quot.sound]"
    assert normalized.count(allowed) == 9, lean.stdout
    assert "sorryAx" not in lean.stdout
    for declaration in (
        "degree_le_maxDegree", "incidenceSet_finite", "incidentColor_injective",
        "maxDegree_le_of_degree_le", "lowerBound", "edgePaletteEmbedding",
        "edgeColorable_of_edge_ncard_le",
        "upperBound_of_boundedSatzC",
        "konigEdgeColoring_of_boundedSatzC",
    ):
        assert declaration in lean.stdout

    print("check_proof: ok")
    print(lean.stdout, end="")


if __name__ == "__main__":
    main()
