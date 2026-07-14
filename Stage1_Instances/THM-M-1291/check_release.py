#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1291-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1291"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1291-RELEASE"
THEOREM = "THM-M-1291"
BASE_REVISION = "6cf20c1ab97fcd6970455baa23022062ebc14fe1"
BASE_TREE = "5fa65edc9a9b91b49f7f925ad524ec374328e14c"
EXPRESSION_SHA256 = "d33af3afa4d754bac48547f753d7bda319f46e538766e7c763fa437376599884"
DENOMINATOR_SHA256 = "4331556ba27d32b56189b66a2438dd243ec27af5396f615cc98bb7a763be4748"
VALIDATION_RECEIPT_SHA256 = "65b9bb9a1ecc324d192d1b836c7c4e690aada8e286d23f0df86fffd3631587a5"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M1291-ROOT",
    "M1291-S-STATEMENT",
    "M1291-S-MEASURABILITY",
    "M1291-S-BOUNDARY",
    "M1291-S-FOUNDATION",
    "M1291-B-SUBUNIT",
    "M1291-B-SUPERUNIT",
    "M1291-B-MERGE",
    "M1291-L-POINTWISE",
    "M1291-L-TRUNCATION",
    "M1291-L-TAIL",
    "M1291-T-INTEGRAL",
    "M1291-T-ALGEBRA",
    "M1291-T-ASSEMBLE",
    "M1291-X-SOURCE",
    "M1291-X-PROVENANCE",
    "M1291-X-TRUST",
]
MACHINE_IDS = INVENTORY_IDS[:14]
UPSTREAM_INPUTS = {
    "Statement.lean": "ef19e70e68cd8c9179130141706954825b7de8529ecef6aec1dc6e87c76dd92f",
    "Proof.lean": "a5e3f1e9abd93eb15b124eb7bdd8fd3e860154e7f5bada6326f6d88115ecdbc9",
    "Validation.lean": "8d9a105d0375254dfe0b7e96f0454e7ffa8821b025105bf3498fc2ad26bade98",
    "statement.json": "8d40d41aced47bc55716b67c6bba43a9c2489f887acd00ea3e8e18fa86c031fb",
    "obligation-registry.json": "b432ca10fd9904d2a94fc51391dac293b8cffcd23339a5196d50db7eba4f05a7",
    "typed-graphs.json": "b6f34e8196e95a4c043b5868be326f3cc377c7629adbf9334d71aca1f9a317bc",
    "source-statement-crosswalk.md": "3544bc9220f7855118cd63edeac8ef362af534196ca57d57db0e405e1f89ef53",
    "proof-receipt.json": "e7a32f380d5537bb49cb5a1a58affda62e58c7ecb50b6c82011ead48d32ff014",
    "validation-spec.json": "81dbad7a7c7cccf74d09164b8f68bc365f20dbaf8971235657aff2f04da0f4a7",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.sh": "429a5ff515401f8d02e78b8e8290a492624a8ca1e9e55cb098f622fe91bda0bc",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "e528ae8ca95fdfae8e77543dd98f4d39c189d9dcaa5ad1161f8d0800667c1c79",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3d2f2694c5a382aaf6974369d00c1d39ddeef607c68f0ccebcd812dbd3313476",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1291 current network-isolated trust-zero Lean replay",
    "PASS release inputs, provisional dependency, frozen denominator, and negative authority boundary reconciled",
    "OPEN provisional H2/M3/R4; no accepted transition; AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false",
    "BLOCKED dependency acceptance, node mapping, hermetic release, independent verification, and master acceptance",
)


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


def run(argv: list[str], *, timeout: int = 900) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    assert result.returncode == 0, (
        f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
    )
    return result


def git(*args: str) -> str:
    return run(["git", *args], timeout=60).stdout.rstrip()


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(?P<axioms>.*?)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group("axioms").split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if not __debug__:
        raise RuntimeError("release validation requires Python assertions")

    decision = load(HERE / "release-decision.json")
    spec = load(HERE / "release-spec.json")
    receipt = load(HERE / "release-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in UPSTREAM_INPUTS.items():
        assert sha256(HERE / name) == expected, f"upstream input drifted: {name}"
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 462
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1291.BrezisLiebTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == UPSTREAM_INPUTS["Statement.lean"]
    assert statement["theorem_complete"] is False
    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1291-VALIDATION"
    )
    assert release_item["state"] == "[ ]" and release_item["attempts"] == 0
    assert release_item["depends_on"] == ["S56-M-1291-VALIDATION"]
    assert release_item["owned_paths"] == [f"Stage1_Instances/{THEOREM}"]
    assert validation_item["state"] == "[_]" and validation_item["attempts"] >= 1

    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert registry["status_observed_after_freeze"] == {
        "closed_obligations": [],
        "root_machine_debt": "M3",
    }
    assert all(row["terminal_proof_body_id"] is None for row in registry["obligations"])
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["remaining_root_cut_set"] == ["M1291-T-INTEGRAL"]
    assert closure["composition_certificates"] == []
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    assert proof["accepted"] is False
    assert proof["canonical_target"] == formal["declaration_or_expression"]
    assert proof["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof["provisionally_closed_obligation_ids"] == MACHINE_IDS
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert validation["item_id"] == "S56-M-1291-VALIDATION"
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["accepted_closed_obligation_ids"] == []
    assert validation["canonical_target"] == {
        "declaration": formal["declaration_or_expression"],
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "statement_source_sha256": UPSTREAM_INPUTS["Statement.lean"],
        "registry_denominator_sha256": DENOMINATOR_SHA256,
        "exact_statement_delta": "none",
    }
    assert validation["result"]["accepted_root_vector"] == {
        "H": "H2", "M": "M3", "R": "R4"
    }
    assert validation["result"]["accepted_root_closed"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["execution_rank"] == 462
    assert decision["phase"] == decision["intent"] == "release"
    assert decision["depends_on"] == ["S56-M-1291-VALIDATION"]
    assert decision["canonical_target"] == formal["declaration_or_expression"]
    assert decision["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]"
    assert decision["release_grade"] is False
    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["scheduler_projection"] == validation_item["state"] == "[_]"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["receipt_support_state"] == validation["support_state"]
    assert dependency["receipt_accepted"] is False
    assert dependency["master_accepted"] is False
    assert dependency["receipt_release_grade"] is False
    assert dependency["receipt_release_grade"] == validation["release_grade"]
    assert decision["accepted_receipt_ids"] == []
    reconciled = decision["evidence_reconciliation"]
    assert reconciled["release_gate_evaluation_method"].startswith(
        "Fail closed after the first dependency hard stop"
    )
    assert reconciled["accepted_closed_obligation_ids"] == []
    assert reconciled["authoritative_graph_remaining_root_cut_set"] == [
        "M1291-T-INTEGRAL"
    ]
    for key in (
        "validation_dependency_master_accepted",
        "node_specific_proof_body_and_composition_mapping",
        "human_source_h0_accepted",
        "readability_r0_accepted",
        "accepted_foundation_profile",
        "complete_transitive_tcb_and_provenance",
        "immutable_clean_release_input",
        "cold_empty_cache_build",
        "offline_archive_replay",
        "complete_sbom_and_license_closure",
        "deterministic_release_bundle",
        "content_addressed_release_recipe_and_receipt_ids",
        "distinct_runner_independent_verification",
        "independently_implemented_minimal_verifier",
        "second_signed_attestation",
        "master_acceptance",
    ):
        assert reconciled[key] is False, key
    terminal = decision["decision"]
    assert terminal["verdict"] == "blocked"
    assert terminal["lifecycle_before"] == terminal["lifecycle_after"] == "planned"
    assert terminal["master_accepted_root_vector_before"] is None
    assert terminal["master_accepted_root_vector_after"] is None
    assert terminal["current_provisional_structured_classification_before"] == (
        terminal["current_provisional_structured_classification_after"]
    ) == {
        "H": "H2", "M": "M3", "R": "R4"
    }
    assert terminal["audit_complete"] is terminal["theorem_complete"] is False
    assert terminal["release_accepted"] is False
    assert terminal["audit_z"] is terminal["theorem_z"] is False
    assert terminal["audit_z_status"] == terminal["theorem_z_status"] == "blocked"
    assert terminal["accepted_receipt_ids"] == []
    assert decision["status_boundary"].startswith(
        "Self-tested negative release reconciliation only"
    )
    assert terminal["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert terminal["first_failed_gate_detail"] == (
        "dependency.S56-M-1291-VALIDATION.master_acceptance"
    )
    assert terminal["first_failed_release_protocol_gate"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert terminal["next_failed_release_protocol_gate"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    cut = "\n".join(terminal["remaining_root_cut_set"])
    for fragment in (
        "S56-M-1291-VALIDATION.master_acceptance",
        "node-specific body and composition",
        "accepted H0",
        "R0 readable",
        "foundation profile",
        "empty-cache network-denied cold build",
        "SBOM, license",
        "deterministic content-addressed release bundle",
        "two signed attestations",
        "minimal release verifier",
        "AUDIT-Z, THEOREM-Z",
    ):
        assert fragment in cut, fragment

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 900
    assert spec["expected_exit"] == 0
    assert spec["network_policy"] == "denied"
    assert spec["covered_obligation_ids"] == MACHINE_IDS
    assert spec["negative_status_only_obligation_ids"] == INVENTORY_IDS[14:]
    assert spec["covered_declarations"] == [
        "Stage1Instances.THM_M_1291.BrezisLiebTarget",
        "Stage1Instances.THM_M_1291.rpow_add_le_weighted",
        "Stage1Instances.THM_M_1291.abs_rpow_norm_sub_rpow_norm_sub_le_weighted",
        "Stage1Instances.THM_M_1291.rpow_coeff_tendsto_zero",
        "Stage1Instances.THM_M_1291.truncatedError_nonneg",
        "Stage1Instances.THM_M_1291.truncatedError_le",
        "Stage1Instances.THM_M_1291.integrable_of_ae_tendsto_of_uniform_integral_bound",
        "Stage1Instances.THM_M_1291.abs_rpow_norm_add_sub_rpow_norm_le",
        "Stage1Instances.THM_M_1291.splittingLimit_subunit",
        "Stage1Instances.THM_M_1291.splittingLimit_superunit",
        "Stage1Instances.THM_M_1291.brezisLiebTarget_proof",
    ]
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["master_acceptance"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["owner"] == "THM-M-1291 release lane"
    assert receipt["review_due"].startswith("2026-08-14 or before master acceptance")
    assert receipt["worktree_ref"].startswith("detached HEAD")
    assert receipt["diff_summary"].startswith("Five new release artifacts")
    assert receipt["canonical_target"] == {
        "declaration": formal["declaration_or_expression"],
        "proof_declaration": "Stage1Instances.THM_M_1291.brezisLiebTarget_proof",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "statement_source_sha256": UPSTREAM_INPUTS["Statement.lean"],
        "registry_denominator_sha256": DENOMINATOR_SHA256,
        "exact_statement_delta": "none",
    }
    assert receipt["proof_body_location"]["source"] == (
        f"Stage1_Instances/{THEOREM}/Proof.lean"
    )
    assert receipt["proof_body_location"]["source_sha256"] == UPSTREAM_INPUTS[
        "Proof.lean"
    ]
    assert receipt["dependency"] == dependency
    assert receipt["decision"] == terminal
    assert receipt["release_gate_evaluation_method"].startswith(
        "Fail closed after the first dependency hard stop"
    )
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["status_boundary"] == decision["status_boundary"]
    repository_state = receipt["repository_state"]
    assert repository_state["commit"] == BASE_REVISION
    assert repository_state["tree"] == BASE_TREE
    assert repository_state["preexisting_tracked_target_diff_empty"] is True
    assert repository_state["immutable_clean_release_input"] is False
    assert receipt["repository_state"]["accepted_state_changed"] is False
    assert receipt["freshness"]["revocation_state"] == "unaccepted"
    assert receipt["invalidation_inputs"] == decision["invalidation_inputs"]
    assert receipt["content_addressing_boundary"].startswith(
        "This timestamped provisional node receipt is not"
    )
    assert decision["inputs"] == receipt["inputs"] == UPSTREAM_INPUTS
    assert decision["authority_inputs"] == receipt["authority_inputs"] == AUTHORITY_INPUTS
    assert set(decision["tool_inputs"]) == set(receipt["tool_inputs"]) == {
        "lean-toolchain", "lake-manifest.json", "lean_toolchain", "lean_commit",
        "mathlib_revision",
    }
    assert decision["tool_inputs"] == receipt["tool_inputs"]
    assert decision["tool_inputs"]["lean-toolchain"] == TOOL_INPUTS["lean-toolchain"]
    assert decision["tool_inputs"]["lake-manifest.json"] == TOOL_INPUTS[
        "lake-manifest.json"
    ]
    assert decision["decision"]["retry_condition"]

    lean_replay = run(["bash", str(HERE / "check_validation.sh")])
    output = lean_replay.stdout
    assert output.count("Declarations are sorry-free!") == 10
    assert "declaration uses 'sorry'" not in output
    assert "sorryAx" not in output and "error:" not in output
    root_declaration = "Stage1Instances.THM_M_1291.brezisLiebTarget_proof"
    assert reported_axioms(output, root_declaration) == EXPECTED_AXIOMS
    assert receipt["upstream_replay"]["exit_code"] == 0
    assert receipt["upstream_replay"]["stdout_sha256"] == hashlib.sha256(
        output.encode("utf-8")
    ).hexdigest()
    assert receipt["upstream_replay"]["stdout_bytes"] == len(output.encode("utf-8"))
    assert receipt["upstream_replay"]["observed_root_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["upstream_replay"]["accepted_root_closure"] is False
    assert receipt["upstream_replay"]["sorry_free_declaration_count"] == 10
    assert receipt["upstream_replay"]["root_kernel_replay"] == "provisional_pass"
    assert receipt["upstream_replay"]["lean_trust_level"] == 0
    assert receipt["result"]["exit_code"] == 0
    assert receipt["result"]["release_checker_log"].startswith(
        "stdout is the four exact output_summary lines"
    )
    assert receipt["result"]["output_summary"] == list(SUMMARY_LINES)

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == list(SUMMARY_LINES)
    assert packet["known_failures"] == decision["known_failures"]
    lake_link = LEAN_ROOT / ".lake"
    assert lake_link.is_symlink(), "automation-provided pinned .lake link is absent"
    canonical_lake = lake_link.resolve(strict=True)
    assert canonical_lake.is_dir()
    assert (canonical_lake / "packages" / "mathlib").is_dir()
    base_target_diff = git("diff", "--binary", "HEAD", "--", str(HERE))
    assert base_target_diff == "", "owned target was dirty before release outputs"
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    status = git(
        "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for path in (
        HERE / "release-decision.json",
        HERE / "release-receipt.json",
        HERE / "release-phase.md",
    ):
        public = path.read_text(encoding="utf-8")
        assert "/home/" not in public and ".cron/" not in public
        assert "theorem_complete=true" not in public

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
