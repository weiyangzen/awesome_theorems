#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0931-VALIDATION."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import time


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0931"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0931-VALIDATION"
THEOREM = "THM-M-0931"
BASE_REVISION = "4a10a7a4ddff88e302d5a303b16dd687d9468f63"
BASE_TREE = "730de242597680b39a7087d3204dfd1e6c41c60e"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "b872e0de4aedbd0da8825d2c7dd9ecb30e01215131c61e73dc3050776711718a"
DENOMINATOR_SHA256 = "2b96d10afc8120ac78b0b3029f490c99406b9ea53a07ec3a933108354ae5cd6a"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_AXIOM_LIST = ["propext", "Classical.choice", "Quot.sound"]
EXACT_DECLARATION_EVIDENCE_IDS = [
    "M0931-ROOT",
    "M0931-T-ROOT-COMPOSE",
    "M0931-S-COUNT-TRANSPORT",
    "M0931-A-MULTISET-EGZ",
    "M0931-N-ENUMERATE",
    "M0931-L-INDEXED-EGZ",
]
EXPECTED_INPUTS = {
    "Statement.lean": "d0e7e43d896a0625e87b3fac55319d5e999351c8f74cdda4e699d9360d651020",
    "ObligationTree.lean": "0e2e918e613f47fb6fefad481a9f7519bdda6a1a7c190ee3cae79280a6df4243",
    "Proof.lean": "01388ff60613831a83597b5647db19c08451a8b6fb1a574592fbadb658649f9f",
    "Validation.lean": "40a61533c3b46afdcf2577c2b278ee59055b62f7b141b15cf60253c80e35db59",
    "statement.json": "84e0e15bc6545467b3ed6442dd33c07a9f471d550546c17ebc2adb9040fe1b4d",
    "instance.json": "f5742b911dc2157ce3ab4d2a3d88bea08d34c5858c16b21bb25bf84e506bc6c2",
    "task-dag.json": "2d79adba8c7b7aa43e9e186888f81f05c568cfdcedd2e34b9cad62ec2eb58707",
    "anchor-audit.json": "233ac0f45554eb565e7aab423a687a0a716e9d15760cd04acc0c8f604d09d53e",
    "obligation-registry.json": "ebdf51a2fd9bd2a724c38888e4b530d05398e2b441160922e8777f84ca71057a",
    "typed-graphs.json": "69a0d48b2697373ac9d708a548a0cd5765a0eda9df063b5e2c69924a558c7f2b",
    "validation-specs.json": "aa7785b616f86700f6b2cf804087a43430334b345f28c62fa7ee099d16131b48",
    "proof-receipt.json": "b40d076951b9326b3fb3f04e173976b14d341a2d135afba745761fd0a2e9642d",
    "check_validation.sh": "04dd31d0f2b578a12a86d6c1b8ba2e29713b000a9c26d1b9205792e58591b93d",
    "validation-spec.json": "be1472dcb9ba4ba9f573f9d4fa3cfd047813c057946ae24f6b3a09e303103a6f",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
EGZ_SOURCE = "Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.lean"
EGZ_SOURCE_BLOB = "dbe223c73d6c612461bc900d3d7dd70be3c1d747"
EGZ_SOURCE_SHA256 = "13f8adfc07c9cffd89a0c2a2d3c265348b698fbf724d8b74e6de39434bbc79f7"
EGZ_OLEAN_SHA256 = "c09bb27e362e854347e306031e41c41ebab2b1ef904ebceedc0958e902a1ecbc"
INDEXED_BODY_SHA256 = "cc6b5e2b4a77fb2fd1e2fdeb38fa41aebe0a804b7212eee65b973b37f4b5145a"
MULTISET_BODY_SHA256 = "8607537347277f54f4096d259d938d96edb8408876cb9e069f52710a6a72cec4"
CHEVALLEY_SOURCE = "Mathlib/FieldTheory/ChevalleyWarning.lean"
CHEVALLEY_SOURCE_BLOB = "144087d302ebc67510cc3cf6903ab84706326b41"
CHEVALLEY_SOURCE_SHA256 = "a47186d1cd0c94b9ce1660686e8986df54e338a821e3266a9280e7f28d138684"
CHEVALLEY_OLEAN_SHA256 = "1bf10c8ba723f216ae4880e3b4f2896ffd677f927c06ebfb6a795e74f2b5a0a7"
CHEVALLEY_BODY_SHA256 = "c2d0c18a4688430f3563715783123e7dfee1f9f0eaf50a91e9147df638da49f6"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
LEAN_SHA256 = "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
LAKE_SHA256 = "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
PYTHON_SHA256 = "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
GIT_SHA256 = "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
BWRAP_SHA256 = "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0"
PROOF_DECLARATIONS = (
    "Int.erdos_ginzburg_ziv_multiset",
    "Int.erdos_ginzburg_ziv",
    "char_dvd_card_solutions_of_add_lt",
    "Stage1Instances.THM_M_0931.Proof.pinnedIndexedIntegerEGZ",
    "Stage1Instances.THM_M_0931.Proof.pinnedAtLeastCountAnchor",
    "Stage1Instances.THM_M_0931.Proof.atLeastCountAnchor_via_frozen_enumeration",
    "Stage1Instances.THM_M_0931.Proof.erdosGinzburgZiv_via_frozen_composition",
    "Stage1Instances.THM_M_0931.Proof.erdosGinzburgZiv_direct",
    "Stage1Instances.THM_M_0931.Proof.erdosGinzburgZiv",
)
DIFFERENTIAL_DECLARATIONS = (
    "Int.erdos_ginzburg_ziv",
    "char_dvd_card_solutions_of_add_lt",
    "Stage1Instances.THM_M_0931.Validation."
    "independentlyReconstructedErdosGinzburgZiv",
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
    "PASS THM-M-0931 narrow validation",
    "PASS network-isolated kernel replay: exact statement, frozen composition, proof roots, and differential indexed-to-multiset root elaborated",
    "PASS trust observation: proof and differential declarations report exactly propext, Classical.choice, and Quot.sound",
    "PASS selected provenance: frozen hashes, EGZ and Chevalley sources/blobs/bodies/oleans, clean mathlib pin, remote, license, and tools agree",
    "PASS hygiene and architecture: Lean sorry reports, local prohibited scan, frozen proof graph, and unverified-decomposition boundary agree",
    "FAIL CLOSED authority/trust: proof master acceptance and complete foundation, provenance, and TCB closure remain open at H1/M3/R4",
    "FAIL CLOSED hermetic release: shared warm .lake is not clean-checkout empty-cache bootstrap, offline restoration, or a deterministic TCB/SBOM bundle",
    "FAIL CLOSED independent release: differential indexed-to-multiset proof used this worker and shared cache, not a distinct signed verifier",
    "audit_complete=false; theorem_complete=false",
)
VALIDATION_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 600.0


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
        raise TimeoutError("validation recipe exceeded its 600-second wall-clock bound")
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
    assert target["execution_rank"] == 1470 and target["baseline"] == "L0"
    assert target["lifecycle_mode"] == "planned"
    assert target["rework_required"] is True and target["theorem_complete"] is False
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1470,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0931-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    predecessor = next(
        row for row in execution["items"] if row["id"] == "S56-M-0931-PROOF"
    )
    assert predecessor["state"] == "[_]"
    local_proof = next(row for row in local_dag["tasks"] if row["id"].endswith("-PROOF"))
    local_validation = next(
        row for row in local_dag["tasks"] if row["id"] == ITEM
    )
    assert local_proof["state"] == local_validation["state"] == "open"
    assert local_validation["depends_on"] == ["S56-M-0931-PROOF"]

    assert instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R4"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False
    assert closure["accepted_root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert len(graphs["unverified_decomposition_plans"]) == 6
    assert all(
        row["status"]
        == "source_body_decomposition_unverified_as_child_to_parent_composition"
        for row in graphs["unverified_decomposition_plans"]
    )

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"
    formal = statement["canonical_formal_target"]
    assert formal["declaration_or_expression"] == (
        "Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget"
    )
    assert formal["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert formal["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert anchor["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    root_evidence = proof_receipt["root_evidence"]
    assert root_evidence["root_kernel_declaration_closed"] is True
    assert root_evidence["accepted_root_closed"] is False
    assert root_evidence["machine_debt_proposal"] == "M0-W"
    assert root_evidence["closed_obligation_ids"] == []
    assert root_evidence["exact_declaration_evidence_ids"] == EXACT_DECLARATION_EVIDENCE_IDS
    assert root_evidence["internal_per_node_composition_credit"] is False
    assert root_evidence["unverified_internal_composition_count"] == 6
    assert proof_receipt["result"]["axioms"] == EXPECTED_AXIOM_LIST
    assert proof_receipt["accepted"] is False
    assert frozen_specs["item_id"] == "S56-M-0931-OBLIGATION_TREE"

    proof_children: dict[str, list[str]] = {}
    for edge in graphs["graphs"]["proof"]["edges"]:
        if edge["type"] == "proof_requires":
            proof_children.setdefault(edge["from"], []).append(edge["to"])
    reachable: set[str] = set()
    pending = ["M0931-ROOT"]
    while pending:
        obligation = pending.pop()
        if obligation in reachable:
            continue
        reachable.add(obligation)
        pending.extend(proof_children.get(obligation, []))
    assert reachable == set(EXACT_DECLARATION_EVIDENCE_IDS)

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
        "Int.erdos_ginzburg_ziv_multiset",
        "erdosGinzburgZiv_direct",
        "erdosGinzburgZiv_via_frozen_composition",
    ):
        assert forbidden not in differential, forbidden
    for required in (
        "Int.erdos_ginzburg_ziv",
        "s.toEnumFinset",
        "Multiset.map_fst_le_of_subset_toEnumFinset",
        "assert_no_sorry independentlyReconstructedErdosGinzburgZiv",
        "#print axioms independentlyReconstructedErdosGinzburgZiv",
    ):
        assert required in differential, required

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == MATHLIB_REVISION
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    remotes = git("remote", "-v", cwd=MATHLIB).splitlines()
    assert f"origin\t{MATHLIB_REMOTE} (fetch)" in remotes
    assert f"origin\t{MATHLIB_REMOTE} (push)" in remotes
    egz = MATHLIB / EGZ_SOURCE
    egz_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/Combinatorics/Additive/ErdosGinzburgZiv.olean"
    chevalley = MATHLIB / CHEVALLEY_SOURCE
    chevalley_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/FieldTheory/ChevalleyWarning.olean"
    assert git("rev-parse", f"HEAD:{EGZ_SOURCE}", cwd=MATHLIB) == EGZ_SOURCE_BLOB
    assert git("rev-parse", f"HEAD:{CHEVALLEY_SOURCE}", cwd=MATHLIB) == CHEVALLEY_SOURCE_BLOB
    assert sha256(egz) == EGZ_SOURCE_SHA256
    assert sha256(egz_olean) == EGZ_OLEAN_SHA256
    assert sha256_lines(egz, 110, 178) == INDEXED_BODY_SHA256
    assert sha256_lines(egz, 192, 195) == MULTISET_BODY_SHA256
    assert sha256(chevalley) == CHEVALLEY_SOURCE_SHA256
    assert sha256(chevalley_olean) == CHEVALLEY_OLEAN_SHA256
    assert sha256_lines(chevalley, 189, 194) == CHEVALLEY_BODY_SHA256
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256
    terminal_text = code_without_comments(egz.read_text(encoding="utf-8"))
    terminal_text += code_without_comments(chevalley.read_text(encoding="utf-8"))
    assert prohibited.search(terminal_text) is None

    lean_bin = Path(run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip())
    lake_bin = Path(run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip())
    python_bin = Path(shutil.which("python3") or "").resolve()
    git_bin = Path(shutil.which("git") or "").resolve()
    bwrap_bin = Path(shutil.which("bwrap") or "").resolve()
    assert sha256(lean_bin) == LEAN_SHA256
    assert sha256(lake_bin) == LAKE_SHA256
    assert sha256(python_bin) == PYTHON_SHA256
    assert sha256(git_bin) == GIT_SHA256
    assert sha256(bwrap_bin) == BWRAP_SHA256
    version = run([str(lean_bin), "--version"])
    assert "Lean (version 4.29.0" in version and LEAN_COMMIT in version
    assert platform.system() == "Linux" and platform.machine() == "x86_64"

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["recipe_id"] == "S56-M-0931-VALIDATION-narrow-v1"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-B", "Stage1_Instances/THM-M-0931/check_validation.py"
    ]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 600
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "read-only host root" in spec["network_enforcement"]
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact nine-line PASS/FAIL-CLOSED status summary",
    }]
    assert set(spec["covered_obligation_ids"]) == {
        *EXACT_DECLARATION_EVIDENCE_IDS, "M0931-X-PROVENANCE", "M0931-X-TRUST"
    }
    assert "grant no accepted closure" in spec["scope_boundary"]

    output = run(["bash", str(HERE / "check_validation.sh")], cwd=ROOT)
    for declaration in PROOF_DECLARATIONS:
        assert printed_axioms(output, declaration) == EXPECTED_AXIOMS
    for declaration in DIFFERENTIAL_DECLARATIONS:
        assert printed_axioms(output, declaration) == EXPECTED_AXIOMS
    assert output.count("Declarations are sorry-free!") == 12
    assert "sorryAx" not in output and "error:" not in output
    assert hashlib.sha256(output.encode()).hexdigest() == (
        "fc6cb44a5e47f577b1f168fde3af77a6da234d9f395e9e433fcb18c5d9df2d6b"
    )
    assert len(output.encode()) == 1789

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["phase"] == "validation" and receipt["intent"] == "validate"
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["proposed_state"] == "[_]" and receipt["accepted"] is False
    assert receipt["release_grade"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert receipt["covered_obligation_ids"] == spec["covered_obligation_ids"]
    assert receipt["accepted_closed_obligation_ids"] == []
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert receipt["tool_inputs"][name] == expected
    assert receipt["result"]["axioms"] == EXPECTED_AXIOM_LIST
    assert receipt["result"]["lean_replay_stdout_sha256"] == hashlib.sha256(
        output.encode()
    ).hexdigest()
    assert receipt["result"]["lean_replay_stdout_bytes"] == len(output.encode())
    assert receipt["result"]["placeholder_scan"] == "pass"
    assert receipt["result"]["root_kernel_replayed"] is True
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["accepted_machine_debt"] == "M3"
    assert receipt["result"]["audit_complete"] is False
    assert receipt["result"]["theorem_complete"] is False
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_verification_gate"] == "fail_closed"
    assert receipt["recipe"] == {
        **{key: spec[key] for key in (
            "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
            "network_policy", "network_enforcement", "expected_exit",
            "expected_outputs", "covered_obligation_ids", "covered_declarations",
            "scope_boundary",
        )},
        "observed_exit": 0,
    }
    environment = receipt["environment"]
    assert environment["lean_executable_sha256"] == sha256(lean_bin)
    assert environment["lake_executable_sha256"] == sha256(lake_bin)
    assert environment["python_executable_sha256"] == sha256(python_bin)
    assert environment["git_executable_sha256"] == sha256(git_bin)
    assert environment["bubblewrap_executable_sha256"] == sha256(bwrap_bin)
    provenance = receipt["provenance"]
    assert provenance["dependency_revision"] == MATHLIB_REVISION
    assert provenance["dependency_tree"] == MATHLIB_TREE
    assert provenance["origin_remote"] == MATHLIB_REMOTE
    assert provenance["terminal_source_sha256"] == EGZ_SOURCE_SHA256
    assert provenance["terminal_olean_sha256"] == EGZ_OLEAN_SHA256
    assert provenance["indexed_body_sha256"] == INDEXED_BODY_SHA256
    assert provenance["multiset_body_sha256"] == MULTISET_BODY_SHA256
    assert provenance["chevalley_source_sha256"] == CHEVALLEY_SOURCE_SHA256
    assert provenance["chevalley_olean_sha256"] == CHEVALLEY_OLEAN_SHA256
    assert provenance["chevalley_body_sha256"] == CHEVALLEY_BODY_SHA256
    assert provenance["license_sha256"] == LICENSE_SHA256
    assert set(receipt["validated_declarations"]) == set(spec["covered_declarations"]) - {
        "Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget",
    } | {
        "Stage1Instances.THM_M_0931.Proof.pinnedIndexedIntegerEGZ",
        "Stage1Instances.THM_M_0931.Proof.pinnedAtLeastCountAnchor",
        "Stage1Instances.THM_M_0931.Proof.atLeastCountAnchor_via_frozen_enumeration",
    }
    assert receipt["accepted_receipt_ids"] == []
    assert receipt["remaining_root_cut_set"] == proof_receipt["remaining_root_cut_set"]
    assert receipt["known_failures"] == packet["known_failures"]
    assert set(receipt["changed_paths"]) == set(packet["changed_paths"]) == CHANGED_PATHS

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
    assert packet["output_summary"] == list(SUMMARY_LINES)
    assert receipt["output_summary"] == list(SUMMARY_LINES)
    status = run(["git", "status", "--short", "--untracked-files=all"])
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS, (actual_changes, CHANGED_PATHS)
    assert git("diff", "--check", "--", str(HERE), str(ROOT / ".stage1-worker-selftest.json")) == ""
    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    validation = (HERE / "validation-phase.md").read_text(encoding="utf-8")
    for marker in (
        "S56-M-0931-VALIDATION",
        "network-isolated",
        "warm",
        "not section 10.6",
        "not section 10.7",
        "H1/M3/R4",
        "theorem_complete=false",
    ):
        assert marker in validation, marker

    for line in SUMMARY_LINES:
        print(line)


if __name__ == "__main__":
    main()
