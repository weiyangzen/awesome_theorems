#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0025-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0025"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
DECISION_BASE = "7d0965498598e684e3e3d0a01836c2bf36a02959"
DECISION_TREE = "753e16a89fce09f051af066f8b58d3e6b2722ade"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict), name
    return value


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


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


def git(*args: str) -> str:
    result = run(["git", *args])
    assert result.returncode == 0, result.stdout
    return result.stdout.strip()


def assert_axioms(output: str, declaration: str) -> None:
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)\]",
        output,
        re.DOTALL,
    )
    assert match is not None, (declaration, output)
    actual = {part.strip() for part in match.group(1).split(",")}
    assert actual == EXPECTED_AXIOMS, (declaration, actual)


def replay_validation_probe() -> str:
    lean_result = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT)
    path_result = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT)
    assert lean_result.returncode == path_result.returncode == 0
    lean = lean_result.stdout.strip()
    lean_path = path_result.stdout.strip()
    base_env = os.environ.copy()
    base_env.update({"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"})
    with tempfile.TemporaryDirectory(prefix="m0025-release-") as tmp_name:
        tmp = Path(tmp_name)
        for name in ("Statement.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        statement_env = base_env.copy()
        statement_env["LEAN_PATH"] = lean_path
        statement_result = run(
            [lean, "-o", "Statement.olean", "Statement.lean"],
            cwd=tmp,
            env=statement_env,
        )
        assert statement_result.returncode == 0, statement_result.stdout
        validation_env = base_env.copy()
        validation_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        validation_result = run(
            [lean, "Validation.lean"], cwd=tmp, env=validation_env
        )
        assert validation_result.returncode == 0, validation_result.stdout
    output = validation_result.stdout
    for declaration in (
        "Polynomial.isNoetherianRing",
        "Stage1Instances.THM_M_0025.Validation.differentialHilbertBasisTheorem",
    ):
        assert_axioms(output, declaration)
    assert output.count("Declarations are sorry-free!") == 2
    assert "sorryAx" not in output
    return output


def main() -> None:
    decision = load("release-decision.json")
    instance = load("instance.json")
    local_dag = load("task-dag.json")
    registry = load("obligation-registry.json")
    graphs = load("typed-graphs.json")
    proof = load("proof-receipt.json")
    validation = load("validation-receipt.json")
    targets = json.loads(
        (ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
    )
    execution = json.loads(
        (ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text(
            encoding="utf-8"
        )
    )

    assert decision["base_revision"] == DECISION_BASE
    assert decision["base_tree"] == DECISION_TREE
    assert git("rev-parse", f"{DECISION_BASE}^{{tree}}") == DECISION_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == "THM-M-0025")
    release_item = next(row for row in execution["items"] if row["id"] == decision["item_id"])
    validation_item = next(row for row in execution["items"] if row["id"] == validation["item_id"])

    assert target["execution_rank"] == release_item["execution_rank"] == 1070
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    assert release_item["phase"] == "release" and release_item["state"] == "[ ]"
    assert release_item["depends_on"] == [validation_item["id"]]
    assert release_item["owned_paths"] == ["Stage1_Instances/THM-M-0025"]
    assert validation_item["state"] == "[_]"

    assert instance["lifecycle"] == "planned" and instance["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is False
    assert local_dag["lifecycle"] == "planned" and local_dag["accepted_states"] == []
    assert local_dag["audit_complete"] is local_dag["theorem_complete"] is False
    local_release = next(row for row in local_dag["tasks"] if row["id"] == decision["item_id"])
    assert local_release["state"] == "open"

    assert registry["root_obligation_id"] == "M0025-ROOT"
    assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["accepted_closed_obligations"] == []
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == "S56-M-0025-RELEASE"
    assert decision["theorem_id"] == "THM-M-0025" and decision["intent"] == "release"
    assert decision["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == []

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0025-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == digest("validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["worker_projection"] == "[_]" and dependency["master_accepted"] is False

    for name, expected in decision["reconciled_inputs"].items():
        assert digest(name) == expected, f"stale reconciled input: {name}"

    root = decision["root_vector"]
    assert root["accepted_before"] == root["accepted_after"] == ["H1", "M3", "R3"]
    assert root["best_provisional_evidence"] == ["H1", "M0-W", "R3"]
    terminal = decision["terminal_decisions"]
    assert terminal["audit_complete"] is terminal["theorem_complete"] is False
    assert terminal["release_accepted"] is False
    assert terminal["audit_z"] == terminal["theorem_z"] == "blocked"

    assert proof["support_state"] == validation["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is validation["accepted"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    result = validation["result"]
    assert result["exact_root_kernel_closed"] is True
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_closed_obligations"] == []
    assert result["hermetic_release_gate"] == "fail_closed"
    assert result["complete_provenance_gate"] == "fail_closed"
    assert result["complete_tcb_gate"] == "fail_closed"
    assert result["independent_distinct_runner_gate"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False

    evidence = decision["evidence_reconciliation"]
    assert evidence["structured_state_freshness"].startswith("failed:")
    assert evidence["local_task_state_freshness"].startswith("failed:")
    assert evidence["recorded_validation_recipe_replay"].startswith("failed:")
    assert not (ROOT / ".stage1-worker-selftest.json").exists() or load_selftest(decision)
    historical_replay = run(
        ["python3", "-B", str(HERE / "check_validation.py")], cwd=ROOT
    )
    assert historical_replay.returncode != 0
    assert "AssertionError" in historical_replay.stdout

    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    cut = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "S56-M-0025-VALIDATION", "typed-graph", "replayable recipe", "AUDIT-Z",
        "H0 primary-source", "R0 node-by-node", "transitive declaration",
        "empty-cache network-denied cold build", "SBOM and license",
        "two signed attestations", "minimal release verifier",
        "mutation, differential, and metamorphic",
        "deterministic content-addressed evidence bundle",
    ):
        assert fragment in cut, f"release cut set omits {fragment!r}"
    for key in (
        "audit_inventory_reconciliation", "human_source_acceptance",
        "readability_acceptance", "complete_provenance_and_trust_closure",
        "hermetic_release_reproduction", "supply_chain_closure",
        "independent_release_verification", "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert evidence[key] == "missing", key

    validation_output = replay_validation_probe()
    assert "Declarations are sorry-free!" in validation_output
    print("PASS S56-M-0025-RELEASE reconciliation")
    print("narrow replay: exact root provisional; recorded validation recipe is stale")
    print("verdict=blocked lifecycle=planned root_vector=H1/M3/R3")
    print("AUDIT-Z=false THEOREM-Z=false theorem_complete=false accepted_receipts=0")
    print("first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE")
    print("first_failed_release_gate=S56-10.6-HERMETIC-COLD-BUILD")
    print(f"platform={platform.system()} {platform.machine()}")


def load_selftest(decision: dict) -> bool:
    packet_path = ROOT / ".stage1-worker-selftest.json"
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == decision["item_id"] and packet["state"] == "[_]"
    assert packet["base_revision"] == decision["base_revision"]
    assert packet["changed_paths"] == decision["changed_paths"]
    return True


if __name__ == "__main__":
    main()
