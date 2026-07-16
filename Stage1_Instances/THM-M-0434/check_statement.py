#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0434 statement packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0434"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM_ID = "S56-M-0434-STATEMENT"
THEOREM_ID = "THM-M-0434"
BASE_REVISION = "307c34d30fc3763c82a944a142ae922b48ff18aa"
BASE_TREE = "ef45ba442c71959db78ad146a023bcf32946a53f"
GRAPH_SHA256 = "8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROBE_STDOUT_SHA256 = "6301409cbcad14585946ce70a8fdee223e07d8322d672e5090ba652b0391136f"

ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0434/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0434/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0434/source_statement_crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0434/statement-receipt.json",
}
ROLE_HASHES = {
    "statement_record": "703f97ade153ca51338dea81f81fa8d2c1be7a29d9889e4ba36633578f489c5d",
    "statement_source": "8f627d0c8fccedd6116e66700ad87f7312cfe594cace0674cb3e7b795d7e91af",
    "source_crosswalk": "d6b925dd141d7807bb034c0fc8b8c0b04592683b371ded20241420452ab35503",
}
ROLE_BLOBS = {
    "statement_record": "f61b3bbf581870c4c48868ac82376c256fd25e81",
    "statement_source": "b070e6c12237b3e3da27b4e6229964d883952278",
    "source_crosswalk": "1167c0645114e42df64ce61b9e11dc9329a3a317",
}
AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": "2a5bc7d397e03969aac1a9f8f21b437152b8ef63ef453055acf67857ced628b5",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "fe70128eba4e3878fbc58625bc7f602be4020e5e2edd6b94b134436568086d65",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
SUPPORT_HASHES = {
    "Stage1_Instances/THM-M-0434/intake.json": "04f4ac8032e9891a24d31fc9be1e26984de5884e7b137aaac082b7585874aa21",
    "Stage1_Instances/THM-M-0434/dependency-reuse-ledger.json": "ec1def76df0cd07a524731165cf22ebfc00d07adcf740fe040a822deec0c4d39",
    "Stage1_Instances/THM-M-0434/statement-blocker-head-307c34d30.md": "930cc66a75904fee3662000f6f13bb13e9ba48a3a267086c5e33b99d3153365d",
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_083.lean": "d105f07451150a7e396e969ff063967e166b898b007f45990b6b9f20bd5913b8",
}
DIRECT_IMPORTS = (
    "Mathlib.NumberTheory.LocalField.Basic",
    "Mathlib.AlgebraicGeometry.Scheme",
    "Mathlib.MeasureTheory.Measure.Haar.Basic",
)
EXPECTED_CHECKS = (
    "IsNonarchimedeanLocalField",
    "AlgebraicGeometry.Scheme",
    "MeasureTheory.Measure.IsHaarMeasure",
)
EXPECTED_CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    "Stage1_Instances/THM-M-0434/Statement.lean",
    "Stage1_Instances/THM-M-0434/check_statement.py",
    "Stage1_Instances/THM-M-0434/dependency-reuse-ledger.json",
    "Stage1_Instances/THM-M-0434/statement-blocker-head-307c34d30.md",
    "Stage1_Instances/THM-M-0434/statement-receipt.json",
    "Stage1_Instances/THM-M-0434/statement.json",
]
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)
CANONICAL_DECLARATION = re.compile(
    r"^[ \t]*(?:def|theorem|lemma|example|abbrev|opaque|axiom)\s+"
    r"(?:Ngo|FundamentalLemma|CanonicalTarget|StatementShape)",
    flags=re.MULTILINE | re.IGNORECASE,
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


def fail(message: str) -> NoReturn:
    raise ValueError(message)


def load(relative: str) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate JSON key {key!r} in {relative}")
            result[key] = value
        return result

    value = json.loads(
        (ROOT / relative).read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicates,
    )
    if not isinstance(value, dict):
        fail(f"{relative} is not one JSON object")
    return value


def digest(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def git_blob(relative: str) -> str:
    data = (ROOT / relative).read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git(*argv: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *argv], cwd=cwd, text=True, capture_output=True, timeout=30
    )
    if result.returncode:
        fail(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def pointer(value: Any, raw: str) -> Any:
    current = value
    for token in raw.lstrip("/").split("/"):
        if not isinstance(current, dict) or token not in current:
            fail(f"missing receipt pointer {raw}")
        current = current[token]
    return current


def run_lean(relative: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["lake", "env", "lean", "--trust=0", relative],
        cwd=LEAN_ROOT,
        env={"PATH": str(Path(sys.executable).parent) + ":" + __import__("os").environ["PATH"],
             "LC_ALL": "C", "TZ": "UTC"},
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=180,
    )


def validate_authority() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("repository HEAD differs from the worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("repository tree differs from the worker base")
    for relative, expected in AUTHORITY_HASHES.items():
        if digest(relative) != expected:
            fail(f"authority input changed: {relative}")
    for relative, expected in SUPPORT_HASHES.items():
        if digest(relative) != expected:
            fail(f"support input changed: {relative}")

    targets = load("Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row.get("theorem_id") == THEOREM_ID)
    if target.get("execution_rank") != 83 or target.get("lifecycle_mode") != "planned":
        fail("target identity or lifecycle changed")
    if target.get("legacy_artifacts_accepted") is not False:
        fail("legacy evidence unexpectedly acquired acceptance")

    execution = load("Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row.get("id") == ITEM_ID)
    expected_item = {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 83,
        "phase": "statement",
        "layer": 1,
        "state": "[ ]",
        "depends_on": ["S56-M-0434-INTAKE"],
        "owned_paths": ["Stage1_Instances/THM-M-0434"],
        "deliverable": "Elaborate the exact Lean 4 target with the minimal pinned imports.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    if item != expected_item:
        fail("authoritative statement item changed")

    theorem_dag = load("Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM_ID)
    if node.get("v2_execution_rank") != 309 or node.get("topological_layer") != 0:
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
            fail(f"dependency field {field} is no longer empty")

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
        fail("statement artifact role selection changed")
    validators = [
        row["path_pattern"].format(theorem_id=THEOREM_ID)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM_ID)).is_file()
    ]
    if validators != ["Stage1_Instances/THM-M-0434/check_statement.py"]:
        fail("validator candidate selection is not exactly one declared path")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("contract unexpectedly permits blocked phase closure")
    if phase.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        fail("contract unexpectedly treats negative findings as the deliverable")


def validate_ledger() -> None:
    ledger = load("Stage1_Instances/THM-M-0434/dependency-reuse-ledger.json")
    if ledger.get("schema_version") != "stage1-dependency-reuse-ledger/1.1":
        fail("dependency ledger schema changed")
    if ledger.get("consumer_theorem_id") != THEOREM_ID:
        fail("dependency ledger owner changed")
    if ledger.get("observed_theorem_dag_sha256") != GRAPH_SHA256:
        fail("dependency ledger graph binding changed")
    if ledger.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency ledger context binding changed")
    if ledger.get("repository_revision") != BASE_REVISION:
        fail("dependency ledger repository revision changed")
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
            fail(f"empty dependency field {field} changed")
    closure = ledger.get("closure_audit", {})
    if closure.get("claim_order_key") != [309, 1, ITEM_ID]:
        fail("dependency ledger claim order changed")
    if closure.get("parent_inspection_order") != []:
        fail("parent inspection order is not the exact empty closure")
    if closure.get("provider_acceptance_inherited") is not False:
        fail("dependency ledger transfers provider acceptance")


def validate_statement_boundary() -> None:
    statement = load(ROLE_PATHS["statement_record"])
    source = (ROOT / ROLE_PATHS["statement_source"]).read_text(encoding="utf-8")
    crosswalk = (ROOT / ROLE_PATHS["source_crosswalk"]).read_text(encoding="utf-8")
    blocker = (HERE / "statement-blocker-head-307c34d30.md").read_text(encoding="utf-8")
    legacy = (ROOT / "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_083.lean").read_text(
        encoding="utf-8"
    )
    for role, expected in ROLE_HASHES.items():
        if digest(ROLE_PATHS[role]) != expected or git_blob(ROLE_PATHS[role]) != ROLE_BLOBS[role]:
            fail(f"selected artifact binding changed: {role}")
    if statement.get("schema_version") != "stage1-statement/1.0":
        fail("statement record schema changed")
    if statement.get("item_id") != ITEM_ID or statement.get("theorem_id") != THEOREM_ID:
        fail("statement record identity changed")
    if statement.get("canonical_statement") is not None:
        fail("a canonical mathematical statement was invented")
    formal = statement.get("canonical_formal_target", {})
    for field in (
        "declaration_or_expression",
        "elaborated_expression_sha256",
        "environment_expression_fingerprint",
    ):
        if formal.get(field) is not None:
            fail(f"canonical formal field {field} was invented")
    if statement.get("statement_fingerprints") != []:
        fail("statement record invents a fingerprint")
    if set(statement.get("mutation_tests", {}).values()) != {"not_run_no_canonical_target"}:
        fail("statement mutation blocker changed")
    if statement.get("statement_elaborated") is not False:
        fail("statement record falsely claims exact elaboration")
    if statement.get("phase_predicate_proven") is not False or statement.get("phase_accepted") is not False:
        fail("statement record falsely claims the positive predicate")
    if statement.get("audit_complete") is not False or statement.get("theorem_complete") is not False:
        fail("statement record falsely closes a terminal decision")

    imports = tuple(re.findall(r"^import ([^\s]+)$", source, re.MULTILINE))
    checks = tuple(re.findall(r"^#check ([^\s]+)$", source, re.MULTILINE))
    if imports != DIRECT_IMPORTS or checks != EXPECTED_CHECKS:
        fail("negative probe boundary changed")
    if PROHIBITED.search(source) or CANONICAL_DECLARATION.search(source):
        fail("negative probe contains a prohibited or canonical declaration")
    combined = crosswalk + "\n" + blocker
    required_terms = (
        "Lie-algebra Fundamental Lemma",
        "characteristic",
        "normalization",
        "statementShape_of_orbital_integral_identity",
        "declares no canonical target",
    )
    if any(term not in combined for term in required_terms):
        fail("source or blocker boundary is incomplete")
    for term in (
        "structure OrbitalIntegralComparison",
        "def StatementShape",
        "def StatementShapeWithHyperspecialModel",
        "theorem statementShape_of_orbital_integral_identity",
    ):
        if term not in legacy:
            fail("legacy discovery boundary changed")

    probe = run_lean("../../Stage1_Instances/THM-M-0434/Statement.lean")
    if probe.returncode or probe.stderr:
        fail(f"negative Lean probe failed: {probe.stdout}{probe.stderr}")
    if hashlib.sha256(probe.stdout.encode()).hexdigest() != PROBE_STDOUT_SHA256:
        fail("negative Lean probe output changed")
    if probe.stdout.count(" : Prop") != 2 or "Scheme" not in probe.stdout:
        fail("negative Lean probe did not check the declared interfaces")

    version = subprocess.run(
        ["lake", "env", "lean", "--version"],
        cwd=LEAN_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
    )
    if version.returncode or LEAN_COMMIT not in version.stdout:
        fail("Lean toolchain identity changed")
    mathlib = LEAN_ROOT / ".lake/packages/mathlib"
    if git("rev-parse", "HEAD", cwd=mathlib) != MATHLIB_REVISION:
        fail("mathlib revision changed")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != MATHLIB_TREE:
        fail("mathlib tree changed")
    if git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib):
        fail("mathlib dependency worktree is dirty")


def validate_receipt_and_packet() -> None:
    receipt = load(ROLE_PATHS["phase_receipt"])
    for raw in REQUIRED_RECEIPT_POINTERS:
        pointer(receipt, raw)
    if receipt.get("schema_version") != "stage1-node-receipt/1.0":
        fail("phase receipt schema changed")
    if (receipt.get("item_id"), receipt.get("theorem_id"), receipt.get("phase"), receipt.get("intent")) != (
        ITEM_ID, THEOREM_ID, "statement", "audit"
    ):
        fail("phase receipt identity changed")
    if receipt.get("base_revision") != BASE_REVISION or receipt.get("base_tree") != BASE_TREE:
        fail("phase receipt base changed")
    if receipt.get("support_state") != "provisional_worker_selftest_blocked":
        fail("phase receipt support state changed")
    if receipt.get("proposed_state") != "[_]" or receipt.get("selftest_status") != "passed":
        fail("phase receipt worker handoff changed")
    if receipt.get("accepted") is not False or receipt.get("verdict") != "blocked":
        fail("phase receipt no longer preserves blocked semantics")
    if receipt.get("phase_predicate_proven") is not False or receipt.get("phase_accepted") is not False:
        fail("phase receipt falsely claims positive statement closure")
    if receipt.get("statement_fingerprints") != []:
        fail("phase receipt invents a statement fingerprint")
    if set(receipt.get("mutation_tests", {}).values()) != {"not_run_no_canonical_target"}:
        fail("phase receipt mutation boundary changed")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("phase receipt falsely closes a terminal decision")
    if receipt.get("first_failed_gate") != (
        "S02-EXACT-TARGET.exact_source_statement_identity_and_definition_chain"
    ):
        fail("phase receipt first failed gate changed")
    inputs = receipt.get("inputs", {})
    if inputs.get("parent_inspection_order") != [] or inputs.get("provider_acceptance_inherited") is not False:
        fail("phase receipt dependency boundary changed")
    for label, binding in inputs.items():
        if not isinstance(binding, dict) or "path" not in binding:
            continue
        relative = binding.get("path")
        if not isinstance(relative, str) or not (ROOT / relative).is_file():
            fail(f"phase receipt input path is missing: {label}")
        if binding.get("sha256") != digest(relative):
            fail(f"phase receipt input SHA-256 is stale: {label}")
        if binding.get("git_blob") != git_blob(relative):
            fail(f"phase receipt input Git blob is stale: {label}")

    validator_binding = receipt.get("validator_binding", {})
    validator_relative = "Stage1_Instances/THM-M-0434/check_statement.py"
    if validator_binding.get("path") != validator_relative:
        fail("phase receipt validator path changed")
    if validator_binding.get("sha256") != digest(validator_relative):
        fail("phase receipt validator SHA-256 is stale")
    if validator_binding.get("git_blob") != git_blob(validator_relative):
        fail("phase receipt validator Git blob is stale")

    bindings = {row.get("role"): row for row in receipt.get("artifact_bindings", [])}
    if set(bindings) != set(ROLE_PATHS):
        fail("phase receipt artifact role bindings are incomplete")
    for role in ROLE_HASHES:
        binding = bindings[role]
        if (
            binding.get("path") != ROLE_PATHS[role]
            or binding.get("sha256") != ROLE_HASHES[role]
            or binding.get("git_blob") != ROLE_BLOBS[role]
        ):
            fail(f"phase receipt selected binding changed: {role}")
    self_binding = bindings["phase_receipt"]
    if self_binding.get("path") != ROLE_PATHS["phase_receipt"]:
        fail("phase receipt self-binding path changed")
    if self_binding.get("sha256") is not None or self_binding.get("git_blob") is not None:
        fail("phase receipt self-binding is recursive")

    packet = load(".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id", "worker_verdict", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }:
        fail("worker packet fields changed")
    if packet.get("item_id") != ITEM_ID or packet.get("worker_verdict") != "blocked":
        fail("worker packet identity changed")
    if packet.get("base_revision") != BASE_REVISION or packet.get("state") != "[_]":
        fail("worker packet base or state changed")
    if packet.get("changed_paths") != EXPECTED_CHANGED_PATHS:
        fail("worker packet changed-path inventory changed")
    if packet.get("commands") != receipt.get("selftest_result", {}).get("commands"):
        fail("worker packet commands differ from the receipt")
    if packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet known failures differ from the receipt")
    if packet.get("output_summary") != receipt.get("selftest_result", {}).get("output_summary"):
        fail("worker packet output summary differs from the receipt")
    if receipt.get("changed_paths") != EXPECTED_CHANGED_PATHS:
        fail("phase receipt changed-path inventory changed")

    actual = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all", "--", str(HERE), ".stage1-worker-selftest.json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
    )
    if actual.returncode:
        fail("could not inspect the owned worktree delta")
    actual_paths = sorted(line[3:] for line in actual.stdout.splitlines() if len(line) > 3)
    if actual_paths != sorted(EXPECTED_CHANGED_PATHS):
        fail("owned worktree delta differs from the handoff inventory")
    for relative in EXPECTED_CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            fail(f"changed file has a noncanonical byte boundary: {relative}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            fail(f"changed file has trailing whitespace: {relative}")


def semantic_result(message: str) -> dict[str, Any]:
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
        "first_failed_gate": (
            "S02-EXACT-TARGET.exact_source_statement_identity_and_definition_chain"
        ),
        "open_obligations": 4,
        "stale_inputs": [],
        "blocked": True,
        "message": message,
    }


def main() -> None:
    try:
        validate_authority()
        validate_ledger()
        validate_statement_boundary()
        validate_receipt_and_packet()
    except Exception as exc:
        result = semantic_result(
            f"negative statement packet validation failed: {type(exc).__name__}: {exc}"
        )
        result.update({
            "status": "failed",
            "verdict": "repair_required",
            "first_failed_gate": "VALIDATOR-INTERNAL-CONSISTENCY",
            "blocked": False,
        })
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    print(json.dumps(
        semantic_result(
            "Target-scoped negative statement packet self-tested: the exact source proposition, "
            "faithful Lean object model, expression fingerprint, checked transports, and four "
            "mutation classes remain open; command success does not imply phase acceptance."
        ),
        sort_keys=True,
        separators=(",", ":"),
    ))


if __name__ == "__main__":
    main()
