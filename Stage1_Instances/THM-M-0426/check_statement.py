#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0426 statement packet."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0426"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0426-STATEMENT"
THEOREM_ID = "THM-M-0426"
BASE_REVISION = "94009a6bebd743588e09c3b45bfbf18bf9b5c5e3"
BASE_TREE = "daabee9f9b2c6e98d84b6290f78a209b950485fc"
GRAPH_SHA256 = "eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROBE_STDOUT_SHA256 = "2f44f648c4bf45d59e2b1612aa03da64e31f25cdf15acf645d7eee3dfb8a47d2"
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()
EXPECTED_OWNED_SHA256 = {
    "Statement.lean": "f9e38f406511cdc47078bff77e9705747111edaa82ad241ca53b1bac50a2efd7",
    "dependency-reuse-ledger.json": "4e43824eaac53832a309d89aed4c6bf16c18df77cca496bd2a2c28823c18b566",
    "statement.json": "9521a5ff73ff220917d7653c1619efc49a640cd55820dc66153c520dff1d4bd2",
    "source_statement_crosswalk.md": "1c0df9ff97f03e85f064b0b0f42ae0a8542d7ce8bbc85981b24c7151f3f5d595",
    "statement-blocker.md": "bc693835c9efb90ea2267053eeabc416d4ad2c7609369c5a47153b7b4a665a7a",
}
EXPECTED_OWNED_BLOBS = {
    "Statement.lean": "51d6cb1cbff0892662055a91efa2d0c673c6236d",
    "dependency-reuse-ledger.json": "89c81f9886c35af27827920c768aae61fe6e528d",
    "statement.json": "7a79c461d2fee9f6b388fe09df85ef0ada0738b8",
    "source_statement_crosswalk.md": "2903fac8bd1b744dc998528f050b5a919632bd1d",
    "statement-blocker.md": "bb70ee31447305a4a7f595d2b5f5adbc3b4c43a4",
}
EXPECTED_AUTHORITY_SHA256 = {
    "Docs/Stage1_Blueprint_v2.md": "f7f8bcf307b737c56eb7ebc77fa2192046dc07b27ce58df5876ba4fdc4f1d7fb",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "skills/execute-stage1-rev56/SKILL.md": "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_080.lean": "d48833b1368787ecadb73ff635769f28a9e991b5ed760a9785730b80b01abc87",
    "Stage1_Instances/THM-M-0426/intake.json": "26ae3880895444a79133b6e2b7b6d271e125c7ff861561550cc1cc591e6c1601",
}
DIRECT_IMPORTS = (
    "Mathlib.NumberTheory.LSeries.AbstractFuncEq",
    "Mathlib.NumberTheory.LSeries.DirichletContinuation",
    "Mathlib.NumberTheory.NumberField.AdeleRing",
    "Mathlib.NumberTheory.NumberField.ProductFormula",
)
CHECKED_SYMBOLS = (
    "WeakFEPair",
    "WeakFEPair.functional_equation",
    "StrongFEPair",
    "StrongFEPair.functional_equation",
    "DirichletCharacter.completedLFunction",
    "DirichletCharacter.IsPrimitive.completedLFunction_one_sub",
    "NumberField.AdeleRing",
    "NumberField.AdeleRing.algebraMap_injective",
    "NumberField.prod_abs_eq_one",
)
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
EXPECTED_CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0426/Statement.lean",
    "Stage1_Instances/THM-M-0426/check_statement.py",
    "Stage1_Instances/THM-M-0426/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0426/source_statement_crosswalk.md",
    "Stage1_Instances/THM-M-0426/statement-blocker.md",
    "Stage1_Instances/THM-M-0426/statement-receipt.json",
    "Stage1_Instances/THM-M-0426/statement.json",
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
    "first_failed_gate": "S02-EXACT-TARGET.source_statement_identity_and_normalization",
    "open_obligations": 4,
    "stale_inputs": [],
    "blocked": True,
    "message": "THM-M-0426 has no source-selected exact proposition; the checked packet is a target-scoped statement blocker.",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob(path: Path) -> str:
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
        ["/usr/bin/git", *args], cwd=cwd, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if result.returncode != 0:
        raise ValueError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def pointer(document: dict[str, Any], raw: str) -> Any:
    value: Any = document
    for component in raw.removeprefix("/").split("/"):
        if not isinstance(value, dict) or component not in value:
            raise ValueError(f"receipt lacks required pointer {raw}")
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
    if depth or in_string:
        raise ValueError("unterminated Lean comment or string")
    return "".join(output)


def run_lean(path: Path) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "TZ": "UTC"})
    return subprocess.run(
        ["lake", "env", "lean", "--trust=0", str(path)], cwd=LEAN_ROOT,
        env=environment, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        timeout=180, check=False,
    )


def verify_authority() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION:
        raise ValueError("repository HEAD differs from the worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("repository base tree differs from the receipt")
    for relative, expected in EXPECTED_AUTHORITY_SHA256.items():
        if sha256(ROOT / relative) != expected:
            raise ValueError(f"authority or support input drifted: {relative}")

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM_ID)
    if target["execution_rank"] != 80 or target["lifecycle_mode"] != "planned":
        raise ValueError("target manifest identity changed")
    if target["legacy_artifacts_accepted"] is not False or target["theorem_complete"] is not False:
        raise ValueError("target manifest unexpectedly grants completion credit")

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    item_line = next(line for line in blueprint.splitlines() if f"`{ITEM_ID}`" in line)
    if not item_line.startswith("- [ ]") or "{attempts=0}" not in item_line:
        raise ValueError("authoritative statement cursor changed")
    if "Depends: `S56-M-0426-INTAKE`" not in blueprint:
        raise ValueError("intra-theorem dependency changed")

    graph = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in graph["theorems"] if row["theorem_id"] == THEOREM_ID)
    if node["v2_execution_rank"] != 306 or node["dependency_context_sha256"] != CONTEXT_SHA256:
        raise ValueError("claim order or dependency context changed")
    if node["phase_states"]["statement"] != "[ ]" or node["phase_attempts"]["statement"] != 0:
        raise ValueError("v2 statement cursor changed")
    for field in (
        "direct_hard_parents", "transitive_hard_ancestors",
        "direct_reuse_hint_ids", "shared_lemma_group_ids",
    ):
        if node[field] != []:
            raise ValueError(f"declared empty dependency field changed: {field}")

    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    if phase["intent"] != "audit" or phase["raw_blocked_can_close_phase"] is not False:
        raise ValueError("statement negative boundary changed")
    if phase["classified_negative_findings_may_satisfy_deliverable"] is not False:
        raise ValueError("negative finding unexpectedly became phase-completing")
    if tuple(phase["phase_receipt_required_fields"]) != REQUIRED_RECEIPT_POINTERS:
        raise ValueError("receipt contract fields changed")
    expected_roles = {
        "statement_record": "Stage1_Instances/THM-M-0426/statement.json",
        "statement_source": "Stage1_Instances/THM-M-0426/Statement.lean",
        "source_crosswalk": "Stage1_Instances/THM-M-0426/source_statement_crosswalk.md",
        "phase_receipt": "Stage1_Instances/THM-M-0426/statement-receipt.json",
    }
    for role in phase["required_artifact_roles"]:
        candidates = [path.format(theorem_id=THEOREM_ID) for path in role["path_candidates"]]
        existing = [path for path in candidates if (ROOT / path).is_file()]
        if existing != [expected_roles[role["role"]]]:
            raise ValueError(f"artifact role {role['role']} is missing or ambiguous")
    validator_paths = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    if validator_paths != ["Stage1_Instances/THM-M-0426/check_statement.py"]:
        raise ValueError("validator candidate selection is not exactly one path")


def verify_packet() -> None:
    for name, expected in EXPECTED_OWNED_SHA256.items():
        if sha256(HERE / name) != expected:
            raise ValueError(f"owned input drifted: {name}")
        if blob(HERE / name) != EXPECTED_OWNED_BLOBS[name]:
            raise ValueError(f"owned Git blob drifted: {name}")

    ledger = load(HERE / "dependency-reuse-ledger.json")
    if ledger["schema_version"] != "stage1-dependency-reuse-ledger/1.1":
        raise ValueError("dependency ledger schema changed")
    if ledger["consumer_theorem_id"] != THEOREM_ID:
        raise ValueError("dependency ledger owner changed")
    if ledger["observed_theorem_dag_sha256"] != GRAPH_SHA256:
        raise ValueError("dependency ledger graph digest changed")
    if ledger["dependency_context_sha256"] != CONTEXT_SHA256:
        raise ValueError("dependency ledger context changed")
    if ledger["repository_revision"] != BASE_REVISION:
        raise ValueError("dependency ledger base changed")
    empty_fields = (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "parent_inspection_order",
        "inspections", "reuse_decisions", "unresolved_compatibility_obligations",
    )
    if any(ledger[field] != [] for field in empty_fields):
        raise ValueError("declared empty dependency closure is not empty")
    if ledger["claim_order"] != {
        "v2_execution_rank": 306,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        raise ValueError("dependency ledger claim order changed")
    if ledger["closure_audit"]["inspection_order"] != []:
        raise ValueError("empty parent inspection order changed")

    statement = load(HERE / "statement.json")
    if statement["status"] != "blocked_unfrozen" or statement["canonical_human_statement"] is not None:
        raise ValueError("statement record does not fail closed")
    formal = statement["canonical_formal_target"]
    for field in (
        "module", "declaration_or_expression", "elaborated_expression_sha256",
        "environment_expression_fingerprint",
    ):
        if formal[field] is not None:
            raise ValueError(f"statement record invents canonical field {field}")
    if statement["alternate_encodings"] != [] or statement["statement_fingerprints"] != []:
        raise ValueError("statement record invents a transport or fingerprint")
    required_mutations = {
        "removed_hypothesis", "changed_domain", "changed_binder_scope", "boundary_case",
    }
    if set(statement["mutation_tests"]) != required_mutations:
        raise ValueError("statement mutation classes are incomplete")
    if any(
        value != {"status": "not_run_missing_canonical_target", "passed": False}
        for value in statement["mutation_tests"].values()
    ):
        raise ValueError("statement record falsely passes a mutation")
    if statement["audit_complete"] is not False or statement["theorem_complete"] is not False:
        raise ValueError("statement record overclaims a terminal decision")

    source = (HERE / "Statement.lean").read_text(encoding="utf-8")
    imports = tuple(re.findall(r"^import ([^\s]+)$", source, re.MULTILINE))
    checks = tuple(re.findall(r"^#check ([^\s]+)$", source, re.MULTILINE))
    if imports != DIRECT_IMPORTS or checks != CHECKED_SYMBOLS:
        raise ValueError("boundary probe imports or checks changed")
    code = lean_without_comments(source)
    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
        r"^\s*(?:theorem|lemma|def|abbrev|structure|class|instance|axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    if prohibited.search(code):
        raise ValueError("boundary probe declares a target, proof, placeholder, or trust escape")

    probe = run_lean(HERE / "Statement.lean")
    if probe.returncode != 0:
        raise ValueError(f"boundary probe failed: {probe.stdout}{probe.stderr}")
    if hashlib.sha256(probe.stdout.encode()).hexdigest() != PROBE_STDOUT_SHA256:
        raise ValueError("boundary probe stdout changed")
    if hashlib.sha256(probe.stderr.encode()).hexdigest() != EMPTY_SHA256:
        raise ValueError("boundary probe stderr changed")

    legacy = run_lean(LEAN_ROOT / "AwesomeTheorems" / "Stage1" / "S1_M_080.lean")
    if legacy.returncode != 0 or legacy.stdout or legacy.stderr:
        raise ValueError("historical abstract module no longer elaborates silently")
    legacy_source = (LEAN_ROOT / "AwesomeTheorems" / "Stage1" / "S1_M_080.lean").read_text()
    required_legacy_terms = (
        "structure HeckeLFunctionData", "completedLFunction : Character → ℂ → ℂ",
        "def StatementShape", "Statement-level functional equation",
        "a terminal proof of the Hecke-character functional equation",
    )
    if any(term not in legacy_source for term in required_legacy_terms):
        raise ValueError("historical abstract-boundary evidence changed")

    version = subprocess.run(
        ["lake", "env", "lean", "--version"], cwd=LEAN_ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if version.returncode != 0 or LEAN_COMMIT not in version.stdout:
        raise ValueError("pinned Lean identity changed")
    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    if git("rev-parse", "HEAD", cwd=mathlib) != MATHLIB_REVISION:
        raise ValueError("pinned mathlib revision changed")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != MATHLIB_TREE:
        raise ValueError("pinned mathlib tree changed")
    if git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib) != "":
        raise ValueError("pinned mathlib worktree is dirty")

    crosswalk = (HERE / "source_statement_crosswalk.md").read_text(encoding="utf-8")
    blocker = (HERE / "statement-blocker.md").read_text(encoding="utf-8")
    required_terms = (
        "THM-M-0022", "canonical-root ownership", "Hecke", "primary",
        "phase_accepted=false", "exact target",
    )
    if any(term not in crosswalk + "\n" + blocker for term in required_terms):
        raise ValueError("source ambiguity or status boundary is incomplete")


def verify_receipt_and_packet() -> None:
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
        raise ValueError("receipt base changed")
    if receipt["verdict"] != "blocked" or receipt["accepted"] is not False:
        raise ValueError("receipt does not preserve blocked semantics")
    if receipt["proposed_state"] != "[_]" or receipt["selftest_status"] != "passed":
        raise ValueError("receipt worker handoff state changed")
    if receipt["selftest_result"]["exit_code"] != 0 or not receipt["selftest_result"]["commands"]:
        raise ValueError("receipt lacks successful exact self-test commands")
    if receipt["selftest_result"]["phase_predicate_passed"] is not False:
        raise ValueError("receipt falsely passes the statement predicate")
    if receipt["first_failed_gate"] != SEMANTIC_RESULT["first_failed_gate"]:
        raise ValueError("receipt first failed gate changed")
    if receipt["statement_fingerprints"] != []:
        raise ValueError("receipt invents a statement fingerprint")
    if any(row["passed"] is not False for row in receipt["mutation_tests"]):
        raise ValueError("receipt falsely passes a mutation")
    if receipt["audit_complete"] is not False or receipt["theorem_complete"] is not False:
        raise ValueError("receipt overclaims a terminal decision")

    for binding in receipt["inputs"].values():
        path = ROOT / binding["path"]
        if sha256(path) != binding["sha256"] or blob(path) != binding["git_blob"]:
            raise ValueError(f"receipt input binding is stale: {binding['path']}")
    selected = {row["role"]: row for row in receipt["selected_artifacts"]}
    if set(selected) != {"statement_record", "statement_source", "source_crosswalk", "phase_receipt"}:
        raise ValueError("receipt selected roles changed")
    for role in ("statement_record", "statement_source", "source_crosswalk"):
        path = ROOT / selected[role]["path"]
        if sha256(path) != selected[role]["sha256"] or blob(path) != selected[role]["git_blob"]:
            raise ValueError(f"selected artifact binding is stale: {role}")
    phase_receipt = selected["phase_receipt"]
    if phase_receipt["path"] != "Stage1_Instances/THM-M-0426/statement-receipt.json":
        raise ValueError("phase receipt self path changed")
    if phase_receipt["sha256"] is not None or phase_receipt["git_blob"] is not None:
        raise ValueError("receipt recursively claims a self hash")

    packet = load(ROOT / ".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }:
        raise ValueError("worker packet fields changed")
    if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
        raise ValueError("worker packet identity changed")
    if packet["base_revision"] != BASE_REVISION:
        raise ValueError("worker packet base changed")
    if set(packet["changed_paths"]) != EXPECTED_CHANGED_PATHS:
        raise ValueError("worker packet changed-path inventory is stale")
    if packet["commands"] != receipt["selftest_result"]["commands"]:
        raise ValueError("worker packet commands differ from the receipt")
    if packet["known_failures"] != receipt["known_failures"]:
        raise ValueError("worker packet failures differ from the receipt")
    if packet["output_summary"] != receipt["selftest_result"]["output_summary"]:
        raise ValueError("worker packet summary differs from the receipt")

    for relative in EXPECTED_CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            raise ValueError(f"artifact formatting changed: {relative}")


def verify() -> None:
    if not __debug__ or sys.flags.optimize != 0:
        raise ValueError("statement validator requires assertions enabled")
    verify_authority()
    verify_packet()
    verify_receipt_and_packet()


def main() -> None:
    try:
        verify()
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
