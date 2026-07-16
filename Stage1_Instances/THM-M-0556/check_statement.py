#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0556 statement packet."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0556"
LEAN_DIR = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0556-STATEMENT"
THEOREM_ID = "THM-M-0556"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
FAILED_GATE = "S02-EXACT-TARGET.source_statement_underdetermined"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0556/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0556/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0556/source_statement_crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0556/statement-receipt.json",
}
EXPECTED_ROLE_HASHES = {
    "statement_record": "a08a89ffc1badf37ee06d1416c184ec42454f2f833c56af41fd9633db3f33e62",
    "statement_source": "367991c66d66f6f631a3ddf032967a961a59791aa3c2e7a1961dbb6c07216aa9",
    "source_crosswalk": "4223019aa131e15e1f9c8b7fb885b20537ad531739a0236c4d8364b0b27a4efb",
}
EXPECTED_ROLE_BLOBS = {
    "statement_record": "8a73331fcaa781e365b0216176d2ab29151ac2de",
    "statement_source": "3886fecf95f4a76823ef5a6ff4123fe0dc12981d",
    "source_crosswalk": "a00eb54272c0177dff786d9a414b75d65d7ef51c",
}
EXPECTED_SUPPORT_HASHES = {
    "Stage1_Instances/THM-M-0556/dependency-reuse-ledger.json": (
        "98f890821dfdfac8d5b9a8502b3c155b557310a3f471d72b4bf9d38d7e8c0f9a"
    ),
    "Stage1_Instances/THM-M-0556/statement-blocker.json": (
        "3dab19a0dfdaa42711acb86d84d847382e72f221736cc56e8817a66d613e04d4"
    ),
    "Stage1_Instances/THM-M-0556/statement-blocker-head-1cc6aa61-slot123.md": (
        "b37fc0d9b4fbf5a9fd1ad4190f2b7479d10d819cc234de52e259f93c88b30bf7"
    ),
    "Stage1_Instances/THM-M-0556/intake.json": (
        "2fa039d76dc11cbf1d129f6df5d0002ea54b3e148c275bdaeeb0c97753f86344"
    ),
    "Stage1_Instances/THM-M-0556/StatementProbe.lean": (
        "4b5ebb2c5e11e9930fbc2aa5bc02bf1402da5819d888bbedc65c0a952439dda1"
    ),
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_112.lean": (
        "a93e9c2b84ba8a5f55ace8286cd9afdf69fcbd4f65c064e75c248681397522ea"
    ),
    "Docs/researches/math_theorems.md": (
        "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29"
    ),
}
EXPECTED_AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": "fb6cd286dc5c47e22d754ab73e5162986e98a18b5bc6d8e7213ae5d39b4256d1",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "skills/execute-stage1-rev56/SKILL.md": "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
DIRECT_IMPORTS = (
    "Mathlib.Algebra.Homology.SpectralObject.SpectralSequence",
    "Mathlib.Topology.FiberBundle.Basic",
)
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    re.MULTILINE,
)
CANONICAL_DECLARATION = re.compile(
    r"^[ \t]*(?:def|theorem|lemma|abbrev|structure|class|inductive)\s+",
    re.MULTILINE,
)


def sha256(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def git_blob(relative: str) -> str:
    data = (ROOT / relative).read_bytes()
    framed = f"blob {len(data)}\0".encode("ascii") + data
    return hashlib.sha1(framed).hexdigest()


def load(relative: str) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r} in {relative}")
            result[key] = value
        return result

    value = json.loads(
        (ROOT / relative).read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicates,
    )
    if not isinstance(value, dict):
        raise ValueError(f"{relative} is not one JSON object")
    return value


def git(*argv: str) -> str:
    result = subprocess.run(
        ["/usr/bin/git", *argv],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    if result.returncode:
        raise ValueError(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def require_identity() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION:
        raise ValueError("repository HEAD differs from the worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("repository base tree differs from the receipt")
    for relative, expected in EXPECTED_AUTHORITY_HASHES.items():
        if sha256(relative) != expected:
            raise ValueError(f"authority input drifted: {relative}")
    for relative, expected in EXPECTED_SUPPORT_HASHES.items():
        if sha256(relative) != expected:
            raise ValueError(f"support input drifted: {relative}")

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    pattern = (
        r"^- \[ \] `S56-M-0556-STATEMENT` / `THM-M-0556` / `statement`:.*\n"
        r"  Depends: `S56-M-0556-INTAKE`\. Owned paths: `Stage1_Instances/THM-M-0556`\."
    )
    if re.search(pattern, blueprint, re.MULTILINE) is None:
        raise ValueError("authoritative v2 statement item changed")

    dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in dag["theorems"] if row["theorem_id"] == THEOREM_ID)
    if node["v2_execution_rank"] != 328 or node["topological_layer"] != 0:
        raise ValueError("v2 claim order changed")
    if node["dependency_context_sha256"] != CONTEXT_SHA256:
        raise ValueError("dependency context changed")
    if node["phase_states"]["intake"] != "[_]" or node["phase_states"]["statement"] != "[ ]":
        raise ValueError("authoritative phase state changed")
    for field in (
        "direct_hard_parents",
        "transitive_hard_ancestors",
        "direct_reuse_hint_ids",
        "shared_lemma_group_ids",
    ):
        if node[field] != []:
            raise ValueError(f"declared empty dependency field changed: {field}")

    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row["phase"] == "statement")
    selected: dict[str, str] = {}
    for role in phase["required_artifact_roles"]:
        matches = [
            path.format(theorem_id=THEOREM_ID)
            for path in role["path_candidates"]
            if (ROOT / path.format(theorem_id=THEOREM_ID)).is_file()
        ]
        if len(matches) != 1:
            raise ValueError(f"role {role['role']} is missing or ambiguous")
        selected[role["role"]] = matches[0]
    if selected != ROLE_PATHS:
        raise ValueError("statement role selection changed")
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    if validators != ["Stage1_Instances/THM-M-0556/check_statement.py"]:
        raise ValueError("validator candidate selection is not exactly one")
    if phase["raw_blocked_can_close_phase"] is not False:
        raise ValueError("blocked statement unexpectedly became phase-closing")
    if phase["classified_negative_findings_may_satisfy_deliverable"] is not False:
        raise ValueError("negative statement finding unexpectedly satisfies the deliverable")


def require_ledger() -> None:
    ledger = load("Stage1_Instances/THM-M-0556/dependency-reuse-ledger.json")
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
        if ledger[field] != []:
            raise ValueError(f"empty dependency closure is not empty: {field}")
    closure = ledger["closure_audit"]
    if closure["parent_inspection_order"] != []:
        raise ValueError("parent inspection order is not the exact empty closure")
    if closure["claim_order"] != {
        "v2_execution_rank": 328,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        raise ValueError("dependency ledger claim order changed")
    if closure["provider_acceptance_inherited"] is not False:
        raise ValueError("dependency ledger transfers provider acceptance")


def require_statement_boundary() -> None:
    statement = load(ROLE_PATHS["statement_record"])
    blocker = load("Stage1_Instances/THM-M-0556/statement-blocker.json")
    source = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    report = (HERE / "statement-blocker-head-1cc6aa61-slot123.md").read_text(
        encoding="utf-8"
    )
    repository_source = (ROOT / "Docs/researches/math_theorems.md").read_text(
        encoding="utf-8"
    )
    legacy = (
        ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_112.lean"
    ).read_text(encoding="utf-8")

    for role, expected in EXPECTED_ROLE_HASHES.items():
        if sha256(ROLE_PATHS[role]) != expected:
            raise ValueError(f"selected role bytes drifted: {role}")
        if git_blob(ROLE_PATHS[role]) != EXPECTED_ROLE_BLOBS[role]:
            raise ValueError(f"selected role Git blob drifted: {role}")

    if statement["schema_version"] != "stage1-statement/1.0":
        raise ValueError("statement record schema changed")
    if statement["item_id"] != ITEM_ID or statement["theorem_id"] != THEOREM_ID:
        raise ValueError("statement record identity changed")
    if statement["canonical_claim_status"] != "blocked_source_statement_underdetermined":
        raise ValueError("statement ambiguity is no longer explicit")
    if statement["canonical_statement"] is not None:
        raise ValueError("a canonical human statement was invented")
    formal = statement["canonical_formal_target"]
    for field in (
        "declaration_or_expression",
        "elaborated_expression_sha256",
        "environment_expression_fingerprint",
    ):
        if formal[field] is not None:
            raise ValueError(f"canonical target field was invented: {field}")
    if statement["statement_fingerprints"] != []:
        raise ValueError("a statement fingerprint was invented")
    if statement["credited_transports"] != [] or statement["checked_alternate_encodings"] != []:
        raise ValueError("a target transport was invented")
    if statement["statement_elaborated"] is not False:
        raise ValueError("statement record falsely claims target elaboration")
    if statement["phase_predicate_proven"] is not False or statement["phase_accepted"] is not False:
        raise ValueError("statement record falsely claims phase acceptance")
    if statement["audit_complete"] is not False or statement["theorem_complete"] is not False:
        raise ValueError("statement record falsely closes a terminal decision")
    if set(statement["mutation_tests"]) != {
        "removed_hypothesis", "changed_domain", "changed_binder_scope", "boundary_case"
    }:
        raise ValueError("statement mutation classes are incomplete")
    if any(
        value != {"status": "not_run_missing_canonical_target", "passed": False}
        for value in statement["mutation_tests"].values()
    ):
        raise ValueError("statement record falsely passes a mutation")

    imports = tuple(re.findall(r"^import ([^\s]+)$", source, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        raise ValueError("boundary probe imports changed")
    if CANONICAL_DECLARATION.search(source):
        raise ValueError("boundary probe unexpectedly declares a target")
    if PROHIBITED.search(source):
        raise ValueError("boundary probe contains a prohibited construct")
    if tuple(re.findall(r"^#check ([^\s]+)$", source, re.MULTILINE)) != (
        "FiberBundle", "E₂CohomologicalSpectralSequenceNat"
    ):
        raise ValueError("boundary probe checks changed")

    required_terms = (
        "homology or cohomology",
        "local coefficient",
        "convergence",
        "unconstrained `Prop`",
    )
    combined = crosswalk + "\n" + report
    if any(term not in combined for term in required_terms):
        raise ValueError("source ambiguity or legacy non-credit boundary is incomplete")
    if "纤维化的谱序列" not in repository_source:
        raise ValueError("repository source phrase changed")
    if "structure LeraySerrePackage" not in legacy or "def StatementShape" not in legacy:
        raise ValueError("legacy discovery boundary changed")
    if blocker["canonical_statement"] is not None or blocker["canonical_formal_target"] is not None:
        raise ValueError("blocker invents a target")
    if blocker["first_failed_gate"] != FAILED_GATE:
        raise ValueError("blocker first failed gate changed")
    if blocker["phase_predicate_proven"] is not False or blocker["phase_accepted"] is not False:
        raise ValueError("blocker falsely claims the positive predicate")

    environment = os.environ.copy()
    environment.update({"LC_ALL": "C", "TZ": "UTC"})
    result = subprocess.run(
        ["lake", "env", "lean", "--trust=0", "../../Stage1_Instances/THM-M-0556/Statement.lean"],
        cwd=LEAN_DIR,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=120,
    )
    if result.returncode != 0:
        raise ValueError(f"pinned Lean boundary failed: {result.stderr[:400]}")
    if "FiberBundle" not in result.stdout or "E₂CohomologicalSpectralSequenceNat" not in result.stdout:
        raise ValueError("pinned Lean boundary output is incomplete")


def require_receipt_and_packet() -> None:
    receipt = load(ROLE_PATHS["phase_receipt"])
    packet = load(".stage1-worker-selftest.json")
    required = {
        "schema_version", "receipt_id", "item_id", "theorem_id", "phase", "intent",
        "base_revision", "base_tree", "inputs", "support_state", "proposed_state",
        "accepted", "verdict", "selftest_status", "selftest_result", "known_failures",
        "first_failed_gate", "retry_condition", "status_boundary", "audit_complete",
        "theorem_complete", "invalidation_inputs", "statement_fingerprints", "mutation_tests",
    }
    if not required.issubset(receipt):
        raise ValueError("phase receipt omits contract-required fields")
    if receipt["schema_version"] != "stage1-node-receipt/1.0":
        raise ValueError("phase receipt schema changed")
    if (receipt["item_id"], receipt["theorem_id"], receipt["phase"], receipt["intent"]) != (
        ITEM_ID, THEOREM_ID, "statement", "audit"
    ):
        raise ValueError("phase receipt identity changed")
    if receipt["base_revision"] != BASE_REVISION or receipt["base_tree"] != BASE_TREE:
        raise ValueError("phase receipt base changed")
    if receipt["accepted"] is not False or receipt["verdict"] != "blocked":
        raise ValueError("phase receipt does not preserve blocked semantics")
    if receipt["proposed_state"] != "[_]" or receipt["selftest_status"] != "passed":
        raise ValueError("phase receipt does not preserve self-tested negative semantics")
    if receipt["selftest_result"].get("phase_predicate_passed") is not False:
        raise ValueError("phase receipt falsely passes the positive predicate")
    if receipt["statement_fingerprints"] != []:
        raise ValueError("phase receipt invents a statement fingerprint")
    if receipt["first_failed_gate"] != FAILED_GATE:
        raise ValueError("phase receipt first failed gate changed")
    if receipt["audit_complete"] is not False or receipt["theorem_complete"] is not False:
        raise ValueError("phase receipt falsely closes a terminal decision")
    if any(row["passed"] is not False for row in receipt["mutation_tests"]):
        raise ValueError("phase receipt falsely passes a mutation")
    bindings = receipt["artifact_bindings"]
    if set(bindings) != set(ROLE_PATHS):
        raise ValueError("phase receipt selected role bindings are incomplete")
    for role in EXPECTED_ROLE_HASHES:
        binding = bindings[role]
        if binding != {
            "role": role,
            "path": ROLE_PATHS[role],
            "sha256": EXPECTED_ROLE_HASHES[role],
            "git_blob": EXPECTED_ROLE_BLOBS[role],
        }:
            raise ValueError(f"phase receipt role binding drifted: {role}")
    self_binding = bindings["phase_receipt"]
    if self_binding["path"] != ROLE_PATHS["phase_receipt"]:
        raise ValueError("phase receipt self-binding path changed")
    if self_binding["sha256"] is not None or self_binding["git_blob"] is not None:
        raise ValueError("phase receipt self-binding must remain scheduler-owned and acyclic")
    if receipt["inputs"]["parent_inspection_order"] != []:
        raise ValueError("phase receipt parent inspection order changed")
    if receipt["inputs"]["provider_acceptance_inherited"] is not False:
        raise ValueError("phase receipt transfers provider acceptance")
    for field, expected_path in {
        "statement_validator": "Stage1_Instances/THM-M-0556/check_statement.py",
        "validation_record": "Stage1_Instances/THM-M-0556/statement-validation.md",
    }.items():
        binding = receipt["inputs"].get(field, {})
        if binding.get("path") != expected_path:
            raise ValueError(f"phase receipt {field} path changed")
        if binding.get("sha256") != sha256(expected_path):
            raise ValueError(f"phase receipt {field} SHA-256 binding changed")
        if binding.get("git_blob") != git_blob(expected_path):
            raise ValueError(f"phase receipt {field} Git-blob binding changed")

    expected_owned_changed = [
        "Stage1_Instances/THM-M-0556/Statement.lean",
        "Stage1_Instances/THM-M-0556/check_statement.py",
        "Stage1_Instances/THM-M-0556/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0556/statement-blocker-head-1cc6aa61-slot123.md",
        "Stage1_Instances/THM-M-0556/statement-blocker.json",
        "Stage1_Instances/THM-M-0556/statement-receipt.json",
        "Stage1_Instances/THM-M-0556/statement-validation.md",
        "Stage1_Instances/THM-M-0556/statement.json",
    ]
    expected_changed = [".stage1-worker-selftest.json", *expected_owned_changed]
    status = subprocess.run(
        ["/usr/bin/git", "status", "--porcelain", "--", "Stage1_Instances/THM-M-0556"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    if status.returncode:
        raise ValueError("could not inspect the target-owned worktree delta")
    actual_owned_changed = sorted(line[3:] for line in status.stdout.splitlines())
    if actual_owned_changed != expected_owned_changed:
        raise ValueError("target-owned worktree delta differs from the packet")
    if set(packet) != {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state"
    }:
        raise ValueError("worker packet fields changed")
    if packet["item_id"] != ITEM_ID or packet["state"] != "[_]":
        raise ValueError("worker packet identity or state changed")
    if packet["base_revision"] != BASE_REVISION:
        raise ValueError("worker packet base changed")
    if packet["changed_paths"] != expected_changed:
        raise ValueError("worker packet changed path inventory changed")
    if packet["commands"] != receipt["selftest_result"]["commands"]:
        raise ValueError("worker packet commands differ from receipt commands")
    if packet["known_failures"] != receipt["known_failures"]:
        raise ValueError("worker packet failures differ from receipt failures")


def semantic(*, failed: bool = False, message: str) -> dict[str, Any]:
    if failed:
        return {
            "schema_version": "stage1-validator-semantic-result/1.0",
            "item_id": ITEM_ID,
            "theorem_id": THEOREM_ID,
            "phase": "statement",
            "status": "failed",
            "verdict": "repair_required",
            "phase_accepted": False,
            "audit_complete": False,
            "theorem_complete": False,
            "phase_predicate_proven": False,
            "first_failed_gate": "S01-ARTIFACTS",
            "open_obligations": 1,
            "stale_inputs": [],
            "blocked": False,
            "message": message,
        }
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
        "first_failed_gate": FAILED_GATE,
        "open_obligations": 5,
        "stale_inputs": [],
        "blocked": True,
        "message": message,
    }


def main() -> None:
    try:
        require_identity()
        require_ledger()
        require_statement_boundary()
        require_receipt_and_packet()
    except Exception as error:
        result = semantic(failed=True, message=f"negative statement packet validation failed: {error}")
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    result = semantic(
        message=(
            "The source-underdetermined Leray-Serre boundary, empty dependency closure, "
            "pinned interface probe, and negative receipt are internally consistent; "
            "the positive statement predicate remains blocked."
        )
    )
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
