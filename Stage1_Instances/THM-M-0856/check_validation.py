#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0856-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0856-VALIDATION"
THEOREM = "THM-M-0856"
BASE_REVISION = "9d50d838c8132b2aaf005a4863baeb5385e52a97"
BASE_TREE = "ef268baf236c1fe55806a57847c7f78ed6587b9d"
EXPRESSION_SHA256 = "5364250d1d4e132aaf1d5ce8ad5425369546963189991202f49b2fcf65095bae"
DENOMINATOR_SHA256 = "9d6a920afceb2d2c42ce432e12008329977aa733eecb42c28ed2c44686aca20c"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
TERMINAL_SOURCE = "Mathlib/Combinatorics/SimpleGraph/Tutte.lean"
TERMINAL_SOURCE_BLOB = "4b7931e61e4dd6a3aae37fcecf698ddc238fbc4e"
TERMINAL_SOURCE_SHA256 = "47072b914aa564222ef8013092c38fa62227fea8230e308cc3eb5f11afcdffc3"
TERMINAL_BODY_SHA256 = "424b3cde58e3407307ef398cd52eeaf2a7ce122fd5049275745c445aceeac132"
TERMINAL_OLEAN_SHA256 = "d0669fb8cd3a48f382490d39a102c7033f7a81e9582d09bda2c2ae172ff399ee"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
EXPECTED_INPUTS = {
    "Statement.lean": "cd7ec3e97a02ccc24578de4431a1a8ebf0e9572f9616b271b67f145d72fbedce",
    "ObligationTree.lean": "752c07615d8402e96dcee57945aa971acca58ba827b1094c534f104ad0bf1c15",
    "Proof.lean": "93ccd4e6dbfe926a21ee0648421bc456dc2f7e2a8cae02b629001a807556938d",
    "Validation.lean": "cd0127cf621f5e8ef922b7a8e04e797f76295d337056a27fd06cade6b33dabb9",
    "statement.json": "476e6f5d9570153e7a30fc15e9c5487fd1ce02dc7a192dcbf5b01ffc8c7f3fb6",
    "instance.json": "3c4a74c095da5ac0d0fa5e071ae960f46fb4a2e4d4f79e5f2d0a5f40ad37cdfd",
    "task-dag.json": "585a5b9781eb0dcfb6e4012f6905f69a9c65e17cbf0a422dc7adef7fce0c68cc",
    "anchor-audit.json": "b95fa97389e8349527c9e0476e4eeb6cbe44e39f1b34fd639dc092929728fcce",
    "obligation-registry.json": "58d63b99f758183dae5aad4ffe7c4b35a1c3e3c54292faa254e2b98b5701c5d6",
    "typed-graphs.json": "ca937f1acd688e122ebdb307fc16e2326add0c51f9d0f169dc018179a7ad54ff",
    "validation-specs.json": "fbc84f3ad1ed7927a99e9d2db2b019b681ff236e45290828a9cbf0a0c852571b",
    "proof-receipt.json": "1db25f6c6c46c90a164cc980b8346e7d3fafd4e3c4f5fac4855d489a4b7886f1",
    "check_validation.sh": "197490aad3e762ec8a0e52dff9b25a1c3fd8f93a1fd2830d3fd9d0c327526341",
    "validation-spec.json": "aae20f1254cf922b6266960a06bdad8856fe71bb11511e5cd86478e0777d0868",
    "validation-phase.md": "86ab3ea5beda4f0b2d2dbc8c0ebc903a24ab3433b5cbf953a46bc43622e329ef",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EXPECTED_TOOL_HASHES = {
    "lean": "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf",
    "lake": "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359",
    "python": "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700",
    "git": "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45",
    "bubblewrap": "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0",
}
KERNEL_OUTPUT_SHA256 = "d68efcd7d6a83b769b857c96179fdf7f9be3d161c438e9f5b251690b06b5ac84"
KERNEL_OUTPUT_BYTES = 3006
RECIPE_OUTPUT_SHA256 = "9ee0e273e3a14a918a39712b361aa6b739194ec069be88d8e420aee1e0d2bb0f"
RECIPE_OUTPUT_BYTES = 985
EMPTY_OUTPUT_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
PROOF_RECIPE_OUTPUT_SHA256 = "d590c80efda1900056c6c889dba2db6be6df6ae6966ff9959106a8406ba53274"
PROOF_RECIPE_OUTPUT_BYTES = 804
OBLIGATION_RECIPE_OUTPUT_SHA256 = "b9cc3057c2c410a6a78ce32f9186438e9f34b5358e66e1302f76cb67a2948122"
OBLIGATION_RECIPE_OUTPUT_BYTES = 606
GENERATOR_RECIPE_OUTPUT_SHA256 = "a74785778a5be59739c07e1201664af54c66af4879d5eed4ec48f1aaeec88195"
GENERATOR_RECIPE_OUTPUT_BYTES = 44
MACHINE_IDS = ["M0856-ROOT", "M0856-T-UPSTREAM", "M0856-T-ADAPTER"]
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
    "PASS THM-M-0856 narrow validation",
    "PASS network-isolated kernel replay: exact statement, root composition, proof roots, and differential exact root elaborated",
    "PASS trust observation: proof and differential roots report exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, terminal source/blob/body/olean, clean mathlib pin, remote, license, and tools agree",
    "PASS hygiene and architecture: Lean sorry reports, local prohibited scan, 44 reachable IDs, and 16 unverified compositions agree",
    "FAIL CLOSED authority/trust: proof master acceptance and complete transitive foundation, provenance, and TCB closure remain open at H1/M3/R4",
    "FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout empty-cache bootstrap, offline restoration, or a deterministic TCB/SBOM bundle",
    "FAIL CLOSED independent release: differential reconstruction used this worker and shared cache, not a distinct signed verifier",
    "audit_complete=false; theorem_complete=false",
)


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
    result = run_result(argv, cwd=cwd)
    if result.returncode != 0:
        raise RuntimeError(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def run_result(argv: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )


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
    assert os.environ.get("STAGE1_NETWORK_ISOLATED") == "1", (
        "run the recorded recipe through check_validation.sh"
    )
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
    assert target["execution_rank"] == 1410 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1410,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0856-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(row for row in execution["items"] if row["id"] == "S56-M-0856-PROOF")
    assert predecessor["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0856-PROOF"]

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
    assert formal["declaration_or_expression"] == "Stage1Instances.THM_M_0856.TutteOneFactorTarget"
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert anchor["canonical_target"]["expression_sha256"] == EXPRESSION_SHA256
    assert anchor["canonical_target"]["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    candidate = next(
        row for row in anchor["candidates"]
        if row["candidate_id"] == "M0856-C02-PINNED-MATHLIB-TUTTE"
    )
    assert candidate["remote"] == MATHLIB_REMOTE
    assert candidate["revision"] == MATHLIB_REVISION and candidate["tree"] == MATHLIB_TREE
    assert candidate["file"] == TERMINAL_SOURCE
    assert candidate["file_sha256"] == TERMINAL_SOURCE_SHA256
    assert candidate["kernel_checked"] is True and candidate["accepted"] is False
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert len(registry["obligations"]) == 56
    assert len(registry["frozen_denominators"]["required_machine"]) == 44
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    root_evidence = proof_receipt["root_evidence"]
    assert root_evidence["root_kernel_declaration_closed"] is True
    assert root_evidence["accepted_root_closed"] is False
    assert root_evidence["machine_debt_proposal"] == "M0-W"
    assert root_evidence["accepted_closed_obligation_ids"] == []
    assert root_evidence["exact_declaration_evidence_ids"] == MACHINE_IDS
    assert root_evidence["mapped_proof_graph_id_count"] == 44
    assert root_evidence["internal_per_node_composition_credit"] is False
    assert root_evidence["unverified_internal_composition_count"] == 16
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOM_LIST
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert frozen_specs["item_id"] == "S56-M-0856-OBLIGATION_TREE"
    assert len(graphs["composition_certificates"]) == 1
    assert len(graphs["unverified_decomposition_plans"]) == 16
    assert graphs["composition_certificates"][0]["checked_declaration"].endswith("compose_root")
    proof_children: dict[str, list[str]] = {}
    for edge in graphs["graphs"]["proof"]["edges"]:
        if edge["type"] == "proof_requires":
            proof_children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()
    pending = ["M0856-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(proof_children.get(obligation, []))
    assert reachable == set(registry["frozen_denominators"]["required_machine"])

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
        "import Proof", "import ObligationTree", "Proof.", "compose_root",
        "terminal_adapter", "pinnedTerminal", "pinned_mathlib_terminal",
    ):
        assert forbidden not in differential, forbidden
    assert "SimpleGraph.tutte (G := G)" in differential
    assert "assert_no_sorry tutteOneFactor_differential" in differential

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == mathlib_entry["inputRev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    terminal_source = MATHLIB / TERMINAL_SOURCE
    terminal_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/Combinatorics/SimpleGraph/Tutte.olean"
    assert git("rev-parse", f"HEAD:{TERMINAL_SOURCE}", cwd=MATHLIB) == TERMINAL_SOURCE_BLOB
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert sha256_lines(terminal_source, 315, 322) == TERMINAL_BODY_SHA256
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256
    terminal_region = b"".join(
        terminal_source.read_bytes().splitlines(keepends=True)[314:322]
    ).decode("utf-8")
    assert prohibited.search(code_without_comments(terminal_region)) is None
    for marker in (
        "theorem tutte :", "not_isTutteViolator_of_isPerfectMatching hM",
        "by_cases hvOdd : Odd (Nat.card V)", "exact exists_isTutteViolator h",
    ):
        assert marker in terminal_source.read_text(encoding="utf-8")

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    assert "4.29.0" in run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "5.0.0-src+98dc76e" in run(["lake", "--version"], cwd=LEAN_ROOT)
    python = Path(os.path.realpath(os.sys.executable))
    git_path = shutil.which("git")
    bwrap = shutil.which("bwrap")
    assert git_path is not None and bwrap is not None
    assert sha256(Path(lean)) == EXPECTED_TOOL_HASHES["lean"]
    assert sha256(Path(lake)) == EXPECTED_TOOL_HASHES["lake"]
    assert sha256(python) == EXPECTED_TOOL_HASHES["python"]
    assert sha256(Path(os.path.realpath(git_path))) == EXPECTED_TOOL_HASHES["git"]
    assert sha256(Path(os.path.realpath(bwrap))) == EXPECTED_TOOL_HASHES["bubblewrap"]

    runner_output = run(["bash", str(HERE / "check_validation.sh"), "--lean-only"])
    runner_bytes = runner_output.encode("utf-8")
    assert hashlib.sha256(runner_bytes).hexdigest() == KERNEL_OUTPUT_SHA256
    assert len(runner_bytes) == KERNEL_OUTPUT_BYTES
    obligation_declarations = (
        "SimpleGraph.tutte",
        "Stage1Instances.THM_M_0856.ObligationTree.terminal_adapter",
        "Stage1Instances.THM_M_0856.ObligationTree.pinned_mathlib_terminal",
        "Stage1Instances.THM_M_0856.ObligationTree.compose_root",
    )
    proof_declarations = (
        "SimpleGraph.tutte",
        "Stage1Instances.THM_M_0856.Proof.pinnedTerminal",
        "Stage1Instances.THM_M_0856.Proof.tutteOneFactor_via_frozen_composition",
        "Stage1Instances.THM_M_0856.Proof.tutteOneFactor_direct",
    )
    differential_declarations = (
        "SimpleGraph.tutte",
        "Stage1Instances.THM_M_0856.Validation.tutteOneFactor_differential",
    )
    for declaration in obligation_declarations + proof_declarations + differential_declarations:
        assert printed_axioms(runner_output, declaration) == EXPECTED_AXIOMS
    assert runner_output.count("Declarations are sorry-free!") == 8
    assert "sorryAx" not in runner_output and "declaration uses 'sorry'" not in runner_output

    proof_replay = run_result(["bash", str(HERE / "check_proof.sh")])
    proof_bytes = proof_replay.stdout.encode("utf-8")
    assert proof_replay.returncode == 0
    assert len(proof_bytes) == PROOF_RECIPE_OUTPUT_BYTES
    assert hashlib.sha256(proof_bytes).hexdigest() == PROOF_RECIPE_OUTPUT_SHA256
    obligation_replay = run_result(["python3", "-B", str(HERE / "check_obligation_tree.py")])
    obligation_bytes = obligation_replay.stdout.encode("utf-8")
    assert obligation_replay.returncode == 1
    assert len(obligation_bytes) == OBLIGATION_RECIPE_OUTPUT_BYTES
    assert hashlib.sha256(obligation_bytes).hexdigest() == OBLIGATION_RECIPE_OUTPUT_SHA256
    assert "frozen_against_execution_dag_sha256" in obligation_replay.stdout
    generator_replay = run_result(
        ["python3", "-B", str(HERE / "build_obligation_artifacts.py"), "--check"]
    )
    generator_bytes = generator_replay.stdout.encode("utf-8")
    assert generator_replay.returncode == 1
    assert len(generator_bytes) == GENERATOR_RECIPE_OUTPUT_BYTES
    assert hashlib.sha256(generator_bytes).hexdigest() == GENERATOR_RECIPE_OUTPUT_SHA256
    assert generator_replay.stdout == "generated artifact drift: typed-graphs.json\n"

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == ["bash", f"Stage1_Instances/{THEOREM}/check_validation.sh"]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 180
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "bubblewrap --unshare-net" in spec["network_enforcement"]
    assert "entire recorded validation recipe" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == MACHINE_IDS
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact nine-line PASS/FAIL-CLOSED status summary",
    }]

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["verdict"] == "blocked"
    assert receipt["depends_on"] == ["S56-M-0856-PROOF"]
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    assert receipt["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert receipt["mapped_proof_graph_id_count"] == 44
    assert set(receipt["mapped_proof_graph_ids"]) == reachable
    assert receipt["validated_declarations"] == spec["covered_declarations"]
    assert receipt["root_vector_before"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert receipt["root_vector_after_worker_selftest"] == receipt["root_vector_before"]
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected, name
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["worker_packet"] == sha256(ROOT / ".stage1-worker-selftest.json")
    assert receipt["canonical_target"] == {
        "declaration": "Stage1Instances.THM_M_0856.TutteOneFactorTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    environment = receipt["environment"]
    assert environment["platform"] == f"{platform.system()} {platform.release()} {platform.machine()}"
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
        "SimpleGraph.tutte:lines-315-322": f"sha256:{TERMINAL_BODY_SHA256}",
    }
    assert receipt["provenance"]["license_sha256"] == LICENSE_SHA256
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key], key
    result = receipt["result"]
    assert result["exit_code"] == 0
    assert result["kernel_output_sha256"] == KERNEL_OUTPUT_SHA256
    assert result["kernel_output_bytes"] == KERNEL_OUTPUT_BYTES
    assert result["recipe_stdout_sha256"] == RECIPE_OUTPUT_SHA256
    assert result["recipe_stdout_bytes"] == RECIPE_OUTPUT_BYTES
    assert result["recipe_stderr_sha256"] == EMPTY_OUTPUT_SHA256
    assert result["recipe_stderr_bytes"] == 0
    assert result["exact_root_kernel_replay"] == "provisional_pass"
    assert result["differential_exact_root_replay"] == "provisional_pass_same_worker"
    assert result["observed_axioms"] == EXPECTED_AXIOM_LIST
    assert result["placeholder_and_unsafe_scan"] == "pass"
    assert result["selected_provenance"] == "pass"
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["recorded_proof_recipe"] == "pass"
    assert result["recorded_obligation_bundle_recipe"].startswith("fail_closed_exit_1")
    assert result["recorded_obligation_generator_recipe"].startswith("fail_closed_exit_1")
    assert result["proof_master_acceptance"] == "fail_closed"
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_root_closed"] is False
    assert result["unverified_internal_composition_count"] == 16
    assert result["internal_per_node_composition_credit"] is False
    assert result["foundation_and_complete_trust_closure"] == "fail_closed"
    assert result["hermetic_cold_offline_replay"] == "fail_closed"
    assert result["independent_distinct_runner"] == "fail_closed"
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0856-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert packet["commands"] == receipt["commands_and_results"]
    assert packet["output_summary"] == receipt["output_summary"]
    replay_commands = {tuple(row["argv"]): row for row in receipt["commands_and_results"]}
    proof_record = replay_commands[("bash", f"Stage1_Instances/{THEOREM}/check_proof.sh")]
    assert proof_record["exit_code"] == 0
    assert proof_record["stdout_and_stderr_sha256"] == PROOF_RECIPE_OUTPUT_SHA256
    obligation_record = replay_commands[
        ("python3", "-B", f"Stage1_Instances/{THEOREM}/check_obligation_tree.py")
    ]
    assert obligation_record["expected_exit"] == 0 and obligation_record["exit_code"] == 1
    assert obligation_record["stdout_and_stderr_sha256"] == OBLIGATION_RECIPE_OUTPUT_SHA256
    generator_record = replay_commands[
        (
            "python3", "-B",
            f"Stage1_Instances/{THEOREM}/build_obligation_artifacts.py", "--check",
        )
    ]
    assert generator_record["expected_exit"] == 0 and generator_record["exit_code"] == 1
    assert generator_record["stdout_sha256"] == GENERATOR_RECIPE_OUTPUT_SHA256
    status = git("status", "--short", "--untracked-files=all")
    actual_changed = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    phase_notes = (HERE / "validation-phase.md").read_text(encoding="utf-8")
    assert "theorem completion are false" in phase_notes
    assert "same-worker" in phase_notes and "empty-cache cold bootstrap" in phase_notes
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
