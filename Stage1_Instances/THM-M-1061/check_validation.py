#!/usr/bin/env python3
"""Fail-closed validation for S56-M-1061-VALIDATION."""

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
TOOLCHAIN_BIN = Path.home() / ".elan/toolchains/leanprover--lean4---v4.29.0/bin"

ITEM = "S56-M-1061-VALIDATION"
THEOREM = "THM-M-1061"
BASE_REVISION = "4ba3f2fd1e609b5958f24e0415eef9300da16924"
BASE_TREE = "6abc1f64758c17a59dad8c80ac44f238983dc720"
EXPRESSION_SHA256 = "681a5c8fcbefe363119923dd4424876a37b90d0418e715ff46daf781b5e32119"
DENOMINATOR_SHA256 = "9b84baaedfed9f75ef3fce37e77b91bb48ddabb2dd1316216bf7c84ea5d4e811"
TOOLCHAIN_SHA256 = "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
MANIFEST_SHA256 = "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}

EXPECTED_INPUTS = {
    "Statement.lean": "19f51da84ce06f338e5320efe3a7c9843110375f23e2ed1d1b1180f460f70af1",
    "ObligationTree.lean": "f44afa56d0b552798d026ec92604a815a52511726a91e56ac3300770abd5a6f5",
    "Proof.lean": "6a8dfb9e10acb56a79559bfd17d8b828815827aa955a98496774f6c91b88df85",
    "AnchorAudit.lean": "8b2746a8333fb3741fe9e6bc07ddd1a36876aa2aef4a4fd070f07ca61dbcdc40",
    "Validation.lean": "a842c3239274231115fcb16cb437769f05cc4b79e05786b2464ac528e749bda8",
    "statement.json": "3f4247f50a0ebb6a2f331b9dc106017efdda47e960abe7b47d034852d4730b00",
    "anchor-audit.json": "5de4cc88db6b0be992ca6a8eebc34efa7841fd17d0313598c1541ed2ed985190",
    "obligation-registry.json": "b2921c93154cd6eb3f700cf8f991dc422ba1f17bc0f73a5044fceb44ccb598ff",
    "typed-graphs.json": "5c4c8d5382962ab8d8621701ce88daf3bd7c3dd25426c478fa09b66828e40055",
    "validation-specs.json": "74b811df5f2a268bd22f577aa0bd1a45863feaf3024e4f5d2b7646becebcd34e",
    "proof-receipt.json": "5c1fe2eba1e661c6db5d94bd8d0effa64a5d04219262c6d194faf68cc273370f",
    "proof-blocker.json": "0e094a580357dc86bce0089b5023d70e22e2ca0659e2420059a5aa23e21e1eaa",
    "check_validation.sh": "3649d077ca9f9702517cf843ecba38647ec4c8dc3c07d78fc84d7b53542bba25",
    "validation-spec.json": "f7b2c981a39c5b335a536b4ef48035e85e44146833ec0d2fb62096b566d60e06",
}

PROOF_DECLARATIONS = {
    "Stage1Instances.THM_M_1061.Proof.probabilityMeasure_of_satisfiesLDP",
    "Stage1Instances.THM_M_1061.Proof.speed_pos_of_satisfiesLDP",
    "Stage1Instances.THM_M_1061.Proof.speed_tendsto_zero_of_satisfiesLDP",
    "Stage1Instances.THM_M_1061.Proof.basic_boundaries_of_satisfiesLDP",
    "Stage1Instances.THM_M_1061.Proof.closed_upper_of_satisfiesLDP",
    "Stage1Instances.THM_M_1061.Proof.open_lower_of_satisfiesLDP",
    "Stage1Instances.THM_M_1061.Proof.lowerSemicontinuous_of_isGoodRateFunction",
    "Stage1Instances.THM_M_1061.Proof.compact_sublevel_of_isGoodRateFunction",
    "Stage1Instances.THM_M_1061.Proof.logExpIntegral_upper_bound",
    "Stage1Instances.THM_M_1061.Proof.logExpIntegral_lower_bound",
    "Stage1Instances.THM_M_1061.Proof.logExpIntegral_bounds_of_satisfiesLDP",
    "Stage1Instances.THM_M_1061.Proof.tendsto_of_variational_liminf_limsup",
    "Stage1Instances.THM_M_1061.Proof.logExpIntegral_tendsto_of_bounds",
}
VALIDATION_DECLARATIONS = {
    "Stage1Instances.THM_M_1061.Validation.independentlyProjectedOpenLower",
    "Stage1Instances.THM_M_1061.Validation.independentlyMergedLiminfLimsup",
}
ANCHOR_DECLARATIONS = {
    "LowerSemicontinuous",
    "IsCompact",
    "Filter.limsup",
    "Filter.liminf",
    "ENNReal.log",
    "MeasureTheory.lintegral",
    "MeasureTheory.IsProbabilityMeasure",
}
OPEN_CUT = [
    "M1061-L-LOWER-LOCAL",
    "M1061-T-LOWER",
    "M1061-C-COMPACT-COVER",
    "M1061-L-CORE-UPPER",
    "M1061-L-TAIL-UPPER",
    "M1061-T-UPPER",
]
SUMMARY = (
    "PASS THM-M-1061 narrow validation",
    "PASS network-isolated trust-zero replay: exact statement, conditional root transport, thirteen partial proof declarations, anchors, and two differential probes elaborated",
    "PASS trust observation: all checked proof, transport, and differential declarations report exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, proof receipt boundary, clean mathlib pin/tree/remote/license, tool identities, and selected sources agree",
    "PASS hygiene: target Lean sources contain no placeholders, bodyless declarations, unsafe/oracle mechanisms, or sorry reports",
    "FAIL CLOSED authority/root: proof master acceptance is pending and the exact Varadhan root remains open M3 with six analytic cut obligations",
    "FAIL CLOSED foundation/provenance: observed axioms and selected source hashes are not a complete transitive declaration, TCB, or supply-chain closure",
    "FAIL CLOSED hermetic/independent release: the shared warm cache is not a cold offline restore and same-worker probes are not a distinct signed verifier",
    "audit_complete=false; theorem_complete=false",
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL THM-M-1061 validation: {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate JSON key {key!r} in {path.relative_to(ROOT)}")
            result[key] = value
        return result

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates
        )
    except (OSError, json.JSONDecodeError) as error:
        fail(f"cannot load {path.relative_to(ROOT)}: {error}")
    if not isinstance(value, dict):
        fail(f"expected JSON object in {path.relative_to(ROOT)}")
    return value


def run(
    argv: list[str], *, cwd: Path = ROOT, timeout: int = 900
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
        env={
            **os.environ,
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
            "TZ": "UTC",
            "LEAN_NUM_THREADS": "1",
        },
    )
    if result.returncode:
        fail(f"command exited {result.returncode}: {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd, timeout=60).rstrip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


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


def main() -> None:
    if not __debug__:
        fail("Python assertions must be enabled")

    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    proof_blocker = load(HERE / "proof-blocker.json")
    targets = load(ROOT / "Docs" / "Stage1_Targets_rev-5.6.json")
    dag = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")


    if git("rev-parse", "HEAD") != BASE_REVISION:
        fail("base revision changed")
    if git("rev-parse", "HEAD^{tree}") != BASE_TREE:
        fail("base tree changed")

    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 504
    assert target["baseline"] == "L0" and target["rework_required"] is True
    assert target["lifecycle_mode"] == "planned" and target["theorem_complete"] is False
    item = next(row for row in dag["items"] if row["id"] == ITEM)
    predecessor = next(row for row in dag["items"] if row["id"] == "S56-M-1061-PROOF")
    assert item["state"] == "[ ]" and item["depends_on"] == ["S56-M-1061-PROOF"]
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1

    assert spec["schema_version"] == "stage1-validation-spec/1.0"
    assert spec["item_id"] == receipt["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-I", "-B", "Stage1_Instances/THM-M-1061/check_validation.py"
    ]
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert len(spec["covered_obligation_ids"]) == 15
    assert len(spec["covered_obligation_ids"]) == len(set(spec["covered_obligation_ids"]))
    assert set(spec["covered_declarations"]) == (
        PROOF_DECLARATIONS
        | VALIDATION_DECLARATIONS
        | ANCHOR_DECLARATIONS
        | {
            "Stage1Instances.THM_M_1061.VaradhanIntegralLemmaTarget",
            "Stage1Instances.THM_M_1061.ObligationTree.root_of_integralLemmaTerminal",
        }
    )

    for key in (
        "recipe_id", "cwd", "argv", "fixed_env", "timeout_seconds",
        "network_policy", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations", "scope_boundary",
    ):
        assert receipt["recipe"][key] == spec[key], key

    for name, expected in EXPECTED_INPUTS.items():
        actual = sha256(HERE / name)
        if actual != expected:
            fail(f"stale input {name}: expected {expected}, got {actual}")
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["check_validation.py"] == sha256(Path(__file__).resolve())

    assert statement["canonical_formal_target"]["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["root_obligation_id"] == graphs["root_node_id"] == "M1061-ROOT"
    assert registry["denominator_sha256"] == graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    ids = [row["obligation_id"] for row in registry["obligations"]]
    assert ids == registry["frozen_denominators"]["inventory"]
    assert set(ids) == {node["obligation_id"] for node in graphs["nodes"]}
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == ["M1061-S-DEFINITIONS", "M1061-T-ROOT-TRANSPORT"]
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert closure["remaining_root_cut_set"] == ["M1061-T-LIMIT-MERGE"]

    assert proof_receipt["support_state"] == "provisional_worker_selftest"
    assert proof_receipt["accepted"] is False
    assert proof_receipt["provisionally_closed_obligation_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["root_kernel_closed"] is False
    assert proof_receipt["remaining_root_cut_set"] == OPEN_CUT
    assert proof_blocker["remaining_root_cut_set"] == OPEN_CUT
    assert proof_blocker["root_closed"] is proof_blocker["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b"
        r"|^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "ObligationTree.lean", "Proof.lean",
        "AnchorAudit.lean", "Validation.lean",
    ):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        if prohibited.search(source):
            fail(f"prohibited Lean mechanism in {name}")
    validation_source = (HERE / "Validation.lean").read_text(encoding="utf-8")
    assert "import Proof" not in validation_source
    assert "import ObligationTree" not in validation_source
    assert "VaradhanIntegralLemmaTarget := by" not in validation_source

    if sha256(LEAN_ROOT / "lean-toolchain") != TOOLCHAIN_SHA256:
        fail("Lean toolchain pin changed")
    if sha256(LEAN_ROOT / "lake-manifest.json") != MANIFEST_SHA256:
        fail("Lake manifest pin changed")
    assert MATHLIB.resolve().is_dir(), "canonical pinned mathlib artifact is missing"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", "--untracked-files=all", cwd=MATHLIB) == ""
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert sha256(MATHLIB / "LICENSE") == MATHLIB_LICENSE_SHA256
    assert anchor["immutable_environment"]["mathlib_revision"] == MATHLIB_REVISION

    lean = TOOLCHAIN_BIN / "lean"
    lake = TOOLCHAIN_BIN / "lake"
    bwrap = shutil.which("bwrap")
    assert bwrap is not None
    assert sha256(lean) == LEAN_SHA256 and sha256(lake) == LAKE_SHA256
    assert sha256(Path(os.path.realpath(bwrap))) == BWRAP_SHA256
    assert sha256(Path(os.path.realpath(sys.executable))) == PYTHON_SHA256
    git_executable = shutil.which("git")
    assert git_executable is not None
    assert sha256(Path(os.path.realpath(git_executable))) == GIT_SHA256
    assert "98dc76e3c0a9b856c9b98726b713fb04fab16740" in run([str(lean), "--version"])

    selected_sources = receipt["provenance"]["selected_mathlib_sources"]
    for relative, expected in selected_sources.items():
        source = MATHLIB / relative
        olean = MATHLIB / ".lake/build/lib/lean" / relative.replace(".lean", ".olean")
        assert git("rev-parse", f"HEAD:{relative}", cwd=MATHLIB) == expected["blob"]
        assert sha256(source) == expected["source_sha256"]
        assert sha256(olean) == expected["olean_sha256"]

    replay = run(["bash", str(HERE / "check_validation.sh")], timeout=900)
    if "sorryAx" in replay or "declaration uses 'sorry'" in replay:
        fail("Lean replay reported a placeholder")
    reports = axiom_reports(replay)
    checked = PROOF_DECLARATIONS | VALIDATION_DECLARATIONS | {
        "Stage1Instances.THM_M_1061.ObligationTree.root_of_integralLemmaTerminal"
    }
    for declaration in checked:
        if reports.get(declaration) != EXPECTED_AXIOMS:
            fail(f"unexpected or missing axiom report for {declaration}")
    assert "(h : IntegralLemmaTerminal" in replay
    assert "VaradhanIntegralLemmaTarget" in replay

    semantic_summary = "\n".join(SUMMARY) + "\n"
    assert semantic_summary.startswith("PASS THM-M-1061 narrow validation\n")
    assert semantic_summary.endswith("audit_complete=false; theorem_complete=false\n")

    assert receipt["accepted"] is receipt["release_grade"] is False
    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["receipt_id"] == "S56-M-1061-VALIDATION-local-20260715-slot1"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]"
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["verdict"] == "blocked"
    assert receipt["signature"] is None
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["result"]["raw_replay_output_sha256"] is None
    assert set(receipt["result"]["observed_axioms"]) == EXPECTED_AXIOMS
    assert receipt["result"]["network_isolated_trust_zero_replay"] == "pass"
    assert receipt["result"]["complete_transitive_foundation_tcb_provenance"] == "fail_closed"
    assert receipt["result"]["hermetic_cold_offline_replay"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner"] == "fail_closed"
    assert receipt["result"]["root_kernel_closed"] is False
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-1061-PROOF.master_acceptance"
    assert receipt["remaining_root_cut_set"] == OPEN_CUT
    assert receipt["frozen_architecture_cut_set"] == ["M1061-T-LIMIT-MERGE"]
    assert receipt["root_vector_before"] == receipt["root_vector_after"] == {
        "H": "H1", "M": "M3", "R": "R3"
    }

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert len(packet["known_failures"]) == len(receipt["known_failures"]) == 7
    assert packet["commands"] == [row["command"] for row in receipt["commands"]]
    assert "exact-root closure" in packet["output_summary"]
    expected_changed = set(receipt["changed_paths"])
    assert set(packet["changed_paths"]) == expected_changed
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == expected_changed, (actual_changed, expected_changed)

    for line in SUMMARY:
        print(line)


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, StopIteration) as error:
        _, _, traceback = sys.exc_info()
        line = traceback.tb_next.tb_lineno if traceback and traceback.tb_next else "unknown"
        fail(f"invariant failed at line {line}: {error}")
    except subprocess.TimeoutExpired as error:
        fail(f"command timed out after {error.timeout} seconds: {error.cmd!r}")
