#!/usr/bin/env python3
"""Validate the truthful negative statement packet for THM-M-0435."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0435"
ITEM_ID = "S56-M-0435-STATEMENT"
THEOREM_ID = "THM-M-0435"
BASE_REVISION = "74d4c272070069bc62df15798895293b4795940a"
BASE_TREE = "6693e584a3d529077306168fe38abd693d210ef0"
GRAPH_SHA256 = "cb4b83c4c4a5474fce51f98098f1421315fe7f1bd8cd52205932e57eced9f675"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
BLUEPRINT_SHA256 = "725f999ec03ac768762a481c1268f9532198c009d71bac94013406ba674528de"
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide)\b|"
    r"^[ \t]*(?:axiom|constant|opaque|unsafe\s+(?:def|theorem)|theorem)\b",
    re.MULTILINE,
)


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
        raise ValueError(f"{path} must contain one JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


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


def binding_matches(binding: object, relative: str) -> bool:
    if not isinstance(binding, dict) or binding.get("path") != relative:
        return False
    path = ROOT / relative
    return binding.get("sha256") == sha256(path) and binding.get("git_blob") == git_blob(path)


def verify() -> None:
    dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    ledger = load(HERE / "dependency-reuse-ledger.json")
    record = load(HERE / "statement.json")
    receipt = load(HERE / "statement-receipt.json")

    if git("rev-parse", "HEAD") != BASE_REVISION or git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("repository HEAD or base tree differs from the worker claim")
    if sha256(ROOT / "Docs/Stage1_Blueprint_v2.md") != BLUEPRINT_SHA256:
        raise ValueError("task-state authority bytes changed")
    if sha256(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") != GRAPH_SHA256:
        raise ValueError("theorem DAG bytes changed")
    if sha256(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") != CONTRACT_SHA256:
        raise ValueError("phase contract bytes changed")

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    if "- [ ] `S56-M-0435-STATEMENT`" not in blueprint or "{attempts=0}" not in blueprint:
        raise ValueError("authoritative statement item is not the claimed open attempt")

    node = next(row for row in dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    if node["v2_execution_rank"] != 310 or node["dependency_context_sha256"] != CONTEXT_SHA256:
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
    expected_scalars = {
        "consumer_theorem_id": THEOREM_ID,
        "observed_theorem_dag_sha256": GRAPH_SHA256,
        "dependency_context_sha256": CONTEXT_SHA256,
        "repository_revision": BASE_REVISION,
    }
    for key, value in expected_scalars.items():
        if ledger.get(key) != value:
            raise ValueError(f"dependency ledger {key} mismatch")
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
        if ledger.get(key) != []:
            raise ValueError(f"empty dependency closure is not empty: {key}")
    if ledger.get("claim_order") != {
        "v2_execution_rank": 310,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        raise ValueError("claim order binding mismatch")

    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    if phase["intent"] != "audit" or phase["raw_blocked_can_close_phase"] is not False:
        raise ValueError("statement contract negative boundary changed")
    candidates = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    if candidates != [f"Stage1_Instances/{THEOREM_ID}/check_statement.py"]:
        raise ValueError("the HEAD contract does not resolve exactly one validator candidate")
    base_validator = subprocess.run(
        ["/usr/bin/git", "cat-file", "-e", f"{BASE_REVISION}:Stage1_Instances/{THEOREM_ID}/check_statement.py"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if base_validator.returncode == 0:
        raise ValueError("negative packet boundary changed: validator unexpectedly existed at base")

    if record["schema_version"] != "stage1-statement-record/1.0":
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
            raise ValueError(f"statement record invents canonical target field {field}")
    if record["statement_fingerprints"] != [] or record["alternate_encodings"] != []:
        raise ValueError("statement record invents a fingerprint or transport")
    mutations = record["mutation_tests"]
    required_mutations = {
        "removed_hypothesis",
        "changed_domain",
        "changed_binder_scope",
        "boundary_case",
    }
    if set(mutations) != required_mutations:
        raise ValueError("statement mutation inventory is incomplete")
    if any(
        row != {"status": "not_run_missing_canonical_target", "passed": False}
        for row in mutations.values()
    ):
        raise ValueError("statement record falsely claims a mutation result")

    source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    imports = re.findall(r"^import ([^\s]+)$", source, re.MULTILINE)
    if imports != record["negative_probe"]["direct_imports"]:
        raise ValueError("negative probe imports disagree with the statement record")
    for symbol in (
        "#check NumberField",
        "#check QuaternionAlgebra",
        "#check QuaternionAlgebra.basisOneIJK",
        "#check Scheme.{u}",
        "#check IsProper",
        "#check SmoothOfRelativeDimension",
    ):
        if symbol not in source:
            raise ValueError(f"negative probe omits {symbol}")
    if re.search(r"^\s*(?:def|theorem)\s+.*(?:Target|Statement)", source, re.MULTILINE):
        raise ValueError("negative probe unexpectedly declares a canonical target")
    if PROHIBITED.search(source):
        raise ValueError("negative probe contains a prohibited construct")

    required_fields = {
        pointer.removeprefix("/")
        for pointer in phase["phase_receipt_required_fields"]
        if pointer.count("/") == 1
    }
    if not required_fields <= set(receipt):
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
        raise ValueError("statement receipt proposes an invalid worker handoff")
    if receipt["first_failed_gate"] != "S02-EXACT-TARGET":
        raise ValueError("statement receipt first failed gate mismatch")
    if receipt["statement_fingerprints"] != []:
        raise ValueError("statement receipt invents a fingerprint")
    if any(row["passed"] is not False for row in receipt["mutation_tests"]):
        raise ValueError("statement receipt falsely passes a mutation")
    if receipt["audit_complete"] is not False or receipt["theorem_complete"] is not False:
        raise ValueError("statement receipt overclaims a terminal decision")
    validator_binding = receipt["inputs"].get("statement_validator")
    if not isinstance(validator_binding, dict):
        raise ValueError("receipt lacks its validator binding")
    if validator_binding.get("base_tracking_state") != "new candidate in this worker delta":
        raise ValueError("receipt hides the validator's current-base tracking boundary")

    for role, relative in {
        "statement_record": f"Stage1_Instances/{THEOREM_ID}/statement.json",
        "statement_source": f"Stage1_Instances/{THEOREM_ID}/Statement.lean",
        "source_crosswalk": f"Stage1_Instances/{THEOREM_ID}/source-statement-crosswalk.md",
    }.items():
        if not binding_matches(receipt["artifact_bindings"].get(role), relative):
            raise ValueError(f"receipt binding is stale for {role}")
    own_binding = receipt["artifact_bindings"].get("phase_receipt")
    if not isinstance(own_binding, dict) or own_binding.get("path") != f"Stage1_Instances/{THEOREM_ID}/statement-receipt.json":
        raise ValueError("receipt does not identify its scheduler-bound self-reference")
    if own_binding.get("sha256") is not None or own_binding.get("git_blob") is not None:
        raise ValueError("worker cannot content-bind a self-referential receipt")


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
    print(
        json.dumps(
            semantic_result(
                message=(
                    "The target-owned packet truthfully establishes that the Shimura-curve "
                    "topic has no source-selected exact Lean proposition; statement acceptance "
                    "remains blocked."
                )
            ),
            sort_keys=True,
            separators=(",", ":"),
        )
    )


if __name__ == "__main__":
    main()
