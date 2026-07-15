#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1085-RELEASE."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1085"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
FLT = LEAN_ROOT / ".lake" / "packages" / "flt-regular"
ITEM = "S56-M-1085-RELEASE"
THEOREM = "THM-M-1085"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
VALIDATION_BASE_REVISION = "4ba3f2fd1e609b5958f24e0415eef9300da16924"
VALIDATION_BASE_TREE = "6abc1f64758c17a59dad8c80ac44f238983dc720"
VALIDATION_RECEIPT_SHA256 = (
    "5f3ee75d3161179f1c38ed7047ff01a6bb7787f891d0c1b76d07f94a39d4ea58"
)
EXPRESSION_SHA256 = "2af285ae0bb208a80c325d1b8ba89cd273b83d01b2fef018b13e2feca9d43315"
DENOMINATOR_SHA256 = "c0367c009b2f628b52c7cf782f7785730d0207f7e90ec30afa47c1523a8a4dc4"
FLT_REVISION = "56161b6eb5281fbfe9c38f2bcec0f429ebc11a27"
VECTOR = {"H": "H1", "M": "M4", "R": "R4"}
INVENTORY_IDS = [
    "M1085-ROOT", "M1085-S-DEFINITIONS", "M1085-S-DOMAINS",
    "M1085-S-BOUNDARY", "M1085-S-FOUNDATION", "M1085-N-LAWS",
    "M1085-N-MATRIX", "M1085-C-INTERPOLATION", "M1085-C-SMOOTHER",
    "M1085-L-INTERPOLATION-ID", "M1085-L-MIXED-SIGN",
    "M1085-L-MONOTONE", "M1085-L-LIMIT", "M1085-T-COMPARISON",
    "M1085-T-COMPOSE", "M1085-X-SOURCE", "M1085-X-PROVENANCE",
]
MATHEMATICAL_CUT = [
    "M1085-N-LAWS", "M1085-C-INTERPOLATION",
    "M1085-L-INTERPOLATION-ID", "M1085-L-MIXED-SIGN", "M1085-L-LIMIT",
]
EXPECTED_INPUTS = {
    "README.md": "35d70195e7157fdb9aa3466e00cf58e022dcdddd218184b3398fc7ddd9e96646",
    "instance.json": "d22545c42fd51e6fe26041eb07911b6169c7f428586df53cbd5af4890f313da0",
    "task-dag.json": "6995b7e1899f142b319604fa2632e079428540bf7c9547c789462169d0db7472",
    "Statement.lean": "ac7160af49ed699e13856c10d7a0aba637aaa5f76e30eb1ca943a9cbf3136a9d",
    "AnchorAudit.lean": "07984d6f04ab3c4bb6dc67d0ac29889660e687a14202509d5b712b4b6c7deef8",
    "ObligationTree.lean": "f2d917824b406c3d871d3621d392a78200ff92d58172a96d934ea7e6ee0531b9",
    "LawReduction.lean": "1a5394659dba9d5d1502494a636fdc71b47799322684d72f22cc1de07bfd6f96",
    "Validation.lean": "6aad43cd2e46cb4b63ebabdfe8b0428072a887038118812f145ca7ed800f09d4",
    "source-statement-crosswalk.md": "ad7f36e7c5919590008c8340dd11e54d94c4d3f5fe2b2f217e14e6133fecc56a",
    "statement.json": "12da4e651eafb78d25193163da4a9138d05147d16d2faa9ac6f8215ff1259a1b",
    "anchor-audit.json": "33c82a2973972d046376847e801c23450509df3ff18f44c344e506db421dfe10",
    "obligation-registry.json": "0da7c6b059548a2a6c77db369d025695669c9be1ab452c63e9adf03426d2d355",
    "typed-graphs.json": "6f820c55b712708851b9595abbca0b6f1b5f289a2fc4b7a75abaea9f6f850a78",
    "proof-receipt.json": "c8a3d1875e7d7cd44324931a72fdc88ba3368077e9556848b0449293e4ae7be0",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "validation-spec.json": "4515530a0f53ef6781da33445909400ed8a7cfa70c5b765615ddba2d0c6ffb83",
    "check_validation.py": "72500f69a996002501c65e5d9ef16633205debf66266a05d3670cc5d8630997e",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "0bb2f433832fe71156aa46c0828102ec3fb61a00dec81fae129c2826a59f63ca",
    "Docs/Stage1_Blueprint_rev-5.6.md": "c09f9f713bdbc820559e41e1e1840423d60cc2af666aeaf5f3c88587de77f161",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
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
    "PASS S56-M-1085-RELEASE negative reconciliation",
    "PASS authority and evidence hashes: planned H1/M4/R4 with zero accepted receipts",
    "BLOCKED dependency.S56-M-1085-VALIDATION.master_acceptance",
    "BLOCKED exact root: no LawSlepianTarget proof body is supplied or accepted; five-node cut open",
    "BLOCKED current Lean replay: pinned flt-regular HEAD is unresolvable; no repair attempted",
    "verdict=blocked audit_complete=false theorem_complete=false",
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


def run_result(
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 60,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=timeout, check=False,
    )


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 60) -> str:
    result = run_result(argv, cwd=cwd, timeout=timeout)
    assert result.returncode == 0, (
        f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
    )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
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
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data, path
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines()), path


def main() -> None:
    if sys.flags.optimize != 0:
        raise RuntimeError("release checker requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    manifest = load(LEAN_ROOT / "lake-manifest.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert run([
        "git", "merge-base", "--is-ancestor", VALIDATION_BASE_REVISION, BASE_REVISION,
    ]) == ""
    assert git("rev-parse", f"{VALIDATION_BASE_REVISION}^{{tree}}") == VALIDATION_BASE_TREE

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    assert decision["reconciled_inputs"] == EXPECTED_INPUTS
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    assert decision["authority_inputs"] == AUTHORITY_INPUTS

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 527
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    items = {row["id"]: row for row in execution["items"]}
    assert items[ITEM] == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 527,
        "phase": "release", "layer": 6, "state": "[ ]",
        "depends_on": ["S56-M-1085-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    assert items["S56-M-1085-VALIDATION"]["state"] == "[_]"
    assert items["S56-M-1085-VALIDATION"]["attempts"] == 1

    assert instance["lifecycle"] == local_dag["lifecycle"] == "planned"
    assert instance["root_vector"] == VECTOR
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    assert local_dag["accepted_states"] == []
    local_tasks = {row["id"]: row for row in local_dag["tasks"]}
    assert local_tasks[ITEM] == {
        "id": ITEM, "depends_on": ["S56-M-1085-VALIDATION"], "state": "open",
    }
    assert local_tasks["S56-M-1085-VALIDATION"]["state"] == "open"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_1085.SlepianTarget"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["root_obligation_id"] == "M1085-ROOT"
    assert registry["frozen_denominators"]["inventory"] == INVENTORY_IDS
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert all(row["terminal_proof_body_id"] is None for row in registry["obligations"])
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert [row["obligation_id"] for row in graphs["nodes"]] == INVENTORY_IDS
    root = graphs["nodes"][0]
    assert root["obligation_id"] == "M1085-ROOT"
    assert (root["human_debt"], root["machine_debt"], root["readability_debt"]) == (
        "H1", "M4", "R4",
    )
    assert root["evidence_ids"] == []
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == [] and closure["root_closed"] is False
    assert closure["root_machine_debt"] == "M4"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == MATHEMATICAL_CUT
    assert graphs["graphs"]["evidence"]["edges"] == []
    assert anchor["exact_candidates"] == [] and anchor["machine_debt"] == "M4"

    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["provisionally_closed_obligation_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["result"]["root_closed"] is proof["result"]["theorem_complete"] is False
    assert proof["remaining_root_cut_set"] == MATHEMATICAL_CUT

    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["base_revision"] == VALIDATION_BASE_REVISION
    assert validation["base_tree"] == VALIDATION_BASE_TREE
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["accepted"] is validation["release_grade"] is False
    validation_result = validation["result"]
    assert validation_result["root_kernel_closed"] is False
    assert validation_result["accepted_root_closed"] is False
    assert validation_result["remaining_root_cut_set"] == MATHEMATICAL_CUT
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False
    assert validation["first_failed_gate"] == "dependency.S56-M-1085-PROOF.master_acceptance"

    predecessor = (HERE / "check_validation.py").read_text(encoding="utf-8")
    assert f'BASE_REVISION = "{VALIDATION_BASE_REVISION}"' in predecessor
    assert '"state": "[ ]"' in predecessor and '"attempts": 0' in predecessor
    assert 'load(ROOT / ".stage1-worker-selftest.json")' in predecessor

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean",
        "LawReduction.lean", "Validation.lean",
    ):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited construct in {name}"
    law_source = code_without_comments((HERE / "LawReduction.lean").read_text(encoding="utf-8"))
    assert law_source.count("def LawSlepianTarget : Prop") == 1
    assert re.search(r"(?:theorem|def)\s+lawSlepianTarget\b", law_source) is None
    assert law_source.count("(h : LawSlepianTarget") == 1

    flt_entry = next(
        row for row in manifest["packages"]
        if row["name"].strip("\u00ab\u00bb") == "flt-regular"
    )
    assert flt_entry["rev"] == flt_entry["inputRev"] == FLT_REVISION
    assert FLT.is_dir() and (FLT / ".git").is_dir()
    assert (FLT / ".git/HEAD").read_text(encoding="utf-8") == "ref: refs/heads/.invalid\n"
    artifact_probe = run_result(["git", "rev-parse", "--verify", "HEAD"], cwd=FLT)
    assert artifact_probe.returncode == 128
    assert "Needed a single revision" in artifact_probe.stdout
    assert not (FLT / ".git/refs/heads/.invalid").exists()

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["phase"] == decision["intent"] == "release"
    assert decision["verdict"] == "blocked"
    assert decision["release_grade"] is decision["release_accepted"] is False
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == []
    assert decision["accepted_closed_obligation_ids"] == []
    assert decision["root_vector"] == {"before": VECTOR, "after": VECTOR}
    assert decision["terminal_decisions"] == {
        "audit_complete": False, "theorem_complete": False,
        "audit_z": "blocked", "theorem_z": "blocked", "release_accepted": False,
    }
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_gate"]["dependency_gate"] == (
        "dependency.S56-M-1085-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_theorem_gate"]["gate_id"] == "proof.root_kernel_closure"
    assert decision["first_failed_audit_gate"]["gate_id"] == "S56-8.1-H0-R0-RECONCILIATION"
    assert decision["first_failed_reproduction_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert decision["mathematical_root_cut_set"] == MATHEMATICAL_CUT
    assert decision["dependency"]["receipt_id"] == validation["receipt_id"]
    assert decision["dependency"]["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert decision["dependency"]["accepted"] is decision["dependency"]["master_accepted"] is False
    assert decision["artifact_probe"]["manifest_revision"] == FLT_REVISION
    assert decision["artifact_probe"]["head_resolvable"] is False
    assert decision["artifact_probe"]["probe_exit_code"] == 128
    assert decision["artifact_probe"]["lean_replay_attempted_during_release_recipe"] is False
    assert decision["evidence_reconciliation"]["current_lean_replay"] == (
        "not_attempted_pinned_artifact_unusable"
    )

    assert spec["schema_version"] == "stage1-release-recipe/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py",
    ]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 180 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == [] and spec["covered_declarations"] == []
    assert spec["observed_open_state_obligation_ids"] == INVENTORY_IDS
    assert "proof evidence for none" in spec["coverage_semantics"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["depends_on"] == ["S56-M-1085-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["accepted"] is receipt["release_grade"] is receipt["master_accepted"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["decision_id"] == decision["decision_id"]
    assert receipt["decision_sha256"] == sha256(HERE / "release-decision.json")
    assert receipt["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["release_validation_sha256"] == sha256(HERE / "release-validation.md")
    assert receipt["checker_sha256"] == sha256(HERE / "check_release.py")
    assert receipt["verdict"] == "blocked"
    assert receipt["recipe"] == {
        key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
            "covered_obligation_ids", "observed_open_state_obligation_ids",
            "coverage_semantics", "covered_declarations",
        )
    }
    result = receipt["result"]
    assert result["verdict"] == "blocked"
    assert result["lifecycle_before"] == result["lifecycle_after"] == "planned"
    assert result["root_vector_before"] == result["root_vector_after"] == VECTOR
    assert result["accepted_receipt_ids"] == result["accepted_closed_obligation_ids"] == []
    assert result["mathematical_root_cut_set"] == MATHEMATICAL_CUT
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["release_accepted"] is False
    assert result["current_lean_replay"] == "not_attempted_pinned_artifact_unusable"
    receipt_probe = receipt["artifact_probe"]
    assert receipt_probe["manifest_revision"] == FLT_REVISION
    assert receipt_probe["head_contents"] == "ref: refs/heads/.invalid"
    assert receipt_probe["head_resolvable"] is False
    assert receipt_probe["probe_exit_code"] == artifact_probe.returncode
    assert receipt_probe["probe_output"] in artifact_probe.stdout
    assert receipt_probe["pinned_commit_object_present"] is True
    assert receipt_probe["working_tree_materialized"] is False
    assert receipt_probe["release_recipe_lean_replay_attempted"] is False
    commit_object = run_result([
        "git", "cat-file", "-e", f"{FLT_REVISION}^{{commit}}",
    ], cwd=FLT)
    assert commit_object.returncode == 0
    assert not any(path.is_file() for path in FLT.iterdir()), (
        "flt-regular working tree unexpectedly materialized"
    )
    assert receipt["output_summary"] == SUMMARY_LINES
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["known_failures"] == decision["known_failures"]
    assert receipt["changed_paths"] == sorted(CHANGED_PATHS)

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert packet["changed_paths"] == sorted(CHANGED_PATHS)
    assert packet["known_failures"] == decision["known_failures"]
    actual_changed = {
        line[3:] for line in git(
            "status", "--short", "--untracked-files=all", "--",
            str(HERE.relative_to(ROOT)), ".stage1-worker-selftest.json",
        ).splitlines()
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    handoff = (HERE / "release-validation.md").read_text(encoding="utf-8")
    for fragment in (
        "`blocked`", "`[H1, M4, R4]`", "`AUDIT-Z`", "`THEOREM-Z`",
        "This worker accepts no receipt", "could not resolve 'HEAD' to a commit",
    ):
        assert fragment in handoff, fragment
    assert str(ROOT) not in handoff
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
