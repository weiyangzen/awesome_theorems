#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0028-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0028"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0028-RELEASE"
THEOREM = "THM-M-0028"
BASE_REVISION = "75ab5edd624df749325d391b41b669f8d72774b2"
BASE_TREE = "26562e2b8168d91a92a8164c9d8f0fc55178836e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "89e7e911ed4a5b75c153d824133091ad74ba20a0ecab19bd609b23a54badbee4"
DENOMINATOR_SHA256 = "65d02abdd95b23837143f3a9562ea2ae68a7f0e32f917af40827e25b2aec121b"
EXPECTED_INPUTS = {
    "instance.json": "c41d5af8f52edcc8880388af9e9db7d3d46964f5d80f809c84582e97f9f7b077",
    "task-dag.json": "6517003fcbf5a12a47411fb7f5503d56fdf9f1154f9c4647bac4af77d1f46f8b",
    "statement.json": "bc45c9ddbdb23f2675c2768b5d4dd4e3da097a905fab72e78fb072051dc149b5",
    "source-statement-crosswalk.md": "8f62995f5219b9817d2cec48c790b42bc76f214b32f51836d6ad5bd39e86997d",
    "obligation-registry.json": "ec5c959612d823cffb5863ec0e82e858d1a214948b3a9fbb3a11489176bb0344",
    "typed-graphs.json": "3502e4422934fa7e76124f969b06694d50fcdfc917062315f0d605c535602ae5",
    "ObligationTree.lean": "7c58c2e8b7c63608abfa1f3baeb161b8f80d9f0a159aca962d756d13389f0980",
    "Proof.lean": "eaeb61f403d1cf97fe53de9d4140cb6c4bc9acf4cae05a9b715e6e7a27014bff",
    "proof-receipt.json": "bf7a963cf23bfb06d7f77ffc2dea66f981735c7897179302e592810304492c96",
    "Validation.lean": "8e9e79e197d06fc8a881775a23ae389b1365492542905b6a750874b8aac9c066",
    "validation-receipt.json": "109fa6a0bf8d5d4828c63a6a75687ae309a40a13d2311e30a827a234469bd892",
    "validation-spec.json": "11a2675ad10541e60d07ce6850678d859871ab025ba14450210901830880a4e6",
    "check_validation.py": "50b27eb447eb7d2f9bbf2dd655e9626b661586796f53b2499161ac98a07c38dd",
}
EXPECTED_CHANGES = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release.md",
}
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )


def checked(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    result = run(argv, cwd=cwd, env=env)
    assert result.returncode == 0, (argv, result.stdout)
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return checked(["git", *args], cwd=cwd).strip()


def assert_axioms(output: str, declaration: str, expected: set[str]) -> None:
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)\]",
        output,
        re.DOTALL,
    )
    assert match is not None, declaration
    actual = {part.strip() for part in match.group(1).split(",")}
    assert actual == expected, (declaration, actual)


def replay_differential_validation() -> str:
    lean = checked(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lean_path = checked(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT
    ).strip()
    base_env = os.environ.copy()
    base_env.update({"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"})
    with tempfile.TemporaryDirectory(prefix="m0028-release-") as tmp_name:
        tmp = Path(tmp_name)
        for name in ("Statement.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        statement_env = base_env.copy()
        statement_env["LEAN_PATH"] = lean_path
        checked(
            [lean, "-o", "Statement.olean", "Statement.lean"],
            cwd=tmp,
            env=statement_env,
        )
        validation_env = base_env.copy()
        validation_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        output = checked([lean, "Validation.lean"], cwd=tmp, env=validation_env)

    small_axioms = {"propext", "Quot.sound"}
    assert output.count("Declarations are sorry-free!") == 3
    assert_axioms(output, "isNoetherianRing_iff_ideal_fg", small_axioms)
    assert_axioms(output, "monotone_stabilizes_iff_noetherian", EXPECTED_AXIOMS)
    assert_axioms(
        output,
        "Stage1Instances.THM_M_0028.Validation.differentialIdealAscendingChainTheorem",
        EXPECTED_AXIOMS,
    )
    assert "sorryAx" not in output
    return output


def main() -> None:
    decision = load(HERE / "release-decision.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale release input: {name}"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1073
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    dependency = next(
        row for row in execution["items"] if row["id"] == "S56-M-0028-VALIDATION"
    )
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1073,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0028-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert dependency["state"] == "[_]"
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-0028-VALIDATION"]

    accepted_vector = {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["lifecycle_mode"] == local_dag["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == accepted_vector
    assert instance["accepted_receipt_ids"] == instance["accepted_proof_state"] == []
    assert local_dag["accepted_states"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert local_dag["audit_complete"] is local_dag["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == [
        "M0028-B-FG-NOETHERIAN",
        "M0028-B-NOETHERIAN-CHAIN",
        "M0028-S-FOUNDATION",
        "M0028-X-SOURCE",
        "M0028-X-PROVENANCE",
        "M0028-X-TRUST",
        "M0028-X-READABLE",
        "M0028-X-WORKFLOW",
    ]
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
        EXPRESSION_SHA256
    )
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False and proof["result"]["root_kernel_closed"] is True
    assert proof["accepted_closed_obligation_ids"] == []
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["result"]["exact_root_kernel_closed"] is True
    assert validation["result"]["accepted_root_machine_debt"] == "M3"
    assert validation["result"]["accepted_closed_obligations"] == []
    assert validation["result"]["hermetic_release_gate"] == "fail_closed"
    assert validation["result"]["complete_tcb_gate"] == "fail_closed"
    assert validation["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == packet["item_id"] == ITEM
    assert decision["theorem_id"] == THEOREM and decision["intent"] == "release"
    assert decision["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    assert decision["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == packet["state"] == "[_]"
    assert decision["release_grade"] is False and decision["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector"]["accepted_before"] == accepted_vector
    assert decision["root_vector"]["accepted_after"] == accepted_vector
    assert decision["accepted_receipt_ids"] == []
    assert decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
        "release_accepted": False,
    }
    assert decision["dependency"]["receipt_sha256"] == EXPECTED_INPUTS[
        "validation-receipt.json"
    ]
    assert decision["dependency"]["master_accepted"] is False
    assert decision["first_failed_gate"]["gate_id"] == (
        "S56-10.2-DEPENDENCY-ACCEPTANCE"
    )
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    for name, expected in EXPECTED_INPUTS.items():
        assert decision["reconciled_inputs"][name] == expected
    assert decision["reconciled_inputs"]["check_release.py"] == sha256(
        HERE / "check_release.py"
    )
    required_cut_fragments = (
        "master acceptance",
        "H0",
        "R0",
        "TCB",
        "empty-cache",
        "SBOM",
        "two signed attestations",
        "minimal release verifier",
        "deterministic content-addressed",
    )
    cut_text = "\n".join(decision["remaining_root_cut_set"])
    for fragment in required_cut_fragments:
        assert fragment in cut_text, fragment

    historical_validator = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert 'BASE_REVISION = "a16267e7165144d202080fb647261658fa75ceb2"' in (
        historical_validator
    )
    assert 'packet = load(ROOT / ".stage1-worker-selftest.json")' in historical_validator
    assert decision["evidence_reconciliation"]["recorded_validation_recipe_replay"].startswith(
        "stale_at_integrated_snapshot"
    )

    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    proof_output = checked(["bash", str(HERE / "check_proof.sh")])
    assert proof_output.count("Declarations are sorry-free!") == 6
    differential_output = replay_differential_validation()
    assert differential_output.count("Declarations are sorry-free!") == 3
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert set(packet["changed_paths"]) == set(decision["changed_paths"]) == EXPECTED_CHANGES
    assert packet["known_failures"] == decision["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == EXPECTED_CHANGES, actual_changes
    for relative in EXPECTED_CHANGES:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0028 release evidence reconciliation")
    print("PASS narrow Lean replay: exact direct, frozen-composition, and differential roots elaborate")
    print("BLOCKED dependency: S56-M-0028-VALIDATION is provisional and not master accepted")
    print("BLOCKED release gates: H0/R0, full TCB, hermetic replay, independent verification, and bundle")
    print("verdict=blocked; lifecycle=planned; AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false")


if __name__ == "__main__":
    main()
