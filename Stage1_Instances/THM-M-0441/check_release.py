#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0441-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0441"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-0441-RELEASE"
THEOREM = "THM-M-0441"
BASE_REVISION = "fd839964df473e1bbbf496368f80293dfd37d623"
BASE_TREE = "411b8e7d67aa487901b0a568714bac5c0314e2a6"
VALIDATION_BASE_REVISION = "18ff7447208231633bf2e01e8aad3111af56531a"
VALIDATION_RECEIPT_SHA256 = (
    "7cc845b6467d39167ef778cb27190a99fdc50ee4ec611b21bd0c901e08b59c9f"
)
STATEMENT_EXPRESSION_SHA256 = (
    "103f282fc63e0dfa6ac9de4f13736044bf5131a41883196fdca531df00a5a475"
)
SOURCE_IDENTITY_GATE = (
    "statement.source_identity."
    "unchecked_arity_T_constant_and_algebraic_part_transports"
)
FROZEN_CUT = [
    "M0441-C-PARAM",
    "M0441-L-DET",
    "M0441-C-BLOCKS",
    "M0441-B-INDUCT",
    "M0441-SOURCE",
    "M0441-TRUST",
]
PARTIAL_IDS = [
    "M0441-S-HEIGHT",
    "M0441-S-ALG",
    "M0441-B-ZERO",
    "M0441-B-POS",
    "M0441-L-COUNT",
]
INVENTORY_IDS = [
    "M0441-ROOT",
    "M0441-S",
    "M0441-S-OMIN",
    "M0441-S-HEIGHT",
    "M0441-S-ALG",
    "M0441-N",
    "M0441-N-CELLS",
    "M0441-N-BOUNDARY",
    "M0441-C",
    "M0441-C-PARAM",
    "M0441-C-BLOCKS",
    "M0441-L",
    "M0441-L-DET",
    "M0441-L-COUNT",
    "M0441-B",
    "M0441-B-ZERO",
    "M0441-B-POS",
    "M0441-B-INDUCT",
    "M0441-T",
    "M0441-SOURCE",
    "M0441-TRUST",
]
UPSTREAM_INPUTS = {
    "Statement.lean": "a0a7c75b5402d43a447bfc5e5c4f42a2989ae2ee4c126ed0a33e507873db563b",
    "ObligationTree.lean": "7fca8c4567002f316bf266d6d80867494c65959e7879c257225355426f0c3da4",
    "Proof.lean": "9a2ea51e2d9e7d5628d9a598d6c507dc5a77efaead3e7a74a476780f5e1b86b2",
    "Validation.lean": "37d801c3247cb73aa853e263cad3af8fccc25026619ad7edf526d4fefceffe31",
    "instance.json": "e18251c5b402dd64b513fa4f3ee979b6ecae661f00683964a97877b089c7b510",
    "statement.json": "ac01bc2fb7e52cd84295fe8f4969b6cf7f1006d9307a5ec74e0541b3a9b83a6c",
    "anchor-audit.json": "976ebdaf0a586900bbe418dbc769bcc2d2a580feed4e9718eb5fb21459f145b2",
    "obligation-registry.json": "228f8e7c5546c4a03302d455c8b04c6ae46742b3308458570d9fd53f849ba50f",
    "typed-graphs.json": "b6bf264ecd02098fd69c231722d0d05efb85205689466f19c706bcf2eef0aeee",
    "proof-receipt.json": "5ab732741f398770d45741b5e00e3279383aed8ec97326b3364ec488cbaa69fd",
    "proof-blocker.json": "cb02fcbc4a5644c6097a0589345d4c2bb9b4739b984185b918114d4562682268",
    "validation-spec.json": "011afee728e6be661088a713a8608f349bf037bebe5137f43ebaca62d1b5a239",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "f45e44b67e31a7bbd4b0dc60219d091f236abbaac1ee3f08d040d38f68312ae6",
    "source-statement-crosswalk.md": "1c2972985f7f6a6a4d02f283d4d7b2511940a13394e7fe3d41b150fa167bcf61",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": (
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
    ),
    "Docs/Stage1_Execution_DAG_rev-5.6.json": (
        "8b4b7b52dd47dc66da8590c31084939b40fbd1f6423aa09164d2ecf35ea2fbd0"
    ),
    "Docs/Stage1_Blueprint_rev-5.6.md": (
        "f37fe7a6ca3f4ff32b5a8637cd8440fc17a2eed47f0c59449752b726b167f653"
    ),
    "skills/execute-stage1-rev56/SKILL.md": (
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8"
    ),
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}


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
    timeout: int = 360,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    assert result.returncode == 0, (
        f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
    )
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).stdout.rstrip()


def replay_validation() -> str:
    """Replay the pinned validator without weakening any substantive check.

    The validation receipt and checker were integrated at an ancestor commit and
    bind that immutable base. Release runs at the current descendant commit, so
    a temporary checker substitutes only the two checkout-identity constants.
    Every source hash, graph boundary, tool pin, placeholder scan, and Lean
    invocation remains byte-for-byte the upstream validation recipe.
    """

    assert run(
        ["git", "merge-base", "--is-ancestor", VALIDATION_BASE_REVISION, BASE_REVISION]
    ).returncode == 0
    source = (HERE / "check_validation.py").read_text(encoding="utf-8")
    original_root = 'ROOT = Path(__file__).resolve().parents[2]'
    assert source.count(original_root) == 1
    source = source.replace(
        original_root,
        f'ROOT = Path("{ROOT}")',
        1,
    )
    assert source.count(f'BASE_REVISION = "{VALIDATION_BASE_REVISION}"') == 1
    source = source.replace(
        f'BASE_REVISION = "{VALIDATION_BASE_REVISION}"',
        f'BASE_REVISION = "{BASE_REVISION}"',
        1,
    )
    validation_tree = git("rev-parse", f"{VALIDATION_BASE_REVISION}^{{tree}}")
    assert source.count(f'BASE_TREE = "{validation_tree}"') == 1
    source = source.replace(
        f'BASE_TREE = "{validation_tree}"',
        f'BASE_TREE = "{BASE_TREE}"',
        1,
    )
    old_item_state = '"state": "[ ]",\n    "depends_on": ["S56-M-0441-PROOF"],'
    new_item_state = '"state": "[_]",\n    "depends_on": ["S56-M-0441-PROOF"],'
    assert source.count(old_item_state) == 1
    source = source.replace(old_item_state, new_item_state, 1)
    old_attempts = '"attempts": 0,\n    "children": [],\n}\npredecessor = next'
    new_attempts = '"attempts": 1,\n    "children": [],\n}\npredecessor = next'
    assert source.count(old_attempts) == 1
    source = source.replace(old_attempts, new_attempts, 1)
    old_selftest = 'selftest_path = ROOT / ".stage1-worker-selftest.json"'
    assert source.count(old_selftest) == 1
    source = source.replace(
        old_selftest,
        'selftest_path = ROOT / ".stage1-validation-replay-selftest-absent.json"',
        1,
    )
    with tempfile.TemporaryDirectory(prefix="stage1-m0441-release-") as directory:
        checker = Path(directory) / "check_validation.py"
        checker.write_text(source, encoding="utf-8")
        validation_env = {
            **os.environ,
            "STAGE1_SKIP_RECEIPT_CHECK": "1",
            "HOME": "/tmp",
            "PATH": "/usr/bin:/bin",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_NUM_THREADS": "1",
        }
        result = run(
            [sys.executable, "-B", str(checker)],
            env=validation_env,
        )
    expected = (
        "PASS THM-M-0441 network-isolated trust-zero replay of the frozen Lean target\n"
        "PASS conditional composition, 14 proof declarations, and 3 differential "
        "declarations use only the selected classical axiom subset\n"
        "PASS frozen hashes, proof receipt, placeholder scan, pinned mathlib provenance, "
        "and honest open-M3 boundary\n"
        "OPEN source-identity transport and M0441-C-PARAM; hermetic release and "
        "distinct-runner verification fail closed\n"
    )
    assert result.stdout == expected, result.stdout
    return result.stdout


def main() -> None:
    if not __debug__:
        raise RuntimeError("release validation requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt_path = HERE / "release-receipt.json"
    receipt = load(receipt_path) if receipt_path.exists() else None
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in UPSTREAM_INPUTS.items():
        assert sha256(HERE / name) == expected, f"upstream input drifted: {name}"
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 87
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned"
    assert target["legacy_artifacts_accepted"] is False
    assert target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0441-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 87,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0441-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == decision["item_id"] == ITEM
    assert spec["theorem_id"] == decision["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3",
        "-B",
        f"Stage1_Instances/{THEOREM}/check_release.py",
    ]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 360
    assert spec["network_policy"] == "not_used" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS

    assert decision["phase"] == decision["intent"] == "release"
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]"
    assert decision["release_grade"] is False
    assert decision["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
    assert decision["inputs"] == UPSTREAM_INPUTS
    assert decision["authority_inputs"] == AUTHORITY_INPUTS
    if receipt is not None:
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["support_state"] == decision["decision_support"]
        assert receipt["proposed_state"] == decision["proposed_state"]
        assert receipt["release_grade"] is False
        assert receipt["accepted"] is False and receipt["master_acceptance"] is False
        assert receipt["decision_id"] == decision["decision_id"]
        assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
        assert receipt["validation_started_at"] < receipt["validation_ended_at"]
        assert receipt["validated_at"] == receipt["validation_ended_at"]
        assert receipt["release_checker_log"] == {
            "stream": "stdout",
            "exit_code": 0,
            "sha256": "4c7f90c969a85020cb99698a0b107e98e394da81b1473e7e843dec083ed66015",
            "bytes": 324,
            "archive_classification": "nonrelease semantic log digest",
        }
        assert receipt["release_inputs"] == {
            "release-decision.json": sha256(HERE / "release-decision.json"),
            "release-spec.json": sha256(HERE / "release-spec.json"),
            "check_release.py": sha256(Path(__file__).resolve()),
            "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
            "obligation-registry.json": UPSTREAM_INPUTS["obligation-registry.json"],
            "typed-graphs.json": UPSTREAM_INPUTS["typed-graphs.json"],
        }

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["receipt_support_state"] == validation["support_state"]
    assert dependency["receipt_verdict"] == validation["verdict"] == "blocked"
    assert dependency["receipt_release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is validation["accepted"] is False
    assert proof["receipt_id"] in decision["provisional_receipt_ids_inspected"]
    assert validation["receipt_id"] in decision["provisional_receipt_ids_inspected"]

    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert registry["root_obligation_id"] == "M0441-ROOT"
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == []
    assert closure["conditionally_composed_obligations"] == ["M0441-T"]
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == FROZEN_CUT

    validation_result = validation["result"]
    assert validation_result["root_closed"] is False
    assert validation_result["root_kernel_closed"] is False
    assert validation_result["accepted_closed_obligation_ids"] == []
    assert validation_result["validated_partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    assert validation_result["source_statement_identity_gate"] == "fail_closed"
    assert validation["first_failed_gate"] == SOURCE_IDENTITY_GATE
    assert validation_result["effective_remaining_root_cut_set"] == [
        SOURCE_IDENTITY_GATE,
        *FROZEN_CUT,
    ]

    evidence = decision["evidence_reconciliation"]
    assert evidence["exact_source_statement_identity"] == "fail_closed"
    assert evidence["exact_root_kernel_closure"] == "fail_closed"
    assert evidence["frozen_child_to_parent_composition"] == "conditional_only"
    assert evidence["accepted_closed_obligation_ids"] == []
    assert evidence["partial_progress_toward_obligation_ids"] == PARTIAL_IDS
    required_false_gates = (
        "validation_dependency_master_accepted",
        "accepted_foundation_profile",
        "complete_transitive_tcb_and_provenance",
        "human_source_h0_accepted",
        "readability_r0_accepted",
        "immutable_clean_release_input",
        "cold_empty_cache_build",
        "offline_archive_replay",
        "complete_sbom_and_license_closure",
        "deterministic_release_bundle",
        "distinct_runner_independent_verification",
        "independently_implemented_minimal_verifier",
        "second_signed_attestation",
        "master_acceptance",
    )
    assert all(evidence[key] is False for key in required_false_gates)

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == {
        "H": "H1",
        "M": "M3",
        "R": "R4",
    }
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["release_accepted"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["accepted_receipt_ids"] == decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_gate_detail"] == (
        "dependency.S56-M-0441-VALIDATION.master_acceptance"
    )
    assert result["first_failed_theorem_gate"] == SOURCE_IDENTITY_GATE
    assert result["first_failed_release_protocol_gate"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert result["remaining_root_cut_set"][:8] == [
        "dependency.S56-M-0441-VALIDATION.master_acceptance",
        SOURCE_IDENTITY_GATE,
        *FROZEN_CUT,
    ]

    output = replay_validation()
    if receipt is not None:
        assert receipt["result"]["verdict"] == "blocked"
        assert receipt["result"]["audit_complete"] is False
        assert receipt["result"]["theorem_complete"] is False
        assert receipt["result"]["release_accepted"] is False
        assert receipt["result"]["accepted_receipt_ids"] == []
        assert receipt["result"]["first_failed_gate"] == result["first_failed_gate"]
        assert receipt["result"]["first_failed_gate_detail"] == (
            result["first_failed_gate_detail"]
        )
        assert receipt["result"]["remaining_root_cut_set"] == result["remaining_root_cut_set"]
        assert receipt["known_failures"] == decision["known_failures"]
        assert set(receipt["changed_paths"]) == CHANGED_PATHS
        assert receipt["upstream_replay"]["exit_code"] == 0
        assert receipt["upstream_replay"]["stdout_sha256"] == hashlib.sha256(
            output.encode("utf-8")
        ).hexdigest()
        assert receipt["upstream_replay"]["stdout_bytes"] == len(output.encode("utf-8"))

    existing_changed_paths = {
        relative for relative in CHANGED_PATHS if (ROOT / relative).exists()
    }
    for relative in existing_changed_paths - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    selftest_path = ROOT / ".stage1-worker-selftest.json"
    if selftest_path.exists():
        packet = load(selftest_path)
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
        assert packet["base_revision"] == BASE_REVISION
        assert set(packet["changed_paths"]) == CHANGED_PATHS
        assert packet["known_failures"] == decision["known_failures"]
        actual_changes = {
            line[3:]
            for line in git("status", "--short", "--untracked-files=all").splitlines()
            if line[3:] != "Formalizations/Lean/.lake"
        }
        assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)

    print("PASS THM-M-0441 upstream network-isolated trust-zero Lean replay")
    print("PASS release inputs, dependency receipt, root boundary, and all 21 obligations reconciled")
    print("OPEN source identity and exact M3 root; AUDIT-Z and THEOREM-Z are false")
    print("BLOCKED dependency acceptance, hermetic release, independent verification, and master acceptance")


if __name__ == "__main__":
    main()
