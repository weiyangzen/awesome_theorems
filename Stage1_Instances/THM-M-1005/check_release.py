#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1005-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1005"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1005-RELEASE"
THEOREM = "THM-M-1005"
BASE_REVISION = "e8499ef6898f9562fb480587db7eb9220c04b6fc"
BASE_TREE = "d88a39b243dd6a835f2e7463b9805d1cb175fb80"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "32343e66034f94d4afabc10f4d15cbae77daf650c757023a2142aafba50366e5"
DENOMINATOR_SHA256 = "188df14160a2cf8e92debc91b667ff27e71c15010b7e175b93f58941ca7d1933"
VALIDATION_STDOUT_SHA256 = "54f89b6403cd9da22b20c820785b4de3a30e444405b43a50d89d713ca39b581a"
VALIDATION_RECEIPT_RUNNER_SHA256 = "1750a9d5c733a5d4c20818b3bb8d0c88287c0c566f3bdc1a0b18ddb99f86872b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_DECLARATIONS = [
    "Stage1Instances.THM_M_1005.Statement",
    "Stage1Instances.THM_M_1005.ObligationTree.root_of_strongDoobTerminal",
    "MeasureTheory.maximal_ineq_Lp",
    "Stage1Instances.THM_M_1005.Proof.absSubmartingale",
    "Stage1Instances.THM_M_1005.Proof.measurable_runningAbsMax",
    "Stage1Instances.THM_M_1005.Proof.weakMaximal_abs",
    "Stage1Instances.THM_M_1005.Proof.doobLpMomentEstimate",
    "Stage1Instances.THM_M_1005.Proof.doobLpMomentEstimate_via_frozen_composition",
    "Stage1Instances.THM_M_1005.Validation.independentlyReconstructedDoobLpMomentEstimate",
]
INVENTORY_IDS = [
    "M1005-ROOT",
    "M1005-S-DEFINITIONS",
    "M1005-S-BOUNDARIES",
    "M1005-S-FOUNDATION",
    "M1005-N-ABS-SUBMARTINGALE",
    "M1005-C-MAXIMUM",
    "M1005-L-WEAK-MAXIMAL",
    "M1005-L-LAYER-CAKE",
    "M1005-L-HOLDER",
    "M1005-L-CONSTANT",
    "M1005-T-STRONG-ESTIMATE",
    "M1005-T-ROOT-TRANSPORT",
    "M1005-X-WEAK-PROVENANCE",
    "M1005-X-SOURCE",
]
EXPECTED_INPUTS = {
    "instance.json": "583dbbd6389ae74da78617470b8b7afe33816a5cb44950ed292c4262db9e2f97",
    "task-dag.json": "b5d806bbe418d19f6ea83cbe01494a18e636a5107b32487279e83c610727135d",
    "README.md": "b06b843c6051af01117d8ef440d5d8fa6c8f30d3269f591c8ba1c065c259f208",
    "Statement.lean": "03e36de9b3040e757f9620b3eac5e6f95d003abb5b9b2ffb58416b8f478f38f6",
    "statement.json": "f855d13a849b0dc42fdfe18f4cc68b0208f427a5fe4d88d578e43da8e466f6c3",
    "anchor-audit.json": "71aab3a3368aa8a76d3faa0246eb3990859c25700074e15be2503339ba178b53",
    "obligation-registry.json": "ffa63ad21328ee58f873a49f5603347b9a909430370f71f30172b413da2c7ccf",
    "typed-graphs.json": "44b7b63d17f1c4b306096068a057d85920969fb934e3a0723d3664d8d10dfe45",
    "ObligationTree.lean": "fd19100d3c8b2517f09de1498db1477016f79d2ae5d688315d576d65f437cd5c",
    "DoobLp.lean": "66ad60b7e5ca344df51e5c12007bd7cfe4b7ef5133240f415db5c47b59e8d4ef",
    "Proof.lean": "8d1ae03ba45809ecc2aab3fb904e96e1f91276d002640f75a15c3d5c57c8eb43",
    "proof-receipt.json": "54e2e248d54193cf49ca7a2f18c65a0bd846040035a3c3d463ed8d4752fb7253",
    "proof-validation.md": "3260bb28d6ffcc28fc2939d2e7f8295e1dab1e96990d299d4119ec3eccf8821f",
    "Validation.lean": "e9943c1f34b38594be78efc798d9ba9cb69211b1104ae4fd483354ee6d36928a",
    "check_validation.py": "82c0ee3a487b4a4d6382cf7f866ab2b0d0302093f9f8ff8593649f36ef16c9f6",
    "check_validation.sh": "33846322b26f21742a1788e8adcec5299ab66d03c5f2b143b7f7823196bacea2",
    "validation-spec.json": "7f3290732b49a313b18942484965e83734c71771853584bdf590c2444bc423c8",
    "validation-receipt.json": "491320d7bc99e95212309ee0354e0c80500cff2533f36dc6dde73bac5a158b56",
    "validation-phase.md": "1fe901f091efc14114a103d2d9aad8b94b55b63363bc13c45023e723c473cb03",
    "source-statement-crosswalk.md": "9897486878f9266f65390ba2b6ef58f1a4a77417d71aec9a6e5ca89f6e1e3d81",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "b990243b7d219432eb35a0207492fad90252edc1adc08b0f8744fc5a2383e1e2",
    "Docs/Stage1_Blueprint_rev-5.6.md": "ad8e78fa378d031fe7d694d9652beb89bfbdf8d1151432de40988c24c0a103a0",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/README.md",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = (
    "PASS release inputs: target identity and frozen hashes verified; stale validation receipt detected; DAG snapshots verified",
    "PASS current Lean replay: exact root and same-workspace differential route are sorry-free; observed axioms exactly propext, Classical.choice, Quot.sound",
    "PASS fail-closed reconciliation: conflicting structured states resolve to H2/M4/R4; accepted receipts 0",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted",
    "BLOCKED S56-10.6-HERMETIC-COLD-BUILD and independent release gates",
    "verdict=blocked audit_complete=false theorem_complete=false",
)
RECIPE_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 600
EXPECTED_COMMANDS = [
    {
        "argv": ["python3", "Docs/tools/check_stage1_standard.py"],
        "cwd": ".",
        "exit_code": 0,
        "result": "15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed",
    },
    {
        "argv": ["python3", "scripts/stage1_target.py", "check"],
        "cwd": ".",
        "exit_code": 0,
        "result": "1546 unique targets with ranks 1 through 1546 passed",
    },
    {
        "argv": ["python3", "scripts/stage1_target.py", "show", THEOREM],
        "cwd": ".",
        "exit_code": 0,
        "result": "rank 285 remains planned, L0/rework-required, and theorem-incomplete",
    },
    {
        "argv": ["bash", f"Stage1_Instances/{THEOREM}/check_validation.sh"],
        "cwd": ".",
        "exit_code": 0,
        "result": (
            "network-isolated exact proof/composition and same-workspace differential roots "
            "passed with exactly three observed axioms and transitive sorry exclusion"
        ),
    },
    {
        "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"],
        "cwd": ".",
        "exit_code": 0,
        "result": (
            "release authority, hashes, stale-receipt detection, state conflict, fresh Lean "
            "replay, worker packet, and fail-closed AUDIT-Z/THEOREM-Z decisions passed"
        ),
    },
    {
        "argv": ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"],
        "cwd": ".",
        "env": {"PYTHONOPTIMIZE": "1"},
        "exit_code": 1,
        "result": "expected fail-closed rejection when Python assertions are disabled",
    },
    *[
        {
            "argv": ["python3", "-m", "json.tool", path],
            "cwd": ".",
            "exit_code": 0,
            "result": result,
        }
        for path, result in (
            (f"Stage1_Instances/{THEOREM}/release-spec.json", "release specification parsed as JSON"),
            (f"Stage1_Instances/{THEOREM}/release-decision.json", "release decision parsed as JSON"),
            (f"Stage1_Instances/{THEOREM}/release-receipt.json", "release receipt parsed as JSON"),
            (".stage1-worker-selftest.json", "worker packet parsed as JSON"),
        )
    ],
    {
        "argv": ["python3", "-m", "py_compile", f"Stage1_Instances/{THEOREM}/check_release.py"],
        "cwd": ".",
        "env": {"PYTHONPYCACHEPREFIX": "/tmp/stage1-m1005-release-pycache"},
        "exit_code": 0,
        "result": "release checker syntax compiled outside the repository",
    },
    {
        "argv": [
            "git", "diff", "--check", "--", f"Stage1_Instances/{THEOREM}",
            ".stage1-worker-selftest.json",
        ],
        "cwd": ".",
        "exit_code": 0,
        "result": "no whitespace diagnostics",
    },
]


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - RECIPE_STARTED)
    if remaining <= 0:
        raise RuntimeError("release recipe exceeded its total 600-second timeout")
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    # Supplemental scan only; Lean's transitive assert_no_sorry check is primary evidence.
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    graphs = load(HERE / "typed-graphs.json")
    registry = load(HERE / "obligation-registry.json")
    local_dag = load(HERE / "task-dag.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["intent"] == decision["phase"] == "release"
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["intent"] == receipt["phase"] == "release"
    assert receipt["depends_on"] == ["S56-M-1005-VALIDATION"]
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 285
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1005-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 285,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1005-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in local_dag["tasks"] if row["id"] == "S56-M-1005-VALIDATION"
    )
    assert local_release["state"] == local_validation["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-1005-VALIDATION"]
    assert local_dag["accepted_states"] == []
    assert all(row["state"] == "open" for row in local_dag["tasks"])

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert receipt["authority_inputs"] == EXPECTED_AUTHORITY_INPUTS
    expected_receipt_inputs = {
        **{
            f"Stage1_Instances/{THEOREM}/{name}": expected
            for name, expected in EXPECTED_INPUTS.items()
        },
        **{
            f"Formalizations/Lean/{name}": expected
            for name, expected in EXPECTED_TOOL_INPUTS.items()
        },
    }
    assert receipt["input_bindings"] == expected_receipt_inputs
    for relative, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"

    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["decision_support"] == receipt["support_state"]
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert decision["content_addressed"] is receipt["content_addressed"] is False
    assert receipt["accepted"] is False
    assert receipt["owner"] == "S56-M-1005-RELEASE worker slot5"
    assert receipt["master_acceptance"] == "pending_and_not_claimed"
    assert receipt["decision_id"] == decision["decision_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    checker_sha256 = sha256(Path(__file__))
    assert decision["release_checker_sha256"] == checker_sha256
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    interval = receipt["validation_interval"]
    assert set(interval) == {"started_at", "completed_at", "boundary"}
    started_at = datetime.fromisoformat(interval["started_at"])
    completed_at = datetime.fromisoformat(interval["completed_at"])
    assert started_at.tzinfo is not None and completed_at.tzinfo is not None
    assert started_at <= completed_at
    assert interval["boundary"] == (
        "This interval records one complete successful comprehensive recipe replay used to "
        "assemble this provisional receipt; later checker reruns are verification, not "
        "release-grade attestations."
    )
    handoff = receipt["worker_handoff"]
    assert handoff["exact_statements_added_or_changed"] == []
    assert handoff["typed_graph_changes"] == []
    assert handoff["composition_certificates_changed"] == []
    assert handoff["owned_scope"] == [f"Stage1_Instances/{THEOREM}"]
    assert set(handoff["change_impact_set"]) == {
        ITEM, "S56-M-1005-VALIDATION freshness status",
    }
    assert BASE_REVISION in handoff["worktree_reference"] and "detached HEAD" in handoff["worktree_reference"]
    dirty_evidence = receipt["nonrelease_dirty_input_evidence"]
    tracked_patch = run([
        "git", "diff", "--binary", "--",
        f"Stage1_Instances/{THEOREM}/README.md",
        f"Stage1_Instances/{THEOREM}/check_validation.sh",
    ])
    assert hashlib.sha256(tracked_patch.encode("utf-8")).hexdigest() == dirty_evidence["tracked_patch_sha256"]
    for relative, expected in dirty_evidence["untracked_input_hashes"].items():
        assert sha256(ROOT / relative) == expected
    assert "self-referential hashes" in dirty_evidence["recursive_output_boundary"]
    assert receipt["release_artifact_bindings"] == {
        f"Stage1_Instances/{THEOREM}/check_release.py": checker_sha256,
        f"Stage1_Instances/{THEOREM}/release-spec.json": sha256(HERE / "release-spec.json"),
        f"Stage1_Instances/{THEOREM}/release-decision.json": sha256(HERE / "release-decision.json"),
        f"Stage1_Instances/{THEOREM}/release-validation.md": sha256(HERE / "release-validation.md"),
    }
    assert receipt["binding_cycle_boundary"].startswith(
        "The receipt binds the upstream release specification"
    )

    dependency = decision["dependency"]
    assert dependency == {**receipt["dependency"], "worker_projection": "[_]"}
    assert dependency["item_id"] == validation["item_id"] == "S56-M-1005-VALIDATION"
    assert dependency["target_local_state"] == "open"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["proposed_state"] == validation["proposed_state"] == "[_]"
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["content_addressed_release_evidence"] is False
    assert validation["content_addressed_release_evidence"] is False
    assert dependency["master_accepted"] is False
    validation_freshness = decision["validation_receipt_input_freshness"]
    assert validation_freshness == receipt["validation_receipt_input_freshness"]
    assert validation_freshness == {
        "fresh": False,
        "invalidation_input": "check_validation.sh",
        "receipt_bound_sha256": VALIDATION_RECEIPT_RUNNER_SHA256,
        "current_sha256": EXPECTED_INPUTS["check_validation.sh"],
        "effect": (
            "validation receipt is stale and cannot support dependency acceptance; "
            "the current runner replay is separate provisional nonrelease evidence"
        ),
    }
    assert validation["inputs"]["check_validation.sh"] == VALIDATION_RECEIPT_RUNNER_SHA256
    assert sha256(HERE / "check_validation.sh") == validation_freshness["current_sha256"]
    assert validation_freshness["receipt_bound_sha256"] != validation_freshness["current_sha256"]
    assert "check_validation.sh" in validation["invalidation_inputs"]
    assert decision["provisional_receipt_ids_inspected"] == [
        proof["receipt_id"], validation["receipt_id"]
    ]
    missing_receipts = decision["missing_transitive_phase_receipt_ids"]
    assert missing_receipts == [
        "S56-M-1005-INTAKE",
        "S56-M-1005-STATEMENT",
        "S56-M-1005-ANCHOR_AUDIT",
        "S56-M-1005-OBLIGATION_TREE",
    ]
    for phase in ("intake", "statement", "anchor-audit", "obligation-tree"):
        assert not (HERE / f"{phase}-receipt.json").exists()

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["normative_profile"] == "machine-theorem-assurance/1.0"
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 600 and spec["network_policy"] == "denied"
    assert "unshared network namespace" in spec["network_enforcement"]
    assert "warm and read-only" in spec["network_enforcement"]
    assert spec["expected_exit"] == 0
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact six-line PASS/BLOCKED release status summary",
    }]
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_declarations"] == EXPECTED_DECLARATIONS
    assert "reconciled, not accepted" in spec["scope_boundary"]
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations", "scope_boundary",
    ):
        assert receipt["recipe"][key] == spec[key], key

    result = decision["decision"]
    receipt_result = receipt["result"]
    assert result["verdict"] == receipt_result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    vector = {"H": "H2", "M": "M4", "R": "R4"}
    assert result["root_vector_before"] == result["root_vector_after"] == vector
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == vector
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert receipt_result["exit_code"] == 0
    assert receipt_result["accepted_receipt_ids"] == []
    assert receipt_result["accepted_closed_obligations"] == []
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["audit_z"] == receipt_result["theorem_z"] == "blocked"
    assert receipt_result["release_accepted"] is False
    assert set(receipt_result["observed_axioms"]) == EXPECTED_AXIOMS
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt_result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt_result["first_failed_release_specific_gate"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert receipt_result["next_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["first_failed_gate"] == receipt_result["first_failed_gate"]
    assert receipt["first_failed_release_specific_gate"] == (
        receipt_result["first_failed_release_specific_gate"]
    )
    assert receipt["next_failed_release_gate"] == receipt_result["next_failed_release_gate"]
    semantic_output = "\n".join(SUMMARY_LINES) + "\n"
    semantic_sha256 = hashlib.sha256(semantic_output.encode("utf-8")).hexdigest()
    assert decision["release_output_sha256"] == semantic_sha256
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": semantic_sha256,
        "stdout_bytes": len(semantic_output.encode("utf-8")),
        "expected_line_count": len(SUMMARY_LINES),
        "exit_code": 0,
    }
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["retry_condition"] == decision["retry_condition"]
    assert receipt["changed_paths"] == decision["changed_paths"] == sorted(CHANGED_PATHS)
    expected_worktree = (
        "nonrelease dirty worker checkout containing the eight declared changed paths plus "
        "the pre-existing automation-provided Formalizations/Lean/.lake symlink"
    )
    assert decision["worktree_classification"] == expected_worktree
    assert receipt["environment"]["worktree_classification"] == expected_worktree

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == vector
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert statement["canonical_formal_target"]["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1005.Statement"
    )
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M1005-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert registry["frozen_denominators"]["required_readable"] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    boundary = graphs["closure_boundary"]
    assert boundary == {
        "closed_obligations": ["M1005-S-DEFINITIONS", "M1005-T-ROOT-TRANSPORT"],
        "root_closed": False,
        "theorem_complete": False,
        "remaining_root_cut_set": ["M1005-T-STRONG-ESTIMATE"],
        "root_machine_debt": "M3",
    }
    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert proof["result"]["machine_debt_proposal"].startswith("M0-L")
    assert proof["debt_vector"]["accepted_after_worker_selftest"] == {
        "H": "H2", "M": "M3", "R": "R4",
    }
    validation_result = validation["result"]
    assert validation_result["kernel_replay"] == "provisional_pass"
    assert validation_result["network_isolated_lean_replay"] == "pass"
    assert validation_result["accepted_root_closed"] is False
    assert validation_result["structured_state_reconciliation"] == (
        "fail_closed_instance_M4_vs_graph_and_proof_M3"
    )
    assert validation_result["hermetic_cold_offline_replay"] == "fail_closed"
    assert validation_result["independent_distinct_runner"] == "fail_closed"
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False
    assert anchor["root_machine_classification"] == "M3"
    assert anchor["audit_complete"] is anchor["theorem_complete"] is False

    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "accepted_exact_root_m0_l_e0",
        "authoritative_state_reconciled",
        "validation_receipt_inputs_current",
        "audit_inventory_complete_and_reconciled",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "foundation_policy_accepted",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["accepted_closed_obligations"] == []
    assert set(reconciliation["observed_axioms"]) == EXPECTED_AXIOMS
    cut_set = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "S56-M-1005-VALIDATION",
        "stale validation receipt",
        "H2/M4/R4",
        "M1005-T-STRONG-ESTIMATE",
        "AUDIT-Z",
        "M1005-X-SOURCE",
        "R0 structured reconstruction",
        "M1005-S-FOUNDATION",
        "PR 39349",
        "empty-cache network-denied cold build",
        "SBOM",
        "two signed attestations",
        "minimal release verifier",
        "protected CI",
        "deterministic content-addressed release bundle",
        "THEOREM-Z",
    ):
        assert fragment in cut_set, fragment

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "DoobLp.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    optional_source = MATHLIB / "Mathlib/Probability/Martingale/OptionalStopping.lean"
    optional_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/Probability/Martingale/OptionalStopping.olean"
    assert git("rev-parse", "HEAD:Mathlib/Probability/Martingale/OptionalStopping.lean", cwd=MATHLIB) == (
        "199f7399cc38d5c1c33e4be34c0933f40a216deb"
    )
    assert sha256(optional_source) == "a9bfa392263b80af96da9b547d36f5bef1342bb86054a7a973fb90a6597011c9"
    assert sha256(optional_olean) == "0aa93d0c78aa37415c4e9124faeaa35b4a3ca01ee892cbbb83efd416a8b8a2e3"
    assert sha256(MATHLIB / "LICENSE") == "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
    assert git("hash-object", f"Stage1_Instances/{THEOREM}/DoobLp.lean") == (
        "38bbfc206617c14db63cf9e597613dc3c61e318b"
    )
    proof_body = proof["proof_body"]
    assert proof_body["upstream_pull_request"] == 39349
    assert proof_body["upstream_revision"] == "4b63335c679c15aab74a00d37714d41aa99d701d"
    assert proof_body["upstream_git_blob"] == "c7750503d8ec2a973e6ab0655c1f43f5b122b8c2"
    assert proof_body["upstream_raw_sha256"] == (
        "0a23b4378b723fb19080d259ead92fca5eade70c64a76205581cf83ab88f9706"
    )
    assert proof_body["upstream_status"] == (
        "closed_unmerged_submission_labeled_llm_generated_without_mathlib_acceptance"
    )

    toolchain = (LEAN_ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()
    toolchain_root = Path.home() / ".elan" / "toolchains" / toolchain.replace("/", "--").replace(":", "---")
    lean_path = toolchain_root / "bin" / "lean"
    lake_path = toolchain_root / "bin" / "lake"
    assert lean_path.is_file() and lake_path.is_file()
    python_path = Path(os.path.realpath(sys.executable))
    git_path = Path(shutil.which("git") or "").resolve()
    bwrap_path = Path(shutil.which("bwrap") or "").resolve()
    assert LEAN_COMMIT in run([str(lean_path), "--version"], cwd=LEAN_ROOT)
    environment = receipt["environment"]
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert sha256(lean_path) == environment["lean_executable_sha256"]
    assert sha256(lake_path) == environment["lake_executable_sha256"]
    assert sha256(python_path) == environment["python_executable_sha256"]
    assert sha256(git_path) == environment["git_executable_sha256"]
    assert sha256(bwrap_path) == environment["bubblewrap_executable_sha256"]
    assert environment["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )

    replay = run(["bash", str(HERE / "check_validation.sh")])
    assert hashlib.sha256(replay.encode("utf-8")).hexdigest() == VALIDATION_STDOUT_SHA256
    assert replay.splitlines() == [
        "PASS THM-M-1005 network-isolated narrow kernel replay",
        "PASS exact proof and differential roots: propext, Classical.choice, Quot.sound",
        "PASS transitive sorry check: vendored terminal and differential root are sorry-free",
    ]

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    assert packet["output_summary"] == list(SUMMARY_LINES)
    assert packet["commands"] == EXPECTED_COMMANDS
    status = run(["git", "status", "--porcelain=v1", "--untracked-files=all"])
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "The verdict is `blocked`", "`[H2, M4, R4]`", "`AUDIT-Z`",
        "`THEOREM-Z`", "This worker accepts no receipt", "`release_grade=false`",
        "stale",
    ):
        assert fragment in handoff, fragment
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
