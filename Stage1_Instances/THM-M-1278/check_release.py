#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1278-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1278"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1278-RELEASE"
THEOREM = "THM-M-1278"
BASE_REVISION = "fcfd52dc69db3bf455310be55903278133a15a10"
BASE_TREE = "3580154b2d6b61f9bfee3079ce78939155de16ca"
EXPRESSION_SHA256 = "a267837ccca68a9ad86620bd4ce7c26c8d56861b57d76d6198ddce94ae671fdb"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
ROOT_CUT = ["M1278-L-SHARP-ONOFRI", "M1278-S-AREA", "M1278-S-FINITE"]
INVENTORY_IDS = [
    "M1278-ROOT",
    "M1278-S-DEFINITIONS",
    "M1278-S-AREA",
    "M1278-S-FINITE",
    "M1278-S-FOUNDATION",
    "M1278-N-SUBTRACT-MEAN",
    "M1278-N-ZERO-MEAN",
    "M1278-N-ENERGY",
    "M1278-N-EXP-SHIFT",
    "M1278-T-SHIFT",
    "M1278-L-SHARP-ONOFRI",
    "M1278-L-SOURCE-ROUTE",
    "M1278-T-COMPOSE",
    "M1278-X-SOURCE",
    "M1278-X-PROVENANCE",
]
PARTIAL_IDS = ["M1278-N-SUBTRACT-MEAN", "M1278-N-ENERGY"]
EXPECTED_INPUTS = {
    "Statement.lean": "efd71349e6a5dd719a804c4d04bd092cd0f400c2130c024775635de7c93fd7f6",
    "ObligationTree.lean": "9bff86d3a95b897a8e4578c833666afca66ea55eb5a8aee6a0251a3a13737b68",
    "Proof.lean": "f9c507e8b8f0cfbea269971dae327379cb06154e40724f5f0e3a19cf83cef7f6",
    "Validation.lean": "fa521ad7b59158633a1418e23156a179e65e30511efc94e32e4b2f9dd2c6f39e",
    "instance.json": "458098afdf633a1319333ea4dbd4fff68f7a2c80f59d93f51ebc04c06a96af8d",
    "task-dag.json": "849efab1bb7c2e306f588b14ff288152e58b7ef6f185b8c70a6327525ed979b2",
    "statement.json": "7357d50f8ebcce95bad23c2196df5f80c636a52641fe1fc8440794db1ce643d7",
    "anchor-audit.json": "208d7a95170a9f939b5f33a9de142875d3b987099af55b89bca06e00575b6801",
    "obligation-registry.json": "11ee1f36ce79a110fdb3772ece76e615b01aebecbf59f11f0806566a4ab74f56",
    "typed-graphs.json": "2eca74f50cf35949b5dcc7d5b34e39bfa75aeb212ae2087c3989dfaf0502efa7",
    "proof-phase.json": "9dd46d2fd9ad69dbd91b3ed48b45883ffd269c5674b5f74d7d531fcaaf96a18e",
    "proof-receipt.json": "5555473c7b928fff52936d6d164eb3f806e844a61512c1d216eb05e8a8865dd1",
    "validation-spec.json": "76a408db587e35be8b5e35368e355558dfdfe0089d6177ee469bdceaf96a597c",
    "validation-receipt.json": "5bc4fadcebb6fd5d5ce26331cbf196ec0063c9e19176d116128d969747115e09",
    "check_validation.py": "4eca0320e4c3c125efc4bf23b6ba03d413f28c5d086570cacaf28f04490f0e5c",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = (
    "PASS release inputs: target, DAG dependency, receipts, graph, and hashes agree",
    "PASS narrow Lean replay: two partial bodies and two probes checked with network denied",
    "BLOCKED dependency and root: validation unaccepted; sharp Onofri, area, and finiteness open",
    "BLOCKED audit/release: H0/R0, clean cold/offline, trust/SBOM, independent verifier, and bundle open",
    "verdict=blocked lifecycle=planned audit_complete=false theorem_complete=false",
)


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=600,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str) -> str:
    return run(["git", *args]).strip()


def without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions (no -O/PYTHONOPTIMIZE)")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    local_dag = load(HERE / "task-dag.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 449
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1278-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 449,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1278-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]"
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-1278-VALIDATION"]

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1278-ROOT"
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False
    assert boundary["root_machine_debt"] == "M3"
    assert boundary["closed_obligations"] == []
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert boundary["remaining_root_cut_set"] == ROOT_CUT

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["closed_obligation_ids"] == PARTIAL_IDS
    assert proof["result"]["root_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["accepted_closed_obligation_ids"] == []
    assert validation["locally_revalidated_provisional_obligation_ids"] == PARTIAL_IDS
    assert validation["result"]["root_closed"] is False
    assert validation["result"]["root_machine_debt"] == "M3"
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["remaining_root_cut_set"] == ROOT_CUT

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["execution_rank"] == 449 and decision["intent"] == "release"
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]"
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    assert decision["accepted_receipt_ids"] == []
    assert decision["provisional_receipt_ids_inspected"] == [
        proof["receipt_id"], validation["receipt_id"]
    ]

    outcome = decision["decision"]
    assert outcome["verdict"] == "blocked"
    assert outcome["lifecycle_before"] == outcome["lifecycle_after"] == "planned"
    expected_vector = {"H": "H2", "M": "M4", "R": "R4"}
    assert outcome["root_vector_before"] == outcome["root_vector_after"] == expected_vector
    assert outcome["audit_complete"] is outcome["theorem_complete"] is False
    assert outcome["audit_z"] == outcome["theorem_z"] == "blocked"
    assert outcome["release_accepted"] is False
    assert outcome["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert outcome["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert outcome["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert outcome["remaining_root_cut_set"] == ROOT_CUT
    release_cut = "\n".join(outcome["remaining_release_cut_set"])
    for fragment in (
        "S56-M-1278-VALIDATION",
        "M1278-L-SHARP-ONOFRI",
        "canonical Statement.OnofriInequality",
        "H0 primary-source",
        "R0 node-anchored",
        "AUDIT-Z",
        "empty-cache network-denied cold build",
        "two signed attestations",
        "minimal release verifier",
        "deterministic content-addressed release bundle",
    ):
        assert fragment in release_cut, fragment

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["depends_on"] == ["S56-M-1278-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["verdict"] == "blocked"
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["kernel_replayed_obligation_ids"] == PARTIAL_IDS
    assert receipt["accepted_receipt_ids"] == []
    result = receipt["result"]
    assert result["verdict"] == "blocked"
    assert result["root_vector_before"] == result["root_vector_after"] == expected_vector
    assert result["best_provisional_root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}
    assert result["observed_axioms"] == EXPECTED_AXIOMS
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["release_accepted"] is False
    assert result["remaining_root_cut_set"] == ROOT_CUT
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["changed_paths"] == decision["changed_paths"]

    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "accepted_exact_root_kernel_closure",
        "canonical_statement_transport",
        "authoritative_graph_reconciled",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_mutation_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["accepted_closed_obligations"] == []

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        assert prohibited.search(without_comments((HERE / name).read_text(encoding="utf-8"))) is None

    validation_env = os.environ.copy()
    validation_env.update(
        LANG="C.UTF-8", LC_ALL="C.UTF-8", TZ="UTC", LEAN_NUM_THREADS="1"
    )
    validation_output = run(
        ["python3", "-B", str(HERE / "check_validation.py")], env=validation_env
    )
    for fragment in (
        "PASS THM-M-1278 narrow validation",
        "root open: sharp Onofri, area/finiteness",
        "blocked: proof master acceptance, cold empty-cache release replay",
    ):
        assert fragment in validation_output, fragment

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H2, M4, R4]`", "`[H2, M3, R4]`", "`AUDIT-Z`",
        "`THEOREM-Z`", "This worker accepts no receipt", "release_grade=false",
    ):
        assert fragment in handoff, fragment
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
