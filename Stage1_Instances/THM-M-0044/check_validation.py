#!/usr/bin/env python3
"""Fail-closed narrow validator for S56-M-0044-VALIDATION."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / "Stage1_Instances" / "THM-M-0044"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0044-VALIDATION"
THEOREM = "THM-M-0044"
BASE_REVISION = "9a1ce196889e32911beeeffa685084b48a969866"
BASE_TREE = "00d5c1749015f44fb0c5694181253c3a08db5d47"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPECTED_INPUTS = {
    "Statement.lean": "29f45600f5bc00edbd42756c7dd70c8599cdf2f04f07a570eb9f4e9b3d30141c",
    "ObligationTree.lean": "406d197fd43977485301785df9d96133be5ae0bee01d62d4c662601cf287de45",
    "Proof.lean": "aed09e85710bdfd9527a25881fcdf147f757b2c268531d05dd0e800a7a4060bc",
    "proof-receipt.json": "344e11c8355928ed2b0c07e0d3eab8da44c3c03d6955db1f3d21e56825f71d11",
    "obligation-registry.json": "b0e721bf26c60a775712bdf5c0b2e4454e3ffa4428291da44e86a858bf938be6",
    "typed-graphs.json": "5bb2d11465b44e54bbad0ad67b9145ff676465645ec52d12417f99d3a8ce6414",
    "validation-specs.json": "d3ce3bad646a5f48086e5cf8b6c235bc21711b98a00d060625d7f75d973e4ee3",
    "anchor-audit.json": "d378103f2cae1293337261ff856fbbdd666825a4df72fb4439a8c2cf4cba9e59",
    "Validation.lean": "1f6be5f4b7311620a92b594fc0c070ffe2633e8e4c8949fc5d3b50ad1bfe4d52",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
SOURCE_BOUNDARY = {
    "Mathlib/Analysis/InnerProductSpace/Adjoint.lean": (
        "08218f9c59623e93818c293000810a2d15a9b543340feaba3b1a58b4749831a6",
        "3be11d32be2df343d8845b0eabe6d0dbe553509b68cfd15b31bf75525f97bf29",
    ),
    "Mathlib/Analysis/InnerProductSpace/GramSchmidtOrtho.lean": (
        "0eb98a48c591bfe2c4677a89e719b1973b199a55d6b1cfc9ce73c265ea22288a",
        "fea3920813230f255cc6df8506f72b84082837eefefdfd621fd4a6f0abda9dfc",
    ),
    "Mathlib/Analysis/InnerProductSpace/PiL2.lean": (
        "4df49dd497992b022f3d18ee79ea0ae5536be7a452779b4c2400b1d136b7a2bb",
        "b421e082ec7b4bfab92f0fd05c51968deb0933812e975beec781bdab0a826ea4",
    ),
    "Mathlib/Analysis/InnerProductSpace/Positive.lean": (
        "85390d44bfc0c5bd8d832b498b7739d3cdae617314b4fcbdddbf55537bdbe675",
        "8cd65b76e044265d0dacf027d6406854ae33531ebdb3748ab848182ff524599b",
    ),
    "Mathlib/Analysis/InnerProductSpace/SingularValues.lean": (
        "cfc6d04849895b65fa0293d6cc3a234279e757726bc92fd99ce530ccc35863aa",
        "18fe63dfdcfaba8bf071a2454b969c355d62b4c818c6ff0aa59933cef816b631",
    ),
    "Mathlib/Analysis/InnerProductSpace/Spectrum.lean": (
        "49eeec917a355497936a4f779eb6403af0910c66d0f3fbbfd131ad7833c4f555",
        "e958a85bd9f9d8d3810a35fbc147db593ea3f8bf9aa8249bd996bba176fdbf5e",
    ),
    "Mathlib/Analysis/Matrix/Spectrum.lean": (
        "1a1a96a6f057a73b0d428b62cdbb3da824981928c162b52a15335abdafc8b0db",
        "81f5583c031af1331491f292f5d19514ebfbe8fde6dbbee71acf4efc84a5f98d",
    ),
    "Mathlib/LinearAlgebra/Matrix/Hermitian.lean": (
        "40e15d6eeaf22ac4ec97a7acf02e362dc6f22ae538e6c49640d2005c03927ea7",
        "b664c4ddd8a3f72b6ecc8f976566c3ef45786fee0619edbfb5690b7659daabc4",
    ),
    "Mathlib/LinearAlgebra/UnitaryGroup.lean": (
        "0136abe584007ffe1b9e9b0016b792ed92bc2de36fa710e87af9cb87d0808f93",
        "2f02f7cedf8b9e2fe6513cd585655f566eef466f48818e165874ad8626539313",
    ),
}
CHANGED_PATHS = {
    ".stage1-worker-selftest.json",
    f"Stage1_Instances/{THEOREM}/Validation.lean",
    f"Stage1_Instances/{THEOREM}/check_validation.py",
    f"Stage1_Instances/{THEOREM}/validation-phase.md",
    f"Stage1_Instances/{THEOREM}/validation-receipt.json",
    f"Stage1_Instances/{THEOREM}/validation-spec.json",
}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict), path
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    argv: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None
) -> str:
    result = subprocess.run(
        argv,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_axioms(output: str, declaration: str) -> None:
    pattern = re.compile(
        rf"'[^'\n]*{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, (declaration, output)
    observed = {part.strip() for part in match.group(1).split(",")}
    assert observed == EXPECTED_AXIOMS, (declaration, observed)


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs/Stage1_Execution_DAG_rev-5.6.json")

    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1084,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0044-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    proof_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0044-PROOF"
    )
    assert proof_item["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0044-PROOF"]
    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["cwd"] == "." and spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 180 and spec["network_policy"] == "denied"
    assert spec["expected_exit"] == 0
    assert len(spec["covered_obligation_ids"]) == 25

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    assert statement["canonical_formal_target"]["statement_file_sha256"] == (
        EXPECTED_INPUTS["Statement.lean"]
    )
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == (
        "ca7e41568d1de7831322431b4b7821d0c443907eededff9c9d94cb464c44bd91"
    )
    assert graphs["registry_denominator_sha256"] == registry["denominator_sha256"]
    assert proof_receipt["proof_body"]["source_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["result"]["root_kernel_closed"] is True
    assert proof_receipt["result"]["accepted_root_closed"] is False
    assert proof_receipt["accepted"] is False
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False
    closure = graphs["closure_boundary"]
    assert closure["root_closed"] is False and closure["root_machine_debt"] == "M3"
    assert closure["accepted_closed_obligations"] == []
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    prohibited = re.compile(
        r"\b(?:sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|"
        r"^[ \t]*(?:axiom|constant|opaque|unsafe)\b",
        re.MULTILINE,
    )
    for name in (
        "Statement.lean", "AnchorAudit.lean", "ObligationTree.lean", "Proof.lean",
        "Validation.lean",
    ):
        source = code_without_comments((HERE / name).read_text(encoding="utf-8"))
        assert prohibited.search(source) is None, f"prohibited source token in {name}"
    differential = (HERE / "Validation.lean").read_text(encoding="utf-8")
    for forbidden in (
        "import Proof", "import ObligationTree", "Proof.singularValueDecomposition",
        "exact singularValueDecomposition",
    ):
        assert forbidden not in differential, forbidden
    assert "assert_no_sorry differentialSingularValueDecomposition" in differential

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["url"] == "https://github.com/leanprover-community/mathlib4.git"
    assert mathlib_entry["rev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("status", "--porcelain", "--untracked-files=all", cwd=MATHLIB) == ""
    assert sha256(MATHLIB / "LICENSE") == anchor["immutable_environment"]["license_sha256"]
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == (
        anchor["immutable_environment"]["mathlib_remote"]
    )
    for relative, (source_sha, olean_sha) in SOURCE_BOUNDARY.items():
        source = MATHLIB / relative
        olean = MATHLIB / ".lake/build/lib/lean" / Path(relative).with_suffix(".olean")
        assert sha256(source) == source_sha, relative
        assert sha256(olean) == olean_sha, str(olean)

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    assert sha256(Path(lean)) == "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf"
    assert sha256(Path(lake)) == "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359"
    version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in version and LEAN_COMMIT in version
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    base_env = {
        "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC", "LEAN_PATH": lean_path,
    }
    with tempfile.TemporaryDirectory(prefix="m0044-validation-", dir=LEAN_ROOT) as tmp_name:
        tmp = Path(tmp_name)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        statement_output = run(
            [lean, "--root", str(ROOT), "-o", str(tmp / "Statement.olean"),
             str(tmp / "Statement.lean")],
            cwd=LEAN_ROOT, env=base_env,
        )
        module_env = dict(base_env)
        module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        obligation_output = run(
            [lean, "--root", str(ROOT), "-o", str(tmp / "ObligationTree.olean"),
             str(tmp / "ObligationTree.lean")],
            cwd=LEAN_ROOT, env=module_env,
        )
        proof_output = run(
            [lean, "--root", str(ROOT), str(tmp / "Proof.lean")],
            cwd=LEAN_ROOT, env=module_env,
        )
        differential_output = run(
            [lean, "--root", str(ROOT), str(tmp / "Validation.lean")],
            cwd=LEAN_ROOT, env=module_env,
        )

    assert "SingularValueDecompositionTarget : Prop" in statement_output
    assert_axioms(
        obligation_output,
        "Stage1Instances.THM_M_0044.ObligationTree.root_of_real_and_complex",
    )
    for declaration in (
        "Stage1Instances.THM_M_0044.Proof.singularValueDecomposition",
        "Stage1Instances.THM_M_0044.Proof.svdBasisTall",
        "Stage1Instances.THM_M_0044.Proof.isFullSVD_of_le",
        "Stage1Instances.THM_M_0044.Proof.isFullSVD_of_ge",
        "Stage1Instances.THM_M_0044.Proof.fullSVDOver",
    ):
        assert_axioms(proof_output, declaration)
    assert "Declarations are sorry-free!" in differential_output
    assert_axioms(
        differential_output,
        "Stage1Instances.THM_M_0044.Validation.differentialSingularValueDecomposition",
    )
    assert "sorryAx" not in obligation_output + proof_output + differential_output

    assert receipt["item_id"] == ITEM and receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == BASE_REVISION and receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["release_grade"] is False
    assert receipt["inputs"]["validator_sha256"] == sha256(HERE / "check_validation.py")
    assert receipt["inputs"]["validation_spec_sha256"] == sha256(HERE / "validation-spec.json")
    assert receipt["result"]["provisional_exact_root_kernel_closed"] is True
    assert receipt["result"]["accepted_root_kernel_closed"] is False
    assert receipt["result"]["accepted_closed_obligation_ids"] == []
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0044-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["item_id"] == ITEM and packet["state"] == "[_]"
    assert packet["base_revision"] == BASE_REVISION
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = run(["git", "status", "--short", "--untracked-files=all"])
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)
    for relative in CHANGED_PATHS - {".stage1-worker-selftest.json"}:
        data = (ROOT / relative).read_bytes()
        assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
        assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())

    print("PASS THM-M-0044 narrow validation")
    print("PASS kernel replay: exact proof, frozen composition, and differential exact root elaborated")
    print("PASS trust observation: checked declarations report only propext, Classical.choice, and Quot.sound")
    print("PASS local provenance: frozen hashes, direct source/olean boundary, clean mathlib pin, remote, and license agree")
    print("PASS hygiene: Lean assert_no_sorry plus a supplemental prohibited-construct scan passed")
    print("FAIL CLOSED authority: proof/master reconciliation is pending; accepted root remains H1/M3/R3")
    print("FAIL CLOSED hermetic release: shared warm .lake is not an empty-cache offline replay or complete TCB/SBOM archive")
    print("FAIL CLOSED independent release: differential proof used this worker/shared cache, not a distinct signed runner")
    print("audit_complete=false; theorem_complete=false")


if __name__ == "__main__":
    main()
