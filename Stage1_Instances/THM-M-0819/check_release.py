#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0819-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0819"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0819-RELEASE"
THEOREM = "THM-M-0819"
BASE_REVISION = "ff3db6d51326417873f49c410421f8f3e13be993"
BASE_TREE = "9160a80a3e3588fd96fcd79323230668cc7d3df1"
VALIDATION_RECEIPT_SHA256 = "6cdd4509ec19a12b65ac2b4b5f5f84fc237c9ec22dc8578dd4ed7528d78e8961"
EXPRESSION_SHA256 = "bdf0aa8f8adac4be9bf2080951be62eac168872b8c589a804ac8587c1878bb19"
DENOMINATOR_SHA256 = "3e19428b16575891198438f798957373f440bf15623c22c44df4c1f69239742c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_ORIGIN = "https://github.com/leanprover-community/mathlib4.git"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
TRUST_DECLARATIONS = (
    "minAntichainPartition_eq_chainHeight",
    "minChainPartition_eq_antichainWidth",
    "Stage1Instances.THM_M_0819_Proof.dilworthPrimary",
)
EXPECTED_INPUTS = {
    "Statement.lean": "c3e600a4a5c2b48686bf244915aea79972e4537a2d89120ad739018716056b52",
    "FiniteDilworth.lean": "825275407850c60f8fe1417a2cee408fb262b60f26eaa9ab30662ea46829e2c1",
    "Proof.lean": "c64e830b6c1a8770319bdaf9549dcd0a8a557da6710272c127560a931da8cd22",
    "Validation.lean": "e997194630e857d27b38730ea5c1164c8a29ea06392234a885b9e8b67f168c39",
    "LICENSE": "c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4",
    "statement.json": "56d8c2af848287eab330da7497ad4fb5039a6305d4584e68415863cc6e0edf7c",
    "instance.json": "5e15e8b602d128fe9e525b36449b8b11de806127a0aff119fbe81b2c0b91f935",
    "task-dag.json": "7fd03c20aa1a8a9e0290047013529431e24aaceb76dfd204ddbe27b0f35007e6",
    "obligation-registry.json": "4ef75dba4309a4c59e46a6394c0eb9345ebfd0e90b483cee8eaeb73760667554",
    "typed-graphs.json": "1397445ffb49c0e099c5bc76c40a2c000edeea6ebfcf9da3191f3e846f5ba2d6",
    "proof-receipt.json": "266eae1986ace9ef8bb38bd8e13e3a929fe774aa660cd06cf167f64132453c56",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-spec.json": "2fa93fe93ae061168e19b07cb056cb65a3174a307f7497706bb22fc2e4ac59d1",
    "check_validation.sh": "58cc39e16c46e290d30dbc9d3babc4cd2cab75be6acb06162a9f6187795394ae",
    "source-statement-crosswalk.md": "906ef72ea36e0474348984a13ebaf8e98ca9c47ee60c52e6f3c2c1c4d5d09777",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "5f212731e50e4a32878d530fb9d453ee0f7f7524ef5f35a0ce44614bdb2de0ae",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "1647d88702a0344efb5051043387a74218cb1edc6279f7b0becbd63a85c6e3b5",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_OUTPUT_HASHES = {
    "release-spec.json": "0b6d3b2894b06cf4fb15f48f337e21c7e5b60e7fe2fa59001889566bab0bd144",
    "release-decision.json": "a8cc27e6fe95c5a29a8f5afde8a8deceab7c2e9bda6a75db473cb51681c94170",
    "release-phase.md": "d14aae7a5f7187ebc00c4095a9411d56187dfff464fe2af6b2a03a6a265fb2d3",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, receipts, authorities, and hashes agree",
    "PASS narrow Lean replay: exact arbitrary-poset root is sorry-free at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED authority and audit: accepted H1/M3/R3 stays open; stale intake remains unreconciled",
    "BLOCKED release assurance: clean cold/offline bundle, TCB/SBOM, and independent verifier are absent",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 900) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).strip()


def reported_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1377 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1377,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0819-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0819-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] >= 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
        assert receipt["inputs"][name] == expected, name
    for relative, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
        assert receipt["inputs"][relative] == expected, relative
    for name, expected in RELEASE_OUTPUT_HASHES.items():
        assert sha256(HERE / name) == expected, f"release output drifted: {name}"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0819.DilworthPrimaryTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M0819-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == (
        DENOMINATOR_SHA256
    )
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["authoritative_root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_release_cut_set"] == [
        "M0819-B-WIDTH-POSITIVE",
        "M0819-X-PRIMARY-SOURCE",
        "M0819-S-FOUNDATION",
        "M0819-X-RADO-PROVENANCE",
        "M0819-X-PROVENANCE",
        "M0819-X-TRUST",
        "M0819-X-READABLE",
        "M0819-X-WORKFLOW",
    ]

    # The intake-era authorities disagree with later frozen evidence and therefore fail closed.
    assert instance["lifecycle"] == "planned" and instance["theorem_complete"] is False
    assert instance["root_vector"] == {"H": "H1", "M": "M5", "R": "R3"}
    assert instance["canonical_formal_target"]["declaration_or_expression"] is None
    assert instance["obligation_registry_hash"] is None
    assert all(row["state"] == "open" for row in task_dag["tasks"])

    assert proof["item_id"] == "S56-M-0819-PROOF" and proof["accepted"] is False
    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert proof["result"]["theorem_complete"] is False

    assert validation["item_id"] == "S56-M-0819-VALIDATION"
    assert validation["receipt_id"] == decision["dependency"]["receipt_id"]
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["first_failed_gate"] == "dependency.S56-M-0819-PROOF.master_acceptance"
    assert validation["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    result = validation["result"]
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_root_closed"] is False
    assert result["accepted_closed_obligations"] == []
    assert result["audit_complete"] is result["theorem_complete"] is False
    dependency = decision["dependency"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["receipt_accepted"] is dependency["receipt_release_grade"] is False
    assert dependency["master_accepted"] is False

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["verdict"] == "blocked" and decision["proposed_state"] == "[_]"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["release_grade"] is False and decision["accepted_receipt_ids"] == []
    vector = {"H": "H1", "M": "M3", "R": "R3"}
    assert decision["root_vector"]["typed_graph_and_validation_before"] == vector
    assert decision["root_vector"]["typed_graph_and_validation_after"] == vector
    assert decision["root_vector"]["stale_intake_projection"] == instance["root_vector"]
    assert decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }
    assert decision["first_failed_gate"]["gate_id"] == (
        "S56-10.2-DEPENDENCY-ACCEPTANCE"
    )
    assert decision["first_failed_gate"]["dependency_gate"] == (
        "dependency.S56-M-0819-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert decision["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    for gate in (
        "authoritative_instance_task_registry_graph_reconciliation",
        "node_specific_proof_body_and_composition_acceptance",
        "accepted_h0_primary_source_review",
        "independently_reviewed_r0_reconstruction",
        "accepted_foundation_and_complete_transitive_tcb",
        "complete_provenance_sbom_and_license_archive",
        "immutable_clean_cold_offline_reproduction",
        "deterministic_content_addressed_release_bundle",
        "distinct_signed_independent_runners",
        "independently_implemented_minimal_verifier",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][gate] == "missing", gate

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    recipe = spec["recipe"]
    assert recipe["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert recipe["network_policy"] == "denied" and recipe["expected_exit"] == 0
    assert "--unshare-net" in recipe["network_enforcement"]
    assert receipt["recipe"]["argv"] == recipe["argv"]

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "release" and receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0819-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == vector
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_dependency_gate"] == (
        "dependency.S56-M-0819-VALIDATION.master_acceptance"
    )
    assert receipt["freshness"]["revocation_state"] == "not_revoked"

    assert MATHLIB.is_dir() and git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_ORIGIN
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    kernel_output = run(["bash", str(HERE / "check_validation.sh")])
    assert kernel_output.count("Declarations are sorry-free!") == len(TRUST_DECLARATIONS)
    assert "declaration uses 'sorry'" not in kernel_output
    assert "sorryAx" not in kernel_output and "error:" not in kernel_output
    assert "Stage1Instances.THM_M_0819_Proof.dilworthPrimary" in kernel_output
    assert "PASS THM-M-0819 network-isolated trust-zero validation replay" in kernel_output
    for declaration in TRUST_DECLARATIONS:
        assert reported_axioms(kernel_output, declaration) == EXPECTED_AXIOMS

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["output_summary"] == receipt["output_summary"] == SUMMARY_LINES
    assert packet["commands"] == receipt["commands"]
    assert packet["known_failures"] == receipt["known_failures"]

    status = git(
        "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for path in (HERE / "release-decision.json", HERE / "release-receipt.json", HERE / "release-phase.md"):
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
