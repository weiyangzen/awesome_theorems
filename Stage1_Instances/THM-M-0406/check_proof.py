#!/usr/bin/env python3
"""Fail-closed semantic proof validator for S56-M-0406-PROOF."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0406"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
FLR = LEAN_ROOT / ".lake" / "packages" / "flt-regular"
ITEM = "S56-M-0406-PROOF"
THEOREM = "THM-M-0406"
BASE_REVISION = "94009a6bebd743588e09c3b45bfbf18bf9b5c5e3"
BASE_TREE = "daabee9f9b2c6e98d84b6290f78a209b950485fc"
GRAPH_SHA256 = "eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
FLR_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
FLR_TREE = "32c9eace926573a9981787ae97643e520353c893"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
DENOMINATOR_SHA256 = "46deb9e278a5e0383923334b032877af6743372ba6cafa2fd0d03a569d1d90a7"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_HASHES = {
    "Statement.lean": "9d6e2a94131455eedcee2ae75765746958988f23f6398cc5c4ea3fbc193258ec",
    "ObligationTree.lean": "bbcd4865cc660a210b104c50e19d5ca66055dacdab07182f6d4693c096f3f02c",
    "Proof.lean": "afeb346ab8f1ff9e41b87395744faa7a352509d28ef842f10f18a3ec00874aaf",
    "obligation-registry.json": "90d988ef727c9f1cbe99cfffb73c21b05f32f6d0b61a2177b624217cfb4612b6",
    "typed-graphs.json": "f4da55995c5413f92314904e9687721153b52e7d1d1e1e27fe551f0d7333da17",
    "anchor-audit.json": "8e0f84a533e183b8b70ef48955d9fa2dc8dbf39274f4345c600c8f2c143cfd21",
    "proof-blocker.json": "684a88b29c2b7a43d94515abba454a8eeb6fcc7178b6792316c4b82cb926a3d6",
}
OPEN_IDS = {
    "M0406-ROOT", "M0406-S-DEFINITIONS", "M0406-S-FOUNDATION",
    "M0406-N-BOUNDARY", "M0406-N-INTEGRAL", "M0406-C-AUXILIARY",
    "M0406-L-HEIGHT-INEQUALITY", "M0406-X-SUBSPACE",
    "M0406-B-EXCEPTIONAL", "M0406-L-DIMENSION-DROP",
    "M0406-C-CURVE-UNION", "M0406-T-ENGINE",
    "M0406-T-ROOT-ADAPTER", "M0406-X-PROVENANCE",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern|run_tac)\b|"
    r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
    r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
    r"(?:axiom|constant|opaque|unsafe)\b",
    re.MULTILINE,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key {key!r} in {path}")
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def run(argv: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=180, check=False,
    )


def checked_output(argv: list[str], *, cwd: Path) -> str:
    result = run(argv, cwd=cwd)
    if result.returncode:
        raise ValueError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout.strip()


def checked_stdout(argv: list[str], *, cwd: Path) -> str:
    result = run(argv, cwd=cwd)
    if result.returncode:
        raise ValueError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*argv: str, cwd: Path = ROOT) -> str:
    return checked_output(["git", *argv], cwd=cwd)


def source_without_comments(source: str) -> str:
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
                output.append('"')
                index += 1
            else:
                index += 1
        elif source.startswith("/-", index):
            depth = 1
            index += 2
        elif source.startswith("--", index):
            newline = source.find("\n", index)
            index = len(source) if newline < 0 else newline
        elif source[index] == '"':
            in_string = True
            output.append('"')
            index += 1
        else:
            output.append(source[index])
            index += 1
    if depth or in_string:
        raise ValueError("unterminated Lean comment or string")
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    short = declaration.rsplit(".", 1)[-1]
    match = re.search(
        rf"'[^']*{re.escape(short)}' depends on axioms:\s*\[(.*?)\]",
        output, flags=re.DOTALL,
    )
    if match is None:
        if re.search(rf"'[^']*{re.escape(short)}' does not depend on any axioms", output):
            return set()
        raise ValueError(f"missing axiom report for {declaration}")
    return {value.strip() for value in match.group(1).replace("\n", "").split(",") if value.strip()}


def replay_countermodel() -> None:
    lean = Path(checked_output(["lake", "env", "which", "lean"], cwd=LEAN_ROOT))
    lake = Path(checked_output(["lake", "env", "which", "lake"], cwd=LEAN_ROOT))
    if sha256(lean) != LEAN_SHA256 or sha256(lake) != LAKE_SHA256:
        raise ValueError("pinned Lean or Lake executable digest mismatch")
    if LEAN_COMMIT not in checked_output([str(lean), "--version"], cwd=LEAN_ROOT):
        raise ValueError("pinned Lean executable identity mismatch")
    base_path = checked_output(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT)
    fixed_env = {
        **os.environ,
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
        "LEAN_PATH": base_path,
    }
    with tempfile.TemporaryDirectory(prefix="m0406-proof-", dir="/tmp") as raw:
        scratch = Path(raw)
        statement = scratch / "Statement.lean"
        proof = scratch / "Proof.lean"
        statement.write_bytes((HERE / "Statement.lean").read_bytes())
        proof.write_bytes((HERE / "Proof.lean").read_bytes())
        statement_result = run(
            [str(lean), "--trust=0", "--root", str(scratch), "-o",
             str(scratch / "Statement.olean"), str(statement)],
            cwd=LEAN_ROOT, env=fixed_env,
        )
        if statement_result.returncode:
            raise ValueError(f"statement replay failed\n{statement_result.stdout}")
        proof_result = run(
            [str(lean), "--trust=0", "--root", str(scratch), "-o",
             str(scratch / "Proof.olean"), str(proof)],
            cwd=LEAN_ROOT, env={**fixed_env, "LEAN_PATH": f"{scratch}:{base_path}"},
        )
        if proof_result.returncode:
            raise ValueError(f"countermodel replay failed\n{proof_result.stdout}")
        if hashlib.sha256(statement_result.stdout.encode()).hexdigest() != (
            "0f59d3486b6464922278f83f5e3871c79e0c2e7964d1e3a8a412f16e567b385b"
        ):
            raise ValueError("statement replay output drifted")
        if hashlib.sha256(proof_result.stdout.encode()).hexdigest() != (
            "942b7cc706eaa0b7aa1143e3ecfba1f8387659e19954b5b978ea77b98188a1f8"
        ):
            raise ValueError("countermodel replay output drifted")
        if sha256(scratch / "Statement.olean") != (
            "deafda332045568236e3354ba2870233cfdfd906e0105c9eb67b8fc575004a27"
        ):
            raise ValueError("statement compiled object drifted")
        for declaration in (
            "Stage1Instances.THMM0406.proofPhaseCounterexampleBoundary",
            "Stage1Instances.THMM0406.not_corvajaZannierTheoremOne",
        ):
            if printed_axioms(proof_result.stdout, declaration) != EXPECTED_AXIOMS:
                raise ValueError(f"unexpected axiom profile for {declaration}")


def verify_ledger() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    if ledger.get("schema_version") != "stage1-dependency-reuse-ledger/1.1":
        raise ValueError("dependency ledger schema mismatch")
    if ledger.get("consumer_theorem_id") != THEOREM:
        raise ValueError("dependency ledger owner mismatch")
    if ledger.get("observed_theorem_dag_sha256") != GRAPH_SHA256:
        raise ValueError("dependency ledger graph binding is stale")
    if ledger.get("dependency_context_sha256") != CONTEXT_SHA256:
        raise ValueError("dependency ledger context binding is stale")
    if ledger.get("repository_revision") != BASE_REVISION:
        raise ValueError("dependency ledger revision binding is stale")
    for key in (
        "direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
        "reuse_hint_ids", "shared_group_ids", "inspections", "reuse_decisions",
        "unresolved_compatibility_obligations",
    ):
        if ledger.get(key) != []:
            raise ValueError(f"empty dependency closure changed: {key}")
    if ledger.get("closure_audit") != {
        "parent_inspection_order": [],
        "expected_inspection_count": 0,
        "actual_inspection_count": 0,
        "status": "empty_hard_parent_closure_inspected",
        "proof_work_started_after_audit": True,
        "note": (
            "The authoritative v2 node has no direct hard parent, transitive hard ancestor, "
            "reuse hint, or shared lemma group. No provider body, receipt, phase acceptance, "
            "or evidence credit was consumed."
        ),
    }:
        raise ValueError("empty dependency closure audit is incomplete")


def verify() -> None:
    if git("rev-parse", "HEAD") != BASE_REVISION or git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        raise ValueError("worker base revision or tree drifted")
    if sha256(ROOT / "Docs/Stage1_Theorem_DAG_v2.json") != GRAPH_SHA256:
        raise ValueError("theorem DAG digest drifted")
    if sha256(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json") != CONTRACT_SHA256:
        raise ValueError("phase contract digest drifted")
    if sha256(LEAN_ROOT / "lean-toolchain") != TOOLCHAIN_SHA256:
        raise ValueError("Lean toolchain file drifted")
    if sha256(LEAN_ROOT / "lake-manifest.json") != MANIFEST_SHA256:
        raise ValueError("Lake manifest drifted")
    for name, expected in EXPECTED_HASHES.items():
        if sha256(HERE / name) != expected:
            raise ValueError(f"owned frozen input drifted: {name}")

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    target = next(row for row in targets["targets"] if row.get("theorem_id") == THEOREM)
    if target.get("execution_rank") != 19 or target.get("lifecycle_mode") != "planned":
        raise ValueError("target manifest identity or lifecycle drifted")
    if target.get("theorem_complete") is not False:
        raise ValueError("target manifest unexpectedly claims theorem completion")

    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    phase_items = {row["phase"]: row for row in execution["items"] if row.get("theorem_id") == THEOREM}
    if phase_items["proof"].get("state") != "[ ]" or phase_items["proof"].get("attempts") != 0:
        raise ValueError("proof item no longer matches the assigned claim")
    if phase_items["proof"].get("depends_on") != ["S56-M-0406-OBLIGATION_TREE"]:
        raise ValueError("proof prerequisite identity changed")
    if phase_items["obligation_tree"].get("state") != "[_]":
        raise ValueError("proof prerequisite observation changed")

    theorem_dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in theorem_dag["theorems"] if row.get("theorem_id") == THEOREM)
    if node.get("v2_execution_rank") != 258 or node.get("topological_layer") != 0:
        raise ValueError("v2 claim order changed")
    for key in (
        "direct_hard_parents", "transitive_hard_ancestors",
        "direct_reuse_hint_ids", "shared_lemma_group_ids",
    ):
        if node.get(key) != []:
            raise ValueError(f"unexpected dependency member in {key}")
    if node.get("dependency_context_sha256") != CONTEXT_SHA256:
        raise ValueError("dependency context digest changed")
    verify_ledger()

    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    proof_contracts = [row for row in contract.get("phases", []) if row.get("phase") == "proof"]
    if len(proof_contracts) != 1:
        raise ValueError("HEAD contract lacks exactly one proof row")
    proof_contract = proof_contracts[0]
    if proof_contract.get("intent") != "prove" or proof_contract.get("layer") != 4:
        raise ValueError("proof phase contract changed")
    candidates = proof_contract.get("validator_candidates", [])
    existing_candidates = [
        row["path_pattern"].format(theorem_id=THEOREM) for row in candidates
        if (ROOT / row["path_pattern"].format(theorem_id=THEOREM)).is_file()
    ]
    if existing_candidates != ["Stage1_Instances/THM-M-0406/check_proof.py"]:
        raise ValueError("proof validator candidate selection is not exact")

    receipt = load(HERE / "proof-receipt.json")
    required = {
        "schema_version", "receipt_id", "item_id", "theorem_id", "phase", "intent",
        "base_revision", "base_tree", "inputs", "support_state", "proposed_state",
        "accepted", "verdict", "selftest_status", "selftest_result", "known_failures",
        "first_failed_gate", "retry_condition", "status_boundary", "audit_complete",
        "theorem_complete", "invalidation_inputs", "canonical_target",
        "exact_declarations", "closed_obligation_ids", "proof_body", "result",
    }
    if not required <= set(receipt):
        raise ValueError("proof receipt lacks a contract-required field")
    if receipt.get("schema_version") != "stage1-node-receipt/1.0":
        raise ValueError("proof receipt schema mismatch")
    if (receipt.get("item_id"), receipt.get("theorem_id"), receipt.get("phase"), receipt.get("intent")) != (ITEM, THEOREM, "proof", "prove"):
        raise ValueError("proof receipt identity mismatch")
    if receipt.get("base_revision") != BASE_REVISION or receipt.get("base_tree") != BASE_TREE:
        raise ValueError("proof receipt base binding mismatch")
    if receipt.get("support_state") != "provisional_worker_selftest" or receipt.get("proposed_state") != "[_]":
        raise ValueError("proof receipt worker state mismatch")
    if receipt.get("accepted") is not False or receipt.get("verdict") != "blocked":
        raise ValueError("proof receipt overstates acceptance")
    if receipt.get("selftest_status") != "passed" or receipt.get("selftest_result", {}).get("exit_code") != 0:
        raise ValueError("proof receipt self-test is not passing")
    if not receipt.get("selftest_result", {}).get("commands"):
        raise ValueError("proof receipt lacks exact self-test commands")
    if receipt.get("audit_complete") is not False or receipt.get("theorem_complete") is not False:
        raise ValueError("proof receipt crosses a terminal boundary")
    if receipt.get("closed_obligation_ids") != []:
        raise ValueError("negative evidence cannot close positive obligations")
    if receipt.get("exact_declarations") != ["Stage1Instances.THMM0406.not_corvajaZannierTheoremOne"]:
        raise ValueError("proof receipt declaration boundary mismatch")
    if receipt.get("proof_body", {}).get("source_sha256") != EXPECTED_HASHES["Proof.lean"]:
        raise ValueError("proof receipt source hash mismatch")
    if receipt.get("result") != {
        "exit_code": 0,
        "semantic_verdict": "blocked",
        "phase_predicate_proven": False,
        "phase_accepted": False,
        "blocked": True,
        "audit_complete": False,
        "theorem_complete": False,
        "root_closed": False,
        "open_obligations": len(OPEN_IDS),
    }:
        raise ValueError("proof receipt semantic result mismatch")

    packet = load(ROOT / ".stage1-worker-selftest.json")
    if set(packet) != {"item_id", "changed_paths", "commands", "output_summary", "base_revision", "known_failures", "state"}:
        raise ValueError("worker self-test packet schema mismatch")
    if packet.get("item_id") != ITEM or packet.get("state") != "[_]" or packet.get("base_revision") != BASE_REVISION:
        raise ValueError("worker self-test packet identity mismatch")
    if packet.get("commands") != receipt.get("selftest_result", {}).get("commands"):
        raise ValueError("worker packet and receipt commands disagree")
    if packet.get("known_failures") != receipt.get("known_failures"):
        raise ValueError("worker packet and receipt failures disagree")
    expected_changed = {
        ".stage1-worker-selftest.json",
        "Stage1_Instances/THM-M-0406/check_proof.py",
        "Stage1_Instances/THM-M-0406/dependency-reuse-ledger.json",
        "Stage1_Instances/THM-M-0406/proof-receipt.json",
        "Stage1_Instances/THM-M-0406/proof-validation.md",
    }
    if set(packet.get("changed_paths", [])) != expected_changed:
        raise ValueError("worker packet changed-path scope mismatch")
    status = checked_stdout(["git", "status", "--short", "--untracked-files=all"], cwd=ROOT)
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] not in {"Formalizations/Lean/.lake", "Formalizations/Lean/.lake/"}
    }
    if actual_changed != expected_changed:
        raise ValueError("worktree delta escapes or omits the declared target scope")

    input_bindings = receipt.get("input_bindings")
    if not isinstance(input_bindings, dict):
        raise ValueError("proof receipt lacks input bindings")
    for name, expected in {**EXPECTED_HASHES, "dependency-reuse-ledger.json": sha256(HERE / "dependency-reuse-ledger.json")}.items():
        binding = input_bindings.get(name)
        path = HERE / name
        if not isinstance(binding, dict) or binding.get("sha256") != expected:
            raise ValueError(f"proof receipt input SHA-256 mismatch: {name}")
        if binding.get("git_blob") != git("hash-object", "--no-filters", str(path)):
            raise ValueError(f"proof receipt input Git blob mismatch: {name}")
    validator_binding = input_bindings.get("check_proof.py")
    if not isinstance(validator_binding, dict):
        raise ValueError("proof receipt lacks validator binding")
    if validator_binding.get("sha256") != sha256(HERE / "check_proof.py"):
        raise ValueError("proof validator SHA-256 binding mismatch")
    if validator_binding.get("git_blob") != git("hash-object", "--no-filters", str(HERE / "check_proof.py")):
        raise ValueError("proof validator Git blob binding mismatch")

    registry = load(HERE / "obligation-registry.json")
    rows = registry.get("obligations")
    if not isinstance(rows, list) or {row.get("obligation_id") for row in rows} != OPEN_IDS:
        raise ValueError("frozen obligation denominator identity changed")
    if registry.get("denominator_sha256") != DENOMINATOR_SHA256:
        raise ValueError("frozen denominator digest changed")
    if any(row.get("terminal_proof_body_id") is not None for row in rows):
        raise ValueError("registry unexpectedly records a terminal proof body")
    closure = load(HERE / "typed-graphs.json").get("closure_boundary")
    if closure.get("closed_obligations") != [] or closure.get("theorem_complete") is not False:
        raise ValueError("typed graph unexpectedly closes the root")

    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean"):
        if PROHIBITED.search(source_without_comments((HERE / name).read_text(encoding="utf-8"))):
            raise ValueError(f"prohibited proof construct found in {name}")
    for dependency, revision, tree in (
        (MATHLIB, MATHLIB_REVISION, MATHLIB_TREE),
        (FLR, FLR_REVISION, FLR_TREE),
    ):
        if git("rev-parse", "HEAD", cwd=dependency) != revision:
            raise ValueError(f"dependency revision drifted: {dependency.name}")
        if git("rev-parse", "HEAD^{tree}", cwd=dependency) != tree:
            raise ValueError(f"dependency tree drifted: {dependency.name}")
        if git("status", "--porcelain=v1", cwd=dependency) != "":
            raise ValueError(f"dependency checkout is dirty: {dependency.name}")
    replay_countermodel()


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
            "P04-KERNEL/S56-5.1-EXACT-TARGET-CONSISTENCY/M0406-S-DEFINITIONS"
            if verified else "P01-ARTIFACTS"
        ),
        "open_obligations": len(OPEN_IDS),
        "stale_inputs": [],
        "blocked": verified,
        "message": (
            "The frozen target is refuted by the checked empty-curve model; zero frozen "
            "obligations are closed and the proof phase remains blocked."
            if verified else f"Proof blocker replay failed: {error}"
        ),
    }


def main() -> int:
    try:
        verify()
    except Exception as exc:
        result = semantic_result(verified=False, error=str(exc))
        code = 1
    else:
        result = semantic_result(verified=True)
        code = 0
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
