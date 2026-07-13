#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-1008-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1008"
ITEM = "S56-M-1008-RELEASE"
THEOREM = "THM-M-1008"
BASE_REVISION = "09a2e94f8f331e8fa7938c55db7dddafb47a6c74"
BASE_TREE = "31b53f41ab005b6c095c80080147c15a11077149"
DENOMINATOR_SHA256 = "d41339ef9ffeddf215d8f5f37732901fbfecdb1b1f662e794344c7a2f4665b3d"
VALIDATION_RECEIPT_SHA256 = "191c27c81c7b51afb0d197ff6d27b806d1aed1be31539d38c3f7fc074a2959a9"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = (
    "PASS THM-M-1008 release reconciliation: validation receipt identity, hashes, and provisional kernel observations agree",
    "FAIL CLOSED dependency: S56-M-1008-VALIDATION is nonrelease worker evidence and is not master accepted",
    "FAIL CLOSED authority: planned lifecycle accepts no vector; weaker recorded H1/M3/R3 controls and the direct proof route is not reconciled with the frozen graph",
    "FAIL CLOSED audit/release: H0, R0, complete trust/provenance, cold offline replay, supply chain, independent verification, and deterministic bundle are absent",
    "verdict=blocked; lifecycle=planned; audit_complete=false; theorem_complete=false; accepted_receipt_ids=[]",
)


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail(f"expected JSON object: {path}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=60, check=False,
    )
    if result.returncode:
        fail(f"git command failed: {args!r}\n{result.stdout}")
    return result.stdout.strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
        fail(f"text hygiene failed: {path}")
    if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
        fail(f"trailing whitespace: {path}")


def main() -> None:
    decision = load(HERE / "release-decision.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    if git("rev-parse", "HEAD") != BASE_REVISION or git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("base revision or tree changed")
    target = next((row for row in targets["targets"] if row["theorem_id"] == THEOREM), None)
    if target is None or target["execution_rank"] != 288:
        fail("target membership or execution rank drifted")
    if target["baseline"] != "L0" or target["rework_required"] is not True:
        fail("uniform target baseline drifted")
    if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
        fail("target authority no longer supports the recorded open state")
    if intake["lifecycle_mode"] != "planned" or intake["theorem_complete"] is not False:
        fail("instance authority no longer supports the recorded open state")
    if intake["root_vector"] != {"human": "H1", "machine": "M3", "readability": "R3"}:
        fail("structured intake vector drifted")

    item = next((row for row in execution["items"] if row["id"] == ITEM), None)
    expected_item = {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 288,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1008-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    if item != expected_item:
        fail("release DAG item drifted")
    dependency_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1008-VALIDATION"
    )
    if dependency_item["state"] != "[_]" or dependency_item["attempts"] != 1:
        fail("validation dependency is not the recorded provisional state")

    if decision["item_id"] != ITEM or decision["theorem_id"] != THEOREM:
        fail("wrong release decision identity")
    if decision["intent"] != "release" or decision["verdict"] != "blocked":
        fail("release intent or blocked verdict drifted")
    if decision["base_revision"] != BASE_REVISION or decision["base_tree"] != BASE_TREE:
        fail("decision base identity drifted")
    if decision["decision_support"] != "provisional_worker_selftest":
        fail("decision support was silently promoted")
    if decision["release_grade"] is not False or decision["release_accepted"] is not False:
        fail("nonrelease decision was silently promoted")
    if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
        fail("blocked worker decision must not advance lifecycle")
    if decision["accepted_receipt_ids"]:
        fail("worker-provisional evidence was represented as accepted")
    terminal = decision["terminal_decisions"]
    if terminal != {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }:
        fail("terminal decision boundary changed")

    dependency = decision["dependency"]
    if dependency["item_id"] != validation["item_id"] or dependency["receipt_id"] != validation["receipt_id"]:
        fail("validation dependency identity mismatch")
    if dependency["receipt_sha256"] != VALIDATION_RECEIPT_SHA256:
        fail("recorded validation receipt digest drifted")
    if sha256(HERE / "validation-receipt.json") != VALIDATION_RECEIPT_SHA256:
        fail("validation receipt content changed")
    if dependency["receipt_support_state"] != validation["support_state"]:
        fail("validation support state mismatch")
    if dependency["master_accepted"] is not False:
        fail("dependency master acceptance was fabricated")
    if dependency["receipt_release_grade"] is not False or validation["release_grade"] is not False:
        fail("validation receipt was silently promoted to release grade")
    if validation["accepted"] is not False or validation["accepted_closed_obligation_ids"]:
        fail("validation worker receipt unexpectedly claims accepted closure")

    result = validation["result"]
    if result["root_kernel_closed_locally"] is not True or result["accepted_root_closed"] is not False:
        fail("local/accepted root closure boundary changed")
    if result["audit_complete"] is not False or result["theorem_complete"] is not False:
        fail("validation terminal boundary changed")
    if result["proof_master_acceptance"] != "fail_closed":
        fail("proof acceptance blocker disappeared")
    if result["hermetic_cold_offline_replay"] != "fail_closed":
        fail("cold hermetic blocker disappeared")
    if result["independent_distinct_runner"] != "fail_closed":
        fail("independent verification blocker disappeared")

    if statement["theorem_complete"] is not False:
        fail("statement artifact claims theorem completion")
    if registry["denominator_sha256"] != DENOMINATOR_SHA256:
        fail("obligation denominator drifted")
    if graphs["registry_denominator_sha256"] != DENOMINATOR_SHA256:
        fail("graph/registry denominator mismatch")
    boundary = graphs["closure_boundary"]
    if boundary["root_closed"] is not False or boundary["theorem_complete"] is not False:
        fail("frozen graph no longer records its pre-proof open boundary")
    if boundary["remaining_root_cut_set"] != ["M1008-T-SELF-INDEPENDENCE"]:
        fail("frozen graph cut set drifted")
    root_node = next(node for node in graphs["nodes"] if node["obligation_id"] == "M1008-ROOT")
    if root_node["machine_debt"] != "M2":
        fail("provisional graph root machine observation drifted")

    expected_vector = ["H1", "M3", "R3"]
    if decision["root_vector"]["recorded_before"] != expected_vector:
        fail("recorded-before vector disagrees with the weaker structured record")
    if decision["root_vector"]["recorded_after"] != expected_vector:
        fail("release silently changed the recorded vector")
    conflict = decision["evidence_reconciliation"]["structured_vector_conflict"]
    if "intake records H1/M3/R3" not in conflict or "graph and validation receipt record H1/M2/R3" not in conflict:
        fail("structured vector conflict is not recorded")
    if decision["first_failed_gate"]["gate_id"] != "S56-10.2-DEPENDENCY-ACCEPTANCE":
        fail("first failed node gate drifted")
    if decision["first_failed_release_gate"]["gate_id"] != "S56-10.6-HERMETIC-COLD-BUILD":
        fail("first failed release gate drifted")

    for name, expected in decision["reconciled_inputs"].items():
        if sha256(HERE / name) != expected:
            fail(f"reconciled input drifted: {name}")
    cut_set = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "master acceptance of S56-M-1008-VALIDATION",
        "structured proof receipt",
        "graph and checked-composition reconciliation",
        "AUDIT-Z",
        "H0 primary-source",
        "R0 node-by-node",
        "transitive declaration/body/import provenance",
        "empty-cache network-denied cold build",
        "supply-chain archive",
        "two signed attestations",
        "minimal release verifier",
        "deterministic content-addressed signed release bundle",
        "THEOREM-Z",
    ):
        if fragment not in cut_set:
            fail(f"release cut set omits {fragment!r}")
    for key in (
        "validation_dependency_acceptance",
        "proof_receipt_and_master_acceptance",
        "authoritative_graph_and_composition_freshness",
        "audit_inventory_reconciliation",
        "human_source_acceptance",
        "readability_acceptance",
        "complete_provenance_foundation_and_tcb_closure",
        "hermetic_release_reproduction",
        "supply_chain_sbom_and_license_archive",
        "independent_release_verification",
        "deterministic_release_bundle",
    ):
        if decision["evidence_reconciliation"][key] != "missing":
            fail(f"release blocker {key!r} was silently cleared")

    expected_packet = {
        "item_id": ITEM,
        "changed_paths": sorted(CHANGED_PATHS),
        "commands": packet["commands"],
        "output_summary": "\n".join(SUMMARY_LINES),
        "base_revision": BASE_REVISION,
        "known_failures": packet["known_failures"],
        "state": "[_]",
    }
    if packet != expected_packet:
        fail("worker self-test packet shape or summary drifted")
    actual_changes = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    if actual_changes != CHANGED_PATHS:
        fail(f"unexpected changed paths: {sorted(actual_changes)}")
    for path in CHANGED_PATHS:
        assert_text_hygiene(ROOT / path)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
