#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0822-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import time


if not __debug__:
    raise SystemExit("check_validation.py must run without Python optimization")


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0822"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0822-VALIDATION"
THEOREM = "THM-M-0822"
BASE_REVISION = "5b35bc151522d93c7f54966ef64f1fc630371537"
BASE_TREE = "fe77824631ab2573a4596bddc1a2534c06cd23f8"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "646e9860afcf5efd962b6f69c9c2825220f23418d05f7675490b783e63afe209"
DENOMINATOR_SHA256 = "40ff944c9434231f2656a60ff306e27b69ef6fe302df8dc1bd56f89d314a8f15"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
MACHINE_IDS = [
    "M0822-ROOT",
    "M0822-T-ASSEMBLE",
    "M0822-T-ATTAINMENT",
    "M0822-C-STAR",
    "M0822-L-STAR-IMAGE",
    "M0822-L-STAR-INTERSECTING",
    "M0822-L-STAR-SIZED",
    "M0822-L-STAR-CARD",
    "M0822-L-GROUND-ELEMENT",
    "M0822-T-UPPER-ADAPTER",
    "M0822-T-MATHLIB-EKR",
]
PROOF_REQUIRES = {
    ("M0822-ROOT", "M0822-T-ASSEMBLE"),
    ("M0822-T-ASSEMBLE", "M0822-T-ATTAINMENT"),
    ("M0822-T-ASSEMBLE", "M0822-T-UPPER-ADAPTER"),
    ("M0822-T-ATTAINMENT", "M0822-C-STAR"),
    ("M0822-T-ATTAINMENT", "M0822-L-STAR-INTERSECTING"),
    ("M0822-T-ATTAINMENT", "M0822-L-STAR-SIZED"),
    ("M0822-T-ATTAINMENT", "M0822-L-STAR-CARD"),
    ("M0822-C-STAR", "M0822-L-GROUND-ELEMENT"),
    ("M0822-L-STAR-CARD", "M0822-L-STAR-IMAGE"),
    ("M0822-T-UPPER-ADAPTER", "M0822-T-MATHLIB-EKR"),
}
COMPOSITION_DECLARATIONS = {
    "M0822-ROOT": "Stage1Instances.THM_M_0822.ObligationTree.rootOfExactAssembly",
    "M0822-T-ASSEMBLE": "Stage1Instances.THM_M_0822.ObligationTree.composeRoot",
    "M0822-T-ATTAINMENT": (
        "Stage1Instances.THM_M_0822.ObligationTree.attainment_of_starPackages"
    ),
    "M0822-C-STAR": (
        "Stage1Instances.THM_M_0822.ObligationTree.starConstruction_of_groundElement"
    ),
    "M0822-L-STAR-CARD": (
        "Stage1Instances.THM_M_0822.ObligationTree.starCard_of_image"
    ),
    "M0822-T-UPPER-ADAPTER": (
        "Stage1Instances.THM_M_0822.ObligationTree.upperBound_of_mathlibTerminal"
    ),
}
PROOF_DECLARATIONS = (
    "Finset.erdos_ko_rado",
    "Stage1Instances.THM_M_0822.Proof.groundElement",
    "Stage1Instances.THM_M_0822.Proof.starConstruction",
    "Stage1Instances.THM_M_0822.Proof.starImage",
    "Stage1Instances.THM_M_0822.Proof.starIntersecting",
    "Stage1Instances.THM_M_0822.Proof.starSized",
    "Stage1Instances.THM_M_0822.Proof.starCard",
    "Stage1Instances.THM_M_0822.Proof.starAttainment",
    "Stage1Instances.THM_M_0822.Proof.mathlibUpperBound",
    "Stage1Instances.THM_M_0822.Proof.universalUpperBound",
    "Stage1Instances.THM_M_0822.Proof.exactAssembly",
    "Stage1Instances.THM_M_0822.Proof.erdosKoRadoMaximum",
)
VALIDATION_ROOT_DECLARATION = (
    "Stage1Instances.THM_M_0822.Proof.erdosKoRadoMaximum"
)
EXPECTED_INPUTS = {
    "Statement.lean": "b91d0fce7cd10a12585860b11af519cbe7496f555d04a751d5b4b6309309582d",
    "ObligationTree.lean": "2a1b89b25537b105eaba06fcf100fe6811b1f29470282ae24c469f4467322696",
    "Proof.lean": "1fe64b97e021ac3a3a817bf6d24af075ecdf5f7a61fc056b773d2bfc9e74cb01",
    "Validation.lean": "9654759e0988696850a6f0acd1db06ebef3a04a4895731125086032b49e3e72b",
    "statement.json": "07c9d2c949841df151a02d23b5bb568a64f299e8728910961070c93acec82b42",
    "instance.json": "76eb233e115a86db5d5916e4be794485273bc5a13f0714bda5ce9994dd2447d8",
    "task-dag.json": "7ee08eb684996c3f46a8f3c4bf2b066199a5a42faff56ec7975d066e6a5212b4",
    "anchor-audit.json": "380c1d6f3e10084bc82f24fca8a881a12fdc4794885b2e3f1ff7b5fd7985afee",
    "obligation-registry.json": "57d38c8d20bc4c8615707d52c7e30b18f0976af68cb1eed0a95a2e88de82e716",
    "typed-graphs.json": "2b4ad3930023606c4f25a07fa2c8c11908d396de19c54d4f116914e921a742e5",
    "validation-specs.json": "14d396502a30d7753756b1e8a4834bd167e53a868d3760978410dd41f0dbd801",
    "proof-receipt.json": "a66afe73f88e58648a6fb6987a04aa82b8a30b0bff2adff3519ae065d98056c3",
    "check_validation.sh": "58cd905918469d957423723ecddf2a3f10900897f8824108fcc9201673416a75",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
TERMINAL_SOURCE = "Mathlib/Combinatorics/SetFamily/KruskalKatona.lean"
TERMINAL_SOURCE_BLOB = "f388fc0bfd201e1d9eb1279b5bd1c6dcbd253b34"
TERMINAL_SOURCE_SHA256 = "c6351d7ee422db9eed8f45335f4128eb3a66fe09997d12abc15eba38e9863f1c"
TERMINAL_OLEAN_SHA256 = "96e8f29576d4353c3fa6450edc9bb096454f80512eb778c1c5da7599cd0c584a"
EKR_BODY_SHA256 = "bafaad9695ea929dc30acd5dbc1275c48eb5d062b99c56e0ddd2013374e783c0"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
EXPECTED_LEAN_OUTPUT_SHA256 = "2de5d4df63c14cbafe24afac9f36d6f5bb1a37644e8b921ccc4f7bf363e686c4"
EXPECTED_LEAN_OUTPUT_BYTES = 7921
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
    "PASS THM-M-0822 narrow validation",
    "PASS network-isolated trust-0 kernel replay: exact statement, six frozen compositions, proof root, and validation recheck elaborated",
    "PASS trust observation: proof root and validation recheck report only propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, terminal source/blob/body/olean, clean mathlib pin, remote, license, and tools agree",
    "PASS hygiene and architecture: Lean sorry reports, local prohibited scan, reciprocal proof graph, and frozen compositions agree",
    "FAIL CLOSED authority/trust: proof master acceptance and complete transitive foundation, provenance, and TCB closure remain open at H1/M3/R4",
    "FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout empty-cache bootstrap, offline restoration, or a deterministic TCB/SBOM bundle",
    "FAIL CLOSED independent release: validation replay used this worker and shared cache, not a distinct signed verifier",
    "audit_complete=false; theorem_complete=false",
)
STARTED = time.monotonic()
TIMEOUT_SECONDS = 600.0


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
    remaining = TIMEOUT_SECONDS - (time.monotonic() - STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its wall-clock bound")
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
    assert target["execution_rank"] == 1380 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1380,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0822-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0822-PROOF"
    )
    assert predecessor["state"] == "[_]" and predecessor["attempts"] == 1
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0822-PROOF"]

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
        "Stage1Instances.THM_M_0822.ErdosKoRadoMaximumTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert anchor["canonical_target"]["expression_sha256"] == EXPRESSION_SHA256
    assert anchor["canonical_target"]["statement_file_sha256"] == (
        EXPECTED_INPUTS["Statement.lean"]
    )
    candidate = next(
        row
        for row in anchor["candidates"]
        if row["candidate_id"] == "M0822-C02-MATHLIB-UPPER-BOUND"
    )
    assert candidate["remote"] == MATHLIB_REMOTE
    assert candidate["revision"] == MATHLIB_REVISION
    assert candidate["tree"] == MATHLIB_TREE
    assert candidate["terminal_declaration"] == "Finset.erdos_ko_rado"
    assert candidate["candidate_classification"] == "M3"
    assert candidate["eligible_route_shape_after_E1"] == "M0-W"
    assert candidate["kernel_checked"] is True and candidate["accepted"] is False
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert registry["frozen_denominators"]["required_machine"] == MACHINE_IDS
    assert len(registry["obligations"]) == 27

    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["provisionally_closed_proof_obligation_ids"] == MACHINE_IDS
    assert proof_receipt["required_machine_open_ids"] == []
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["accepted"] is False and proof_receipt["content_addressed"] is False
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOM_LIST
    assert frozen_specs["item_id"] == "S56-M-0822-OBLIGATION_TREE"
    assert len(graphs["composition_certificates"]) == 6
    assert graphs["unverified_decomposition_plans"] == []
    assert {
        row["parent_obligation_id"]: row["declaration"]
        for row in graphs["composition_certificates"]
    } == COMPOSITION_DECLARATIONS
    proof_requires = {
        (edge["from"], edge["to"])
        for edge in graphs["graphs"]["proof"]["edges"]
        if edge["type"] == "proof_requires"
    }
    composes = {
        (edge["to"], edge["from"])
        for edge in graphs["graphs"]["proof"]["edges"]
        if edge["type"] == "composes"
    }
    assert proof_requires == composes == PROOF_REQUIRES
    reachable: set[str] = set()
    pending = ["M0822-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(child for parent, child in proof_requires if parent == obligation)
    assert reachable == set(MACHINE_IDS)

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
    validation_probe = code_without_comments(
        (HERE / "Validation.lean").read_text(encoding="utf-8")
    )
    assert "import Proof" in validation_probe
    assert not re.search(r"\b(?:theorem|lemma|example)\b", validation_probe)
    assert "assert_no_sorry Finset.erdos_ko_rado" in validation_probe
    assert "assert_no_sorry erdosKoRadoMaximum" in validation_probe

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
        MATHLIB
        / ".lake/build/lib/lean/Mathlib/Combinatorics/SetFamily/KruskalKatona.olean"
    )
    assert git("rev-parse", f"HEAD:{TERMINAL_SOURCE}", cwd=MATHLIB) == TERMINAL_SOURCE_BLOB
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert sha256_lines(terminal_source, 343, 390) == EKR_BODY_SHA256
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256
    terminal_region = b"".join(
        terminal_source.read_bytes().splitlines(keepends=True)[342:390]
    ).decode("utf-8")
    assert prohibited.search(code_without_comments(terminal_region)) is None
    for marker in (
        "theorem erdos_ko_rado",
        "Nat.eq_zero_or_pos r",
        "kruskal_katona_lovasz_form",
        "Set.Sized.card_le",
    ):
        assert marker in terminal_region

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    lake_version = run(["lake", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    assert "5.0.0-src+98dc76e" in lake_version
    python = Path(os.path.realpath(sys.executable))
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

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["recipe_id"] == receipt["recipe"]["recipe_id"]
    assert spec["item_id"] == receipt["item_id"] == packet["item_id"] == ITEM
    assert spec["theorem_id"] == receipt["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3",
        "-I",
        "-B",
        f"Stage1_Instances/{THEOREM}/check_validation.py",
    ]
    assert spec["env_allowlist"] == {
        "PATH": "explicitly_variable_for_pinned_Lake_launcher_and_hash_checked_host_helpers",
        "HOME": (
            "explicitly_variable_for_pinned_Elan_toolchain_locator_only; "
            "replaced by a temporary home for every Lean replay"
        ),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
    }
    assert spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert spec["covered_obligation_ids"] == MACHINE_IDS
    expected_covered_declarations = {
        "Stage1Instances.THM_M_0822.ErdosKoRadoMaximumTarget",
        *COMPOSITION_DECLARATIONS.values(),
        *PROOF_DECLARATIONS,
        VALIDATION_ROOT_DECLARATION,
    }
    assert set(spec["covered_declarations"]) == expected_covered_declarations

    lean_output = run(["bash", str(HERE / "check_validation.sh")])
    lean_output_bytes = lean_output.encode("utf-8")
    assert len(lean_output_bytes) == EXPECTED_LEAN_OUTPUT_BYTES
    assert hashlib.sha256(lean_output_bytes).hexdigest() == EXPECTED_LEAN_OUTPUT_SHA256
    for declaration in COMPOSITION_DECLARATIONS.values():
        observed = printed_axioms(lean_output, declaration)
        assert observed and observed <= EXPECTED_AXIOMS, declaration
    for declaration in PROOF_DECLARATIONS:
        observed = printed_axioms(lean_output, declaration)
        assert observed and observed <= EXPECTED_AXIOMS, declaration
    assert printed_axioms(lean_output, VALIDATION_ROOT_DECLARATION) == EXPECTED_AXIOMS
    assert lean_output.count("Declarations are sorry-free!") == len(PROOF_DECLARATIONS) + 2
    assert "sorryAx" not in lean_output
    assert "declaration uses 'sorry'" not in lean_output
    assert "error:" not in lean_output

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["depends_on"] == ["S56-M-0822-PROOF"]
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["content_addressed_release_evidence"] is False
    canonical = receipt["canonical_target"]
    assert canonical["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert canonical["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["covered_obligation_ids"] == MACHINE_IDS
    assert receipt["accepted_closed_obligation_ids"] == []
    assert set(receipt["validated_declarations"]) == expected_covered_declarations
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["validation-phase.md"] == sha256(HERE / "validation-phase.md")
    assert receipt["inputs"]["worker_packet"] == sha256(
        ROOT / ".stage1-worker-selftest.json"
    )
    assert receipt["inputs"]["lean-toolchain"] == EXPECTED_TOOL_INPUTS["lean-toolchain"]
    assert receipt["inputs"]["lake-manifest.json"] == EXPECTED_TOOL_INPUTS["lake-manifest.json"]
    assert receipt["recipe"] == spec
    result = receipt["result"]
    assert result["exit_code"] == 0
    assert result["kernel_output_sha256"] == EXPECTED_LEAN_OUTPUT_SHA256
    assert result["kernel_output_bytes"] == EXPECTED_LEAN_OUTPUT_BYTES
    assert result["exact_root_kernel_replay"] == "provisional_pass"
    assert result["validation_root_recheck"] == "provisional_pass_same_worker"
    assert result["observed_axioms"] == EXPECTED_AXIOM_LIST
    assert result["network_isolated_lean_replay"] == "pass"
    assert result["accepted_root_machine_debt"] == "M3"
    assert result["accepted_root_closed"] is False
    assert result["audit_complete"] is result["theorem_complete"] is False
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert receipt["root_vector_before"] == receipt["root_vector_after_worker_selftest"] == {
        "H": "H1",
        "M": "M3",
        "R": "R4",
    }
    assert receipt["known_failures"] == packet["known_failures"]
    assert receipt["first_failed_gate"] == "dependency.S56-M-0822-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"
    assert receipt["audit_complete"] is receipt["theorem_complete"] is False
    assert receipt["accepted_receipt_ids"] == []

    assert set(packet) == {
        "item_id",
        "changed_paths",
        "commands",
        "output_summary",
        "base_revision",
        "known_failures",
        "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["output_summary"] == "\n".join(SUMMARY_LINES)
    assert isinstance(packet["commands"], list) and packet["commands"]
    assert all(
        set(row) == {"command", "exit_code", "result"}
        and isinstance(row["exit_code"], int)
        and isinstance(row["result"], str)
        and row["result"]
        for row in packet["commands"]
    )
    command_results = {row["command"]: row["exit_code"] for row in packet["commands"]}
    assert command_results[f"bash Stage1_Instances/{THEOREM}/check_validation.sh"] == 0
    assert command_results[
        f"python3 -I -B Stage1_Instances/{THEOREM}/check_validation.py"
    ] == 0
    assert command_results[
        f"python3 -O -I -B Stage1_Instances/{THEOREM}/check_validation.py"
    ] == 1

    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:]
        for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)
    assert platform.system() == "Linux" and platform.machine() == "x86_64"

    print("\n".join(SUMMARY_LINES))


if __name__ == "__main__":
    main()
