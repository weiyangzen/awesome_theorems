#!/usr/bin/env python3
"""Fail-closed release reconciliation for S56-M-1061-RELEASE."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-1061"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1061-RELEASE"
THEOREM = "THM-M-1061"
BASE_REVISION = "443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b"
BASE_TREE = "c5771c47c12b80aba613e6d844570f83b39ded6d"
EXPRESSION_SHA256 = "681a5c8fcbefe363119923dd4424876a37b90d0418e715ff46daf781b5e32119"
DENOMINATOR_SHA256 = "9b84baaedfed9f75ef3fce37e77b91bb48ddabb2dd1316216bf7c84ea5d4e811"
VALIDATION_RECEIPT_ID = "S56-M-1061-VALIDATION-local-20260715-slot1"
VALIDATION_RECEIPT_SHA256 = (
    "dc2c076e4a303220e861ea2962f92caa68ac7135cb6b353acdb07bc6a1e1dbe9"
)
PROOF_RECEIPT_ID = "S56-M-1061-PROOF-local-20260715-slot51"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = (
    "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
)
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
ALLOWED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
VECTOR = {"H": "H1", "M": "M3", "R": "R3"}
ANALYTIC_CUT = [
    "M1061-L-LOWER-LOCAL",
    "M1061-T-LOWER",
    "M1061-C-COMPACT-COVER",
    "M1061-L-CORE-UPPER",
    "M1061-L-TAIL-UPPER",
    "M1061-T-UPPER",
]
FROZEN_CUT = ["M1061-T-LIMIT-MERGE"]
INVENTORY_IDS = [
    "M1061-ROOT",
    "M1061-S-DEFINITIONS",
    "M1061-S-BOUNDARIES",
    "M1061-S-FOUNDATION",
    "M1061-N-VARIATIONAL",
    *ANALYTIC_CUT,
    "M1061-T-LIMIT-MERGE",
    "M1061-T-ROOT-TRANSPORT",
    "M1061-X-SOURCE",
    "M1061-X-PROVENANCE",
]
RECONCILED_INPUTS = {
    "intake.json": "6a6aec2642e1265c8418091904d6c3a9afc697a9c995e6b3435c56b6bcb5ed38",
    "README.md": "c86d0f290879a14a12ff8716a032d08fd4e1ff604c376c078557076b7b1d4823",
    "source_statement_crosswalk.md": "19f259354bb4acc9b7f1f96075555064946ba2b7c246d1e1840821d5db67f49c",
    "statement.json": "3f4247f50a0ebb6a2f331b9dc106017efdda47e960abe7b47d034852d4730b00",
    "Statement.lean": "19f51da84ce06f338e5320efe3a7c9843110375f23e2ed1d1b1180f460f70af1",
    "anchor-audit.json": "5de4cc88db6b0be992ca6a8eebc34efa7841fd17d0313598c1541ed2ed985190",
    "AnchorAudit.lean": "8b2746a8333fb3741fe9e6bc07ddd1a36876aa2aef4a4fd070f07ca61dbcdc40",
    "obligation-registry.json": "b2921c93154cd6eb3f700cf8f991dc422ba1f17bc0f73a5044fceb44ccb598ff",
    "typed-graphs.json": "5c4c8d5382962ab8d8621701ce88daf3bd7c3dd25426c478fa09b66828e40055",
    "ObligationTree.lean": "f44afa56d0b552798d026ec92604a815a52511726a91e56ac3300770abd5a6f5",
    "obligation-tree.md": "a982474d5dcf525343bc19e80653268fd2033b445fccea5969cd997cb0d9dc43",
    "proof-receipt.json": "5c1fe2eba1e661c6db5d94bd8d0effa64a5d04219262c6d194faf68cc273370f",
    "proof-blocker.json": "0e094a580357dc86bce0089b5023d70e22e2ca0659e2420059a5aa23e21e1eaa",
    "Proof.lean": "6a8dfb9e10acb56a79559bfd17d8b828815827aa955a98496774f6c91b88df85",
    "validation-spec.json": "f7b2c981a39c5b335a536b4ef48035e85e44146833ec0d2fb62096b566d60e06",
    "validation-receipt.json": VALIDATION_RECEIPT_SHA256,
    "Validation.lean": "a842c3239274231115fcb16cb437769f05cc4b79e05786b2464ac528e749bda8",
    "check_validation.sh": "3649d077ca9f9702517cf843ecba38647ec4c8dc3c07d78fc84d7b53542bba25",
    "check_validation.py": "22b1d828b50d8b371401152e74279d867628afac3c3aa7bcf174c5321aa6af2c",
    "validation-phase.md": "7452ccb443c57ffea71e092043d29bb3df5ed07e40be083e46f6e09003898066",
    "validation-specs.json": "74b811df5f2a268bd22f577aa0bd1a45863feaf3024e4f5d2b7646becebcd34e",
}
AUTHORITY_INPUTS = {
    "Docs/Stage1_Targets_rev-5.6.json": "02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c",
    "Docs/Stage1_Execution_DAG_rev-5.6.json": "0bb2f433832fe71156aa46c0828102ec3fb61a00dec81fae129c2826a59f63ca",
    "Docs/Stage1_Blueprint_rev-5.6.md": "c09f9f713bdbc820559e41e1e1840423d60cc2af666aeaf5f3c88587de77f161",
    "Docs/Blueprint_Guidelines.md": "a06c07b5ca1b270b4935ad3dab893e9a0e078c29c8da2ef9dca1e71193310535",
    "skills/execute-stage1-rev56/SKILL.md": "26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8",
    "Formalizations/Lean/lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "Formalizations/Lean/lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
RELEASE_OUTPUTS = {
    "release-spec.json": "6c1990f19ebff061040ff9f453a2d5e34a28370c7ba73876db23b73005da5fa9",
    "release-decision.json": "783bed800ef138ed1590be88ff68387b50be4a8051c87cc8e52a58f73b223e84",
    "release-validation.md": "a714f18e0fae49a2b1c16e24460964e1afd460802e768c0366ef8000a7b99948",
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
    "PASS S56-M-1061-RELEASE negative reconciliation",
    "PASS fresh trust-zero network-isolated replay: exact statement, conditional root transport, thirteen partial bodies, anchors, and two differential probes",
    "BLOCKED dependency: S56-M-1061-VALIDATION is provisional and not master-accepted",
    "BLOCKED exact root: M1061-L-LOWER-LOCAL and five downstream analytic obligations have no premise-free closure",
    "BLOCKED assurance: H0/R0/trust/cold-offline/SBOM/independent-verifier/bundle gates remain open",
    "verdict=blocked lifecycle=planned root_vector=H1/M3/R3 audit_complete=false theorem_complete=false",
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


def run(argv: list[str], *, cwd: Path = ROOT, timeout: int = 900) -> str:
    env = os.environ.copy()
    env.update({
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "TZ": "UTC",
        "LEAN_NUM_THREADS": "1",
    })
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
    if result.returncode:
        raise AssertionError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).strip()


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


def axiom_reports(output: str) -> dict[str, set[str]]:
    pattern = re.compile(
        r"'(?P<declaration>[^']+)' depends on axioms:\s*\[(?P<axioms>.*?)\]",
        re.DOTALL,
    )
    return {
        match.group("declaration"): {
            item.strip()
            for item in match.group("axioms").split(",")
            if item.strip()
        }
        for match in pattern.finditer(output)
    }


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    if not __debug__:
        raise RuntimeError("release checker requires Python assertions")
    os.umask(0o022)

    decision = load(HERE / "release-decision.json")
    receipt = load(HERE / "release-receipt.json")
    spec = load(HERE / "release-spec.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    intake = load(HERE / "intake.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof = load(HERE / "proof-receipt.json")
    blocker = load(HERE / "proof-blocker.json")
    validation = load(HERE / "validation-receipt.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 504
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["legacy_artifacts_accepted"] is False
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False

    release_item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert release_item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 504,
        "phase": "release",
        "layer": 6,
        "state": "[ ]",
        "depends_on": ["S56-M-1061-VALIDATION"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Reconcile evidence and decide the exact theorem-completion verdict.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    validation_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-1061-VALIDATION"
    )
    assert validation_item["state"] == "[_]" and validation_item["attempts"] == 1

    assert decision["reconciled_inputs"] == RECONCILED_INPUTS
    for name, expected in RECONCILED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"reconciled input drifted: {name}"
    assert decision["authority_inputs"] == AUTHORITY_INPUTS
    for relative, expected in AUTHORITY_INPUTS.items():
        assert sha256(ROOT / relative) == expected, f"authority input drifted: {relative}"
    for name, expected in RELEASE_OUTPUTS.items():
        assert sha256(HERE / name) == expected, f"release output drifted: {name}"

    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_1061.VaradhanIntegralLemmaTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == RECONCILED_INPUTS["Statement.lean"]
    assert intake["root_vector"] == {
        "human": "H1", "machine": "M4", "readability": "R3"
    }
    assert intake["theorem_complete"] is False
    assert anchor["root_machine_classification"] == "M4"
    assert anchor["theorem_proved"] is anchor["theorem_complete"] is False

    assert registry["root_obligation_id"] == "M1061-ROOT"
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert [row["obligation_id"] for row in registry["obligations"]] == INVENTORY_IDS
    assert registry["status_observed_after_freeze"]["root_machine_debt"] == "M3"
    root_registry = registry["obligations"][0]
    assert root_registry["statement_fingerprint"] == (
        f"lean-file-sha256:{RECONCILED_INPUTS['Statement.lean']}"
    )

    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is closure["audit_complete"] is False
    assert closure["theorem_complete"] is False
    assert closure["root_machine_debt"] == "M3"
    assert closure["remaining_root_cut_set"] == FROZEN_CUT
    assert closure["composition_certificates"] == [
        "Stage1Instances.THM_M_1061.ObligationTree.root_of_integralLemmaTerminal"
    ]
    root_node = next(row for row in graphs["nodes"] if row["obligation_id"] == "M1061-ROOT")
    assert (
        root_node["human_debt"],
        root_node["machine_debt"],
        root_node["readability_debt"],
    ) == ("H1", "M3", "R3")
    assert root_node["evidence_ids"] == []
    for obligation_id in ANALYTIC_CUT:
        node = next(row for row in graphs["nodes"] if row["obligation_id"] == obligation_id)
        assert node["machine_debt"] == "M4" and node["evidence_ids"] == []

    assert proof["receipt_id"] == PROOF_RECEIPT_ID
    assert proof["support_state"] == "provisional_worker_selftest"
    assert proof["accepted"] is False
    assert proof["provisionally_closed_obligation_ids"] == []
    assert proof["accepted_closed_obligation_ids"] == []
    assert proof["result"]["root_kernel_closed"] is False
    assert proof["remaining_root_cut_set"] == ANALYTIC_CUT
    assert blocker["first_failed_gate"] == "M1061-L-LOWER-LOCAL"
    assert blocker["remaining_root_cut_set"] == ANALYTIC_CUT
    assert blocker["root_closed"] is blocker["theorem_complete"] is False

    assert validation["receipt_id"] == VALIDATION_RECEIPT_ID
    assert sha256(HERE / "validation-receipt.json") == VALIDATION_RECEIPT_SHA256
    assert validation["support_state"] == "provisional_worker_selftest"
    assert validation["proposed_state"] == "[_]"
    assert validation["accepted"] is validation["release_grade"] is False
    assert validation["verdict"] == "blocked"
    assert validation["first_failed_gate"] == "dependency.S56-M-1061-PROOF.master_acceptance"
    assert validation["remaining_root_cut_set"] == ANALYTIC_CUT
    assert validation["frozen_architecture_cut_set"] == FROZEN_CUT
    validation_result = validation["result"]
    assert validation_result["root_kernel_closed"] is False
    assert validation_result["accepted_closed_obligation_ids"] == []
    assert validation_result["complete_transitive_foundation_tcb_provenance"] == "fail_closed"
    assert validation_result["hermetic_cold_offline_replay"] == "fail_closed"
    assert validation_result["independent_distinct_runner"] == "fail_closed"
    assert validation_result["audit_complete"] is validation_result["theorem_complete"] is False

    assert decision["schema_version"] == "stage1-release-decision/1.0"
    assert decision["item_id"] == ITEM and decision["theorem_id"] == THEOREM
    assert decision["phase"] == decision["intent"] == "release"
    assert decision["base_revision"] == BASE_REVISION and decision["base_tree"] == BASE_TREE
    assert decision["support_state"] == "provisional_worker_selftest"
    assert decision["proposed_state"] == "[_]" and decision["accepted"] is False
    assert decision["release_grade"] is decision["content_addressed_release_evidence"] is False
    assert decision["verdict"] == "blocked"
    assert decision["lifecycle_before"] == decision["lifecycle_after"] == "planned"
    assert decision["accepted_receipt_ids"] == []
    dependency = decision["dependency"]
    assert dependency["item_id"] == validation["item_id"]
    assert dependency["receipt_id"] == validation["receipt_id"]
    assert dependency["receipt_sha256"] == VALIDATION_RECEIPT_SHA256
    assert dependency["worker_projection"] == "[_]"
    assert dependency["master_accepted"] is dependency["receipt_accepted"] is False
    assert dependency["receipt_release_grade"] is False
    assert decision["root_vector"]["before"] == decision["root_vector"]["after"] == VECTOR
    assert decision["terminal_decisions"] == {
        "audit_complete": False,
        "theorem_complete": False,
        "audit_z": "blocked",
        "theorem_z": "blocked",
        "release_accepted": False,
        "master_acceptance": False,
    }
    assert decision["first_failed_gate"]["gate_id"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert decision["first_failed_gate"]["dependency_gate"] == (
        "dependency.S56-M-1061-VALIDATION.master_acceptance"
    )
    assert decision["first_failed_theorem_gate"]["gate_id"] == "M1061-L-LOWER-LOCAL"
    assert decision["first_failed_release_gate"]["gate_id"] == (
        "S56-10.6-HERMETIC-COLD-BUILD"
    )
    assert decision["canonical_obligation_ids"] == INVENTORY_IDS
    assert decision["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert decision["statement_fingerprint"] == f"lean-expression-sha256:{EXPRESSION_SHA256}"
    assert decision["analytic_root_cut"] == ANALYTIC_CUT
    assert decision["frozen_architecture_cut"] == FROZEN_CUT
    for key in (
        "audit_inventory_reconciliation",
        "human_source_acceptance",
        "readability_acceptance",
        "foundation_and_trust_closure",
        "hermetic_release_reproduction",
        "supply_chain_closure",
        "independent_release_verification",
        "protected_ci_and_adversarial_gates",
        "deterministic_release_bundle",
        "master_acceptance",
    ):
        assert decision["evidence_reconciliation"][key].startswith("missing"), key
    assert decision["evidence_reconciliation"]["root_kernel_closure"].startswith("failed")
    cut_text = "\n".join(decision["remaining_root_cut_set"])
    for fragment in (
        "master acceptance",
        "M1061-L-LOWER-LOCAL",
        "premise-free exact-root",
        "AUDIT-Z",
        "accepted H0",
        "accepted R0",
        "accepted foundation profile",
        "empty-cache network-denied cold build",
        "SBOM and license",
        "two signed attestations",
        "minimal release verifier",
        "deterministic build-twice content-addressed release bundle",
    ):
        assert fragment in cut_text, fragment

    assert spec["schema_version"] == "stage1-release-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-1061-RELEASE-negative-reconciliation-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == INVENTORY_IDS
    assert receipt["recipe"] == {
        key: spec[key]
        for key in (
            "recipe_id",
            "cwd",
            "argv",
            "env_allowlist",
            "timeout_seconds",
            "network_policy",
            "network_enforcement",
            "expected_exit",
            "expected_outputs",
            "covered_obligation_ids",
            "covered_declarations",
        )
    }

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|run_tac)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    lean_files = (
        "Statement.lean",
        "AnchorAudit.lean",
        "ObligationTree.lean",
        "Proof.lean",
        "Validation.lean",
    )
    for name in lean_files:
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    validation_source = code_without_comments((HERE / "Validation.lean").read_text())
    assert "VaradhanIntegralLemmaTarget := by" not in validation_source
    proof_source = code_without_comments((HERE / "Proof.lean").read_text())
    assert "VaradhanIntegralLemmaTarget := by" not in proof_source

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256

    toolchain_bin = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin"
    lean = toolchain_bin / "lean"
    lake = toolchain_bin / "lake"
    bwrap = shutil.which("bwrap")
    git_path = shutil.which("git")
    assert bwrap is not None and git_path is not None
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(Path(os.path.realpath(sys.executable))) == PYTHON_SHA256
    assert sha256(Path(os.path.realpath(git_path))) == GIT_SHA256
    assert sha256(Path(os.path.realpath(bwrap))) == BWRAP_SHA256
    assert LEAN_COMMIT in run([str(lean), "--version"], timeout=60)
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"], timeout=60)
    environment = receipt["environment"]
    assert environment["lean_executable_sha256"] == LEAN_SHA256
    assert environment["lake_executable_sha256"] == LAKE_SHA256
    assert environment["python_executable_sha256"] == PYTHON_SHA256
    assert environment["git_executable_sha256"] == GIT_SHA256
    assert environment["bubblewrap_executable_sha256"] == BWRAP_SHA256
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    assert environment["mathlib_license_sha256"] == MATHLIB_LICENSE_SHA256

    replay = run(["bash", str(HERE / "check_validation.sh")], timeout=900)
    assert "error:" not in replay
    assert "sorryAx" not in replay and "declaration uses 'sorry'" not in replay
    assert "(h : IntegralLemmaTerminal" in replay and "VaradhanIntegralLemmaTarget" in replay
    reports = axiom_reports(replay)
    checked_declarations = set(spec["covered_declarations"]) - {
        "Stage1Instances.THM_M_1061.VaradhanIntegralLemmaTarget"
    }
    for declaration in checked_declarations:
        assert reports.get(declaration) == ALLOWED_AXIOMS, declaration

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == receipt["intent"] == "release"
    assert receipt["depends_on"] == ["S56-M-1061-VALIDATION"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is receipt["content_addressed_release_evidence"] is False
    assert receipt["signature"] is None
    assert receipt["result"]["verdict"] == "blocked"
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == VECTOR
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["provisional_receipt_ids_inspected"] == [
        PROOF_RECEIPT_ID, VALIDATION_RECEIPT_ID
    ]
    assert receipt["first_failed_gate"] == "S56-10.2-DEPENDENCY-ACCEPTANCE"
    assert receipt["first_failed_dependency_gate"] == (
        "dependency.S56-M-1061-VALIDATION.master_acceptance"
    )
    assert receipt["first_failed_theorem_gate"] == "M1061-L-LOWER-LOCAL"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["analytic_root_cut"] == ANALYTIC_CUT
    assert receipt["frozen_architecture_cut"] == FROZEN_CUT
    assert receipt["remaining_root_cut_set"] == decision["remaining_root_cut_set"]
    assert receipt["inputs"]["release_spec_sha256"] == sha256(HERE / "release-spec.json")
    assert receipt["inputs"]["release_decision_sha256"] == sha256(
        HERE / "release-decision.json"
    )
    assert receipt["inputs"]["release_validation_sha256"] == sha256(
        HERE / "release-validation.md"
    )
    for name, expected in RECONCILED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["item_id"] == ITEM and packet["base_revision"] == BASE_REVISION
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["output_summary"] == receipt["output_summary"] == SUMMARY_LINES
    assert packet["commands"] == receipt["commands"]
    assert packet["commands"][-1] == {
        "argv": ["python3", "-I", "-B", f"Stage1_Instances/{THEOREM}/check_release.py"],
        "exit_code": 0,
        "result": (
            "hash-bound negative release reconciliation and fresh network-isolated "
            "trust-zero Lean replay passed"
        ),
    }

    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    obligation_output = run([
        "python3", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py"
    ])
    assert "root closure: open (M3)" in obligation_output
    public = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("release-decision.json", "release-validation.md")
    )
    assert "/home/" not in public and ".cron/" not in public

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
