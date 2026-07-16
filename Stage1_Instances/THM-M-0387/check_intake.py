#!/usr/bin/env python3
"""Replay the scheduler-owned intake predicate for THM-M-0387."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEOREM_ID = "THM-M-0387"
ITEM_ID = "S56-M-0387-INTAKE"
CONTEXT_SHA256 = "90f56448880bb5c1f54b618027daea5b7b32be6e0d05ba2723c43bcc39e17235"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
SHARED_GROUPS = [
    "SHARED-MODULE-12060056b1f9fd84",
    "SHARED-MODULE-2884526d078231ae",
    "SHARED-MODULE-4f11ecbb9eb91fb0",
    "SHARED-MODULE-97c08d929c8c634f",
    "SHARED-MODULE-d59c2e49212cb785",
]
ROLE_PATHS = {
    "instance_manifest": "Stage1_Instances/THM-M-0387/intake.json",
    "scope_map": "Stage1_Instances/THM-M-0387/scope-map.md",
    "source_crosswalk": "Stage1_Instances/THM-M-0387/source-statement-crosswalk.md",
    "open_task_dag": "Stage1_Instances/THM-M-0387/task-dag.json",
    "phase_receipt": "Stage1_Instances/THM-M-0387/intake-receipt.json",
}
PHASES = (
    ("STATEMENT", "statement"),
    ("ANCHOR_AUDIT", "anchor_audit"),
    ("OBLIGATION_TREE", "obligation_tree"),
    ("PROOF", "proof"),
    ("VALIDATION", "validation"),
    ("RELEASE", "release"),
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_OID_RE = re.compile(r"^[0-9a-f]{40,64}$")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def load(relative: str) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, child in pairs:
            require(key not in value, f"duplicate JSON key {key!r} in {relative}")
            value[key] = child
        return value

    value = json.loads(
        (ROOT / relative).read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicates,
    )
    require(isinstance(value, dict), f"{relative} must contain a JSON object")
    return value


def sha256(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def git_blob(relative: str) -> str:
    data = (ROOT / relative).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def require_pointer(record: dict, pointer: str) -> None:
    value: object = record
    for component in pointer.removeprefix("/").split("/"):
        require(
            isinstance(value, dict) and component in value,
            f"phase receipt lacks contract field {pointer}",
        )
        value = value[component]


def require_nonempty_strings(value: object, message: str) -> None:
    require(
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and bool(item.strip()) for item in value),
        message,
    )


def require_stable_provenance_consistency(
    instance: dict, receipt: dict, ledger: dict
) -> None:
    revisions = instance["source_revisions"]
    inputs = receipt["inputs"]
    require(
        revisions["repository_base"]
        == receipt["base_revision"]
        == ledger["repository_revision"],
        "repository base disagrees across intake evidence",
    )
    require(
        revisions["repository_base_tree"] == receipt["base_tree"],
        "repository base tree disagrees across intake evidence",
    )
    require(
        revisions["v2_blueprint_sha256"]
        == inputs["task_state_authority"]["sha256"],
        "base Blueprint digest disagrees across intake evidence",
    )
    require(
        revisions["theorem_dag_sha256"]
        == inputs["theorem_dag_sha256"]
        == ledger["observed_theorem_dag_sha256"],
        "base theorem DAG digest disagrees across intake evidence",
    )
    require(
        revisions["phase_contract_sha256"]
        == inputs["phase_contract_sha256"]
        == CONTRACT_SHA256,
        "phase contract digest disagrees across intake evidence",
    )
    require(
        revisions["target_manifest_sha256"]
        == inputs["target_manifest"]["sha256"],
        "target manifest digest disagrees across intake evidence",
    )
    require(
        revisions["authoritative_blueprint_sha256"]
        == inputs["assurance_authority"]["sha256"],
        "assurance Blueprint digest disagrees across intake evidence",
    )


def check() -> None:
    manifest = load("Docs/Stage1_Targets_rev-5.6.json")
    execution = load("Docs/Stage1_Execution_DAG_rev-5.6.json")
    theorem_dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")
    instance = load(ROLE_PATHS["instance_manifest"])
    task_dag = load(ROLE_PATHS["open_task_dag"])
    receipt = load(ROLE_PATHS["phase_receipt"])
    ledger = load("Stage1_Instances/THM-M-0387/dependency-reuse-ledger.json")

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    require(target["execution_rank"] == instance["execution_rank"] == 1, "rank drift")
    require(
        target["legacy_priority_slot"] == instance["legacy_priority_slot"] == "S1-M-001",
        "legacy slot drift",
    )
    require(target["name"] == instance["name_zh"] == "费马大定理", "name drift")
    require(
        target["category"] == instance["category"] == "数论 / 丢番图方程",
        "category drift",
    )
    require(target["baseline"] == instance["baseline"] == "L0", "baseline drift")
    require(target["rework_required"] is instance["rework_required"] is True, "rework drift")
    require(
        target["legacy_artifacts_accepted"] is instance["legacy_artifacts_accepted"] is False,
        "legacy acceptance drift",
    )
    require(target["target_lane"] == instance["target_lane"], "target lane drift")
    require(target["intake_score"] == instance["intake_score"] == 279, "intake score drift")
    require(target["source_status_untrusted"] == instance["source_status_untrusted"], "source status drift")
    require(target["lifecycle_mode"] == instance["lifecycle_mode"] == "planned", "lifecycle drift")
    require(target["theorem_complete"] is instance["theorem_complete"] is False, "terminal overclaim")

    authoritative = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    require(authoritative["theorem_id"] == THEOREM_ID, "item theorem drift")
    require(authoritative["phase"] == "intake" and authoritative["layer"] == 0, "phase drift")
    require(authoritative["state"] in {"[_]", "[x]"}, "intake lacks worker evidence")
    require(authoritative["depends_on"] == [], "intake gained a predecessor")
    require(authoritative["owned_paths"] == [f"Stage1_Instances/{THEOREM_ID}"], "ownership drift")
    require(
        authoritative["deliverable"]
        == "Create the theorem dossier, scope map, and source-statement crosswalk.",
        "deliverable drift",
    )
    require(
        authoritative["completion_gate"] == "rev-5.6 node-specific receipt and master acceptance",
        "completion gate drift",
    )

    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    require(node["v2_execution_rank"] == 1 and node["topological_layer"] == 0, "claim order drift")
    require(node["direct_hard_parents"] == node["transitive_hard_ancestors"] == [], "hard closure drift")
    require(node["direct_reuse_hint_ids"] == [], "reuse hint drift")
    require(sorted(node["shared_lemma_group_ids"]) == SHARED_GROUPS, "shared group drift")
    require(node["dependency_context_sha256"] == CONTEXT_SHA256, "dependency context drift")

    phase_contract = next(row for row in contract["phases"] if row["phase"] == "intake")
    require(contract["schema_version"] == "stage1-phase-acceptance-contracts/1.0", "contract schema drift")
    require(sha256("Docs/Stage1_Phase_Acceptance_Contracts.json") == CONTRACT_SHA256, "contract bytes drift")
    require(phase_contract["intent"] == "intake" and phase_contract["layer"] == 0, "contract phase drift")
    require(
        phase_contract["worker_verdicts_eligible_for_review"] == ["accepted", "no_state_change"],
        "eligible verdict drift",
    )
    selected: dict[str, str] = {}
    for role in phase_contract["required_artifact_roles"]:
        candidates = [
            pattern.format(theorem_id=THEOREM_ID)
            for pattern in role["path_candidates"]
            if (ROOT / pattern.format(theorem_id=THEOREM_ID)).is_file()
        ]
        require(len(candidates) == 1, f"artifact role {role['role']} is missing or ambiguous")
        selected[role["role"]] = candidates[0]
    require(selected == ROLE_PATHS, "selected intake role paths drifted")
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase_contract["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    require(validators == ["Stage1_Instances/THM-M-0387/check_intake.py"], "validator selection is ambiguous")

    require(instance["schema_version"] == "stage1-instance-intake/1.0", "instance schema drift")
    require(instance["normative_profile"] == "machine-theorem-assurance/1.0", "profile drift")
    require(instance["item_id"] == ITEM_ID and instance["intent"] == "intake", "instance identity drift")
    require(instance["lifecycle"] == instance["lifecycle_mode"] == "planned", "instance lifecycle drift")
    require(bool(instance["canonical_statement"]) and bool(instance["domain_and_universes"]), "claim is empty")
    formal = instance["canonical_formal_target"]
    require(formal["backend"] == "lean4" and formal["module"] == "Mathlib.NumberTheory.FLT.Basic", "formal backend drift")
    require(formal["declaration_or_expression"] == "FermatLastTheorem", "formal candidate drift")
    require(formal["elaborated_expression_hash"] is None, "intake claims an expression hash")
    require(formal["environment_fingerprint"] is None, "intake claims an environment fingerprint")
    require(formal["gate_state"] == "open_pending_statement_phase" and formal["open_boundary"], "statement boundary missing")
    require(instance["ordered_binders"] == ["n : Nat", "x : Nat", "y : Nat", "z : Nat"], "binder drift")
    require(bool(instance["quantifiers"]) and len(instance["hypotheses"]) == 4, "claim shape is incomplete")
    require(instance["conclusion"] == "x ^ n + y ^ n != z ^ n", "conclusion drift")
    require(len(instance["alternate_encodings"]) == 4, "alternate encoding inventory drift")
    require(all(row["checked_witness"] is None for row in instance["alternate_encodings"]), "intake credits a transport")
    require(instance["candidate_encodings_not_credited"] is True, "candidate credit boundary missing")
    require(bool(instance["excluded_degenerate_cases"]), "degenerate-case boundary missing")
    for profile in ("foundation_profile", "tcb_profile", "computation_profile"):
        require(isinstance(instance[profile], dict) and instance[profile].get("profile_id"), f"{profile} is incomplete")
    require(instance["formal_system"]["toolchain_file"] == "Formalizations/Lean/lean-toolchain", "toolchain drift")
    require(instance["obligation_registry_hash"] is None, "intake freezes an obligation denominator")
    require(instance["discovery_protocol_hash"] is None, "intake freezes a discovery denominator")
    require(instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == [], "intake imports proof credit")
    require(instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}, "root vector drift")
    require(instance["audit_complete"] is instance["theorem_complete"] is False, "terminal overclaim")
    require(bool(instance["downstream_blockers"]) and bool(instance["status_boundary"]), "open boundary missing")
    require(instance["owners_and_reviewers"]["acceptance_owner"] == "Stage1 integration lane", "acceptance owner drift")
    freshness = instance["freshness_and_revocation_policy"]
    require(
        isinstance(freshness["review_due"], str) and bool(freshness["review_due"].strip()),
        "freshness review trigger is empty",
    )
    require_nonempty_strings(
        freshness["invalidation_inputs"], "freshness invalidation inputs are empty"
    )
    require(
        isinstance(freshness["incident_path"], str) and bool(freshness["incident_path"].strip()),
        "freshness incident path is empty",
    )

    revisions = instance["source_revisions"]
    require(GIT_OID_RE.fullmatch(revisions["repository_base"]) is not None, "base revision is malformed")
    require(GIT_OID_RE.fullmatch(revisions["repository_base_tree"]) is not None, "base tree is malformed")
    require(SHA256_RE.fullmatch(revisions["v2_blueprint_sha256"]) is not None, "blueprint digest is malformed")
    require(SHA256_RE.fullmatch(revisions["theorem_dag_sha256"]) is not None, "DAG digest is malformed")
    require(revisions["phase_contract_sha256"] == CONTRACT_SHA256, "contract provenance drift")
    require(GIT_OID_RE.fullmatch(revisions["repository_source_record_blob"]) is not None, "source blob is malformed")
    require(GIT_OID_RE.fullmatch(revisions["mathlib"]) is not None, "mathlib revision is malformed")
    require(GIT_OID_RE.fullmatch(revisions["mathlib_tree"]) is not None, "mathlib tree is malformed")
    require(SHA256_RE.fullmatch(revisions["mathlib_flt_basic_sha256"]) is not None, "mathlib source hash is malformed")

    expected_tasks: list[str] = []
    predecessor = ITEM_ID
    for layer, (suffix, phase) in enumerate(PHASES, start=1):
        task_id = f"S56-M-0387-{suffix}"
        row = next(task for task in task_dag["tasks"] if task["id"] == task_id)
        authority = next(task for task in execution["items"] if task["id"] == task_id)
        require(row["phase"] == authority["phase"] == phase, f"task phase drift: {task_id}")
        require(row["layer"] == authority["layer"] == layer, f"task layer drift: {task_id}")
        require(row["depends_on"] == [predecessor], f"task dependency drift: {task_id}")
        require(row["owned_paths"] == authority["owned_paths"], f"task ownership drift: {task_id}")
        require(row["deliverable"] == authority["deliverable"], f"task deliverable drift: {task_id}")
        require(row["completion_gate"] == authority["completion_gate"], f"task gate drift: {task_id}")
        require(row["state"] == "open" and row["evidence_ids"] == [], f"planned DAG credits state: {task_id}")
        expected_tasks.append(task_id)
        predecessor = task_id
    require(task_dag["schema_version"] == "stage1-open-task-dag/1.0", "task DAG schema drift")
    require(task_dag["theorem_id"] == THEOREM_ID, "task DAG owner drift")
    require(task_dag["lifecycle_mode"] == "planned", "task DAG lifecycle drift")
    require(task_dag["accepted_states"] == [] and task_dag["theorem_complete"] is False, "task DAG credits closure")
    require([row["id"] for row in task_dag["tasks"]] == expected_tasks, "task DAG order drift")

    require(ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1", "ledger schema drift")
    require(ledger["consumer_theorem_id"] == THEOREM_ID, "ledger consumer drift")
    require(SHA256_RE.fullmatch(ledger["observed_theorem_dag_sha256"]) is not None, "ledger DAG digest malformed")
    require(ledger["dependency_context_sha256"] == CONTEXT_SHA256, "ledger context drift")
    require(GIT_OID_RE.fullmatch(ledger["repository_revision"]) is not None, "ledger base malformed")
    require(ledger["direct_parent_ids"] == ledger["transitive_ancestor_ids"] == [], "ledger hard closure is nonempty")
    require(ledger["hard_edge_ids"] == ledger["reuse_hint_ids"] == [], "ledger edge closure is nonempty")
    require(ledger["shared_group_ids"] == SHARED_GROUPS, "ledger shared groups drift")
    require(ledger["inspections"] == [] and ledger["unresolved_compatibility_obligations"] == [], "ledger has unresolved hard work")
    decisions = ledger["reuse_decisions"]
    require([row["source_id"] for row in decisions] == SHARED_GROUPS, "shared decision order drift")
    require(all(row["provider_theorem_id"] == "THM-M-0133" for row in decisions), "shared provider drift")
    require(all(row["decision"] == "not_applicable" for row in decisions), "intake claims shared reuse")
    require(all(row["context_digest"] == CONTEXT_SHA256 for row in decisions), "decision context drift")
    require(all(row["non_reuse_reason"] for row in decisions), "shared decision lacks a reason")
    for row in decisions:
        for relative, digest in row["inspected_member_artifacts"].items():
            require(relative.startswith("Stage1_Instances/THM-M-0133/"), "shared evidence owner drift")
            require(digest == sha256(relative), f"shared evidence hash drift: {relative}")
    require(ledger["closure_audit"]["parent_inspection_order"] == [], "parent inspection order drift")

    scope = (ROOT / ROLE_PATHS["scope_map"]).read_text(encoding="utf-8")
    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    require("all-exponent root" in scope and "Out of scope" in scope, "scope boundary is incomplete")
    require("n = 3" in scope and "regular primes" in scope, "partial-family exclusions are missing")
    require("Repository source record" in crosswalk and "Exact-statement choices still open" in crosswalk, "crosswalk boundary is incomplete")
    require("10.2307/2118559" in crosswalk and "10.2307/2118560" in crosswalk, "primary-source leads are missing")

    for pointer in set(contract["artifact_resolution"]["worker_phase_receipt_required_fields"]) | set(
        phase_contract["phase_receipt_required_fields"]
    ):
        require_pointer(receipt, pointer)
    require(receipt["schema_version"] == "stage1-node-receipt/1.0", "receipt schema drift")
    require(receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID, "receipt identity drift")
    require(receipt["phase"] == "intake" and receipt["intent"] == "intake", "receipt phase drift")
    require(GIT_OID_RE.fullmatch(receipt["base_revision"]) is not None, "receipt base malformed")
    require(GIT_OID_RE.fullmatch(receipt["base_tree"]) is not None, "receipt tree malformed")
    require(receipt["support_state"] == "provisional_worker_selftest", "support state drift")
    require(receipt["proposed_state"] == "[_]" and receipt["accepted"] is False, "worker/master boundary drift")
    require(receipt["verdict"] in {"accepted", "no_state_change"}, "worker verdict is not reviewable")
    require(receipt["selftest_status"] in {"passed", "passed_with_expected_projection_drift"}, "self-test did not pass")
    require(receipt["selftest_result"]["exit_code"] == 0, "aggregate self-test is nonzero")
    require(isinstance(receipt["selftest_result"]["commands"], list) and receipt["selftest_result"]["commands"], "command evidence missing")
    validator_argvs = {
        tuple(command.get("argv", []))
        for command in receipt["selftest_result"]["commands"]
        if isinstance(command, dict) and command.get("exit_code") == 0
    }
    require(
        (
            "/usr/bin/python3",
            "-I",
            "-B",
            "Stage1_Instances/THM-M-0387/check_intake.py",
        )
        in validator_argvs,
        "successful scheduler-owned validator command is missing",
    )
    require(receipt["audit_complete"] is receipt["theorem_complete"] is False, "receipt terminal overclaim")
    inputs = receipt["inputs"]
    require(inputs["dependency_context_sha256"] == CONTEXT_SHA256, "receipt context drift")
    require(inputs["phase_contract_sha256"] == CONTRACT_SHA256, "receipt contract drift")
    require(inputs["accepted_receipt_ids"] == [] and inputs["parent_inspection_order"] == [], "receipt imports acceptance")
    require(inputs["provider_acceptance_inherited"] is False, "receipt inherits provider acceptance")
    require(inputs["task_state_authority"]["path"] == "Docs/Stage1_Blueprint_v2.md", "task authority path drift")
    require(inputs["task_state_authority"]["item_state_observed"] == "[_]", "receipt state observation drift")
    require(SHA256_RE.fullmatch(inputs["task_state_authority"]["sha256"]) is not None, "base blueprint hash malformed")
    require(SHA256_RE.fullmatch(inputs["theorem_dag_sha256"]) is not None, "base DAG hash malformed")
    require_stable_provenance_consistency(instance, receipt, ledger)
    require_nonempty_strings(receipt["known_failures"], "receipt known failures are empty")
    require(
        isinstance(receipt["retry_condition"], str) and bool(receipt["retry_condition"].strip()),
        "receipt retry condition is empty",
    )
    require(
        isinstance(receipt["status_boundary"], str) and bool(receipt["status_boundary"].strip()),
        "receipt status boundary is empty",
    )
    require_nonempty_strings(
        receipt["invalidation_inputs"], "receipt invalidation inputs are empty"
    )

    bindings = receipt["artifact_bindings"]
    require(set(bindings) == set(ROLE_PATHS), "receipt role bindings are incomplete")
    for role, relative in ROLE_PATHS.items():
        binding = bindings[role]
        require(binding["role"] == role and binding["path"] == relative, f"receipt role path drift: {role}")
        if role == "phase_receipt":
            require(binding["sha256"] == binding["git_blob"] == "self_referential_excluded", "receipt self-binding drift")
        else:
            require(binding["sha256"] == sha256(relative), f"receipt role hash drift: {role}")
            require(binding["git_blob"] == git_blob(relative), f"receipt role blob drift: {role}")

    for relative in {
        *ROLE_PATHS.values(),
        "Stage1_Instances/THM-M-0387/check_intake.py",
        "Stage1_Instances/THM-M-0387/dependency-reuse-ledger.json",
    }:
        data = (ROOT / relative).read_bytes()
        require(data.endswith(b"\n"), f"missing final newline: {relative}")
        require(b"\r" not in data and b"\x00" not in data, f"invalid byte: {relative}")
        require(all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), f"trailing whitespace: {relative}")


def main() -> None:
    try:
        check()
    except Exception as error:
        result = {
            "schema_version": "stage1-validator-semantic-result/1.0",
            "item_id": ITEM_ID,
            "theorem_id": THEOREM_ID,
            "phase": "intake",
            "status": "failed",
            "verdict": "repair_required",
            "phase_accepted": False,
            "audit_complete": False,
            "theorem_complete": False,
            "phase_predicate_proven": False,
            "first_failed_gate": "S56-M-0387-INTAKE.validator",
            "open_obligations": 1,
            "stale_inputs": [],
            "blocked": False,
            "message": f"Intake evidence failed closed: {error}",
        }
    else:
        result = {
            "schema_version": "stage1-validator-semantic-result/1.0",
            "item_id": ITEM_ID,
            "theorem_id": THEOREM_ID,
            "phase": "intake",
            "status": "passed",
            "verdict": "phase_accepted",
            "phase_accepted": True,
            "audit_complete": False,
            "theorem_complete": False,
            "phase_predicate_proven": True,
            "first_failed_gate": None,
            "open_obligations": 0,
            "stale_inputs": [],
            "blocked": False,
            "message": "Complete planned FLT intake and empty hard-parent closure passed.",
        }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
