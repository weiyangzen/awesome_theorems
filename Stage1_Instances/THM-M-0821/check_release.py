#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0821-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0821"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0821-RELEASE"
THEOREM = "THM-M-0821"
BASE_REVISION = "c45f3c7090cb4adf616d45e5414985f956e807b2"
BASE_TREE = "da6f991c07f11e8608ddc090af9356558d64d360"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_REPLAY_SHA256 = (
    "2f60f518d7193b8826f907c7d251fbf7731ca30ad7bdad8439ef1958eb0e05a6"
)
EXPECTED_INPUTS = {
    "Statement.lean": "572f1655ca4d40ce6e1ce1bf6567cee2d640eb54534569d8a8980dff184c0100",
    "ObligationTree.lean": "d223cad2f1f9c9ac3e54a5c423609c4816225276e697dfcdbfab97c8e9bdd00f",
    "Proof.lean": "0f366927737a83b07d7f90e399f5e0c6bc9254604efcad7d39d3c50f1468c444",
    "Validation.lean": "d49f638f7d994303b66bf8311baf062e13742afd120e0989eae18568147d4d28",
    "instance.json": "a01e6ac2e1245ec959c646e44fd2e540a6734458de9ad2dfa2862bbeecc1cc56",
    "task-dag.json": "f50166dce557e46e611c2ddb67bef5eb2da5dafb06e8912cf45f8a992b2bcbed",
    "statement.json": "1bc0d5f7a002649ba47a12dea437a5950e01a95e443ab6468d0c0e4db19b78e2",
    "anchor-audit.json": "050fae06052c03a8556804d2481e089ffb8e5095cd2baaf2b6e42ace5387c682",
    "obligation-registry.json": "16bc89dfe581930beb9d1aadc82e72ac4db3788702d1d6fc52712f6689ea2728",
    "typed-graphs.json": "dab4f84c604468a45db8cdd957e42c2301edfcc0d9fac3b04bb220736a041f77",
    "proof-receipt.json": "42b5b31487cde5fb7b679e9386133709948fc0752e1993fe46af17c498ab56b0",
    "validation-spec.json": "66209bc2d7606ef8071419d37a07142b9074303e2d9d4973962ac9e812e4c37c",
    "validation-receipt.json": "aa575d2751694cd298238d854e87c02df63d8613ac3ad840891fccb3ea0417f5",
    "check_validation.py": "6b6caaa557e2f5aee5a350f7e7bee335f8c12bbe40bd0dd12049662e2d67fed2",
    "check_validation.sh": "a5eaba5132f169fc4211174ac7133ab6aff90082361746062b3230a24b7136b0",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
MACHINE_IDS = [
    "M0821-ROOT",
    "M0821-T-ROOT-COMPOSE",
    "M0821-B-MAXIMUM",
    "M0821-T-ATTAIN",
    "M0821-C-MIDDLE-LAYER",
    "M0821-L-MIDDLE-ANTICHAIN",
    "M0821-C-MIDDLE-SIZED",
    "M0821-L-MIDDLE-CARD",
    "M0821-T-UPPER",
    "M0821-L-SPERNER-UPPER",
]
INVENTORY_IDS = [
    "M0821-ROOT",
    "M0821-S-INTERFACE",
    "M0821-S-BOUNDARY",
    "M0821-S-TRANSPORT",
    "M0821-S-FOUNDATION",
    "M0821-N-LOWER-MIDDLE",
    "M0821-N-NO-OTHER",
    "M0821-B-MAXIMUM",
    "M0821-B-NO-CASES",
    "M0821-C-MIDDLE-LAYER",
    "M0821-C-MIDDLE-SIZED",
    "M0821-L-MIDDLE-ANTICHAIN",
    "M0821-L-MIDDLE-CARD",
    "M0821-L-SPERNER-UPPER",
    "M0821-L-CHOOSE-MIDDLE",
    "M0821-L-LYM-INV",
    "M0821-N-FIBERWISE-SLICES",
    "M0821-L-LYM-CARD",
    "M0821-L-FALLING-ZERO",
    "M0821-C-FALLING",
    "M0821-L-FALLING-TOP",
    "M0821-B-FALLING-INDUCTION",
    "M0821-L-SLICE-SHADOW",
    "M0821-L-DISJOINT-SHADOW",
    "M0821-L-LOCAL-LYM",
    "M0821-L-LOCAL-LYM-MUL",
    "M0821-C-SHADOW",
    "M0821-L-DOUBLE-COUNT",
    "M0821-T-ATTAIN",
    "M0821-T-UPPER",
    "M0821-T-ROOT-COMPOSE",
    "M0821-X-SOURCE",
    "M0821-X-PROVENANCE",
    "M0821-X-TRUST",
    "M0821-X-READABLE",
    "M0821-X-WORKFLOW",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = (
    "PASS release inputs: target, DAG dependency, receipts, graph, and hashes agree",
    "PASS current Lean replay: exact root and differential root are sorry-free with recorded axiom profile",
    "PASS fail-closed state: lifecycle planned; accepted root H1/M3/R4; accepted receipts 0",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted",
    "BLOCKED source/readability, trust, clean cold/offline, and independent release gates",
    "verdict=blocked audit_complete=false theorem_complete=false",
)


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 180) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, declaration
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions (no -O/PYTHONOPTIMIZE)")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    graphs = load(HERE / "typed-graphs.json")
    registry = load(HERE / "obligation-registry.json")
    local_dag = load(HERE / "task-dag.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1379
    assert target["lifecycle_mode"] == "planned"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0821-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1379,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0821-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]"
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-0821-VALIDATION"]

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS

    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["execution_rank"] == 1379 and decision["intent"] == "release"
    assert decision["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == BASE_TREE
    assert decision["decision_support"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]"
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0821-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert decision["release_recipe_id"] == spec["recipe_id"]
    assert decision["node_receipt_id"] == receipt["receipt_id"]
    assert decision["provisional_receipt_ids_inspected"] == [
        proof["receipt_id"], validation["receipt_id"]
    ]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 180 and spec["network_policy"] == "denied"
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["depends_on"] == ["S56-M-0821-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["verdict"] == "blocked"
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["kernel_replayed_obligation_ids"] == MACHINE_IDS
    assert receipt["accepted_receipt_ids"] == []
    for name, expected in receipt["input_bindings"].items():
        path = ROOT / name if name.startswith("Stage1_") else LEAN_ROOT / name
        assert sha256(path) == expected, f"receipt input drifted: {name}"
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "expected_exit",
    ):
        assert receipt["recipe"][key] == spec[key], key

    result = decision["decision"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == [
        "H1", "M3", "R4"
    ]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    receipt_result = receipt["result"]
    assert receipt_result["verdict"] == "blocked"
    assert receipt_result["root_vector_before"] == receipt_result["root_vector_after"] == [
        "H1", "M3", "R4"
    ]
    assert receipt_result["audit_complete"] is receipt_result["theorem_complete"] is False
    assert receipt_result["accepted_receipt_ids"] == []
    assert receipt_result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt_result["next_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": (
            "c1c56e4aa558581c44e2eac58b9a1a975212636424d1d1cfa099ad63c82929b2"
        ),
        "expected_line_count": 6,
        "exit_code": 0,
    }
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["changed_paths"] == decision["changed_paths"]

    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is False
    assert boundary["accepted_root_machine_debt"] == "M3"
    assert boundary["closed_obligations"] == []
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert len(graphs["unverified_decomposition_plans"]) == 8

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["root_evidence"]["root_kernel_declaration_closed"] is True
    assert proof["root_evidence"]["accepted_root_closed"] is False
    assert proof["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    validation_result = validation["result"]
    assert validation_result["exact_root_kernel_replay"] == "provisional_pass"
    assert validation_result["accepted_root_machine_debt"] == "M3"
    assert validation_result["accepted_root_closed"] is False
    assert validation_result["unverified_internal_composition_count"] == 8
    assert validation_result["hermetic_cold_offline_replay"] == "fail_closed"
    assert validation_result["independent_distinct_runner"] == "fail_closed"
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False

    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "accepted_exact_root_kernel_closure",
        "authoritative_graph_reconciled",
        "audit_z_accepted",
        "pinpoint_h0_review",
        "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input",
        "hermetic_cold_offline_replay",
        "sbom_license_archive_closure",
        "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_mutation_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["accepted_closed_obligations"] == []
    assert reconciliation["internal_composition_certificates_missing"] == 8
    cut_set = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "S56-M-0821-VALIDATION",
        "eight internal LYM",
        "H0 primary-source",
        "R0 node-anchored",
        "AUDIT-Z",
        "empty-cache network-denied cold build",
        "two signed attestations",
        "minimal release verifier",
        "deterministic content-addressed release bundle",
    ):
        assert fragment in cut_set, fragment

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert shutil.which("bwrap") is not None
    replay = run(["bash", str(HERE / "check_validation.sh")])
    assert hashlib.sha256(replay.encode("utf-8")).hexdigest() == EXPECTED_REPLAY_SHA256
    proof_declarations = (
        "IsAntichain.sperner",
        "Stage1Instances.THM_M_0821.Proof.middleLayerAttainment",
        "Stage1Instances.THM_M_0821.Proof.universalUpperBound",
        "Stage1Instances.THM_M_0821.Proof.spernerMaximum",
    )
    validation_declarations = (
        "Stage1Instances.THM_M_0821.Validation.independentMiddleLayerAttainment",
        "Stage1Instances.THM_M_0821.Validation.independentlyReconstructedSpernerMaximum",
    )
    for declaration in proof_declarations + validation_declarations:
        assert printed_axioms(replay, declaration) == EXPECTED_AXIOMS, declaration
    assert replay.count("Declarations are sorry-free!") == 8
    assert "sorryAx" not in replay and "declaration uses 'sorry'" not in replay

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(decision["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H1, M3, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "This worker accepts no receipt", "release_grade=false",
    ):
        assert fragment in handoff, fragment
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
