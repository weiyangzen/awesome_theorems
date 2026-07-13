#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0484-RELEASE."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0484"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0484-RELEASE"
THEOREM = "THM-M-0484"
BASE_REVISION = "e0a9d2c084c4d594e507b71814771c796d0a07a9"
BASE_TREE = "bec710b64b57f2e7b6363ddc0d32722b57728dc5"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
TERMINAL_SOURCE_SHA256 = "6321c156165f59d49954c0e6e47706e765c0277df20b97a20333ceba29e8bead"
TERMINAL_OLEAN_SHA256 = "c02832844a7c1605945cf05750cbcc0909909124ea7ba45f335888bae0157844"
EXPRESSION_SHA256 = "6bd6024bd44d0bd9c50f6425b9ce5fdaecaf783ac84d32688717d3bde3151aea"
DENOMINATOR_SHA256 = "af0c1b5d7bfd4da0a7f1b982646906d20217976af4c5805295d37e43d0b39edf"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
MACHINE_CUT = ["M0484-T-SUFFICIENCY", "M0484-T-NECESSITY"]
RELEASE_CUT = [
    "M0484-X-SOURCE",
    "M0484-S-FOUNDATION",
    "M0484-X-PROVENANCE",
    "M0484-X-TRUST",
    "M0484-X-READABLE",
    "M0484-X-WORKFLOW",
]
SEMANTIC_OUTPUT = "\n".join(
    (
        "PASS S56-M-0484-RELEASE: exact root and residue route trust-zero replay agree",
        "PASS reconciliation: pins, receipts, authority, graph cuts, and unchanged vector agree",
        "BLOCKED first gate: S56-10.2-DEPENDENCY-ACCEPTANCE",
        (
            "BLOCKED assurance: H0/R0/composition/trust/TCB/hermetic/independent/"
            "bundle gates remain"
        ),
        "VERDICT blocked: planned H1/M3/R4; audit_complete=false; theorem_complete=false",
    )
)
CHANGED_PATHS = [
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
]

if not __debug__:
    raise RuntimeError("release validation requires Python assertions")


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    timeout: int = 330,
) -> str:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"command failed ({completed.returncode}): {argv!r}\n{completed.stdout}")
    return completed.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).rstrip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def check_authority(receipt: dict, decision: dict) -> None:
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    dag = load(HERE / "task-dag.json")
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1365
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release = next(row for row in execution["items"] if row["id"] == ITEM)
    validation = next(
        row for row in execution["items"] if row["id"] == "S56-M-0484-VALIDATION"
    )
    expected = {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1365,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0484-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert release == expected
    assert validation["state"] == "[_]" and validation["attempts"] == 1
    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is False and instance["theorem_complete"] is False
    assert dag["accepted_states"] == []
    assert dag["audit_complete"] is False and dag["theorem_complete"] is False
    local_release = next(row for row in dag["tasks"] if row["id"] == ITEM)
    local_validation = next(
        row for row in dag["tasks"] if row["id"] == "S56-M-0484-VALIDATION"
    )
    assert local_release["state"] == local_validation["state"] == "open"

    assert receipt["authority_inputs"] == {
        "Docs/Stage1_Targets_rev-5.6.json": sha256(
            ROOT / "Docs/Stage1_Targets_rev-5.6.json"
        ),
        "Docs/Stage1_Execution_DAG_rev-5.6.json": sha256(
            ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json"
        ),
        "task-dag.json": sha256(HERE / "task-dag.json"),
        "instance.json": sha256(HERE / "instance.json"),
    }
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    vector = {"H": "H1", "M": "M3", "R": "R4"}
    assert decision["root_vector_before"] == decision["root_vector_after"] == vector
def check_reconciliation(receipt: dict, decision: dict, spec: dict) -> None:
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["normative_profile"] == "machine-theorem-assurance/1.0"
    assert receipt["execution_rank"] == decision["execution_rank"] == 1365
    assert receipt["phase"] == receipt["intent"] == decision["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-0484-VALIDATION"]
    assert receipt["verdict"] == decision["verdict"] == "blocked"
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["receipt_class"] == receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["receipt_id"] == "S56-M-0484-RELEASE-local-20260713T232552+0800"
    assert receipt["acceptance_authority"] == "Stage1 integration lane"
    assert receipt["content_addressed"] is False and receipt["release_grade"] is False
    assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
    assert receipt["master_acceptance"] == "pending_and_not_claimed"
    assert receipt["accepted_receipt_ids"] == decision["accepted_receipt_ids"] == []
    assert receipt["result"]["semantic_output_sha256"] == hashlib.sha256(
        SEMANTIC_OUTPUT.encode("utf-8")
    ).hexdigest()
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    for name, expected in receipt["release_artifact_inputs"].items():
        assert sha256(HERE / name) == expected, f"release artifact input drifted: {name}"

    for name, expected in decision["reconciled_inputs"].items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    assert decision["dependency"]["receipt_sha256"] == sha256(
        HERE / "validation-receipt.json"
    )
    assert decision["dependency"]["receipt_id"] == validation["receipt_id"]
    assert decision["dependency"]["item_id"] == validation["item_id"]
    assert validation["accepted"] is False and validation["proposed_state"] == "[_]"
    assert validation["content_addressed"] is False and validation["release_grade"] is False
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False

    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == sha256(HERE / "Statement.lean")
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == "M0484-ROOT"
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["accepted_closed_obligations"] == []
    assert closure["audit_complete"] is False and closure["theorem_complete"] is False
    assert closure["remaining_machine_root_cut_set"] == MACHINE_CUT
    assert closure["remaining_release_cut_set"] == RELEASE_CUT
    assert len(graphs["unverified_decomposition_plans"]) == 17
    assert decision["authoritative_graph_remaining_machine_root_cut_set"] == MACHINE_CUT
    assert decision["authoritative_graph_remaining_release_cut_set"] == RELEASE_CUT

    assert proof["accepted"] is False and proof["proposed_state"] == "[_]"
    assert proof["result"]["root_kernel_declaration_closed"] is True
    assert proof["result"]["accepted_root_closed"] is False
    assert proof["closed_obligation_ids"] == proof["accepted_closed_obligation_ids"] == []
    assert proof["internal_composition_boundary"]["unverified_internal_composition_count"] == 17

    assert decision["verdict"] == receipt["result"]["verdict"] == "blocked"
    assert decision["audit_complete"] is receipt["result"]["audit_complete"] is False
    assert decision["theorem_complete"] is receipt["result"]["theorem_complete"] is False
    assert decision["release_accepted"] is False
    assert decision["first_failed_gate"]["gate_id"] == receipt["first_failed_gate"]
    assert receipt["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["known_failures"] == receipt["known_failures"]
    assert decision["remaining_root_cut_set"] == receipt["remaining_root_cut_set"]
    assert decision["retry_condition"] == receipt["retry_condition"]
    assert decision["invalidation_inputs"] == receipt["invalidation_inputs"]
    assert decision["freshness"] == receipt["freshness"]
    result = receipt["result"]
    assert result["exit_code"] == 0
    assert result["observed_axioms"] == sorted(EXPECTED_AXIOMS)
    assert result["terminal_closure_declarations"] == 35389
    assert result["terminal_closure_modules"] == 1243
    assert result["local_kernel_replay"] == (
        "pass_for_exact_statement_direction_composition_exact_root_and_residue_route"
    )
    assert result["dependency_master_acceptance"] == "fail_closed"
    assert result["authoritative_root_state"] == "H1/M3/R4_open"
    for gate in (
        "audit_z",
        "theorem_z",
        "hermetic_release_gate",
        "supply_chain_gate",
        "independent_verification_gate",
        "deterministic_bundle_gate",
    ):
        assert result[gate] == "fail_closed", f"receipt silently cleared {gate}"
    assert result["master_acceptance_gate"] == "pending"

    required_false = (
        "authoritative_graph_reconciled",
        "accepted_root_m0_e1",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "accepted_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_offline_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_release_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle",
        "master_acceptance",
    )
    reconciliation = decision["evidence_reconciliation"]
    for gate in required_false:
        assert reconciliation[gate] is False, f"release gate silently cleared: {gate}"

    cut = "\n".join(decision["remaining_root_cut_set"])
    for phrase in (
        "master acceptance",
        "M0-W/E1",
        "17 abstract-child composition certificates",
        "H0 primary-source",
        "R0 anchored",
        "TCB closure",
        "empty-cache network-denied cold build",
        "SBOM",
        "two signed attestations",
        "minimal release verifier",
        "protected CI",
        "deterministic content-addressed release bundle",
    ):
        assert phrase in cut, f"release cut set omits {phrase!r}"

    assert spec["argv"] == [
        "python3",
        "-I",
        "-B",
        f"Stage1_Instances/{THEOREM}/check_release.py",
        "--worker-packet",
        ".stage1-worker-selftest.json",
    ]
    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["recipe_id"] == receipt["recipe"]["recipe_id"]
    assert spec["cwd"] == "." and spec["network_policy"] == "denied"
    assert spec["timeout_seconds"] == 360 and spec["expected_exit"] == 0
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id",
            "cwd",
            "argv",
            "env_allowlist",
            "timeout_seconds",
            "network_policy",
            "expected_exit",
        )
    }
    assert spec["expected_outputs"] == [
        {
            "path_or_stream": "stdout",
            "semantic_hash_policy": (
                "contains PASS S56-M-0484-RELEASE, the first failed "
                "dependency-acceptance gate, and the blocked unchanged terminal decision"
            ),
        }
    ]
    assert set(spec["covered_obligation_ids"]) <= {
        row["obligation_id"] for row in registry["obligations"]
    }
    assert spec["covered_obligation_ids"] == [
        "M0484-ROOT",
        "M0484-T-ASSEMBLE",
        "M0484-T-SUFFICIENCY",
        "M0484-T-NECESSITY",
    ]
    assert spec["negative_status_only_obligation_ids"] == RELEASE_CUT
    assert spec["covered_declarations"] == [
        "Stage1Instances.THM_M_0484.LucasLehmerTestTarget",
        "Stage1Instances.THM_M_0484.Proof.lucasLehmerCriterion",
        "Stage1Instances.THM_M_0484.Validation.differentialLucasLehmerCriterion",
    ]
    assert "receive no closure credit" in spec["scope_boundary"]

    prose = (HERE / "release-phase.md").read_text(encoding="utf-8")
    for fragment in (
        "The release verdict is **blocked**.",
        "`audit_complete=false`",
        "`theorem_complete=false`",
        "`S56-10.2-DEPENDENCY-ACCEPTANCE`",
        "not theorem completion",
    ):
        assert fragment in prose, f"release prose lost boundary: {fragment}"


def replay_validation(spec: dict) -> str:
    env = os.environ.copy()
    env.update(spec["env_allowlist"])
    assert sha256(LEAN_ROOT / "lean-toolchain") == TOOLCHAIN_SHA256
    assert sha256(LEAN_ROOT / "lake-manifest.json") == MANIFEST_SHA256
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=env).strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT, env=env).strip())
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    version = run([str(lean), "--version"], cwd=LEAN_ROOT, env=env)
    assert "4.29.0" in version and LEAN_COMMIT in version
    assert MATHLIB.is_dir() and (LEAN_ROOT / ".lake").is_symlink()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    terminal = MATHLIB / "Mathlib/NumberTheory/LucasLehmer.lean"
    terminal_olean = (
        MATHLIB / ".lake/build/lib/lean/Mathlib/NumberTheory/LucasLehmer.olean"
    )
    assert sha256(terminal) == TERMINAL_SOURCE_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean",
        "ObligationTree.lean",
        "Proof.lean",
        "Validation.lean",
        "AnchorAudit.lean",
    ):
        assert prohibited.search(code_without_comments((HERE / name).read_text())) is None
    assert prohibited.search(code_without_comments(terminal.read_text())) is None

    output = run(
        [
            "python3",
            "-I",
            "-B",
            str(HERE / "check_validation.py"),
            "--probe",
        ],
        cwd=ROOT,
        env=env,
    )
    observation = json.loads(output)
    recorded = load(HERE / "validation-receipt.json")["result"]
    receipt = load(HERE / "release-receipt.json")
    canonical_observation = json.dumps(observation, sort_keys=True, separators=(",", ":"))
    assert receipt["result"]["predecessor_observation_sha256"] == hashlib.sha256(
        canonical_observation.encode("utf-8")
    ).hexdigest()
    assert observation["output_sha256"] == recorded["lean_output_sha256"]
    assert observation["observed_axioms"] == sorted(EXPECTED_AXIOMS)
    assert observation["anchor_closure_declarations"] == 35389
    assert observation["anchor_closure_modules"] == 1243
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    return output


def check_worker_packet(receipt: dict, packet_path: Path) -> None:
    packet = load(packet_path.resolve())
    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == receipt["changed_paths"] == CHANGED_PATHS
    assert packet["commands"] == receipt["worker_packet_commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]

    status = git("status", "--short", "--untracked-files=all")
    temporary_prefix = "Formalizations/Lean/stage1-m0484-validation-"
    temporary_paths = {
        line[3:] for line in status.splitlines() if line[3:].startswith(temporary_prefix)
    }
    assert not temporary_paths or any(
        (ROOT / path).parent.name.startswith("stage1-m0484-validation-")
        for path in temporary_paths
    )
    actual = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
        and not line[3:].startswith(temporary_prefix)
    }
    assert actual == set(CHANGED_PATHS), (actual, set(CHANGED_PATHS))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-packet", type=Path)
    args = parser.parse_args()

    spec = load(HERE / "release-spec.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    check_authority(receipt, decision)
    check_reconciliation(receipt, decision, spec)
    replay_validation(spec)
    if args.worker_packet is not None:
        check_worker_packet(receipt, args.worker_packet)

    for relative in CHANGED_PATHS[1:]:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print(SEMANTIC_OUTPUT)


if __name__ == "__main__":
    main()
