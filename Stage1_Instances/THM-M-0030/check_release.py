#!/usr/bin/env python3
"""Fail-closed reconciliation check for S56-M-0030-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0030"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0030-RELEASE"
THEOREM = "THM-M-0030"
BASE_REVISION = "c45f3c7090cb4adf616d45e5414985f956e807b2"
BASE_TREE = "da6f991c07f11e8608ddc090af9356558d64d360"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "737a2cf8a656d39617aecf8aa7d8b2bb3d5739807ea34f6e75dbb833f3c6978e",
    "AnchorAudit.lean": "5fb18fef99524a311526378fc7c12bc29c5c6f2661c0d011d6717e3c4ff5d2cf",
    "ObligationTree.lean": "cd18b0839882f77e63483dda9a593c3aef89920b6c6d6261f4fe5a632752dff0",
    "Proof.lean": "dc915c2fb61a414f485d06322479c4e4706a817aceaf4f68a4fb0097af71f9fd",
    "Validation.lean": "7a6c69dec5d4d4fcbd0670893fc719f5c7ea8d3e31138cedc324069ec2d5caaf",
    "instance.json": "b70e84c41a9a19ae0cf596615c8ab1de9de09b485cb2c42a4740019a617328d0",
    "task-dag.json": "a171a4b37295cafbb56818d2ca32f39d39c78a68b5a3fba60064f70d4c97c5e8",
    "statement.json": "53c3c581691c12e049cf571ec79315bf645c699cee8af5720a10948a844bac37",
    "anchor-audit.json": "d87b987723e114f6792d20b255489bbe4a1840d876b4e50e9eadd260c3bfbc1c",
    "obligation-registry.json": "eb8f21f00749297d3ee2a3d6320fa8e120fdc6bda146de3a2c628c50f453668c",
    "typed-graphs.json": "bf95a4b6b69aa9583c01aa274c86520713406cead2b56debe15c615aa94f8126",
    "validation-specs.json": "d56e7efae6109c831caae11c1e071b009b4e418965df919198fdb834aad307a3",
    "proof-receipt.json": "52138bf5236416854b3550bbdb4263e47e6d34d68c78b7acef253e5a9f2d5310",
    "validation-spec.json": "1b135d7df0506e0f7f8234448ad76f6fe2f017d7459d6d31582b7f44d8495207",
    "validation-receipt.json": "75bb56ab39f8d166508e724e259e56edb1b6807c2de9f214fbd4ac1ca985fa09",
    "check_validation.py": "01b74ca7a63ed5afe523bac84ce9118f17f50a7529cd31b5a2b9456691e3e183",
    "check_proof.sh": "ea6ee5e5d5c4b06c4f7e03599cea61d785952df925d8e5bf89053c106b387472",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
INVENTORY_IDS = [
    "M0030-ROOT", "M0030-S-INTERFACE", "M0030-S-MEMBERSHIP-TRANSPORT",
    "M0030-S-PROPER-BOUNDARY", "M0030-S-FOUNDATION", "M0030-X-MATHLIB-BODY",
    "M0030-N-FINITE-MODULE", "M0030-N-JACOBSON", "M0030-N-LOCAL-CONTAINMENT",
    "M0030-L-PROPER-MAXIMAL", "M0030-L-MAXIMAL-JACOBSON",
    "M0030-L-JACOBSON-UNIT", "M0030-X-JACOBSON-UNIT-SOURCE",
    "M0030-N-FIXEDPOINT-IFF", "M0030-T-FIXEDPOINT-COMPOSE",
    "M0030-C-INFIMUM-SUBMODULE", "M0030-C-STABLE-INTERSECTION",
    "M0030-L-STABILIZATION-INDEX", "M0030-T-STABILITY-EVALUATE",
    "M0030-L-FG-NAKAYAMA", "M0030-B-FIXEDPOINT-FORWARD",
    "M0030-B-FIXEDPOINT-BACKWARD", "M0030-L-POWER-INDUCTION",
    "M0030-X-SOURCE", "M0030-X-PROVENANCE", "M0030-X-TRUST",
    "M0030-X-READABLE", "M0030-X-WORKFLOW",
]
SOURCE_MAPPED_IDS = [
    "M0030-C-INFIMUM-SUBMODULE", "M0030-C-STABLE-INTERSECTION",
    "M0030-L-STABILIZATION-INDEX", "M0030-T-STABILITY-EVALUATE",
    "M0030-L-FG-NAKAYAMA", "M0030-L-POWER-INDUCTION",
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
    assert target["execution_rank"] == 1075
    assert target["lifecycle_mode"] == "planned"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0030-VALIDATION"
    )
    assert release_item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 1075,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-0030-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    assert validation_item["state"] == "[_]"
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-0030-VALIDATION"]

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["execution_rank"] == 1075 and decision["intent"] == "release"
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]"
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0030-VALIDATION"
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
    assert receipt["depends_on"] == ["S56-M-0030-VALIDATION"]
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
        "H1", "M3", "R3"
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
        "H1", "M3", "R3"
    ]
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["accepted_receipt_ids"] == []

    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False
    assert boundary["root_machine_debt"] == "M3"
    assert boundary["accepted_closed_obligations"] == []
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["source_mapped_not_individually_closed_ids"] == SOURCE_MAPPED_IDS
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
        "deep_refinement_node_closure_complete", "audit_z_accepted",
        "pinpoint_h0_review", "independent_r0_review",
        "complete_provenance_foundation_tcb_closure", "immutable_clean_release_input",
        "hermetic_cold_offline_replay", "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier", "protected_ci_and_mutation_gates",
        "deterministic_release_bundle", "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["accepted_closed_obligations"] == []
    assert reconciliation["source_mapped_not_individually_closed_count"] == 6
    cut_set = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "S56-M-0030-VALIDATION", "six deeper", "M0030-X-SOURCE",
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
        "Ideal.iInf_pow_eq_bot_of_isLocalRing",
        "Ideal.iInf_pow_smul_eq_bot_of_isLocalRing",
        "Ideal.iInf_pow_smul_eq_bot_of_le_jacobson",
        "Ideal.mem_iInf_smul_pow_eq_bot_iff",
        "Stage1Instances.THM_M_0030.Proof.exactMathlibAnchor",
        "Stage1Instances.THM_M_0030.Proof.finiteModuleIntersection",
        "Stage1Instances.THM_M_0030.Proof.jacobsonIntersection",
        "Stage1Instances.THM_M_0030.Proof.properToMaximal",
        "Stage1Instances.THM_M_0030.Proof.maximalToJacobson",
        "Stage1Instances.THM_M_0030.Proof.jacobsonUnitSource",
        "Stage1Instances.THM_M_0030.Proof.fixedPointCharacterization",
        "Stage1Instances.THM_M_0030.Proof.fixedPointForward",
        "Stage1Instances.THM_M_0030.Proof.fixedPointBackward",
        "Stage1Instances.THM_M_0030.Proof.localProperIdealJacobson",
        "Stage1Instances.THM_M_0030.Proof.jacobsonUnit",
        "Stage1Instances.THM_M_0030.Proof.fixedPointCharacterization_via_branches",
        "Stage1Instances.THM_M_0030.Proof.jacobsonIntersection_via_frozen_composition",
        "Stage1Instances.THM_M_0030.Proof.finiteModuleIntersection_via_frozen_composition",
        "Stage1Instances.THM_M_0030.Proof.exactMathlibAnchor_via_frozen_composition",
        "Stage1Instances.THM_M_0030.Proof.krullIntersection_direct",
        "Stage1Instances.THM_M_0030.Proof.krullIntersection_via_pinned_anchor",
        "Stage1Instances.THM_M_0030.Proof.krullIntersection_via_frozen_composition",
    )
    for declaration in declarations:
        assert printed_axioms(replay, declaration) == EXPECTED_AXIOMS, declaration
    assert replay.count("Declarations are sorry-free!") == 9
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
        "`blocked`", "`[H1, M3, R3]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "This worker accepts no receipt", "`release_grade=false`",
    ):
        assert fragment in handoff, fragment
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    print("PASS S56-M-0030-RELEASE reconciliation")
    print("verdict=blocked lifecycle=planned accepted_root_vector=H1/M3/R3")
    print("provisional_kernel_root=M0-W audit_complete=false theorem_complete=false")
    print("first_failed_gate=S56-10.2-DEPENDENCY-ACCEPTANCE")
    print("next_failed_release_gate=S56-10.6-HERMETIC-COLD-BUILD")


if __name__ == "__main__":
    main()
