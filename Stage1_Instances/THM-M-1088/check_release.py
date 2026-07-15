#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1088-RELEASE."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1088"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1088-RELEASE"
THEOREM = "THM-M-1088"
BASE_REVISION = "a9274bb02f984e5c74d2c97339044c6db8eb14f9"
BASE_TREE = "c72a5af07dd4ab3f7088c516c74235e794a6de09"
VALIDATION_BASE_REVISION = "9584b263a758e0dbab59344389554570dcf2e535"
VALIDATION_BASE_TREE = "d4ea7039d087ff41783f81c4f1b35c2817dd6a1b"
VALIDATION_RECEIPT_SHA256 = (
    "bb92724d5b00991734ae809e4fab23a3e4ce96361835f698567347ba4516185d"
)
DENOMINATOR_SHA256 = "56fb1860d804859c9580000d4f003ce8ad997dea3f9e40aca50d5b1efe921f3d"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
ALL_OBLIGATIONS = [
    "M1088-ROOT",
    "M1088-S-CONTEXT",
    "M1088-S-SUPREMUM",
    "M1088-S-BOUNDARY",
    "M1088-S-FOUNDATION",
    "M1088-N-ENUMERATION",
    "M1088-C-FINITE-MAX",
    "M1088-L-FINITE-CONCENTRATION",
    "M1088-L-COVARIANCE",
    "M1088-B-POSITIVE-TAIL",
    "M1088-B-ZERO-TAIL",
    "M1088-B-MERGE",
    "M1088-L-MEAN-LIMIT",
    "M1088-L-PROBABILITY-LIMIT",
    "M1088-T-ENGINE",
    "M1088-T-ASSEMBLE",
    "M1088-X-SOURCE",
    "M1088-X-PROVENANCE",
    "M1088-X-TRUST",
]
PROOF_CUT = [
    "M1088-L-FINITE-CONCENTRATION",
    "M1088-L-COVARIANCE",
    "M1088-L-MEAN-LIMIT",
    "M1088-L-PROBABILITY-LIMIT",
    "M1088-T-ENGINE",
]
PROOF_DECLARATIONS = {
    "Stage1Instances.THM_M_1088.Proof.coordinate_hasSubgaussianMGF",
    "Stage1Instances.THM_M_1088.Proof.zeroTailBound_of_isGaussianProcess",
    "Stage1Instances.THM_M_1088.Proof.upperTailBound_of_hasSubgaussianMGF",
    "Stage1Instances.THM_M_1088.Proof.upperTailBound_of_process_hasSubgaussianMGF",
}
SUMMARY_LINES = [
    "PASS release inputs: manifest, DAG, archived receipts, registry, graphs, and hashes agree",
    "PASS current partial Lean replay: four trust-zero axiom reports",
    "PASS fail-closed state: lifecycle planned; root H2/M3/R4; accepted receipts 0",
    "BLOCKED dependency.S56-M-1088-VALIDATION.master_acceptance",
    "BLOCKED M1088-L-FINITE-CONCENTRATION and M1088-T-ENGINE kernel closure",
    "BLOCKED audit, trust, cold/offline, independent-verifier, and bundle gates",
    "verdict=blocked audit_complete=false theorem_complete=false",
]
EXPECTED_INPUTS = {
    "README.md": "2b268be46a7c30daf6f8865673ebc5ab5ef29fb9bb196d81421d203f26e75283",
    "instance.json": "e454b9504f98eeec55999d9555b85a65c58315313b2bfff7355401005ee43e76",
    "task-dag.json": "c25b5f22ba0ff40af0de6cc0810dc4fe381e9b708e187781b89f4a68fd7e182c",
    "Statement.lean": "907c7a7e9cefced10649e3de0b3230e78bf852484b93caf02b6f40ff9920e1c7",
    "ObligationTree.lean": "3a84b1dddb7d61e43fda96574732531f49c6aac353b35e17de80a1ed056a5939",
    "Proof.lean": "77e8587590de79fa2f58029f1bdcddda1d61c6e2461740508be252f754ed21c5",
    "Validation.lean": "b2bef1c81f2544d69b4be7268da3504e45e43a58fb7239d7044fbb39c72f4d75",
    "anchor-audit.md": "d19940bb5a7ad055c1a1a6a2f95ce3570be4e1833b9e769a5234f32070ce8086",
    "source-statement-crosswalk.md": "956e15c97c92706871cdf30d131e0ebde9e57128a171c8f39f4b0c970ff16acf",
    "obligation-registry.json": "ea7883a01a2ed602fa365888a2c836a64a6dacd1d404e38aa98818e5ecded495",
    "typed-graphs.json": "737f489744cc0342a47d05549aa9acf45f3fe21e6a0451cd2301298050b05069",
    "proof-receipt.json": "fc9dc7a73c59ca8785cee48cd012b43600f9878e5b679dda9c034ef34d45f2c1",
    "proof-blocker.json": "ad74bc238c86bc7dc7485024c228472c03c8a25eb564592aecd3480b3b79c1fe",
    "validation-spec.json": "2448c56fab3463264f4117b34c2ef729bae1a9e5bf77c8508ccc4daa01a61290",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "edb3ddd3e403b859ad41e9e6e54091eb6cd12819714c98196c3442db526b9176",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "4f5335b6a1724a2856bb155e3147debd858e7fc1cf07d4b70c757e6515f5dd23",
    "Docs/Stage1_Blueprint_rev-5.6.md": "770174567b83623a839cf4f9a68c1a78524d516ecd1bc18e17c64130a48052e5",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}


def fail(message: str) -> None:
    raise SystemExit(f"release-decision: FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key in {path}: {key}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    require(isinstance(value, dict), f"JSON object required: {path}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_result(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as error:
        fail(f"command timed out: {argv!r}\n{error.stdout or ''}")


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900,
) -> str:
    completed = run_result(argv, cwd=cwd, env=env, timeout=timeout)
    require(
        completed.returncode == 0,
        f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}",
    )
    return completed.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).strip()


def code_without_comments(source: str) -> str:
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
    require(depth == 0, "unterminated Lean block comment")
    return "".join(output)


def axiom_reports(output: str) -> dict[str, list[str]]:
    matches = re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL)
    return {
        name: [part.strip() for part in raw.split(",") if part.strip()]
        for name, raw in matches
    }


def current_kernel_replay() -> tuple[str, str]:
    """Replay the exact statement source and four partial proof declarations."""

    statement_output = run([
        "lake", "env", "lean", "--trust=0",
        f"../../Stage1_Instances/{THEOREM}/Statement.lean",
    ], cwd=LEAN_ROOT, timeout=300)
    require("def Stage1Instances.THM_M_1088.BorellTISTarget." in statement_output and
            ": Prop :=" in statement_output,
            "current statement replay did not print the exact target")
    output = run(["bash", str(HERE / "check_proof.sh")], timeout=610)
    proof_reports = axiom_reports(output)
    require(set(proof_reports) == PROOF_DECLARATIONS,
            "partial proof declaration coverage drifted")
    require(all(value == EXPECTED_AXIOMS for value in proof_reports.values()),
            "partial proof axiom profile drifted")
    require("error:" not in output and "sorryAx" not in output,
            "Lean replay observed an error or placeholder axiom")
    require("PASS THM-M-1088 isolated Lean replay" in output,
            "partial proof replay did not reach its success boundary")
    return statement_output, output


def main() -> None:
    require(not sys.flags.optimize, "optimized Python disables fail-closed checks")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    require(git("rev-parse", "HEAD") == BASE_REVISION, "base revision drifted")
    require(git("rev-parse", "HEAD^{tree}") == BASE_TREE, "base tree drifted")
    require(
        run(["git", "merge-base", "--is-ancestor", VALIDATION_BASE_REVISION, BASE_REVISION]) == "",
        "validation base is not an ancestor of the release base",
    )
    require(git("rev-parse", f"{VALIDATION_BASE_REVISION}^{{tree}}") == VALIDATION_BASE_TREE,
            "validation base tree drifted")
    for name, expected in EXPECTED_INPUTS.items():
        require(digest(HERE / name) == expected, f"reconciled input drifted: {name}")
    require(decision["reconciled_inputs"] == EXPECTED_INPUTS, "decision input map drifted")
    for name, expected in AUTHORITY_INPUTS.items():
        require(digest(ROOT / name) == expected, f"authority input drifted: {name}")
    require(decision["authority_inputs"] == AUTHORITY_INPUTS, "decision authority map drifted")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    require(target["execution_rank"] == 530, "execution rank drifted")
    require(target["baseline"] == "L0" and target["rework_required"] is True,
            "uniform L0 baseline drifted")
    require(target["lifecycle_mode"] == "planned", "target lifecycle drifted")
    require(target["legacy_artifacts_accepted"] is False, "legacy evidence became accepted")
    require(target["theorem_complete"] is False, "manifest claims theorem completion")

    items = {row["id"]: row for row in execution["items"]}
    require(items[ITEM] == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 530,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1088-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }, "release execution item drifted")
    require(items["S56-M-1088-VALIDATION"]["state"] == "[_]",
            "validation dependency is no longer worker-provisional")
    require(items["S56-M-1088-VALIDATION"]["attempts"] == 1,
            "validation dependency attempt count drifted")

    require(instance["lifecycle"] == "planned", "instance lifecycle drifted")
    require(instance["root_vector"] == {"H": "H2", "M": "M3", "R": "R4"},
            "instance root vector drifted")
    require(instance["audit_complete"] is instance["theorem_complete"] is False,
            "instance claims a terminal decision")
    require(instance["accepted_proof_state"] == [], "instance has accepted proof state")
    require("Proof.lean" not in instance["owned_artifacts"],
            "expected stale instance artifact inventory was silently changed")
    require(task_dag["accepted_states"] == [], "local task DAG has accepted states")
    local_states = {row["id"]: row["state"] for row in task_dag["tasks"]}
    require(local_states["S56-M-1088-VALIDATION"] == "open",
            "expected stale local validation projection was silently changed")
    require(local_states[ITEM] == "open", "local release projection drifted")

    require(registry["denominator_sha256"] == DENOMINATOR_SHA256,
            "registry denominator drifted")
    require([row["obligation_id"] for row in registry["obligations"]] == ALL_OBLIGATIONS,
            "obligation inventory drifted")
    require(graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256,
            "graph/registry denominator mismatch")
    require({row["obligation_id"] for row in graphs["nodes"]} == set(ALL_OBLIGATIONS),
            "typed graph obligation universe drifted")
    root = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1088-ROOT")
    require((root["human_debt"], root["machine_debt"], root["readability_debt"])
            == ("H2", "M3", "R4"), "typed graph root vector drifted")
    require(root["evidence_ids"] == [] and root["source_crosswalk_id"] ==
            "primary-source-pinpoint-pending", "root source/evidence boundary drifted")
    require(root["provenance_id"] == "pending", "root provenance boundary drifted")
    boundary = graphs["closure_boundary"]
    require(boundary["closed_obligations"] == [], "typed graph claims obligation closure")
    require(boundary["root_closed"] is False, "typed graph claims root closure")
    require(boundary["audit_complete"] is boundary["theorem_complete"] is False,
            "typed graph claims terminal completion")
    require(boundary["remaining_root_cut_set"] == ["M1088-T-ENGINE"],
            "typed graph root cut drifted")
    require(graphs["graphs"]["evidence"]["edges"] == [], "evidence graph is not empty")

    require(proof["support_state"] == "provisional_worker_selftest",
            "proof support boundary drifted")
    require(proof["accepted"] is False, "proof receipt claims acceptance")
    require(proof["provisionally_closed_obligation_ids"] == [],
            "proof receipt claims provisional frozen closure")
    require(proof["accepted_closed_obligation_ids"] == [],
            "proof receipt claims accepted frozen closure")
    require(proof["result"]["root_kernel_closed"] is False,
            "proof receipt claims root closure")
    require(proof["result"]["theorem_complete"] is False,
            "proof receipt claims theorem completion")
    require(proof["remaining_root_cut_set"] == PROOF_CUT, "proof root cut drifted")
    require(blocker["provisionally_closed_obligation_ids"] == [],
            "proof blocker claims frozen closure")
    require(blocker["root_closed"] is blocker["theorem_complete"] is False,
            "proof blocker claims completion")

    require(digest(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256,
            "validation receipt bytes drifted")
    require(validation["base_revision"] == VALIDATION_BASE_REVISION,
            "validation receipt base drifted")
    require(validation["base_tree"] == VALIDATION_BASE_TREE,
            "validation receipt base tree drifted")
    require(validation["support_state"] == "provisional_worker_selftest",
            "validation support boundary drifted")
    require(validation["accepted"] is False and validation["release_grade"] is False,
            "validation became accepted or release grade")
    result = validation["result"]
    require(result["accepted_closed_obligation_ids"] == [],
            "validation claims accepted obligation closure")
    require(result["root_kernel_closed"] is False, "validation claims root closure")
    require(result["root_vector_after"] == {"H": "H2", "M": "M3", "R": "R4"},
            "validation root vector drifted")
    require(result["proof_execution_remaining_root_cut_set"] == PROOF_CUT,
            "validation proof cut drifted")
    require(result["audit_complete"] is False and result["theorem_complete"] is False,
            "validation claims terminal completion")

    historical_validator = (HERE / "check_validation.py").read_text(encoding="utf-8")
    require(f'BASE_REVISION = "{VALIDATION_BASE_REVISION}"' in historical_validator,
            "historical validator no longer binds its archived base")
    require('"state": "[ ]"' in historical_validator and
            '"attempts": 0' in historical_validator,
            "historical validator no longer binds its archived DAG row")
    predecessor_replay = run_result(
        ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"], timeout=60,
    )
    require(predecessor_replay.returncode == 1,
            "historical validation recipe unexpectedly became current")
    require(
        'assert git("rev-parse", "HEAD") == BASE_REVISION' in predecessor_replay.stdout and
        "AssertionError" in predecessor_replay.stdout,
        "historical validation recipe failed for an unexpected reason")

    require(decision["schema_version"] == "stage1-release-decision/1.0",
            "release decision schema drifted")
    require(decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM,
            "release decision identity drifted")
    require(decision["intent"] == "release" and decision["verdict"] == "blocked",
            "release intent or verdict drifted")
    require(decision["release_grade"] is decision["release_accepted"] is False,
            "release decision claims release grade")
    require(decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE,
            "decision base drifted")
    require(decision["lifecycle_before"] == decision["lifecycle_after"] == "planned",
            "blocked release advanced lifecycle")
    require(decision["accepted_receipt_ids"] == [], "worker accepted a receipt")
    require(decision["root_vector"] == {
        "before": {"H": "H2", "M": "M3", "R": "R4"},
        "after": {"H": "H2", "M": "M3", "R": "R4"},
    }, "release changed the authoritative root vector")
    require(decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }, "terminal decisions do not fail closed")
    require(decision["first_failed_gate"]["gate_id"] ==
            "S56-10.2-DEPENDENCY-ACCEPTANCE", "first node gate drifted")
    require(decision["first_failed_gate"]["detail"] ==
            "dependency.S56-M-1088-VALIDATION.master_acceptance",
            "direct dependency gate drifted")
    require(decision["first_failed_theorem_gate"]["gate_id"] ==
            "M1088-L-FINITE-CONCENTRATION.kernel_closure",
            "first theorem gate drifted")
    require(decision["first_failed_target_gate"]["gate_id"] ==
            "S56-5.1-CANONICAL-EXPRESSION-FINGERPRINT",
            "first target gate drifted")
    require(decision["first_failed_audit_gate"]["gate_id"] ==
            "S56-8.1-H0-R0-RECONCILIATION", "first audit gate drifted")
    require(decision["first_failed_release_gate"]["gate_id"] ==
            "S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE",
            "first assurance gate drifted")
    require(decision["first_failed_reproduction_gate"]["gate_id"] ==
            "S56-10.6-HERMETIC-COLD-EMPTY-CACHE",
            "first reproduction gate drifted")
    require(decision["remaining_root_cut_set"] == PROOF_CUT,
            "decision mathematical root cut drifted")
    require(decision["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256,
            "decision dependency receipt hash drifted")
    require(decision["dependency"]["receipt_id"] == validation["receipt_id"],
            "decision names wrong dependency receipt")
    require(decision["dependency"]["master_accepted"] is False,
            "decision claims dependency master acceptance")
    for key in (
        "validation_dependency_master_accepted",
        "exact_root_kernel_closed",
        "structured_public_state_reconciled",
        "pinpoint_h0_and_independent_source_review",
        "independent_r0_review",
        "audit_z_accepted",
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
        require(decision["evidence_reconciliation"][key] is False,
                f"release silently cleared {key}")
    require(decision["evidence_reconciliation"]["accepted_closed_obligation_ids"] == [],
            "release reconciliation claims accepted closure")
    require(decision["evidence_reconciliation"]["current_partial_kernel_replay"] ==
            "pass_as_provisional_trust_zero_warm_cache_evidence",
            "current partial replay classification drifted")
    require(decision["evidence_reconciliation"]["predecessor_recipe_freshness"] ==
            "fail_closed_phase_bound_to_old_head_and_old_dag_state",
            "stale predecessor recipe was hidden")

    require(spec["schema_version"] == "stage1-validation-recipe/1.0",
            "release recipe schema drifted")
    require(spec["item_id"] == receipt["item_id"] == ITEM,
            "release recipe/receipt item drifted")
    require(spec["theorem_id"] == receipt["theorem_id"] == THEOREM,
            "release recipe/receipt theorem drifted")
    require(spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py",
    ], "release argv drifted")
    require(spec["cwd"] == "." and spec["network_policy"] == "denied",
            "release recipe policy drifted")
    require(spec["timeout_seconds"] == 900 and spec["expected_exit"] == 0,
            "release recipe resource contract drifted")
    require(spec["env_allowlist"] == {
        "HOME": "inherited_nonrelease_input",
        "PATH": "inherited_nonrelease_input; resolves Python, Git, Bash, Lake, timeout, tee, and core utilities",
        "LANG": "inherited_nonrelease_input",
        "LC_ALL": "inherited_nonrelease_input",
        "TZ": "inherited_nonrelease_input",
        "ELAN_TOOLCHAIN": "inherited_nonrelease_input",
        "LEAN_NUM_THREADS": "set to 1 only by the nested proof replay",
        "PYTHONOPTIMIZE": "must be unset or zero; checker rejects optimized execution",
    }, "negative release recipe environment boundary drifted")
    require(spec["covered_obligation_ids"] == [],
            "negative release recipe must not claim proof coverage")
    require(spec["observed_open_state_obligation_ids"] == ALL_OBLIGATIONS,
            "release recipe does not reconcile the frozen open inventory")
    require(spec["coverage_semantics"].endswith("proof evidence for none of them."),
            "release recipe open-state coverage boundary drifted")
    require(set(spec["covered_declarations"]) == {
        "Stage1Instances.THM_M_1088.BorellTISTarget",
        "Stage1Instances.THM_M_1088.target_iff_expandedSourceShape",
        *PROOF_DECLARATIONS,
    },
            "release declaration coverage drifted")
    require(len(spec["covered_declarations"]) == 6,
            "release declaration coverage contains duplicates")

    require(receipt["schema_version"] == "stage1-node-receipt/1.0",
            "release receipt schema drifted")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE,
            "release receipt base drifted")
    started = datetime.fromisoformat(receipt["validation_started_at"])
    ended = datetime.fromisoformat(receipt["validation_ended_at"])
    validated = datetime.fromisoformat(receipt["validated_at"])
    require(started <= ended == validated, "release receipt timing drifted")
    require(ended <= datetime.now(ended.tzinfo), "release receipt end time is in the future")
    require(receipt["support_state"] == "provisional_worker_selftest",
            "release receipt support drifted")
    require(receipt["accepted"] is False and receipt["release_grade"] is False,
            "release receipt claims acceptance")
    require(receipt["content_addressed_release_evidence"] is False,
            "worker receipt claims content-addressed release evidence")
    require(receipt["master_accepted"] is False, "worker claims master acceptance")
    require(receipt["decision_id"] == decision["decision_id"], "receipt names wrong decision")
    require(receipt["decision_sha256"] == digest(HERE / "release-decision.json"),
            "release decision hash drifted")
    require(receipt["release_spec_sha256"] == digest(HERE / "release-spec.json"),
            "release spec hash drifted")
    require(receipt["checker_sha256"] == digest(HERE / "check_release.py"),
            "release checker hash drifted")
    require(receipt["public_projection_sha256"] == digest(HERE / "release-validation.md"),
            "release projection hash drifted")
    require(receipt["dependency"] == decision["dependency"],
            "dependency ledgers disagree")
    repository_state = receipt["repository_state"]
    require(repository_state["initial_status"] == ["?? Formalizations/Lean/.lake"],
            "release initial worktree state drifted")
    require(repository_state["base_owned_path_patch_sha256"] == hashlib.sha256(b"").hexdigest(),
            "release base owned-path patch boundary drifted")
    require(repository_state["worktree_classification"] == "dirty nonrelease worker evidence",
            "release worktree classification drifted")
    require(set(repository_state["final_expected_status_excluding_preexisting_cache"]) ==
            CHANGED_PATHS, "release final worktree inventory drifted")
    require(set(repository_state["untracked_input_hashes"]) == {
        "Formalizations/Lean/.lake",
    }, "release untracked input inventory drifted")
    cache_input = repository_state["untracked_input_hashes"]["Formalizations/Lean/.lake"]
    cache_text = (LEAN_ROOT / ".lake").readlink().as_posix().encode("utf-8")
    require(cache_input["object_type"] == "symbolic_link",
            "release cache input type drifted")
    require(cache_input["bytes"] == len(cache_text) == 66,
            "release cache symlink length drifted")
    require(cache_input["sha256"] == hashlib.sha256(cache_text).hexdigest(),
            "release cache symlink digest drifted")
    handoff = receipt["worker_handoff"]
    require(handoff["exact_statements_added_or_changed"] == [],
            "release handoff claims a statement delta")
    require(handoff["typed_graph_changes"] == [],
            "release handoff claims a typed-graph delta")
    require(handoff["debt_vector_change"] == "none: H2/M3/R4 -> H2/M3/R4",
            "release handoff debt delta drifted")
    require(handoff["declaration_ownership"] == [],
            "release handoff claims Lean declaration ownership")
    expected_fingerprints = {
        row["obligation_id"]: row["statement_fingerprint"]
        for row in registry["obligations"]
    }
    require(handoff["obligation_statement_fingerprints"] == expected_fingerprints,
            "release handoff obligation fingerprints drifted")
    require(handoff["proof_body_locations"] == [
        f"Stage1_Instances/{THEOREM}/Proof.lean",
    ], "release handoff proof-body location drifted")
    require(handoff["receipt_ids"][-1] == receipt["receipt_id"],
            "release handoff omits its receipt id")
    require(handoff["recipe_ids"][-1] == spec["recipe_id"],
            "release handoff omits its recipe id")
    require(set(handoff["actual_source_ownership"]) == {
        f"Stage1_Instances/{THEOREM}/check_release.py",
        f"Stage1_Instances/{THEOREM}/release-spec.json",
        f"Stage1_Instances/{THEOREM}/release-decision.json",
        f"Stage1_Instances/{THEOREM}/release-receipt.json",
    }, "release handoff source ownership drifted")
    require(handoff["readable_ownership"] == [
        f"Stage1_Instances/{THEOREM}/release-validation.md",
    ], "release handoff readable ownership drifted")
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "observed_open_state_obligation_ids",
        "coverage_semantics", "covered_declarations", "scope_boundary",
    ):
        require(receipt["recipe"][key] == spec[key],
                f"receipt/spec recipe mismatch: {key}")
    require(receipt["known_failures"] == decision["known_failures"],
            "failure ledgers disagree")
    require(set(receipt["changed_paths"]) == CHANGED_PATHS,
            "release receipt changed paths drifted")
    require(receipt["result"]["verdict"] == "blocked", "receipt verdict drifted")
    require(receipt["result"]["accepted_receipt_ids"] == [],
            "receipt result claims accepted receipts")
    require(receipt["result"]["accepted_closed_obligation_ids"] == [],
            "receipt result claims accepted obligations")
    require(receipt["result"]["audit_complete"] is False and
            receipt["result"]["theorem_complete"] is False,
            "receipt claims terminal completion")
    require(receipt["result"]["remaining_root_cut_set"] == PROOF_CUT,
            "receipt root cut drifted")
    require(receipt["result"]["first_failed_gate"] ==
            "dependency.S56-M-1088-VALIDATION.master_acceptance",
            "receipt direct dependency failure drifted")
    require(receipt["result"]["first_failed_target_gate"] ==
            "S56-5.1-CANONICAL-EXPRESSION-FINGERPRINT",
            "receipt target failure drifted")

    require(packet["item_id"] == ITEM and packet["state"] == "[_]",
            "worker packet identity/state drifted")
    require(packet["base_revision"] == BASE_REVISION, "worker packet base drifted")
    require(set(packet["changed_paths"]) == CHANGED_PATHS,
            "worker packet changed paths drifted")
    require(packet["known_failures"] == decision["known_failures"],
            "worker packet failure ledger drifted")
    for fragment in (
        "verdict blocked",
        "planned",
        "H2/M3/R4",
        "accepted receipts are empty",
        "M1088-T-ENGINE remains open",
        "audit_complete=false",
        "theorem_complete=false",
    ):
        require(fragment in packet["output_summary"],
                f"worker output summary omits {fragment!r}")

    actual_changes = {
        line[3:] for line in git(
            "status", "--porcelain=v1", "--untracked-files=all", "--",
            f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
        ).splitlines() if line
    }
    require(actual_changes == CHANGED_PATHS,
            f"actual scoped changes differ from handoff: {sorted(actual_changes)}")

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        require(prohibited.search(source) is None, f"prohibited Lean construct in {name}")
    proof_source = code_without_comments((HERE / "Proof.lean").read_text(encoding="utf-8"))
    require("(hmgf : ProbabilityTheory.HasSubgaussianMGF" in proof_source,
            "partial proof no longer exposes the missing MGF premise")
    require("theorem BorellTISTarget" not in proof_source,
            "proof source unexpectedly declares an exact root body")

    require(MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable")
    require(git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION,
            "mathlib revision drifted")
    require(git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE,
            "mathlib tree drifted")
    require(git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE,
            "mathlib remote drifted")
    require(git("status", "--porcelain=v1", cwd=MATHLIB) == "",
            "mathlib worktree is dirty before replay")
    lean_path = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake_path = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    require(receipt["environment"]["lean_executable_sha256"] == digest(lean_path),
            "Lean executable digest drifted")
    require(receipt["environment"]["lake_executable_sha256"] == digest(lake_path),
            "Lake executable digest drifted")
    bwrap_path = shutil.which("bwrap")
    require(bwrap_path is not None, "bubblewrap is unavailable")
    require(receipt["environment"]["bubblewrap_executable_sha256"] ==
            digest(Path(bwrap_path)), "bubblewrap executable digest drifted")
    require(receipt["environment"]["python"] == f"CPython {platform.python_version()}",
            "Python version drifted")
    require(receipt["environment"]["python_executable_sha256"] == digest(Path(sys.executable)),
            "Python executable digest drifted")
    git_path = shutil.which("git")
    require(git_path is not None, "git is unavailable")
    require(receipt["environment"]["git"] == run([git_path, "--version"]).strip(),
            "git version drifted")
    require(receipt["environment"]["git_executable_sha256"] == digest(Path(git_path)),
            "git executable digest drifted")

    statement_output, replay_output = current_kernel_replay()
    require(git("status", "--porcelain=v1", cwd=MATHLIB) == "",
            "mathlib worktree changed during replay")
    require(receipt["current_kernel_replay"]["stdout_sha256"] ==
            hashlib.sha256(replay_output.encode("utf-8")).hexdigest(),
            "current replay output hash drifted")
    require(receipt["current_kernel_replay"]["stdout_bytes"] ==
            len(replay_output.encode("utf-8")), "current replay byte count drifted")
    require(receipt["current_kernel_replay"]["statement_stdout_sha256"] ==
            hashlib.sha256(statement_output.encode("utf-8")).hexdigest(),
            "current statement replay output hash drifted")
    require(receipt["current_kernel_replay"]["statement_stdout_bytes"] ==
            len(statement_output.encode("utf-8")),
            "current statement replay byte count drifted")
    require(receipt["current_kernel_replay"]["axiom_report_count"] == 4,
            "receipt axiom report count drifted")

    validation_action = receipt["validation_action"]
    require(validation_action["cwd"] == "." and validation_action["argv"] == spec["argv"],
            "release validation action command drifted")
    action_started = datetime.fromisoformat(validation_action["started_at"])
    action_ended = datetime.fromisoformat(validation_action["ended_at"])
    require(action_started == started and action_ended == ended,
            "release validation action timing disagrees with receipt")
    require(validation_action["exit_code"] == 0,
            "release validation action did not pass")
    expected_stdout = ("\n".join(SUMMARY_LINES) + "\n").encode("ascii")
    empty_sha256 = hashlib.sha256(b"").hexdigest()
    require(validation_action["stdout_sha256"] == hashlib.sha256(expected_stdout).hexdigest(),
            "release validation stdout hash drifted")
    require(validation_action["stdout_bytes"] == len(expected_stdout),
            "release validation stdout byte count drifted")
    require(validation_action["stderr_sha256"] == empty_sha256 and
            validation_action["stderr_bytes"] == 0,
            "release validation stderr evidence drifted")
    require(validation_action["combined_log_sha256"] ==
            hashlib.sha256(expected_stdout).hexdigest() and
            validation_action["combined_log_bytes"] == len(expected_stdout),
            "release validation combined log evidence drifted")

    public = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`",
        "`[H2, M3, R4]`",
        "`AUDIT-Z`",
        "`THEOREM-Z`",
        "release_grade=false",
        "accepts\nno receipt",
        "M1088-L-FINITE-CONCENTRATION",
    ):
        require(fragment in public, f"release projection omits {fragment!r}")
    require("/home/" not in public and ".cron/" not in public,
            "public release projection exposes a private worker path")
    require("theorem_complete=true" not in public,
            "public release projection claims theorem completion")

    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        require(data.endswith(b"\n"), f"missing final newline: {relative}")
        require(b"\r" not in data and b"\x00" not in data,
                f"invalid byte in {relative}")
        require(all(not line.endswith((b" ", b"\t")) for line in data.splitlines()),
                f"trailing whitespace in {relative}")

    require(receipt["environment"]["platform"] == f"{platform.system()} {platform.machine()}",
            "receipt platform drifted")
    sys.stdout.write("\n".join(SUMMARY_LINES) + "\n")


if __name__ == "__main__":
    main()
