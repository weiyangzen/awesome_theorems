#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0821-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import time


if not __debug__:
    raise SystemExit("check_validation.py must run without Python optimization")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0821"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0821-VALIDATION"
THEOREM = "THM-M-0821"
BASE_REVISION = "4a10a7a4ddff88e302d5a303b16dd687d9468f63"
BASE_TREE = "730de242597680b39a7087d3204dfd1e6c41c60e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "8f5d05428a35e3b6f13947097ac52417ba900b3cf9b1b45c0bb173766c914d7c"
DENOMINATOR_SHA256 = "4ea4814dfb5bf3db63946381630ecfa30114c54515612c9e385fa660b53bbc75"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
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
MAPPED_PROOF_IDS = [
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
    "M0821-L-CHOOSE-MIDDLE",
    "M0821-L-LYM-INV",
    "M0821-N-FIBERWISE-SLICES",
    "M0821-L-LYM-CARD",
    "M0821-L-FALLING-TOP",
    "M0821-L-FALLING-ZERO",
    "M0821-C-FALLING",
    "M0821-B-FALLING-INDUCTION",
    "M0821-L-SLICE-SHADOW",
    "M0821-L-DISJOINT-SHADOW",
    "M0821-L-LOCAL-LYM",
    "M0821-L-LOCAL-LYM-MUL",
    "M0821-C-SHADOW",
    "M0821-L-DOUBLE-COUNT",
]
EXPECTED_INPUTS = {
    "Statement.lean": "572f1655ca4d40ce6e1ce1bf6567cee2d640eb54534569d8a8980dff184c0100",
    "ObligationTree.lean": "d223cad2f1f9c9ac3e54a5c423609c4816225276e697dfcdbfab97c8e9bdd00f",
    "Proof.lean": "0f366927737a83b07d7f90e399f5e0c6bc9254604efcad7d39d3c50f1468c444",
    "Validation.lean": "d49f638f7d994303b66bf8311baf062e13742afd120e0989eae18568147d4d28",
    "statement.json": "1bc0d5f7a002649ba47a12dea437a5950e01a95e443ab6468d0c0e4db19b78e2",
    "instance.json": "a01e6ac2e1245ec959c646e44fd2e540a6734458de9ad2dfa2862bbeecc1cc56",
    "task-dag.json": "f50166dce557e46e611c2ddb67bef5eb2da5dafb06e8912cf45f8a992b2bcbed",
    "anchor-audit.json": "050fae06052c03a8556804d2481e089ffb8e5095cd2baaf2b6e42ace5387c682",
    "obligation-registry.json": "16bc89dfe581930beb9d1aadc82e72ac4db3788702d1d6fc52712f6689ea2728",
    "typed-graphs.json": "dab4f84c604468a45db8cdd957e42c2301edfcc0d9fac3b04bb220736a041f77",
    "validation-specs.json": "22cf1d10a73b9b69ff728eb2995a05b5241702e77177e78f508ebaac0a3600cc",
    "proof-receipt.json": "42b5b31487cde5fb7b679e9386133709948fc0752e1993fe46af17c498ab56b0",
    "check_validation.sh": "a5eaba5132f169fc4211174ac7133ab6aff90082361746062b3230a24b7136b0",
    "validation-spec.json": "66209bc2d7606ef8071419d37a07142b9074303e2d9d4973962ac9e812e4c37c",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
TERMINAL_SOURCE = "Mathlib/Combinatorics/SetFamily/LYM.lean"
TERMINAL_SOURCE_BLOB = "0f52fe96b02566b3c69ce0fa6de36619cdbf6c9f"
TERMINAL_SOURCE_SHA256 = "b19d4cbe58af9422dc36864d1ad1eee717c264a90d94fd579d3c8305f0feb630"
TERMINAL_OLEAN_SHA256 = "d55fb20a47a998695477eb5503c15f4f3c2eafd82425c96e233245f814473f48"
SPERNER_BODY_SHA256 = "4c9d9bc094e21136e779721f051704dd842d997537f8ad5538b06f32b6559fe2"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
PROOF_DECLARATIONS = (
    "IsAntichain.sperner",
    "Stage1Instances.THM_M_0821.Proof.middleLayerAttainment",
    "Stage1Instances.THM_M_0821.Proof.universalUpperBound",
    "Stage1Instances.THM_M_0821.Proof.spernerMaximum",
)
COMPOSITION_DECLARATIONS = (
    "Stage1Instances.THM_M_0821_Obligations.root_of_terminal",
    "Stage1Instances.THM_M_0821_Obligations.compose_root",
    "Stage1Instances.THM_M_0821_Obligations.maximumSplit_of_packages",
    "Stage1Instances.THM_M_0821_Obligations.attainment_of_middleLayer",
    "Stage1Instances.THM_M_0821_Obligations.middleLayerAntichain_of_sized",
    "Stage1Instances.THM_M_0821_Obligations.upperBound_of_sperner",
)
DIFFERENTIAL_DECLARATION = (
    "Stage1Instances.THM_M_0821.Validation."
    "independentlyReconstructedSpernerMaximum"
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
    "PASS THM-M-0821 narrow validation",
    "PASS network-isolated kernel replay: exact statement, six frozen compositions, proof root, and differential exact root elaborated",
    "PASS trust observation: proof and differential roots report exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, terminal source/blob/body/olean, clean mathlib pin, remote, license, and tools agree",
    "PASS hygiene and architecture: Lean sorry reports, local prohibited scan, and frozen composition boundary agree",
    "FAIL CLOSED authority/trust: proof master acceptance and complete transitive foundation, provenance, and TCB closure remain open at H1/M3/R4",
    "FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout empty-cache bootstrap, offline restoration, or a deterministic TCB/SBOM bundle",
    "FAIL CLOSED independent release: differential reconstruction used this worker and shared cache, not a distinct signed verifier",
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
    assert match is not None, declaration
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
    assert target["execution_rank"] == 1379 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1379,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0821-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0821-PROOF"
    )
    assert predecessor["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0821-PROOF"]

    assert instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0821.SpernerMaximumTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert anchor["canonical_target"]["expression_sha256"] == EXPRESSION_SHA256
    assert anchor["canonical_target"]["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    candidate = next(
        row for row in anchor["candidates"]
        if row["candidate_id"] == "M0821-C01-MATHLIB-COMPOSITE"
    )
    assert candidate["remote"] == MATHLIB_REMOTE
    assert candidate["revision"] == MATHLIB_REVISION and candidate["tree"] == MATHLIB_TREE
    assert candidate["candidate_classification"] == "M0-W"
    assert candidate["evidence_level"] == "E2"
    assert candidate["kernel_checked"] is True and candidate["accepted"] is False
    lym_file = next(row for row in candidate["files"] if row["path"] == TERMINAL_SOURCE)
    assert lym_file == {
        "path": TERMINAL_SOURCE,
        "blob": TERMINAL_SOURCE_BLOB,
        "sha256": TERMINAL_SOURCE_SHA256,
    }
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert len(registry["obligations"]) == 36
    assert len(registry["frozen_denominators"]["required_machine"]) == 29
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    root_evidence = proof_receipt["root_evidence"]
    assert root_evidence["root_kernel_declaration_closed"] is True
    assert root_evidence["accepted_root_closed"] is False
    assert root_evidence["machine_debt_proposal"] == "M0-W"
    assert root_evidence["closed_obligation_ids"] == []
    assert root_evidence["exact_declaration_evidence_ids"] == MACHINE_IDS
    assert root_evidence["mapped_proof_graph_ids"] == MAPPED_PROOF_IDS
    assert root_evidence["mapped_proof_graph_id_count"] == len(MAPPED_PROOF_IDS)
    assert root_evidence["checked_composition_certificate_count"] == 6
    assert root_evidence["internal_per_node_composition_credit"] is False
    assert root_evidence["unverified_internal_composition_count"] == 8
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOM_LIST
    assert proof_receipt["result"]["accepted_state_changed"] is False
    assert frozen_specs["item_id"] == "S56-M-0821-OBLIGATION_TREE"
    assert len(graphs["composition_certificates"]) == 6
    assert len(graphs["unverified_decomposition_plans"]) == 8
    assert {row["checked_declaration"] for row in graphs["composition_certificates"]} == set(
        COMPOSITION_DECLARATIONS
    )
    proof_children: dict[str, list[str]] = {}
    for edge in graphs["graphs"]["proof"]["edges"]:
        if edge["type"] == "proof_requires":
            proof_children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()
    pending = ["M0821-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(proof_children.get(obligation, []))
    assert reachable == set(MAPPED_PROOF_IDS)

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
        "compose_root",
        "maximumSplit_of_packages",
        "middleLayerAttainment",
    ):
        assert forbidden not in differential, forbidden
    assert "Set.sized_powersetCard" in differential
    assert "exact hA.sperner" in differential
    assert "assert_no_sorry independentlyReconstructedSpernerMaximum" in differential

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    terminal_source = MATHLIB / TERMINAL_SOURCE
    terminal_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/Combinatorics/SetFamily/LYM.olean"
    assert git("rev-parse", f"HEAD:{TERMINAL_SOURCE}", cwd=MATHLIB) == TERMINAL_SOURCE_BLOB
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert sha256_lines(terminal_source, 234, 245) == SPERNER_BODY_SHA256
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256
    terminal_region = b"".join(
        terminal_source.read_bytes().splitlines(keepends=True)[233:245]
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
    runner_bytes = runner_output.encode("utf-8")
    assert hashlib.sha256(runner_bytes).hexdigest() == receipt["result"]["kernel_output_sha256"]
    assert len(runner_bytes) == receipt["result"]["kernel_output_bytes"]
    for declaration in COMPOSITION_DECLARATIONS:
        observed = printed_axioms(runner_output, declaration)
        assert observed and observed <= EXPECTED_AXIOMS, declaration
    for declaration in PROOF_DECLARATIONS:
        assert printed_axioms(runner_output, declaration) == EXPECTED_AXIOMS
    assert printed_axioms(runner_output, DIFFERENTIAL_DECLARATION) == EXPECTED_AXIOMS
    assert runner_output.count("Declarations are sorry-free!") == 8
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
    assert receipt["depends_on"] == ["S56-M-0821-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["mapped_proof_graph_ids"] == MAPPED_PROOF_IDS
    assert receipt["validated_declarations"] == spec["covered_declarations"]
    assert receipt["root_vector_before"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert receipt["root_vector_after_worker_selftest"] == receipt["root_vector_before"]
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["inputs"]["worker_packet"] == sha256(ROOT / ".stage1-worker-selftest.json")
    assert receipt["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_0821.SpernerMaximumTarget",
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
    assert environment["bubblewrap_executable_sha256"] == sha256(Path(os.path.realpath(bwrap)))
    assert environment["mathlib_revision"] == MATHLIB_REVISION
    assert environment["mathlib_tree"] == MATHLIB_TREE
    origin = receipt["provenance"]["origin"]
    assert origin["remote"] == MATHLIB_REMOTE
    assert origin["revision"] == MATHLIB_REVISION and origin["tree_hash"] == MATHLIB_TREE
    assert origin["file"] == TERMINAL_SOURCE
    assert origin["source_blob"] == TERMINAL_SOURCE_BLOB
    assert origin["source_sha256"] == TERMINAL_SOURCE_SHA256
    assert origin["olean_sha256"] == TERMINAL_OLEAN_SHA256
    assert receipt["provenance"]["terminal_body_identities"] == {
        "IsAntichain.sperner:lines-234-245": f"sha256:{SPERNER_BODY_SHA256}",
    }
    assert receipt["provenance"]["license_sha256"] == LICENSE_SHA256
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit",
        "expected_outputs", "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    result = receipt["result"]
    assert result["exit_code"] == 0
    assert result["exact_root_kernel_replay"] == "provisional_pass"
    assert result["differential_exact_root_replay"] == "provisional_pass_same_worker"
    assert result["observed_axioms"] == EXPECTED_AXIOM_LIST
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["selected_provenance"] == "pass"
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_root_closed"] is False
    assert result["unverified_internal_composition_count"] == 8
    assert result["internal_per_node_composition_credit"] is False
    assert result["foundation_and_complete_trust_closure"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0821-PROOF.master_acceptance"
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
    assert "same-worker differential" in phase_notes
    assert "empty-cache cold bootstrap" in phase_notes
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
