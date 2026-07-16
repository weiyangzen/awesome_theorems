#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0126 statement packet."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import traceback
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0126"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0126-STATEMENT"
THEOREM_ID = "THM-M-0126"
BASE_REVISION = "307c34d30fc3763c82a944a142ae922b48ff18aa"
BASE_TREE = "ef45ba442c71959db78ad146a023bcf32946a53f"
GRAPH_SHA256 = "8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
CONTRACT_GIT_BLOB = "84b92df9eaf457ab954b652c3f20f4d513cf0a88"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
PROBE_STDOUT_SHA256 = "1d36c0c2eba71f0e2ca0e617f00d5cab25408b56dda37c02e789d8b73bae8272"
EXPECTED_CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0126/Statement.lean",
    "Stage1_Instances/THM-M-0126/check_statement.py",
    "Stage1_Instances/THM-M-0126/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0126/source_statement_crosswalk.md",
    "Stage1_Instances/THM-M-0126/statement-blocker.md",
    "Stage1_Instances/THM-M-0126/statement-receipt.json",
    "Stage1_Instances/THM-M-0126/statement.json",
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
    "first_failed_gate": (
        "S02-EXACT-TARGET.exact_source_statement_identity_and_theorem_variant_selection"
    ),
    "open_obligations": 1,
    "stale_inputs": [],
    "blocked": True,
    "message": "The repository does not identify one exact Shimura-curve proposition.",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def load(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, child in pairs:
            assert key not in value, f"duplicate JSON key in {path}: {key}"
            value[key] = child
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, timeout=30, check=False,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def pointer(document: dict[str, Any], raw: str) -> Any:
    value: Any = document
    for component in raw.removeprefix("/").split("/"):
        assert isinstance(value, dict) and component in value, raw
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
    assert depth == 0 and not in_string
    return "".join(output)


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "TZ": "UTC"})
    return subprocess.run(
        ["lake", "env", "lean", str(path)], cwd=LEAN_ROOT, env=environment,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=180, check=False,
    )


def validate_authorities() -> None:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    authority_hashes = {
        "Docs/Stage1_Blueprint_v2.md": (
            "2a5bc7d397e03969aac1a9f8f21b437152b8ef63ef453055acf67857ced628b5"
        ),
        "Docs/Stage1_Blueprint_rev-5.6.md": (
            "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8"
        ),
        "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
        "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
        "Docs/Stage1_Targets_rev-5.6.json": (
            "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
        ),
        "skills/execute-stage1-rev56/SKILL.md": (
            "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454"
        ),
        "Docs/Blueprint_Guidelines.md": (
            "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535"
        ),
        "Formalizations/Lean/lean-toolchain": (
            "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
        ),
        "Formalizations/Lean/lake-manifest.json": (
            "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
        ),
    }
    for relative, digest in authority_hashes.items():
        assert sha256(ROOT / relative) == digest, relative

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    line = next(row for row in blueprint.splitlines() if f"`{ITEM_ID}`" in row)
    assert line.startswith("- [ ]") and "{attempts=0}" in line
    assert "Depends: `S56-M-0126-INTAKE`" in blueprint

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    assert target["execution_rank"] == 45
    assert target["lifecycle_mode"] == "planned"
    assert target["legacy_artifacts_accepted"] is target["theorem_complete"] is False

    graph = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in graph["theorems"] if row["theorem_id"] == THEOREM_ID)
    assert node["v2_execution_rank"] == 279 and node["topological_layer"] == 0
    assert node["phase_states"]["intake"] == "[_]"
    assert node["phase_states"]["statement"] == "[ ]"
    assert node["phase_attempts"]["statement"] == 0
    assert node["dependency_context_sha256"] == CONTEXT_SHA256
    assert node["direct_hard_parents"] == node["transitive_hard_ancestors"] == []
    assert node["direct_reuse_hint_ids"] == node["shared_lemma_group_ids"] == []

    contract_path = ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json"
    contract = load(contract_path)
    assert git_blob(contract_path) == CONTRACT_GIT_BLOB
    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    assert phase["raw_blocked_can_close_phase"] is False
    assert phase["classified_negative_findings_may_satisfy_deliverable"] is False
    assert tuple(phase["phase_receipt_required_fields"]) == REQUIRED_RECEIPT_POINTERS
    selected = {
        "statement_record": "Stage1_Instances/THM-M-0126/statement.json",
        "statement_source": "Stage1_Instances/THM-M-0126/Statement.lean",
        "source_crosswalk": "Stage1_Instances/THM-M-0126/source_statement_crosswalk.md",
        "phase_receipt": "Stage1_Instances/THM-M-0126/statement-receipt.json",
    }
    for role in phase["required_artifact_roles"]:
        candidates = [
            value.format(theorem_id=THEOREM_ID) for value in role["path_candidates"]
            if (ROOT / value.format(theorem_id=THEOREM_ID)).is_file()
        ]
        assert candidates == [selected[role["role"]]], role["role"]
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    assert validators == ["Stage1_Instances/THM-M-0126/check_statement.py"]


def validate_statement_boundary() -> None:
    statement = load(HERE / "statement.json")
    assert statement["schema_version"] == "stage1-statement/1.0"
    assert statement["item_id"] == ITEM_ID and statement["theorem_id"] == THEOREM_ID
    assert statement["claim_order"] == {
        "v2_execution_rank": 279,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }
    assert statement["canonical_statement"] is None
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_sha256"] is None
    assert formal["environment_fingerprint"] is None
    assert statement["direct_imports"] == statement["statement_fingerprints"] == []
    assert statement["statement_elaborated"] is statement["phase_predicate_proven"] is False
    assert statement["phase_accepted"] is statement["audit_complete"] is False
    assert statement["theorem_complete"] is False
    assert set(statement["mutation_tests"].values()) == {"not_run_no_canonical_target"}
    assert statement["dependency_context"]["parent_inspection_order"] == []
    assert statement["dependency_context"]["provider_acceptance_inherited"] is False

    source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    code = lean_source_without_comments(source)
    assert not re.search(r"^\s*import\s", code, re.MULTILINE)
    assert not re.search(
        r"^\s*(?:theorem|lemma|def|abbrev|structure|class|instance|"
        r"axiom|constant|opaque|unsafe|extern)\b",
        code, re.MULTILINE,
    )
    source_result = run_lean(HERE / "Statement.lean")
    assert source_result.returncode == 0, source_result.stdout + source_result.stderr
    assert source_result.stdout == source_result.stderr == ""

    probe_result = run_lean(HERE / "StatementInfrastructure.lean")
    assert probe_result.returncode == 0, probe_result.stdout + probe_result.stderr
    assert hashlib.sha256(probe_result.stdout.encode()).hexdigest() == PROBE_STDOUT_SHA256
    assert hashlib.sha256(probe_result.stderr.encode()).hexdigest() == EMPTY_SHA256
    assert "QuaternionAlgebra" in probe_result.stdout
    assert "AlgebraicGeometry.Scheme" in probe_result.stdout

    legacy = (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_045.lean").read_text(
        encoding="utf-8"
    )
    assert "placeholder propositions" in legacy
    assert "does not assert that mathlib already" in legacy
    assert "RepresentsQuaternionicModuli" in legacy

    version = subprocess.run(
        ["lake", "env", "lean", "--version"], cwd=LEAN_ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=False,
    )
    assert version.returncode == 0 and LEAN_COMMIT in version.stdout
    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""


def validate_ledger_and_packet() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    assert ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1"
    assert ledger["consumer_theorem_id"] == THEOREM_ID
    assert ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256
    assert ledger["dependency_context_sha256"] == CONTEXT_SHA256
    assert ledger["repository_revision"] == BASE_REVISION
    for field in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "inspections", "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        assert ledger[field] == [], field
    assert ledger["closure_audit"]["parent_inspection_order"] == []
    assert ledger["closure_audit"]["provider_acceptance_inherited"] is False

    receipt = load(HERE / "statement-receipt.json")
    for raw in REQUIRED_RECEIPT_POINTERS:
        pointer(receipt, raw)
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == "statement" and receipt["intent"] == "audit"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == "blocked" and receipt["selftest_status"] == "passed"
    assert receipt["phase_predicate_proven"] is receipt["phase_accepted"] is False
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["statement_fingerprints"] == []
    assert set(receipt["mutation_tests"].values()) == {"not_run_no_canonical_target"}
    assert receipt["first_failed_gate"] == SEMANTIC_RESULT["first_failed_gate"]
    assert receipt["selftest_result"]["exit_code"] == 0
    assert receipt["selftest_result"]["commands"]

    selected = {row["role"]: row for row in receipt["selected_artifacts"]}
    assert set(selected) == {
        "statement_record", "statement_source", "source_crosswalk", "phase_receipt"
    }
    for role in ("statement_record", "statement_source", "source_crosswalk"):
        path = ROOT / selected[role]["path"]
        assert selected[role]["sha256"] == sha256(path)
        assert selected[role]["git_blob"] == git_blob(path)
    assert selected["phase_receipt"]["path"] == (
        "Stage1_Instances/THM-M-0126/statement-receipt.json"
    )
    assert selected["phase_receipt"]["sha256"] is None
    assert selected["phase_receipt"]["git_blob"] is None
    for binding in receipt["inputs"].values():
        path = ROOT / binding["path"]
        assert binding["sha256"] == sha256(path), binding["path"]
        assert binding["git_blob"] == git_blob(path), binding["path"]

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "worker_verdict", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["worker_verdict"] == "blocked"
    assert packet["base_revision"] == BASE_REVISION and packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == EXPECTED_CHANGED_PATHS
    assert packet["commands"] == receipt["selftest_result"]["commands"]
    assert packet["commands"] == receipt["commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert receipt["changed_paths"] == packet["changed_paths"]

    actual_changed = set(
        git("diff", "--name-only", "HEAD", "--", "Stage1_Instances/THM-M-0126").splitlines()
    )
    actual_changed.update(
        git("ls-files", "--others", "--exclude-standard", "--", "Stage1_Instances/THM-M-0126").splitlines()
    )
    assert actual_changed == EXPECTED_CHANGED_PATHS - {".stage1-worker-selftest.json"}

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^\s*(?:axiom|constant|opaque|unsafe|extern)\b", re.MULTILINE,
    )
    for path in (HERE / "Statement.lean", HERE / "StatementInfrastructure.lean"):
        code = lean_source_without_comments(path.read_text(encoding="utf-8"))
        assert prohibited.search(code) is None, path
    for relative in EXPECTED_CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def validate() -> None:
    validate_authorities()
    validate_statement_boundary()
    validate_ledger_and_packet()


def main() -> None:
    try:
        validate()
    except Exception as exc:
        traceback.print_exc()
        failure = dict(SEMANTIC_RESULT)
        failure.update({
            "status": "failed",
            "verdict": "repair_required",
            "first_failed_gate": "VALIDATOR-INTERNAL-CONSISTENCY",
            "blocked": False,
            "message": f"Validator consistency failure: {type(exc).__name__}: {exc}",
        })
        print(json.dumps(failure, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    print(json.dumps(SEMANTIC_RESULT, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
