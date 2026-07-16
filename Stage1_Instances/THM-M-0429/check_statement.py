#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0429 statement boundary."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0429"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
LAKE = Path.home() / ".elan" / "bin" / "lake"
ITEM_ID = "S56-M-0429-STATEMENT"
THEOREM_ID = "THM-M-0429"
BASE_REVISION = "94009a6bebd743588e09c3b45bfbf18bf9b5c5e3"
BASE_TREE = "daabee9f9b2c6e98d84b6290f78a209b950485fc"
GRAPH_SHA256 = "eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153"
CONTEXT_SHA256 = "ad0389ffad83587050de416b510bdf7bc9d5c045a9b95371702b155ccb2d606e"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
CONTRACT_GIT_BLOB = "84b92df9eaf457ab954b652c3f20f4d513cf0a88"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
FIRST_GATE = "S02-EXACT-TARGET.missing_concrete_source_faithful_artin_l_function_definition"
EXPECTED_CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0429/Statement.lean",
    "Stage1_Instances/THM-M-0429/check_statement.py",
    "Stage1_Instances/THM-M-0429/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0429/statement-blocker.json",
    "Stage1_Instances/THM-M-0429/statement-contract-blocker.md",
    "Stage1_Instances/THM-M-0429/statement-receipt.json",
    "Stage1_Instances/THM-M-0429/statement.json",
}
REQUIRED_RECEIPT_POINTERS = (
    "/schema_version", "/receipt_id", "/item_id", "/theorem_id", "/phase",
    "/intent", "/base_revision", "/base_tree", "/inputs", "/support_state",
    "/proposed_state", "/accepted", "/verdict", "/selftest_status",
    "/selftest_result/exit_code", "/selftest_result/commands", "/known_failures",
    "/first_failed_gate", "/retry_condition", "/status_boundary", "/audit_complete",
    "/theorem_complete", "/invalidation_inputs", "/statement_fingerprints",
    "/mutation_tests",
)
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0429/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0429/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0429/source_statement_crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0429/statement-receipt.json",
}
ROLE_HASHES = {
    "statement_record": "5f5d59dd68d5d60dd0b818fc34492dece8da71a318452283122e8446a3208532",
    "statement_source": "71fd743491c661b4a808db66c2ac61394d7c887359905e4a89eac0f2d53b4312",
    "source_crosswalk": "7fe9b20d186b9a05365c8cdd0de84deb9ace9b380f1e3f8a01bb52df0643c7da",
}
ROLE_BLOBS = {
    "statement_record": "54dc1ba55c1940ea2ea4823c78763c0d704f70e1",
    "statement_source": "7ef50b5af810f59c1b3b3b4dd6ed5045e489973b",
    "source_crosswalk": "736a2d6364d2210100270d083a8d8c95d6a2a9d0",
}
AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": "f7f8bcf307b737c56eb7ebc77fa2192046dc07b27ce58df5876ba4fdc4f1d7fb",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "skills/execute-stage1-rev56/SKILL.md": "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_082.lean": "56e7ee6e2408e62615a5f58df9495315abbf642aa7a7d178e8491be0688ca744",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
}
SUPPORT_HASHES = {
    "Stage1_Instances/THM-M-0429/dependency-reuse-ledger.json": "65c264a3d56685242699c1f0ef6ddc83edb84e1fab3b0265cb97989982e48778",
    "Stage1_Instances/THM-M-0429/statement-blocker.json": "f7b63c8d99bec71890781c6d824d80f668c2cf7967bbd550a7d543b78bc040bc",
    "Stage1_Instances/THM-M-0429/statement-contract-blocker.md": "0ab6d980c1b45062461885ce76cd1df66afd2e202759fdc9bcbf31a1470cf602",
}
PROVIDER_HASHES = {
    "Stage1_Instances/THM-M-0075/instance.json": "cc39055cd5ef3ef6ea6b56a6e860766cd1dbfed7382ed866488794c64e69357f",
    "Stage1_Instances/THM-M-0075/IntakeProbe.lean": "70b74e9eb5e74521af2881a00e67d3642b64399b58a142cab23c517e3e2181e4",
    "Stage1_Instances/THM-M-0075/intake-receipt.json": "ece8edcd2bfec91c4b874df666c2cb902631dbfa88610aa68335fd9a599fb2ce",
    "Stage1_Instances/THM-M-0075/task-dag.json": "fcafda0bdbd9ebd1ef94917fc8ac334170d508c6bd798299a1725f9c6a06bfb4",
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
    "first_failed_gate": FIRST_GATE,
    "open_obligations": 1,
    "stale_inputs": [],
    "blocked": True,
    "message": "The pinned environment has no concrete source-faithful Artin L-function target.",
}


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
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False, timeout=30,
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
        [str(LAKE), "env", "lean", str(path)], cwd=LEAN_ROOT, env=environment,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=180, check=False,
    )


def validate_authorities_and_contract() -> None:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for relative, expected in AUTHORITY_HASHES.items():
        path = ROOT / relative
        assert sha256(path) == expected, relative

    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    assert git_blob(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") == CONTRACT_GIT_BLOB
    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    assert phase["raw_blocked_can_close_phase"] is False
    assert phase["classified_negative_findings_may_satisfy_deliverable"] is False
    assert tuple(phase["phase_receipt_required_fields"]) == REQUIRED_RECEIPT_POINTERS
    selected: dict[str, str] = {}
    for role in phase["required_artifact_roles"]:
        candidates = [
            raw.format(theorem_id=THEOREM_ID) for raw in role["path_candidates"]
            if (ROOT / raw.format(theorem_id=THEOREM_ID)).is_file()
        ]
        assert len(candidates) == 1, role["role"]
        selected[role["role"]] = candidates[0]
    assert selected == ROLE_PATHS
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    assert validators == ["Stage1_Instances/THM-M-0429/check_statement.py"]

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    line = next(row for row in blueprint.splitlines() if f"`{ITEM_ID}`" in row)
    assert line.startswith("- [ ]") and "{attempts=0}" in line
    assert "Depends: `S56-M-0429-INTAKE`" in blueprint

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row["id"] == ITEM_ID)
    assert item == {
        "id": ITEM_ID, "theorem_id": THEOREM_ID, "execution_rank": 82,
        "phase": "statement", "layer": 1, "state": "[ ]",
        "depends_on": ["S56-M-0429-INTAKE"],
        "owned_paths": ["Stage1_Instances/THM-M-0429"],
        "deliverable": "Elaborate the exact Lean 4 target with the minimal pinned imports.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    graph = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in graph["theorems"] if row["theorem_id"] == THEOREM_ID)
    assert node["v2_execution_rank"] == 308 and node["topological_layer"] == 0
    assert node["phase_states"]["statement"] == "[ ]"
    assert node["phase_attempts"]["statement"] == 0
    assert node["dependency_context_sha256"] == CONTEXT_SHA256
    assert node["direct_hard_parents"] == node["transitive_hard_ancestors"] == []
    assert node["direct_reuse_hint_ids"] == []
    assert node["shared_lemma_group_ids"] == ["SHARED-MODULE-c40c460949245661"]


def validate_statement_boundary() -> None:
    for role, relative in ROLE_PATHS.items():
        assert (ROOT / relative).is_file(), role
        if role != "phase_receipt":
            assert sha256(ROOT / relative) == ROLE_HASHES[role]
            assert git_blob(ROOT / relative) == ROLE_BLOBS[role]
    for relative, expected in SUPPORT_HASHES.items():
        assert sha256(ROOT / relative) == expected, relative

    statement = load(ROOT / ROLE_PATHS["statement_record"])
    assert statement["item_id"] == ITEM_ID and statement["theorem_id"] == THEOREM_ID
    assert statement["canonical_statement"].startswith("For a finite Galois extension")
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_sha256"] is None
    assert formal["environment_fingerprint"] is None
    assert statement["direct_imports"] == statement["statement_fingerprints"] == []
    assert statement["statement_elaborated"] is statement["phase_predicate_proven"] is False
    assert statement["phase_accepted"] is statement["audit_complete"] is False
    assert statement["theorem_complete"] is False
    assert set(statement["mutation_tests"].values()) == {"not_run_no_canonical_target"}
    assert statement["first_failed_gate"] == FIRST_GATE

    source = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    code = lean_source_without_comments(source)
    assert not re.search(r"^\s*import\s", code, re.MULTILINE)
    assert not re.search(
        r"^\s*(?:theorem|lemma|def|abbrev|structure|class|instance|axiom|constant|opaque|unsafe|extern)\b",
        code, re.MULTILINE,
    )
    result = run_lean(ROOT / ROLE_PATHS["statement_source"])
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout == result.stderr == ""

    legacy = (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_082.lean").read_text(
        encoding="utf-8"
    )
    for marker in (
        "structure ArtinLFunctionData", "artinLFunction :", "galoisExtensionModel : Prop",
        "eulerProductMatchesRepresentation : Prop", "brauerInductionReduction : Prop",
        "abelianLFunctionContinuationInputs : Prop", "def StatementShape : Prop",
        "This is a statement-shape candidate, not a proof of Brauer's theorem.",
    ):
        assert marker in legacy
    legacy_result = run_lean(
        ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_082.lean"
    )
    assert legacy_result.returncode == 0, legacy_result.stdout + legacy_result.stderr

    blocker = load(HERE / "statement-blocker.json")
    assert blocker["base_revision"] == BASE_REVISION and blocker["base_tree"] == BASE_TREE
    assert blocker["first_failed_gate"] == FIRST_GATE
    assert blocker["statement_gate_passed"] is blocker["statement_elaborated"] is False
    assert blocker["statement_accepted"] is blocker["audit_complete"] is False
    assert blocker["theorem_complete"] is False
    assert blocker["canonical_formal_target"] is blocker["minimal_imports"] is None
    assert blocker["statement_fingerprints"] == []
    assert blocker["dependency_context"]["parent_inspection_order"] == []


def validate_dependency_ledger() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    assert ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1"
    assert ledger["consumer_theorem_id"] == THEOREM_ID
    assert ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256
    assert ledger["dependency_context_sha256"] == CONTEXT_SHA256
    assert ledger["repository_revision"] == BASE_REVISION
    for field in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids", "reuse_hint_ids",
        "parent_inspection_order", "inspections", "unresolved_compatibility_obligations",
    ):
        assert ledger[field] == [], field
    assert ledger["shared_group_ids"] == ["SHARED-MODULE-c40c460949245661"]
    assert len(ledger["reuse_decisions"]) == 1
    decision = ledger["reuse_decisions"][0]
    assert decision["source_id"] == "SHARED-MODULE-c40c460949245661"
    assert decision["provider_theorem_id"] == "THM-M-0075"
    assert decision["decision"] == "not_applicable"
    assert decision["context_digest"] == CONTEXT_SHA256
    assert decision["inspected_member"]["phase_states"] == {
        "intake": "[_]", "statement": "[ ]", "anchor_audit": "[ ]",
        "obligation_tree": "[ ]", "proof": "[ ]", "validation": "[ ]", "release": "[ ]",
    }
    for relative, expected in PROVIDER_HASHES.items():
        assert sha256(ROOT / relative) == expected, relative
        assert decision["inspected_member"]["artifact_digests"][relative] == expected
    assert ledger["closure_audit"]["status"] == "complete_for_observed_context"
    assert ledger["closure_audit"]["parent_inspection_order"] == []
    assert ledger["closure_audit"]["proof_credit_transferred"] is False


def validate_receipt_and_packet() -> None:
    receipt = load(HERE / "statement-receipt.json")
    for raw in REQUIRED_RECEIPT_POINTERS:
        pointer(receipt, raw)
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == "statement" and receipt["intent"] == "audit"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["verdict"] == receipt["worker_verdict"] == "blocked"
    assert receipt["selftest_status"] == "passed"
    assert receipt["phase_predicate_proven"] is receipt["phase_accepted"] is False
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["statement_fingerprints"] == []
    assert set(receipt["mutation_tests"].values()) == {"not_run_no_canonical_target"}
    assert receipt["first_failed_gate"] == FIRST_GATE
    assert receipt["selftest_result"]["exit_code"] == 0
    assert receipt["selftest_result"]["commands"]
    selected = {row["role"]: row for row in receipt["selected_artifacts"]}
    assert set(selected) == set(ROLE_PATHS)
    for role in ("statement_record", "statement_source", "source_crosswalk"):
        assert selected[role]["path"] == ROLE_PATHS[role]
        assert selected[role]["sha256"] == ROLE_HASHES[role]
        assert selected[role]["git_blob"] == ROLE_BLOBS[role]
    assert selected["phase_receipt"]["sha256"] is None
    assert selected["phase_receipt"]["git_blob"] is None
    for binding in receipt["inputs"].values():
        path = ROOT / binding["path"]
        assert sha256(path) == binding["sha256"], binding["path"]
        assert git_blob(path) == binding["git_blob"], binding["path"]

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "worker_verdict", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["worker_verdict"] == "blocked"
    assert packet["base_revision"] == BASE_REVISION and packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == EXPECTED_CHANGED_PATHS
    assert packet["commands"] == receipt["selftest_result"]["commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert receipt["commands"] == packet["commands"]
    assert receipt["changed_paths"] == packet["changed_paths"]


def validate_hygiene() -> None:
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^\s*(?:axiom|constant|opaque|unsafe|extern)\b", re.MULTILINE,
    )
    source = lean_source_without_comments((HERE / "Statement.lean").read_text(encoding="utf-8"))
    assert prohibited.search(source) is None
    for relative in EXPECTED_CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())
    version = subprocess.run(
        [str(LAKE), "env", "lean", "--version"], cwd=LEAN_ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=30,
    )
    assert version.returncode == 0 and LEAN_COMMIT in version.stdout
    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""


def main() -> None:
    try:
        validate_authorities_and_contract()
        validate_statement_boundary()
        validate_dependency_ledger()
        validate_receipt_and_packet()
        validate_hygiene()
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
        print(json.dumps(failure, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    print(json.dumps(SEMANTIC_RESULT, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
