#!/usr/bin/env python3
"""Validate the truthful negative statement packet for THM-M-0148."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0148"
ITEM_ID = "S56-M-0148-STATEMENT"
THEOREM_ID = "THM-M-0148"
BASE_REVISION = "2dc5a410b68eff806858fd6ed0cb33d57f6209f7"
BASE_TREE = "841bdd6114e7436cff4a3a1ff248fc1e884a9ddc"
GRAPH_SHA256 = "3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
EXPECTED_OWNED_SHA256 = {
    "Statement.lean": "dc927360172cd822b1532b3070c916a7e5c2ee7ff7d98954ea94f8c78e8b4846",
    "statement.json": "9104f6f1a895b246f273d886e79e41ccf328786c34ceba09006b0d236eacd3ba",
    "source-statement-crosswalk.md": "24caaa414857f4a6338c177f403092f311f1aac817eb9e6de6ae6229834e8ab5",
    "dependency-reuse-ledger.json": "17040b103ff13e1042350ea66fefe33c4e775234ecde0f1395d368a84f2553a1",
    "statement-phase-blocker-2026-07-17-head-2dc5a410-slot20.md": "4d6212c298d04e57e1b08c0adfc5802ffe9c9debac6ae7667bfeab71e7f5fe04",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
    re.MULTILINE,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r} in {path}")
            result[key] = value
        return result

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


def verify() -> None:
    if sys.flags.optimize != 0:
        raise ValueError("statement validator requires Python assertions")

    record = load(HERE / "statement.json")
    receipt = load(HERE / "statement-receipt.json")
    ledger = load(HERE / "dependency-reuse-ledger.json")
    instance = load(HERE / "instance.json")
    blocker = load(HERE / "statement-blocker.json")
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
    if node["v2_execution_rank"] != 265 or node["dependency_context_sha256"] != CONTEXT_SHA256:
        raise ValueError("target rank or dependency context disagrees")
    for key in (
        "direct_hard_parents",
        "transitive_hard_ancestors",
        "direct_reuse_hint_ids",
        "shared_lemma_group_ids",
    ):
        if node[key] != []:
            raise ValueError(f"declared empty dependency field changed: {key}")

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
    for key in (
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
        if ledger[key] != []:
            raise ValueError(f"empty dependency closure is not empty: {key}")
    if ledger["claim_order"] != {
        "v2_execution_rank": 265,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        raise ValueError("claim order binding mismatch")

    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    if phase["intent"] != "audit" or phase["raw_blocked_can_close_phase"] is not False:
        raise ValueError("statement contract negative boundary changed")
    if phase["classified_negative_findings_may_satisfy_deliverable"] is not False:
        raise ValueError("negative statement finding unexpectedly became phase-completing")
    if [row["gate_id"] for row in phase["semantic_gates"]] != [
        "S01-ARTIFACTS",
        "S02-EXACT-TARGET",
        "S03-MUTATIONS",
    ]:
        raise ValueError("statement semantic gate set changed")

    if instance["canonical_formal_target"]["status"] != "not_frozen":
        raise ValueError("instance unexpectedly claims a frozen target")
    for field in (
        "module",
        "declaration_or_expression",
        "elaborated_expression_hash",
        "environment_fingerprint",
    ):
        if instance["canonical_formal_target"][field] is not None:
            raise ValueError(f"instance unexpectedly fills canonical target field {field}")
    if blocker["statement_gate_passed"] is not False or blocker["statement_elaborated"] is not False:
        raise ValueError("prior blocker semantics changed")

    if record["status"] != "blocked_unfrozen":
        raise ValueError("statement record is not fail-closed")
    if record["canonical_human_statement"] is not None:
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

    source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    if source.count("\nimport ") != 0 or not source.startswith(
        "import Mathlib.AlgebraicGeometry.RationalMap\n"
    ):
        raise ValueError("negative probe does not have exactly one direct import")
    if "#check Scheme.{u}" not in source or "#check Scheme.RationalMap" not in source:
        raise ValueError("negative probe does not check its declared object boundary")
    if re.search(r"^\s*(?:def|theorem)\s+.*(?:Target|Statement)", source, re.MULTILINE):
        raise ValueError("negative probe unexpectedly declares a canonical target")
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
        or receipt["selftest_result"].get("phase_predicate_passed") is not False
    ):
        raise ValueError("statement receipt proposes an illegal worker transition")
    if receipt["first_failed_gate"] != "S02-EXACT-TARGET":
        raise ValueError("statement receipt first failed gate mismatch")
    if receipt["statement_fingerprints"] != []:
        raise ValueError("statement receipt invents a fingerprint")
    if any(row["passed"] is not False for row in receipt["mutation_tests"]):
        raise ValueError("statement receipt falsely passes a mutation")
    if receipt["audit_complete"] is not False or receipt["theorem_complete"] is not False:
        raise ValueError("statement receipt overclaims a terminal decision")

    bound_roles = {
        "statement_record": receipt["inputs"]["statement_record"],
        "statement_source": receipt["inputs"]["statement_source"],
        "source_crosswalk": receipt["inputs"]["source_crosswalk"],
    }
    for role, binding in bound_roles.items():
        path = ROOT / binding["path"]
        if sha256(path) != binding["sha256"]:
            raise ValueError(f"receipt {role} sha256 binding is stale")
        if git("hash-object", str(path)) != binding["git_blob"]:
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
        "first_failed_gate": "S02-EXACT-TARGET",
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
            "The target-owned packet truthfully proves that the Mori programme slogan has no "
            "source-selected exact Lean proposition; statement acceptance remains blocked."
        )
    )
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
