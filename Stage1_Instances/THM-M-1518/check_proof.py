#!/usr/bin/env python3
"""Fail-closed source, receipt, and pinned Lean checks for THM-M-1518."""

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
LEAN_DIR = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1518-PROOF"
THEOREM = "THM-M-1518"
BASE = "bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad"
MATHLIB_REV = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
SOURCES = (
    "Statement.lean",
    "ObligationTree.lean",
    "Proof.lean",
    "WeakToPointwise.lean",
    "ExactProof.lean",
)
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def source_without_comments(text: str) -> str:
    text = re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)
    return re.sub(r"--.*", "", text)


for name in SOURCES:
    source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
    forbidden = re.compile(
        r"\b(sorry|admit|sorryAx|implemented_by|native_decide)\b"
        r"|^\s*(axiom|unsafe|opaque|external|constant)\b",
        flags=re.MULTILINE,
    )
    assert forbidden.search(source) is None, f"prohibited construct in {name}"

proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
weak = (HERE / "WeakToPointwise.lean").read_text(encoding="utf-8")
exact = (HERE / "ExactProof.lean").read_text(encoding="utf-8")
for fragment in (
    "theorem firstVariation_formula",
    "theorem firstVariationFormula : ObligationTree.FirstVariationFormula",
    "#print axioms firstVariationFormula",
):
    assert fragment in proof, fragment
for fragment in (
    "theorem weak_to_pointwise_abstract",
    "theorem weakToPointwise : WeakToPointwise",
    "Measure.eqOn_open_of_ae_eq",
    "#print axioms weakToPointwise",
):
    assert fragment in weak, fragment
for fragment in (
    "theorem stationaryActionEulerLagrange : StationaryActionEulerLagrangeTarget",
    "ObligationTree.exactTarget_of_packages",
    "firstVariationFormula ObligationTree.weakToPointwise",
    "#print axioms stationaryActionEulerLagrange",
):
    assert fragment in exact, fragment

receipt = load(HERE / "proof-receipt.json")
assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
assert receipt["base_revision"] == BASE
assert receipt["support_state"] == "provisional_worker_selftest"
assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
assert receipt["canonical_expression_sha256"] == (
    "4cc15786f13f4e4ad7594012ab3e96613f5bffbf572523e8282b41139fe6979f"
)
assert receipt["inputs"]["statement_sha256"] == sha(HERE / "Statement.lean")
assert receipt["inputs"]["obligation_tree_sha256"] == sha(
    HERE / "ObligationTree.lean"
)
assert receipt["inputs"]["obligation_registry_sha256"] == sha(
    HERE / "obligation-registry.json"
)
for name in ("Proof.lean", "WeakToPointwise.lean", "ExactProof.lean"):
    assert receipt["proof_bodies"][name]["source_sha256"] == sha(HERE / name)
assert receipt["result"]["root_kernel_closed"] is True
assert receipt["result"]["accepted_root_closed"] is False
assert receipt["result"]["theorem_complete"] is False
assert set(receipt["result"]["axioms"]) == ALLOWED_AXIOMS
assert receipt["debt_vector"]["accepted_before"] == {
    "H": "H2", "M": "M4", "R": "R3"
}
assert receipt["debt_vector"]["proposed_after_proof_master_acceptance"] == {
    "H": "H2", "M": "M0-L", "R": "R3"
}
assert receipt["debt_vector"]["accepted_after_worker_selftest"] == {
    "H": "H2", "M": "M4", "R": "R3"
}

registry = load(HERE / "obligation-registry.json")
graphs = load(HERE / "typed-graphs.json")
assert receipt["inputs"]["registry_denominator_sha256"] == registry[
    "denominator_sha256"
]
assert graphs["closure_boundary"]["root_closed"] is False
assert graphs["closure_boundary"]["theorem_complete"] is False

selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    selftest = load(selftest_path)
    assert set(selftest) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert selftest["item_id"] == ITEM and selftest["state"] == "[_]"
    assert selftest["base_revision"] == BASE
    assert selftest["known_failures"] == receipt["known_failures"]
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
    )
    actual_changes = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == set(selftest["changed_paths"]), (
        actual_changes,
        set(selftest["changed_paths"]),
    )

manifest = load(LEAN_DIR / "lake-manifest.json")
assert next(p["rev"] for p in manifest["packages"] if p["name"] == "mathlib") == (
    MATHLIB_REV
)

with tempfile.TemporaryDirectory(prefix="thm-m-1518-proof-") as directory:
    cache = Path(directory)
    module_dir = cache / "Stage1_Instances" / THEOREM
    module_dir.mkdir(parents=True)
    env = os.environ.copy()
    env["LEAN_NUM_THREADS"] = "1"

    commands = [
        [
            "lake", "env", "lean", "--trust=0", "-R", str(ROOT), "-o",
            str(module_dir / "Statement.olean"), str(HERE / "Statement.lean"),
        ],
        [
            "lake", "env", "lean", "--trust=0", "-R", str(ROOT), "-o",
            str(module_dir / "ObligationTree.olean"),
            str(HERE / "ObligationTree.lean"),
        ],
        [
            "lake", "env", "lean", "--trust=0", "-R", str(ROOT), "-o",
            str(module_dir / "Proof.olean"), str(HERE / "Proof.lean"),
        ],
        [
            "lake", "env", "lean", "--trust=0", "-R", str(ROOT), "-o",
            str(module_dir / "WeakToPointwise.olean"),
            str(HERE / "WeakToPointwise.lean"),
        ],
        [
            "lake", "env", "lean", "--trust=0", "-R", str(ROOT), "-o",
            str(module_dir / "ExactProof.olean"), str(HERE / "ExactProof.lean"),
        ],
    ]

    output = []
    for index, command in enumerate(commands):
        step_env = env.copy()
        if index:
            step_env["LEAN_PATH"] = f"{cache}:{step_env.get('LEAN_PATH', '')}"
        result = subprocess.run(
            command,
            cwd=LEAN_DIR,
            env=step_env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if result.returncode or index >= 2:
            sys.stdout.write(result.stdout)
        assert result.returncode == 0, f"Lean step {index + 1} failed"
        output.append(result.stdout)

    all_output = "\n".join(output)
    for declaration in (
        "Stage1Instances.THM_M_1518.firstVariationFormula",
        "Stage1Instances.THM_M_1518.ObligationTree.weakToPointwise",
        "Stage1Instances.THM_M_1518.stationaryActionEulerLagrange",
    ):
        match = re.search(
            re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
            all_output,
            flags=re.DOTALL,
        )
        assert match, f"missing axiom report for {declaration}"
        actual = {name.strip() for name in match.group(1).split(",")}
        assert actual == ALLOWED_AXIOMS, (declaration, actual)
    assert "sorryAx" not in all_output

    sorry_probe = cache / "NoSorry.lean"
    sorry_probe.write_text(
        "import «Stage1_Instances».«THM-M-1518».ExactProof\n"
        "import Mathlib.Util.AssertNoSorry\n"
        "assert_no_sorry Stage1Instances.THM_M_1518.firstVariationFormula\n"
        "assert_no_sorry "
        "Stage1Instances.THM_M_1518.ObligationTree.weakToPointwise\n"
        "assert_no_sorry "
        "Stage1Instances.THM_M_1518.stationaryActionEulerLagrange\n",
        encoding="utf-8",
    )
    probe_env = env.copy()
    probe_env["LEAN_PATH"] = f"{cache}:{probe_env.get('LEAN_PATH', '')}"
    probe = subprocess.run(
        ["lake", "env", "lean", "--trust=0", str(sorry_probe)],
        cwd=LEAN_DIR,
        env=probe_env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    sys.stdout.write(probe.stdout)
    assert probe.returncode == 0, "transitive sorry probe failed"

print("PASS THM-M-1518 proof phase: exact frozen root kernel-closed")
print(f"exact proof source sha256: {sha(HERE / 'ExactProof.lean')}")
print("accepted state unchanged; validation, release, and master acceptance remain open")
