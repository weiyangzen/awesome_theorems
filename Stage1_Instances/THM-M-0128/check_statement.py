#!/usr/bin/env python3
"""Validate THM-M-0128's fail-closed statement evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ITEM = "S56-M-0128-STATEMENT"
THEOREM = "THM-M-0128"
BASE_REVISION = "dae1951609072752d49d111bf00e78e4512f2d14"
BASE_TREE = "9d8cc27cc0e09489c78b0bdbdeb57b15c5840f13"
GRAPH_SHA256 = "3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
STATEMENT_SHA256 = "6fe3fb36ed8ed662a05599e39fdc8f8d41bfb7c1732de6b0051ab4eeb18623e4"
RECORD_SHA256 = "42a52d43e71499d657c1de7173226f0b0738f02910d9f2417ee6032ea6cdc5d7"
CROSSWALK_SHA256 = "6b511c1149216fc6d024360c943d7012f69c547691c43821c7e831da2c145251"
LEDGER_SHA256 = "29b0a3e56b7a87f0dc3b047c4534d8620a8915dc107263fffc858af6e7d09deb"
FAILED_GATE = "S02-EXACT-TARGET.exact_source_statement_identity_and_convention_selection"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0128/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0128/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0128/source-statement-crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0128/statement-receipt.json",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|axiom|constant|opaque|unsafe|implemented_by|native_decide)\b"
)


def fail(message: str) -> None:
    raise RuntimeError(message)


def load(relative: str) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate JSON key in {relative}: {key}")
            result[key] = value
        return result

    value = json.loads(
        (ROOT / relative).read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicates,
    )
    if not isinstance(value, dict):
        fail(f"{relative} must contain one JSON object")
    return value


def sha256(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def git_blob(relative: str) -> str:
    data = (ROOT / relative).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def check() -> None:
    source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    record = load(ROLE_PATHS["statement_record"])
    receipt = load(ROLE_PATHS["phase_receipt"])
    ledger = load("Stage1_Instances/THM-M-0128/dependency-reuse-ledger.json")
    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")
    theorem_dag = load("Docs/Stage1_Theorem_DAG_v2.json")

    if sha256("Docs/Stage1_Phase_Acceptance_Contracts.json") != CONTRACT_SHA256:
        fail("phase contract changed")
    if sha256("Docs/Stage1_Theorem_DAG_v2.json") != GRAPH_SHA256:
        fail("theorem DAG changed")
    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    if phase["intent"] != "audit" or phase["raw_blocked_can_close_phase"] is not False:
        fail("statement blocked semantics changed")
    selected = {}
    for role in phase["required_artifact_roles"]:
        candidates = [
            path.format(theorem_id=THEOREM)
            for path in role["path_candidates"]
            if (ROOT / path.format(theorem_id=THEOREM)).is_file()
        ]
        if len(candidates) != 1:
            fail(f"role {role['role']} does not resolve exactly once")
        selected[role["role"]] = candidates[0]
    if selected != ROLE_PATHS:
        fail("selected statement roles changed")
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM)).is_file()
    ]
    if validators != ["Stage1_Instances/THM-M-0128/check_statement.py"]:
        fail("validator candidate is missing or ambiguous")

    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM)
    if node["dependency_context_sha256"] != CONTEXT_SHA256:
        fail("dependency context changed")
    if any(
        node[field]
        for field in (
            "direct_hard_parents",
            "transitive_hard_ancestors",
            "direct_reuse_hint_ids",
            "shared_lemma_group_ids",
        )
    ):
        fail("empty dependency closure changed")
    if ledger != {
        "schema_version": "stage1-dependency-reuse-ledger/1.1",
        "consumer_theorem_id": THEOREM,
        "observed_theorem_dag_sha256": GRAPH_SHA256,
        "dependency_context_sha256": CONTEXT_SHA256,
        "repository_revision": BASE_REVISION,
        "direct_parent_ids": [],
        "transitive_ancestor_ids": [],
        "hard_edge_ids": [],
        "reuse_hint_ids": [],
        "shared_group_ids": [],
        "inspections": [],
        "reuse_decisions": [],
        "unresolved_compatibility_obligations": [],
    }:
        fail("dependency ledger is not the exact audited empty context")
    if sha256("Stage1_Instances/THM-M-0128/dependency-reuse-ledger.json") != LEDGER_SHA256:
        fail("dependency ledger bytes changed")

    imports = re.findall(r"^import (\S+)$", source, re.MULTILINE)
    if imports != [
        "Mathlib.NumberTheory.NumberField.AdeleRing",
        "Mathlib.NumberTheory.NumberField.CMField",
    ]:
        fail("substrate imports changed")
    if source.count("#check NumberField.IsCMField") != 1:
        fail("CM-field substrate check changed")
    if source.count("#check NumberField.AdeleRing") != 1:
        fail("adele-ring substrate check changed")
    if re.search(r"^(?:def|theorem|lemma|example)\s+", source, re.MULTILINE):
        fail("Statement.lean must not invent a canonical declaration")
    if PROHIBITED.search(source):
        fail("prohibited Lean construct found")
    if sha256(ROLE_PATHS["statement_source"]) != STATEMENT_SHA256:
        fail("statement source bytes changed")
    if sha256(ROLE_PATHS["statement_record"]) != RECORD_SHA256:
        fail("statement record bytes changed")
    if sha256(ROLE_PATHS["source_crosswalk"]) != CROSSWALK_SHA256:
        fail("source crosswalk bytes changed")

    formal = record["canonical_formal_target"]
    if record["schema_version"] != "stage1-statement/1.0":
        fail("statement record schema changed")
    if record["item_id"] != ITEM or record["theorem_id"] != THEOREM:
        fail("statement record identity changed")
    if record["canonical_statement"] is not None:
        fail("statement record invents a canonical statement")
    if any(
        formal[field] is not None
        for field in (
            "declaration_or_expression",
            "elaborated_expression_sha256",
            "environment_fingerprint_sha256",
        )
    ):
        fail("statement record invents a canonical expression or fingerprint")
    if formal["statement_file_sha256"] != STATEMENT_SHA256:
        fail("statement record source binding changed")
    if record["statement_elaborated"] is not False:
        fail("statement record falsely claims elaboration")
    if record["gate_state"] != "blocked" or record["first_failed_gate"] != FAILED_GATE:
        fail("statement record blocked boundary changed")
    if record["accepted_receipt_ids"] != []:
        fail("statement record invents accepted evidence")
    mutations = record["mutation_tests"]
    if set(mutations) != {
        "removed_hypothesis",
        "changed_domain",
        "changed_binder_scope",
        "boundary_case",
    } or set(mutations.values()) != {"undefined_without_canonical_statement"}:
        fail("undefined mutation boundary changed")

    required_fields = {
        pointer.split("/")[-1]
        for pointer in phase["phase_receipt_required_fields"]
        if pointer.count("/") == 1
    }
    if not required_fields <= set(receipt):
        fail("receipt lacks a contract-required field")
    if receipt["schema_version"] != "stage1-node-receipt/1.0":
        fail("receipt schema changed")
    if receipt["item_id"] != ITEM or receipt["theorem_id"] != THEOREM:
        fail("receipt identity changed")
    if receipt["phase"] != "statement" or receipt["intent"] != "audit":
        fail("receipt phase or intent changed")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        fail("receipt base binding changed")
    if receipt["proposed_state"] != "[_]" or receipt["accepted"] is not False:
        fail("negative receipt does not preserve provisional worker-only state")
    if receipt["verdict"] != "blocked" or receipt["selftest_status"] != "passed":
        fail("negative receipt semantics changed")
    if receipt["selftest_result"]["exit_code"] != 0:
        fail("negative evidence self-test did not pass")
    if not receipt["selftest_result"]["commands"]:
        fail("receipt lacks exact commands")
    if receipt["first_failed_gate"] != FAILED_GATE:
        fail("receipt failed gate changed")
    if receipt["statement_fingerprints"] != []:
        fail("receipt invents a statement fingerprint")
    if receipt["audit_complete"] is not False or receipt["theorem_complete"] is not False:
        fail("receipt falsely closes a terminal gate")
    if receipt["mutation_tests"] != mutations:
        fail("receipt and record mutation boundaries disagree")
    packet = load(".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }:
        fail("worker packet fields are not exact")
    if packet["item_id"] != ITEM or packet["state"] != "[_]":
        fail("worker packet identity or state changed")
    if packet["base_revision"] != BASE_REVISION:
        fail("worker packet base changed")
    if packet["commands"] != receipt["selftest_result"]["commands"]:
        fail("worker packet commands disagree with the receipt")
    if packet["known_failures"] != receipt["known_failures"]:
        fail("worker packet known failures disagree with the receipt")
    if set(packet["changed_paths"]) != {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0128/Statement.lean",
        "Stage1_Instances/THM-M-0128/check_statement.py",
        "Stage1_Instances/THM-M-0128/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0128/statement-blocker.md",
        "Stage1_Instances/THM-M-0128/statement-receipt.json",
        "Stage1_Instances/THM-M-0128/statement.json",
    }:
        fail("worker packet changed-path coverage changed")
    for input_name, relative in (
        ("statement_validator", "Stage1_Instances/THM-M-0128/check_statement.py"),
        ("dependency_reuse_ledger", "Stage1_Instances/THM-M-0128/dependency-reuse-ledger.json"),
    ):
        if receipt["inputs"][input_name] != {
            "path": relative,
            "sha256": sha256(relative),
            "git_blob": git_blob(relative),
        }:
            fail(f"receipt {input_name} input binding is stale")
    bindings = receipt["artifact_bindings"]
    if set(bindings) != set(ROLE_PATHS):
        fail("receipt artifact roles changed")
    for role in ("statement_record", "statement_source", "source_crosswalk"):
        binding = bindings[role]
        relative = ROLE_PATHS[role]
        if binding != {
            "role": role,
            "path": relative,
            "sha256": sha256(relative),
            "git_blob": git_blob(relative),
        }:
            fail(f"receipt {role} binding is stale")
    if bindings["phase_receipt"] != {
        "role": "phase_receipt",
        "path": ROLE_PATHS["phase_receipt"],
        "sha256": "self_referential_excluded",
        "git_blob": "self_referential_excluded",
    }:
        fail("phase receipt self-binding boundary changed")
def main() -> None:
    try:
        check()
    except Exception as exc:
        semantic = {
            "schema_version": "stage1-validator-semantic-result/1.0",
            "item_id": ITEM,
            "theorem_id": THEOREM,
            "phase": "statement",
            "status": "failed",
            "verdict": "repair_required",
            "phase_accepted": False,
            "audit_complete": False,
            "theorem_complete": False,
            "phase_predicate_proven": False,
            "first_failed_gate": "S01-ARTIFACTS.negative_evidence_validation",
            "open_obligations": 5,
            "stale_inputs": [],
            "blocked": False,
            "message": str(exc),
        }
        print(json.dumps(semantic, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)

    semantic = {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "phase": "statement",
        "status": "blocked",
        "verdict": "blocked",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": FAILED_GATE,
        "open_obligations": 5,
        "stale_inputs": [],
        "blocked": True,
        "message": (
            "Negative statement evidence is internally consistent, but no exact source-"
            "authorized proposition, expression fingerprint, checked transports, or mutation "
            "suite exists; S56-M-0128-STATEMENT remains open."
        ),
    }
    print(json.dumps(semantic, ensure_ascii=True, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
