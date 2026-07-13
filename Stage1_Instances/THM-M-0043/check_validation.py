#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0043-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0043"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0043-VALIDATION"
THEOREM = "THM-M-0043"
BASE_REVISION = "9a1ce196889e32911beeeffa685084b48a969866"
BASE_TREE = "00d5c1749015f44fb0c5694181253c3a08db5d47"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPRESSION_SHA256 = "a46ee23911b8027aa5de93149fd781def441429e386cb9181fc2064b2898557a"
DENOMINATOR_SHA256 = "1a92339af83640c1cf5d8853722d8c381b11a9d4139c4cb251cea3781d5b2af8"
EXPECTED_INPUTS = {
    "Statement.lean": "d2e524169f6c8a4e8d11b5c33eb3c218a62531966953150b3ec77b9a0f9e0d9c",
    "AnchorAudit.lean": "b75caf959f70c8c25724382009622c17abeddd3e31f71390fea92f2747c28cc9",
    "anchor-audit.json": "d07cbe2225d71e2e06fc9f394f943f32b2110f738e24752c6ad848cbf748f453",
    "ObligationTree.lean": "4f2a1b9c828de386c9edd397755454068d435e3ecddcded9860fd891f95faa5c",
    "Proof.lean": "d1d861debf06a6c12f21aef89015eca8b641812d83928ff33eff5a8695da0db3",
    "proof-receipt.json": "30def276bce24ab63c7d634339f5170642d5260472bbd3003f980e0adbfe4012",
    "statement.json": "34679ba95e58896a9730c677b0dd6b9f3cfd8b6984962ce3557c506cd796e353",
    "obligation-registry.json": "9efc55f4807f62199096aac1c6e6e5c1117238015773e75e0d7e46bf1b70d0d1",
    "typed-graphs.json": "83a9b401f4944c9922d194041cbfd7f81b14bb4ff6dce01b40993acb0d3c7a57",
    "validation-specs.json": "a47572de52f15386c30e1ca12a8f57ae30840ede9fe254accad9844dc2900558",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
PINNED_SOURCES = {
    "Mathlib/Analysis/InnerProductSpace/JointEigenspace.lean": (
        "9342a846990506a5240299915ff3788c89a12856",
        "901b240b008bc3c2e240072ba271db3076c43ea600fd57da95df20d05380902c",
        "e4157ba47e0b5487af984633db41504cffc56904211f5924d4f2901ed9740b8f",
    ),
    "Mathlib/Analysis/Matrix/Spectrum.lean": (
        "1e6809ddfb7d49841b23b4084e45141277c8daf8",
        "1a1a96a6f057a73b0d428b62cdbb3da824981928c162b52a15335abdafc8b0db",
        "81f5583c031af1331491f292f5d19514ebfbe8fde6dbbee71acf4efc84a5f98d",
    ),
    "Mathlib/LinearAlgebra/Complex/Module.lean": (
        "849e35dcd943e8fcc458903add32331ec08e0013",
        "ca73134270bfa2973baf2545708bcbd78f161f90ef49b8d36aec29f52d45edf7",
        "9fb8fb01cb0d1f12a76d35166cea9f77d607814a3ca01f53937e14c02dc3c9f4",
    ),
    "Mathlib/Analysis/InnerProductSpace/PiL2.lean": (
        "1809daf0493b8bbfde55c8f4d1bdcb2eb3feda7a",
        "4df49dd497992b022f3d18ee79ea0ae5536be7a452779b4c2400b1d136b7a2bb",
        "b421e082ec7b4bfab92f0fd05c51968deb0933812e975beec781bdab0a826ea4",
    ),
}
PROOF_IDS = [
    "M0043-ROOT", "M0043-N-NORMAL-COMMUTE", "M0043-C-HERMITIAN-PARTS",
    "M0043-L-H-HERMITIAN", "M0043-L-K-HERMITIAN", "M0043-T-M-RECONSTRUCT",
    "M0043-L-HK-COMMUTE", "M0043-T-LINEAR-COMMUTE", "M0043-C-JOINT-EIGENSPACE",
    "M0043-L-JOINT-DECOMP", "M0043-L-JOINT-ORTHOGONAL", "M0043-L-FINITE-EIGENVALUES",
    "M0043-B-NONZERO-SUBTYPE", "M0043-L-SUBORDINATE-BASIS", "M0043-C-BASIS-REINDEX",
    "M0043-T-OPERATOR-DECOMP", "M0043-C-EIGENVALUES", "M0043-L-BASIS-EIGENVECTORS",
    "M0043-L-UNITARY-BASIS", "M0043-C-UNITARY-MATRIX", "M0043-L-MATRIX-EIGEN-RELATION",
    "M0043-T-CONJUGATED-DIAGONAL", "M0043-T-ROOT-COMPOSE",
]
VALIDATED_IDS = [item for item in PROOF_IDS if item != "M0043-T-OPERATOR-DECOMP"]
VALIDATED_DECLARATIONS = [
    "Stage1Instances.THM_M_0043.ObligationTree.root_of_exactConjugatedDiagonalAnchor",
    "Stage1Instances.THM_M_0043.Proof.commutingHermitianParts_conjugatedDiagonal",
    "Stage1Instances.THM_M_0043.Proof.normalComplexConjugatedDiagonal",
    "Stage1Instances.THM_M_0043.Proof.spectralTheorem_via_frozen_composition",
    "Stage1Instances.THM_M_0043.Validation.differentialCommutingHermitianDiagonalization",
    "Stage1Instances.THM_M_0043.Validation.differentialSpectralTheorem",
]
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}
VALIDATION_STARTED = time.monotonic()
RECIPE_TIMEOUT_SECONDS = 180.0


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> str:
    remaining = RECIPE_TIMEOUT_SECONDS - (time.monotonic() - VALIDATION_STARTED)
    if remaining <= 0:
        raise TimeoutError("validation recipe exceeded its 180-second wall-clock bound")
    result = subprocess.run(
        argv, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, timeout=remaining, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}")
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_axioms(output: str, declaration: str) -> None:
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)]", re.DOTALL
    )
    match = pattern.search(output)
    assert match is not None, (declaration, output)
    observed = {part.strip() for part in match.group(1).split(",")}
    assert observed == {"propext", "Classical.choice", "Quot.sound"}, (declaration, observed)


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    statement = load(HERE / "statement.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM, "theorem_id": THEOREM, "execution_rank": 1083,
        "phase": "validation", "layer": 5, "state": "[ ]",
        "depends_on": ["S56-M-0043-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0, "children": [],
    }
    proof_item = next(row for row in execution["items"] if row["id"] == "S56-M-0043-PROOF")
    assert proof_item["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0043-PROOF"]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "." and spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {} and spec["timeout_seconds"] == 180
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert spec["recipe_id"] == "VAL-M0043-NARROW-KERNEL-TRUST-PROVENANCE-DIFFERENTIAL"
    assert spec["expected_outputs"] == [{
        "path_or_stream": "stdout",
        "semantic_hash_policy": "exact five-line PASS/STALE/BLOCKED gate summary",
    }]
    assert "did not provision a kernel network namespace" in spec["network_enforcement"]
    assert spec["covered_obligation_ids"] == VALIDATED_IDS
    assert spec["covered_declarations"] == VALIDATED_DECLARATIONS
    assert "M0043-T-OPERATOR-DECOMP is not mapped" in spec["coverage_boundary"]

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert statement["canonical_formal_target"]["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["metrics_projection"]["proof_reachable_ids"] == PROOF_IDS
    assert proof_receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert proof_receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["inputs"]["statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert proof_receipt["inputs"]["obligation_tree_sha256"] == EXPECTED_INPUTS["ObligationTree.lean"]
    assert proof_receipt["inputs"]["obligation_registry_sha256"] == EXPECTED_INPUTS["obligation-registry.json"]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["closed_obligation_ids"] == PROOF_IDS
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert proof_receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    certified_ids: set[str] = set()
    for certificate in proof_receipt["composition_certificates"]:
        certified_ids.add(certificate["parent"])
        certified_ids.update(certificate["children"])
    assert certified_ids == set(VALIDATED_IDS)
    assert set(proof_receipt["closed_obligation_ids"]) - certified_ids == {
        "M0043-T-OPERATOR-DECOMP"
    }
    assert instance["lifecycle_mode"] == "planned"
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

    proof_edges = {
        (edge["from"], edge["to"])
        for edge in graphs["graphs"]["proof"]["edges"]
        if edge["type"] == "proof_requires"
    }
    for edge in (
        ("M0043-ROOT", "M0043-T-ROOT-COMPOSE"),
        ("M0043-T-ROOT-COMPOSE", "M0043-T-CONJUGATED-DIAGONAL"),
        ("M0043-T-CONJUGATED-DIAGONAL", "M0043-L-MATRIX-EIGEN-RELATION"),
        ("M0043-L-HK-COMMUTE", "M0043-N-NORMAL-COMMUTE"),
    ):
        assert edge in proof_edges

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:@\[[^]\n]*\][ \t]*)*"
        r"(?:(?:private|protected|noncomputable|local|scoped)[ \t]+)*"
        r"(?:axiom|constant|opaque|unsafe)\b", re.MULTILINE,
    )
    for name in ("Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    differential = (HERE / "Validation.lean").read_text(encoding="utf-8")
    for forbidden in ("import Proof", "import ObligationTree", "Proof.", "root_of_exactConjugatedDiagonalAnchor"):
        assert forbidden not in differential, forbidden
    for marker in (
        "hHs.directSum_isInternal_of_commute hKs hcomm",
        "hActiveInternal.subordinateOrthonormalBasis",
        "theorem differentialSpectralTheorem : SpectralTheoremTarget.{u}",
    ):
        assert marker in differential, marker

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""
    for rel, (blob, source_hash, olean_hash) in PINNED_SOURCES.items():
        source = MATHLIB / rel
        olean = MATHLIB / ".lake/build/lib/lean" / Path(rel).with_suffix(".olean")
        assert git("rev-parse", f"HEAD:{rel}", cwd=MATHLIB) == blob
        assert sha256(source) == source_hash
        assert sha256(olean) == olean_hash
    assert sha256(MATHLIB / "LICENSE") == "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    python = Path(os.path.realpath(os.sys.executable))
    git_path = shutil.which("git")
    assert git_path is not None
    git_executable = Path(git_path)
    assert sha256(Path(lean)) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(Path(lake)) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    assert sha256(python) == "b8d8288faefdd300201f43fcf00f6f539a27218eeed3a3dff5ab10b9c4c99700"
    assert sha256(git_executable) == "8a48eefa306b9a2a9c3e576784a74ad7485779279e5a46ec43361a1864760e45"
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    base_env = os.environ.copy()
    base_env.update({"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"})
    with tempfile.TemporaryDirectory(prefix="m0043-validation-") as tmp_name:
        tmp = Path(tmp_name)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        statement_env = base_env.copy()
        statement_env["LEAN_PATH"] = lean_path
        run([lean, "-t", "0", "-o", "Statement.olean", "Statement.lean"], cwd=tmp, env=statement_env)
        module_env = base_env.copy()
        module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        obligation_output = run(
            [lean, "-t", "0", "-o", "ObligationTree.olean", "ObligationTree.lean"], cwd=tmp, env=module_env
        )
        proof_output = run([lean, "-t", "0", "Proof.lean"], cwd=tmp, env=module_env)
        validation_output = run([lean, "-t", "0", "Validation.lean"], cwd=tmp, env=module_env)

    assert_axioms(
        obligation_output,
        "Stage1Instances.THM_M_0043.ObligationTree.root_of_exactConjugatedDiagonalAnchor",
    )
    proof_declarations = (
        "Stage1Instances.THM_M_0043.Proof.commutingHermitianParts_conjugatedDiagonal",
        "Stage1Instances.THM_M_0043.Proof.normalComplexConjugatedDiagonal",
        "Stage1Instances.THM_M_0043.Proof.spectralTheorem_via_frozen_composition",
    )
    validation_declarations = (
        "Stage1Instances.THM_M_0043.Validation.differentialCommutingHermitianDiagonalization",
        "Stage1Instances.THM_M_0043.Validation.differentialSpectralTheorem",
    )
    for declaration in proof_declarations:
        assert_axioms(proof_output, declaration)
    for declaration in validation_declarations:
        assert_axioms(validation_output, declaration)
    assert proof_output.count("Declarations are sorry-free!") == len(proof_declarations)
    assert validation_output.count("Declarations are sorry-free!") == len(validation_declarations)
    assert "sorryAx" not in obligation_output + proof_output + validation_output

    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["audit_complete"] is closure["theorem_complete"] is False
    assert set(closure["remaining_root_cut_set"]) == {
        "M0043-T-CONJUGATED-DIAGONAL", "M0043-X-SOURCE", "M0043-S-FOUNDATION",
        "M0043-X-PROVENANCE", "M0043-X-EVIDENCE", "M0043-X-TRUST",
        "M0043-X-READABLE", "M0043-X-WORKFLOW",
    }

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["depends_on"] == ["S56-M-0043-PROOF"]
    assert receipt["proposed_state"] == packet["state"] == "[_]"
    assert receipt["release_grade"] is receipt["accepted"] is False
    assert receipt["canonical_target_expression_sha256"] == EXPRESSION_SHA256
    assert receipt["registry_denominator_sha256"] == DENOMINATOR_SHA256
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["Validation.lean"] == sha256(HERE / "Validation.lean")
    assert receipt["inputs"]["validation-spec.json"] == sha256(HERE / "validation-spec.json")
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["lean-toolchain"] == EXPECTED_TOOL_INPUTS["lean-toolchain"]
    assert receipt["inputs"]["lake-manifest.json"] == EXPECTED_TOOL_INPUTS["lake-manifest.json"]
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "expected_outputs",
        "covered_obligation_ids", "covered_declarations", "coverage_boundary",
    ):
        assert receipt["recipe"][key] == spec[key]
    assert receipt["output_evidence"]["stdout_semantic_sha256"] == (
        "7bf142e9b8c0997a4247228717d185571a4dc680935fb8598a1431cabff5aa24"
    )
    assert receipt["result"]["locally_validated_obligation_ids"] == VALIDATED_IDS
    assert receipt["result"]["uncertified_claimed_proof_obligation_ids"] == [
        "M0043-T-OPERATOR-DECOMP"
    ]
    assert receipt["result"]["axioms"] == ["propext", "Classical.choice", "Quot.sound"]
    assert receipt["result"]["narrow_kernel_replay"] == "pass_at_trust_level_zero"
    assert receipt["result"]["accepted_root_closed"] is False
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert set(receipt["changed_paths"]) == CHANGED_PATHS
    assert set(packet["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert receipt["environment"]["lean_executable_sha256"] == sha256(Path(lean))
    assert receipt["environment"]["lake_executable_sha256"] == sha256(Path(lake))
    assert receipt["environment"]["python_executable_sha256"] == sha256(python)
    assert receipt["environment"]["git_executable_sha256"] == sha256(git_executable)
    assert receipt["environment"]["platform"] == (
        f"{platform.system()} {platform.release()} {platform.machine()}"
    )
    assert platform.system() == "Linux"

    status = git("status", "--short", "--untracked-files=all")
    actual_changes = {
        line[3:] for line in status.splitlines() if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changes == CHANGED_PATHS
    for path in (HERE / "Validation.lean", HERE / "check_validation.py", HERE / "validation-phase.md"):
        data = path.read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS narrow kernel: exact proof, frozen composition, and differential root replay at Lean trust level zero")
    print("PASS trust observation: six declarations report only propext, Classical.choice, and Quot.sound")
    print("PASS local provenance: bound inputs, selected source/olean hashes, clean mathlib pin, license, and tool identities agree")
    print("STALE authoritative state: graph remains M3/root_open and proof dependency remains provisional pending master acceptance")
    print("BLOCKED release gates: warm shared .lake, incomplete transitive TCB/SBOM/offline archive, and no distinct runner")


if __name__ == "__main__":
    main()
