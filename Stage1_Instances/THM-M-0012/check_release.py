#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0012-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0012"


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict), name
    return value


def digest(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


decision = load("release-decision.json")
instance = load("instance.json")
registry = load("obligation-registry.json")
graphs = load("typed-graphs.json")
proof = load("proof-receipt.json")
validation = load("validation-receipt.json")
targets = json.loads(
    (ROOT / "Docs" / "Stage1_Targets_rev-5.6.json").read_text(encoding="utf-8")
)
execution = json.loads(
    (ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json").read_text(
        encoding="utf-8"
    )
)

target = next(row for row in targets["targets"] if row["theorem_id"] == "THM-M-0012")
release_item = next(row for row in execution["items"] if row["id"] == decision["item_id"])
validation_item = next(row for row in execution["items"] if row["id"] == validation["item_id"])

assert target["execution_rank"] == release_item["execution_rank"] == 1062
assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
assert instance["lifecycle"] == "planned" and instance["theorem_complete"] is False
assert instance["accepted_proof_state"] == [] and instance["accepted_receipt_ids"] == []
assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
assert registry["root_obligation_id"] == "M0012-ROOT"
assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]

assert release_item["phase"] == "release" and release_item["state"] == "[ ]"
assert release_item["depends_on"] == [validation_item["id"]]
assert validation_item["state"] == "[_]"
assert release_item["owned_paths"] == ["Stage1_Instances/THM-M-0012"]

assert decision["schema_version"] == "stage1-release-decision/1.0"
assert decision["item_id"] == "S56-M-0012-RELEASE"
assert decision["theorem_id"] == "THM-M-0012" and decision["intent"] == "release"
assert decision["support_state"] == "provisional_worker_selftest"
assert decision["release_grade"] is False
assert decision["verdict"] == "blocked"
assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
assert decision["accepted_receipt_ids"] == []

dependency = decision["dependency"]
assert dependency["item_id"] == validation["item_id"] == "S56-M-0012-VALIDATION"
assert dependency["receipt_id"] == validation["receipt_id"]
assert dependency["receipt_sha256"] == digest("validation-receipt.json")
assert dependency["support_state"] == validation["support_state"]
assert dependency["release_grade"] is validation["release_grade"] is False
assert dependency["master_accepted"] is False and dependency["worker_projection"] == "[_]"

for name, expected in decision["reconciled_inputs"].items():
    assert digest(name) == expected, f"stale reconciled input: {name}"

root = decision["root_vector"]
assert root["accepted_before"] == root["accepted_after"] == ["H1", "M3", "R4"]
assert root["best_provisional_evidence"] == ["H1", "M0-W", "R4"]
terminal = decision["terminal_decisions"]
assert terminal["audit_complete"] is terminal["theorem_complete"] is False
assert terminal["release_accepted"] is False
assert terminal["audit_z"] == terminal["theorem_z"] == "blocked"

assert proof["support_state"] == "provisional_worker_selftest"
assert proof["accepted"] is False and proof["accepted_closed_obligation_ids"] == []
assert proof["result"]["root_kernel_closed"] is True
assert proof["result"]["accepted_root_closed"] is False
assert validation["result"]["provisional_root_kernel_closed"] is True
assert validation["result"]["audit_complete"] is False
assert validation["result"]["theorem_complete"] is False
assert validation["result"]["structured_state_freshness"] == "fail_closed"
assert validation["result"]["hermetic_release_gate"] == "fail_closed"
assert validation["result"]["independent_verification_gate"] == "fail_closed"

closure = graphs["closure_boundary"]
assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
assert closure["accepted_closed_obligations"] == []
assert closure["audit_complete"] is closure["theorem_complete"] is False
assert decision["evidence_reconciliation"]["structured_state_freshness"].startswith(
    "failed:"
)
assert decision["evidence_reconciliation"]["receipt_snapshot_freshness"].startswith(
    "failed:"
)
assert proof["base_revision"] != decision["base_revision"]
assert validation["base_revision"] != decision["base_revision"]

assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
assert decision["first_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
cut = "\n".join(decision["remaining_root_cut_set"])
for fragment in (
    "S56-M-0012-VALIDATION",
    "typed-graph",
    "exact immutable release snapshot",
    "AUDIT-Z",
    "H0 primary-source",
    "R0 node-by-node",
    "transitive declaration",
    "empty-cache network-denied cold build",
    "SBOM and license",
    "two signed attestations",
    "minimal release verifier",
    "mutation, differential, and metamorphic",
    "deterministic content-addressed evidence bundle",
):
    assert fragment in cut, f"release cut set omits {fragment!r}"

for key in (
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
    assert decision["evidence_reconciliation"][key] == "missing", key

replay = subprocess.run(
    ["python3", "-B", str(HERE / "check_validation.py")],
    cwd=ROOT,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    timeout=180,
    check=False,
)
assert replay.returncode == 0, replay.stdout
assert "PASS THM-M-0012 narrow validation" in replay.stdout
assert "blocked: cold hermetic replay" in replay.stdout

selftest_path = ROOT / ".stage1-worker-selftest.json"
if selftest_path.exists():
    selftest = json.loads(selftest_path.read_text(encoding="utf-8"))
    if selftest.get("item_id") == decision["item_id"]:
        assert set(selftest) == {
            "item_id",
            "changed_paths",
            "commands",
            "output_summary",
            "base_revision",
            "known_failures",
            "state",
        }
        assert selftest["state"] == "[_]"
        assert selftest["base_revision"] == decision["base_revision"]
        assert selftest["changed_paths"] == [
            ".stage1-worker-selftest.json",
            "Stage1_Instances/THM-M-0012/check_release.py",
            "Stage1_Instances/THM-M-0012/release-decision.json",
            "Stage1_Instances/THM-M-0012/release.md",
        ]
        assert selftest["known_failures"]
        assert any(
            command.get("argv")
            and command["argv"][-1].endswith("/check_release.py")
            and command.get("exit_code") == 0
            for command in selftest["commands"]
        )

print("PASS S56-M-0012-RELEASE reconciliation")
print("validation replay: exact root provisional; authoritative graph remains open")
print("verdict=blocked lifecycle=planned root_vector=H1/M3/R4")
print("AUDIT-Z=false THEOREM-Z=false theorem_complete=false accepted_receipts=0")
print("first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE")
print("first_failed_release_gate=S56-10.6-HERMETIC-COLD-BUILD")
