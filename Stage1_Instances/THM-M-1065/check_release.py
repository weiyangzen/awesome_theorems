#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1065-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1065"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
TOOLCHAIN_BIN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin"

ITEM = "S56-M-1065-RELEASE"
THEOREM = "THM-M-1065"
BASE_REVISION = "21798c9c8a9ed9ea40e8df489d9c661b59026564"
BASE_TREE = "9150bea4c07c5bc89526ce2540709f0e9e8fda24"
EXPRESSION_SHA256 = "b257ceb188a0b84aab11fd389b5df322129c283dbc38f5c226900a4fec5cebd0"
DENOMINATOR_SHA256 = "d5e21a3abc7d96576d5aeba4b8377a8ef8d92136b5ed448f9f28723f00d91ac2"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
OPEN_ROOT_CUT = [
    "M1065-C-SPACE",
    "M1065-L-BLOCK-COUPLING",
    "M1065-L-MAXIMAL-TAIL",
]
INVENTORY_IDS = [
    "M1065-ROOT",
    "M1065-S-LAW",
    "M1065-S-EVENT",
    "M1065-S-BOUNDARY",
    "M1065-S-FOUNDATION",
    "M1065-C-SPACE",
    "M1065-L-X-LAWS",
    "M1065-L-X-INDEP",
    "M1065-L-Y-LAWS",
    "M1065-L-Y-INDEP",
    "M1065-L-EVENT-MEAS",
    "M1065-C-CONSTANTS",
    "M1065-L-BLOCK-COUPLING",
    "M1065-L-MAXIMAL-TAIL",
    "M1065-T-WITNESS",
    "M1065-T-COMPOSE",
    "M1065-X-SOURCE",
    "M1065-X-PROVENANCE",
]
EXPECTED_INPUTS = {
    "README.md": "ad139da90f361e21bbbb4554a5ab0852ca525fefa78bc4827e9a297656d9f7e2",
    "instance.json": "85818edf62136acee862596b776b9f09e75f39ee8113e10ffff76de7f3146af1",
    "task-dag.json": "7e35f3ac1f43d0d85b65129924390270dc1efba4c8a5bb7e329b657d4f240f77",
    "Statement.lean": "7f3b249e058dcdc4410c966622b1d707daff6cd486a0666bf3c0c8cf1e2edaf1",
    "statement.json": "940f961fc3d0970df44a354edccea84ecfcaf76fec6321348387792fda748995",
    "source-statement-crosswalk.md": "4feb419258a94b5a7d784314707a2c9ce89b2b2c7e1545da7cd3eb2c1aacac93",
    "AnchorAudit.lean": "64d04f6cdbf62fc7aea44798f914010dc12d66abbfd5c9ea1a7e8445135930c9",
    "anchor-audit.json": "ecb5d943f920d43832fe007283321c777a72a96fb8d9f81f6e8dbe3134973d27",
    "ObligationTree.lean": "9aa9a38f406f2d8f38deaeb919d41af053547b4e8322d6ec99b3496e03ab5873",
    "obligation-registry.json": "79eb5a4cc430f81c41baf2b70160f82037a600b795cf1d7dd4c23bdee27a7b44",
    "typed-graphs.json": "dcb4876d08a30eb8dc5bf604e18ac7e83c0fa864c04ef808bf720ceeb41c325c",
    "Proof.lean": "e445a607d6291e1a8991551c4cc6d3140146df2213637d468a9753b586fae5fb",
    "proof-receipt-2026-07-15-head-72a35d5f-slot53.json": (
        "b7b86cdf1f471181478650e294524ca7aeeee844da575a8ef84a455388803e47"
    ),
    "proof-blocker-2026-07-15-head-72a35d5f-slot53.json": (
        "bdd292d4c86e54538d290788fa00b5c9b51b15e3cd8c5410cd593ef7e48fdd3d"
    ),
    "Validation.lean": "edb1c9a3b2d54adeb5b2d27e3aa457409b12d4727f29c960265a111fb8d8775e",
    "validation-spec.json": "2b11c9fa03483f4207a50b992edc1e796947d8a9a65aaabad0cdcd012aa592ce",
    "validation-receipt.json": "0aeed8ccbe42357e6de85e95a7ac0eaabd158d030e0fadbffc162a661492dbc7",
    "validation-blocker.json": "9c23446b22b63b77854ba84a1a2f2c8a730fd3eff384b5d3771f89c1a50dcaf5",
    "validation-phase.md": "bcd67abc4f9db20729ae470a0eac0f80c778367d3c4b65c4e81110f0796a9a47",
    "check_validation.py": "fd4cf2d39e334dacec82343adf768784ff8340a3ad91b11bc8b23ef0d592edf4",
    "check_validation.sh": "a912f589d69ef3b7a889a95b8f7de2deeeaad441d090f49c94e43bf4f0bf7be1",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "0c3b72642383ff79ab7164b112ccba44271f7f63cd93d02743718442b4ff377f",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "c7a28e4144c2260845177b08a3e0a70629ac15d3a374cea3241245e661b618de",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_OUTPUTS = (
    "release-spec.json",
    "release-decision.json",
    "release-receipt.json",
    "release-validation.md",
)
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    *(f"Stage1_Instances/{THEOREM}/{name}" for name in RELEASE_OUTPUTS),
}
SUMMARY_LINES = (
    "PASS release reconciliation: target, DAG, receipts, registry, graphs, and hashes agree",
    "PASS narrow Lean replay: exact statement, conditional composition, two partial bodies, two negative anchor decisions, and two differential probes checked at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED exact root: H2/M4/R4 unchanged; zero frozen obligations closed",
    "BLOCKED AUDIT-Z and THEOREM-Z: source/readability, trust, hermetic, and independent gates are open",
    "verdict=blocked lifecycle=planned audit_complete=false theorem_complete=false accepted_receipts=0",
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL THM-M-1065 release: {message}")


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate JSON key {key!r} in {path.relative_to(ROOT)}")
            result[key] = value
        return result

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
        )
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {path.relative_to(ROOT)}: {error}")
    if not isinstance(value, dict):
        fail(f"expected JSON object in {path.relative_to(ROOT)}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 900,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update({
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    })
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if check and result.returncode:
        fail(f"command exited {result.returncode}: {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).stdout.rstrip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def reported_axioms(output: str, declaration: str) -> set[str]:
    no_axioms = f"'{declaration}' does not depend on any axioms"
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert output.count(no_axioms) + (match is not None) == 1, declaration
    if match is None:
        return set()
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def main() -> None:
    if sys.flags.optimize:
        fail("Python assertions must be enabled")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt-2026-07-15-head-72a35d5f-slot53.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 507,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM,
        "name": "Koml\u00f3s-Major-Tusn\u00e1dy\u903c\u8fd1",
        "category": "\u6982\u7387\u8bba\u4e0e\u968f\u673a\u8fc7\u7a0b / \u968f\u673a\u8fc7\u7a0b",
        "source_status_untrusted": "\u5df2\u9a8c\u8bc1",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_mathlib_anchor_and_wrapper",
        "intake_score": 138,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    items = {row["id"]: row for row in execution["items"]}
    assert items[ITEM] == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 507,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1065-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert items["S56-M-1065-VALIDATION"]["state"] == "[_]"
    assert items["S56-M-1065-VALIDATION"]["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for relative, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    assert decision["authority_inputs"] == EXPECTED_AUTHORITY_INPUTS

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert task_dag["lifecycle"] == "planned" and task_dag["accepted_states"] == []
    assert all(row["state"] == "open" for row in task_dag["tasks"])
    local_release = next(row for row in task_dag["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in task_dag["tasks"] if row["id"] == "S56-M-1065-VALIDATION"
    )
    assert local_release["depends_on"] == ["S56-M-1065-VALIDATION"]
    assert local_release["state"] == local_validation["state"] == "open"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1065.KMTStrongApproximationTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1065-ROOT"
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert all(row["terminal_proof_body_id"] is None for row in registry["obligations"])
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert [row["obligation_id"] for row in graphs["nodes"]] == INVENTORY_IDS
    assert all(row["evidence_ids"] == [] for row in graphs["nodes"])
    assert all(row["validation_spec_id"].endswith("-PENDING") for row in graphs["nodes"])
    assert graphs["closure_boundary"] == {
        "closed_obligations": [],
        "root_closed": False,
        "root_machine_debt": "M4",
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": OPEN_ROOT_CUT,
    }

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["supported_obligation_ids"] == []
    assert proof["provisionally_closed_obligation_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert proof["remaining_root_cut_set"] == OPEN_ROOT_CUT

    assert validation["item_id"] == "S56-M-1065-VALIDATION"
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["accepted_receipt_ids"] == []
    validation_result = validation["result"]
    assert validation_result["accepted_closed_obligation_ids"] == []
    assert validation_result["root_kernel_closed"] is False
    assert validation_result["root_machine_debt"] == "M4"
    assert validation_result["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False
    assert validation_result["hermetic_cold_offline_replay"] == "fail_closed"
    assert validation_result["independent_distinct_runner"] == "fail_closed"
    assert sha256(HERE / "validation-receipt.json") == decision["dependency"]["receipt_sha256"]
    assert decision["dependency"]["receipt_id"] == validation["receipt_id"]

    assert decision["item_id"] == receipt["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["accepted"] is receipt["accepted"] is False
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    terminal = decision["terminal_decisions"]
    assert terminal["verdict"] == "blocked"
    assert terminal["lifecycle_before"] == terminal["lifecycle_after"] == "planned"
    assert terminal["audit_complete"] is terminal["theorem_complete"] is False
    assert terminal["audit_z"] == terminal["theorem_z"] == "blocked"
    assert terminal["release_accepted"] is terminal["master_acceptance"] is False
    assert decision["root_vector"]["authoritative_before"] == instance["root_vector"]
    assert decision["root_vector"]["authoritative_after"] == instance["root_vector"]
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_theorem_gate"]["gate_id"] == (
        "S56-THEOREM-EXACT-ROOT-KERNEL-CLOSURE"
    )
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert decision["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert decision["remaining_root_cut_set"] == OPEN_ROOT_CUT
    assert decision["evidence_reconciliation"]["accepted_closed_obligation_ids"] == []
    for key in (
        "validation_dependency_master_accepted",
        "exact_root_kernel_closed",
        "audit_z_accepted",
        "pinpoint_h0_and_independent_source_review",
        "independent_r0_review",
        "accepted_foundation_profile",
        "complete_transitive_provenance_and_tcb",
        "immutable_clean_release_input",
        "hermetic_empty_cache_cold_offline_replay",
        "complete_sbom_license_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key

    recipe = spec["recipe"]
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert recipe["cwd"] == "."
    assert recipe["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert recipe["network_policy"] == "denied"
    assert recipe["covered_obligation_ids"] == INVENTORY_IDS
    assert receipt["recipe"] == recipe
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["canonical_statement"] == decision["canonical_target"]

    assert (LEAN_ROOT / ".lake").is_symlink()
    assert MATHLIB.is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=no", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    assert sha256(TOOLCHAIN_BIN / "lean") == receipt["environment"]["lean_executable_sha256"]

    replay = run(["bash", str(HERE / "check_validation.sh")], timeout=650).stdout
    assert replay.count("Declarations are sorry-free!") == 9
    assert "sorryAx" not in replay and "declaration uses 'sorry'" not in replay
    declarations = {
        "Stage1Instances.THM_M_1065.target_iff_expandedSourceShape",
        "Stage1Instances.THM_M_1065.discrepancyEvent_one",
        "Stage1Instances.THM_M_1065.ObligationTree.kmtTarget_iff_couplingData",
        "Stage1Instances.THM_M_1065.exists_commonIIDSequences",
        "Stage1Instances.THM_M_1065.measurableSet_discrepancyEvent",
        "Stage1Instances.THM_M_1065.AnchorAudit.noRetainedCandidateClaimsTerminalProof",
        "Stage1Instances.THM_M_1065.AnchorAudit.anchorAuditPermitsTheoremCompletion_eq_false",
        "Stage1Instances.THM_M_1065.Validation.independentlyReconstructedTargetExpansion",
        "Stage1Instances.THM_M_1065.Validation.independentlyReconstructedDiscrepancyEventOne",
    }
    for declaration in declarations:
        assert reported_axioms(replay, declaration) <= EXPECTED_AXIOMS

    output_hash = hashlib.sha256(replay.encode()).hexdigest()
    assert receipt["result"]["lean_replay_stdout_sha256"] == output_hash
    assert receipt["result"]["lean_replay_stdout_bytes"] == len(replay.encode())
    assert receipt["input_bindings"] == {
        f"Stage1_Instances/{THEOREM}/{name}": expected
        for name, expected in EXPECTED_INPUTS.items()
    } | EXPECTED_AUTHORITY_INPUTS
    assert receipt["release_output_bindings"] == {
        f"Stage1_Instances/{THEOREM}/{name}": sha256(HERE / name)
        for name in ("release-spec.json", "release-decision.json", "release-validation.md")
    } | {f"Stage1_Instances/{THEOREM}/check_release.py": sha256(HERE / "check_release.py")}

    for path in (
        HERE / "check_release.py",
        *(HERE / name for name in RELEASE_OUTPUTS),
    ):
        assert_text_hygiene(path)

    packet_path = ROOT / ".stage1-worker-selftest.json"
    if packet_path.exists():
        packet = load(packet_path)
        assert packet["item_id"] == ITEM
        assert packet["state"] == "[_]"
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
