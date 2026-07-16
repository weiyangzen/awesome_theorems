#!/usr/bin/env python3
"""Fail-closed semantic validator for S56-M-0122-PROOF."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any, NoReturn


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0122"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0122-PROOF"
THEOREM = "THM-M-0122"
BASE_REVISION = "307c34d30fc3763c82a944a142ae922b48ff18aa"
BASE_TREE = "ef45ba442c71959db78ad146a023bcf32946a53f"
GRAPH_SHA256 = "8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
ROOT_EXPRESSION_SHA256 = "f3e5f585b30ab9543bc47551d0d91c695523bace26fdb5484869add319ef7dac"
REGISTRY_DENOMINATOR = "fa58b3f6f5f390a8fd776a0d789158582ec5ded0f22616a94460d6eb0306a508"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
PROOF_STDOUT_SHA256 = "fb39843cb284e2a02ec84fb3449f4759358ff524799a36b5f654d3e21b967a55"
ROOT_CUT = [
    "M0122-N-FINITE-EXTENSION",
    "M0122-C-ABEL-JACOBI",
    "M0122-L-MORDELL-WEIL",
    "M0122-L-MORDELL-LANG",
    "M0122-L-NO-POSITIVE-COSET",
    "M0122-L-FINITE-INTERSECTION",
]
EXACT_DECLARATIONS = [
    "Stage1Instances.THMM0122.Proof.finite_of_injective_to",
    "Stage1Instances.THMM0122.Proof.finite_of_two_injections",
    "Stage1Instances.THMM0122.Proof.faltingsTarget_of_packages",
]
EXPECTED_STATIC_HASHES = {
    "Statement.lean": "824c2d9410bbf3117fa6340e4259f9a3a7df6ff892c4b7cc6dad94a03ab437e8",
    "ObligationTree.lean": "c081ee9e08e5bf5aeb3060605ebc9c7f7926d08d04632380e105e8ff1c783c69",
    "Proof.lean": "07c9c730d01964dc4aeea81b2af34a8fc59a105301751e78ea0eccfa1a521e1a",
    "anchor-audit.json": "3da3f5c769e138a1c623eea5395483982e068a1d23c7f06fd69842f13524ac16",
    "obligation-registry.json": "776919528add8197b01b864b11c71aeea85c549dbcfead8b3b9395e340a43ff0",
    "typed-graphs.json": "d3d8f88bb2cb87910c63b5664e1e2695fc7641a538e52954e8cd08df9dc8e329",
    "validation-specs.json": "e84f59f222c73a7cf847cc3189e59040492e915048fa3b4d29a60cab2fca4d3f",
    "dependency-reuse-ledger.json": "eb8858b6e9554a702800dd4e892b5e10f4c83133a116579736504d3f959d301d",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Proof.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json",
    f"Stage1_Instances/{THEOREM}/proof-blocker.json",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe|extern)\b",
    re.MULTILINE,
)


class ValidationError(RuntimeError):
    """A target-scoped semantic validation failure."""


def fail(message: str) -> NoReturn:
    raise ValidationError(message)


def load(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate JSON key {key!r} in {path.relative_to(ROOT)}")
            result[key] = value
        return result

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
        )
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {path.relative_to(ROOT)}: {error}")
    if not isinstance(value, dict):
        fail(f"expected one JSON object in {path.relative_to(ROOT)}")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, timeout=timeout, check=False,
    )


def git(*argv: str, cwd: Path = ROOT) -> str:
    result = run(["git", *argv], cwd=cwd)
    if result.returncode:
        fail(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def git_blob(relative: str) -> str:
    return git("hash-object", "--no-filters", relative)


def strip_comments_and_strings(source: str) -> str:
    output: list[str] = []
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
                output.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif quoted:
            output.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            index += 1
        elif pair == "/-":
            depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            end = source.find("\n", index)
            if end < 0:
                output.extend(" " * (len(source) - index))
                index = len(source)
            else:
                output.extend(" " * (end - index))
                index = end
        elif char == '"':
            quoted = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    if depth or quoted:
        fail("unterminated Lean comment or string")
    return "".join(output)


def lean_replay() -> str:
    lake = shutil.which("lake")
    if lake is None:
        fail("pinned Lake launcher is unavailable")
    lean_path_result = run([lake, "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT)
    if lean_path_result.returncode:
        fail(f"cannot resolve pinned LEAN_PATH: {lean_path_result.stderr.strip()}")
    lean_result = run([lake, "env", "which", "lean"], cwd=LEAN_ROOT)
    if lean_result.returncode:
        fail(f"cannot resolve pinned Lean: {lean_result.stderr.strip()}")
    lean = lean_result.stdout.strip()
    if not Path(lean).is_file():
        fail("resolved Lean executable is not a file")
    base_env = {
        **os.environ,
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "NO_COLOR": "1",
        "LEAN_NUM_THREADS": "1",
    }
    with tempfile.TemporaryDirectory(prefix="thm-m-0122-proof-") as raw_tmp:
        tmp = Path(raw_tmp)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        commands = [
            ("Statement.lean", "Statement.olean"),
            ("ObligationTree.lean", "ObligationTree.olean"),
            ("Proof.lean", None),
        ]
        proof_output = ""
        for index, (source, object_name) in enumerate(commands):
            argv = [
                lean, "--trust=0", "-t0", f"--root={tmp}", str(tmp / source),
            ]
            if object_name is not None:
                argv += ["-o", str(tmp / object_name)]
            env = dict(base_env)
            env["LEAN_PATH"] = (
                lean_path_result.stdout.strip()
                if index == 0
                else f"{tmp}:{lean_path_result.stdout.strip()}"
            )
            result = subprocess.run(
                argv, cwd=LEAN_ROOT, env=env, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=240, check=False,
            )
            if result.returncode:
                fail(
                    f"trust-zero Lean replay step {index + 1} failed: "
                    f"{result.stdout}{result.stderr}"
                )
            if index == 2:
                proof_output = result.stdout + result.stderr
    return proof_output


def verify_authorities() -> tuple[dict[str, Any], dict[str, Any]]:
    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("repository HEAD differs from the claimed worker base")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("repository tree differs from the claimed worker base")
    if sha256(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") != GRAPH_SHA256:
        fail("authoritative theorem DAG changed")
    if sha256(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") != CONTRACT_SHA256:
        fail("HEAD phase contract changed")
    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    expected_row = (
        "- [ ] `S56-M-0122-PROOF` / `THM-M-0122` / `proof`: "
        "Implement or pin/import the required proof bodies without placeholders. {attempts=0}"
    )
    if blueprint.count(expected_row) != 1:
        fail("authoritative proof row changed or is ambiguous")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    item = next(row for row in execution["items"] if row.get("id") == ITEM)
    if item != {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 41,
        "phase": "proof",
        "layer": 4,
        "state": "[ ]",
        "depends_on": ["S56-M-0122-OBLIGATION_TREE"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Implement or pin/import the required proof bodies without placeholders.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }:
        fail("authoritative proof item changed")
    predecessor = next(
        row for row in execution["items"]
        if row.get("id") == "S56-M-0122-OBLIGATION_TREE"
    )
    if predecessor.get("state") != "[_]":
        fail("observed prerequisite state changed")
    theorem_dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(
        row for row in theorem_dag["theorems"]
        if row.get("theorem_id") == THEOREM
    )
    if node.get("v2_execution_rank") != 275 or node.get("topological_layer") != 0:
        fail("v2 claim order changed")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        fail("dependency context changed")
    for field in (
        "direct_hard_parents", "transitive_hard_ancestors",
        "direct_reuse_hint_ids", "shared_lemma_group_ids",
    ):
        if node.get(field) != []:
            fail(f"authoritative empty dependency context changed at {field}")
    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row.get("phase") == "proof")
    if phase.get("layer") != 4 or phase.get("intent") != "prove":
        fail("proof phase contract identity changed")
    if phase.get("raw_blocked_can_close_phase") is not False:
        fail("blocked proof semantics changed")
    candidates = [
        row["path_pattern"].format(theorem_id=THEOREM)
        for row in phase["validator_candidates"]
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM)).is_file()
    ]
    if candidates != [f"Stage1_Instances/{THEOREM}/check_proof.py"]:
        fail("proof validator candidate selection is missing or ambiguous")
    at_base = run([
        "git", "cat-file", "-e",
        f"{BASE_REVISION}:Stage1_Instances/{THEOREM}/check_proof.py",
    ])
    if at_base.returncode == 0:
        fail("validator unexpectedly existed at the worker base")
    return phase, node


def verify_artifacts(phase: dict[str, Any]) -> None:
    for name, expected in EXPECTED_STATIC_HASHES.items():
        if sha256(HERE / name) != expected:
            fail(f"target proof input changed: {name}")
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
        fail("dependency ledger base binding changed")
    for field in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "parent_inspection_order",
        "inspections", "reuse_decisions", "unresolved_compatibility_obligations",
    ):
        if ledger.get(field) != []:
            fail(f"empty dependency closure changed at {field}")
    if ledger.get("closure_audit", {}).get("status") != "complete_for_declared_empty_context":
        fail("empty dependency closure was not audited")
    statement = load(HERE / "statement.json")
    if statement["canonical_formal_target"]["elaborated_expression_sha256"] != ROOT_EXPRESSION_SHA256:
        fail("canonical target fingerprint changed")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    if registry.get("denominator_sha256") != REGISTRY_DENOMINATOR:
        fail("obligation denominator changed")
    if graphs.get("registry_denominator_sha256") != REGISTRY_DENOMINATOR:
        fail("typed graph denominator changed")
    closure = graphs.get("closure_boundary", {})
    if closure.get("accepted_closed_obligations") != []:
        fail("typed graph invents accepted proof closure")
    if closure.get("root_closed") is not False:
        fail("typed graph falsely closes the root")
    if closure.get("remaining_machine_root_cut_set") != ROOT_CUT:
        fail("machine root cut changed")
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        source = (HERE / name).read_text(encoding="utf-8")
        if PROHIBITED.search(strip_comments_and_strings(source)):
            fail(f"prohibited proof or trust construct in {name}")
    proof = (HERE / "Proof.lean").read_text(encoding="utf-8")
    for marker in (
        "theorem finite_of_injective_to",
        "theorem finite_of_two_injections",
        "theorem faltingsTarget_of_packages",
        "(normalize : FiniteExtensionNormalization.{u})",
        "(abelJacobi : AbelJacobiPackage.{u})",
        "(mordellLang : MordellLangFinitenessPackage.{u})",
        "assert_no_sorry faltingsTarget_of_packages",
    ):
        if marker not in proof:
            fail(f"proof source is missing marker: {marker}")
    receipt = load(HERE / "proof-receipt.json")
    required = {
        pointer.split("/")[-1]
        for pointer in phase["phase_receipt_required_fields"]
        if pointer.count("/") == 1
    }
    if not required <= set(receipt):
        fail("proof receipt omits contract-required fields")
    for field, expected in (
        ("schema_version", "stage1-node-receipt/1.0"),
        ("item_id", ITEM), ("theorem_id", THEOREM),
        ("phase", "proof"), ("intent", "prove"),
        ("base_revision", BASE_REVISION), ("base_tree", BASE_TREE),
        ("support_state", "provisional_worker_selftest"),
        ("proposed_state", "[_]"), ("verdict", "blocked"),
        ("selftest_status", "passed"),
    ):
        if receipt.get(field) != expected:
            fail(f"proof receipt field changed: {field}")
    if receipt.get("accepted") is not False:
        fail("proof receipt overstates master acceptance")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        fail("proof receipt crosses a terminal boundary")
    if receipt.get("canonical_target_expression_sha256") != ROOT_EXPRESSION_SHA256:
        fail("proof receipt target fingerprint changed")
    if receipt.get("exact_declarations") != EXACT_DECLARATIONS:
        fail("proof receipt declaration inventory changed")
    if receipt.get("closed_obligation_ids") != []:
        fail("proof receipt invents accepted obligation closure")
    if receipt.get("remaining_root_cut_set") != ROOT_CUT:
        fail("proof receipt root cut changed")
    result = receipt.get("result", {})
    if result.get("exit_code") != 0 or result.get("semantic_verdict") != "blocked":
        fail("proof receipt semantic result changed")
    if result.get("phase_predicate_proven") is not False:
        fail("proof receipt falsely proves the complete phase predicate")
    if result.get("phase_accepted") is not False or result.get("root_kernel_closed") is not False:
        fail("proof receipt falsely closes the phase or root")
    if result.get("proof_stdout_sha256") != PROOF_STDOUT_SHA256:
        fail("proof receipt Lean output binding changed")
    inputs = receipt.get("inputs", {})
    if inputs.get("parent_inspection_order") != []:
        fail("proof receipt parent inspection order changed")
    if inputs.get("provider_acceptance_inherited") is not False:
        fail("proof receipt inherits provider acceptance")
    if "provider_material" in inputs:
        fail("proof receipt claims provider material despite no reuse")
    if inputs.get("proof_sources") != [{
        "path": f"Stage1_Instances/{THEOREM}/Proof.lean",
        "sha256": sha256(HERE / "Proof.lean"),
        "git_blob": git_blob(f"Stage1_Instances/{THEOREM}/Proof.lean"),
    }]:
        fail("proof source binding changed")
    if inputs.get("dependency_reuse_ledger") != {
        "path": f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json",
        "sha256": sha256(HERE / "dependency-reuse-ledger.json"),
        "git_blob": git_blob(f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json"),
    }:
        fail("dependency ledger binding changed")
    for field, name in (
        ("proof_blocker", "proof-blocker.json"),
        ("proof_validation", "proof-validation.md"),
    ):
        relative = f"Stage1_Instances/{THEOREM}/{name}"
        if inputs.get(field) != {
            "path": relative,
            "sha256": sha256(HERE / name),
            "git_blob": git_blob(relative),
        }:
            fail(f"proof receipt evidence binding changed: {field}")
    validator = inputs.get("validator_candidate", {})
    validator_relative = f"Stage1_Instances/{THEOREM}/check_proof.py"
    if validator != {
        "path": validator_relative,
        "sha256": sha256(HERE / "check_proof.py"),
        "git_blob": git_blob(validator_relative),
        "existed_at_base": False,
        "current_claim_selection_eligible": False,
        "boundary": (
            "The validator is supplied for integration but did not exist at the worker "
            "base, so it cannot satisfy unchanged-base selection for this claim."
        ),
    }:
        fail("proof validator binding changed")
    blocker = load(HERE / "proof-blocker.json")
    if blocker.get("first_failed_gate") != "P04-KERNEL.M0122-N-FINITE-EXTENSION":
        fail("target-scoped blocker gate changed")
    if blocker.get("remaining_machine_root_cut_set") != ROOT_CUT:
        fail("target-scoped blocker cut changed")
    if blocker.get("proof_phase_complete") is not False:
        fail("target-scoped blocker falsely completes the proof phase")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "verdict", "state",
    }:
        fail("worker packet fields changed")
    if packet.get("item_id") != ITEM or packet.get("state") != "[_]":
        fail("worker packet identity or state changed")
    if packet.get("verdict") != "blocked" or packet.get("base_revision") != BASE_REVISION:
        fail("worker packet verdict or base changed")
    if set(packet.get("changed_paths", [])) != CHANGED_PATHS:
        fail("worker packet changed-path inventory is incomplete")
    if packet.get("commands") != receipt.get("selftest_result", {}).get("commands"):
        fail("worker packet commands disagree with the proof receipt")
    if packet.get("known_failures") != receipt.get("known_failures"):
        fail("worker packet failure boundary disagrees with the receipt")
    status = git("status", "--short", "--untracked-files=all")
    actual = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
        if (line[3:] if line[:2] == "??" else line[2:].lstrip())
        != "Formalizations/Lean/.lake"
    }
    if actual != CHANGED_PATHS:
        fail(f"worktree delta disagrees with worker packet: {sorted(actual)}")
    for relative in CHANGED_PATHS:
        data = (ROOT / relative).read_bytes()
        if not data.endswith(b"\n") or b"\r" in data or b"\x00" in data:
            fail(f"invalid text normalization: {relative}")
        if any(line.endswith((b" ", b"\t")) for line in data.splitlines()):
            fail(f"trailing whitespace: {relative}")


def verify_environment_and_lean() -> None:
    mathlib = LEAN_ROOT / ".lake" / "packages" / "mathlib"
    if not mathlib.is_dir():
        fail("pinned mathlib artifacts are unavailable; fetching is forbidden")
    if git("rev-parse", "HEAD", cwd=mathlib) != MATHLIB_REVISION:
        fail("pinned mathlib revision changed")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != MATHLIB_TREE:
        fail("pinned mathlib tree changed")
    if git("status", "--porcelain=v1", "--untracked-files=all", cwd=mathlib):
        fail("pinned mathlib worktree is dirty")
    output = lean_replay()
    if hashlib.sha256(output.encode("utf-8")).hexdigest() != PROOF_STDOUT_SHA256:
        fail("trust-zero proof output digest changed")
    if output.count("Declarations are sorry-free!") != 1:
        fail("Lean no-sorry assertion did not pass")
    if "sorryAx" in output or "declaration uses 'sorry'" in output:
        fail("Lean output reports a placeholder")
    normalized = re.sub(r"\s+", " ", output)
    if normalized.count("[propext, Classical.choice, Quot.sound]") != 3:
        fail("proof axiom profile changed")


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
            "P04-KERNEL.M0122-N-FINITE-EXTENSION" if passed else "P01-ARTIFACTS"
        ),
        "open_obligations": len(ROOT_CUT),
        "stale_inputs": [],
        "blocked": passed,
        "message": message,
    }


def main() -> int:
    try:
        phase, _node = verify_authorities()
        verify_artifacts(phase)
        verify_environment_and_lean()
    except (AssertionError, KeyError, OSError, RuntimeError, ValueError) as error:
        print(json.dumps(
            semantic_result(
                passed=False,
                message=f"proof evidence replay failed: {error}",
            ),
            sort_keys=True,
            separators=(",", ":"),
        ))
        return 1
    print(json.dumps(
        semantic_result(
            passed=True,
            message=(
                "The empty dependency closure and three target-owned partial or "
                "conditional bodies replayed at trust zero; six arithmetic-geometric "
                "root-cut packages and the complete proof predicate remain open."
            ),
        ),
        sort_keys=True,
        separators=(",", ":"),
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
