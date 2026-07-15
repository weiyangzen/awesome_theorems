#!/usr/bin/env python3
"""Fail-closed structural checker for the THM-M-0321 release decision."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0321"
ITEM = "S56-M-0321-RELEASE"
THEOREM = "THM-M-0321"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
ROOT_VECTOR = {"H": "H2", "M": "M3", "R": "R4"}
VALIDATION_RECEIPT_SHA256 = "348bcb9f14c844dfa3e19eac28b999d39c459574cb2696f714a9fb76f8bd644f"
EXPRESSION_SHA256 = "7a9628fca04eb72d787efad1f852517f4385377b3ad16f3eba662ccea4bb86a5"
DENOMINATOR_SHA256 = "9963eb2002e7418a51e79b3ed2dd651e2c29a701cdfa1e18f47123041207f9ac"
FLT_REGULAR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
EXPECTED_INPUTS = {
    "README.md": "a539f54a96177a2635d422accf6c98843c2bd3973d8497b8e783f59b241c0eed",
    "instance.json": "ef6a27e14a6b5df2f77b9268876d1d388c9c0cfeb5e9b98df60e050a57b397b8",
    "Statement.lean": "2eed8783dc85ee0ab4f07c68d096c7bab70a3936dfb86d6a30285279b96388dd",
    "ObligationTree.lean": "c3b3e313e7db5dcd3b22d2de153ebed8d50697412540b748c0d67bf6b93f7273",
    "Proof.lean": "e34100a1471ea5e20bb2af9cec123ce21e1fde9a0131baa1381a3a881638b644",
    "Validation.lean": "e032f53e7c677e76558631401c9aba40236cb595ff86438585cf392c7b5aadcb",
    "statement.json": "1c590c636af5d7562083131d5d8b23dceff5902b97da0e79e481eeb14406b2d2",
    "obligation-registry.json": "f40fa32165ad49bfed9a7b2db898a9df01380f59d186bb4659fcf3fcb8eb59b0",
    "typed-graphs.json": "a2b9ff8667a791051ec919f63682666e7e739d3b3d1282132c6f3b07ae037d64",
    "source-statement-crosswalk.md": "89f075ed551e193b99abf015da7fb1e45e1ac27fe4bb89168093fe5fcdb391ca",
    "proof-receipt.json": "a46ecd9989e8c4ce623e2ffc02ec99933f2986f4f7f47791cf7919203e4c778c",
    "proof-blocker.json": "cdbb8fea127c80227dd3715a03a5e9182619c21b867a9649899089b7cca9740c",
    "validation-spec.json": "234fe6b1cd9e7475fc6e6998d285010bbd9cad953335d7d167b4b84a52d6bf6f",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "task-dag.json": "d0e989bd1e86c255aa8f8300d887a4d0f2ebfa76ecdc113b023c1ed6ba078d9f",
}
EXPECTED_AUTHORITY = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "0bb2f433832fe71156aa46c0828102ec3fb61a00dec81fae129c2826a59f63ca",
    "Docs/Stage1_Blueprint_rev-5.6.md": "c09f9f713bdbc820559e41e1e1840423d60cc2af666aeaf5f3c88587de77f161",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
EXPECTED_STDOUT_LINES = (
    "PASS release inputs: current authority and target evidence hashes agree",
    "PASS dependency decision: validation remains provisional and unaccepted",
    "PASS proof boundary: historical exact-root evidence is nonrelease; M0321-T-UPGRADE remains open",
    "PASS artifact boundary: incomplete pinned flt-regular checkout is recorded without mutation",
    "BLOCKED AUDIT-Z: source, graph, readable, evidence, and public reconciliation remain unaccepted",
    "BLOCKED THEOREM-Z: accepted audit, composition, trust, hermetic, independent, and bundle gates fail",
    "verdict=blocked audit_complete=false theorem_complete=false",
)
EXPECTED_STDOUT_SHA256 = "7a6ed9e26c8f27094587a76df788bf8ac7c69b8f64245e7a1450332c82ae972a"
EXPECTED_STDOUT_BYTES = 588
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
KNOWN_FAILURES = [
    "The validation prerequisite is provisional [_], accepted=false, release_grade=false, and not master-accepted.",
    "M0321-T-UPGRADE lacks accepted composition closure because the frozen CompactnessUpgrade interface is false without continuity or closedness.",
    "H0/R0, authoritative graph/public reconciliation, foundation/provenance/TCB/SBOM/license, cold offline replay, independent verifier, protected CI, deterministic bundle, AUDIT-Z, THEOREM-Z, and master acceptance remain open.",
    "The current automation-provided flt-regular artifact has HEAD at refs/heads/.invalid and lacks the manifest-pinned checkout; no fetch or mutation was permitted.",
]

if not __debug__:
    raise RuntimeError("release checking requires Python assertions")


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, item in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str, cwd: Path = ROOT, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=30, check=False,
    )
    if check:
        assert result.returncode == 0, result.stdout
    return result.stdout.strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    decision = load(HERE / "release-decision.json")
    spec = load(HERE / "release-spec.json")
    receipt = load(HERE / "release-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    manifest = load(ROOT / "Formalizations/Lean/lake-manifest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, name
        assert decision["reconciled_inputs"][name] == expected, name
    for relative, expected in EXPECTED_AUTHORITY.items():
        assert sha256(ROOT / relative) == expected, relative
        assert decision["authority_inputs"][relative] == expected, relative

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 687 and target["baseline"] == "L0"
    assert target["rework_required"] is True and target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0321-VALIDATION"
    )
    assert release_item["state"] == "[ ]" and release_item["depends_on"] == [validation_item["id"]]
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    assert instance["lifecycle"] == "planned" and instance["root_vector"] == ROOT_VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert statement["canonical_formal_target"]["expression_sha256"] == EXPRESSION_SHA256
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "closed_obligations": [],
        "root_machine_debt": "M3",
        "remaining_root_cut_set": ["M0321-L-SINGLE", "M0321-L-FIP-COMPACT"],
        "composition_certificates_checked": ["M0321-T-ASSEMBLE"],
        "theorem_complete": False,
    }

    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["accepted"] is False and proof_receipt["proposed_state"] == "[_]"
    assert proof_receipt["result"]["root_closed"] is True
    assert proof_receipt["result"]["theorem_complete"] is False
    assert proof_blocker["remaining_root_cut_set"] == ["M0321-T-UPGRADE"]
    assert proof_blocker["frozen_interface_defect"]["declaration"].endswith("CompactnessUpgrade")
    assert validation["receipt_id"] == decision["dependency"]["receipt_id"]
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is False and validation["release_grade"] is False
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted_receipt_ids"] == []
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["remaining_root_cut_set"] == ["M0321-T-UPGRADE"]

    assert decision["item_id"] == ITEM and decision["verdict"] == "blocked"
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["release_accepted"] is False
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector"]["accepted_before"] == ROOT_VECTOR
    assert decision["root_vector"]["accepted_after"] == ROOT_VECTOR
    assert decision["accepted_receipt_ids"] == decision["accepted_closed_obligation_ids"] == []
    assert decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }
    dependency = decision["dependency"]
    assert dependency["scheduler_projection"] == "[_]"
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["accepted"] is dependency["release_grade"] is dependency["master_accepted"] is False
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_gate"]["node_gate"] == "dependency.S56-M-0321-VALIDATION.master_acceptance"
    assert decision["first_failed_reproduction_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert decision["remaining_root_cut_set"] == ["M0321-T-UPGRADE"]
    assert decision["authoritative_graph_cut_set_before_reconciliation"] == [
        "M0321-L-SINGLE", "M0321-L-FIP-COMPACT"
    ]

    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["observed_axioms"] == ["Classical.choice", "Quot.sound", "propext"]
    assert reconciliation["historical_validation_closure"] == {
        "declarations": 14374,
        "modules": 553,
        "bodyless_nonaxioms": [],
        "unsafe_declarations": [],
    }
    for key in (
        "dependency_master_acceptance", "human_source_acceptance", "readability_acceptance",
        "foundation_and_transitive_tcb_closure", "sbom_license_and_offline_archive",
        "hermetic_empty_cache_reproduction", "independent_signed_verification",
        "independently_implemented_minimal_verifier", "protected_adversarial_ci",
        "deterministic_release_bundle", "master_acceptance",
    ):
        assert reconciliation[key] == "missing", key

    flt = next(row for row in manifest["packages"] if row["name"] == "\u00abflt-regular\u00bb")
    assert flt["rev"] == flt["inputRev"] == FLT_REGULAR_REVISION
    lake = ROOT / "Formalizations/Lean/.lake"
    assert lake.is_symlink()
    flt_root = lake / "packages/flt-regular"
    assert (flt_root / ".git/HEAD").read_text(encoding="utf-8").strip() == "ref: refs/heads/.invalid"
    current = git("rev-parse", "--verify", "HEAD^{commit}", cwd=flt_root, check=False)
    assert "fatal:" in current or current == "", current
    assert reconciliation["current_narrow_lean_replay"] == "blocked_missing_pinned_artifact"

    assert spec["item_id"] == ITEM and spec["network_policy"] == "denied_not_required"
    assert spec["coverage_kind"] == "negative_release_reconciliation_no_closure_credit"
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]
    assert receipt["item_id"] == ITEM and receipt["verdict"] == "blocked"
    assert receipt["decision_sha256"] == sha256(HERE / "release-decision.json")
    assert receipt["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["checker_sha256"] == sha256(HERE / "check_release.py")
    assert receipt["public_projection_sha256"] == sha256(HERE / "release-validation.md")
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["master_accepted"] is receipt["release_grade"] is False
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["remaining_root_cut_set"] == ["M0321-T-UPGRADE"]
    assert receipt["execution"]["checker_stdout_sha256"] == EXPECTED_STDOUT_SHA256
    assert receipt["execution"]["checker_stdout_bytes"] == EXPECTED_STDOUT_BYTES
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == KNOWN_FAILURES
    actual = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual == CHANGED_PATHS, (actual, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    stdout = "\n".join(EXPECTED_STDOUT_LINES) + "\n"
    assert hashlib.sha256(stdout.encode()).hexdigest() == EXPECTED_STDOUT_SHA256
    assert len(stdout.encode()) == EXPECTED_STDOUT_BYTES
    print(stdout, end="")


if __name__ == "__main__":
    main()
