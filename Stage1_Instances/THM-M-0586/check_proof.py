#!/usr/bin/env python3
"""Fail-closed semantic proof replay for S56-M-0586-PROOF."""

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
from typing import Any


if sys.flags.optimize:
    raise SystemExit("check_proof.py requires assertions; do not run Python with -O")


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0586-PROOF"
THEOREM = "THM-M-0586"
BASE_REVISION = "1cc6aa61bb055a5c032297ee457905c849af7608"
BASE_TREE = "dc3053b55c5724ccb2e6a247e7deffebca9dbb99"
GRAPH_SHA256 = "e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b"
CONTEXT_SHA256 = "cdf6c9f8de36e769dba3868e130e3dbcced7e1e38e0429fb4b3a728c4b787aff"
CANONICAL_EXPRESSION_SHA256 = (
    "48062820803a28b54a2bcf9b1122a10ce4d4b53b1d9e37e5f0c8b119955346e7"
)
DENOMINATOR_SHA256 = (
    "bbeb74bba464fc32a5741776c0e5bfa6784f3d7b57a4f4630347f07e73007b3e"
)
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
OPEN_CUT = ["M0586-T-FIVE", "M0586-T-STABLE"]
EXPECTED_HASHES = {
    "Statement.lean": "326186c55d4b7abcefbd6f3c3e2813e8f0271bcbfc266ae937b6e7f220b42b49",
    "ObligationTree.lean": "6a6c73d0c86269fd7ba460d1761d075265e8c1009b31317dc60be0b999b14772",
    "ProofBlockerProbe.lean": "9429253c38669e7ab5fffe05eefff44a302df97429d77b42f6d154789d91270e",
    "ProofEvidence.lean": "83b42a4a44a2f90f0303eb875638e71b02b331b6cdb9027c06b5ede12e5265a9",
    "statement.json": "c1fb6784933d698502b2720912056c953128481b95330642bf9b7400a7333d56",
    "obligation-registry.json": "ffa535b4a41e8eb5be13ebac45d0603e7d843f11361fabb0bc441a8bd8a8d913",
    "typed-graphs.json": "355c2fcf5c0d27351b38e8b6dc332a4ce2d09654fb4cc17fbc9c6a33f634389d",
    "anchor-audit.json": "c9f7de88584d686d18d9b8b17e182dc39e4ded67ebf28580958b00cb61ce894e",
    "validation-specs.json": "1c169c75083741ee6ff3c0f3b620a8cced9f39c97309b487f7bc81dd85323c7f",
    "dependency-reuse-ledger.json": "f92909de5505dbe84882b4d01b4250b5b93514a4b39a27310c42eca3b4463a41",
}
EXPECTED_PROVIDER_HASHES = {
    "Statement.lean": "307061f5847f145fb8cb4e91116ed8ab0c76e3ddc0e9301486fd879be1cf3de8",
    "AnchorAudit.lean": "40a767ff49b55bcbfccc9455cec77ae7878476b64b0cecd36dfe639fb2c3550f",
    "ObligationTree.lean": "f5214263374c23fd2f235cdf4d06bc9cadfd50d4abbe41de32dd55a7e35f0c63",
    "ProofBlockerProbe.lean": "e4bc1b79c8e1525b8bf8f7f8edceeb95be6cd95251aa1e69f6052b32618541a3",
    "anchor-audit.json": "0285a80d4d59466d71fdd1d163e1c6a09f7a96b1d0372ea8f682fd69c251f7e7",
    "proof-blocker.json": "3967c5a0a4382109a40c4b127bbc3139d282e27a850ce39863f4bb0fa47403d8",
}
EXPECTED_CHANGED = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/ProofEvidence.lean",
    f"Stage1_Instances/{THEOREM}/check_proof.py",
    f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json",
    f"Stage1_Instances/{THEOREM}/proof-receipt.json",
    f"Stage1_Instances/{THEOREM}/proof-validation.md",
}
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
PROHIBITED = re.compile(
    r"\b(sorry|admit|sorryAx|implemented_by|native_decide)\b|"
    r"^[ \t]*(axiom|constant|opaque|unsafe|extern)[ \t]+",
    re.MULTILINE,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, child in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON key in {path}: {key}")
            value[key] = child
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    if not isinstance(value, dict):
        raise ValueError(f"{path} is not a JSON object")
    return value


def output(argv: list[str], *, cwd: Path = ROOT) -> str:
    return subprocess.check_output(argv, cwd=cwd, text=True).strip()


def source_without_comments_and_strings(source: str) -> str:
    result: list[str] = []
    index = 0
    depth = 0
    quoted = False
    while index < len(source):
        pair = source[index : index + 2]
        char = source[index]
        if depth:
            if pair == "/-":
                depth += 1
                result.extend("  ")
                index += 2
            elif pair == "-/":
                depth -= 1
                result.extend("  ")
                index += 2
            else:
                result.append("\n" if char == "\n" else " ")
                index += 1
        elif quoted:
            if char == "\\" and index + 1 < len(source):
                result.extend("  ")
                index += 2
            elif char == '"':
                quoted = False
                result.append(" ")
                index += 1
            else:
                result.append("\n" if char == "\n" else " ")
                index += 1
        elif pair == "/-":
            depth = 1
            result.extend("  ")
            index += 2
        elif pair == "--":
            while index < len(source) and source[index] != "\n":
                result.append(" ")
                index += 1
        elif char == '"':
            quoted = True
            result.append(" ")
            index += 1
        else:
            result.append(char)
            index += 1
    if depth or quoted:
        raise ValueError("unterminated Lean comment or string")
    return "".join(result)


def run_lean(lean: str, source: str, *, cwd: Path, lean_path: str) -> str:
    environment = os.environ.copy()
    environment.update(
        {
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_NUM_THREADS": "1",
            "LEAN_PATH": lean_path,
        }
    )
    result = subprocess.run(
        [lean, "--trust=0", "-t0", "-o", f"{source.removesuffix('.lean')}.olean", source],
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=600,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stdout)
    return result.stdout


def replay_lean() -> str:
    lean = output(["lake", "env", "which", "lean"], cwd=LEAN_ROOT)
    lean_path = output(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT)
    with tempfile.TemporaryDirectory(prefix="thm-m-0586-proof-") as raw:
        temporary = Path(raw)
        names = (
            "Statement.lean",
            "ObligationTree.lean",
            "ProofBlockerProbe.lean",
            "ProofEvidence.lean",
        )
        for name in names:
            shutil.copyfile(HERE / name, temporary / name)
        chunks = [run_lean(lean, names[0], cwd=temporary, lean_path=lean_path)]
        local_path = f"{temporary}:{lean_path}"
        for name in names[1:]:
            chunks.append(run_lean(lean, name, cwd=temporary, lean_path=local_path))
    return "".join(chunks)


def verify() -> None:
    if output(["git", "rev-parse", "HEAD"]) != BASE_REVISION:
        raise ValueError("worker base revision changed")
    if output(["git", "rev-parse", "HEAD^{tree}"]) != BASE_TREE:
        raise ValueError("worker base tree changed")
    for name, expected in EXPECTED_HASHES.items():
        if sha256(HERE / name) != expected:
            raise ValueError(f"bound target input changed: {name}")

    blueprint = (ROOT / "Docs" / "Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    item_pattern = re.compile(
        r"^- \[ \] `S56-M-0586-PROOF` / `THM-M-0586` / `proof`:"
        r".*\{attempts=0\}$",
        re.MULTILINE,
    )
    if item_pattern.search(blueprint) is None:
        raise ValueError("authoritative proof item/state/attempts changed")
    dag = load(ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json")
    if sha256(ROOT / "Docs" / "Stage1_Theorem_DAG_v2.json") != GRAPH_SHA256:
        raise ValueError("theorem DAG bytes changed")
    node = next(row for row in dag["theorems"] if row["theorem_id"] == THEOREM)
    if (
        node["v2_execution_rank"] != 333
        or node["topological_layer"] != 0
        or node["phase_states"]["proof"] != "[ ]"
        or node["direct_hard_parents"] != []
        or node["transitive_hard_ancestors"] != []
        or node["direct_reuse_hint_ids"] != []
        or node["shared_lemma_group_ids"] != ["SHARED-MODULE-b3a9d89c683d7166"]
        or node["dependency_context_sha256"] != CONTEXT_SHA256
    ):
        raise ValueError("target DAG context changed")

    ledger = load(HERE / "dependency-reuse-ledger.json")
    if (
        ledger.get("schema_version") != "stage1-dependency-reuse-ledger/1.1"
        or ledger.get("consumer_theorem_id") != THEOREM
        or ledger.get("observed_theorem_dag_sha256") != GRAPH_SHA256
        or ledger.get("dependency_context_sha256") != CONTEXT_SHA256
        or ledger.get("repository_revision") != BASE_REVISION
    ):
        raise ValueError("dependency ledger identity is stale")
    for field in (
        "direct_parent_ids",
        "transitive_ancestor_ids",
        "hard_edge_ids",
        "reuse_hint_ids",
        "inspections",
        "unresolved_compatibility_obligations",
    ):
        if ledger.get(field) != []:
            raise ValueError(f"dependency ledger {field} is not the exact empty closure")
    if ledger.get("shared_group_ids") != ["SHARED-MODULE-b3a9d89c683d7166"]:
        raise ValueError("dependency ledger shared-group closure changed")
    decisions = ledger.get("reuse_decisions")
    if not isinstance(decisions, list) or len(decisions) != 1:
        raise ValueError("dependency ledger must contain one shared-group decision")
    decision = decisions[0]
    if (
        decision.get("source_id") != "SHARED-MODULE-b3a9d89c683d7166"
        or decision.get("provider_theorem_id") != "THM-M-0579"
        or decision.get("decision") != "not_applicable"
        or decision.get("context_digest") != CONTEXT_SHA256
    ):
        raise ValueError("shared-group decision changed")
    provider = ROOT / "Stage1_Instances" / "THM-M-0579"
    inspected = decision.get("inspected_member_artifacts")
    if not isinstance(inspected, dict):
        raise ValueError("shared-group decision lacks inspected member bytes")
    for name, expected in EXPECTED_PROVIDER_HASHES.items():
        relative = f"Stage1_Instances/THM-M-0579/{name}"
        if inspected.get(relative) != expected or sha256(provider / name) != expected:
            raise ValueError(f"inspected shared-group member changed: {name}")

    statement = load(HERE / "statement.json")
    if (
        statement["canonical_formal_target"]["elaborated_expression_sha256"]
        != CANONICAL_EXPRESSION_SHA256
    ):
        raise ValueError("canonical expression fingerprint changed")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    if registry.get("denominator_sha256") != DENOMINATOR_SHA256:
        raise ValueError("obligation denominator changed")
    if graphs.get("closure_boundary") != {
        "closed_obligations": ["M0586-T-ASSEMBLE"],
        "root_closed": False,
        "audit_complete": False,
        "theorem_complete": False,
        "remaining_root_cut_set": OPEN_CUT,
        "composition_certificates": [
            "Stage1Instances.THMM0586.highDimensionalPoincare_of_dimension_packages"
        ],
        "reason": "Final dimension recomposition is checked, but both mathematical branch packages remain open.",
    }:
        raise ValueError("frozen closure boundary changed")

    for name in (
        "Statement.lean",
        "ObligationTree.lean",
        "ProofBlockerProbe.lean",
        "ProofEvidence.lean",
    ):
        source = source_without_comments_and_strings((HERE / name).read_text(encoding="utf-8"))
        if PROHIBITED.search(source):
            raise ValueError(f"prohibited proof construct found in {name}")

    receipt = load(HERE / "proof-receipt.json")
    if (
        receipt.get("schema_version") != "stage1-node-receipt/1.0"
        or receipt.get("item_id") != ITEM
        or receipt.get("theorem_id") != THEOREM
        or receipt.get("phase") != "proof"
        or receipt.get("intent") != "prove"
        or receipt.get("base_revision") != BASE_REVISION
        or receipt.get("base_tree") != BASE_TREE
        or receipt.get("accepted") is not False
        or receipt.get("verdict") != "blocked"
        or receipt.get("selftest_status") != "passed"
        or receipt.get("closed_obligation_ids") != ["M0586-T-ASSEMBLE"]
        or receipt.get("audit_complete") is not False
        or receipt.get("theorem_complete") is not False
    ):
        raise ValueError("proof receipt semantic boundary changed")
    proof_sources = receipt.get("inputs", {}).get("proof_sources")
    if not isinstance(proof_sources, list) or len(proof_sources) != 1:
        raise ValueError("proof receipt must bind one target-owned proof evidence source")
    source_binding = proof_sources[0]
    if (
        source_binding.get("path") != f"Stage1_Instances/{THEOREM}/ProofEvidence.lean"
        or source_binding.get("sha256") != EXPECTED_HASHES["ProofEvidence.lean"]
    ):
        raise ValueError("proof source binding changed")

    packet = load(ROOT / ".stage1-worker-selftest.json")
    if set(packet) != {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }:
        raise ValueError("worker packet schema changed")
    if (
        packet.get("item_id") != ITEM
        or packet.get("state") != "[_]"
        or packet.get("base_revision") != BASE_REVISION
        or set(packet.get("changed_paths", [])) != EXPECTED_CHANGED
        or packet.get("commands") != receipt.get("selftest_result", {}).get("commands")
        or packet.get("known_failures") != receipt.get("known_failures")
    ):
        raise ValueError("worker packet disagrees with the proof receipt")
    status = output(["git", "status", "--short", "--untracked-files=all"])
    actual_changed = {
        (line[3:] if line.startswith("?? ") else line[2:].lstrip())
        for line in status.splitlines()
        if (line[3:] if line.startswith("?? ") else line[2:].lstrip())
        != "Formalizations/Lean/.lake"
    }
    if actual_changed != EXPECTED_CHANGED:
        raise ValueError(f"worktree delta mismatch: {sorted(actual_changed)}")

    if output(["git", "rev-parse", "HEAD"], cwd=MATHLIB) != MATHLIB_REVISION:
        raise ValueError("mathlib revision changed")
    if output(["git", "rev-parse", "HEAD^{tree}"], cwd=MATHLIB) != MATHLIB_TREE:
        raise ValueError("mathlib tree changed")
    if output(["git", "status", "--porcelain=v1"], cwd=MATHLIB):
        raise ValueError("mathlib worktree is dirty")
    poincare = (MATHLIB / "Mathlib/Geometry/Manifold/PoincareConjecture.lean").read_text(
        encoding="utf-8"
    )
    if poincare.count("proof_wanted ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere") != 1:
        raise ValueError("pinned Poincare proof_wanted boundary changed")

    lean_output = replay_lean()
    if "Unknown constant `ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere`" not in lean_output:
        raise ValueError("discarded generalized Poincare marker became available")
    if "Unknown constant `SimplyConnectedSpace.nonempty_homeomorph_sphere_three`" not in lean_output:
        raise ValueError("discarded three-dimensional Poincare marker became available")
    reported = set(re.findall(r"propext|Classical\.choice|Quot\.sound|sorryAx", lean_output))
    if reported != ALLOWED_AXIOMS:
        raise ValueError(f"unexpected axiom profile: {sorted(reported)}")


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
            "P04-KERNEL.M0586-T-FIVE+M0586-T-STABLE" if verified else "P01-ARTIFACTS"
        ),
        "open_obligations": 15,
        "stale_inputs": [],
        "blocked": verified,
        "message": (
            "The exact root-cut characterization and conditional composer replay at trust zero, "
            "but no placeholder-free inhabitant of either terminal dimension package exists in "
            "the pinned closure; the complete proof predicate remains false."
            if verified
            else f"THM-M-0586 proof evidence replay failed: {error}"
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
