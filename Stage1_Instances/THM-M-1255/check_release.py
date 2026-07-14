#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1255-RELEASE."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1255"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
ITEM = "S56-M-1255-RELEASE"
THEOREM = "THM-M-1255"
BASE_REVISION = "09af5fd5d9b0a28553ca62f9711b940deff167c2"
BASE_TREE = "2355497ef61fd804007dddb1dca29804cd340c84"
VALIDATION_BASE_REVISION = "bad90e2e2479d376609447202eb4f437789d0d11"
VALIDATION_RECEIPT_SHA256 = (
    "e82bbab6fe20ef07b6bbb04b2825f83dee68f13ddbd3c85199d0bbceef4cfbe1"
)
STATEMENT_EXPRESSION_SHA256 = (
    "0ea54a511c4baf6d8bfacb7e784833be9ca4faef66bf1c736765465ed65ad3cf"
)
DENOMINATOR_SHA256 = (
    "7cbea3ad9b0c61388cb73afed61f64984ca5670e061dc3a966a7d6599411c2c9"
)
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
INVENTORY_IDS = [
    "M1255-ROOT",
    "M1255-S-DEFINITIONS",
    "M1255-L-COMMUTE",
    "M1255-C-ACTION",
    "M1255-N-FOURIER",
    "M1255-L-DIVISION",
    "M1255-C-FUNDSOL",
    "M1255-T-ASSEMBLE",
    "M1255-S-BOUNDARY",
    "M1255-S-FOUNDATION",
    "M1255-X-SOURCE",
    "M1255-X-PROVENANCE",
    "M1255-X-READABLE",
]
FROZEN_CLOSED_IDS = ["M1255-S-DEFINITIONS", "M1255-T-ASSEMBLE"]
FROZEN_CUT = ["M1255-C-ACTION", "M1255-C-FUNDSOL"]
PROVISIONAL_IDS = ["M1255-L-COMMUTE", "M1255-C-ACTION"]
PROPOSED_CUT = ["M1255-C-FUNDSOL"]
PROPOSED_LEAF_CUT = ["M1255-N-FOURIER", "M1255-L-DIVISION"]
UPSTREAM_INPUTS = {
    "Statement.lean": "06e76a02a0781eafc5166ea68721b7dd6095e5f45ef686df425c2f236ab9e94f",
    "ObligationTree.lean": "65399202b8c561581317f0b2b7225a521c690741d864fdd1903e33a54446fceb",
    "Proof.lean": "a7711cc22e3171347fefeff287f55766071d999cf92d6d7f5821744b99502cd3",
    "Validation.lean": "92cbba15d21c4e57ee622d8260cde5e41b2d99519bc2897c25bebd30738379da",
    "intake.json": "2421d8704c1c671c1dd69ca82dc2017d3a21565de1cdd4f0cdea160b8c3c1230",
    "statement.json": "c49c783ae7939e8ff65b50c096febd62dc912111aceebc270e0ea1a169ec3b0e",
    "anchor-audit.json": "c04284cabc3ce0ec458cd8ab2cd38baface183bf8166f54fae60ca1ce1a0b516",
    "obligation-registry.json": "01908384973c7ec7f5471f6bfe60b9c6f4570ea4e655fdb859e74569c6dd9db7",
    "typed-graphs.json": "f01cc5ce57f61acc502b66c3ef95ae354a2b73413b29c86cb0eabbb1537b3c30",
    "proof-receipt.json": "943d241b6b89d2637ae81dc8a6ae5a8b2179a5b69478157631fae3769a0d3b23",
    "validation-spec.json": "4578c24b7d1197f030b8f8b2c234ae8b0ff0d8aa9dc3e9de5638cc5d35ac8d65",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "check_validation.py": "6325d2da1615507b2345e457b7ce807e5423d9d612a17adbb221e20a4d160900",
    "source_statement_crosswalk.md": "695b155070d720d528639e1f49e27edb4221fdccbeaad49dbe3ffd713e72753d",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": (
        "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c"
    ),
    "Docs/Stage1_Execution_DAG_rev-5.6.json": (
        "be8d8a624df43913222d8087606b3a7303723c7888cb0e65a6684727d209fa8d"
    ),
    "Docs/Stage1_Blueprint_rev-5.6.md": (
        "5a5465bb7725c24c4b24d70f622a05717b58900f7daea30790a43f3d03a0afd2"
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
    timeout: int = 600,
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


def reported_axioms(output: str, declaration: str) -> set[str]:
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[(?P<axioms>.*?)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group("axioms").split(",") if part.strip()}


def canonical_replay() -> str:
    """Fresh trust-zero replay of the canonical statement and differential probe."""

    fixed_env = os.environ.copy()
    fixed_env.update(
        {
            "ELAN_TOOLCHAIN": "leanprover/lean4:v4.29.0",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_NUM_THREADS": "1",
        }
    )
    lean = Path(
        run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT, env=fixed_env)
        .stdout.strip()
    )
    lean_path = run(
        ["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT, env=fixed_env
    ).stdout.strip()
    assert lean.is_file()

    temporary = Path(tempfile.mkdtemp(prefix="stage1-m1255-release-", dir="/tmp"))
    try:
        shutil.copy2(HERE / "Statement.lean", temporary / "Statement.lean")
        shutil.copy2(HERE / "Validation.lean", temporary / "Validation.lean")
        statement = run(
            [str(lean), "--trust=0", "-t0", "-o", "Statement.olean", "Statement.lean"],
            cwd=temporary,
            env={**fixed_env, "LEAN_PATH": lean_path},
        ).stdout
        validation = run(
            [str(lean), "--trust=0", "-t0", "Validation.lean"],
            cwd=temporary,
            env={**fixed_env, "LEAN_PATH": f"{temporary}:{lean_path}"},
        ).stdout
    finally:
        shutil.rmtree(temporary)

    assert "sorryAx" not in statement + validation
    assert "Declarations are sorry-free!" in validation
    for declaration in (
        "Stage1Instances.THM_M_1255.Validation.differentialCoordinateDerivativesCommute",
        "Stage1Instances.THM_M_1255.Validation.differentialPolynomialActionExists",
    ):
        assert reported_axioms(validation, declaration) == EXPECTED_AXIOMS
    return statement + validation


def main() -> None:
    if not __debug__:
        raise RuntimeError("release validation requires Python assertions")

    decision = load(HERE / "release-decision.json")
    receipt_path = HERE / "release-receipt.json"
    receipt = load(receipt_path) if receipt_path.exists() else None
    spec = load(HERE / "release-spec.json")
    validation = load(HERE / "validation-receipt.json")
    proof = load(HERE / "proof-receipt.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    assert run(
        ["git", "merge-base", "--is-ancestor", VALIDATION_BASE_REVISION, BASE_REVISION]
    ).returncode == 0
    for name, expected in UPSTREAM_INPUTS.items():
        assert sha256(HERE / name) == expected, f"upstream input drifted: {name}"
    for name, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / name) == expected, f"authority input drifted: {name}"
    for name, expected in TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"tool input drifted: {name}"

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 160
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned"
    assert target["legacy_artifacts_accepted"] is False
    assert target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1255-VALIDATION"
    )
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 160,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1255-VALIDATION"],
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
        "-I",
        "-B",
        f"Stage1_Instances/{THEOREM}/check_release.py",
    ]
    assert spec["cwd"] == "." and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "not_used" and spec["expected_exit"] == 0
    assert spec["env_overrides"] == {
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    }
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

    assert intake["lifecycle_mode"] == "planned"
    assert intake["theorem_complete"] is False
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == (
        STATEMENT_EXPRESSION_SHA256
    )
    assert statement["theorem_complete"] is False
    assert registry["root_obligation_id"] == "M1255-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    nodes = {row["obligation_id"]: row for row in graphs["nodes"]}
    assert nodes["M1255-ROOT"]["human_debt"] == "H3"
    assert nodes["M1255-ROOT"]["machine_debt"] == "M3"
    assert nodes["M1255-ROOT"]["readability_debt"] == "R4"
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == FROZEN_CLOSED_IDS
    assert closure["root_closed"] is False
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == FROZEN_CUT

    validation_result = validation["result"]
    assert validation_result["accepted_closed_obligation_ids"] == []
    assert validation_result["provisionally_validated_obligation_ids"] == PROVISIONAL_IDS
    assert validation_result["root_closed"] is False
    assert validation_result["accepted_root_machine_debt"] == "M3"
    assert validation_result["accepted_root_vector"] == ["H3", "M3", "R4"]
    assert validation_result["accepted_remaining_root_cut_set"] == FROZEN_CUT
    assert validation_result["proposed_remaining_root_cut_set_after_proof_acceptance"] == (
        PROPOSED_CUT
    )
    assert validation_result[
        "proposed_remaining_root_leaf_cut_set_after_proof_acceptance"
    ] == PROPOSED_LEAF_CUT
    assert validation_result["audit_complete"] is False
    assert validation_result["theorem_complete"] is False

    obligation_source = source_without_comments(
        (HERE / "ObligationTree.lean").read_text(encoding="utf-8")
    )
    assert "import Statement" not in obligation_source.split("namespace", 1)[0]
    assert "def MalgrangeEhrenpreisTarget" in obligation_source
    proof_source = source_without_comments((HERE / "Proof.lean").read_text(encoding="utf-8"))
    assert "FundamentalSolutionsFor polynomialActionPackage" not in proof_source
    assert "MalgrangeEhrenpreisTarget" not in proof_source

    evidence = decision["evidence_reconciliation"]
    assert evidence["exact_frozen_target_elaboration"] == "provisional_pass"
    assert evidence["canonical_differential_action_reconstruction"] == "provisional_pass"
    assert evidence["exact_canonical_module_linkage"] == "fail_closed"
    assert evidence["exact_root_kernel_closure"] == "fail_closed"
    assert evidence["frozen_child_to_parent_composition"] == "conditional_only"
    assert evidence["accepted_closed_obligation_ids"] == []
    assert evidence["provisionally_validated_obligation_ids"] == PROVISIONAL_IDS
    required_false_gates = (
        "validation_dependency_master_accepted",
        "accepted_foundation_profile",
        "complete_transitive_tcb_and_provenance",
        "source_fidelity_h0_accepted",
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
        "H": "H3",
        "M": "M3",
        "R": "R4",
    }
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert result["release_accepted"] is False
    assert result["audit_z"] == result["theorem_z"] == "blocked"
    assert result["accepted_receipt_ids"] == decision["accepted_receipt_ids"] == []
    assert result["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert result["first_failed_gate_detail"] == (
        "dependency.S56-M-1255-VALIDATION.master_acceptance"
    )
    assert result["first_failed_theorem_gate"] == "M1255-C-FUNDSOL"
    assert result["first_failed_release_protocol_gate"] == (
        "S56-10.6-HERMETIC-COLD-EMPTY-CACHE"
    )
    assert result["accepted_remaining_root_cut_set"] == FROZEN_CUT
    assert result["proposed_remaining_root_cut_set_after_proof_acceptance"] == PROPOSED_CUT
    assert result["proposed_remaining_root_leaf_cut_set_after_proof_acceptance"] == (
        PROPOSED_LEAF_CUT
    )

    replay_output = canonical_replay()
    if receipt is not None:
        assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
        assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
        assert receipt["support_state"] == decision["decision_support"]
        assert receipt["proposed_state"] == decision["proposed_state"]
        assert receipt["release_grade"] is False
        assert receipt["accepted"] is False and receipt["master_acceptance"] is False
        assert receipt["decision_id"] == decision["decision_id"]
        assert receipt["canonical_target_expression_sha256"] == STATEMENT_EXPRESSION_SHA256
        assert receipt["release_inputs"] == {
            "release-decision.json": sha256(HERE / "release-decision.json"),
            "release-spec.json": sha256(HERE / "release-spec.json"),
            "check_release.py": sha256(Path(__file__).resolve()),
            "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
            "obligation-registry.json": UPSTREAM_INPUTS["obligation-registry.json"],
            "typed-graphs.json": UPSTREAM_INPUTS["typed-graphs.json"],
        }
        assert receipt["result"]["verdict"] == "blocked"
        assert receipt["result"]["audit_complete"] is False
        assert receipt["result"]["theorem_complete"] is False
        assert receipt["result"]["release_accepted"] is False
        assert receipt["result"]["accepted_receipt_ids"] == []
        assert receipt["result"]["first_failed_gate"] == result["first_failed_gate"]
        assert receipt["result"]["first_failed_gate_detail"] == result[
            "first_failed_gate_detail"
        ]
        assert receipt["result"]["remaining_root_cut_set"] == result["remaining_root_cut_set"]
        assert receipt["known_failures"] == decision["known_failures"]
        assert set(receipt["changed_paths"]) == CHANGED_PATHS
        assert receipt["canonical_replay"]["exit_code"] == 0
        assert receipt["canonical_replay"]["stdout_sha256"] == hashlib.sha256(
            replay_output.encode("utf-8")
        ).hexdigest()
        assert receipt["canonical_replay"]["stdout_bytes"] == len(
            replay_output.encode("utf-8")
        )

    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        path = ROOT / relative
        if not path.exists():
            continue
        data = path.read_bytes()
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

    print("PASS THM-M-1255 canonical trust-zero statement and differential replay")
    print("PASS release inputs, dependency receipt, root boundary, and all 13 obligations reconciled")
    print("OPEN exact M3 root; AUDIT-Z and THEOREM-Z are false")
    print("BLOCKED dependency acceptance, hermetic release, independent verification, and master acceptance")


if __name__ == "__main__":
    main()
