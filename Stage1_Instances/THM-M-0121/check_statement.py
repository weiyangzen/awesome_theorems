#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0121 statement packet."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0121"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0121-STATEMENT"
THEOREM_ID = "THM-M-0121"
BASE_REVISION = "307c34d30fc3763c82a944a142ae922b48ff18aa"
BASE_TREE = "ef45ba442c71959db78ad146a023bcf32946a53f"
GRAPH_SHA256 = "8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
CONTRACT_GIT_BLOB = "84b92df9eaf457ab954b652c3f20f4d513cf0a88"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
LAKE_MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
DIRECT_IMPORT = "Mathlib.AlgebraicGeometry.RationalMap"
DIRECT_IMPORT_SHA256 = "e6de15c0db2a37ca0455976b8e4fd736b9298adc36537daeff06d924c67301ae"
EXPECTED_INPUT_SHA256 = {
    "Statement.lean": "316011057d5f6e0739ba9b0ec380274bad22f5e3404b416d06b96d82caff06ee",
    "statement.json": "8b6ecf569944230a9cd5ecefd8980e93e3dc6b7e4f765d2d7fa78350d61d2177",
    "dependency-reuse-ledger.json": "0b8bb6960497243fc42ba2d435e2f8d2018933550639d7db00ebdfeb7ebb6816",
    "source_statement_crosswalk.md": "468362254e4e51fb92982d5f9bd26b60477614ef823bd2ee85431a8ec03fa0a2",
    "StatementProbe.lean": "1fc64a6366d4a6e5649403a25d3e713fb60566b6d942468b1ac9c4e8580ab651",
    "intake.json": "93df2b7b18460573ea3fcaecd07e498bcf64fba67b784e389bb83f8a7691e43b",
    "statement-blocker.json": "fa620e08e0efe57cb3bc18095330ad70506b4a8b13d06201d2fb9ee06d8b1b62",
    "statement-blocker.md": "c775ea90a4e553ebd9a231b22ddc78b4239453dc1bb31749d0f754ee2cf2a312",
    "statement-phase-blocker-2026-07-17-head-307c34d3-slot61.md":
        "25f26071ff889cde40c48982c688cb931d540dc8f58ff2cd2423dd6ab7ba92a9",
}
EXPECTED_CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0121/Statement.lean",
    "Stage1_Instances/THM-M-0121/check_statement.py",
    "Stage1_Instances/THM-M-0121/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0121/statement-phase-blocker-2026-07-17-head-307c34d3-slot61.md",
    "Stage1_Instances/THM-M-0121/statement-receipt.json",
    "Stage1_Instances/THM-M-0121/statement.json",
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
    "open_obligations": 5,
    "stale_inputs": [],
    "blocked": True,
    "message": (
        "The repository does not select one exact proposition behind the Mori rationality label."
    ),
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


def load(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
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
        ["lake", "env", "lean", str(path)],
        cwd=LEAN_ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )


def validate_authority() -> tuple[dict[str, Any], dict[str, Any]]:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    blueprint_path = ROOT / "Docs" / "Stage1_Blueprint_v2.md"
    blueprint = blueprint_path.read_text(encoding="utf-8")
    line = next(row for row in blueprint.splitlines() if f"`{ITEM_ID}`" in row)
    assert line.startswith("- [ ]") and "{attempts=0}" in line
    assert "Depends: `S56-M-0121-INTAKE`" in blueprint

    graph_path = ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json"
    graph = load(graph_path)
    assert sha256(graph_path) == GRAPH_SHA256
    node = next(row for row in graph["theorems"] if row["theorem_id"] == THEOREM_ID)
    assert node["v2_execution_rank"] == 274
    assert node["phase_states"]["intake"] == "[_]"
    assert node["phase_states"]["statement"] == "[ ]"
    assert node["phase_attempts"]["statement"] == 0
    assert node["topological_layer"] == 0
    assert node["dependency_context_sha256"] == CONTEXT_SHA256
    assert node["direct_hard_parents"] == node["transitive_hard_ancestors"] == []
    assert node["direct_reuse_hint_ids"] == node["shared_lemma_group_ids"] == []

    contract_path = ROOT / "Docs" / "Stage1_Phase_Acceptance_Contracts.json"
    contract = load(contract_path)
    assert sha256(contract_path) == CONTRACT_SHA256
    assert git("hash-object", str(contract_path)) == CONTRACT_GIT_BLOB
    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    assert phase["intent"] == "audit"
    assert phase["raw_blocked_can_close_phase"] is False
    assert phase["classified_negative_findings_may_satisfy_deliverable"] is False
    assert tuple(phase["phase_receipt_required_fields"]) == REQUIRED_RECEIPT_POINTERS
    assert [row["gate_id"] for row in phase["semantic_gates"]] == [
        "S01-ARTIFACTS",
        "S02-EXACT-TARGET",
        "S03-MUTATIONS",
    ]
    assert [row["path_pattern"] for row in phase["validator_candidates"]] == [
        "Stage1_Instances/{theorem_id}/check_statement.py",
        "Stage1_Instances/{theorem_id}/check_statement_artifacts.py",
    ]
    expected_roles = {
        "statement_record": HERE / "statement.json",
        "statement_source": HERE / "Statement.lean",
        "source_crosswalk": HERE / "source_statement_crosswalk.md",
        "phase_receipt": HERE / "statement-receipt.json",
    }
    for role in phase["required_artifact_roles"]:
        candidates = [
            ROOT / path.format(theorem_id=THEOREM_ID) for path in role["path_candidates"]
        ]
        assert expected_roles[role["role"]] in candidates
        assert sum(path.is_file() for path in candidates) == 1
    return node, phase


def validate_ledger() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    assert ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1"
    assert ledger["consumer_theorem_id"] == THEOREM_ID
    assert ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256
    assert ledger["dependency_context_sha256"] == CONTEXT_SHA256
    assert ledger["repository_revision"] == BASE_REVISION
    assert ledger["claim_order"] == {
        "v2_execution_rank": 274,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }
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
        assert ledger[key] == [], key
    closure = ledger["closure_audit"]
    assert closure["inspection_order"] == []
    assert closure["status"] == "empty_declared_context_inspected"


def validate_statement_boundary() -> None:
    for name, expected in EXPECTED_INPUT_SHA256.items():
        assert sha256(HERE / name) == expected, name

    intake = load(HERE / "intake.json")
    formal = intake["canonical_formal_target"]
    assert intake["canonical_statement"] is None
    for field in ("module", "declaration_or_expression", "elaborated_expression_hash", "environment_fingerprint"):
        assert formal[field] is None
    assert formal["gate_state"] == "blocked_pending_source_disambiguation"
    assert intake["theorem_complete"] is False

    statement = load(HERE / "statement.json")
    assert statement["item_id"] == ITEM_ID and statement["theorem_id"] == THEOREM_ID
    assert statement["status"] == "blocked_unfrozen"
    assert statement["canonical_statement"] is None
    target = statement["canonical_formal_target"]
    assert target["module"] == "Stage1_Instances/THM-M-0121/Statement.lean"
    for field in ("declaration_or_expression", "elaborated_expression_sha256", "environment_fingerprint"):
        assert target[field] is None
    assert statement["direct_imports"] == statement["statement_fingerprints"] == []
    assert statement["checked_alternate_encodings"] == []
    assert set(statement["mutation_tests"].values()) == {"not_run_no_canonical_target"}
    assert statement["statement_elaborated"] is statement["phase_predicate_proven"] is False
    assert statement["phase_accepted"] is statement["audit_complete"] is False
    assert statement["theorem_complete"] is False

    source_path = HERE / "Statement.lean"
    source = source_path.read_text(encoding="utf-8")
    code = lean_source_without_comments(source)
    assert tuple(re.findall(r"^import ([^\s]+)$", code, re.MULTILINE)) == (DIRECT_IMPORT,)
    assert not re.search(
        r"^\s*(?:theorem|lemma|def|abbrev|structure|class|instance|axiom|constant|opaque|unsafe|extern)\b",
        code,
        re.MULTILINE,
    )
    assert PROHIBITED.search(code) is None
    assert tuple(re.findall(r"^#check ([^\n]+)$", code, re.MULTILINE)) == (
        "Scheme.RationalMap",
        "Scheme.RationalMap.domain",
        "Scheme.RationalMap.equivFunctionField",
    )
    result = run_lean(source_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.count("AlgebraicGeometry.Scheme.RationalMap") >= 3

    probe_source = (HERE / "StatementProbe.lean").read_text(encoding="utf-8")
    assert PROHIBITED.search(lean_source_without_comments(probe_source)) is None
    probe = run_lean(HERE / "StatementProbe.lean")
    assert probe.returncode == 0, probe.stdout + probe.stderr
    assert probe.stdout.count("AlgebraicGeometry.Scheme.RationalMap") >= 3

    version = subprocess.run(
        ["lake", "env", "lean", "--version"],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert version.returncode == 0 and LEAN_COMMIT in version.stdout
    assert (LEAN_ROOT / "lean-toolchain").read_text(encoding="utf-8").strip() == LEAN_TOOLCHAIN
    assert sha256(LEAN_ROOT / "lean-toolchain") == LEAN_TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == LAKE_MANIFEST_SHA256
    manifest = load(LEAN_ROOT / "lake-manifest.json")
    assert next(row["rev"] for row in manifest["packages"] if row["name"] == "mathlib") == MATHLIB_REVISION
    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""
    import_path = mathlib / "Mathlib" / "AlgebraicGeometry" / "RationalMap.lean"
    assert sha256(import_path) == DIRECT_IMPORT_SHA256

    combined = (
        (HERE / "source_statement_crosswalk.md").read_text(encoding="utf-8")
        + "\n"
        + (HERE / "statement-phase-blocker-2026-07-17-head-307c34d3-slot61.md").read_text(encoding="utf-8")
    )
    for term in (
        "Nef-threshold rationality",
        "rational curves",
        "rational connectedness",
        "every Fano\nvariety",
        "MoriRationalityStatementShape",
    ):
        assert term in combined


def validate_receipt() -> None:
    receipt = load(HERE / "statement-receipt.json")
    for raw in REQUIRED_RECEIPT_POINTERS:
        pointer(receipt, raw)
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == "statement" and receipt["intent"] == "audit"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest_blocked"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == receipt["worker_verdict"] == "blocked"
    assert receipt["selftest_status"] == "passed"
    assert receipt["selftest_result"]["exit_code"] == 0
    assert receipt["selftest_result"]["phase_predicate_passed"] is False
    assert receipt["selftest_result"]["commands"]
    assert receipt["phase_predicate_proven"] is receipt["phase_accepted"] is False
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["canonical_formal_target"] is receipt["minimal_imports"] is None
    assert receipt["statement_fingerprints"] == []
    assert set(receipt["mutation_tests"].values()) == {"not_run_no_canonical_target"}
    assert receipt["first_failed_gate"] == SEMANTIC_RESULT["first_failed_gate"]
    assert receipt["claim_order"] == {
        "v2_execution_rank": 274,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }
    assert receipt["dependency_context"]["parent_inspection_order"] == []
    assert receipt["dependency_context"]["provider_acceptance_inherited"] is False

    selected = {row["role"]: row for row in receipt["selected_artifacts"]}
    assert set(selected) == {"statement_record", "statement_source", "source_crosswalk", "phase_receipt"}
    for role in ("statement_record", "statement_source", "source_crosswalk"):
        binding = selected[role]
        path = ROOT / binding["path"]
        assert binding["sha256"] == sha256(path)
        assert binding["git_blob"] == git("hash-object", str(path))
    self_binding = selected["phase_receipt"]
    assert self_binding["path"] == "Stage1_Instances/THM-M-0121/statement-receipt.json"
    assert self_binding["sha256"] is self_binding["git_blob"] is None
    for binding in receipt["inputs"].values():
        path = ROOT / binding["path"]
        assert binding["sha256"] == sha256(path)
        assert binding["git_blob"] == git("hash-object", str(path))

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id",
        "worker_verdict",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["worker_verdict"] == "blocked"
    assert packet["base_revision"] == BASE_REVISION and packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == EXPECTED_CHANGED_PATHS
    assert packet["commands"] == receipt["selftest_result"]["commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["selftest_result"]["output_summary"]

    changed = {".stage1-worker-selftest.json"}
    for line in git("status", "--porcelain=v1", "--untracked-files=all").splitlines():
        path = line[3:] if line[:2] == "??" else line[2:].lstrip()
        if path == "Formalizations/Lean/.lake":
            continue
        if path == ".stage1-worker-selftest.json":
            continue
        assert path.startswith(f"Stage1_Instances/{THEOREM_ID}/"), path
        changed.add(path)
    assert changed == EXPECTED_CHANGED_PATHS
    for relative in EXPECTED_CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    try:
        validate_authority()
        validate_ledger()
        validate_statement_boundary()
        validate_receipt()
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
        print(json.dumps(failure, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    print(json.dumps(SEMANTIC_RESULT, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
