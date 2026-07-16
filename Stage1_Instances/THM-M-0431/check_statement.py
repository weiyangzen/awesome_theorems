#!/usr/bin/env python3
"""Validate the truthful negative statement packet for THM-M-0431."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0431"
LEAN_DIR = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0431-STATEMENT"
THEOREM_ID = "THM-M-0431"
BASE_REVISION = "94009a6bebd743588e09c3b45bfbf18bf9b5c5e3"
BASE_TREE = "daabee9f9b2c6e98d84b6290f78a209b950485fc"
GRAPH_SHA256 = "eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
SOURCE_SHA256 = "5b08c5e097e3fead10df0d1841d4ada028a75ac7664a8acc423b25808a6d10a9"
EXPECTED_OWNED_SHA256 = {
    "Statement.lean": SOURCE_SHA256,
    "statement.json": "2ee0cd02a5cc4716912cc1512b7f573f60fe186d85b47b297dc464c836c4d003",
    "source_statement_crosswalk.md": "1bb887cdcb0c5ba1d9799cf2710b7d5300885f9cb78bad7482c427623cfe286a",
    "dependency-reuse-ledger.json": "91035a0bcf26c251c4b193db1f56369d56f750824f210247f1d918f1b6ff96ca",
    "statement-blocker.md": "27a45e07ea7d635632d4143a9575d2dba8eba98b099c6b4705b5273c13f91b0c",
}
DIRECT_IMPORTS = {
    "Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic": (
        "ff27602d6ad45c3c8608143aac680ec19fbb15e5298669dfc8e696322c743f6c"
    ),
    "Mathlib.NumberTheory.LocalField.Basic": (
        "9036b0e9502699785330486ca2fcae7fc23944abeb0a9a947ce288d9e2c8fed8"
    ),
    "Mathlib.RepresentationTheory.Basic": (
        "096a215fb48039b61bcb195b05a24b4271fb003d327d14e738bf873437aa95ad"
    ),
}
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0431/Statement.lean",
    "Stage1_Instances/THM-M-0431/check_statement.py",
    "Stage1_Instances/THM-M-0431/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0431/source_statement_crosswalk.md",
    "Stage1_Instances/THM-M-0431/statement-blocker.md",
    "Stage1_Instances/THM-M-0431/statement-receipt.json",
    "Stage1_Instances/THM-M-0431/statement.json",
]
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx)\b|^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
    re.MULTILINE,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    framed = f"blob {len(data)}\0".encode("ascii") + data
    return hashlib.sha1(framed).hexdigest()


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
        raise ValueError(f"{path.relative_to(ROOT)} is not a JSON object")
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


def run_lean() -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "TZ": "UTC"})
    return subprocess.run(
        [
            "lake",
            "env",
            "lean",
            "--trust=0",
            "../../Stage1_Instances/THM-M-0431/Statement.lean",
        ],
        cwd=LEAN_DIR,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def verify_authority() -> tuple[dict, dict]:
    if sys.flags.optimize != 0:
        raise ValueError("statement validator requires Python assertions")
    if git("rev-parse", "HEAD") != BASE_REVISION:
        raise ValueError("repository HEAD differs from the worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("repository base tree differs from the receipt")
    if sha256(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") != GRAPH_SHA256:
        raise ValueError("v2 theorem DAG digest drifted")
    if sha256(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") != CONTRACT_SHA256:
        raise ValueError("phase acceptance contract digest drifted")

    dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    if node["v2_execution_rank"] != 293 or node["dependency_context_sha256"] != CONTEXT_SHA256:
        raise ValueError("target rank or dependency context disagrees")
    for key in (
        "direct_hard_parents",
        "transitive_hard_ancestors",
        "direct_reuse_hint_ids",
        "shared_lemma_group_ids",
    ):
        if node[key] != []:
            raise ValueError(f"declared empty dependency field changed: {key}")

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    intake = re.search(
        r"^- \[(?P<state>.)\] `S56-M-0431-INTAKE`.*\{attempts=(?P<attempts>\d+)\}$",
        blueprint,
        re.MULTILINE,
    )
    statement = re.search(
        r"^- \[(?P<state>.)\] `S56-M-0431-STATEMENT`.*\{attempts=(?P<attempts>\d+)\}$",
        blueprint,
        re.MULTILINE,
    )
    if not intake or (intake.group("state"), intake.group("attempts")) != ("_", "1"):
        raise ValueError("intake predecessor state or attempts changed")
    if not statement or (statement.group("state"), statement.group("attempts")) != (" ", "0"):
        raise ValueError("statement item state or attempts changed")

    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
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
        raise ValueError("statement semantic gates changed")
    return node, phase


def verify_ledger() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    expected_empty = (
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
        raise ValueError("dependency ledger owner mismatch")
    if ledger["observed_theorem_dag_sha256"] != GRAPH_SHA256:
        raise ValueError("dependency ledger graph digest mismatch")
    if ledger["dependency_context_sha256"] != CONTEXT_SHA256:
        raise ValueError("dependency ledger context mismatch")
    if ledger["repository_revision"] != BASE_REVISION:
        raise ValueError("dependency ledger revision mismatch")
    if ledger["claim_order"] != {
        "v2_execution_rank": 293,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        raise ValueError("dependency ledger claim order changed")
    for key in expected_empty:
        if ledger[key] != []:
            raise ValueError(f"empty dependency closure is not empty: {key}")
    if ledger["closure_audit"]["status"] != "empty_declared_context_inspected":
        raise ValueError("empty dependency closure was not marked inspected")


def verify_statement() -> None:
    for name, expected in EXPECTED_OWNED_SHA256.items():
        if sha256(HERE / name) != expected:
            raise ValueError(f"owned statement input drifted: {name}")

    record = load(HERE / "statement.json")
    if record["status"] != "blocked_unfrozen" or record["canonical_human_statement"] is not None:
        raise ValueError("statement record does not preserve the source-identity blocker")
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
        raise ValueError("statement record invents fingerprints or transports")
    if record["phase_predecessor"] != {
        "item_id": "S56-M-0431-INTAKE",
        "authoritative_state": "[_]",
        "attempts": 1,
        "receipt": None,
        "lean_declaration_bodies": [],
        "reusable_artifacts": [],
        "consumption_boundary": (
            "The predecessor dossier was inspected as provisional guidance only. It is not "
            "master accepted and transfers no acceptance or proof credit."
        ),
    }:
        raise ValueError("phase predecessor inspection changed")
    required_mutations = {
        "removed_hypothesis",
        "changed_domain",
        "changed_binder_scope",
        "boundary_case",
    }
    if set(record["mutation_tests"]) != required_mutations:
        raise ValueError("statement mutation inventory is incomplete")
    if any(
        row != {"status": "not_run_missing_canonical_target", "passed": False}
        for row in record["mutation_tests"].values()
    ):
        raise ValueError("statement record falsely claims a mutation result")

    source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    import_lines = re.findall(r"^import (\S+)$", source, re.MULTILINE)
    if import_lines != list(DIRECT_IMPORTS):
        raise ValueError("negative probe imports changed")
    for marker in (
        "#check IsNonarchimedeanLocalField",
        "#check Matrix.GeneralLinearGroup",
        "#check Representation",
    ):
        if source.count(marker) != 1:
            raise ValueError(f"negative probe marker changed: {marker}")
    if re.search(r"^\s*(?:def|theorem)\s+", source, re.MULTILINE):
        raise ValueError("negative probe unexpectedly declares a target or theorem")
    if PROHIBITED.search(source):
        raise ValueError("negative probe contains a prohibited construct")
    for module, expected in DIRECT_IMPORTS.items():
        module_path = LEAN_DIR / ".lake" / "packages" / "mathlib" / (
            module.replace(".", "/") + ".lean"
        )
        if sha256(module_path) != expected:
            raise ValueError(f"pinned import source changed: {module}")
    lean = run_lean()
    if lean.returncode != 0:
        raise ValueError(f"Lean boundary probe failed: {lean.stdout[:500]}")
    for output in ("IsNonarchimedeanLocalField", "Matrix.GeneralLinearGroup", "Representation"):
        if output not in lean.stdout:
            raise ValueError(f"Lean probe output omitted {output}")


def verify_receipt_and_packet() -> None:
    receipt = load(HERE / "statement-receipt.json")
    required = {
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
    if not required.issubset(receipt):
        raise ValueError("statement receipt omits a contract-required field")
    if (
        receipt["schema_version"],
        receipt["item_id"],
        receipt["theorem_id"],
        receipt["phase"],
        receipt["intent"],
    ) != ("stage1-node-receipt/1.0", ITEM_ID, THEOREM_ID, "statement", "audit"):
        raise ValueError("statement receipt identity changed")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        raise ValueError("statement receipt base changed")
    if receipt["verdict"] != "blocked" or receipt["accepted"] is not False:
        raise ValueError("statement receipt overclaims acceptance")
    if (
        receipt["proposed_state"] != "[_]"
        or receipt["support_state"] != "provisional_worker_selftest_blocked"
        or receipt["selftest_status"] != "passed"
        or receipt["selftest_result"].get("exit_code") != 0
        or receipt["selftest_result"].get("phase_predicate_passed") is not False
    ):
        raise ValueError("statement receipt worker boundary changed")
    if receipt["statement_fingerprints"] != [] or any(
        row["passed"] is not False for row in receipt["mutation_tests"]
    ):
        raise ValueError("statement receipt invents positive statement evidence")
    if receipt["audit_complete"] is not False or receipt["theorem_complete"] is not False:
        raise ValueError("statement receipt overclaims a terminal decision")
    if receipt["changed_paths"] != CHANGED_PATHS:
        raise ValueError("statement receipt changed-path inventory changed")
    if receipt["inputs"]["parent_inspection_order"] != []:
        raise ValueError("statement receipt parent inspection order changed")
    if receipt["inputs"]["intake_predecessor"]["authoritative_state"] != "[_]":
        raise ValueError("statement receipt predecessor observation changed")
    if receipt["inputs"]["intake_predecessor"]["acceptance_inherited"] is not False:
        raise ValueError("statement receipt transfers predecessor acceptance")

    bindings = receipt["artifact_bindings"]
    if {row["role"] for row in bindings} != {
        "statement_record",
        "statement_source",
        "source_crosswalk",
    } or len(bindings) != 3:
        raise ValueError("statement receipt artifact roles changed")
    for binding in bindings:
        path = ROOT / binding["path"]
        if sha256(path) != binding["sha256"] or git_blob(path) != binding["git_blob"]:
            raise ValueError(f"statement receipt artifact binding stale: {binding['role']}")
    expected_self = {
        "role": "phase_receipt",
        "path": "Stage1_Instances/THM-M-0431/statement-receipt.json",
        "binding_kind": "git_object_at_integration",
        "expected_sha256": None,
        "expected_git_blob": None,
        "status": "deferred_to_scheduler_master_lane_after_HEAD_tracking",
    }
    if receipt["phase_receipt_self_binding"] != expected_self:
        raise ValueError("phase-receipt self-binding boundary changed")

    packet = load(ROOT / ".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }:
        raise ValueError("worker packet fields changed")
    if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
        raise ValueError("worker packet identity or state changed")
    if packet["base_revision"] != BASE_REVISION or packet["changed_paths"] != CHANGED_PATHS:
        raise ValueError("worker packet base or changed paths changed")
    if packet["commands"] != receipt["selftest_result"]["commands"]:
        raise ValueError("worker packet commands differ from receipt commands")
    if packet["known_failures"] != receipt["known_failures"]:
        raise ValueError("worker packet failures differ from receipt failures")


def semantic_result(*, status: str, verdict: str, gate: str, blocked: bool, message: str) -> dict:
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "phase": "statement",
        "status": status,
        "verdict": verdict,
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": gate,
        "open_obligations": 5,
        "stale_inputs": [],
        "blocked": blocked,
        "message": message,
    }


def main() -> None:
    try:
        verify_authority()
        verify_ledger()
        verify_statement()
        verify_receipt_and_packet()
    except Exception as exc:
        result = semantic_result(
            status="failed",
            verdict="repair_required",
            gate="S01-ARTIFACTS",
            blocked=False,
            message=f"Negative statement packet validation failed: {exc}",
        )
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    result = semantic_result(
        status="blocked",
        verdict="blocked",
        gate="S02-EXACT-TARGET.source_identity_and_object_model",
        blocked=True,
        message=(
            "Negative statement boundary self-tested: the source-selected exact theorem, concrete "
            "object model, expression fingerprint, checked transports, and four mutation classes "
            "remain open; phase acceptance is false."
        ),
    )
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
