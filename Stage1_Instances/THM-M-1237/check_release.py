#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-1237-RELEASE."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1237"
ITEM = "S56-M-1237-RELEASE"
THEOREM = "THM-M-1237"
BASE_REVISION = "2aab68338c370228923a5f7aba2a10b328902eab"
BASE_TREE = "cb6f7e43b6cb5a6b852dea13a3a42cc992176213"


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail(f"expected JSON object: {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
        fail(f"text hygiene failed: {path}")
    if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
        fail(f"trailing whitespace: {path}")


def main() -> None:
    decision = load(HERE / "release-decision.json")
    intake = load(HERE / "intake.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    dag = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
        text=True, stdout=subprocess.PIPE,
    ).stdout.strip()
    tree = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, check=True,
        text=True, stdout=subprocess.PIPE,
    ).stdout.strip()
    if head != BASE_REVISION or tree != BASE_TREE:
        fail("base revision or tree drifted")

    target = next(
        (row for row in targets["targets"] if row["theorem_id"] == THEOREM), None
    )
    if target is None or target["execution_rank"] != 175:
        fail("target membership or execution rank drifted")
    if target["baseline"] != "L0" or target["rework_required"] is not True:
        fail("uniform L0/rework baseline drifted")
    if target["lifecycle_mode"] != "planned" or target["theorem_complete"] is not False:
        fail("manifest authority no longer supports the planned incomplete state")
    if intake["lifecycle_mode"] != "planned" or intake["theorem_complete"] is not False:
        fail("intake authority no longer supports the planned incomplete state")
    if intake["root_vector"] != {"human": "H1", "machine": "M3", "readability": "R3"}:
        fail("intake root vector drifted")

    items = {row["id"]: row for row in dag["items"]}
    dependency_item = items.get("S56-M-1237-VALIDATION")
    release_item = items.get(ITEM)
    if dependency_item is None or dependency_item["state"] != "[_]":
        fail("validation dependency is no longer worker-provisional")
    if release_item is None or release_item["state"] != "[ ]":
        fail("release task authority no longer records the unclaimed state")
    if release_item["depends_on"] != ["S56-M-1237-VALIDATION"]:
        fail("release dependency drifted")
    if release_item["owned_paths"] != [f"Stage1_Instances/{THEOREM}"]:
        fail("release ownership drifted")

    if decision["schema_version"] != "stage1-release-decision/1.0":
        fail("release schema drifted")
    if decision["item_id"] != ITEM or decision["theorem_id"] != THEOREM:
        fail("wrong release item or theorem")
    if decision["intent"] != "release" or decision["verdict"] != "blocked":
        fail("release intent or blocked verdict drifted")
    if decision["base_revision"] != BASE_REVISION or decision["base_tree"] != BASE_TREE:
        fail("decision is not bound to this base snapshot")
    if decision["decision_support"] != "provisional_worker_selftest":
        fail("worker decision support boundary drifted")
    if decision["lifecycle_before"] != "planned" or decision["lifecycle_after"] != "planned":
        fail("blocked worker reconciliation must not advance lifecycle")
    if decision["accepted_receipt_ids"]:
        fail("worker-provisional evidence was represented as accepted")
    terminal = decision["terminal_decisions"]
    if terminal != {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }:
        fail("terminal decisions do not fail closed")
    vector = decision["root_vector"]
    expected_vector = ["H1", "M3", "R3"]
    for key in ("accepted_before", "accepted_after", "best_provisional_evidence"):
        if vector[key] != expected_vector:
            fail(f"root vector drifted at {key}")

    for name, expected in decision["reconciled_inputs"].items():
        if digest(HERE / name) != expected:
            fail(f"reconciled input drifted: {name}")
    if graphs["registry_denominator_sha256"] != registry["denominator_sha256"]:
        fail("typed graph and frozen registry denominator disagree")

    dependency = decision["dependency"]
    if dependency["item_id"] != validation["item_id"]:
        fail("validation dependency item mismatch")
    if dependency["receipt_id"] != validation["receipt_id"]:
        fail("validation dependency receipt mismatch")
    if dependency["receipt_sha256"] != digest(HERE / "validation-receipt.json"):
        fail("validation receipt hash mismatch")
    if dependency["worker_projection"] != "[_]" or dependency["master_accepted"] is not False:
        fail("validation dependency acceptance was overstated")
    if validation["support_state"] != "provisional_worker_selftest":
        fail("validation support state drifted")
    if validation["accepted"] is not False or validation["release_grade"] is not False:
        fail("validation evidence became accepted or release-grade without reconciliation")

    boundary = graphs["closure_boundary"]
    if boundary["closed_obligations"] != []:
        fail("authoritative graph unexpectedly records accepted closed obligations")
    if boundary["root_closed"] is not False or boundary["root_machine_debt"] != "M3":
        fail("authoritative graph no longer records the open M3 root")
    if boundary["audit_complete"] is not False or boundary["theorem_complete"] is not False:
        fail("authoritative graph no longer records false terminal decisions")
    result = validation["result"]
    if result["accepted_root_closed"] is not False or result["accepted_root_machine_debt"] != "M3":
        fail("validation receipt no longer records the open M3 root")
    if result["audit_complete"] is not False or result["theorem_complete"] is not False:
        fail("validation receipt no longer records false terminal decisions")
    if proof["disproved_interface_obligation_ids"] != ["M1237-L-VALUE"]:
        fail("kernel-refuted frozen interface record drifted")
    if proof["result"]["root_closed"] is not False:
        fail("proof receipt silently claims root closure")
    if decision["remaining_root_cut_set"] != [
        "M1237-L-HOLDER", "M1237-L-VALUE architecture repair and exact proof"
    ]:
        fail("mathematical root cut set drifted")
    if decision["authoritative_open_root_cut_set"] != boundary["remaining_root_cut_set"]:
        fail("authoritative graph cut set drifted")
    if decision["provisional_local_proof_cut_set"] != proof["remaining_root_cut_set"]:
        fail("provisional local proof cut set drifted")

    nodes = {row["obligation_id"]: row for row in graphs["nodes"]}
    if nodes["M1237-T"]["machine_debt"] != "M0-L" or nodes["M1237-T"]["evidence_ids"]:
        fail("recorded M1237-T graph inconsistency drifted and must be re-audited")
    proof_edges = graphs["graphs"]["proof"]["edges"]
    c_dependencies = {
        edge["to"] for edge in proof_edges
        if edge["type"] == "proof_requires" and edge["from"] == "M1237-C"
    }
    if c_dependencies != {"M1237-N", "M1237-B"}:
        fail("recorded M1237-C graph prerequisites drifted")
    if proof["closed_obligation_ids"] != ["M1237-C"]:
        fail("provisional local C classification drifted")

    if decision["first_failed_gate"]["gate_id"] != "S56-10.2-DEPENDENCY-ACCEPTANCE":
        fail("first dependency gate drifted")
    if decision["next_failed_theorem_gate"]["gate_id"] != "S56-5.1-EXACT-SOURCE-FIDELITY":
        fail("first intrinsic theorem gate drifted")
    if decision["first_failed_release_gate"] != "S56-10.6-HERMETIC-COLD-BUILD":
        fail("first release-specific gate drifted")
    required_cut_fragments = (
        "master acceptance", "repair of the frozen", "kernel closure",
        "accepted AUDIT-Z", "accepted H0 primary-source", "accepted R0",
        "proof-body provenance", "empty-cache network-denied cold build",
        "SBOM", "two signed attestations", "minimal release verifier",
        "deterministic content-addressed release bundle",
    )
    release_cut = "\n".join(decision["release_gate_cut_set"])
    for fragment in required_cut_fragments:
        if fragment not in release_cut:
            fail(f"release cut set omits {fragment!r}")
    for key in (
        "complete_provenance_foundation_and_tcb", "human_source_acceptance",
        "readability_acceptance", "supply_chain_closure",
        "independent_release_verification", "deterministic_release_bundle",
    ):
        if not decision["evidence_reconciliation"][key].startswith("missing"):
            fail(f"release blocker {key!r} was silently cleared")
    if not decision["evidence_reconciliation"]["exact_source_statement_fidelity"].startswith(
        "failed closed"
    ):
        fail("source-statement fidelity blocker was silently cleared")
    if not decision["evidence_reconciliation"]["typed_graph_reconciliation"].startswith(
        "failed"
    ):
        fail("typed-graph reconciliation blocker was silently cleared")

    replay = subprocess.run(
        ["bash", str(HERE / "check_validation.sh")], cwd=ROOT,
        capture_output=True, text=True, timeout=600, check=False,
    )
    if replay.returncode:
        fail(f"narrow Lean replay failed:\n{replay.stdout}{replay.stderr}")
    replay_bytes = replay.stdout.encode("utf-8")
    expected_hash = validation["result"]["kernel_output_sha256"]
    expected_bytes = validation["result"]["kernel_output_bytes"]
    if hashlib.sha256(replay_bytes).hexdigest() != expected_hash:
        fail("narrow Lean replay output hash drifted")
    if len(replay_bytes) != expected_bytes:
        fail("narrow Lean replay output length drifted")
    if replay.stdout.count("Declarations are sorry-free!") != 5:
        fail("narrow Lean replay did not cover all five audited declarations")
    if "sorryAx" in replay.stdout or "declaration uses 'sorry'" in replay.stdout:
        fail("narrow Lean replay observed a placeholder")

    public = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("release-decision.json", "release-validation.md")
    )
    if "/home/" in public or ".cron/" in public:
        fail("public release artifacts expose a private absolute worker path")
    if '"theorem_complete": true' in public or "theorem_complete=true" in public:
        fail("public release artifacts overstate theorem completion")

    packet = load(ROOT / ".stage1-worker-selftest.json")
    changed_paths = [
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/check_release.py",
        f"Stage1_Instances/{THEOREM}/release-decision.json",
        f"Stage1_Instances/{THEOREM}/release-validation.md",
    ]
    if packet["item_id"] != ITEM or packet["state"] != "[_]":
        fail("worker packet identity or state drifted")
    if packet["base_revision"] != BASE_REVISION:
        fail("worker packet base revision drifted")
    if packet["changed_paths"] != changed_paths:
        fail("worker packet changed-path inventory drifted")
    expected_commands = [
        "python3 Docs/tools/check_stage1_standard.py",
        "python3 scripts/stage1_target.py check",
        "python3 scripts/stage1_target.py show THM-M-1237",
        "python3 Stage1_Instances/THM-M-1237/check_release.py",
        "python3 -m json.tool Stage1_Instances/THM-M-1237/release-decision.json",
        "python3 -m json.tool .stage1-worker-selftest.json",
        "git diff --check -- Stage1_Instances/THM-M-1237 .stage1-worker-selftest.json",
    ]
    if packet["commands"] != expected_commands:
        fail("worker packet command inventory drifted")
    if not packet["known_failures"]:
        fail("worker packet omits known failures")
    for relative in changed_paths:
        assert_text_hygiene(ROOT / relative)

    status = subprocess.run(
        [
            "git", "status", "--porcelain=v1", "-uall", "--",
            f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
            "Formalizations/Lean/.lake",
        ],
        cwd=ROOT, check=True, text=True, stdout=subprocess.PIPE,
    ).stdout.splitlines()
    expected_status = {f"?? {path}" for path in changed_paths}
    expected_status.add("?? Formalizations/Lean/.lake")
    if set(status) != expected_status:
        fail(f"changed-path boundary drifted: {status!r}")

    print("release-decision: ok (blocked; dependency unaccepted; H1/M3/R3 unchanged)")
    print("Lean replay: ok (recorded statement and negative interface evidence only; root open)")
    print("AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]")


if __name__ == "__main__":
    main()
