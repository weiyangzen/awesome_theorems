#!/usr/bin/env python3
"""Validate the fail-closed statement packet for THM-M-0570."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import traceback
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0570"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0570-STATEMENT"
THEOREM_ID = "THM-M-0570"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
CONTRACT_GIT_BLOB = "84b92df9eaf457ab954b652c3f20f4d513cf0a88"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_AUTHORITY_SHA256 = {
    "Docs/Stage1_Blueprint_v2.md": "fb6cd286dc5c47e22d754ab73e5162986e98a18b5bc6d8e7213ae5d39b4256d1",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "skills/execute-stage1-rev56/SKILL.md": "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_OWNED_SHA256 = {
    "Statement.lean": "b37906b2a9aaf62983464e2056ccf76cfaaae82b081541e318429f3dedda239c",
    "dependency-reuse-ledger.json": "0aad7e7503440a295fef08f33596892b776f9f25a4ac1b59088890bfac554e02",
    "statement.json": "64a1ebb50556ccb1f6f8a3c928e831d90973ad8c309f21f740820c9504ad66c2",
    "source-statement-crosswalk.md": "6265a5cd3d7f553027720053d727592e9bfd8fde5395916a3c63d15c8006a551",
    "instance.json": "e6098fd59a6e2ff1d64c29311f231756c5030faa5d5c74bc3d77be544f57ef2e",
    "statement-blocker.md": "dcd375c24a2c3d9d0f3b2fda0f2f4458e1f0bc3d87639a42f7a84e4b735dd511",
}
REQUIRED_RECEIPT_POINTERS = (
    "/schema_version",
    "/receipt_id",
    "/item_id",
    "/theorem_id",
    "/phase",
    "/intent",
    "/base_revision",
    "/base_tree",
    "/inputs",
    "/support_state",
    "/proposed_state",
    "/accepted",
    "/verdict",
    "/selftest_status",
    "/selftest_result/exit_code",
    "/selftest_result/commands",
    "/known_failures",
    "/first_failed_gate",
    "/retry_condition",
    "/status_boundary",
    "/audit_complete",
    "/theorem_complete",
    "/invalidation_inputs",
    "/statement_fingerprints",
    "/mutation_tests",
)
EXPECTED_CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0570/Statement.lean",
    "Stage1_Instances/THM-M-0570/check_statement.py",
    "Stage1_Instances/THM-M-0570/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0570/statement-blocker.json",
    "Stage1_Instances/THM-M-0570/statement-blocker.md",
    "Stage1_Instances/THM-M-0570/statement-receipt.json",
    "Stage1_Instances/THM-M-0570/statement.json",
}
SEMANTIC_RESULT = {
    "schema_version": "stage1-validator-semantic-result/1.0",
    "item_id": ITEM_ID,
    "theorem_id": THEOREM_ID,
    "phase": "statement",
    "status": "blocked",
    "verdict": "blocked",
    "phase_accepted": False,
    "audit_complete": False,
    "theorem_complete": False,
    "phase_predicate_proven": False,
    "first_failed_gate": "S02-EXACT-TARGET.primary_source_and_variant_selection",
    "open_obligations": 5,
    "stale_inputs": [],
    "blocked": True,
    "message": (
        "The repository does not select one exact proposition for the heat-kernel "
        "proof of the index theorem; the content-bound blocker is internally consistent."
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r} in {path}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object in {path}")
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
        check=False,
    )
    if result.returncode:
        raise ValueError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def pointer(document: dict[str, Any], raw: str) -> Any:
    value: Any = document
    for component in raw.removeprefix("/").split("/"):
        if not isinstance(value, dict) or component not in value:
            raise ValueError(f"missing JSON pointer {raw}")
        value = value[component]
    return value


def lean_source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    in_string = False
    while index < len(source):
        if depth:
            if source.startswith("/-", index):
                depth += 1
                index += 2
            elif source.startswith("-/", index):
                depth -= 1
                index += 2
            else:
                index += 1
        elif in_string:
            if source[index] == "\\" and index + 1 < len(source):
                index += 2
            elif source[index] == '"':
                in_string = False
                index += 1
            else:
                index += 1
        elif source.startswith("/-", index):
            depth = 1
            index += 2
        elif source.startswith("--", index):
            end = source.find("\n", index)
            index = len(source) if end < 0 else end
        elif source[index] == '"':
            in_string = True
            index += 1
        else:
            output.append(source[index])
            index += 1
    if depth or in_string:
        raise ValueError("unterminated Lean comment or string")
    return "".join(output)


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "TZ": "UTC"})
    return subprocess.run(
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
        check=False,
    )


def validate_authority() -> None:
    if sys.flags.optimize != 0:
        raise ValueError("validator must run without Python optimization")
    if git("rev-parse", "HEAD") != BASE_REVISION:
        raise ValueError("repository HEAD differs from worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("repository base tree differs from receipt")
    for relative, expected in EXPECTED_AUTHORITY_SHA256.items():
        if sha256(ROOT / relative) != expected:
            raise ValueError(f"authority input changed: {relative}")
    for relative, expected in EXPECTED_OWNED_SHA256.items():
        if sha256(HERE / relative) != expected:
            raise ValueError(f"target-owned input changed: {relative}")

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    rows = [
        row
        for row in blueprint.splitlines()
        if f"`{ITEM_ID}`" in row and row.startswith("- ")
    ]
    if len(rows) != 1 or not rows[0].startswith("- [ ]") or "{attempts=0}" not in rows[0]:
        raise ValueError("authoritative statement row or attempts changed")
    line_number = blueprint[: blueprint.index(rows[0])].count("\n") + 1
    if line_number != 2239:
        raise ValueError("authoritative statement row moved unexpectedly")

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    if target["execution_rank"] != 113 or target["lifecycle_mode"] != "planned":
        raise ValueError("target manifest identity or lifecycle changed")
    if target["legacy_artifacts_accepted"] is not False or target["theorem_complete"] is not False:
        raise ValueError("legacy or theorem state unexpectedly acquired acceptance")

    dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    if node["v2_execution_rank"] != 329 or node["topological_layer"] != 0:
        raise ValueError("v2 claim order changed")
    if node["phase_states"]["statement"] != "[ ]" or node["phase_attempts"]["statement"] != 0:
        raise ValueError("v2 statement state or attempt changed")
    if node["dependency_context_sha256"] != CONTEXT_SHA256:
        raise ValueError("dependency context changed")
    for key in (
        "direct_hard_parents",
        "transitive_hard_ancestors",
        "direct_reuse_hint_ids",
        "shared_lemma_group_ids",
    ):
        if node[key] != []:
            raise ValueError(f"declared empty dependency field changed: {key}")

    contract_path = ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json"
    contract = load(contract_path)
    if git("hash-object", str(contract_path)) != CONTRACT_GIT_BLOB:
        raise ValueError("phase contract Git blob changed")
    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    if phase["intent"] != "audit" or phase["raw_blocked_can_close_phase"] is not False:
        raise ValueError("statement negative boundary changed")
    if phase["classified_negative_findings_may_satisfy_deliverable"] is not False:
        raise ValueError("negative findings unexpectedly became phase-completing")
    if tuple(phase["phase_receipt_required_fields"]) != REQUIRED_RECEIPT_POINTERS:
        raise ValueError("statement receipt contract changed")
    expected_roles = {
        "statement_record": "Stage1_Instances/THM-M-0570/statement.json",
        "statement_source": "Stage1_Instances/THM-M-0570/Statement.lean",
        "source_crosswalk": "Stage1_Instances/THM-M-0570/source-statement-crosswalk.md",
        "phase_receipt": "Stage1_Instances/THM-M-0570/statement-receipt.json",
    }
    for role in phase["required_artifact_roles"]:
        candidates = [path.format(theorem_id=THEOREM_ID) for path in role["path_candidates"]]
        if expected_roles[role["role"]] not in candidates:
            raise ValueError(f"required role path changed: {role['role']}")
        if sum((ROOT / path).is_file() for path in candidates) != 1:
            raise ValueError(f"required role is missing or ambiguous: {role['role']}")
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    if validators != ["Stage1_Instances/THM-M-0570/check_statement.py"]:
        raise ValueError("validator candidate selection is not exactly one worktree path")


def validate_ledger_and_statement() -> None:
    instance = load(HERE / "instance.json")
    if instance["item_id"] != "S56-M-0570-INTAKE" or instance["lifecycle"] != "planned":
        raise ValueError("intake identity or lifecycle changed")
    if instance["canonical_claim_status"] != "blocked_on_primary_source_and_variant_selection":
        raise ValueError("intake no longer preserves the statement blocker")
    if instance["canonical_claim"] is not None:
        raise ValueError("intake unexpectedly supplies a canonical claim")
    if instance["root_vector"] != {"H": "H2", "M": "M4", "R": "R4"}:
        raise ValueError("intake debt vector changed")
    if instance["audit_complete"] is not False or instance["theorem_complete"] is not False:
        raise ValueError("intake falsely closes a terminal decision")

    ledger = load(HERE / "dependency-reuse-ledger.json")
    if ledger["schema_version"] != "stage1-dependency-reuse-ledger/1.1":
        raise ValueError("dependency ledger schema changed")
    if ledger["consumer_theorem_id"] != THEOREM_ID:
        raise ValueError("dependency ledger owner changed")
    if ledger["observed_theorem_dag_sha256"] != GRAPH_SHA256:
        raise ValueError("dependency ledger graph binding changed")
    if ledger["dependency_context_sha256"] != CONTEXT_SHA256:
        raise ValueError("dependency ledger context binding changed")
    if ledger["repository_revision"] != BASE_REVISION:
        raise ValueError("dependency ledger base changed")
    for key in (
        "direct_parent_ids",
        "transitive_ancestor_ids",
        "hard_edge_ids",
        "reuse_hint_ids",
        "shared_group_ids",
        "inspections",
        "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        if ledger[key] != []:
            raise ValueError(f"empty dependency ledger field changed: {key}")
    closure = ledger["closure_audit"]
    if closure["parent_inspection_order"] != [] or closure["status"] != "empty_closure_inspected":
        raise ValueError("empty parent closure was not audited exactly once")
    if closure["claim_order"] != {
        "v2_execution_rank": 329,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        raise ValueError("claim order binding changed")
    if closure["provider_acceptance_inherited"] is not False:
        raise ValueError("dependency ledger transfers provider acceptance")

    statement = load(HERE / "statement.json")
    if statement["schema_version"] != "stage1-statement/1.0":
        raise ValueError("statement schema changed")
    if statement["item_id"] != ITEM_ID or statement["theorem_id"] != THEOREM_ID:
        raise ValueError("statement identity changed")
    if statement["canonical_statement"] is not None:
        raise ValueError("a canonical human statement was invented")
    formal = statement["canonical_formal_target"]
    for field in (
        "declaration_or_expression",
        "elaborated_expression_sha256",
        "environment_fingerprint",
        "unresolved_metavariables",
    ):
        if formal[field] is not None:
            raise ValueError(f"a canonical formal target field was invented: {field}")
    if statement["direct_imports"] != [] or statement["statement_fingerprints"] != []:
        raise ValueError("statement record invents imports or fingerprints")
    if statement["checked_alternate_encodings"] != []:
        raise ValueError("statement record invents a checked transport")
    expected_mutations = {
        "removed_hypothesis": "not_run_no_canonical_target",
        "changed_domain": "not_run_no_canonical_target",
        "changed_binder_scope": "not_run_no_canonical_target",
        "boundary_case": "not_run_no_canonical_target",
    }
    if statement["mutation_tests"] != expected_mutations:
        raise ValueError("statement mutation blocker boundary changed")
    for field in (
        "statement_elaborated",
        "phase_predicate_proven",
        "phase_accepted",
        "theorem_proved",
        "audit_complete",
        "theorem_complete",
    ):
        if statement[field] is not False:
            raise ValueError(f"statement record falsely claims {field}")

    source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    code = lean_source_without_comments(source)
    prohibited = re.compile(
        r"^\s*(?:import|theorem|lemma|def|abbrev|structure|class|instance|axiom|constant|"
        r"opaque|unsafe|extern)\b|\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b",
        re.MULTILINE,
    )
    if prohibited.search(code):
        raise ValueError("declaration-free boundary contains an import or prohibited construct")
    source_result = run_lean(HERE / "Statement.lean")
    if source_result.returncode or source_result.stdout or source_result.stderr:
        raise ValueError("declaration-free statement boundary did not elaborate silently")

    legacy_path = LEAN_ROOT / "AwesomeTheorems" / "Stage1" / "S1_M_113.lean"
    if sha256(legacy_path) != "ee6fd72f6b3f5eb00a2d55addfe783befeed55f6632ee7da27314d05b9d19324":
        raise ValueError("legacy discovery module changed")
    legacy = legacy_path.read_text(encoding="utf-8")
    for marker in (
        "structure HeatKernelIndexData",
        "def HeatKernelIndexFormula",
        "def StatementShape",
        "remain\nabstract",
        "statement-shape candidate",
    ):
        if marker not in legacy:
            raise ValueError(f"legacy non-credit boundary lost marker: {marker}")
    legacy_result = run_lean(legacy_path)
    if legacy_result.returncode:
        raise ValueError("legacy discovery module no longer elaborates")

    version = subprocess.run(
        ["lake", "env", "lean", "--version"],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
        check=False,
    )
    if version.returncode or LEAN_COMMIT not in version.stdout:
        raise ValueError("pinned Lean identity changed")
    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    if git("rev-parse", "HEAD", cwd=mathlib) != MATHLIB_REVISION:
        raise ValueError("pinned mathlib revision changed")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != MATHLIB_TREE:
        raise ValueError("pinned mathlib tree changed")
    if git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) != "":
        raise ValueError("pinned mathlib worktree is dirty")


def validate_receipt_and_handoff() -> None:
    blocker = load(HERE / "statement-blocker.json")
    receipt = load(HERE / "statement-receipt.json")
    for raw in REQUIRED_RECEIPT_POINTERS:
        pointer(receipt, raw)
    if blocker["item_id"] != ITEM_ID or blocker["theorem_id"] != THEOREM_ID:
        raise ValueError("blocker identity changed")
    if blocker["base_revision"] != BASE_REVISION or blocker["base_tree"] != BASE_TREE:
        raise ValueError("blocker base changed")
    if blocker["first_failed_gate"] != SEMANTIC_RESULT["first_failed_gate"]:
        raise ValueError("blocker first failed gate changed")
    if blocker["dependency_reuse_context"]["parent_inspection_order"] != []:
        raise ValueError("blocker parent inspection order changed")
    if blocker["dependency_reuse_context"]["provider_acceptance_inherited"] is not False:
        raise ValueError("blocker transfers provider acceptance")
    for field in (
        "accepted",
        "statement_gate_passed",
        "statement_elaborated",
        "phase_predicate_proven",
        "phase_accepted",
        "theorem_proved",
        "audit_complete",
        "theorem_complete",
    ):
        if blocker[field] is not False:
            raise ValueError(f"blocker falsely claims {field}")

    if receipt["schema_version"] != "stage1-node-receipt/1.0":
        raise ValueError("receipt schema changed")
    if (receipt["item_id"], receipt["theorem_id"], receipt["phase"], receipt["intent"]) != (
        ITEM_ID,
        THEOREM_ID,
        "statement",
        "audit",
    ):
        raise ValueError("receipt identity changed")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        raise ValueError("receipt base changed")
    if receipt["support_state"] != "provisional_worker_selftest":
        raise ValueError("receipt support state changed")
    if receipt["proposed_state"] != "[_]" or receipt["selftest_status"] != "passed":
        raise ValueError("receipt does not preserve worker self-test state")
    if receipt["verdict"] != "blocked" or receipt["worker_verdict"] != "blocked":
        raise ValueError("receipt loses blocked worker verdict")
    for field in (
        "accepted",
        "phase_predicate_proven",
        "phase_accepted",
        "statement_elaborated",
        "audit_complete",
        "theorem_complete",
    ):
        if receipt[field] is not False:
            raise ValueError(f"receipt falsely claims {field}")
    if receipt["statement_fingerprints"] != []:
        raise ValueError("receipt invents a statement fingerprint")
    if receipt["first_failed_gate"] != SEMANTIC_RESULT["first_failed_gate"]:
        raise ValueError("receipt first failed gate changed")
    if receipt["selftest_result"]["exit_code"] != 0:
        raise ValueError("receipt self-test exit changed")
    if not receipt["selftest_result"]["commands"]:
        raise ValueError("receipt has no self-test commands")

    selected = {row["role"]: row for row in receipt["selected_artifacts"]}
    if set(selected) != {
        "statement_record",
        "statement_source",
        "source_crosswalk",
        "phase_receipt",
    }:
        raise ValueError("selected artifact roles changed")
    for role in ("statement_record", "statement_source", "source_crosswalk"):
        binding = selected[role]
        path = ROOT / binding["path"]
        if binding["sha256"] != sha256(path):
            raise ValueError(f"selected artifact SHA-256 is stale: {role}")
        if binding["git_blob"] != git("hash-object", str(path)):
            raise ValueError(f"selected artifact Git blob is stale: {role}")
    self_binding = selected["phase_receipt"]
    if self_binding["sha256"] is not None or self_binding["git_blob"] is not None:
        raise ValueError("receipt recursively binds its own bytes")
    for name in (
        "task_state_authority",
        "assurance_authority",
        "phase_contract",
        "target_manifest",
        "theorem_dag",
        "execution_skill",
        "statement_record",
        "statement_source",
        "source_crosswalk",
        "dependency_ledger",
        "blocker_record",
        "readable_blocker",
        "phase_validator",
    ):
        binding = receipt["inputs"][name]
        path = ROOT / binding["path"]
        if sha256(path) != binding["sha256"]:
            raise ValueError(f"receipt input SHA-256 is stale: {name}")
        if git("hash-object", str(path)) != binding["git_blob"]:
            raise ValueError(f"receipt input Git blob is stale: {name}")
    if receipt["inputs"]["parent_inspection_order"] != []:
        raise ValueError("receipt parent inspection order changed")
    if receipt["inputs"]["provider_acceptance_inherited"] is not False:
        raise ValueError("receipt transfers provider acceptance")
    validator_binding = receipt["validator_binding"]
    validator_path = ROOT / validator_binding["path"]
    if validator_path.resolve() != Path(__file__).resolve():
        raise ValueError("receipt binds a different phase validator")
    if validator_binding["sha256"] != sha256(validator_path):
        raise ValueError("validator SHA-256 binding is stale")
    if validator_binding["git_blob"] != git("hash-object", str(validator_path)):
        raise ValueError("validator Git blob binding is stale")
    if validator_binding["worker_base_tracking_state"] != "not_present_at_worker_base":
        raise ValueError("validator base-tracking boundary changed")

    packet = load(ROOT / ".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id",
        "worker_verdict",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }:
        raise ValueError("worker self-test packet schema changed")
    if packet["item_id"] != ITEM_ID or packet["worker_verdict"] != "blocked":
        raise ValueError("worker self-test packet identity changed")
    if packet["base_revision"] != BASE_REVISION or packet["state"] != "[_]":
        raise ValueError("worker self-test packet state changed")
    if set(packet["changed_paths"]) != EXPECTED_CHANGED_PATHS:
        raise ValueError("worker self-test changed-path inventory changed")
    if packet["commands"] != receipt["commands"]:
        raise ValueError("worker commands differ from receipt")
    if packet["known_failures"] != receipt["known_failures"]:
        raise ValueError("worker failures differ from receipt")
    if packet["output_summary"] != receipt["output_summary"]:
        raise ValueError("worker output summary differs from receipt")
    if receipt["changed_paths"] != packet["changed_paths"]:
        raise ValueError("receipt and worker changed paths differ")

    for relative in EXPECTED_CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            raise ValueError(f"noncanonical file bytes: {relative}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            raise ValueError(f"trailing whitespace: {relative}")


def validate() -> None:
    validate_authority()
    validate_ledger_and_statement()
    validate_receipt_and_handoff()


def main() -> None:
    try:
        validate()
    except Exception as exc:
        traceback.print_exc(file=sys.stderr)
        failure = dict(SEMANTIC_RESULT)
        failure.update(
            {
                "status": "failed",
                "verdict": "repair_required",
                "first_failed_gate": "VALIDATOR-INTERNAL-CONSISTENCY",
                "blocked": False,
                "message": f"Validator consistency failure: {type(exc).__name__}: {exc}",
            }
        )
        print(json.dumps(failure, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    print(json.dumps(SEMANTIC_RESULT, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
