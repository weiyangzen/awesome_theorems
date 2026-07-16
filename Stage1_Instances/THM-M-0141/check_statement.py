#!/usr/bin/env python3
"""Validate the fail-closed statement boundary for THM-M-0141."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0141"
THEOREM_ID = "THM-M-0141"
ITEM_ID = "S56-M-0141-STATEMENT"
BASE_REVISION = "778c2db4855d48868391ea236f702e592067e798"
BASE_TREE = "27abf0ec82dad50561a14d1db471126fb7ac8665"
GRAPH_SHA256 = "9db2a7cc29bf218211004677abe45ce1742f597405c2d879675dbc66542c4c8b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
FAILED_GATE = "S02-EXACT-TARGET.exact_source_statement_identity"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0141/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0141/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0141/source-statement-crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0141/statement-receipt.json",
}
EXPECTED_ROLE_HASHES = {
    "statement_record": "2ba876efff47f128653eadb06a6f7982d7a99449150990a73896031c9f33e830",
    "statement_source": "9642340a52badec81161793cb031127c764e6a583b111b58916c8e844b998e35",
    "source_crosswalk": "d9395ece448caec3fbccc1600e406a52010d771da05af544dd6e15cdfc23fbea",
}
EXPECTED_ROLE_BLOBS = {
    "statement_record": "87cf052e01572f7093f727898548f9e2a58e3d31",
    "statement_source": "d7e3e5ee9aea8266ef1e278d33fa190438a02bc2",
    "source_crosswalk": "85750bf3b4ca6b46f1f324e1b713e2af5207b673",
}
EXPECTED_AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": "af9c686849cec4da9f2680c70bb0eb7e78330681c2b422d0100de43b32c85aee",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "skills/execute-stage1-rev56/SKILL.md": "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_SUPPORT_HASHES = {
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_057.lean": (
        "f9da457a5367f2e59e691300f0866b57658d3acfd90100c88149652d645229de"
    ),
    "Stage1_Instances/THM-M-0141/dependency-reuse-ledger.json": (
        "9b191c51873716bca16d375f64aa45d74809a115242ff24177dd0ddd00872aa5"
    ),
    "Stage1_Instances/THM-M-0141/statement-blocker.md": (
        "070d027c2e42ee8c5bbacf4119bada8d2d20a0f480ff561f88693b9078fa39e7"
    ),
}
DIRECT_IMPORTS = (
    "Mathlib.RingTheory.HopfAlgebra.Basic",
    "Mathlib.LinearAlgebra.Basis.Defs",
    "Mathlib.LinearAlgebra.RootSystem.CartanMatrix",
)
SEMANTIC = {
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
    "first_failed_gate": FAILED_GATE,
    "open_obligations": 5,
    "stale_inputs": [],
    "blocked": True,
    "message": (
        "Negative statement boundary self-tested: pinpoint source identity, exact Lean target, "
        "expression fingerprint, checked transports, and four mutation classes remain open."
    ),
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)
CANONICAL_DECLARATION = re.compile(
    r"^[ \t]*(?:def|theorem|lemma|example|abbrev|opaque|axiom)\s+"
    r"(?:Lusztig|CanonicalBasis|CanonicalTarget|StatementShape)",
    flags=re.MULTILINE | re.IGNORECASE,
)


def fail(message: str) -> NoReturn:
    print(f"THM-M-0141 statement validator: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(relative: str) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate JSON key {key!r} in {relative}")
            result[key] = value
        return result

    try:
        value = json.loads(
            (ROOT / relative).read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicates,
        )
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {relative}: {error}")
    if not isinstance(value, dict):
        fail(f"expected one JSON object in {relative}")
    return value


def sha256(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def git_blob(relative: str) -> str:
    data = (ROOT / relative).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git(*argv: str) -> str:
    result = subprocess.run(
        ["git", *argv], cwd=ROOT, capture_output=True, text=True, timeout=20
    )
    if result.returncode:
        fail(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def validate_authority() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("repository HEAD differs from the claimed worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("repository tree differs from the claimed worker base")
    for relative, expected in EXPECTED_AUTHORITY_HASHES.items():
        if sha256(relative) != expected:
            fail(f"authority input changed: {relative}")
    for relative, expected in EXPECTED_SUPPORT_HASHES.items():
        if sha256(relative) != expected:
            fail(f"support input changed: {relative}")

    target = next(
        row
        for row in load("Docs/Stage1_Targets_rev-5.6.json")["targets"]
        if row.get("theorem_id") == THEOREM_ID
    )
    if (
        target.get("execution_rank") != 57
        or target.get("lifecycle_mode") != "planned"
        or target.get("legacy_artifacts_accepted") is not False
    ):
        fail("target manifest identity, lifecycle, or legacy boundary changed")

    item = next(
        row
        for row in load("Docs/Stage1_Execution_DAG_rev-5.6.json")["items"]
        if row.get("id") == ITEM_ID
    )
    expected_item = {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 57,
        "phase": "statement",
        "layer": 1,
        "state": "[ ]",
        "depends_on": ["S56-M-0141-INTAKE"],
        "owned_paths": ["Stage1_Instances/THM-M-0141"],
        "deliverable": "Elaborate the exact Lean 4 target with the minimal pinned imports.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    if item != expected_item:
        fail("authoritative statement item changed")

    theorem_dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    node = next(
        row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM_ID
    )
    if node.get("v2_execution_rank") != 291 or node.get("topological_layer") != 0:
        fail("v2 claim order changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency context changed")
    for field in (
        "direct_hard_parents",
        "transitive_hard_ancestors",
        "direct_reuse_hint_ids",
        "shared_lemma_group_ids",
    ):
        if node.get(field) != []:
            fail(f"theorem dependency field {field} is no longer empty")

    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row.get("phase") == "statement")
    selected: dict[str, str] = {}
    for role in phase["required_artifact_roles"]:
        candidates = [
            candidate.format(theorem_id=THEOREM_ID)
            for candidate in role["path_candidates"]
            if (ROOT / candidate.format(theorem_id=THEOREM_ID)).is_file()
        ]
        if len(candidates) != 1:
            fail(f"role {role['role']} is missing or ambiguous")
        selected[role["role"]] = candidates[0]
    if selected != ROLE_PATHS:
        fail("statement artifact-role selection changed")
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    if validators != ["Stage1_Instances/THM-M-0141/check_statement.py"]:
        fail("validator candidate selection is not exactly one declared path")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("statement contract unexpectedly permits blocked phase closure")
    if phase.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        fail("statement contract unexpectedly treats negative findings as the deliverable")


def validate_ledger() -> None:
    ledger = load("Stage1_Instances/THM-M-0141/dependency-reuse-ledger.json")
    if ledger.get("schema_version") != "stage1-dependency-reuse-ledger/1.1":
        fail("dependency ledger schema changed")
    if ledger.get("consumer_theorem_id") != THEOREM_ID:
        fail("dependency ledger owner changed")
    if ledger.get("observed_theorem_dag_sha256") != GRAPH_SHA256:
        fail("dependency ledger graph binding changed")
    if ledger.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency ledger context binding changed")
    if ledger.get("repository_revision") != BASE_REVISION:
        fail("dependency ledger revision changed")
    for field in (
        "direct_parent_ids",
        "transitive_ancestor_ids",
        "hard_edge_ids",
        "reuse_hint_ids",
        "shared_group_ids",
        "inspections",
        "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        if ledger.get(field) != []:
            fail(f"empty dependency ledger field {field} changed")
    closure = ledger.get("closure_audit", {})
    if closure.get("parent_inspection_order") != []:
        fail("parent inspection order is not the exact empty closure")
    if closure.get("status") != "empty_complete_closure_audited":
        fail("empty dependency closure was not fully audited")


def validate_statement_boundary() -> None:
    record = load(ROLE_PATHS["statement_record"])
    source = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    blocker = (HERE / "statement-blocker.md").read_text(encoding="utf-8")
    repository_source = (ROOT / "Docs/researches/math_theorems.md").read_text(
        encoding="utf-8"
    )
    legacy = (
        ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_057.lean"
    ).read_text(encoding="utf-8")

    for role, expected in EXPECTED_ROLE_HASHES.items():
        if sha256(ROLE_PATHS[role]) != expected:
            fail(f"selected artifact bytes changed: {role}")
        if git_blob(ROLE_PATHS[role]) != EXPECTED_ROLE_BLOBS[role]:
            fail(f"selected artifact Git blob changed: {role}")
    if record.get("schema_version") != "stage1-statement/1.0":
        fail("statement record schema changed")
    if record.get("item_id") != ITEM_ID or record.get("theorem_id") != THEOREM_ID:
        fail("statement record identity changed")
    if record.get("canonical_claim_status") != "blocked_on_exact_primary_source_statement":
        fail("statement ambiguity is no longer explicit")
    formal = record.get("canonical_formal_target", {})
    if record.get("canonical_statement") is not None:
        fail("a canonical mathematical statement was invented")
    if formal.get("declaration_or_expression") is not None:
        fail("a canonical Lean declaration or expression was invented")
    if formal.get("elaborated_expression_sha256") is not None:
        fail("a missing expression fingerprint was invented")
    if formal.get("statement_file_sha256") != EXPECTED_ROLE_HASHES["statement_source"]:
        fail("statement boundary source hash is stale")
    if tuple(record.get("direct_imports", [])) != DIRECT_IMPORTS:
        fail("statement boundary imports changed")
    mutations = record.get("mutation_tests", {})
    if (
        mutations.get("executed") != []
        or mutations.get("status") != "blocked_without_canonical_expression"
    ):
        fail("mutation blocker boundary changed")
    if any(
        record.get(field) is not False
        for field in (
            "statement_elaborated",
            "phase_predicate_proven",
            "phase_accepted",
            "audit_complete",
            "theorem_complete",
        )
    ):
        fail("statement record overstates phase or terminal completion")

    imports = tuple(re.findall(r"^import ([^\s]+)$", source, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        fail("boundary source direct imports disagree")
    if PROHIBITED.search(source):
        fail("boundary source contains a prohibited placeholder or trust construct")
    if CANONICAL_DECLARATION.search(source):
        fail("boundary source unexpectedly declares a canonical target")
    checks = tuple(re.findall(r"^#check ([^\s]+)$", source, re.MULTILINE))
    if checks != (
        "HopfAlgebra.antipode",
        "Module.Basis",
        "RootPairing",
        "RootPairing.Base.cartanMatrix",
    ):
        fail("boundary interface probes changed")
    required_terms = (
        "exact theorem/proposition",
        "Cartan datum binder",
        "canonical basis conclusion",
        "no H0",
        "S02-EXACT-TARGET.exact_source_statement_identity",
        "parent_inspection_order",
    )
    combined = crosswalk + "\n" + blocker
    if any(term not in combined for term in required_terms):
        fail("source ambiguity or dependency boundary is incomplete")
    if "卢斯蒂格典范基" not in repository_source or "量子群的典范基" not in repository_source:
        fail("repository source record changed")
    for term in (
        "structure QuantumGroupSkeleton",
        "structure CanonicalBasisCandidate",
        "def StatementShape : Prop",
        "proposition-valued target",
    ):
        if term not in legacy:
            fail("legacy discovery-source boundary changed")


def validate_receipt_and_packet() -> None:
    receipt = load(ROLE_PATHS["phase_receipt"])
    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row.get("phase") == "statement")
    required = {
        pointer.removeprefix("/")
        for pointer in phase["phase_receipt_required_fields"]
        if isinstance(pointer, str) and pointer.count("/") == 1
    }
    if not required <= set(receipt):
        fail("phase receipt omits a contract-required field")
    if receipt.get("schema_version") != "stage1-node-receipt/1.0":
        fail("phase receipt schema changed")
    if receipt.get("item_id") != ITEM_ID or receipt.get("theorem_id") != THEOREM_ID:
        fail("phase receipt identity changed")
    if receipt.get("phase") != "statement" or receipt.get("intent") != "audit":
        fail("phase receipt phase or intent changed")
    if receipt.get("base_revision") != BASE_REVISION or receipt.get("base_tree") != BASE_TREE:
        fail("phase receipt base changed")
    if receipt.get("support_state") != "provisional_worker_selftest":
        fail("phase receipt support state changed")
    if receipt.get("proposed_state") != "[_]" or receipt.get("accepted") is not False:
        fail("worker receipt claims master acceptance")
    if receipt.get("verdict") != "blocked" or receipt.get("selftest_status") != "passed":
        fail("receipt no longer records a self-tested blocker")
    if receipt.get("first_failed_gate") != FAILED_GATE:
        fail("phase receipt first failed gate changed")
    if receipt.get("statement_fingerprints") != []:
        fail("phase receipt invents a statement fingerprint")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("phase receipt falsely closes a terminal decision")
    if receipt.get("semantic_result") != SEMANTIC:
        fail("receipt and validator semantic result disagree")
    if receipt.get("inputs", {}).get("parent_inspection_order") != []:
        fail("phase receipt parent inspection order changed")
    if receipt.get("inputs", {}).get("provider_acceptance_inherited") is not False:
        fail("phase receipt transfers provider acceptance")

    bindings = receipt.get("artifact_bindings")
    if not isinstance(bindings, dict) or set(bindings) != set(ROLE_PATHS):
        fail("phase receipt selected role bindings are incomplete")
    for role in EXPECTED_ROLE_HASHES:
        binding = bindings.get(role, {})
        if binding.get("role") != role or binding.get("path") != ROLE_PATHS[role]:
            fail(f"phase receipt role binding changed: {role}")
        if binding.get("sha256") != EXPECTED_ROLE_HASHES[role]:
            fail(f"phase receipt SHA-256 binding changed: {role}")
        if binding.get("git_blob") != EXPECTED_ROLE_BLOBS[role]:
            fail(f"phase receipt Git-blob binding changed: {role}")
    self_binding = bindings.get("phase_receipt", {})
    if self_binding.get("role") != "phase_receipt" or self_binding.get("path") != ROLE_PATHS["phase_receipt"]:
        fail("phase receipt self-binding identity changed")
    if self_binding.get("sha256") is not None or self_binding.get("git_blob") is not None:
        fail("self-referential receipt binding must remain scheduler-owned")

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
        fail("worker packet field set changed")
    if packet.get("item_id") != ITEM_ID or packet.get("state") != "[_]":
        fail("worker packet identity or state changed")
    if packet.get("base_revision") != BASE_REVISION:
        fail("worker packet base changed")
    if packet.get("commands") != receipt.get("selftest_result", {}).get("commands"):
        fail("worker packet commands differ from the phase receipt")
    if packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet known failures differ from the phase receipt")
    expected_changed = [
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0141/Statement.lean",
        "Stage1_Instances/THM-M-0141/check_statement.py",
        "Stage1_Instances/THM-M-0141/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0141/source-statement-crosswalk.md",
        "Stage1_Instances/THM-M-0141/statement-blocker.md",
        "Stage1_Instances/THM-M-0141/statement-receipt.json",
        "Stage1_Instances/THM-M-0141/statement.json",
    ]
    if packet.get("changed_paths") != expected_changed:
        fail("worker packet changed-path inventory changed")
    status = subprocess.run(
        ["git", "status", "--porcelain", "--", "Stage1_Instances/THM-M-0141"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
    )
    if status.returncode:
        fail("could not inspect the target-owned worktree delta")
    actual_changed = sorted(line[3:] for line in status.stdout.splitlines() if len(line) > 3)
    if actual_changed != expected_changed[1:]:
        fail("target-owned worktree delta differs from the handoff inventory")

    for relative in {*ROLE_PATHS.values(), "Stage1_Instances/THM-M-0141/check_statement.py"}:
        data = (ROOT / relative).read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            fail(f"text artifact has a malformed byte boundary: {relative}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            fail(f"text artifact has trailing whitespace: {relative}")


def main() -> None:
    validate_authority()
    validate_ledger()
    validate_statement_boundary()
    validate_receipt_and_packet()
    print(json.dumps(SEMANTIC, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
