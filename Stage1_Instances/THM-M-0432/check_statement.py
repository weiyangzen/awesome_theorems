#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0432 statement boundary."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0432"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0432-STATEMENT"
THEOREM_ID = "THM-M-0432"
BASE_REVISION = "94009a6bebd743588e09c3b45bfbf18bf9b5c5e3"
BASE_TREE = "daabee9f9b2c6e98d84b6290f78a209b950485fc"
GRAPH_SHA256 = "eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
CONTRACT_GIT_BLOB = "84b92df9eaf457ab954b652c3f20f4d513cf0a88"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROBE_STDOUT_SHA256 = "1df616814cfb0cbe3f556affe36e2263b4bfcad2f4a3b033e32b00809a8cf1e8"
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
DIRECT_IMPORTS = (
    "Mathlib.FieldTheory.AbsoluteGaloisGroup",
    "Mathlib.NumberTheory.ClassNumber.FunctionField",
    "Mathlib.RepresentationTheory.Basic",
    "Mathlib.RingTheory.Frobenius",
)
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0432/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0432/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0432/source_statement_crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0432/statement-receipt.json",
}
EXPECTED_HASHES = {
    "Stage1_Instances/THM-M-0432/Statement.lean":
        "ded357ff7142b51d1813a45da406d91d989e153d4162cc0afd88c358b4fd2343",
    "Stage1_Instances/THM-M-0432/statement.json":
        "a3f32f5e08e7bf3d260048f23403f4d80a7e82b26538d36143dbfaf3df8625b9",
    "Stage1_Instances/THM-M-0432/source_statement_crosswalk.md":
        "084da9e5ab567104aa66fddaa1263255b5607f62e8445a3deed86798d87cc7f8",
    "Stage1_Instances/THM-M-0432/dependency-reuse-ledger.json":
        "97d9a82a3ebae538aef60ea285df7212b66a79f8aec2cc01d597c6770bd2bc7c",
    "Stage1_Instances/THM-M-0432/statement-blocker.md":
        "e669f27a0ba8a9cbb7102a08ed702f0185e212090eff6d110a0f0a3f429d1166",
    "Stage1_Instances/THM-M-0432/intake.json":
        "bc113cf8265b1aff6da9c0183fd649578b9a1239e9b6250fc8284840ecf5db2b",
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_060.lean":
        "4ccf33366955894287ab2a1c0b20529f5eecb7ac4bd7703fc5bc13bb9d751849",
    "Docs/Stage1_Blueprint_v2.md":
        "f7f8bcf307b737c56eb7ebc77fa2192046dc07b27ce58df5876ba4fdc4f1d7fb",
    "Docs/Stage1_Blueprint_rev-5.6.md":
        "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Stage1_Targets_rev-5.6.json":
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/researches/math_theorems.md":
        "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "skills/execute-stage1-rev56/SKILL.md":
        "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Formalizations/Lean/lean-toolchain":
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json":
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_BLOBS = {
    "Stage1_Instances/THM-M-0432/Statement.lean": "fad72f7407733464e713778fb281f3d5a1757d12",
    "Stage1_Instances/THM-M-0432/statement.json": "d5022a02069ba8a4a9acdebea3a0baf9a1f9ce4e",
    "Stage1_Instances/THM-M-0432/source_statement_crosswalk.md": "2addd435744729032d8a6e8526d72b2d452c5133",
}
REQUIRED_RECEIPT_POINTERS = (
    "/schema_version", "/receipt_id", "/item_id", "/theorem_id", "/phase",
    "/intent", "/base_revision", "/base_tree", "/inputs", "/support_state",
    "/proposed_state", "/accepted", "/verdict", "/selftest_status",
    "/selftest_result/exit_code", "/selftest_result/commands", "/known_failures",
    "/first_failed_gate", "/retry_condition", "/status_boundary",
    "/audit_complete", "/theorem_complete", "/invalidation_inputs",
    "/statement_fingerprints", "/mutation_tests",
)
EXPECTED_CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0432/Statement.lean",
    "Stage1_Instances/THM-M-0432/check_statement.py",
    "Stage1_Instances/THM-M-0432/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0432/source_statement_crosswalk.md",
    "Stage1_Instances/THM-M-0432/statement-blocker.md",
    "Stage1_Instances/THM-M-0432/statement-receipt.json",
    "Stage1_Instances/THM-M-0432/statement.json",
]
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
    "first_failed_gate": "S02-EXACT-TARGET.exact_source_statement_identity_and_rank_two_scope",
    "open_obligations": 5,
    "stale_inputs": [],
    "blocked": True,
    "message": (
        "The negative boundary is content-bound and self-tested, but no exact source-authorized "
        "Drinfeld claim, canonical Lean expression, fingerprint, transport, or mutation suite exists."
    ),
}


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


def lean_without_comments(source: str) -> str:
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
        ["lake", "env", "lean", "--trust=0", str(path)], cwd=LEAN_ROOT,
        env=environment, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=180, check=False,
    )


def validate_authority_and_contract() -> None:
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for relative, expected in EXPECTED_HASHES.items():
        assert sha256(ROOT / relative) == expected, relative

    contract_path = ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json"
    assert git("hash-object", str(contract_path)) == CONTRACT_GIT_BLOB
    contract = load(contract_path)
    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    assert phase["raw_blocked_can_close_phase"] is False
    assert phase["classified_negative_findings_may_satisfy_deliverable"] is False
    assert tuple(phase["phase_receipt_required_fields"]) == REQUIRED_RECEIPT_POINTERS
    selected: dict[str, str] = {}
    for role in phase["required_artifact_roles"]:
        candidates = [
            candidate.format(theorem_id=THEOREM_ID)
            for candidate in role["path_candidates"]
            if (ROOT / candidate.format(theorem_id=THEOREM_ID)).is_file()
        ]
        assert len(candidates) == 1, role["role"]
        selected[role["role"]] = candidates[0]
    assert selected == ROLE_PATHS
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    assert validators == ["Stage1_Instances/THM-M-0432/check_statement.py"]

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    item_line = next(line for line in blueprint.splitlines() if f"`{ITEM_ID}`" in line)
    assert item_line.startswith("- [ ]") and "{attempts=0}" in item_line
    assert "Depends: `S56-M-0432-INTAKE`" in blueprint
    graph = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in graph["theorems"] if row["theorem_id"] == THEOREM_ID)
    assert node["v2_execution_rank"] == 294 and node["topological_layer"] == 0
    assert node["phase_states"]["intake"] == "[_]"
    assert node["phase_states"]["statement"] == "[ ]"
    assert node["phase_attempts"]["statement"] == 0
    assert node["dependency_context_sha256"] == CONTEXT_SHA256
    assert node["direct_hard_parents"] == node["transitive_hard_ancestors"] == []
    assert node["direct_reuse_hint_ids"] == node["shared_lemma_group_ids"] == []


def validate_ledger() -> None:
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
    assert ledger["closure_audit"]["status"] == "empty_complete_closure_audited"

    import importlib.util
    cron_path = ROOT / "scripts" / "stage1_execution_cron.py"
    spec = importlib.util.spec_from_file_location("m0432_stage1_execution_cron", cron_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    validated = module.validate_dependency_reuse_ledger(
        HERE / "dependency-reuse-ledger.json",
        THEOREM_ID,
        expected_observed_graph_sha256=GRAPH_SHA256,
        expected_repository_revision=BASE_REVISION,
    )
    assert validated["closure_audit"]["status"] == "empty_complete_closure_audited"


def validate_statement_boundary() -> None:
    statement = load(HERE / "statement.json")
    assert statement["item_id"] == ITEM_ID and statement["theorem_id"] == THEOREM_ID
    assert statement["canonical_statement"] is None
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] is None
    assert formal["elaborated_expression_sha256"] is None
    assert formal["environment_fingerprint"] is None
    assert tuple(statement["direct_imports"]) == DIRECT_IMPORTS
    assert statement["statement_fingerprints"] == []
    assert statement["statement_elaborated"] is False
    assert statement["phase_predicate_proven"] is statement["phase_accepted"] is False
    assert statement["audit_complete"] is statement["theorem_complete"] is False
    assert set(statement["mutation_tests"].values()) == {"not_run_no_canonical_target"}

    source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    code = lean_without_comments(source)
    imports = tuple(re.findall(r"^import\s+(\S+)$", code, flags=re.MULTILINE))
    assert imports == DIRECT_IMPORTS
    declarations = re.compile(
        r"^\s*(?:theorem|lemma|def|abbrev|structure|class|instance|axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    assert declarations.search(code) is None
    checks = tuple(re.findall(r"^#check\s+(\S+)$", code, flags=re.MULTILINE))
    assert checks == (
        "Field.absoluteGaloisGroup", "Representation", "FunctionField",
        "FunctionField.classNumber", "Matrix.GeneralLinearGroup", "AlgHom.IsArithFrobAt",
    )
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^\s*(?:axiom|constant|opaque|unsafe|extern)\b", flags=re.MULTILINE,
    )
    assert prohibited.search(code) is None
    result = run_lean(HERE / "Statement.lean")
    assert result.returncode == 0, result.stdout + result.stderr
    assert hashlib.sha256(result.stdout.encode()).hexdigest() == PROBE_STDOUT_SHA256
    assert hashlib.sha256(result.stderr.encode()).hexdigest() == EMPTY_SHA256

    for module in DIRECT_IMPORTS:
        candidate = source.replace(f"import {module}\n", "", 1)
        fixture = HERE / f"ImportDeletion_{module.rsplit('.', 1)[-1]}.lean"
        assert not fixture.exists()
        fixture.write_text(candidate, encoding="utf-8")
        try:
            deletion = run_lean(fixture)
        finally:
            fixture.unlink()
        assert deletion.returncode != 0, f"probe import is redundant: {module}"

    crosswalk = (HERE / "source_statement_crosswalk.md").read_text(encoding="utf-8")
    blocker = (HERE / "statement-blocker.md").read_text(encoding="utf-8")
    combined = crosswalk + "\n" + blocker
    for term in (
        "Drinfeld", "rank-two", "Lafforgue", "geometric/arithmetic Frobenius",
        "unconstrained `corresponds`", "phase_accepted=false",
    ):
        assert term in combined, term

    legacy = (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_060.lean").read_text(
        encoding="utf-8"
    )
    assert "terminalCorrespondenceStatement := false" in legacy
    assert "corresponds : LanglandsParameter" in legacy
    catalog = (ROOT / "Docs/researches/math_theorems.md").read_text(encoding="utf-8")
    assert "**函数域朗兰兹对应**" in catalog and "提出者: Vladimir Drinfeld" in catalog

    version = subprocess.run(
        ["lake", "env", "lean", "--version"], cwd=LEAN_ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=30,
    )
    assert version.returncode == 0 and LEAN_COMMIT in version.stdout
    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    assert git("rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) == ""


def validate_receipt_and_packet() -> None:
    receipt = load(HERE / "statement-receipt.json")
    for raw in REQUIRED_RECEIPT_POINTERS:
        pointer(receipt, raw)
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM_ID and receipt["theorem_id"] == THEOREM_ID
    assert receipt["phase"] == "statement" and receipt["intent"] == "audit"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["claim_order"] == {
        "v2_execution_rank": 294,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }
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
    assert set(selected) == set(ROLE_PATHS)
    for role in ("statement_record", "statement_source", "source_crosswalk"):
        relative = ROLE_PATHS[role]
        assert selected[role]["path"] == relative
        assert selected[role]["sha256"] == sha256(ROOT / relative)
        assert selected[role]["git_blob"] == git("hash-object", relative)
        assert EXPECTED_BLOBS[relative] == selected[role]["git_blob"]
    assert selected["phase_receipt"]["sha256"] is None
    assert selected["phase_receipt"]["git_blob"] is None

    packet = load(ROOT / ".stage1-worker-selftest.json")
    assert set(packet) == {
        "item_id", "worker_verdict", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM_ID and packet["worker_verdict"] == "blocked"
    assert packet["base_revision"] == BASE_REVISION and packet["state"] == "[_]"
    assert packet["changed_paths"] == EXPECTED_CHANGED_PATHS
    assert packet["commands"] == receipt["selftest_result"]["commands"]
    assert packet["commands"] == receipt["commands"]
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert receipt["changed_paths"] == EXPECTED_CHANGED_PATHS

    for relative in EXPECTED_CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def validate() -> None:
    validate_authority_and_contract()
    validate_ledger()
    validate_statement_boundary()
    validate_receipt_and_packet()


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
        print(json.dumps(failure, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    print(json.dumps(SEMANTIC_RESULT, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
