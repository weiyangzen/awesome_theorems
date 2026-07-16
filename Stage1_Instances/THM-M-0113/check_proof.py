#!/usr/bin/env python3
"""Fail-closed semantic validator for S56-M-0113-PROOF."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0113"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0113-PROOF"
THEOREM = "THM-M-0113"
BASE_REVISION = "94009a6bebd743588e09c3b45bfbf18bf9b5c5e3"
BASE_TREE = "daabee9f9b2c6e98d84b6290f78a209b950485fc"
GRAPH_SHA256 = "eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
TARGET_PRINT_SHA256 = "483a37eb70184d0596b11301c4e15018629fd00bbd8a601fdc6ad7691dcd7e84"
DENOMINATOR_SHA256 = "e509c1920e23d809083d43f1c19996cd20a97c5931144d4cb266eca39484cbd5"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
FLR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
FLR_TREE = "32c9eace926573a9981787ae97643e520353c893"
FROZEN_HASHES = {
    "Statement.lean": "73010040e7a16c02d00bfa95db270e2370440f433e8c3519e5e2ab429cd236dd",
    "statement.json": "38fed31b8341e67729ae2f638edb595361a099a7b7ecbaa0f1e336d0b342ac22",
    "AnchorAudit.lean": "2f62f6b16b5179d5d6634a885c47b6019529d4e36f64ed14f551a74035c5d565",
    "anchor-audit.json": "96d93459b27f3a95357e041e0a9cf589d849ef5066894551e646b5dbb5027795",
    "ObligationTree.lean": "c9fe3593539b1a3d221496ad45c3b5a9cfcd1355b3875f7b42d4012337273a95",
    "obligation-registry.json": "c8f592dd2961e08782a241355e0eaf2f1d6841b8e66b325bab5d07c936847f2d",
    "typed-graphs.json": "31b91ed2b0c42702819148e6ab02e222e06f801bd0e1cc9e81788d26f2606e34",
    "Proof.lean": "b05f2ef3eef236e026930097803c614d53eeaba65d5fa936b0293a7c4879ec6f",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    flags=re.MULTILINE,
)


class ValidationError(RuntimeError):
    pass


def fail(message: str) -> NoReturn:
    raise ValidationError(message)


def load(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, child in pairs:
            if key in value:
                fail(f"duplicate JSON key {key!r} in {path.relative_to(ROOT)}")
            value[key] = child
        return value

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
        )
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {path.relative_to(ROOT)}: {error}")
    if not isinstance(value, dict):
        fail(f"expected JSON object in {path.relative_to(ROOT)}")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*argv: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ["git", *argv], cwd=cwd, capture_output=True, text=True, timeout=30
    )
    if result.returncode:
        fail(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def strip_comments_and_strings(source: str) -> str:
    out: list[str] = []
    index = 0
    depth = 0
    quoted = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                out.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                out.extend("  ")
                index += 2
            else:
                out.append("\n" if char == "\n" else " ")
                index += 1
        elif quoted:
            out.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            index += 1
        elif pair == "/-":
            depth = 1
            out.extend("  ")
            index += 2
        elif pair == "--":
            end = source.find("\n", index)
            if end == -1:
                out.extend(" " * (len(source) - index))
                index = len(source)
            else:
                out.extend(" " * (end - index))
                index = end
        elif char == '"':
            quoted = True
            out.append(" ")
            index += 1
        else:
            out.append(char)
            index += 1
    if depth or quoted:
        fail("unterminated comment or string in Lean source")
    return "".join(out)


def verify_authorities() -> dict[str, Any]:
    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("repository HEAD differs from the claimed worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("repository tree differs from the claimed worker base")
    if digest(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") != GRAPH_SHA256:
        fail("authoritative theorem DAG changed")
    if digest(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") != CONTRACT_SHA256:
        fail("authoritative proof phase contract changed")

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row.get("theorem_id") == THEOREM)
    if target.get("execution_rank") != 25 or target.get("lifecycle_mode") != "planned":
        fail("target manifest identity or lifecycle changed")
    if target.get("theorem_complete") is not False:
        fail("target manifest unexpectedly claims theorem completion")

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row.get("id") == ITEM)
    expected_item = {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 25,
        "phase": "proof",
        "layer": 4,
        "state": "[ ]",
        "depends_on": ["S56-M-0113-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    if item != expected_item:
        fail("authoritative proof item changed")
    predecessor = next(
        row for row in execution["items"]
        if row.get("id") == "S56-M-0113-OBLIGATION_TREE"
    )
    if predecessor.get("state") != "[_]":
        fail("observed obligation-tree predecessor state changed")

    theorem_dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM)
    if node.get("v2_execution_rank") != 262 or node.get("topological_layer") != 0:
        fail("v2 claim order changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency context changed")
    for field in (
        "direct_hard_parents", "transitive_hard_ancestors",
        "direct_reuse_hint_ids", "shared_lemma_group_ids",
    ):
        if node.get(field) != []:
            fail(f"authoritative empty dependency closure changed: {field}")

    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase_rows = [row for row in contract["phases"] if row.get("phase") == "proof"]
    if len(phase_rows) != 1:
        fail("proof phase contract is missing or ambiguous")
    phase = phase_rows[0]
    if phase.get("layer") != 4 or phase.get("intent") != "prove":
        fail("proof phase layer or intent changed")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("proof contract no longer fails closed on blocked evidence")
    if phase.get("classified_negative_findings_may_satisfy_deliverable") is not False:
        fail("proof contract improperly credits negative evidence")
    candidates = phase.get("validator_candidates", [])
    if [row.get("path_pattern") for row in candidates] != [
        "Stage1_Instances/{theorem_id}/check_proof.py",
        "Stage1_Instances/{theorem_id}/check_proof.sh",
    ]:
        fail("proof validator candidates changed")
    existing = [
        row["path_pattern"].format(theorem_id=THEOREM) for row in candidates
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM)).is_file()
    ]
    if existing != [f"Stage1_Instances/{THEOREM}/check_proof.py"]:
        fail("proof validator candidate selection is not exact")
    return phase


def verify_owned_artifacts(phase: dict[str, Any]) -> dict[str, Any]:
    for name, expected in FROZEN_HASHES.items():
        if digest(HERE / name) != expected:
            fail(f"target-owned proof input changed: {name}")

    ledger = load(HERE / "dependency-reuse-ledger.json")
    if ledger.get("schema_version") != "stage1-dependency-reuse-ledger/1.1":
        fail("dependency ledger schema changed")
    if ledger.get("consumer_theorem_id") != THEOREM:
        fail("dependency ledger consumer changed")
    if ledger.get("observed_theorem_dag_sha256") != GRAPH_SHA256:
        fail("dependency ledger graph binding changed")
    if ledger.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency ledger context binding changed")
    if ledger.get("repository_revision") != BASE_REVISION:
        fail("dependency ledger revision binding changed")
    for field in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "inspections", "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        if ledger.get(field) != []:
            fail(f"dependency ledger empty closure changed: {field}")
    if ledger.get("closure_audit") != {
        "claim_order": {
            "v2_execution_rank": 262,
            "phase_layer": 4,
            "phase_item_id": ITEM,
        },
        "parent_inspection_order": [],
        "expected_inspection_count": 0,
        "actual_inspection_count": 0,
        "status": "empty_closure_inspected",
        "note": (
            "The authoritative v2 node has no direct hard parents, transitive hard "
            "ancestors, reuse hints, or shared lemma groups. The complete closure was "
            "inspected exactly once as empty; no provider bytes, receipt, declaration, "
            "or acceptance state were consumed."
        ),
    }:
        fail("dependency ledger closure audit changed")

    statement = load(HERE / "statement.json")
    if statement.get("declaration") != "Stage1Instances.THMM0113.HodgeDecompositionTarget":
        fail("canonical target declaration changed")
    if statement.get("elaborated_print_sha256") != TARGET_PRINT_SHA256:
        fail("canonical target expression fingerprint changed")
    if statement.get("source_sha256") != FROZEN_HASHES["Statement.lean"]:
        fail("statement source binding changed")
    if statement.get("proof_status") != "No proof of HodgeDecompositionTarget is declared or claimed.":
        fail("frozen statement status changed")

    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    if registry.get("root_obligation_id") != "M0113-ROOT":
        fail("root obligation changed")
    if registry.get("denominator_sha256") != DENOMINATOR_SHA256:
        fail("obligation denominator changed")
    if len(registry.get("obligations", [])) != 26:
        fail("obligation count changed")
    if len(graphs.get("nodes", [])) != 26:
        fail("typed graph node count changed")
    closure = graphs.get("closure_boundary", {})
    if closure.get("closed_obligations") != [] or closure.get("theorem_complete") is not False:
        fail("frozen graph improperly closes a positive obligation or theorem")

    for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean"):
        source = strip_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        if PROHIBITED.search(source):
            fail(f"prohibited proof or trust construct found in {name}")
    proof_source = (HERE / "Proof.lean").read_text(encoding="utf-8")
    for marker in (
        "theorem not_hodgeDecompositionTarget",
        "¬ HodgeDecompositionTarget.{0, 0, 0, 0}",
        "#print axioms not_hodgeDecompositionTarget",
    ):
        if marker not in proof_source:
            fail(f"negative kernel witness marker is missing: {marker}")

    receipt = load(HERE / "proof-receipt.json")
    required_top_level = {
        pointer[1:] for pointer in phase.get("phase_receipt_required_fields", [])
        if pointer.count("/") == 1
    }
    if not required_top_level <= set(receipt):
        fail("proof receipt omits contract-required fields")
    for field, expected in (
        ("schema_version", "stage1-node-receipt/1.0"),
        ("item_id", ITEM), ("theorem_id", THEOREM),
        ("phase", "proof"), ("intent", "prove"),
        ("base_revision", BASE_REVISION), ("base_tree", BASE_TREE),
        ("support_state", "provisional_worker_selftest"),
        ("proposed_state", "[_]"), ("verdict", "blocked"),
        ("selftest_status", "passed"),
        ("canonical_target", "Stage1Instances.THMM0113.HodgeDecompositionTarget"),
    ):
        if receipt.get(field) != expected:
            fail(f"proof receipt field changed: {field}")
    if receipt.get("accepted") is not False:
        fail("proof receipt overstates acceptance")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("proof receipt crosses a terminal boundary")
    if receipt.get("closed_obligation_ids") != []:
        fail("negative evidence cannot close positive obligations")
    if receipt.get("exact_declarations") != [
        "Stage1Instances.THMM0113.not_hodgeDecompositionTarget"
    ]:
        fail("proof receipt declaration inventory changed")
    if receipt.get("selftest_result", {}).get("exit_code") != 0:
        fail("proof receipt self-test exit code changed")
    commands = receipt.get("selftest_result", {}).get("commands")
    if not isinstance(commands, list) or not commands:
        fail("proof receipt lacks exact self-test commands")
    if not all(
        isinstance(row, dict) and isinstance(row.get("argv"), list)
        and isinstance(row.get("exit_code"), int) for row in commands
    ):
        fail("proof receipt self-test commands are malformed")
    expected_blocker_hash = digest(HERE / "proof-blocker.json")
    blocker = load(HERE / "proof-blocker.json")
    if blocker.get("base_revision") != BASE_REVISION or blocker.get("base_tree") != BASE_TREE:
        fail("proof blocker base binding changed")
    if blocker.get("outcome") != "blocked_by_current_base_checked_countermodel":
        fail("proof blocker outcome changed")
    if blocker.get("root_closed") is not False:
        fail("proof blocker unexpectedly closes the root")
    if blocker.get("audit_complete") is not False or blocker.get("theorem_complete") is not False:
        fail("proof blocker crosses a terminal boundary")
    if blocker.get("selftest_manifest_written") is not False:
        fail("proof blocker incorrectly claims to be the worker self-test manifest")

    inputs = receipt.get("inputs", {})
    proof_sources = inputs.get("proof_sources")
    if proof_sources != [{
        "path": f"Stage1_Instances/{THEOREM}/Proof.lean",
        "sha256": FROZEN_HASHES["Proof.lean"],
        "git_blob": git("hash-object", str(HERE / "Proof.lean")),
    }]:
        fail("proof receipt source binding changed")
    ledger_binding = inputs.get("dependency_reuse_ledger")
    if ledger_binding != {
        "path": f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json",
        "sha256": digest(HERE / "dependency-reuse-ledger.json"),
        "git_blob": git("hash-object", str(HERE / "dependency-reuse-ledger.json")),
    }:
        fail("proof receipt dependency ledger binding changed")
    if "provider_material" in inputs:
        fail("proof receipt invents provider material for an empty reuse context")
    for field, name in (
        ("statement_sha256", "Statement.lean"),
        ("statement_record_sha256", "statement.json"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
        ("proof_blocker_sha256", "proof-blocker.json"),
    ):
        expected = expected_blocker_hash if name == "proof-blocker.json" else digest(HERE / name)
        if inputs.get(field) != expected:
            fail(f"proof receipt input binding changed: {field}")
    validator = inputs.get("proof_validator", {})
    validator_path = HERE / "check_proof.py"
    if validator != {
        "path": f"Stage1_Instances/{THEOREM}/check_proof.py",
        "sha256": digest(validator_path),
        "git_blob": git("hash-object", str(validator_path)),
        "existed_at_base": False,
        "current_claim_selection_eligible": False,
    }:
        fail("proof receipt validator binding changed")
    body = receipt.get("proof_body", {})
    if body.get("source_sha256") != FROZEN_HASHES["Proof.lean"]:
        fail("proof receipt proof-body source binding changed")
    if body.get("positive_proof_credit") is not False:
        fail("proof receipt improperly credits the negative declaration")
    result = receipt.get("result", {})
    if result.get("exit_code") != 0 or result.get("semantic_verdict") != "blocked":
        fail("proof receipt semantic result changed")
    if result.get("phase_accepted") is not False or result.get("phase_predicate_proven") is not False:
        fail("proof receipt overstates the proof predicate")
    return receipt


def lean_replay() -> str:
    lake = LEAN_ROOT / ".lake"
    if not lake.exists():
        fail("pinned .lake artifacts are unavailable; dependency fetching is forbidden")
    mathlib = lake / "packages" / "mathlib"
    flr = lake / "packages" / "flt-regular"
    for package, revision, tree in (
        (mathlib, MATHLIB_REVISION, MATHLIB_TREE),
        (flr, FLR_REVISION, FLR_TREE),
    ):
        if git("rev-parse", "HEAD", cwd=package) != revision:
            fail(f"pinned package revision changed: {package.name}")
        if git("rev-parse", "HEAD^{tree}", cwd=package) != tree:
            fail(f"pinned package tree changed: {package.name}")
        if git("status", "--porcelain=v1", cwd=package):
            fail(f"pinned package worktree is dirty: {package.name}")

    lake_bin = Path.home() / ".elan" / "bin" / "lake"
    if not lake_bin.is_file():
        fail("pinned Lake launcher is unavailable")
    path_result = subprocess.run(
        [str(lake_bin), "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT,
        capture_output=True, text=True, timeout=60,
    )
    if path_result.returncode:
        fail(f"cannot resolve pinned LEAN_PATH: {path_result.stderr.strip()}")
    base_path = path_result.stdout.strip()

    with tempfile.TemporaryDirectory(prefix="thm-m-0113-proof-", dir="/tmp") as raw:
        scratch = Path(raw)
        for name in ("Statement.lean", "Proof.lean"):
            (scratch / name).write_bytes((HERE / name).read_bytes())
        fixed_env = {
            "HOME": str(Path.home()),
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "NO_COLOR": "1",
            "LEAN_NUM_THREADS": "1",
            "PATH": f"{lake_bin.parent}:/usr/local/bin:/usr/bin:/bin",
        }
        commands = [
            ([
                str(lake_bin), "env", "lean", "--trust=0", "-t0",
                f"--root={scratch}", "-o", str(scratch / "Statement.olean"),
                str(scratch / "Statement.lean"),
            ], fixed_env),
            ([
                str(lake_bin), "env", "lean", "--trust=0", "-t0",
                f"--root={scratch}", str(scratch / "Proof.lean"),
            ], {**fixed_env, "LEAN_PATH": f"{scratch}:{base_path}"}),
        ]
        outputs: list[str] = []
        for index, (argv, env) in enumerate(commands):
            result = subprocess.run(
                argv, cwd=LEAN_ROOT, env=env, capture_output=True, text=True, timeout=300
            )
            if result.returncode:
                fail(
                    f"trust-zero Lean replay step {index + 1} failed: "
                    f"{result.stdout}{result.stderr}"
                )
            outputs.append(result.stdout + result.stderr)
    output = outputs[-1]
    if (
        "theorem Stage1Instances.THMM0113.not_hodgeDecompositionTarget : "
        "¬HodgeDecompositionTarget" not in output
    ):
        fail("Lean replay did not print the exact refuted specialization")
    axiom_match = re.search(
        r"'Stage1Instances\.THMM0113\.not_hodgeDecompositionTarget' depends on axioms: "
        r"\[(?P<axioms>.*?)\]",
        output,
        flags=re.DOTALL,
    )
    if axiom_match is None:
        fail("Lean replay omitted the negative declaration axiom report")
    axioms = set(re.findall(r"[A-Za-z][A-Za-z0-9_.]*", axiom_match.group("axioms")))
    if axioms != {"propext", "Classical.choice", "Quot.sound"}:
        fail(f"unexpected negative declaration axiom profile: {sorted(axioms)}")
    return output


def verify_worker_packet(receipt: dict[str, Any]) -> None:
    packet = load(ROOT / ".stage1-worker-selftest.json")
    if packet.get("item_id") != ITEM or packet.get("state") != "[_]":
        fail("worker packet identity or state changed")
    if packet.get("verdict") != "blocked" or packet.get("base_revision") != BASE_REVISION:
        fail("worker packet verdict or base changed")
    required = {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/check_proof.py",
        f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json",
        f"Stage1_Instances/{THEOREM}/proof-blocker.json",
        f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    }
    if set(packet.get("changed_paths", [])) != required:
        fail("worker packet changed-path inventory is incomplete")
    if packet.get("commands") != receipt.get("selftest_result", {}).get("commands"):
        fail("worker packet command records disagree with the proof receipt")
    if packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet failures disagree with the proof receipt")
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    if actual != required:
        fail(f"worktree delta disagrees with worker packet: {sorted(actual)}")


def verify() -> None:
    phase = verify_authorities()
    receipt = verify_owned_artifacts(phase)
    verify_worker_packet(receipt)
    lean_replay()


def semantic_result(*, verified: bool, error: str | None = None) -> dict[str, Any]:
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "phase": "proof",
        "status": "blocked" if verified else "failed",
        "verdict": "blocked" if verified else "repair_required",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": (
            "P04-KERNEL/S56-5.1-EXACT-TARGET-CONSISTENCY/M0113-S-DATA"
            if verified else "P01-ARTIFACTS"
        ),
        "open_obligations": 26,
        "stale_inputs": [],
        "blocked": verified,
        "message": (
            "The empty dependency closure and target-owned exact countermodel were "
            "replayed at trust level zero; the frozen positive target is false, zero "
            "positive obligations are closed, and the proof phase remains blocked."
            if verified else f"Proof evidence replay failed: {error}"
        ),
    }


def main() -> int:
    try:
        verify()
    except Exception as error:
        result = semantic_result(verified=False, error=str(error))
        code = 1
    else:
        result = semantic_result(verified=True)
        code = 0
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
