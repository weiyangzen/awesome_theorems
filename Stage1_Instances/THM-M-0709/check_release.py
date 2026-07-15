#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0709-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0709"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = (LEAN_ROOT / ".lake/packages/mathlib").resolve()
ITEM = "S56-M-0709-RELEASE"
THEOREM = "THM-M-0709"
BASE_REVISION = "ab6974ae3bcabe677e7138ff057a7c005aac12d4"
BASE_TREE = "c640af240d44f02c83a29dfa2f985f601a0dfcc2"
VALIDATION_BASE = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
TOOLCHAIN = "leanprover/lean4:v4.29.0"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
EXPRESSION_SHA256 = "5d375802e054a1c87b9fe6c8c24b728e9bcf8bfa20025ebe987d461545926d03"
DENOMINATOR_SHA256 = "f3731049c66ed6cf5e4687115b723249d54dae577f83859e130b76911f519b38"
ACCEPTED_VECTOR = {"H": "H1", "M": "M4", "R": "R3"}
PROVISIONAL_VECTOR = {"H": "H1", "M": "M3", "R": "R3"}
PROVISIONAL_ROOT_CUT = [
    "M0709-C-MACHINE",
    "M0709-C-MPCP",
    "M0709-T-MPCP-PCP",
    "M0709-N-BINARY",
    "M0709-T-REDUCTION",
]
ACCEPTED_FIRST_OPEN_CUT = [
    "M0709-N-HALTING",
    "M0709-C-MACHINE",
    "M0709-C-MPCP",
    "M0709-X-SOURCE",
    "M0709-X-FOUNDATION",
]
EXPECTED_INPUTS = {
    "README.md": "b3b7882e0e8dd780462293ad2668a08f5e10c2d722b480c94a361d8b38734b32",
    "instance.json": "7e132cf93df7f73f6b3ae2ad3e72bda8e7365a2b94b9cf8b0a20629ca6daf300",
    "task-dag.json": "5f2f26c0e3df6fa998d8caba0d7d95de5067d95a57c66f6081f3c052c06de3c0",
    "source-statement-crosswalk.md": "35ca7ab5ed12607c902955fa52eb376d05fdcc962cfaa8f2d3d10a49e125a6fb",
    "Statement.lean": "354a0a291b2c304451ad1e22157ba233ce18730c792a09d9d339b7df3ab29121",
    "statement.json": "0552d73a85d26e55d9db6d2493bb34954f56b6c51475928f5aa13db3fe0dfe7d",
    "anchor-audit.json": "ea7cbf9af3afb94ef90f55b75ce4307ebbcc64288d9c5d7e5b8ca762db4f2b05",
    "ObligationTree.lean": "0b6806c0a66432d88c3c0ca0ed918304e4bdee8033bd3efa242b71ba5d7ddce2",
    "obligation-registry.json": "c1416c5954697319b053d0e5b416ce3caad3cb3650b537a4bfe7005e143d56db",
    "typed-graphs.json": "178ef0452526de4e9f078a3b3a6aa88e5e7b88b36f33ad74a58b97d08eebea93",
    "Proof.lean": "0dc9bc3950f59ba31380934472b8a464124dfca8c89aeb56376b0bd1a9335744",
    "proof-receipt.json": "bca9c6b2399530404223006ff727f5f729bec3e39ca0ecc447e1a54d921a9b35",
    "proof-blocker.json": "8121066819e46b9f5659df2e6117de1e828c6710d4ed7024f8131a489a65e6f1",
    "Validation.lean": "f36a8265fab01a346a8645f6f8b8ce9562a1665760f0faa5a5f49bc5d0b7f668",
    "validation-receipt.json": "2ac6b84869b42db3d119db8ee8ac7df7609bacc1d92453a5e3f46b473f670728",
    "validation-spec.json": "aa6598093e7510bda2fc0f1784c97365385a459eda8fff77a8245a3943b5e6e9",
    "check_validation.py": "25a3dabaf08748be2e3e154c892c7eedad953355e2ddc591255301ee6f4a8d42",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Blueprint_rev-5.6.md": "b53ed32bbe850156ea6c474d28f3f2f701c898f80cccd3bad5e27ad0107c8986",
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "94b815ed7c260a4e0e71af994e09f6780a5618fd119628cdcae973bd33852330",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_OUTPUT_NAMES = (
    "release-spec.json",
    "release-decision.json",
    "release-phase.md",
    "check_release.py",
)
EXPECTED_RELEASE_OUTPUTS: dict[str, str] = {}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    *(f"Stage1_Instances/{THEOREM}/{name}" for name in RELEASE_OUTPUT_NAMES),
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
}
SUMMARY_LINES = [
    "PASS release reconciliation: target, DAG, receipts, registry, graphs, and hashes agree",
    "PASS narrow Lean replay: exact frozen statement elaborated with lake env lean at trust zero",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and not master accepted",
    "OPEN exact root: accepted H1/M4/R3 unchanged; provisional H1/M3/R3 reduction cut remains open",
    "BLOCKED AUDIT-Z: source/readability and accepted authority reconciliation are incomplete",
    "BLOCKED THEOREM-Z: root, trust, hermetic, independent, bundle, and master gates are open",
    "verdict=blocked audit_complete=false theorem_complete=false accepted_receipts=0",
]


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
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None,
    timeout: int = 600, check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).stdout.strip()


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def source_without_comments(source: str) -> str:
    output: list[str] = []
    index = 0
    depth = 0
    while index < len(source):
        if depth == 0 and source.startswith("--", index):
            newline = source.find("\n", index)
            if newline < 0:
                break
            output.append("\n")
            index = newline + 1
        elif source.startswith("/-", index):
            depth += 1
            index += 2
        elif depth and source.startswith("-/", index):
            depth -= 1
            index += 2
        elif depth:
            if source[index] == "\n":
                output.append("\n")
            index += 1
        else:
            output.append(source[index])
            index += 1
    assert depth == 0, "unterminated Lean block comment"
    return "".join(output)


def narrow_lake_env_lean_replay() -> str:
    assert (LEAN_ROOT / ".lake").is_symlink(), "automation .lake symlink is missing"
    assert MATHLIB.is_dir(), "pinned mathlib checkout is missing"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""

    package_names = (
        "Cli", "batteries", "Qq", "aesop", "proofwidgets", "importGraph",
        "LeanSearchClient", "plausible", "checkdecls", "mathlib",
    )
    compiled_roots: list[Path] = []
    for name in package_names:
        path = (LEAN_ROOT / ".lake/packages" / name).resolve() / ".lake/build/lib/lean"
        if path.is_dir():
            compiled_roots.append(path)
    assert (MATHLIB / ".lake/build/lib/lean") in compiled_roots
    assert all("flt-regular" not in str(path) for path in compiled_roots)

    fixed_env = os.environ.copy()
    fixed_env.update({
        "ELAN_TOOLCHAIN": TOOLCHAIN,
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
        "LEAN_PATH": os.pathsep.join(str(path) for path in compiled_roots),
    })
    version = run(["lake", "env", "lean", "--version"], cwd=MATHLIB, env=fixed_env).stdout
    assert LEAN_COMMIT in version
    output = run(
        ["lake", "env", "lean", "--trust=0", str(HERE / "Statement.lean")],
        cwd=MATHLIB, env=fixed_env,
    ).stdout
    assert "Stage1Instances.THM_M_0709.PostCorrespondenceUndecidable : Prop" in output
    assert "ComputablePred HasSolution" in output
    assert "error:" not in output and "sorryAx" not in output
    return hashlib.sha256(output.encode()).hexdigest()


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    statement = load(HERE / "statement.json")
    instance = load(HERE / "instance.json")
    task_dag = load(HERE / "task-dag.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target == {
        "execution_rank": 750,
        "legacy_priority_slot": None,
        "theorem_id": THEOREM,
        "name": "Post对应问题",
        "category": "数理逻辑 / 证明论",
        "source_status_untrusted": "已验证",
        "baseline": "L0",
        "rework_required": True,
        "legacy_artifacts_accepted": False,
        "target_lane": "hard_statement_first_partial_verification",
        "intake_score": 124,
        "lifecycle_mode": "planned",
        "theorem_complete": False,
    }
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 750,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0709-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0709-VALIDATION"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale release input: {name}"
    for name, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"stale authority input: {name}"
    for name, expected in EXPECTED_RELEASE_OUTPUTS.items():
        assert sha256(HERE / name) == expected, f"stale release output: {name}"

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert statement["canonical_formal_target"]["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0709-ROOT"
    assert len(registry["obligations"]) == len(graphs["nodes"]) == 18
    root = next(node for node in graphs["nodes"] if node["obligation_id"] == "M0709-ROOT")
    assert {"H": root["human_debt"], "M": root["machine_debt"], "R": root["readability_debt"]} == PROVISIONAL_VECTOR
    assert graphs["closure_boundary"] == {
        "root_closed": False,
        "root_machine_classification": "M3",
        "theorem_complete": False,
        "first_open_cut": ACCEPTED_FIRST_OPEN_CUT,
    }
    assert all(node["evidence_ids"] == [] for node in graphs["nodes"])
    assert instance["lifecycle"] == "planned"
    assert instance["root_vector"] == ACCEPTED_VECTOR
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert instance["accepted_proof_state"] == []
    assert task_dag["accepted_states"] == []
    assert all(task["state"] == "open" for task in task_dag["tasks"])

    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["item_id"] == predecessor["id"]
    assert validation["receipt_id"] == decision["dependency"]["receipt_id"]
    assert sha256(HERE / "validation-receipt.json") == decision["dependency"]["receipt_sha256"]
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["accepted_receipt_ids"] == []
    validation_result = validation["result"]
    assert validation_result["accepted_closed_obligation_ids"] == []
    assert validation_result["root_kernel_closed"] is False
    assert validation_result["proof_phase_open_root_cut_set"] == PROVISIONAL_ROOT_CUT
    assert validation_result["complete_trust_provenance_gate"] == "fail_closed"
    assert validation_result["hermetic_release_gate"] == "fail_closed"
    assert validation_result["independent_distinct_runner_gate"] == "fail_closed"
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False
    assert validation["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert proof["accepted"] is False and proof["accepted_closed_obligation_ids"] == []
    assert proof["remaining_root_cut_set"] == PROVISIONAL_ROOT_CUT
    assert blocker["root_closed"] is blocker["theorem_complete"] is False
    assert blocker["remaining_root_cut_set"] == PROVISIONAL_ROOT_CUT

    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["verdict"] == receipt["verdict"] == "blocked"
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert receipt["accepted"] is False and receipt["proposed_state"] == "[_]"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_root_vector_before"] == ACCEPTED_VECTOR
    assert decision["accepted_root_vector_after"] == ACCEPTED_VECTOR
    assert decision["best_provisional_root_vector"] == PROVISIONAL_VECTOR
    assert decision["root_vector_before"] == decision["root_vector_after"] == ACCEPTED_VECTOR
    assert decision["audit_complete"] is decision["theorem_complete"] is False
    assert decision["release_accepted"] is False
    assert decision["terminal_decisions"] == {"audit_z": "blocked", "theorem_z": "blocked"}
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_mathematical_gate"]["gate_id"] == "M0709-C-MACHINE.root_kernel_closure"
    assert decision["remaining_root_cut_set"] == PROVISIONAL_ROOT_CUT
    assert decision["accepted_state_first_open_cut"] == ACCEPTED_FIRST_OPEN_CUT
    reconciliation = decision["evidence_reconciliation"]
    for gate in (
        "dependency_master_accepted", "authoritative_state_reconciled",
        "accepted_root_m0", "exact_root_kernel_closed", "audit_z_accepted",
        "pinpoint_h0_source_review", "independent_r0_review",
        "complete_provenance_foundation_tcb_closure", "immutable_clean_release_input",
        "lake_manifest_package_closure_usable", "hermetic_cold_empty_cache_offline_replay",
        "complete_sbom_license_archive_closure", "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_release_verifier",
        "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle", "master_acceptance",
    ):
        assert reconciliation[gate] is False, gate

    assert spec["argv"] == ["python3", "-I", "-B", str(HERE.relative_to(ROOT) / "check_release.py")]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["dependency"]["receipt_sha256"] == EXPECTED_INPUTS["validation-receipt.json"]
    assert receipt["recipe"]["recipe_id"] == spec["recipe_id"]
    assert receipt["inputs"]["release-decision.json"] == sha256(HERE / "release-decision.json")
    assert receipt["inputs"]["release-spec.json"] == sha256(HERE / "release-spec.json")
    assert receipt["inputs"]["check_release.py"] == sha256(HERE / "check_release.py")
    assert receipt["inputs"]["release-phase.md"] == sha256(HERE / "release-phase.md")
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["result"]["output_summary"] == SUMMARY_LINES
    semantic = hashlib.sha256(("\n".join(SUMMARY_LINES) + "\n").encode()).hexdigest()
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == semantic

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited proof construct in {name}"

    flt = (LEAN_ROOT / ".lake/packages/flt-regular").resolve()
    assert flt.is_dir() and (flt / ".git").is_dir()
    assert run(["git", "rev-parse", "--verify", "HEAD"], cwd=flt, check=False).returncode != 0
    statement_output_sha256 = narrow_lake_env_lean_replay()
    assert receipt["result"]["statement_replay_stdout_sha256"] == statement_output_sha256

    worker = load(ROOT / ".stage1-worker-selftest.json")
    assert set(worker) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert worker["item_id"] == ITEM and worker["state"] == "[_]"
    assert worker["base_revision"] == BASE_REVISION
    assert set(worker["changed_paths"]) == CHANGED_PATHS
    assert worker["output_summary"] == SUMMARY_LINES
    assert worker["known_failures"] == decision["known_failures"]

    actual = set(git("status", "--porcelain=v1", "--untracked-files=all").splitlines())
    expected_status = {f"?? {path}" for path in CHANGED_PATHS}
    expected_status.add("?? Formalizations/Lean/.lake")
    assert actual == expected_status, (actual, expected_status)
    for path in sorted(CHANGED_PATHS):
        assert_text_hygiene(ROOT / path)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
