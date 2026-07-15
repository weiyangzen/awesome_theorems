#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0034-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0034"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0034-RELEASE"
THEOREM = "THM-M-0034"
BASE_REVISION = "38502dd8cfdb1c7b89d62d802952ab596838ec7e"
BASE_TREE = "334fd05726c0b982153d6aec154745629a2c9bc1"
TARGET_EXPRESSION_SHA256 = (
    "d80cc9860ed5a53c81a0851b4dc8e702aa5a23d448f373ae6d68ed0c9b5604b1"
)
REGISTRY_DENOMINATOR_SHA256 = (
    "0f1fd6b2f8450f934acd51372109d93d3b86bfc9ecaac8fe0f58bc566d7fb090"
)
SELECTED_EXTERNAL_REVISION = "e8d85a6f6fa210ba0be12bd02aa22009699f0c35"
CHECKED_EXTERNAL_REVISION = "51ed173b17b274e61f759556ab3e1c090267d1bd"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
GRAPH_CUT = [
    "M0034-X-EXTERNAL-BODY",
    "M0034-X-SOURCE",
    "M0034-S-FOUNDATION",
    "M0034-X-LICENSE",
    "M0034-X-PROVENANCE",
    "M0034-X-TRUST",
    "M0034-X-READABLE",
    "M0034-X-WORKFLOW",
]
EXPECTED_INPUTS = {
    "Statement.lean": "cfdfeabe825f5b7936905cee310c2306dba8b18a4b25281fb09c7d10719b79e8",
    "Proof.lean": "44fd994f47c80f6dc3d6578615cd97c832cfb02badb6c82902c2df11c9d83c83",
    "Validation.lean": "db03ea574fadda2a4b1c3c9d686eebabcba857b1773bc2da7a66d5114fc1ec91",
    "instance.json": "d0cf02b0c2d4061391165ccffa818f7cccd4479cec5065a8edce777881bfb359",
    "task-dag.json": "cbf7bd1b38dfc403fe782905fa7dc7edb6fdd57e1b92c85c3e232a003dd6eb78",
    "obligation-registry.json": "de388aac08659553285062670f11ef3c68d0fa5539c6c575e6e8744fa1a1e133",
    "typed-graphs.json": "fa5cfa00873556291a783b7376d3cb0d949cfc36b4d6a9bcf34e8c96d90e3c0b",
    "proof-receipt.json": "466c2c3818cfb8b1b62ec1e8666f2218fe524d1095502a5b21f436507dbea9ef",
    "validation-receipt.json": "6b5f2504546368558b6eebabafffe29adacaff7c97fcaecec53589f27a1405ae",
    "validation-spec.json": "f3067eed95abedf4e995da13e3bb26a7ad3ea80a27bbad67d110963146b7665b",
    "check_validation.py": "d8b10b234a02049b996faa9405dda21a236807aaa04177f64f21e13470e787f5",
    "check_proof.sh": "6d1cff2873daeaa79483eea5805676a0970ef4c665ee7770a9bd573fa08a2333",
    "vendor-manifest.json": "f2806ec825b0dfe2495f5666a99c5dc906442cd610f33ec6c5743e861910371d",
}
EXPECTED_AUTHORITY = {
    "Docs/Stage1_Blueprint_rev-5.6.md": (
        "a4e106e577354350d267f4a7273b4baf52670f98c7fd094333f5d422c1f30e55"
    ),
    "Docs/Stage1_Execution_DAG_rev-5.6.json": (
        "9861a08cf65fe6aff8c6364a6089774a107d0fd4c0e0c42044588cdf0ceb8d4a"
    ),
    "Docs/Stage1_Targets_rev-5.6.json": (
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
    ),
    "skills/execute-stage1-rev56/SKILL.md": (
        "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8"
    ),
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}
SUMMARY_LINES = [
    "PASS current kernel replay: exact target, vendored PID theorem, and adapter checked at trust zero",
    "PASS reconciliation: accepted authority remains planned H1/M3/R4 with no accepted receipts",
    "FAIL CLOSED dependency and route: validation is unaccepted and registry v1 selects another body",
    "FAIL CLOSED release assurance: H0/R0, cold offline, supply-chain, and independent gates are open",
    "VERDICT blocked: audit_complete=false theorem_complete=false release_accepted=false",
]


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            assert key not in result, f"duplicate key {key!r} in {path}"
            result[key] = value
        return result

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 300) -> str:
    env = os.environ.copy()
    env.update({"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"})
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
    return run(["git", *args], cwd=cwd).strip()


def source_without_comments_and_strings(source: str) -> str:
    output: list[str] = []
    index = 0
    block_depth = 0
    in_string = False
    in_char = False
    escaped = False
    while index < len(source):
        pair = source[index:index + 2]
        char = source[index]
        if block_depth:
            if pair == "/-":
                block_depth += 1
                output.extend("  ")
                index += 2
            elif pair == "-/":
                block_depth -= 1
                output.extend("  ")
                index += 2
            else:
                output.append("\n" if char == "\n" else " ")
                index += 1
        elif in_string or in_char:
            output.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif in_string and char == '"':
                in_string = False
            elif in_char and char == "'":
                in_char = False
            index += 1
        elif pair == "/-":
            block_depth = 1
            output.extend("  ")
            index += 2
        elif pair == "--":
            newline = source.find("\n", index)
            if newline < 0:
                output.extend(" " * (len(source) - index))
                index = len(source)
            else:
                output.extend(" " * (newline - index))
                index = newline
        elif char == '"':
            in_string = True
            output.append(" ")
            index += 1
        elif char == "'" and index + 2 < len(source) and source[index + 2] == "'":
            in_char = True
            output.append(" ")
            index += 1
        else:
            output.append(char)
            index += 1
    assert block_depth == 0 and not in_string and not in_char
    return "".join(output)


def printed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, (declaration, output)
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    spec = load(HERE / "release-spec.json")
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    instance = load(HERE / "instance.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    local_dag = load(HERE / "task-dag.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1078
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0034-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1078,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0034-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    local_release = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_release["state"] == "open"
    assert local_release["depends_on"] == ["S56-M-0034-VALIDATION"]
    assert local_dag["accepted_states"] == []

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    for name, expected in EXPECTED_AUTHORITY.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    assert receipt["reconciled_inputs"] == EXPECTED_INPUTS
    assert receipt["authority_inputs"] == EXPECTED_AUTHORITY
    release_bindings = receipt["release_artifact_bindings"]
    assert set(release_bindings) == {
        "release-spec.json", "release-decision.json", "check_release.py",
        "release-validation.md",
    }
    for name, expected in release_bindings.items():
        assert sha256(HERE / name) == expected, f"release artifact drifted: {name}"

    recipe = spec["recipe"]
    expected_argv = [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["schema_version"] == "stage1-release-spec/1.0"
    assert spec["item_id"] == decision["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == decision["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert recipe["argv"] == expected_argv
    assert recipe["cwd"] == "." and recipe["network_policy"] == "denied"
    assert recipe["timeout_seconds"] == 300 and recipe["expected_exit"] == 0
    inventory = registry["frozen_denominators"]["inventory"]
    assert recipe["covered_obligation_ids"] == inventory
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
    ):
        assert receipt["recipe"][key] == recipe[key]

    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["decision_id"] == receipt["decision_id"]
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["decision_support"] == receipt["support_state"]
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert receipt["accepted"] is receipt["master_accepted"] is False
    assert receipt["release_accepted"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["verdict"] == decision["verdict"] == "blocked"
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert decision["accepted_closed_obligation_ids"] == []
    assert receipt["accepted_closed_obligation_ids"] == []

    dependency = decision["dependency"]
    receipt_dependency = receipt["dependency"]
    assert dependency["item_id"] == validation["item_id"] == "S56-M-0034-VALIDATION"
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == sha256(HERE / "validation-receipt.json")
    for key in (
        "receipt_id", "receipt_sha256", "support_state", "accepted", "release_grade",
        "master_accepted", "verdict", "validation_phase_complete",
    ):
        assert receipt_dependency[key] == dependency[key], key
    assert validation["support_state"] == "provisional_worker_selftest_blocked"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["result"]["validation_phase_complete"] is False
    assert validation["result"]["accepted_closed_obligation_ids"] == []
    assert validation["result"]["frozen_graph_root_closed"] is False
    assert validation["result"]["frozen_graph_machine_debt"] == "M3"

    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == VECTOR
    assert instance["accepted_receipt_ids"] == instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    formal = statement["canonical_formal_target"]
    assert formal["elaborated_expression_sha256"] == TARGET_EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["denominator_sha256"] == REGISTRY_DENOMINATOR_SHA256
    assert registry["selected_external_revision"] == SELECTED_EXTERNAL_REVISION
    assert registry["append_only_delta"] == []
    assert registry["proof_body_aliases"]["mbkybky.QuillenSuslin.quillenSuslin"] == (
        "alternative_body_no_selected_credit"
    )
    alternate = next(
        row for row in registry["obligations"]
        if row["obligation_id"] == "M0034-X-ALT-PID"
    )
    assert alternate["machine_eligibility"] == "informational"
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == GRAPH_CUT

    assert proof["accepted"] is False and proof["proposed_state"] == "[_]"
    assert proof["result"]["root_kernel_inhabitant_observed"] is True
    assert proof["result"]["frozen_graph_closed"] is False
    assert proof["accepted_closed_obligation_ids"] == []
    pending = proof["graph_reconciliation_pending"]
    assert pending["required"] is True
    assert pending["frozen_selected_revision"] == SELECTED_EXTERNAL_REVISION
    assert pending["observed_alternate_revision"] == CHECKED_EXTERNAL_REVISION

    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector_before"] == decision["root_vector_after"] == VECTOR
    assert decision["audit_z"] == decision["theorem_z"] == "blocked"
    assert decision["audit_complete"] is decision["theorem_complete"] is False
    assert decision["release_accepted"] is False
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    )
    assert decision["first_failed_reproduction_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    assert decision["authoritative_graph_remaining_root_cut_set"] == GRAPH_CUT
    assert decision["known_failures"] == receipt["known_failures"]
    assert decision["retry_condition"] == receipt["retry_condition"]
    reconciliation = decision["evidence_reconciliation"]
    for key in (
        "authoritative_graph_reconciled", "accepted_exact_root_kernel_closure",
        "pinpoint_h0_review", "independent_r0_review", "audit_z_accepted",
        "complete_foundation_provenance_tcb_closure", "immutable_clean_release_input",
        "hermetic_cold_offline_replay", "sbom_license_archive_closure",
        "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_verifier", "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle", "master_acceptance",
    ):
        assert reconciliation[key] is False, key

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)[ \t]+",
        re.MULTILINE,
    )
    lean_sources = [
        HERE / "Statement.lean", HERE / "ObligationTree.lean", HERE / "Proof.lean",
        HERE / "ProofAudit.lean", HERE / "Validation.lean",
        *sorted((HERE / "Vendor").rglob("*.lean")),
    ]
    for path in lean_sources:
        source = source_without_comments_and_strings(path.read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {path}"

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()).resolve()
    assert sha256(lean) == LEAN_SHA256
    lean_version = run([str(lean), "--version"])
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version

    proof_output = run(["bash", str(HERE / "check_proof.sh")], timeout=300)
    assert proof_output == (
        "PASS THM-M-0034 isolated proof elaboration "
        "(8 vendored modules, --trust=0 -t0)\n"
    )
    proof_audit = (HERE / "ProofAudit.lean").read_text(encoding="utf-8")
    assert "assert_no_sorry quillenSuslin" in proof_audit
    assert "assert_no_sorry Stage1Instances.THM_M_0034.quillenSuslinTarget" in proof_audit
    assert EXPECTED_AXIOMS == set(proof["validation_action"]["observed_axioms"])

    packet_keys = {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert set(packet) == packet_keys
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == decision["known_failures"]
    assert "verdict=blocked" in packet["output_summary"].lower()
    assert "audit_complete=false" in packet["output_summary"].lower()
    assert "theorem_complete=false" in packet["output_summary"].lower()

    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
        and not line[3:].startswith("Formalizations/Lean/.lake/")
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    assert receipt["changed_paths"] == sorted(CHANGED_PATHS)
    expected_output = ("\n".join(SUMMARY_LINES) + "\n").encode("utf-8")
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == digest(expected_output)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "**`blocked`**", "`[H1, M3, R4]`", "`audit_complete=false`",
        "`theorem_complete=false`", "`AUDIT-Z`", "`THEOREM-Z`",
        "This worker accepts\nno receipt",
    ):
        assert fragment in handoff, fragment

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
