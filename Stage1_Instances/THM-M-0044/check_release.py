#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0044-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0044"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0044-RELEASE"
THEOREM = "THM-M-0044"
BASE_REVISION = "eb9c2192f79a480deff66d2c0f8e31032bcc2d9f"
BASE_TREE = "57b76c2fceacd8819b0ec8b9abcd42cfcc74b8e2"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def source_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_axioms(output: str, declaration: str) -> None:
    pattern = re.compile(
        rf"'[^'\n]*{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, (declaration, output)
    observed = {part.strip() for part in match.group(1).split(",")}
    assert observed == EXPECTED_AXIOMS, (declaration, observed)


def main() -> None:
    decision = load(HERE / "release-decision.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    tasks = load(HERE / "task-dag.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    receipt = load(HERE / "release-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0044-VALIDATION"
    )
    local_release = next(row for row in tasks["tasks"] if row["id"] == ITEM)

    assert target["execution_rank"] == release_item["execution_rank"] == 1084
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    assert release_item["phase"] == "release" and release_item["state"] == "[ ]"
    assert release_item["depends_on"] == [validation_item["id"]]
    assert validation_item["state"] == "[_]"
    assert release_item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert local_release["state"] == "open" and local_release["evidence_ids"] == []
    assert tasks["lifecycle"] == "planned" and tasks["accepted_states"] == []
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["intent"] == "release" and decision["verdict"] == "blocked"
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    assert decision["support_state"] == "provisional_worker_selftest"
    assert decision["release_grade"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == []

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["intent"] == "release"
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["release_grade"] is False and receipt["accepted"] is False
    assert receipt["proposed_state"] == "[_]" and receipt["accepted_receipt_ids"] == []
    assert receipt["recipe"] == {
        "cwd": ".",
        "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"],
        "expected_exit": 0,
        "timeout_seconds": 180,
        "network": "not_used",
    }
    for name, expected in receipt["inputs"].items():
        assert digest(HERE / name) == expected, f"stale receipt input: {name}"

    for name, expected in decision["reconciled_inputs"].items():
        assert digest(HERE / name) == expected, f"stale reconciled input: {name}"

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == validation_item["id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == digest(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert dependency["worker_projection"] == "[_]"

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert registry["root_obligation_id"] == "M0044-ROOT"
    assert len(registry["obligations"]) == 39
    assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["accepted_closed_obligations"] == []
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False and proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert validation["result"]["provisional_exact_root_kernel_closed"] is True
    assert validation["result"]["accepted_root_kernel_closed"] is False
    assert validation["result"]["hermetic_release_gate"] == "fail_closed"
    assert validation["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert receipt["result"] == {
        "exit_code": 0,
        "verdict": "blocked",
        "lifecycle": "planned",
        "accepted_root_vector": ["H1", "M3", "R3"],
        "provisional_exact_root_kernel_replay": "pass",
        "observed_axioms": ["propext", "Classical.choice", "Quot.sound"],
        "audit_complete": False,
        "theorem_complete": False,
        "release_accepted": False,
    }

    root = decision["root_vector"]
    assert root["accepted_before"] == root["accepted_after"] == ["H1", "M3", "R3"]
    assert root["best_provisional_kernel_evidence"] == ["H1", "M0-L", "R3"]
    terminal = decision["terminal_decisions"]
    assert terminal == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
        "release_accepted": False,
    }
    assert decision["first_failed_gate"]["gate_id"] == (
        "S56-10.2-DEPENDENCY-ACCEPTANCE"
    )
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    assert receipt["first_failed_gate"] == decision["first_failed_gate"]
    assert receipt["first_failed_release_gate"] == decision["first_failed_release_gate"]
    assert receipt["remaining_root_cut_set"] == decision["remaining_root_cut_set"]

    evidence = decision["evidence_reconciliation"]
    assert evidence["structured_state_freshness"].startswith("failed:")
    assert evidence["receipt_snapshot_freshness"].startswith("failed:")
    assert evidence["provisional_machine_debt_classification"].startswith("conflict:")
    for key in (
        "per_obligation_reconciliation",
        "audit_inventory_reconciliation",
        "human_source_acceptance",
        "readability_acceptance",
        "complete_provenance_and_trust_closure",
        "hermetic_release_reproduction",
        "supply_chain_closure",
        "independent_release_verification",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert evidence[key].startswith("missing"), key

    cut = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "S56-M-0044-VALIDATION",
        "39 frozen obligations",
        "M0-L versus M0-W",
        "AUDIT-Z",
        "THM-M-1449",
        "H0 immutable primary-source",
        "R0 node-by-node",
        "executable/bootstrap TCB closure",
        "immutable clean release snapshot",
        "empty-cache network-denied cold build",
        "SBOM and license",
        "two signed attestations",
        "minimal release verifier",
        "mutation, differential, and metamorphic",
        "deterministic content-addressed evidence bundle",
    ):
        assert fragment in cut, f"release cut set omits {fragment!r}"

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean",
        "AnchorAudit.lean",
        "ObligationTree.lean",
        "Proof.lean",
        "Validation.lean",
    ):
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    base_env = dict(os.environ)
    base_env.update({"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"})
    with tempfile.TemporaryDirectory(prefix="m0044-release-") as tmp_name:
        tmp = Path(tmp_name)
        statement_output = run(
            [
                "lake", "env", "lean", "--root", str(ROOT),
                "-o", str(tmp / "Statement.olean"), str(HERE / "Statement.lean"),
            ],
            cwd=LEAN_ROOT,
            env=base_env,
        )
        module_env = dict(base_env)
        module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        obligation_output = run(
            [
                "lake", "env", "lean", "--root", str(ROOT),
                "-o", str(tmp / "ObligationTree.olean"),
                str(HERE / "ObligationTree.lean"),
            ],
            cwd=LEAN_ROOT,
            env=module_env,
        )
        proof_output = run(
            ["lake", "env", "lean", "--root", str(ROOT), str(HERE / "Proof.lean")],
            cwd=LEAN_ROOT,
            env=module_env,
        )
        differential_output = run(
            [
                "lake", "env", "lean", "--root", str(ROOT),
                str(HERE / "Validation.lean"),
            ],
            cwd=LEAN_ROOT,
            env=module_env,
        )

    assert "SingularValueDecompositionTarget : Prop" in statement_output
    assert_axioms(
        obligation_output,
        "Stage1Instances.THM_M_0044.ObligationTree.root_of_real_and_complex",
    )
    assert_axioms(
        proof_output,
        "Stage1Instances.THM_M_0044.Proof.singularValueDecomposition",
    )
    assert "Declarations are sorry-free!" in differential_output
    assert_axioms(
        differential_output,
        "Stage1Instances.THM_M_0044.Validation.differentialSingularValueDecomposition",
    )
    assert "sorryAx" not in obligation_output + proof_output + differential_output

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert any(
        command.get("argv")
        and command["argv"][-1].endswith("check_release.py")
        and command.get("exit_code") == 0
        for command in packet["commands"]
    )
    actual_changed = {
        line[3:]
        for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS S56-M-0044-RELEASE reconciliation")
    print("PASS narrow Lean replay: exact local root and differential root elaborate")
    print("PASS observed axioms: propext, Classical.choice, Quot.sound")
    print("verdict=blocked lifecycle=planned root_vector=H1/M3/R3")
    print("AUDIT-Z=false THEOREM-Z=false theorem_complete=false accepted_receipts=0")
    print("first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE")
    print("first_failed_release_gate=S56-10.6-HERMETIC-COLD-BUILD")


if __name__ == "__main__":
    main()
