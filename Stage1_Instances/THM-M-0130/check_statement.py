#!/usr/bin/env python3
"""Validate the fail-closed statement packet for THM-M-0130."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import traceback
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0130"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0130-STATEMENT"
THEOREM_ID = "THM-M-0130"
BASE_REVISION = "94009a6bebd743588e09c3b45bfbf18bf9b5c5e3"
BASE_TREE = "daabee9f9b2c6e98d84b6290f78a209b950485fc"
GRAPH_SHA256 = "eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
DIRECT_IMPORT = "Mathlib.AlgebraicGeometry.Scheme"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0130/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0130/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0130/source_statement_crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0130/statement-receipt.json",
}
EXPECTED_INPUTS = {
    "statement_record": (
        "Stage1_Instances/THM-M-0130/statement.json",
        "5f73036920551ab9eaf5e8bb734c76f72e0c286a4aa5ee744cda5834f380f0e0",
        "9277276bcec460062c59d010de0db95be0a397ad",
    ),
    "statement_source": (
        "Stage1_Instances/THM-M-0130/Statement.lean",
        "72d5a1040326613d7a34912ac02325715f3d8345500386cc60eec74065249871",
        "acd453b162db97d5661a5ffd00a789f5e4ea7284",
    ),
    "source_crosswalk": (
        "Stage1_Instances/THM-M-0130/source_statement_crosswalk.md",
        "c96ba5a25645fc927efd4e49b90f315052e060ca3413cb7ee2a69edc9652c585",
        "451cd64cdad8ccc1f9bb2566592fb95ebb9c5399",
    ),
    "dependency_reuse_ledger": (
        "Stage1_Instances/THM-M-0130/dependency-reuse-ledger.json",
        "29fd9b2d42090d6973738509ac9477bc9d7828e4bca591446a3d1ee8b9f00cac",
        "32d90e440051c7f0172d9752b6465db4bd8875a3",
    ),
    "blocker_report": (
        "Stage1_Instances/THM-M-0130/statement-contract-blocker.md",
        "dd314089d444928af308b4956bd58bdab3912b1f85c8da277b251ffc01a7c902",
        "012bf4a6c8400beccffe216a9d63887fb9e899ca",
    ),
    "prior_blocker_record": (
        "Stage1_Instances/THM-M-0130/statement-blocker.json",
        "900830c49fcdb25486e60982db336994498d68c9dc5b3d6560d8bd2f80a5fa2e",
        "c153795f713ce160f4014879f7f9cb8384fcbb8c",
    ),
    "prior_blocker_report": (
        "Stage1_Instances/THM-M-0130/statement-blocker.md",
        "94a40c01f1b6c65adea91e3b96eec084a433414d88fbcf5da2b6633551bd1cc1",
        "f16340fdd49c48f046f5d7d7afd4a9bd695b9f5b",
    ),
    "intake_record": (
        "Stage1_Instances/THM-M-0130/intake.json",
        "530763b835a7a3e8968a753e801093162a6717cc2de852493f23ebbae8889f89",
        "8b0a93e6f6fe876ea93278fbe7da6f3c06c3e262",
    ),
    "legacy_discovery_source": (
        "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_026.lean",
        "ed079329724bf6202356a98c9e80377cae37baf6e2176f2d4f2105e237eb8b8e",
        "801c0f708a6500de41ca87f0421a89ceab61787e",
    ),
    "task_state_authority": (
        "Docs/Stage1_Blueprint_v2.md",
        "f7f8bcf307b737c56eb7ebc77fa2192046dc07b27ce58df5876ba4fdc4f1d7fb",
        "a861d47fe8683f9a6127a43f8cb8717fa85691d0",
    ),
    "assurance_authority": (
        "Docs/Stage1_Blueprint_rev-5.6.md",
        "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
        "00b304bc44f3d1c52f3723cf1553bb13a2ad4018",
    ),
    "theorem_dag": (
        "Docs/Stage1_Theorem_DAG_v2.json",
        GRAPH_SHA256,
        "69c7daa8e627c40f12a04c8f597a040181c74666",
    ),
    "phase_contract": (
        "Docs/Stage1_Phase_Acceptance_Contracts.json",
        CONTRACT_SHA256,
        "84b92df9eaf457ab954b652c3f20f4d513cf0a88",
    ),
    "target_manifest": (
        "Docs/Stage1_Targets_rev-5.6.json",
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
        "3c85586d3060c219bad5462121b85717360a0665",
    ),
    "execution_skill": (
        "skills/execute-stage1-rev56/SKILL.md",
        "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
        "9b1a2dd279ea94d9b4ca840b063cc8d7fc0d6a49",
    ),
}
EXPECTED_CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0130/Statement.lean",
    "Stage1_Instances/THM-M-0130/check_statement.py",
    "Stage1_Instances/THM-M-0130/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0130/statement-contract-blocker.md",
    "Stage1_Instances/THM-M-0130/statement-receipt.json",
    "Stage1_Instances/THM-M-0130/statement.json",
]
MUTATIONS = {
    "removed_hypothesis": "not_run_no_canonical_target",
    "changed_domain": "not_run_no_canonical_target",
    "changed_binder_scope": "not_run_no_canonical_target",
    "boundary_case": "not_run_no_canonical_target",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)
CANONICAL_DECLARATION = re.compile(
    r"^[ \t]*(?:def|theorem|lemma|example|abbrev|opaque|axiom)\s+"
    r".*(?:Shimura|CanonicalTarget|StatementShape|StatementTarget)",
    flags=re.MULTILINE | re.IGNORECASE,
)
REQUIRED_RECEIPT_FIELDS = {
    "schema_version",
    "receipt_id",
    "item_id",
    "theorem_id",
    "phase",
    "intent",
    "base_revision",
    "base_tree",
    "inputs",
    "support_state",
    "proposed_state",
    "accepted",
    "verdict",
    "selftest_status",
    "selftest_result",
    "known_failures",
    "first_failed_gate",
    "retry_condition",
    "status_boundary",
    "audit_complete",
    "theorem_complete",
    "invalidation_inputs",
    "statement_fingerprints",
    "mutation_tests",
}


def load(relative: str) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r} in {relative}")
            result[key] = value
        return result

    value = json.loads(
        (ROOT / relative).read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicates,
    )
    if not isinstance(value, dict):
        raise ValueError(f"{relative} is not one JSON object")
    return value


def sha256(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def git_blob(relative: str) -> str:
    data = (ROOT / relative).read_bytes()
    framed = f"blob {len(data)}\0".encode("ascii") + data
    return hashlib.sha1(framed).hexdigest()


def run(argv: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "TZ": "UTC", "LEAN_NUM_THREADS": "1"})
    return subprocess.run(
        argv,
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )


def git(*argv: str) -> str:
    result = run(["git", *argv])
    if result.returncode:
        raise ValueError(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def validate_authority() -> tuple[dict[str, Any], dict[str, Any]]:
    if sys.flags.optimize != 0:
        raise ValueError("validator requires Python assertions to remain enabled")
    if git("rev-parse", "HEAD") != BASE_REVISION:
        raise ValueError("repository HEAD differs from the worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("repository tree differs from the worker base")
    for _, (relative, expected_sha256, expected_blob) in EXPECTED_INPUTS.items():
        if sha256(relative) != expected_sha256:
            raise ValueError(f"bound input SHA-256 changed: {relative}")
        if git_blob(relative) != expected_blob:
            raise ValueError(f"bound input Git blob changed: {relative}")

    target_manifest = load("Docs/Stage1_Targets_rev-5.6.json")
    target = next(
        row for row in target_manifest["targets"] if row.get("theorem_id") == THEOREM_ID
    )
    if target != {
        "execution_rank": 26,
        "legacy_priority_slot": "S1-M-026",
        "theorem_id": THEOREM_ID,
        "name": "志村簇",
        "category": "几何学 / 代数几何",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "frontier_deep_formalization_debt",
        "intake_score": 179,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }:
        raise ValueError("target manifest identity or baseline changed")

    execution = load("Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row.get("id") == ITEM_ID)
    if item != {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 26,
        "phase": "statement",
        "layer": 1,
        "state": "[ ]",
        "depends_on": ["S56-M-0130-INTAKE"],
        "owned_paths": ["Stage1_Instances/THM-M-0130"],
        "deliverable": "Elaborate the exact Lean 4 target with the minimal pinned imports.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }:
        raise ValueError("authoritative statement item changed")
    intake_item = next(
        row for row in execution["items"] if row.get("id") == "S56-M-0130-INTAKE"
    )
    if intake_item.get("state") != "[_]" or intake_item.get("attempts") != 1:
        raise ValueError("intake predecessor state changed")

    theorem_dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    node = next(
        row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM_ID
    )
    if node.get("v2_execution_rank") != 263 or node.get("topological_layer") != 0:
        raise ValueError("v2 claim order changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        raise ValueError("dependency context changed")
    if node.get("phase_states", {}).get("statement") != "[ ]":
        raise ValueError("authoritative statement state changed")
    for field in (
        "direct_hard_parents",
        "transitive_hard_ancestors",
        "direct_reuse_hint_ids",
        "shared_lemma_group_ids",
        "reusable_artifacts",
    ):
        if node.get(field) != []:
            raise ValueError(f"declared empty theorem context changed: {field}")

    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row.get("phase") == "statement")
    if phase.get("intent") != "audit":
        raise ValueError("statement phase intent changed")
    if phase.get("raw_blocked_can_close_phase") is not False:
        raise ValueError("blocked statement unexpectedly closes the phase")
    if phase.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        raise ValueError("negative statement finding unexpectedly satisfies the deliverable")
    if [row.get("gate_id") for row in phase.get("semantic_gates", [])] != [
        "S01-ARTIFACTS",
        "S02-EXACT-TARGET",
        "S03-MUTATIONS",
    ]:
        raise ValueError("statement semantic gates changed")
    selected: dict[str, str] = {}
    for role in phase["required_artifact_roles"]:
        candidates = [
            raw.format(theorem_id=THEOREM_ID)
            for raw in role["path_candidates"]
            if (ROOT / raw.format(theorem_id=THEOREM_ID)).is_file()
        ]
        if len(candidates) != 1:
            raise ValueError(f"artifact role {role['role']} is missing or ambiguous")
        selected[role["role"]] = candidates[0]
    if selected != ROLE_PATHS:
        raise ValueError("contract-selected artifact roles changed")
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    if validators != ["Stage1_Instances/THM-M-0130/check_statement.py"]:
        raise ValueError("validator selection is not exactly one declared candidate")
    return node, phase


def validate_ledger(node: dict[str, Any]) -> None:
    ledger = load("Stage1_Instances/THM-M-0130/dependency-reuse-ledger.json")
    if ledger.get("schema_version") != "stage1-dependency-reuse-ledger/1.1":
        raise ValueError("dependency ledger schema changed")
    if ledger.get("consumer_theorem_id") != THEOREM_ID:
        raise ValueError("dependency ledger owner changed")
    if ledger.get("observed_theorem_dag_sha256") != GRAPH_SHA256:
        raise ValueError("dependency ledger graph binding changed")
    if ledger.get("dependency_context_sha256") != CONTEXT_SHA256:
        raise ValueError("dependency ledger context binding changed")
    if ledger.get("repository_revision") != BASE_REVISION:
        raise ValueError("dependency ledger revision changed")
    if ledger.get("claim_order") != {
        "v2_execution_rank": 263,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        raise ValueError("dependency ledger claim order changed")
    for field in (
        "direct_parent_ids",
        "transitive_ancestor_ids",
        "hard_edge_ids",
        "reuse_hint_ids",
        "shared_group_ids",
        "parent_inspection_order",
        "inspections",
        "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        if ledger.get(field) != []:
            raise ValueError(f"empty dependency ledger field changed: {field}")
    if ledger.get("closure_audit", {}).get("inspection_order") != []:
        raise ValueError("parent inspection order is not the exact empty closure")
    if node.get("dependency_audit_status") != "unknown_not_independent_proof_claim":
        raise ValueError("theorem dependency audit boundary changed")


def validate_statement_boundary() -> None:
    statement = load("Stage1_Instances/THM-M-0130/statement.json")
    intake = load("Stage1_Instances/THM-M-0130/intake.json")
    prior = load("Stage1_Instances/THM-M-0130/statement-blocker.json")
    source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    crosswalk = (HERE / "source_statement_crosswalk.md").read_text(encoding="utf-8")
    blocker = (HERE / "statement-contract-blocker.md").read_text(encoding="utf-8")

    if intake.get("canonical_formal_target", {}).get("gate_state") != (
        "open_source_statement_disambiguation_required"
    ):
        raise ValueError("intake no longer preserves source ambiguity")
    for field in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        if intake["canonical_formal_target"].get(field) is not None:
            raise ValueError(f"intake unexpectedly fills canonical target field {field}")
    if prior.get("statement_gate_passed") is not False:
        raise ValueError("prior blocker unexpectedly passes the statement gate")
    if prior.get("first_failed_gate") != "exact_source_statement_identity":
        raise ValueError("prior exact-source blocker changed")

    if statement.get("schema_version") != "stage1-statement/1.0":
        raise ValueError("statement record schema changed")
    if statement.get("item_id") != ITEM_ID or statement.get("theorem_id") != THEOREM_ID:
        raise ValueError("statement record identity changed")
    if statement.get("canonical_claim_status") != "blocked_exact_source_statement_identity":
        raise ValueError("statement source ambiguity is no longer explicit")
    if statement.get("canonical_statement") is not None:
        raise ValueError("a canonical mathematical statement was invented")
    formal = statement.get("canonical_formal_target", {})
    for field in (
        "declaration_or_expression",
        "elaborated_expression_sha256",
        "environment_fingerprint",
    ):
        if formal.get(field) is not None:
            raise ValueError(f"a canonical target field was invented: {field}")
    if statement.get("direct_imports") != [DIRECT_IMPORT]:
        raise ValueError("boundary-probe imports changed")
    if statement.get("statement_fingerprints") != []:
        raise ValueError("a statement fingerprint was invented")
    if statement.get("checked_alternate_encodings") != []:
        raise ValueError("a checked transport was invented")
    if statement.get("mutation_tests") != MUTATIONS:
        raise ValueError("statement mutation blocker boundary changed")
    for field in (
        "statement_elaborated",
        "phase_predicate_proven",
        "phase_accepted",
        "theorem_proved",
        "audit_complete",
        "theorem_complete",
    ):
        if statement.get(field) is not False:
            raise ValueError(f"statement record overclaims {field}")

    imports = re.findall(r"^import ([^\s]+)$", source, re.MULTILINE)
    if imports != [DIRECT_IMPORT]:
        raise ValueError("Statement.lean does not have exactly one declared import")
    if "#check Scheme.{u}" not in source:
        raise ValueError("Statement.lean omits its adjacent scheme check")
    if CANONICAL_DECLARATION.search(source):
        raise ValueError("Statement.lean unexpectedly declares a canonical target")
    if PROHIBITED.search(source):
        raise ValueError("Statement.lean contains a prohibited construct")
    for required in (
        "The candidates are not interchangeable.",
        "Canonical models over the reflex field",
        "Hodge-type integral canonical models",
    ):
        if required not in crosswalk:
            raise ValueError("source crosswalk no longer records all candidate families")
    for required in (
        "phase_accepted=false",
        "validator did not exist at this worker base",
        "No provider was\ninspected because none appears in the declared closure",
    ):
        if required not in blocker:
            raise ValueError("blocker report omits a required status boundary")


def validate_lean() -> None:
    boundary = run(
        [
            "lake",
            "env",
            "lean",
            "--trust=0",
            "../../Stage1_Instances/THM-M-0130/Statement.lean",
        ],
        cwd=LEAN_ROOT,
    )
    if boundary.returncode != 0 or boundary.stderr:
        raise ValueError(
            "declaration-free boundary did not elaborate cleanly: "
            f"{(boundary.stdout + boundary.stderr)[:600]}"
        )
    if boundary.stdout != "Scheme : Type (u + 1)\n":
        raise ValueError("boundary probe output changed")

    legacy = run(
        ["lake", "env", "lean", "AwesomeTheorems/Stage1/S1_M_026.lean"],
        cwd=LEAN_ROOT,
    )
    if legacy.returncode != 0 or legacy.stderr:
        raise ValueError(
            f"legacy discovery source did not elaborate cleanly: {(legacy.stdout + legacy.stderr)[:600]}"
        )
    for marker in (
        "AwesomeTheorems.Stage1.S1_M_026.StatementShape",
        "AwesomeTheorems.Stage1.S1_M_026.p08RepoLocalClosureCompleted_eq_false",
        "AwesomeTheorems.Stage1.S1_M_026.p03DatumDefinitionDecision_is_localSkeleton",
    ):
        if marker not in legacy.stdout:
            raise ValueError("legacy replay no longer exposes its negative boundary markers")

    mathlib_root = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    if run(["git", "rev-parse", "HEAD"], cwd=mathlib_root).stdout.strip() != (
        "8a178386ffc0f5fef0b77738bb5449d50efeea95"
    ):
        raise ValueError("pinned mathlib revision changed")
    if run(["git", "rev-parse", "HEAD^{tree}"], cwd=mathlib_root).stdout.strip() != (
        "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
    ):
        raise ValueError("pinned mathlib tree changed")
    if run(["git", "status", "--short"], cwd=mathlib_root).stdout:
        raise ValueError("pinned mathlib worktree is dirty")

    roots = [mathlib_root / "Mathlib"]
    flt_regular = LEAN_ROOT / ".lake" / "packages" / "flt-regular"
    if flt_regular.is_dir():
        roots.append(flt_regular)
    search = run(
        [
            "rg",
            "-n",
            "-i",
            "--glob",
            "*.lean",
            r"Shimura|reflex.?field|Hodge.?type",
            *[str(path) for path in roots],
        ]
    )
    if search.returncode not in {1} or search.stdout or search.stderr:
        raise ValueError("bounded pinned dependency search result changed")


def validate_receipt_and_packet() -> None:
    receipt = load("Stage1_Instances/THM-M-0130/statement-receipt.json")
    packet = load(".stage1-worker-selftest.json")
    validator_path = "Stage1_Instances/THM-M-0130/check_statement.py"
    validator_binding = receipt.get("inputs", {}).get("statement_validator")
    if not isinstance(validator_binding, dict):
        raise ValueError("receipt lacks the validator input binding")
    if validator_binding != {
        "role": "phase_validator",
        "path": validator_path,
        "sha256": sha256(validator_path),
        "git_blob": git_blob(validator_path),
    }:
        raise ValueError("receipt validator input binding is stale")

    if not REQUIRED_RECEIPT_FIELDS.issubset(receipt):
        raise ValueError("statement receipt omits a contract-required field")
    if receipt.get("schema_version") != "stage1-node-receipt/1.0":
        raise ValueError("statement receipt schema changed")
    if (
        receipt.get("item_id"),
        receipt.get("theorem_id"),
        receipt.get("phase"),
        receipt.get("intent"),
    ) != (ITEM_ID, THEOREM_ID, "statement", "audit"):
        raise ValueError("statement receipt identity changed")
    if receipt.get("base_revision") != BASE_REVISION or receipt.get("base_tree") != BASE_TREE:
        raise ValueError("statement receipt base changed")
    if receipt.get("accepted") is not False or receipt.get("verdict") != "blocked":
        raise ValueError("statement receipt acceptance boundary changed")
    if receipt.get("worker_verdict") != "blocked":
        raise ValueError("statement receipt worker verdict changed")
    if receipt.get("support_state") != "provisional_worker_selftest_blocked":
        raise ValueError("statement receipt support state changed")
    if receipt.get("proposed_state") != "[_]" or receipt.get("selftest_status") != "passed":
        raise ValueError("statement receipt does not propose a self-tested handoff")
    selftest = receipt.get("selftest_result", {})
    if selftest.get("exit_code") != 0 or selftest.get("phase_predicate_passed") is not False:
        raise ValueError("statement receipt self-test boundary changed")
    if receipt.get("phase_predicate_proven") is not False:
        raise ValueError("statement receipt falsely proves the phase predicate")
    if receipt.get("phase_accepted") is not False:
        raise ValueError("statement receipt falsely accepts the phase")
    if receipt.get("statement_elaborated") is not False:
        raise ValueError("statement receipt falsely claims exact target elaboration")
    if receipt.get("statement_fingerprints") != [] or receipt.get("mutation_tests") != MUTATIONS:
        raise ValueError("statement receipt invents fingerprint or mutation credit")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        raise ValueError("statement receipt overclaims a terminal decision")
    if receipt.get("first_failed_gate") != "S02-EXACT-TARGET.exact_source_statement_identity":
        raise ValueError("statement receipt first failed gate changed")
    if not receipt.get("known_failures"):
        raise ValueError("statement receipt omits known failures")

    selected = {row.get("role"): row for row in receipt.get("selected_artifacts", [])}
    if set(selected) != set(ROLE_PATHS):
        raise ValueError("statement receipt selected-role inventory changed")
    for role in ("statement_record", "statement_source", "source_crosswalk"):
        relative, expected_sha256, expected_blob = EXPECTED_INPUTS[role]
        if selected[role] != {
            "role": role,
            "path": relative,
            "sha256": expected_sha256,
            "git_blob": expected_blob,
        }:
            raise ValueError(f"selected artifact binding changed: {role}")
    self_binding = selected["phase_receipt"]
    if self_binding.get("path") != ROLE_PATHS["phase_receipt"]:
        raise ValueError("phase receipt selected path changed")
    if self_binding.get("sha256") is not None or self_binding.get("git_blob") is not None:
        raise ValueError("phase receipt recursively claims its own digest")

    inputs = receipt.get("inputs", {})
    for name, (relative, expected_sha256, expected_blob) in EXPECTED_INPUTS.items():
        binding = inputs.get(name)
        if not isinstance(binding, dict):
            raise ValueError(f"receipt lacks bound input {name}")
        if binding.get("path") != relative:
            raise ValueError(f"receipt input path changed: {name}")
        if binding.get("sha256") != expected_sha256:
            raise ValueError(f"receipt input SHA-256 changed: {name}")
        if binding.get("git_blob") != expected_blob:
            raise ValueError(f"receipt input Git blob changed: {name}")

    expected_command = {
        "argv": [
            "/usr/bin/python3",
            "-I",
            "-B",
            "Stage1_Instances/THM-M-0130/check_statement.py",
        ],
        "cwd": ".",
        "exit_code": 0,
        "semantic_status": "blocked",
        "phase_accepted": False,
    }
    if receipt.get("commands") != [expected_command]:
        raise ValueError("statement receipt command record changed")
    if selftest.get("commands") != receipt.get("commands"):
        raise ValueError("receipt self-test commands differ from command record")
    if receipt.get("changed_paths") != EXPECTED_CHANGED_PATHS:
        raise ValueError("statement receipt changed-path inventory changed")

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
    if packet.get("item_id") != ITEM_ID or packet.get("worker_verdict") != "blocked":
        raise ValueError("worker packet identity or verdict changed")
    if packet.get("base_revision") != BASE_REVISION or packet.get("state") != "[_]":
        raise ValueError("worker packet base or state changed")
    if packet.get("changed_paths") != EXPECTED_CHANGED_PATHS:
        raise ValueError("worker packet changed-path inventory changed")
    if packet.get("commands") != receipt.get("commands"):
        raise ValueError("worker packet commands differ from the phase receipt")
    if packet.get("known_failures") != receipt.get("known_failures"):
        raise ValueError("worker packet known failures differ from the phase receipt")
    if packet.get("output_summary") != receipt.get("output_summary"):
        raise ValueError("worker packet summary differs from the phase receipt")

    for relative in EXPECTED_CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\0" in data:
            raise ValueError(f"artifact formatting changed: {relative}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            raise ValueError(f"artifact has trailing whitespace: {relative}")


def validate() -> None:
    node, _ = validate_authority()
    validate_ledger(node)
    validate_statement_boundary()
    validate_lean()
    validate_receipt_and_packet()


def semantic_result() -> dict[str, Any]:
    return {
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
        "first_failed_gate": "S02-EXACT-TARGET.exact_source_statement_identity",
        "open_obligations": 5,
        "stale_inputs": [],
        "blocked": True,
        "message": (
            "Target-scoped blocker self-tested: source identity, exact Lean target, "
            "expression/environment fingerprints, checked transports, and all four "
            "mutation classes remain open; phase acceptance is false."
        ),
    }


def main() -> None:
    try:
        validate()
    except Exception as error:
        traceback.print_exc(file=sys.stderr)
        failure = semantic_result()
        failure.update(
            {
                "status": "failed",
                "verdict": "repair_required",
                "first_failed_gate": "VALIDATOR-INTERNAL-CONSISTENCY",
                "blocked": False,
                "message": f"Statement blocker validation failed: {type(error).__name__}: {error}",
            }
        )
        print(json.dumps(failure, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    print(json.dumps(semantic_result(), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
