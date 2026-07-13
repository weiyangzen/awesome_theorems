#!/usr/bin/env python3
"""Fail-closed source and pinned-kernel checks for S56-M-0041-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_DIR = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_DIR / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0041-PROOF"
THEOREM_ID = "THM-M-0041"
BASE_REVISION = "c5f6fb269f6eb84efa935ee66c4e9bab92495e61"
BASE_TREE = "7a41063c920c1b9cb849aa35c2f02ec4a4733655"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_HASHES = {
    "Statement.lean": "3b218c1a96922399bb8ed2d852d556422a92901dca10efdd431a677eaefd2b0b",
    "ObligationTree.lean": "bdf7444fdbdd6cbb7414514151c017c6c051b05565d9fee5ad0dd88828eefcdc",
    "obligation-registry.json": "7d8f26df395fa73ca9dacb9f20fe9564f8f3232491c62976f57c86ee12936cac",
}
UPSTREAM = MATHLIB / "Mathlib/LinearAlgebra/Matrix/Charpoly/Basic.lean"
UPSTREAM_SHA256 = "9e22d8fdace32c7bb8304335027b95ccb4cca18b5d430076ac4f87b2d76ca3f2"
DECLARATIONS = (
    "adjugateIdentity", "matrixPolynomialTransport", "rightFactorEvaluation",
    "scalarEvaluationTransport", "matrixCayleyHamiltonExpanded",
    "pinnedMatrixCayleyHamilton", "cayleyHamilton", "cayleyHamiltonExpanded",
)
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path} must contain a JSON object")
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def main() -> None:
    proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
    if re.search(
        r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|opaque|unsafe)\b",
        proof,
        re.MULTILINE,
    ):
        raise SystemExit("proof source contains a prohibited construct")
    for declaration in DECLARATIONS:
        if not re.search(rf"^theorem {declaration}\b", proof, re.MULTILINE):
            raise SystemExit(f"missing proof declaration: {declaration}")
        if f"#print axioms {declaration}" not in proof:
            raise SystemExit(f"missing axiom probe: {declaration}")
    for marker in (
        "import ObligationTree", "Matrix.adjugate_mul A.charmatrix",
        "congrArg matPolyEquiv h", "Polynomial.eval_mul_X_sub_C",
        "matPolyEquiv_smul_one", "Polynomial.eval_map",
        "Matrix.aeval_self_charpoly A",
        "root_of_characteristicPolynomialTransport_and_matrixCayleyHamilton",
        "characteristicPolynomialTransport pinnedMatrixCayleyHamilton",
    ):
        if marker not in proof:
            raise SystemExit(f"missing exact proof marker: {marker}")

    for filename, expected in EXPECTED_HASHES.items():
        if sha256(HERE / filename) != expected:
            raise SystemExit(f"prerequisite changed: {filename}")
    if sha256(UPSTREAM) != UPSTREAM_SHA256:
        raise SystemExit("pinned Matrix charpoly source changed")
    if (git("rev-parse", "HEAD", cwd=MATHLIB), git("rev-parse", "HEAD^{tree}", cwd=MATHLIB)) != (
        MATHLIB_REVISION, MATHLIB_TREE,
    ):
        raise SystemExit("materialized mathlib revision or tree changed")
    if (git("rev-parse", "HEAD"), git("rev-parse", "HEAD^{tree}")) != (
        BASE_REVISION, BASE_TREE,
    ):
        raise SystemExit("worker base revision or tree changed")

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if (item["theorem_id"], item["phase"], item["layer"]) != (THEOREM_ID, "proof", 4):
        raise SystemExit("authoritative proof item identity changed")
    if item["depends_on"] != ["S56-M-0041-OBLIGATION_TREE"]:
        raise SystemExit("authoritative proof dependency changed")
    if item["owned_paths"] != [f"Stage1_Instances/{THEOREM_ID}"]:
        raise SystemExit("authoritative proof ownership changed")

    result = subprocess.run(
        ["bash", f"../../Stage1_Instances/{THEOREM_ID}/check_proof.sh"],
        cwd=LEAN_DIR, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, check=False,
    )
    if result.returncode:
        print(result.stdout, end="")
        raise SystemExit(result.returncode)
    if "error:" in result.stdout or "sorryAx" in result.stdout:
        raise SystemExit("Lean output contains an error or placeholder axiom")
    for declaration in DECLARATIONS:
        qualified = f"Stage1Instances.THM_M_0041.Proof.{declaration}"
        if f"'{qualified}' depends on axioms:" not in result.stdout:
            raise SystemExit(f"missing Lean axiom report for {qualified}")
    reported = set(re.findall(r"(?:propext|Classical\.choice|Quot\.sound|sorryAx)", result.stdout))
    if reported != ALLOWED_AXIOMS:
        raise SystemExit(f"unexpected Lean axiom closure: {sorted(reported)}")

    receipt = load(HERE / "proof-receipt.json")
    if receipt["item_id"] != ITEM_ID or receipt["theorem_id"] != THEOREM_ID:
        raise SystemExit("proof receipt identity changed")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        raise SystemExit("proof receipt base changed")
    if receipt["inputs"]["proof_sha256"] != sha256(HERE / "Proof.lean"):
        raise SystemExit("proof receipt source hash is stale")
    if set(receipt["result"]["axioms"]) != ALLOWED_AXIOMS:
        raise SystemExit("proof receipt axiom set is stale")
    if receipt["result"]["theorem_complete"] is not False:
        raise SystemExit("proof receipt may not claim theorem completion")

    packet = load(ROOT / ".stage1-worker-selftest.json")
    required_packet_fields = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    if set(packet) != required_packet_fields:
        raise SystemExit("worker packet fields changed")
    if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
        raise SystemExit("worker packet identity or state changed")
    if packet["base_revision"] != BASE_REVISION:
        raise SystemExit("worker packet base changed")
    if packet["known_failures"] != receipt["known_failures"]:
        raise SystemExit("worker packet and receipt failure boundaries disagree")

    print(
        "PASS THM-M-0041 proof: exact pinned and expanded roots elaborated; "
        "axioms propext, Classical.choice, Quot.sound"
    )


if __name__ == "__main__":
    main()
