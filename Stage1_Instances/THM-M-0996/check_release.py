#!/usr/bin/env python3
"""Fail-closed self-test for the THM-M-0996 negative release decision."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0996-RELEASE"
THEOREM = "THM-M-0996"
BASE_REVISION = "b62c08f262435e44a30ad3fc88a4712e3954afc7"
BASE_TREE = "f7374dcf5690374a2e9e5d13ac124b34c7ecfab1"
STATEMENT_SHA256 = "cdecb06daf3ca5cbc2b6f8f5def0a82fb3fc712695fdd5c2a047189d683edd14"
DENOMINATOR_SHA256 = "8d3affee638ef1cc6e3fbb2ee9d52fc76212b0a91327f7b42ecba1b4ae8b6e9e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
OPEN_ROOT_CUT = ["M0996-L-HALFSPACE", "M0996-L-GENERAL"]
SUPPORTED_IDS = [
    "M0996-N-PROFILE",
    "M0996-N-COORD",
    "M0996-B-DIM",
    "M0996-C-HALFSPACE",
    "M0996-L-HALFSPACE",
    "M0996-T-ASSEMBLE",
]
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "ae8758d4d0ff157366b0e10c8b3226c3d22cecc07d4f32cd45fa23c6fdd1e270",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "73176f3fe9b58b7387913c0949415c3786a8c30661f46d334ca7e05dd967c070",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_INPUTS = {
    "instance.json": "69f7f955f60c464a198b9c4f80dacd58cb7e294934c90a28da1b056dbc77d48f",
    "Statement.lean": STATEMENT_SHA256,
    "statement.json": "bca25f50f58fa2d386905a6520ed390367dac4a029175d0eb66899b1ffe790f7",
    "anchor-audit.json": "37a8f757f327d13d6be0b260b2c70c53cddf30bca7ffd1e21bbb63cba8d282e5",
    "obligation-registry.json": "756adee275abf1d881e9227a3c2019bf4734f96cdc8e5ab5729896cb9c696711",
    "typed-graphs.json": "582265d4259e4dee4e963a4703f3e130ea43424a9168d46fa9987bc43414b06e",
    "ObligationTree.lean": "017fd72aaf20e6b2e72077f53c2ea4a467f80d2ea7353529327898f3d8649118",
    "Proof.lean": "f700eaa0401497c645131614d333da45b4a95e5ca9f9e5ef9712edef5c918202",
    "proof-receipt.json": "dabbfe02983961d78ed336a9c7655da185871354f79229c1d39229d1f7acbf18",
    "proof-blocker.json": "b214268cbd29cc86aa925c79de4f23427cc574c091cd2939c9b02e478478ddb5",
    "Validation.lean": "79311d28aa5db3305aae2dec9f327f4be988643a964f82d074a5c982de174d53",
    "validation-spec.json": "757f1ed1fed96b0e73d17f51bc2b6ef92a671c944c19fb64817fc8f35c6300cb",
    "validation-receipt.json": "4b2f4bcc209b8acab38cffcfb142ddf65f7303600a2ef7633cf3e039ac95f790",
    "validation-phase.md": "1c0af3828ecb99cf909871ada7b9d39e505aee82a02beaa75b66e718d687cdf6",
    "check_validation.py": "2aa53be6f94dbb055d010e3b8b4c3e93d597a0dab3e192409c2d5d42fac115df",
    "source-statement-crosswalk.md": "7b5f2b9d453b5ebdfec37c9140d32211d810aabc6a9c41b4247fc1b4a0bb0a60",
}
INVENTORY_IDS = [
    "M0996-ROOT",
    "M0996-S-EXACT",
    "M0996-S-BOUNDARY",
    "M0996-S-TRANSPORT",
    "M0996-S-FOUNDATION",
    "M0996-N-PROFILE",
    "M0996-N-COORD",
    "M0996-B-DIM",
    "M0996-C-HALFSPACE",
    "M0996-C-SEMIGROUP",
    "M0996-L-HALFSPACE",
    "M0996-L-GRADIENT",
    "M0996-L-INTERPOLATE",
    "M0996-L-LIMIT",
    "M0996-L-GENERAL",
    "M0996-T-ASSEMBLE",
    "M0996-X-ANCHORS",
    "M0996-X-SOURCE",
    "M0996-X-TCB",
]
COVERED_DECLARATIONS = [
    "Stage1Instances.THM_M_0996.GaussianIsoperimetricTarget",
    "Stage1Instances.THM_M_0996.target_of_profile_bounds",
    "Stage1Instances.THM_M_0996.measurableSet_of_isUnitHalfspace",
    "Stage1Instances.THM_M_0996.coordEquiv",
    "Stage1Instances.THM_M_0996.coordEquiv_map_stdGaussian",
    "Stage1Instances.THM_M_0996.coordEquiv_preimage_stdGaussian",
    "Stage1Instances.THM_M_0996.coordEquiv_image_stdGaussian",
    "Stage1Instances.THM_M_0996.coordEquiv_image_thickening",
    "Stage1Instances.THM_M_0996.coordEquiv_preimage_thickening",
    "Stage1Instances.THM_M_0996.coordEquiv_thickening_measure",
    "Stage1Instances.THM_M_0996.coordEquiv_comp_norm",
    "Stage1Instances.THM_M_0996.coordEquiv_image_isUnitHalfspace",
    "Stage1Instances.THM_M_0996.stdGaussian_unitHalfspace_measure",
    "Stage1Instances.THM_M_0996.norm_sub_apply_le_of_isUnitNormal",
    "Stage1Instances.THM_M_0996.thickening_unitHalfspace_subset",
    "Stage1Instances.THM_M_0996.shifted_unitHalfspace_subset_thickening",
    "Stage1Instances.THM_M_0996.thickening_unitHalfspace_eq",
    "Stage1Instances.THM_M_0996.stdGaussian_unitHalfspace_thickening_measure",
    "Stage1Instances.THM_M_0996.stdGaussianReal_Ioc_pos",
    "Stage1Instances.THM_M_0996.strictMono_stdGaussianReal_Iic",
    "Stage1Instances.THM_M_0996.stdGaussianReal_Iic_pos",
    "Stage1Instances.THM_M_0996.stdGaussianReal_Iic_lt_one",
    "Stage1Instances.THM_M_0996.continuous_stdGaussianReal_cdf",
    "Stage1Instances.THM_M_0996.continuous_stdGaussianReal_Iic",
    "Stage1Instances.THM_M_0996.stdGaussianReal_Iic_surjective_Ioo",
    "Stage1Instances.THM_M_0996.stdGaussianReal_Iic_range",
    "Stage1Instances.THM_M_0996.halfspaceProfile",
    "Stage1Instances.THM_M_0996.halfspaceProfile_stdGaussianReal_Iic",
    "Stage1Instances.THM_M_0996.halfspaceEnlargementFormula",
    "Stage1Instances.THM_M_0996.unitHalfspace_profile_formula",
    "Stage1Instances.THM_M_0996.coordEquiv_unitHalfspace_profile_formula",
    "Stage1Instances.THM_M_0996.no_unitHalfspace_of_finrank_zero",
    "Stage1Instances.THM_M_0996.finrank_pos_of_unitHalfspace",
    "Stage1Instances.THM_M_0996.target_of_finrank_zero",
    "Stage1Instances.THM_M_0996.target_of_generalSetEnlargementBound",
    "Stage1Instances.THM_M_0996.target_of_positive_finrank_branch",
    "Stage1Instances.THM_M_0996.Validation.measurableSet_of_isUnitHalfspace_direct",
    "Stage1Instances.THM_M_0996.Validation.conditionalTargetDirect",
]
RELEASE_OUTPUT_NAMES = (
    "check_release.py",
    "release-decision.json",
    "release-receipt.json",
    "release-spec.json",
    "release-validation.md",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    *(f"Stage1_Instances/{THEOREM}/{name}" for name in RELEASE_OUTPUT_NAMES),
}
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, receipts, registry, graphs, and hashes agree",
    "PASS narrow Lean replay: statement, tree, and 34 partial proof bodies checked at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root: GeneralSetEnlargementBound remains an explicit premise; H2/M4/R4 unchanged",
    "BLOCKED AUDIT-Z and THEOREM-Z: source/readability, trust, hermetic, and independent gates are open",
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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 1200) -> str:
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


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                output.append("\n")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


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
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    run(["git", "merge-base", "--is-ancestor", BASE_REVISION, "HEAD"], timeout=60)
    assert git("rev-parse", f"{BASE_REVISION}^{{tree}}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 276 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 276,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0996-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0996-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert decision["authority_inputs"] == EXPECTED_AUTHORITY_INPUTS

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert statement["declaration"] == "Stage1Instances.THM_M_0996.GaussianIsoperimetricTarget"
    assert statement["statement_sha256"] == STATEMENT_SHA256
    assert statement["formal_status"] == "exact target elaborated; no proof of the target claimed"
    assert statement["theorem_complete"] is False
    assert anchor["exact_root_candidate"] is None
    assert anchor["audit_complete"] is anchor["theorem_complete"] is False
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0996-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == (
        DENOMINATOR_SHA256
    )
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert registry["status_observed_after_freeze"] == {
        "closed_obligations": [],
        "conditionally_checked_compositions": ["M0996-T-ASSEMBLE"],
        "root_machine_debt": "M3",
    }
    assert graphs["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert graphs["theorem_complete"] is False
    assert all(node["evidence_ids"] == [] for node in graphs["nodes"])
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0996-ROOT")
    assert [root["human_debt"], root["machine_debt"], root["readability_debt"]] == [
        "H2", "M3", "R3"
    ]
    by_id = {row["obligation_id"]: row for row in registry["obligations"]}
    assert all(by_id[oid]["statement_fingerprint"].startswith("planned:v1:sha256:")
               for oid in SUPPORTED_IDS)

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["provisionally_closed_obligation_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert proof["authoritative_graph_open_cut_set_unchanged"] == OPEN_ROOT_CUT
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False
    assert proof_blocker["authoritative_graph_open_cut_set_unchanged"] == OPEN_ROOT_CUT
    assert validation["item_id"] == "S56-M-0996-VALIDATION"
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["result"]["root_kernel_closed"] is False
    assert validation["result"]["provisionally_closed_obligation_ids"] == []
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["remaining_root_cut_set"] == OPEN_ROOT_CUT

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False

    result = decision["decision"]
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == "[_]" and decision["release_grade"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == ["H2", "M4", "R4"]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_theorem_gate"]["gate_id"] == "M0996-L-GENERAL.kernel_closure"
    assert result["first_failed_audit_gate"]["gate_id"] == (
        "S56-AUDIT-FROZEN-INVENTORY-SOURCE-BOUNDARY-RECONCILIATION"
    )
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert result["remaining_root_cut_set"] == OPEN_ROOT_CUT
    disagreement = decision["authority_disagreement"]
    assert disagreement["intake_projection"] == ["H2", "M4", "R4"]
    assert disagreement["later_provisional_evidence_projection"] == ["H2", "M3", "R4"]
    assert disagreement["conservative_release_vector"] == ["H2", "M4", "R4"]
    assert disagreement["reconciled"] is False
    reconciliation = decision["evidence_reconciliation"]
    assert reconciliation["validated_partial_progress_toward_obligations"] == SUPPORTED_IDS
    assert reconciliation["accepted_closed_obligations"] == []
    for key in (
        "accepted_exact_root_kernel_closure",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 1200
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_declarations"] == COVERED_DECLARATIONS
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0996-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is receipt["master_accepted"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    receipt_result = receipt["result"]
    assert receipt_result["verdict"] == "blocked"
    assert receipt_result["accepted_closed_obligations"] == []
    assert receipt_result["accepted_root_closed"] is False
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == [
        "H2", "M4", "R4"
    ]
    assert receipt_result["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert receipt_result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt_result["first_failed_theorem_gate"] == "M0996-L-GENERAL.kernel_closure"
    assert receipt_result["first_failed_release_specific_gate"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    expected_bindings = {
        **{
            f"Stage1_Instances/{THEOREM}/{name}": digest
            for name, digest in EXPECTED_INPUTS.items()
        },
        **EXPECTED_AUTHORITY_INPUTS,
    }
    assert receipt["input_bindings"] == expected_bindings
    for relative, expected in expected_bindings.items():
        assert sha256(ROOT / relative) == expected, f"receipt input drifted: {relative}"
    expected_release_bindings = {
        f"Stage1_Instances/{THEOREM}/{name}": sha256(HERE / name)
        for name in RELEASE_OUTPUT_NAMES if name != "release-receipt.json"
    }
    assert receipt["release_output_bindings"] == expected_release_bindings
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        expected_stdout
    ).hexdigest()
    assert receipt["output_evidence"]["expected_line_count"] == len(SUMMARY_LINES)

    mathlib = ROOT / "Formalizations/Lean/.lake/packages/mathlib"
    assert mathlib.is_dir()
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b|\bextern[ \t]+",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        source = source.replace("#print sorries", "")
        assert prohibited.search(source) is None, f"prohibited construct in {name}"
    proof_source = (HERE / "Proof.lean").read_text(encoding="utf-8")
    assert "theorem target_of_generalSetEnlargementBound" in proof_source
    assert "(hGeneral : forall (E : Type u)" in proof_source
    assert "GeneralSetEnlargementBound (E := E) halfspaceProfile" in proof_source
    assert "exact target_of_profile_bounds halfspaceProfile halfspaceEnlargementFormula hGeneral" in (
        proof_source
    )

    with tempfile.TemporaryDirectory(prefix="m0996-release-packet-", dir="/tmp") as name:
        hidden_packet = Path(name) / ".stage1-worker-selftest.json"
        packet_path = ROOT / ".stage1-worker-selftest.json"
        shutil.copy2(packet_path, hidden_packet)
        packet_path.unlink()
        try:
            replay = run([sys.executable, "-I", "-B", str(HERE / "check_validation.py")])
        finally:
            shutil.copy2(hidden_packet, packet_path)
    assert "PASS network-isolated trust-zero fresh replay" in replay
    assert "FAIL CLOSED exact root and authority" in replay
    assert "audit_complete=false; theorem_complete=false" in replay
    assert "no output contains sorryAx" in replay
    assert "declaration uses 'sorry'" not in replay and "error:" not in replay

    packet_path = ROOT / ".stage1-worker-selftest.json"
    if packet_path.exists():
        packet = load(packet_path)
        assert set(packet) == {
            "item_id", "changed_paths", "commands", "output_summary",
            "base_revision", "known_failures", "state",
        }
        assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
        assert packet["state"] == "[_]"
        assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
        assert packet["commands"] == receipt["commands_and_results"]
        assert packet["output_summary"] == receipt["output_summary"] == SUMMARY_LINES
        assert packet["known_failures"] == decision["known_failures"] == receipt["known_failures"]
        status = git("status", "--short", "--untracked-files=all")
        actual_changes = {
            line[3:] for line in status.splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
        for relative in CHANGED_PATHS:
            assert_text_hygiene(ROOT / relative)

    for name in RELEASE_OUTPUT_NAMES[1:]:
        text = (HERE / name).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert '"theorem_complete": true' not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
