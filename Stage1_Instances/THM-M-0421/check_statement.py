#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0421 statement packet."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0421"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0421-STATEMENT"
THEOREM_ID = "THM-M-0421"
BASE_REVISION = "94009a6bebd743588e09c3b45bfbf18bf9b5c5e3"
BASE_TREE = "daabee9f9b2c6e98d84b6290f78a209b950485fc"
GRAPH_SHA256 = "eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
CONTRACT_GIT_BLOB = "84b92df9eaf457ab954b652c3f20f4d513cf0a88"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROBE_STDOUT_SHA256 = "b9e99e1d894ff26ab388e8e2ae00e8290224713048d113853bb28379ae6c6a99"
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
DIRECT_IMPORTS = (
    "Mathlib.FieldTheory.Galois.Basic",
    "Mathlib.NumberTheory.LocalField.Basic",
)
EXPECTED_OWNED_SHA256 = {
    "Statement.lean": "44d82c5dd0889c993b56a6efbedeb877446404dbb0022aa6e88942c94251f0c5",
    "dependency-reuse-ledger.json": "2528ded0fb35ab41dbb2306d87cbc732f183023614b2519fb59dbc23b895a226",
    "source_statement_crosswalk.md": "58471d3c370f2dce835542bdec1ae0417a188109e8a638e8343e834ec7baa72b",
    "statement-blocker.md": "066c23d7d44fcd76f955897f2fbd58ff67cd7754e09fb787b5b4a950de095561",
    "statement.json": "3d7743d5cb8d8f43cd8020fe02260a83248acebbb03bfac98f3116afc3cc4a42",
}
EXPECTED_CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0421/Statement.lean",
    "Stage1_Instances/THM-M-0421/check_statement.py",
    "Stage1_Instances/THM-M-0421/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0421/source_statement_crosswalk.md",
    "Stage1_Instances/THM-M-0421/statement-blocker.md",
    "Stage1_Instances/THM-M-0421/statement-receipt.json",
    "Stage1_Instances/THM-M-0421/statement.json",
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
    "first_failed_gate": "S02-EXACT-TARGET.exact_source_statement_identity",
    "open_obligations": 4,
    "stale_inputs": [],
    "blocked": True,
    "message": "No admitted source selects one exact local-class-field-theory proposition.",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
    r"^\s*(?:axiom|constant|opaque|unsafe|extern)\b",
    re.MULTILINE,
)


if not __debug__:
    raise RuntimeError("statement validation requires Python assertions")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


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
        raise ValueError(f"{path} is not a JSON object")
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if result.returncode != 0:
        raise ValueError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def pointer(document: dict[str, Any], raw: str) -> Any:
    value: Any = document
    for component in raw.removeprefix("/").split("/"):
        if not isinstance(value, dict) or component not in value:
            raise ValueError(f"missing receipt pointer {raw}")
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
        raise ValueError("unclosed Lean comment or string")
    return "".join(output)


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "TZ": "UTC"})
    return subprocess.run(
        ["lake", "env", "lean", str(path)], cwd=LEAN_ROOT, env=environment,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=120, check=False,
    )


def validate_import_deletions(source: str) -> None:
    for module in DIRECT_IMPORTS:
        candidate = source.replace(f"import {module}\n", "", 1)
        with tempfile.NamedTemporaryFile(
            "w", suffix=".lean", encoding="utf-8", dir=os.environ.get("TMPDIR", "/tmp"),
            delete=False,
        ) as handle:
            handle.write(candidate)
            path = Path(handle.name)
        try:
            result = run_lean(path)
        finally:
            path.unlink()
        if result.returncode == 0:
            raise ValueError(f"negative-probe import is redundant: {module}")


def validate() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION:
        raise ValueError("repository HEAD differs from worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("repository base tree differs from worker receipt")

    contract_path = ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json"
    contract = load(contract_path)
    if sha256(contract_path) != CONTRACT_SHA256 or git("hash-object", str(contract_path)) != CONTRACT_GIT_BLOB:
        raise ValueError("phase contract bytes changed")
    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    if phase["raw_blocked_can_close_phase"] is not False:
        raise ValueError("statement blocker unexpectedly closes the phase")
    if phase["classified_negative_findings_may_satisfy_deliverable"] is not False:
        raise ValueError("negative statement evidence unexpectedly satisfies the deliverable")
    if tuple(phase["phase_receipt_required_fields"]) != REQUIRED_RECEIPT_POINTERS:
        raise ValueError("statement receipt contract changed")
    roles = {row["role"]: row for row in phase["required_artifact_roles"]}
    selected = {
        "statement_record": "Stage1_Instances/THM-M-0421/statement.json",
        "statement_source": "Stage1_Instances/THM-M-0421/Statement.lean",
        "source_crosswalk": "Stage1_Instances/THM-M-0421/source_statement_crosswalk.md",
        "phase_receipt": "Stage1_Instances/THM-M-0421/statement-receipt.json",
    }
    for role, expected in selected.items():
        candidates = [path.format(theorem_id=THEOREM_ID) for path in roles[role]["path_candidates"]]
        if expected not in candidates or sum((ROOT / path).is_file() for path in candidates) != 1:
            raise ValueError(f"contract role is missing or ambiguous: {role}")
    validator_candidates = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
    ]
    if validator_candidates != [
        "Stage1_Instances/THM-M-0421/check_statement.py",
        "Stage1_Instances/THM-M-0421/check_statement_artifacts.py",
    ] or sum((ROOT / path).is_file() for path in validator_candidates) != 1:
        raise ValueError("statement validator candidate is missing or ambiguous")

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    item_line = next(row for row in blueprint.splitlines() if f"`{ITEM_ID}`" in row)
    if not item_line.startswith("- [ ]") or "{attempts=0}" not in item_line:
        raise ValueError("authoritative statement state or attempts changed")
    if "Depends: `S56-M-0421-INTAKE`" not in blueprint:
        raise ValueError("statement predecessor changed")

    dag_path = ROOT / "Docs/Stage1_Theorem_DAG_v2.json"
    dag = load(dag_path)
    if sha256(dag_path) != GRAPH_SHA256:
        raise ValueError("theorem DAG digest changed")
    node = next(row for row in dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    if node["v2_execution_rank"] != 302 or node["topological_layer"] != 0:
        raise ValueError("v2 claim order changed")
    if node["phase_states"]["intake"] != "[_]" or node["phase_states"]["statement"] != "[ ]":
        raise ValueError("authoritative phase states changed")
    if node["dependency_context_sha256"] != CONTEXT_SHA256:
        raise ValueError("dependency context changed")
    for field in (
        "direct_hard_parents", "transitive_hard_ancestors",
        "direct_reuse_hint_ids", "shared_lemma_group_ids",
    ):
        if node[field] != []:
            raise ValueError(f"declared empty dependency field changed: {field}")

    ledger = load(HERE / "dependency-reuse-ledger.json")
    if ledger != {
        "schema_version": "stage1-dependency-reuse-ledger/1.1",
        "consumer_theorem_id": THEOREM_ID,
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
        raise ValueError("empty dependency-reuse ledger changed")

    for name, expected in EXPECTED_OWNED_SHA256.items():
        if sha256(HERE / name) != expected:
            raise ValueError(f"owned statement input drifted: {name}")

    statement = load(HERE / "statement.json")
    if statement["item_id"] != ITEM_ID or statement["theorem_id"] != THEOREM_ID:
        raise ValueError("statement identity changed")
    if statement["canonical_statement"] is not None:
        raise ValueError("statement record invents a canonical human claim")
    formal = statement["canonical_formal_target"]
    for field in ("declaration_or_expression", "elaborated_expression_sha256", "environment_fingerprint"):
        if formal[field] is not None:
            raise ValueError(f"statement record invents canonical target field {field}")
    if statement["statement_fingerprints"] != [] or statement["checked_alternate_encodings"] != []:
        raise ValueError("statement record invents fingerprints or transports")
    if statement["direct_imports"] != list(DIRECT_IMPORTS):
        raise ValueError("negative-probe import inventory changed")
    if statement["statement_elaborated"] is not False or statement["phase_predicate_proven"] is not False:
        raise ValueError("statement record overclaims elaboration or the phase predicate")
    if statement["phase_accepted"] is not False or statement["audit_complete"] is not False:
        raise ValueError("statement record overclaims phase or audit acceptance")
    if statement["theorem_complete"] is not False:
        raise ValueError("statement record overclaims theorem completion")
    if set(statement["mutation_tests"].values()) != {"not_run_no_canonical_target"}:
        raise ValueError("statement record falsely claims a mutation result")

    source_path = HERE / "Statement.lean"
    source = source_path.read_text(encoding="utf-8")
    imports = tuple(re.findall(r"^import ([^\s]+)$", source, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        raise ValueError("negative-probe imports changed")
    code = lean_source_without_comments(source)
    if re.search(r"^\s*(?:theorem|lemma|def|abbrev|structure|class|instance)\b", code, re.MULTILINE):
        raise ValueError("negative probe unexpectedly declares a target or support declaration")
    if PROHIBITED.search(code):
        raise ValueError("negative probe contains a prohibited construct")
    for symbol in ("IsNonarchimedeanLocalField", "IsGalois", "Algebra.norm", "OpenSubgroup"):
        if f"#check {symbol}" not in source:
            raise ValueError(f"negative probe no longer checks {symbol}")
    result = run_lean(source_path)
    if result.returncode != 0:
        raise ValueError(f"negative Lean probe failed: {result.stdout}{result.stderr}")
    if hashlib.sha256(result.stdout.encode()).hexdigest() != PROBE_STDOUT_SHA256:
        raise ValueError("negative Lean probe stdout changed")
    if hashlib.sha256(result.stderr.encode()).hexdigest() != EMPTY_SHA256:
        raise ValueError("negative Lean probe stderr changed")
    validate_import_deletions(source)

    version = subprocess.run(
        ["lake", "env", "lean", "--version"], cwd=LEAN_ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if version.returncode != 0 or LEAN_COMMIT not in version.stdout:
        raise ValueError("Lean toolchain identity changed")
    mathlib = LEAN_ROOT / ".lake/packages/mathlib"
    if git("rev-parse", "HEAD", cwd=mathlib) != MATHLIB_REVISION:
        raise ValueError("mathlib revision changed")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != MATHLIB_TREE:
        raise ValueError("mathlib tree changed")
    if git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) != "":
        raise ValueError("pinned mathlib worktree is dirty")

    receipt = load(HERE / "statement-receipt.json")
    for raw in REQUIRED_RECEIPT_POINTERS:
        pointer(receipt, raw)
    if receipt["schema_version"] != "stage1-node-receipt/1.0":
        raise ValueError("receipt schema changed")
    if (receipt["item_id"], receipt["theorem_id"], receipt["phase"], receipt["intent"]) != (
        ITEM_ID, THEOREM_ID, "statement", "audit",
    ):
        raise ValueError("receipt identity changed")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        raise ValueError("receipt base identity changed")
    if receipt["support_state"] != "provisional_worker_selftest_blocked":
        raise ValueError("receipt support state changed")
    if receipt["proposed_state"] != "[_]" or receipt["accepted"] is not False:
        raise ValueError("receipt acceptance boundary changed")
    if receipt["verdict"] != "blocked" or receipt["worker_verdict"] != "blocked":
        raise ValueError("receipt worker verdict changed")
    if receipt["selftest_status"] != "passed" or receipt["selftest_result"]["exit_code"] != 0:
        raise ValueError("receipt self-test status changed")
    if receipt["phase_predicate_proven"] is not False or receipt["phase_accepted"] is not False:
        raise ValueError("receipt overclaims the statement predicate")
    if receipt["audit_complete"] is not False or receipt["theorem_complete"] is not False:
        raise ValueError("receipt overclaims a terminal decision")
    if receipt["statement_fingerprints"] != []:
        raise ValueError("receipt invents a statement fingerprint")
    if set(receipt["mutation_tests"].values()) != {"not_run_no_canonical_target"}:
        raise ValueError("receipt falsely claims a mutation result")
    if receipt["first_failed_gate"] != SEMANTIC_RESULT["first_failed_gate"]:
        raise ValueError("receipt failed-gate identity changed")
    if set(receipt["changed_paths"]) != EXPECTED_CHANGED_PATHS:
        raise ValueError("receipt changed-path inventory changed")
    if receipt["dependency_context"]["parent_inspection_order"] != []:
        raise ValueError("receipt invents a parent inspection")

    selected_artifacts = {row["role"]: row for row in receipt["selected_artifacts"]}
    if set(selected_artifacts) != {
        "statement_record", "statement_source", "source_crosswalk", "phase_receipt"
    }:
        raise ValueError("receipt selected-artifact roles changed")
    for role in ("statement_record", "statement_source", "source_crosswalk"):
        binding = selected_artifacts[role]
        path = ROOT / binding["path"]
        if binding["sha256"] != sha256(path) or binding["git_blob"] != git_blob(path):
            raise ValueError(f"receipt selected-artifact binding changed: {role}")
    phase_receipt = selected_artifacts["phase_receipt"]
    if phase_receipt["path"] != "Stage1_Instances/THM-M-0421/statement-receipt.json":
        raise ValueError("phase-receipt selected path changed")
    if phase_receipt["sha256"] is not None or phase_receipt["git_blob"] is not None:
        raise ValueError("receipt recursively claims its own bytes")
    for binding in receipt["inputs"].values():
        path = ROOT / binding["path"]
        if binding["sha256"] != sha256(path) or binding["git_blob"] != git_blob(path):
            raise ValueError(f"receipt input binding changed: {binding['path']}")

    packet = load(ROOT / ".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id", "worker_verdict", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }:
        raise ValueError("worker handoff fields changed")
    if packet["item_id"] != ITEM_ID or packet["worker_verdict"] != "blocked":
        raise ValueError("worker handoff identity changed")
    if packet["base_revision"] != BASE_REVISION or packet["state"] != "[_]":
        raise ValueError("worker handoff base or state changed")
    if set(packet["changed_paths"]) != EXPECTED_CHANGED_PATHS:
        raise ValueError("worker handoff changed-path inventory changed")
    if packet["commands"] != receipt["selftest_result"]["commands"]:
        raise ValueError("worker handoff commands differ from receipt")
    if packet["known_failures"] != receipt["known_failures"]:
        raise ValueError("worker handoff failures differ from receipt")
    if packet["output_summary"] != receipt["output_summary"]:
        raise ValueError("worker handoff summary differs from receipt")

    for relative in EXPECTED_CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            raise ValueError(f"artifact formatting changed: {relative}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            raise ValueError(f"artifact contains trailing whitespace: {relative}")


def main() -> None:
    try:
        validate()
    except Exception as exc:
        traceback.print_exc(file=sys.stderr)
        failure = dict(SEMANTIC_RESULT)
        failure.update({
            "status": "failed",
            "verdict": "repair_required",
            "first_failed_gate": "VALIDATOR-INTERNAL-CONSISTENCY",
            "blocked": False,
            "message": f"Validator consistency failure: {type(exc).__name__}: {exc}",
        })
        print(json.dumps(failure, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    print(json.dumps(SEMANTIC_RESULT, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
