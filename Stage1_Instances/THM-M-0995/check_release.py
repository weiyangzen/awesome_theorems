#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0995-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0995"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0995-RELEASE"
THEOREM = "THM-M-0995"
BASE_REVISION = "4d2c77230343716176b4192dc38e26f4c20c7547"
BASE_TREE = "9eebdfdfda6b289fea0b6e778fae8e13327395b2"
VALIDATION_BASE = "92246ea92c0c44282c05728798bc7c7e4a5a1464"
EXPRESSION_SHA256 = "0201bd579e5b8f490d8079891aec8d7e8b4d69c1534a18a9e6bc77e464faafa2"
DENOMINATOR_SHA256 = "29fa162b68c22ecc1c0b1edb83306a411eb8ddea7a4b546fbeb082270a425b18"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_REPLAY_SHA256 = "c9dd937b380fd9701391a2616452af6278026a9bf7a4a8d1c23ddcdb4a695454"
EXPECTED_REPLAY_BYTES = 10899
EXPECTED_INPUTS = {
    "Statement.lean": "b50beed65dc1cd10f656024aa09085458e94233b0ac9baedec4c0c9ad31856c4",
    "ObligationTree.lean": "e58b7449e67e34bd17d73c7c586865815eb818fcf8527d11d4f861aa04636de2",
    "Proof.lean": "cfd897575f18ac24487454973d704adc1a2a28b3d7d08f9c564dceabb74b35bf",
    "Validation.lean": "3d98335d8e126547900a7c4277ec8a59895ae39c7eb407d85558b9676365e4d7",
    "intake.json": "9edb86ac0887c1cedd404df5d8b225c4e475df092adaaea3df2df9e138f22aa6",
    "statement.json": "33903f9a1be5ef4708e3502d1b14089f17fe2914088bc8701c9b8479f2696c7d",
    "anchor-audit.json": "2d537d4b61da85531850fdc3c3feb749d6202414abb7685caf610b522cd50c5c",
    "obligation-registry.json": "75257ea402dd35de1806255af02bbcd76cd9e542faf95832ca424f3ec4a1dfc0",
    "typed-graphs.json": "9cb8a3570b7ef7be64a66f1398ec6edb295e963c17abc2ca4544ab90c5c1b3c3",
    "proof-receipt.json": "386a3891cb8c474eebe71971ffbccef7ece1b6dee6b5c9f620cbdfdaba92e3e7",
    "validation-spec.json": "f02f8269615fd7e22509bd9a861a575620de48ff35b18f2ad0cd1c7626da1c15",
    "validation-receipt.json": "e56bb32883699ec28366e7442e07d067eb89e81eb06d77d12f6f015c63ffdbba",
    "check_validation.py": "910bff7fc2334b84461c35408112832dd1411f1a1ddbaeacae166a4f7f2ce437",
    "check_validation.sh": "2f528954f5e808906cfae5c5d42939e8338bc94141cf133d6fa4800952dc805c",
    "validation-phase.md": "96a73d417f4081e2d2c15ffd07dba84b4646258850afe04ed561356175353997",
}
EXPECTED_AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Blueprint_rev-5.6.md": "8e7ba1bfc4d0c283a989344ff342fe38acc46ac50312f7bf3ba4149af0e4466f",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "d19a89e49de74448ac9cd4f5d6b7ba6f5c1daae03c800c0ff48c530ed683ce1b",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
EXPECTED_TOOL_INPUTS = {
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_INPUTS = {
    "release-decision.json": "2909b869d6e2bd7c321378228a3c7874328bb37fef66f3f08cf273bc7e1e8cb0",
    "release-spec.json": "7a4fc3e77b51db7f72c1918a30ed2a10ec5dfee32676b59ce3d9a8837ad92a69",
    "release-validation.md": "3b23ed436e8e3624a88f356a9ef87e0aaa33352566953f1bdb235268dee68585",
}
INVENTORY_IDS = [
    "M0995-ROOT", "M0995-S-EXACT", "M0995-L-EXP-REMAINDER",
    "M0995-L-IND-MGF", "M0995-T-IND-MGF", "M0995-L-PREFIX-MGF",
    "M0995-L-SUM-MGF", "M0995-T-SUM-MGF", "M0995-L-CHERNOFF",
    "M0995-L-OPTIMIZE-POS", "M0995-L-VAR-ZERO-AE",
    "M0995-B-ZERO-DENOM", "M0995-B-VAR-ZERO", "M0995-T-VAR-ZERO",
    "M0995-B-EMPTY", "M0995-T-ASSEMBLE-V2", "M0995-X-MATHLIB",
    "M0995-X-EXTERNAL", "M0995-X-SOURCE", "M0995-X-TCB",
    "M0995-X-V1-REFUTATION",
]
KERNEL_IDS = [
    "M0995-ROOT", "M0995-S-EXACT", "M0995-L-EXP-REMAINDER",
    "M0995-L-IND-MGF", "M0995-T-IND-MGF", "M0995-L-PREFIX-MGF",
    "M0995-L-SUM-MGF", "M0995-T-SUM-MGF", "M0995-L-CHERNOFF",
    "M0995-L-OPTIMIZE-POS", "M0995-L-VAR-ZERO-AE",
    "M0995-B-ZERO-DENOM", "M0995-B-VAR-ZERO", "M0995-T-VAR-ZERO",
    "M0995-B-EMPTY", "M0995-T-ASSEMBLE-V2", "M0995-X-V1-REFUTATION",
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
    "PASS release inputs: target, DAG, receipts, graph, and content hashes agree",
    "PASS current Lean replay: exact roots and compositions are sorry-free with the recorded axiom profile",
    "PASS fail-closed state: lifecycle planned; accepted root H2/M3/R3; accepted receipts 0",
    "BLOCKED S56-10.2-DEPENDENCY-ACCEPTANCE: validation is provisional and unaccepted",
    "BLOCKED audit, immutable input, cold/offline, trust, source/readability, and independent release gates",
    "verdict=blocked audit_complete=false theorem_complete=false",
)


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> str:
    result = subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=30).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output, re.DOTALL,
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
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 275
    assert target["lifecycle_mode"] == "planned"
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0995-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 275,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0995-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]"

    for name, expected in EXPECTED_AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    assert decision["authority_inputs"] == EXPECTED_AUTHORITY_INPUTS
    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"tool input drifted: {name}"
    for name, expected in RELEASE_INPUTS.items():
        assert sha256(HERE / name) == expected, f"release input drifted: {name}"
        assert receipt["input_bindings"][f"Stage1_Instances/{THEOREM}/{name}"] == expected
    assert receipt["input_bindings"][f"Stage1_Instances/{THEOREM}/check_release.py"] == (
        sha256(HERE / "check_release.py")
    )
    assert receipt["input_bindings"][".stage1-worker-selftest.json"] == (
        sha256(ROOT / ".stage1-worker-selftest.json")
    )

    assert decision["item_id"] == receipt["item_id"] == spec["item_id"] == ITEM
    assert decision["theorem_id"] == receipt["theorem_id"] == spec["theorem_id"] == THEOREM
    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["decision_support"] == receipt["support_state"] == (
        "provisional_worker_selftest"
    )
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert decision["decision_id"] == receipt["decision_id"] == receipt["receipt_id"]
    assert decision["release_recipe_id"] == spec["recipe_id"]

    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0995-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    assert dependency["support_state"] == validation["support_state"]
    assert dependency["accepted"] is validation["accepted"] is False
    assert dependency["release_grade"] is validation["release_grade"] is False
    assert dependency["master_accepted"] is False
    assert receipt["dependency_receipt"]["item_id"] == dependency["item_id"]
    assert receipt["dependency_receipt"]["receipt_id"] == dependency["receipt_id"]
    assert receipt["dependency_receipt"]["support_state"] == dependency["support_state"]
    assert receipt["dependency_receipt"]["accepted"] is False
    assert receipt["dependency_receipt"]["release_grade"] is False
    assert receipt["dependency_receipt"]["receipt_sha256"] == dependency["receipt_sha256"]
    assert receipt["dependency_receipt"]["master_accepted"] is False

    assert decision["provisional_receipt_ids_inspected"] == [
        proof["receipt_id"], validation["receipt_id"]
    ]
    assert validation["base_revision"] == VALIDATION_BASE
    assert validation["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert validation["result"]["audit_complete"] is False
    assert validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == (
        "dependency.S56-M-0995-PROOF.master_acceptance"
    )
    assert validation["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["result"]["root_proof_body_present"] is True
    assert proof["result"]["theorem_complete"] is False

    assert intake["lifecycle_mode"] == "planned"
    assert intake["root_vector"] == {
        "human": "H2", "machine": "M3", "readability": "R3"
    }
    assert intake["theorem_complete"] is False
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0995.StatementShape"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["registry_version"] == graphs["registry_version"] == 2
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    boundary = graphs["closure_boundary"]
    assert boundary["root_closed"] is True
    assert boundary["root_machine_debt"] == "M0-L"
    assert boundary["remaining_root_cut_set"] == []
    assert boundary["audit_complete"] is boundary["theorem_complete"] is False

    result = decision["decision"]
    assert result["verdict"] == receipt["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == [
        "H2", "M3", "R3"
    ]
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert result["first_failed_gate"]["gate_id"] == (
        "S56-10.2-DEPENDENCY-ACCEPTANCE"
    )
    assert result["first_failed_release_specific_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert result["next_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )

    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "accepted_exact_root_kernel_closure", "authoritative_instance_reconciled",
        "audit_z_accepted", "pinpoint_h0_review", "independent_r0_review",
        "complete_provenance_foundation_tcb_closure",
        "immutable_clean_release_input", "hermetic_cold_offline_replay",
        "sbom_license_archive_closure", "independent_clean_runner_attestations",
        "independently_implemented_minimal_verifier",
        "protected_ci_and_mutation_gates", "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert reconciliation[key] is False, key
    assert reconciliation["accepted_closed_obligations"] == []
    assert reconciliation["historical_validation_recipe_replay"] == (
        "stale_outside_original_worker_packet_and_base_revision"
    )
    cut_set = "\n".join(result["remaining_root_cut_set"])
    for fragment in (
        "S56-M-0995-VALIDATION", "H0 primary-source", "R0 node-anchored",
        "AUDIT-Z", "empty-cache network-denied cold build", "SBOM",
        "two signed attestations", "minimal release verifier",
        "deterministic content-addressed release bundle",
    ):
        assert fragment in cut_set, fragment

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 600 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    assert receipt["canonical_obligation_ids"] == INVENTORY_IDS
    assert receipt["kernel_replayed_obligation_ids"] == KERNEL_IDS
    assert receipt["known_failures"] == decision["known_failures"]
    assert set(receipt["changed_paths"]) == set(decision["changed_paths"]) == CHANGED_PATHS
    expected_summary = "\n".join(SUMMARY_LINES) + "\n"
    assert receipt["output_evidence"] == {
        "stdout_semantic_sha256": hashlib.sha256(expected_summary.encode()).hexdigest(),
        "stdout_bytes": len(expected_summary.encode()),
        "expected_line_count": len(SUMMARY_LINES),
        "log_sha256": hashlib.sha256(expected_summary.encode()).hexdigest(),
        "exit_code": 0,
    }
    assert "prevents release-grade timing evidence" in (
        receipt["timing"]["duration_seconds"]
    )

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
    assert not list(HERE.glob("*.olean")) and not list(HERE.glob("tmp*.lean"))

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
    assert len(replay.encode("utf-8")) == EXPECTED_REPLAY_BYTES
    assert hashlib.sha256(replay.encode("utf-8")).hexdigest() == EXPECTED_REPLAY_SHA256
    checked_declarations = (
        "Stage1Instances.THM_M_0995.ObligationTree.individualMGF_compose",
        "Stage1Instances.THM_M_0995.ObligationTree.sumMGF_compose",
        "Stage1Instances.THM_M_0995.ObligationTree.zeroVariance_compose",
        "Stage1Instances.THM_M_0995.ObligationTree.root_compose_v2",
        "Stage1Instances.THM_M_0995.Proof.bernsteinInequality_via_registry_v2",
        "Stage1Instances.THM_M_0995.Proof.bernsteinInequality",
        "Stage1Instances.THM_M_0995.Proof.not_optimizeExponentPackage",
        "Stage1Instances.THM_M_0995.Validation.exactRootViaRegistry",
        "Stage1Instances.THM_M_0995.Validation.exactRootDirect",
        "Stage1Instances.THM_M_0995.Validation.expandedRoot",
    )
    for declaration in checked_declarations:
        assert printed_axioms(replay, declaration) == EXPECTED_AXIOMS, declaration
    assert replay.count("Declarations are sorry-free!") == 3
    assert "PASS axiom profile: 31 reports" in replay
    assert "PASS THM-M-0995 proof hygiene" in replay
    assert "sorryAx" not in replay and "declaration uses 'sorry'" not in replay

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    changed_manifest = "\n".join(
        line for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    ) + "\n"
    assert receipt["environment"]["nonrelease_changed_path_manifest_sha256"] == (
        hashlib.sha256(changed_manifest.encode()).hexdigest()
    )

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H2, M3, R3]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "worker accepts no receipt", "`accepted=false`",
    ):
        assert fragment in handoff, fragment
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert os.environ.get("PYTHONOPTIMIZE", "") in ("", "0")
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
