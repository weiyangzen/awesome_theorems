#!/usr/bin/env python3
"""Fail-closed source and pinned-kernel checks for S56-M-0451-PROOF."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LEAN_DIR = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_DIR / ".lake" / "packages" / "mathlib"
ITEM_ID = "S56-M-0451-PROOF"
THEOREM_ID = "THM-M-0451"
BASE_REVISION = "c45f3c7090cb4adf616d45e5414985f956e807b2"
BASE_TREE = "da6f991c07f11e8608ddc090af9356558d64d360"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_HASHES = {
    "Statement.lean": "f288b8eb0959aa199c316bc0727f84a85df9d3c3612c257da49b94dd8a6a6c52",
    "ObligationTree.lean": "96a2a4b4955baad71cd23ca45e3a60070d84dc6793f4751036d5fabc70831f38",
    "obligation-registry.json": "b31f76ecf12e6936dcbfe0e536df7b0a353f0adf83af31d07a96341b130ae100",
}
DECLARATIONS = (
    "tateSequence_tendsto",
    "tateLimit_sub_le",
    "tateLimit_map",
    "limit_formula_of_doubling_bound",
    "bounded_difference_of_doubling_bound",
    "constructedCanonicalHeight_double",
    "constructedCanonicalHeight_nonnegative",
    "constructedCanonicalHeight_parallelogram_of_bounds",
    "constructedCanonicalHeight_quadratic_of_bounds",
    "constructedCanonicalHeight_torsion_zero",
    "torsion_to_zero_of_quadratic",
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


def lake_env_value(name: str) -> str:
    return subprocess.check_output(
        ["lake", "env", "printenv", name], cwd=LEAN_DIR, text=True
    ).strip()


def lean_replay() -> str:
    lean = subprocess.check_output(
        ["lake", "env", "which", "lean"], cwd=LEAN_DIR, text=True
    ).strip()
    lean_path = lake_env_value("LEAN_PATH")
    with tempfile.TemporaryDirectory(prefix="thm-m-0451-proof-") as tmp_name:
        tmp = Path(tmp_name)
        for filename in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
            shutil.copy2(HERE / filename, tmp / filename)
        commands = (
            ([lean, "-o", "Statement.olean", "Statement.lean"], lean_path),
            ([lean, "-o", "ObligationTree.olean", "ObligationTree.lean"], f"{tmp}:{lean_path}"),
            ([lean, "Proof.lean"], f"{tmp}:{lean_path}"),
        )
        output: list[str] = []
        for argv, path_value in commands:
            result = subprocess.run(
                argv,
                cwd=tmp,
                env={**__import__("os").environ, "LEAN_PATH": path_value},
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            output.append(result.stdout)
            if result.returncode:
                print("".join(output), end="")
                raise SystemExit(result.returncode)
        return "".join(output)


def main() -> None:
    proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
    if re.search(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        proof,
        re.MULTILINE,
    ):
        raise SystemExit("proof source contains a prohibited construct")
    for declaration in DECLARATIONS:
        if not re.search(rf"^(?:lemma|theorem) {declaration}\b", proof, re.MULTILINE):
            raise SystemExit(f"missing proof declaration: {declaration}")
        if f"#print axioms {declaration}" not in proof:
            raise SystemExit(f"missing axiom probe: {declaration}")
    for marker in (
        "import ObligationTree",
        "def constructedCanonicalHeight",
        "tateSequence_eq_target_sequence",
        "tateLimit_parallelogram",
        "quadratic_zsmul_of_parallelogram",
        "tateLimit_torsion_zero",
    ):
        if marker not in proof:
            raise SystemExit(f"missing exact proof marker: {marker}")

    for filename, expected in EXPECTED_HASHES.items():
        if sha256(HERE / filename) != expected:
            raise SystemExit(f"prerequisite changed: {filename}")
    if (git("rev-parse", "HEAD", cwd=MATHLIB), git("rev-parse", "HEAD^{tree}", cwd=MATHLIB)) != (
        MATHLIB_REVISION,
        MATHLIB_TREE,
    ):
        raise SystemExit("materialized mathlib revision or tree changed")
    if (git("rev-parse", "HEAD"), git("rev-parse", "HEAD^{tree}")) != (
        BASE_REVISION,
        BASE_TREE,
    ):
        raise SystemExit("worker base revision or tree changed")

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    if (item["theorem_id"], item["phase"], item["layer"]) != (
        THEOREM_ID,
        "proof",
        4,
    ):
        raise SystemExit("authoritative proof item identity changed")
    if item["depends_on"] != ["S56-M-0451-OBLIGATION_TREE"]:
        raise SystemExit("authoritative proof dependency changed")
    if item["owned_paths"] != [f"Stage1_Instances/{THEOREM_ID}"]:
        raise SystemExit("authoritative proof ownership changed")

    output = lean_replay()
    if "error:" in output or "sorryAx" in output:
        raise SystemExit("Lean output contains an error or placeholder axiom")
    for declaration in DECLARATIONS:
        qualified = f"Stage1Instances.THM_M_0451.Proof.{declaration}"
        if f"'{qualified}' depends on axioms:" not in output:
            raise SystemExit(f"missing Lean axiom report for {qualified}")
    reported = set(
        re.findall(r"(?:propext|Classical\.choice|Quot\.sound|sorryAx)", output)
    )
    if reported != ALLOWED_AXIOMS:
        raise SystemExit(f"unexpected Lean axiom closure: {sorted(reported)}")

    receipt = load(HERE / "proof-receipt.json")
    if receipt["item_id"] != ITEM_ID or receipt["theorem_id"] != THEOREM_ID:
        raise SystemExit("proof receipt identity changed")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        raise SystemExit("proof receipt base changed")
    if receipt["inputs"]["proof_sha256"] != sha256(HERE / "Proof.lean"):
        raise SystemExit("proof receipt source hash is stale")
    if receipt["newly_closed_obligation_ids"] != []:
        raise SystemExit("conditional bodies may not claim frozen obligation closure")
    if set(receipt["result"]["axioms"]) != ALLOWED_AXIOMS:
        raise SystemExit("proof receipt axiom set is stale")
    if receipt["result"]["root_closed"] is not False:
        raise SystemExit("proof receipt may not claim root closure")
    if receipt["result"]["theorem_complete"] is not False:
        raise SystemExit("proof receipt may not claim theorem completion")

    print(
        "PASS THM-M-0451 proof phase: conditional Tate bodies elaborated; "
        "no frozen obligation or exact root claimed closed"
    )


if __name__ == "__main__":
    main()
