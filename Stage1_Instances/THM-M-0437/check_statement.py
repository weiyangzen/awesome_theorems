#!/usr/bin/env python3
"""Validate THM-M-0437's truthful negative statement packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0437"
ITEM_ID = "S56-M-0437-STATEMENT"
THEOREM_ID = "THM-M-0437"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
FAILED_GATE = "S02-EXACT-TARGET"
EXPECTED_OWNED_SHA256 = {
    "Statement.lean": "560a8758e97845d105cedfe80d4431347c0aab39caa72b55ca38df1fdb2dd1e8",
    "statement.json": "01f4bc8357714e383f84d866f369d7bc7ecaa4efecbdfdd88f305238d9fc87e8",
    "source-statement-crosswalk.md": "f9d8aab349738e1bee388e52f1ef2022631123a2c5f983b713dff6c91180d9fa",
    "dependency-reuse-ledger.json": "0355cbaa90d0914f58cc7ad124c028a94fc1eb2556e21da86d361d57617d663b",
    "statement-phase-blocker-2026-07-17-head-1cc6aa61-slot104.md": (
        "a1fc13739afdaf8e9a7791537b88856e5dfea866f37095ea1dea8289ceee3550"
    ),
}
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0437/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0437/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0437/source-statement-crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0437/statement-receipt.json",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe|implemented_by|native_decide)\b"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        value: dict[str, object] = {}
        for key, child in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON key {key!r} in {path}")
            value[key] = child
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    if not isinstance(value, dict):
        raise ValueError(f"{path} is not a JSON object")
    return value


def git(*argv: str) -> str:
    result = subprocess.run(
        ["/usr/bin/git", *argv],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise ValueError(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def base_blob(relative: str) -> str | None:
    result = subprocess.run(
        ["/usr/bin/git", "rev-parse", "--verify", f"{BASE_REVISION}:{relative}"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def verify() -> None:
    if sys.flags.optimize != 0:
        raise ValueError("statement validator requires Python assertions")

    record = load(HERE / "statement.json")
    receipt = load(HERE / "statement-receipt.json")
    ledger = load(HERE / "dependency-reuse-ledger.json")
    intake = load(HERE / "intake.json")
    prior_blocker = load(HERE / "statement-head-contract-blocker.json")
    dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")

    if git("rev-parse", "HEAD") != BASE_REVISION:
        raise ValueError("repository HEAD differs from the worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("repository base tree differs from the receipt")
    if sha256(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") != GRAPH_SHA256:
        raise ValueError("v2 theorem DAG digest drifted")
    if sha256(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") != CONTRACT_SHA256:
        raise ValueError("phase acceptance contract digest drifted")
    for name, expected in EXPECTED_OWNED_SHA256.items():
        if sha256(HERE / name) != expected:
            raise ValueError(f"owned statement input drifted: {name}")

    node = next(row for row in dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    if node["v2_execution_rank"] != 300 or node["dependency_context_sha256"] != CONTEXT_SHA256:
        raise ValueError("target rank or dependency context disagrees")
    if node["phase_states"] != {
        "intake": "[_]",
        "statement": "[ ]",
        "anchor_audit": "[ ]",
        "obligation_tree": "[ ]",
        "proof": "[ ]",
        "validation": "[ ]",
        "release": "[ ]",
    }:
        raise ValueError("authoritative phase-state snapshot changed")
    for key in (
        "direct_hard_parents",
        "transitive_hard_ancestors",
        "direct_reuse_hint_ids",
        "shared_lemma_group_ids",
        "reusable_artifacts",
    ):
        if node[key] != []:
            raise ValueError(f"declared empty dependency field changed: {key}")

    empty_fields = (
        "direct_parent_ids",
        "transitive_ancestor_ids",
        "hard_edge_ids",
        "reuse_hint_ids",
        "shared_group_ids",
        "parent_inspection_order",
        "inspections",
        "reuse_decisions",
        "unresolved_compatibility_obligations",
    )
    if ledger["schema_version"] != "stage1-dependency-reuse-ledger/1.1":
        raise ValueError("dependency ledger schema mismatch")
    if ledger["consumer_theorem_id"] != THEOREM_ID:
        raise ValueError("dependency ledger consumer mismatch")
    if ledger["observed_theorem_dag_sha256"] != GRAPH_SHA256:
        raise ValueError("dependency ledger graph digest mismatch")
    if ledger["dependency_context_sha256"] != CONTEXT_SHA256:
        raise ValueError("dependency ledger context mismatch")
    if ledger["repository_revision"] != BASE_REVISION:
        raise ValueError("dependency ledger base mismatch")
    if ledger["claim_order"] != {
        "v2_execution_rank": 300,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        raise ValueError("dependency ledger claim order mismatch")
    for key in empty_fields:
        if ledger[key] != []:
            raise ValueError(f"empty dependency closure is not empty: {key}")
    if ledger["closure_audit"]["status"] != "empty_declared_context_inspected":
        raise ValueError("empty dependency traversal is not audited")

    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    if phase["intent"] != "audit" or phase["raw_blocked_can_close_phase"] is not False:
        raise ValueError("statement blocked semantics changed")
    if phase["classified_negative_findings_may_satisfy_deliverable"] is not False:
        raise ValueError("negative statement finding unexpectedly became phase-completing")
    if [row["gate_id"] for row in phase["semantic_gates"]] != [
        "S01-ARTIFACTS",
        "S02-EXACT-TARGET",
        "S03-MUTATIONS",
    ]:
        raise ValueError("statement semantic gate set changed")
    selected: dict[str, str] = {}
    for role in phase["required_artifact_roles"]:
        matches = [
            pattern.format(theorem_id=THEOREM_ID)
            for pattern in role["path_candidates"]
            if (ROOT / pattern.format(theorem_id=THEOREM_ID)).is_file()
        ]
        if len(matches) != 1:
            raise ValueError(f"role {role['role']} does not resolve exactly once")
        selected[role["role"]] = matches[0]
    if selected != ROLE_PATHS:
        raise ValueError("selected statement roles changed")
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    if validators != ["Stage1_Instances/THM-M-0437/check_statement.py"]:
        raise ValueError("statement validator is missing or ambiguous")
    if base_blob(validators[0]) is not None:
        raise ValueError("negative packet no longer records a worker-created validator boundary")

    if intake["canonical_formal_target"]["declaration_or_expression"] is not None:
        raise ValueError("intake unexpectedly identifies a formal target")
    if prior_blocker["statement_gate_passed"] is not False:
        raise ValueError("prior blocker semantics changed")
    if record["schema_version"] != "stage1-statement/1.0":
        raise ValueError("statement record schema mismatch")
    if record["item_id"] != ITEM_ID or record["theorem_id"] != THEOREM_ID:
        raise ValueError("statement record identity mismatch")
    if record["status"] != "blocked_unfrozen" or record["canonical_human_statement"] is not None:
        raise ValueError("statement record invents a canonical human claim")
    target = record["canonical_formal_target"]
    for field in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_sha256",
        "environment_expression_fingerprint",
    ):
        if target[field] is not None:
            raise ValueError(f"statement record invents target field {field}")
    if target["statement_source_sha256"] != EXPECTED_OWNED_SHA256["Statement.lean"]:
        raise ValueError("statement record source binding changed")
    if target["minimal_imports"] != ["Mathlib.AlgebraicGeometry.Scheme"]:
        raise ValueError("statement probe imports changed")
    if record["statement_elaborated"] is not False or record["probe_elaborated"] is not True:
        raise ValueError("statement versus probe elaboration boundary changed")
    if record["statement_fingerprints"] != [] or record["alternate_encodings"] != []:
        raise ValueError("statement record invents fingerprints or transports")
    mutations = record["mutation_tests"]
    required_mutations = {
        "removed_hypothesis",
        "changed_domain",
        "changed_binder_scope",
        "boundary_case",
    }
    if set(mutations) != required_mutations:
        raise ValueError("statement mutation classes are incomplete")
    if any(
        row != {"status": "not_run_missing_canonical_target", "passed": False}
        for row in mutations.values()
    ):
        raise ValueError("statement record falsely claims a mutation result")
    if record["audit_complete"] is not False or record["theorem_complete"] is not False:
        raise ValueError("statement record overclaims a terminal decision")

    source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    imports = re.findall(r"^import (\S+)$", source, re.MULTILINE)
    if imports != ["Mathlib.AlgebraicGeometry.Scheme"]:
        raise ValueError("negative probe does not have exactly one direct import")
    if source.count("#check Scheme.{u}") != 1:
        raise ValueError("negative probe does not check its declared object boundary")
    if re.search(r"^\s*(?:def|theorem|lemma|example)\s+", source, re.MULTILINE):
        raise ValueError("negative probe unexpectedly declares a target")
    if PROHIBITED.search(source):
        raise ValueError("negative probe contains a prohibited construct")

    required_receipt_fields = {
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
    if not required_receipt_fields.issubset(receipt):
        raise ValueError("statement receipt omits a contract-required field")
    if receipt["schema_version"] != "stage1-node-receipt/1.0":
        raise ValueError("statement receipt schema mismatch")
    if (receipt["item_id"], receipt["theorem_id"], receipt["phase"], receipt["intent"]) != (
        ITEM_ID,
        THEOREM_ID,
        "statement",
        "audit",
    ):
        raise ValueError("statement receipt identity mismatch")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        raise ValueError("statement receipt base mismatch")
    if receipt["verdict"] != "blocked" or receipt["accepted"] is not False:
        raise ValueError("statement receipt does not preserve blocked semantics")
    if (
        receipt["proposed_state"] != "[_]"
        or receipt["support_state"] != "provisional_worker_selftest_blocked"
        or receipt["selftest_status"] != "passed"
        or receipt["selftest_result"].get("exit_code") != 0
        or receipt["selftest_result"].get("phase_predicate_passed") is not False
        or not isinstance(receipt["selftest_result"].get("commands"), list)
        or not receipt["selftest_result"]["commands"]
        or any(
            not isinstance(command, dict)
            or command.get("exit_code") != 0
            or not isinstance(command.get("argv"), list)
            or not command["argv"]
            for command in receipt["selftest_result"]["commands"]
        )
    ):
        raise ValueError("statement receipt worker handoff semantics are invalid")
    if receipt["first_failed_gate"] != FAILED_GATE:
        raise ValueError("statement receipt first failed gate mismatch")
    if receipt["statement_fingerprints"] != []:
        raise ValueError("statement receipt invents a fingerprint")
    if any(row["passed"] is not False for row in receipt["mutation_tests"]):
        raise ValueError("statement receipt falsely passes a mutation")
    if receipt["audit_complete"] is not False or receipt["theorem_complete"] is not False:
        raise ValueError("statement receipt overclaims a terminal decision")

    artifact_bindings = receipt["artifact_bindings"]
    if set(artifact_bindings) != set(ROLE_PATHS):
        raise ValueError("statement receipt artifact roles changed")
    for role in ("statement_record", "statement_source", "source_crosswalk"):
        relative = ROLE_PATHS[role]
        path = ROOT / relative
        if artifact_bindings[role] != {
            "role": role,
            "path": relative,
            "sha256": sha256(path),
            "git_blob": git_blob(path),
        }:
            raise ValueError(f"receipt {role} artifact binding is stale")
    if artifact_bindings["phase_receipt"] != {
        "role": "phase_receipt",
        "path": ROLE_PATHS["phase_receipt"],
        "sha256": None,
        "git_blob": None,
        "binding_owner": "scheduler integration lane",
        "status_boundary": (
            "The receipt cannot embed its own final byte hashes without a cycle; the scheduler "
            "binds the integrated HEAD receipt bytes."
        ),
    }:
        raise ValueError("phase receipt self-binding boundary changed")

    for role, relative in ROLE_PATHS.items():
        if role == "phase_receipt":
            # The scheduler binds this selected receipt directly from HEAD;
            # embedding its own digest in its bytes would be recursive.
            continue
        binding = receipt["inputs"][role]
        if binding["path"] != relative:
            raise ValueError(f"receipt {role} path binding changed")
        path = ROOT / relative
        if sha256(path) != binding["sha256"]:
            raise ValueError(f"receipt {role} sha256 binding is stale")
        if git_blob(path) != binding["git_blob"]:
            raise ValueError(f"receipt {role} Git blob binding is stale")


def semantic_result(*, message: str) -> dict:
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
        "first_failed_gate": FAILED_GATE,
        "open_obligations": 4,
        "stale_inputs": [],
        "blocked": True,
        "message": message,
    }


def main() -> None:
    try:
        verify()
    except Exception as exc:
        result = {
            **semantic_result(message=f"negative statement packet validation failed: {exc}"),
            "status": "failed",
            "verdict": "repair_required",
            "first_failed_gate": "S01-ARTIFACTS",
            "blocked": False,
        }
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    result = semantic_result(
        message=(
            "The target-owned packet truthfully proves that the Hodge-type Shida/Shimura "
            "topic phrase has no source-selected exact Lean proposition; statement "
            "acceptance remains blocked."
        )
    )
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
