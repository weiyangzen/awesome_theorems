#!/usr/bin/env python3
"""Fail-closed reconciliation for S56-M-1518-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1518"
ITEM = "S56-M-1518-RELEASE"
THEOREM = "THM-M-1518"
BASE_REVISION = "3551812aeaf826b94804e464b34511a7bbc7f6ff"
BASE_TREE = "6ed6612d0a642e6879579700427c67045c1a34d7"
EXPRESSION_SHA256 = "4cc15786f13f4e4ad7594012ab3e96613f5bffbf572523e8282b41139fe6979f"
DENOMINATOR_SHA256 = "dc5ea1db035dfa578766c6af2fac7c562127454ec7c9a7f7f073766e095002b1"
VALIDATION_RECEIPT_ID = "S56-M-1518-VALIDATION-local-20260714T025954+0800"
PROOF_RECEIPT_ID = "S56-M-1518-PROOF-local-20260714T015427+0800"
AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
CANONICAL_IDS = [
    "M1518-ROOT",
    "M1518-S-DEFINITIONS",
    "M1518-S-BOUNDARY",
    "M1518-S-FOUNDATION",
    "M1518-N-DIFFERENTIATE",
    "M1518-N-WEAK",
    "M1518-L-IBP",
    "M1518-L-FUNDAMENTAL",
    "M1518-L-WEAK-POINTWISE",
    "M1518-T-ASSEMBLE",
    "M1518-X-SOURCE",
    "M1518-X-PROVENANCE",
]
MACHINE_IDS = CANONICAL_IDS[:10]
RECONCILED_INPUTS = {
    "Statement.lean": "c5f7022ac18e06a2dd9e5ee8d35590e15ee46777468c2c197884535230c1c167",
    "ObligationTree.lean": "026f35442b9a3580db9dd8aed098d273c95c9d559f86b8cdba1331703999fdc6",
    "Proof.lean": "1b93c59d624e8989ac79910253c071b044588b8daae22dae39ebb5e68c5ab8f4",
    "WeakToPointwise.lean": "db0514399f5f07c7f49537dcfc26c9a2616cd24160a76689ca0efcd1edf2648d",
    "ExactProof.lean": "e234f8dfa16e2f6867895ae393c4dd9d023a177fe61adcce7c4893ee65269d46",
    "Validation.lean": "69f0692771817a14ba2b231fbd75a1606596e25fb352b9ce56f6802785f407d2",
    "statement.json": "ce936dd890c8d808fae5a2869f0831fc7b8854a343ce90ed78d1647e48a6ef9f",
    "anchor-audit.json": "b7f872bd76e8157715ecddfa61cfe8e9ce8b7fa18c6e0cdd7bb394836c5d264e",
    "obligation-registry.json": "32502789f8cd24c0c816e58a36f505d7fb71dfbb65904cb13292e38b5ab0f35c",
    "typed-graphs.json": "5e98dbe3ee8bd5c884f4a1785472a092823cec2026e17c69370d38f64e8761cb",
    "proof-receipt.json": "d03954c0f4db858feb332df30e847b6717f03e60089d9b59cb2fc6f39d376d31",
    "validation-spec.json": "0649ddc0ca76193f876277d35b729b548055098561d0acf4c308b79ee687c233",
    "validation-receipt.json": "9c7ea559144c8617969a4d5ef55052a15503912e751e66887e4d92314e39301b",
    "check_validation.py": "336ef72f4a6b6329ea1e7d168e6f675aa739cf226e32e06421237ad9e375df0b",
    "check_validation.sh": "d343758eac9110a85fda26aab202a96f0841004521fa671ba3f081eb1989cfcb",
    "validation-phase.md": "6f0586fc09d364ad1a5607656de0ba28d046cbd10a9b1ecb8c371e609a53cd61",
}
SUMMARY_LINES = (
    "PASS THM-M-1518 negative release reconciliation",
    "PASS fresh narrow Lean replay: exact and differential roots are sorry-free with axioms propext, Classical.choice, Quot.sound",
    "BLOCKED dependency: S56-M-1518-VALIDATION is provisional, unaccepted, and nonrelease",
    "BLOCKED authority: accepted root remains H2/M4/R3 with graph reconciliation and foundation/provenance open",
    "BLOCKED audit: pinpoint H0, independent R0, structured reconciliation, and deterministic bundle are absent; AUDIT-Z=false",
    "BLOCKED theorem: clean cold/offline, independent verifier, release bundle, and master gates are open; THEOREM-Z=false",
)


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    assert result.returncode == 0, f"command failed: {argv!r}\n{result.stdout}"
    return result.stdout


def git(*args: str) -> str:
    return run(["git", *args], timeout=30).strip()


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, declaration
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def main() -> None:
    if sys.flags.optimize:
        raise SystemExit("release check failed: Python optimization disables assertions")

    decision = load(HERE / "release-decision.json")
    spec = load(HERE / "release-spec.json")
    receipt = load(HERE / "release-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 187,
        "legacy_priority_slot": "S1-M-187",
        "theorem_id": THEOREM,
        "name": "最小作用量原理",
        "category": "其他重要领域 / 数学物理",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_mathlib_anchor_and_wrapper",
        "intake_score": 136,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 187,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1518-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1518-VALIDATION"
    )
    assert validation_item["state"] == "[_]"

    for name, expected in RECONCILED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
        assert decision["reconciled_inputs"][name] == expected, name

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1518.StationaryActionEulerLagrangeTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M1518-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert [row["obligation_id"] for row in registry["obligations"]] == CANONICAL_IDS
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == [
        "M1518-N-DIFFERENTIATE", "M1518-L-IBP", "M1518-L-FUNDAMENTAL"
    ]
    root_node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1518-ROOT")
    assert [root_node[key] for key in ("human_debt", "machine_debt", "readability_debt")] == [
        "H2", "M4", "R3"
    ]

    assert proof["receipt_id"] == PROOF_RECEIPT_ID
    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert proof["result"]["axioms"] == AXIOM_LIST
    assert validation["receipt_id"] == VALIDATION_RECEIPT_ID
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is False
    assert validation["release_grade"] is False
    assert validation["content_addressed_release_evidence"] is False
    assert validation["first_failed_gate"] == (
        "dependency.S56-M-1518-PROOF.master_acceptance"
    )
    assert validation["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert validation["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert validation["result"]["accepted_root_machine_debt"] == "M4"
    assert validation["result"]["accepted_root_closed"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["execution_rank"] == 187 and decision["intent"] == "release"
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]"
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["worker_projection"] == "[_]"
    assert dependency["receipt_support_state"] == validation["support_state"]
    assert dependency["master_accepted"] is False
    assert dependency["receipt_accepted"] is validation["accepted"] is False
    assert dependency["receipt_release_grade"] is validation["release_grade"] is False
    assert dependency["receipt_content_addressed_release_evidence"] is False
    assert decision["canonical_obligation_ids"] == CANONICAL_IDS
    assert decision["accepted_receipt_ids"] == []
    assert decision["provisional_receipt_ids_inspected"] == [
        PROOF_RECEIPT_ID, VALIDATION_RECEIPT_ID
    ]
    vector = decision["root_vector"]
    assert vector["accepted_before"] == vector["accepted_after"] == {
        "H": "H2", "M": "M4", "R": "R3"
    }
    assert vector["best_provisional_kernel_evidence"] == {
        "H": "H2", "M": "M0-L", "R": "R3",
        "support_state": "candidate_pending_acceptance",
    }
    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_gate"]["dependency_gate"] == (
        "dependency.S56-M-1518-VALIDATION.master_acceptance"
    )
    assert result["nested_predecessor_failure"]["gate_id"] == (
        "dependency.S56-M-1518-PROOF.master_acceptance"
    )
    assert result["next_failed_node_gate"]["gate_id"] == (
        "S56-10.5-VALIDATION-RECIPE-FRESHNESS"
    )
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    cut = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "S56-M-1518-VALIDATION",
        "M1518-N-DIFFERENTIATE",
        "M1518-S-FOUNDATION",
        "M1518-X-SOURCE",
        "R0 reconstruction",
        "empty-cache network-denied cold build",
        "complete SBOM",
        "two signed attestations",
        "minimal release verifier",
        "deterministic content-addressed release bundle",
    ):
        assert fragment in cut, fragment
    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "accepted_validation_dependency",
        "accepted_exact_root_kernel_closure",
        "authoritative_graph_reconciled",
        "foundation_and_complete_trust_closure",
        "pinpoint_h0_review",
        "independent_r0_review",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_mutation_gates",
        "deterministic_release_bundle",
        "audit_z_accepted",
        "theorem_z_accepted",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["recorded_validation_recipe_freshness"].startswith(
        "fail closed:"
    )
    assert decision["known_failures"]
    assert decision["typed_graph_delta"].startswith("none;")

    assert spec["schema_version"] == "stage1-release-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "--unshare-net" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == CANONICAL_IDS
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact six-line PASS/BLOCKED status summary",
    }]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-1518-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["canonical_obligation_ids"] == CANONICAL_IDS
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["recipe"] == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids", "covered_declarations",
        )
    }
    receipt_result = receipt["result"]
    assert receipt_result["verdict"] == "blocked"
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["accepted_receipt_ids"] == []
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == {
        "H": "H2", "M": "M4", "R": "R3"
    }
    assert receipt["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["first_failed_dependency_gate"] == (
        "dependency.S56-M-1518-VALIDATION.master_acceptance"
    )
    assert receipt["first_failed_release_specific_gate"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["remaining_root_cut_set"] == result["remaining_root_cut_set"]
    assert receipt["known_failures"] == decision["known_failures"]
    for name, expected in RECONCILED_INPUTS.items():
        assert receipt["input_bindings"][f"Stage1_Instances/{THEOREM}/{name}"] == expected
    for name in ("release-decision.json", "release-phase.md", "release-spec.json"):
        assert receipt["input_bindings"][f"Stage1_Instances/{THEOREM}/{name}"] == sha256(HERE / name)
    assert receipt["input_bindings"][f"Stage1_Instances/{THEOREM}/check_release.py"] == (
        sha256(HERE / "check_release.py")
    )
    assert receipt["input_bindings"]["Formalizations/Lean/lean-toolchain"] == (
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    )
    assert receipt["input_bindings"]["Formalizations/Lean/lake-manifest.json"] == (
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
    )

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "ObligationTree.lean", "Proof.lean",
        "WeakToPointwise.lean", "ExactProof.lean", "Validation.lean",
    ):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    replay = run(["bash", str(HERE / "check_validation.sh")], timeout=540)
    declarations = (
        "Stage1Instances.THM_M_1518.ObligationTree.exactTarget_of_packages",
        "Stage1Instances.THM_M_1518.firstVariationFormula",
        "Stage1Instances.THM_M_1518.ObligationTree.weakToPointwise",
        "Stage1Instances.THM_M_1518.stationaryActionEulerLagrange",
        "Stage1Instances.THM_M_1518.Validation."
        "independentlyRecomposedStationaryActionEulerLagrange",
    )
    for declaration in declarations:
        assert observed_axioms(replay, declaration) == AXIOMS, declaration
    assert replay.count("Declarations are sorry-free!") == 3
    assert "sorryAx" not in replay and "declaration uses 'sorry'" not in replay

    expected_changed = {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/check_release.py",
        f"Stage1_Instances/{THEOREM}/release-decision.json",
        f"Stage1_Instances/{THEOREM}/release-phase.md",
        f"Stage1_Instances/{THEOREM}/release-receipt.json",
        f"Stage1_Instances/{THEOREM}/release-spec.json",
    }
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == expected_changed
    assert packet["known_failures"] == decision["known_failures"]
    for command in packet["commands"]:
        if command.get("expected_failure") is True:
            assert command["exit_code"] == 1
        else:
            assert command["exit_code"] == 0
    assert "theorem_complete=false" in packet["output_summary"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == expected_changed, (actual_changed, expected_changed)

    handoff = (HERE / "release-phase.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H2, M4, R3]`", "This worker accepts no receipt",
        "`AUDIT-Z`", "`THEOREM-Z`", "`release_grade=false`",
    ):
        assert fragment in handoff, fragment
    for path in [HERE / name for name in (
        "check_release.py", "release-decision.json", "release-phase.md",
        "release-receipt.json", "release-spec.json",
    )] + [ROOT / ".stage1-worker-selftest.json"]:
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
