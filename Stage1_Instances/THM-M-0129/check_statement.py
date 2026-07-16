#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0129 statement packet."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_DIR = ROOT / "Formalizations" / "Lean"
THEOREM_ID = "THM-M-0129"
ITEM_ID = "S56-M-0129-STATEMENT"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0129/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0129/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0129/source_statement_crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0129/statement-receipt.json",
}
EXPECTED_IMPORTS = (
    "Mathlib.NumberTheory.ModularForms.Basic",
    "Mathlib.NumberTheory.DirichletCharacter.Basic",
)
INFRASTRUCTURE_PATH = "Stage1_Instances/THM-M-0129/StatementInfrastructure.lean"
INTEGRATED_SOURCE_RECHECK_PATH = (
    "Stage1_Instances/THM-M-0129/statement-recheck-2026-07-16-head-6bf9ee93-slot76.json"
)
INTEGRATED_SOURCE_RECHECK_SHA256 = (
    "1045ecae4dab3b0cf5e2cf5ef203a8ff61331571464ba2b55188c48eb89ddf32"
)
EXPECTED_NATIVE_CHECKS = (
    "CuspForm",
    "DirichletCharacter",
    "DirichletCharacter.conductor",
)
EXPECTED_MISSING_CHECKS = (
    "HalfIntegralWeightModularForm",
    "ShimuraLift",
    "ShimuraCorrespondence",
)
PROHIBITED = re.compile(
    r"\b(sorry|admit|sorryAx|axiom|constant|opaque|unsafe|implemented_by|native_decide)\b"
)


def load(relative: str) -> dict:
    value = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    assert isinstance(value, dict), f"{relative} must contain one JSON object"
    return value


def sha256(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def git_blob(relative: str) -> str:
    data = (ROOT / relative).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
    ).strip()


def fresh_theorem_dag() -> dict:
    generator = ROOT / "Docs/tools/generate_stage1_theorem_dag_v2.py"
    spec = importlib.util.spec_from_file_location("thm_m_0129_dag_generator", generator)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    value = module.build()
    assert isinstance(value, dict)
    return value


def check() -> None:
    manifest = load("Docs/Stage1_Targets_rev-5.6.json")
    theorem_dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")
    statement = load(ROLE_PATHS["statement_record"])
    receipt = load(ROLE_PATHS["phase_receipt"])
    ledger = load("Stage1_Instances/THM-M-0129/dependency-reuse-ledger.json")
    base_revision = receipt["base_revision"]
    base_tree = receipt["base_tree"]
    assert isinstance(base_revision, str) and re.fullmatch(r"[0-9a-f]{40}", base_revision)
    assert isinstance(base_tree, str) and re.fullmatch(r"[0-9a-f]{40}", base_tree)

    target = next(row for row in manifest["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 47
    assert target["name"] == "志村提升定理"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned"
    assert target["theorem_complete"] is False

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    blueprint_lines = blueprint.splitlines()
    statement_rows = [
        (index, line)
        for index, line in enumerate(blueprint_lines)
        if line.startswith("- ") and f"`{ITEM_ID}`" in line
    ]
    assert len(statement_rows) == 1
    row_index, statement_row = statement_rows[0]
    observed_state = receipt["inputs"]["task_state_authority"]["item_state_observed"]
    observed_attempts = receipt["inputs"]["task_state_authority"]["attempts_observed"]
    assert observed_state in {"[ ]", "[_]"}
    assert isinstance(observed_attempts, int) and observed_attempts >= 0
    assert statement_row.startswith(f"- {observed_state} ")
    assert f"{{attempts={observed_attempts}}}" in statement_row
    assert "Depends: `S56-M-0129-INTAKE`." in blueprint_lines[row_index + 1]

    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    assert node["v2_execution_rank"] == 281 and node["topological_layer"] == 0
    assert node["phase_states"]["intake"] == receipt["inputs"]["task_state_authority"][
        "prerequisite_state_observed"
    ]
    assert node["phase_states"]["statement"] == observed_state
    assert node["phase_attempts"]["statement"] == observed_attempts
    assert node["direct_hard_parents"] == []
    assert node["transitive_hard_ancestors"] == []
    assert node["direct_reuse_hint_ids"] == []
    assert node["shared_lemma_group_ids"] == []
    graph_sha256 = sha256("Docs/Stage1_Theorem_DAG_v2.json")
    context_sha256 = node["dependency_context_sha256"]
    assert re.fullmatch(r"[0-9a-f]{64}", context_sha256)

    regenerated = fresh_theorem_dag()
    old_rows = {row["theorem_id"]: row for row in theorem_dag["theorems"]}
    new_rows = {row["theorem_id"]: row for row in regenerated["theorems"]}
    assert [key for key in old_rows if old_rows[key] != new_rows[key]] == [THEOREM_ID]
    old_target = dict(old_rows[THEOREM_ID])
    new_target = dict(new_rows[THEOREM_ID])
    old_target.pop("evidence_inventory")
    old_target.pop("reusable_artifacts")
    new_target.pop("evidence_inventory")
    new_target.pop("reusable_artifacts")
    assert old_target == new_target
    assert {
        key: value for key, value in theorem_dag.items() if key != "theorems"
    } == {key: value for key, value in regenerated.items() if key != "theorems"}

    phase_contract = next(row for row in contract["phases"] if row["phase"] == "statement")
    assert contract["schema_version"] == "stage1-phase-acceptance-contracts/1.0"
    assert sha256("Docs/Stage1_Phase_Acceptance_Contracts.json") == CONTRACT_SHA256
    assert contract["artifact_resolution"]["selected_files_must_be_head_tracked"] is True
    assert contract["validator_selection"]["candidate_must_exist_at_worker_base"] is True
    assert contract["validator_selection"]["candidate_head_blob_must_equal_worker_base_blob"] is True
    assert contract["verdict_protocol"]["blocked_policy"] == {
        "raw_blocked_can_close_phase": False,
        "raw_blocked_auto_promotes": False,
        "required_action": "remain_worker_self_tested_and_emit_repair_or_blocker",
    }
    assert phase_contract["intent"] == "audit" and phase_contract["layer"] == 1
    assert phase_contract["raw_blocked_can_close_phase"] is False
    assert phase_contract["classified_negative_findings_may_satisfy_deliverable"] is False
    assert phase_contract["worker_verdicts_eligible_for_review"] == [
        "accepted",
        "no_state_change",
    ]
    selected = {}
    for role in phase_contract["required_artifact_roles"]:
        matches = [
            pattern.format(theorem_id=THEOREM_ID)
            for pattern in role["path_candidates"]
            if (ROOT / pattern.format(theorem_id=THEOREM_ID)).is_file()
        ]
        expected_path = ROLE_PATHS[role["role"]]
        assert expected_path in matches, f"role {role['role']} is missing"
        selected[role["role"]] = expected_path
    assert selected == ROLE_PATHS
    validator_matches = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase_contract["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    assert validator_matches == ["Stage1_Instances/THM-M-0129/check_statement.py"]
    validator_at_base = subprocess.run(
        ["git", "cat-file", "-e", f"{base_revision}:Stage1_Instances/THM-M-0129/check_statement.py"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    assert validator_at_base.returncode != 0

    assert statement["schema_version"] == "stage1-statement/1.0"
    assert statement["item_id"] == ITEM_ID and statement["intent"] == "audit"
    assert statement["canonical_statement_status"] == "blocked_unresolved_source_identity"
    for field in (
        "canonical_human_statement",
        "canonical_formal_target",
        "exact_declaration_or_expression",
        "elaborated_expression_sha256",
        "environment_expression_fingerprint",
        "minimal_direct_imports",
        "fixed_options_namespaces_universes_typeclasses",
    ):
        assert statement[field] is None
    assert statement["credited_alternate_encodings"] == []
    assert statement["first_failed_gate"] == "S02-EXACT-TARGET"
    assert statement["audit_complete"] is statement["theorem_complete"] is False
    assert statement["boundary_probe"] == {
        "contract_role_path": ROLE_PATHS["statement_source"],
        "contract_role_behavior": (
            "Elaborates with the adjacent-interface imports but deliberately declares no canonical target."
        ),
        "infrastructure_probe_path": INFRASTRUCTURE_PATH,
        "infrastructure_probe_behavior": (
            "Checks three available adjacent interfaces and three expected-missing topic identifiers "
            "in the pinned closure."
        ),
        "direct_imports": list(EXPECTED_IMPORTS),
        "credit_boundary": (
            "These imports are minimal only for the adjacent-interface probe. They are not claimed "
            "minimal for the absent canonical target, and the probe declares no Shimura-lifting "
            "proposition."
        ),
    }
    assert statement["dependency_context"] == {
        "observed_theorem_dag_sha256": graph_sha256,
        "dependency_context_sha256": context_sha256,
        "parent_inspection_order": [],
        "direct_parent_ids": [],
        "transitive_ancestor_ids": [],
        "hard_edge_ids": [],
        "reuse_hint_ids": [],
        "shared_group_ids": [],
        "provider_acceptance_inherited": False,
    }
    expected_mutations = {
        "removed_hypothesis": "not_executable_without_an_accepted_canonical_target",
        "changed_domain": "not_executable_without_an_accepted_canonical_target",
        "changed_binder_scope": "not_executable_without_an_accepted_canonical_target",
        "boundary_case": "not_executable_without_an_accepted_canonical_target",
    }
    assert statement["mutation_tests"] == expected_mutations

    integrated_recheck = load(INTEGRATED_SOURCE_RECHECK_PATH)
    assert sha256(INTEGRATED_SOURCE_RECHECK_PATH) == INTEGRATED_SOURCE_RECHECK_SHA256
    assert integrated_recheck["verdict"] == "blocked"
    assert integrated_recheck["canonical_human_statement"] is None
    assert integrated_recheck["canonical_formal_target"] is None
    assert integrated_recheck["source_boundary"]["discovery_scan_sha256"] == (
        "78105f883d5a6646110de8a819d42d051f1f3a2ba221ac8cfb6ab8773bcc64f4"
    )
    assert integrated_recheck["source_boundary"]["printed_pages_457_459_text_sha256"] == (
        "1627c70197fc5f43c018574c683fa0d6874a86088500cfd9472112be3741dba8"
    )
    assert "silently conjoining them invents a new root" in integrated_recheck["reason"]

    assert ledger == {
        "schema_version": "stage1-dependency-reuse-ledger/1.1",
        "consumer_theorem_id": THEOREM_ID,
        "observed_theorem_dag_sha256": graph_sha256,
        "dependency_context_sha256": context_sha256,
        "repository_revision": base_revision,
        "direct_parent_ids": [],
        "transitive_ancestor_ids": [],
        "hard_edge_ids": [],
        "reuse_hint_ids": [],
        "shared_group_ids": [],
        "inspections": [],
        "reuse_decisions": [],
        "unresolved_compatibility_obligations": [],
    }

    required_receipt_fields = {
        pointer.split("/")[-1]
        for pointer in phase_contract["phase_receipt_required_fields"]
        if pointer.count("/") == 1
    }
    assert required_receipt_fields <= set(receipt)
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == "statement" and receipt["intent"] == "audit"
    assert git("rev-parse", "HEAD") == base_revision
    assert git("rev-parse", "HEAD^{tree}") == base_tree
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked"
    assert receipt["phase_accepted"] is receipt["phase_predicate_proven"] is False
    assert receipt["selftest_status"] == "passed"
    assert receipt["selftest_result"]["exit_code"] == 0
    assert receipt["selftest_result"]["commands"]
    assert receipt["first_failed_gate"] == "S02-EXACT-TARGET"
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["statement_fingerprints"] == []
    assert receipt["mutation_tests"] == expected_mutations
    assert receipt["known_failures"] and receipt["retry_condition"]
    assert any("not present at the immutable base" in row for row in receipt["known_failures"])
    assert receipt["status_boundary"] and receipt["invalidation_inputs"]
    assert receipt["inputs"]["theorem_dag"]["sha256"] == graph_sha256
    assert receipt["inputs"]["dependency_context_sha256"] == context_sha256
    assert receipt["inputs"]["parent_inspection_order"] == []
    assert receipt["inputs"]["task_state_authority"]["prerequisite_state_observed"] == "[_]"
    assert receipt["status_boundary"].startswith(
        "Fresh target-owned, worker-self-tested negative statement packet only."
    )
    authoritative_commands = receipt["selftest_result"]["commands"]
    assert any(
        row.get("argv")
        == [
            "/usr/bin/python3",
            "-I",
            "-B",
            "Stage1_Instances/THM-M-0129/check_statement.py",
        ]
        and row.get("exit_code") == 0
        and row.get("semantic_result") == "blocked"
        for row in authoritative_commands
    )
    assert any(
        row.get("argv")
        == [
            "lake",
            "env",
            "lean",
            "../../Stage1_Instances/THM-M-0129/Statement.lean",
        ]
        and row.get("exit_code") == 0
        and row.get("result")
        == "the contract-selected role file elaborates with no declarations and no canonical target credit"
        for row in authoritative_commands
    )

    for role, relative in ROLE_PATHS.items():
        binding = receipt["artifact_bindings"][role]
        assert binding["role"] == role and binding["path"] == relative
        if role == "phase_receipt":
            assert binding["sha256"] == "self_referential_excluded"
            assert binding["git_blob"] == "self_referential_excluded"
        else:
            assert binding["sha256"] == sha256(relative)
            assert binding["git_blob"] == git_blob(relative)

    source = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    assert tuple(re.findall(r"^import ([^\s]+)$", source, re.MULTILINE)) == EXPECTED_IMPORTS
    code = re.sub(r"/-.*?-\/", "", source, flags=re.DOTALL)
    code = re.sub(r"--.*", "", code)
    assert re.search(r"^(theorem|lemma|def|axiom|constant|opaque)\b", code, re.MULTILINE) is None
    assert PROHIBITED.search(code) is None

    statement_lean = subprocess.run(
        ["lake", "env", "lean", str(ROOT / ROLE_PATHS["statement_source"])],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    assert statement_lean.returncode == 0, statement_lean.stdout
    assert not [
        line
        for line in statement_lean.stdout.splitlines()
        if not line.startswith("Failed to create stream fd:")
    ]

    infrastructure = (ROOT / INFRASTRUCTURE_PATH).read_text(encoding="utf-8")
    assert tuple(re.findall(r"^import ([^\s]+)$", infrastructure, re.MULTILINE)) == EXPECTED_IMPORTS
    for name in EXPECTED_NATIVE_CHECKS:
        assert len(re.findall(rf"^#check {re.escape(name)}$", infrastructure, re.MULTILINE)) == 1
    for name in EXPECTED_MISSING_CHECKS:
        assert len(
            re.findall(rf"^#check_failure {re.escape(name)}$", infrastructure, re.MULTILINE)
        ) == 1
    probe = subprocess.run(
        ["lake", "env", "lean", str(ROOT / INFRASTRUCTURE_PATH)],
        cwd=LEAN_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    assert probe.returncode == 0, probe.stdout
    lines = [
        line
        for line in probe.stdout.splitlines()
        if not line.startswith("Failed to create stream fd:")
    ]
    assert len(lines) == 6
    for name in EXPECTED_NATIVE_CHECKS:
        assert any(line.startswith(name) for line in lines)
    for name in EXPECTED_MISSING_CHECKS:
        assert lines.count(f"Unknown identifier `{name}`") == 1

    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    assert "10.2307/1970831" in crosswalk
    assert "not vendored" in crosswalk
    assert "No exact canonical Lean proposition" in crosswalk
    worker_packet = load(".stage1-worker-selftest.json")
    assert worker_packet["item_id"] == ITEM_ID and worker_packet["state"] == "[_]"
    assert worker_packet["base_revision"] == base_revision
    assert worker_packet["worker_verdict"] == receipt["verdict"] == "blocked"
    assert worker_packet["commands"] == receipt["selftest_result"]["commands"]
    assert worker_packet["known_failures"] == receipt["known_failures"]
    assert worker_packet["output_summary"]
    assert worker_packet["status_boundary"]
    assert worker_packet["status_boundary"].startswith(
        "Worker-self-tested negative packet only."
    )
    assert all(
        row.get("expected_failure")
        == (
            "new target-owned Lean, receipt, and structured-record inventory changes only THM-M-0129 "
            "evidence_inventory/reusable_artifacts; master integration must regenerate the checked-in "
            "theorem-DAG projection"
        )
        for row in worker_packet["commands"][:2]
    )
    expected_changed = {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0129/Statement.lean",
        "Stage1_Instances/THM-M-0129/check_statement.py",
        "Stage1_Instances/THM-M-0129/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0129/source_statement_crosswalk.md",
        "Stage1_Instances/THM-M-0129/statement-head-blocker-dae195160907-slot67.md",
        "Stage1_Instances/THM-M-0129/statement-receipt.json",
        "Stage1_Instances/THM-M-0129/statement.json",
    }
    assert set(worker_packet["changed_paths"]) == expected_changed
    tracked_changes = set(
        git(
            "diff",
            "--name-only",
            "--",
            "Stage1_Instances/THM-M-0129",
            ".stage1-worker-selftest.json",
        ).splitlines()
    )
    untracked_changes = set(
        git(
            "ls-files",
            "--others",
            "--exclude-standard",
            "--",
            "Stage1_Instances/THM-M-0129",
            ".stage1-worker-selftest.json",
        ).splitlines()
    )
    deleted_changes = set(
        git(
            "diff",
            "--name-only",
            "--diff-filter=D",
            "--",
            "Stage1_Instances/THM-M-0129",
            ".stage1-worker-selftest.json",
        ).splitlines()
    )
    assert tracked_changes | untracked_changes == expected_changed
    assert deleted_changes == set()

    checked_paths = {
        *ROLE_PATHS.values(),
        INFRASTRUCTURE_PATH,
        "Stage1_Instances/THM-M-0129/check_statement.py",
        "Stage1_Instances/THM-M-0129/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0129/statement-head-blocker-dae195160907-slot67.md",
        ".stage1-worker-selftest.json",
    }
    for relative in checked_paths:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n"), f"missing final newline: {relative}"
        assert b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def semantic_result(*, internal_ok: bool, message: str) -> dict:
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "phase": "statement",
        "status": "blocked" if internal_ok else "failed",
        "verdict": "blocked" if internal_ok else "repair_required",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": "S02-EXACT-TARGET" if internal_ok else "S01-ARTIFACTS",
        "open_obligations": 1,
        "stale_inputs": [],
        "blocked": internal_ok,
        "message": message,
    }


def main() -> None:
    try:
        check()
    except Exception as exc:
        result = semantic_result(
            internal_ok=False,
            message=f"statement packet check failed: {type(exc).__name__}: {exc}",
        )
    else:
        result = semantic_result(
            internal_ok=True,
            message=(
                "The negative packet is internally consistent, but no exact canonical Shimura-"
                "lifting target or executable mutation suite exists; the positive statement gate "
                "remains blocked."
            ),
        )
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    if result["status"] == "failed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
