#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0741-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0741"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0741-VALIDATION"
THEOREM = "THM-M-0741"
BASE_REVISION = "b243ebc0f9058ba5afafef8240b92c2dfb2edc6e"
BASE_TREE = "b4b092069141ac54ea1ab5a6ea946192a30ec78c"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "1a96ad274a14ef0c7285734258d28a7ff6e49febe1470bfbb957d757a92e718c"
DENOMINATOR_SHA256 = "ee9b5029b7cb4a820132e16aeeb1a5c6e304e81bb8624f0f931aee9547cb9bcd"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
MACHINE_IDS = [
    "M0741-ROOT",
    "M0741-N-FIXED-ZERO",
    "M0741-C-PAIR-ZERO",
    "M0741-L-RESTRICT",
    "M0741-X-FIXED-HALTING",
    "M0741-X-RICE",
    "M0741-B-FIXED-WITNESSES",
]
EXPECTED_INPUTS = {
    "Statement.lean": "79e8f14fa5219760ef0fa3b26c95ebe40916f0ed2881a6491fce36944398d4c7",
    "ObligationTree.lean": "aa51e74a13003408b26ab1fada33e28705a0ff4f7a3bc20e6afd4a2d8b8222a4",
    "Proof.lean": "85b043bac9d0f3e7154f98eebacca0d764dfc2e9e81ca95bc6c1d6b5875cb432",
    "Validation.lean": "35657f623af70ac75b0d17e1034ef98aee0bfbfd4bbeefceb3546ed12ead5a73",
    "statement.json": "23b9c4d94ad0ded786b532ebd5bb75de1ad7160f87cdd242a9dd145772a2ccf3",
    "instance.json": "379dac76912dd9fad9591e3286a18b08d0e2134ac0711b03828cab3c1a96e63e",
    "task-dag.json": "9720f893b30b37381f765d908f6fd75d05d5b1e1ad92a1b8c2cfd1dc6d3bb90b",
    "anchor-audit.json": "96b2f1874d80a96e4e4443466a80110262c4665ee99611545bc36a1a2f60360c",
    "obligation-registry.json": "8183bd5438235801fce2169bb2379653b4f16d0ce374160d793782e96fc819a5",
    "typed-graphs.json": "21a5f7a010d5c98376f125c9bc8d0f8651a849f9332d7459023de773f856dc44",
    "validation-specs.json": "05eedca770941f25fe0b61a7d1e8beecc5452ce89d56103cb0e4feb8df922b4c",
    "proof-receipt.json": "4edd83103df2c49d9d30c0dab32eb8ce3046776288728c2082eed481952afd4b",
    "check_validation.sh": "d748156527cd3fb35a905bde4a762acbe5ec7c510565aa10cfbd3acc1ab48204",
    "validation-spec.json": "472a43468fd2f8ab2e216e1da6060eec8ae041cd19e9b66d622d8f8c756f0629",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
TERMINAL_SOURCE = "Mathlib/Computability/Halting.lean"
TERMINAL_SOURCE_BLOB = "0834371356762db805d37208b9cf8a1fc0efd217"
TERMINAL_SOURCE_SHA256 = "c2a073a05c631e7fc957577a66025e9ac36dac741f9aa865e0f053b17f0c85de"
TERMINAL_OLEAN_SHA256 = "a4d0f485725fd93028f52418d4c5b6251cbd59cececed2b4ff1f4ac5578a61ba"
RICE_BODY_SHA256 = "7b1ffed124cbbab29edb690e35fedff63aabb101470802ee0d2dbf8c8fd4f7a1"
HALTING_BODY_SHA256 = "c79df2fcf31c93fe6ac57f179d2b03c41416baa313d68b9bbe76dc3499c5d41d"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
PROOF_DECLARATIONS = (
    "ComputablePred.rice",
    "ComputablePred.halting_problem",
    "Stage1Instances.THM_M_0741.Proof.riceBridge_pinned",
    "Stage1Instances.THM_M_0741.Proof.fixedInputZeroUndecidable_via_rice",
    "Stage1Instances.THM_M_0741.Proof.fixedInputZeroUndecidable_pinned",
    "Stage1Instances.THM_M_0741.Proof.fixedInputReduction_checked",
    "Stage1Instances.THM_M_0741.Proof.haltingProblemUndecidable",
    "Stage1Instances.THM_M_0741.Proof.haltingProblemUndecidable_via_rice",
)
COMPOSITION_DECLARATIONS = (
    "Stage1Instances.THM_M_0741.ObligationTree.pairZeroEmbedding_computable",
    "Stage1Instances.THM_M_0741.ObligationTree.pairToFixedRestriction_of_embedding",
    "Stage1Instances.THM_M_0741.ObligationTree.fixedInputReduction_of_restriction",
    "Stage1Instances.THM_M_0741.ObligationTree.fixedZeroWitnessPackage",
    "Stage1Instances.THM_M_0741.ObligationTree.fixedInputZeroUndecidable_of_rice",
    "Stage1Instances.THM_M_0741.ObligationTree.root_of_reduction_and_fixedInput",
)
DIFFERENTIAL_DECLARATION = (
    "Stage1Instances.THM_M_0741.Validation."
    "independentlyReconstructedHaltingProblemUndecidable"
)
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
    "PASS THM-M-0741 narrow validation",
    "PASS network-isolated kernel replay: exact statement, six frozen compositions, two proof roots, and input-one differential root elaborated",
    "PASS trust observation: ten proof and validation declarations report exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, terminal source/blob/body/olean, clean mathlib pin, remote, license, and tools agree",
    "PASS hygiene and architecture: Lean sorry reports, local prohibited scan, and frozen proof graph agree",
    "FAIL CLOSED authority/trust: proof master acceptance and complete foundation, provenance, and TCB closure remain open at H1/M3/R4",
    "FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout empty-cache bootstrap, offline restoration, or a deterministic TCB/SBOM bundle",
    "FAIL CLOSED independent release: differential input-one proof used this worker and shared cache, not a distinct signed verifier",
    "audit_complete=false; theorem_complete=false",
)
VALIDATION_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 180.0


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_lines(path: Path, start: int, end: int) -> str:
    lines = path.read_bytes().splitlines(keepends=True)
    return hashlib.sha256(b"".join(lines[start - 1 : end])).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - VALIDATION_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 180-second wall-clock bound")
    result = subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=remaining,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
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
    assert match is not None, (declaration, output)
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


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
    proof_receipt = load(HERE / "proof-receipt.json")
    frozen_specs = load(HERE / "validation-specs.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    target = next(row for row in targets["targets"] if row["theorem_id"] == THEOREM)
    assert target["execution_rank"] == 1329 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1329,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0741-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0741-PROOF"
    )
    assert predecessor["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0741-PROOF"]

    assert instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0741.HaltingProblemUndecidable"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert anchor["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["provisionally_closed_proof_obligation_ids"] == MACHINE_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["proof_graph_composition"]["all_required_proof_edges_consumed"] is True
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOM_LIST
    assert proof_receipt["accepted"] is False
    assert frozen_specs["item_id"] == "S56-M-0741-OBLIGATION_TREE"

    proof_pairs = {
        (edge["from"], edge["to"])
        for edge in graphs["graphs"]["proof"]["edges"]
        if edge["type"] == "proof_requires"
    }
    assert proof_pairs == {
        ("M0741-ROOT", "M0741-N-FIXED-ZERO"),
        ("M0741-ROOT", "M0741-X-FIXED-HALTING"),
        ("M0741-N-FIXED-ZERO", "M0741-L-RESTRICT"),
        ("M0741-L-RESTRICT", "M0741-C-PAIR-ZERO"),
        ("M0741-X-FIXED-HALTING", "M0741-X-RICE"),
        ("M0741-X-FIXED-HALTING", "M0741-B-FIXED-WITNESSES"),
    }

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
    differential = code_without_comments((HERE / "Validation.lean").read_text(encoding="utf-8"))
    for forbidden in (
        "import Proof",
        "import ObligationTree",
        "Proof.",
        "fixedInputReduction_checked",
        "haltingProblemUndecidable_via_rice",
    ):
        assert forbidden not in differential, forbidden
    assert "ComputablePred.halting_problem 1" in differential
    assert "Computable.const 1" in differential
    assert "assert_no_sorry independentlyReconstructedHaltingProblemUndecidable" in differential

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    terminal_source = MATHLIB / TERMINAL_SOURCE
    terminal_olean = (
        MATHLIB / ".lake/build/lib/lean/Mathlib/Computability/Halting.olean"
    )
    assert git("rev-parse", f"HEAD:{TERMINAL_SOURCE}", cwd=MATHLIB) == TERMINAL_SOURCE_BLOB
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert sha256_lines(terminal_source, 208, 218) == RICE_BODY_SHA256
    assert sha256_lines(terminal_source, 240, 242) == HALTING_BODY_SHA256
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256
    terminal_region = b"".join(
        terminal_source.read_bytes().splitlines(keepends=True)[207:242]
    ).decode("utf-8")
    assert prohibited.search(code_without_comments(terminal_region)) is None

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    lake_version = run(["lake", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in lake_version
    python = Path(os.path.realpath(os.sys.executable))
    git_path = shutil.which("git")
    bwrap = shutil.which("bwrap")
    assert git_path is not None and bwrap is not None
    assert sha256(Path(lean)) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(Path(lake)) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert sha256(python) == "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
    assert sha256(Path(os.path.realpath(git_path))) == (
        "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
    )
    assert sha256(Path(os.path.realpath(bwrap))) == (
        "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
    )

    runner_output = run(["bash", str(HERE / "check_validation.sh")])
    for declaration in PROOF_DECLARATIONS:
        assert printed_axioms(runner_output, declaration) == EXPECTED_AXIOMS
    assert printed_axioms(runner_output, DIFFERENTIAL_DECLARATION) == EXPECTED_AXIOMS
    assert runner_output.count("Declarations are sorry-free!") == 10
    assert "sorryAx" not in runner_output and "declaration uses 'sorry'" not in runner_output

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 180
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == MACHINE_IDS
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact nine-line PASS/FAIL-CLOSED status summary",
    }]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-0741-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(
        HERE / "check_validation.py"
    )
    assert receipt["inputs"]["validation-phase.md"] == sha256(
        HERE / "validation-phase.md"
    )
    assert receipt["inputs"]["worker_packet"] == sha256(
        ROOT / ".stage1-worker-selftest.json"
    )
    assert receipt["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_0741.HaltingProblemUndecidable",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    environment = receipt["environment"]
    assert environment["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert environment["lean_executable_sha256"] == sha256(Path(lean))
    assert environment["lake_executable_sha256"] == sha256(Path(lake))
    assert environment["python_executable_sha256"] == sha256(python)
    assert environment["git_executable_sha256"] == sha256(Path(os.path.realpath(git_path)))
    assert environment["bubblewrap_executable_sha256"] == sha256(
        Path(os.path.realpath(bwrap))
    )
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    provenance = receipt["provenance"]
    origin = provenance["origin"]
    assert origin["remote"] == MATHLIB_REMOTE
    assert origin["revision"] == MATHLIB_REVISION and origin["tree_hash"] == MATHLIB_TREE
    assert origin["file"] == TERMINAL_SOURCE
    assert origin["source_blob"] == TERMINAL_SOURCE_BLOB
    assert origin["source_sha256"] == TERMINAL_SOURCE_SHA256
    assert origin["olean_sha256"] == TERMINAL_OLEAN_SHA256
    assert provenance["terminal_body_identities"] == {
        "ComputablePred.rice:lines-208-218": f"sha256:{RICE_BODY_SHA256}",
        "ComputablePred.halting_problem:lines-240-242": f"sha256:{HALTING_BODY_SHA256}",
    }
    assert provenance["license_sha256"] == LICENSE_SHA256
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    result = receipt["result"]
    assert result["exact_root_kernel_replay"] == "provisional_pass"
    assert result["differential_exact_root_replay"] == "provisional_pass_same_worker"
    assert result["observed_axioms"] == EXPECTED_AXIOM_LIST
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["selected_provenance"] == "pass"
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_root_closed"] is False
    assert result["foundation_and_complete_trust_closure"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0741-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    phase_notes = (HERE / "validation-phase.md").read_text(encoding="utf-8")
    assert "theorem completion are false" in phase_notes
    assert "differential same-worker" in phase_notes
    assert "empty-cache cold bootstrap" in phase_notes
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
