#!/usr/bin/env python3
"""Re-run the local, nonrelease validation claimed for THM-M-0399."""

from pathlib import Path
import hashlib
import json
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RECORD = json.loads((HERE / "validation-phase.json").read_text())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"validation phase check failed: {message}")


def run(argv: list[str], cwd: Path = ROOT, stdin: str | None = None) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        input=stdin,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
    )
    require(result.returncode == 0, f"{' '.join(argv)} failed:\n{result.stdout}")
    return result.stdout


require(RECORD["item_id"] == "S56-M-0399-VALIDATION", "wrong item")
require(RECORD["theorem_id"] == "THM-M-0399", "wrong theorem")
require(RECORD["verdict"] == "blocked", "open root must block release-grade validation")
require(RECORD["theorem_complete"] is False, "open Roth root reported complete")
require(RECORD["root_vector"] == {"H": "H1", "M": "M4", "R": "R4"},
        "debt vector drift")
require(RECORD["closed_obligation_ids"] == ["M0399-ROOT-COMPOSE"],
        "unexpected proof credit")
require("M0399-STRONG-FINITE" in RECORD["remaining_root_cut_set"],
        "central open premise omitted")
require(RECORD["release_gate_results"]["exact_root_kernel_closure"] == "failed_open_root",
        "root closure result is not fail-closed")
require(RECORD["release_gate_results"]["hermetic_cold_offline_replay"] ==
        "not_run_worker_environment_not_hermetic",
        "warm shared-cache replay misreported as hermetic")
require(RECORD["release_gate_results"]["independent_verification"] ==
        "not_run_no_independent_runner_or_attestor",
        "same-workspace replay misreported as independent")
require(RECORD["accepted_receipt_ids"] == [], "worker invented accepted receipts")

for relative, expected in RECORD["input_sha256"].items():
    actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    require(actual == expected, f"input digest drift: {relative}")

source = (HERE / "RothComposition.lean").read_text()
for forbidden in (r"\bsorry\b", r"\badmit\b", r"\baxiom\b", r"\bunsafe\b", r"sorryAx"):
    require(re.search(forbidden, source) is None, f"forbidden source token: {forbidden}")

statement_output = run(
    ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0399/RothStatement.lean"],
    ROOT / "Formalizations" / "Lean",
)
require("Stage1Instances.THM_M_0399.RothStatement" in statement_output,
        "canonical declaration was not elaborated")

composition_output = run(
    ["lake", "env", "lean", "../../Stage1_Instances/THM-M-0399/RothComposition.lean"],
    ROOT / "Formalizations" / "Lean",
)
require("rothStatement_of_strongFinite" in composition_output,
        "composition declaration was not checked")

axiom_probe = source.replace(
    "#check Stage1Instances.THM_M_0399.rothStatement_of_strongFinite",
    "#print axioms Stage1Instances.THM_M_0399.rothStatement_of_strongFinite",
)
axiom_output = run(
    ["lake", "env", "lean", "--stdin"],
    ROOT / "Formalizations" / "Lean",
    axiom_probe,
)
require("[propext, Classical.choice, Quot.sound]" in axiom_output,
        f"unexpected axiom report: {axiom_output.strip()}")

for validator, marker in (
    ("check_statement.py", '"statement_sha256"'),
    ("check_anchor_audit.py", "anchor audit check: ok"),
    ("check_obligation_tree.py", "obligation tree check: ok"),
    ("check_proof_phase.py", "proof phase check: ok"),
):
    output = run(["python3", str(HERE / validator)])
    require(marker in output, f"missing success marker from {validator}")

print("validation phase check: ok; local evidence replayed, release gates truthfully blocked")
