#!/usr/bin/env python3
"""Fail-closed narrow validation for S56-M-0041-VALIDATION."""

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
HERE = ROOT / "Stage1_Instances" / "THM-M-0041"
LEAN_ROOT = ROOT / "Formalizations" / "Lean"
MATHLIB = LEAN_ROOT / ".lake" / "packages" / "mathlib"
ITEM = "S56-M-0041-VALIDATION"
THEOREM = "THM-M-0041"
BASE_REVISION = "ebd5f75831296a8a35e7b33013b964f2baf31bb9"
BASE_TREE = "d1e4bc83c803eefcd9898aac57352265a29f0658"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
MATHLIB_TREE = "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
MATHLIB_REMOTE = "https://github.com/leanprover-community/mathlib4.git"
LEAN_COMMIT = "98dc76e3c0a9b856c9b98726b713fb04fab16740"
EXPECTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
EXPRESSION_SHA256 = "5aad8415af4578ca43d0ec58eee038ed4470dce17896766215d3bf9f49d8e711"
DENOMINATOR_SHA256 = "c854b50bfd112e0e20a94f25fc6db6f4fda74e248e61b647ffd93d93977c33dc"
EXPECTED_INPUTS = {
    "Statement.lean": "3b218c1a96922399bb8ed2d852d556422a92901dca10efdd431a677eaefd2b0b",
    "AnchorAudit.lean": "e0b5de6bd28603ec22be337f34462987478734b1bd2617e9fbae809ccddc2cd3",
    "anchor-audit.json": "ac307c8c22163f14c44fc09b2beae9036921e599e53b0f829b53e7aca81664aa",
    "ObligationTree.lean": "bdf7444fdbdd6cbb7414514151c017c6c051b05565d9fee5ad0dd88828eefcdc",
    "Proof.lean": "051ac9b2030db4c21edece622b80820a82a41a5f444912570b736d5f5e688506",
    "proof-receipt.json": "5443de832daf6f4f3c76f07e8ea6936cdf2f0448bcc057141fd1640b4968e2d9",
    "obligation-registry.json": "7d8f26df395fa73ca9dacb9f20fe9564f8f3232491c62976f57c86ee12936cac",
    "typed-graphs.json": "8bb7d50066c36b84935880b240d79091e964ce53a0599f90ebdf6a408c5c84b1",
    "Validation.lean": "cfb78c37b4ef84a9c7609918047c328dcdab6abaabeb616ab8fd6307b603dccc",
    "validation-spec.json": "c5e667aaa9f0729ac2e61e07d915ee9364579b3513518294957b752589488c4f",
}
EXPECTED_TOOL_INPUTS = {
    "lean-toolchain": "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2",
    "lake-manifest.json": "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81",
}
TERMINAL_SOURCE_SHA256 = "9e22d8fdace32c7bb8304335027b95ccb4cca18b5d430076ac4f87b2d76ca3f2"
TERMINAL_SOURCE_BLOB = "f9f5b9423cbc597a427c6da31f42ad6466c2940b"
TERMINAL_BODY_SHA256 = "427ef4b3af84b4d5f1445bf4b7cadc44af97aca88833bbc30307661b7915c7cd"
TERMINAL_OLEAN_SHA256 = "882236875a32debd61e2ca5cdb3026350a01240abe7eb5d6c5a93863c5b591aa"
LICENSE_SHA256 = "b40930bbcf80744c86c46a12bc9da056641d722716c378f5659b9e555ef833e1"
PROVISIONAL_CLOSED = {
    "M0041-ROOT", "M0041-S-INTERFACE", "M0041-S-CHARPOLY",
    "M0041-S-BOUNDARY", "M0041-T-CHARPOLY", "M0041-A-MATHLIB-ANCHOR",
}
COVERED = PROVISIONAL_CLOSED | {
    "M0041-C-ADJUGATE", "M0041-N-MATPOLY", "M0041-L-RIGHT-FACTOR",
    "M0041-T-SCALAR-EVAL", "M0041-T-BODY-ASSEMBLE",
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
            f"validation failed ({result.returncode}): {argv!r}\n{result.stdout}"
        )
    return result.stdout


def git(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).strip()


def code_without_comments(source: str) -> str:
    source = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
    return re.sub(r"--.*$", "", source, flags=re.MULTILINE)


def assert_axioms(output: str, declaration: str) -> None:
    pattern = re.compile(
        rf"'{re.escape(declaration)}' depends on axioms:\s*\[([^]]+)\]",
        re.DOTALL,
    )
    match = pattern.search(output)
    assert match is not None, (declaration, output)
    observed = {part.strip() for part in match.group(1).split(",")}
    assert observed == EXPECTED_AXIOMS, (declaration, observed)


def assert_text_hygiene(path: Path) -> None:
    data = path.read_bytes()
    assert data.endswith(b"\n") and b"\r" not in data and b"\x00" not in data
    assert all(not line.endswith((b" ", b"\t")) for line in data.splitlines())


def main() -> None:
    spec = load(HERE / "validation-spec.json")
    receipt = load(HERE / "validation-receipt.json")
    packet = load(ROOT / ".stage1-worker-selftest.json")
    statement = load(HERE / "statement.json")
    anchor = load(HERE / "anchor-audit.json")
    registry = load(HERE / "obligation-registry.json")
    graphs = load(HERE / "typed-graphs.json")
    proof_receipt = load(HERE / "proof-receipt.json")
    instance = load(HERE / "instance.json")
    local_dag = load(HERE / "task-dag.json")
    execution = load(ROOT / "Docs" / "Stage1_Execution_DAG_rev-5.6.json")

    assert git("rev-parse", "HEAD") == BASE_REVISION
    assert git("rev-parse", "HEAD^{tree}") == BASE_TREE
    item = next(row for row in execution["items"] if row["id"] == ITEM)
    assert item == {
        "id": ITEM,
        "theorem_id": THEOREM,
        "execution_rank": 1081,
        "phase": "validation",
        "layer": 5,
        "state": "[ ]",
        "depends_on": ["S56-M-0041-PROOF"],
        "owned_paths": [f"Stage1_Instances/{THEOREM}"],
        "deliverable": "Run hermetic kernel, trust, provenance, and independent validation gates.",
        "completion_gate": "rev-5.6 node-specific receipt and master acceptance",
        "attempts": 0,
        "children": [],
    }
    proof_item = next(
        row for row in execution["items"] if row["id"] == "S56-M-0041-PROOF"
    )
    assert proof_item["state"] == "[_]"
    local_task = next(row for row in local_dag["tasks"] if row["id"] == ITEM)
    assert local_task["state"] == "open"
    assert local_task["depends_on"] == ["S56-M-0041-PROOF"]

    assert spec["schema_version"] == "stage1-validation-recipe/1.0"
    assert spec["item_id"] == ITEM and spec["theorem_id"] == THEOREM
    assert spec["cwd"] == "."
    assert spec["argv"] == [
        "python3", "-B", f"Stage1_Instances/{THEOREM}/check_validation.py"
    ]
    assert spec["env_allowlist"] == {}
    assert spec["timeout_seconds"] == 180
    assert spec["network_policy"] == "denied" and spec["expected_exit"] == 0
    assert "did not provision a kernel network namespace" in spec["network_enforcement"]
    assert set(spec["covered_obligation_ids"]) == COVERED

    for name, expected in EXPECTED_INPUTS.items():
        assert sha256(HERE / name) == expected, f"stale validation input: {name}"
    for name, expected in EXPECTED_TOOL_INPUTS.items():
        assert sha256(LEAN_ROOT / name) == expected, f"changed tool input: {name}"

    assert statement["canonical_formal_target"]["elaborated_expression_sha256"] == EXPRESSION_SHA256
    assert statement["canonical_formal_target"]["statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert anchor["canonical_expression_sha256"] == EXPRESSION_SHA256
    assert anchor["canonical_statement_file_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_statement_sha256"] == EXPECTED_INPUTS["Statement.lean"]
    assert registry["frozen_against_anchor_audit_sha256"] == EXPECTED_INPUTS["anchor-audit.json"]
    assert registry["denominator_sha256"] == DENOMINATOR_SHA256
    assert graphs["registry_denominator_sha256"] == DENOMINATOR_SHA256
    assert proof_receipt["inputs"]["proof_sha256"] == EXPECTED_INPUTS["Proof.lean"]
    assert proof_receipt["inputs"]["obligation_tree_sha256"] == EXPECTED_INPUTS["ObligationTree.lean"]
    assert proof_receipt["inputs"]["obligation_registry_sha256"] == EXPECTED_INPUTS["obligation-registry.json"]
    assert proof_receipt["result"]["root_closed_by_kernel"] is True
    assert set(proof_receipt["proposed_closed_machine_obligation_ids"]) == PROVISIONAL_CLOSED
    assert set(proof_receipt["covered_obligation_ids"]) == COVERED
    assert proof_receipt["accepted_closed_obligation_ids"] == []
    assert set(proof_receipt["result"]["axioms"]) == EXPECTED_AXIOMS
    assert instance["lifecycle_mode"] == "planned"
    assert instance["root_vector"] == {"H": "H1", "M": "M3", "R": "R3"}
    assert instance["accepted_proof_state"] == instance["accepted_receipt_ids"] == []
    assert instance["audit_complete"] is instance["theorem_complete"] is False

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
        "import Proof", "import ObligationTree", "Proof.cayleyHamilton",
        "root_of_characteristicPolynomialTransport_and_matrixCayleyHamilton",
    ):
        assert forbidden not in differential, forbidden
    assert "exact Matrix.aeval_self_charpoly A" in differential

    manifest = load(LEAN_ROOT / "lake-manifest.json")
    mathlib_entry = next(row for row in manifest["packages"] if row["name"] == "mathlib")
    assert mathlib_entry["rev"] == MATHLIB_REVISION
    assert MATHLIB.resolve().is_dir(), "pinned mathlib artifact is unavailable"
    assert git("rev-parse", "HEAD", cwd=MATHLIB) == MATHLIB_REVISION
    assert git("rev-parse", "HEAD^{tree}", cwd=MATHLIB) == MATHLIB_TREE
    assert git("remote", "get-url", "origin", cwd=MATHLIB) == MATHLIB_REMOTE
    assert git("status", "--porcelain=v1", cwd=MATHLIB) == ""

    terminal_source = MATHLIB / "Mathlib/LinearAlgebra/Matrix/Charpoly/Basic.lean"
    terminal_olean = MATHLIB / ".lake/build/lib/lean/Mathlib/LinearAlgebra/Matrix/Charpoly/Basic.olean"
    assert sha256(terminal_source) == TERMINAL_SOURCE_SHA256
    assert git("rev-parse", "HEAD:Mathlib/LinearAlgebra/Matrix/Charpoly/Basic.lean", cwd=MATHLIB) == TERMINAL_SOURCE_BLOB
    body = terminal_source.read_bytes().splitlines(keepends=True)[210:231]
    assert hashlib.sha256(b"".join(body)).hexdigest() == TERMINAL_BODY_SHA256
    assert sha256(terminal_olean) == TERMINAL_OLEAN_SHA256
    assert sha256(MATHLIB / "LICENSE") == LICENSE_SHA256
    terminal_text = terminal_source.read_text(encoding="utf-8").split(
        "theorem aeval_self_charpoly", 1
    )[1].split("theorem charpoly_mul_comm'", 1)[0]
    assert prohibited.search(code_without_comments(terminal_text)) is None

    lean = run(["lake", "env", "which", "lean"], cwd=LEAN_ROOT).strip()
    lake = run(["lake", "env", "which", "lake"], cwd=LEAN_ROOT).strip()
    lean_version = run(["lake", "env", "lean", "--version"], cwd=LEAN_ROOT)
    assert "4.29.0" in lean_version and LEAN_COMMIT in lean_version
    lean_path = run(["lake", "env", "printenv", "LEAN_PATH"], cwd=LEAN_ROOT).strip()
    base_env = os.environ.copy()
    base_env.update({"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "TZ": "UTC"})
    with tempfile.TemporaryDirectory(prefix="m0041-validation-", dir=LEAN_ROOT) as tmp_name:
        tmp = Path(tmp_name)
        for name in ("Statement.lean", "ObligationTree.lean", "Proof.lean", "Validation.lean"):
            (tmp / name).write_bytes((HERE / name).read_bytes())
        statement_env = base_env.copy()
        statement_env["LEAN_PATH"] = lean_path
        run([lean, "-o", "Statement.olean", "Statement.lean"], cwd=tmp, env=statement_env)
        module_env = base_env.copy()
        module_env["LEAN_PATH"] = f"{tmp}:{lean_path}"
        obligation_output = run([lean, "-o", "ObligationTree.olean", "ObligationTree.lean"], cwd=tmp, env=module_env)
        proof_output = run([lean, "Proof.lean"], cwd=tmp, env=module_env)
        validation_output = run([lean, "Validation.lean"], cwd=tmp, env=module_env)

    proof_declarations = (
        "Stage1Instances.THM_M_0041.Proof.adjugateIdentity",
        "Stage1Instances.THM_M_0041.Proof.matrixPolynomialTransport",
        "Stage1Instances.THM_M_0041.Proof.rightFactorEvaluation",
        "Stage1Instances.THM_M_0041.Proof.scalarEvaluationTransport",
        "Stage1Instances.THM_M_0041.Proof.matrixCayleyHamiltonExpanded",
        "Stage1Instances.THM_M_0041.Proof.pinnedMatrixCayleyHamilton",
        "Stage1Instances.THM_M_0041.Proof.cayleyHamilton",
        "Stage1Instances.THM_M_0041.Proof.cayleyHamiltonExpanded",
        "Matrix.aeval_self_charpoly",
    )
    for declaration in proof_declarations:
        assert_axioms(proof_output, declaration)
    assert_axioms(validation_output, "Matrix.aeval_self_charpoly")
    assert_axioms(validation_output, "Stage1Instances.THM_M_0041.Validation.differentialCayleyHamilton")
    assert validation_output.count("Declarations are sorry-free!") == 2
    assert "sorryAx" not in obligation_output + proof_output + validation_output

    closure = graphs["closure_boundary"]
    assert closure["accepted_closed_obligations"] == []
    assert closure["root_closed"] is False
    assert set(closure["remaining_root_cut_set"]) == {
        "M0041-T-CHARPOLY", "M0041-A-MATHLIB-ANCHOR", "M0041-X-SOURCE",
        "M0041-S-FOUNDATION", "M0041-X-PROVENANCE", "M0041-X-TRUST",
        "M0041-X-READABLE", "M0041-X-WORKFLOW",
    }
    assert closure["audit_complete"] is closure["theorem_complete"] is False

    assert receipt["schema_version"] == "stage1-node-receipt/1.0"
    assert receipt["item_id"] == packet["item_id"] == ITEM
    assert receipt["theorem_id"] == THEOREM
    assert receipt["base_revision"] == packet["base_revision"] == BASE_REVISION
    assert receipt["base_tree"] == BASE_TREE
    assert receipt["support_state"] == "provisional_worker_selftest"
    assert receipt["release_grade"] is False and receipt["accepted"] is False
    for name, expected in EXPECTED_INPUTS.items():
        assert receipt["inputs"][name] == expected
    assert receipt["inputs"]["check_validation.py"] == sha256(HERE / "check_validation.py")
    assert receipt["target"] == {
        "canonical_declaration": "Stage1Instances.THM_M_0041.CayleyHamiltonTarget",
        "elaborated_expression_sha256": EXPRESSION_SHA256,
        "registry_denominator_sha256": DENOMINATOR_SHA256,
    }
    assert receipt["environment"]["lean_executable_sha256"] == sha256(Path(lean))
    assert receipt["environment"]["lake_executable_sha256"] == sha256(Path(lake))
    assert receipt["environment"]["platform"] == f"{platform.system()} {platform.machine()}"
    assert receipt["environment"]["mathlib_revision"] == MATHLIB_REVISION
    assert receipt["environment"]["mathlib_tree"] == MATHLIB_TREE
    assert receipt["provenance"]["terminal_source_sha256"] == TERMINAL_SOURCE_SHA256
    assert receipt["provenance"]["terminal_source_blob"] == TERMINAL_SOURCE_BLOB
    assert receipt["provenance"]["terminal_body_sha256"] == TERMINAL_BODY_SHA256
    assert receipt["provenance"]["terminal_olean_sha256"] == TERMINAL_OLEAN_SHA256
    assert receipt["provenance"]["license_sha256"] == LICENSE_SHA256
    for key in (
        "recipe_id", "cwd", "argv", "env_allowlist", "timeout_seconds",
        "network_policy", "network_enforcement", "expected_exit", "covered_obligation_ids",
        "covered_declarations",
    ):
        assert receipt["recipe"][key] == spec[key]
    assert receipt["result"]["exact_root_kernel_closed"] is True
    assert receipt["result"]["observed_axioms"] == [
        "propext", "Classical.choice", "Quot.sound"
    ]
    assert receipt["result"]["accepted_root_machine_debt"] == "M3"
    assert receipt["result"]["accepted_closed_obligations"] == []
    assert receipt["result"]["hermetic_release_gate"] == "fail_closed"
    assert receipt["result"]["independent_distinct_runner_gate"] == "fail_closed"
    assert receipt["result"]["audit_complete"] is receipt["result"]["theorem_complete"] is False
    assert receipt["first_failed_gate"] == "dependency.S56-M-0041-PROOF.master_acceptance"
    assert receipt["first_failed_release_gate"] == "S56-10.6-HERMETIC-COLD-BUILD"

    assert set(packet) == {
        "item_id", "changed_paths", "commands", "output_summary",
        "base_revision", "known_failures", "state",
    }
    assert packet["state"] == "[_]"
    assert set(packet["changed_paths"]) == set(receipt["changed_paths"]) == CHANGED_PATHS
    assert packet["known_failures"] == receipt["known_failures"]
    status = run(["git", "status", "--short", "--untracked-files=all"])
    actual_changed = {
        line[3:] for line in status.splitlines()
        if line[3:] != "Formalizations/Lean/.lake"
    }
    assert actual_changed == CHANGED_PATHS, (actual_changed, CHANGED_PATHS)

    for relative in CHANGED_PATHS:
        assert_text_hygiene(ROOT / relative)

    print("PASS THM-M-0041 narrow validation")
    print("PASS kernel replay: exact terminal, frozen composition, proof roots, and differential exact root elaborated")
    print("PASS trust observation: all checked declarations report only propext, Classical.choice, and Quot.sound")
    print("PASS local provenance: frozen hashes, terminal source/body/olean, clean mathlib pin, remote, and license agree")
    print("PASS hygiene: Lean assert_no_sorry plus a supplemental prohibited-construct scan passed")
    print("FAIL CLOSED authority: proof/master reconciliation is pending; accepted root remains H1/M3/R3")
    print("FAIL CLOSED hermetic release: shared warm .lake is not an empty-cache offline replay or complete TCB/SBOM archive")
    print("FAIL CLOSED independent release: differential probe used this worker/shared cache, not a distinct signed runner")
    print("audit_complete=false; theorem_complete=false")


if __name__ == "__main__":
    main()
