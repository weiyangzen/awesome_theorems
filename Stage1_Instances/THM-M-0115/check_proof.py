#!/usr/bin/env python3
"""Fail-closed semantic validator for S56-M-0115-PROOF."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0115"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0115-PROOF"
THEOREM = "THM-M-0115"
BASE_REVISION = "307c34d30fc3763c82a944a142ae922b48ff18aa"
BASE_TREE = "ef45ba442c71959db78ad146a023bcf32946a53f"
GRAPH_SHA256 = "8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47"
CONTEXT_SHA256 = "068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c"
CONTRACT_SHA256 = "1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4"
TARGET_SHA256 = "eada246ab2968c378c5b6c31c2ffd84c10873d9206b499457c451ae3848c160e"
DENOMINATOR_SHA256 = "f1455869731874b94cb533d3a6ee70bb15d428438472ffc205b63888eae68527"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPECTED_HASHES = {
    "Statement.lean": "26648a8514a0a9240c831132918c9ad0f735eb7accce33f2287a45961394d538",
    "ObligationTree.lean": "7aeb4e6dfe6789365302e1ca6cc92ab8278233b9710d19b8882e3e76616f5c7e",
    "Proof.lean": "ce0ab46f7ab8815cdd22a992d6d0ec4db8d6fa6ea6d5464f5700aec24465fca9",
    "statement.json": "241a8d4b943a6431050fece1beca135557777c42ff44e8169d30383c66763e3f",
    "obligation-registry.json": "1259038b59ce7429205a1813b97c31f2be5075b7c6ee784f3d602110d13f37c3",
    "typed-graphs.json": "ccf1757734fe4f37aae3bc65bebcb9fbf63a65f6d59031f74156607df91a768a",
    "anchor-audit.json": "1aa93316cb6fec237cf88f0ce4bf9633bbcc25a26f54a1c11a69c41225ff8d4f",
    "obligation-tree-receipt.json": "38623d2be0d7be786abd96d3b3d8344e6dd5a01d9453401fe29111eeaecf5e80",
    "dependency-reuse-ledger.json": "7df2ec53f34afc9ac1f82b34a255baef5d4795568f2f2ff19e69e504e876c62d",
}
PROHIBITED = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|proof_wanted)\b|"
    r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern|external)\b",
    re.MULTILINE,
)
RESULT_FIELDS = {
    "schema_version", "item_id", "theorem_id", "phase", "status", "verdict",
    "phase_accepted", "audit_complete", "theorem_complete",
    "phase_predicate_proven", "first_failed_gate", "open_obligations",
    "stale_inputs", "blocked", "message",
}


class GateFailure(Exception):
    def __init__(self, gate: str, message: str, *, stale: list[str] | None = None):
        super().__init__(message)
        self.gate = gate
        self.message = message
        self.stale = stale or []


def require(condition: bool, gate: str, message: str, *, stale: list[str] | None = None) -> None:
    if not condition:
        raise GateFailure(gate, message, stale=stale)


def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise GateFailure("P01-ARTIFACTS", f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    require(isinstance(value, dict), "P01-ARTIFACTS", f"{path.name} is not one JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output(*argv: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(argv, cwd=cwd, text=True, stderr=subprocess.DEVNULL).strip()


def assert_authorities() -> None:
    require(output("git", "rev-parse", "HEAD") == BASE_REVISION,
            "G09-FRESHNESS", "repository revision differs from worker base", stale=["HEAD"])
    require(output("git", "rev-parse", "HEAD^{tree}") == BASE_TREE,
            "G09-FRESHNESS", "repository tree differs from worker base", stale=["HEAD^{tree}"])
    authorities = {
        ROOT / "Docs/Stage1_Theorem_DAG_v2.json": GRAPH_SHA256,
        ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json": CONTRACT_SHA256,
    }
    for path, expected in authorities.items():
        require(sha256(path) == expected, "G09-FRESHNESS",
                f"authority changed: {path.relative_to(ROOT)}", stale=[str(path.relative_to(ROOT))])
    for name, expected in EXPECTED_HASHES.items():
        require(sha256(HERE / name) == expected, "G09-FRESHNESS",
                f"proof input changed: {name}", stale=[f"Stage1_Instances/{THEOREM}/{name}"])


def assert_contract_and_claim() -> None:
    contract = load(ROOT / "Docs/Stage1_Phase_Acceptance_Contracts.json")
    phase = next(row for row in contract["phases"] if row["phase"] == "proof")
    require(phase["layer"] == 4 and phase["item_suffix"] == "PROOF" and phase["intent"] == "prove",
            "P01-ARTIFACTS", "proof phase contract identity changed")
    candidates = [row["path_pattern"].replace("{theorem_id}", THEOREM)
                  for row in phase["validator_candidates"]]
    present = [path for path in candidates if (ROOT / path).is_file()]
    require(present == [f"Stage1_Instances/{THEOREM}/check_proof.py"],
            "P01-ARTIFACTS", "proof validator candidate selection is not exact")
    required_roles = {row["role"] for row in phase["required_artifact_roles"]
                      if row["requirement"] == "required"}
    require(required_roles == {"dependency_reuse_ledger", "proof_sources", "phase_receipt"},
            "P01-ARTIFACTS", "required proof artifact roles changed")

    blueprint = (ROOT / "Docs/Stage1_Blueprint_v2.md").read_text(encoding="utf-8")
    row = re.compile(
        r"^- \[ \] `S56-M-0115-PROOF` / `THM-M-0115` / `proof`:.*\{attempts=0\}$",
        re.MULTILINE,
    )
    require(row.search(blueprint) is not None, "G01-SSOT-CAS",
            "authoritative proof item is not the assigned open claim")
    require("- [_] `S56-M-0115-OBLIGATION_TREE`" in blueprint, "G02-TOPOLOGY",
            "predecessor was not observed in its authoritative provisional state")

    dag = load(ROOT / "Docs/Stage1_Theorem_DAG_v2.json")
    node = next(row for row in dag["theorems"] if row["theorem_id"] == THEOREM)
    require(node["v2_execution_rank"] == 260 and node["topological_layer"] == 0,
            "P02-CONTEXT", "target claim order changed")
    require(node["phase_states"]["proof"] == "[ ]" and node["phase_attempts"]["proof"] == 0,
            "G01-SSOT-CAS", "authoritative proof cursor changed")
    require(node["dependency_context_sha256"] == CONTEXT_SHA256,
            "P02-CONTEXT", "dependency context changed")
    for key in ("direct_hard_parents", "transitive_hard_ancestors",
                "direct_reuse_hint_ids", "shared_lemma_group_ids"):
        require(node[key] == [], "P02-CONTEXT", f"unexpected dependency member in {key}")


def assert_ledger() -> None:
    ledger = load(HERE / "dependency-reuse-ledger.json")
    require(ledger["schema_version"] == "stage1-dependency-reuse-ledger/1.1",
            "P03-REUSE", "dependency ledger schema changed")
    require((ledger["consumer_theorem_id"], ledger["item_id"], ledger["phase"]) ==
            (THEOREM, ITEM, "proof"), "P03-REUSE", "dependency ledger identity changed")
    require(ledger["observed_theorem_dag_sha256"] == GRAPH_SHA256 and
            ledger["dependency_context_sha256"] == CONTEXT_SHA256 and
            ledger["repository_revision"] == BASE_REVISION,
            "P02-CONTEXT", "dependency ledger graph, context, or revision is stale")
    require(ledger["claim_order"] == {
        "v2_execution_rank": 260, "phase_layer": 4, "phase_item_id": ITEM,
    }, "P02-CONTEXT", "dependency ledger claim order changed")
    for key in ("direct_parent_ids", "transitive_ancestor_ids", "hard_edge_ids",
                "reuse_hint_ids", "shared_group_ids", "parent_inspection_order",
                "inspections", "reuse_decisions", "unresolved_compatibility_obligations"):
        require(ledger[key] == [], "P03-REUSE", f"empty dependency closure changed: {key}")
    require(ledger["closure_audit"]["expected_inspection_count"] == 0 and
            ledger["closure_audit"]["actual_inspection_count"] == 0 and
            ledger["provider_acceptance_inherited"] is False,
            "P03-REUSE", "empty closure was not audited fail-closed")


def assert_frozen_proof_boundary() -> None:
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    formal = statement["canonical_formal_target"]
    require(formal["declaration_or_expression"] ==
            "Stage1Instances.THMM0115.GrothendieckRiemannRochExpandedTarget" and
            formal["elaborated_expression_sha256"] == TARGET_SHA256,
            "P04-KERNEL", "canonical target or fingerprint changed")
    require(registry["root_obligation_id"] == "M0115-ROOT" and
            registry["denominator_sha256"] == DENOMINATOR_SHA256,
            "P06-COMPOSITION", "frozen obligation denominator changed")
    require(graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256 and
            graphs["closure_boundary"]["root_closed"] is False and
            graphs["closure_boundary"]["closed_obligations"] == [] and
            graphs["closure_boundary"]["remaining_machine_root_cut_set"] ==
            ["M0115-T-RELATIVE", "M0115-T-TODD_ACTION"],
            "P06-COMPOSITION", "frozen graph closure boundary changed")

    source = (HERE / "Proof.lean").read_text(encoding="utf-8")
    stripped = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    stripped = re.sub(r"--.*", "", stripped)
    require(PROHIBITED.search(stripped) is None, "P05-HYGIENE",
            "proof source contains a prohibited construct")
    for marker in (
        "def counterexampleData :",
        "theorem counterexampleData_hypotheses :",
        "theorem not_grothendieckRiemannRochTarget :",
        "¬ GrothendieckRiemannRochTarget.{0, 0}",
        "#print axioms not_grothendieckRiemannRochTarget",
        "#print sorries not_grothendieckRiemannRochTarget",
    ):
        require(marker in source, "P04-KERNEL", f"negative proof marker missing: {marker}")


def lean_replay() -> str:
    require((LEAN_ROOT / ".lake").exists(), "P04-KERNEL", "pinned .lake artifacts are unavailable")
    mathlib = LEAN_ROOT / ".lake/packages/mathlib"
    require(output("git", "rev-parse", "HEAD", cwd=mathlib) == MATHLIB_REVISION and
            output("git", "rev-parse", "HEAD^{tree}", cwd=mathlib) == MATHLIB_TREE and
            output("git", "status", "--porcelain=v1", cwd=mathlib) == "",
            "G09-FRESHNESS", "pinned mathlib revision, tree, or cleanliness changed")
    lean = output("lake", "env", "which", "lean", cwd=LEAN_ROOT)
    lean_path = output("lake", "env", "printenv", "LEAN_PATH", cwd=LEAN_ROOT)
    env = {
        **os.environ, "LEAN_PATH": lean_path, "LC_ALL": "C", "LANG": "C",
        "TZ": "UTC", "NO_COLOR": "1", "LEAN_NUM_THREADS": "1",
    }
    with tempfile.TemporaryDirectory(prefix="thm-m-0115-proof-") as temporary:
        temp = Path(temporary)
        statement = subprocess.run(
            [lean, "--trust=0", "-o", str(temp / "Statement.olean"), str(HERE / "Statement.lean")],
            cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=240, check=False,
        )
        require(statement.returncode == 0, "P04-KERNEL", "Statement.lean replay failed")
        proof = subprocess.run(
            [lean, "--trust=0", str(HERE / "Proof.lean")], cwd=ROOT,
            env={**env, "LEAN_PATH": f"{temp}:{lean_path}"}, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=240, check=False,
        )
        require(proof.returncode == 0, "P04-KERNEL", "Proof.lean replay failed")
    text = proof.stdout
    require("sorryAx" not in text and text.count("Declarations are sorry-free!") == 2,
            "P05-HYGIENE", "negative declaration is not sorry-free")
    for declaration in ("counterexampleData_hypotheses", "not_grothendieckRiemannRochTarget"):
        require(f"'{declaration}' depends on axioms: [propext," in text or
                f"'Stage1Instances.THMM0115.Proof.{declaration}' depends on axioms: [propext," in text,
                "P04-KERNEL", f"axiom report missing for {declaration}")
    require(text.count("Classical.choice") == 2 and text.count("Quot.sound") == 2,
            "P04-KERNEL", "negative declarations have an unexpected axiom profile")
    return hashlib.sha256(text.encode()).hexdigest()


def assert_receipt_and_packet(lean_output_sha256: str) -> None:
    receipt = load(HERE / "proof-receipt.json")
    required = {
        "schema_version", "receipt_id", "item_id", "theorem_id", "phase", "intent",
        "base_revision", "base_tree", "inputs", "support_state", "proposed_state",
        "accepted", "verdict", "selftest_status", "selftest_result", "known_failures",
        "first_failed_gate", "retry_condition", "status_boundary", "audit_complete",
        "theorem_complete", "invalidation_inputs", "canonical_target",
        "exact_declarations", "closed_obligation_ids", "proof_body", "result",
    }
    require(required <= set(receipt), "P01-ARTIFACTS", "proof receipt omits required fields")
    require(receipt["schema_version"] == "stage1-node-receipt/1.0" and
            (receipt["item_id"], receipt["theorem_id"], receipt["phase"], receipt["intent"]) ==
            (ITEM, THEOREM, "proof", "prove"), "P01-ARTIFACTS", "proof receipt identity changed")
    require(receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE,
            "G09-FRESHNESS", "proof receipt base changed")
    require(receipt["support_state"] == "provisional_worker_selftest" and
            receipt["proposed_state"] == "[_]" and receipt["accepted"] is False and
            receipt["verdict"] == "blocked" and receipt["selftest_status"] == "passed",
            "P01-ARTIFACTS", "proof receipt overstates phase acceptance")
    require(receipt["selftest_result"]["exit_code"] == 0 and
            receipt["selftest_result"]["commands"], "P01-ARTIFACTS", "proof self-test is empty")
    require(receipt["audit_complete"] is False and receipt["theorem_complete"] is False and
            receipt["closed_obligation_ids"] == [], "P04-KERNEL", "negative proof closed a positive boundary")
    require(receipt["exact_declarations"] == [
        "Stage1Instances.THMM0115.Proof.counterexampleData_hypotheses",
        "Stage1Instances.THMM0115.Proof.not_grothendieckRiemannRochTarget",
    ], "P04-KERNEL", "proof declaration inventory changed")
    require(receipt["proof_body"]["source_sha256"] == EXPECTED_HASHES["Proof.lean"] and
            receipt["result"]["lean_output_sha256"] == lean_output_sha256,
            "P04-KERNEL", "proof source or Lean-output binding changed")
    require(receipt["result"]["phase_accepted"] is False and
            receipt["result"]["phase_predicate_proven"] is False and
            receipt["result"]["blocked"] is True and receipt["result"]["exit_code"] == 0,
            "P04-KERNEL", "proof semantic result changed")
    require(receipt["inputs"]["proof_validator"] == {
        "path": f"Stage1_Instances/{THEOREM}/check_proof.py",
        "sha256": sha256(HERE / "check_proof.py"),
        "git_blob": output("git", "hash-object", "--no-filters", str(HERE / "check_proof.py")),
        "existed_at_base": False,
        "current_claim_selection_eligible": False,
    }, "P01-ARTIFACTS", "receipt validator binding changed")
    require(receipt["inputs"]["phase_receipt"] == {
        "path": f"Stage1_Instances/{THEOREM}/proof-receipt.json",
        "sha256": "scheduler_recomputed_after_integration",
        "git_blob": "scheduler_recomputed_after_integration",
    }, "P01-ARTIFACTS", "phase-receipt self-binding boundary changed")
    ledger = receipt["inputs"]["dependency_reuse_ledger"]
    require(ledger["sha256"] == EXPECTED_HASHES["dependency-reuse-ledger.json"] and
            ledger["path"] == f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json",
            "P03-REUSE", "receipt dependency-ledger binding changed")
    proof_source = receipt["inputs"]["proof_sources"]
    require(proof_source == [{
        "path": f"Stage1_Instances/{THEOREM}/Proof.lean",
        "sha256": EXPECTED_HASHES["Proof.lean"],
        "git_blob": output("git", "hash-object", "--no-filters", str(HERE / "Proof.lean")),
    }], "P01-ARTIFACTS", "receipt proof-source binding changed")

    packet = load(ROOT / ".stage1-worker-selftest.json")
    require(set(packet) == {"item_id", "changed_paths", "commands", "output_summary",
                            "base_revision", "known_failures", "state"},
            "P01-ARTIFACTS", "worker packet field set changed")
    require(packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION and
            packet["state"] == "[_]", "P01-ARTIFACTS", "worker packet identity changed")
    require(packet["commands"] == receipt["selftest_result"]["commands"] and
            packet["known_failures"] == receipt["known_failures"],
            "P01-ARTIFACTS", "worker packet and receipt disagree")
    expected_changed = {
        ".stage1-worker-selftest.json",
        f"Stage1_Instances/{THEOREM}/Proof.lean",
        f"Stage1_Instances/{THEOREM}/check_proof.py",
        f"Stage1_Instances/{THEOREM}/dependency-reuse-ledger.json",
        f"Stage1_Instances/{THEOREM}/proof-blocker.json",
        f"Stage1_Instances/{THEOREM}/proof-receipt.json",
        f"Stage1_Instances/{THEOREM}/proof-validation.md",
    }
    require(set(packet["changed_paths"]) == expected_changed,
            "P01-ARTIFACTS", "worker packet changed-path inventory is incomplete")
    status = output("git", "status", "--short", "--untracked-files=all")
    actual = {
        (line[3:] if line.startswith("?? ") else line[2:].lstrip())
        for line in status.splitlines()
        if (line[3:] if line.startswith("?? ") else line[2:].lstrip())
        != "Formalizations/Lean/.lake"
    }
    require(actual == expected_changed, "P01-ARTIFACTS", "worktree delta differs from worker packet")


def semantic(*, replayed: bool, gate: str | None, message: str,
             stale: list[str] | None = None) -> dict:
    value = {
        "schema_version": "stage1-validator-semantic-result/1.0",
        "item_id": ITEM,
        "theorem_id": THEOREM,
        "phase": "proof",
        "status": "blocked" if replayed else ("stale" if stale else "failed"),
        "verdict": "blocked" if replayed else "repair_required",
        "phase_accepted": False,
        "audit_complete": False,
        "theorem_complete": False,
        "phase_predicate_proven": False,
        "first_failed_gate": "P04-KERNEL/EXACT-TARGET-CONSISTENCY" if replayed else gate,
        "open_obligations": 32,
        "stale_inputs": stale or [],
        "blocked": replayed,
        "message": message,
    }
    require(set(value) == RESULT_FIELDS, "P01-ARTIFACTS", "internal semantic schema changed")
    return value


def main() -> int:
    try:
        assert_authorities()
        assert_contract_and_claim()
        assert_ledger()
        assert_frozen_proof_boundary()
        lean_sha256 = lean_replay()
        assert_receipt_and_packet(lean_sha256)
        result = semantic(
            replayed=True,
            gate=None,
            message=(
                "The exact empty dependency closure and a placeholder-free trust-zero "
                "countermodel were replayed. The frozen abstract target is false because "
                "its semantic compatibility propositions do not constrain its operations; "
                "the positive proof predicate remains unsatisfied and requires statement repair."
            ),
        )
    except GateFailure as exc:
        result = semantic(replayed=False, gate=exc.gate, message=exc.message, stale=exc.stale)
    except Exception as exc:
        result = semantic(
            replayed=False, gate="VALIDATOR-INTERNAL",
            message=f"unexpected validator failure: {type(exc).__name__}: {exc}",
        )
    sys.stdout.write(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n")
    return 0 if result["status"] == "blocked" else 1


if __name__ == "__main__":
    raise SystemExit(main())
