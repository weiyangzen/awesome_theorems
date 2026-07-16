#!/usr/bin/env python3
"""Fail-closed semantic validator for S56-M-0423-PROOF."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0423"
ITEM = "S56-M-0423-PROOF"
THEOREM = "THM-M-0423"
BASE_REVISION = "2dc5a410b68eff806858fd6ed0cb33d57f6209f7"
BASE_TREE = "841bdd6114e7436cff4a3a1ff248fc1e884a9ddc"
GRAPH_SHA256 = "3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa"
CONTEXT_SHA256 = "ced38ea3f671f427ebca5031cbe9686378aa8ecec11067923cafe84643218044"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
REGISTRY_DENOMINATOR = "32a5c78d7f9cf7b59541a9a35c52331cf5055159b93dbe758b3eb6134f7da866"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
SHARED_GROUPS = [
    "SHARED-MODULE-42c19d5b5a6d6b9e",
    "SHARED-MODULE-74cc3b6464e1332d",
]
EXACT_DECLARATIONS = [
    "Stage1.THM_M_0423.Proof.isIsotropic_iff_of_isometryEquiv",
    "Stage1.THM_M_0423.Proof.equivalent_weightedSumSquares_units",
    "Stage1.THM_M_0423.Proof.equivalent_sumSquares_of_isAlgClosed",
    "Stage1.THM_M_0423.Proof.equivalent_sumSquares_complex",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}
EXPECTED_AXIOMS = {
    "isIsotropic_iff_of_isometryEquiv": {"propext", "Quot.sound"},
    "equivalent_weightedSumSquares_units": {
        "propext", "Classical.choice", "Quot.sound",
    },
    "equivalent_sumSquares_of_isAlgClosed": {
        "propext", "Classical.choice", "Quot.sound",
    },
    "equivalent_sumSquares_complex": {
        "propext", "Classical.choice", "Quot.sound",
    },
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


def printed_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        rf"'Stage1\.THM_M_0423\.Proof\.{re.escape(declaration)}' "
        r"depends on axioms: \[(?P<axioms>.*?)\]",
        flags=re.DOTALL,
    )
    match = pattern.search(output)
    if match is None:
        fail(f"missing axiom report for {declaration}")
    return set(re.findall(r"[A-Za-z][A-Za-z0-9_.]*", match.group("axioms")))


def lean_replay() -> str:
    lean_root = ROOT / "Formalizations" / "Lean"
    lake = lean_root / ".lake"
    if not lake.exists():
        fail("pinned .lake artifacts are unavailable; dependency fetching is forbidden")
    mathlib = lake / "packages" / "mathlib"
    if git("rev-parse", "HEAD", cwd=mathlib) != MATHLIB_REVISION:
        fail("pinned mathlib revision changed")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != MATHLIB_TREE:
        fail("pinned mathlib tree changed")
    if git("status", "--porcelain=v1", cwd=mathlib):
        fail("pinned mathlib worktree is dirty")

    lake_bin = Path(os.environ.get("HOME", str(Path.home()))) / ".elan" / "bin" / "lake"
    if not lake_bin.is_file():
        fail("pinned Lake launcher is unavailable")
    env_result = subprocess.run(
        [str(lake_bin), "env", "printenv", "LEAN_PATH"],
        cwd=lean_root,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if env_result.returncode:
        fail(f"cannot resolve pinned LEAN_PATH: {env_result.stderr.strip()}")
    lean_path = env_result.stdout.strip()
    outputs: list[str] = []
    with tempfile.TemporaryDirectory(prefix="thm-m-0423-proof-") as raw_tmp:
        tmp = Path(raw_tmp)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        commands = [
            [
                str(lake_bin), "env", "lean", "--trust=0", "-t0", f"--root={tmp}",
                str(tmp / "Statement.lean"), "-o", str(tmp / "Statement.olean"),
            ],
            [
                str(lake_bin), "env", "lean", "--trust=0", "-t0", f"--root={tmp}",
                str(tmp / "ObligationTree.lean"), "-o", str(tmp / "ObligationTree.olean"),
            ],
            [
                str(lake_bin), "env", "lean", "--trust=0", "-t0", f"--root={tmp}",
                str(tmp / "Proof.lean"),
            ],
        ]
        for index, argv in enumerate(commands):
            env = {
                "LC_ALL": "C",
                "LANG": "C",
                "TZ": "UTC",
                "NO_COLOR": "1",
                "LEAN_NUM_THREADS": "1",
                "PATH": (
                    str(lake_bin.parent) + ":" + str(Path(sys.executable).parent)
                    + ":/usr/local/bin:/usr/bin:/bin"
                ),
                "HOME": str(Path.home()),
            }
            if index:
                env["LEAN_PATH"] = f"{tmp}:{lean_path}"
            result = subprocess.run(
                argv, cwd=lean_root, env=env, capture_output=True, text=True, timeout=240
            )
            if result.returncode:
                fail(
                    f"trust-zero Lean replay step {index + 1} failed: "
                    f"{result.stdout}{result.stderr}"
                )
            outputs.append(result.stdout + result.stderr)
    return outputs[-1]


def verify() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("repository HEAD differs from the claimed worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("repository tree differs from the claimed worker base")

    authorities = {
        "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
        "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    }
    for relative, expected in authorities.items():
        if digest(ROOT / relative) != expected:
            fail(f"authority input changed: {relative}")

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row.get("theorem_id") == THEOREM)
    if target.get("execution_rank") != 67 or target.get("theorem_complete") is not False:
        fail("target membership, rank, or completion boundary changed")

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row.get("id") == ITEM)
    if item != {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 67,
        "phase": "proof",
        "layer": 4,
        "state": "[ ]",
        "depends_on": ["S56-M-0423-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }:
        fail("authoritative proof item changed")
    predecessor = next(
        row for row in execution["items"]
        if row.get("id") == "S56-M-0423-OBLIGATION_TREE"
    )
    if predecessor.get("state") != "[_]":
        fail("observed prerequisite state changed")

    theorem_dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM)
    if node.get("v2_execution_rank") != 301 or node.get("topological_layer") != 0:
        fail("v2 execution order changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency context changed")
    if node.get("direct_hard_parents") != [] or node.get("transitive_hard_ancestors") != []:
        fail("hard-parent closure is no longer empty")
    if node.get("direct_reuse_hint_ids") != []:
        fail("reuse-hint closure is no longer empty")
    if node.get("shared_lemma_group_ids") != SHARED_GROUPS:
        fail("shared-group context changed")

    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row.get("phase") == "proof")
    if phase.get("layer") != 4 or phase.get("intent") != "prove":
        fail("proof phase contract changed")
    if [row.get("path_pattern") for row in phase["validator_candidates"]] != [
        "Stage1_Instances/{theorem_id}/check_proof.py",
        "Stage1_Instances/{theorem_id}/check_proof.sh",
    ]:
        fail("proof validator candidates changed")
    if (HERE / "check_proof.sh").exists():
        fail("proof validator selection is ambiguous")

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
        fail("dependency ledger base changed")
    for field in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids", "reuse_hint_ids",
        "inspections", "unresolved_compatibility_obligations",
    ):
        if ledger.get(field) != []:
            fail(f"dependency ledger field {field} is no longer empty")
    if ledger.get("shared_group_ids") != SHARED_GROUPS:
        fail("dependency ledger shared groups changed")
    decisions = ledger.get("reuse_decisions")
    if not isinstance(decisions, list) or [row.get("source_id") for row in decisions] != SHARED_GROUPS:
        fail("dependency ledger decisions are incomplete or out of order")
    for row in decisions:
        if row.get("decision") != "not_applicable":
            fail("dependency ledger invents accepted reuse")
        if row.get("context_digest") != CONTEXT_SHA256 or not row.get("non_reuse_reason"):
            fail("dependency ledger weak-group decision is unbound")
        for relative, expected in row.get("inspected_member_artifacts", {}).items():
            if digest(ROOT / relative) != expected:
                fail(f"inspected weak-group artifact changed: {relative}")
    audit = ledger.get("closure_audit", {})
    if audit.get("parent_inspection_order") != []:
        fail("parent inspection order is not the authoritative empty closure")
    if audit.get("claim_order") != {
        "v2_execution_rank": 301,
        "phase_layer": 4,
        "phase_item_id": ITEM,
    }:
        fail("claim order changed")

    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    if registry.get("denominator_sha256") != REGISTRY_DENOMINATOR:
        fail("obligation denominator changed")
    if graphs.get("registry_denominator_sha256") != REGISTRY_DENOMINATOR:
        fail("typed graph denominator changed")
    if len(registry.get("obligations", [])) != 105:
        fail("obligation count changed")
    if len(graphs.get("nodes", [])) != 105:
        fail("typed graph node count changed")
    if graphs.get("composition_certificates") != []:
        fail("unreviewed composition certificates appeared")

    proof_source = (HERE / "Proof.lean").read_text(encoding="utf-8")
    if PROHIBITED.search(strip_comments_and_strings(proof_source)):
        fail("prohibited placeholder or trust construct found in Proof.lean")
    required_markers = {
        "theorem isIsotropic_iff_of_isometryEquiv",
        "theorem equivalent_weightedSumSquares_units",
        "theorem equivalent_sumSquares_of_isAlgClosed",
        "theorem equivalent_sumSquares_complex",
        "#print axioms isIsotropic_iff_of_isometryEquiv",
        "#print axioms equivalent_weightedSumSquares_units",
        "#print axioms equivalent_sumSquares_of_isAlgClosed",
        "#print axioms equivalent_sumSquares_complex",
    }
    missing = sorted(marker for marker in required_markers if marker not in proof_source)
    if missing:
        fail(f"proof source is missing required declaration markers: {missing}")

    receipt = load(HERE / "proof-receipt.json")
    required_fields = {
        pointer.split("/")[-1]
        for pointer in phase.get("phase_receipt_required_fields", [])
        if pointer.count("/") == 1
    }
    if not required_fields <= set(receipt):
        fail("proof receipt omits contract-required fields")
    if receipt.get("schema_version") != "stage1-node-receipt/1.0":
        fail("proof receipt schema changed")
    for field, expected in (
        ("item_id", ITEM), ("theorem_id", THEOREM), ("phase", "proof"),
        ("intent", "prove"), ("base_revision", BASE_REVISION), ("base_tree", BASE_TREE),
    ):
        if receipt.get(field) != expected:
            fail(f"proof receipt field {field} changed")
    if receipt.get("support_state") != "provisional_worker_selftest":
        fail("proof receipt support state changed")
    if receipt.get("proposed_state") != "[_]" or receipt.get("accepted") is not False:
        fail("proof receipt overstates acceptance")
    if receipt.get("verdict") != "blocked":
        fail("proof receipt worker verdict changed")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("proof contract no longer keeps blocked evidence open")
    if receipt.get("selftest_status") != "passed":
        fail("proof receipt self-test status changed")
    commands = receipt.get("selftest_result", {}).get("commands")
    if not isinstance(commands, list) or not commands:
        fail("proof receipt lacks exact self-test commands")
    if not all(isinstance(row, dict) and isinstance(row.get("argv"), list) for row in commands):
        fail("proof receipt self-test command records are malformed")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("proof receipt overstates a terminal decision")
    if receipt.get("canonical_target") != "Stage1.THM_M_0423.HasseMinkowskiStatement":
        fail("canonical target changed")
    if receipt.get("exact_declarations") != EXACT_DECLARATIONS:
        fail("exact declaration inventory changed")
    if receipt.get("closed_obligation_ids") != []:
        fail("proof receipt invents accepted obligation closure")
    body = receipt.get("proof_body", {})
    if body.get("source") != f"Stage1_Instances/{THEOREM}/Proof.lean":
        fail("proof body path changed")
    if body.get("source_sha256") != digest(HERE / "Proof.lean"):
        fail("proof body source binding changed")
    inputs = receipt.get("inputs", {})
    expected_inputs = {
        "proof_sources": [{
            "path": f"Stage1_Instances/{THEOREM}/Proof.lean",
            "sha256": digest(HERE / "Proof.lean"),
            "git_blob": git("hash-object", str(HERE / "Proof.lean")),
        }],
        "dependency_reuse_ledger": {
            "path": f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json",
            "sha256": digest(HERE / "dependency-reuse-ledger.json"),
            "git_blob": git("hash-object", str(HERE / "dependency-reuse-ledger.json")),
        },
    }
    for field, expected in expected_inputs.items():
        if inputs.get(field) != expected:
            fail(f"proof receipt input binding changed: {field}")
    if "provider_material" in inputs:
        fail("proof receipt claims provider material despite no reuse")
    for field, filename in (
        ("statement_sha256", "Statement.lean"),
        ("obligation_tree_sha256", "ObligationTree.lean"),
        ("obligation_registry_sha256", "obligation-registry.json"),
        ("typed_graphs_sha256", "typed-graphs.json"),
        ("anchor_audit_sha256", "anchor-audit.json"),
    ):
        if inputs.get(field) != digest(HERE / filename):
            fail(f"proof receipt input changed: {field}")
    validator_binding = inputs.get("proof_validator", {})
    if validator_binding != {
        "path": f"Stage1_Instances/{THEOREM}/check_proof.py",
        "sha256": digest(HERE / "check_proof.py"),
        "git_blob": git("hash-object", str(HERE / "check_proof.py")),
    }:
        fail("proof receipt validator binding changed")
    for field, filename in (
        ("proof_blocker", "proof-blocker.json"),
        ("proof_validation", "proof-validation.md"),
    ):
        if inputs.get(field) != {
            "path": f"Stage1_Instances/{THEOREM}/{filename}",
            "sha256": digest(HERE / filename),
            "git_blob": git("hash-object", str(HERE / filename)),
        }:
            fail(f"proof receipt evidence binding changed: {field}")
    if receipt.get("result", {}).get("exit_code") != 0:
        fail("proof receipt does not record a successful target validator")
    if receipt.get("result", {}).get("phase_predicate_proven") is not False:
        fail("proof receipt falsely proves the complete phase predicate")
    if receipt.get("result", {}).get("phase_accepted") is not False:
        fail("proof receipt falsely accepts the proof phase")
    if receipt.get("result", {}).get("root_kernel_closed") is not False:
        fail("proof receipt falsely closes the root")

    packet = load(ROOT / ".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "verdict", "state",
    }:
        fail("worker packet fields changed")
    if packet.get("item_id") != ITEM or packet.get("state") != "[_]":
        fail("worker packet identity or state changed")
    if packet.get("verdict") != "blocked":
        fail("worker packet verdict changed")
    if packet.get("base_revision") != BASE_REVISION:
        fail("worker packet base changed")
    if set(packet.get("changed_paths", [])) != CHANGED_PATHS:
        fail("worker packet changed-path inventory is incomplete")
    if packet.get("commands") != commands:
        fail("worker packet commands disagree with the proof receipt")
    if packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet failures disagree with the proof receipt")
    status = subprocess.check_output(
        ["git", "status", "--short", "--untracked-files=all"], cwd=ROOT, text=True
    )
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    if actual_changed != CHANGED_PATHS:
        fail(f"worktree delta disagrees with worker packet: {sorted(actual_changed)}")

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            fail(f"invalid text encoding or final newline: {relative}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            fail(f"trailing whitespace: {relative}")

    lean_output = lean_replay()
    for declaration, expected in EXPECTED_AXIOMS.items():
        if printed_axioms(lean_output, declaration) != expected:
            fail(f"unexpected axiom profile for {declaration}")


def semantic_result(*, passed: bool, message: str) -> dict[str, Any]:
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "phase": "proof",
        "status": "blocked" if passed else "failed",
        "verdict": "blocked" if passed else "repair_required",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": (
            "P04-KERNEL.M0423-T-LOCAL-GLOBAL" if passed else "P01-ARTIFACTS"
        ),
        "open_obligations": 94,
        "stale_inputs": [],
        "blocked": passed,
        "message": message,
    }


def main() -> None:
    try:
        verify()
    except (AssertionError, KeyError, OSError, RuntimeError, ValueError) as error:
        result = semantic_result(
            passed=False, message=f"proof evidence replay failed: {error}"
        )
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        raise SystemExit(1)
    result = semantic_result(
        passed=True,
        message=(
            "The empty hard-parent closure, both weak shared groups, four partial "
            "placeholder-free declarations, and their trust-zero axiom profiles were "
            "replayed; the exact local-to-global body and complete proof predicate remain open."
        ),
    )
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
