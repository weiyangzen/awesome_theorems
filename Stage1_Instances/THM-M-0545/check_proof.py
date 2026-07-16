#!/usr/bin/env python3
"""Fail-closed semantic validator for S56-M-0545-PROOF."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0545"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0545-PROOF"
THEOREM = "THM-M-0545"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
DENOMINATOR_SHA256 = "52a39eb004a0689d978588caae3599283b4573967e97d66a8b8eb6caaae9896e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
STATEMENT_OLEAN_SHA256 = "0cb3c19973217747cb7ee91bb25171d50212bdef10d4246cd1d5ccc952cb1bce"
BOUNDARY_OUTPUT_SHA256 = "a3e7a99920e583bc2f934ad400af951ae9989b24410e7d7c68d18ae89a0c9f62"
REALIZATION_OUTPUT_SHA256 = "ea27796c6b2205a152959ad24901f96ca03213689439e9530ab83b4ddaff6e60"
EXPECTED_INPUT_HASHES = {
    "Statement.lean": "896d7efeaeaedb0ca19799622231b621f1fa731cd3f54634b687f0157afaf861",
    "ProofBoundaryCountermodel-2026-07-15.lean": "49e8a803d6e77a25045900bf94573f80f0da9a7353917277214b8316a6f06c27",
    "ProofCountermodel-2026-07-14.lean": "ba0abcdbae4e89bae1102f166c908233ab88cb8ad3999fd1d9b37705eb9f5d48",
    "statement.json": "e8201c7d9376b647aaa4724eacdd40bab178269752a49aad60272822d98f6892",
    "anchor-audit.json": "5b58b0c3d1e6c109654f8b0b3aa0ccd848783f37a4a5f0701857ae69c4d620d5",
    "obligation-registry.json": "7846553600eadbefe981c563071055292c6a714d38448cdc02d227a38d46fd04",
    "typed-graphs.json": "83bd6ca7107a2bed3d28660be0ed5139913079f1f17c50718cb64dd36d2e43e7",
}
PROOF_SOURCES = (
    "ProofBoundaryCountermodel-2026-07-15.lean",
    "ProofCountermodel-2026-07-14.lean",
)
NEGATIVE_DECLARATIONS = (
    "Stage1Instances.THMM0545.not_hodgeDecompositionTarget_degreeZero",
    "Stage1Instances.THMM0545.not_hodgeDecompositionTarget",
)
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
    r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern|external)\b",
    flags=re.MULTILINE,
)
COMMIT_RE = re.compile(r"[0-9a-f]{40,64}")
REMAINING_ROOT_CUT_SET = [
    "M0545-S-REALIZATION",
    "M0545-A-COMPLETION",
    "M0545-A-D",
    "M0545-A-ADJOINT",
    "M0545-A-LAPLACIAN",
    "M0545-A-ELLIPTIC",
    "M0545-A-GREEN",
    "M0545-L-CLOSED-RANGES",
    "M0545-S-BOUNDARY",
]


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


def run(argv: list[str], *, cwd: Path, env: dict[str, str]) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=600,
    )
    if result.returncode:
        fail(
            f"command failed ({result.returncode}): {' '.join(argv)}\n"
            f"{result.stdout}{result.stderr}"
        )
    return result.stdout + result.stderr


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        rf"'{re.escape(declaration)}' depends on axioms: \[(?P<axioms>.*?)\]",
        output,
        flags=re.DOTALL,
    )
    if match is None:
        fail(f"missing axiom report for {declaration}")
    return set(re.findall(r"[A-Za-z][A-Za-z0-9_.]*", match.group("axioms")))


def lean_replay() -> tuple[str, str, str]:
    lake = LEAN_ROOT / ".lake"
    if not lake.exists():
        fail("pinned .lake artifacts are unavailable; dependency fetching is forbidden")
    mathlib = lake / "packages" / "mathlib"
    if git("rev-parse", "HEAD", cwd=mathlib) != MATHLIB_REVISION:
        fail("pinned mathlib revision changed")
    if git("rev-parse", "HEAD^{tree}", cwd=mathlib) != MATHLIB_TREE:
        fail("pinned mathlib tree changed")
    if git("status", "--porcelain=v1", cwd=mathlib):
        fail("pinned mathlib worktree is dirty")

    lake_bin = Path.home() / ".elan" / "bin" / "lake"
    if not lake_bin.is_file():
        fail("pinned Lake launcher is unavailable")
    base_env = {
        "HOME": str(Path.home()),
        "PATH": f"{lake_bin.parent}:/usr/bin:/bin",
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "NO_COLOR": "1",
        "LEAN_NUM_THREADS": "1",
    }
    lean_path = run(
        [str(lake_bin), "env", "printenv", "LEAN_PATH"],
        cwd=LEAN_ROOT,
        env=base_env,
    ).strip()
    with tempfile.TemporaryDirectory(prefix="thm-m-0545-proof-") as raw_tmp:
        tmp = Path(raw_tmp)
        (tmp / "Statement.lean").write_bytes((HERE / "Statement.lean").read_bytes())
        (tmp / "ProofBoundaryCountermodel.lean").write_bytes(
            (HERE / PROOF_SOURCES[0]).read_bytes()
        )
        (tmp / "ProofCountermodel.lean").write_bytes(
            (HERE / PROOF_SOURCES[1]).read_bytes()
        )
        statement_env = dict(base_env, LEAN_PATH=lean_path)
        proof_env = dict(base_env, LEAN_PATH=f"{tmp}:{lean_path}")
        statement_output = run(
            [
                str(lake_bin), "env", "lean", "--trust=0", "-t0",
                f"--root={tmp}", "-o", str(tmp / "Statement.olean"),
                str(tmp / "Statement.lean"),
            ],
            cwd=LEAN_ROOT,
            env=statement_env,
        )
        boundary_output = run(
            [
                str(lake_bin), "env", "lean", "--trust=0", "-t0",
                f"--root={tmp}", str(tmp / "ProofBoundaryCountermodel.lean"),
            ],
            cwd=LEAN_ROOT,
            env=proof_env,
        )
        realization_output = run(
            [
                str(lake_bin), "env", "lean", "--trust=0", "-t0",
                f"--root={tmp}", str(tmp / "ProofCountermodel.lean"),
            ],
            cwd=LEAN_ROOT,
            env=proof_env,
        )
        if digest(tmp / "Statement.olean") != STATEMENT_OLEAN_SHA256:
            fail("Statement.olean content drifted")
    if hashlib.sha256(boundary_output.encode()).hexdigest() != BOUNDARY_OUTPUT_SHA256:
        fail("degree-zero countermodel output drifted")
    if hashlib.sha256(realization_output.encode()).hexdigest() != REALIZATION_OUTPUT_SHA256:
        fail("operator-realization countermodel output drifted")
    return statement_output, boundary_output, realization_output


def validate() -> None:
    if sys.flags.optimize:
        fail("proof validator requires Python assertions")
    authority_revision = git("rev-parse", "HEAD")
    authority_tree = git("rev-parse", "HEAD^{tree}")
    graph_sha256 = digest(ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json")
    contract_sha256 = digest(ROOT / "Docs" / "Stage1_Phase_Acceptance_Contracts.json")
    for name, expected in EXPECTED_INPUT_HASHES.items():
        if digest(HERE / name) != expected:
            fail(f"proof input drifted: {name}")

    theorem_dag = load(ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json")
    node = next(row for row in theorem_dag["theorems"] if row["theorem_id"] == THEOREM)
    if (node["v2_execution_rank"], node["topological_layer"]) != (321, 0):
        fail("v2 claim order identity drifted")
    if node["phase_states"]["proof"] not in {"[ ]", "[_]"}:
        fail("authoritative proof phase is outside worker-reviewable states")
    if node["dependency_context_sha256"] != CONTEXT_SHA256:
        fail("dependency context drifted")
    for key in (
        "direct_hard_parents", "transitive_hard_ancestors",
        "direct_reuse_hint_ids", "shared_lemma_group_ids",
    ):
        if node[key] != []:
            fail(f"unexpected dependency closure member in {key}")

    ledger = load(HERE / "dependency-reuse-ledger.json")
    expected_empty = (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "inspections", "reuse_decisions",
        "unresolved_compatibility_obligations",
    )
    if ledger["schema_version"] != "stage1-dependency-reuse-ledger/1.1":
        fail("dependency ledger schema drifted")
    if ledger["consumer_theorem_id"] != THEOREM:
        fail("dependency ledger owner drifted")
    if ledger["observed_theorem_dag_sha256"] != graph_sha256:
        fail("dependency ledger graph binding is stale")
    if ledger["dependency_context_sha256"] != CONTEXT_SHA256:
        fail("dependency ledger context binding is stale")
    ledger_revision = ledger.get("repository_revision")
    if (
        not isinstance(ledger_revision, str)
        or COMMIT_RE.fullmatch(ledger_revision) is None
        or subprocess.run(
            ["git", "merge-base", "--is-ancestor", ledger_revision, authority_revision],
            cwd=ROOT,
            capture_output=True,
            timeout=30,
        ).returncode != 0
    ):
        fail("dependency ledger revision binding is stale")
    if any(ledger[key] != [] for key in expected_empty):
        fail("empty dependency closure was not preserved")
    if ledger.get("closure_audit") != {
        "inspection_order": [],
        "expected_inspection_count": 0,
        "actual_inspection_count": 0,
        "status": "empty_closure_inspected",
        "note": (
            "The authoritative v2 node has no direct hard parents, transitive hard "
            "ancestors, reuse hints, or shared lemma groups. No provider evidence or "
            "acceptance was consumed."
        ),
    }:
        fail("empty dependency closure audit is incomplete")

    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    if registry["root_obligation_id"] != "M0545-ROOT":
        fail("root obligation drifted")
    if registry["denominator_sha256"] != DENOMINATOR_SHA256:
        fail("obligation denominator drifted")
    if graphs["registry_denominator_sha256"] != DENOMINATOR_SHA256:
        fail("typed graph denominator drifted")
    boundary = graphs["closure_boundary"]
    if boundary["root_closed"] is not False:
        fail("typed graph falsely closes the root")
    if boundary["remaining_root_cut_set"] != REMAINING_ROOT_CUT_SET:
        fail("typed graph root cut set drifted")

    for name in ("Statement.lean", *PROOF_SOURCES):
        source = strip_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        if PROHIBITED.search(source):
            fail(f"prohibited proof or trust construct in {name}")
    boundary_source = (HERE / PROOF_SOURCES[0]).read_text(encoding="utf-8")
    realization_source = (HERE / PROOF_SOURCES[1]).read_text(encoding="utf-8")
    for marker in (
        "theorem not_isExact_zero",
        "theorem no_degreeZeroDecomposition",
        "theorem not_hodgeDecompositionTarget_degreeZero",
        "#print axioms not_hodgeDecompositionTarget_degreeZero",
    ):
        if marker not in boundary_source:
            fail(f"degree-zero negative witness is missing: {marker}")
    for marker in (
        "theorem counterexampleData_no_decomposition",
        "theorem not_hodgeDecompositionTarget",
        "#print axioms not_hodgeDecompositionTarget",
    ):
        if marker not in realization_source:
            fail(f"operator-realization negative witness is missing: {marker}")

    _statement_output, boundary_output, realization_output = lean_replay()
    if printed_axioms(boundary_output, NEGATIVE_DECLARATIONS[0]) != EXPECTED_AXIOMS:
        fail("degree-zero countermodel axiom profile drifted")
    if printed_axioms(realization_output, NEGATIVE_DECLARATIONS[1]) != EXPECTED_AXIOMS:
        fail("operator-realization countermodel axiom profile drifted")

    receipt = load(HERE / "proof-receipt.json")
    required_fields = {
        "schema_version", "receipt_id", "item_id", "theorem_id", "phase",
        "intent", "base_revision", "base_tree", "inputs", "support_state",
        "proposed_state", "accepted", "verdict", "selftest_status",
        "selftest_result", "known_failures", "first_failed_gate",
        "retry_condition", "status_boundary", "audit_complete",
        "theorem_complete", "invalidation_inputs", "canonical_target",
        "exact_declarations", "closed_obligation_ids", "proof_body", "result",
    }
    if not required_fields <= set(receipt):
        fail("proof receipt omits contract-required fields")
    if receipt["schema_version"] != "stage1-node-receipt/1.0":
        fail("proof receipt schema drifted")
    if (receipt["item_id"], receipt["theorem_id"], receipt["phase"], receipt["intent"]) != (
        ITEM, THEOREM, "proof", "prove"
    ):
        fail("proof receipt identity drifted")
    base_revision = receipt["base_revision"]
    if (
        not isinstance(base_revision, str)
        or COMMIT_RE.fullmatch(base_revision) is None
        or subprocess.run(
            ["git", "merge-base", "--is-ancestor", base_revision, authority_revision],
            cwd=ROOT,
            capture_output=True,
            timeout=30,
        ).returncode != 0
        or receipt["base_tree"] != git("rev-parse", f"{base_revision}^{{tree}}")
    ):
        fail("proof receipt base binding drifted")
    if authority_revision == base_revision and authority_tree != receipt["base_tree"]:
        fail("proof receipt current-base tree binding drifted")
    if receipt["support_state"] != "provisional_worker_selftest":
        fail("proof receipt support state drifted")
    if receipt["proposed_state"] != "[_]":
        fail("proof receipt proposed state drifted")
    if receipt["accepted"] is not False or receipt["verdict"] != "blocked":
        fail("proof receipt overstates acceptance")
    if receipt["selftest_status"] != "passed":
        fail("proof receipt self-test status drifted")
    if receipt["selftest_result"].get("exit_code") != 0:
        fail("proof receipt self-test exit drifted")
    if not receipt["selftest_result"].get("commands"):
        fail("proof receipt lacks exact self-test commands")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }:
        fail("worker self-test packet fields drifted")
    if (
        packet["item_id"] != ITEM
        or packet["base_revision"] != base_revision
        or packet["state"] != "[_]"
        or packet["known_failures"] != receipt["known_failures"]
        or [row.get("argv") for row in packet["commands"]]
        != [row.get("argv") for row in receipt["selftest_result"]["commands"]]
    ):
        fail("worker self-test packet and proof receipt disagree")
    expected_changed = {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/check_proof.py",
        f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json",
        f"Stage1_Instances/{THEOREM}/proof-blocker-2026-07-17-slot116.md",
        f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    }
    if set(packet["changed_paths"]) != expected_changed:
        fail("worker self-test changed-path inventory drifted")
    status = subprocess.run(
        [
            "git", "status", "--porcelain=v1", "--untracked-files=all", "--",
            f"Stage1_Instances/{THEOREM}", ".stage1-worker-selftest.json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    ).stdout.splitlines()
    actual_changed = {
        line[3:] if line.startswith("?? ") else line[2:].lstrip()
        for line in status
    }
    if actual_changed != expected_changed:
        fail("owned worker delta and handoff inventory disagree")
    if receipt["audit_complete"] is not False or receipt["theorem_complete"] is not False:
        fail("proof receipt crosses a terminal boundary")
    if receipt["closed_obligation_ids"] != []:
        fail("negative evidence cannot close positive obligations")
    if receipt["exact_declarations"] != list(NEGATIVE_DECLARATIONS):
        fail("proof receipt declaration inventory drifted")
    if receipt["result"] != {
        "exit_code": 0,
        "semantic_verdict": "blocked",
        "phase_predicate_proven": False,
        "phase_accepted": False,
        "blocked": True,
        "audit_complete": False,
        "theorem_complete": False,
        "open_obligations": 14,
        "stale_inputs": [],
        "statement_olean_sha256": STATEMENT_OLEAN_SHA256,
        "boundary_output_sha256": BOUNDARY_OUTPUT_SHA256,
        "realization_output_sha256": REALIZATION_OUTPUT_SHA256,
        "machine_derived_axioms": sorted(EXPECTED_AXIOMS),
    }:
        fail("proof receipt result drifted")
    proof_bindings = receipt["inputs"]["proof_sources"]
    if not isinstance(proof_bindings, list) or [row.get("path") for row in proof_bindings] != [
        f"Stage1_Instances/{THEOREM}/{name}" for name in PROOF_SOURCES
    ]:
        fail("proof receipt source bindings drifted")
    for row, name in zip(proof_bindings, PROOF_SOURCES, strict=True):
        relative = f"Stage1_Instances/{THEOREM}/{name}"
        if row != {
            "path": relative,
            "sha256": EXPECTED_INPUT_HASHES[name],
            "git_blob": git("hash-object", "--no-filters", relative),
        }:
            fail(f"proof receipt source binding drifted: {name}")
    ledger_relative = f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json"
    if receipt["inputs"]["dependency_reuse_ledger"] != {
        "path": ledger_relative,
        "sha256": digest(HERE / "dependency-reuse-ledger.json"),
        "git_blob": git("hash-object", "--no-filters", ledger_relative),
    }:
        fail("proof receipt dependency ledger binding drifted")
    if receipt["inputs"].get("theorem_dag_sha256") != graph_sha256:
        fail("proof receipt theorem DAG binding drifted")
    if receipt["inputs"].get("phase_contract_sha256") != contract_sha256:
        fail("proof receipt phase contract binding drifted")
    validator_binding = receipt["inputs"].get("validator_candidate")
    validator_relative = f"Stage1_Instances/{THEOREM}/check_proof.py"
    if not isinstance(validator_binding, dict):
        fail("proof receipt validator binding is missing")
    if (
        validator_binding.get("path") != validator_relative
        or validator_binding.get("sha256") != digest(Path(__file__))
        or validator_binding.get("git_blob")
        != git("hash-object", "--no-filters", validator_relative)
    ):
        fail("proof receipt validator binding drifted")
    base_has_validator = subprocess.run(
        ["git", "cat-file", "-e", f"{base_revision}:{validator_relative}"],
        cwd=ROOT,
        capture_output=True,
        timeout=30,
    ).returncode == 0
    if validator_binding.get("existed_at_base") is not base_has_validator:
        fail("proof receipt validator base-presence binding drifted")
    if validator_binding.get("current_claim_selection_eligible") is not base_has_validator:
        fail("proof receipt validator selection eligibility drifted")


def semantic_result() -> dict[str, Any]:
    return {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "phase": "proof",
        "status": "blocked",
        "verdict": "blocked",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": "P04-KERNEL/EXACT-TARGET-CONSISTENCY",
        "open_obligations": 14,
        "stale_inputs": [],
        "blocked": True,
        "message": (
            "The exact frozen proposition is kernel-refuted at universes (0,0); "
            "positive proof work requires an accepted statement repair."
        ),
    }


def main() -> None:
    try:
        validate()
        result = semantic_result()
    except (ValidationError, OSError, subprocess.SubprocessError) as error:
        result = semantic_result()
        result["status"] = "failed"
        result["verdict"] = "repair_required"
        result["first_failed_gate"] = "P01-ARTIFACTS/VALIDATOR-SELF-CHECK"
        result["stale_inputs"] = [str(error)]
        result["message"] = str(error)
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
