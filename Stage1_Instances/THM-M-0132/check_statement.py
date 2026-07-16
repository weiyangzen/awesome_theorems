#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0132 statement evidence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import os
import subprocess
import sys
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0132"
THEOREM_ID = "THM-M-0132"
ITEM_ID = "S56-M-0132-STATEMENT"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
FAILED_GATE = "S02-EXACT-TARGET.source_faithful_modularity_relation_unavailable"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0132/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0132/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0132/source_statement_crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0132/statement-receipt.json",
}
EXPECTED_ROLE_HASHES = {
    "statement_record": "d3b1a67878e7aae62f991b08e3b9848b006effe3ca2ba5924e23171b8a6eaa3c",
    "statement_source": "536ec9d5c3a0ce4b84e784d53df7904bdd9038ab67e9ff7590606898d58c0422",
    "source_crosswalk": "16f353789bf1feae52c1008ee3983b53c11f40b0568a243a89fe1ab6a5060e38",
}
EXPECTED_ROLE_BLOBS = {
    "statement_record": "96be119cc4f083a64059e0795d3e4cb4697d3cf1",
    "statement_source": "befbcfe169b1ebced2c1fc483e528a395eb2ceae",
    "source_crosswalk": "a021dc047e921832a1eb7a2c5b3d7900598118b3",
}
EXPECTED_AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": (
        "fb6cd286dc5c47e22d754ab73e5162986e98a18b5bc6d8e7213ae5d39b4256d1"
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
EXPECTED_SUPPORT_HASHES = {
    "Stage1_Instances/THM-M-0132/dependency-reuse-ledger.json": (
        "3bb8ede3062dd499e13e63bb7b366f8bc4db06d7e0dccb866a3bd40f9a8bd18d"
    ),
    "Stage1_Instances/THM-M-0132/intake.json": (
        "489fd32dcc5c3463cceeea5a2841c25ed26a830f48fddf15593bd82e7e500d1a"
    ),
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_049.lean": (
        "b70401b238c5a04a846bb05e5dd23c2f8303818c348da4fcc432e2fd5e41aba9"
    ),
}
DIRECT_IMPORTS = (
    "Mathlib.AlgebraicGeometry.EllipticCurve.Weierstrass",
    "Mathlib.NumberTheory.ModularForms.Basic",
)
MUTATION_STATUS = {
    "removed_hypothesis": "not_executable_without_a_canonical_statement",
    "changed_domain": "not_executable_without_a_canonical_statement",
    "changed_binder_scope": "not_executable_without_a_canonical_statement",
    "boundary_case": "not_executable_without_a_canonical_statement",
}
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
        "The exact BCDT modularity target cannot be encoded from the pinned "
        "conductor/newform/compatibility interfaces; the negative packet is internally "
        "self-tested, but its validator is absent at the worker base and cannot support "
        "master acceptance."
    ),
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe|theorem|lemma|example)\b",
    flags=re.MULTILINE,
)


def fail(message: str) -> NoReturn:
    print(f"THM-M-0132 statement validator: {message}", file=sys.stderr)
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


def digest(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def git_blob(relative: str) -> str:
    data = (ROOT / relative).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git(*argv: str) -> str:
    result = subprocess.run(
        ["git", *argv],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
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
        if digest(relative) != expected:
            fail(f"authority input changed: {relative}")
    for relative, expected in EXPECTED_SUPPORT_HASHES.items():
        if digest(relative) != expected:
            fail(f"support input changed: {relative}")

    targets = load("Docs/Stage1_Targets_rev-5.6.json")
    target = next(
        row for row in targets["targets"] if row.get("theorem_id") == THEOREM_ID
    )
    if target.get("execution_rank") != 49 or target.get("lifecycle_mode") != "planned":
        fail("target manifest identity or lifecycle changed")
    if target.get("legacy_artifacts_accepted") is not False:
        fail("legacy evidence unexpectedly acquired acceptance")

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    item_pattern = re.compile(
        rf"^- \[ \] `{ITEM_ID}` / `{THEOREM_ID}` / `statement`: "
        rf"Elaborate the exact Lean 4 target with the minimal pinned imports\. "
        rf"\{{attempts=0\}}$",
        flags=re.MULTILINE,
    )
    if len(item_pattern.findall(blueprint)) != 1:
        fail("sole task-state authority item changed")
    if (
        f"Depends: `S56-M-0132-INTAKE`. Owned paths: `Stage1_Instances/{THEOREM_ID}`. "
        "Gate: rev-5.6 node-specific receipt and master acceptance."
    ) not in blueprint:
        fail("statement dependency, ownership, or gate changed")

    theorem_dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    node = next(
        row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM_ID
    )
    if node.get("v2_execution_rank") != 283 or node.get("topological_layer") != 0:
        fail("v2 claim order changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency context changed")
    if node.get("phase_states", {}).get("statement") != "[ ]":
        fail("authoritative statement phase state changed")
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
    if validators != ["Stage1_Instances/THM-M-0132/check_statement.py"]:
        fail("validator candidate selection is not exactly one declared path")
    base_validator = subprocess.run(
        [
            "git",
            "cat-file",
            "-e",
            f"{BASE_REVISION}:Stage1_Instances/THM-M-0132/check_statement.py",
        ],
        cwd=ROOT,
        capture_output=True,
        timeout=20,
        check=False,
    )
    if base_validator.returncode == 0:
        fail("worker-base validator unexpectedly exists; blocker classification changed")
    policy = contract.get("validator_selection", {})
    if policy.get("candidate_must_exist_at_worker_base") is not True:
        fail("HEAD contract no longer requires a worker-base validator")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("statement contract unexpectedly permits blocked phase closure")
    if phase.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        fail("statement contract unexpectedly treats negative findings as the deliverable")


def validate_ledger() -> None:
    ledger = load("Stage1_Instances/THM-M-0132/dependency-reuse-ledger.json")
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
    closure = ledger.get("closure_audit", {})
    if closure.get("parent_inspection_order") != []:
        fail("parent inspection order is not the exact empty closure")
    if closure.get("status") != "empty_complete_closure_audited":
        fail("empty closure audit is not complete")


def validate_statement_boundary() -> None:
    statement = load(ROLE_PATHS["statement_record"])
    source = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    blocker = (HERE / "statement-blocker.md").read_text(encoding="utf-8")

    for role, expected in EXPECTED_ROLE_HASHES.items():
        if digest(ROLE_PATHS[role]) != expected:
            fail(f"selected artifact bytes changed: {role}")
        if git_blob(ROLE_PATHS[role]) != EXPECTED_ROLE_BLOBS[role]:
            fail(f"selected artifact Git blob changed: {role}")

    if statement.get("schema_version") != "stage1-statement/1.0":
        fail("statement record schema changed")
    if statement.get("item_id") != ITEM_ID or statement.get("theorem_id") != THEOREM_ID:
        fail("statement record identity changed")
    if statement.get("canonical_claim_status") != (
        "blocked_on_missing_source_faithful_modularity_interfaces"
    ):
        fail("missing-interface boundary is no longer explicit")
    formal = statement.get("canonical_formal_target", {})
    if statement.get("canonical_statement") is not None:
        fail("a canonical Lean statement was invented")
    if formal.get("declaration_or_expression") is not None:
        fail("a canonical Lean declaration or expression was invented")
    if formal.get("elaborated_expression_sha256") is not None:
        fail("a missing expression fingerprint was invented")
    if formal.get("statement_file_sha256") != EXPECTED_ROLE_HASHES["statement_source"]:
        fail("statement boundary source hash is stale")
    if tuple(statement.get("direct_imports", [])) != DIRECT_IMPORTS:
        fail("statement boundary imports changed")
    if statement.get("statement_fingerprints") != []:
        fail("statement record invents a statement fingerprint")
    if statement.get("credited_transports") != []:
        fail("statement record invents a checked transport")
    if statement.get("mutation_tests") != MUTATION_STATUS:
        fail("required mutation blocker inventory changed")
    if statement.get("first_failed_gate") != FAILED_GATE:
        fail("statement record first failed gate changed")
    for field in (
        "statement_elaborated",
        "phase_predicate_proven",
        "phase_accepted",
        "theorem_proved",
        "audit_complete",
        "theorem_complete",
    ):
        if statement.get(field) is not False:
            fail(f"statement record overstates {field}")

    imports = tuple(re.findall(r"^import ([^\s]+)$", source, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        fail("boundary source direct imports disagree")
    if PROHIBITED.search(source):
        fail("boundary source contains a proof, placeholder, or trust escape")
    checks = tuple(re.findall(r"^#check ([^\s]+)$", source, re.MULTILINE))
    if checks != (
        "WeierstrassCurve.IsElliptic",
        "CongruenceSubgroup.Gamma0",
        "CongruenceSubgroup.Gamma1",
        "CuspForm",
    ):
        fail("boundary interface probes changed")
    required_terms = (
        "Every elliptic curve over `Q` is modular",
        "normalized weight-two newform",
        "Frobenius-trace",
        "Galois-representation",
        "Gamma1/X1",
        "not source-admitted",
    )
    combined = crosswalk + "\n" + blocker
    if any(term not in combined for term in required_terms):
        fail("source crosswalk or blocker omits the exact non-credit boundary")


def validate_receipt_and_packet() -> None:
    receipt = load(ROLE_PATHS["phase_receipt"])
    contract = load("Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row.get("phase") == "statement")
    for pointer in phase.get("phase_receipt_required_fields", []):
        if pointer.count("/") == 1 and pointer.removeprefix("/") not in receipt:
            fail(f"phase receipt omits contract-required field {pointer}")
    required_nested = receipt.get("selftest_result", {})
    if "exit_code" not in required_nested or "commands" not in required_nested:
        fail("phase receipt lacks required nested self-test fields")
    if receipt.get("schema_version") != "stage1-node-receipt/1.0":
        fail("phase receipt schema changed")
    if receipt.get("item_id") != ITEM_ID or receipt.get("theorem_id") != THEOREM_ID:
        fail("phase receipt identity changed")
    if receipt.get("phase") != "statement" or receipt.get("intent") != "audit":
        fail("phase receipt phase or intent changed")
    if receipt.get("base_revision") != BASE_REVISION or receipt.get("base_tree") != BASE_TREE:
        fail("phase receipt base changed")
    if receipt.get("accepted") is not False or receipt.get("verdict") != "blocked":
        fail("phase receipt no longer preserves the negative verdict")
    if receipt.get("proposed_state") != "[_]" or receipt.get("selftest_status") != "passed":
        fail("phase receipt does not preserve the self-tested negative handoff")
    if required_nested.get("exit_code") != 0 or not required_nested.get("commands"):
        fail("phase receipt has no exact successful blocker self-test")
    if receipt.get("statement_fingerprints") != []:
        fail("phase receipt invents a statement fingerprint")
    if receipt.get("mutation_tests") != MUTATION_STATUS:
        fail("phase receipt mutation boundary changed")
    if receipt.get("first_failed_gate") != FAILED_GATE:
        fail("phase receipt first failed gate changed")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("phase receipt falsely closes a terminal decision")
    if receipt.get("inputs", {}).get("parent_inspection_order") != []:
        fail("phase receipt parent inspection order changed")
    if receipt.get("inputs", {}).get("provider_acceptance_inherited") is not False:
        fail("phase receipt transfers provider acceptance")
    if receipt.get("semantic_result") != SEMANTIC:
        fail("phase receipt and validator semantic result disagree")

    bindings = receipt.get("artifact_bindings", {})
    if set(bindings) != set(ROLE_PATHS):
        fail("phase receipt selected role bindings are incomplete")
    for role in EXPECTED_ROLE_HASHES:
        binding = bindings.get(role, {})
        if binding.get("role") != role or binding.get("path") != ROLE_PATHS[role]:
            fail(f"phase receipt role binding changed: {role}")
        if binding.get("sha256") != EXPECTED_ROLE_HASHES[role]:
            fail(f"phase receipt SHA-256 binding changed: {role}")
        if binding.get("git_blob") != EXPECTED_ROLE_BLOBS[role]:
            fail(f"phase receipt Git blob binding changed: {role}")
    self_binding = bindings.get("phase_receipt", {})
    if self_binding.get("path") != ROLE_PATHS["phase_receipt"]:
        fail("phase receipt self-binding path changed")
    if self_binding.get("sha256") is not None or self_binding.get("git_blob") is not None:
        fail("phase receipt self-binding must remain scheduler-owned and acyclic")

    for name, relative in (
        ("dependency_reuse_ledger", "Stage1_Instances/THM-M-0132/dependency-reuse-ledger.json"),
        ("validator", "Stage1_Instances/THM-M-0132/check_statement.py"),
    ):
        binding = receipt.get("inputs", {}).get(name, {})
        if binding.get("path") != relative:
            fail(f"phase receipt {name} path changed")
        if binding.get("sha256") != digest(relative):
            fail(f"phase receipt {name} SHA-256 is stale")
        if binding.get("git_blob") != git_blob(relative):
            fail(f"phase receipt {name} Git blob is stale")

    packet = load(".stage1-worker-selftest.json")
    expected_packet_fields = {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    if set(packet) != expected_packet_fields:
        fail("worker packet fields changed")
    if packet.get("item_id") != ITEM_ID or packet.get("state") != "[_]":
        fail("worker packet identity or state changed")
    if packet.get("base_revision") != BASE_REVISION:
        fail("worker packet base changed")
    if packet.get("commands") != required_nested.get("commands"):
        fail("worker packet commands differ from the phase receipt")
    if packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet known failures differ from the phase receipt")
    expected_changed = [
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0132/Statement.lean",
        "Stage1_Instances/THM-M-0132/check_statement.py",
        "Stage1_Instances/THM-M-0132/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0132/statement-blocker.md",
        "Stage1_Instances/THM-M-0132/statement-receipt.json",
        "Stage1_Instances/THM-M-0132/statement.json",
    ]
    if packet.get("changed_paths") != expected_changed:
        fail("worker packet changed-path inventory changed")

    status = subprocess.run(
        [
            "git",
            "-c",
            "status.relativePaths=false",
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    if status.returncode:
        fail("could not inspect the worker-owned delta")
    actual_changed = []
    for line in status.stdout.splitlines():
        relative = line[3:]
        if relative == "Formalizations/Lean/.lake":
            continue
        if relative == ".stage1-worker-selftest.json" or relative.startswith(
            f"Stage1_Instances/{THEOREM_ID}/"
        ):
            actual_changed.append(relative)
            continue
        fail(f"unexpected changed path outside worker ownership: {relative}")
    if sorted(actual_changed) != sorted(expected_changed):
        fail("worker packet changed paths do not match the Git delta")


def validate_text_boundaries() -> None:
    relatives = {
        *ROLE_PATHS.values(),
        "Stage1_Instances/THM-M-0132/check_statement.py",
        "Stage1_Instances/THM-M-0132/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0132/statement-blocker.md",
        ".stage1-worker-selftest.json",
    }
    for relative in relatives:
        data = (ROOT / relative).read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            fail(f"text artifact has a malformed byte boundary: {relative}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            fail(f"text artifact has trailing whitespace: {relative}")


def validate_lean_probe() -> None:
    result = subprocess.run(
        [
            "lake",
            "env",
            "lean",
            "--trust=0",
            "../../Stage1_Instances/THM-M-0132/Statement.lean",
        ],
        cwd=ROOT / "Formalizations" / "Lean",
        env={**os.environ, "LC_ALL": "C", "TZ": "UTC"},
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if result.returncode:
        fail(f"trust-level-0 Lean boundary probe failed: {result.stderr.strip()}")
    expected = (
        "WeierstrassCurve.IsElliptic",
        "CongruenceSubgroup.Gamma0",
        "CongruenceSubgroup.Gamma1",
        "CuspForm",
    )
    if any(token not in result.stdout for token in expected):
        fail("Lean boundary probe output is incomplete")


def main() -> None:
    validate_authority()
    validate_ledger()
    validate_statement_boundary()
    validate_receipt_and_packet()
    validate_text_boundaries()
    validate_lean_probe()
    print(json.dumps(SEMANTIC, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
