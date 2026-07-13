#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0276-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0276"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0276-RELEASE"
THEOREM = "THM-M-0276"
BASE_REVISION = "9f2a15ae074a155a719c4b743df26f1e993312da"
BASE_TREE = "f86e49cf644956699ddb4e82c561101847086c5f"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "ede62e0c7bbf3804f6a81c2f1115643048c69ced4750453af7e8ebd845c6aeea",
    "AnchorAudit.lean": "370b505369246ac2e1ccc5336a3ae0e75cd26d5028ae5e4a536a749f46b38a0b",
    "ObligationTree.lean": "e5757cdf296ba2c12b52658dd7e8231decf8de61a0ff97718139b7a864ab2a76",
    "Proof.lean": "6db08255c52f0314a059858270bdfb9949faec3e56c300affc1032fe7ba8c608",
    "Validation.lean": "14bb1e0cbf014f7fb866ffd698b81526c28f76c30eb775d1f3e47fa536eca8b0",
    "instance.json": "42504860c02a989c5c47b44136152403bb68dfae82453fe036c9143eaad7e7f5",
    "task-dag.json": "a3fac7a02fa77494038120ae265bdd9006af7832e10a9d44dd5cb9657154b958",
    "statement.json": "08de715ccc964a72329e52ebef6cab2a09c1a3341ef32c49945229e1406cdf29",
    "anchor-audit.json": "d84027b9f12d99c5617d719f7ce48bb1b34917a90414f476589e53c17934b906",
    "obligation-registry.json": "0a5df1dbb570e1ec995f609e6e75e6fe0e1e33e306f7f180eeb3a2a139647004",
    "typed-graphs.json": "853fc1e01fe0abc25bc0d8ab82a2b1013562b21a7d277215930fa86359ed4ea3",
    "validation-specs.json": "18d146c8cfa420b914fa2970987bc1fda939f4060af27d57bcc501840f494bd0",
    "proof-receipt.json": "cbd0b7e696e2a9637e1be53d9a0d30f352d1f7c85e645518adc771a53748719b",
    "validation-spec.json": "64ad64351125a17c872caa12bf0d543bb1c830e262b7f63a9cdacf887086d841",
    "validation-receipt.json": "a6b92e26ced08d7e62d7afef7caa68de2b758535112b12050c4f6701e75c9bac",
    "check_validation.py": "50f97c0b8f550978002775042935b38094bc69d79dbed9c9b208379f6c8b7a59",
    "check_proof.sh": "8caf2833196298a36ee5304905e4856913dc8ec25d4e1e5f33246b97c6731831",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
INVENTORY_IDS = [
    "M0276-ROOT", "M0276-S-TARGET", "M0276-S-BOUNDARY",
    "M0276-S-OPEN-EXPANSION", "M0276-S-FOUNDATION", "M0276-N-SAME-FIELD",
    "M0276-T-ASSEMBLE", "M0276-T-ADAPTER", "M0276-T-UPSTREAM",
    "M0276-B-REAL", "M0276-B-COMPLEX", "M0276-T-ISOPENMAP",
    "M0276-L-LOCAL-OPEN-BALL", "M0276-L-EXACT-PREIMAGE",
    "M0276-C-APPROX-SELECTION", "M0276-L-RESIDUAL-GEOMETRIC",
    "M0276-L-SUMMABLE-SERIES", "M0276-L-TELESCOPE", "M0276-L-LIMIT-IMAGE",
    "M0276-L-APPROX-PREIMAGE", "M0276-C-BAIRE-COVER",
    "M0276-L-BAIRE-INTERIOR", "M0276-L-RESCALE-SHELL",
    "M0276-C-CLOSURE-PAIR", "M0276-X-SOURCE", "M0276-X-PROVENANCE",
    "M0276-X-TRUST", "M0276-X-READABLE", "M0276-X-WORKFLOW",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate key {key!r} in {path}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=180, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output, re.DOTALL,
    )
    assert match is not None, (declaration, output)
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


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
    graphs = load(HERE / "typed-graphs.json")
    registry = load(HERE / "obligation-registry.json")
    local_dag = load(HERE / "task-dag.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1282
    assert target["lifecycle_mode"] == "planned"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0276-VALIDATION"
    )
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 1282,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0276-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    assert validation_item["state"] == "[_]"
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-0276-VALIDATION"]

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["execution_rank"] == 1282 and decision["intent"] == "release"
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]"
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0276-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["content_addressed"] is validation["content_addressed"] is False
    assert dependency["master_accepted"] is False
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert decision["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert decision["provisional_receipt_ids_inspected"] == [
        proof["receipt_id"], validation["receipt_id"]
    ]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 180 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["depends_on"] == ["S56-M-0276-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["verdict"] == "blocked"
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["accepted_receipt_ids"] == []
    required_bindings = {
        *(f"Stage1_Instances/{THEOREM}/{name}" for name in EXPECTED_INPUTS),
        f"Stage1_Instances/{THEOREM}/release-spec.json",
        f"Stage1_Instances/{THEOREM}/release-decision.json",
        f"Stage1_Instances/{THEOREM}/release-validation.md",
        f"Stage1_Instances/{THEOREM}/check_release.py",
        *EXPECTED_TOOL_INPUTS,
    }
    assert set(receipt["input_bindings"]) == required_bindings
    for name, expected in receipt["input_bindings"].items():
        path = ROOT / name if name.startswith((".", "Stage1_")) else LEAN_ROOT / name
        assert sha256(path) == expected, f"receipt input drifted: {name}"
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == [
        "H2", "M3", "R4"
    ]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    receipt_result = receipt["result"]
    assert receipt_result["verdict"] == "blocked"
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == [
        "H2", "M3", "R4"
    ]
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["accepted_receipt_ids"] == []

    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False
    assert boundary["accepted_root_machine_debt"] == "M3"
    assert boundary["closed_obligations"] == []
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["root_evidence"]["root_kernel_declaration_closed"] is True
    assert proof["root_evidence"]["accepted_root_closed"] is False
    assert proof["root_evidence"]["unverified_internal_composition_count"] == 14
    assert proof["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    validation_result = validation["result"]
    assert validation_result["exact_root_kernel_closed"] is True
    assert validation_result["accepted_root_machine_debt"] == "M3"
    assert validation_result["accepted_closed_obligations"] == []
    assert validation_result["hermetic_release_gate"] == "fail_closed"
    assert validation_result["independent_distinct_runner_gate"] == "fail_closed"
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False

    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "accepted_exact_root_kernel_closure", "authoritative_graph_reconciled",
        "internal_abstract_child_composition_complete", "audit_z_accepted",
        "pinpoint_h0_review", "independent_r0_review",
        "complete_provenance_foundation_tcb_closure", "immutable_clean_release_input",
        "hermetic_cold_offline_replay", "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier", "protected_ci_and_mutation_gates",
        "deterministic_release_bundle", "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["accepted_closed_obligations"] == []
    assert reconciliation["unverified_internal_composition_count"] == 14
    cut_set = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "S56-M-0276-VALIDATION", "14 currently uncredited", "B(0,1)-versus-B(0,n)",
        "R0 node-anchored", "AUDIT-Z", "empty-cache network-denied cold build",
        "two signed attestations", "minimal release verifier",
        "deterministic content-addressed release bundle",
    ):
        assert fragment in cut_set, fragment

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    replay = run(["bash", str(HERE / "check_proof.sh")])
    declarations = (
        "ContinuousLinearMap.exists_approx_preimage_norm_le",
        "ContinuousLinearMap.exists_preimage_norm_le",
        "ContinuousLinearMap.isOpenMap",
        "Stage1Instances.THM_M_0276.Proof.pinnedApproximatePreimage",
        "Stage1Instances.THM_M_0276.Proof.pinnedExactPreimage",
        "Stage1Instances.THM_M_0276.Proof.pinnedOpenMap",
        "Stage1Instances.THM_M_0276.Proof.pinnedMathlibTerminal",
        "Stage1Instances.THM_M_0276.Proof.realOpenMapping",
        "Stage1Instances.THM_M_0276.Proof.complexOpenMapping",
        "Stage1Instances.THM_M_0276.Proof.banachOpenMapping_direct",
        "Stage1Instances.THM_M_0276.Proof.banachOpenMapping_via_frozen_composition",
        "Stage1Instances.THM_M_0276.Proof.expandedBanachOpenMapping",
    )
    for declaration in declarations:
        assert printed_axioms(replay, declaration) == EXPECTED_AXIOMS, declaration
    assert replay.count("Declarations are sorry-free!") == 12
    assert "sorryAx" not in replay and "declaration uses 'sorry'" not in replay

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    status = git(
        "status", "--short", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H2, M3, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "This worker accepts no receipt", "`release_grade=false`",
    ):
        assert fragment in handoff, fragment
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    print("PASS S56-M-0276-RELEASE reconciliation")
    print("verdict=blocked lifecycle=planned accepted_root_vector=H2/M3/R4")
    print("provisional_kernel_root=M0-W audit_complete=false theorem_complete=false")
    print("first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE")
    print("next_failed_release_gate=S56-10.6-HERMETIC-COLD-BUILD")


if __name__ == "__main__":
    main()
