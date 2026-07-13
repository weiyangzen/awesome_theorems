#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0667-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0667"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
DECISION_BASE = "c45f3c7090cb4adf616d45e5414985f956e807b2"
DECISION_TREE = "da6f991c07f11e8608ddc090af9356558d64d360"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict), name
    return value


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )


def git(*args: str, cwd: Path = ROOT) -> str:
    result = run(["git", *args], cwd=cwd)
    assert result.returncode == 0, result.stdout
    return result.stdout.strip()


def main() -> None:
    decision = load("release-decision.json")
    intake = load("intake.json")
    statement = load("statement.json")
    anchor = load("anchor-audit.json")
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

    target = next(row for row in targets["targets"] if row["theorem_id"] == "THM-M-0667")
    release_item = next(row for row in execution["items"] if row["id"] == decision["item_id"])
    validation_item = next(row for row in execution["items"] if row["id"] == validation["item_id"])
    assert target["execution_rank"] == release_item["execution_rank"] == 711
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    assert release_item["phase"] == "release" and release_item["state"] == "[ ]"
    assert release_item["depends_on"] == [validation_item["id"]]
    assert release_item["owned_paths"] == ["Stage1_Instances/THM-M-0667"]
    assert validation_item["state"] == "[_]"

    assert intake["lifecycle_mode"] == "planned" and intake["theorem_complete"] is False
    assert intake["root_vector"] == {
        "human": "H1",
        "machine": "M3",
        "readability": "R3",
    }
    assert statement["theorem_complete"] is False
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
        "5e34e0af4e8fd26edeebd02c2494f0efa7e14d4b340b23004e479c186815e7ab"
    )

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == "S56-M-0667-RELEASE"
    assert decision["theorem_id"] == "THM-M-0667" and decision["intent"] == "release"
    assert decision["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == []

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == validation_item["id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == digest("validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["worker_projection"] == "[_]" and dependency["master_accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False

    for name, expected in decision["reconciled_inputs"].items():
        assert digest(name) == expected, f"stale reconciled input: {name}"

    root = decision["root_vector"]
    assert root["accepted_before"] == root["accepted_after"] == ["H1", "M3", "R3"]
    assert root["best_provisional_evidence"] == ["H1", "M0-W-candidate", "R3"]
    terminal = decision["terminal_decisions"]
    assert terminal["audit_complete"] is terminal["theorem_complete"] is False
    assert terminal["audit_z"] == terminal["theorem_z"] == "blocked"
    assert terminal["release_accepted"] is False

    assert registry["root_obligation_id"] == "M0667-ROOT"
    assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
    closure = graphs["closure_boundary"]
    assert closure["root_machine_debt"] == "M3" and closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == [
        "M0667-N-DOMINATION",
        "M0667-X-FOUNDATION",
        "M0667-X-SOURCE",
    ]
    root_node = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0667-ROOT")
    assert [root_node[key] for key in ("human_debt", "machine_debt", "readability_debt")] == [
        "H1",
        "M3",
        "R3",
    ]
    assert root_node["evidence_ids"] == []
    provisional_m0p = {
        node["obligation_id"]
        for node in graphs["nodes"]
        if node["machine_debt"] == "M0-P"
    }
    assert provisional_m0p == {
        "M0667-S-NORMALIZATION",
        "M0667-S-ENCODING",
        "M0667-N-DIAGONAL",
        "M0667-T-NAT-BRIDGE",
        "M0667-T-CONTRADICTION",
        "M0667-T-ASSEMBLE",
    }
    assert all(
        node["evidence_ids"] == []
        for node in graphs["nodes"]
        if node["obligation_id"] in provisional_m0p
    )

    assert proof["support_state"] == validation["support_state"] == "provisional_worker_selftest"
    assert proof["result"]["root_closed"] is validation["result"]["root_kernel_closed"] is True
    assert proof["result"]["theorem_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["hermetic_release_gate"] == "fail_closed"
    assert validation["result"]["independent_distinct_runner_gate"] == "fail_closed"

    candidate = next(
        row
        for row in anchor["candidates"]
        if row["candidate_id"] == "M0667-CAND-MATHLIB-NOT-PRIMREC2-ACK"
    )
    assert candidate["revision"] == MATHLIB_REVISION
    mathlib = (LEAN_ROOT / ".lake" / "packages" / "mathlib").resolve()
    assert mathlib.is_dir(), "pinned mathlib artifact missing"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--short", cwd=mathlib) == ""
    assert candidate["tree_hash"] != MATHLIB_TREE
    assert decision["evidence_reconciliation"]["provenance_identity_consistency"].startswith(
        "failed:"
    )

    assert decision["first_failed_gate"]["gate_id"] == (
        "dependency.S56-M-0667-VALIDATION.master_acceptance"
    )
    assert decision["nested_validation_first_failed_gate"]["gate_id"] == validation[
        "first_failed_gate"
    ]
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    assert validation["base_revision"] != DECISION_BASE
    assert decision["evidence_reconciliation"]["receipt_freshness"].startswith(
        "failed:"
    )
    assert validation["environment"]["network"].startswith(
        "not used by the validation commands"
    )
    assert decision["evidence_reconciliation"]["network_isolation"].startswith(
        "missing:"
    )
    assert "H1" in (HERE / "source_statement_crosswalk.md").read_text(encoding="utf-8")
    assert all(node["readability_debt"] == "R3" for node in graphs["nodes"])
    for key in (
        "audit_inventory_reconciliation",
        "complete_provenance_and_trust_closure",
        "hermetic_release_reproduction",
        "supply_chain_closure",
        "independent_release_verification",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] == "missing"

    cut_set = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "master acceptance",
        "graph reconciliation",
        "AUDIT-Z",
        "H0 primary-source",
        "R0 node-by-node",
        "transitive declaration",
        "empty-cache cold build",
        "SBOM and license",
        "two signed attestations",
        "minimal release verifier",
        "deterministic content-addressed evidence bundle",
        "THEOREM-Z",
    ):
        assert fragment in cut_set, f"release cut set omits {fragment!r}"

    replay = run(["python3", "-B", str(HERE / "check_validation.py")])
    assert replay.returncode == 0, replay.stdout
    for marker in (
        "PASS THM-M-0667 narrow kernel replay",
        "STALE structured state: pre-proof graph remains M3",
        "BLOCKED hermetic gate: shared warm .lake",
        "BLOCKED independent gate",
    ):
        assert marker in replay.stdout, replay.stdout

    print("PASS S56-M-0667-RELEASE truthful negative reconciliation")
    print("PASS exact-root validation replay; provisional M0-W candidate only")
    print("BLOCKED dependency.S56-M-0667-VALIDATION.master_acceptance")
    print("BLOCKED stale graph/provenance, AUDIT-Z/H0/R0, hermetic, supply-chain, independent, and bundle gates")
    print("verdict=blocked lifecycle=planned root_vector=H1/M3/R3")
    print("audit_complete=false theorem_complete=false accepted_receipts=0")


if __name__ == "__main__":
    main()
