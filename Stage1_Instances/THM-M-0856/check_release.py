#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-0856-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0856"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0856-RELEASE"
THEOREM = "THM-M-0856"
BASE_REVISION = "b8c0a0c119a82ef435e23f9ff85bfd783db95736"
BASE_TREE = "831576eb7d1273d01e99653d36b616e99e85dc0f"
EXPRESSION_SHA256 = "5364250d1d4e132aaf1d5ce8ad5425369546963189991202f49b2fcf65095bae"
DENOMINATOR_SHA256 = "9d6a920afceb2d2c42ce432e12008329977aa733eecb42c28ed2c44686aca20c"
VALIDATION_RECEIPT_SHA256 = "00b36ca02e98518762e480cf5ceb1beb9952fdc3a33ecbce00c63508482a778e"
PROOF_RECEIPT_SHA256 = "1db25f6c6c46c90a164cc980b8346e7d3fafd4e3c4f5fac4855d489a4b7886f1"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TERMINAL_SOURCE = "Mathlib/Combinatorics/SimpleGraph/Tutte.lean"
TERMINAL_SOURCE_SHA256 = "47072b914aa564222ef8013092c38fa62227fea8230e308cc3eb5f11afcdffc3"
TERMINAL_BODY_SHA256 = "424b3cde58e3407307ef398cd52eeaf2a7ce122fd5049275745c445aceeac132"
TERMINAL_OLEAN_SHA256 = "d0669fb8cd3a48f382490d39a102c7033f7a81e9582d09bda2c2ae172ff399ee"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_OUTPUT_SHA256 = "d68efcd7d6a83b769b857c96179fdf7f9be3d161c438e9f5b251690b06b5ac84"
LEAN_OUTPUT_BYTES = 3006
OBLIGATION_OUTPUT_SHA256 = "b9cc3057c2c410a6a78ce32f9186438e9f34b5358e66e1302f76cb67a2948122"
OBLIGATION_OUTPUT_BYTES = 606
GENERATOR_OUTPUT_SHA256 = "a74785778a5be59739c07e1201664af54c66af4879d5eed4ec48f1aaeec88195"
GENERATOR_OUTPUT_BYTES = 44
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
VECTOR = {"H": "H1", "M": "M3", "R": "R4"}
EVIDENCE_INPUTS = {
    "Statement.lean": "cd7ec3e97a02ccc24578de4431a1a8ebf0e9572f9616b271b67f145d72fbedce",
    "ObligationTree.lean": "752c07615d8402e96dcee57945aa971acca58ba827b1094c534f104ad0bf1c15",
    "Proof.lean": "93ccd4e6dbfe926a21ee0648421bc456dc2f7e2a8cae02b629001a807556938d",
    "Validation.lean": "cd0127cf621f5e8ef922b7a8e04e797f76295d337056a27fd06cade6b33dabb9",
    "instance.json": "3c4a74c095da5ac0d0fa5e071ae960f46fb4a2e4d4f79e5f2d0a5f40ad37cdfd",
    "task-dag.json": "585a5b9781eb0dcfb6e4012f6905f69a9c65e17cbf0a422dc7adef7fce0c68cc",
    "statement.json": "476e6f5d9570153e7a30fc15e9c5487fd1ce02dc7a192dcbf5b01ffc8c7f3fb6",
    "anchor-audit.json": "b95fa97389e8349527c9e0476e4eeb6cbe44e39f1b34fd639dc092929728fcce",
    "obligation-registry.json": "58d63b99f758183dae5aad4ffe7c4b35a1c3e3c54292faa254e2b98b5701c5d6",
    "typed-graphs.json": "ca937f1acd688e122ebdb307fc16e2326add0c51f9d0f169dc018179a7ad54ff",
    "proof-receipt.json": PROOF_RECEIPT_SHA256,
    "validation-spec.json": "aae20f1254cf922b6266960a06bdad8856fe71bb11511e5cd86478e0777d0868",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-phase.md": "86ab3ea5beda4f0b2d2dbc8c0ebc903a24ab3433b5cbf953a46bc43622e329ef",
    "scope-map.md": "51e20ddd50f18e11865199466bd663c15796e45af421ee19f665247ba721c9c9",
    "source-statement-crosswalk.md": "4c0ecbe9266e822de5055cdba9bf9592f489e330fd503073929442c974629d30",
    "check_validation.sh": "197490aad3e762ec8a0e52dff9b25a1c3fd8f93a1fd2830d3fd9d0c327526341",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "89b38a84a11fb9beeb96794ac1affb8fa433c6d1b87ead215658f28f326791f6",
    "Docs/Stage1_Blueprint_rev-5.6.md": "972a2ca9fd6b8e283aeb923875c2e14960706f936605a48868b321a11f94e1c4",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
}
TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_INPUTS = {
    "release-spec.json": "0888478725e5e3d9db0fb2bea5e591f655f43fbbbc09c7c8b4f56dae5bc4ecbd",
    "release-decision.json": "88227fb54cc8a0b800b0c529de0b470cd4b86cf6606bf6be95b02647b9fe735c",
    "release-validation.md": "6cc4facf74cd2bffb1965f87c453843973a5c106e13a29f40d0c11cdd65257ab",
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/check_release.py",
    f"Stage1_Instances/{THEOREM}/release-decision.json",
    f"Stage1_Instances/{THEOREM}/release-receipt.json",
    f"Stage1_Instances/{THEOREM}/release-spec.json",
    f"Stage1_Instances/{THEOREM}/release-validation.md",
}


if not __debug__:
    raise RuntimeError("release checker requires Python assertions")


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


def sha256_lines(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 600) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update({"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC", "LEAN_NUM_THREADS": "1"})
    return subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )


def git(*args: str, cwd: Path = ROOT) -> str:
    completed = run(["/usr/bin/git", *args], cwd=cwd)
    assert completed.returncode == 0, completed.stdout
    return completed.stdout.strip()


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


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def printed_axioms(output: str) -> list[set[str]]:
    reports = re.findall(r"'[^']+' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL)
    return [
        {name.strip() for name in raw.split(",") if name.strip()}
        for raw in reports
    ]


def main() -> None:
    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    tasks = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    for name, expected in EVIDENCE_INPUTS.items():
        assert sha256(HERE / name) == expected, f"evidence input drifted: {name}"
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"
    for name, expected in RELEASE_INPUTS.items():
        assert sha256(HERE / name) == expected, f"release input drifted: {name}"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1410
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0856-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1410,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-0856-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1
    assert validation_item["depends_on"] == ["S56-M-0856-PROOF"]

    assert instance["lifecycle"] == instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == VECTOR
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert tasks["lifecycle"] == "planned" and tasks["accepted_states"] == []
    local_tasks = {row["id"]: row for row in tasks["tasks"]}
    assert local_tasks["S56-M-0856-VALIDATION"]["state"] == "open"
    assert local_tasks[ITEM]["state"] == "open"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0856.TutteOneFactorTarget"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EVIDENCE_INPUTS["Statement.lean"]
    inventory = registry["frozen_denominators"]["inventory"]
    assert len(inventory) == len(registry["obligations"]) == len(graphs["nodes"]) == 56
    assert [row["obligation_id"] for row in registry["obligations"]] == inventory
    assert spec["covered_obligation_ids"] == inventory
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M0856-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert len(registry["frozen_denominators"]["required_machine"]) == 44
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["accepted_closed_obligations"] == []
    assert closure["unverified_internal_decomposition_count"] == 16
    assert len(graphs["unverified_decomposition_plans"]) == 16
    assert len(graphs["composition_certificates"]) == 1
    assert graphs["evidence_objects"] == []

    assert sha256(HERE / "proof-receipt.json") == PROOF_RECEIPT_SHA256
    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is proof["content_addressed"] is False
    assert proof["accepted_receipt_ids"] == []
    root_evidence = proof["root_evidence"]
    assert root_evidence["root_kernel_declaration_closed"] is True
    assert root_evidence["accepted_root_closed"] is False
    assert root_evidence["machine_debt_proposal"] == "M0-W"
    assert root_evidence["unverified_internal_composition_count"] == 16
    assert root_evidence["internal_per_node_composition_credit"] is False
    assert proof["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]

    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["accepted_receipt_ids"] == []
    assert validation["result"]["exact_root_kernel_replay"] == "provisional_pass"
    assert validation["result"]["accepted_root_closed"] is False
    assert validation["result"]["audit_complete"] is validation["result"]["theorem_complete"] is False
    assert validation["first_failed_gate"] == "dependency.S56-M-0856-PROOF.master_acceptance"

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == decision["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == decision["theorem_id"] == THEOREM
    assert spec["recipe_id"] == decision["release_recipe_id"]
    assert spec["argv"] == ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_decisions"] == ["AUDIT-Z", "THEOREM-Z"]
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_declarations", "covered_decisions",
    ):
        assert receipt["recipe"][key] == spec[key], key

    assert decision["base_revision"] == receipt["base_revision"] == BASE_REVISION
    assert decision["base_tree"] == receipt["base_tree"] == BASE_TREE
    assert decision["decision_support"] == receipt["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == receipt["proposed_state"] == "[_]"
    assert decision["release_grade"] is receipt["release_grade"] is False
    assert receipt["accepted"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["master_accepted"] is receipt["release_accepted"] is False
    assert decision["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert decision["dependency"]["master_accepted"] is False
    assert receipt["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert receipt["dependency"]["master_accepted"] is False

    assert decision["verdict"] == receipt["verdict"] == receipt["result"]["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["root_vector_before"] == decision["root_vector_after"] == VECTOR
    assert receipt["result"]["root_vector_before"] == receipt["result"]["root_vector_after"] == VECTOR
    assert decision["audit_complete"] is decision["theorem_complete"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert decision["release_accepted"] is receipt["result"]["release_accepted"] is False
    assert decision["accepted_receipt_ids"] == receipt["accepted_receipt_ids"] == []
    assert decision["first_failed_gate"]["gate_id"] == "dependency.S56-M-0856-VALIDATION.master_acceptance"
    assert decision["first_failed_audit_gate"]["gate_id"] == "AUDIT-Z.inventory_and_evidence_reconciliation"
    assert decision["first_failed_theorem_gate"]["gate_id"] == "THEOREM-Z.requires_accepted_AUDIT-Z"
    assert decision["first_failed_release_gate"]["gate_id"] == "S56-RELEASE-IMMUTABLE-CLEAN-INPUT"
    assert decision["next_failed_release_gate"]["gate_id"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert decision["evidence_reconciliation"]["provisional_machine_debt_proposal"] == "M0-W"
    assert decision["evidence_reconciliation"]["accepted_root_machine_debt"] == "M3"
    assert decision["evidence_reconciliation"]["unverified_internal_composition_count"] == 16
    for key in (
        "audit_inventory_reconciliation", "human_source_h0_acceptance",
        "readability_r0_acceptance", "complete_transitive_provenance_foundation_tcb",
        "immutable_clean_release_input", "hermetic_cold_offline_replay",
        "sbom_license_archive_closure", "two_independent_signed_runner_attestations",
        "independently_implemented_minimal_verifier", "protected_ci_and_adversarial_gates",
        "deterministic_content_addressed_release_bundle", "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key] == "missing", key

    assert decision["reconciled_inputs"] == {
        key: value for key, value in EVIDENCE_INPUTS.items() if key != "check_validation.sh"
    }
    assert decision["authority_inputs"] == AUTHORITY_INPUTS
    assert receipt["evidence_inputs"] == EVIDENCE_INPUTS
    assert receipt["authority_inputs"] == AUTHORITY_INPUTS
    assert receipt["release_artifact_inputs"] == RELEASE_INPUTS
    assert receipt["tool_inputs"]["lean-toolchain"] == TOOL_INPUTS["lean-toolchain"]
    assert receipt["tool_inputs"]["lake-manifest.json"] == TOOL_INPUTS["lake-manifest.json"]

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|run_tac|implemented_by)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        flags=re.MULTILINE,
    )
    for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = source_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, name

    assert MATHLIB.resolve().is_dir()
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    terminal_source = MATHLIB / TERMINAL_SOURCE
    terminal_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/Combinatorics/SimpleGraph/Tutte.olean"
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert sha256_lines(terminal_source, 315, 322) == TERMINAL_BODY_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256

    replay = run(["bash", f"Stage1_Instances/{THEOREM}/check_validation.sh", "--lean-only"])
    assert replay.returncode == 0, replay.stdout
    replay_bytes = replay.stdout.encode("utf-8")
    assert len(replay_bytes) == LEAN_OUTPUT_BYTES
    assert hashlib.sha256(replay_bytes).hexdigest() == LEAN_OUTPUT_SHA256
    reports = printed_axioms(replay.stdout)
    assert len(reports) == 12
    assert all(report == EXPECTED_AXIOMS for report in reports)
    assert replay.stdout.count("Declarations are sorry-free!") == 8
    assert "sorryAx" not in replay.stdout and "declaration uses 'sorry'" not in replay.stdout
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""

    obligation = run(["python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"])
    obligation_bytes = obligation.stdout.encode("utf-8")
    assert obligation.returncode == 1
    assert len(obligation_bytes) == OBLIGATION_OUTPUT_BYTES
    assert hashlib.sha256(obligation_bytes).hexdigest() == OBLIGATION_OUTPUT_SHA256
    assert "frozen_against_execution_dag_sha256" in obligation.stdout
    generator = run([
        "python3", "-B", f"Stage1_Instances/{THEOREM}/build_obligation_artifacts.py", "--check"
    ])
    generator_bytes = generator.stdout.encode("utf-8")
    assert generator.returncode == 1
    assert len(generator_bytes) == GENERATOR_OUTPUT_BYTES
    assert hashlib.sha256(generator_bytes).hexdigest() == GENERATOR_OUTPUT_SHA256
    assert generator.stdout == "generated artifact drift: typed-graphs.json\n"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["commands"] == receipt["commands"]
    assert packet["output_summary"] == receipt["output_summary"]
    assert packet["known_failures"] == receipt["known_failures"]

    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, sorted(actual_changed)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("PASS S56-M-0856-RELEASE negative reconciliation")
    print("verdict=blocked lifecycle=planned root_vector=H1/M3/R4")
    print("warm_exact_root=provisional_M0-W accepted_root=M3")
    print("audit_complete=false theorem_complete=false")
    print("first_failed_gate=dependency.S56-M-0856-VALIDATION.master_acceptance")
    print("release_gates=immutable-clean-input,cold-offline,independent-verifier,bundle")


if __name__ == "__main__":
    main()
