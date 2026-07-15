#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1021-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1021"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1021-RELEASE"
THEOREM = "THM-M-1021"
BASE_REVISION = "557b928b377b386864527c9fb4831d45857837aa"
BASE_TREE = "e677879a6eb4cb9d6795ba1bd78726af06ab9465"
EXPRESSION_SHA256 = "5b397ee9de0936db2c62ba953794ee0c2b9dc3192370aa06825fdf4aafc8322b"
DENOMINATOR_SHA256 = "032b467a59ae30caf2d637b9707358e6ba7259edf774ba0bd8bf162e48924688"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
TRUST_DECLARATIONS = [
    "bochner_theorem",
    "AwesomeTheorems.Stage1.THM_M_1021.bochner_forward",
    "AwesomeTheorems.Stage1.THM_M_1021.bochner_reverse",
    "AwesomeTheorems.Stage1.THM_M_1021.bochner_exact",
]
RECONCILED_INPUTS = {
    "intake.json": "22d0cea865740fdbe2cef30852f5ffb02d693214f3b8584eddd891f915da24c3",
    "statement.json": "732283f757dc082397efc69fe2bf0041c7b5baf85c2fab9851f01e607164ecd5",
    "anchor_audit.json": "f5295a343f2b61af865a34352aa46104c973325698e2eeee42c3a78830d784e3",
    "obligation-registry.json": "790f2ed3c2b1683c1b47ddbfeef440bee89ff246da428656a256bffd169d8013",
    "typed-graphs.json": "0f40c21c44439a8604e1745e96af9067d634a9db325f878df38f27e38036cba0",
    "BochnerStatement.lean": "e17aaf1304266aba6bb84783cf6709b4eca34e08cc9274aebacf1479ac8762cd",
    "Proof.lean": "389f719bb6610fa8978597e793ec743c8f8680d022a166ddecbb35cfb0c5a400",
    "Validation.lean": "24a36e59f6040fa321895e0d4172209a36d75c4802d4336bb662f233c0fc61cf",
    "proof-receipt.json": "f2c6baa065adf681dc849127889ec8ec0625b5af55d0253a8cdf0e8d5e01614d",
    "validation-spec.json": "117bf8d135dae25cdea59d157c7e27f17489c7b534140b7390ced6f55601b1ae",
    "validation-receipt.json": "62e005e89e6952456dde9d933fd935ffca6625dd3a177eacd732871d1d1f7104",
    "source_statement_crosswalk.md": "6747ce08a059df983741c2778cb5c904f5df636f91fe8a5a9434ec2c95246c86",
    "README.md": "78bddb26fa204c8739d05cb5e52b8ded52c889d58cb8b0279e4ca4ade9626071",
    "check_validation.sh": "97099743871a6f3a1fb026c4ca658742807abf66e09f691ffd70a742d7070ba6",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": (
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
    ),
    "Docs/Stage1_Execution_DAG_rev-5.6.json": (
        "ab3bfabcf3ccff2b4e684273f9eaf7db9376bab69c4455f808196a6af05b3973"
    ),
    "Docs/Stage1_Blueprint_rev-5.6.md": (
        "8830573c4a74ff560daebbfcde9278136a30d9841a81816cee8a7ce9c0f5eee4"
    ),
    "skills/execute-stage1-rev56/SKILL.md": (
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8"
    ),
}
TOOL_INPUTS = {
    "Formalizations/Lean/lean-toolchain": (
        "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
    ),
    "Formalizations/Lean/lake-manifest.json": (
        "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
    ),
}
EXPECTED_TOOLS = {
    "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "lake": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
    "python": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "git": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
    "bash": "3efccc187bafa75ff1e37d246270ab3e7aa559f242c7a52bf3ec2a1b5450bdbd",
    "bubblewrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
    "elan": "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385",
}
INVENTORY_IDS = [
    "M1021-ROOT", "M1021-S", "M1021-S1", "M1021-S2", "M1021-S3",
    "M1021-S3.1", "M1021-S3.2", "M1021-S3.3", "M1021-S4", "M1021-S5",
    "M1021-N", "M1021-N1", "M1021-N1.1", "M1021-N1.2", "M1021-N2",
    "M1021-N3", "M1021-N4", "M1021-B", "M1021-BF", "M1021-BR",
    "M1021-BM", "M1021-C", "M1021-C1", "M1021-C1.1", "M1021-C1.2",
    "M1021-C2", "M1021-C2.1", "M1021-C2.2", "M1021-C3", "M1021-C3.1",
    "M1021-C3.2", "M1021-C4", "M1021-C5", "M1021-C5.1", "M1021-C5.2",
    "M1021-L", "M1021-L1", "M1021-L2", "M1021-L3", "M1021-L3.1",
    "M1021-L3.2", "M1021-T", "M1021-T1", "M1021-T2", "M1021-T3",
    "M1021-T4", "M1021-X", "M1021-X1", "M1021-X2", "M1021-X3",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-phase.md",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
}
SUMMARY_LINES = (
    "PASS release inputs: target, DAG, receipts, frozen registry, graphs, and hashes agree",
    "PASS current narrow replay: exact root is sorry-free and reports only the recorded observed axioms",
    "PASS fail-closed state: lifecycle planned; accepted root H1/M3/R3; accepted receipts 0",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "BLOCKED release assurance: graph reconciliation, H0/R0, TCB, cold offline bundle, and independent verifier are open",
    "verdict=blocked audit_complete=false theorem_complete=false",
)
KNOWN_FAILURES = [
    "S56-M-1021-VALIDATION is provisional [_], accepted=false, release_grade=false, and not master accepted.",
    "The exact root kernel-replays, but accepted state remains H1/M3/R3 with no accepted closed obligation.",
    "The checked Gaussian-regularization, tightness, and Prokhorov route differs from the frozen C1-C5 Riesz-Markov architecture; M1021-T2 lacks its required composition certificate.",
    "The frozen anchor audit says no external candidate was found, so the later vendored discovery requires append-only provenance and architecture reconciliation.",
    "The source crosswalk is H1 only, no required readable obligation has accepted independent R0 review, and AUDIT-Z is not accepted.",
    "Complete accepted foundation, transitive declaration/source provenance, TCB, SBOM, license, offline restoration, deterministic bundle, protected CI, and independent verification evidence is absent.",
    "The current narrow replay reuses the automation-provided shared warm .lake symlink and is not release-grade cold evidence.",
    "README.md still describes the pre-proof boundary, so the public projection is stale relative to provisional proof and validation evidence.",
]


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate JSON key in {path}: {key}"
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
    )
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 900, check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).stdout.strip()


def elan_binary(name: str) -> Path:
    env = dict(os.environ)
    env["ELAN_TOOLCHAIN"] = LEAN_TOOLCHAIN
    result = run(["elan", "which", name], cwd=LEAN_ROOT, env=env, timeout=30)
    path = Path(result.stdout.strip())
    assert path.is_file(), path
    return path


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    if match is None:
        assert f"'{declaration}' does not depend on any axioms" in output
        return set()
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    assert not sys.flags.optimize, "Python assertions must remain enabled"
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor_audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    decision = load(HERE / "release-decision.json")
    spec = load(HERE / "release-spec.json")
    receipt = load(HERE / "release-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")

    for relative, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, relative
    for relative, expected in TOOL_INPUTS.items():
        assert sha256(ROOT / relative) == expected, relative
    for relative, expected in RECONCILED_INPUTS.items():
        assert sha256(HERE / relative) == expected, relative
    assert decision["reconciled_inputs"] == RECONCILED_INPUTS

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 497 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 497,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1021-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1021-VALIDATION"
    )
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    assert intake["lifecycle_mode"] == "planned"
    assert intake["root_vector"] == {
        "human": "H1", "machine": "M3", "readability": "R3",
    }
    assert intake["theorem_complete"] is False
    assert statement["elaborated_print_sha256"] == EXPRESSION_SHA256
    assert anchor["exact_candidate_found"] is anchor["external_candidate_found"] is False
    assert registry["root_obligation_id"] == "M1021-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert {row["obligation_id"] for row in graphs["nodes"]} == set(INVENTORY_IDS)
    assert graphs["registry_sha256"] == DENOMINATOR_SHA256
    assert graphs["closure_boundary"] == {
        "closed_obligations": [], "root_machine_debt": "M3",
        "remaining_root_cut_set": ["M1021-BR", "M1021-C"],
        "proof_claimed": False, "theorem_complete": False,
    }

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["result"]["root_kernel_closed"] is True
    assert proof["result"]["frozen_graph_closed"] is False
    assert proof["result"]["theorem_complete"] is False
    assert validation["receipt_id"] == decision["dependency"]["receipt_id"]
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert validation["result"]["observed_axioms"] == EXPECTED_AXIOM_LIST
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["accepted_closed_obligation_ids"] == []

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is dependency["release_grade"] is False
    assert dependency["master_accepted"] is False
    terminal = decision["decision"]
    assert terminal["verdict"] == "blocked"
    assert terminal["lifecycle_before"] == terminal["lifecycle_after"] == "planned"
    assert terminal["root_vector_before"] == terminal["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R3",
    }
    assert terminal["audit_complete"] is terminal["theorem_complete"] is False
    assert terminal["release_accepted"] is False and terminal["accepted_receipt_ids"] == []
    assert terminal["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert terminal["first_failed_gate_detail"] == (
        "dependency.S56-M-1021-VALIDATION.master_acceptance"
    )
    assert terminal["first_failed_release_specific_gate"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    assert terminal["authoritative_graph_remaining_root_cut_set"] == [
        "M1021-BR", "M1021-C",
    ]
    assert decision["accepted_receipt_ids"] == []
    assert decision["known_failures"] == KNOWN_FAILURES
    assert decision["authority_reconciliation"]["reconciled"] is False
    for key in (
        "validation_dependency_master_accepted",
        "frozen_route_and_composition_reconciled",
        "late_external_discovery_reconciled",
        "authoritative_public_projection_reconciled",
        "audit_inventory_reconciled", "human_source_h0_accepted",
        "readability_r0_accepted", "accepted_foundation_profile",
        "complete_transitive_provenance_and_tcb", "immutable_clean_release_input",
        "cold_empty_cache_offline_replay", "complete_sbom_license_and_offline_archive",
        "deterministic_content_addressed_release_bundle",
        "two_distinct_signed_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_required_adversarial_gates", "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] is False, key
    assert "No `H0`" in (HERE / "source_statement_crosswalk.md").read_text()
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    assert "No proof is present or claimed." in readme

    assert spec["recipe_id"] == "S56-M-1021-RELEASE-negative-reconciliation-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py",
    ]
    assert spec["timeout_seconds"] == 900 and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert spec["covered_declarations"] == [
        "AwesomeTheorems.Stage1.THM_M_1021.BochnerTarget", *TRUST_DECLARATIONS,
    ]
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib["rev"] == mathlib["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    lean = elan_binary("lean")
    lake = elan_binary("lake")
    tools = {
        "lean": lean, "lake": lake,
        "python": Path(os.path.realpath(sys.executable)),
        "git": Path(os.path.realpath(shutil.which("git") or "")),
        "bash": Path(os.path.realpath(shutil.which("bash") or "")),
        "bubblewrap": Path(os.path.realpath(shutil.which("bwrap") or "")),
        "elan": Path(os.path.realpath(shutil.which("elan") or "")),
    }
    assert {name: sha256(path) for name, path in tools.items()} == EXPECTED_TOOLS
    assert "4.29.0" in run([str(lean), "--version"], cwd=LEAN_ROOT).stdout
    assert LEAN_COMMIT in run([str(lean), "--version"], cwd=LEAN_ROOT).stdout

    replay = run(["bash", str(HERE / "check_validation.sh")], timeout=900).stdout
    assert replay.count("Declarations are sorry-free!") == len(TRUST_DECLARATIONS)
    assert "declaration uses 'sorry'" not in replay
    assert "sorryAx" not in replay and "error:" not in replay
    for declaration in TRUST_DECLARATIONS:
        assert observed_axioms(replay, declaration) == EXPECTED_AXIOMS

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["master_accepted"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["verdict"] == "blocked" and receipt["accepted_receipt_ids"] == []
    assert receipt["recipe"] == spec
    assert receipt["known_failures"] == KNOWN_FAILURES
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["result"]["observed_axioms"] == EXPECTED_AXIOM_LIST
    assert receipt["result"]["kernel_output_sha256"] == hashlib.sha256(
        replay.encode()
    ).hexdigest()
    for relative, expected in receipt["input_bindings"].items():
        assert sha256(ROOT / relative) == expected, relative

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == KNOWN_FAILURES
    assert packet["output_summary"] == list(SUMMARY_LINES)

    status = git(
        "status", "--porcelain=v1", "--untracked-files=all", "--",
        str(HERE), str(ROOT / ".stage1-worker-selftest.json"),
    )
    actual_changes = {
        line[3:] if line[:2] == "??" else line[2:].lstrip()
        for line in status.splitlines()
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    for relative in (
        f"Stage1_Instances/{THEOREM}/release-decision.json",
        f"Stage1_Instances/{THEOREM}/release-receipt.json",
        f"Stage1_Instances/{THEOREM}/release-phase.md",
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "/home/" not in text and ".cron/" not in text
        assert "theorem_complete=true" not in text

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
