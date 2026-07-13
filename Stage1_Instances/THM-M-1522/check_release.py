#!/usr/bin/env python3
"""Fail-closed reconciliation for S56-M-1522-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1522"
ITEM = "S56-M-1522-RELEASE"
THEOREM = "THM-M-1522"
BASE_REVISION = "f78ecdb166de720e4af8d8859826b4a22a4c1733"
BASE_TREE = "6d72b645f5722769d4ed5d9eea3559c9e4c69856"
EXPRESSION_SHA256 = "1ae3d8a352060fb26372a07d0128af2f465933e4c3c08b6c752b0b5fe72c83b5"
VALIDATION_RECEIPT_ID = "S56-M-1522-VALIDATION-local-20260714T011720+0800"
AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
CANONICAL_IDS = [
    "M1522-ROOT",
    "M1522-S-DEFINITIONS",
    "M1522-S-DOMAIN",
    "M1522-S-BOUNDARY",
    "M1522-S-TRANSPORT",
    "M1522-S-FOUNDATION",
    "M1522-N-GENERAL",
    "M1522-C-LIMIT-DATA",
    "M1522-L-POINTWISE",
    "M1522-B-ERGODIC",
    "M1522-L-INTEGRAL-ID",
    "M1522-T-IDENTIFY",
    "M1522-T-ASSEMBLE",
    "M1522-X-UPSTREAM",
    "M1522-X-SOURCE",
    "M1522-X-PROVENANCE",
]
RECONCILED_INPUTS = {
    "statement.json": "2812ad428abf680cd4ee518b780b80697cb1fd008c8bbf9c7736ea77f6bd3e75",
    "anchor-audit.json": "131a286180faec74ffbf95803269dbb0d4119ab2a2cdb95105d322e1dc697e7f",
    "obligation-registry.json": "46e2fee724bfbd90b554b02daabe0d73d9c9b8eaded63851aad9f80fcf6c52dd",
    "typed-graphs.json": "9506ce707579e0055afd1ad1edd04ae97bc4dcbc993c04c9db5294647cd935cc",
    "Proof.lean": "f75d7d98d250bb557188c8a44139d7d5ce05275bd91962f37e51e619aaba797f",
    "proof-receipt.json": "262d47cd3aee6b7ea0fa92339208a88ae3b13722008ac3f668c023442783346e",
    "Validation.lean": "e77211bd2ea3ef8220dd05344598d25ce5e6bb923db7a0a1fb9782b81af3b651",
    "validation-spec.json": "a111434124357601d4e0cf78358b84d49288efe33736f6007ff5568f5873ea68",
    "validation-receipt.json": "41b78ad4cd0768e6647b6bd15d136d26022a9c8a60c72634bdd52ef0aba5b260",
    "check_validation.sh": "0655b1c88460a2b5944fa0a2094cf92f9b00ffb12f25ae8683aadc5bb7612013",
}
RELEASE_INPUTS = {
    "release-decision.json": "83951ca28102d6cc30ae597b9cfcd233db66b35b2b502178a3d90cfff84d7989",
    "release-phase.md": "32bd45393a81ef80f568ed0de6540183c4eae7c17aa314c0ec7acc96d46adb17",
    "release-spec.json": "aef5a2ff46b0bf6f5ab265dc74341d7722864b2e31bd21a090d2aa39728360af",
}
SUMMARY_LINES = (
    "PASS THM-M-1522 negative release reconciliation",
    "PASS fresh narrow Lean replay: exact root adapters are sorry-free with axioms propext, Classical.choice, Quot.sound",
    "BLOCKED dependency: S56-M-1522-VALIDATION is provisional, unaccepted, and nonrelease",
    "BLOCKED audit: frozen upstream/proof provenance and public projections are unreconciled; AUDIT-Z=false",
    "BLOCKED theorem: accepted root H1/M3/R3; hermetic, independent, bundle, and master gates open; THEOREM-Z=false",
)


def load(name: str) -> dict:
    value = json.loads((HERE / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict), name
    return value


def sha256(name: str) -> str:
    return hashlib.sha256((HERE / name).read_bytes()).hexdigest()


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True,
        timeout=30, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout.strip()


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, declaration
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def main() -> None:
    if sys.flags.optimize:
        raise SystemExit("release check failed: Python optimization disables assertions")

    decision = load("release-decision.json")
    spec = load("release-spec.json")
    receipt = load("release-receipt.json")
    validation = load("validation-receipt.json")
    proof = load("proof-receipt.json")
    statement = load("statement.json")
    registry = load("obligation-registry.json")
    graphs = load("typed-graphs.json")
    targets = json.loads((ROOT / "Docs/Stage1_Targets_rev-5.6.json").read_text())
    execution = json.loads(
        (ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json").read_text()
    )

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 190
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 190,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1522-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"]
        if row["id"] == "S56-M-1522-VALIDATION"
    )
    assert predecessor["state"] == "[_]"

    for name, expected in RECONCILED_INPUTS.items():
        assert sha256(name) == expected, f"reconciled input drifted: {name}"
        assert decision["reconciled_inputs"][name] == expected

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == "M1522-ROOT"
    assert [row["obligation_id"] for row in registry["obligations"]] == CANONICAL_IDS
    assert len(registry["frozen_denominators"]["required_human_source"]) == 12
    closure = graphs["closure_boundary"]
    assert closure["root_machine_debt"] == "M3"
    assert closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == [
        "M1522-L-POINTWISE", "M1522-T-IDENTIFY"
    ]
    upstream = next(
        row for row in graphs["nodes"] if row["obligation_id"] == "M1522-X-UPSTREAM"
    )
    assert upstream["formal_target"] == (
        "lua-vr/pointwise-birkhoff@fc06094ca0506d8d74eba8b45b34882ce5930bf4"
    )

    assert validation["receipt_id"] == VALIDATION_RECEIPT_ID
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is False and validation["release_grade"] is False
    assert validation["result"]["accepted_root_machine_debt"] == "M3"
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert proof["accepted"] is False
    assert proof["proof_body"]["machine_candidate_classification"] == "M0-P"
    assert proof["proof_body"]["proof_sha256"] == RECONCILED_INPUTS["Proof.lean"]
    assert "vendored under the owned target" in proof["proof_body"]["body_location_boundary"]
    assert proof["proof_body"]["origin"]["project"] == (
        "marcmorningstar/lean4-ergodic-theory"
    )

    assert decision["item_id"] == ITEM and decision["verdict"] == "blocked"
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == []
    before = decision["root_vector"]["accepted_before"]
    assert before == decision["root_vector"]["accepted_after"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }
    assert decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
    }
    assert decision["first_failed_gate"]["gate_id"] == (
        "S56-10.2-DEPENDENCY-ACCEPTANCE"
    )
    assert decision["first_failed_release_assurance_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    assert decision["canonical_obligation_ids"] == CANONICAL_IDS
    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "authoritative_root_closure",
        "frozen_upstream_reconciliation",
        "public_projection_reconciliation",
        "human_source_acceptance",
        "readability_acceptance",
        "foundation_and_trust_closure",
        "hermetic_release_reproduction",
        "supply_chain_closure",
        "independent_release_verification",
        "deterministic_release_bundle",
    ):
        assert reconciliation[key].startswith("missing"), key

    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["timeout_seconds"] == 600

    assert receipt["receipt_id"] == "S56-M-1522-RELEASE-local-20260714T120000+0800"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is False and receipt["release_grade"] is False
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"]
    assert receipt["recipe"] == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids", "covered_declarations",
        )
    }
    for name, expected in RELEASE_INPUTS.items():
        assert sha256(name) == expected, f"release input drifted: {name}"
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_release.py"] == sha256("check_release.py")

    replay = subprocess.run(
        ["bash", str(HERE / "check_validation.sh")],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=540,
        check=False,
    )
    assert replay.returncode == 0, replay.stdout
    declarations = (
        "Stage1Instances.THM_M_1522.birkhoffPointwiseErgodicDirect",
        "Stage1Instances.THM_M_1522.Validation."
        "independentlyReconstructedBirkhoffPointwiseErgodic",
    )
    for declaration in declarations:
        assert observed_axioms(replay.stdout, declaration) == set(AXIOMS)
    assert replay.stdout.count("Declarations are sorry-free!") == 11
    assert "sorryAx" not in replay.stdout and "declaration uses 'sorry'" not in replay.stdout

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
