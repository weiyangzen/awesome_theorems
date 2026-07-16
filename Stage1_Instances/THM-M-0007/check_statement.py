#!/usr/bin/env python3
"""Validate the fail-closed THM-M-0007 statement evidence packet."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0007"
THEOREM_ID = "THM-M-0007"
ITEM_ID = "S56-M-0007-STATEMENT"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
ROLE_PATHS = {
    "statement_record": "Stage1_Instances/THM-M-0007/statement.json",
    "statement_source": "Stage1_Instances/THM-M-0007/Statement.lean",
    "source_crosswalk": "Stage1_Instances/THM-M-0007/source-statement-crosswalk.md",
    "phase_receipt": "Stage1_Instances/THM-M-0007/statement-receipt.json",
}
EXPECTED_ROLE_HASHES = {
    "statement_record": "fb95cd8a536bb37217e19e09b7b8cd3de589f9f7369d8789283583462819d256",
    "statement_source": "fa3d7efa2c6376a0401d2af98c535725eff1eb01581c3c222399ff4a06feff98",
    "source_crosswalk": "f94ec499c564a19df87fa08fa893508f512b053d67786ff8aa510b6ac715cb50",
}
EXPECTED_ROLE_BLOBS = {
    "statement_record": "0efa30b51c1556ca6489185ddf0e38f0d5429b64",
    "statement_source": "67fa1aaadf8bdd1a8011fb818dd534e92f0930f6",
    "source_crosswalk": "967c58302007a6535e2848411a9d4b193cd1046a",
}
EXPECTED_AUTHORITY_HASHES = {
    "Docs/Stage1_Blueprint_v2.md": "fb6cd286dc5c47e22d754ab73e5162986e98a18b5bc6d8e7213ae5d39b4256d1",
    "Docs/Stage1_Blueprint_rev-5.6.md": "3779901013ac5e0b1f1b2bb4ea7a2ee08429f85bb1ee26c4b96905d6796c65c8",
    "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "5da11caafdb40b121c2fd19e13cd232a1b13a615f7a64eb314aa82cc19fea454",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_SUPPORT_HASHES = {
    "Docs/researches/math_theorems.md": "bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29",
    "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_094.lean": "99790fe00cca6aaa5429cb183e410095cd1febe648f5162af232abc2feaef5b7",
    "Stage1_Instances/THM-M-0007/instance.json": "89b53807b8b517a4aecc317db758c6e1744fe82dc38b126a22b1f9f4d4369bd6",
    "Stage1_Instances/THM-M-0007/scope-map.md": "6ffb5ae59343ab3cf2d9186e41a938a6912671f2bd29ff6d566d8e729e9b079e",
    "Stage1_Instances/THM-M-0007/task-dag.json": "0900689d5bef88be1b5c43351965474b9aed99bc986f259520c1d99f542eb893",
    "Stage1_Instances/THM-M-0007/dependency-reuse-ledger.json": "cf723437655235405deda4d88b33d2a8b0f0842caaddb9d5e15130084537385a",
    "Stage1_Instances/THM-M-0007/statement-blocker.md": "0ab04721dddc0ad8ba6633222cec477125ea1633b4ee7186f81b2d7d5d0ea544",
}
DIRECT_IMPORTS = (
    "Mathlib.CategoryTheory.Abelian.RightDerived",
    "Mathlib.Algebra.Homology.SpectralSequence.Basic",
)
CHECKED_SYMBOLS = (
    "ExpectedE2Term",
    "ExpectedAbutment",
    "FirstQuadrantE2Carrier",
    "SpectralSequence.page",
)
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)
CANONICAL_DECLARATION = re.compile(
    r"^[ \t]*(?:def|theorem|lemma|example|abbrev|opaque|axiom|structure)\s+"
    r"(?:GrothendieckSpectralSequenceTarget|CanonicalTarget|StatementShape)\b",
    flags=re.MULTILINE,
)


def fail(message: str) -> NoReturn:
    print(f"THM-M-0007 statement validator: {message}", file=sys.stderr)
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
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def git(*argv: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *argv],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
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
    if target.get("execution_rank") != 94 or target.get("lifecycle_mode") != "planned":
        fail("target manifest identity or lifecycle changed")
    if target.get("legacy_artifacts_accepted") is not False:
        fail("legacy evidence unexpectedly acquired acceptance")

    execution = load("Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row.get("id") == ITEM_ID)
    expected_item = {
        "id": ITEM_ID,
        "theorem_id": THEOREM_ID,
        "execution_rank": 94,
        "phase": "statement",
        "layer": 1,
        "state": "[ ]",
        "depends_on": ["S56-M-0007-INTAKE"],
        "owned_paths": ["Stage1_Instances/THM-M-0007"],
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
    if node.get("v2_execution_rank") != 316 or node.get("topological_layer") != 0:
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
    if validators != ["Stage1_Instances/THM-M-0007/check_statement.py"]:
        fail("validator candidate selection is not exactly one path")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("statement contract unexpectedly permits blocked phase closure")
    if phase.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        fail("statement contract unexpectedly treats negative evidence as completion")


def validate_ledger() -> None:
    ledger = load("Stage1_Instances/THM-M-0007/dependency-reuse-ledger.json")
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
    if closure.get("claim_order") != {
        "v2_execution_rank": 316,
        "phase_layer": 1,
        "phase_item_id": ITEM_ID,
    }:
        fail("dependency ledger claim order changed")


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
        "blocked_on_source_exact_convergence_and_naturality_boundary"
    ):
        fail("statement ambiguity is no longer explicit")
    formal = statement.get("canonical_formal_target", {})
    if statement.get("canonical_statement") is not None:
        fail("a canonical mathematical statement was invented")
    if formal.get("declaration_or_expression") is not None:
        fail("a canonical Lean declaration or expression was invented")
    if formal.get("elaborated_expression_sha256") is not None:
        fail("a missing expression fingerprint was invented")
    if formal.get("statement_file_sha256") != EXPECTED_ROLE_HASHES["statement_source"]:
        fail("statement boundary source hash is stale")
    negative_probe = statement.get("negative_probe", {})
    if tuple(negative_probe.get("direct_imports", [])) != DIRECT_IMPORTS:
        fail("structured direct imports changed")
    mutations = statement.get("mutation_tests", {})
    if mutations.get("executed") != [] or mutations.get("status") != (
        "blocked_without_canonical_expression"
    ):
        fail("mutation blocker boundary changed")
    if statement.get("statement_elaborated") is not False:
        fail("statement record falsely claims exact target elaboration")
    if statement.get("audit_complete") is not False or statement.get("theorem_complete") is not False:
        fail("statement record falsely closes a terminal decision")

    imports = tuple(re.findall(r"^import ([^\s]+)$", source, re.MULTILINE))
    if imports != DIRECT_IMPORTS:
        fail("boundary source direct imports disagree")
    if PROHIBITED.search(source):
        fail("boundary source contains a prohibited placeholder or trust construct")
    if CANONICAL_DECLARATION.search(source):
        fail("boundary source unexpectedly declares a canonical target")
    checks = tuple(re.findall(r"^#check ([^\s]+)$", source, re.MULTILINE))
    if checks != CHECKED_SYMBOLS:
        fail("boundary source interface probes changed")
    for name in ("ExpectedE2Term", "ExpectedAbutment", "FirstQuadrantE2Carrier"):
        if len(re.findall(rf"^abbrev {name}\b", source, re.MULTILINE)) != 1:
            fail(f"boundary abbreviation missing or duplicated: {name}")
    required_terms = (
        "page-level transcription",
        "objectwise construction versus a natural spectral sequence",
        "weak, strong, or another source-defined convergence notion",
        "excluded proxy",
    )
    combined = crosswalk + "\n" + blocker
    if any(term not in combined for term in required_terms):
        fail("source ambiguity or proxy non-credit boundary is incomplete")


def validate_environment() -> None:
    lean_dir = ROOT / "Formalizations" / "Lean"
    manifest = load("Formalizations/Lean/lake-manifest.json")
    mathlib_revision = next(
        row["rev"] for row in manifest["packages"] if row.get("name") == "mathlib"
    )
    mathlib = lean_dir / ".lake" / "packages" / "mathlib"
    if not mathlib.is_dir():
        fail("canonical pinned mathlib artifact is unavailable")
    if mathlib_revision != "8a178386ffc0f5fef0b77738bb5449d50efeea95":
        fail("mathlib manifest revision changed")
    if git("rev-parse", "HEAD", cwd=mathlib) != mathlib_revision:
        fail("materialized mathlib revision changed")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != (
        "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
    ):
        fail("materialized mathlib tree changed")
    import_hashes = {
        "Mathlib.CategoryTheory.Abelian.RightDerived": (
            "60f35e828394accc6e20610bf1df4200bc3ca27e5c054d84426d77cb1d5cc70f"
        ),
        "Mathlib.Algebra.Homology.SpectralSequence.Basic": (
            "23bb64ea21861fe1f216b6204779007599e5ac873686505811c27a1aef03cfd8"
        ),
    }
    for module, expected in import_hashes.items():
        path = mathlib / (module.replace(".", "/") + ".lean")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            fail(f"direct import source changed: {module}")

    matches: list[str] = []
    convergence = re.compile(
        r"StronglyConverges|stronglyConverges|ConvergesTo|convergesTo|abutment|Abutment"
    )
    for subtree in (
        mathlib / "Mathlib" / "Algebra" / "Homology",
        mathlib / "Mathlib" / "CategoryTheory",
    ):
        for path in subtree.rglob("*.lean"):
            if convergence.search(path.read_text(encoding="utf-8", errors="strict")):
                matches.append(str(path.relative_to(mathlib)))
    if matches:
        fail("typed convergence-token search is no longer empty")


def validate_receipt_and_packet() -> None:
    receipt = load(ROLE_PATHS["phase_receipt"])
    required = {
        "schema_version",
        "receipt_id",
        "item_id",
        "theorem_id",
        "phase",
        "intent",
        "base_revision",
        "base_tree",
        "inputs",
        "support_state",
        "proposed_state",
        "accepted",
        "verdict",
        "selftest_status",
        "selftest_result",
        "known_failures",
        "first_failed_gate",
        "retry_condition",
        "status_boundary",
        "audit_complete",
        "theorem_complete",
        "invalidation_inputs",
        "statement_fingerprints",
        "mutation_tests",
    }
    if not required <= set(receipt):
        fail("phase receipt omits contract-required fields")
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
    if receipt.get("selftest_result", {}).get("phase_predicate_passed") is not False:
        fail("phase receipt falsely says the positive phase predicate passed")
    if receipt.get("statement_fingerprints") != []:
        fail("phase receipt invents a statement fingerprint")
    if receipt.get("first_failed_gate") != (
        "S02-EXACT-TARGET.source_exact_convergence_unfrozen"
    ):
        fail("phase receipt first failed gate changed")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("phase receipt falsely closes a terminal decision")
    if receipt.get("inputs", {}).get("parent_inspection_order") != []:
        fail("phase receipt parent inspection order changed")
    if receipt.get("inputs", {}).get("provider_acceptance_inherited") is not False:
        fail("phase receipt transfers provider acceptance")

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
            fail(f"phase receipt Git-blob binding changed: {role}")
    self_binding = bindings.get("phase_receipt", {})
    if self_binding.get("path") != ROLE_PATHS["phase_receipt"]:
        fail("phase receipt self-binding path changed")
    if self_binding.get("sha256") is not None or self_binding.get("git_blob") is not None:
        fail("phase receipt self-binding must remain scheduler-owned and acyclic")

    packet = load(".stage1-worker-selftest.json")
    required_packet_fields = {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    if set(packet) != required_packet_fields:
        fail("worker packet fields changed")
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
        "Stage1_Instances/THM-M-0007/README.md",
        "Stage1_Instances/THM-M-0007/Statement.lean",
        "Stage1_Instances/THM-M-0007/check_statement.py",
        "Stage1_Instances/THM-M-0007/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0007/source-statement-crosswalk.md",
        "Stage1_Instances/THM-M-0007/statement-blocker.md",
        "Stage1_Instances/THM-M-0007/statement-receipt.json",
        "Stage1_Instances/THM-M-0007/statement.json",
    ]
    if packet.get("changed_paths") != expected_changed:
        fail("worker packet changed-path inventory changed")


def semantic_result() -> dict[str, Any]:
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
        "first_failed_gate": "S02-EXACT-TARGET.source_exact_convergence_unfrozen",
        "open_obligations": 6,
        "stale_inputs": [],
        "blocked": True,
        "message": (
            "Negative statement packet self-tested: the pinned categorical substrate elaborates, "
            "but the source-exact convergence target, expression fingerprint, typed transport, "
            "and four required mutations remain unavailable."
        ),
    }


def main() -> None:
    try:
        validate_authority()
        validate_ledger()
        validate_statement_boundary()
        validate_environment()
        validate_receipt_and_packet()
    except Exception as error:
        if isinstance(error, SystemExit):
            raise
        fail(str(error))
    print(json.dumps(semantic_result(), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
