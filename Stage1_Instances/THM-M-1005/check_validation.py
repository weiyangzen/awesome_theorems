#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-1005-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-1005"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-1005-VALIDATION"
THEOREM = "THM-M-1005"
BASE_REVISION = "3bb4cb3ae15dff8b48c93242019edec3bf858e48"
BASE_TREE = "8e911f5a101bd92eb0951794fa0d9a3c0c3a2ddc"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "32343e66034f94d4afabc10f4d15cbae77daf650c757023a2142aafba50366e5"
DENOMINATOR_SHA256 = "188df14160a2cf8e92debc91b667ff27e71c15010b7e175b93f58941ca7d1933"
EXPECTED_AXIOMS = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_RUNNER_STDOUT_SHA256 = "54f89b6403cd9da22b20c820785b4de3a30e444405b43a50d89d713ca39b581a"
EXPECTED_INPUTS = {
    "Statement.lean": "03e36de9b3040e757f9620b3eac5e6f95d003abb5b9b2ffb58416b8f478f38f6",
    "ObligationTree.lean": "fd19100d3c8b2517f09de1498db1477016f79d2ae5d688315d576d65f437cd5c",
    "DoobLp.lean": "66ad60b7e5ca344df51e5c12007bd7cfe4b7ef5133240f415db5c47b59e8d4ef",
    "Proof.lean": "8d1ae03ba45809ecc2aab3fb904e96e1f91276d002640f75a15c3d5c57c8eb43",
    "Validation.lean": "e9943c1f34b38594be78efc798d9ba9cb69211b1104ae4fd483354ee6d36928a",
    "statement.json": "f855d13a849b0dc42fdfe18f4cc68b0208f427a5fe4d88d578e43da8e466f6c3",
    "instance.json": "583dbbd6389ae74da78617470b8b7afe33816a5cb44950ed292c4262db9e2f97",
    "task-dag.json": "b5d806bbe418d19f6ea83cbe01494a18e636a5107b32487279e83c610727135d",
    "anchor-audit.json": "71aab3a3368aa8a76d3faa0246eb3990859c25700074e15be2503339ba178b53",
    "obligation-registry.json": "ffa63ad21328ee58f873a49f5603347b9a909430370f71f30172b413da2c7ccf",
    "typed-graphs.json": "44b7b63d17f1c4b306096068a057d85920969fb934e3a0723d3664d8d10dfe45",
    "validation-specs.json": "b0a38a677123eadfe1deeedfbc6799601533fa9f543e12eaa7be735d1fd16392",
    "proof-receipt.json": "54e2e248d54193cf49ca7a2f18c65a0bd846040035a3c3d463ed8d4752fb7253",
    "proof-validation.md": "3260bb28d6ffcc28fc2939d2e7f8295e1dab1e96990d299d4119ec3eccf8821f",
    "source-statement-crosswalk.md": "9897486878f9266f65390ba2b6ef58f1a4a77417d71aec9a6e5ca89f6e1e3d81",
    "check_validation.sh": "1750a9d5c733a5d4c20818b3bb8d0c88287c0c566f3bdc1a0b18ddb99f86872b",
    "validation-spec.json": "7f3290732b49a313b18942484965e83734c71771853584bdf590c2444bc423c8",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
OPTIONAL_STOPPING_SOURCE = "Mathlib/Probability/Martingale/OptionalStopping.lean"
OPTIONAL_STOPPING_BLOB = "199f7399cc38d5c1c33e4be34c0933f40a216deb"
OPTIONAL_STOPPING_SHA256 = "a9bfa392263b80af96da9b547d36f5bef1342bb86054a7a973fb90a6597011c9"
OPTIONAL_STOPPING_OLEAN_SHA256 = "0aa93d0c78aa37415c4e9124faeaa35b4a3ca01ee892cbbb83efd416a8b8a2e3"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
UPSTREAM_REVISION = "4b63335c679c15aab74a00d37714d41aa99d701d"
UPSTREAM_RAW_SHA256 = "0a23b4378b723fb19080d259ead92fca5eade70c64a76205581cf83ab88f9706"
UPSTREAM_BLOB = "c7750503d8ec2a973e6ab0655c1f43f5b122b8c2"
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/check_validation.sh",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
SUMMARY_LINES = (
    "PASS THM-M-1005 narrow validation",
    "PASS kernel replay: exact statement, vendored analytic body, proof root, frozen composition, and differential root elaborated under network isolation",
    "PASS trust observation: checked roots use exactly propext, Classical.choice, and Quot.sound and are transitively sorry-free",
    "PASS selected provenance: frozen hashes, vendored/upstream identities, pinned source/blob/olean, clean mathlib pin, license, and tool identities agree",
    "PASS hygiene: parser-aware Lean checks plus a supplemental comment-stripped prohibited-construct scan passed",
    "FAIL CLOSED authority: proof master acceptance and conflicting M4/M3 structured state require master reconciliation; accepted root is conservatively H2/M4/R4",
    "FAIL CLOSED trust: M1005-S-FOUNDATION, a complete transitive declaration/TCB/SBOM closure, and accepted foundation policy remain open",
    "FAIL CLOSED hermetic/independent: shared warm .lake and same-worker differential transport are neither cold offline replay nor distinct signed verification",
    "audit_complete=false; theorem_complete=false",
)
TIMEOUT_SECONDS = 300.0


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=TIMEOUT_SECONDS,
        check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"command failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).stdout.strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    targets = load(ROOT / "Docs/Stage1_Targets_rev-5.6.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    frozen_specs = load(HERE / "validation-specs.json")
    proof_receipt = load(HERE / "proof-receipt.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 285 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 285,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-1005-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-1005-PROOF")
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-1005-PROOF"]

    assert instance["root_vector"] == {"H": "H2", "M": "M4", "R": "R4"}
    assert instance["accepted_proof_state"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["closed_obligations"] == ["M1005-S-DEFINITIONS", "M1005-T-ROOT-TRANSPORT"]
    assert closure["theorem_complete"] is False
    assert proof_receipt["debt_vector"]["accepted_after_worker_selftest"] == {
        "H": "H2", "M": "M3", "R": "R4",
    }

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_1005.Statement"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert anchor["audited_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256

    assert proof_receipt["statement_fingerprints"]["canonical_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["statement_fingerprints"]["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["proof_body"]["vendored_source_sha256"] == EXPECTED_INPUTS["DoobLp.lean"]
    assert proof_receipt["proof_body"]["upstream_revision"] == UPSTREAM_REVISION
    assert proof_receipt["proof_body"]["upstream_raw_sha256"] == UPSTREAM_RAW_SHA256
    assert proof_receipt["proof_body"]["upstream_git_blob"] == UPSTREAM_BLOB
    assert proof_receipt["proof_body"]["upstream_status"] == (
        "closed_unmerged_submission_labeled_llm_generated_without_mathlib_acceptance"
    )
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["open_proof_or_release_boundaries"] == [
        "M1005-S-FOUNDATION", "M1005-X-SOURCE",
    ]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOMS
    assert proof_receipt["accepted"] is False and proof_receipt["result"]["theorem_complete"] is False
    assert proof_receipt["validation_results"] and all(
        row["exit_code"] == 0 for row in proof_receipt["validation_results"]
    )
    proof_phase_text = (HERE / "proof-validation.md").read_text(encoding="utf-8")
    assert "cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-1005/check_proof.sh" in proof_phase_text
    assert "all six axiom reports were exactly" in proof_phase_text

    assert frozen_specs["item_id"] == "S56-M-1005-OBLIGATION_TREE"
    assert all(row["network_policy"] == "denied" for row in frozen_specs["recipes"])
    assert all(row["argv"][-1].endswith("check_obligation_tree.py") for row in frozen_specs["recipes"])

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in ("Statement.lean", "ObligationTree.lean", "DoobLp.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    differential = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    for forbidden in (
        "import Proof", "import ObligationTree", "Proof.", "root_of_strongDoobTerminal",
        "doobLpMomentEstimate_via_frozen_composition",
    ):
        assert forbidden not in differential, forbidden
    assert "MeasureTheory.maximal_ineq_Lp" in differential
    assert "assert_no_sorry independentlyReconstructedDoobLpMomentEstimate" in differential

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    optional_source = MATHLIB / OPTIONAL_STOPPING_SOURCE
    optional_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/Probability/Martingale/OptionalStopping.olean"
    assert git("rev-parse", f"HEAD:{OPTIONAL_STOPPING_SOURCE}", cwd=MATHLIB) == OPTIONAL_STOPPING_BLOB
    assert sha256(optional_source) == OPTIONAL_STOPPING_SHA256
    assert sha256(optional_olean) == OPTIONAL_STOPPING_OLEAN_SHA256
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256

    lean = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).stdout.strip())
    lake = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).stdout.strip())
    python = Path(os.path.realpath(os.sys.executable))
    git_path = shutil.which("git")
    bwrap_path = shutil.which("bwrap")
    assert git_path is not None and bwrap_path is not None
    assert LEAN_COMMIT in run([str(lean), "--version"]).stdout
    assert "5.0.0-src+98dc76e" in run([str(lake), "--version"]).stdout
    assert sha256(lean) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(lake) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert sha256(python) == "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
    assert sha256(Path(os.path.realpath(git_path))) == "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
    assert sha256(Path(os.path.realpath(bwrap_path))) == "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"

    runner = run(["bash", str(HERE / "check_validation.sh")]).stdout
    assert hashlib.sha256(runner.encode()).hexdigest() == EXPECTED_RUNNER_STDOUT_SHA256
    assert runner.splitlines() == [
        "PASS THM-M-1005 network-isolated narrow kernel replay",
        "PASS exact proof and differential roots: propext, Classical.choice, Quot.sound",
        "PASS transitive sorry check: vendored terminal and differential root are sorry-free",
    ]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 300
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "unshared network namespace" in spec["network_enforcement"]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-1005-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False and receipt["content_addressed_release_evidence"] is False
    assert receipt["covered_obligation_ids"] == spec["covered_obligation_ids"]
    assert receipt["accepted_closed_obligation_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["inputs"]["worker_packet"] == sha256(ROOT / ".stage1-worker-selftest.json")
    assert receipt["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_1005.Statement",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    assert receipt["result"]["kernel_replay"] == "provisional_pass"
    assert receipt["result"]["network_isolated_lean_replay"] == "pass"
    assert receipt["result"]["observed_axioms"] == EXPECTED_AXIOMS
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["root_vector_before"] == {"H": "H2", "M": "M4", "R": "R4"}
    assert receipt["root_vector_after_worker_selftest"] == receipt["root_vector_before"]
    assert receipt["first_failed_gate"] == "dependency.S56-M-1005-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert set(receipt["changed_paths"]) == CHANGED_PATHS

    assert packet == {
        "item_id": ITEM,
        "changed_paths": receipt["changed_paths"],
        "commands": receipt["worker_commands"],
        "output_summary": "\n".join(SUMMARY_LINES),
        "base_revision": BASE_REVISION,
        "known_failures": receipt["known_failures"],
        "state": "[_]",
    }
    actual_changes = {
        line[3:] for line in git("status", "--short", "--untracked-files=all").splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for path in CHANGED_PATHS:
        assert_text_hygiene(ROOT / path)

    assert receipt["output_evidence"]["stdout_semantic_sha256"] == hashlib.sha256(
        ("\n".join(SUMMARY_LINES) + "\n").encode()
    ).hexdigest()
    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
